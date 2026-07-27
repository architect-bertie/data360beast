---
name: data360beast
description: Use this skill for Salesforce Data 360 architecture, implementation, troubleshooting, Connect API payloads, metadata discovery, query SQL, calculated insights, semantic layer, search, segmentation, activation, data actions, governance, data spaces, and agentic validation workflows.
---

# Data360 Beast

Data360 Beast turns Salesforce Data 360 work into a proof-driven execution
loop. Use it whenever the user is designing, building, validating, executing, or
debugging Data 360.

Beast is not only a knowledge system. It is an execution system rooted in
proven knowledge with proof and learning loops. The skill outcome should be
execution-ready for the target org, not just advice:

```text
Execute in any authorized, compatible Data 360 org after preflight confirms
org, data space, permissions, available tools, and mutation approval.
```

## Companion MCP Setup (do this first)

Without these two servers the agent runs in degraded mode:

1. **sf-docs** - fetches help.salesforce.com and developer.salesforce.com
   pages as clean Markdown. Install: docs/mcp-dependencies.md.
2. **data360** - exposes Data 360 Connect API tools (search,
   payload_examples, execute). Install: docs/mcp-dependencies.md.

### Degraded-Mode Rules

Apply these rules when one or both companion MCPs are unavailable.

**When sf-docs is unavailable**

- Use only static references listed in this skill.
- Do not state limits, quotas, feature availability, or billing figures from memory.
- Label answers: source: docs-unverified (sf-docs unavailable)
- Lower confidence to inferred for any claim requiring a live doc check.

**When data360 MCP is unavailable**

- Do not attempt live Connect API calls or org validation.
- Generate payloads from OpenAPI shape and proof ledger evidence only.
- Label answers: validation: live-validation-unavailable (data360 MCP unavailable)
- Do not fabricate returned IDs, status codes, or org-specific behavior.

**When both are unavailable**

- Restrict to architecture guidance and structural payload design from static references.
- Open every response with: [degraded mode: static references only]
- Stop rather than guess for: field names not in the OpenAPI spec, current feature
  availability, limit values, connector behavior, and production mutation steps.

**Stop condition**

Stop and ask for authoritative input when: both MCPs are unavailable, the fact
is absent from every static reference, and a wrong answer would cause data loss,
an incorrect production mutation, or a security boundary violation.

## Operating Loop

Use the four-layer loop from
[docs/operating-model.md](../../docs/operating-model.md):

```text
Think -> Act -> Prove -> Learn
```

1. **Think** with Beast preflight, phase proof matrix, official docs, OpenAPI,
   Beast specialists, proof ledger evidence, and optional Salesforce `sf-skills`
   companion guidance.
2. **Act** only after authorization is clear, using the right MCP, direct `sf`
   REST, `sf data360` CLI, metadata/deployment tool, or helper script.
3. **Prove** with returned ID, readback, status, count, data space, metadata,
   query result, log, event, or delivery signal.
4. **Learn** by promoting only distilled public-safe lessons into Beast or
   routing scenario-heavy work to Labs.

For limits, use
[docs/data360/limits-source-precedence.md](../../docs/data360/limits-source-precedence.md):
current Data 360 limits first, Data Services usage when referenced, and legacy
Customer Data Platform limits only when explicitly in scope.

End non-trivial responses as one of: execution-ready plan, executed-and-proven
result, done-but-waiting result, blocked-with-reason, or lab-required.

## Source Hierarchy

1. User-provided target org, files, data space, API version, and business goal.
2. Official Salesforce docs fetched on demand.
3. User-supplied or locally available Data 360 Connect API OpenAPI spec.
4. Data360 Beast public docs and proof ledger.
5. Live org validation in an explicitly authorized org.

Companion MCP install paths are documented in
[docs/mcp-dependencies.md](../../docs/mcp-dependencies.md). Do not assume
`sf-docs` or `data360` MCP servers are bundled with the skill pack.

## Salesforce sf-skills Data 360 Companion

After installing Beast, agents can optionally install the Salesforce
`forcedotcom/sf-skills` Data 360 companion subset for `sf data360` execution
playbooks, readiness checks, command templates, and CLI troubleshooting.

Use the companion only after Beast preflight and phase routing. Beast remains
the authority for source order, proof labels, limits precedence, official-doc
routing, OpenAPI discipline, confidence, and Labs promotion. `sf-docs` remains
the official-doc path for current Salesforce setup, permission, limit,
licensing, and behavior claims.

The companion helps with command planning and runtime gotchas. Actual org
actions still happen through approved CLI, MCP, API, metadata, or helper tools
inside the preflight authorization boundary.

Install or dry-run the companion with:

```bash
python3 skills/data360beast/scripts/install_sf_skills_data360_companion.py --dry-run
```

The companion contract is documented in
[docs/data360/sf-skills-data360-companion.md](../../docs/data360/sf-skills-data360-companion.md)
and the router reference is
[references/sf-skills-data360-companion.md](references/sf-skills-data360-companion.md).
Use **Data 360** in Beast-facing guidance; preserve exact Salesforce
`sf-skills` names only for folders, install paths, package metadata, or command
surfaces.

Public-safe operating references:
- [docs/beast-preflight.md](../../docs/beast-preflight.md): required envelope,
  tool inventory, proof target, and mutation gate.
- [docs/phase-proof-matrix.json](../../docs/phase-proof-matrix.json):
  machine-readable phase routing, required sources, proof targets, and forbidden
  assumptions.
- [docs/phase-coverage-matrix.json](../../docs/phase-coverage-matrix.json):
  machine-readable coverage by phase, source, proof, helper, and frontier.
- [docs/data360/help/index.md](../../docs/data360/help/index.md): 369 indexed Salesforce Help pages.
- [docs/data360/developer/index.md](../../docs/data360/developer/index.md): 24 indexed Salesforce Developer Guide pages.
- [docs/data360/developer/learning-map.md](../../docs/data360/developer/learning-map.md): developer-guide synthesis for routing and skill updates.
- [docs/data360/model-gallery-implementation-map.md](../../docs/data360/model-gallery-implementation-map.md): public Data 360 model-gallery synthesis for DMO anchors, relationship paths, model grain, and implementation traps.
- [docs/data360/limits-source-precedence.md](../../docs/data360/limits-source-precedence.md): current Data 360 limits first, Data Services usage follow-through, and legacy CDP comparison rules.
- [docs/data360/rag-search-index-retriever-playbook.md](../../docs/data360/rag-search-index-retriever-playbook.md): public-safe RAG, search-index, chunking, retriever, and troubleshooting playbook distilled from a 45-page Salesforce public-facing best-practices PDF.
- [docs/data360/cost-usage-sizing-contract.md](../../docs/data360/cost-usage-sizing-contract.md): cost and usage sizing contract for ingestion, query, insights, RAG, segmentation, activation, automation, and environment replay.
- [docs/data360/develop-package-deployment-matrix.md](../../docs/data360/develop-package-deployment-matrix.md): develop, package, data kit, deploy, and readback matrix.
- [docs/data360/mcp-tool-selection.md](../../docs/data360/mcp-tool-selection.md): tool-selection guidance for `sf-docs`, `data360`, `datacloud-mcp-query`, and direct `sf` REST calls.
- [docs/data360/sf-skills-data360-companion.md](../../docs/data360/sf-skills-data360-companion.md): Salesforce `sf-skills` Data 360 companion contract for optional `sf data360` execution playbooks.
- [docs/data360/docs-watch-operating-model.md](../../docs/data360/docs-watch-operating-model.md): weekly official-doc refresh, oversized Help fallback, audit, skill-sync, and GitHub publishing model.
- [docs/proof-ledger.md](../../docs/proof-ledger.md): public-safe evidence,
  caveats, confidence labels, labs references, and promotion status.
- [docs/labs-interface.md](../../docs/labs-interface.md): boundary between
  Beast and the Labs proving ground for golden scenarios, synthetic journeys,
  payload experiments, traces, and future cookbook candidates.
- [docs/beast-evals.md](../../docs/beast-evals.md): lightweight eval checks for
  future Beast mode changes.

Do not treat this repository as official Salesforce documentation. Do not
hallucinate endpoint paths, payload fields, limits, permissions, or feature
availability.

## Beast Preflight

For non-trivial work, capture or infer:

- business goal and target phase
- target org or alias, API version, data space, license posture, and user
  persona
- asset lifecycle: disposable lab, sandbox, or production
- authorization boundary: docs-only, metadata read, live validation, create or
  update, or production mutation
- available thinking sources: `sf-docs`, OpenAPI/Swagger, Beast specialists,
  proof ledger, optional Salesforce `sf-skills` Data 360 companion, and
  user-provided files
- available action/proof tools: `data360` MCP,
  `datacloud-mcp-query`, direct `sf` REST, `sf data360` CLI commands planned
  through the companion, metadata/deployment tools, and helper scripts
- proof target and confidence label

If a required fact is missing, continue only when the task can safely proceed
with an explicit assumption. Lower confidence instead of filling gaps with
guesses.

## Phase Router

Use [docs/phase-proof-matrix.json](../../docs/phase-proof-matrix.json) as the
machine-readable routing table. The bullets below are the human shorthand.

- **Connect**: connectors, connections, connector schema, refresh, ingestion
  setup, connector permissions.
- **Prepare**: data streams, DLOs, transforms, ingestion status, document
  processing.
- **Harmonize**: DMOs, mappings, relationships, identity resolution, data graphs,
  model-gallery subject areas, anchor DMO selection, and relationship-path design.
- **Govern**: data spaces, tags, classifications, security policies, access.
- **Retrieve**: Query SQL, Query v2, Profile API, metadata discovery.
- **Insight**: calculated insights, streaming insights, SQL validation.
- **Semantic**: C360 semantic models, metrics, dimensions, shared dimensions.
- **AI/Search**: search indexes, retrievers, unstructured retrieval, grounding.
- **Segment**: segment create/read/publish/count, DBT segments, membership proof.
- **Act**: activation targets, activations, data action targets, data actions.
- **Automation**: triggered flows, DataObjectDataChgEvent, activation-triggered
  flows, refresh cadence, monitoring.
- **Develop/Package**: API surface selection, External Client App auth,
  development environments, data kits, packageability, sandbox-to-production
  deployment, metadata coverage, cost and usage.

## Engine-Aware Triage

Use [docs/data360/architecture-engine-map.md](../../docs/data360/architecture-engine-map.md)
when the work involves architecture, performance, cross-surface mismatches, or
ambiguous troubleshooting.

Use [docs/data360/interoperability-decision-map.md](../../docs/data360/interoperability-decision-map.md)
when the work involves external lakehouses, zero copy, ingestion strategy,
freshness, cost/I/O, or hybrid architecture.

Use [docs/data360/model-gallery-implementation-map.md](../../docs/data360/model-gallery-implementation-map.md)
when the work involves Data 360 data models, DMO choice, model diagrams, subject
areas such as Case, Party, Privacy, Engagement, Product, Sales Order,
Financial Services, Healthcare Provider, Vehicle Charger and Telematics, Student
Financial Aid, or GenAI Audit and Feedback.

Use [docs/data360/rag-search-index-retriever-playbook.md](../../docs/data360/rag-search-index-retriever-playbook.md)
when the work involves RAG architecture, Agentforce Data Libraries, manual
search indexes, chunking, hybrid/vector search, retriever filters, prompt
grounding, Flow/Apex RAG orchestration, or retrieval troubleshooting.

Default loop:

```text
symptom -> surface -> DSO/DLO/DMO/CIO/graph layer -> likely execution plane -> proof path
```

Interoperability loop:

```text
workload -> freshness need -> governance need -> cost/I/O profile -> access pattern -> integration pattern -> proof path
```

Treat engine mapping as inferred unless proven in the target org. Spark-like
processing, Trino-like query, Hyper-like analytics serving, Airflow-like
orchestration, and Iceberg-style storage are useful mental models, not public
API guarantees.

## Specialist Skill Routing

After loading this router, use the matching specialist skill when the work is
specific:

- [sf-datacloud](../sf-datacloud/SKILL.md): cross-phase architecture.
- [sf-datacloud-connectapi](../sf-datacloud-connectapi/SKILL.md): REST,
  OpenAPI, Apex ConnectApi, payload design.
- [sf-datacloud-connect](../sf-datacloud-connect/SKILL.md): connectors and
  connections.
- [sf-datacloud-prepare](../sf-datacloud-prepare/SKILL.md): streams, DLOs,
  transforms.
- [sf-datacloud-harmonize](../sf-datacloud-harmonize/SKILL.md): DMOs,
  mappings, identity, data graphs.
- [sf-datacloud-governance](../sf-datacloud-governance/SKILL.md): data spaces,
  access, tags, masking, policies.
- [sf-datacloud-retrieve](../sf-datacloud-retrieve/SKILL.md): SQL, profile,
  metadata, query tools.
- [sf-datacloud-calculated-insights](../sf-datacloud-calculated-insights/SKILL.md):
  calculated and streaming insight SQL.
- [sf-datacloud-segment](../sf-datacloud-segment/SKILL.md): segments, counts,
  publish proof.
- [sf-datacloud-act](../sf-datacloud-act/SKILL.md): activations and data
  action delivery.
- [sf-datacloud-automation](../sf-datacloud-automation/SKILL.md): flows,
  events, monitoring.
- [sf-datacloud-semantic-layer](../sf-datacloud-semantic-layer/SKILL.md):
  semantic models and metrics.
- [sf-datacloud-ai-models](../sf-datacloud-ai-models/SKILL.md): AI models and
  model outputs.
- [sf-datacloud-unstructured-retrieval](../sf-datacloud-unstructured-retrieval/SKILL.md):
  search indexes and retrievers.
- [sf-datacloud-analytics](../sf-datacloud-analytics/SKILL.md): reports,
  dashboards, analytics.
- [sf-datacloud-metadata-agentic](../sf-datacloud-metadata-agentic/SKILL.md):
  metadata semantics for agents.

## Connect API Workflow

For API work:

1. Require or infer the target data space and API version.
2. Search the OpenAPI spec for the operation family before writing payloads.
3. Use the smallest valid payload first.
4. Create only disposable lab assets unless the user explicitly asks for
   production changes.
5. Read back by returned ID and check status/count/metadata.
6. Capture caveats in the response so the next agent does not rediscover them.

## Proof Kernel

Use the specialist skills and public docs for details. Keep this top router
small and enforce these cross-cutting rules:

- Use [docs/phase-proof-matrix.json](../../docs/phase-proof-matrix.json) to pick
  the required source and proof target before answering.
- Query success does not prove segment, transform, analytics, activation, or
  orchestration behavior; proof must match the target surface.
- Use the model-gallery map before choosing DMO anchors, model grain,
  relationship paths, custom DMOs, or Data Graph shape.
- Diagnose RAG as an offline chain and an online chain: source, chunk, index,
  retrieve, hydrate, prompt, generate, cite, and enforce access.
- Choose external data architecture before payloads: ingestion, real-time
  ingestion, streaming ingestion, batch ingestion, live query, accelerated
  query, file federation, or hybrid.
- Use the cost and usage sizing contract when a recommendation affects
  ingestion volume, query volume, refresh cadence, RAG indexing, AI processing,
  activation payloads, or multi-environment replay.
- For limits, quotas, connector counts, licensing, billing, and feature
  availability, default to current Data 360 Limits and Guidelines. Follow Data
  Services Billable Usage Types when current docs route there. Treat Customer
  Data Platform limits as legacy unless the user explicitly says CDP/Customer
  Data Platform, the target org is known to use that license, or the answer is a
  labeled comparison.
- Choose the API surface before coding: Connect REST, Apex `ConnectApi`, Data
  360 API / Direct API, SOQL-supported paths, Metadata API, or data kits.
- Promote evidence only when it has official docs or OpenAPI shape, a minimal
  payload or command, readback proof, caveats, and failure modes.
- Cost is a design gate: query only required fields, filter early, ingest
  selectively, aggregate before ingest when raw detail is unnecessary, and keep
  test data small.
- Use `datacloud-mcp-query` only as a retrieve-phase accelerator for Query SQL,
  list tables, and describe table. Use `data360` MCP or direct REST for broader
  Connect API operations.

## Output Contract

Prefer answers with this shape:

```text
Preflight
Recommendation
Source path: documented | tested | inferred
Payload/command/query
Validation readback
Caveats
Next proof step
```

If the task is customer-facing, keep the answer sharp and avoid internal lab
details unless they directly support the recommendation.
