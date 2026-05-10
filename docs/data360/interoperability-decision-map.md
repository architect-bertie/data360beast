# Data 360 Interoperability Decision Map

This reference helps agents choose between Data 360 ingestion, zero-copy
federation, and hybrid patterns. It is derived from Salesforce Architect Data
360 interoperability guidance plus Data360 Beast field rules. Use it as a
decision aid, then verify current setup, limits, connector behavior, and
permissions with official docs and the target org.

Sources:
- https://architect.salesforce.com/docs/architect/decision-guides/guide/data-360-interoperability
- https://architect.salesforce.com/docs/architect/decision-guides/guide/data-360-interoperability.html

## First Question

Before designing connectors, DLOs, DMOs, SQL, segments, or activations, ask:

```text
Should this data be copied, queried live, cached, federated as files, or blended?
```

Use this loop:

```text
workload -> freshness need -> governance need -> cost/I/O profile -> access pattern -> integration pattern -> proof path
```

## Pattern Selection

| Pattern | Use When | Avoid Or Recheck When | Proof Path |
| --- | --- | --- | --- |
| Data ingestion | The data is high-value, regulated, identity-critical, activation-critical, or needs canonical DMO governance | The data is massive, volatile, exploratory, or already well-governed in an external platform | connection, stream status, DLO row count, DMO mapping, governed user test |
| Real-time ingestion | The workflow needs sub-second operational response, personalization, fraud, or urgent Agentforce action | Source systems cannot support low latency, volume is high, or value does not justify cost and complexity | ingestion event proof, latency sample, pipeline saturation check |
| Streaming ingestion | The workflow tolerates minute-level freshness and needs predictable incremental updates | Critical sub-second decisions are required or micro-batch sizing creates spikes | stream refresh status, incremental count, freshness sample |
| Batch ingestion | The data is historical, low velocity, compliance/reporting oriented, or cost-sensitive | Time-sensitive operations or live personalization depend on it | scheduled run status, row reconciliation, freshness SLA |
| Zero Copy live query | Freshness matters more than local persistence and the external source can serve the query efficiently | Query volume is high, predicates are weak, or source compute cost/latency is unacceptable | federated query result, source pushdown/latency check, cost profile |
| Accelerated query | Reads are frequent and slightly stale results are acceptable | Sub-second decisioning or strict real-time correctness is required | cache interval, refresh status, stale-data tolerance, result comparison |
| File federation | Large external datasets live in object storage/open table formats and batch-heavy analytics or AI/ML need direct access | Real-time dashboards, writeback, or fine-grained operational triggers require fresh local state | file/table metadata, partition/predicate probe, scan cost estimate |
| Hybrid | A stable governed core must be combined with fresh or high-volume edge data | Teams cannot define which data is core vs edge or governance ownership is unclear | core ingestion proof plus federated edge query proof |

## Ingestion Method Decision

| Method | Freshness | Best Fit | Cost And I/O Notes |
| --- | --- | --- | --- |
| Real-time | sub-second to seconds | operational alerts, fraud, live personalization, urgent Agentforce actions | highest complexity and cost; filter fields and use CDC/incremental patterns |
| Streaming | minutes | campaign orchestration, near-live engagement, operational reports | moderate cost; manage micro-batch size and windowed aggregation |
| Batch | hourly to daily or scheduled | historical analytics, regulated reporting, low-velocity sources | lower cost; watch load-window I/O and network throughput |

## Zero Copy Method Decision

| Method | Where Work Happens | Best Fit | Key Caveat |
| --- | --- | --- | --- |
| Query federation / live query | External system compute | real-time dashboards, operational queries, exploratory access | source performance, source SQL dialect, pushdown, and source compute cost matter |
| Accelerated query / caching | Data 360 cache over external data | frequent reads, BI dashboards, segmentation-style analytics with stale tolerance | freshness depends on refresh interval; cache management becomes design work |
| File federation | Data 360 compute directly reads external storage | object-store lakehouse data, large historical analytics, AI/ML training | read-only; performance depends on format, partitioning, pruning, and region/I/O |

## Governance Decision

| Question | If Yes | If No |
| --- | --- | --- |
| Must Data 360 be the canonical governed copy? | Ingest into governed DLO/DMO/CIO paths | Federation can be acceptable |
| Must Data 360 policies own access, lineage, and auditability? | Ingest or materialize the required data | Confirm source-side RLS, masking, and audit controls |
| Is source-side governance already strong and aligned to enterprise identity? | Federation is viable | Ingestion or additional identity/policy mapping may be safer |
| Are source and Salesforce users mapped to a common enterprise identity? | Federation governance can be validated | Add identity mapping before claiming governed federation |

Always state whether governance is expected to apply in Data 360, at the
external source, or both.

## Workload Archetypes

| Archetype | Recommended Pattern | Why |
| --- | --- | --- |
| Single Source of Truth | Data ingestion | build governed unified profiles, identity resolution, and trusted operational activation |
| Real-Time Insights | Zero Copy federation | use fresh external data without duplicating massive or fast-changing datasets |
| Hybrid Intelligence | Hybrid | ingest the governed customer core and federate volatile edge signals such as behavior or events |

## Design Checks

For every integration recommendation, capture:

1. latency target
2. freshness tolerance
3. access pattern: ad hoc, high-QPS, dashboard, segment, activation, AI/ML
4. data volume and expected scan size
5. governance owner: Data 360, source system, or both
6. cost driver: storage, Data 360 compute, source compute, network I/O, cache refresh
7. proof gate: stream status, cache status, federated query, source policy test, DMO mapping, segment count, or dashboard/report validation

## Agent Output Habit

When answering interoperability questions, use:

```text
Recommendation
Pattern: ingestion | real-time ingestion | streaming ingestion | batch ingestion | live query | accelerated query | file federation | hybrid
Why this pattern
Governance owner
Cost/I/O caveat
Validation proof
Remaining risk
```
