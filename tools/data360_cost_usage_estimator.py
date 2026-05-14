#!/usr/bin/env python3
"""Produce a qualitative Data 360 cost/usage sizing review."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def band(value: float, low: float, high: float) -> str:
    if value <= low:
        return "low"
    if value <= high:
        return "medium"
    return "high"


def evaluate(scenario: dict[str, Any]) -> dict[str, Any]:
    rows = float(scenario.get("monthlyRowsIngested", 0))
    queries = float(scenario.get("monthlyQueries", 0))
    insight_runs = float(scenario.get("monthlyInsightRuns", 0))
    segment_publishes = float(scenario.get("monthlySegmentPublishes", 0))
    activation_payloads = float(scenario.get("monthlyActivationPayloads", 0))
    docs = float(scenario.get("ragDocuments", 0))
    chunks = float(scenario.get("ragAverageChunksPerDocument", 0))
    envs = float(scenario.get("environments", 1))

    rag_chunks = docs * chunks
    return {
        "name": scenario.get("name", "unnamed"),
        "bands": {
            "ingestion": band(rows * envs, 1_000_000, 50_000_000),
            "query": band(queries * envs, 10_000, 250_000),
            "insightRefresh": band(insight_runs * envs, 100, 2_000),
            "segmentation": band(segment_publishes * envs, 20, 500),
            "activation": band(activation_payloads * envs, 100_000, 5_000_000),
            "ragIndexing": band(rag_chunks * envs, 10_000, 1_000_000)
        },
        "derived": {
            "environmentMultiplier": envs,
            "estimatedRagChunks": rag_chunks
        },
        "proofQuestions": [
            "Which limits route to Data Services Billable Usage Types?",
            "What does Digital Wallet show for the target org?",
            "Which workloads run in sandbox/UAT as well as production?",
            "Can fields be filtered, projected, or aggregated before ingest?",
            "Can RAG indexes be partitioned by access cohort and refreshed incrementally?",
            "Can activation tests use bounded cohorts before full publish?"
        ],
        "caveat": "Qualitative sizing only; validate pricing, credits, and limits against current Salesforce docs, contract, and org telemetry."
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("scenario", help="JSON scenario file")
    args = parser.parse_args()

    scenario = json.loads(Path(args.scenario).read_text(encoding="utf-8"))
    print(json.dumps(evaluate(scenario), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
