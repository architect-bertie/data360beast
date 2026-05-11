#!/usr/bin/env python3
"""Audit indexed Data 360 Help and Developer docs for capture completeness."""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
HELP_DIR = ROOT / "docs" / "data360" / "help"
DEV_DIR = ROOT / "docs" / "data360" / "developer"
OUT_JSON = ROOT / "docs" / "data360" / "docs-watch-audit.json"
OUT_MD = ROOT / "docs" / "data360" / "docs-watch-audit.md"
PLACEHOLDER_RE = re.compile(r"Cannot populate due to large Document size", re.I)


def slug(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", value).removesuffix(".htm")


def read_json(path: Path, fallback: Any) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return fallback


def parse_help_index() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for line in (HELP_DIR / "index.md").read_text(encoding="utf-8").splitlines():
        if not line.startswith("|") or "http" not in line:
            continue
        parts = [part.strip() for part in line.strip("|").split("|")]
        if len(parts) < 4:
            continue
        rows.append({"title": parts[0], "articleId": parts[1], "source": parts[3]})
    return rows


def developer_rows() -> list[dict[str, str]]:
    manifest = read_json(DEV_DIR / "manifest.json", [])
    rows: list[dict[str, str]] = []
    for item in manifest:
        guide_path = item.get("guidePath") or ""
        rows.append(
            {
                "title": item.get("title") or "",
                "guidePath": guide_path,
                "source": item.get("source") or "",
                "rawPath": item.get("rawPath") or f"docs/data360/developer/raw/{Path(guide_path).stem}.md",
            }
        )
    return rows


def file_status(raw_path: Path, summary_path: Path) -> dict[str, Any]:
    raw_exists = raw_path.exists()
    summary_exists = summary_path.exists()
    chars = 0
    placeholder = False
    if raw_exists:
        text = raw_path.read_text(encoding="utf-8")
        chars = len(text)
        placeholder = bool(PLACEHOLDER_RE.search(text))
    if not raw_exists:
        status = "missing_raw"
    elif not summary_exists:
        status = "missing_summary"
    elif placeholder:
        status = "placeholder"
    elif chars < 500:
        status = "suspiciously_small"
    else:
        status = "captured"
    return {
        "status": status,
        "rawExists": raw_exists,
        "summaryExists": summary_exists,
        "chars": chars,
        "placeholder": placeholder,
    }


def audit_help() -> list[dict[str, Any]]:
    results = []
    for row in parse_help_index():
        name = slug(row["articleId"])
        raw_path = HELP_DIR / "raw" / f"{name}.md"
        summary_path = HELP_DIR / "summaries" / f"{name}.json"
        results.append(
            {
                **row,
                "rawPath": str(raw_path.relative_to(ROOT)),
                "summaryPath": str(summary_path.relative_to(ROOT)),
                **file_status(raw_path, summary_path),
            }
        )
    return results


def audit_developer() -> list[dict[str, Any]]:
    results = []
    for row in developer_rows():
        raw_path = ROOT / row["rawPath"]
        summary_path = DEV_DIR / "summaries" / f"{Path(row['guidePath']).stem}.json"
        results.append(
            {
                **row,
                "summaryPath": str(summary_path.relative_to(ROOT)),
                **file_status(raw_path, summary_path),
            }
        )
    return results


def counts(rows: list[dict[str, Any]]) -> dict[str, int]:
    out: dict[str, int] = {}
    for row in rows:
        status = row["status"]
        out[status] = out.get(status, 0) + 1
    return out


def render_md(payload: dict[str, Any]) -> str:
    help_counts = payload["summary"]["help"]
    dev_counts = payload["summary"]["developer"]
    problem_rows = [
        ("Help", row.get("articleId") or row.get("guidePath"), row)
        for row in payload["help"]
        if row["status"] != "captured"
    ]
    problem_rows.extend(
        ("Developer", row.get("guidePath"), row)
        for row in payload["developer"]
        if row["status"] != "captured"
    )
    lines = [
        "# Data360 Beast Docs Watch Audit",
        "",
        f"Generated: {payload['generatedAt']}",
        "",
        "## Summary",
        "",
        f"- Help indexed: {payload['summary']['helpIndexed']}",
        f"- Help status: {json.dumps(help_counts, sort_keys=True)}",
        f"- Developer indexed: {payload['summary']['developerIndexed']}",
        f"- Developer status: {json.dumps(dev_counts, sort_keys=True)}",
        "",
        "## Gaps",
        "",
    ]
    if not problem_rows:
        lines.append("- No missing, placeholder, or suspiciously small indexed docs.")
    else:
        for kind, identifier, row in problem_rows:
            lines.append(
                f"- {kind}: `{identifier}` -> {row['status']} ({row['chars']} chars)"
            )
    lines.extend(["", "## Notes", ""])
    lines.append(
        "- Oversized Help articles should be captured with `node tools/capture_help_prerendered.mjs --placeholders`, which uses official Help prerendered HTML."
    )
    lines.append(
        "- This audit checks indexed pages only; it does not claim coverage of every Salesforce Help or Developer page."
    )
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    help_results = audit_help()
    dev_results = audit_developer()
    payload = {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "summary": {
            "helpIndexed": len(help_results),
            "help": counts(help_results),
            "developerIndexed": len(dev_results),
            "developer": counts(dev_results),
        },
        "help": help_results,
        "developer": dev_results,
    }
    OUT_JSON.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    OUT_MD.write_text(render_md(payload), encoding="utf-8")
    print(f"Wrote audit to {OUT_MD.relative_to(ROOT)}")
    gaps = [
        row
        for row in [*help_results, *dev_results]
        if row["status"] not in {"captured"}
    ]
    if gaps:
        print(f"Found {len(gaps)} indexed documentation capture gaps.")
    else:
        print("All indexed documentation pages are captured.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
