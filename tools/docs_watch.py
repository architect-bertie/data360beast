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
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse


ROOT = Path(__file__).resolve().parents[1]
HELP_SEED = "https://help.salesforce.com/s/articleView?id=data.c360_a_product_considerations.htm&language=en_US&type=5"
DEV_CENTER = "https://developer.salesforce.com/developer-centers/data-cloud"
HELP_CRAWLER = ROOT / "tools/sf_docs_help_crawl.mjs"
DEV_CRAWLER = ROOT / "tools/sf_docs_developer_guide_crawl.mjs"
EXPECTED_DEVELOPER_TOPICS = {
    "acceleration-and-refresh",
    "authentication-and-permissions",
    "code-extension",
    "connections-and-connectors",
    "data-shares-and-targets",
    "data-streams-and-ingestion",
    "dmo-modeling-and-mapping",
    "file-federation",
    "governance-and-security",
    "identity-resolution",
    "limits-and-considerations",
    "packaging-and-deployment",
    "query-and-sql",
    "query-federation",
    "segmentation-and-activation",
    "troubleshooting-and-readiness",
    "unstructured-and-search",
    "web-and-mobile-sdk",
    "zero-copy-and-federation",
}
TOPIC_PATTERNS = {
    "authentication-and-permissions": r"auth|oauth|permission|credential|access token|external client app",
    "connections-and-connectors": r"connection|connector|source system",
    "data-streams-and-ingestion": r"data stream|ingest|\bdlo\b|data lake object",
    "zero-copy-and-federation": r"zero.?copy|federat|direct access|live query",
    "file-federation": r"file federation|iceberg|unity catalog",
    "query-federation": r"query federation|lakehouse federation",
    "acceleration-and-refresh": r"accelerat|refresh|schedule",
    "data-shares-and-targets": r"data share|data target|activation target",
    "dmo-modeling-and-mapping": r"\bdmo\b|data model object|mapping|customer 360 data model",
    "identity-resolution": r"identity resolution|unified individual|unified profile",
    "query-and-sql": r"query|\bsql\b|\bsoql\b|jdbc|python connector",
    "code-extension": r"code extension|custom script|custom function|data custom code",
    "unstructured-and-search": r"unstructured|search index|chunk|retriever|vector",
    "packaging-and-deployment": r"data kit|package|deploy|migration|sandbox|production",
    "limits-and-considerations": r"limit|consideration|guideline|unsupported|preview",
    "troubleshooting-and-readiness": r"troubleshoot|prerequisite|readiness|monitor|status|error",
    "segmentation-and-activation": r"segment|audience|activation|data action",
    "web-and-mobile-sdk": r"web sdk|mobile sdk|interactions sdk|website sitemap",
    "governance-and-security": r"govern|security|policy|firewall|allowlist|private connect",
}
APPROVED_STAGES = {
    ".gitignore",
    "README.md",
    "llms.txt",
    "manifest.json",
    "docs/agent-manifest.json",
    "docs/index.html",
    "docs/llms-full.txt",
    "docs/llms.txt",
    "docs/skills.md",
    "docs/proof-ledger.md",
    "docs/data360/implementation-foundation.md",
    "docs/data360/interoperability-decision-map.md",
    "docs/data360/help/index.md",
    "docs/data360/developer/index.md",
    "docs/data360/developer/learning-map.md",
    "docs/data360/developer/skill-update-synthesis.md",
    "docs/data360/develop-package-deployment-matrix.md",
    "docs/data360/docs-knowledge-graph.json",
    "docs/data360/docs-watch-reconciliation.json",
    "docs/data360/sf-skills-data360-companion.json",
    "docs/data360/sf-skills-data360-companion.md",
    "docs/data360/deployment-runtime.md",
    "docs/architecture-evals.json",
    "skills/data360beast/SKILL.md",
    "skills/data360beast/scripts/data360beast.py",
    "skills/data360beast/runtime/__init__.py",
    "skills/data360beast/runtime/data360beast_runtime.py",
    "skills/sf-datacloud/references/production-implementation-checklist.md",
    "skills/data360beast/scripts/install_sf_skills_data360_companion.py",
    "tools/check_sf_skills_drift.py",
    "tools/audit_indexed_docs.py",
    "tools/docs_watch.py",
    "tools/refresh_skills_from_sf_docs.py",
    "tools/sf_docs_developer_guide_crawl.mjs",
    "tools/validate_docs_watch.py",
    "tools/build_knowledge_graph.py",
    "tools/run_architecture_evals.py",
    "tools/validate_expertise.py",
    "tests/test_docs_watch.py",
    "tests/test_data360beast_runtime.py",
}
APPROVED_STAGES.update({
    "docs/data360/schemas/implementation-spec.schema.json",
    "docs/data360/schemas/deployment-plan.schema.json",
    "docs/data360/schemas/run-state.schema.json",
    "docs/data360/schemas/certification-attestation.schema.json",
    "docs/data360/knowledge/ontology.json",
    "docs/data360/knowledge/claims.json",
    "docs/data360/knowledge/decisions.json",
    "docs/data360/packs/beastwear.json",
})
APPROVED_STAGES.update({
    f"skills/{name}/SKILL.md"
    for name in (
        "sf-datacloud", "sf-datacloud-act", "sf-datacloud-automation", "sf-datacloud-connect",
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


def json_at_head(relative_path: str, fallback):
    result = subprocess.run(
        ["git", "show", f"HEAD:{relative_path}"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode:
        return fallback
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return fallback


def normalize_official_url(value: str) -> str:
    parsed = urlparse(value)
    host = (parsed.hostname or "").lower()
    if host not in {"help.salesforce.com", "developer.salesforce.com"}:
        raise ValueError(f"unsupported official-doc host: {host or value}")
    path = re.sub(r"/{2,}", "/", parsed.path or "/")
    if host == "help.salesforce.com":
        article_id = parse_qs(parsed.query).get("id", [None])[0]
        if not article_id:
            raise ValueError(f"Help URL has no article id: {value}")
        query = urlencode({"id": article_id, "language": "en_US", "type": "5"})
        path = "/s/articleView"
    else:
        query = ""
        if path != "/":
            path = path.rstrip("/")
    return urlunparse(("https", host, path, "", query, ""))


def source_classification(value: str) -> str:
    host = (urlparse(value).hostname or "").lower()
    if host == "help.salesforce.com":
        return "help"
    if host == "developer.salesforce.com":
        return "developer"
    raise ValueError(f"unsupported official-doc source: {value}")


def looks_like_shell(title: str, text: str) -> bool:
    haystack = f"{title}\n{text}".lower()
    return any(
        token in haystack
        for token in (
            "sorry to interrupt",
            "css error",
            "we looked high and low",
            "couldn't find that page",
        )
    ) or (
        len(text.strip()) < 120
        and title.strip().lower() in {"salesforce help", "untitled", "loading", "404", "404 error", "page not found"}
    )


def classify_topic_tags(text: str, supplied: list[str] | None = None) -> list[str]:
    tags = {
        topic
        for topic in (supplied or [])
        if topic in EXPECTED_DEVELOPER_TOPICS
    }
    lowered = text.lower()
    tags.update(
        topic
        for topic, pattern in TOPIC_PATTERNS.items()
        if re.search(pattern, lowered)
    )
    return sorted(tags)


def deduplicate_records(records: list[dict]) -> list[dict]:
    by_source: dict[str, dict] = {}
    for record in records:
        source = normalize_official_url(record["source"])
        normalized = {**record, "source": source}
        existing = by_source.get(source)
        if existing is None or (existing.get("status") != "captured" and normalized.get("status") == "captured"):
            by_source[source] = normalized
    return sorted(by_source.values(), key=lambda item: item["source"])


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
        try:
            normalized_url = normalize_official_url(url)
        except ValueError as exc:
            raise RuntimeError(f"non-official source returned by crawler: {url}") from exc
        if source_classification(normalized_url) != source_type:
            raise RuntimeError(f"source classification mismatch for {url}: expected {source_type}")
        title = str(item.get("title") or "").strip()
        if not title or title.lower() == "untitled":
            raise RuntimeError(f"untitled source returned by crawler: {url}")
        summary = item.get("summary") or {}
        content = "\n".join([title, summary.get("lead", ""), *summary.get("topics", []), *summary.get("headings", []), *summary.get("bullets", [])])
        topic_tags = classify_topic_tags(content, summary.get("topics", []))
        if looks_like_shell(title, content):
            raise RuntimeError(f"shell or soft-404 source returned by crawler: {url}")
        parent = item.get("parent")
        if isinstance(parent, str) and parent.startswith(("https://help.salesforce.com/", "https://developer.salesforce.com/")):
            parent = normalize_official_url(parent)
        records.append({
            "id": f"page:{sha256(normalized_url)[:20]}",
            "source": normalized_url,
            "sourceType": source_type,
            "title": title,
            "identifier": item.get("articleId") or item.get("guidePath") or parsed.path,
            "depth": item.get("depth", 0),
            "parent": parent,
            "contentHash": item.get("contentHash") or sha256(content),
            "status": item.get("extractionStatus") or "captured",
            "extractionMethod": item.get("extractionMethod"),
            "guideFamily": item.get("guideFamily"),
            "navLabel": item.get("navLabel"),
            "topicTags": topic_tags,
            "topics": sorted(set(summary.get("topics", []) + summary.get("headings", []) + summary.get("bullets", [])))[:24],
            "lead": summary.get("lead", "")[:500],
        })
    if not records:
        raise RuntimeError(f"crawler produced no {source_type} records: {path}")
    return deduplicate_records(records)


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
    node_ids: set[str] = set()
    edge_keys: set[tuple[str, str, str]] = set()
    topic_ids: dict[str, str] = {}
    skill_by_phase = {phase.get("phase"): phase.get("specialistSkill") for phase in phases}

    def add_node(node: dict) -> None:
        if node["id"] not in node_ids:
            nodes.append(node)
            node_ids.add(node["id"])

    def add_edge(source: str, target: str, edge_type: str) -> None:
        key = (source, target, edge_type)
        if key not in edge_keys:
            edges.append({"from": source, "to": target, "type": edge_type})
            edge_keys.add(key)

    for phase in phases:
        phase_id = phase.get("phase")
        add_node({"id": f"phase:{phase_id}", "type": "phase", "key": phase_id, "label": phase.get("name", phase_id)})
        skill = skill_by_phase.get(phase_id)
        if skill:
            skill_id = f"skill:{skill}"
            add_node({"id": skill_id, "type": "specialist-skill", "key": skill, "label": skill})
            add_edge(f"phase:{phase_id}", skill_id, "routes-to")

    source_ids = {record["source"]: record["id"] for record in records}
    label_ids: dict[tuple[str, str, str], str] = {}
    for record in records:
        family = record.get("guideFamily") or ""
        for label in (record.get("navLabel"), record.get("title", "").split(" | ", 1)[0]):
            if label:
                label_ids[(record["sourceType"], family, re.sub(r"\s+", " ", label.strip().lower()))] = record["id"]

    for record in records:
        page_id = record["id"]
        matched_phases = phase_matches(record, phases)
        topic_tags = record.get("topicTags") or classify_topic_tags(
            " ".join([record.get("title", ""), record.get("lead", ""), *record.get("topics", [])])
        )
        page_node = {
            key: record[key]
            for key in ("id", "sourceType", "source", "title", "identifier", "depth", "parent", "contentHash", "status")
        } | {
            "type": "official-page",
            "topics": topic_tags,
            "phases": matched_phases,
        }
        for optional in ("guideFamily", "extractionMethod"):
            if record.get(optional):
                page_node[optional] = record[optional]
        add_node(page_node)
        for phase_id in matched_phases:
            add_edge(page_id, f"phase:{phase_id}", "covers-phase")
            skill = skill_by_phase.get(phase_id)
            if skill:
                add_edge(page_id, f"skill:{skill}", "informs-skill")
        for topic in topic_tags:
            topic_key = re.sub(r"\s+", " ", topic.strip().lower())
            if len(topic_key) < 3:
                continue
            topic_id = topic_ids.setdefault(topic_key, f"topic:{sha256(topic_key)[:20]}")
            add_node({"id": topic_id, "type": "topic", "key": topic_key, "label": topic.strip()})
            add_edge(page_id, topic_id, "covers-topic")

        parent = record.get("parent")
        parent_id = source_ids.get(parent)
        if not parent_id and isinstance(parent, str):
            parent_key = re.sub(r"\s+", " ", parent.strip().lower())
            parent_id = label_ids.get((record["sourceType"], record.get("guideFamily") or "", parent_key))
        if parent_id and parent_id != page_id:
            add_edge(page_id, parent_id, "discovered-from")

    graph = {
        "schemaVersion": "1.2",
        "generatedAt": generated_at,
        "scope": {
            "helpSeed": HELP_SEED,
            "developerCenter": DEV_CENTER,
            "maxDepth": 4,
            "officialDomains": ["help.salesforce.com", "developer.salesforce.com"],
            "contentHashContract": "crawler-content-sha256-v1",
        },
        "nodes": nodes,
        "edges": edges,
    }
    return attach_knowledge_nodes(graph, phases)


def attach_knowledge_nodes(graph: dict, phases: list[dict]) -> dict:
    """Attach public claim and decision records without exposing source bodies."""
    knowledge_dir = ROOT / "docs" / "data360" / "knowledge"
    claims_path = knowledge_dir / "claims.json"
    decisions_path = knowledge_dir / "decisions.json"
    if not claims_path.is_file():
        return graph
    nodes = graph["nodes"]
    edges = graph["edges"]
    node_ids = {node["id"] for node in nodes}
    edge_ids = {(edge["from"], edge["to"], edge["type"]) for edge in edges}
    skills = {phase.get("phase"): phase.get("specialistSkill") for phase in phases}
    pages = {node.get("source"): node.get("id") for node in nodes if node.get("type") == "official-page"}

    def add_node(node: dict) -> None:
        if node["id"] not in node_ids:
            nodes.append(node)
            node_ids.add(node["id"])

    def add_edge(source: str, target: str, kind: str) -> None:
        key = (source, target, kind)
        if key not in edge_ids:
            edges.append({"from": source, "to": target, "type": kind})
            edge_ids.add(key)

    for claim in json_load(claims_path, {}).get("claims", []):
        claim_id = f"claim:{claim['id']}"
        add_node({"id": claim_id, "type": "claim", **claim})
        phase = claim.get("phase")
        if phase:
            add_edge(claim_id, f"phase:{phase}", "applies-to")
            skill = skills.get(phase)
            if skill:
                add_edge(claim_id, f"skill:{skill}", "informs-skill")
        source = claim.get("source")
        if source in pages:
            add_edge(claim_id, pages[source], "proved-by")
    for decision in json_load(decisions_path, {}).get("decisions", []):
        decision_id = f"decision:{decision['id']}"
        add_node({"id": decision_id, "type": "decision", **decision})
        owner = decision.get("owner")
        if owner:
            add_edge(decision_id, f"skill:{owner}", "applies-to")
    return graph


def old_urls(path: Path) -> set[str]:
    if not path.exists():
        return set()
    urls: set[str] = set()
    for raw in re.findall(r"https://(?:help|developer)\.salesforce\.com/[^\s) |]+", path.read_text(encoding="utf-8")):
        try:
            urls.add(normalize_official_url(raw.rstrip(".,;")))
        except ValueError:
            continue
    return urls


def reconcile(records: list[dict], graph: dict, generated_at: str, previous_graph: dict | None = None) -> dict:
    current = {record["source"]: record for record in records}
    if previous_graph is None:
        previous_graph = json_at_head("docs/data360/docs-knowledge-graph.json", {})
    previous = {node.get("source"): node for node in previous_graph.get("nodes", []) if node.get("type") == "official-page" and node.get("source")}
    new_pages = sorted(set(current) - set(previous))
    removed_pages = sorted(set(previous) - set(current))
    hash_deltas = {
        url
        for url in set(current) & set(previous)
        if current[url].get("contentHash") != previous[url].get("contentHash")
    }
    same_hash_contract = (
        previous_graph.get("scope", {}).get("contentHashContract")
        == graph.get("scope", {}).get("contentHashContract")
    )
    changed_pages = sorted(hash_deltas if same_hash_contract else set())
    rehashed_pages = sorted(set() if same_hash_contract else hash_deltas)
    referenced = old_urls(ROOT / "docs/data360/help/index.md") | old_urls(ROOT / "docs/data360/developer/index.md")
    stale_refs = sorted((referenced & set(previous)) - set(current))
    covered_phases = {edge["to"].removeprefix("phase:") for edge in graph["edges"] if edge["type"] == "covers-phase"}
    expected_phases = {phase.get("phase") for phase in phase_data()}
    observed_topics = {
        topic
        for record in records
        for topic in record.get("topicTags", [])
    }
    extraction_failures = [
        {"url": record["source"], "status": record.get("status", "unknown")}
        for record in records
        if record.get("status") not in {"captured", "cataloged"}
    ]
    source_counts = {
        source_type: len([record for record in records if record["sourceType"] == source_type])
        for source_type in ("help", "developer")
    }
    developer_families: dict[str, dict[str, int]] = {}
    for record in records:
        family = record.get("guideFamily")
        if record["sourceType"] != "developer" or not family:
            continue
        counts = developer_families.setdefault(family, {"total": 0, "captured": 0, "cataloged": 0})
        counts["total"] += 1
        if record.get("status") in counts:
            counts[record["status"]] += 1
    candidate_discrepancies = [
        {"url": url, "reason": "changed source touches limits, permissions, licensing, availability, or behavior-sensitive guidance"}
        for url in changed_pages
        if re.search(r"limit|permission|license|availability|behavior|api|setup|deploy", current[url]["title"] + " " + current[url]["lead"], re.IGNORECASE)
    ]
    uncovered_topics = sorted(EXPECTED_DEVELOPER_TOPICS - observed_topics)
    return {
        "schemaVersion": "1.1",
        "generatedAt": generated_at,
        "scope": graph["scope"],
        "summary": {
            "currentPages": len(current),
            "helpPages": source_counts["help"],
            "developerPages": source_counts["developer"],
            "developerCaptured": sum(counts["captured"] for counts in developer_families.values()),
            "developerCataloged": sum(counts["cataloged"] for counts in developer_families.values()),
            "newPages": len(new_pages),
            "removedPages": len(removed_pages),
            "changedPages": len(changed_pages),
            "rehashedPages": len(rehashed_pages),
            "staleReferences": len(stale_refs),
            "uncoveredTopics": len(uncovered_topics),
            "uncoveredPhases": len(expected_phases - covered_phases),
            "extractionFailures": len(extraction_failures),
        },
        "sourceCounts": source_counts,
        "developerFamilies": dict(sorted(developer_families.items())),
        "newPages": new_pages,
        "removedPages": removed_pages,
        "changedPages": changed_pages,
        "rehashedPages": rehashed_pages,
        "staleBeastReferences": stale_refs,
        "uncoveredTopics": uncovered_topics,
        "uncoveredPhases": sorted(expected_phases - covered_phases),
        "extractionFailures": extraction_failures,
        "candidateDiscrepancies": candidate_discrepancies,
    }


def without_timestamp(payload: dict) -> dict:
    return {key: value for key, value in payload.items() if key != "generatedAt"}


def run_crawlers(work: Path) -> list[dict]:
    help_out = work / "help"
    dev_out = work / "developer"
    help_result = run(node_command() + [str(HELP_CRAWLER), "--outdir", str(help_out), "--seed", HELP_SEED, "--depth", "4", "--refresh"], timeout=3600)
    run(node_command() + [str(DEV_CRAWLER), "--outdir", str(dev_out), "--center", DEV_CENTER], timeout=7200)
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


def update_public_metadata(graph: dict) -> None:
    pages = [node for node in graph.get("nodes", []) if node.get("type") == "official-page"]
    help_pages = sum(node.get("sourceType") == "help" for node in pages)
    developer_pages = [node for node in pages if node.get("sourceType") == "developer"]
    developer_captured = sum(node.get("status") == "captured" for node in developer_pages)
    developer_cataloged = sum(node.get("status") == "cataloged" for node in developer_pages)
    proof_entries = len(
        re.findall(
            r"^\| `BEAST-PROOF-\d{3}` \|",
            (ROOT / "docs/proof-ledger.md").read_text(encoding="utf-8"),
            re.MULTILINE,
        )
    )
    sync_blocks = sum(
        path.read_text(encoding="utf-8", errors="ignore").count("SF_DOC_SYNC_START:")
        for base in (ROOT / "docs", ROOT / "skills")
        for path in base.rglob("*.md")
    )

    manifest_path = ROOT / "manifest.json"
    manifest = json_load(manifest_path, {})
    if graph.get("generatedAt"):
        manifest["lastReviewed"] = str(graph["generatedAt"])[:10]
    stats = manifest.setdefault("sourceStats", {})
    stats.update({
        "helpDocsAnalyzed": help_pages,
        "developerGuidePagesAnalyzed": developer_captured,
        "developerPagesIndexed": len(developer_pages),
        "developerReferencePagesCataloged": developer_cataloged,
        "officialDocsIndexed": len(pages),
        "docSyncedBlocksTotal": sync_blocks,
        "proofLedgerEntries": proof_entries,
    })
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    agent_path = ROOT / "docs/agent-manifest.json"
    agent = json_load(agent_path, {})
    if graph.get("generatedAt"):
        agent["lastReviewed"] = str(graph["generatedAt"])[:10]
    agent.setdefault("entrypoints", {})["implementationFoundation"] = (
        "https://architect-bertie.github.io/data360beast/data360/implementation-foundation.md"
    )
    official = agent.setdefault("officialDocIndexes", {})
    official.update({
        "helpSalesforcePages": help_pages,
        "developerSalesforceGuidePages": developer_captured,
        "developerSalesforcePagesIndexed": len(developer_pages),
        "developerReferencePagesCataloged": developer_cataloged,
        "officialPagesIndexed": len(pages),
    })
    proof_stats = agent.setdefault("proofArtifactStats", {})
    proof_stats.update({
        "proofLedgerEntries": proof_entries,
        "docSyncedBlocksTotal": sync_blocks,
    })
    agent_path.write_text(json.dumps(agent, indent=2) + "\n", encoding="utf-8")


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


def stage_and_open_pr() -> tuple[str | None, str | None]:
    files = changed_files()
    if not files:
        return None, None
    branch = "automation/docs-watch-" + datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    run(["git", "switch", "-c", branch])
    run(["git", "add", "--", *files])
    staged = run(["git", "diff", "--cached", "--name-only"]).stdout.splitlines()
    if any(path not in APPROVED_STAGES for path in staged):
        raise RuntimeError("unexpected staged files in PR flow")
    run(["python3", "tools/validate_docs_watch.py"])
    run(["python3", "tools/validate_expertise.py"])
    run(["git", "commit", "-m", "Refresh Data 360 docs watch index"])
    sha = run(["git", "rev-parse", "HEAD"]).stdout.strip()
    run(["git", "push", "-u", "origin", branch], timeout=600)
    pr = run([
        "gh", "pr", "create", "--base", "main", "--head", branch,
        "--title", "Refresh Data 360 docs watch index", "--label", "automation:knowledge",
        "--body", "Automated public-safe documentation and knowledge-claim refresh.",
    ], timeout=300).stdout.strip()
    return sha, "pr-opened:" + pr


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="Run source refresh and reports without changing the repository")
    parser.add_argument("--apply", action="store_true", help="Apply public index and graph changes without committing")
    parser.add_argument("--commit", action="store_true", help="Apply, validate, commit, and push the public-safe diff")
    parser.add_argument("--pr", action="store_true", help="Apply, validate, and open a gated knowledge-refresh pull request")
    args = parser.parse_args()
    if not (args.dry_run or args.apply or args.commit or args.pr):
        parser.error("choose --dry-run, --apply, --commit, or --pr")
    if args.commit or args.pr:
        args.apply = True
    generated_at = datetime.now(timezone.utc).isoformat()
    try:
        preflight = check_preflight()
        with tempfile.TemporaryDirectory(prefix="data360beast-docs-watch-") as raw:
            work = Path(raw)
            records = run_crawlers(work)
            phases = phase_data()
            graph = build_graph(records, phases, generated_at)
            live_reconciliation = reconcile(records, graph, generated_at)
            reconciliation = live_reconciliation
            previous_graph = json_load(ROOT / "docs/data360/docs-knowledge-graph.json", {})
            previous_reconciliation = json_load(ROOT / "docs/data360/docs-watch-reconciliation.json", {})
            if (
                previous_graph
                and previous_reconciliation
                and without_timestamp(graph) == without_timestamp(previous_graph)
            ):
                generated_at = previous_graph.get("generatedAt") or previous_reconciliation.get("generatedAt") or generated_at
                graph = build_graph(records, phases, generated_at)
                reconciliation = previous_reconciliation
            (work / "docs-knowledge-graph.json").write_text(json.dumps(graph, indent=2) + "\n", encoding="utf-8")
            (work / "docs-watch-reconciliation.json").write_text(json.dumps(reconciliation, indent=2) + "\n", encoding="utf-8")
            # The companion check is source-only and its output is never copied.
            drift = run(["python3", "tools/check_sf_skills_drift.py", "--json"], timeout=300)
            drift_payload = json.loads(drift.stdout)
            print(json.dumps({"changed": drift_payload["changed"], "categories": drift_payload["categories"], "changedFiles": len(drift_payload["changedFiles"]), "source": drift_payload["source"]}, indent=2))
            run(["python3", "skills/data360beast/scripts/install_sf_skills_data360_companion.py", "--dry-run"], timeout=300)
            developer_manifest = work / "developer" / "manifest.json"
            sync_check = run(
                ["python3", "tools/refresh_skills_from_sf_docs.py", "--developer-manifest", str(developer_manifest), "--help-summaries-dir", str(work / "help" / "summaries"), "--check"],
                check=False,
                timeout=300,
            )
            if sync_check.returncode not in (0, 2):
                raise RuntimeError("marker-delimited docs sync check failed")
            print(json.dumps({"preflight": preflight, "records": len(records), "reconciliation": live_reconciliation["summary"], "mode": "dry-run" if args.dry_run else "apply"}, indent=2))
            if args.dry_run:
                return 0
            copy_public_outputs(work)
            shutil.copyfile(work / "docs-knowledge-graph.json", ROOT / "docs/data360/docs-knowledge-graph.json")
            shutil.copyfile(work / "docs-watch-reconciliation.json", ROOT / "docs/data360/docs-watch-reconciliation.json")
            apply_companion_drift(drift_payload)
            run(
                ["python3", "tools/refresh_skills_from_sf_docs.py", "--developer-manifest", str(developer_manifest), "--help-summaries-dir", str(work / "help" / "summaries"), "--apply"],
                timeout=300,
            )
            update_public_metadata(graph)
        run(["python3", "tools/validate_docs_watch.py"])
        run(["python3", "tools/validate_expertise.py"])
        run(["python3", "tools/run_architecture_evals.py"])
        sha = push_status = None
        if args.commit:
            sha, push_status = stage_and_push()
        elif args.pr:
            sha, push_status = stage_and_open_pr()
        print(json.dumps({"status": "ok", "commitSha": sha, "pushStatus": push_status}, indent=2))
        return 0
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, RuntimeError, OSError) as exc:
        print(f"FAIL: docs watch stopped before publication: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
