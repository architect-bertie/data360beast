#!/usr/bin/env python3
"""Run deterministic Data360 Beast prompt eval checks.

This runner validates the fixture file and, when supplied with an answers
directory, checks each answer for required proof-habit terms and known bad
shortcuts. It intentionally does not call an LLM; CI or an agent workflow can
generate answer files, then this script grades the public-safe text.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_FIXTURES = ROOT / "docs" / "beast-evals.json"
OUT_JSON = ROOT / "tools" / "beast-eval-report.json"
OUT_MD = ROOT / "tools" / "beast-eval-report.md"

CONFIDENCE_TERMS = ("documented", "tested", "inferred", "docs-unverified", "live-validation-unavailable")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def normalize(text: str) -> str:
    return " ".join(text.lower().split())


def answer_path(answers_dir: Path, eval_id: str) -> Path | None:
    for suffix in (".md", ".txt"):
        candidate = answers_dir / f"{eval_id}{suffix}"
        if candidate.is_file():
            return candidate
    return None


def evaluate_answer(eval_case: dict[str, Any], answer: str | None) -> dict[str, Any]:
    if answer is None:
        return {
            "id": eval_case["id"],
            "status": "not_run",
            "missingRequiredGroups": [],
            "forbiddenHits": [],
            "confidenceHit": False,
        }

    text = normalize(answer)
    missing_groups = []
    for group in eval_case.get("mustMentionAny", []):
        if not any(term.lower() in text for term in group):
            missing_groups.append(group)

    forbidden_hits = [term for term in eval_case.get("mustNotMention", []) if term.lower() in text]
    confidence_hit = True
    if eval_case.get("confidenceRequired", False):
        confidence_hit = any(term in text for term in CONFIDENCE_TERMS)

    status = "pass" if not missing_groups and not forbidden_hits and confidence_hit else "fail"
    return {
        "id": eval_case["id"],
        "status": status,
        "missingRequiredGroups": missing_groups,
        "forbiddenHits": forbidden_hits,
        "confidenceHit": confidence_hit,
    }


def validate_fixtures(fixtures: dict[str, Any]) -> list[str]:
    issues = []
    seen = set()
    for index, eval_case in enumerate(fixtures.get("evals", []), start=1):
        eval_id = eval_case.get("id")
        if not eval_id:
            issues.append(f"eval #{index} is missing id")
            continue
        if eval_id in seen:
            issues.append(f"duplicate eval id: {eval_id}")
        seen.add(eval_id)
        if not eval_case.get("prompt"):
            issues.append(f"{eval_id}: missing prompt")
        if not eval_case.get("mustMentionAny"):
            issues.append(f"{eval_id}: missing mustMentionAny")
    return issues


def write_report(report: dict[str, Any]) -> None:
    OUT_JSON.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# Beast Eval Report",
        "",
        f"_Generated {report['generatedAt']}._",
        "",
        f"Mode: `{report['mode']}`",
        "",
        "| Eval | Status | Missing groups | Forbidden hits | Confidence |",
        "|---|---|---|---|---|",
    ]
    for result in report["results"]:
        missing = "ok" if not result["missingRequiredGroups"] else "; ".join(
            " / ".join(group) for group in result["missingRequiredGroups"]
        )
        forbidden = "ok" if not result["forbiddenHits"] else ", ".join(result["forbiddenHits"])
        confidence = "ok" if result["confidenceHit"] else "missing"
        lines.append(f"| `{result['id']}` | {result['status']} | {missing} | {forbidden} | {confidence} |")
    lines.append("")
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixtures", default=str(DEFAULT_FIXTURES), help="Path to beast-evals.json")
    parser.add_argument("--answers-dir", help="Directory containing <eval-id>.md or <eval-id>.txt answers")
    args = parser.parse_args()

    fixtures_path = Path(args.fixtures)
    fixtures = load_json(fixtures_path)
    fixture_issues = validate_fixtures(fixtures)
    if fixture_issues:
        for issue in fixture_issues:
            print(f"fixture error: {issue}", file=sys.stderr)
        return 1

    answers_dir = Path(args.answers_dir) if args.answers_dir else None
    results = []
    for eval_case in fixtures["evals"]:
        answer = None
        if answers_dir:
            path = answer_path(answers_dir, eval_case["id"])
            answer = path.read_text(encoding="utf-8") if path else ""
        results.append(evaluate_answer(eval_case, answer))

    mode = "answers" if answers_dir else "fixture-validation"
    report = {
        "generatedAt": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "mode": mode,
        "fixtures": str(fixtures_path),
        "answersDir": str(answers_dir) if answers_dir else None,
        "summary": {
            "total": len(results),
            "passed": sum(1 for result in results if result["status"] == "pass"),
            "failed": sum(1 for result in results if result["status"] == "fail"),
            "notRun": sum(1 for result in results if result["status"] == "not_run"),
        },
        "results": results,
    }
    write_report(report)

    failed = report["summary"]["failed"]
    if failed:
        print(f"FAIL: {failed} eval answer(s) failed. See {OUT_MD.relative_to(ROOT)}.", file=sys.stderr)
        return 1
    print(f"OK: {mode} complete. See {OUT_MD.relative_to(ROOT)}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
