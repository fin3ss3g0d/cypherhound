import requests
import json
import base64
import hmac
import hashlib
import datetime
import argparse
import sys
import os
import time

MAX_RETRIES = 5

def build_signature(method: str, uri: str, body: bytes, token_key: str) -> (str, str):
    digester = hmac.new(token_key.encode(), None, hashlib.sha256)
    digester.update(f'{method}{uri}'.encode())

    digester = hmac.new(digester.digest(), None, hashlib.sha256)

    now = datetime.datetime.now().astimezone()
    date_header = now.isoformat('T')
    digester.update(date_header[:13].encode())

    digester = hmac.new(digester.digest(), None, hashlib.sha256)

    if body:
        digester.update(body)

    signature = base64.b64encode(digester.digest()).decode()
    return date_header, signature

def load_queries(file_path: str, platforms_filter: list[str] | None = None):
    """
    Read the SpecterOps query-library JSON and return only the queries whose
    'platforms' list intersects with `platforms_filter` (case-insensitive).

    Args:
        file_path:  Path to the master queries JSON.
        platforms_filter:  List of platform strings (lower-cased).  If None or
                           empty, no filtering is applied.

    Returns:
        List[dict] with keys: name, description, query
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"Query file not found: {file_path}")

    with open(file_path, "r") as fh:
        try:
            raw_data = json.load(fh)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON format: {e}")

    if not isinstance(raw_data, list):
        raise ValueError("Expected a list of query objects at top level")

    flattened = []
    filter_active = bool(platforms_filter)
    skipped_platform = 0
    for idx, entry in enumerate(raw_data):
        try:
            # ----- platform gating ------------------------------------------------
            entry_platforms = [p.lower() for p in entry.get("platforms", [])]
            if filter_active and not any(p in entry_platforms for p in platforms_filter):
                skipped_platform += 1
                continue

            query_text = entry.get("query")
            if not query_text:
                print(f"[!] Skipping entry #{idx+1} (missing 'query' field)")
                continue

            name        = entry.get("name", f"Unnamed Query {idx+1}")
            category    = entry.get("category", "Uncategorized")
            description = entry.get("description") or f"{name} - {category}"

            flattened.append({
                "name":        name,
                "description": description,
                "query":       query_text
            })

        except Exception as exc:
            print(f"[!] Error processing entry #{idx+1}: {exc}")

    print(f"[+] Loaded {len(flattened)} queries from {file_path}"
          f"{' after platform filtering' if filter_active else ''}")
    if skipped_platform and filter_active:
        print(f"    [-] Skipped {skipped_platform} queries (platform mismatch)")
    return flattened

def submit_query_with_retries(url, headers, body, query_name):
    for attempt in range(1, MAX_RETRIES + 1):
        response = requests.post(url=url, headers=headers, data=body)

        if response.status_code != 429:
            print(f"    Status: {response.status_code} - {response.text}")
            return

        retry_after = response.headers.get("Retry-After")
        if retry_after:
            wait_time = int(retry_after)
            print(f"[!] 429 received. Retry-After: {wait_time}s (Attempt {attempt}/{MAX_RETRIES})")
        else:
            wait_time = 2 ** attempt  # Exponential backoff
            print(f"[!] 429 received. No Retry-After header. Waiting {wait_time}s (Attempt {attempt}/{MAX_RETRIES})")

        time.sleep(wait_time)

    print(f"[X] Failed to submit query '{query_name}' after {MAX_RETRIES} retries due to rate limiting.")

def main():
    parser = argparse.ArgumentParser(description="Submit BloodHound queries via API from Queries.json")
    parser.add_argument("--token-id", required=True, help="API token ID")
    parser.add_argument("--token-key", required=True, help="API token key")
    parser.add_argument("--queries-file", required=True, help="Path to JSON file containing custom queries")
    parser.add_argument("--base-url", default="http://127.0.0.1:8080", help="BloodHound API base URL")
    parser.add_argument(
        "--platforms",
        nargs="+",                   # allow 1 + values:  --platforms "Active Directory" "Azure AD"
        metavar="PLATFORM",
        help="Import only queries that list one of these platform strings "
             "(case-insensitive).  If omitted, all queries are imported."
    )

    args = parser.parse_args()

    # Normalize platform filters to lower-case once
    platform_filters = [p.lower() for p in (args.platforms or [])]

    try:
        queries = load_queries(args.queries_file, platform_filters if platform_filters else None)
        
        for query in queries:
            body = json.dumps(query).encode()
            uri = "/api/v2/saved-queries"
            method = "POST"
            url = args.base_url + uri

            request_date, signature = build_signature(method, uri, body, args.token_key)

            headers = {
                "Authorization": f"bhesignature {args.token_id}",
                "RequestDate": request_date,
                "Signature": signature,
                "Content-Type": "application/json",
                "User-Agent": "bhe-python-sdk 0001",
            }

            print(f"[+] Submitting query: {query['name']}")
            submit_query_with_retries(url, headers, body, query['name'])

    except Exception as e:
        print(f"[!] Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
