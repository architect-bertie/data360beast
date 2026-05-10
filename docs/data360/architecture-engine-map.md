# Data 360 Architecture Engine Map

This note captures a public-safe operating model for reasoning about Data 360
architecture and troubleshooting. It is derived from user-provided architecture
material and the Data360 Beast operating model. Treat it as an inferred mental
model, not official Salesforce documentation or an API contract.

## Source Boundary

- Use official Salesforce docs for setup, limits, permissions, and supported
  product behavior.
- Use the Connect API OpenAPI catalog for endpoint and payload shape.
- Use live org validation for tenant-specific truth.
- Do not publish raw architecture deck images, org metadata, customer data, or
  implementation details that are not needed for field guidance.

Related decision map:
- `docs/data360/interoperability-decision-map.md`

## Core Stack Model

Data 360 work becomes easier to reason about when separated into layers:

| Layer | What To Ask | Common Proof |
| --- | --- | --- |
| Experience and APIs | Which surface is the user touching? | UI state, API response, returned ID |
| Messaging and query plane | Is this query, profile, segment, activation, or graph retrieval? | query job status, rows, profile result, segment count |
| Compute plane | Is this a processing job, query job, analytics serving path, or orchestration? | run status, error code, readback object, output count |
| Data/storage plane | Is the data in DSO, DLO, DMO, CIO, graph, or external storage? | metadata, field list, row count, sample records |
| Governance plane | Could data space, permission, tags, masking, or RLS change the answer? | non-admin validation, policy readback |

## Object Progression

Use this progression before writing SQL, formulas, segments, or activation
logic:

| Object Layer | Mental Model | Common Work |
| --- | --- | --- |
| DSO | Original source or transient connector shape | schema inspection, source header references |
| DLO | Lakehouse storage shape, often schema-enforced and source-adjacent | data streams, formula fields, ingestion validation |
| DMO | Curated model shape used by business features | mappings, relationships, identity, segments, activations |
| CIO | Materialized calculated insight output | reusable metrics, segmentation, reports, activation inputs |
| Data Graph | Read-optimized graph record over DMO data | profile context, agent grounding, real-time retrieval |

## Engine-Aware Heuristics

These engine associations are useful for triage, but they are inferred and can
change by release, tenant, feature, or surface.

| Engine Or Plane | Think Of It As | Agent Guidance |
| --- | --- | --- |
| Spark-like processing | heavy data processing, transforms, materialization, lakehouse writes | validate job status, output objects, row counts, and reruns |
| Trino-like query | federated SQL and lakehouse query access | validate query syntax, data space, field metadata, and result pages |
| Hyper-like serving | high-performance analytics and Tableau-style consumption | validate report/dashboard/semantic output, freshness, and cache behavior |
| Airflow-like orchestration | scheduling and workflow coordination | validate task/run status before blaming data or SQL |
| Iceberg-style storage | table metadata, snapshots, manifests, Parquet files, pruning | reason about selective filters, partition-like columns, file pruning, and scan cost |

## Triage Loop

Use this loop when a Data 360 symptom is ambiguous:

```text
symptom
-> user-facing surface
-> DSO/DLO/DMO/CIO/graph layer
-> likely execution plane
-> metadata and governance checks
-> proof path for that layer
```

Examples:

| Symptom | First Interpretation | Better Proof Path |
| --- | --- | --- |
| Formula field is invalid | Do not assume SQL syntax | Check Data 360 formula library syntax and `sourceField['Header Label']` casing |
| Query works but segment fails | Query plane and segment compiler can differ | Validate DMO grain, relationships, Segment On primary key, create status, and count |
| CI preview works but output is missing | Preview is not materialization proof | Run/publish the insight and query the `__cio` output |
| Report differs from Query Editor | Analytics serving, semantic definitions, cache, or governance can differ | Validate report grain, semantic metric, dashboard refresh, and target user access |
| Query is slow | It may be a scan/pruning problem, not just SQL syntax | Check predicate selectivity, joins, date filters, projected fields, and row counts |
| Activation has no members | Segment status and activation delivery are separate | Check segment count/status, publish status, target readback, and destination logs |

## Performance Lens

When a query or report is slow, avoid jumping straight to syntax fixes. Check:

1. Is the filter selective and applied to a field that can reduce scanned data?
2. Is the query pulling unnecessary columns or high-cardinality groupings?
3. Is the join multiplying rows before filters apply?
4. Is the data fresh in the object layer being queried?
5. Is the consuming surface using a different cache, semantic model, or serving
   path than the validation query?

For external data, also ask whether the data is ingested, queried live,
accelerated through a cache, accessed through file federation, or blended
through a hybrid pattern. The integration pattern changes the likely cost,
governance owner, freshness, and proof path.

## Output Habit

For architecture-sensitive answers, include:

1. surface touched
2. object layer
3. likely execution plane, labeled as inferred unless proven
4. command, payload, query, or UI readback
5. remaining caveat
