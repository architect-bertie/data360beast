---
name: sf-datacloud-segment
description: >
  Salesforce Data 360 Segment phase for calculated insights, segments, member
  counts, and DBT segment troubleshooting. TRIGGER when: the user creates,
  debugs, publishes, or validates segments or calculated insights.
license: MIT
metadata:
  version: "2.0.0"
  author: "architect-bertie"
---

# sf-datacloud-segment

Use this skill for the **CI and segment lifecycle plane**.

Beast references:
- Beast preflight: [docs/beast-preflight.md](../../docs/beast-preflight.md)
- Phase proof matrix: [docs/phase-proof-matrix.json](../../docs/phase-proof-matrix.json)
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

<!-- SF_DOC_SYNC_START:segment-types-lifecycle -->
### Segment Types and Lifecycle

_Distilled from official Salesforce Help and Trailhead._

**Sources:**
- data.c360_a_segments.htm — Create Segments in Data 360
- data.c360_a_create_a_segment.htm — Create a Standard Segment
- data.c360_a_create_a_dynamic_segment.htm — Create a Dynamic Segment
- data.c360_a_create_a_realtime_segment.htm — Create a Real-Time Segment
- data.c360_a_publish_segment.htm — Publish a Segment

**Standard segments:**
- Default 90-day lookback (configurable up to 2 years depending on org).
- Publish on a schedule (daily, weekly, monthly) or manually on demand.
- Populate `Segment Membership` DMOs; downstream activations consume these.
- For segment-on-CI scenarios, the profile DMO primary key must be a CI
  dimension and the segmented DMO must be joined in the CI SQL.

**Dynamic segments:**
- Query-only; do not persist membership data.
- Use filters with placeholder values that arrive at runtime.
- Triggered through API calls via broadcast flow.
- Cannot be published or scheduled.

**Real-time segments:**
- Complete in milliseconds against a real-time data graph.
- Require Segment ID and Timestamp fields in the real-time data graph.
- Limitations: no exclusion criteria, no nested batch segments, no counts,
  no manual publish.

**Rapid publish segments:**
- 1-hour or 4-hour refresh; uses only the past 7 days of engagement data.
- Maximum 20 rapid segments per org.
- Activates only to Marketing Cloud Engagement and Cloud File Storage.

**Waterfall segments:**
- Process existing segments in priority order for mutually exclusive audiences.
- Support up to 20 segments in the waterfall.

**Lookback and publishing rules:**
- Lookback applies only to standard and dynamic segments, not rapid or
  real-time.
- Adjust lookback for the campaign type: 30 days for flash sales, 90 days
  default, 6-12 months for win-back.
- Publishing is a separate step from segment creation; verify
  `MarketSegment.PublishStatus` and publish history.
- Segmentation and activation consume credits; keep test audiences small.
<!-- SF_DOC_SYNC_END:segment-types-lifecycle -->

<!-- SF_DOC_SYNC_START:segment-creation-canvas -->
### Creating and Configuring Segments (UI and API)

_Distilled from official Salesforce Help, Trailhead, and community guides._

**Sources:**
- data.c360_a_create_a_segment.htm — Create a Standard Segment
- trailhead.salesforce.com/content/learn/projects/explore-data-cloud-core-functionality/build-a-segment-and-report

**Standard segment creation steps:**
1. Segments tab → New.
2. Select **Use a Visual Builder** → **Standard Segment** → Next.
3. Choose **Segment On** object (Unified Individual, Account, or custom DMO).
4. Enter name, API name, description.
5. Set lookback window (default 90 days; filter-container lookback overrides
   if shorter).
6. Configure publish schedule: Standard (every 12 or 24 hours), Rapid
   (1 or 4 hours), or No Refresh (manual only).
7. Build segment logic on the Segment Canvas → Save.
8. Optionally preview count before publishing.

**Segment Canvas anatomy:**
- **Direct attributes** — one-to-one fields on the Segment On object (e.g.,
  postal code, first name).
- **Related attributes** — multi-record relationships (e.g., orders,
  interactions, calculated insights).
- **Containers** — group filters; container-level lookback overrides the
  segment-level lookback when shorter.
- **Filter operators** — vary by data type (date, numeric, text, Boolean).
- **Aggregation** — Count, Sum, Average, Max, Min on related attributes.
- **Logic** — AND / OR to combine filters within or across containers.
- **Container Path** — join path when multiple relationships exist between
  Segment On and the related DMO.

**Einstein Segments (AI-assisted):**
- Describe the audience in natural language; get a suggested segment with
  relevant attributes.
- System blocks biased/unethical descriptions and deselects demographic
  attributes that introduce bias.
- Uses sample data for grounding without exposing PII.

**Segment from a Data Kit:**
- Choose a predefined segment from a data kit.
- Check dependencies (child segments, insights) → edit and schedule.

**Waterfall segment creation:**
- Select **Waterfall Segment** at creation.
- Add up to 20 existing active segments in priority order.
- Result: mutually exclusive audiences (each profile lands in highest-
  priority segment only).
- Cannot nest waterfalls or use Rapid Publish.

**Dynamic segment creation:**
- Select **Dynamic Segment** at creation.
- Define filter criteria with placeholder parameters.
- Runtime invocation via API / broadcast flow supplies actual values.
- No publish schedule; no membership DMO persisted.

**Real-time segment creation:**
- Select **Real-Time Segment** at creation.
- Requires Segment ID and Timestamp fields in real-time data graph config.
- Returns results in milliseconds; cannot use exclusion criteria or manual
  publish.

**Publishing behaviour:**
- Standard publish runs every 12 or 24 hours (configurable).
- When concurrent publish limit is reached, Data Cloud queues and defers
  segments until capacity frees.
- Rapid Publish uses incremental mode (indexes by profile ID).
- Manual publish takes priority over scheduled runs.
- Each publish creates or updates two membership DMOs:
  - **Latest** — current audience after publish.
  - **History** — previous audience within the last 30 days.
- Removed members are dropped at next publish cycle.

**Segment statuses:**
| Status | Meaning |
|---|---|
| Active | Segment is healthy and publishing on schedule |
| Processing | Segment build or publish in progress |
| Recounting | Audience recount running |
| Error | Definition, publish, or downstream failure |
| Inactive | Segment paused or deactivated |

**Publish statuses:** Succeeded, Failed, Skipped, In Progress, Deferred.

**Billing considerations:**
- Segmentation consumes credits based on processing volume and frequency.
- Preview, reduced cadence, narrower lookback, and limited end dates reduce
  consumption.
- Max 9,950 segments per org.

**Troubleshooting checklist:**
1. Segment references too many data objects → simplify rules or use CI.
2. Count mismatches → check DMO grain, relationships, Segment On key,
   identity resolution config, governance.
3. Inactive segments → verify all referenced DMOs and CIs are still published.
4. Date/timezone issues → use absolute timestamp literals; confirm timezone.
5. Publish deferral → reduce concurrent segment publishes or shift schedules.
<!-- SF_DOC_SYNC_END:segment-creation-canvas -->

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
