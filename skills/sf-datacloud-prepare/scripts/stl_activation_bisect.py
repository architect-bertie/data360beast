#!/usr/bin/env python3
"""Bisect silent STL activation/run failures with constant-output scratch probes.

Localizes a transform that validates and activates but wedges or fails at run
(see BEAST-PROOF-026). Each probe keeps one cut node and all of its transitive
ancestors, replaces the production output with a constant mapping to a
pre-created scratch DLO, validates, creates, and waits for ACTIVE or ERROR (and
optionally a terminal run). Ordered cuts must describe an ancestor-growing path
through the graph, so a binary search over them pins the failing boundary one
variable at a time.

Offline preview is the default. Live work requires --execute and a declared
lab/sandbox boundary. API version is explicit or discovered; there is no fallback.
The pure body-shaping helpers (`ancestors`, `build_probe`, `build_output_probe`,
`probe_name`) call no org and are unit-testable on their own.
"""
from __future__ import annotations

import argparse
import copy
import json
import re
import sys
import uuid
import subprocess
import tempfile
import time
from pathlib import Path

from stl_graph import allocate_name, validate_graph, validate_probe, validate_scratch

TERMINAL_RUN_STATUSES = {
    "SUCCESS",
    "FAILURE",
    "CANCELED",
    "PARTIAL_FAILURE",
    "PARTIALLY_CANCELED",
    "SKIPPED_NO_CHANGES",
}

class Inconclusive(RuntimeError):
    """No defensible bisection boundary was established."""



def default_runner(command: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(command, capture_output=True, text=True, timeout=60)


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
    validate_graph(nodes)
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
    validate_scratch(full, scratch_dlo)
    all_nodes = full["definition"]["nodes"]
    keep = ancestors(all_nodes, cut)
    nodes = {
        node_id: copy.deepcopy(node)
        for node_id, node in all_nodes.items()
        if node_id in keep
    }
    if any(all_nodes[n]['action'] == 'outputD360' for n in keep):
        raise ValueError('output nodes cannot be probe cuts or ancestors')
    occupied = set(nodes)
    key_node = allocate_name('PROBE_KEY', occupied)
    out_node = allocate_name('PROBE_OUT', occupied)
    nodes[key_node] = {
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
    nodes[out_node] = {
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
        "sources": [key_node],
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
    validate_probe(probe, scratch_dlo)
    return probe


def build_output_probe(
    full: dict,
    *,
    limit: int,
    name: str,
    scratch_dlo: str,
) -> dict:
    """Keep the full graph but write a prefix of production mappings to scratch."""
    validate_scratch(full, scratch_dlo)
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
    validate_probe(probe, scratch_dlo)
    return probe


class ConnectClient:
    def __init__(self, org: str, api_version: str, runner=default_runner, *,
                 execute=False, invocation=None, clock=time.monotonic, sleep=time.sleep):
        self.org = org
        self.runner = runner
        self.base = f"/services/data/v{check_api_version(api_version)}/ssot/data-transforms"
        self.execute = execute
        self.invocation = invocation or uuid.uuid4().hex
        self.owned = {}
        self.clock, self.sleep = clock, sleep

    def request(self, path, method="GET", body=None, *, allow_not_found=False):
        query_read = method == 'POST' and path.split('?')[0].endswith('/ssot/queryv2')
        if method != 'GET' and not query_read and not self.execute:
            raise RuntimeError('refusing mutation without explicit execution')
        command = ['sf', 'api', 'request', 'rest', path,
                   '--target-org', self.org, '--method', method]
        temp_path = None
        if body is not None:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as handle:
                json.dump(body, handle)
                temp_path = Path(handle.name)
            command += ['--body', f'@{temp_path}']
        try:
            result = self.runner(command)
        finally:
            if temp_path is not None:
                temp_path.unlink(missing_ok=True)
        try:
            parsed = json.loads(result.stdout) if result.stdout.strip() else None
        except json.JSONDecodeError as exc:
            raise RuntimeError(f'{method} {path}: invalid JSON response') from exc
        not_found = isinstance(parsed, list) and bool(parsed) and all(
            isinstance(item, dict) and item.get('errorCode') == 'ITEM_NOT_FOUND'
            for item in parsed)
        if allow_not_found and not_found:
            return None
        if result.returncode != 0 or isinstance(parsed, list):
            raise RuntimeError(f'{method} {path}: API request failed: {parsed or result.stderr.strip()}')
        if parsed is None and method != 'DELETE':
            raise RuntimeError(f'{method} {path}: missing JSON response')
        return parsed

    def get(self, name):
        if not re.fullmatch(r'[A-Za-z][A-Za-z0-9_]*', name):
            raise ValueError('invalid transform API name')
        return self.request(f'{self.base}/{name}', allow_not_found=True)

    def require_owned(self, name):
        record = self.owned.get(name)
        if not record or record['state'] != 'created':
            raise RuntimeError(f'unresolved cleanup for {name}: creation identity is not proven')
        current = self.get(name)
        if current is None:
            return None
        if (current.get('id') != record['id'] or
                current.get('description') != record['marker']):
            raise RuntimeError(f'unresolved cleanup for {name}: ownership readback differs')
        return current

    def drop(self, name, timeout=180):
        if not self.execute:
            raise RuntimeError('refusing deletion without explicit execution')
        current = self.require_owned(name)
        if current is not None:
            self.request(f'{self.base}/{name}', 'DELETE', {})
            deadline = self.clock() + timeout
            while self.clock() < deadline:
                if self.get(name) is None:
                    break
                self.sleep(5)
            else:
                raise TimeoutError(f'unresolved cleanup: {name} was not deleted')
        self.owned.pop(name, None)

    def cleanup(self, name):
        if name not in self.owned:
            return  # A refused collision is never ours to clean up.
        current = self.require_owned(name)
        record = self.owned[name]
        if current is not None and record.get('run_started'):
            if current.get('lastRunStatus') not in TERMINAL_RUN_STATUSES:
                self.stop_run(name)
        self.drop(name)

    def validate(self, body):
        result = self.request(f'{self.base}-validation', 'POST', body)
        if not isinstance(result, dict):
            raise RuntimeError('invalid validation response')
        issues = result.get('issues') or []
        if result.get('success') is False or any(
            (item.get('errorSeverity') or item.get('severity')) in {'ERROR', 'FATAL'}
            for item in issues):
            raise RuntimeError(f'probe validation failed: {issues}')

    def activate(self, body, timeout):
        if not self.execute:
            raise RuntimeError('refusing creation without explicit execution')
        name = body['name']
        if self.get(name) is not None:
            raise RuntimeError(f'probe name already exists: {name}; refusing replacement')
        marker = f'Beast scratch probe; invocation={self.invocation}; name={name}'
        body = copy.deepcopy(body)
        body['description'] = marker
        self.validate(body)
        # Mark an attempted POST before sending. An exception may mean the server
        # accepted it; without a returned ID automatic deletion is unsafe.
        self.owned[name] = {'state': 'ambiguous', 'marker': marker, 'id': None}
        result = self.request(self.base, 'POST', body)
        identity = result.get('id') if isinstance(result, dict) else None
        if not isinstance(identity, str) or not identity:
            raise RuntimeError(f'unresolved cleanup for {name}: create returned no identity')
        self.owned[name].update(state='created', id=identity)
        started = self.clock()
        while self.clock() - started < timeout:
            current = self.require_owned(name)
            status = (current or {}).get('status')
            if status in {'ACTIVE', 'ERROR'}:
                return status, round(self.clock() - started)
            self.sleep(min(10, max(0, timeout - (self.clock() - started))))
        return 'TIMEOUT', round(self.clock() - started)

    def start_run(self, name: str) -> None:
        if self.require_owned(name) is None:
            raise RuntimeError('owned probe disappeared before run')
        self.owned[name]['run_started'] = True
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
        previous = self.request(f"{self.base}/{name}/run-history?limit=1")
        if not isinstance(previous, dict) or previous.get('histories'):
            raise Inconclusive('new probe has unexpected run history; refusing ambiguous run')
        self.start_run(name)
        started = self.clock()
        deadline = started + timeout
        while self.clock() < deadline:
            current = self.require_owned(name) or {}
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
                        round(self.clock() - started),
                        detail,
                    )

            if status in TERMINAL_RUN_STATUSES:
                return status, round(self.clock() - started), "summary terminal"

            print(
                f"  poll {name}: summary={status} lastRunDate={run_date} "
                f"elapsed={round(self.clock() - started)}s (flop-tolerant)",
                flush=True,
            )
            self.sleep(min(15, max(0, deadline - self.clock())))
        current = self.require_owned(name) or {}
        return (
            f"TIMEOUT:{current.get('lastRunStatus')}",
            round(self.clock() - started),
            "no terminal history",
        )

    def stop_run(self, name: str, timeout: int = 180) -> None:
        current = self.require_owned(name) or {}
        if current.get("lastRunStatus") in TERMINAL_RUN_STATUSES:
            return
        self.request(f"{self.base}/{name}/actions/cancel", "POST", {})
        self.request(f"{self.base}/{name}/actions/refresh-status", "POST", {})
        deadline = self.clock() + timeout
        while self.clock() < deadline:
            current = self.require_owned(name) or {}
            if current.get("lastRunStatus") in TERMINAL_RUN_STATUSES:
                return
            self.sleep(5)
        raise TimeoutError(f"{name} run was not canceled within {timeout}s")


def check_api_version(value):
    if not isinstance(value, str) or not re.fullmatch(r'[1-9][0-9]*\.[0-9]+', value):
        raise ValueError('a valid API version is required; supply --api-version')
    return value


def resolve_api_version(org: str, runner=default_runner) -> str:
    result = runner(['sf', 'org', 'display', '--json', '--target-org', org])
    if result.returncode != 0:
        raise RuntimeError('API version discovery failed; supply --api-version')
    return check_api_version(json.loads(result.stdout).get('result', {}).get('apiVersion'))


def probe_name(prefix, index, invocation=None):
    name = f'{prefix}_{invocation}_{index:04d}' if invocation else f'{prefix}{index:02d}'
    if len(name) > 32 or not re.fullmatch(r'[A-Za-z][A-Za-z0-9_]*', name):
        raise ValueError('probe name must be an API identifier of at most 32 characters')
    return name


def execute_probe(client, body, phase, timeout):
    name = body['name']
    original = None
    try:
        status, elapsed = client.activate(body, timeout)
        if status == 'ACTIVE' and phase == 'run':
            status, elapsed, detail = client.run(name, timeout)
        print(f'RESULT {name} status={status} elapsed={elapsed}s', flush=True)
        if status.startswith('TIMEOUT'):
            raise Inconclusive(f'{name}: timeout; no failing boundary is proven')
        return status
    except BaseException as exc:
        original = exc
        raise
    finally:
        try:
            client.cleanup(name)
        except BaseException as cleanup_error:
            print(f'UNRESOLVED CLEANUP {name}: {cleanup_error}', file=sys.stderr)
            if original is None:
                raise


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('transform', type=Path)
    parser.add_argument('--org', required=True)
    parser.add_argument('--scratch-dlo', required=True)
    parser.add_argument('--scratch-key-field', default='RecordKey__c')
    parser.add_argument('--name-prefix', default='DTTMPBISECT')
    parser.add_argument('--timeout', type=int, default=1200)
    parser.add_argument('--phase', choices=('activation', 'run'), default='activation')
    parser.add_argument('--execute', action='store_true', help='create/run/delete owned scratch probes')
    parser.add_argument('--environment', choices=('lab', 'sandbox'))
    parser.add_argument('--api-version')
    selection = parser.add_mutually_exclusive_group(required=True)
    selection.add_argument('--cuts', nargs='+')
    selection.add_argument('--aggregate-prefix-node')
    selection.add_argument('--output-prefix', action='store_true')
    selection.add_argument('--aggregate-field', nargs=2, metavar=('NODE', 'FIELD'))
    args = parser.parse_args()
    if args.execute and not args.environment:
        parser.error('--execute requires --environment lab|sandbox')
    if args.timeout <= 0:
        parser.error('--timeout must be positive')
    if args.api_version:
        check_api_version(args.api_version)
    full = json.loads(args.transform.read_text())
    validate_scratch(full, args.scratch_dlo)
    nodes = full['definition']['nodes']
    invocation = uuid.uuid4().hex[:10]
    probes, labels = [], []
    if args.cuts:
        sets = [ancestors(nodes, cut) for cut in args.cuts]
        if any(not earlier < later for earlier, later in zip(sets, sets[1:])):
            raise ValueError('cuts must form a strictly ancestor-growing sequence')
        for cut in args.cuts:
            probes.append(build_probe(full, cut, probe_name(args.name_prefix, len(probes), invocation),
                                      args.scratch_dlo, args.scratch_key_field))
            labels.append(cut)
    elif args.output_prefix:
        outputs = [node for node in nodes.values() if node['action'] == 'outputD360']
        if len(outputs) != 1:
            raise ValueError('output-prefix requires exactly one original output')
        mappings = outputs[0]['parameters']['fieldsMappings']
        for count in range(1, len(mappings) + 1):
            probes.append(build_output_probe(full, limit=count,
                name=probe_name(args.name_prefix, count, invocation), scratch_dlo=args.scratch_dlo))
            labels.append(f'output mappings={count}')
    else:
        cut = args.aggregate_prefix_node or args.aggregate_field[0]
        if cut not in nodes or nodes[cut]['action'] != 'aggregate':
            raise ValueError(f'{cut} is not an aggregate node')
        fields = nodes[cut]['parameters']['aggregations']
        names = {field['name'] for field in fields}
        if args.aggregate_field and args.aggregate_field[1] not in names:
            raise ValueError('unknown aggregate field')
        counts = [len(fields)] if args.aggregate_field else range(1, len(fields) + 1)
        for count in counts:
            body = build_probe(full, cut, probe_name(args.name_prefix, count, invocation),
                               args.scratch_dlo, args.scratch_key_field)
            if args.aggregate_field:
                select_aggregate_fields(body['definition']['nodes'][cut], {args.aggregate_field[1]})
            else:
                limit_aggregate_fields(body['definition']['nodes'][cut], count)
            probes.append(body)
            labels.append(f'{cut} aggregate fields={args.aggregate_field[1] if args.aggregate_field else count}')
    if not probes:
        raise ValueError('no probe candidates')
    for body in probes:
        validate_probe(body, args.scratch_dlo)
    if not args.execute:
        print(json.dumps({'mode': 'offline-preview', 'org': args.org,
            'environment': args.environment, 'apiVersion': args.api_version,
            'scratchDlo': args.scratch_dlo, 'phase': args.phase, 'probes': probes}, indent=2))
        return 0
    version = args.api_version or resolve_api_version(args.org)
    client = ConnectClient(args.org, version, execute=True, invocation=invocation)
    passed = 'SUCCESS' if args.phase == 'run' else 'ACTIVE'
    results = {}

    def test(index):
        if index not in results:
            results[index] = execute_probe(client, probes[index], args.phase, args.timeout)
        return results[index]

    first = test(0)
    if args.aggregate_field:
        print(f'OBSERVATION {labels[0]} status={first}; no general boundary proven')
        return 0
    if first != passed:
        raise Inconclusive(f'earliest probe failed: {labels[0]} ({first}); no passing baseline')
    last = len(probes) - 1
    if test(last) == passed:
        print('NO FAILING BOUNDARY: all tested endpoints passed; original target is untested')
        return 0
    low, high = 0, last
    while high - low > 1:
        middle = (low + high) // 2
        if test(middle) == passed:
            low = middle
        else:
            high = middle
    print(f'OBSERVED BOUNDARY last_pass={labels[low]} first_fail={labels[high]}; '
          'assumes monotonic behavior; not root-cause or output-correctness proof')
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (ValueError, RuntimeError, TimeoutError) as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(2)
