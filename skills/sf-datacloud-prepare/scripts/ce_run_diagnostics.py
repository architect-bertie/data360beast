#!/usr/bin/env python3
"""Read scoped Code Extension history and logs; never certify output correctness.

Uses documented DataCustomCodeLogs__dll fields. A snapshot is the default;
--wait-seconds enables bounded polling for terminal history and delayed logs.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import math
import sys
import time
from pathlib import Path
from urllib.parse import quote

sys.path.insert(0, str(Path(__file__).resolve().parent))
from stl_activation_bisect import (  # noqa: E402
    ConnectClient, TERMINAL_RUN_STATUSES, check_api_version, resolve_api_version,
)

LOG_FIELDS = ('EventId__c', 'Timestamp__c', 'Message__c', 'CorrelationId__c',
              'DataCustomCodeName__c', 'ProcessDefinitionName__c', 'ExecutionId__c')


def literal(value):
    if not isinstance(value, str) or not value or any(ord(c) < 32 for c in value):
        raise ValueError('filter values must be nonempty strings without control characters')
    # ANSI SQL uses doubled single quotes. Backslashes are rejected rather than
    # depending on a server-specific escape-string setting.
    if '\\' in value:
        raise ValueError('backslashes are unsupported in filter values')
    return "'" + value.replace("'", "''") + "'"


def timestamp(value):
    parsed = datetime.fromisoformat(value.replace('Z', '+00:00'))
    if parsed.tzinfo is None:
        raise ValueError('timestamps require a timezone')
    return parsed.astimezone(timezone.utc).isoformat()


def build_logs_query(name, limit=50, *, execution_id=None, since=None, until=None):
    if not isinstance(limit, int) or not 1 <= limit <= 1000:
        raise ValueError('limit must be in 1..1000')
    filters = [f'"ProcessDefinitionName__c" = {literal(name)}']
    if execution_id:
        filters.append(f'"ExecutionId__c" = {literal(execution_id)}')
    start, end = timestamp(since) if since else None, timestamp(until) if until else None
    if start and end and start > end:
        raise ValueError('--since must not be after --until')
    if start:
        filters.append(f'"Timestamp__c" >= {literal(start)}')
    if end:
        filters.append(f'"Timestamp__c" <= {literal(end)}')
    fields = ', '.join(f'"{field}"' for field in LOG_FIELDS)
    return (f'SELECT {fields} FROM "DataCustomCodeLogs__dll" WHERE ' +
            ' AND '.join(filters) + f' ORDER BY "Timestamp__c" DESC LIMIT {limit}')


def summarize_run_history(history):
    rows = (history or {}).get('histories') or []
    if not rows:
        return {'status': None, 'processedRows': None, 'errorMessage': None}
    row = rows[0]
    return {'status': row.get('status'), 'processedRows': row.get('processedRows'),
            'errorMessage': row.get('errorMessage') or ''}


def fetch_logs(client, base, sql, limit, *, deadline=None, clock=time.monotonic, data_space=None):
    suffix = '?dataspace=' + quote(data_space, safe='') if data_space else ''
    page = client.request(f'{base}/queryv2{suffix}', 'POST', {'sql': sql})
    rows, seen = [], set()
    metadata = None
    while True:
        if not isinstance(page, dict) or not isinstance(page.get('data'), list):
            raise RuntimeError('invalid query response; log completeness is unknown')
        metadata = metadata or page.get('metadata')
        remaining = limit - len(rows)
        rows.extend(page['data'][:remaining])
        done = page.get('done') is True
        overflow = len(page['data']) > remaining
        capped = len(rows) >= limit
        if done or capped:
            return {'data': rows, 'metadata': metadata, 'done': done and not overflow,
                    'truncated': overflow or capped, 'paginationComplete': done and not overflow}
        cursor = page.get('nextBatchId')
        if (not isinstance(cursor, str) or not cursor or cursor in seen or
                (deadline is not None and clock() >= deadline)):
            return {'data': rows, 'metadata': metadata, 'done': False,
                    'truncated': True, 'paginationComplete': False}
        seen.add(cursor)
        # Empty pages can still carry a cursor, so bound requests separately.
        if len(seen) > 100:
            return {'data': rows, 'metadata': metadata, 'done': False,
                    'truncated': True, 'paginationComplete': False}
        page = client.request(f'{base}/queryv2/{quote(cursor, safe="")}{suffix}', 'GET')


def collect(client, api_version, name, *, limit=50, execution_id=None,
            since=None, until=None, wait_seconds=0, poll_seconds=15,
            clock=time.monotonic, sleep=time.sleep, data_space=None):
    if (not math.isfinite(wait_seconds) or not 0 <= wait_seconds <= 3600 or
            not math.isfinite(poll_seconds) or poll_seconds <= 0):
        raise ValueError('wait must be in 0..3600 seconds and poll interval must be positive')
    sql = build_logs_query(name, limit, execution_id=execution_id, since=since, until=until)
    base = f'/services/data/v{check_api_version(api_version)}/ssot'
    started = clock()
    deadline = started + wait_seconds
    report = None
    while True:
        history = client.request(f'{base}/data-transforms/{quote(name, safe="")}/run-history?limit=1', 'GET')
        if not isinstance(history, dict):
            raise RuntimeError('invalid run-history response')
        run = summarize_run_history(history)
        errors = []
        try:
            logs = fetch_logs(client, base, sql, limit, clock=clock,
                              deadline=deadline if wait_seconds else None, data_space=data_space)
        except RuntimeError as exc:
            logs = {'data': [], 'done': False, 'paginationComplete': False, 'truncated': False}
            errors.append(f'Scoped log query failed; verify documented log fields and permissions: {exc}')
        terminal = run['status'] in TERMINAL_RUN_STATUSES
        available = bool(logs['data'])
        scope = 'execution' if execution_id else 'transform'
        report = {'transform': name, 'run': run, 'logs': logs,
                  'correlation': {'scope': scope, 'executionId': execution_id,
                      'historyScope': 'latest-transform-run', 'historyExecutionMatched': False},
                  'complete': terminal and available and logs['paginationComplete'] and not logs['truncated'],
                  'runTerminal': terminal, 'logsAvailable': available,
                  'truncated': logs['truncated'], 'errors': errors,
                  'proof': 'diagnostic-only; logs are not matched to the history execution',
                  'timedOut': False}
        if report['complete'] or errors or not wait_seconds or clock() >= deadline:
            report['timedOut'] = bool(wait_seconds and not report['complete'] and clock() >= deadline)
            return report
        sleep(min(poll_seconds, deadline - clock()))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('transform')
    parser.add_argument('--org', required=True)
    parser.add_argument('--api-version')
    parser.add_argument('--data-space', required=True, help='explicit Query API data-space context')
    parser.add_argument('--limit', type=int, default=50)
    parser.add_argument('--execution-id')
    parser.add_argument('--since')
    parser.add_argument('--until')
    parser.add_argument('--wait-seconds', type=float, default=0)
    parser.add_argument('--poll-seconds', type=float, default=15)
    args = parser.parse_args()
    # Check filters before even resolving the authenticated API version.
    build_logs_query(args.transform, args.limit, execution_id=args.execution_id,
                     since=args.since, until=args.until)
    if (not math.isfinite(args.wait_seconds) or not 0 <= args.wait_seconds <= 3600 or
            not math.isfinite(args.poll_seconds) or args.poll_seconds <= 0):
        parser.error('invalid polling bounds')
    version = check_api_version(args.api_version) if args.api_version else resolve_api_version(args.org)
    report = collect(ConnectClient(args.org, version), version, args.transform,
        limit=args.limit, execution_id=args.execution_id, since=args.since, until=args.until,
        wait_seconds=args.wait_seconds, poll_seconds=args.poll_seconds, data_space=args.data_space)
    print(json.dumps(report, indent=2))
    return 0 if report['complete'] else 2


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (ValueError, RuntimeError) as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(2)
