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
PROOF_HEADERS = [
    "ID",
    "Source",
    "Surface",
    "Phase",
    "Data-Space Assumptions",
    "Proof/Readback",
    "Caveat",
    "Confidence",
    "Labs Reference",
    "Status",
]
PROOF_STATUSES = {"lab-only", "candidate", "documented", "tested", "promoted", "retired"}
DEVELOPER_FAMILIES = {
    "developer-guide",
    "code-extension",
    "connect-rest-api",
    "connect-rest-api-guide",
    "connect-rest-api-reference",
    "dmo-mapping",
    "integration",
    "query-guide",
    "sql-reference",
}
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
    matrix_phases = {phase.get("phase") for phase in matrix.get("phases", [])}
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
        if not matrix_phases.issubset(graph_phases):
            fail(issues, "knowledge graph does not represent all proof phases")
        developer_nodes = [
            node
            for node in graph.get("nodes", [])
            if node.get("type") == "official-page" and node.get("sourceType") == "developer"
        ]
        families = {node.get("guideFamily") for node in developer_nodes}
        missing_families = sorted(DEVELOPER_FAMILIES - families)
        if missing_families:
            fail(issues, "knowledge graph missing Developer families: " + ", ".join(missing_families))
        captured_families = {
            node.get("guideFamily") for node in developer_nodes if node.get("status") == "captured"
        }
        missing_captures = sorted(DEVELOPER_FAMILIES - captured_families)
        if missing_captures:
            fail(issues, "Developer families without content captures: " + ", ".join(missing_captures))
        if not any(node.get("status") == "cataloged" for node in developer_nodes):
            fail(issues, "knowledge graph must distinguish catalog-only Developer references")
        edge_types = {edge.get("type") for edge in graph.get("edges", [])}
        for expected in {"covers-topic", "covers-phase", "routes-to", "informs-skill", "discovered-from"}:
            if expected not in edge_types:
                fail(issues, f"knowledge graph missing edge type: {expected}")

        reconciliation = json.loads((ROOT / "docs/data360/docs-watch-reconciliation.json").read_text(encoding="utf-8"))
        summary = reconciliation.get("summary", {})
        if summary.get("currentPages") != len([node for node in graph.get("nodes", []) if node.get("type") == "official-page"]):
            fail(issues, "reconciliation page count disagrees with knowledge graph")
        if summary.get("developerPages") != len(developer_nodes):
            fail(issues, "reconciliation Developer count disagrees with knowledge graph")
        if summary.get("extractionFailures"):
            fail(issues, "reconciliation contains extraction failures")
        if reconciliation.get("uncoveredTopics"):
            fail(issues, "reconciliation contains uncovered Developer topics")

        page_nodes = [node for node in graph.get("nodes", []) if node.get("type") == "official-page"]
        help_count = sum(node.get("sourceType") == "help" for node in page_nodes)
        captured_count = sum(node.get("status") == "captured" for node in developer_nodes)
        cataloged_count = sum(node.get("status") == "cataloged" for node in developer_nodes)
        manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
        source_stats = manifest.get("sourceStats", {})
        expected_manifest_stats = {
            "helpDocsAnalyzed": help_count,
            "developerGuidePagesAnalyzed": captured_count,
            "developerPagesIndexed": len(developer_nodes),
            "developerReferencePagesCataloged": cataloged_count,
            "officialDocsIndexed": len(page_nodes),
        }
        for key, expected in expected_manifest_stats.items():
            if source_stats.get(key) != expected:
                fail(issues, f"manifest sourceStats.{key} disagrees with knowledge graph")

        agent = json.loads((ROOT / "docs/agent-manifest.json").read_text(encoding="utf-8"))
        official = agent.get("officialDocIndexes", {})
        expected_agent_stats = {
            "helpSalesforcePages": help_count,
            "developerSalesforceGuidePages": captured_count,
            "developerSalesforcePagesIndexed": len(developer_nodes),
            "developerReferencePagesCataloged": cataloged_count,
            "officialPagesIndexed": len(page_nodes),
        }
        for key, expected in expected_agent_stats.items():
            if official.get(key) != expected:
                fail(issues, f"agent-manifest officialDocIndexes.{key} disagrees with knowledge graph")
        if "implementationFoundation" not in agent.get("entrypoints", {}):
            fail(issues, "agent-manifest is missing the implementation foundation entrypoint")

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

    validate_proof_ledger(issues, matrix_phases)

    proof_entry_count = len(
        re.findall(
            r"^\| `BEAST-PROOF-\d{3}` \|",
            (ROOT / "docs/proof-ledger.md").read_text(encoding="utf-8"),
            re.MULTILINE,
        )
    )
    manifest_stats = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8")).get("sourceStats", {})
    agent_stats = json.loads((ROOT / "docs/agent-manifest.json").read_text(encoding="utf-8")).get("proofArtifactStats", {})
    if manifest_stats.get("proofLedgerEntries") != proof_entry_count:
        fail(issues, "manifest proofLedgerEntries disagrees with proof ledger")
    if agent_stats.get("proofLedgerEntries") != proof_entry_count:
        fail(issues, "agent-manifest proofLedgerEntries disagrees with proof ledger")


def parse_markdown_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def validate_proof_ledger(issues: list[str], matrix_phases: set[str]) -> None:
    text = (ROOT / "docs/proof-ledger.md").read_text(encoding="utf-8")
    section = text.split("## Current Evidence", 1)
    if len(section) != 2:
        fail(issues, "proof ledger is missing Current Evidence")
        return
    lines = [line for line in section[1].splitlines() if line.strip().startswith("|")]
    if len(lines) < 3:
        fail(issues, "proof ledger Current Evidence table is missing")
        return
    headers = parse_markdown_row(lines[0])
    if headers != PROOF_HEADERS:
        fail(issues, "proof ledger fields do not match the required ten-field contract")
        return
    seen_ids: set[str] = set()
    for line in lines[2:]:
        cells = parse_markdown_row(line)
        if len(cells) != len(PROOF_HEADERS):
            fail(issues, f"proof ledger row has {len(cells)} fields instead of {len(PROOF_HEADERS)}: {line[:80]}")
            continue
        values = dict(zip(PROOF_HEADERS, cells))
        evidence_id = values["ID"].strip("`")
        if not re.fullmatch(r"BEAST-PROOF-\d{3}", evidence_id):
            fail(issues, f"invalid proof ledger ID: {values['ID']}")
        if evidence_id in seen_ids:
            fail(issues, f"duplicate proof ledger ID: {evidence_id}")
        seen_ids.add(evidence_id)
        for field, value in values.items():
            if not value:
                fail(issues, f"proof ledger {evidence_id} has empty field: {field}")
        phase_values = {value.strip() for value in values["Phase"].split(",")}
        if not phase_values.issubset(matrix_phases):
            fail(issues, f"proof ledger {evidence_id} references unknown phase: {values['Phase']}")
        status = values["Status"].strip("`")
        if status not in PROOF_STATUSES:
            fail(issues, f"proof ledger {evidence_id} has invalid status: {status}")


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
        "docs/data360/implementation-foundation.md",
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
