#!/usr/bin/env python3
"""Bisect silent STL activation/run failures with constant-output scratch probes.

Localizes a transform that validates and activates but wedges or fails at run
(see BEAST-PROOF-025). Each probe keeps one cut node and all of its transitive
ancestors, replaces the production output with a constant mapping to a
pre-created scratch DLO, validates, creates, and waits for ACTIVE or ERROR (and
optionally a terminal run). Ordered cuts must describe an ancestor-growing path
through the graph, so a binary search over them pins the failing boundary one
variable at a time.

Org access uses the Salesforce CLI (`sf api request rest`) at the org's own
authenticated API version — no hard-coded version, no stored org identifiers.
The pure body-shaping helpers (`ancestors`, `build_probe`, `build_output_probe`,
`probe_name`) call no org and are unit-testable on their own.
"""
from __future__ import annotations

import argparse
import copy
import json
import subprocess
import tempfile
import time
from pathlib import Path

TERMINAL_RUN_STATUSES = {
    "SUCCESS",
    "FAILURE",
    "CANCELED",
    "PARTIAL_FAILURE",
    "PARTIALLY_CANCELED",
    "SKIPPED_NO_CHANGES",
}

DEFAULT_API_VERSION = "66.0"


def default_runner(command: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(command, capture_output=True, text=True)


def limit_aggregate_fields(node: dict, limit: int) -> None:
    """Keep the first N aggregate fields and their matching schema entries."""
    aggregations = node["parameters"]["aggregations"][:limit]
    names = {field["name"] for field in aggregations}
    node["parameters"]["aggregations"] = aggregations
    node["schema"]["fields"] = [
        field for field in node["schema"]["fields"] if field["name"] in names
    ]


def select_aggregate_fields(node: dict, names: set[str]) -> None:
    """Keep named aggregate fields and their matching schema entries."""
    node["parameters"]["aggregations"] = [
        field
        for field in node["parameters"]["aggregations"]
        if field["name"] in names
    ]
    node["schema"]["fields"] = [
        field for field in node["schema"]["fields"] if field["name"] in names
    ]


def ancestors(nodes: dict, target: str) -> set[str]:
    """Return target plus every node it transitively depends on."""
    seen: set[str] = set()
    stack = [target]
    while stack:
        node_id = stack.pop()
        if node_id in seen:
            continue
        if node_id not in nodes:
            raise KeyError(f"unknown cut/source node: {node_id}")
        seen.add(node_id)
        stack.extend(nodes[node_id].get("sources") or [])
    return seen


def build_probe(
    full: dict, cut: str, name: str, scratch_dlo: str, key_field: str
) -> dict:
    """Build an activation probe that holds the write boundary constant."""
    all_nodes = full["definition"]["nodes"]
    keep = ancestors(all_nodes, cut)
    nodes = {
        node_id: copy.deepcopy(node)
        for node_id, node in all_nodes.items()
        if node_id in keep
    }
    nodes["PROBE_KEY"] = {
        "action": "formula",
        "parameters": {
            "expressionType": "SQL",
            "fields": [{
                "name": "probe_key",
                "formulaExpression": "'probe'",
                "type": "TEXT",
                "precision": 255,
            }],
        },
        "sources": [cut],
    }
    nodes["PROBE_OUT"] = {
        "action": "outputD360",
        "parameters": {
            "name": scratch_dlo,
            "type": "dataLakeObject",
            "writeMode": "OVERWRITE",
            "dedupOrder": [],
            "fieldsMappings": [{
                "sourceField": "probe_key",
                "targetField": key_field,
            }],
        },
        "sources": ["PROBE_KEY"],
    }

    definition = {
        "type": full["definition"]["type"],
        "version": full["definition"]["version"],
        "nodes": nodes,
    }

    probe = {
        "name": name,
        "label": name,
        "description": f"Activation bisect probe cut at {cut}",
        "type": full["type"],
        "creationType": full.get("creationType", "CUSTOM"),
        "currencyIsoCode": full.get("currencyIsoCode", "USD"),
        "primarySource": full["primarySource"],
        "definition": definition,
    }
    if "dataSpaceName" in full:
        probe["dataSpaceName"] = full["dataSpaceName"]
    return probe


def build_output_probe(
    full: dict,
    *,
    limit: int,
    name: str,
    scratch_dlo: str,
) -> dict:
    """Keep the full graph but write a prefix of production mappings to scratch."""
    nodes = copy.deepcopy(full["definition"]["nodes"])
    outputs = [
        node for node in nodes.values()
        if node["action"] == "outputD360"
    ]
    if len(outputs) != 1:
        raise ValueError(f"expected one outputD360 node, found {len(outputs)}")
    output = outputs[0]
    mappings = output["parameters"]["fieldsMappings"]
    if not 1 <= limit <= len(mappings):
        raise ValueError(f"mapping limit must be in 1..{len(mappings)}")
    output["parameters"]["name"] = scratch_dlo
    output["parameters"]["fieldsMappings"] = mappings[:limit]

    definition = {
        "type": full["definition"]["type"],
        "version": full["definition"]["version"],
        "nodes": nodes,
    }
    probe = {
        "name": name,
        "label": name,
        "description": f"Output mapping bisect probe with {limit} mappings",
        "type": full["type"],
        "creationType": full.get("creationType", "CUSTOM"),
        "currencyIsoCode": full.get("currencyIsoCode", "USD"),
        "primarySource": full["primarySource"],
        "definition": definition,
    }
    if "dataSpaceName" in full:
        probe["dataSpaceName"] = full["dataSpaceName"]
    return probe


class ConnectClient:
    def __init__(self, org: str, api_version: str, runner=default_runner):
        self.org = org
        self.runner = runner
        self.base = f"/services/data/v{api_version}/ssot/data-transforms"

    def request(
        self,
        path: str,
        method: str = "GET",
        body: dict | None = None,
        *,
        allow_not_found: bool = False,
    ):
        command = [
            "sf", "api", "request", "rest", path,
            "--target-org", self.org,
            "--method", method,
        ]
        temp_path: Path | None = None
        if body is not None:
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".json", delete=False
            ) as handle:
                json.dump(body, handle)
                temp_path = Path(handle.name)
            command += ["--body", f"@{temp_path}"]
        try:
            result = self.runner(command)
        finally:
            if temp_path is not None:
                temp_path.unlink(missing_ok=True)

        parsed = None
        if result.stdout.strip():
            try:
                parsed = json.loads(result.stdout)
            except json.JSONDecodeError:
                parsed = None
        not_found = (
            isinstance(parsed, list)
            and any(item.get("errorCode") == "ITEM_NOT_FOUND" for item in parsed)
        )
        if result.returncode != 0 and not (allow_not_found and not_found):
            detail = result.stdout.strip() or result.stderr.strip()
            raise RuntimeError(
                f"{method} {path} failed with exit {result.returncode}: {detail}"
            )
        return None if not_found else parsed

    def get(self, name: str):
        return self.request(f"{self.base}/{name}", allow_not_found=True)

    def drop(self, name: str, timeout: int = 180) -> None:
        if self.get(name) is None:
            return
        self.request(f"{self.base}/{name}", "DELETE", {})
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            if self.get(name) is None:
                return
            time.sleep(5)
        raise TimeoutError(f"{name} was not deleted within {timeout}s")

    def validate(self, body: dict) -> None:
        result = self.request(f"{self.base}-validation", "POST", body)
        issues = (result or {}).get("issues") or []
        errors = [
            issue for issue in issues
            if (issue.get("errorSeverity") or issue.get("severity")) in {
                "ERROR", "FATAL"
            }
        ]
        if errors:
            raise RuntimeError(f"probe validation failed: {json.dumps(errors)}")

    def activate(self, body: dict, timeout: int) -> tuple[str, int]:
        name = body["name"]
        self.drop(name)
        self.validate(body)
        self.request(self.base, "POST", body)
        started = time.monotonic()
        deadline = started + timeout
        while time.monotonic() < deadline:
            current = self.get(name)
            status = (current or {}).get("status")
            if status in {"ACTIVE", "ERROR"}:
                return status, round(time.monotonic() - started)
            time.sleep(10)
        current = self.get(name)
        return f"TIMEOUT:{(current or {}).get('status')}", round(
            time.monotonic() - started
        )

    def start_run(self, name: str) -> None:
        result = self.request(
            f"{self.base}/{name}/actions/run",
            "POST",
            {"shouldForceFullRun": True},
        )
        if not (result or {}).get("success"):
            raise RuntimeError(f"run rejected for {name}: {result}")

    def run(self, name: str, timeout: int) -> tuple[str, int, str]:
        """Trigger a run and poll patiently to a real terminal.

        A freshly created probe transform starts with an empty run-history, so
        the first terminal row that appears there IS this run's result and is
        authoritative. Some orgs oscillate lastRunStatus IN_PROGRESS<->PENDING
        and re-advance lastRunDate before a run terminates; those flops are NOT
        failures, so we ignore them and keep polling until run-history (or the
        summary) reports a terminal, or the timeout expires.
        """
        self.start_run(name)
        started = time.monotonic()
        deadline = started + timeout
        while time.monotonic() < deadline:
            current = self.get(name) or {}
            status = current.get("lastRunStatus")
            run_date = current.get("lastRunDate")

            history = self.request(f"{self.base}/{name}/run-history?limit=1") or {}
            histories = history.get("histories") or []
            if histories:
                row = histories[0]
                history_status = row.get("status")
                if history_status in TERMINAL_RUN_STATUSES:
                    detail = (
                        f"rows={row.get('processedRows')} "
                        f"duration={row.get('duration')} "
                        f"error={row.get('errorMessage') or ''}"
                    )
                    return (
                        history_status,
                        round(time.monotonic() - started),
                        detail,
                    )

            if status in TERMINAL_RUN_STATUSES:
                return status, round(time.monotonic() - started), "summary terminal"

            print(
                f"  poll {name}: summary={status} lastRunDate={run_date} "
                f"elapsed={round(time.monotonic() - started)}s (flop-tolerant)",
                flush=True,
            )
            time.sleep(15)
        current = self.get(name) or {}
        return (
            f"TIMEOUT:{current.get('lastRunStatus')}",
            round(time.monotonic() - started),
            "no terminal history",
        )

    def stop_run(self, name: str, timeout: int = 180) -> None:
        current = self.get(name) or {}
        if current.get("lastRunStatus") in TERMINAL_RUN_STATUSES:
            return
        self.request(f"{self.base}/{name}/actions/cancel", "POST", {})
        self.request(f"{self.base}/{name}/actions/refresh-status", "POST", {})
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            current = self.get(name) or {}
            if current.get("lastRunStatus") in TERMINAL_RUN_STATUSES:
                return
            time.sleep(5)
        raise TimeoutError(f"{name} run was not canceled within {timeout}s")


def resolve_api_version(org: str, runner=default_runner) -> str:
    """Resolve the org's authenticated API version, falling back to a default."""
    result = runner(["sf", "org", "display", "--json", "--target-org", org])
    if result.returncode != 0:
        raise RuntimeError(result.stdout.strip() or result.stderr.strip())
    payload = json.loads(result.stdout)
    api_version = str(payload["result"].get("apiVersion") or DEFAULT_API_VERSION)
    if not api_version[0].isdigit():
        api_version = DEFAULT_API_VERSION
    return api_version


def probe_name(prefix: str, index: int) -> str:
    name = f"{prefix}{index:02d}"
    if len(name) > 32:
        raise ValueError(f"probe name exceeds 32 characters: {name}")
    return name


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("transform", type=Path)
    parser.add_argument("--org", required=True)
    parser.add_argument("--scratch-dlo", required=True)
    parser.add_argument(
        "--scratch-key-field",
        default="RecordKey__c",
        help="primary-key target field on the scratch DLO",
    )
    parser.add_argument("--name-prefix", default="DTTMPBISECT")
    parser.add_argument("--timeout", type=int, default=1200)
    parser.add_argument(
        "--phase",
        choices=("activation", "run"),
        default="activation",
    )
    selection = parser.add_mutually_exclusive_group(required=True)
    selection.add_argument("--cuts", nargs="+")
    selection.add_argument("--aggregate-prefix-node")
    selection.add_argument("--output-prefix", action="store_true")
    selection.add_argument(
        "--aggregate-field",
        nargs=2,
        metavar=("NODE", "FIELD"),
    )
    args = parser.parse_args()

    full = json.loads(args.transform.read_text())
    nodes = full["definition"]["nodes"]
    if args.cuts:
        cut_sets = [ancestors(nodes, cut) for cut in args.cuts]
        for earlier, later in zip(cut_sets, cut_sets[1:]):
            if not earlier < later:
                raise ValueError("cuts must form a strictly ancestor-growing sequence")

    client = ConnectClient(args.org, resolve_api_version(args.org))
    pass_status = "SUCCESS" if args.phase == "run" else "ACTIVE"

    def execute_body(body: dict, name: str, description: str) -> str:
        print(
            f"PROBE {description} "
            f"nodes={len(body['definition']['nodes'])}",
            flush=True,
        )
        status = "UNSET"
        try:
            activation_status, elapsed = client.activate(body, args.timeout)
            if activation_status != "ACTIVE":
                raise RuntimeError(
                    f"{description} did not activate: {activation_status}"
                )
            detail = ""
            if args.phase == "run":
                status, run_elapsed, detail = client.run(name, args.timeout)
                elapsed += run_elapsed
            else:
                status = activation_status
            print(
                f"RESULT {description} status={status} elapsed={elapsed}s {detail}",
                flush=True,
            )
            return status
        finally:
            if status != "UNSET":
                if args.phase == "run" and status not in TERMINAL_RUN_STATUSES:
                    client.stop_run(name)
                client.drop(name)

    def execute(
        cut: str,
        name: str,
        aggregate_limit: int | None = None,
        aggregate_fields: set[str] | None = None,
    ) -> str:
        body = build_probe(
            full, cut, name, args.scratch_dlo, args.scratch_key_field
        )
        if aggregate_limit is not None:
            limit_aggregate_fields(
                body["definition"]["nodes"][cut],
                aggregate_limit,
            )
        if aggregate_fields is not None:
            select_aggregate_fields(
                body["definition"]["nodes"][cut],
                aggregate_fields,
            )
        return execute_body(
            body,
            name,
            f"cut={cut} aggregate_limit={aggregate_limit}",
        )

    if args.output_prefix:
        output = next(
            node for node in nodes.values()
            if node["action"] == "outputD360"
        )
        mappings = output["parameters"]["fieldsMappings"]
        results: dict[int, str] = {}

        def test_mapping_count(count: int) -> str:
            if count not in results:
                name = probe_name(args.name_prefix, count)
                body = build_output_probe(
                    full,
                    limit=count,
                    name=name,
                    scratch_dlo=args.scratch_dlo,
                )
                results[count] = execute_body(
                    body,
                    name,
                    f"output_mappings={count}",
                )
            return results[count]

        first = test_mapping_count(1)
        if first != pass_status:
            raise RuntimeError(
                f"first output mapping did not pass {args.phase}: {first}"
            )
        last = test_mapping_count(len(mappings))
        if last == pass_status:
            print(
                f"BOUNDARY after output mappings; all {len(mappings)} "
                f"passed {args.phase}",
                flush=True,
            )
            return 0
        low, high = 1, len(mappings)
        while high - low > 1:
            middle = (low + high) // 2
            if test_mapping_count(middle) == pass_status:
                low = middle
            else:
                high = middle
        failing = mappings[high - 1]
        print(
            f"BOUNDARY last_pass_count={low} first_fail_count={high} "
            f"first_fail_source={failing['sourceField']} "
            f"first_fail_target={failing['targetField']}",
            flush=True,
        )
        return 0

    if args.aggregate_field:
        cut, field_name = args.aggregate_field
        node = nodes.get(cut)
        if not node or node.get("action") != "aggregate":
            raise ValueError(f"{cut} is not an aggregate node")
        available = {
            field["name"] for field in node["parameters"]["aggregations"]
        }
        if field_name not in available:
            raise ValueError(f"{field_name} is not an aggregation in {cut}")
        status = execute(
            cut,
            probe_name(args.name_prefix, 0),
            aggregate_fields={field_name},
        )
        print(
            f"BOUNDARY aggregate={cut} field={field_name} "
            f"status={status}",
            flush=True,
        )
        return 0

    if args.aggregate_prefix_node:
        cut = args.aggregate_prefix_node
        node = nodes.get(cut)
        if not node or node.get("action") != "aggregate":
            raise ValueError(f"{cut} is not an aggregate node")
        aggregations = node["parameters"]["aggregations"]
        if not aggregations:
            raise ValueError(f"{cut} has no aggregate fields")
        results: dict[int, str] = {}

        def test_count(count: int) -> str:
            if count not in results:
                results[count] = execute(
                    cut,
                    probe_name(args.name_prefix, count),
                    count,
                )
            return results[count]

        first = test_count(1)
        if first != pass_status:
            raise RuntimeError(
                f"first aggregate field did not pass {args.phase}: "
                f"{aggregations[0]['name']} status={first}"
            )
        last = test_count(len(aggregations))
        if last == pass_status:
            print(
                f"BOUNDARY after {cut}; all {len(aggregations)} aggregate "
                f"fields passed {args.phase}",
                flush=True,
            )
            return 0
        low, high = 1, len(aggregations)
        while high - low > 1:
            middle = (low + high) // 2
            if test_count(middle) == pass_status:
                low = middle
            else:
                high = middle
        print(
            f"BOUNDARY aggregate={cut} last_pass_count={low} "
            f"first_fail_count={high} "
            f"first_fail_field={aggregations[high - 1]['name']}",
            flush=True,
        )
        return 0

    results: dict[int, str] = {}

    def test(index: int) -> str:
        if index not in results:
            cut = args.cuts[index]
            results[index] = execute(
                cut,
                probe_name(args.name_prefix, index),
            )
        return results[index]

    first = test(0)
    if first != pass_status:
        raise RuntimeError(
            f"earliest cut {args.cuts[0]} did not pass {args.phase}: {first}"
        )

    last = test(len(args.cuts) - 1)
    if last == pass_status:
        print(
            f"BOUNDARY production output mapping/target; "
            f"every compute cut passed {args.phase}",
            flush=True,
        )
        return 0

    low, high = 0, len(args.cuts) - 1
    while high - low > 1:
        middle = (low + high) // 2
        status = test(middle)
        if status == pass_status:
            low = middle
        else:
            high = middle
    print(
        f"BOUNDARY last_active={args.cuts[low]} "
        f"first_error={args.cuts[high]}",
        flush=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
