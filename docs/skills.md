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

## Optional Salesforce sf-skills Data 360 Companion

Install this companion only when the agent needs `sf data360` execution
playbooks, readiness checks, command templates, or CLI troubleshooting. Beast
keeps ownership of source hierarchy, proof labels, official-doc routing, limits
precedence, OpenAPI discipline, and Labs promotion.

```bash
python3 skills/data360beast/scripts/install_sf_skills_data360_companion.py --dry-run
python3 skills/data360beast/scripts/install_sf_skills_data360_companion.py
```

| Beast phase | Beast specialist | Salesforce `sf-skills` companion |
| --- | --- | --- |
| Cross-phase | `sf-datacloud` | `orchestrating-datacloud` |
| Connect | `sf-datacloud-connect` | `connecting-datacloud` |
| Prepare | `sf-datacloud-prepare` | `preparing-datacloud` |
| Harmonize | `sf-datacloud-harmonize` | `harmonizing-datacloud` |
| Segment | `sf-datacloud-segment` | `segmenting-datacloud` |
| Act | `sf-datacloud-act` | `activating-datacloud` |
| Retrieve | `sf-datacloud-retrieve` | `retrieving-datacloud` |
| Retrieve schema | `sf-datacloud-retrieve` | `getting-datacloud-schema` |
| Develop/package | `sf-datacloud` | `developing-datacloud-code-extension` |

Use **Data 360** in Beast-facing prose. Preserve upstream `*-datacloud` names
only for exact folders, package references, and command surfaces from
[`forcedotcom/sf-skills`](https://github.com/forcedotcom/sf-skills).

## Supporting References And Scripts

- `docs/beast-preflight.md`: required envelope, tool inventory, proof target, and mutation gate.
- `docs/phase-proof-matrix.json`: machine-readable phase routing, source requirements, proof targets, and forbidden assumptions.
- `docs/phase-coverage-matrix.json`: machine-readable phase coverage by source, proof, helper, and frontier.
- `docs/mcp-dependencies.md`: companion MCP install paths for `sf-docs` and the official Data 360 MCP server.
- `docs/data360/mcp-tool-selection.md`: decision guide for `sf-docs`, `data360`, `datacloud-mcp-query`, and direct `sf` REST calls.
- `docs/data360/cost-usage-sizing-contract.md`: qualitative cost and usage sizing contract.
- `docs/data360/develop-package-deployment-matrix.md`: develop/package/deploy proof matrix.
- `docs/release-discipline.md`: release, validation, and publishing discipline.
- `docs/data360/sf-skills-data360-companion.md`: Salesforce `sf-skills` Data 360 companion contract.
- `docs/data360/sf-skills-data360-companion.json`: machine-readable companion install, naming, authority, and phase crosswalk.
- `docs/data360/help/index.md`: public-safe index of 77 Salesforce Help pages analyzed for Data 360.
- `docs/data360/developer/index.md`: public-safe index of 23 Salesforce Developer Guide pages analyzed for Data 360 development.
- `docs/data360/developer/learning-map.md`: synthesized developer-guide learning map for skill routing.
- `docs/data360/model-gallery-implementation-map.md`: public Data 360 model-gallery synthesis for anchor DMOs, grain, relationship paths, and live-build traps.
- `docs/data360/rag-search-index-retriever-playbook.md`: public-safe RAG/search-index/retriever playbook for ADL versus manual setup, field roles, chunking, hybrid search, dynamic filters, prompt grounding, Flow/Apex fallbacks, and debugging.
- `docs/data360/architecture-engine-map.md`: engine-aware architecture and troubleshooting map.
- `docs/data360/interoperability-decision-map.md`: ingestion, zero-copy, and hybrid pattern selection.
- `docs/data360/docs-watch-operating-model.md`: weekly official-doc refresh, oversized Help fallback, indexed-doc audit, skill sync, and GitHub publishing.
- `docs/proof-ledger.md`: public-safe evidence entries, caveats, confidence labels, Labs references, and promotion status.
- `docs/labs-interface.md`: boundary between this operating-model repo and the Labs proving ground.
- `sf-datacloud-connectapi/references/*`: API surface cards and live gotchas.
- `tools/audit_indexed_docs.py`: validates indexed Help and Developer capture completeness.
- `tools/capture_help_prerendered.mjs`: captures oversized official Help pages when sf-docs returns placeholders.
- `tools/refresh_skills_from_sf_docs.py`: refreshes marker-delimited docs-side evidence and specialist skill guidance from official-doc exports.
- `tools/run_beast_evals.py`: executable prompt-eval harness for `docs/beast-evals.json`.
- `tools/skill_install_smoke.py`: portable skill-pack install/layout smoke test.
- `tools/mcp_readiness.py`: local MCP dependency readiness check.
- `skills/data360beast/scripts/install_sf_skills_data360_companion.py`: installs only the approved Data 360 companion subset from `forcedotcom/sf-skills`.
- `tools/data360_cost_usage_estimator.py`: qualitative cost/usage sizing review from a scenario JSON file.
- `tools/release_readiness.py`: release hygiene validator for manifests, docs, and changelog.
- `sf-datacloud-connectapi/scripts/data360_accelerator.py`: portable snippets and optional Postman/DMO helpers.
- `sf-datacloud-calculated-insights/references/ci-sql-patterns.md`: reusable CI SQL patterns.
- `sf-datacloud-calculated-insights/scripts/ci_sql_guard.py`: static CI SQL guard.
- `sf-datacloud-governance/references/policy-enforcement-matrix.md`: runtime policy behavior map.
- `sf-datacloud-governance/references/{govern-and-secure-overview,policy-based-governance,tagging-and-classification,data-spaces-detailed}.md`: extended doc-synced governance distillations (Phase 3B).
- `sf-datacloud-connect/references/connector-implementation-cards.md`: full A-Z catalog of 140+ Data 360 connectors with GA/Beta status, direction, data type, ingestion method, and authoritative dev guide URL.
- `sf-datacloud-harmonize/references/{dmo-and-mapping,dmo-relationships,identity-resolution-and-graphs}.md`: extended doc-synced DMO, mapping, relationship, identity-resolution, and Data Graph distillations (Phase 3C).
- `sf-datacloud-unstructured-retrieval/references/process-content.md`: extended UDLO -> UDMO -> Index -> Retriever pipeline distillation (Phase 3E).
- `sf-datacloud-automation/references/{data-cloud-triggered-flows,activation-triggered-flows,api-activations-and-orchestration,flow-creation-editing}.md`: extended flow distillations sourced from official Salesforce Help, Trailhead, and the official MuleSoft blog (Phase 3H).
- `sf-datacloud-act/references/activation-target-cards.md`: activation target type cards.
- `sf-datacloud-metadata-agentic/scripts/metadata_semantic_score.py`: metadata description scoring.
- `sf-datacloud/references/production-implementation-checklist.md`: end-to-end production checklist.
- `docs/beast-evals.md`: prompt-level evals for endpoint discipline, data-space handling, RAG troubleshooting, governance proof, and confidence labels.

## Public Boundary

The skill pack includes curated instructions, references, and small helper
scripts. It does not include raw Salesforce Help exports, generated local docs
caches, lab org metadata, raw Labs payload dumps, credentials, or bulky
Postman/OpenAPI dumps.
