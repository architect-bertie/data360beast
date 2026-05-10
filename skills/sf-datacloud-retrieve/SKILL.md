---
name: sf-datacloud-retrieve
description: >
  Salesforce Data 360 Retrieve phase for query-sql, queryv2, profile APIs,
  metadata introspection, and query MCP usage. TRIGGER when: the user writes or
  debugs Data 360 SQL, profile retrieval, metadata lookup, or query tooling.
license: MIT
metadata:
  version: "2.0.0"
  author: "Codex"
---

# sf-datacloud-retrieve

Use this skill for the **query and metadata plane**.

Beast references:
- Public operating model: [docs/operating-model.md](../../docs/operating-model.md)
- Interoperability decision map: [docs/data360/interoperability-decision-map.md](../../docs/data360/interoperability-decision-map.md)
- Companion MCP installs: [docs/mcp-dependencies.md](../../docs/mcp-dependencies.md)
- Public API cookbook: [docs/api-cookbook.md](../../docs/api-cookbook.md)
- Public LLM map: [docs/llms.txt](../../docs/llms.txt)
- For exact Salesforce behavior, fetch official Help/Developer docs on demand with `sf-docs`.
- For endpoint shape, use OpenAPI from the official spec or the user-supplied Swagger before writing payloads.

## Default surfaces

- Apex `ConnectApi.CdpQuery.queryAnsiSqlV2`
- `POST /ssot/queryv2`
- `POST /ssot/query-sql`
- `GET /ssot/query-sql/:queryId`
- `GET /ssot/query-sql/:queryId/rows`
- `GET /ssot/metadata`
- `GET /ssot/profile/metadata`
- `GET /ssot/profile/:dataModelName`
- `GET /ssot/insight/metadata`
- `GET /ssot/insight/metadata/:ciName`
- Universal ID Lookup
- Data Graph API retrieval
- Data 360 MCP facade tools: `search`, `payload_examples`, `execute`

## Rules

- For Calculated Insight SQL, use [sf-datacloud-calculated-insights](../sf-datacloud-calculated-insights/SKILL.md) after metadata discovery.
- Query Editor is the official UI surface for SQL exploration, data validation, query testing, and troubleshooting across DLOs, DMOs, CIOs, and data graphs.
- Use Data Explorer to validate object data and formulas; use Profile Explorer to validate unified profile views.
- Data 360 SQL is ANSI/PostgreSQL-like, not SOQL.
- Quote identifiers carefully when the surface requires it.
- Use `IS NOT NULL` for null checks.
- Use metadata/profile discovery before inventing table or field names.
- Prefer query-sql or `ConnectApi.CdpQuery` when you need robust pagination or large result handling.
- Use Data 360 API / Direct API for high-performance tenant-side read paths when available.
- Treat query jobs as asynchronous: submit, poll, page rows, and handle status codes.
- For query performance, reason from the object layer first: DLO, DMO, CIO, or data graph. Selective predicates, date filters, projected fields, join grain, and row counts often matter more than cosmetic SQL changes.
- Treat Trino-like or Iceberg-style query behavior as an inferred mental model only. Use it to choose proof steps such as metadata checks, smaller probes, count queries, and predicate selectivity tests.
- For zero-copy work, distinguish live query, accelerated query, and file federation. Live query is freshness-first and source-compute-dependent; accelerated query trades freshness for repeated-read performance; file federation is read-only and depends on object format, partitioning, pruning, and region/I/O.
- Push predicates and aggregations to the source when using query federation. Avoid unfiltered scans over massive federated datasets.
- Prefer profile endpoints when you need record-centric retrieval instead of ad hoc SQL.
- Use metadata retrieval before exposing objects to agents or semantic models.
- Governed queries can omit fields from `SELECT *`; explicit inaccessible fields should fail.
- View All/Modify All can expose metadata in some UI paths, but query policy enforcement still applies.
- Dynamic masking is applied at retrieval time; do not use masked values as join/filter truth.
- For data spaces, check token exchange, SQL connector/Python connector `dataspace`, or ConnectApi extra parameter handling before blaming query syntax.

## Query MCP

When a local query tool helps, prefer the official Data 360 MCP server
configured from [docs/mcp-dependencies.md](../../docs/mcp-dependencies.md).
Use any legacy local query MCP only if it is already present in the user's
workspace and the user authorizes live org access.

## Hard-won rules

- Query success does not prove segment SQL will compile.
- CI tables are fine for discovery queries and proposal logic.
- DBT segment creation is stricter than the query plane.
- Analytics, segments, transforms, and activations can consume the same logical data through different serving or processing paths; validate the target surface directly.
- Profile, metadata, calculated insight, and data graph retrieval all have different response shapes; do not normalize them casually.
- When a query differs from a segment, graph, report, or transform result, check governance enforcement differences before assuming data drift.
