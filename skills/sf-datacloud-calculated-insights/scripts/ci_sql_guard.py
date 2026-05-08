#!/usr/bin/env python3
import argparse
import json
import re
import sys
from pathlib import Path


AGG_FUNCS = [
    "SUM",
    "AVG",
    "MIN",
    "MAX",
    "COUNT",
    "MEAN",
    "RANK",
    "DENSE_RANK",
    "PERCENT_RANK",
    "NTILE",
    "APPROX_COUNT_DISTINCT",
    "PERCENTILE",
    "STDDEV",
]

NON_AGGREGATABLE_HINTS = [
    "RANK",
    "DENSE_RANK",
    "PERCENT_RANK",
    "NTILE",
    "LEAD",
    "LAG",
    "ROW_NUMBER",
    "APPROX_COUNT_DISTINCT",
    "PERCENTILE",
    "STDDEV",
]


def strip_comments(sql: str) -> str:
    sql = re.sub(r"/\*.*?\*/", " ", sql, flags=re.S)
    sql = re.sub(r"--.*?$", " ", sql, flags=re.M)
    return sql


def normalize(sql: str) -> str:
    return re.sub(r"\s+", " ", strip_comments(sql)).strip()


def top_level_positions(sql: str, phrase: str) -> list[int]:
    positions = []
    depth = 0
    i = 0
    phrase_upper = phrase.upper()
    sql_upper = sql.upper()
    while i < len(sql_upper):
        char = sql_upper[i]
        if char == "'":
            i += 1
            while i < len(sql_upper):
                if sql_upper[i] == "'" and (i + 1 >= len(sql_upper) or sql_upper[i + 1] != "'"):
                    i += 1
                    break
                i += 2 if sql_upper[i] == "'" and i + 1 < len(sql_upper) and sql_upper[i + 1] == "'" else 1
            continue
        if char == "(":
            depth += 1
        elif char == ")":
            depth = max(0, depth - 1)
        elif depth == 0 and sql_upper.startswith(phrase_upper, i):
            before = sql_upper[i - 1] if i > 0 else " "
            after_index = i + len(phrase_upper)
            after = sql_upper[after_index] if after_index < len(sql_upper) else " "
            if not (before.isalnum() or before == "_") and not (after.isalnum() or after == "_"):
                positions.append(i)
        i += 1
    return positions


def count_aliases(sql: str) -> list[str]:
    return re.findall(r"\bAS\s+([A-Za-z_][A-Za-z0-9_]*__c)\b", sql, flags=re.I)


def main() -> int:
    parser = argparse.ArgumentParser(description="Static guardrails for Data 360 Calculated Insight SQL.")
    parser.add_argument("sql_file", help="Path to a SQL file")
    args = parser.parse_args()

    raw = Path(args.sql_file).read_text(encoding="utf-8")
    sql = normalize(raw)
    upper = sql.upper()
    findings = []

    def add(severity: str, code: str, message: str):
        findings.append({"severity": severity, "code": code, "message": message})

    if len(raw) > 131021:
        add("blocker", "SQL_TOO_LONG", "Calculated Insight SQL limit is 131,021 characters.")

    if not re.search(r"\bSELECT\b", upper) or not re.search(r"\bFROM\b", upper):
        add("blocker", "MISSING_SELECT_FROM", "CI SQL must include SELECT and FROM.")

    if not re.search(r"\bGROUP\s+BY\b", upper):
        add("blocker", "MISSING_GROUP_BY", "CI SQL should group by all dimensions.")

    if re.search(r"\bSELECT\s+DISTINCT\b", upper):
        add("blocker", "TOP_LEVEL_DISTINCT", "Top-level DISTINCT is not allowed in CI SQL.")

    if re.search(r"\bCOUNT\s*\(\s*\*\s*\)", upper):
        add("blocker", "COUNT_STAR", "COUNT(*) is not supported; count a concrete field.")

    if top_level_positions(sql, "ORDER BY"):
        add("blocker", "ORDER_BY", "Top-level ORDER BY is not allowed in Calculated Insight SQL.")

    if not any(re.search(rf"\b{func}\s*\(", upper) for func in AGG_FUNCS):
        add("blocker", "NO_MEASURE", "A calculated insight must include at least one aggregate measure.")

    if re.search(r"\b(SUM|AVG|MIN|MAX|COUNT|MEAN)\s*\([^)]*\b(SUM|AVG|MIN|MAX|COUNT|MEAN)\s*\(", upper):
        add("blocker", "NESTED_AGGREGATE", "Nested aggregate functions are not allowed.")

    where_match = re.search(r"\bWHERE\b(.*?)(\bGROUP\s+BY\b|\bORDER\s+BY\b|$)", upper)
    if where_match and re.search(r"\b(SUM|AVG|MIN|MAX|COUNT|MEAN|APPROX_COUNT_DISTINCT)\s*\(", where_match.group(1)):
        add("blocker", "AGGREGATE_IN_WHERE", "WHERE cannot contain aggregate expressions.")

    aliases = count_aliases(sql)
    if len(aliases) > 60:
        add("warning", "MANY_ALIASES", "Review dimensions/measures; CI limits are 10 dimensions and 50 measures.")

    used_non_agg = [func for func in NON_AGGREGATABLE_HINTS if re.search(rf"\b{func}\s*\(", upper)]
    if used_non_agg:
        add(
            "warning",
            "NON_AGGREGATABLE_MEASURE",
            "Non-aggregatable functions detected: " + ", ".join(sorted(set(used_non_agg))) + ". Preserve all dimensions downstream.",
        )

    if re.search(r"\bCONVERT_CURRENCY\s*\(", upper) and not re.search(r"\bTRY_CONVERT_CURRENCY\s*\(", upper):
        add("warning", "CURRENCY_CONVERSION", "Prefer TRY_CONVERT_CURRENCY for CI currency measures.")

    result = {
        "file": args.sql_file,
        "characters": len(raw),
        "aliases": aliases,
        "findingCount": len(findings),
        "blockerCount": sum(1 for item in findings if item["severity"] == "blocker"),
        "findings": findings,
    }
    print(json.dumps(result, indent=2))
    return 1 if result["blockerCount"] else 0


if __name__ == "__main__":
    sys.exit(main())
