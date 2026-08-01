#!/usr/bin/env python3
"""Validate public-safety and structural contracts for docs-watch output."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASES = 12
APPROVED = {
    "golden path": {"docs/data360/docs-watch-operating-model.md", "docs/labs-interface.md"},
    "customer journey": {"docs/data360/docs-watch-operating-model.md", "docs/labs-interface.md"},
    "step-by-step": {"docs/data360/docs-watch-operating-model.md", "docs/labs-interface.md"},
    "build a complete": {"docs/data360/docs-watch-operating-model.md", "docs/labs-interface.md"},
    "solution accelerator": {"docs/data360/docs-watch-operating-model.md", "docs/labs-interface.md"},
}


def tracked_files() -> list[str]:
    result = subprocess.run(
        ["git", "ls-files"], cwd=ROOT, text=True, capture_output=True, check=True
    )
    return [line for line in result.stdout.splitlines() if line]


def fail(issues: list[str], message: str) -> None:
    issues.append(message)


def validate_json(issues: list[str]) -> None:
    for rel in tracked_files():
        if not rel.endswith(".json"):
            continue
        try:
            json.loads((ROOT / rel).read_text(encoding="utf-8"))
        except Exception as exc:
            fail(issues, f"invalid JSON {rel}: {exc}")
    for rel in ("docs/data360/docs-knowledge-graph.json", "docs/data360/docs-watch-reconciliation.json"):
        path = ROOT / rel
        if not path.is_file():
            fail(issues, f"missing docs-watch artifact: {rel}")


def validate_structure(issues: list[str]) -> None:
    matrix = json.loads((ROOT / "docs" / "phase-proof-matrix.json").read_text(encoding="utf-8"))
    if len(matrix.get("phases", [])) != PHASES:
        fail(issues, f"phase-proof-matrix must contain exactly {PHASES} phases")
    graph_path = ROOT / "docs/data360/docs-knowledge-graph.json"
    if graph_path.is_file():
        graph = json.loads(graph_path.read_text(encoding="utf-8"))
        node_types = {node.get("type") for node in graph.get("nodes", [])}
        for expected in {"official-page", "topic", "phase", "specialist-skill"}:
            if expected not in node_types:
                fail(issues, f"knowledge graph missing node type: {expected}")
        graph_phases = {node.get("key") for node in graph.get("nodes", []) if node.get("type") == "phase"}
        matrix_phases = {phase.get("phase") for phase in matrix.get("phases", [])}
        if not matrix_phases.issubset(graph_phases):
            fail(issues, "knowledge graph does not represent all proof phases")

    contract = json.loads((ROOT / "docs/data360/sf-skills-data360-companion.json").read_text(encoding="utf-8"))
    names = [item.get("upstreamName") for item in contract.get("companionSkills", [])]
    if len(names) != 9 or len(set(names)) != 9:
        fail(issues, "companion contract must contain exactly nine unique skills")
    markdown = (ROOT / "docs/data360/sf-skills-data360-companion.md").read_text(encoding="utf-8")
    for name in names:
        if name not in markdown:
            fail(issues, f"companion markdown missing approved skill: {name}")
    if (ROOT / "llms.txt").read_text(encoding="utf-8") != (ROOT / "docs/llms.txt").read_text(encoding="utf-8"):
        fail(issues, "root llms.txt and docs/llms.txt diverge")


def validate_boundary(issues: list[str]) -> None:
    diff = subprocess.run(["git", "diff", "HEAD", "--name-only"], cwd=ROOT, text=True, capture_output=True, check=True).stdout.splitlines()
    status = subprocess.run(["git", "status", "--short"], cwd=ROOT, text=True, capture_output=True, check=True).stdout.splitlines()
    untracked = [line[3:] for line in status if line.startswith("?? ") and line[3:] in {
        "tests/test_docs_watch.py",
        "tools/docs_watch.py",
        "tools/check_sf_skills_drift.py",
        "tools/validate_docs_watch.py",
        "docs/data360/docs-knowledge-graph.json",
        "docs/data360/docs-watch-reconciliation.json",
    }]
    files = sorted(set(diff + untracked))
    for rel in files:
        if rel in {"tools/validate_docs_watch.py", "docs/data360/docs-watch-operating-model.md", "docs/labs-interface.md"}:
            continue
        if rel in {"docs/data360/docs-knowledge-graph.json", "docs/data360/docs-watch-reconciliation.json"}:
            continue
        path = ROOT / rel
        if not path.is_file():
            continue
        if rel in diff:
            patch = subprocess.run(["git", "diff", "HEAD", "--unified=0", "--", rel], cwd=ROOT, text=True, capture_output=True, check=True).stdout
            text = "\n".join(line[1:] for line in patch.splitlines() if line.startswith("+") and not line.startswith("+++"))
        else:
            text = path.read_text(encoding="utf-8", errors="ignore")
        lower = text.lower()
        for phrase, allowed in APPROVED.items():
            if phrase in lower and rel not in allowed:
                fail(issues, f"prohibited Labs-style phrase '{phrase}' in {rel}")
        if re.search(r"-----BEGIN (?:RSA|EC|OPENSSH|PGP) PRIVATE KEY-----", text):
            fail(issues, f"credential material detected in {rel}")
        if re.search(r"(?:client_secret|access_token|refresh_token|password)\s*[:=]", lower):
            fail(issues, f"credential-like field detected in {rel}")
    for rel in ("CLAUDE.md", "CODEX.md"):
        if rel in files:
            text = (ROOT / rel).read_text(encoding="utf-8")
            if "AGENTS.md" not in text or len(text.splitlines()) > 40:
                fail(issues, f"{rel} is not a thin AGENTS.md shim")


def main() -> int:
    issues: list[str] = []
    validate_json(issues)
    validate_structure(issues)
    validate_boundary(issues)
    if issues:
        for issue in issues:
            print(f"FAIL: {issue}", file=sys.stderr)
        return 1
    print("OK: docs-watch structural and public-boundary validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
