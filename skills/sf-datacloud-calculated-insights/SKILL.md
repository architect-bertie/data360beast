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
  author: "Codex"
  validated: "Built from official Salesforce Help, OpenAPI/Data 360 Connect API surfaces, and live project CI/segment work"
---

# sf-datacloud-calculated-insights

Use this skill for the **Calculated and Streaming Insight SQL plane**.

Beast references:
- Public operating model: [docs/operating-model.md](../../docs/operating-model.md)
- Public API cookbook: [docs/api-cookbook.md](../../docs/api-cookbook.md)
- Public LLM map: [docs/llms.txt](../../docs/llms.txt)
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
