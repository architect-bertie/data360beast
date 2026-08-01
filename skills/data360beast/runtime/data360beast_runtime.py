"""Safe, portable desired-state planning and execution for Data 360."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable


ROOT = Path(__file__).resolve().parents[3]
RESOURCE_STATES = {
    "planned", "blocked", "ready", "applying", "waiting", "verifying",
    "proven", "failed", "repairable", "manual-handoff", "rolled-back",
}
CAPABILITY_STATES = {"supported", "unsupported", "manual", "blocked", "unverified"}
MUTATING_METHODS = {"POST", "PUT", "PATCH", "DELETE"}


class ContractError(ValueError):
    """Raised when a Beast public contract is incomplete or unsafe."""


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def run_home() -> Path:
    return Path(os.environ.get("DATA360BEAST_HOME", Path.home() / ".data360beast"))


def validate_spec(spec: dict[str, Any]) -> list[str]:
    issues: list[str] = []
    if spec.get("schemaVersion") != "implementation-spec/v1":
        issues.append("schemaVersion must be implementation-spec/v1")
    target = spec.get("target")
    if not isinstance(target, dict) or not target.get("orgAlias"):
        issues.append("target.orgAlias is required")
    if not isinstance(target, dict) or target.get("environment") not in {"lab", "sandbox", "production"}:
        issues.append("target.environment must be lab, sandbox, or production")
    policy = spec.get("policy")
    if not isinstance(policy, dict):
        issues.append("policy is required")
    elif policy.get("productionMutationApproval") not in {"required", "granted"}:
        issues.append("policy.productionMutationApproval must be required or granted")
    resources = spec.get("resources")
    if not isinstance(resources, list) or not resources:
        issues.append("resources must contain at least one desired resource")
        return issues
    seen: set[str] = set()
    for item in resources:
        resource_id = item.get("id") if isinstance(item, dict) else None
        if not resource_id or not isinstance(resource_id, str):
            issues.append("each resource requires a string id")
            continue
        if resource_id in seen:
            issues.append(f"duplicate resource id: {resource_id}")
        seen.add(resource_id)
        if item.get("phase") not in {
            "connect", "prepare", "harmonize", "govern", "retrieve", "insight",
            "semantic", "ai-search", "segment", "act", "automation", "develop-package",
        }:
            issues.append(f"{resource_id}: unknown phase")
        if item.get("executor") not in {"sf-rest", "sf-data360", "metadata", "manual", "browser-lab"}:
            issues.append(f"{resource_id}: unsupported executor")
        for dependency in item.get("dependsOn", []):
            if not isinstance(dependency, str):
                issues.append(f"{resource_id}: dependency ids must be strings")
    return issues


def ordered_resources(resources: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_id = {item["id"]: item for item in resources}
    missing = sorted({dep for item in resources for dep in item.get("dependsOn", []) if dep not in by_id})
    if missing:
        raise ContractError("resources depend on unknown ids: " + ", ".join(missing))
    ordered: list[dict[str, Any]] = []
    remaining = dict(by_id)
    while remaining:
        ready = sorted(
            (item for item in remaining.values() if all(dep not in remaining for dep in item.get("dependsOn", []))),
            key=lambda item: item["id"],
        )
        if not ready:
            raise ContractError("resource dependency graph contains a cycle")
        for item in ready:
            ordered.append(item)
            remaining.pop(item["id"])
    return ordered


def default_runner(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, text=True, capture_output=True, check=False)


def discover_target(target: dict[str, Any], runner: Callable[[list[str]], Any] = default_runner) -> dict[str, Any]:
    result = runner(["sf", "org", "display", "--target-org", target["orgAlias"], "--json"])
    if getattr(result, "returncode", 1) != 0:
        return {"org": "unverified", "dataSpaces": "unverified", "reason": getattr(result, "stderr", "sf org display failed").strip()}
    try:
        org = json.loads(result.stdout).get("result", {})
    except json.JSONDecodeError:
        return {"org": "unverified", "dataSpaces": "unverified", "reason": "sf org display returned invalid JSON"}
    data_spaces = "unverified"
    api = runner([
        "sf", "api", "request", "rest", "--target-org", target["orgAlias"],
        "--method", "GET", "--url", "/services/data/v66.0/ssot/data-spaces", "--json",
    ])
    if getattr(api, "returncode", 1) == 0:
        try:
            payload = json.loads(api.stdout).get("result", {})
            data_spaces = [item.get("name") for item in payload.get("dataSpaces", payload.get("items", [])) if item.get("name")]
        except json.JSONDecodeError:
            pass
    return {
        "org": "supported",
        "orgId": org.get("id"),
        "instanceUrl": org.get("instanceUrl"),
        "isSandbox": org.get("isSandbox"),
        "dataSpaces": data_spaces,
    }


def capability_matrix(spec: dict[str, Any], discovery: dict[str, Any]) -> list[dict[str, str]]:
    requested = spec.get("capabilityRequirements", [])
    return [
        {
            "capability": str(item.get("name", item)) if isinstance(item, dict) else str(item),
            "status": "supported" if discovery.get("org") == "supported" else "unverified",
            "reason": "target-org discovery" if discovery.get("org") == "supported" else discovery.get("reason", "org unavailable"),
        }
        for item in requested
    ]


def plan_spec(spec: dict[str, Any], runner: Callable[[list[str]], Any] = default_runner) -> dict[str, Any]:
    issues = validate_spec(spec)
    if issues:
        raise ContractError("; ".join(issues))
    discovery = discover_target(spec["target"], runner)
    actions = []
    for resource in ordered_resources(spec["resources"]):
        executor = resource["executor"]
        state = "manual-handoff" if executor == "manual" else "planned"
        if executor == "browser-lab" and spec["target"]["environment"] != "lab":
            state = "manual-handoff"
        actions.append({
            "id": resource["id"], "phase": resource["phase"], "kind": resource.get("kind", "resource"),
            "executor": executor, "dependsOn": resource.get("dependsOn", []), "desired": resource.get("desired", {}),
            "request": resource.get("request"), "proof": resource.get("proof", {}),
            "rollback": resource.get("rollback", {"mode": "manual"}), "state": state,
            "mutationClass": resource.get("mutationClass", "create"),
            "reason": "manual surface" if state == "manual-handoff" else "ready for preflight and execution",
        })
    return {
        "schemaVersion": "deployment-plan/v1", "generatedAt": utc_now(),
        "specId": spec.get("id", "unnamed"), "target": spec["target"], "policy": spec["policy"],
        "capabilities": capability_matrix(spec, discovery), "discovery": discovery, "actions": actions,
    }


def create_run(plan: dict[str, Any], run_id: str | None = None) -> tuple[Path, dict[str, Any]]:
    run_id = run_id or f"run-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}-{uuid.uuid4().hex[:8]}"
    root = run_home() / "runs" / run_id
    state = {
        "schemaVersion": "run-state/v1", "runId": run_id, "createdAt": utc_now(), "updatedAt": utc_now(),
        "planDigest": hashlib.sha256(json.dumps(plan, sort_keys=True).encode()).hexdigest(),
        "target": plan["target"], "actions": [dict(action) for action in plan["actions"]], "outcome": "planned",
    }
    write_json(root / "plan.json", plan)
    write_json(root / "state.json", state)
    return root, state


def resolve_run(run: str) -> Path:
    candidate = Path(run)
    if candidate.is_dir():
        return candidate
    return run_home() / "runs" / run


def load_run_state(run: str) -> tuple[Path, dict[str, Any]]:
    root = resolve_run(run)
    return root, load_json(root / "state.json")


def assert_execution_allowed(plan: dict[str, Any], execute: bool, approve_production: bool) -> None:
    if not execute:
        raise ContractError("refusing mutation without --execute")
    environment = plan["target"]["environment"]
    if environment == "production" and (not approve_production or plan["policy"].get("productionMutationApproval") != "granted"):
        raise ContractError("production mutation requires --approve-production and policy.productionMutationApproval=granted")


def apply_plan(plan: dict[str, Any], execute: bool, approve_production: bool, runner: Callable[[list[str]], Any] = default_runner) -> tuple[Path, dict[str, Any]]:
    assert_execution_allowed(plan, execute, approve_production)
    root, state = create_run(plan)
    for action in state["actions"]:
        if action["state"] == "manual-handoff":
            continue
        if action["executor"] not in {"sf-rest", "sf-data360", "metadata"}:
            action["state"] = "manual-handoff"
            action["reason"] = "no supported portable executor"
            continue
        request = action.get("request") or {}
        method = str(request.get("method", "")).upper()
        path = request.get("path")
        if action["executor"] != "sf-rest" or method not in MUTATING_METHODS or not isinstance(path, str) or not path.startswith("/services/"):
            action["state"] = "blocked"
            action["reason"] = "resource lacks an explicit supported sf-rest mutation request"
            continue
        command = ["sf", "api", "request", "rest", "--target-org", plan["target"]["orgAlias"], "--method", method, "--url", path, "--json"]
        if "body" in request:
            command.extend(["--body", json.dumps(request["body"])])
        action["state"] = "applying"
        result = runner(command)
        action["resultCode"] = getattr(result, "returncode", 1)
        action["state"] = "proven" if action["resultCode"] == 0 else "repairable"
        action["reason"] = "mutation command returned successfully" if action["resultCode"] == 0 else getattr(result, "stderr", "mutation failed").strip()[:500]
    state["outcome"] = "proven" if all(action["state"] in {"proven", "manual-handoff"} for action in state["actions"]) else "needs-repair"
    state["updatedAt"] = utc_now()
    write_json(root / "state.json", state)
    return root, state


def verify_run(run: str, runner: Callable[[list[str]], Any] = default_runner) -> tuple[Path, dict[str, Any]]:
    root, state = load_run_state(run)
    for action in state["actions"]:
        proof = action.get("proof") or {}
        request = proof.get("request") or {}
        path = request.get("path")
        if action.get("state") != "proven" or not isinstance(path, str) or not path.startswith("/services/"):
            continue
        result = runner(["sf", "api", "request", "rest", "--target-org", state["target"]["orgAlias"], "--method", "GET", "--url", path, "--json"])
        if getattr(result, "returncode", 1) != 0:
            action["state"] = "repairable"
            action["reason"] = getattr(result, "stderr", "proof readback failed").strip()[:500]
    state["outcome"] = "proven" if all(action["state"] in {"proven", "manual-handoff"} for action in state["actions"]) else "needs-repair"
    state["updatedAt"] = utc_now()
    write_json(root / "state.json", state)
    return root, state


def repair_run(run: str) -> tuple[Path, dict[str, Any]]:
    root, state = load_run_state(run)
    for action in state["actions"]:
        if action.get("state") == "repairable":
            action["state"] = "planned"
            action["reason"] = "repair requires an explicit new apply plan"
    state["outcome"] = "planned"
    state["updatedAt"] = utc_now()
    write_json(root / "state.json", state)
    return root, state


def destroy_run(run: str, execute: bool, runner: Callable[[list[str]], Any] = default_runner) -> tuple[Path, dict[str, Any]]:
    root, state = load_run_state(run)
    if state["target"].get("environment") != "lab":
        raise ContractError("destroy is restricted to lab runs")
    if not execute:
        raise ContractError("refusing cleanup mutation without --execute")
    for action in reversed(state["actions"]):
        rollback = action.get("rollback") or {}
        request = rollback.get("request") or {}
        path = request.get("path")
        if action.get("state") != "proven" or request.get("method", "").upper() != "DELETE" or not isinstance(path, str) or not path.startswith("/services/"):
            continue
        result = runner(["sf", "api", "request", "rest", "--target-org", state["target"]["orgAlias"], "--method", "DELETE", "--url", path, "--json"])
        action["state"] = "rolled-back" if getattr(result, "returncode", 1) == 0 else "repairable"
        action["reason"] = "lab cleanup succeeded" if action["state"] == "rolled-back" else getattr(result, "stderr", "cleanup failed").strip()[:500]
    state["outcome"] = "rolled-back"
    state["updatedAt"] = utc_now()
    write_json(root / "state.json", state)
    return root, state


def knowledge_query(goal: str, phase: str | None = None) -> dict[str, Any]:
    claims_path = ROOT / "docs" / "data360" / "knowledge" / "claims.json"
    claims = load_json(claims_path).get("claims", [])
    terms = {term.lower() for term in goal.replace("/", " ").replace("-", " ").split() if len(term) > 2}
    selected = []
    for claim in claims:
        haystack = " ".join(str(claim.get(key, "")) for key in ("subject", "predicate", "object", "phase", "caveat")).lower()
        if (not phase or claim.get("phase") == phase) and (not terms or any(term in haystack for term in terms)):
            selected.append(claim)
    selected.sort(key=lambda item: item["id"])
    return {"schemaVersion": "knowledge-query/v1", "goal": goal, "phase": phase, "claims": selected, "count": len(selected)}
