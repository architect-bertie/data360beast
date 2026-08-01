#!/usr/bin/env python3
"""Run the Data360 Beast official documentation watch.

The command is intentionally repository-owned so the scheduled automation has
one deterministic entrypoint. Crawl outputs stay in a temporary directory;
only public indexes, graph metadata, reconciliation metadata, and approved
marker-delimited guidance are eligible for application.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
HELP_SEED = "https://help.salesforce.com/s/articleView?id=data.c360_a_product_considerations.htm&language=en_US&type=5"
DEV_SEED = "https://developer.salesforce.com/docs/data/data-cloud-dev/guide/dc-get-started.html"
HELP_CRAWLER = ROOT / "tools/sf_docs_help_crawl.mjs"
DEV_CRAWLER = ROOT / "tools/sf_docs_developer_guide_crawl.mjs"
APPROVED_STAGES = {
    ".gitignore",
    "manifest.json",
    "docs/agent-manifest.json",
    "docs/index.html",
    "docs/llms-full.txt",
    "docs/skills.md",
    "docs/proof-ledger.md",
    "docs/data360/help/index.md",
    "docs/data360/developer/index.md",
    "docs/data360/developer/learning-map.md",
    "docs/data360/docs-knowledge-graph.json",
    "docs/data360/docs-watch-reconciliation.json",
    "docs/data360/sf-skills-data360-companion.json",
    "docs/data360/sf-skills-data360-companion.md",
    "skills/data360beast/scripts/install_sf_skills_data360_companion.py",
    "tools/check_sf_skills_drift.py",
    "tools/docs_watch.py",
    "tools/refresh_skills_from_sf_docs.py",
    "tools/validate_docs_watch.py",
    "tests/test_docs_watch.py",
}
APPROVED_STAGES.update({
    f"skills/{name}/SKILL.md"
    for name in (
        "sf-datacloud", "sf-datacloud-act", "sf-datacloud-automation",
        "sf-datacloud-calculated-insights", "sf-datacloud-connectapi",
        "sf-datacloud-governance", "sf-datacloud-harmonize", "sf-datacloud-prepare",
        "sf-datacloud-retrieve", "sf-datacloud-segment", "sf-datacloud-unstructured-retrieval",
    )
})


def run(command: list[str], *, cwd: Path = ROOT, check: bool = True, timeout: int = 1800) -> subprocess.CompletedProcess[str]:
    print("$ " + " ".join(command))
    result = subprocess.run(command, cwd=cwd, text=True, capture_output=True, check=False, timeout=timeout)
    if result.stdout:
        print(result.stdout.strip())
    if result.returncode and result.stderr:
        print(result.stderr.strip(), file=sys.stderr)
    if check and result.returncode:
        error = subprocess.CalledProcessError(result.returncode, command, result.stdout, result.stderr)
        raise error
    return result


def node_command() -> list[str]:
    """Use the supported Node 22 runtime when fnm provides it."""
    if shutil.which("fnm"):
        return ["fnm", "exec", "--using", "v22.22.3", "node"]
    return ["node"]


def sha256(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def json_load(path: Path, fallback):
    if not path.exists():
        return fallback
    return json.loads(path.read_text(encoding="utf-8"))


def check_preflight() -> dict:
    if ROOT != Path("/Users/bertie/Documents/projects/data360beast"):
        raise RuntimeError(f"unexpected repository root: {ROOT}")
    if not (ROOT / ".git").exists():
        raise RuntimeError("repository metadata is missing")
    required = [HELP_CRAWLER, DEV_CRAWLER, ROOT / "tools/export_sf_docs_cache.py", ROOT / "skills/data360beast/scripts/install_sf_skills_data360_companion.py"]
    missing = [str(path.relative_to(ROOT)) for path in required if not path.exists()]
    if missing:
        raise RuntimeError("missing required repository tools: " + ", ".join(missing))
    for command in ("git", "python3", "node"):
        if shutil.which(command) is None:
            raise RuntimeError(f"required runtime is unavailable: {command}")
    remote = run(["git", "remote", "get-url", "origin"]).stdout.strip()
    if "github.com/architect-bertie/data360beast" not in remote:
        raise RuntimeError(f"unexpected origin: {remote}")
    sf_root = Path(os.environ.get("SF_DOCS_MCP_ROOT", Path.home() / ".data360beast/mcp-servers/sf-docs-mcp")).expanduser()
    extractor = sf_root / "dist/extractors/index.js"
    cache = Path(os.environ.get("SF_DOCS_CACHE_DB", sf_root / "sf-docs-cache.db")).expanduser()
    if not extractor.exists():
        raise RuntimeError(f"sf-docs extractor is unavailable: {extractor}")
    if not cache.exists():
        raise RuntimeError(f"sf-docs cache is unavailable: {cache}")
    binding = run(node_command() + ["-e", "require('better-sqlite3'); console.log(process.version)"], cwd=sf_root, check=False)
    if binding.returncode:
        raise RuntimeError("sf-docs better-sqlite3 binding is unavailable; rebuild it under the supported Node runtime")
    return {"root": str(ROOT), "origin": remote, "sfDocsRoot": str(sf_root), "sfDocsCache": str(cache)}


def manifest_records(path: Path, source_type: str) -> list[dict]:
    records = []
    for item in json_load(path, []):
        url = item.get("source") or item.get("url")
        if not url:
            continue
        parsed = urlparse(url)
        if parsed.hostname not in {"help.salesforce.com", "developer.salesforce.com"}:
            raise RuntimeError(f"non-official source returned by crawler: {url}")
        title = str(item.get("title") or "").strip()
        if not title or title.lower() == "untitled":
            raise RuntimeError(f"untitled source returned by crawler: {url}")
        summary = item.get("summary") or {}
        content = "\n".join([title, summary.get("lead", ""), *summary.get("topics", []), *summary.get("headings", []), *summary.get("bullets", [])])
        records.append({
            "id": f"page:{sha256(url)[:20]}",
            "source": url,
            "sourceType": source_type,
            "title": title,
            "identifier": item.get("articleId") or item.get("guidePath") or parsed.path,
            "depth": item.get("depth", 0),
            "parent": item.get("parent"),
            "contentHash": sha256(content),
            "status": "captured",
            "topics": sorted(set(summary.get("topics", []) + summary.get("headings", []) + summary.get("bullets", [])))[:24],
            "lead": summary.get("lead", "")[:500],
        })
    if not records:
        raise RuntimeError(f"crawler produced no {source_type} records: {path}")
    return records


def phase_data() -> list[dict]:
    matrix = json_load(ROOT / "docs/phase-proof-matrix.json", {})
    return matrix.get("phases", [])


def phase_matches(record: dict, phases: list[dict]) -> list[str]:
    text = " ".join([record["title"], record["lead"], *record["topics"]]).lower()
    keywords = {
        "connect": ("connect", "connector", "connection", "source"),
        "prepare": ("ingest", "stream", "transform", "dlo", "document"),
        "harmonize": ("dmo", "mapping", "identity", "relationship", "unify"),
        "govern": ("govern", "permission", "data space", "security", "policy"),
        "retrieve": ("query", "sql", "metadata", "profile", "api"),
        "insight": ("calculated insight", "insight", "analytics"),
        "semantic": ("semantic", "metric", "dimension"),
        "ai-search": ("search", "retriever", "rag", "chunk", "vector"),
        "segment": ("segment", "audience"),
        "act": ("activation", "activate", "data action", "destination"),
        "automation": ("flow", "automation", "event", "refresh"),
        "develop-package": ("developer", "api", "package", "data kit", "deploy", "sandbox"),
    }
    found = []
    for phase in phases:
        phase_id = phase.get("phase")
        if phase_id in keywords and any(term in text for term in keywords[phase_id]):
            found.append(phase_id)
    return found or ["retrieve"]


def build_graph(records: list[dict], phases: list[dict], generated_at: str) -> dict:
    nodes: list[dict] = []
    edges: list[dict] = []
    topic_ids: dict[str, str] = {}
    skill_by_phase = {phase.get("phase"): phase.get("specialistSkill") for phase in phases}
    for phase in phases:
        phase_id = phase.get("phase")
        nodes.append({"id": f"phase:{phase_id}", "type": "phase", "key": phase_id, "label": phase.get("name", phase_id)})
        skill = skill_by_phase.get(phase_id)
        if skill:
            skill_id = f"skill:{skill}"
            if not any(node["id"] == skill_id for node in nodes):
                nodes.append({"id": skill_id, "type": "specialist-skill", "key": skill, "label": skill})
            edges.append({"from": f"phase:{phase_id}", "to": skill_id, "type": "routes-to"})
    for record in records:
        page_id = record["id"]
        nodes.append({key: record[key] for key in ("id", "sourceType", "source", "title", "identifier", "depth", "parent", "contentHash", "status") } | {"type": "official-page"})
        for phase_id in phase_matches(record, phases):
            edges.append({"from": page_id, "to": f"phase:{phase_id}", "type": "covers-phase"})
        for topic in record["topics"][:12]:
            topic_key = re.sub(r"\s+", " ", topic.strip().lower())
            if len(topic_key) < 3:
                continue
            topic_id = topic_ids.setdefault(topic_key, f"topic:{sha256(topic_key)[:20]}")
            if not any(node["id"] == topic_id for node in nodes):
                nodes.append({"id": topic_id, "type": "topic", "key": topic_key, "label": topic.strip()})
            edges.append({"from": page_id, "to": topic_id, "type": "covers-topic"})
    return {"schemaVersion": "1.0", "generatedAt": generated_at, "scope": {"helpSeed": HELP_SEED, "developerSeed": DEV_SEED, "maxDepth": 4, "officialDomains": ["help.salesforce.com", "developer.salesforce.com"]}, "nodes": nodes, "edges": edges}


def old_urls(path: Path) -> set[str]:
    if not path.exists():
        return set()
    return set(re.findall(r"https://(?:help|developer)\.salesforce\.com/[^\s) |]+", path.read_text(encoding="utf-8")))


def reconcile(records: list[dict], graph: dict, generated_at: str) -> dict:
    current = {record["source"]: record for record in records}
    previous_graph = json_load(ROOT / "docs/data360/docs-knowledge-graph.json", {})
    previous = {node.get("source"): node for node in previous_graph.get("nodes", []) if node.get("type") == "official-page" and node.get("source")}
    new_pages = sorted(set(current) - set(previous))
    removed_pages = sorted(set(previous) - set(current))
    changed_pages = sorted(url for url in set(current) & set(previous) if current[url].get("contentHash") != previous[url].get("contentHash"))
    stale_refs = sorted((old_urls(ROOT / "docs/data360/help/index.md") | old_urls(ROOT / "docs/data360/developer/index.md")) - set(current))
    covered_phases = {edge["to"].removeprefix("phase:") for edge in graph["edges"] if edge["type"] == "covers-phase"}
    expected_phases = {phase.get("phase") for phase in phase_data()}
    candidate_discrepancies = [
        {"url": url, "reason": "changed source touches limits, permissions, licensing, availability, or behavior-sensitive guidance"}
        for url in changed_pages
        if re.search(r"limit|permission|license|availability|behavior|api|setup|deploy", current[url]["title"] + " " + current[url]["lead"], re.IGNORECASE)
    ]
    return {"schemaVersion": "1.0", "generatedAt": generated_at, "scope": graph["scope"], "summary": {"currentPages": len(current), "newPages": len(new_pages), "removedPages": len(removed_pages), "changedPages": len(changed_pages), "staleReferences": len(stale_refs), "uncoveredPhases": len(expected_phases - covered_phases)}, "newPages": new_pages, "removedPages": removed_pages, "changedPages": changed_pages, "staleBeastReferences": stale_refs, "uncoveredTopics": [], "uncoveredPhases": sorted(expected_phases - covered_phases), "extractionFailures": [], "candidateDiscrepancies": candidate_discrepancies}


def run_crawlers(work: Path) -> list[dict]:
    help_out = work / "help"
    dev_out = work / "developer"
    help_result = run(node_command() + [str(HELP_CRAWLER), "--outdir", str(help_out), "--seed", HELP_SEED, "--depth", "4", "--refresh"], timeout=3600)
    dev_result = run(node_command() + [str(DEV_CRAWLER), "--outdir", str(dev_out), "--seed", DEV_SEED], timeout=3600)
    return manifest_records(help_out / "manifest.json", "help") + manifest_records(dev_out / "manifest.json", "developer")


def copy_public_outputs(work: Path) -> list[str]:
    copies = [
        (work / "help/index.md", ROOT / "docs/data360/help/index.md"),
        (work / "developer/index.md", ROOT / "docs/data360/developer/index.md"),
        (work / "developer/learning-map.md", ROOT / "docs/data360/developer/learning-map.md"),
    ]
    for source, target in copies:
        shutil.copyfile(source, target)
    return [str(target.relative_to(ROOT)) for _, target in copies]


def apply_companion_drift(drift: dict) -> None:
    if not drift.get("changed") or not drift.get("categories"):
        return
    contract_path = ROOT / "docs/data360/sf-skills-data360-companion.json"
    contract = json_load(contract_path, {})
    observed = drift["observed"]
    upstream = contract.setdefault("upstream", {})
    upstream.update({
        "repository": observed.get("repository"),
        "packageName": observed.get("packageName"),
        "observedPackageVersion": observed.get("packageVersion"),
        "observedRef": observed.get("commit") or observed.get("ref"),
        "observedRefDate": (observed.get("date") or "")[:10] or datetime.now(timezone.utc).date().isoformat(),
    })
    contract["updated"] = datetime.now(timezone.utc).date().isoformat()
    contract["observedFiles"] = observed.get("files", {})
    contract_path.write_text(json.dumps(contract, indent=2) + "\n", encoding="utf-8")
    markdown_path = ROOT / "docs/data360/sf-skills-data360-companion.md"
    markdown = markdown_path.read_text(encoding="utf-8")
    markdown = re.sub(r"- Version: `[^`]+`", f"- Version: `{observed.get('packageVersion')}`", markdown)
    markdown = re.sub(r"- Commit: `[^`]+`", f"- Commit: `{observed.get('commit') or observed.get('ref')}`", markdown)
    markdown = re.sub(r"- Observed: [0-9-]+", f"- Observed: {datetime.now(timezone.utc).date().isoformat()}", markdown)
    markdown_path.write_text(markdown, encoding="utf-8")


def changed_files() -> list[str]:
    result = run(["git", "status", "--short", "--untracked-files=all"], check=True)
    paths: list[str] = []
    for line in result.stdout.splitlines():
        if not line or line.startswith("?? "):
            path = line[3:] if line.startswith("?? ") else ""
            if path in APPROVED_STAGES:
                paths.append(path)
            continue
        path = line[3:]
        if path not in APPROVED_STAGES:
            raise RuntimeError("refusing to stage unexpected tracked change: " + path)
        paths.append(path)
    return sorted(set(paths))


def stage_and_push() -> tuple[str | None, str | None]:
    files = changed_files()
    unexpected = [path for path in files if path not in APPROVED_STAGES]
    if unexpected:
        raise RuntimeError("refusing to stage unexpected files: " + ", ".join(unexpected))
    if not files:
        return None, None
    run(["git", "add", "--", *files])
    staged = run(["git", "diff", "--cached", "--name-only"]).stdout.splitlines()
    unexpected_staged = [path for path in staged if path not in APPROVED_STAGES]
    if unexpected_staged:
        raise RuntimeError("unexpected staged files: " + ", ".join(unexpected_staged))
    run(["python3", "tools/validate_docs_watch.py"])
    run(["git", "commit", "-m", "Refresh Data 360 docs watch index"])
    sha = run(["git", "rev-parse", "HEAD"]).stdout.strip()
    run(["git", "push", "origin", "HEAD:main"], timeout=600)
    return sha, "pushed"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="Run source refresh and reports without changing the repository")
    parser.add_argument("--apply", action="store_true", help="Apply public index and graph changes without committing")
    parser.add_argument("--commit", action="store_true", help="Apply, validate, commit, and push the public-safe diff")
    args = parser.parse_args()
    if not (args.dry_run or args.apply or args.commit):
        parser.error("choose --dry-run, --apply, or --commit")
    if args.commit:
        args.apply = True
    generated_at = datetime.now(timezone.utc).isoformat()
    try:
        preflight = check_preflight()
        with tempfile.TemporaryDirectory(prefix="data360beast-docs-watch-") as raw:
            work = Path(raw)
            records = run_crawlers(work)
            phases = phase_data()
            graph = build_graph(records, phases, generated_at)
            reconciliation = reconcile(records, graph, generated_at)
            (work / "docs-knowledge-graph.json").write_text(json.dumps(graph, indent=2) + "\n", encoding="utf-8")
            (work / "docs-watch-reconciliation.json").write_text(json.dumps(reconciliation, indent=2) + "\n", encoding="utf-8")
            # The companion check is source-only and its output is never copied.
            drift = run(["python3", "tools/check_sf_skills_drift.py", "--json"], timeout=300)
            drift_payload = json.loads(drift.stdout)
            print(json.dumps({"changed": drift_payload["changed"], "categories": drift_payload["categories"], "changedFiles": len(drift_payload["changedFiles"]), "source": drift_payload["source"]}, indent=2))
            run(["python3", "skills/data360beast/scripts/install_sf_skills_data360_companion.py", "--dry-run"], timeout=300)
            sync_check = run(["python3", "tools/refresh_skills_from_sf_docs.py", "--check"], check=False, timeout=300)
            if sync_check.returncode not in (0, 2):
                raise RuntimeError("marker-delimited docs sync check failed")
            print(json.dumps({"preflight": preflight, "records": len(records), "reconciliation": reconciliation["summary"], "mode": "dry-run" if args.dry_run else "apply"}, indent=2))
            if args.dry_run:
                return 0
            copy_public_outputs(work)
            shutil.copyfile(work / "docs-knowledge-graph.json", ROOT / "docs/data360/docs-knowledge-graph.json")
            shutil.copyfile(work / "docs-watch-reconciliation.json", ROOT / "docs/data360/docs-watch-reconciliation.json")
            apply_companion_drift(drift_payload)
            run(["python3", "tools/refresh_skills_from_sf_docs.py", "--apply"], timeout=300)
        run(["python3", "tools/validate_docs_watch.py"])
        sha = push_status = None
        if args.commit:
            sha, push_status = stage_and_push()
        print(json.dumps({"status": "ok", "commitSha": sha, "pushStatus": push_status}, indent=2))
        return 0
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, RuntimeError, OSError) as exc:
        print(f"FAIL: docs watch stopped before publication: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
