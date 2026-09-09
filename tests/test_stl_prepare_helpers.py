"""Unit tests for the sf-datacloud-prepare STL helper scripts.

Loads each script by path (they live under skills/.../scripts/ and are not
importable as a package) and exercises the pure, org-free helpers plus the
ConnectClient request layer with an injected fake runner.
"""
import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "skills/sf-datacloud-prepare/scripts"


def load(module_name: str, filename: str):
    spec = importlib.util.spec_from_file_location(module_name, SCRIPTS / filename)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


ref_check = load("stl_ref_check", "stl_ref_check.py")
builder_shape = load("stl_builder_shape", "stl_builder_shape.py")
bisect = load("stl_activation_bisect", "stl_activation_bisect.py")


def fake_result(stdout="", returncode=0, stderr=""):
    return type(
        "R", (), {"stdout": stdout, "returncode": returncode, "stderr": stderr}
    )()


class RefCheckTests(unittest.TestCase):
    def test_join_qualifier_renames_right_side(self):
        nodes = {
            "L": {"action": "load", "parameters": {"fields": ["A", "B"]}},
            "R": {"action": "load", "parameters": {"fields": ["C"]}},
            "J": {
                "action": "join",
                "parameters": {"rightQualifier": "r"},
                "sources": ["L", "R"],
            },
        }
        cols = ref_check.node_columns(nodes)
        self.assertEqual(cols("J"), {"A", "B", "r.C"})

    def test_bare_and_qualified_unresolved(self):
        nodes = {
            "L": {"action": "load", "parameters": {"fields": ["A", "B"]}},
            "R": {"action": "load", "parameters": {"fields": ["C"]}},
            "J": {
                "action": "join",
                "parameters": {"rightQualifier": "r"},
                "sources": ["L", "R"],
            },
            "F": {
                "action": "formula",
                "sources": ["J"],
                "parameters": {
                    "fields": [{
                        "name": "OUT",
                        # r.C resolves; A resolves; MISSING and q.C do not.
                        "formulaExpression": '"r.C" + A + MISSING + "q.C"',
                    }],
                },
            },
        }
        import json
        import tempfile

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as handle:
            json.dump({"definition": {"nodes": nodes}}, handle)
            path = handle.name
        bad = ref_check.unresolved(path)
        Path(path).unlink()
        refs = {(ref, kind) for _, _, ref, kind in bad}
        self.assertIn(("MISSING", "bare"), refs)
        self.assertIn(("q.C", "qualified"), refs)
        self.assertNotIn(("A", "bare"), refs)


class BuilderShapeTests(unittest.TestCase):
    def test_expand_multi_field_formula(self):
        nodes = {
            "L": {"action": "load", "parameters": {"fields": ["A"]}},
            "F": {
                "action": "formula",
                "sources": ["L"],
                "parameters": {
                    "fields": [
                        {"name": "X", "formulaExpression": "A"},
                        {"name": "Y", "formulaExpression": "A"},
                    ]
                },
            },
            "O": {"action": "outputD360", "parameters": {}, "sources": ["F"]},
        }
        expanded = builder_shape.expand_formula_nodes(nodes)
        formula_nodes = [
            n for n in expanded.values()
            if n["action"] == "formula"
        ]
        self.assertTrue(all(len(n["parameters"]["fields"]) == 1 for n in formula_nodes))
        self.assertEqual(len(formula_nodes), 2)
        # Output is rewired to the tail of the expanded formula chain.
        self.assertNotEqual(expanded["O"]["sources"], ["F"])

    def test_aggregate_over_aggregate_rejected(self):
        nodes = {
            "L": {"action": "load", "parameters": {"fields": ["A"]}},
            "AGG1": {
                "action": "aggregate",
                "sources": ["L"],
                "parameters": {"groupings": ["A"], "aggregations": []},
            },
            "AGG2": {
                "action": "aggregate",
                "sources": ["AGG1"],
                "parameters": {"groupings": ["A"], "aggregations": []},
            },
        }
        with self.assertRaises(AssertionError):
            builder_shape.assert_no_aggregate_over_aggregate(nodes)

    def test_aggregate_over_load_ok(self):
        nodes = {
            "L": {"action": "load", "parameters": {"fields": ["A"]}},
            "AGG": {
                "action": "aggregate",
                "sources": ["L"],
                "parameters": {"groupings": ["A"], "aggregations": []},
            },
        }
        builder_shape.assert_no_aggregate_over_aggregate(nodes)

    def test_attach_grain_extraction(self):
        nodes = {
            "L": {"action": "load", "parameters": {"fields": ["A"]}},
            "AGG": {
                "action": "aggregate",
                "sources": ["L"],
                "parameters": {"groupings": ["A"], "aggregations": []},
            },
        }
        attached = builder_shape.attach_grain_extractions(nodes)
        self.assertIn("GRAIN_AGG", attached)
        self.assertEqual(attached["GRAIN_AGG"]["action"], "extractGrains")
        self.assertEqual(attached["AGG"]["sources"], ["GRAIN_AGG"])


def sample_full():
    return {
        "type": "BATCH",
        "primarySource": {"name": "SRC"},
        "definition": {
            "type": "SQL",
            "version": "1",
            "nodes": {
                "L": {"action": "load", "parameters": {"fields": ["A"]}},
                "F": {
                    "action": "formula",
                    "sources": ["L"],
                    "parameters": {"fields": [{"name": "X", "formulaExpression": "A"}]},
                },
                "O": {
                    "action": "outputD360",
                    "sources": ["F"],
                    "parameters": {
                        "name": "PROD__dll",
                        "fieldsMappings": [
                            {"sourceField": "X", "targetField": "X__c"},
                            {"sourceField": "A", "targetField": "A__c"},
                        ],
                    },
                },
            },
        },
    }


class BisectHelperTests(unittest.TestCase):
    def test_ancestors(self):
        nodes = sample_full()["definition"]["nodes"]
        self.assertEqual(bisect.ancestors(nodes, "F"), {"F", "L"})

    def test_build_probe_shape(self):
        probe = bisect.build_probe(sample_full(), "F", "DTTMP00", "SCRATCH__dll", "RecordKey__c")
        nodes = probe["definition"]["nodes"]
        self.assertIn("PROBE_KEY", nodes)
        self.assertIn("PROBE_OUT", nodes)
        # Only ancestors of the cut are kept, plus the two probe nodes.
        self.assertEqual(set(nodes) - {"PROBE_KEY", "PROBE_OUT"}, {"F", "L"})
        self.assertEqual(nodes["PROBE_OUT"]["parameters"]["name"], "SCRATCH__dll")
        self.assertEqual(
            nodes["PROBE_OUT"]["parameters"]["fieldsMappings"][0]["targetField"],
            "RecordKey__c",
        )
        # No builder-only ui layer is emitted.
        self.assertNotIn("ui", probe["definition"])

    def test_build_output_probe_prefix(self):
        probe = bisect.build_output_probe(
            sample_full(), limit=1, name="DTTMP01", scratch_dlo="SCRATCH__dll"
        )
        output = next(
            n for n in probe["definition"]["nodes"].values()
            if n["action"] == "outputD360"
        )
        self.assertEqual(len(output["parameters"]["fieldsMappings"]), 1)
        self.assertEqual(output["parameters"]["name"], "SCRATCH__dll")

    def test_build_output_probe_rejects_bad_limit(self):
        with self.assertRaises(ValueError):
            bisect.build_output_probe(
                sample_full(), limit=9, name="DTTMP01", scratch_dlo="SCRATCH__dll"
            )

    def test_probe_name_length_guard(self):
        self.assertEqual(bisect.probe_name("DTTMPBISECT", 3), "DTTMPBISECT03")
        with self.assertRaises(ValueError):
            bisect.probe_name("D" * 31, 3)


class ResolveApiVersionTests(unittest.TestCase):
    def test_reads_org_api_version(self):
        runner = lambda _: fake_result(stdout='{"result": {"apiVersion": "63.0"}}')
        self.assertEqual(bisect.resolve_api_version("org", runner=runner), "63.0")

    def test_falls_back_when_missing(self):
        runner = lambda _: fake_result(stdout='{"result": {}}')
        self.assertEqual(
            bisect.resolve_api_version("org", runner=runner),
            bisect.DEFAULT_API_VERSION,
        )


class ConnectClientTests(unittest.TestCase):
    def test_get_returns_none_on_item_not_found(self):
        runner = lambda _: fake_result(
            stdout='[{"errorCode": "ITEM_NOT_FOUND"}]', returncode=1
        )
        client = bisect.ConnectClient("org", "66.0", runner=runner)
        self.assertIsNone(client.get("DTMISSING"))

    def test_get_returns_parsed_body(self):
        runner = lambda _: fake_result(stdout='{"status": "ACTIVE"}')
        client = bisect.ConnectClient("org", "66.0", runner=runner)
        self.assertEqual(client.get("DTX"), {"status": "ACTIVE"})

    def test_request_raises_on_error(self):
        runner = lambda _: fake_result(stdout="", returncode=1, stderr="boom")
        client = bisect.ConnectClient("org", "66.0", runner=runner)
        with self.assertRaises(RuntimeError):
            client.request("/x", "GET")


if __name__ == "__main__":
    unittest.main()
