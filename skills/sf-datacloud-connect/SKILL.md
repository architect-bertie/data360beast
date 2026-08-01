---
name: sf-datacloud-connect
description: >
  Salesforce Data 360 Connect phase for connectors and connection lifecycle.
  TRIGGER when: the user works on connectors, connections, connection schema,
  connection test flows, or source-object discovery.
license: MIT
metadata:
  version: "2.0.0"
  author: "architect-bertie"
---

# sf-datacloud-connect

Use this skill for the **connection plane**.

Connector catalog: [references/connector-implementation-cards.md](references/connector-implementation-cards.md)

Beast references:
- Beast preflight: [docs/beast-preflight.md](../../docs/beast-preflight.md)
- Phase proof matrix: [docs/phase-proof-matrix.json](../../docs/phase-proof-matrix.json)
- Public operating model: [docs/operating-model.md](../../docs/operating-model.md)
- Interoperability decision map: [docs/data360/interoperability-decision-map.md](../../docs/data360/interoperability-decision-map.md)
- Developer Guide index: [docs/data360/developer/index.md](../../docs/data360/developer/index.md)
- Proof ledger: [docs/proof-ledger.md](../../docs/proof-ledger.md)
- Public LLM map: [docs/llms.txt](../../docs/llms.txt)
- Limits source precedence: [docs/data360/limits-source-precedence.md](../../docs/data360/limits-source-precedence.md)
- For exact Salesforce behavior, fetch official Help/Developer docs on demand with `sf-docs`.
- For endpoint shape, use OpenAPI from the official spec or the user-supplied Swagger before writing payloads.

## Prefer these Connect API families

- `GET /ssot/connectors`
- `GET /ssot/connectors/:connectorType`
- `GET /ssot/connections`
- `POST /ssot/connections`
- `GET /ssot/connections/:connectionId`
- `PATCH /ssot/connections/:connectionId`
- `POST /ssot/connections/actions/test`
- `POST /ssot/connections/:connectionId/actions/test`
- `GET/PUT /ssot/connections/:connectionId/schema`

## Default workflow

1. inspect connector metadata
2. classify the connector as ingestion, query federation, file federation, sharing, or hybrid
3. inspect existing connections
4. test before creating when possible
5. upload or verify schema for ingestion-style connectors
6. hand off to Prepare or Retrieve once the connection and pattern are clear

## Rules

- Prefer REST payload inspection over guessing connector parameters.
- Reuse the OpenAPI catalog through [sf-datacloud-connectapi](../sf-datacloud-connectapi/SKILL.md); Postman is optional comparison only.
- For local development, CLI-auth or direct access token is usually faster than creating a new connected app.
- Review source prerequisites before creating streams. Help docs separate source configuration from stream setup.
- For connector-count and CRM-org-count questions, use current Data 360 Limits
  and Guidelines first. Follow Data Services Billable Usage Types when the
  current page points there. Use legacy Customer Data Platform CRM-org limits
  only when CDP is explicitly in scope or as a labeled comparison.
- Inspect connector metadata and test the connection before handing off to Prepare.
- Treat a successful connection test as control-plane proof only. Before calling
  a source ready, prove source-object discovery, source-side grants, and any
  connector-specific eligibility rules; for file federation, include table
  kind/format, catalog access, and the underlying storage path.
- When the requested scope continues past connection setup, use the readiness
  chain `connection -> source discovery -> stream/DLO -> DLO query -> DMO
  mapping -> DMO query`. Report downstream links as unproved instead of
  inferring them from healthy authentication.
- If data spaces are involved, confirm where the connection, stream, and resulting DLOs are scoped.
- For external lakehouses, choose the interoperability pattern before creating assets: ingestion for canonical governance, live query for maximum freshness, accelerated query for frequent reads with stale tolerance, file federation for large object-store/open-table workloads, or hybrid for governed core plus fresh edge.
- Capture source-system cost and governance assumptions for federated connections. Query federation can depend on external compute and source-side policies; file federation depends on storage access, table format, partitioning, and Data 360 compute.
- For Databricks zero-copy work, classify the exact connector mode before
  giving network guidance: query federation, accelerated query, file
  federation, data share, or batch ingestion. Do not let the umbrella
  "Databricks connector" hide different runtime paths.
- Separate `Salesforce Private Connect` from `Private Connect for Data 360`.
  Use current official docs and tenant validation before claiming Databricks
  private routing, especially for AWS-hosted Databricks. Public docs have been
  explicit for Databricks-on-Azure PNR setup, while AWS claims need exact source
  support or live org proof.
- For Databricks query federation, treat Data 360 IP allowlisting as both a
  setup gate and a runtime dependency for query, acceleration refresh, mapping,
  and downstream workloads. The primary allowlist point is Databricks-side
  workspace or SQL warehouse network control; customer-managed AWS firewalls,
  proxies, or PrivateLink-style layers add separate enforcement points.
- For Databricks file federation, map both network legs: Data 360 to the
  Databricks or Unity Catalog endpoint, and Data 360 to the underlying storage
  layer such as S3. Recheck current docs before promising PrivateLink support;
  prior official docs required public accessibility for Unity Catalog and
  storage and did not support AWS PrivateLink or Azure Private Link for this
  connector mode.
- When connector metadata is available, inspect it before payload design. In a
  prior Databricks query-federation surface, useful fields included
  `hasPrivateNetworkRoute`, `outboundnetworkconnection`, `jdbc_connection_url`,
  and `httpPath`; for Databricks file federation, inspect catalog endpoint,
  storage type, storage credentials, and identity-provider fields.
- Classify integration path before implementation: built-in Salesforce connector,
  external connector, Ingestion API bulk/streaming, Amazon S3 data stream,
  Salesforce Interactions SDK for web behavior, Engagement Mobile SDK for
  mobile events, MuleSoft, or zero-copy/federation.
- For API-driven ingestion, confirm OAuth scope requirements and whether the
  work is bulk historical load, recurring bulk load, or small-batch streaming.

## Validation gate

Connection work is not done until connector metadata is understood, auth is
healthy, an eligible source object and its grants are proven, schema is
discovered or uploaded, the integration pattern is explicit, and the next Data
Stream/DLO/federated-query step is clear.

## Doc-Synced Notes

<!-- SF_DOC_SYNC_START:connect-data-help-side -->
### Connect Data: Help-Side Concepts (Data Sources, Data Streams, Schedules)

_Distilled from official Salesforce sources only._

**Sources:**
- data.c360_a_connectors.htm — Data Sources in Data 360
- data.c360_a_connection_tasks.htm — Data Source Configuration in Data 360
- data.c360_a_data_streams.htm — Data Streams in Data 360
- data.c360_a_data_stream_schedule.htm — Data Stream Schedule
- data.c360_a_data_streams_tab.htm — Data Streams Tab Navigation
- developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-create-ingestion-data-stream.html — Create an Ingestion API Data Stream
- developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-create-sftp-data-stream.html — Create an SFTP Data Stream

**Data Source vs Data Stream:**
- A **Data Source** is the connector-level connection (auth, endpoint,
  credentials). Configured once per source system.
- A **Data Stream** is an ingestion pipeline from a Data Source into a
  specific Data Lake Object. Many streams can use one source.
- The "Data Sources" tab manages connections; the "Data Streams" tab
  manages ingestion pipelines and schedules.

**Creating a Data Stream (UI flow):**
1. App Launcher → Data Streams → New (or Data Streams tab → New).
2. Choose connector source (Ingestion API, SFTP, Salesforce CRM, S3,
   Snowflake, etc.).
3. Select or create the **Data Lake Object (DLO)** — the landing object
   in the Data 360 data lake.
4. Assign a label, API name, and category (Profile, Engagement, Other).
5. Choose **Primary Key** — required, must uniquely identify each record.
   - Platform Events: Event Identifier field.
   - Ingestion API / SFTP: any unique field.
6. Map fields if needed (or use auto-detected schema).
7. Choose **Refresh Mode**: Incremental (insert new), Full Refresh, or
   Partial (Profile/Other only — partial record updates without full
   replace).
8. Configure **Schedule** (see below).
9. Click Deploy.
10. Optionally click **Refresh Data Stream Immediately** to start ingest
    right after deployment.

**Refresh modes:**
| Mode | Behavior | Best for |
|---|---|---|
| Incremental | Inserts/updates new records by primary key | Append-only or high-volume streams |
| Full Refresh | Replaces all records on every run | Reference data, small dimension tables |
| Partial | Updates specified fields without full replace | Profile/Other category, partial CDC |

**Schedule options:**
- Frequencies: hourly (where supported), daily, weekly, monthly, or
  manual-only.
- Different connectors support different schedule granularities; check
  connector page.
- Manual refresh always available — overrides schedule when invoked.
- Concurrent refresh limits apply per org; long-running streams may
  defer if capacity is constrained.

**Data Streams Tab Navigation:**
- Lists all streams with status (Active, Error, Inactive, Processing).
- Filter by data source, refresh mode, or DLO.
- Inspect stream history (run logs, record counts, error counts).
- Edit, deactivate, or refresh from this tab.

**Pre-flight checks before creating a stream:**
- Connector authenticated and tested? (`POST /ssot/connections/actions/test`)
- Schema discovered or uploaded? (Ingestion API requires OAS/YAML upload.)
- DLO category chosen (Profile, Engagement, Other)?
- Primary key chosen?
- Refresh mode aligned with use case?
- Schedule frequency aligned with downstream consumer cadence?
- Data space scoping correct?

**Common errors and remedies:**
- "Schema mismatch" → re-upload schema or align field types in the source.
- "Primary key not unique" → choose a different field or composite key not
  supported (must use single-field uniqueness).
- "Authentication expired" → rotate credentials in the Data Source, then
  retest the connection.
- Stream stuck in Processing → check connector page for source-specific
  rate limits; verify source-side scheduling.
<!-- SF_DOC_SYNC_END:connect-data-help-side -->

<!-- SF_DOC_SYNC_START:developer-integration-catalog -->
### Integration and connector catalog gate

_Auto-synced from sf-docs captures of official Salesforce Developer documentation._

**Sources:**
- https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-data-cloud-integrations.html - Data 360 Integrations | Data 360 Integration Guide | Salesforce Developers
- https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-databricks-connector.html - Databricks Connectors | Data 360 Integrations | Data 360 Integration Guide | Salesforce Developers
- https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-set-up-databricks-file-federation-connection.html - Set Up a Databricks File Federation Connection | Data 360 Integrations | Data 360 Integration Guide | Salesforce Developers
- https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-ingestion-api.html - Ingestion API | Data 360 Integrations | Data 360 Integration Guide | Salesforce Developers

**Source fingerprint:** `189417577b6f42e77f931e75`

**Implementation notes:**
- Classify each connector by supported direction and mode: ingestion, query federation, file federation, data share, unstructured ingestion, activation, or bidirectional use.
- For Databricks, select the exact mode before setup; batch ingestion, query federation, file federation, and data sharing have different network, compute, catalog, and storage proof paths.
- For file federation, verify both the catalog endpoint and underlying object storage path, supported table format, source table eligibility, and required grants.
- For Ingestion API, treat schema agreement, connector setup, External Client App auth, data-stream deployment, object-endpoint delivery, and DMO mapping as separate gates.
- Connector availability, authentication, limitations, and supported objects change frequently; route current claims back through the exact connector page and Help limits.

<!-- SF_DOC_SYNC_END:developer-integration-catalog -->
