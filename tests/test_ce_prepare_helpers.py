"""Unit tests for the sf-datacloud-prepare code-extension helper scripts.

Loads each script by path (they live under skills/.../scripts/ and are not
importable as a package) and exercises the offline helpers plus the diagnostics
collect path with an injected fake runner. The scripts dir is placed on sys.path
so ce_run_diagnostics can import the ConnectClient transport it reuses.
"""
import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "skills/sf-datacloud-prepare/scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))


def load(module_name: str, filename: str):
    spec = importlib.util.spec_from_file_location(module_name, SCRIPTS / filename)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


# stl_activation_bisect loaded first so ce_run_diagnostics' import resolves it.
load("stl_activation_bisect", "stl_activation_bisect.py")
closure_mod = load("ce_payload_closure", "ce_payload_closure.py")
diagnostics = load("ce_run_diagnostics", "ce_run_diagnostics.py")


def fake_result(stdout="", returncode=0, stderr=""):
    return type(
        "R", (), {"stdout": stdout, "returncode": returncode, "stderr": stderr}
    )()


class PayloadClosureTests(unittest.TestCase):
    def _tree(self):
        """A source pkg, a payload with roots, and a payload closure copy."""
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        tmp = Path(directory.name)
        source = tmp / "src"
        payload = tmp / "payload"
        copy = payload / "closure"
        source.mkdir()
        copy.mkdir(parents=True)
        # source modules: a imports b (relative), b imports nothing local.
        (source / "a.py").write_text("from . import b\nimport os\n")
        (source / "b.py").write_text("x = 1\n")
        (source / "unused.py").write_text("import snowflake.connector\n")
        # root under payload imports a.
        (payload / "entrypoint.py").write_text("import a\n")
        return tmp, source, payload, copy

    def test_local_imports_filters_to_known(self):
        tmp, source, payload, _ = self._tree()
        known = {"a", "b", "unused"}
        self.assertEqual(
            closure_mod.local_imports(payload / "entrypoint.py", known), {"a"}
        )
        # relative `from . import b` plus stdlib `os` -> only b is known.
        self.assertEqual(closure_mod.local_imports(source / "a.py", known), {"b"})

    def test_closure_is_transitive_and_excludes_unreached(self):
        tmp, source, payload, _ = self._tree()
        names = {p.name for p in closure_mod.closure(["entrypoint"], source, payload)}
        self.assertEqual(names, {"a.py", "b.py"})
        self.assertNotIn("unused.py", names)

    def test_drift_detects_unreachable_and_missing(self):
        tmp, source, payload, copy = self._tree()
        # A correct copy has no drift.
        closure_mod.write(["entrypoint"], source, payload, copy)
        self.assertEqual(
            closure_mod.drift(["entrypoint"], source, payload, copy), []
        )
        # Add an unreachable module to the copy -> flagged.
        (copy / "unused.py").write_text("import snowflake.connector\n")
        problems = closure_mod.drift(["entrypoint"], source, payload, copy)
        self.assertTrue(any("unreachable in payload: unused.py" in p for p in problems))
        # Remove a required module -> flagged missing.
        (copy / "b.py").unlink()
        problems = closure_mod.drift(["entrypoint"], source, payload, copy)
        self.assertTrue(any("missing from payload: b.py" in p for p in problems))

    def test_drift_detects_content_difference(self):
        tmp, source, payload, copy = self._tree()
        closure_mod.write(["entrypoint"], source, payload, copy)
        (copy / "b.py").write_text("x = 999\n")  # diverge from source
        problems = closure_mod.drift(["entrypoint"], source, payload, copy)
        self.assertTrue(any("differs from source: b.py" in p for p in problems))


class LogsQueryTests(unittest.TestCase):
    def test_query_is_scoped_with_limit(self):
        sql = diagnostics.build_logs_query('ce_engine', limit=25)
        self.assertIn('"ProcessDefinitionName__c" = \'ce_engine\'', sql)
        self.assertTrue(sql.endswith('LIMIT 25'))
        self.assertNotIn('SELECT *', sql)

    def test_execution_filter(self):
        sql = diagnostics.build_logs_query('ce_engine', limit=5, execution_id='run-1')
        self.assertIn('"ExecutionId__c" = \'run-1\'', sql)

    def test_bad_limit_rejected(self):
        for limit in (0, 5000):
            with self.assertRaises(ValueError):
                diagnostics.build_logs_query('ce_engine', limit=limit)


class RunHistorySummaryTests(unittest.TestCase):
    def test_terminal_failure_row(self):
        history = {"histories": [
            {"status": "FAILURE", "processedRows": 0, "outputStatus": {}}
        ]}
        self.assertEqual(
            diagnostics.summarize_run_history(history),
            {"status": "FAILURE", "processedRows": 0, "errorMessage": ""},
        )

    def test_empty_history(self):
        self.assertEqual(
            diagnostics.summarize_run_history({"histories": []}),
            {"status": None, "processedRows": None, "errorMessage": None},
        )
        self.assertEqual(
            diagnostics.summarize_run_history(None),
            {"status": None, "processedRows": None, "errorMessage": None},
        )


class CollectTests(unittest.TestCase):
    def test_collect_pulls_run_and_logs(self):
        def runner(command):
            joined = " ".join(command)
            if "run-history" in joined:
                return fake_result(
                    stdout='{"histories":[{"status":"FAILURE","processedRows":0}]}'
                )
            return fake_result(stdout='{"data":[["log-row"]]}')

        client = diagnostics.ConnectClient("org", "66.0", runner=runner)
        report = diagnostics.collect(client, "66.0", "ce_engine", limit=5)
        self.assertEqual(report["transform"], "ce_engine")
        self.assertEqual(report["run"]["status"], "FAILURE")
        self.assertEqual(report["logs"]["data"], [["log-row"]])
        self.assertFalse(report["complete"])


if __name__ == "__main__":
    unittest.main()
