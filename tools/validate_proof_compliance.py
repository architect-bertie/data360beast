#!/usr/bin/env python3
"""Validate Data360 Beast skill-pack proof-contract compliance.

Reads `manifest.json`, `docs/phase-proof-matrix.json`, and every SKILL.md the
manifest declares, then checks each one against four classes of rule:

1. REQUIRED references: every SKILL.md must cite the four proof-contract
   artifacts (`docs/phase-proof-matrix.json`, `docs/beast-preflight.md`,
   `docs/proof-ledger.md`, `docs/data360/limits-source-precedence.md`).
2. REQUIRED file pointers: every `references/*.md` and `scripts/*.py` link
   inside a SKILL.md must resolve on disk.
3. REQUIRED banned phrases: the terminology guardrails declared in
   `docs/data360/docs-watch-operating-model.md` must not appear in any SKILL.md.
4. WARNING heading conformance: each specialist skill should expose at least
   one of the canonical heading variants per category (Production Workflow,
   Validation Gates, Handoff, Output Format). Router and orchestrator skills
   are exempt.

Outputs `tools/proof-compliance-report.json` and
`tools/proof-compliance-report.md` (both gitignored). Exits non-zero on any
REQUIRED failure.
"""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "manifest.json"
MATRIX = ROOT / "docs" / "phase-proof-matrix.json"
OUT_JSON = ROOT / "tools" / "proof-compliance-report.json"
OUT_MD = ROOT / "tools" / "proof-compliance-report.md"

ROUTER_SKILLS = {"data360beast", "sf-datacloud"}

REQUIRED_REFERENCES = {
    "phase-proof-matrix": "docs/phase-proof-matrix.json",
    "beast-preflight": "docs/beast-preflight.md",
    "proof-ledger": "docs/proof-ledger.md",
    "limits-source-precedence": "docs/data360/limits-source-precedence.md",
}

# Sourced from docs/data360/docs-watch-operating-model.md §"Terminology Guardrails".
BANNED_PHRASES = (
    "golden path",
    "customer journey",
    "step-by-step",
    "build a complete",
    "solution accelerator",
    "raw payload",
    "raw readback",
)

HEADING_CATEGORIES: dict[str, tuple[str, ...]] = {
    "workflow": (
        "## production workflow",
        "## default workflow",
        "## production gates",
        "## org-adapted workflow",
        "## first routing decision",
    ),
    "validation": (
        "## validation gates",
        "## validation gate",
        "## quality gates",
        "## recommended verification",
        "## failure-risk self evaluation",
    ),
    "handoff": (
        "## handoff",
        "## handoffs",
        "## governance handoff",
    ),
    "output": (
        "## output format",
    ),
}

LINK_FILE_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
HEADING_RE = re.compile(r"^##\s+.+$", re.MULTILINE)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def skill_name_from_path(rel_path: str) -> str:
    return Path(rel_path).parent.name


def check_required_references(text: str) -> list[str]:
    missing = []
    for label, target in REQUIRED_REFERENCES.items():
        if target not in text:
            missing.append(f"{label} ({target})")
    return missing


def check_banned_phrases(text: str) -> list[str]:
    lowered = text.lower()
    return [phrase for phrase in BANNED_PHRASES if phrase in lowered]


def check_local_pointers(skill_md: Path, text: str) -> list[str]:
    """Return broken local references/scripts pointers (not docs/ links)."""
    skill_dir = skill_md.parent
    broken = []
    for match in LINK_FILE_RE.finditer(text):
        target = match.group(1).split("#", 1)[0].strip()
        if not target or target.startswith(("http://", "https://", "mailto:")):
            continue
        if not (target.startswith("references/") or target.startswith("scripts/")):
            continue
        resolved = (skill_dir / target).resolve()
        if not resolved.exists():
            broken.append(target)
    return broken


def check_heading_conformance(text: str) -> list[str]:
    """Return categories that have no matching heading variant."""
    lowered = text.lower()
    missing_categories = []
    for category, variants in HEADING_CATEGORIES.items():
        if not any(variant in lowered for variant in variants):
            missing_categories.append(category)
    return missing_categories


def evaluate_skill(rel_path: str) -> dict[str, Any]:
    skill_md = ROOT / rel_path
    name = skill_name_from_path(rel_path)
    is_router = name in ROUTER_SKILLS

    if not skill_md.is_file():
        return {
            "skill": name,
            "path": rel_path,
            "isRouter": is_router,
            "exists": False,
            "missingReferences": list(REQUIRED_REFERENCES.keys()),
            "bannedPhrases": [],
            "brokenLocalPointers": [],
            "missingHeadings": [],
        }

    text = skill_md.read_text(encoding="utf-8")
    return {
        "skill": name,
        "path": rel_path,
        "isRouter": is_router,
        "exists": True,
        "missingReferences": check_required_references(text),
        "bannedPhrases": check_banned_phrases(text),
        "brokenLocalPointers": check_local_pointers(skill_md, text),
        "missingHeadings": [] if is_router else check_heading_conformance(text),
    }


def cross_check_matrix(skill_results: list[dict[str, Any]], matrix: dict[str, Any]) -> list[str]:
    declared = {phase["specialistSkill"] for phase in matrix.get("phases", [])}
    skills_present = {result["skill"] for result in skill_results}
    issues = []
    for declared_skill in declared:
        if declared_skill not in skills_present:
            issues.append(
                f"phase-proof-matrix.json declares specialistSkill `{declared_skill}` "
                "but manifest.json does not list a matching SKILL.md."
            )
    return issues


def write_reports(report: dict[str, Any]) -> None:
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    lines: list[str] = []
    lines.append("# Proof Compliance Report")
    lines.append("")
    lines.append(f"_Generated {report['generatedAt']}._")
    lines.append("")
    summary = report["summary"]
    lines.append(
        f"**Skills checked:** {summary['skillsChecked']} | "
        f"**Required failures:** {summary['requiredFailures']} | "
        f"**Warnings:** {summary['warnings']}"
    )
    lines.append("")
    if report.get("matrixIssues"):
        lines.append("## Matrix vs manifest issues (REQUIRED)")
        lines.append("")
        for issue in report["matrixIssues"]:
            lines.append(f"- {issue}")
        lines.append("")

    lines.append("## Per-skill results")
    lines.append("")
    lines.append("| Skill | Refs | Banned | Broken pointers | Missing headings |")
    lines.append("|---|---|---|---|---|")
    for result in report["skills"]:
        refs = "ok" if not result["missingReferences"] else ", ".join(result["missingReferences"])
        banned = "ok" if not result["bannedPhrases"] else ", ".join(result["bannedPhrases"])
        broken = "ok" if not result["brokenLocalPointers"] else ", ".join(result["brokenLocalPointers"])
        headings = "ok" if not result["missingHeadings"] else ", ".join(result["missingHeadings"])
        lines.append(
            f"| `{result['skill']}` | {refs} | {banned} | {broken} | {headings} |"
        )
    lines.append("")
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    manifest = load_json(MANIFEST)
    matrix = load_json(MATRIX)

    skill_results = [evaluate_skill(rel) for rel in manifest.get("skills", [])]
    matrix_issues = cross_check_matrix(skill_results, matrix)

    required_failures = sum(
        1
        for r in skill_results
        if r["missingReferences"] or r["bannedPhrases"] or r["brokenLocalPointers"] or not r["exists"]
    )
    warnings = sum(1 for r in skill_results if r["missingHeadings"])

    report = {
        "generatedAt": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "summary": {
            "skillsChecked": len(skill_results),
            "requiredFailures": required_failures + len(matrix_issues),
            "warnings": warnings,
        },
        "matrixIssues": matrix_issues,
        "skills": skill_results,
    }

    write_reports(report)

    if required_failures or matrix_issues:
        print(
            f"FAIL: {required_failures} skill(s) missing required content, "
            f"{len(matrix_issues)} matrix issue(s). See {OUT_MD.relative_to(ROOT)}.",
            file=sys.stderr,
        )
        return 1

    print(
        f"OK: {len(skill_results)} skills compliant. {warnings} warning(s). "
        f"Report: {OUT_MD.relative_to(ROOT)}."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
