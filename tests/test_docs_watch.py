import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("docs_watch", ROOT / "tools/docs_watch.py")
docs_watch = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = docs_watch
SPEC.loader.exec_module(docs_watch)

DRIFT_SPEC = importlib.util.spec_from_file_location("sf_skills_drift", ROOT / "tools/check_sf_skills_drift.py")
sf_skills_drift = importlib.util.module_from_spec(DRIFT_SPEC)
sys.modules[DRIFT_SPEC.name] = sf_skills_drift
DRIFT_SPEC.loader.exec_module(sf_skills_drift)
REFRESH_SPEC = importlib.util.spec_from_file_location("refresh_skills", ROOT / "tools/refresh_skills_from_sf_docs.py")
refresh_skills = importlib.util.module_from_spec(REFRESH_SPEC)
sys.modules[REFRESH_SPEC.name] = refresh_skills
REFRESH_SPEC.loader.exec_module(refresh_skills)
VALIDATE_SPEC = importlib.util.spec_from_file_location("validate_docs_watch", ROOT / "tools/validate_docs_watch.py")
validate_docs_watch = importlib.util.module_from_spec(VALIDATE_SPEC)
sys.modules[VALIDATE_SPEC.name] = validate_docs_watch
VALIDATE_SPEC.loader.exec_module(validate_docs_watch)


class DocsWatchTests(unittest.TestCase):
    def test_url_normalization_and_source_classification(self):
        help_url = docs_watch.normalize_official_url(
            "https://help.salesforce.com/s/articleView?type=5&id=data.c360_test.htm#section"
        )
        self.assertEqual(
            help_url,
            "https://help.salesforce.com/s/articleView?id=data.c360_test.htm&language=en_US&type=5",
        )
        self.assertEqual(docs_watch.source_classification(help_url), "help")
        developer_url = docs_watch.normalize_official_url(
            "https://developer.salesforce.com/docs/data/data-cloud-dev/guide/get-started.html?x=1#top"
        )
        self.assertEqual(
            developer_url,
            "https://developer.salesforce.com/docs/data/data-cloud-dev/guide/get-started.html",
        )
        self.assertEqual(docs_watch.source_classification(developer_url), "developer")

    def test_rejects_non_salesforce_and_shell_pages(self):
        with self.assertRaises(ValueError):
            docs_watch.normalize_official_url("https://example.com/data360")
        self.assertTrue(docs_watch.looks_like_shell("Salesforce Help", "Loading\nSorry to interrupt\nCSS Error"))
        self.assertFalse(docs_watch.looks_like_shell("Data 360 Query", "Use Query SQL to retrieve harmonized data. " * 10))

    def test_duplicate_detection_prefers_captured_record(self):
        source = "https://developer.salesforce.com/docs/data/test"
        records = [
            {"source": source + "/", "status": "cataloged", "title": "Catalog"},
            {"source": source, "status": "captured", "title": "Captured"},
        ]
        result = docs_watch.deduplicate_records(records)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["title"], "Captured")

    def test_topic_classification_is_bounded(self):
        tags = docs_watch.classify_topic_tags(
            "Configure OAuth permissions for Databricks file federation and Unity Catalog.",
            ["arbitrary-heading", "file-federation"],
        )
        self.assertIn("authentication-and-permissions", tags)
        self.assertIn("file-federation", tags)
        self.assertNotIn("arbitrary-heading", tags)

    def test_graph_contains_required_node_types_and_phases(self):
        phases = [{"phase": "connect", "name": "Connect", "specialistSkill": "sf-datacloud-connect"}]
        records = [{
            "id": "page:test", "sourceType": "help", "source": "https://help.salesforce.com/s/articleView?id=data.c360_test.htm",
            "title": "Data 360 Connector", "identifier": "data.c360_test.htm", "depth": 0, "parent": None,
            "contentHash": "hash", "status": "captured", "topics": ["Connectors"], "lead": "Configure a connector",
        }]
        graph = docs_watch.build_graph(records, phases, "now")
        self.assertEqual({"official-page", "topic", "phase", "specialist-skill"}, {node["type"] for node in graph["nodes"]})
        self.assertTrue(any(edge["type"] == "covers-phase" for edge in graph["edges"]))

    def test_graph_preserves_developer_family_and_extraction_method(self):
        phases = [{"phase": "retrieve", "name": "Retrieve", "specialistSkill": "sf-datacloud-retrieve"}]
        records = [{
            "id": "page:developer", "sourceType": "developer",
            "source": "https://developer.salesforce.com/docs/data/data-cloud-query-guide/guide/query-guide-get-started.html",
            "title": "Query Data in Data 360", "identifier": "/query", "depth": 0, "parent": None,
            "contentHash": "hash", "status": "captured", "topics": ["Query SQL"], "lead": "Query data",
            "guideFamily": "query-guide", "extractionMethod": "sf-docs-extractor",
        }]
        graph = docs_watch.build_graph(records, phases, "now")
        page = next(node for node in graph["nodes"] if node["type"] == "official-page")
        self.assertEqual(page["guideFamily"], "query-guide")
        self.assertEqual(page["extractionMethod"], "sf-docs-extractor")

    def test_graph_links_discovery_and_specialist_guidance(self):
        phases = [{"phase": "retrieve", "name": "Retrieve", "specialistSkill": "sf-datacloud-retrieve"}]
        records = [
            {
                "id": "page:parent", "sourceType": "developer", "source": "https://developer.salesforce.com/docs/data/guide/root.html",
                "title": "Query Guide", "navLabel": "Query Guide", "identifier": "/root", "depth": 0, "parent": None,
                "contentHash": "parent", "status": "captured", "topics": ["Query SQL"], "topicTags": ["query-and-sql"],
                "lead": "Query data", "guideFamily": "query-guide",
            },
            {
                "id": "page:child", "sourceType": "developer", "source": "https://developer.salesforce.com/docs/data/guide/child.html",
                "title": "Run a Query", "navLabel": "Run a Query", "identifier": "/child", "depth": 1, "parent": "Query Guide",
                "contentHash": "child", "status": "captured", "topics": ["Query SQL"], "topicTags": ["query-and-sql"],
                "lead": "Run Query SQL", "guideFamily": "query-guide",
            },
        ]
        graph = docs_watch.build_graph(records, phases, "now")
        edges = {(edge["from"], edge["to"], edge["type"]) for edge in graph["edges"]}
        self.assertIn(("page:child", "page:parent", "discovered-from"), edges)
        self.assertIn(("page:child", "skill:sf-datacloud-retrieve", "informs-skill"), edges)

    def test_proof_ledger_contract_parser(self):
        row = "| `BEAST-PROOF-001` | source | surface | connect | assumption | proof | caveat | tested | none | promoted |"
        cells = validate_docs_watch.parse_markdown_row(row)
        self.assertEqual(len(cells), 10)
        self.assertEqual(cells[0], "`BEAST-PROOF-001`")

    def test_graph_counts_support_public_metadata(self):
        graph = {
            "nodes": [
                {"type": "official-page", "sourceType": "help", "status": "captured"},
                {"type": "official-page", "sourceType": "developer", "status": "captured"},
                {"type": "official-page", "sourceType": "developer", "status": "cataloged"},
            ]
        }
        pages = [node for node in graph["nodes"] if node["type"] == "official-page"]
        self.assertEqual(sum(node["sourceType"] == "help" for node in pages), 1)
        self.assertEqual(sum(node["sourceType"] == "developer" for node in pages), 2)

    def test_reconciliation_detects_new_changed_and_removed(self):
        with tempfile.TemporaryDirectory() as temp:
            old = ROOT / "docs/data360/docs-knowledge-graph.json"
            original = old.read_text(encoding="utf-8") if old.exists() else None
            old.write_text(json.dumps({"nodes": [{"type": "official-page", "source": "https://help.salesforce.com/removed", "contentHash": "a"}, {"type": "official-page", "source": "https://help.salesforce.com/changed", "contentHash": "a"}]}), encoding="utf-8")
            try:
                record = {"id": "page:new", "source": "https://help.salesforce.com/changed", "title": "Changed limits", "lead": "limits", "topics": [], "contentHash": "b", "status": "captured", "sourceType": "help", "identifier": "changed", "depth": 0, "parent": None}
                result = docs_watch.reconcile(
                    [record],
                    {"scope": {"contentHashContract": "test-v1"}, "edges": [], "nodes": []},
                    "now",
                    previous_graph={
                        "scope": {"contentHashContract": "test-v1"},
                        "nodes": [
                            {"type": "official-page", "source": "https://help.salesforce.com/removed", "contentHash": "a"},
                            {"type": "official-page", "source": "https://help.salesforce.com/changed", "contentHash": "a"},
                        ],
                    },
                )
                self.assertEqual(result["newPages"], [])
                self.assertEqual(result["removedPages"], ["https://help.salesforce.com/removed"])
                self.assertEqual(result["changedPages"], ["https://help.salesforce.com/changed"])
            finally:
                if original is None:
                    old.unlink(missing_ok=True)
                else:
                    old.write_text(original, encoding="utf-8")

    def test_reconciliation_separates_hash_contract_migration(self):
        record = {
            "id": "page:changed", "source": "https://developer.salesforce.com/docs/data/changed",
            "title": "Changed", "lead": "", "topics": [], "topicTags": [], "contentHash": "new",
            "status": "captured", "sourceType": "developer", "identifier": "changed", "depth": 0,
            "parent": None, "guideFamily": "developer-guide",
        }
        result = docs_watch.reconcile(
            [record],
            {"scope": {"contentHashContract": "crawler-content-sha256-v1"}, "edges": [], "nodes": []},
            "now",
            previous_graph={
                "scope": {},
                "nodes": [{"type": "official-page", "source": record["source"], "contentHash": "old"}],
            },
        )
        self.assertEqual(result["changedPages"], [])
        self.assertEqual(result["rehashedPages"], [record["source"]])

    def test_companion_allowlist_is_exact(self):
        contract = {"upstream": {}, "observedFiles": {"skills/data360-connect/SKILL.md": {"sha256": "old"}}}
        observed = {"packageName": "pkg", "packageVersion": "1", "files": {"skills/data360-connect/SKILL.md": {"sha256": "new"}}, "skills": ["data360-connect"]}
        result = sf_skills_drift.compare(observed, contract)
        self.assertEqual(result["changedFiles"], ["skills/data360-connect/SKILL.md"])
        self.assertIn("content", result["categories"])

    def test_marker_refresh_preserves_unrelated_blocks(self):
        original = """# Skill\n\n## Doc-Synced Notes\n\n<!-- SF_DOC_SYNC_START:keep -->\nkeep this evidence\n<!-- SF_DOC_SYNC_END:keep -->\n\n<!-- SF_DOC_SYNC_START:update -->\nold\n<!-- SF_DOC_SYNC_END:update -->\n"""
        replacement = refresh_skills.apply_doc_synced_blocks(original, {"update": "new"})
        self.assertIn("keep this evidence", replacement)
        self.assertIn("new", replacement)

    def test_marker_refresh_does_not_duplicate_doc_synced_heading(self):
        original = "# Skill\n\n## Doc-Synced Notes\n\nexisting\n"
        replacement = refresh_skills.apply_doc_synced_blocks(original, {"new": "new evidence"})
        self.assertEqual(replacement.count("## Doc-Synced Notes"), 1)

    def test_developer_evidence_block_has_sources_and_fingerprint(self):
        source = {
            "source": "https://developer.salesforce.com/docs/data/test",
            "title": "Test Data 360 Guide",
            "contentHash": "abc123",
        }
        block = refresh_skills.render_developer_block("Developer gate", [source], ["Verify target metadata."])
        self.assertIn(source["source"], block)
        self.assertIn("Source fingerprint", block)
        self.assertIn("Verify target metadata", block)


if __name__ == "__main__":
    unittest.main()
