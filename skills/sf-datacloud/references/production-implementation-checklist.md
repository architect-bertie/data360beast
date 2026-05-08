# Data 360 Production Implementation Checklist

## Foundation

- Confirm Data 360 edition, licenses, data spaces, and user permission sets.
- Decide API surface:
  - Connect API / Apex when building with Salesforce Platform features
  - Data 360 API / Direct API when tenant-side read performance matters
  - Ingestion API for external data loads
  - Metadata API / data kits for deployable metadata
- Define environments, data-kit/package strategy, and promotion process.
- Define naming standards for data spaces, DLOs, DMOs, CIs, data graphs, search indexes, semantic models, activations, and data actions.
- Confirm Enhanced Security Data Spaces and decide the governance posture: broad RBAC, granular ABAC, masking, or a staged migration from Allow All/day-zero access.
- Define taxonomy, tags, classifications, custom permissions, and sensitive/key-field rules before downstream build.

## Build Order

1. Connect sources and validate connection health.
2. Create data streams with correct category, primary key, event time, refresh mode, and data space.
3. Validate DLO records and ingestion latency.
4. Apply baseline tags/classifications and confirm data space access.
5. Map DLOs to DMOs using standard C360 objects where possible.
6. Run identity resolution and validate unified profile quality.
7. Create calculated or streaming insights for reusable metrics.
8. Create data graphs/search indexes/semantic models for retrieval and analytics.
9. Create segments and verify counts.
10. Create activations, data actions, and flows.
11. Build reports/dashboards and monitoring.

## Production Gates

- Metadata descriptions and field semantics are agent-ready.
- Every object has a data owner, refresh expectation, and sensitivity classification.
- Keys, relationship fields, CI dimensions, graph ID/value fields, and activation identifiers are checked before applying masking.
- OLS/FLS/RLS/masking behavior is validated with target non-admin users in query, graph, CI, segment, report, activation, and agent surfaces.
- Queries are validated against actual data spaces and exact API names.
- CIs, segments, activations, and data actions are tested independently.
- Monitoring covers ingestion, transforms, identity resolution, insight runs, segment publish, activation delivery, data action failures, and usage/credits.
- Agentic consumers are tested for hallucination, PII safety, and correct metric/object selection.
