#!/usr/bin/env python3
"""Validate release hygiene for Data360 Beast."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
    agent_manifest = json.loads((ROOT / "docs" / "agent-manifest.json").read_text(encoding="utf-8"))
    changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    issues: list[str] = []

    version = manifest.get("version")
    if not version:
        issues.append("manifest.json missing version")
    if "## [Unreleased]" not in changelog:
        issues.append("CHANGELOG.md missing Unreleased section")
    if str(manifest.get("stats", {}).get("overallScore")) != str(agent_manifest.get("scores", {}).get("overall")):
        issues.append("manifest overallScore and docs/agent-manifest overall diverge")
    if manifest.get("lastReviewed") != agent_manifest.get("lastReviewed"):
        issues.append("manifest lastReviewed and docs/agent-manifest lastReviewed diverge")
    for rel in manifest.get("docs", []):
        if not (ROOT / rel).exists():
            issues.append(f"manifest docs entry missing: {rel}")
    for rel in manifest.get("skills", []):
        if not (ROOT / rel).exists():
            issues.append(f"manifest skills entry missing: {rel}")

    if issues:
        for issue in issues:
            print(f"FAIL: {issue}", file=sys.stderr)
        return 1
    print(f"OK: release readiness passed for version {version}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
