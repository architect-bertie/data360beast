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


class DocsWatchTests(unittest.TestCase):
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

    def test_reconciliation_detects_new_changed_and_removed(self):
        with tempfile.TemporaryDirectory() as temp:
            old = ROOT / "docs/data360/docs-knowledge-graph.json"
            original = old.read_text(encoding="utf-8") if old.exists() else None
            old.write_text(json.dumps({"nodes": [{"type": "official-page", "source": "https://help.salesforce.com/removed", "contentHash": "a"}, {"type": "official-page", "source": "https://help.salesforce.com/changed", "contentHash": "a"}]}), encoding="utf-8")
            try:
                record = {"id": "page:new", "source": "https://help.salesforce.com/changed", "title": "Changed limits", "lead": "limits", "topics": [], "contentHash": "b", "status": "captured", "sourceType": "help", "identifier": "changed", "depth": 0, "parent": None}
                result = docs_watch.reconcile([record], {"scope": {}, "edges": [], "nodes": []}, "now")
                self.assertEqual(result["newPages"], [])
                self.assertEqual(result["removedPages"], ["https://help.salesforce.com/removed"])
                self.assertEqual(result["changedPages"], ["https://help.salesforce.com/changed"])
            finally:
                if original is None:
                    old.unlink(missing_ok=True)
                else:
                    old.write_text(original, encoding="utf-8")

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


if __name__ == "__main__":
    unittest.main()
