#!/usr/bin/env python3
"""
bh_query_converter.py

Convert terminal-style Cypher queries (YAML) into BloodHound Community Edition
UI import JSON.

Rules:
- If the Cypher contains 'shortestPath' (case-insensitive), copy the query verbatim.
- If the RETURN clause yields a single ".name", convert to returning the node as 'result':
    ... RETURN n AS result ...
- If the RETURN clause yields two or more ".name" values OR there is a relationship
  pattern in MATCH, convert to a path query:
    - Ensure MATCH binds a path variable (p) to the first relationship pattern
      (heuristic: insert "p=" after the first MATCH if no path var exists).
    - RETURN p
- Preserve WHERE/ORDER BY when present.
- Description becomes: "<desc> - <GroupTitleCase>"
- Name becomes: "<desc>"

Limitations (by design, to keep it safe and predictable):
- Uses regex/heuristics, not a full Cypher parser. Complex multi-MATCH patterns are best-effort.
- If we cannot confidently detect a node var for single-node style, we fall back to "n".
"""

import argparse
import json
import os
import re
import sys
from typing import Any, Dict, List, Tuple, Set

try:
    import yaml  # PyYAML
except ImportError as e:
    sys.stderr.write(
        "[!] Missing dependency: PyYAML\n"
        "    pip install pyyaml\n"
    )
    sys.exit(1)


def _normalize_group(s: str) -> str:
    return re.sub(r"\s+", " ", s.strip()).lower()


def _parse_groups_arg(raw_groups: List[str] | None) -> Set[str]:
    """
    Accept multiple -g/--groups values; each value may be comma-separated.
    Returns a normalized (lowercased) set. Empty set means 'no filtering'.
    """
    if not raw_groups:
        return set()
    out: Set[str] = set()
    for chunk in raw_groups:
        for item in chunk.split(","):
            g = item.strip()
            if g:
                out.add(_normalize_group(g))
    return out


def dbg(enabled: bool, msg: str):
    if enabled:
        print(f"[DEBUG] {msg}", flush=True)


def load_yaml(path: str, include_groups: Set[str], debug: bool) -> Dict[str, Any]:
    """
    Load YAML and (optionally) keep only queries whose 'group' is in include_groups (case-insensitive).
    If include_groups is empty, no filtering is applied.
    Returns a dict with a single 'queries' key for compatibility with downstream code.
    """
    if not os.path.isfile(path):
        raise FileNotFoundError(f"YAML input not found: {path}")
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        if not isinstance(data, dict) or "queries" not in data or not isinstance(data["queries"], list):
            raise ValueError("YAML must contain a top-level 'queries' list.")

        all_q = data["queries"]
        dbg(debug, f"Loaded YAML with {len(all_q)} total queries.")

        filtered: List[Dict[str, Any]] = []
        for idx, q in enumerate(all_q, 1):
            if not isinstance(q, dict):
                if debug:
                    print(f"[DEBUG] Skipping query #{idx}: not a mapping/object.", flush=True)
                continue

            grp_raw = str(q.get("group", "")).strip()
            grp_norm = _normalize_group(grp_raw) if grp_raw else ""

            if include_groups:
                if not grp_norm:
                    if debug:
                        print(f"[DEBUG] Skipping query #{idx}: no 'group' present; filtering active.", flush=True)
                    continue
                if grp_norm not in include_groups:
                    if debug:
                        print(f"[DEBUG] Skipping query #{idx}: group={grp_raw!r} not in include set.", flush=True)
                    continue

            filtered.append(q)

        if include_groups and debug:
            want = ", ".join(sorted(include_groups))
            print(f"[DEBUG] Filter groups: {want}", flush=True)
        if debug:
            print(f"[DEBUG] Keeping {len(filtered)} queries after filtering.", flush=True)
        if not filtered:
            print("[!] No queries remained after filtering.", file=sys.stderr)

        return {"queries": filtered}

    except yaml.YAMLError as e:
        raise ValueError(f"Invalid YAML: {e}") from e


def split_cypher_parts(cypher: str) -> Tuple[str, str, str]:
    """
    Return (pre_return, return_expr, order_tail)
    - pre_return: everything before RETURN
    - return_expr: expression inside RETURN ... (until ORDER BY or end)
    - order_tail: the ORDER BY ... tail (or '')
    """
    text = cypher.strip().rstrip(";")
    lower = text.lower()

    iret = lower.find(" return ")
    if iret == -1:
        # Also handle linebreak then RETURN
        m = re.search(r"\breturn\b", lower, re.IGNORECASE)
        if not m:
            raise ValueError("Cypher query missing RETURN clause.")
        iret = m.start()

    pre = text[:iret].rstrip()
    post = text[iret+6:].lstrip()  # after 'RETURN'

    m_ord = re.search(r"\border\s+by\b", post, re.IGNORECASE)
    if m_ord:
        ret_expr = post[:m_ord.start()].strip().rstrip(",")
        order_tail = post[m_ord.start():].strip()
    else:
        ret_expr = post.strip().rstrip(",")
        order_tail = ""

    return pre, ret_expr, order_tail


def has_shortest_path(cypher: str) -> bool:
    return "shortestpath" in cypher.lower()


def count_name_refs(return_expr: str) -> int:
    return len(re.findall(r"\b\w+\.name\b", return_expr))


def extract_first_name_var(return_expr: str) -> str:
    m = re.search(r"\b([A-Za-z_]\w*)\.name\b", return_expr)
    return m.group(1) if m else ""


def extract_orderby_var(order_tail: str) -> str:
    m = re.search(r"\border\s+by\s+([A-Za-z_]\w*)\.name\b", order_tail, re.IGNORECASE)
    return m.group(1) if m else ""


def has_relationship_pattern(pre_return: str) -> bool:
    # crude but robust enough: look for )-[  or ]-(  before RETURN
    return bool(re.search(r"\)-\s*\[", pre_return)) or bool(re.search(r"\]-\s*\(", pre_return))


def has_path_var_in_match(pre_return: str) -> bool:
    # MATCH p=...
    return bool(re.search(r"\bmatch\s+[A-Za-z_]\w*\s*=", pre_return, re.IGNORECASE))


def ensure_path_binding(pre_return: str, debug: bool) -> str:
    """
    If there's no explicit path var in the first MATCH and we see a relationship,
    insert 'p=' after the first MATCH. This is a heuristic that works well for
    1-pattern MATCHes and many simple multi-pattern cases.
    """
    if has_path_var_in_match(pre_return):
        return pre_return

    if not has_relationship_pattern(pre_return):
        return pre_return

    # Insert 'p=' after first MATCH keyword
    new_pre = re.sub(r"\bMATCH\s+", "MATCH p=", pre_return, count=1, flags=re.IGNORECASE)
    if new_pre == pre_return:
        dbg(debug, "Failed to inject path variable after MATCH (no change).")
    else:
        dbg(debug, "Injected 'p=' into first MATCH to bind path.")
    return new_pre


def to_ui_single_node(pre_return: str, return_expr: str, order_tail: str, debug: bool) -> str:
    var = extract_first_name_var(return_expr)
    if not var:
        # If we cannot find it in RETURN, try ORDER BY; else default to 'n'
        var = extract_orderby_var(order_tail) or "n"
        dbg(debug, f"Could not find a '.name' var in RETURN; using '{var}' from ORDER BY or fallback.")

    parts = [pre_return, f"RETURN {var} AS result"]
    if order_tail:
        parts.append(order_tail)
    new_q = "\n".join(parts)
    dbg(debug, f"Single-node UI query produced; node var='{var}'.")
    return new_q


def to_ui_relationship(pre_return: str, order_tail: str, debug: bool) -> str:
    pre_with_p = ensure_path_binding(pre_return, debug)
    parts = [pre_with_p, "RETURN p"]
    if order_tail:
        parts.append(order_tail)
    new_q = "\n".join(parts)
    dbg(debug, "Relationship/path UI query produced (RETURN p).")
    return new_q


def normalize_semicolon(q: str) -> str:
    return q.strip().rstrip(";")  # BH UI doesn't need ';'


def transform_one(entry: Dict[str, Any], debug: bool) -> Dict[str, str]:
    desc = (entry.get("desc") or "").strip() or "Unnamed Query"
    group = (entry.get("group") or "General").strip()
    cypher = (entry.get("cypher") or "").strip()

    if not cypher:
        raise ValueError(f"Query '{desc}' has empty 'cypher'.")

    if has_shortest_path(cypher):
        # Pass-through
        new_cypher = normalize_semicolon(cypher)
        dbg(debug, f"'{desc}': shortestPath detected; copying query verbatim.")
    else:
        pre, ret_expr, order_tail = split_cypher_parts(cypher)
        names = count_name_refs(ret_expr)
        rel = has_relationship_pattern(pre)

        dbg(debug, f"'{desc}': names_in_RETURN={names}, has_relationship_in_MATCH={rel}")

        if names <= 1 and not rel:
            new_cypher = to_ui_single_node(pre, ret_expr, order_tail, debug)
        else:
            new_cypher = to_ui_relationship(pre, order_tail, debug)

        new_cypher = normalize_semicolon(new_cypher)

    return {
        "name": desc,
        "description": f"{desc} - {group.title()}",
        "query": new_cypher,
    }


def convert(in_yaml: str, out_json: str, indent: int, include_groups: Set[str], debug: bool) -> int:
    data = load_yaml(in_yaml, include_groups, debug)
    results: List[Dict[str, str]] = []
    errors = 0

    for i, q in enumerate(data["queries"], 1):
        try:
            if not isinstance(q, dict):
                raise ValueError("Each item under 'queries' must be a mapping/object.")
            converted = transform_one(q, debug)
            results.append(converted)
            dbg(debug, f"Converted [{i}]: {converted['name']}")
        except Exception as e:
            errors += 1
            sys.stderr.write(f"[!] Failed to convert query #{i}: {e}\n")

    payload = {"queries": results}

    try:
        with open(out_json, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=indent, ensure_ascii=False)
        print(f"[+] Wrote {len(results)} queries to: {out_json}")
        if errors:
            print(f"[!] Completed with {errors} error(s). See stderr for details.")
    except OSError as e:
        sys.stderr.write(f"[!] Could not write JSON output: {e}\n")
        return 2

    return 0 if errors == 0 else 1


def main():
    parser = argparse.ArgumentParser(
        description="Convert terminal-style BloodHound Cypher YAML to BH CE UI JSON.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("-i", "--input", required=True, help="Path to input YAML file")
    parser.add_argument("-o", "--output", default="bloodhound_queries.json", help="Path to output JSON file")
    parser.add_argument("--indent", type=int, default=2, help="JSON indentation")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable verbose debug prints")
    parser.add_argument(
        "-g", "--groups",
        action="append",
        help="Group(s) to include; may be comma-separated or repeated. Example: -g General -g 'Kerberoasting, ACLs'"
    )

    args = parser.parse_args()

    if not args.input:
        parser.print_help(sys.stderr)
        sys.exit(2)

    try:
        include_groups = _parse_groups_arg(args.groups)
        if args.debug and include_groups:
            print(f"[DEBUG] Include groups (normalized): {sorted(include_groups)}", flush=True)

        rc = convert(args.input, args.output, args.indent, include_groups, args.debug)
        sys.exit(rc)
    except Exception as e:
        sys.stderr.write(f"[!] Fatal: {e}\n")
        sys.exit(2)


if __name__ == "__main__":
    main()
