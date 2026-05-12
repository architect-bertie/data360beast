---
name: sf-datacloud-prepare
description: >
  Salesforce Data 360 Prepare phase for streams, DLOs, transforms, and document processing.
  TRIGGER when: the user creates or troubleshoots data streams, data lake objects,
  transforms, unstructured ingest, search index prep, or Document AI ingestion.
license: MIT
metadata:
  version: "2.0.0"
  author: "architect-bertie"
---

# sf-datacloud-prepare

Use this skill for the **ingestion and lake-prep plane**.

Beast references:
- Public operating model: [docs/operating-model.md](../../docs/operating-model.md)
- Interoperability decision map: [docs/data360/interoperability-decision-map.md](../../docs/data360/interoperability-decision-map.md)
- RAG/search-index playbook: [docs/data360/rag-search-index-retriever-playbook.md](../../docs/data360/rag-search-index-retriever-playbook.md)
- Limits source precedence: [docs/data360/limits-source-precedence.md](../../docs/data360/limits-source-precedence.md)
- Developer Guide index: [docs/data360/developer/index.md](../../docs/data360/developer/index.md)
- Proof ledger: [docs/proof-ledger.md](../../docs/proof-ledger.md)
- Public LLM map: [docs/llms.txt](../../docs/llms.txt)
- For exact Salesforce behavior, fetch official Help/Developer docs on demand with `sf-docs`.
- For endpoint shape, use OpenAPI from the official spec or the user-supplied Swagger before writing payloads.

## Prefer these Connect API families

- `GET/POST/PATCH/DELETE /ssot/data-streams`
- `POST /ssot/data-streams/:recordIdOrDeveloperName/actions/run`
- `GET/POST/PATCH/DELETE /ssot/data-lake-objects`
- `GET/POST/PUT/DELETE /ssot/data-transforms`
- `POST /ssot/data-transforms/:id/actions/run`
- `GET/POST/PATCH/DELETE /ssot/document-processing/configurations`

## Rules

- Do not jump to harmonization until stream and DLO health is clear.
- Keep dataset category decisions explicit: profile, engagement, or supporting data.
- For data streams, lock in primary key, category, event time, record modified field, refresh mode, and data space before deploy.
- Data stream formula fields use the Data 360 formula library, not Data 360 Query SQL. Use uppercase function names (`IF`, `AND`, `OR`, `UPPER`, `TRIM`, `COALESCE`), `sourceField['Header Label']` with exact case-sensitive raw header labels, `==` and `!=` for equality checks, and array-style `COALESCE([sourceField['Field'], ''])`.
- For boolean formula return types, return boolean literals (`true`, `false`) unless the target field is text. Example: `IF(UPPER(TRIM(COALESCE([sourceField['MailingCountry'], '']))) != 'US', true, false)`.
- Treat DLO work as lakehouse-prep work: validate stream status, DLO field shape, row count, null rate, and transform output before debugging downstream DMO, segment, or activation behavior.
- For performance or refresh problems, separate source extraction, DLO write, transform execution, and DMO mapping. A downstream query result is not proof that the upstream processing job is healthy.
- Choose ingestion mode from business need: real-time for sub-second operational value, streaming for minute-level incremental freshness, and batch for historical, low-velocity, or cost-sensitive data.
- Use selective fields, filters, incremental refresh, CDC, micro-batching, and source-side aggregation to control storage, network I/O, and processing cost.
- For ingestion limits, including CRM-org counts, CRM custom objects, stream
  counts, file sizes, and usage categories, use current Data 360 Limits and
  Guidelines first. Use Customer Data Platform limits only for explicit legacy
  CDP orgs or labeled comparison.
- The developer guide frames ingestion as bulk, recurring bulk, and small-batch
  streaming patterns. Match that pattern to the source and workload before
  creating DLOs or transforms.
- For web and mobile events, consider Salesforce Interactions SDK and Engagement
  Mobile SDK ingestion paths before inventing custom capture code.
- When raw detail is not required downstream, aggregate before ingestion to
  reduce storage and processing consumption.
- For engagement streams, event time is mandatory and must describe when the engagement occurred.
- Data streams feed DLOs. If a DLO is associated with a data stream, update fields through the stream rather than directly from the DLO tab.
- CRM data streams perform incremental refreshes every 10 minutes after full refresh; full refresh cadence is configurable.
- Do not modify Marketing Cloud Engagement data stream schedules after creation because supporting automations are dynamically managed.
- DMO-sourced batch transforms are restricted to a data space; DLO-sourced batch transforms are not associated with a data space.
- Use lookup when grain must stay one row per left input row; joins can multiply rows when multiple matches exist.
- Refresh mode decisions can be hard to change later; record the reason for incremental, partial, or full refresh.
- Validate transforms with source row count, output row count, null rate, duplicate rate, and schema drift checks.
- Apply or propagate governance tags to DLOs, DMO outputs, transform outputs, and sensitive fields before downstream consumption.
- Do not mask primary keys, foreign keys, fully qualified keys, event-time fields, or required join/filter fields without validating every query, transform, graph, segment, and activation path.
- Transform preview can enforce RLS differently from runtime execution; compare preview counts with run output before declaring a data issue.
- For unstructured data, curate content before indexing: focused documents,
  headings, explicit Q&A structure, detailed examples, media descriptions,
  split/structured tables, and freshness governance improve retrieval more than
  downstream prompt tweaks.
- Do not treat CSV, JSON, or XML as unstructured merely because it arrived as a
  file. Load structured fields into DLO/DMO shape first, then chunk only
  sentence-level long text fields when RAG is needed.
- For unstructured data, hand off chunking/search index design to [sf-datacloud-unstructured-retrieval](../sf-datacloud-unstructured-retrieval/SKILL.md).
- Use stream reruns for ingestion validation before blaming downstream mappings.
- Prefer programmatic payloads over UI click-memory when the user wants repeatable setup.

## Production Gates

1. connection healthy
2. schema uploaded or discovered
3. stream deployed in correct data space
4. DLO record count matches source expectation
5. DMO mapping path identified
6. transform run completes and output is queryable
7. object and field tags/classifications are applied or propagated
8. target users can view only the intended DLO/DMO/transform output
9. monitoring path exists for failures and late data

## Handoff

When stream output looks right, move to [sf-datacloud-harmonize](../sf-datacloud-harmonize/SKILL.md).
For data spaces, tags, masking, and access policies, use [sf-datacloud-governance](../sf-datacloud-governance/SKILL.md).

## Doc-Synced Notes

<!-- SF_DOC_SYNC_START:limits-data-ingestion -->
### Data ingestion and transform limit gate

_Auto-synced from the local sf-docs cached Salesforce Help export (official docs only).

**Sources (sf-docs cached Help):**
- data.c360_a_limits_and_guidelines.htm (2026-05-11T20:20:31.057Z) — Data 360 Limits and Guidelines

**Notes:**
- Treat the captured Limits and Guidelines page as a required source before making durable guidance for this phase.
- Prioritize current Data 360 limits over legacy Customer Data Platform limits;
  use CDP limits only for explicit legacy scope or labeled comparison.
- If the current limit row points to Data Services Billable Usage Types for
  Data 360, label the number as license/contract-sensitive until proven in the
  target org or Digital Wallet.
- Separate soft guidelines from hard limits, and call out when a limit can require an Account Executive request or org-specific validation.
- Before recommending stream count, refresh cadence, file volume, transform shape, or retry behavior, check the captured ingestion and transform limit families.
- Prefer smaller probes and explicit readback when a design can affect metered ingestion, processing, or storage.
- Relevant limit families currently captured include: General Guidelines and Limits, Activation Guidelines and Limits, Calculated Insights Guidelines and Limits, Code Extension Guidelines and Limits (Beta), Data Actions Guidelines and Limits, Data Explorer Guidelines and Limits, Data Federation Guidelines and Limits, Data Graphs Guidelines and Limits, Data Ingestion Guidelines and Limits, Data Model Object Guidelines and Limits, Data Shares Guidelines and Limits, Data Transforms Guidelines and Limits.
<!-- SF_DOC_SYNC_END:limits-data-ingestion -->
