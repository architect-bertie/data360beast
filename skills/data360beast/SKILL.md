---
name: data360beast
description: Use this skill for Salesforce Data 360 or Data Cloud architecture, implementation, troubleshooting, Connect API payloads, metadata discovery, query SQL, calculated insights, semantic layer, search, segmentation, activation, data actions, governance, data spaces, and agentic validation workflows.
---

# Data360 Beast

Data360 Beast turns Salesforce Data 360 work into a proof-driven agent loop. Use
it whenever the user is designing, building, validating, or debugging Data 360.

## Operating Loop

1. Classify the phase: connect, prepare, harmonize, govern, retrieve, insight,
   semantic layer, AI/search, segment, act, or automation.
2. Identify the object layer and execution plane when relevant: DSO, DLO, DMO,
   CIO, data graph, query plane, processing job, analytics serving path, or
   orchestration.
3. Identify the proof target: docs-only guidance, payload generation, metadata
   discovery, live validation, troubleshooting, or customer explanation.
4. Fetch official Salesforce docs on demand for current setup, limits,
   permissions, and behavior. If `sf-docs` is unavailable, use
   [docs/mcp-dependencies.md](../../docs/mcp-dependencies.md) for the install
   source or label the answer as docs-unverified.
5. Use OpenAPI for Connect API method, path, params, body schema, response
   schema, and version requirements.
6. Apply cookbook lessons for known working payloads and known gotchas.
7. Validate against the target org when authorized. Prefer returned ID,
   readback, status, count, data space, metadata, and sample query proof.
8. State the confidence level: documented, tested, or inferred.

## Source Hierarchy

1. User-provided target org, files, data space, API version, and business goal.
2. Official Salesforce docs fetched on demand.
3. User-supplied or locally available Data 360 Connect API OpenAPI spec.
4. Data360 Beast public docs and cookbook.
5. Live org validation in an explicitly authorized org.

Companion MCP install paths are documented in
[docs/mcp-dependencies.md](../../docs/mcp-dependencies.md). Do not assume
`sf-docs` or `data360` MCP servers are bundled with the skill pack.

Public-safe official doc indexes:
- [docs/data360/help/index.md](../../docs/data360/help/index.md): 77 indexed Salesforce Help pages.
- [docs/data360/developer/index.md](../../docs/data360/developer/index.md): 23 indexed Salesforce Developer Guide pages.
- [docs/data360/developer/learning-map.md](../../docs/data360/developer/learning-map.md): developer-guide synthesis for routing and skill updates.
- [docs/data360/model-gallery-implementation-map.md](../../docs/data360/model-gallery-implementation-map.md): public Data 360 model-gallery synthesis for DMO anchors, relationship paths, model grain, and implementation traps.
- [docs/data360/rag-search-index-retriever-playbook.md](../../docs/data360/rag-search-index-retriever-playbook.md): public-safe RAG, search-index, chunking, retriever, and troubleshooting playbook distilled from a 45-page Salesforce public-facing best-practices PDF.

Do not treat this repository as official Salesforce documentation. Do not
hallucinate endpoint paths, payload fields, limits, permissions, or feature
availability.

## Phase Router

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

Live-tested cookbook lessons to remember:

- Data stream formula fields use Data 360 formula library syntax, not Query SQL.
- The public Data 360 model gallery is a normalized subject-area map. It should
  guide anchor DMO selection, model grain, and relationship paths, not be treated
  as a flat table list.
- Data 360 RAG should be diagnosed as two loops: offline load/chunk/vectorize/index
  and online query/vectorize/retrieve/hydrate/generate. Failures can occur at
  each boundary.
- Agentforce Data Libraries are the fast path for uploaded files and Knowledge
  Articles. Use manual RAG setup when sources, chunking, embeddings, filters,
  return fields, prompt behavior, or access checks need control.
- For search indexes, long text is indexable content; categories, IDs, booleans,
  publication status, entitlement, account, language, product, and region are
  usually filter, prepend, return, or ranking fields.
- Hybrid search is valuable when exact terms and semantic similarity both matter,
  but it is not a standalone category lookup engine and has cost/latency impact.
- Retriever design is an architecture decision: result count, return fields,
  prefilters, dynamic prefilters, version activation, prompt scope, and
  Flow/Apex fallback all shape answer quality.
- RAG quality metrics separate root causes: context relevance points at retrieval,
  faithfulness points at prompt/generation grounding, and answer relevance is
  the end-user outcome.
- Party/identity, contact point/consent, engagement, commerce, product, service,
  asset, and vertical-domain models reuse common hubs. Preserve those hubs and
  validate relationship cardinality before downstream build.
- Query success does not prove segment, analytics, activation, or transform
  behavior because each surface can use a different validation or execution
  path.
- For external data, choose the pattern before the payload: ingestion,
  real-time ingestion, streaming ingestion, batch ingestion, live query,
  accelerated query, file federation, or hybrid.
- For development work, choose the API surface before coding: Connect REST API
  for platform-integrated apps, Apex ConnectApi for Apex, Data 360 API / Direct
  API for tenant-direct performance, SOQL only for supported platform query
  paths, and Metadata API only for supported metadata movement.
- Data 360 metadata deploys through data kits and supported metadata/package
  types; data kits package definitions, not raw data.
- Cost is a design gate: query only required fields, filter early, ingest
  selectively, aggregate before ingest when raw detail is unnecessary, and keep
  test data small.
- DBT segment create used `includeDbt.models.models[]` successfully.
- DBT segment readback can normalize to `includeDbt.models[]`.
- Approximate segment count can fail when the feature is disabled.
- Segment member retrieval depends on a delta window; status and count readback
  are stronger first proofs.
- Activation target readback by returned ID was reliable in lab testing.

## Output Contract

Prefer answers with this shape:

```text
Recommendation
Source path: documented | tested | inferred
Payload/command/query
Validation readback
Caveats
Next proof step
```

If the task is customer-facing, keep the answer sharp and avoid internal lab
details unless they directly support the recommendation.
