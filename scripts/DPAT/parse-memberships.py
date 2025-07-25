#!/usr/bin/env python3
# Author: Dylan Evans | fin3ss3g0d
r"""
Parse BloodHound/kerberoast-like membership lines and map users -> groups,
then scan an NTDS dump and emit one output file per group containing matched users.

Input line example:
  User .SERVICE@EXAMPLE.COM is MemberOf DOMAIN USERS@EXAMPLE.COM (Group/Base)

NTDS formats supported:
  1) DOMAIN\username:hash...
  2) username:RID:LMHASH:NTHASH:::

Usage:
  python groups_from_memberships.py \
    -m memberships.txt -d EXAMPLE.COM -n ntds_dump.txt -o out_dir --debug
"""

import argparse
import collections
import os
import re
import sys
from typing import Dict, Iterable, Match, Optional, Set

# ----------------------- Debug helper ----------------------- #
def dbg(enabled: bool, msg: str):
    if enabled:
        print(f"[DEBUG] {msg}")

# ----------------------- Regex helpers ---------------------- #
NTDS_PATTERNS = [
    # DOMAIN\user:rest
    re.compile(r"^(?P<domain>[^\\]+)\\(?P<user>[^:]+):(?P<rest>.+)$", re.IGNORECASE),
    # pwdump/secretsdump: user:RID:LM:NT:...
    re.compile(
        r"^(?P<user>[^:]+):(?P<rid>\d+):(?P<lm>[0-9A-Fa-f]{32}|\*):(?P<nt>[0-9A-Fa-f]{32}|\*):.*$",
        re.IGNORECASE
    )
]

def parse_ntds_line(line: str) -> Optional[Match[str]]:
    for pat in NTDS_PATTERNS:
        m = pat.match(line)
        if m:
            return m
    return None

# ----------------------- File parsing ----------------------- #
def read_memberships_file(path: str, domain: str, debug: bool, encoding: str = "cp1252") -> Dict[str, Set[str]]:
    """
    Parse file lines like:
      User .SERVICE@EXAMPLE.COM is MemberOf DOMAIN USERS@EXAMPLE.COM (Group/Base)
    Return dict: { username(lower): {group1, group2, ...} }
    """
    user_group_dict: Dict[str, Set[str]] = collections.defaultdict(set)

    dom_esc = re.escape(domain)
    pattern = re.compile(
        rf"^User\s+([\w.$-]+)@{dom_esc}\s+is\s+MemberOf\s+(.*?)@{dom_esc}\s+\((?:Group/Base|Base/Group)\)\s*$",
        re.IGNORECASE
    )

    try:
        with open(path, "r", encoding=encoding, errors="replace") as f:
            for i, raw in enumerate(f, 1):
                line = raw.strip()
                m = pattern.match(line)
                if not m:
                    dbg(debug, f"Line {i}: no match -> '{line}'")
                    continue
                user = m.group(1).lower()
                group = m.group(2).strip()
                user_group_dict[user].add(group)
                dbg(debug, f"Line {i}: user='{user}' group='{group}'")
    except FileNotFoundError:
        raise FileNotFoundError(f"Memberships file not found: {path}")
    except Exception as e:
        raise RuntimeError(f"Error reading memberships file '{path}': {e}")

    dbg(debug, f"user_group_dict size: {len(user_group_dict)}")
    return user_group_dict

def iter_ntds(path: str, debug: bool, encoding: str = "cp1252") -> Iterable[str]:
    try:
        with open(path, "r", encoding=encoding, errors="replace") as f:
            for i, line in enumerate(f, 1):
                if debug and i % 50000 == 0:
                    dbg(debug, f"Processed {i} NTDS lines...")
                yield line.rstrip("\n")
    except FileNotFoundError:
        raise FileNotFoundError(f"NTDS file not found: {path}")
    except Exception as e:
        raise RuntimeError(f"Error reading NTDS file '{path}': {e}")

# ------------------ Processing / Output --------------------- #
def sanitize_group_name(name: str) -> str:
    # For diagnostic prints only; file name is indexed
    return re.sub(r"[^\w .\-]", "_", name)

def process_ntds_file(ntds_path: str,
                      user_group_dict: Dict[str, Set[str]],
                      output_dir: str,
                      debug: bool,
                      encoding: str = "cp1252",
                      netbios: Optional[str] = None,
                      no_index: bool = False) -> None:
    """
    For each user in NTDS that appears in user_group_dict, append 'domain\\user'
    to that group's output file. Group files are named sequentially unless --no-index.
    """
    os.makedirs(output_dir, exist_ok=True)

    group_index = 1
    group_mapping: Dict[str, str] = {}  # group -> filepath

    for line in iter_ntds(ntds_path, debug, encoding):
        m = parse_ntds_line(line)
        if not m:
            dbg(debug, f"NTDS skipped (no match): '{line}'")
            continue

        gdict = m.groupdict()
        user = gdict.get("user", "").lower()

        if user not in user_group_dict:
            dbg(debug, f"Checking for match: {user} -> none")
            continue

        domain_from_line = (gdict.get("domain") or netbios or "").lower()
        dbg(debug, f"Match user '{user}' (domain '{domain_from_line}')")

        for group in user_group_dict[user]:
            if group not in group_mapping:
                if no_index:
                    fname = f"{sanitize_group_name(group)}.txt"
                else:
                    fname = f"group_{group_index:03}.txt"
                    group_index += 1

                fpath = os.path.join(output_dir, fname)
                group_mapping[group] = fpath
                with open(fpath, "w", encoding="utf-8", errors="replace") as gf:
                    gf.write(f"{group}\n")  # header
                dbg(debug, f"Created file for group '{group}' -> {fname}")

            out_path = group_mapping[group]
            with open(out_path, "a", encoding="utf-8", errors="replace") as out_f:
                if domain_from_line:
                    out_f.write(f"{domain_from_line}\\{user}\n")
                else:
                    out_f.write(f"{user}\n")

    # Summary
    print("\nGroup Index Mapping:")
    for group, file_path in group_mapping.items():
        print(f"{os.path.basename(file_path)} -> {group}")

# ---------------------- CLI plumbing ------------------------ #
def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Map users to groups from memberships file and match against NTDS dump.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        add_help=False
    )

    # Required (we'll manually validate)
    p.add_argument("-m", "--memberships-file", dest="memberships_file",
                   help="Path to memberships file (BloodHound-style lines)", required=False)
    p.add_argument("-d", "--domain", dest="domain",
                   help="FQDN domain (e.g., EXAMPLE.COM) used in the membership regex", required=False)
    p.add_argument("-n", "--ntds-file", dest="ntds_file",
                   help="Path to NTDS dump (DOMAIN\\user:hash or pwdump-style)", required=False)
    p.add_argument("-o", "--output-dir", dest="output_dir",
                   help="Directory to write per-group output files", required=False)

    # Optional
    p.add_argument("--netbios", dest="netbios",
                   help="NETBIOS/short domain to prefix when NTDS lines lack a domain (pwdump)", default=None)
    p.add_argument("--encoding", dest="encoding", default="cp1252",
                   help="Encoding for input files")
    p.add_argument("--debug", action="store_true",
                   help="Enable verbose debug output")
    p.add_argument("--no-index", action="store_true",
                   help="Name group files after the group instead of numbered files (unsafe chars replaced)")
    p.add_argument("-h", "--help", action="help", help="Show this help message and exit")

    return p

def validate_args(args: argparse.Namespace):
    required = ("memberships_file", "domain", "ntds_file", "output_dir")
    missing = [r for r in required if getattr(args, r) is None]
    if missing:
        prog = os.path.basename(sys.argv[0])
        print(f"Missing required arguments: {', '.join(missing)}\n", file=sys.stderr)
        print(f"Usage: python {prog} -m <memberships.txt> -d <DOMAIN> -n <ntds.txt> -o <output_dir> [--debug]\n", file=sys.stderr)
        print("Use -h/--help for all options.", file=sys.stderr)
        sys.exit(1)

# --------------------------- Main --------------------------- #
def main():
    parser = build_parser()
    args = parser.parse_args()
    validate_args(args)

    try:
        dbg(args.debug, f"Reading memberships file '{args.memberships_file}' for domain '{args.domain}'")
        user_group = read_memberships_file(args.memberships_file, args.domain, args.debug, args.encoding)

        if not user_group:
            print("No users/groups parsed from memberships file. Exiting.")
            sys.exit(0)

        dbg(args.debug, f"Processing NTDS file '{args.ntds_file}'")
        process_ntds_file(args.ntds_file, user_group, args.output_dir,
                          args.debug, args.encoding, args.netbios, args.no_index)

        print("\nDone.")
    except KeyboardInterrupt:
        print("\nInterrupted by user.")
        sys.exit(130)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(2)

if __name__ == "__main__":
    main()
