# Operating Model

Data360 Beast uses one loop for Salesforce Data 360 work:

1. Run Beast preflight.
2. Classify the phase with the proof matrix.
3. Identify the object layer and likely execution plane.
4. For model work, choose the public model-gallery subject area, anchor DMO,
   grain, and relationship path.
5. For RAG work, choose ADL versus manual setup, source object path, field
   roles, chunking, search type, retriever filters, and prompt/action scope.
6. Identify the proof target.
7. Fetch official docs on demand.
8. Search OpenAPI for API shape.
9. Apply cookbook lessons.
10. Validate in org when authorized.
11. Label confidence as documented, tested, or inferred.

## Beast Preflight

Use [`beast-preflight.md`](beast-preflight.md) before non-trivial work. The
preflight makes the agent name the target org or alias, API version, data space,
persona, lifecycle, authorization boundary, available tools, and proof target.

If live validation, fresh official docs, or OpenAPI shape is unavailable, keep
working only when safe and label the answer as `inferred`, `docs-unverified`,
`path/schema-unverified`, or `live-validation-unavailable`.

## Phase Proof Matrix

Use [`phase-proof-matrix.json`](phase-proof-matrix.json) as the deterministic
routing table for:

- specialist skill selection
- required source type
- preferred tool path
- minimum proof target
- forbidden assumptions

The matrix is the machine-readable contract. The human phase table below is a
quick reference.

## Phase Router

| Phase | Use For | Proof |
| --- | --- | --- |
| Connect | Connectors, connections, schemas, refresh | Connection status, connector schema, ingestion proof |
| Prepare | Data streams, DLOs, transforms | Stream status, DLO fields, transform output |
| Harmonize | DMOs, mappings, identity, data graphs | Mapping status, relationship metadata, resolved records |
| Govern | Data spaces, tags, classifications, access | Data space, policy, permission, classification readback |
| Retrieve | Query SQL, Query v2, Profile API | Query result, profile result, metadata result |
| Insight | Calculated and streaming insights | SQL validation, CI status, output DMO fields |
| Semantic | Semantic models and metrics | Model readback, metric result, dimension mapping |
| AI/Search | Search indexes, retrievers, grounding | Index status, retrieval result, citation quality |
| Segment | Segments, DBT segments, counts | Segment status, count, publish status |
| Act | Activations and data actions | Target/action readback, activation status |
| Automation | Events and triggered flows | Event payload, flow run, monitoring signal |
| Develop/Package | API surface, auth, data kits, packageability, deployment | Chosen API surface, auth mode, data kit membership, metadata coverage |

## Layer And Engine Triage

Use the engine-aware architecture map for cross-surface mismatches,
performance work, or ambiguous failures:

- `docs/data360/architecture-engine-map.md`
- `docs/data360/interoperability-decision-map.md`
- `docs/data360/rag-search-index-retriever-playbook.md`

| Phase | Common Object Layer | Likely Plane To Consider | Proof Habit |
| --- | --- | --- | --- |
| Connect | DSO, source schema | connector and ingress | connection status, schema readback |
| Prepare | DSO, DLO | processing and lakehouse write | stream status, DLO row count, transform output |
| Harmonize | DLO, DMO | mapping and model metadata | relationship metadata, mapped field proof |
| Retrieve | DLO, DMO, CIO, graph | query and profile retrieval | query job rows, profile result, metadata |
| Insight | DMO, CIO | query plus materialization | syntax check, run status, `__cio` rows |
| Segment | DMO, CIO | segment compiler and count path | segment status, count, publish status |
| Analytics | DMO, CIO, semantic model | analytics serving and cache | report totals, dashboard refresh, user access |
| Act | segment, DMO, CIO | activation orchestration | target readback, activation status, delivery proof |
| Automation | DMO, CIO, event | orchestration and event delivery | control event, flow run, emitted payload |
| Develop/Package | metadata, data kits, APIs | development and deployment lifecycle | data kit readback, deploy validation, auth proof |

Do not promote an inferred engine guess to a fact. Use the guess to choose the
next validation step.

## Model Gallery Loop

Use `docs/data360/model-gallery-implementation-map.md` when the task involves
DMO choice, model diagrams, relationship design, Data Graph shape, or
agent-facing metadata.

```text
business outcome -> model-gallery subject area -> anchor DMO -> grain -> relationship path -> proof surface
```

Treat the gallery as a design compass, not runtime proof. Resolve exact DMO and
field names through metadata in the target data space before writing SQL,
segments, activations, or graph definitions.

## Interoperability Decision Loop

For external sources and lakehouses, choose the pattern before designing assets:

```text
workload -> freshness need -> governance need -> cost/I/O profile -> access pattern -> integration pattern -> proof path
```

| Pattern | Use For | Proof Habit |
| --- | --- | --- |
| Ingestion | governed canonical core, identity, compliance, operational activation | stream/DLO/DMO status, non-admin governance test |
| Real-time ingestion | sub-second operational decisions | event latency, pipeline health, saturation check |
| Streaming ingestion | minute-level incremental freshness | micro-batch status, freshness sample |
| Batch ingestion | historical or low-velocity datasets | scheduled run status, row reconciliation |
| Live query | freshest federated reads | source pushdown, latency, source policy check |
| Accelerated query | frequent reads with stale-data tolerance | cache interval, refresh status, result comparison |
| File federation | large object-store/open-table workloads | table metadata, partition/pruning probe |
| Hybrid | governed core plus fresh/high-volume edge | proof for both ingested core and federated edge |

## RAG Retrieval Loop

Use `docs/data360/rag-search-index-retriever-playbook.md` when the task
involves Agentforce Data Libraries, unstructured data, search indexes,
chunking, retrievers, prompt grounding, Flow/Apex retrieval, or RAG debugging.

```text
source content -> ADL/manual setup -> field roles -> chunking -> search type -> retriever -> prompt/action -> evaluation
```

Proof should move through the chain: index DMO/chunk population, retriever output,
prompt resolution, agent action selection, final answer, and non-admin access.

## Source Rules

- Official docs are fetched on demand.
- OpenAPI is used for exact API shape.
- Cookbook lessons are used for working payloads and caveats.
- Live org validation upgrades confidence from documented to tested.

## Confidence Labels

- `Documented`: supported by current official docs or OpenAPI.
- `Tested`: validated in a live authorized org.
- `Inferred`: reasonable but not yet proven in the target org.
