#!/usr/bin/env python3
"""Check that every column an STL formula reads is exposed by its source node.

Static analysis of a Data 360 batch-transform body (`/ssot/data-transforms`
payload JSON) with no org calls. A join that sets a `rightQualifier` renames the
whole right side to ``qualifier.column``, so a formula still reading the bare
name is addressing a column that no longer exists. The runtime reports this
inconsistently — sometimes a named error, sometimes a generic failure — so
resolve supported references statically before deploying (see BEAST-PROOF-020
and BEAST-PROOF-021). Unsupported graph/schema/SQL shapes are inconclusive.

Usage: python3 stl_ref_check.py transform.json [more.json ...]
Exits 1 on unresolved references, 2 on unsupported shapes, or 0 on a clean check.
"""
from __future__ import annotations

import argparse
import html
import json
import re
import sys

from stl_graph import validate_graph

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

class UnsupportedShape(ValueError):
    """The offline checker cannot establish a complete column model."""


TOKEN = re.compile(r"""(?P<space>\s+)|(?P<comment>--[^\n]*(?:\n|$)|/\*.*?\*/)|(?P<string>'(?:''|[^'])*')|(?P<quoted>"(?:""|[^"])*")|(?P<number>\b\d+(?:\.\d*)?(?:[eE][+-]?\d+)?\b)|(?P<ident>[A-Za-z_][A-Za-z0-9_]*)|(?P<punct>[().,+*/%<>=!|&:;-])""", re.DOTALL)


def references(expression):
    tokens, position = [], 0
    while position < len(expression):
        match = TOKEN.match(expression, position)
        if match is None:
            raise UnsupportedShape(f'unsupported SQL token near {expression[position:position + 20]!r}')
        position = match.end()
        if match.lastgroup not in {'space', 'comment', 'string', 'number'}:
            tokens.append((match.lastgroup, match.group()))
    found = []
    index = 0
    while index < len(tokens):
        kind, value = tokens[index]
        if kind not in {'ident', 'quoted'}:
            index += 1
            continue
        name = value[1:-1].replace('""', '"') if kind == 'quoted' else value
        # Also accept separately quoted qualification: "right"."Field".
        while index + 2 < len(tokens) and tokens[index + 1][1] == '.' and tokens[index + 2][0] in {'ident', 'quoted'}:
            index += 2
            next_kind, next_value = tokens[index]
            name += '.' + (next_value[1:-1].replace('""', '"') if next_kind == 'quoted' else next_value)
            kind = 'quoted'
        function = index + 1 < len(tokens) and tokens[index + 1][1] == '('
        if kind == 'quoted' or (name.lower() not in SQL_TOKENS and not function):
            found.append((name, 'qualified' if '.' in name else ('quoted' if kind == 'quoted' else 'bare')))
        index += 1
    return found


def apply_schema(columns, schema):
    if not schema:
        return columns
    if not isinstance(schema, dict) or set(schema) - {'fields', 'slice'}:
        raise UnsupportedShape('unsupported schema shape')
    # schema.fields is type metadata, not a projection. load.parameters.fields
    # supplies the explicit input projection; schema.slice DROP removes columns.
    if 'slice' not in schema:
        return columns
    slice_ = schema['slice']
    if (not isinstance(slice_, dict) or set(slice_) - {'mode', 'fields', 'ignoreMissingFields'} or
            slice_.get('mode') != 'DROP' or not isinstance(slice_.get('fields'), list) or
            not all(isinstance(field, str) for field in slice_['fields'])):
        raise UnsupportedShape('only schema.slice DROP with explicit field names is supported')
    missing = set(slice_['fields']) - columns
    if missing and not slice_.get('ignoreMissingFields', False):
        raise UnsupportedShape(f'schema drops unknown fields: {sorted(missing)}')
    return columns - set(slice_['fields'])


def node_columns(nodes):
    """Map each node id to the set of column names it exposes downstream."""
    validate_graph(nodes)
    memo = {}

    def cols(nid):
        if nid in memo:
            return memo[nid]
        node = nodes[nid]
        action = node["action"]
        params = node.get("parameters") or {}
        srcs = node.get("sources") or []
        if action == "load":
            if 'fields' not in params:
                raise UnsupportedShape(f'{nid}: load requires supplied field metadata')
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
            fields = params.get('fields', [])
            if any('name' not in field for field in fields):
                raise UnsupportedShape(f'{nid}: typeCast source names are required')
            out = (cols(srcs[0]) - {field['name'] for field in fields}) | {
                field['newProperties']['name'] for field in fields}
        elif action in ("filter", "sqlFilter", "extractGrains", "deduplicate", "outputD360"):
            if action == 'extractGrains' and params.get('grainExtractions'):
                raise UnsupportedShape(f'{nid}: nonempty grain extractions require supplied schema support')
            out = cols(srcs[0])
        elif action == "join":
            qualifier = params.get("rightQualifier")
            right = cols(srcs[1])
            out = cols(srcs[0]) | (
                {f"{qualifier}.{c}" for c in right} if qualifier else right
            )
        elif action in ("append", "appendV2"):
            schemas = [cols(s) for s in srcs]
            if not schemas or any(schema != schemas[0] for schema in schemas):
                raise UnsupportedShape(f'{nid}: append with differing schemas is unsupported')
            out = set(schemas[0])
        else:
            raise UnsupportedShape(f'{nid}: unsupported action {action}')
        out = apply_schema(out, node.get('schema'))
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
            for ref, kind in references(expr):
                if ref not in upstream:
                    found.append((nid, field['name'], ref, kind))
    return found


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", help="transform body JSON file(s)")
    args = parser.parse_args()

    total = 0
    for path in args.paths:
        try:
            bad = unresolved(path)
        except (UnsupportedShape, ValueError, KeyError, IndexError) as exc:
            print(f'{path}: INCONCLUSIVE: {exc}', file=sys.stderr)
            return 2
        total += len(bad)
        print("%-46s unresolved=%d" % (path, len(bad)))
        for nid, fname, ref, kind in bad:
            print("    %-20s %-28s %-28s %s" % (nid, fname, ref, kind))
    return 1 if total else 0


if __name__ == "__main__":
    raise SystemExit(main())
