---
name: sf-datacloud-harmonize
description: >
  Salesforce Data 360 Harmonize phase for DMOs, mappings, identity resolution,
  profile resolution, and Data Graphs. TRIGGER when: the user works with DMOs,
  mappings, relationships, identity resolution, unified profiles, or data graphs.
license: MIT
metadata:
  version: "2.0.0"
  author: "architect-bertie"
---

# sf-datacloud-harmonize

Use this skill for the **schema and unification plane**.

Beast references:
- Beast preflight: [docs/beast-preflight.md](../../docs/beast-preflight.md)
- Phase proof matrix: [docs/phase-proof-matrix.json](../../docs/phase-proof-matrix.json)
- Public operating model: [docs/operating-model.md](../../docs/operating-model.md)
- Data 360 model-gallery implementation map: [docs/data360/model-gallery-implementation-map.md](../../docs/data360/model-gallery-implementation-map.md)
- Proof ledger: [docs/proof-ledger.md](../../docs/proof-ledger.md)
- Public LLM map: [docs/llms.txt](../../docs/llms.txt)
- Limits source precedence: [docs/data360/limits-source-precedence.md](../../docs/data360/limits-source-precedence.md)
- For exact Salesforce behavior, fetch official Help/Developer docs on demand with `sf-docs`.
- For endpoint shape, use OpenAPI from the official spec or the user-supplied Swagger before writing payloads.

## Prefer these Connect API families

- `GET/POST/PATCH/DELETE /ssot/data-model-objects`
- `GET/POST/DELETE /ssot/data-model-object-mappings`
- `PATCH /ssot/data-model-object-mappings/.../field-mappings/...`
- `GET/POST /ssot/data-model-objects/:dataModelObjectName/relationships`
- `GET/POST/PATCH/DELETE /ssot/identity-resolutions`
- `POST /ssot/identity-resolutions/:identityResolution/actions/run-now`
- `GET/POST/DELETE /ssot/data-graphs`
- `GET /ssot/data-graphs/metadata`
- `GET /ssot/data-graphs/data/...`
- semantic layer and metadata quality handoff

## Rules

- Resolve runtime DMO/profile names through metadata before writing query or segment logic.
- For model design, load the model-gallery implementation map when choosing
  between Case, Party, Privacy, Engagement, Email Engagement, Google Analytics,
  Product, Sales Order, Financial Services, Healthcare Provider, Vehicle Charger
  and Telematics, Student Financial Aid, or GenAI Audit and Feedback subject
  areas.
- Pick the anchor DMO before designing joins, insights, segments, or graphs.
  Common anchors include Unified Individual, Individual, Account, Account
  Contact, Contact Point plus Consent, Engagement Action, Sales Order, Sales
  Order Product, Product, Case, Asset, and vertical-domain objects.
- Only mapped fields and objects with relationships can be used for segmentation and activation.
- Profile and Other DMOs require primary key mapping; Engagement DMOs require primary key and event datetime mapping.
- For party-area modeling, Party is the reference to `Individual.Id`; map at least one contact point channel for unification and activation.
- Do not treat `Individual`, `Account`, `Account Contact`, `Party`, contact
  point DMOs, and unified DMOs as synonyms. They represent different grains.
- Do not model consent as a single boolean on `Individual`; consent is scoped by
  party, contact point, channel, purpose, brand, status, legal basis, and action.
- Prefer standard C360 DMOs and starter mappings when they match the business concept; customize only when the standard model cannot represent the domain cleanly.
- Model grain explicitly: profile, engagement, transaction, product, account, case, content, or support object.
- Define relationship cardinality before allowing calculated insights, segments, data graphs, or reports to join across objects.
- Relationship cardinality cannot be changed after creation. A bad cardinality choice becomes a downstream segment/activation problem.
- Standard relationships become active only when both participating fields are mapped.
- Treat identity resolution as asynchronous; verify resulting unified shapes after runs.
- A published identity ruleset proves the definition is available, not that an
  identity job has completed or unified outputs are populated. Require a
  terminal job state plus UDMO/link-table counts before downstream use.
- For identity resolution, validate source counts, match/consolidation rate, over-grouping, under-grouping, outlier unified profiles, and contact point quality before trusting segments.
- Verify governance access to unified result and unified link DMOs before downstream reports, graphs, segments, or agents consume identity outputs.
- Use Data Graph for retrieval and enrichment, and only turn graph signals into activation criteria when those signals are represented in segment-safe schema.
- Data Graphs must have a primary DMO, live in a data space, and should include only fields needed for retrieval/agent context.
- Include calculated insights or streaming insights in a Data Graph only when they are based on a DMO also included in the graph.
- Data Graph users can need access to ID/value/fragment DMOs and graph inputs. Masking or deny FLS on graph fields can hide or break the graph.
- Keep Data Graph keys and relationship fields unmasked unless a governed replacement path is tested.
- The current project pattern is: graph context improves proposal quality, but activation rebuilds from DMO-safe criteria.
- Prepare descriptions and relationship semantics with [sf-datacloud-metadata-agentic](../sf-datacloud-metadata-agentic/SKILL.md) when Agentforce or AI Models will consume the metadata.

## Handoff

- For query validation -> [sf-datacloud-retrieve](../sf-datacloud-retrieve/SKILL.md)
- For CIs -> [sf-datacloud-calculated-insights](../sf-datacloud-calculated-insights/SKILL.md)
- For segments -> [sf-datacloud-segment](../sf-datacloud-segment/SKILL.md)
- For semantic models -> [sf-datacloud-semantic-layer](../sf-datacloud-semantic-layer/SKILL.md)
- For tags, masking, RLS, and graph access failures -> [sf-datacloud-governance](../sf-datacloud-governance/SKILL.md)

## Doc-Synced Notes

### Extended Doc-Synced References

The DMO/mapping, relationships, and identity-resolution distillations
live in dedicated reference files to keep this SKILL.md focused on
rules, workflow, and validation:

- [references/dmo-and-mapping.md](references/dmo-and-mapping.md) — DLO
  vs DMO model, DMO categories, standard DMOs, field mapping, starter
  bundles, custom DMOs, DMO-to-DMO transforms, mapping in data spaces,
  normalized vs denormalized.
- [references/dmo-relationships.md](references/dmo-relationships.md) —
  1:1 / N:1 cardinality, primary/foreign/related fields, defining
  relationships via UI/API, common identity DMO examples.
- [references/identity-resolution-and-graphs.md](references/identity-resolution-and-graphs.md) —
  rulesets, match rules (exact/fuzzy/normalized), reconciliation rules,
  unified outputs, Data Graphs, real-time graphs, governance interactions,
  pre-flight checks.

Each reference file retains its SF_DOC_SYNC markers for the doc-watch
pipeline.

<!-- SF_DOC_SYNC_START:limits-modeling-identity-graphs -->
### Modeling, identity, and graph limit gate

_Auto-synced from the local sf-docs cached Salesforce Help export (official docs only)._

**Sources (sf-docs cached Help):**
- data.c360_a_limits_and_guidelines.htm — Data 360 Limits and Guidelines | Salesforce Help

**Source fingerprint:** `1ce0aa69b0b275b02c26170b`

**Notes:**
- Treat the captured Limits and Guidelines page as a required source before making durable guidance for this phase.
- Separate soft guidelines from hard limits, and call out when a limit can require an Account Executive request or org-specific validation.
- Before choosing DMO shape, relationship paths, identity rulesets, or Data Graph shape, check limits for DMOs, identity resolution, and Data Graphs.
- Escalate unclear relationship, key, or graph-volume assumptions into metadata probes instead of baking them into skill guidance.
- Relevant limit families currently captured include: General Guidelines and Limits, Activation Guidelines and Limits, AI Models (formerly Einstein Studio) Guidelines and Limits, Calculated Insights Guidelines and Limits, Code Extension Guidelines and Limits, Data Actions Guidelines and Limits, Data Explorer Guidelines and Limits, Data Federation Guidelines and Limits, Data Graphs Guidelines and Limits, Data Ingestion Guidelines and Limits, Data Model Object Guidelines and Limits, Data Shares Guidelines and Limits.

<!-- SF_DOC_SYNC_END:limits-modeling-identity-graphs -->

<!-- SF_DOC_SYNC_START:developer-dmo-catalog -->
### DMO and mapping reference gate

_Auto-synced from sf-docs captures of official Salesforce Developer documentation._

**Sources:**
- https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-model-data.html - Model Data in Data 360 | Data 360 DMO and Mapping Guide | Salesforce Developers

**Source fingerprint:** `0f6dcc1013a978f8f7038567`

**Implementation notes:**
- Use the official DMO catalog to discover standard schemas, standard DLO-to-DMO mappings, data bundles, extensibility readiness, and legacy schemas.
- The catalog currently carries developer-preview language; verify target-org metadata and current Help before production implementation.
- Prefer standard DMOs when their grain and semantics fit, but do not force source fields into misleading standard attributes; preserve lineage with a justified custom DMO or field when needed.

<!-- SF_DOC_SYNC_END:developer-dmo-catalog -->
