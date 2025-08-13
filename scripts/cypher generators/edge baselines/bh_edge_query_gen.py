#!/usr/bin/env python3
"""
edge_query_expander.py
======================

Generate BloodHound query entries for new traversable edges by cloning a baseline
template YAML and appending to a master YAML.

PRIMARY MODE (recommended):
  • Baseline uses Jinja markers like [[ EDGE ]] in desc/cypher/msg_template/etc.
  • The ENTIRE file is rendered through Jinja2 with [[ ... ]] so runtime {{ ... }} stays intact.

FALLBACK MODE (legacy baselines):
  • If the baseline does not contain [[ EDGE ]], parse YAML and detect the relationship token
    from cypher (e.g., -[r:AddKeyCredentialLink]->), or pass --baseline-edge to override.

Features
--------
• CLI args with help/usage; debug prints
• Dry-run preview and optional backup of output
• Replace-or-add merge policy (skip only on exact group+desc+cypher match; replace on group+desc)
• Literal block scalars (|) for multi-line cypher, always for msg_template
• **NEW**: Edge blacklist (default: MemberOf, SameForestTrust, DCFor, DCSync)

Usage
-----
  python edge_query_expander.py \
    --template baseline_edge_template.yaml \
    --edges GenericAll,WriteSPN,AddMember \
    --output master_queries.yaml --backup --debug

  python edge_query_expander.py \
    --template baseline_legacy_addkey.yaml \
    --edges-file edges.txt \
    --output master_queries.yaml --dry-run

Blacklist examples
------------------
  # default blacklist is active
  python edge_query_expander.py --template t.yaml --edges MemberOf,AddMember --output out.yaml

  # add extra blacklisted edges on top of defaults
  python edge_query_expander.py --template t.yaml --edges A,B \
    --blacklist C,D --output out.yaml

  # provide a blacklist file (one per line)
  python edge_query_expander.py --template t.yaml --edges-file edges.txt \
    --blacklist-file bl.txt --output out.yaml

  # ignore the built-in defaults
  python edge_query_expander.py --template t.yaml --edges X,Y \
    --no-default-blacklist --output out.yaml
"""

import argparse
import os
import sys
import re
import hashlib
from copy import deepcopy
from typing import Dict, Any, List, Tuple, Set

import yaml
from jinja2 import Environment, StrictUndefined

# ---------------- YAML literal block support for multi-line strings ----------------

class LiteralStr(str):
    """Marker type to force PyYAML to emit a literal block scalar (|)."""
    pass

def _literal_representer(dumper, data):
    # emit as literal block scalar
    return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')

# Register for BOTH Dumpers
yaml.add_representer(LiteralStr, _literal_representer)
yaml.SafeDumper.add_representer(LiteralStr, _literal_representer)


# ---------------------------------- Regexes --------------------------------------

REL_PATTERN = re.compile(r"-\s*\[\s*r\s*:\s*([A-Za-z0-9_]+)\s*\]\s*->")


# ---------------------------------- Logging --------------------------------------

def dbg(enabled: bool, msg: str):
    if enabled:
        print(f"[DEBUG] {msg}")

def err(msg: str):
    print(f"[ERROR] {msg}", file=sys.stderr)

def warn(msg: str):
    print(f"[WARN] {msg}")


# ------------------------------ Jinja environment -------------------------------

def make_jinja_env() -> Environment:
    """
    Use [[ ... ]] for generator-time substitutions; keep runtime {{ ... }} intact.
    """
    return Environment(
        variable_start_string="[[",
        variable_end_string="]]",
        trim_blocks=True,
        lstrip_blocks=True,
        undefined=StrictUndefined,
    )


# ------------------------------ Blacklist config ---------------------------------

DEFAULT_EDGE_BLACKLIST: Set[str] = {
    "MemberOf",
    "SameForestTrust",
    "DCFor",
    "DCSync",
}

def read_list_from_file(path: str) -> List[str]:
    if not os.path.isfile(path):
        raise FileNotFoundError(f"File not found: {path}")
    vals: List[str] = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            s = line.strip()
            if s and not s.startswith("#"):
                vals.append(s)
    return vals

def parse_blacklist(blk_arg: str, blk_file: str, include_default: bool, ci: bool, debug: bool) -> Set[str]:
    bl: Set[str] = set()
    if include_default:
        bl |= DEFAULT_EDGE_BLACKLIST
    if blk_arg:
        parts = [p.strip() for p in blk_arg.split(",") if p.strip()]
        bl |= set(parts)
    if blk_file:
        file_edges = read_list_from_file(blk_file)
        bl |= set(file_edges)
    # Normalize case if case-insensitive
    if ci:
        bl = {e.lower() for e in bl}
    dbg(debug, f"Effective blacklist ({'CI' if ci else 'CS'}): {sorted(bl)}")
    return bl


# -------------------------------- File helpers -----------------------------------

def load_text(path: str) -> str:
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Template not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def load_yaml_file(path: str, debug: bool) -> Dict[str, Any]:
    if not os.path.isfile(path):
        raise FileNotFoundError(f"YAML not found: {path}")
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        if not isinstance(data, dict) or "queries" not in data or not isinstance(data["queries"], list):
            raise ValueError(f"YAML must contain a top-level 'queries' list: {path}")
        dbg(debug, f"Loaded YAML '{path}' with {len(data['queries'])} queries.")
        return data
    except yaml.YAMLError as e:
        raise ValueError(f"Invalid YAML in {path}: {e}") from e

def save_yaml_file(path: str, data: Dict[str, Any], backup: bool, debug: bool) -> None:
    # Optional backup
    if backup and os.path.exists(path):
        base, _ = os.path.splitext(path)
        bak = f"{base}.bak"
        try:
            import shutil
            shutil.copy2(path, bak)
            dbg(debug, f"Backed up '{path}' -> '{bak}'")
        except Exception as e:
            warn(f"Failed to create backup '{bak}': {e}")

    try:
        def prepare_literal_blocks(q: Dict[str, Any]) -> Dict[str, Any]:
            q = dict(q)  # shallow copy

            # Always force msg_template to a literal block scalar (even if single-line)
            if "msg_template" in q and q["msg_template"] is not None:
                mt = q["msg_template"]
                if not isinstance(mt, str):
                    mt = str(mt)
                q["msg_template"] = LiteralStr(mt)

            # For cypher: if multi-line, block scalar (toggle to force always)
            if "cypher" in q and q["cypher"] is not None:
                cy = q["cypher"]
                if not isinstance(cy, str):
                    cy = str(cy)
                if "\n" in cy:
                    q["cypher"] = LiteralStr(cy)
                else:
                    q["cypher"] = LiteralStr(cy)

            return q

        out = {"queries": [prepare_literal_blocks(q) for q in data.get("queries", [])]}
        with open(path, "w", encoding="utf-8") as f:
            yaml.safe_dump(out, f, sort_keys=False, allow_unicode=True, width=100)
        dbg(debug, f"Wrote YAML '{path}' with {len(out['queries'])} queries.")
    except Exception as e:
        raise IOError(f"Failed to write YAML to {path}: {e}") from e


# ------------------------------ Edge list parsing --------------------------------

def read_edges(edges_arg: str, edges_file: str, debug: bool) -> List[str]:
    vals: List[str] = []
    if edges_arg:
        parts = [p.strip() for p in edges_arg.split(",") if p.strip()]
        vals.extend(parts)
    if edges_file:
        vals.extend(read_list_from_file(edges_file))

    bad = [e for e in vals if not re.fullmatch(r"[A-Za-z0-9_]+", e)]
    if bad:
        raise ValueError(f"Invalid edge names (letters/digits/_ only): {bad}")

    # De-dup, preserve order
    seen: Set[str] = set()
    ordered = []
    for e in vals:
        if e not in seen:
            seen.add(e)
            ordered.append(e)

    dbg(debug, f"Edges parsed: {ordered}")
    return ordered

def apply_blacklist(edges: List[str], blacklist: Set[str], ci: bool, debug: bool) -> Tuple[List[str], List[str]]:
    if not blacklist:
        return edges, []
    kept: List[str] = []
    skipped: List[str] = []
    if ci:
        bl = blacklist  # already lowercased
        for e in edges:
            if e.lower() in bl:
                skipped.append(e)
            else:
                kept.append(e)
    else:
        bl = blacklist
        for e in edges:
            if e in bl:
                skipped.append(e)
            else:
                kept.append(e)
    if skipped:
        warn(f"Skipping blacklisted edges: {', '.join(skipped)}")
    dbg(debug, f"Edges after blacklist: {kept}")
    return kept, skipped


# ------------------------ Rendering / Generation paths ---------------------------

def template_has_marker(template_text: str) -> bool:
    # Fast check for our Jinja-style marker
    return "[[ EDGE ]]" in template_text

def render_template_yaml_to_queries(template_text: str, edge: str, debug: bool) -> List[Dict[str, Any]]:
    """
    PRIMARY PATH:
      Render the *entire* baseline YAML via Jinja, substituting [[ EDGE ]] -> <edge>,
      then parse YAML and return the 'queries' list.
    """
    env = make_jinja_env()
    tmpl = env.from_string(template_text)
    rendered = tmpl.render(EDGE=edge)
    if debug:
        snippet = rendered[:300].replace("\n", "\\n")
        dbg(debug, f"Rendered YAML for edge '{edge}' (first 300 chars): {snippet}")
    data = yaml.safe_load(rendered)
    if not isinstance(data, dict) or "queries" not in data or not isinstance(data["queries"], list):
        raise ValueError("Rendered YAML must contain a top-level 'queries' list.")
    return data["queries"]

def detect_baseline_edge_from_queries(queries: List[Dict[str, Any]]) -> str:
    edges = set()
    for q in queries:
        cy = q.get("cypher", "")
        if not isinstance(cy, str):
            continue
        for m in REL_PATTERN.finditer(cy):
            edges.add(m.group(1))
    if not edges:
        raise ValueError("Could not detect any relationship token like [r:EdgeName] in template cypher.")
    if len(edges) > 1:
        raise ValueError(f"Multiple different relationship tokens detected in template: {sorted(edges)}")
    return next(iter(edges))

def replacement_in_query(q: Dict[str, Any], baseline_edge: str, new_edge: str, debug: bool) -> Dict[str, Any]:
    new_q = deepcopy(q)
    for k in ("desc", "cypher", "msg_template"):
        v = new_q.get(k)
        if isinstance(v, str):
            replaced = v.replace(baseline_edge, new_edge)
            new_q[k] = replaced
            if debug and v != replaced:
                dbg(debug, f"Replaced in '{k}': '{baseline_edge}' -> '{new_edge}'")
    return new_q

def generate_entries_from_baseline_text(template_text: str, edges: List[str], debug: bool) -> List[Dict[str, Any]]:
    """
    Dispatches to the Jinja render path (if [[ EDGE ]] is present) or legacy path.
    """
    generated: List[Dict[str, Any]] = []
    if template_has_marker(template_text):
        dbg(debug, "Template contains [[ EDGE ]] marker; using Jinja render path.")
        for edge in edges:
            generated.extend(render_template_yaml_to_queries(template_text, edge, debug))
    else:
        # Legacy baseline: parse YAML, detect/replace relationship token
        dbg(debug, "Template has no [[ EDGE ]]; using legacy detection/replace path.")
        base = yaml.safe_load(template_text)
        if not isinstance(base, dict) or "queries" not in base or not isinstance(base["queries"], list):
            raise ValueError("Legacy template must contain a top-level 'queries' list.")
        baseline_edge = detect_baseline_edge_from_queries(base["queries"])
        dbg(debug, f"Detected baseline edge token: '{baseline_edge}'")
        for edge in edges:
            for q in base["queries"]:
                generated.append(replacement_in_query(q, baseline_edge, edge, debug))
    dbg(debug, f"Generated {len(generated)} total entries for {len(edges)} edge(s).")
    return generated


# --------------------------------- Merge logic -----------------------------------

def norm_ws(s: str) -> str:
    return "\n".join(line.rstrip() for line in str(s).strip().splitlines())

def gd_key(q: Dict[str, Any]) -> Tuple[str, str]:
    return (str(q.get("group", "")), str(q.get("desc", "")))

def gdc_key(q: Dict[str, Any]) -> Tuple[str, str, str]:
    return (str(q.get("group", "")), str(q.get("desc", "")), norm_ws(q.get("cypher", "")))

def append_replace_or_add(master: Dict[str, Any],
                          additions: List[Dict[str, Any]],
                          debug: bool) -> Tuple[int, int, int]:
    """
    Merge policy:
      • If (group, desc, cypher) all match an existing entry => SKIP
      • Else if (group, desc) match but cypher differs => REPLACE the existing entry's entire dict with new one
      • Else => APPEND new entry

    Returns: (added, replaced, skipped)
    """
    if "queries" not in master or not isinstance(master["queries"], list):
        master["queries"] = []

    queries = master["queries"]

    # Build indexes for fast lookups
    idx_by_gd: Dict[Tuple[str, str], int] = {}
    idx_by_gdc: Dict[Tuple[str, str, str], int] = {}

    # Detect duplicates on (group, desc) in the master (if any)
    seen_gd: Dict[Tuple[str, str], int] = {}
    for i, q in enumerate(queries):
        gd = gd_key(q)
        gdc = gdc_key(q)
        idx_by_gd.setdefault(gd, i)      # keep the first occurrence
        idx_by_gdc[gdc] = i

        # Optional: warn about multiple same (group, desc) in master
        if gd in seen_gd and debug:
            warn(f"Multiple existing entries share (group, desc)={gd}; first at {seen_gd[gd]}, also at {i}. "
                 "Replacement will target the earliest one.")
        else:
            seen_gd[gd] = i

    added = 0
    replaced = 0
    skipped = 0

    for new_q in additions:
        gd = gd_key(new_q)
        gdc = gdc_key(new_q)

        # Exact triple match => skip
        if gdc in idx_by_gdc:
            skipped += 1
            if debug:
                dbg(debug, f"SKIP (exact match): group={gd[0]!r}, desc={gd[1]!r}")
            continue

        if gd in idx_by_gd:
            # Replace the first matching (group, desc)
            idx = idx_by_gd[gd]
            old_q = queries[idx]
            old_gdc = gdc_key(old_q)

            queries[idx] = new_q
            replaced += 1

            # Update indexes
            if old_gdc in idx_by_gdc:
                del idx_by_gdc[old_gdc]
            idx_by_gdc[gdc] = idx
            # idx_by_gd[gd] remains same index

            if debug:
                dbg(debug, f"REPLACE at index {idx}: group={gd[0]!r}, desc={gd[1]!r}")
        else:
            # Append as new
            queries.append(new_q)
            idx = len(queries) - 1
            added += 1

            # Update indexes
            idx_by_gd[gd] = idx
            idx_by_gdc[gdc] = idx

            if debug:
                dbg(debug, f"ADD at index {idx}: group={gd[0]!r}, desc={gd[1]!r}")

    if debug:
        dbg(debug, f"Merge summary: Added={added}, Replaced={replaced}, Skipped={skipped}, Total={len(queries)}")

    return added, replaced, skipped


# ------------------------------------- Main --------------------------------------

def main():
    ap = argparse.ArgumentParser(
        description="Expand a baseline BloodHound edge query template to multiple edges and append to a master YAML.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    ap.add_argument("--template", required=True, help="Path to baseline template YAML (prefer [[ EDGE ]] markers).")
    ap.add_argument("--output", required=True, help="Path to master queries YAML to append to (created if missing).")

    eg = ap.add_mutually_exclusive_group(required=True)
    eg.add_argument("--edges", help="Comma-separated list of edges, e.g. 'GenericAll,WriteSPN,AddMember'.")
    eg.add_argument("--edges-file", help="File containing one edge per line.")

    # Blacklist controls
    ap.add_argument("--blacklist", help="Comma-separated edge names to blacklist (skip generation).")
    ap.add_argument("--blacklist-file", help="File with one edge per line to blacklist.")
    ap.add_argument("--no-default-blacklist", action="store_true",
                    help="Do not include the built-in default blacklist.")
    ap.add_argument("--blacklist-ci", action="store_true",
                    help="Treat blacklist checks as case-insensitive.")

    ap.add_argument("--backup", action="store_true", help="Backup output to .bak before writing.")
    ap.add_argument("--dry-run", action="store_true", help="Preview changes without writing.")
    ap.add_argument("--debug", action="store_true", help="Verbose debug output.")

    args = ap.parse_args()
    dbg(args.debug, f"Args: {args}")

    try:
        template_text = load_text(args.template)
        edges = read_edges(args.edges, args.blacklist_file and None if False else args.edges_file, args.debug)

        # Build effective blacklist
        blacklist = parse_blacklist(
            blk_arg=args.blacklist,
            blk_file=args.blacklist_file,
            include_default=(not args.no_default_blacklist),
            ci=args.blacklist_ci,
            debug=args.debug,
        )

        # Apply blacklist
        edges, skipped_bl = apply_blacklist(edges, blacklist, args.blacklist_ci, args.debug)
        if not edges:
            warn("All requested edges are blacklisted; nothing to generate.")
            print(f"[+] Skipped by blacklist: {len(skipped_bl)} ({', '.join(skipped_bl)})" if skipped_bl else "")
            return

        # --- Generate entries (JINJA RENDER happens here if [[ EDGE ]] is present) ---
        generated = generate_entries_from_baseline_text(template_text, edges, args.debug)

        # --- Load or create the master YAML ---
        if os.path.exists(args.output):
            master = load_yaml_file(args.output, args.debug)
        else:
            master = {"queries": []}
            dbg(args.debug, f"Master '{args.output}' does not exist; will create.")

        # --- Append + replace-or-add and report ---
        added, replaced, skipped = append_replace_or_add(master, generated, args.debug)

        print(f"[+] Edges requested: {edges}")
        if skipped_bl:
            print(f"[+] Skipped by blacklist: {len(skipped_bl)} ({', '.join(skipped_bl)})")
        print(f"[+] Generated: {len(generated)} | Added: {added} | Replaced: {replaced} | Skipped: {skipped}")
        print(f"[+] Master path: {args.output}")

        if args.dry_run:
            print("[DRY-RUN] Not writing changes. Use without --dry-run to persist.")
            if generated:
                sample = {"queries": [generated[0]]}
                print("\n--- Sample Generated Entry ---")
                print(yaml.safe_dump(sample, sort_keys=False, allow_unicode=True, width=100))
            return

        # --- Persist updated master ---
        save_yaml_file(args.output, master, backup=args.backup, debug=args.debug)
        print("[+] Write complete.")

    except Exception as e:
        err(str(e))
        if args.debug:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
