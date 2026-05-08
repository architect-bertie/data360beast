# Operating Model

Data360 Beast uses one loop for Salesforce Data 360 work:

1. Classify the phase.
2. Identify the proof target.
3. Fetch official docs on demand.
4. Search OpenAPI for API shape.
5. Apply cookbook lessons.
6. Validate in org when authorized.
7. Label confidence as documented, tested, or inferred.

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

## Source Rules

- Official docs are fetched on demand.
- OpenAPI is used for exact API shape.
- Cookbook lessons are used for working payloads and caveats.
- Live org validation upgrades confidence from documented to tested.

## Confidence Labels

- `Documented`: supported by current official docs or OpenAPI.
- `Tested`: validated in a live authorized org.
- `Inferred`: reasonable but not yet proven in the target org.
