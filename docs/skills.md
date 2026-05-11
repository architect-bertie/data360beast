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
| `sf-datacloud-harmonize` | DMOs, mappings, model-gallery anchor choice, relationships, identity resolution, data graphs |
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

- `docs/beast-preflight.md`: required envelope, tool inventory, proof target, and mutation gate.
- `docs/phase-proof-matrix.json`: machine-readable phase routing, source requirements, proof targets, and forbidden assumptions.
- `docs/mcp-dependencies.md`: companion MCP install paths for `sf-docs` and the official Data 360 MCP server.
- `docs/data360/help/index.md`: public-safe index of 77 Salesforce Help pages analyzed for Data 360.
- `docs/data360/developer/index.md`: public-safe index of 23 Salesforce Developer Guide pages analyzed for Data 360 development.
- `docs/data360/developer/learning-map.md`: synthesized developer-guide learning map for skill routing.
- `docs/data360/model-gallery-implementation-map.md`: public Data 360 model-gallery synthesis for anchor DMOs, grain, relationship paths, and live-build traps.
- `docs/data360/rag-search-index-retriever-playbook.md`: public-safe RAG/search-index/retriever playbook for ADL versus manual setup, field roles, chunking, hybrid search, dynamic filters, prompt grounding, Flow/Apex fallbacks, and debugging.
- `docs/data360/architecture-engine-map.md`: engine-aware architecture and troubleshooting map.
- `docs/data360/interoperability-decision-map.md`: ingestion, zero-copy, and hybrid pattern selection.
- `docs/data360/docs-watch-operating-model.md`: weekly official-doc refresh, oversized Help fallback, indexed-doc audit, skill sync, and GitHub publishing.
- `sf-datacloud-connectapi/references/*`: API surface cards and live gotchas.
- `tools/audit_indexed_docs.py`: validates indexed Help and Developer capture completeness.
- `tools/capture_help_prerendered.mjs`: captures oversized official Help pages when sf-docs returns placeholders.
- `tools/refresh_skills_from_sf_docs.py`: refreshes marker-delimited skill guidance from official-doc exports.
- `sf-datacloud-connectapi/scripts/data360_accelerator.py`: portable snippets and optional Postman/DMO helpers.
- `sf-datacloud-calculated-insights/references/ci-sql-patterns.md`: reusable CI SQL patterns.
- `sf-datacloud-calculated-insights/scripts/ci_sql_guard.py`: static CI SQL guard.
- `sf-datacloud-governance/references/policy-enforcement-matrix.md`: runtime policy behavior map.
- `sf-datacloud-metadata-agentic/scripts/metadata_semantic_score.py`: metadata description scoring.
- `sf-datacloud/references/production-implementation-checklist.md`: end-to-end production checklist.
- `docs/beast-evals.md`: prompt-level evals for endpoint discipline, data-space handling, RAG troubleshooting, governance proof, and confidence labels.

## Public Boundary

The skill pack includes curated instructions, references, and small helper
scripts. It does not include raw Salesforce Help exports, generated local docs
caches, lab org metadata, credentials, or bulky Postman/OpenAPI dumps.
