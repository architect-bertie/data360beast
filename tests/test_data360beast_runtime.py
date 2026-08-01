import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / "skills/data360beast/runtime/data360beast_runtime.py"
SPEC = importlib.util.spec_from_file_location("data360beast_runtime", RUNTIME)
runtime = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = runtime
SPEC.loader.exec_module(runtime)


class RuntimeTests(unittest.TestCase):
    def spec(self, environment="lab"):
        return {
            "schemaVersion": "implementation-spec/v1", "id": "test",
            "target": {"orgAlias": "example", "environment": environment},
            "policy": {"productionMutationApproval": "required"},
            "capabilityRequirements": ["data-spaces"],
            "resources": [
                {"id": "connection", "phase": "connect", "executor": "sf-rest"},
                {"id": "stream", "phase": "prepare", "executor": "manual", "dependsOn": ["connection"]},
            ],
        }

    def test_validates_and_orders_resources(self):
        plan = runtime.plan_spec(self.spec(), runner=lambda _: type("R", (), {"returncode": 1, "stderr": "no auth"})())
        self.assertEqual([item["id"] for item in plan["actions"]], ["connection", "stream"])
        self.assertEqual(plan["actions"][1]["state"], "manual-handoff")

    def test_rejects_dependency_cycles(self):
        spec = self.spec()
        spec["resources"][0]["dependsOn"] = ["stream"]
        with self.assertRaises(runtime.ContractError):
            runtime.plan_spec(spec, runner=lambda _: type("R", (), {"returncode": 1, "stderr": "no auth"})())

    def test_production_requires_approval(self):
        spec = self.spec("production")
        plan = runtime.plan_spec(spec, runner=lambda _: type("R", (), {"returncode": 1, "stderr": "no auth"})())
        with self.assertRaises(runtime.ContractError):
            runtime.assert_execution_allowed(plan, True, False)

    def test_knowledge_query_returns_source_backed_claims(self):
        result = runtime.knowledge_query("activation delivery", "act")
        self.assertEqual(result["count"], 1)
        self.assertEqual(result["claims"][0]["id"], "KC-006")

    def test_destroy_requires_lab_and_execute(self):
        with tempfile.TemporaryDirectory() as temp:
            old_home = runtime.run_home
            runtime.run_home = lambda: Path(temp)
            try:
                plan = runtime.plan_spec(self.spec(), runner=lambda _: type("R", (), {"returncode": 1, "stderr": "no auth"})())
                root, state = runtime.create_run(plan, "test-run")
                with self.assertRaises(runtime.ContractError):
                    runtime.destroy_run("test-run", False)
            finally:
                runtime.run_home = old_home


if __name__ == "__main__":
    unittest.main()
