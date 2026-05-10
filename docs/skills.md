# Data360 Beast Skill Pack

Install this repository to give an agent the top-level Beast router plus the
full Salesforce Data 360 specialist layer.

```bash
npx skills add architect-bertie/data360beast
```

## Router

| Skill | Owns |
| --- | --- |
| `data360beast` | Top-level routing, source hierarchy, proof contract |
| `sf-datacloud` | Cross-phase Data 360 planning and orchestration |

## Specialist Skills

| Skill | Owns |
| --- | --- |
| `sf-datacloud-connectapi` | Connect REST API, Apex ConnectApi, OpenAPI lookup, payload design |
| `sf-datacloud-connect` | Connectors, connections, connector schema, connection health |
| `sf-datacloud-prepare` | Data streams, DLOs, transforms, document processing prep |
| `sf-datacloud-harmonize` | DMOs, mappings, relationships, identity resolution, data graphs |
| `sf-datacloud-governance` | Data spaces, access, tags, classifications, masking, policies |
| `sf-datacloud-retrieve` | Query SQL, Query v2, Profile API, metadata retrieval |
| `sf-datacloud-calculated-insights` | Calculated insights, streaming insights, CI SQL guardrails |
| `sf-datacloud-segment` | Segments, DBT segments, counts, publish proof |
| `sf-datacloud-act` | Activation targets, activations, data action delivery |
| `sf-datacloud-automation` | Data actions, triggered flows, events, monitoring |
| `sf-datacloud-semantic-layer` | C360 semantic models, metrics, dimensions |
| `sf-datacloud-ai-models` | Einstein Studio, predictive models, model outputs |
| `sf-datacloud-unstructured-retrieval` | Search indexes, chunking, retrievers, grounding |
| `sf-datacloud-analytics` | Reports, dashboards, reportability, analytics validation |
| `sf-datacloud-metadata-agentic` | Metadata description quality and agentic semantics |

## Supporting References And Scripts

- `docs/data360/architecture-engine-map.md`: engine-aware architecture and troubleshooting map.
- `sf-datacloud-connectapi/references/*`: API surface cards and live gotchas.
- `sf-datacloud-connectapi/scripts/data360_accelerator.py`: portable snippets and optional Postman/DMO helpers.
- `sf-datacloud-calculated-insights/references/ci-sql-patterns.md`: reusable CI SQL patterns.
- `sf-datacloud-calculated-insights/scripts/ci_sql_guard.py`: static CI SQL guard.
- `sf-datacloud-governance/references/policy-enforcement-matrix.md`: runtime policy behavior map.
- `sf-datacloud-metadata-agentic/scripts/metadata_semantic_score.py`: metadata description scoring.
- `sf-datacloud/references/production-implementation-checklist.md`: end-to-end production checklist.

## Public Boundary

The skill pack includes curated instructions, references, and small helper
scripts. It does not include raw Salesforce Help exports, generated local docs
caches, lab org metadata, credentials, or bulky Postman/OpenAPI dumps.
