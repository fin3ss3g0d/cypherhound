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

def load_queries(file_path: str):
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"Query file not found: {file_path}")

    with open(file_path, "r") as file:
        raw_data = json.load(file)

    flattened_queries = []
    for entry in raw_data.get("queries", []):
        name = entry.get("name", "Unnamed Query")
        category = entry.get("category", "Uncategorized")
        final_queries = [q for q in entry.get("queryList", []) if q.get("final", False)]

        for idx, q in enumerate(final_queries):
            query_name = name if len(final_queries) == 1 else f"{name} ({idx + 1})"
            flattened_queries.append({
                "name": query_name,
                "description": f"{name} - {category}",
                "query": q["query"]
            })

    print(f"[+] Loaded {len(flattened_queries)} final queries from {file_path}")
    return flattened_queries

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
    parser = argparse.ArgumentParser(description="Submit custom BloodHound queries via API")
    parser.add_argument("--token-id", required=True, help="API token ID")
    parser.add_argument("--token-key", required=True, help="API token key")
    parser.add_argument("--queries-file", required=True, help="Path to BH Legacy JSON file containing custom queries")
    parser.add_argument("--base-url", default="http://127.0.0.1:8080", help="BloodHound API base URL")

    args = parser.parse_args()

    try:
        queries = load_queries(args.queries_file)

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
