#!/usr/bin/env python3
"""Validate public deployment-grade expertise contracts."""

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    paths = [
        "docs/data360/schemas/implementation-spec.schema.json",
        "docs/data360/schemas/deployment-plan.schema.json",
        "docs/data360/schemas/run-state.schema.json",
        "docs/data360/schemas/certification-attestation.schema.json",
        "docs/data360/knowledge/ontology.json",
        "docs/data360/knowledge/claims.json",
        "docs/data360/knowledge/decisions.json",
        "docs/data360/packs/beastwear.json",
        "docs/architecture-evals.json",
    ]
    issues = []
    for rel in paths:
        try:
            json.loads((ROOT / rel).read_text(encoding="utf-8"))
        except Exception as exc:
            issues.append(f"invalid or missing {rel}: {exc}")
    claims = json.loads((ROOT / "docs/data360/knowledge/claims.json").read_text(encoding="utf-8")).get("claims", [])
    if not claims:
        issues.append("knowledge claims cannot be empty")
    if any("token" in json.dumps(claim).lower() for claim in claims):
        issues.append("knowledge claims contain prohibited credential-like content")
    result = subprocess.run([sys.executable, "tools/run_architecture_evals.py"], cwd=ROOT, text=True, capture_output=True)
    if result.returncode:
        issues.append(result.stdout + result.stderr)
    if issues:
        for issue in issues:
            print(f"FAIL: {issue}", file=sys.stderr)
        return 1
    print(f"OK: expertise contracts passed with {len(claims)} public claims")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
