# Data 360 Project Gotchas

These are live lessons from building a real Agentforce + Data 360 implementation.

## Query plane vs segment compiler

A query can succeed through `query-sql` or `ConnectApi.CdpQuery.queryAnsiSqlV2` and still fail when reused in DBT segment creation. Treat query validation and segment validation as separate gates.

## Calculated Insights are great for discovery, not for DBT segment SQL

Using CI tables in discovery is excellent for aggregate proposals. But DBT segment creation should be rebuilt from DMO-native logic, not by pushing CI SQL directly into `/ssot/segments` or `ConnectApi.CdpSegment.createSegment`.

## Consent on a DLO does not equal segment-safe consent

If the consent signal only exists on a `__dll` shape like `Contact_Home__dll`, the DBT compiler may reject it. If you need consent enforced in the segment itself, harmonize the signal into a DMO-backed path first.

## Use absolute timestamp literals in generated segment SQL

Relative time expressions can behave differently between query execution and DBT segment compilation. For generated DBT segment SQL, building an explicit timestamp literal in code is much safer.

## Verify the resulting MarketSegment, not only the create response

The initial segment creation response can still be followed by `ERROR` status later. Check the created `MarketSegment` record for:

- `SegmentStatus`
- `LastSegmentStatusErrorCode`
- `LastSegmentStatusErrorDetails`

## Data Graph is best used as enrichment context

Use Data Graph output to improve narrative quality, aggregate counts, and marketer guidance. Do not silently convert graph-only context into activation criteria unless it is also represented in segment-safe schema.

## Query editor null syntax

For PostgreSQL-style query editors:

```sql
WHERE "FieldName" IS NOT NULL
```

Do not use invalid variants like `IS <>`.
