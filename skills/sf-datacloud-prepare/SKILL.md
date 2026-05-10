---
name: sf-datacloud-prepare
description: >
  Salesforce Data 360 Prepare phase for streams, DLOs, transforms, and document processing.
  TRIGGER when: the user creates or troubleshoots data streams, data lake objects,
  transforms, unstructured ingest, search index prep, or Document AI ingestion.
license: MIT
metadata:
  version: "2.0.0"
  author: "Codex"
---

# sf-datacloud-prepare

Use this skill for the **ingestion and lake-prep plane**.

Beast references:
- Public operating model: [docs/operating-model.md](../../docs/operating-model.md)
- Interoperability decision map: [docs/data360/interoperability-decision-map.md](../../docs/data360/interoperability-decision-map.md)
- Public API cookbook: [docs/api-cookbook.md](../../docs/api-cookbook.md)
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
