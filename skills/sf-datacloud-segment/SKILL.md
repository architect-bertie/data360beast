---
name: sf-datacloud-segment
description: >
  Salesforce Data 360 Segment phase for calculated insights, segments, member
  counts, and DBT segment troubleshooting. TRIGGER when: the user creates,
  debugs, publishes, or validates segments or calculated insights.
license: MIT
metadata:
  version: "2.0.0"
  author: "Codex"
---

# sf-datacloud-segment

Use this skill for the **CI and segment lifecycle plane**.

Beast references:
- Public operating model: [docs/operating-model.md](../../docs/operating-model.md)
- Developer Guide index: [docs/data360/developer/index.md](../../docs/data360/developer/index.md)
- Proof ledger: [docs/proof-ledger.md](../../docs/proof-ledger.md)
- Public LLM map: [docs/llms.txt](../../docs/llms.txt)
- Limits source precedence: [docs/data360/limits-source-precedence.md](../../docs/data360/limits-source-precedence.md)
- For exact Salesforce behavior, fetch official Help/Developer docs on demand with `sf-docs`.
- For endpoint shape, use OpenAPI from the official spec or the user-supplied Swagger before writing payloads.

## Default surfaces

- `GET/POST/PATCH/DELETE /ssot/calculated-insights`
- `POST /ssot/calculated-insights/:apiName/actions/run`
- `GET/POST/PATCH/DELETE /ssot/segments`
- `POST /ssot/segments/:segmentId/actions/publish`
- `POST /ssot/segments/:segmentApiName/actions/count`
- segment members / included count retrieval
- Apex `ConnectApi.CdpSegment.createSegment`

## Rules

- For calculated insight SQL authoring, use [sf-datacloud-calculated-insights](../sf-datacloud-calculated-insights/SKILL.md) first.
- Separate **discovery** from **activation**:
  - discovery can use published CIs and aggregate query logic
  - activation should rebuild a DMO-native DBT segment definition
- Do not assume a query-safe join is segment-safe.
- Query-plane proof is not segment-plane proof. A segment needs its own create/readback, status, count, and publish validation.
- Prefer segment-safe DMOs with a single unique primary key. Visual Segment Canvas does not reliably handle composite-key joins because relationships support one field.
- Design segment criteria at the same grain as Segment On. Avoid joins that multiply members.
- When using calculated insights in segmentation, the segment-on profile DMO primary key must be a CI dimension and the segmented DMO must be joined in the CI SQL.
- Do not use streaming insights in segments.
- Dynamic segments do not persist Segment Membership DMOs and cannot be scheduled or published through UI or Connect API.
- Real-time segments require Segment ID and Timestamp fields in the real-time data graph and do not support exclusion criteria, nested batch segments, counts, or manual publish.
- Rapid publish uses only the last 7 days of engagement data and publishes to Marketing Cloud only.
- For non-aggregatable CI metrics, preserve required dimensions and understand supported filters.
- Do not assume a create response means the segment is healthy; verify the resulting `MarketSegment`.
- If consent only exists on a DLO path, do not promise consent-filtered segment creation.
- In governed orgs, segment creation enforces object and field access but does not enforce RLS. Validate created member counts against the intended DMO-native criteria.
- Confirm the creator has access to the Segment On DMO and primary key before debugging DBT or count mismatches.
- Activations displayed from segment records can be filtered by access to dependent objects.
- When query counts and segment counts diverge, debug DMO grain, relationships, Segment On primary key, compiler constraints, governance, and refresh timing before rewriting working query SQL.
- Prefer absolute timestamp literals in generated DBT segment SQL.
- Separate audience discovery, segment definition, publish, activation, and downstream campaign/action steps.
- Segmentation and activation consume credits. When proposing or testing
  segments, keep test audiences small, filter early, and avoid publishing or
  counting broad exploratory segments unless the user accepts the usage impact.

## Recommended verification

1. CI published and queryable
2. CI dimensions include the segment-on profile primary key when the CI must appear in segment rules
3. segment create returned a real id
4. resulting `MarketSegment.SegmentStatus` is healthy
5. `MarketSegment.PublishStatus` and publish history are checked when publishing is part of the task
6. member or included counts are nonzero when expected
7. governance policy effects are tested with the target non-admin user

## Reusable Verification Patterns

Default habit:
- run an alignment probe when a proposal count and created segment count disagree
- query `MarketSegment` status before declaring the segment healthy
- run governance checks when proposal counts, query counts, and created segment counts disagree

## Doc-Synced Notes

<!-- SF_DOC_SYNC_START:limits-segmentation -->
### Segmentation limit gate

_Auto-synced from the local sf-docs cached Salesforce Help export (official docs only).

**Sources (sf-docs cached Help):**
- data.c360_a_limits_and_guidelines.htm (2026-05-11T20:20:31.057Z) — Data 360 Limits and Guidelines

**Notes:**
- Treat the captured Limits and Guidelines page as a required source before making durable guidance for this phase.
- Separate soft guidelines from hard limits, and call out when a limit can require an Account Executive request or org-specific validation.
- Before recommending segment shape, publish cadence, counts, or DBT segment strategy, check the segmentation limit family and publish-related Help pages.
- Treat count success, publish success, and activation pickup as separate proof targets.
- Relevant limit families currently captured include: General Guidelines and Limits, Activation Guidelines and Limits, Calculated Insights Guidelines and Limits, Code Extension Guidelines and Limits (Beta), Data Actions Guidelines and Limits, Data Explorer Guidelines and Limits, Data Federation Guidelines and Limits, Data Graphs Guidelines and Limits, Data Ingestion Guidelines and Limits, Data Model Object Guidelines and Limits, Data Shares Guidelines and Limits, Data Transforms Guidelines and Limits.
<!-- SF_DOC_SYNC_END:limits-segmentation -->
