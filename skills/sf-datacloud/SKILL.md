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
  author: "Codex"
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
- query MCP for local SQL discovery

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
