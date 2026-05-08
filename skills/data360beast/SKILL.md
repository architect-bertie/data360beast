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
