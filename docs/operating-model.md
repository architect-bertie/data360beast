# Operating Model

Data360 Beast uses one loop for Salesforce Data 360 work:

1. Classify the phase.
2. Identify the object layer and likely execution plane.
3. Identify the proof target.
4. Fetch official docs on demand.
5. Search OpenAPI for API shape.
6. Apply cookbook lessons.
7. Validate in org when authorized.
8. Label confidence as documented, tested, or inferred.

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

## Layer And Engine Triage

Use the engine-aware architecture map for cross-surface mismatches,
performance work, or ambiguous failures:

- `docs/data360/architecture-engine-map.md`

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

Do not promote an inferred engine guess to a fact. Use the guess to choose the
next validation step.

## Source Rules

- Official docs are fetched on demand.
- OpenAPI is used for exact API shape.
- Cookbook lessons are used for working payloads and caveats.
- Live org validation upgrades confidence from documented to tested.

## Confidence Labels

- `Documented`: supported by current official docs or OpenAPI.
- `Tested`: validated in a live authorized org.
- `Inferred`: reasonable but not yet proven in the target org.
