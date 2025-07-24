import requests
import json
import base64
import hmac
import hashlib
import datetime
import argparse
import sys
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

def get_all_saved_query_ids(base_url, token_id, token_key):
    saved_query_ids = []
    skip = 0
    limit = 100
    uri = "/api/v2/saved-queries"
    method = "GET"

    print("[+] Retrieving saved queries...")

    while True:
        query_string = f"?skip={skip}&limit={limit}"
        full_uri = uri + query_string
        url = base_url + full_uri

        request_date, signature = build_signature(method, full_uri, b'', token_key)
        headers = {
            "Authorization": f"bhesignature {token_id}",
            "RequestDate": request_date,
            "Signature": signature,
            "Accept": "application/json",
            "User-Agent": "bhe-python-sdk 0001"
        }

        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"[!] Failed to retrieve saved queries: {response.status_code} - {response.text}")
            break

        data = response.json()
        chunk = data.get("data", [])
        saved_query_ids.extend([q["id"] for q in chunk])

        print(f"    Retrieved {len(chunk)} queries (skip={skip})")

        if len(chunk) < limit:
            break  # End of pagination

        skip += limit

    print(f"[+] Total saved queries to delete: {len(saved_query_ids)}")
    return saved_query_ids

def delete_saved_query(base_url, token_id, token_key, query_id):
    uri = f"/api/v2/saved-queries/{query_id}"
    url = base_url + uri
    method = "DELETE"
    body = b''

    for attempt in range(1, MAX_RETRIES + 1):
        request_date, signature = build_signature(method, uri, body, token_key)
        headers = {
            "Authorization": f"bhesignature {token_id}",
            "RequestDate": request_date,
            "Signature": signature,
            "Accept": "text/plain",
            "User-Agent": "bhe-python-sdk 0001"
        }

        response = requests.delete(url, headers=headers)

        if response.status_code == 204:
            print(f"    [✓] Deleted query ID {query_id}")
            return True
        elif response.status_code == 429:
            wait = int(response.headers.get("Retry-After", 2 ** attempt))
            print(f"    [!] Rate-limited on ID {query_id}, retrying in {wait}s (Attempt {attempt}/{MAX_RETRIES})")
            time.sleep(wait)
        elif 500 <= response.status_code < 600:
            print(f"    [!] Server error {response.status_code} on ID {query_id}, retrying in 2s (Attempt {attempt}/{MAX_RETRIES})")
            time.sleep(2)
        else:
            print(f"    [X] Failed to delete query ID {query_id}: {response.status_code} - {response.text}")
            return False

    print(f"    [X] Giving up on query ID {query_id} after {MAX_RETRIES} attempts.")
    return False

def main():
    parser = argparse.ArgumentParser(description="Purge all imported BloodHound CE saved queries.")
    parser.add_argument("--token-id", required=True, help="API token ID")
    parser.add_argument("--token-key", required=True, help="API token key")
    parser.add_argument("--base-url", default="http://127.0.0.1:8080", help="BloodHound API base URL")

    args = parser.parse_args()

    try:
        query_ids = get_all_saved_query_ids(args.base_url, args.token_id, args.token_key)

        if not query_ids:
            print("[+] No saved queries to delete.")
            return

        print(f"[+] Starting deletion of {len(query_ids)} queries...")
        for qid in query_ids:
            delete_saved_query(args.base_url, args.token_id, args.token_key, qid)

        print("[+] Deletion process complete.")

    except Exception as e:
        print(f"[!] Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
