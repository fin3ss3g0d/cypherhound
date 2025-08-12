#!/usr/bin/env python3
"""
dedupe_by_description.py
========================
Interactively resolve duplicate descriptions in a BloodHound query YAML.

- Reads a YAML with top-level `queries: [...]`
- Detects duplicates by `desc`
- For each duplicate group, prints *every* entry's cypher and msg_template
  and prompts the user to choose which entries to KEEP (supports multiple)
- Writes the resolved set to the output YAML, preserving overall order where possible
- Forces both cypher and msg_template to YAML literal block scalars (|)

Usage:
  python dedupe_by_description.py --input ad-queries.yaml --output ad-queries.dedup.yaml --debug

Optional:
  --backup    Create output.bak if output exists
  --keep-all-if-none   If a duplicate group prompt receives no selection (just Enter),
                       keep *all* entries in that group (default keeps the FIRST only).
  --prefer-first-noninteractive
               Skip all prompts (non-interactive mode) and automatically keep the FIRST
               entry in each duplicate group.
"""

import argparse
import os
import sys
import yaml
from typing import Dict, Any, List, Tuple, Set

# ---------- YAML literal block support (forces '|' for str subclasses) ----------

class LiteralStr(str):
    """Marker type to force PyYAML to emit a literal block scalar (|)."""
    pass

def _literal_representer(dumper, data):
    return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')

# Register on both dumpers so safe_dump knows about LiteralStr
yaml.add_representer(LiteralStr, _literal_representer)
yaml.SafeDumper.add_representer(LiteralStr, _literal_representer)

# --------------------------------- Helpers --------------------------------------

def dbg(enabled: bool, msg: str):
    if enabled:
        print(f"[DEBUG] {msg}")

def err(msg: str):
    print(f"[ERROR] {msg}", file=sys.stderr)

def warn(msg: str):
    print(f"[WARN] {msg}")

def load_yaml_file(path: str, debug: bool) -> Dict[str, Any]:
    if not os.path.isfile(path):
        raise FileNotFoundError(f"YAML not found: {path}")
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        if not isinstance(data, dict) or "queries" not in data or not isinstance(data["queries"], list):
            raise ValueError(f"YAML must contain a top-level 'queries' list: {path}")
        dbg(debug, f"Loaded '{path}' with {len(data['queries'])} queries.")
        return data
    except yaml.YAMLError as e:
        raise ValueError(f"Invalid YAML in {path}: {e}") from e

def save_yaml_file(path: str, data: Dict[str, Any], backup: bool, debug: bool) -> None:
    # optional backup of output target
    if backup and os.path.exists(path):
        bak = f"{path}.bak"
        try:
            import shutil
            shutil.copy2(path, bak)
            dbg(debug, f"Backed up '{path}' -> '{bak}'")
        except Exception as e:
            warn(f"Failed to create backup '{bak}': {e}")

    try:
        out = {"queries": [prepare_literal_blocks(q) for q in data.get("queries", [])]}
        with open(path, "w", encoding="utf-8") as f:
            yaml.safe_dump(out, f, sort_keys=False, allow_unicode=True, width=100)
        dbg(debug, f"Wrote '{path}' with {len(out['queries'])} queries.")
    except Exception as e:
        raise IOError(f"Failed to write YAML to {path}: {e}") from e

def prepare_literal_blocks(q: Dict[str, Any]) -> Dict[str, Any]:
    """
    Force msg_template to a literal block scalar always.
    Force cypher to a literal block scalar if multi-line (or uncomment to always force).
    """
    q = dict(q)  # shallow copy

    # msg_template -> always block scalar
    if "msg_template" in q and q["msg_template"] is not None:
        mt = q["msg_template"]
        if not isinstance(mt, str):
            mt = str(mt)
        q["msg_template"] = LiteralStr(mt)

    # cypher -> block scalar when multi-line (toggle to force always)
    if "cypher" in q and q["cypher"] is not None:
        cy = q["cypher"]
        if not isinstance(cy, str):
            cy = str(cy)
        if "\n" in cy:
            q["cypher"] = LiteralStr(cy)
        else:
            # Uncomment to also force single-line cypher to block style
            # q["cypher"] = LiteralStr(cy)
            q["cypher"] = cy

    return q

def build_duplicate_index(queries: List[Dict[str, Any]]) -> Dict[str, List[int]]:
    """
    Returns: desc -> list of indices in queries where that desc appears (len >= 1)
    """
    dup: Dict[str, List[int]] = {}
    for i, q in enumerate(queries):
        desc = q.get("desc", "")
        dup.setdefault(desc, []).append(i)
    # Only keep entries where there are duplicates
    return {d: idxs for d, idxs in dup.items() if len(idxs) > 1}

def print_group_block(desc: str, entries: List[Dict[str, Any]]):
    print("\n" + "=" * 80)
    print(f"Duplicate description: {desc}")
    print("=" * 80)
    for i, q in enumerate(entries, 1):
        grp = q.get("group", "")
        cy = q.get("cypher", "")
        mt = q.get("msg_template", "")
        print(f"\n[{i}] group: {grp}")
        print("-" * 80)
        print("CYPHER:")
        print(cy if isinstance(cy, str) else str(cy))
        print("-" * 80)
        print("MESSAGE TEMPLATE:")
        print(mt if isinstance(mt, str) else str(mt))
        print("-" * 80)

def parse_selection(user_input: str, n: int) -> List[int]:
    """
    Parse input like "1,3" -> [1,3]
    Allows 'a'/'A' for all; returns list of 1..n on 'a'
    """
    s = user_input.strip()
    if s.lower() == "a":
        return list(range(1, n + 1))
    if not s:
        return []
    picks: List[int] = []
    for part in s.split(","):
        part = part.strip()
        if not part:
            continue
        if not part.isdigit():
            raise ValueError(f"Non-numeric selection: {part}")
        val = int(part)
        if val < 1 or val > n:
            raise ValueError(f"Selection out of range: {val} (valid 1..{n})")
        if val not in picks:
            picks.append(val)
    return picks

def resolve_duplicates_interactively(queries: List[Dict[str, Any]],
                                     debug: bool,
                                     keep_all_if_none: bool,
                                     noninteractive_prefer_first: bool) -> List[Dict[str, Any]]:
    """
    Returns a new list of queries with duplicates resolved.
    Strategy:
      - For each duplicate desc:
          - If noninteractive => keep first
          - Else prompt until valid selection (supports multiple indices; 'a' = all)
            * If selection is empty: keep first (or keep all if keep_all_if_none=True)
      - Preserve original order; for each desc, on first occurrence we insert the chosen entries
        in the order they were selected; subsequent occurrences are skipped
    """
    desc_to_indices = build_duplicate_index(queries)
    if not desc_to_indices:
        # No duplicates -> return original verbatim
        return list(queries)

    dbg(debug, f"Found {len(desc_to_indices)} duplicate description group(s).")

    # Build chosen entries mapping: desc -> list[Dict]
    chosen_by_desc: Dict[str, List[Dict[str, Any]]] = {}

    if noninteractive_prefer_first:
        for desc, idxs in desc_to_indices.items():
            chosen_by_desc[desc] = [queries[idxs[0]]]
        dbg(debug, "Non-interactive mode: keeping FIRST entry in every duplicate group.")
    else:
        for desc, idxs in desc_to_indices.items():
            entries = [queries[i] for i in idxs]
            print_group_block(desc, entries)

            while True:
                try:
                    prompt = ("Enter the indices to KEEP for this description (comma-separated), "
                              "'a' to keep all, or press Enter "
                              f"to keep {'ALL' if keep_all_if_none else 'FIRST'}: ")
                    raw = input(prompt)
                    picks = parse_selection(raw, len(entries))
                    if not picks:
                        if keep_all_if_none:
                            keep = list(range(1, len(entries) + 1))
                        else:
                            keep = [1]
                    else:
                        keep = picks
                    # Materialize chosen in the order provided
                    chosen = [entries[i - 1] for i in keep]
                    chosen_by_desc[desc] = chosen
                    break
                except Exception as e:
                    err(f"{e}. Please try again.")

    # Rewrite the list preserving overall order: when first occurrence of desc is seen,
    # inject the chosen list and mark desc as handled. Subsequent duplicates are skipped.
    seen: Set[str] = set()
    out: List[Dict[str, Any]] = []
    for i, q in enumerate(queries):
        desc = q.get("desc", "")
        if desc not in desc_to_indices:
            out.append(q)
            continue
        if desc in seen:
            # skip subsequent occurrences
            continue
        # First occurrence of this duplicate desc => insert chosen
        out.extend(chosen_by_desc.get(desc, [q]))
        seen.add(desc)

    return out

# ------------------------------------- Main --------------------------------------

def main():
    ap = argparse.ArgumentParser(
        description="Interactively resolve duplicate descriptions in a BloodHound queries YAML.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    ap.add_argument("--input", required=True, help="Path to input YAML with top-level 'queries' list.")
    ap.add_argument("--output", required=True, help="Path to write the resolved YAML.")
    ap.add_argument("--backup", action="store_true", help="Backup output to <output>.bak if it already exists.")
    ap.add_argument("--debug", action="store_true", help="Verbose debug output.")
    ap.add_argument("--keep-all-if-none", action="store_true",
                    help="If you press Enter at a duplicate prompt, keep ALL (default keeps FIRST).")
    ap.add_argument("--prefer-first-noninteractive", action="store_true",
                    help="Non-interactive mode: automatically keep FIRST entry in each duplicate group.")
    args = ap.parse_args()

    try:
        data = load_yaml_file(args.input, args.debug)
        queries: List[Dict[str, Any]] = data["queries"]

        resolved = resolve_duplicates_interactively(
            queries,
            debug=args.debug,
            keep_all_if_none=args.keep_all_if_none,
            noninteractive_prefer_first=args.prefer_first_noninteractive,
        )

        print(f"[+] Original queries: {len(queries)}")
        print(f"[+] Resolved queries : {len(resolved)}")

        save_yaml_file(args.output, {"queries": resolved}, backup=args.backup, debug=args.debug)
        print(f"[+] Wrote: {args.output}")

    except Exception as e:
        err(str(e))
        if args.debug:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
