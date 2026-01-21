#!/usr/bin/env python3
import argparse
import base64
import datetime
import hashlib
import hmac
import io
import json
import os
import sys
import time
import zipfile
from typing import Any, Dict, List, Optional, Tuple, Union

import requests

MAX_RETRIES = 5

DEFAULT_BHQL_LATEST_JSON_URL = (
    "https://github.com/SpecterOps/BloodHoundQueryLibrary/releases/latest/download/Queries.json"
)
DEFAULT_BHQL_LATEST_ZIP_URL = (
    "https://github.com/SpecterOps/BloodHoundQueryLibrary/releases/latest/download/Queries.zip"
)


def build_signature(method: str, uri: str, body: bytes, token_key: str) -> Tuple[str, str]:
    """
    Build BloodHound CE HMAC signature headers.
    """
    digester = hmac.new(token_key.encode(), None, hashlib.sha256)
    digester.update(f"{method}{uri}".encode())

    digester = hmac.new(digester.digest(), None, hashlib.sha256)

    now = datetime.datetime.now().astimezone()
    date_header = now.isoformat("T")
    digester.update(date_header[:13].encode())

    digester = hmac.new(digester.digest(), None, hashlib.sha256)

    if body:
        digester.update(body)

    signature = base64.b64encode(digester.digest()).decode()
    return date_header, signature


def http_get_with_retries(
    url: str,
    timeout: int = 30,
    max_retries: int = 3,
    verify_tls: bool = True,
) -> bytes:
    """
    Download content from a URL with basic retry/backoff for transient failures.
    """
    headers = {"User-Agent": "cypherhound-bhql-importer/1.0"}
    last_exc: Optional[Exception] = None

    for attempt in range(1, max_retries + 1):
        try:
            print(f"[+] Downloading: {url} (attempt {attempt}/{max_retries})")
            resp = requests.get(url, headers=headers, timeout=timeout, verify=verify_tls)
            if resp.status_code >= 500 or resp.status_code in (408, 429):
                # transient-ish; retry
                print(f"[!] HTTP {resp.status_code} while downloading. Retrying...")
                time.sleep(min(2 ** attempt, 15))
                continue

            resp.raise_for_status()
            print(f"[+] Download complete: {len(resp.content)} bytes")
            return resp.content

        except Exception as exc:
            last_exc = exc
            print(f"[!] Download error: {exc}")
            time.sleep(min(2 ** attempt, 15))

    raise RuntimeError(f"Failed to download URL after {max_retries} attempts: {url}. Last error: {last_exc}")


def parse_queries_from_json_bytes(raw: bytes) -> List[Dict[str, Any]]:
    """
    Parse either:
      - a list[dict] at the top level (BHQL style)
      - OR {"queries": [...]} (common custom format)
    """
    try:
        obj = json.loads(raw.decode("utf-8"))
    except UnicodeDecodeError:
        # fallback, sometimes GitHub artifacts can still be UTF-8 but let's be defensive
        obj = json.loads(raw.decode("utf-8", errors="replace"))
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON format: {e}")

    if isinstance(obj, list):
        return obj
    if isinstance(obj, dict) and isinstance(obj.get("queries"), list):
        return obj["queries"]

    raise ValueError("Expected JSON to be either a list of query objects OR an object with a top-level 'queries' list.")


def parse_queries_from_zip_bytes(raw: bytes) -> List[Dict[str, Any]]:
    """
    Parse a zip containing one-or-many *.json files.

    BHQL's convert.py 'zip' mode writes each query as its own '<name>.json' (single object per file),
    but we'll support:
      - each file as a single dict
      - OR each file as a list of dicts (we'll extend)
    """
    queries: List[Dict[str, Any]] = []
    with zipfile.ZipFile(io.BytesIO(raw), "r") as zf:
        names = [n for n in zf.namelist() if n.lower().endswith(".json")]
        if not names:
            raise ValueError("ZIP contained no .json files to parse.")

        print(f"[+] ZIP contains {len(names)} JSON files")
        for name in names:
            try:
                data = zf.read(name)
                parsed = parse_queries_from_json_bytes(data)
                # parse_queries_from_json_bytes returns list[dict]
                queries.extend(parsed)
            except Exception as exc:
                print(f"[!] Failed to parse '{name}' in ZIP: {exc}")

    if not queries:
        raise ValueError("No queries were successfully parsed from the ZIP.")
    return queries


def load_queries_source(
    queries_file: Optional[str] = None,
    queries_url: Optional[str] = None,
    platforms_filter: Optional[List[str]] = None,
    verify_tls: bool = True,
    timeout: int = 30,
) -> List[Dict[str, str]]:
    """
    Load BHQL queries from either a local file or a URL (JSON or ZIP),
    filter by platform if requested, and flatten to the BHCE saved-query payload:
      { "name": ..., "description": ..., "query": ... }
    """
    if not queries_file and not queries_url:
        raise ValueError("You must supply either --queries-file or --queries-url (or use --bhql-latest/--bhql-latest-zip).")

    raw_data: List[Dict[str, Any]]

    # ----- Load raw query objects -----
    if queries_url:
        content = http_get_with_retries(queries_url, timeout=timeout, max_retries=3, verify_tls=verify_tls)
        if queries_url.lower().endswith(".zip"):
            raw_data = parse_queries_from_zip_bytes(content)
        else:
            raw_data = parse_queries_from_json_bytes(content)
        source_label = queries_url
    else:
        if not os.path.isfile(queries_file):  # type: ignore[arg-type]
            raise FileNotFoundError(f"Query file not found: {queries_file}")
        with open(queries_file, "rb") as fh:
            content = fh.read()

        if str(queries_file).lower().endswith(".zip"):
            raw_data = parse_queries_from_zip_bytes(content)
        else:
            raw_data = parse_queries_from_json_bytes(content)
        source_label = str(queries_file)

    if not isinstance(raw_data, list):
        raise ValueError("Expected a list of query objects after parsing input.")

    # ----- Filter + flatten -----
    flattened: List[Dict[str, str]] = []
    filter_active = bool(platforms_filter)
    skipped_platform = 0
    skipped_missing_query = 0

    for idx, entry in enumerate(raw_data):
        try:
            if not isinstance(entry, dict):
                print(f"[!] Skipping entry #{idx+1} (not an object)")
                continue

            entry_platforms = [str(p).lower() for p in entry.get("platforms", []) if p is not None]
            if filter_active and not any(p in entry_platforms for p in platforms_filter or []):
                skipped_platform += 1
                continue

            query_text = entry.get("query")
            if not query_text:
                skipped_missing_query += 1
                continue

            name = entry.get("name", f"Unnamed Query {idx+1}")
            category = entry.get("category", "Uncategorized")
            description = entry.get("description") or f"{name} - {category}"

            flattened.append(
                {
                    "name": str(name),
                    "description": str(description),
                    "query": str(query_text),
                }
            )
        except Exception as exc:
            print(f"[!] Error processing entry #{idx+1}: {exc}")

    print(
        f"[+] Loaded {len(flattened)} queries from {source_label}"
        + (" after platform filtering" if filter_active else "")
    )
    if filter_active:
        print(f"    [-] Skipped {skipped_platform} queries (platform mismatch)")
    if skipped_missing_query:
        print(f"    [-] Skipped {skipped_missing_query} entries (missing 'query' field)")

    return flattened


def submit_query_with_retries(url: str, headers: Dict[str, str], body: bytes, query_name: str, timeout: int = 30) -> None:
    """
    Submit one saved query with rate-limit and transient error retry handling.
    """
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = requests.post(url=url, headers=headers, data=body, timeout=timeout)
        except requests.RequestException as exc:
            wait_time = min(2 ** attempt, 20)
            print(f"[!] Request error submitting '{query_name}': {exc} (attempt {attempt}/{MAX_RETRIES}) -> sleeping {wait_time}s")
            time.sleep(wait_time)
            continue

        # Success-ish or non-rate-limit failures: print and return
        if response.status_code != 429:
            print(f"    Status: {response.status_code} - {response.text}")
            return

        # Rate limited
        retry_after = response.headers.get("Retry-After")
        if retry_after:
            try:
                wait_time = int(retry_after)
            except ValueError:
                wait_time = min(2 ** attempt, 20)
            print(f"[!] 429 received. Retry-After: {wait_time}s (Attempt {attempt}/{MAX_RETRIES})")
        else:
            wait_time = min(2 ** attempt, 20)
            print(f"[!] 429 received. No Retry-After header. Waiting {wait_time}s (Attempt {attempt}/{MAX_RETRIES})")

        time.sleep(wait_time)

    print(f"[X] Failed to submit query '{query_name}' after {MAX_RETRIES} retries due to rate limiting/transient errors.")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Import SpecterOps BloodHoundQueryLibrary queries into BloodHound Community Edition via API."
    )
    parser.add_argument("--token-id", required=True, help="API token ID")
    parser.add_argument("--token-key", required=True, help="API token key")
    parser.add_argument("--base-url", default="http://127.0.0.1:8080", help="BloodHound API base URL (default: http://127.0.0.1:8080)")

    src = parser.add_mutually_exclusive_group(required=True)
    src.add_argument("--queries-file", help="Path to Queries.json or Queries.zip on disk")
    src.add_argument("--queries-url", help="URL to Queries.json or Queries.zip")
    src.add_argument("--bhql-latest", action="store_true", help=f"Use BHQL latest release Queries.json ({DEFAULT_BHQL_LATEST_JSON_URL})")
    src.add_argument("--bhql-latest-zip", action="store_true", help=f"Use BHQL latest release Queries.zip ({DEFAULT_BHQL_LATEST_ZIP_URL})")

    parser.add_argument(
        "--platforms",
        nargs="+",
        metavar="PLATFORM",
        help='Import only queries that list one of these platform strings (case-insensitive), e.g. --platforms "Active Directory" "Azure".',
    )
    parser.add_argument("--dry-run", action="store_true", help="Parse/filter queries but do not submit them to BloodHound CE.")
    parser.add_argument("--limit", type=int, default=0, help="Only submit the first N queries after filtering (0 = no limit).")
    parser.add_argument("--timeout", type=int, default=30, help="HTTP timeout in seconds for downloads and API calls (default: 30).")
    parser.add_argument("--insecure", action="store_true", help="Disable TLS certificate verification for URL downloads (not recommended).")

    args = parser.parse_args()

    platform_filters = [p.lower() for p in (args.platforms or [])]
    verify_tls = not args.insecure

    if args.bhql_latest:
        queries_url = DEFAULT_BHQL_LATEST_JSON_URL
        queries_file = None
    elif args.bhql_latest_zip:
        queries_url = DEFAULT_BHQL_LATEST_ZIP_URL
        queries_file = None
    else:
        queries_url = args.queries_url
        queries_file = args.queries_file

    try:
        queries = load_queries_source(
            queries_file=queries_file,
            queries_url=queries_url,
            platforms_filter=platform_filters if platform_filters else None,
            verify_tls=verify_tls,
            timeout=args.timeout,
        )

        if args.limit and args.limit > 0:
            print(f"[+] Limiting to first {args.limit} queries")
            queries = queries[: args.limit]

        if args.dry_run:
            print("[+] Dry-run enabled. No queries will be submitted.")
            print(f"[+] Final query count: {len(queries)}")
            return

        uri = "/api/v2/saved-queries"
        method = "POST"
        url = args.base_url.rstrip("/") + uri

        for query in queries:
            body = json.dumps(query).encode()
            request_date, signature = build_signature(method, uri, body, args.token_key)

            headers = {
                "Authorization": f"bhesignature {args.token_id}",
                "RequestDate": request_date,
                "Signature": signature,
                "Content-Type": "application/json",
                "User-Agent": "cypherhound-bhql-importer/1.0",
            }

            print(f"[+] Submitting query: {query.get('name')}")
            submit_query_with_retries(url, headers, body, str(query.get("name")), timeout=args.timeout)

    except Exception as e:
        print(f"[!] Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
