#!/usr/bin/env python3
import argparse
import json
import re
from pathlib import Path
from typing import Any


QUALITY_TERMS = {
    "grain": ["grain", "one row", "per ", "level"],
    "source": ["source", "origin", "mapped from"],
    "freshness": ["refresh", "updated", "cadence", "latency"],
    "governance": ["pii", "sensitive", "mask", "permission", "governance", "safe"],
    "metric": ["formula", "measure", "dimension", "window", "aggregation", "unit"],
    "values": ["valid values", "enum", "possible values", "null", "blank", "unit"],
    "agent": ["agent", "use when", "do not expose", "user-facing", "business meaning"],
}


def walk(value: Any, path: str = "$"):
    if isinstance(value, dict):
        yield path, value
        for key, child in value.items():
            yield from walk(child, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from walk(child, f"{path}[{index}]")


def text_from(item: dict[str, Any], keys: list[str]) -> str:
    values = []
    for key in keys:
        raw = item.get(key)
        if isinstance(raw, str):
            values.append(raw)
    return " ".join(values).strip()


def score_description(text: str) -> tuple[int, list[str]]:
    if not text:
        return 0, ["missing"]
    lowered = text.lower()
    found = [name for name, terms in QUALITY_TERMS.items() if any(term in lowered for term in terms)]
    word_count = len(re.findall(r"\w+", text))
    score = 1
    if word_count >= 8:
        score = 2
    if len(found) >= 2:
        score = 3
    if len(found) >= 4 and word_count >= 20:
        score = 4
    if len(found) >= 6 and word_count >= 35:
        score = 5
    return score, found


def main() -> int:
    parser = argparse.ArgumentParser(description="Score Data 360 metadata descriptions for agentic readiness.")
    parser.add_argument("metadata_json", help="Metadata JSON exported from Data 360 metadata/profile/insight APIs")
    parser.add_argument("--limit", type=int, default=50)
    args = parser.parse_args()

    data = json.loads(Path(args.metadata_json).read_text(encoding="utf-8"))
    rows = []
    for path, item in walk(data):
        if not isinstance(item, dict):
            continue
        label = text_from(item, ["label", "displayName", "name", "apiName", "developerName"])
        description = text_from(item, ["description", "fieldDescription", "businessDescription", "helpText"])
        if not label and not description:
            continue
        score, signals = score_description(description)
        rows.append(
            {
                "path": path,
                "label": label,
                "score": score,
                "signals": signals,
                "description": description,
            }
        )

    rows.sort(key=lambda row: (row["score"], row["label"]))
    summary = {
        "itemCount": len(rows),
        "averageScore": round(sum(row["score"] for row in rows) / len(rows), 2) if rows else 0,
        "productionTarget": ">=4 for agent-facing objects/fields and 5 for metrics",
        "lowestScoring": rows[: args.limit],
    }
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
