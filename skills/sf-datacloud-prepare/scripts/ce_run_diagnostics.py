#!/usr/bin/env python3
"""Diagnose an opaque Data 360 code-extension (`DBT_HIDDEN`) run failure.

A code-extension deploy auto-creates a batch transform whose definition type is
`DBT_HIDDEN`. Its run-history exposes only `status` and `processedRows` with no
error text (see BEAST-PROOF-030), so a deploy-and-observe loop yields nothing.
The engine writes detail to the `DataCustomCodeLogs__dll` log surface instead.
This pulls both: the terminal run-history row for the transform, and recent log
rows via `ssot/queryv2` (which honors `LIMIT` exactly, unlike the local reader).

Org access reuses the bisect harness's `ConnectClient` transport, driving
`sf api request rest` at the org's own authenticated API version -- no hard-coded
version. The query builder (`build_logs_query`) and the run-history summary
(`summarize_run_history`) call no org and are unit-testable on their own.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Reuse the bisect harness's SF-CLI transport and version resolution rather than
# duplicating them; both scripts live side by side in this scripts/ dir.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from stl_activation_bisect import ConnectClient, resolve_api_version  # noqa: E402


def build_logs_query(limit: int = 50, where: str | None = None) -> str:
    """SQL to pull recent code-extension log rows.

    `SELECT *` because the log DLO's field set is org/version dependent and this
    tool must not assume column names; `queryv2` honors the `LIMIT` exactly. Pass
    `where` (single-quoted literals, per Query SQL lexing) once the log schema is
    known in the target org to filter to one extension or a time window.
    """
    if not 1 <= limit <= 1000:
        raise ValueError("limit must be in 1..1000")
    clause = f" WHERE {where}" if where else ""
    return f"SELECT * FROM DataCustomCodeLogs__dll{clause} LIMIT {limit}"


def summarize_run_history(history: dict | None) -> dict:
    """Reduce a `/run-history` response to the terminal row's health fields."""
    rows = (history or {}).get("histories") or []
    if not rows:
        return {"status": None, "processedRows": None, "errorMessage": None}
    row = rows[0]
    return {
        "status": row.get("status"),
        "processedRows": row.get("processedRows"),
        "errorMessage": row.get("errorMessage") or "",
    }


def collect(client, api_version: str, name: str, *, limit: int = 50,
            where: str | None = None) -> dict:
    """Pull the terminal run-history row and recent log rows for one transform."""
    base = f"/services/data/v{api_version}/ssot"
    history = client.request(f"{base}/data-transforms/{name}/run-history?limit=1", "GET")
    logs = client.request(
        f"{base}/queryv2", "POST", {"sql": build_logs_query(limit=limit, where=where)}
    )
    return {"transform": name, "run": summarize_run_history(history), "logs": logs}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("transform", help="the DBT_HIDDEN transform's API name")
    parser.add_argument("--org", required=True)
    parser.add_argument("--limit", type=int, default=50, help="max log rows to pull")
    parser.add_argument("--where", help="optional SQL filter on the log DLO")
    args = parser.parse_args()

    api_version = resolve_api_version(args.org)
    client = ConnectClient(args.org, api_version)
    report = collect(
        client, api_version, args.transform, limit=args.limit, where=args.where
    )
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
