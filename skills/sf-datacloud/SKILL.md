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
- Public operating model: [docs/operating-model.md](../../docs/operating-model.md)
- Interoperability decision map: [docs/data360/interoperability-decision-map.md](../../docs/data360/interoperability-decision-map.md)
- Companion MCP installs: [docs/mcp-dependencies.md](../../docs/mcp-dependencies.md)
- Public API cookbook: [docs/api-cookbook.md](../../docs/api-cookbook.md)
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
5. DMO mappings and identity resolution
6. query validation and metadata checks
7. calculated/streaming insights, search indexes, semantic models, and AI models
8. segment creation and count validation
9. activations, data actions, flows, reports, and monitoring

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

1. Route to the relevant phase skill.
2. Check [docs/operating-model.md](../../docs/operating-model.md) for the phase gate.
3. Use `sf-docs` for exact official Help/Developer docs when a rule, permission, limit, or setup step matters.
4. Use the Data360 Beast OpenAPI catalog for endpoint/method/schema lookup.
5. Use Data 360 MCP `search -> payload_examples -> execute` for live org operations when available; install/configure it from [docs/mcp-dependencies.md](../../docs/mcp-dependencies.md) when missing.
6. Validate with target-org metadata, data space, permission, status, query, count, or publish evidence.

Do not copy long Help pages or endpoint dumps into skills. Keep durable detail in the project reference layer and retrieve exact docs on demand.

## Hard-won orchestration rules

- For external data, do not assume ingestion is the default. Choose based on
  freshness, governance owner, access pattern, data volume, and cost/I/O.
- Ingest the governed core for identity, compliance, and operational activation;
  federate the edge for fresh, high-volume, exploratory, or AI/ML workloads
  when source governance is acceptable.
- The query plane and the DBT segment compiler are different gates.
- Data Graph is excellent for enrichment and retrieval, but should not become activation logic unless the signal is also segment-safe.
- Metadata quality is an agentic feature. Descriptions, grain, relationships, and metric semantics must be production artifacts.
- Governance metadata is also an agentic feature. Tags, classifications, access policies, masking, and agent-safe field notes must be explicit.
- The official DMO catalog is a label directory; runtime names still need metadata resolution.
- Always verify created segment status after the create call.
- Always test governed behavior with a non-admin user; admin metadata visibility can hide runtime access failures.
- Data spaces affect visibility, API context, and names. When a task crosses data spaces, explicitly confirm data space, prefix, and API parameter/token handling.
