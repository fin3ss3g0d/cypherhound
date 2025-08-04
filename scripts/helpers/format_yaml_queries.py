#!/usr/bin/env python3
"""
format_yaml_queries.py
====================
Re-format an *existing* BloodHound queries YAML so that:

• dotted RETURN columns are aliased (foo.bar → foo_bar, labels(x)[0] → …_0)
• templates are rewritten to use the aliases
• Cypher is pretty-printed (one major clause per line)
• long strings are literal block scalars (|) and wrapped to 100 chars

Only the YAML file is read; no connection to Neo4j is required.
"""

import re
import textwrap
import argparse
import sys
from pathlib import Path
import yaml

# ---------------------------------------------------------------------------
# pretty-print helper
# ---------------------------------------------------------------------------
CYCLAUSE = re.compile(r"\s+(MATCH|WHERE|RETURN|WITH|ORDER BY|SET|CREATE|MERGE)\s+",
                      re.I)

def prettify_cypher(query: str) -> str:
    return CYCLAUSE.sub(lambda m: "\n" + m.group(1) + " ", query).strip()

def wrap_long_line(s: str | None, width: int = 100) -> str | None:
    if s is None or "\n" in s or len(s) <= width:
        return s
    return textwrap.fill(s, width=width, break_long_words=False,
                         break_on_hyphens=False)

# ---------------------------------------------------------------------------
# RETURN-aliasing helpers
# ---------------------------------------------------------------------------
IDENT_CLEAN = re.compile(r"[^0-9A-Za-z_]")
KW_AFTER_RETURN = re.compile(r"\b(WHERE|WITH|ORDER\s+BY|SET|CREATE|MERGE|MATCH)\b", re.I)
MULTI_US = re.compile(r"_+")


def make_alias(expr: str) -> str:
    """
    'u.name'          ->  u_name
    'labels(m)'       ->  labels_m
    'labels(m)[0]'    ->  labels_m_0
    '123bad.column'   -> _123bad_column
    """
    # 1) replace every bad char with "_"
    alias = IDENT_CLEAN.sub("_", expr)

    # 2) collapse runs of underscores and trim
    alias = MULTI_US.sub("_", alias).strip("_")

    # 3) if it now starts with a digit, prefix with "_"
    return "_" + alias if alias and alias[0].isdigit() else alias


def alias_return_clause(cypher: str) -> tuple[str, dict[str, str]]:
    m = re.search(r"\bRETURN\b", cypher, re.I)
    if not m:
        return cypher, {}

    start = m.end()
    m2 = KW_AFTER_RETURN.search(cypher[start:])
    end = start + m2.start() if m2 else len(cypher)
    return_list = cypher[start:end]

    mapping = {}
    parts, buf, depth = [], [], 0
    for ch in return_list:
        if ch == "," and depth == 0:
            parts.append("".join(buf).strip()); buf = []
        else:
            depth += (ch in "([{") - (ch in ")]}")
            buf.append(ch)
    parts.append("".join(buf).strip())

    new_parts = []
    for p in parts:
        if re.search(r"\bAS\b", p, re.I):
            new_parts.append(p); continue
        if "." in p or "[" in p or p.startswith("labels("):
            alias = make_alias(p)
            mapping[p] = alias
            new_parts.append(f"{p} AS {alias}")
        else:
            new_parts.append(p)

    new_return = ", ".join(new_parts)
    rest = cypher[end:].lstrip()
    return f"{cypher[:start]} {new_return} {rest}", mapping

def apply_alias_to_template(tmpl: str | None, mapping: dict[str, str]) -> str | None:
    if not tmpl or not mapping:
        return tmpl
    for expr, alias in mapping.items():
        pat = re.compile(r"\{\{\s*" + re.escape(expr) + r"\s*\}\}")
        tmpl = pat.sub(f"{{{{ {alias} }}}}", tmpl)

        # handle indexed forms like  labels(m)[0]  →  labels_m[0]
        if expr.startswith("labels("):
            for idx in ("0", "1"):
                pat_idx = re.compile(rf"\{{\{{\s*{re.escape(expr)}\s*\[\s*{idx}\s*\]\s*\}}\}}")
                tmpl = pat_idx.sub(f"{{{{ {alias}[{idx}] }}}}", tmpl)
    return tmpl

# ---------------------------------------------------------------------------
# PyYAML literal block scalar support
# ---------------------------------------------------------------------------
class LiteralStr(str): pass
def _represent_literal_str(dumper, data):
    return dumper.represent_scalar('tag:yaml.org,2002:str', str(data), style='|')
yaml.add_representer(LiteralStr, _represent_literal_str, Dumper=yaml.SafeDumper)

# ---------------------------------------------------------------------------
# main reformatter
# ---------------------------------------------------------------------------
def format_queries(inp: Path, out: Path) -> None:
    doc = yaml.safe_load(inp.read_text(encoding="utf-8"))
    qlist = doc.get("queries", [])

    for q in qlist:
        cypher, amap = alias_return_clause(q["cypher"])
        q["cypher"] = LiteralStr(prettify_cypher(cypher))

        if q.get("msg_template"):
            tmpl = apply_alias_to_template(q["msg_template"], amap)
            q["msg_template"] = LiteralStr(wrap_long_line(tmpl))
        else:
            q["msg_template"] = None

    qlist.sort(key=lambda x: x["desc"].lower())
    with out.open("w", encoding="utf-8") as fp:
        yaml.safe_dump(doc, fp, sort_keys=False, width=120, allow_unicode=True)

# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main(argv: list[str]) -> None:
    ap = argparse.ArgumentParser(description="Re-format BloodHound queries YAML")
    ap.add_argument("-i", "--input",  required=True, help="input YAML file path")
    ap.add_argument("-o", "--output", required=True, help="output YAML file path")
    args = ap.parse_args(argv)

    inp = Path(args.input).expanduser()
    if not inp.exists():
        sys.exit(f"Input file not found: {inp}")
    out = Path(args.output).expanduser()

    format_queries(inp, out)
    print(f"[+] Wrote formatted YAML → {out}")

if __name__ == "__main__":
    main(sys.argv[1:])
