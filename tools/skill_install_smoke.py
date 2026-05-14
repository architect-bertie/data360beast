#!/usr/bin/env python3
"""Smoke-test the portable Data360 Beast skill-pack layout.

This validates the current repository or an installed skill-pack root without
network access. It checks manifest paths, skill files, docs, agent metadata,
local references, and scripts. It is intentionally stricter than a file list and
lighter than a full package install.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def load_manifest(root: Path) -> dict:
    manifest = root / "manifest.json"
    if not manifest.is_file():
        raise FileNotFoundError(f"missing manifest.json at {manifest}")
    return json.loads(manifest.read_text(encoding="utf-8"))


def check_path(root: Path, rel: str, issues: list[str]) -> None:
    if not (root / rel).exists():
        issues.append(f"missing path: {rel}")


def check_skill_links(root: Path, skill_rel: str, issues: list[str]) -> None:
    skill_path = root / skill_rel
    skill_dir = skill_path.parent
    text = skill_path.read_text(encoding="utf-8")
    if "---" not in text[:200]:
        issues.append(f"{skill_rel}: missing frontmatter")
    if not (skill_dir / "agents" / "openai.yaml").is_file():
        issues.append(f"{skill_rel}: missing agents/openai.yaml")
    for match in LINK_RE.finditer(text):
        target = match.group(1).split("#", 1)[0].strip()
        if not target or target.startswith(("http://", "https://", "mailto:")):
            continue
        if target.startswith("references/") or target.startswith("scripts/"):
            if not (skill_dir / target).exists():
                issues.append(f"{skill_rel}: broken local pointer {target}")
        elif target.startswith("../../docs/"):
            rel = target.removeprefix("../../")
            if not (root / rel).exists():
                issues.append(f"{skill_rel}: broken docs pointer {target}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="Repository or installed skill-pack root")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    manifest = load_manifest(root)
    issues: list[str] = []

    for rel in manifest.get("skills", []):
        check_path(root, rel, issues)
        if (root / rel).is_file():
            check_skill_links(root, rel, issues)

    for rel in manifest.get("docs", []):
        check_path(root, rel, issues)

    for artifact in manifest.get("proofArtifacts", {}).values():
        check_path(root, artifact, issues)

    stats = manifest.get("stats", {})
    if stats.get("specialistSkills") != 17:
        issues.append("manifest stats.specialistSkills must be 17")
    if stats.get("phaseProofMatrixEntries") != 12:
        issues.append("manifest stats.phaseProofMatrixEntries must be 12")

    if issues:
        for issue in issues:
            print(f"FAIL: {issue}", file=sys.stderr)
        return 1
    print(f"OK: skill-pack smoke test passed at {root}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
