#!/usr/bin/env python3
"""Data360 Beast desired-state runtime command."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

RUNTIME = Path(__file__).resolve().parents[1] / "runtime"
sys.path.insert(0, str(RUNTIME))
from data360beast_runtime import ContractError, apply_plan, destroy_run, discover_target, knowledge_query, load_json, plan_spec, repair_run, validate_spec, verify_run


def output(value: dict) -> None:
    print(json.dumps(value, indent=2, sort_keys=True))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("preflight", "plan"):
        command = sub.add_parser(name)
        command.add_argument("--spec", type=Path, required=True)
    apply = sub.add_parser("apply")
    apply.add_argument("--plan", type=Path, required=True)
    apply.add_argument("--execute", action="store_true")
    apply.add_argument("--approve-production", action="store_true")
    resume = sub.add_parser("resume")
    resume.add_argument("--run", required=True)
    verify = sub.add_parser("verify")
    verify.add_argument("--run", required=True)
    repair = sub.add_parser("repair")
    repair.add_argument("--run", required=True)
    destroy = sub.add_parser("destroy")
    destroy.add_argument("--run", required=True)
    destroy.add_argument("--lab-only", action="store_true")
    destroy.add_argument("--execute", action="store_true")
    certify = sub.add_parser("certify")
    certify.add_argument("--pack", required=True)
    certify.add_argument("--target-org", required=True)
    knowledge = sub.add_parser("knowledge")
    knowledge_sub = knowledge.add_subparsers(dest="knowledge_command", required=True)
    query = knowledge_sub.add_parser("query")
    query.add_argument("--goal", required=True)
    query.add_argument("--phase")
    args = parser.parse_args()
    try:
        if args.command == "knowledge":
            output(knowledge_query(args.goal, args.phase))
            return 0
        if args.command in {"preflight", "plan"}:
            spec = load_json(args.spec)
            if args.command == "preflight":
                issues = validate_spec(spec)
                output({"schemaVersion": "preflight/v1", "valid": not issues, "issues": issues})
                return 0 if not issues else 2
            output(plan_spec(spec))
            return 0
        if args.command == "apply":
            plan = load_json(args.plan)
            root, state = apply_plan(plan, args.execute, args.approve_production)
            output({"runDirectory": str(root), "state": state})
            return 0
        if args.command == "verify":
            root, state = verify_run(args.run)
            output({"runDirectory": str(root), "state": state})
            return 0
        if args.command in {"resume", "repair"}:
            root, state = repair_run(args.run)
            output({"runDirectory": str(root), "state": state})
            return 0
        if args.command == "destroy":
            if not args.lab_only:
                raise ContractError("destroy requires --lab-only")
            root, state = destroy_run(args.run, args.execute)
            output({"runDirectory": str(root), "state": state})
            return 0
        if args.command == "certify":
            pack_path = Path(__file__).resolve().parents[3] / "docs" / "data360" / "packs" / f"{args.pack}.json"
            pack = load_json(pack_path)
            discovery = discover_target({"orgAlias": args.target_org})
            output({"schemaVersion": "certification-attestation/v1", "pack": args.pack, "targetProfile": pack.get("targetProfile", {}), "targetOrg": args.target_org, "discovery": discovery, "status": "planned", "proofResults": [], "cleanup": "not-run", "surfaces": pack.get("surfaces", []), "note": "Live execution belongs to the trusted Labs runner; this command performs public-safe preflight only."})
            return 0
    except (ContractError, FileNotFoundError, json.JSONDecodeError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
