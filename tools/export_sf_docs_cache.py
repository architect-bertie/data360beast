#!/usr/bin/env python3
"""Export cached Salesforce docs into project Markdown and compact indexes."""

from __future__ import annotations

import argparse
import json
import re
import sqlite3
from pathlib import Path
from typing import Iterable


DEFAULT_DB = Path("/Users/bertie/.codex/mcp-servers/sf-docs-mcp/sf-docs-cache.db")
DEFAULT_OUT = Path("docs/data360/help")


def article_id(url: str) -> str:
    match = re.search(r"[?&]id=([^&]+)", url)
    return match.group(1) if match else "unknown"


def slug(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", value).removesuffix(".htm")


def extract_links(markdown: str) -> list[str]:
    links = []
    for match in re.finditer(r"\]\((https://help\.salesforce\.com/[^)]+)\)", markdown):
        url = match.group(1)
        if "id=data.c360" in url or "id=sf.c360" in url or "id=data.cdp" in url:
            links.append(url)
    return sorted(set(links))


def compact_summary(markdown: str) -> dict[str, list[str] | str]:
    lines = [
        line.strip()
        for line in markdown.splitlines()
        if line.strip()
        and not line.strip().startswith("![")
        and not line.strip().startswith("You are here")
        and not re.match(r"^\d+\.\s+\[", line.strip())
        and line.strip() not in {"Note", "Important", "Warning", "Tip", "Example"}
    ]
    lead = ""
    for line in lines:
        if not line.startswith("#") and not line.startswith("- ") and not line.startswith("|"):
            lead = re.sub(r"\s+", " ", line)
            break
    headings = [line.removeprefix("## ").strip() for line in lines if line.startswith("## ")][:20]
    bullets = [line.removeprefix("- ").strip() for line in lines if line.startswith("- ")][:20]
    return {"lead": lead, "headings": headings, "bullets": bullets}


def rows(conn: sqlite3.Connection, pattern: str) -> Iterable[sqlite3.Row]:
    conn.row_factory = sqlite3.Row
    query = """
        SELECT url, title, markdown, pageType, extractedAt
        FROM cache
        WHERE url LIKE '%help.salesforce.com%'
          AND url LIKE ?
        ORDER BY title
    """
    yield from conn.execute(query, (pattern,))

def dedupe_rows(latest_first: Iterable[sqlite3.Row]) -> list[sqlite3.Row]:
    """Return at most one row per Help article id.

    The sf-docs cache can contain multiple URLs for the same article id (for
    example, Apex vs. articleView variants). Prefer the most recently extracted
    row when duplicates exist.
    """
    by_id: dict[str, sqlite3.Row] = {}
    for row in latest_first:
        aid = article_id(row["url"])
        if aid == "unknown":
            continue
        if aid not in by_id:
            by_id[aid] = row
    return sorted(by_id.values(), key=lambda r: (r["title"] or "").lower())


def export_cache(db: Path, outdir: Path, pattern: str) -> None:
    outdir.joinpath("raw").mkdir(parents=True, exist_ok=True)
    outdir.joinpath("summaries").mkdir(parents=True, exist_ok=True)
    manifest = []
    with sqlite3.connect(db) as conn:
        # Read all matching rows then dedupe by article id, preferring the most
        # recently extracted entry.
        fetched = list(rows(conn, pattern))
        fetched.sort(key=lambda r: (r["extractedAt"] or ""), reverse=True)
        for row in dedupe_rows(fetched):
            aid = article_id(row["url"])
            name = slug(aid)
            raw_path = outdir / "raw" / f"{name}.md"
            summary_path = outdir / "summaries" / f"{name}.json"
            markdown = row["markdown"]
            frontmatter = "\n".join(
                [
                    "---",
                    f"title: {json.dumps(row['title'])}",
                    f"source: {json.dumps(row['url'])}",
                    f"articleId: {json.dumps(aid)}",
                    f"pageType: {json.dumps(row['pageType'])}",
                    f"extractedAt: {json.dumps(row['extractedAt'])}",
                    "---",
                    "",
                ]
            )
            raw_path.write_text(frontmatter + markdown + "\n", encoding="utf-8")
            summary = compact_summary(markdown)
            links = extract_links(markdown)
            summary_payload = {
                "title": row["title"],
                "source": row["url"],
                "articleId": aid,
                "rawPath": str(raw_path),
                "markdownChars": len(markdown),
                "links": links,
                "summary": summary,
            }
            summary_path.write_text(json.dumps(summary_payload, indent=2) + "\n", encoding="utf-8")
            manifest.append(summary_payload)

    manifest_path = outdir / "cache-manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    index = [
        "# Data 360 Help Cache Export",
        "",
        f"Exported articles: {len(manifest)}",
        "",
        "| Title | Article ID | Chars | Source |",
        "| --- | --- | --- | --- |",
    ]
    for item in sorted(manifest, key=lambda entry: entry["title"].lower()):
        title = item["title"].replace("|", "\\|")
        index.append(
            f"| {title} | {item['articleId']} | {item['markdownChars']} | {item['source']} |"
        )
    index.append("")
    (outdir / "cache-index.md").write_text("\n".join(index), encoding="utf-8")
    print(f"Exported {len(manifest)} cached Salesforce Help articles to {outdir}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", type=Path, default=DEFAULT_DB)
    parser.add_argument("--outdir", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--pattern", default="%c360%")
    args = parser.parse_args()
    export_cache(args.db, args.outdir, args.pattern)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
