# Data 360 Architecture Engine Map

This note captures a public-safe operating model for reasoning about Data 360
architecture and troubleshooting. It is derived from user-provided architecture
material and the Data360 Beast operating model. Treat it as an inferred mental
model, not official Salesforce documentation or an API contract.

## Source Boundary

- Use official Salesforce docs for setup, limits, permissions, and supported
  product behavior.
- Use the Connect API OpenAPI catalog for endpoint and payload shape.
- Use live org validation for tenant-specific truth.
- Do not publish raw architecture deck images, org metadata, customer data, or
  implementation details that are not needed for field guidance.

Related decision map:
- `docs/data360/interoperability-decision-map.md`

## Core Stack Model

Data 360 work becomes easier to reason about when separated into layers:

| Layer | What To Ask | Common Proof |
| --- | --- | --- |
| Experience and APIs | Which surface is the user touching? | UI state, API response, returned ID |
| Messaging and query plane | Is this query, profile, segment, activation, or graph retrieval? | query job status, rows, profile result, segment count |
| Compute plane | Is this a processing job, query job, analytics serving path, or orchestration? | run status, error code, readback object, output count |
| Data/storage plane | Is the data in DSO, DLO, DMO, CIO, graph, or external storage? | metadata, field list, row count, sample records |
| Governance plane | Could data space, permission, tags, masking, or RLS change the answer? | non-admin validation, policy readback |

Use this taxonomy when a question mentions an SDK, notebook, BI client,
database client, driver, connector, API, or query engine:

```text
consumer/tool -> driver/connector -> API -> execution engine -> object/storage layer -> proof
```

| Term | Meaning | Do Not Infer |
| --- | --- | --- |
| Consumer/tool | The UI or application a person uses, such as Query Editor, DBeaver, Tableau, Power BI Desktop, Jupyter, Looker, Apex, or a custom app | The server execution engine or certification status |
| Driver/connector | The client adapter, such as JDBC, ODBC, Python connector, REST client, Apex class, or dedicated BI connector | That every tool with the same adapter is officially supported |
| API surface | The Salesforce/Data 360 endpoint family or Apex namespace actually called | That legacy and current query APIs have identical behavior |
| Execution engine | The server-side compute/query/serving implementation or mental model | That the engine is selected by the client name |
| Object/storage layer | DSO, DLO, DMO, CIO, Data Graph, cached result, or external/federated source | That every consuming surface sees the same grain, cache, or policies |
| Proof | The readback that proves the target surface worked | That upstream success proves downstream behavior |

## Consumer and Interface Matrix

Examples are non-exhaustive. Classify the path before answering compatibility,
performance, or "where does this run?" questions.

| Consumer Or Tool | Typical Interface | Current Evidence Level | Compute Locality | Proof Habit |
| --- | --- | --- | --- | --- |
| Query Editor | Native Data 360 SQL UI | explicitly documented integration | Data 360 query execution | query ID/rows, data space, governed user if access matters |
| DBeaver | Data 360 JDBC driver | explicitly documented integration | Data 360 query execution through JDBC/Query API | driver config, OAuth/JWT auth, data space, result rows |
| Java JDBC apps | Data 360 JDBC driver | interface-compatible from Salesforce JDBC docs | Data 360 query execution through JDBC/Query API | app properties, auth, data space, result rows |
| Python or Jupyter | Data 360 Python Connector / DB-API style cursor | documented read connector | Data 360 query execution, then local Pandas/Python work | SQL result, dataframe shape, auth scopes, data space |
| Power BI Desktop | Data 360 Power BI Desktop Connector / ODBC path | documented connector | DirectQuery queries Data 360 remotely; Import caches a copy in Power BI | DSN, OAuth, Import vs DirectQuery, selected objects, refresh behavior |
| Tableau | Salesforce-documented integrated app / Tableau-oriented consumption | explicitly documented integration | depends on connector and semantic/reporting path | connection, workbook/report result, freshness/cache check |
| Looker | JDBC-style database connection only if a compatible dialect/driver path is proven | inferred/candidate unless current Salesforce and vendor proof or tenant test exists | depends on the proven driver and Looker dialect behavior | driver load, dialect, auth, generated SQL, result rows |
| REST or Postman app | Connect REST `/ssot/query-sql` or Direct `/api/v3/query` | documented API surface | Data 360 query execution | submit, poll/status, rows/chunks/metadata, pagination |
| Apex app | `sfsqlquery` namespace or `ConnectApi.CdpQuery` | documented API surface | Salesforce server-side caller invoking Data 360 query execution | Apex method response, status/rows, governor behavior |
| Native reports/dashboards | Data 360 reporting/semantic/analytics path | documented analytics surface | analytics serving path, often with cache/semantic behavior | report total, dashboard refresh, semantic metric, target user |

Evidence levels:

| Level | Use When | Required Wording |
| --- | --- | --- |
| explicitly documented integration | Salesforce or vendor docs name the tool/integration for Data 360 | "documented" with source |
| interface-compatible | Docs say a driver/protocol works generally, but the specific tool is not named | "should be possible through the documented interface; prove in tenant" |
| tenant-tested | The exact org, client, auth, data space, and query were validated | "tested in this target" with readback |
| inferred/candidate | Architecture suggests a path, but docs or tenant proof are missing | "candidate" or "inferred"; do not call it supported |

## Object Progression

Use this progression before writing SQL, formulas, segments, or activation
logic:

| Object Layer | Mental Model | Common Work |
| --- | --- | --- |
| DSO | Original source or transient connector shape | schema inspection, source header references |
| DLO | Lakehouse storage shape, often schema-enforced and source-adjacent | data streams, formula fields, ingestion validation |
| DMO | Curated model shape used by business features | mappings, relationships, identity, segments, activations |
| CIO | Materialized calculated insight output | reusable metrics, segmentation, reports, activation inputs |
| Data Graph | Read-optimized graph record over DMO data | profile context, agent grounding, real-time retrieval |

## Engine-Aware Heuristics

These engine associations are useful for triage, but they are inferred and can
change by release, tenant, feature, or surface.

| Engine Or Plane | Think Of It As | Agent Guidance |
| --- | --- | --- |
| Spark-like processing | heavy data processing, transforms, materialization, lakehouse writes | validate job status, output objects, row counts, and reruns |
| Trino-like query | federated SQL and lakehouse query access | validate query syntax, data space, field metadata, and result pages |
| Hyper-like serving | high-performance analytics and Tableau-style consumption | validate report/dashboard/semantic output, freshness, and cache behavior |
| Airflow-like orchestration | scheduling and workflow coordination | validate task/run status before blaming data or SQL |
| Iceberg-style storage | table metadata, snapshots, manifests, Parquet files, pruning | reason about selective filters, partition-like columns, file pruning, and scan cost |

The current public Query Guide documents Connect REST `/ssot/query-sql` and
Data 360 Direct `/api/v3/query` paths, including asynchronous execution,
pagination, JSON or Apache Arrow results, and Direct API metadata/chunk
endpoints. A Salesforce developer blog also states that the current Query
Connect API supersedes V1/V2 and is powered by Hyper. Use that as documented
current-query evidence, but still avoid promising that every client, tenant,
or future release uses the same engine implementation.

Terminology guards:

| Term | Guardrail |
| --- | --- |
| Hyper | A SQL/query engine referenced by Salesforce for current Query Connect behavior; validate the actual query surface |
| Hyperforce | Salesforce infrastructure/security foundation, not the Hyper query engine |
| Spark | A useful mental model for Code Extension and batch-processing DataFrame work; it does not by itself explain upload/deployment requirements |
| Trino | A useful query/federation mental model and a connector/source technology in some paths; do not infer it from a BI client |
| Power BI, DBeaver, Looker, Tableau, Jupyter | Consumers/tools; they do not name the Data 360 server engine by themselves |

## Compute Locality

When someone asks "where does this run?", answer at the workload level.

| Workload | Where It Runs | Why It Behaves That Way |
| --- | --- | --- |
| Data 360 Query API, JDBC, Query Editor, REST, Apex query | Data 360 query service, with results returned to the client | Client submits SQL; server executes and pages/caches results |
| Python connector in Jupyter or local app | SQL runs in Data 360, then analysis runs locally in Python/Pandas | The connector extracts query results into the user's Python environment |
| Power BI DirectQuery | Power BI issues recurring remote queries to Data 360 | Dashboard interactions can trigger remote query workload and Data 360 usage |
| Power BI Import or exported CSV | Initial query/extract runs against Data 360; later analysis can run on the imported copy | Cached/imported data can be stale and has separate refresh proof |
| Query federation / zero copy | Data 360 query path reaches into an external source or file/lake path | Freshness, source compute, network, catalog, and pruning determine behavior |
| Batch transforms and Code Extension scripts | Managed Data 360 processing plane | Packaging/upload enables managed deployment, scheduling, security, logs, retries, output ownership, and product readbacks |
| Code Extension local validation | Developer workstation or container | Local success proves syntax/toolchain only, not managed remote execution |

This is the key Python nuance: the Data 360 Python Connector is for querying
and local analysis, while Code Extension Python is packaged for managed Data
360 execution. Spark/DataFrame conventions help explain the programming model
for custom scripts, but upload/deploy is required because the work must execute
inside the managed transform lifecycle with platform security, scheduling,
observability, and output ownership.

## Triage Loop

Use this loop when a Data 360 symptom is ambiguous:

```text
symptom
-> user-facing surface
-> DSO/DLO/DMO/CIO/graph layer
-> likely execution plane
-> metadata and governance checks
-> proof path for that layer
```

Examples:

| Symptom | First Interpretation | Better Proof Path |
| --- | --- | --- |
| Formula field is invalid | Do not assume SQL syntax | Check Data 360 formula library syntax and `sourceField['Header Label']` casing |
| Query works but segment fails | Query plane and segment compiler can differ | Validate DMO grain, relationships, Segment On primary key, create status, and count |
| CI preview works but output is missing | Preview is not materialization proof | Run/publish the insight and query the `__cio` output |
| Report differs from Query Editor | Analytics serving, semantic definitions, cache, or governance can differ | Validate report grain, semantic metric, dashboard refresh, and target user access |
| Query is slow | It may be a scan/pruning problem, not just SQL syntax | Check predicate selectivity, joins, date filters, projected fields, and row counts |
| Activation has no members | Segment status and activation delivery are separate | Check segment count/status, publish status, target readback, and destination logs |

## Performance Lens

When a query or report is slow, avoid jumping straight to syntax fixes. Check:

1. Is the filter selective and applied to a field that can reduce scanned data?
2. Is the query pulling unnecessary columns or high-cardinality groupings?
3. Is the join multiplying rows before filters apply?
4. Is the data fresh in the object layer being queried?
5. Is the consuming surface using a different cache, semantic model, or serving
   path than the validation query?

For external data, also ask whether the data is ingested, queried live,
accelerated through a cache, accessed through file federation, or blended
through a hybrid pattern. The integration pattern changes the likely cost,
governance owner, freshness, and proof path.

## Output Habit

For architecture-sensitive answers, include:

1. surface touched
2. object layer
3. likely execution plane, labeled as inferred unless proven
4. command, payload, query, or UI readback
5. remaining caveat
