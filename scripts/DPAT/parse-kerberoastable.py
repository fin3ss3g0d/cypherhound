#!/usr/bin/env python3
"""
AD Kerberoast ↔ NTDS.dit matcher
Author: Dylan Evans | fin3ss3g0d
"""

import argparse
import os
import re
import sys
from typing import Set, Iterable

NTDS_PATTERNS = [
    re.compile(r"^(?P<domain>[^\\]+)\\(?P<user>[^:]+):(?P<rest>.+)$", re.IGNORECASE),         # DOMAIN\user:...
    re.compile(r"^(?P<user>[^:]+):(?P<rid>\d+):(?P<lm>[0-9A-Fa-f]{32}|\*):(?P<nt>[0-9A-Fa-f]{32}|\*):.*$", re.IGNORECASE)  # pwdump
]

def print_debug(enabled: bool, msg: str):
    if enabled:
        print(f"[DEBUG] {msg}")

def read_kerberoast_file(path: str, domain: str, debug: bool, encoding: str = "cp1252") -> Set[str]:
    """
    Parse kerberoast file lines like:
      User .SERVICE@EXAMPLE.COM is kerberoastable
    Return a set of usernames (lowercased).
    """
    usernames = set()
    # Build case-insensitive regex
    # Allow leading dot, $, digits, underscore, dash, etc. before @domain
    # Example capture: ".SERVICE"
    dom_esc = re.escape(domain)
    pattern = re.compile(rf"^User\s+([A-Za-z0-9._$-]+)@{dom_esc}\s+is\s+kerberoastable\s*$", re.IGNORECASE)

    try:
        with open(path, "r", encoding=encoding, errors="replace") as f:
            for i, line in enumerate(f, 1):
                line = line.strip()
                m = pattern.match(line)
                if m:
                    user = m.group(1).lower()
                    usernames.add(user)
                    print_debug(debug, f"Line {i}: captured kerberoastable user '{user}'")
                else:
                    print_debug(debug, f"Line {i}: no match -> '{line}'")
    except FileNotFoundError:
        raise FileNotFoundError(f"Kerberoast file not found: {path}")
    except Exception as e:
        raise RuntimeError(f"Error reading kerberoast file '{path}': {e}")

    print_debug(debug, f"Total kerberoastable usernames found: {len(usernames)}")
    return usernames

def iter_ntds_lines(path: str, debug: bool, encoding: str = "cp1252") -> Iterable[str]:
    """
    Yield lines from NTDS dump safely.
    """
    try:
        with open(path, "r", encoding=encoding, errors="replace") as f:
            for i, line in enumerate(f, 1):
                if debug and i % 50000 == 0:
                    print_debug(debug, f"Processed {i} lines of NTDS so far...")
                yield line.rstrip("\n")
    except FileNotFoundError:
        raise FileNotFoundError(f"NTDS file not found: {path}")
    except Exception as e:
        raise RuntimeError(f"Error reading NTDS file '{path}': {e}")

def parse_ntds_line(line: str):
    for pat in NTDS_PATTERNS:
        m = pat.match(line)
        if m:
            return m
    return None

def match_ntds(ntds_path: str,
               kerb_users: Set[str],
               output_path: str,
               debug: bool,
               domain: str,
               encoding: str = "cp1252") -> int:
    """
    Match usernames from kerb_users against NTDS dump.
    Write matches to output_path.
    Returns number of matches written.
    """
    
    matches = 0
    try:
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    except Exception as e:
        raise RuntimeError(f"Cannot create output directory: {e}")

    with open(output_path, "w", encoding="utf-8", errors="replace") as out_f:
        for line in iter_ntds_lines(ntds_path, debug, encoding):
            m = parse_ntds_line(line)
            if not m:
                print_debug(debug, f"NTDS line skipped (no regex match): '{line}'")
                continue

            user = m.group("user").lower()
            # domain may not exist in 2nd pattern; use get with default
            dom = (m.groupdict().get("domain") or "").lower()

            # Optional: ensure domain match if you want (NETBIOS vs arg)
            # We rely primarily on username; but we can check arg domain if needed.
            # We'll do a soft check: only if domain arg matches (case-insensitive), else still allow?
            # Following user's instruction: check based on usernames, but they supplied domain for regex matching.
            if user in kerb_users:
                matches += 1
                out_f.write(line + "\n")
                print_debug(debug, f"Match -> wrote full NTDS line for '{user}'")
    print_debug(debug, f"Total NTDS matches written: {matches}")
    return matches

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Match kerberoastable usernames against an NTDS.dit dump file",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        add_help=False  # we'll add custom help to satisfy 'show help when missing args'
    )

    # Required
    parser.add_argument("-k", "--kerb-file", dest="kerb_file", help="Path to Kerberoast output file", required=False)
    parser.add_argument("-n", "--ntds-file", dest="ntds_file", help="Path to NTDS dump file", required=False)
    parser.add_argument("-d", "--domain",    dest="domain",    help="Domain (e.g., EXAMPLE.COM) for regex matching", required=False)
    parser.add_argument("-o", "--output",    dest="output",    help="Path to write matches", required=False)

    # Optional
    parser.add_argument("--encoding", default="cp1252",
                        help="File encoding to use when reading input files")
    parser.add_argument("--debug", action="store_true",
                        help="Enable verbose debug output")
    parser.add_argument("-h", "--help", action="help", help="Show this help message and exit")
    return parser

def validate_args(args: argparse.Namespace):
    missing = [name for name in ("kerb_file", "ntds_file", "domain", "output") if getattr(args, name) is None]
    if missing:
        prog = os.path.basename(sys.argv[0])
        print(f"Missing required arguments: {', '.join(missing)}\n", file=sys.stderr)
        print(f"Usage: python {prog} -k <kerberoast_file> -d <domain> -n <ntds_file> -o <output_file> [--full-lines] [--debug]\n", file=sys.stderr)
        print("Use -h/--help for detailed options.", file=sys.stderr)
        sys.exit(1)

def main():
    parser = build_parser()
    args = parser.parse_args()
    validate_args(args)

    try:
        print_debug(args.debug, f"Reading kerberoast file '{args.kerb_file}' for domain '{args.domain}'")
        kerb_users = read_kerberoast_file(args.kerb_file, args.domain, args.debug, args.encoding)

        if not kerb_users:
            print("No kerberoastable usernames found. Nothing to match. Exiting.")
            sys.exit(0)

        print_debug(args.debug, f"Scanning NTDS file '{args.ntds_file}' for matches...")
        count = match_ntds(args.ntds_file, kerb_users, args.output, args.debug,
                           domain=args.domain, encoding=args.encoding)

        print(f"Done. Wrote {count} matching lines to '{args.output}'.")
    except KeyboardInterrupt:
        print("\nInterrupted by user.")
        sys.exit(130)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(2)

if __name__ == "__main__":
    main()
