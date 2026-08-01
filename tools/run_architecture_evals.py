#!/usr/bin/env python3
"""Validate the Data360 Beast architecture benchmark contract."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    payload = json.loads((ROOT / "docs" / "architecture-evals.json").read_text(encoding="utf-8"))
    phases = payload.get("phases", [])
    patterns = payload.get("patterns", [])
    count = len(phases) * len(patterns)
    if len(phases) != 12 or len(patterns) != 6 or count != 72:
        raise SystemExit("FAIL: architecture eval contract must generate exactly 72 cases")
    print(f"OK: architecture eval contract generates {count} cases")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
