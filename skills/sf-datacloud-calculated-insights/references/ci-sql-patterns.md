# Calculated Insight SQL Patterns

## Official Rules Snapshot

- Create with SQL requires the Data Cloud Architect permission set, a data space, SQL authoring, Check Syntax, activation, and a schedule or manual publish.
- CI SQL has this shape: `SELECT dimensions, aggregate_measures FROM DMO JOIN ... WHERE row_predicate GROUP BY dimensions`.
- Measures are aggregated quantitative values. Dimensions categorize the measures.
- DMO names are case-sensitive and must match the Object API Name in the target org.
- A CI can have up to 10 dimensions, 50 measures, and 131,021 SQL characters.
- Current Data 360 limits include 300 CIs per tenant, 4 nested CIs, 30 manual runs per CI per 24 hours, and a 2-hour execution ceiling.
- The top-level query must not use `ORDER BY`, top-level `DISTINCT`, nested aggregates, aggregate expressions in `WHERE`, or aggregate/measure aliases in `GROUP BY`.
- `COUNT(*)` is not supported; count a concrete field.
- Currency measures must use `TRY_CONVERT_CURRENCY`.
- Formula fields are row-based ingestion calculations. Segment operators are simple segment-time filters. CIs are for reusable complex and multidimensional metrics.
- Streaming insights use tumbling windows from 1 minute through 24 hours and require `WINDOW.start`, `WINDOW.end`, and `GROUP BY WINDOW(...)`. Segment and activation do not support streaming insights.

## Authoring Algorithm

1. Name the business metric in plain English.
2. Pick the grain. Most marketing CIs should be profile grain or profile x business dimension grain.
3. Resolve real DMO and field names from the org.
4. Probe row counts and joins separately before writing the aggregate.
5. Keep dimensions minimal; dimensions multiply output rows and affect retention, reports, and segments.
6. Make null handling explicit with `COALESCE`, `NULLIF`, and `IS NOT NULL`.
7. Prefer deterministic join keys and avoid accidental fanout. If joining line items to orders to people, verify order-level and line-level counts.
8. Add time windows deliberately. Use rolling windows for living metrics; use fixed timestamp bounds for reproducible tests.
9. Validate, run, query the `__cio`, and compare with independent control queries.

## Segment-Ready Profile Metric

Use this when a segment must filter on a CI metric.

```sql
SELECT
  UnifiedIndividual__dlm.ssot__Id__c AS UnifiedIndividualId__c,
  SUM(ssot__SalesOrder__dlm.ssot__GrandTotalAmount__c) AS RevenueAmount__c,
  COUNT(ssot__SalesOrder__dlm.ssot__Id__c) AS OrderCount__c,
  MAX(ssot__SalesOrder__dlm.ssot__PurchaseOrderDate__c) AS LastPurchaseDate__c
FROM ssot__SalesOrder__dlm
JOIN IndividualIdentityLink__dlm
  ON ssot__SalesOrder__dlm.ssot__SoldToCustomerId__c = IndividualIdentityLink__dlm.SourceRecordId__c
JOIN UnifiedIndividual__dlm
  ON IndividualIdentityLink__dlm.UnifiedRecordId__c = UnifiedIndividual__dlm.ssot__Id__c
WHERE ssot__SalesOrder__dlm.ssot__PurchaseOrderDate__c >= SECOND_SUB(NOW(), 7776000)
GROUP BY UnifiedIndividualId__c
```

Adaptations:
- Use the org's actual order date, order amount, sold-to/customer key, and identity link fields.
- If segmenting on Individual instead of Unified Individual, use the selected profile DMO's primary key as the dimension.
- If currency is multi-currency, wrap the measure with `TRY_CONVERT_CURRENCY`.

## Product or Category Metric

Use profile x product/category grain for reusable personalization and audience filters.

```sql
SELECT
  UnifiedIndividual__dlm.ssot__Id__c AS UnifiedIndividualId__c,
  ssot__GoodsProduct__dlm.ssot__PrimaryProductCategory__c AS ProductCategory__c,
  SUM(ssot__ProductOrderEngagement__dlm.ssot__NetOrderAmount__c) AS CategoryRevenue__c,
  COUNT(ssot__SalesOrderProductEngagement__dlm.ssot__Id__c) AS LineCount__c
FROM UnifiedIndividual__dlm
JOIN IndividualIdentityLink__dlm
  ON UnifiedIndividual__dlm.ssot__Id__c = IndividualIdentityLink__dlm.UnifiedRecordId__c
JOIN ssot__ProductOrderEngagement__dlm
  ON IndividualIdentityLink__dlm.SourceRecordId__c = ssot__ProductOrderEngagement__dlm.ssot__IndividualId__c
JOIN ssot__SalesOrderProductEngagement__dlm
  ON ssot__ProductOrderEngagement__dlm.ssot__Id__c = ssot__SalesOrderProductEngagement__dlm.ssot__ProductOrderEngagementId__c
JOIN ssot__GoodsProduct__dlm
  ON ssot__GoodsProduct__dlm.ssot__Id__c = ssot__SalesOrderProductEngagement__dlm.ssot__ProductId__c
GROUP BY
  UnifiedIndividualId__c,
  ProductCategory__c
```

Adaptations:
- Confirm whether the org uses `ssot__SalesOrder__dlm`, `ssot__ProductOrderEngagement__dlm`, or custom order DMOs.
- Probe fanout by comparing distinct orders, product lines, and unified individuals before trusting revenue sums.

## Engagement Metric

```sql
SELECT
  UnifiedIndividual__dlm.ssot__Id__c AS UnifiedIndividualId__c,
  LOWER(Engagement__dlm.Channel__c) AS Channel__c,
  COUNT(Engagement__dlm.Id__c) AS EngagementCount__c,
  MAX(Engagement__dlm.EventDateTime__c) AS LastEngagementDate__c
FROM Engagement__dlm
JOIN IndividualIdentityLink__dlm
  ON Engagement__dlm.IndividualId__c = IndividualIdentityLink__dlm.SourceRecordId__c
JOIN UnifiedIndividual__dlm
  ON IndividualIdentityLink__dlm.UnifiedRecordId__c = UnifiedIndividual__dlm.ssot__Id__c
WHERE Engagement__dlm.EventDateTime__c >= SECOND_SUB(NOW(), 2592000)
GROUP BY
  UnifiedIndividualId__c,
  Channel__c
```

Adaptations:
- Replace the generic engagement DMO with the actual Email, Web, Mobile, Personalization, or custom engagement object.
- Keep channel-specific CIs separate if one cross-channel grain would exceed 10 dimensions or create sparse output.

## Streaming Insight Metric

Use this for near-real-time orchestration or data actions on streaming engagement data.

```sql
SELECT
  WebEngagement__dlm.IndividualId__c AS IndividualId__c,
  WebEngagement__dlm.PageCategory__c AS PageCategory__c,
  COUNT(WebEngagement__dlm.Id__c) AS EventCount__c,
  WINDOW.start AS WindowStart__c,
  WINDOW.end AS WindowEnd__c
FROM WebEngagement__dlm
WHERE WebEngagement__dlm.EventType__c = 'PageView'
GROUP BY
  IndividualId__c,
  PageCategory__c,
  WINDOW(WebEngagement__dlm.EventDateTime__c, '5MINUTES')
```

Adaptations:
- Replace `WebEngagement__dlm` with the real streaming engagement DMO.
- Validate the event time field and supported window duration.
- Use streaming insights for data actions and orchestration, not segmentation.
- Keep the metric small and operational; high-cardinality streaming outputs become noisy quickly.

## RFM and Rank Metrics

Rank, `NTILE`, percentile, and `CASE` over aggregates are powerful but non-aggregatable. Use them when the downstream consumer will filter at the exact dimension grain.

```sql
SELECT
  base.UnifiedIndividualId__c AS UnifiedIndividualId__c,
  NTILE(4) OVER (ORDER BY base.LastPurchaseDate__c DESC) AS RecencyQuartile__c,
  NTILE(4) OVER (ORDER BY base.OrderCount__c ASC) AS FrequencyQuartile__c,
  NTILE(4) OVER (ORDER BY base.RevenueAmount__c ASC) AS MonetaryQuartile__c
FROM (
  SELECT
    UnifiedIndividual__dlm.ssot__Id__c AS UnifiedIndividualId__c,
    MAX(ssot__SalesOrder__dlm.ssot__PurchaseOrderDate__c) AS LastPurchaseDate__c,
    COUNT(ssot__SalesOrder__dlm.ssot__Id__c) AS OrderCount__c,
    SUM(ssot__SalesOrder__dlm.ssot__GrandTotalAmount__c) AS RevenueAmount__c
  FROM ssot__SalesOrder__dlm
  JOIN IndividualIdentityLink__dlm
    ON ssot__SalesOrder__dlm.ssot__SoldToCustomerId__c = IndividualIdentityLink__dlm.SourceRecordId__c
  JOIN UnifiedIndividual__dlm
    ON IndividualIdentityLink__dlm.UnifiedRecordId__c = UnifiedIndividual__dlm.ssot__Id__c
  GROUP BY UnifiedIndividual__dlm.ssot__Id__c
) base
GROUP BY
  base.UnifiedIndividualId__c,
  base.LastPurchaseDate__c,
  base.OrderCount__c,
  base.RevenueAmount__c
```

Adaptations:
- Validate nested query support in the target CI authoring surface.
- Confirm non-aggregatable behavior in segments and reports before promising rollups.

## Identity Resolution Data Quality CIs

Use these after ingestion and before identity-resolution rulesets.

Patterns:
- Summary by source: group by Individual data source and source object; count distinct individuals, emails, phones, addresses, party identifiers.
- Contact points per individual: group by source Individual ID; count distinct contact point IDs and devices.
- Contributing contact points / overgrouping: group by repeated email, phone, address, or party identification values; count distinct parties and occurrences.
- Consolidation rate: compare source profile counts to unified profile counts by source or match key.
- Outlier unified profiles: group by unified profile and count source records/contact points to find suspiciously large profiles.

Adaptations:
- Standard SQL examples must be rewritten for the org's mapped contact point DMOs and identity link fields.
- Use `APPROX_COUNT_DISTINCT` for scalable diagnostics, but remember that it is non-aggregatable.
- Do not surface raw email, phone, address, or individual IDs to an end-user agent unless the use case and permissions explicitly allow it.

## Personalization Standard CIs

Patterns:
- Top sellers: product ID dimension plus total ordered quantity measure.
- Lifetime value by brand/category: unified individual, brand, and category dimensions plus net order amount sum.
- Co-bought: self-join order line products on order ID, exclude identical product pairs, count/sum co-occurrence.
- Co-browsed: self-join browse events by session/visitor/content context, exclude identical content pairs, count co-occurrence.

Adaptations:
- These depend on Personalization and item data graph expectations. Confirm required CI API names, dimensions, and field names for the consuming feature.
- Use default data space `ssot__` names only when the org actually uses the default data space. Non-default data spaces can require a different prefix.

## Validation Checklist

- The data space is correct and accessible.
- Every DMO and field exists with exact casing.
- Join probes show expected cardinality and no accidental fanout.
- The query has at least one measure and no more than 10 dimensions / 50 measures.
- Static guard returns no blockers.
- Query preview returns expected rows and plausible metric ranges.
- Check Syntax passes.
- CI create/update/activate succeeds.
- Manual run or schedule run completes.
- `GET /ssot/insight/metadata/:ciName` or equivalent metadata confirms dimensions/measures.
- Querying the materialized insight returns expected rows.
- Any segment/report/Data Graph consumer can see the metric at the intended grain.
- Streaming insight output is tested through its intended data action or automation path.
