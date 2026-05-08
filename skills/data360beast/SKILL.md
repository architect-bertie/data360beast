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
2. Identify the proof target: docs-only guidance, payload generation, metadata
   discovery, live validation, troubleshooting, or customer explanation.
3. Fetch official Salesforce docs on demand for current setup, limits,
   permissions, and behavior.
4. Use OpenAPI for Connect API method, path, params, body schema, response
   schema, and version requirements.
5. Apply cookbook lessons for known working payloads and known gotchas.
6. Validate against the target org when authorized. Prefer returned ID,
   readback, status, count, data space, metadata, and sample query proof.
7. State the confidence level: documented, tested, or inferred.

## Source Hierarchy

1. User-provided target org, files, data space, API version, and business goal.
2. Official Salesforce docs fetched on demand.
3. User-supplied or locally available Data 360 Connect API OpenAPI spec.
4. Data360 Beast public docs and cookbook.
5. Live org validation in an explicitly authorized org.

Do not treat this repository as official Salesforce documentation. Do not
hallucinate endpoint paths, payload fields, limits, permissions, or feature
availability.

## Phase Router

- **Connect**: connectors, connections, connector schema, refresh, ingestion
  setup, connector permissions.
- **Prepare**: data streams, DLOs, transforms, ingestion status, document
  processing.
- **Harmonize**: DMOs, mappings, relationships, identity resolution, data graphs.
- **Govern**: data spaces, tags, classifications, security policies, access.
- **Retrieve**: Query SQL, Query v2, Profile API, metadata discovery.
- **Insight**: calculated insights, streaming insights, SQL validation.
- **Semantic**: C360 semantic models, metrics, dimensions, shared dimensions.
- **AI/Search**: search indexes, retrievers, unstructured retrieval, grounding.
- **Segment**: segment create/read/publish/count, DBT segments, membership proof.
- **Act**: activation targets, activations, data action targets, data actions.
- **Automation**: triggered flows, DataObjectDataChgEvent, activation-triggered
  flows, refresh cadence, monitoring.

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
