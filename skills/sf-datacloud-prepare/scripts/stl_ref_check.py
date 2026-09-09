#!/usr/bin/env python3
"""Check that every column an STL formula reads is exposed by its source node.

Static analysis of a Data 360 batch-transform body (`/ssot/data-transforms`
payload JSON) with no org calls. A join that sets a `rightQualifier` renames the
whole right side to ``qualifier.column``, so a formula still reading the bare
name is addressing a column that no longer exists. The runtime reports this
inconsistently — sometimes a named error, sometimes a generic failure — so
resolve references statically before deploying (see BEAST-PROOF-019/020).

Usage: python3 stl_ref_check.py transform.json [more.json ...]
Exits 1 on any unresolved reference.
"""
from __future__ import annotations

import argparse
import html
import json
import re
import sys

# Function names and keywords that look like bare column references but are
# resolved by the SQL engine, not by an upstream node.
SQL_TOKENS = {
    "case", "when", "then", "else", "end", "and", "or", "not", "null", "is",
    "in", "as", "coalesce", "round", "cast", "to_date", "to_timestamp",
    "current_timestamp", "current_date", "date", "abs", "min", "max", "sum",
    "avg", "count", "concat", "substring", "length", "trim", "upper", "lower",
    "lpad", "rpad", "replace", "nvl", "if", "greatest", "least", "floor",
    "ceil", "row_number", "rank", "over", "partition", "by", "order", "desc",
    "asc", "distinct", "string", "int", "bigint", "decimal", "double", "true",
    "false", "year", "month", "day", "datediff", "dateadd", "sqrt", "power",
    "mod", "sign", "stddev", "variance", "first_value", "last_value", "lag",
    "lead", "interval", "extract", "from", "select", "where", "like", "between",
    "ltrim", "rtrim", "date_format", "nullif", "instr", "char_length",
    "character_length", "split", "regexp_replace", "regexp_extract", "left",
    "right", "position", "locate", "translate", "ascii", "initcap", "reverse",
    "to_number", "try_cast", "date_trunc", "last_day", "add_months", "months_between",
    "unix_timestamp", "from_unixtime", "current_user", "isnull", "isnotnull",
}

DOTTED = re.compile(r'"([A-Za-z_]\w*\.\w+)"')
IDENT = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")


def node_columns(nodes):
    """Map each node id to the set of column names it exposes downstream."""
    memo = {}

    def cols(nid):
        if nid in memo:
            return memo[nid]
        node = nodes[nid]
        action = node["action"]
        params = node.get("parameters") or {}
        srcs = node.get("sources") or []
        if action == "load":
            out = {
                f if isinstance(f, str) else f.get("name")
                for f in params.get("fields", [])
            }
        elif action == "aggregate":
            out = set(params.get("groupings") or []) | {
                a["name"] for a in params.get("aggregations") or []
            }
        elif action in ("formula", "computeRelative"):
            out = cols(srcs[0]) | {f["name"] for f in params.get("fields", [])}
        elif action == "typeCast":
            out = cols(srcs[0]) | {
                f["newProperties"]["name"] for f in params.get("fields", [])
            }
        elif action in ("filter", "sqlFilter", "extractGrains", "deduplicate"):
            out = cols(srcs[0])
        elif action == "join":
            qualifier = params.get("rightQualifier")
            right = cols(srcs[1])
            out = cols(srcs[0]) | (
                {f"{qualifier}.{c}" for c in right} if qualifier else right
            )
        elif action in ("append", "appendV2"):
            out = set().union(*(cols(s) for s in srcs)) if srcs else set()
        else:
            out = cols(srcs[0]) if srcs else set()
        memo[nid] = out
        return out

    return cols


def unresolved(path):
    """Return (node, field, reference, kind) for each unresolved reference."""
    with open(path) as handle:
        nodes = json.load(handle)["definition"]["nodes"]
    cols = node_columns(nodes)
    found = []
    for nid, node in nodes.items():
        if node["action"] not in ("formula", "computeRelative"):
            continue
        srcs = node.get("sources") or []
        upstream = cols(srcs[0]) if srcs else set()
        for field in (node.get("parameters") or {}).get("fields", []):
            expr = html.unescape(field.get("formulaExpression", ""))
            for ref in DOTTED.findall(expr):
                if ref not in upstream:
                    found.append((nid, field["name"], ref, "qualified"))
            # Strip quoted names and literals so only bare identifiers remain.
            bare = DOTTED.sub(" ", expr)
            bare = re.sub(r'"[^"]*"', " ", bare)
            bare = re.sub(r"'[^']*'", " ", bare)
            bare = re.sub(r"\b\d+(\.\d+)?\b", " ", bare)
            for tok in dict.fromkeys(IDENT.findall(bare)):
                if tok.lower() in SQL_TOKENS:
                    continue
                if tok in upstream or tok == field["name"]:
                    continue
                found.append((nid, field["name"], tok, "bare"))
    return found


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", help="transform body JSON file(s)")
    args = parser.parse_args()

    total = 0
    for path in args.paths:
        bad = unresolved(path)
        total += len(bad)
        print("%-46s unresolved=%d" % (path, len(bad)))
        for nid, fname, ref, kind in bad:
            print("    %-20s %-28s %-28s %s" % (nid, fname, ref, kind))
    return 1 if total else 0


if __name__ == "__main__":
    raise SystemExit(main())
