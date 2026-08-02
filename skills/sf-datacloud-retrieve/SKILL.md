---
name: sf-datacloud-retrieve
description: >
  Salesforce Data 360 Retrieve phase for query-sql, queryv2, profile APIs,
  metadata introspection, and query MCP usage. TRIGGER when: the user writes or
  debugs Data 360 SQL, profile retrieval, metadata lookup, or query tooling.
license: MIT
metadata:
  version: "2.0.0"
  author: "architect-bertie"
---

# sf-datacloud-retrieve

Use this skill for the **query and metadata plane**.

Beast references:
- Beast preflight: [docs/beast-preflight.md](../../docs/beast-preflight.md)
- Phase proof matrix: [docs/phase-proof-matrix.json](../../docs/phase-proof-matrix.json)
- Public operating model: [docs/operating-model.md](../../docs/operating-model.md)
- Architecture engine map: [docs/data360/architecture-engine-map.md](../../docs/data360/architecture-engine-map.md)
- Interoperability decision map: [docs/data360/interoperability-decision-map.md](../../docs/data360/interoperability-decision-map.md)
- RAG/search-index playbook: [docs/data360/rag-search-index-retriever-playbook.md](../../docs/data360/rag-search-index-retriever-playbook.md)
- Developer Guide index: [docs/data360/developer/index.md](../../docs/data360/developer/index.md)
- Companion MCP installs: [docs/mcp-dependencies.md](../../docs/mcp-dependencies.md)
- Proof ledger: [docs/proof-ledger.md](../../docs/proof-ledger.md)
- Public LLM map: [docs/llms.txt](../../docs/llms.txt)
- Limits source precedence: [docs/data360/limits-source-precedence.md](../../docs/data360/limits-source-precedence.md)
- For exact Salesforce behavior, fetch official Help/Developer docs on demand with `sf-docs`.
- For endpoint shape, use OpenAPI from the official spec or the user-supplied Swagger before writing payloads.

## Default surfaces

- `POST /ssot/query-sql`
- `GET /ssot/query-sql/:queryId`
- `GET /ssot/query-sql/:queryId/rows`
- Data 360 Direct API `POST /api/v3/query`
- Data 360 Direct API `GET /api/v3/query/:queryId`
- Data 360 Direct API `GET /api/v3/query/:queryId/rows`
- Data 360 Direct API `GET /api/v3/query/:queryId/chunks/:chunkId`
- Data 360 Direct API `GET /api/v3/query/:queryId/metadata`
- Apex `sfsqlquery` namespace and `ConnectApi.CdpQuery`
- Legacy `POST /ssot/queryv2` only when the target app/version requires it
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
- Prefer current Query Connect `/ssot/query-sql`, Data 360 Direct `/api/v3/query`, and documented Apex query surfaces for new retrieve work. Treat Query V1/V2 references as legacy unless the target client/version still requires them.
- SOQL can query supported Data 360 profile, data source, or DMO objects through
  REST API query or Apex, but it is a narrower platform-integrated path. Use
  ANSI SQL / Query APIs for broad Data 360 querying unless the user specifically
  needs SOQL behavior.
- Quote identifiers carefully when the surface requires it.
- Use `IS NOT NULL` for null checks.
- Use metadata/profile discovery before inventing table or field names.
- For RAG troubleshooting, search indexes produce chunk and index DMOs. Probe
  them directly with small `SELECT ... LIMIT 10` queries and compare chunk/index
  counts with source DMO counts before blaming prompts.
- For pro-code RAG, use Data 360 SQL `vector_search` or `hybrid_search` through
  Query SQL or Apex `ConnectApi.CdpQuery` when no-code retrievers cannot express
  nested filters, unsupported operators, post-filters, majority-vote
  classification, custom joins, or record access checks.
- Prefer query-sql or `ConnectApi.CdpQuery` when you need robust pagination or large result handling.
- Use Data 360 API / Direct API for high-performance tenant-side read paths when available.
- Treat query jobs as asynchronous: submit, poll, page rows, and handle status codes.
- For query performance, reason from the object layer first: DLO, DMO, CIO, or data graph. Selective predicates, date filters, projected fields, join grain, and row counts often matter more than cosmetic SQL changes.
- Prefer filtered queries with explicit field lists over broad record retrieval;
  query cost and credits are part of the design, not just an admin afterthought.
- Treat Trino-like or Iceberg-style query behavior as an inferred mental model only. Use it to choose proof steps such as metadata checks, smaller probes, count queries, and predicate selectivity tests.
- For zero-copy work, distinguish live query, accelerated query, and file federation. Live query is freshness-first and source-compute-dependent; accelerated query trades freshness for repeated-read performance; file federation is read-only and depends on object format, partitioning, pruning, and region/I/O.
- Push predicates and aggregations to the source when using query federation. Avoid unfiltered scans over massive federated datasets.
- Prefer profile endpoints when you need record-centric retrieval instead of ad hoc SQL.
- Use metadata retrieval before exposing objects to agents or semantic models.
- For SDK, notebook, BI client, database-client, driver, or query-engine questions, load the architecture engine map and classify the path as consumer/tool, driver/connector, API, execution engine, object/storage layer, and proof. Power BI, DBeaver, Looker, Tableau, Jupyter, and custom apps are consumers/tools, not engines.
- Classify query clients by interface: JDBC, ODBC or dedicated BI connector, Python connector/DB-API style cursor, REST/Direct API, Apex, or native Data 360 UI. Do not maintain a closed product list or infer support, engine, or compute locality from the client name alone.
- Treat DBeaver as a documented JDBC integration when current Salesforce docs are cited. Treat tools such as Looker as candidate/interface-compatible only until the exact driver, dialect, authentication, SQL behavior, and tenant readback are proven by current docs or live validation.
- Distinguish read-only query extraction from managed transforms: Python connector/Jupyter queries run in Data 360 and then analyze data locally; Code Extension Python runs through managed Data 360 transform execution after package/deploy.
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

## Doc-Synced Notes

<!-- SF_DOC_SYNC_START:data-spaces-retrieve -->
### Data Spaces in Query Tooling

_Auto-synced from the local sf-docs cached Salesforce Help export (official docs only)._

**Sources (sf-docs cached Help):**
- data.c360_a_using_data_cloud_apis_with_data_spaces.htm — Use Data Cloud APIs with Data Spaces

**Source fingerprint:** `914b475541498c62cea77808`

**Notes:**
- If results differ by user or environment, confirm whether the query path is scoped by a data space (token exchange, connector property, or API extra parameter).
- Treat data space selection as part of proof: include the data space in readbacks and troubleshooting probes.

<!-- SF_DOC_SYNC_END:data-spaces-retrieve -->

<!-- SF_DOC_SYNC_START:explore-and-query -->
### Explore and Query Tooling (Data Explorer, Profile Explorer, Query Editor)

_Distilled from official Salesforce sources only._

**Sources:**
- data.c360_a_data_explorer.htm — Data Explorer
- data.c360_a_profile_explorer.htm — Profile Explorer
- data.c360_a_query_editor.htm — Query Editor
- developer.salesforce.com/docs/data/data-cloud-query-guide/guide/dc-query-section.html — Get Started With Data 360 SQL
- developer.salesforce.com/docs/data/data-cloud-query-guide/guide/int-apps-data-cloud.html — Data 360 Integrated Apps
- developer.salesforce.com/docs/data/data-cloud-query-guide/guide/write-simple-query.html — Write a Simple Query

**Three query/exploration surfaces — pick the right one:**

| Tool | Best for | Output |
|---|---|---|
| Data Explorer | Browse DLO/DMO records, inspect schema, filter rows without writing SQL | UI grid, downloadable CSV |
| Profile Explorer | Inspect a specific Unified Individual: contact points, engagement, related DMOs, calculated insights | Per-profile JSON-like view |
| Query Editor | Write SQL across DLOs and DMOs, save queries, share workspaces | Tabular results, save/share |

**Data Explorer workflow:**
1. Data Explorer tab → select Data Lake or Data Model.
2. Choose object → see record count and schema.
3. Browse records (paginated) → apply filters via UI controls.
4. Download a CSV slice for offline inspection.
5. Use this as a first-pass before writing SQL — confirm record counts
   and field shapes before designing CIs/segments.

**Profile Explorer workflow:**
1. Profile Explorer tab → search for an individual by name, email, or
   profile ID.
2. Inspect the unified profile and all linked source profiles.
3. View related contact points, engagement events, calculated insights.
4. Trace identity resolution decisions (which records merged, which
   reconciliation rules fired).
5. Use this to debug identity resolution issues and to confirm that
   activation contact-point selection is what the user expects.

**Query Editor workflow:**
1. Query Editor tab → select or create a Workspace.
2. Workspace defines the DMOs/DLOs accessible to your queries (data
   space scoped).
3. Write SQL: `SELECT … FROM <DMO/DLO> WHERE …`.
4. Click Run; inspect tabular results.
5. Click Save to persist the query.
6. Share the workspace with collaborators (subject to permissions).

**Data 360 SQL essentials:**
- Use `SELECT *` for exploration; explicit field lists for production
  queries (FLS-aware).
- Filters via `WHERE` clause: `BETWEEN`, `LIKE`, comparison operators,
  combined with `AND`/`OR`.
- Aggregations: `COUNT`, `SUM`, `AVG`, `MIN`, `MAX`, `STDDEV`, `CORR`.
- Joins: inner, left outer, right outer, full outer.
- Join records on **both** `ssot__Id__c` and `KQ_Id__c` (key qualifier)
  for accurate matches — fully qualified key uniqueness.
- `GROUP BY` for aggregations; `ORDER BY` for sorting; `LIMIT` for
  pagination.

**Integrated apps for query/visualization:**
- Tableau (native via Tableau Semantics).
- DBeaver (JDBC connection).
- Custom apps via Connect API and Query API.

**Pitfalls:**
- A query that succeeds in Query Editor may not compile as a segment SQL
  (DBT segment compiler is stricter). Validate at the segment plane.
- Profile Explorer may show data the running user cannot see in segments
  due to RLS/masking differences — use Profile Explorer as admin-debug
  tool, not as governance proof.
- Workspace selection scopes the result; switching workspace can change
  query results.
- Cached query results may not reflect very recent ingestion — refresh
  the workspace if results look stale.
<!-- SF_DOC_SYNC_END:explore-and-query -->

<!-- SF_DOC_SYNC_START:developer-query-selection -->
### Query surface selection gate

_Auto-synced from sf-docs captures of official Salesforce Developer documentation._

**Sources:**
- https://developer.salesforce.com/docs/data/data-cloud-query-guide/guide/query-guide-get-started.html - Query Data in Data 360 | Data 360 Query Guide | Salesforce Developers
- https://developer.salesforce.com/docs/data/data-cloud-query-guide/guide/obj-specific-apis.html - Object Specific APIs | Query Data in Data 360 | Data 360 Query Guide | Salesforce Developers
- https://developer.salesforce.com/docs/data/data-cloud-query-guide/guide/dc-sql-query-apis.html - Data 360 SQL Query APIs | Query Data in Data 360 | Data 360 Query Guide | Salesforce Developers
- https://developer.salesforce.com/docs/data/data-cloud-query-guide/guide/dc-apex-query.html - Query Data 360 Data with Apex | Query Data in Data 360 | Data 360 Query Guide | Salesforce Developers
- https://developer.salesforce.com/docs/data/data-cloud-query-guide/guide/dc-soql.html - SOQL With Apex | Query Data in Data 360 | Data 360 Query Guide | Salesforce Developers

**Source fingerprint:** `f5688f5a26555828fd52169a`

**Implementation notes:**
- Prefer an object-specific API when it covers the target object and workflow; use custom Data 360 SQL when joins, aggregation, or unsupported objects require it.
- Use asynchronous query and polling patterns for large Apex workloads, and start with limited data to protect governor limits and validate semantics.
- Treat SOQL as a constrained Platform query path: no `SELECT *`, and Data 360 SOQL does not currently provide the relationship behavior needed to replace SQL joins.
- Calculated insights and data transforms use SQL contracts that differ from the Query Guide; validate in the owning phase rather than reusing Query SQL unchanged.

<!-- SF_DOC_SYNC_END:developer-query-selection -->
