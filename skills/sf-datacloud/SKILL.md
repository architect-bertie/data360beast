---
name: sf-datacloud
description: >
  Salesforce Data 360 cross-phase orchestration for connect, prepare, harmonize,
  retrieve, insights, semantic layer, AI models, reports, automation, segment,
  and act. TRIGGER when: the user needs end-to-end production Data 360 planning,
  delivery, troubleshooting, or agentic architecture across multiple phases. DO
  NOT TRIGGER when: the task is clearly isolated to one specialist skill.
license: MIT
metadata:
  version: "2.0.0"
  author: "architect-bertie"
---

# sf-datacloud

Use this skill when the user needs a **multi-phase Data 360 plan**, not just one endpoint or one query.

Production checklist: [references/production-implementation-checklist.md](references/production-implementation-checklist.md)

Data360 Beast references:
- Beast preflight: [docs/beast-preflight.md](../../docs/beast-preflight.md)
- Phase proof matrix: [docs/phase-proof-matrix.json](../../docs/phase-proof-matrix.json)
- Public operating model: [docs/operating-model.md](../../docs/operating-model.md)
- Data 360 model-gallery implementation map: [docs/data360/model-gallery-implementation-map.md](../../docs/data360/model-gallery-implementation-map.md)
- Interoperability decision map: [docs/data360/interoperability-decision-map.md](../../docs/data360/interoperability-decision-map.md)
- RAG/search-index playbook: [docs/data360/rag-search-index-retriever-playbook.md](../../docs/data360/rag-search-index-retriever-playbook.md)
- Cost and usage sizing contract: [docs/data360/cost-usage-sizing-contract.md](../../docs/data360/cost-usage-sizing-contract.md)
- Develop/package/deploy matrix: [docs/data360/develop-package-deployment-matrix.md](../../docs/data360/develop-package-deployment-matrix.md)
- MCP tool selection: [docs/data360/mcp-tool-selection.md](../../docs/data360/mcp-tool-selection.md)
- Limits source precedence: [docs/data360/limits-source-precedence.md](../../docs/data360/limits-source-precedence.md)
- Developer Guide index: [docs/data360/developer/index.md](../../docs/data360/developer/index.md)
- Companion MCP installs: [docs/mcp-dependencies.md](../../docs/mcp-dependencies.md)
- Proof ledger: [docs/proof-ledger.md](../../docs/proof-ledger.md)
- Public LLM map: [docs/llms.txt](../../docs/llms.txt)
- For exact Salesforce behavior, fetch official Help/Developer docs on demand with `sf-docs`.
- For endpoint shape, use OpenAPI from the official spec or the user-supplied Swagger before writing payloads.

## First routing decision

1. If the user wants **programmatic API work**, start with [sf-datacloud-connectapi](../sf-datacloud-connectapi/SKILL.md).
2. If the user wants a single phase, route immediately:
   - connections -> [sf-datacloud-connect](../sf-datacloud-connect/SKILL.md)
   - streams / DLOs / transforms -> [sf-datacloud-prepare](../sf-datacloud-prepare/SKILL.md)
   - DMOs / mappings / IR / graphs -> [sf-datacloud-harmonize](../sf-datacloud-harmonize/SKILL.md)
   - governance / tags / masking / access policies -> [sf-datacloud-governance](../sf-datacloud-governance/SKILL.md)
   - SQL / metadata / profile / query MCP -> [sf-datacloud-retrieve](../sf-datacloud-retrieve/SKILL.md)
   - calculated insight SQL / measures / dimensions -> [sf-datacloud-calculated-insights](../sf-datacloud-calculated-insights/SKILL.md)
   - unstructured data / chunking / retrievers -> [sf-datacloud-unstructured-retrieval](../sf-datacloud-unstructured-retrieval/SKILL.md)
   - metadata semantics for agentic use cases -> [sf-datacloud-metadata-agentic](../sf-datacloud-metadata-agentic/SKILL.md)
   - semantic models / governed metrics -> [sf-datacloud-semantic-layer](../sf-datacloud-semantic-layer/SKILL.md)
   - AI Models / Einstein Studio -> [sf-datacloud-ai-models](../sf-datacloud-ai-models/SKILL.md)
   - reports / dashboards -> [sf-datacloud-analytics](../sf-datacloud-analytics/SKILL.md)
   - segments / member counts -> [sf-datacloud-segment](../sf-datacloud-segment/SKILL.md)
   - data actions / Data 360 triggered flows -> [sf-datacloud-automation](../sf-datacloud-automation/SKILL.md)
   - activations / data actions -> [sf-datacloud-act](../sf-datacloud-act/SKILL.md)

## Default architecture

Prefer this order:

1. interoperability choice: ingest, live query, accelerated query, file federation, or hybrid
2. connections and source inspection
3. streams / DLOs / transforms
4. governance baseline: data spaces, permission sets, tags, classifications, masking, and policy posture
5. model-gallery fit: choose the subject area, anchor DMO, grain, and relationship path
6. DMO mappings and identity resolution
7. query validation and metadata checks
8. calculated/streaming insights, search indexes, semantic models, and AI models
9. RAG retrieval design when applicable: ADL/manual setup, field roles, chunking,
   search type, retrievers, prompt scope, Flow/Apex fallback, and evaluation
10. segment creation and count validation
11. activations, data actions, flows, reports, and monitoring
12. development lifecycle: environment, API surface, data kits, packageability, deploy path, and cost/usage

## Programmatic-first rule

Default to these surfaces unless the user explicitly asks for a different runtime:

- Connect REST APIs
- Data 360 API / Direct API when tenant-side read performance is the point
- Metadata API and data kits for deployable metadata
- Apex `ConnectApi`
- `datacloud-mcp-query` for local SQL discovery only: Query SQL, list tables,
  and describe table

Treat community `sf data360` commands as optional helpers, not the primary architecture.

## Beast mode loop

Use this for non-trivial Data 360 work:

1. Run [docs/beast-preflight.md](../../docs/beast-preflight.md) for target org,
   API version, data space, persona, lifecycle, authorization boundary, tools,
   and proof target.
2. Route through [docs/phase-proof-matrix.json](../../docs/phase-proof-matrix.json)
   to pick the specialist skill, required source, proof target, and forbidden
   assumptions.
3. Check [docs/operating-model.md](../../docs/operating-model.md) for the phase gate.
4. Use `sf-docs` for exact official Help/Developer docs when a rule, permission, limit, or setup step matters.
5. For limits, use current Data 360 Limits and Guidelines first; follow Data
   Services Billable Usage Types when referenced; use Customer Data Platform
   limits only for explicit legacy CDP scope or labeled comparison.
6. Use the Data360 Beast OpenAPI catalog for endpoint/method/schema lookup.
7. Use Data 360 MCP `search -> payload_examples -> execute` for live org operations when available; install/configure it from [docs/mcp-dependencies.md](../../docs/mcp-dependencies.md) when missing.
8. Validate with target-org metadata, data space, permission, status, query, count, or publish evidence.
9. Run the cost and usage sizing contract when the design has meaningful
   ingestion, query, insight, RAG, activation, automation, or environment-replay
   volume.

Do not copy long Help pages or endpoint dumps into skills. Keep durable detail in the project reference layer and retrieve exact docs on demand.

## Hard-won orchestration rules

- For external data, do not assume ingestion is the default. Choose based on
  freshness, governance owner, access pattern, data volume, and cost/I/O.
- Ingest the governed core for identity, compliance, and operational activation;
  federate the edge for fresh, high-volume, exploratory, or AI/ML workloads
  when source governance is acceptable.
- Data 360 development is not identical to standard Platform development. Confirm
  customer vs partner path, sandbox vs second org, data kit strategy,
  packageability, and metered test usage before recommending a lifecycle.
- Treat develop/package/deploy work as its own proof lane: data kit membership,
  metadata coverage, dependency order, target-org deploy validation, and
  reauthorization readback are required before claiming portability.
- Keep Data 360 metadata and Salesforce Platform metadata packaging separate
  unless current docs explicitly allow the target combination.
- Data spaces, data kit membership, metadata coverage, and connector
  reauthorization are deployment proof points, not cleanup details.
- The query plane and the DBT segment compiler are different gates.
- Data Graph is excellent for enrichment and retrieval, but should not become activation logic unless the signal is also segment-safe.
- Metadata quality is an agentic feature. Descriptions, grain, relationships, and metric semantics must be production artifacts.
- Governance metadata is also an agentic feature. Tags, classifications, access policies, masking, and agent-safe field notes must be explicit.
- The official DMO catalog is a label directory; runtime names still need metadata resolution.
- The public Data 360 model gallery is the best early design compass for
  choosing anchor DMOs and relationship paths. Use it before creating custom
  DMOs or flattening source tables.
- RAG is not just prompt work. Design and validate the source object path,
  chunking, index fields, filter fields, retriever version, prompt resolution,
  and agent/action scope before tuning the answer text.
- Treat `Individual`, `Unified Individual`, `Account`, `Account Contact`,
  `Party`, and contact point DMOs as distinct grains. Do not collapse them into
  one generic customer object.
- Always verify created segment status after the create call.
- Always test governed behavior with a non-admin user; admin metadata visibility can hide runtime access failures.
- Data spaces affect visibility, API context, and names. When a task crosses data spaces, explicitly confirm data space, prefix, and API parameter/token handling.
- Never default to legacy Customer Data Platform limits for current Data 360
  architecture. Use them only when the user names CDP/Customer Data Platform,
  the org's license proves it, or you are comparing legacy and current behavior.

## Doc-Synced Notes

<!-- SF_DOC_SYNC_START:limits-first-architecture -->
### Limits-first architecture gate

_Auto-synced from the local sf-docs cached Salesforce Help export (official docs only).

**Sources (sf-docs cached Help):**
- data.c360_a_limits_and_guidelines.htm (2026-05-11T20:20:31.057Z) — Data 360 Limits and Guidelines

**Notes:**
- Treat the captured Limits and Guidelines page as a required source before making durable guidance for this phase.
- Prioritize current Data 360 limits over legacy Customer Data Platform limits;
  use CDP limits only for explicit legacy scope or labeled comparison.
- When current Data 360 docs route a value to Data Services Billable Usage
  Types, treat the answer as entitlement/usage-sensitive until org contract or
  Digital Wallet proof is available.
- Separate soft guidelines from hard limits, and call out when a limit can require an Account Executive request or org-specific validation.
- For cross-phase designs, explicitly identify the phase that owns each limit: ingest, model, query, insights, segment, activation, automation, search, or API.
- Keep cost, throttling, hard limits, and feature availability in the proof plan, not as afterthoughts.
- Relevant limit families currently captured include: General Guidelines and Limits, Activation Guidelines and Limits, Calculated Insights Guidelines and Limits, Code Extension Guidelines and Limits (Beta), Data Actions Guidelines and Limits, Data Explorer Guidelines and Limits, Data Federation Guidelines and Limits, Data Graphs Guidelines and Limits, Data Ingestion Guidelines and Limits, Data Model Object Guidelines and Limits, Data Shares Guidelines and Limits, Data Transforms Guidelines and Limits.
<!-- SF_DOC_SYNC_END:limits-first-architecture -->

<!-- SF_DOC_SYNC_START:about-and-get-started -->
### About Data 360, Get Started, Editions, and Lifecycle (Router-Level Orientation)

_Distilled from official Salesforce sources only. Deep mechanics belong
in the specialist skills — this block is orientation only._

**Sources:**
- data.c360_a_data_cloud.htm — About Data 360
- data.c360_a_product_considerations.htm — Get Started with Data 360
- data.c360_a_setup_provision.htm — Set Up and Turn On Data 360
- data.c360_a_dc_editions.htm — Editions and Licenses
- data.c360_a_data_spaces.htm — Data Spaces (overview only)
- data.c360_a_lifecycle_management_cleanup.htm — Lifecycle Management
- architect.salesforce.com/docs/architect/decision-guides/guide/data-360-provisioning.html — Data 360 Provisioning Decision Guide
- developer.salesforce.com/docs/data/data-cloud-dev/guide/dc-features-overview.html — Data 360 Features Brief Overview

**About Data 360:**
- Salesforce's cloud-native data platform, formerly known as Data Cloud
  (rebranded **October 14, 2025**). Functionality is unchanged from
  Data Cloud — only the name.
- Built entirely on **Hyperforce** (multi-tenant, ISO 27001, SOC 1/2/3,
  GDPR-ready).
- Goes beyond traditional CDPs: powers Sales, Service, Commerce, AI, and
  Marketing on one unified profile, not just Marketing.
- 300+ pre-built connectors; supports zero-copy federation, real-time
  ingest, and unstructured content for RAG.

**Headline capabilities (route to specialist for depth):**
| Capability | Specialist skill |
|---|---|
| Connect 300+ sources (zero-copy + ingest + streaming) | sf-datacloud-connect |
| Prepare/cleanse/transform raw data | sf-datacloud-prepare |
| Map DLOs to DMOs, run identity resolution, build data graphs | sf-datacloud-harmonize |
| Govern with ABAC + tags + masking | sf-datacloud-governance |
| Query and explore | sf-datacloud-retrieve |
| Calculated/streaming insights | sf-datacloud-calculated-insights |
| Unstructured RAG (search index + retrievers) | sf-datacloud-unstructured-retrieval |
| Semantic models / governed metrics | sf-datacloud-semantic-layer |
| Predictive ML / BYOM | sf-datacloud-ai-models |
| Reports + dashboards | sf-datacloud-analytics |
| Audience segmentation | sf-datacloud-segment |
| Activations + data actions | sf-datacloud-act |
| Flow automation (Data Cloud-triggered, activation-triggered) | sf-datacloud-automation |
| Packaging metadata as data kits | sf-datacloud-metadata-agentic |

**Get Started (admin orientation):**
1. Confirm Data 360 license / SKU is provisioned.
2. Assign permission sets (Data Cloud Architect for setup; User for
   read-only).
3. Connect first data source (typically Salesforce CRM via Sales/Service
   Cloud bundle).
4. Create first data stream and verify DLO populates.
5. Map to a starter DMO (Customer 360 Data Model).
6. Publish first identity resolution ruleset.
7. Build a sample segment + activation as proof.
8. Validate with non-admin user before broader rollout.

**Set Up and Turn On (system requirements):**
- Production org with Data 360 license OR Salesforce Foundations.
- System Administrator profile to access Setup.
- Data 360 is **automatically provisioned** on any production org that
  receives a license — no manual installation step.
- Default data space "default" exists in every org; create additional
  spaces for multi-brand/region needs.
- Sandbox refresh policy applies — Data 360 metadata refreshes per
  sandbox refresh schedule.

**Editions and Licenses (high-level — full SKU detail in Salesforce
sales materials):**
| SKU | Best for | Includes (orientation) |
|---|---|---|
| Data 360 Starter | Standalone Data 360 customers | Flex Credits, data storage allocation, Data 360 instance, admin + identity users |
| Data 360 Provisioning ("Everywhere") | Customers using other Salesforce products that ride on Data 360 | Smaller credit + storage allocation, same instance shape |
| Foundations | Free path for existing Salesforce customers | Limited storage and Flex Credits |

**Pricing models (orientation only):**
- **Flex Credits** — usage-based; consumed by ingestion, query, segment,
  activation, AI inference.
- **Profiles** — per-1k-profiles annual subscription with bundled credits.
- **Enterprise Profiles** — higher-tier profiles bundle including Data
  Masking and Ad Audience add-ons.
- Add-on licenses required for: Ad Audiences (Google Ads/DV360, LinkedIn
  CAPI, Meta, Pinterest, TikTok activations), Data Masking (Enterprise
  Profiles only).

**Plan Data Strategy (decision guide highlights):**
- Choose the **interoperability pattern** before assets:
  - Ingest for canonical governance.
  - Live query (zero-copy) for max freshness.
  - Accelerated query for read-heavy with stale tolerance.
  - File federation for big-object/open-table workloads.
  - Hybrid for governed core + fresh edge.
- Choose **data spaces strategy** early — multi-brand, multi-region, or
  multi-tenant operations should design space boundaries before ingest.
- Choose **identity resolution rule density** based on data quality and
  compliance: looser rules merge more, stricter rules preserve sources.

**Data Spaces (orientation only — deep details in
sf-datacloud-governance):**
- Logical segregation of data, metadata, and processes by brand/region/
  department.
- Every org has 1 "default" data space; add more as needed.
- Provisioned with permission sets; users gain access by permission set
  assignment.
- See sf-datacloud-governance for ABAC, tags, masking, and policy mechanics.

**Lifecycle Management (cleanup, retention, dispose):**
- **Archive** — move older records out of daily use, preserve for compliance.
- **Purge** — permanent deletion after retention period ends.
- **Backup** — copy before cleanup or migration.
- Use the Ingestion API delete endpoint for record-level cleanup
  (`POST /ssot/data-streams/:streamName/actions/delete-records`).
- For unstructured data, the UDLO Delete pathway removes content from
  search indexes (`data.c360_a_unstructured_data_udlo_delete.htm`).
- Retention policies should align with privacy regulations (GDPR right
  to erasure, CCPA opt-out).
- Storage analysis dashboards identify largest objects for cleanup
  prioritization.

**When to use this router skill vs a specialist:**
- Use sf-datacloud when planning **multi-phase work** that crosses
  ingest → harmonize → segment → activate or similar arcs.
- Route immediately to a specialist when the task is single-phase.
- Always start with the Beast preflight + phase-proof matrix before
  committing to any architecture decision.
<!-- SF_DOC_SYNC_END:about-and-get-started -->
