---
name: sf-datacloud-metadata-agentic
description: >
  Salesforce Data 360 metadata API mastery for production agentic use cases:
  metadata retrieval, semantic descriptions, field/object documentation,
  relationship semantics, data graph readiness, prompt/action grounding, and
  metadata quality scoring. TRIGGER when: the user prepares Data 360 metadata
  for Agentforce, AI agents, semantic search, dashboards, prompt grounding, or
  wants metadata descriptions and semantics improved programmatically.
license: MIT
metadata:
  version: "1.0.0"
  author: "architect-bertie"
---

# sf-datacloud-metadata-agentic

Use this skill for the **metadata and agentic semantics plane**.

Beast references:
- Beast preflight: [docs/beast-preflight.md](../../docs/beast-preflight.md)
- Phase proof matrix: [docs/phase-proof-matrix.json](../../docs/phase-proof-matrix.json)
- Public operating model: [docs/operating-model.md](../../docs/operating-model.md)
- Data 360 model-gallery implementation map: [docs/data360/model-gallery-implementation-map.md](../../docs/data360/model-gallery-implementation-map.md)
- RAG/search-index playbook: [docs/data360/rag-search-index-retriever-playbook.md](../../docs/data360/rag-search-index-retriever-playbook.md)
- Developer Guide index: [docs/data360/developer/index.md](../../docs/data360/developer/index.md)
- Developer Guide synthesis: [docs/data360/developer/skill-update-synthesis.md](../../docs/data360/developer/skill-update-synthesis.md)
- Proof ledger: [docs/proof-ledger.md](../../docs/proof-ledger.md)
- Public LLM map: [docs/llms.txt](../../docs/llms.txt)
- Limits source precedence: [docs/data360/limits-source-precedence.md](../../docs/data360/limits-source-precedence.md)
- For exact Salesforce behavior, fetch official Help/Developer docs on demand with `sf-docs`.
- For endpoint shape, use OpenAPI from the official spec or the user-supplied Swagger before writing payloads.

Static scoring utility:

```bash
python3 skills/sf-datacloud-metadata-agentic/scripts/metadata_semantic_score.py metadata.json
```

## Metadata API Surfaces

Prefer official Data 360 metadata surfaces before guessing:

- `GET /ssot/metadata`
- `GET /ssot/profile/metadata`
- `GET /ssot/profile/metadata/:dataModelName`
- `GET /ssot/insight/metadata`
- `GET /ssot/insight/metadata/:ciName`
- `GET /ssot/data-graphs/metadata`
- data model object and relationship metadata from Connect API
- Apex `ConnectApi.CdpQuery` metadata methods where available
- Metadata API for supported Data 360 metadata movement
- data kit metadata and packageability readback for deployable Data 360 assets

## Data Kits And Packageability

- Data kits are the core packaging/deploy abstraction for Data 360 metadata.
  They package definitions, not raw data.
- Verify current Metadata Coverage and the Data 360 metadata component cheat
  sheet before promising packageability.
- Data 360 metadata and Salesforce Platform metadata should be planned as
  separate package tracks unless current docs explicitly support the combined
  target.
- For sandbox-to-production movement, check DevOps data kit membership,
  downloaded `package.xml`, retrieved metadata files, matching data space
  prefixes, and connector reauthorization requirements.
- Watch deployment failures involving missing `FieldSrcTrgtRelationship`
  metadata, generated key qualifier files, and inactive connectors after
  deployment.

## Agentic Metadata Goals

Prepare metadata so an agent can:

- map a business phrase to the right public Data 360 model-gallery subject area
  and anchor DMO before writing SQL or creating a graph
- identify the right object for a business concept
- distinguish similar fields without hallucinating
- understand grain, cardinality, freshness, and governance limits
- choose between DMO, CIO, Data Graph, semantic metric, or search retriever
- understand whether an answer should use query, semantic model, Data Graph, or retriever grounding
- understand which fields are index, prepend, filter, return, ranking, or
  agent-safe citation fields in a RAG design
- explain results using business language without exposing PII
- know when a metric is authoritative vs exploratory

## Production Metadata Workflow

1. Inventory data spaces, DMOs, CIOs, data graphs, semantic models, and search indexes.
2. Classify every object:
   - profile, engagement, other, unified, calculated insight, data graph, semantic view, unstructured chunk/index
3. Add or improve object descriptions:
   - business purpose
   - grain
   - owner
   - refresh cadence
   - permitted consumers
   - PII/sensitivity notes
   - tags, classifications, masking policy, and agent-safe output status
4. Add or improve field descriptions:
   - plain-English meaning
   - valid values or units
   - null semantics
   - source system
   - join/key behavior
   - whether safe for agent output
   - whether the field is join-only, activation-only, restricted, masked, or governed by RLS/FLS
5. Add relationship semantics:
   - one-to-one, one-to-many, many-to-many
   - parent/child role
   - join key and source of truth
   - fanout risk
6. Add metric semantics:
   - formula
   - dimensions
   - aggregatability
   - time window
   - owner and validation source
7. Generate an agent-safe metadata summary for prompts, Agentforce instructions, Data Graph descriptions, retriever descriptions, and action parameter descriptions.
8. For deployable assets, verify data kit membership, packageability, metadata
   coverage, and target-org deployment prerequisites.
9. Validate with agent tests that require the agent to choose the correct object/metric without being shown table names in the user prompt.

## Description Quality Rubric

Score metadata from 0-5:

- 0: missing or source-system jargon only
- 1: label repeats API name
- 2: describes the field but not business meaning
- 3: includes business meaning and source
- 4: includes grain, units, null/valid values, and governance
- 5: includes all of the above plus examples and agent-safe usage guidance

Production target: object descriptions >= 4, agent-facing fields >= 4, metrics >= 5.

## Agentic Anti-Patterns

- Descriptions that say only "customer id", "flag", "amount", or "score".
- Multiple fields with similar labels and no distinction.
- Metrics with no time window or grain.
- Data Graphs with technical object names but no business purpose.
- Metadata that calls everything "customer" and hides whether the grain is
  `Individual`, `Unified Individual`, `Account`, `Account Contact`, `Party`, or
  a contact point.
- Consent metadata that exposes a generic opt-in flag without purpose, channel,
  contact point, brand, legal basis, and status semantics.
- Agent actions whose input descriptions do not define format, units, or valid values.
- Exposing IDs, emails, phones, addresses, or raw source keys in agent responses.
- Treating metadata visibility as access permission. Agents must respect runtime governance and masking.
- Omitting tag/classification semantics, causing agents to use restricted fields as if they were safe context.
- Ignoring semantic model definitions and letting agents invent metric formulas.
- Building retriever descriptions that omit data space, source object, filters, citation behavior, and governance limits.

## Validation Gates

- Metadata API inventory matches the objects the agent can query.
- Agent can map 10 business phrases to correct objects/fields/metrics.
- Agent refuses or asks clarification for ambiguous metadata.
- Agent output uses approved business descriptions and avoids PII.
- Agent output and action inputs are tested with a governed non-admin user profile.
- Data Graph and retriever descriptions match the actual fields included.
- CI/semantic metric descriptions include formulas and time windows.
- Metadata semantic score is >= 4 for agent-facing objects and fields, and 5 for metrics.
- Data kit / Metadata API deployment proof exists for metadata expected to move
  across orgs.

## Handoffs

- Semantic metrics -> [sf-datacloud-semantic-layer](../sf-datacloud-semantic-layer/SKILL.md)
- Data graphs and relationships -> [sf-datacloud-harmonize](../sf-datacloud-harmonize/SKILL.md)
- Agentforce action/topic descriptions -> `sf-ai-agentforce` companion skill when available
- Query and metadata extraction -> [sf-datacloud-retrieve](../sf-datacloud-retrieve/SKILL.md)

## Output Format

Report:

1. metadata sources inspected
2. object/field/metric quality score
3. recommended descriptions
4. relationship and grain notes
5. agent-safe summary
6. update mechanism or manual setup path
7. validation prompts and expected routing

## Doc-Synced Notes

<!-- SF_DOC_SYNC_START:data-kits-and-packaging -->
### Data Kits and Packaging (Build and Share Functionality)

_Distilled from official Salesforce sources only._

**Sources:**
- developer.salesforce.com/docs/data/data-cloud-dev/guide/packages-data-kits.html — Packages and Data Kits
- developer.salesforce.com/docs/data/data-cloud-dev/guide/data-cloud-2gp-workflow.htm — 2GP Workflow for Data 360
- developer.salesforce.com/docs/data/data-cloud-dev/guide/component-cheatsheet.html — Metadata Components Cheat Sheet
- developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360a-api-isv-readiness-data.html — Data 360 Extensibility Readiness Matrix
- developer.salesforce.com/docs/data/data-cloud-dev/guide/dc-deploy-data-kits-using-connect-api.html — Deploy Data 360 Data Kits with Connect REST
- developer.salesforce.com/docs/data/data-cloud-dev/guide/dc-deploy_data_kit_components.html — Deploy Data Kit Components Flow
- developer.salesforce.com/docs/data/data-cloud-dev/guide/app-dev-comparison.html — Differences Between Developing Apps on Data 360 and the Platform

**What is a Data Kit?**
- A Data Kit is a container for **Data 360 metadata definitions**
  (calculated insights, profiles, data streams, DMOs, identity rules,
  search indexes, segments, activations) — NOT the actual data.
- Streamlines packaging and deployment of related Data 360 configurations.
- A package can contain one or more data kits.
- When packaging Data 360 metadata, you MUST add components to a data
  kit first, then add the data kit to a package.

**Two types of Data Kits:**

| Type | Created from | Deployed to | Use case |
|---|---|---|---|
| **Standard Data Kit** | Default data space | Any data space in target org | AppExchange solutions, partner-distributed apps |
| **DevOps Data Kit** | Any data space | The same data space in target org | Sandbox-to-prod migration, internal CI/CD |

**The Two-Package Rule (Winter '25 mandatory):**
- You CANNOT include both Data 360 metadata and non-Data 360 metadata
  in the same package.
- Create two separate packages: one for Data 360, one for everything else.
- Applies to all package types (managed and unmanaged).
- Reason: Data 360 metadata lifecycle and deployment model differs from
  Salesforce Platform metadata.

**Packaging types — pick by audience:**

| Package Type | Audience | Behavior |
|---|---|---|
| Unmanaged | Internal customer dev → prod | Editable in target org, no upgrade path |
| Managed (1GP) | Salesforce Partner → AppExchange | Locked components; legacy path |
| Managed 2GP (Second-Gen) | Modern Partner / customer | Locked, namespaced, version-managed; preferred for new ISV apps |

All Data 360 feature metadata in **managed packages is locked** —
protects components from unauthorized changes in the subscriber org.

**Packageable Data 360 components:**
- Data Package Kit Definition (the kit itself)
- Data Package Kit Object (each component reference inside)
- Data Source / Data Source Bundle Definition
- Activation Platform (in unlocked + 1GP managed)
- Data Streams
- Data Lake Objects (DLOs)
- Data Model Objects (DMOs) — standard and custom
- Calculated Insights
- Identity Resolution Rulesets
- Segments (definitions)
- Activation Targets and Activations (definitions)
- Search Index Configurations
- Retrievers
- Data Mappings

**Not all components are packageable** — check the Data 360
Extensibility Readiness Matrix before designing kit contents.

**DevOps tooling for Data Kits:**
- DevOps Center supports Data 360 metadata.
- Data 360 Metadata API for programmatic kit assembly.
- Salesforce CLI (`sf project deploy/retrieve`) supports kit deployment.
- Connect REST is the current programmatic deployment path for standard and
  DevOps data kits. Set `asyncMode=true`, capture the returned job ID, and poll
  status to `Completed` or `Error`.
- Treat the "Deploy Data Kit Components" flow as a legacy compatibility path
  for new automation guidance.
- Standard and DevOps data kits use different request shapes. Confirm package
  installation, Data 360 Architect permission, data-kit developer name, and
  target data-space parity before deployment.

**2GP Workflow (Salesforce Partners):**
1. Create a development scratch org or sandbox with Data 360 enabled.
2. Build and validate Data 360 metadata in the dev environment.
3. Add components to a Data Kit (Standard type).
4. Create a 2GP managed package (Data 360 metadata only — NOT mixed).
5. Create a package version; tag with semantic versioning.
6. Promote to released (managed-released).
7. Distribute via AppExchange or direct install link.
8. Subscribers install; deploy data kit flow runs to apply metadata to
   their target data space.

**Pre-flight before building a kit:**
- Every component in the kit appears on the Extensibility Readiness Matrix.
- DMO references are resolved (no hanging references to non-packageable DMOs).
- Identity rulesets reference DMOs that ARE in the kit.
- Calculated Insights reference DMOs that ARE in the kit.
- Data Streams reference Data Sources that ARE in the kit.
- Tags and classifications used by policies are documented (policies
  themselves may not be packageable — verify in matrix).
- Target data space exists in the subscriber org.
- License/edition requirements documented for subscribers (Data 360
  edition, add-on licenses for activation connectors, etc.).

**Validation gates after deploying a Data Kit:**
- All components landed in the expected data space.
- Data Streams successfully connect to the subscriber's Data Source.
- DMO mappings resolve to source DLOs.
- Identity Resolution Ruleset publishes successfully.
- Calculated Insight runs successfully on first scheduled execution.
- Search Index produces chunks; retriever returns results.
- Segments compile (DBT validation passes).
- Test the kit in a clean subscriber sandbox before production rollout.
<!-- SF_DOC_SYNC_END:data-kits-and-packaging -->
