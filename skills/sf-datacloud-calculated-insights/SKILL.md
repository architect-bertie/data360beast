---
name: sf-datacloud-calculated-insights
description: >
  Salesforce Data 360 Calculated Insights and Streaming Insights SQL authoring,
  validation, lifecycle, and troubleshooting. TRIGGER when: the user creates,
  reviews, debugs, or deploys calculated/streaming insights, writes insight SQL,
  adapts standard examples to an org data model, validates measures/dimensions,
  or needs low-failure Data 360 insight formulas.
license: MIT
metadata:
  version: "1.0.0"
  author: "architect-bertie"
  validated: "Built from official Salesforce Help, OpenAPI/Data 360 Connect API surfaces, and live project CI/segment work"
---

# sf-datacloud-calculated-insights

Use this skill for the **Calculated and Streaming Insight SQL plane**.

Beast references:
- Beast preflight: [docs/beast-preflight.md](../../docs/beast-preflight.md)
- Phase proof matrix: [docs/phase-proof-matrix.json](../../docs/phase-proof-matrix.json)
- Public operating model: [docs/operating-model.md](../../docs/operating-model.md)
- Proof ledger: [docs/proof-ledger.md](../../docs/proof-ledger.md)
- Public LLM map: [docs/llms.txt](../../docs/llms.txt)
- Limits source precedence: [docs/data360/limits-source-precedence.md](../../docs/data360/limits-source-precedence.md)
- For exact Salesforce behavior, fetch official Help/Developer docs on demand with `sf-docs`.
- For endpoint shape, use OpenAPI from the official spec or the user-supplied Swagger before writing payloads.

## Source Priority

1. Actual org metadata and sample data.
2. Official Salesforce Help and developer docs.
3. Data360 Beast OpenAPI catalog and official Data 360 Connect API surfaces.
4. Archived Salesforce Marketing Cloud CI example repo and reputable field notes.

Detailed authoring notes: [references/ci-sql-patterns.md](references/ci-sql-patterns.md)

Static guard script:

```bash
python3 skills/sf-datacloud-calculated-insights/scripts/ci_sql_guard.py path/to/ci.sql
```

The guard is advisory. It does not replace Data 360 Check Syntax, API create/update validation, or a published `__cio` query.

## When to Choose a CI

Use a calculated insight when the user needs reusable multidimensional metrics, complex joins, multiple DMOs, RFM/CLV/propensity-style features, identity-resolution data quality metrics, personalization item metrics, or metrics reused across segmentation, activation, BI, or Data Graphs.

Use a streaming insight when the user needs near-real-time time-series aggregation on streaming engagement data for orchestration or data actions. Streaming insights require tumbling windows, `WINDOW.start`, `WINDOW.end`, and a `GROUP BY WINDOW(eventTimeField, '<duration>')`; segment and activation do not support streaming insights.

Use a real-time insight when the metric must be evaluated in milliseconds against a real-time data graph for personalization logic.

Do not use a CI for a simple row-based normalization that belongs in ingestion formulas, or for a one-off simple segment filter that segmentation operators can handle cleanly.

## Org-Adapted Workflow

1. Discover the data space and available objects.
2. Resolve exact DMO names and field names from the org. CI DMO names are case-sensitive.
3. Confirm source cardinality with small SQL probes before writing the final aggregate.
4. Pick the output grain first:
   - profile grain: one row per Individual, Unified Individual, Account, or Unified Account
   - product/item grain: one row per product/article/content item
   - profile x dimension grain: profile plus product/category/channel/time
   - data quality grain: source, contact point, source record, or unified profile
5. Define dimensions and measures explicitly. Every non-aggregated SELECT expression is a dimension.
6. Keep the CI within platform limits: maximum 10 dimensions, 50 measures, and 131,021 SQL characters.
7. Validate static SQL rules, then execute a preview query, then run Data 360 Check Syntax or the CI API lifecycle.
8. Run or publish the insight, query the materialized `__cio`, and verify row counts, null rates, and metric ranges.
9. For troubleshooting, keep preview query, CI save, CI run/materialization, and `__cio` retrieval separate. Each step can fail or drift for a different reason.

## CI SQL Rules That Matter

- Include at least one aggregate measure.
- Do not use `COUNT(*)`; count a concrete field.
- Do not use top-level `SELECT DISTINCT`.
- Do not include a top-level `ORDER BY`.
- Do not put aggregate expressions, dimension aliases, or measure aliases in `WHERE`.
- Do not nest aggregate functions.
- Do not put aggregate functions or measure aliases in `GROUP BY`.
- Use `TRY_CONVERT_CURRENCY` for currency measures.
- Use `NOW`, `SECOND_ADD`, and `SECOND_SUB` for rolling time windows when the metric must refresh relative to processing time.
- Treat `RANK`, `NTILE`, `CASE` over aggregates, `APPROX_COUNT_DISTINCT`, percentile, and similar functions as non-aggregatable unless verified otherwise in the target UI/API metadata.
- For non-aggregatable measures, preserve all required dimensions when querying, reporting, or segmenting.
- For segment visibility, include the Segment On profile DMO in the query and include that DMO primary key as a dimension.
- For governed orgs, validate creator access to every referenced DMO/CIO/field during CI save, not only query preview.
- RLS is not enforced during CI creation; do not represent CI output as user-row-filtered unless the consuming query/report enforces it.
- Tags can propagate from source DMO fields to CIO dimensions only when dimensions exactly match; formula-derived dimensions may need manual tagging.
- FLS on CI dimensions can change aggregatable metric rollups and restrict non-aggregatable metrics.
- Streaming insights are not calculated insights for segmentation; do not substitute one for the other.
- Streaming insights can drive data actions, but segment and activation do not support them.
- For streaming insights, only use supported streaming aggregate functions and window durations. Validate event time and late-arriving data behavior.
- Verify lifecycle status with `MktCalculatedInsight.LastRunStatus`, status dates, and error codes when available.
- Query preview success is not proof of materialized CIO health. Always read the output object when a segment, activation, report, or agent depends on the CI.
- For agentic use, write metric descriptions with grain, formula, dimensions, time window, and allowed user-facing interpretation.

## Standard Patterns

Read [references/ci-sql-patterns.md](references/ci-sql-patterns.md) for:

- customer revenue / LTV
- purchase count and average order value
- RFM and rank metrics
- engagement counts
- streaming insight tumbling-window examples
- personalization top sellers, co-bought, co-browsed, and LTV by brand/category
- identity-resolution data quality CIs
- segment-ready CI design

Adapt every pattern to the real org. Standard examples often assume specific SSOT DMOs and relationship fields that can differ by data stream, data space, or mapping.

## Failure-Risk Self Evaluation

Before presenting a CI as ready, assign one of these:

- **High confidence**: org metadata resolved, source fields exist, query preview passed, Data 360 CI syntax/create passed, insight was run/published, and `__cio` output was queried.
- **Medium confidence**: org metadata resolved and query preview passed, but CI syntax/create/run has not been performed.
- **Low confidence**: generic SQL adapted from docs/examples without validating against the target org.

Never claim low probability of failure unless confidence is High. If confidence is Medium or Low, name the exact unverified gate.

## Output Format

When producing CI work, report:

1. intended grain
2. dimensions
3. measures
4. SQL
5. org-adaptation assumptions
6. validation commands or API calls
7. confidence rating and remaining failure risks

## Governance Handoff

Use [sf-datacloud-governance](../sf-datacloud-governance/SKILL.md) when CI validation fails because fields are visible in metadata but fail at save/query time, when CIO tags must drive policies, or when masked/restricted dimensions change metric behavior.

## Doc-Synced Notes

<!-- SF_DOC_SYNC_START:limits-insights -->
### Calculated and streaming insight limit gate

_Auto-synced from the local sf-docs cached Salesforce Help export (official docs only)._

**Sources (sf-docs cached Help):**
- data.c360_a_limits_and_guidelines.htm — Data 360 Limits and Guidelines | Salesforce Help

**Source fingerprint:** `1ce0aa69b0b275b02c26170b`

**Notes:**
- Treat the captured Limits and Guidelines page as a required source before making durable guidance for this phase.
- Separate soft guidelines from hard limits, and call out when a limit can require an Account Executive request or org-specific validation.
- Before promoting CI SQL patterns, check calculated-insight, real-time insight, and streaming-insight limit families.
- Separate SQL validity from job/runtime proof; limits can apply after a query compiles.
- Relevant limit families currently captured include: General Guidelines and Limits, Activation Guidelines and Limits, AI Models (formerly Einstein Studio) Guidelines and Limits, Calculated Insights Guidelines and Limits, Code Extension Guidelines and Limits, Data Actions Guidelines and Limits, Data Explorer Guidelines and Limits, Data Federation Guidelines and Limits, Data Graphs Guidelines and Limits, Data Ingestion Guidelines and Limits, Data Model Object Guidelines and Limits, Data Shares Guidelines and Limits.

<!-- SF_DOC_SYNC_END:limits-insights -->

<!-- SF_DOC_SYNC_START:insights-authoring -->
### Insights Authoring (Calculated and Streaming)

_Distilled from official Salesforce sources only._

**Sources:**
- data.c360_a_insights.htm — Enhance Data with Insights overview
- data.c360_a_calculated_insights.htm — Calculated Insights
- data.c360_a_streaming_insights.htm — Streaming Insights
- data.c360_a_create_streaming_insight.htm — Create a Streaming Insight
- developer.salesforce.com/docs/data/data-cloud-query-guide/references/dc-sql-reference/aggregate.html — Data 360 SQL Aggregate Reference
- developer.salesforce.com/docs/data/data-cloud-query-guide/references/data-cloud-query-api-reference/c360a-api-ci-call-overview.html — Calculated Insights API

**Calculated vs Streaming Insights (different runtimes):**

| Aspect | Calculated Insight (CI) | Streaming Insight |
|---|---|---|
| Runtime | Batch on schedule | Continuous on event arrival |
| Source | DMOs (any category) | Streaming DMOs (engagement only) |
| Output | CIO (Calculated Insight Object), persisted | Time-series aggregates, fed to Data Actions |
| Latency | Hours | Sub-second to seconds |
| Use cases | Customer lifetime value, RFM scoring, rolling 90-day metrics | Fraud signals, real-time engagement scoring, threshold alerts |
| Segment usage | Yes (preferred for stable metrics) | No — use for orchestration, not segments |
| Dashboards | Yes | No (event flow only) |

**SQL structure (both kinds use the same shape):**
```sql
SELECT <Dimensions>, <Aggregation_Measures>
FROM <Data Model Object>
JOIN [Inner | Left | Right | Full] <Data Model Object>
WHERE <predicate>
GROUP BY <Dimensions>
```

**Authoring options:**
- **Visual (drag-and-drop) Builder** — generates SQL behind the scenes;
  good for analysts without SQL expertise.
- **SQL editor** — direct authoring; required for advanced patterns
  (joins, complex predicates, window functions where supported).

**Dimensions vs Measures:**
- **Dimensions** are the grouping fields (categorical attributes).
  Examples: Unified Individual ID, Region, Product Category, Date.
  At least one dimension is required; the segment-on profile primary
  key must be a dimension if the CI participates in segmentation.
- **Measures** are aggregated metrics computed across the grouping.
  Examples: `COUNT(orders)`, `SUM(amount)`, `AVG(score)`,
  `MAX(last_purchase_date)`.

**Supported aggregate functions:**
| Family | Functions |
|---|---|
| Counts | COUNT, COUNT_DISTINCT |
| Numeric | SUM, AVG, MIN, MAX |
| Statistical | STDDEV, VARIANCE, CORR, COVAR |
| Boolean/Bitwise | BIT_AND, BIT_OR, BOOL_AND, BOOL_OR |

**Streaming Insights specifics:**
- Author via Data Actions tab → New Streaming Insight (or via Insights
  Builder).
- SQL expression interface includes pickers for: data model fields,
  previously created insights, functions (Aggregation, Datetime, Other).
- Cannot be created from streaming profile data — only engagement DMOs.
- Outputs feed Data Actions for downstream orchestration (Platform Event,
  webhook, MC Engagement).
- Real-time ingestion: ~95% of events complete end-to-end within ~500ms
  under typical load (Web SDK, Mobile SDK, Server-to-Server).

**Calculated Insights specifics:**
- Created via the Calculated Insights tab → New.
- Schedule: hourly, daily, weekly, or manual run.
- Output stored in CIO; can be queried via Query Editor, Calculated
  Insights API, or used in segments and dashboards.
- API row limit: max 4,999 rows returned per query call.
- For non-aggregatable CI metrics, preserve required dimensions and
  validate supported filters at the segment plane.

**Best practices:**
- Author CIs over governed DMOs only (not raw DLOs) to inherit
  classification tags.
- Keep CI SQL deterministic — avoid `NOW()` or unbounded windows.
- Use absolute date predicates (`WHERE event_date >= '2025-01-01'`)
  rather than relative for reproducibility.
- For segment-on-CI flows, ensure the profile DMO primary key is a CI
  dimension and the segmented DMO is joined in the CI SQL.
- Don't use streaming insights as segment inputs; use CIs instead.
- Validate CI run status (`MarketCalculatedInsight` object) before
  declaring it healthy.
- Tag CIO outputs explicitly — derived dimensions may not auto-inherit
  source tags.

**Pitfalls:**
- A CI SQL that compiles in Query Editor may fail at run time due to
  governance, schedule conflict, or join cardinality issues.
- Joining DMOs on `ssot__Id__c` alone (without `KQ_Id__c`) can produce
  cross-source duplicates.
- Using a CI in a segment requires the profile DMO primary key to be a
  CI dimension — adding/removing dimensions can break dependent segments.
- Streaming insight aggregation windows are typically short
  (seconds/minutes); long-window aggregation belongs in Calculated
  Insights.
<!-- SF_DOC_SYNC_END:insights-authoring -->
