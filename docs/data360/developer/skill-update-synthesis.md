# Data 360 Developer Documentation Skill Update Synthesis

The public [Developer documentation index](index.md) is discovered from the
official Data 360 Developer Center. It currently represents 3,596 pages across
nine guide and reference families. Of those, 951 implementation-oriented pages
were content-captured through sf-docs and 2,645 DMO reference pages were
cataloged by official sidebar metadata without republishing their bodies.

Official source roots include:

- https://developer.salesforce.com/developer-centers/data-cloud
- https://developer.salesforce.com/docs/data/data-cloud-dev/guide/dc-get-started.html
- https://developer.salesforce.com/docs/data/data-cloud-code-ext/guide/use-custom-code.html
- https://developer.salesforce.com/docs/data/connectapi/overview
- https://developer.salesforce.com/docs/data/connectapi/references
- https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-model-data.html
- https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-data-cloud-integrations.html
- https://developer.salesforce.com/docs/data/data-cloud-query-guide/guide/query-guide-get-started.html
- https://developer.salesforce.com/docs/data/data-cloud-query-guide/references/dc-sql-reference/data-cloud-sql-context.html

## Coverage Model

- Fully capture the Developer Guide, Code Extension, Connect REST guide,
  Integration Guide, Query Guide, and SQL root through sf-docs.
- Catalog every DMO/mapping reference page, but content-capture only the
  modeling foundations and high-use implementation DMOs. This keeps the public
  repository lean while preserving complete discovery.
- Treat the DMO and Mapping Guide's developer-preview notice as a production
  gate. Confirm current Help and target-org metadata before using catalog
  commands, schemas, or extensibility claims in production.
- Use source-family fingerprints in `learning-map.md` to detect meaningful
  upstream drift without republishing source bodies.

## Durable Learnings

### API Surface Selection

- Use **Connect REST API** when the app is platform-integrated or needs Data 360
  resources through Salesforce Platform auth. It covers Query, Calculated
  Insights, Profile, Identity Resolution Rulesets, Segments, Universal ID
  Lookup, and metadata.
- Use **Connect API in Apex** when the app runs in Apex. It is a subset of
  Connect REST API and does not cover every Connect REST surface, notably
  profile and Universal ID lookup access.
- Use **Data 360 API / Direct API** when the app does not need Salesforce
  Platform features and wants tenant-direct performance. It uses a two-step
  auth exchange from Salesforce access token to Data 360 access token and a
  tenant-specific endpoint. It does not cover every Connect REST surface,
  notably segments and identity resolution rulesets.
- Use **SOQL** only where the REST API or Apex supports the Data 360 object
  query path. Treat SOQL as a narrower platform-integrated alternative to ANSI
  SQL over Query APIs, not as the default query dialect for all Data 360 work.
- Use **Metadata API** for supported Data 360 metadata migration only after
  checking the current metadata coverage and packageability.
- Prefer an object-specific API over custom SQL when it covers the target
  object and workflow. Use Data 360 SQL when cross-object joins, aggregation,
  or unsupported objects require the flexible query plane.
- Connect REST guide examples are workflow evidence, not payload authority.
  Validate paths and schemas against the current OpenAPI reference.
- DBT segment SQL has a narrower contract than Query SQL. Its top-level output
  must project the Segment On primary key and obey its additional expression,
  aggregation, qualifier, and join restrictions.

### Authentication

- Data 360 API setup starts with an External Client App and OAuth scopes such
  as `cdp_query_api`, `cdp_profile_api`, `cdp_ingest_api`, `refresh_token`,
  and `api`, depending on the use case.
- Data 360 API tenant auth is two-step: authenticate to Salesforce first, then
  exchange the Salesforce token for a Data 360 token and tenant-specific URL.
- Connect REST API and Connect API in Apex stay on the Salesforce Platform auth
  path.

### Architecture And Object Model

- The developer guide reinforces the flow: source data -> DLO in source schema
  -> DMO in Customer 360 model -> Unified DMO through identity resolution ->
  CIO for calculated metrics -> segment/activation/query/action surfaces.
- Unstructured data follows a different path: UDLO -> chunking -> indexing and
  embedding -> vector or hybrid search.
- Data 360 Home Orgs, Companion Orgs, shared data spaces, companion
  connections, Data Cloud One, and Data 360 APIs are separate architecture
  choices that must be called out when an architecture crosses org boundaries.
- Identity resolution creates link tables that preserve original records while
  tying them to unified individuals. Do not explain unified profiles as a lossy
  golden-record overwrite.
- The DMO catalog separates standard DMOs, standard DLO-to-DMO mappings, data
  bundles, extensibility readiness, legacy DMOs, and legacy bundles. Resolve
  which family is in use before proposing mappings or field APIs.
- Preserve business grain. Do not force source attributes into semantically
  misleading standard fields merely to avoid a justified custom support DMO.

### Integration And Connector Selection

- The Integration Guide is a capability catalog, not one generic connector
  workflow. Classify each source by supported direction and mode: ingestion,
  query federation, file federation, data share, unstructured ingestion,
  activation, or bidirectional use.
- Databricks batch ingestion, query federation, file federation, and data
  sharing have different compute, network, catalog, object-storage, and proof
  paths. Select the exact mode before gathering credentials or creating assets.
- File federation needs proof for both the catalog endpoint and underlying
  object storage, plus table format, source-table eligibility, and grants.
- Ingestion API implementation has distinct gates for schema agreement,
  connector setup, External Client App auth, stream deployment, object-endpoint
  delivery, and DMO mapping.

### Query Selection And Readback

- Query tooling includes integrated apps, object-specific APIs, JDBC, Python,
  Connect API in Apex, SOQL-supported paths, and Data 360 SQL APIs. Choose the
  narrowest surface that satisfies the workload.
- Use asynchronous polling for large Apex queries and begin with limited data.
  Carry data-space context and a useful workload name where supported.
- SOQL is intentionally narrower: it has no `SELECT *`, and its current Data
  360 implementation does not provide relationship behavior equivalent to SQL
  joins.
- Calculated Insight SQL and transform SQL are separate language contracts.
  A Query Guide example is not proof that the same SQL is valid in those phases.

### Code Extension

- Scripts run as batch data transforms; functions run in the search-index
  chunking pipeline. Route them to different proof targets.
- Preflight the exact documented local runtime and toolchain before scaffold,
  scan, local execution, or deployment.
- DMO-to-DMO scripts require explicit output schema configuration; do not rely
  on the scan command to infer write schemas.
- Prove execution with deployment/run state, output DLO or DMO readback, and
  `DataCustomCodeLogs__dll`. Deployment alone is not execution proof.
- Move validated code with a DevOps data kit and explicitly include referenced
  DLOs or DMOs when they are not added automatically.

### Development Lifecycle

- Data 360 development is not a clone of standard Salesforce Platform
  development. Customer developers use Data 360 sandboxes where available, or a
  separate Data 360-enabled test org; second org usage is metered.
- ISV partners use Partner Developer Edition orgs and request Data 360 enablement
  through partner channels.
- The role model matters: data administrator owns data strategy, system
  integrator helps setup and mapping, Salesforce partner builds distributable
  apps, and customer developer builds internal custom apps.

### Implementation Foundation

- Treat business outcome, source/data strategy, user permissions, limits, org
  topology, residency, data ethics, and environment lifecycle as pre-build
  decisions rather than setup cleanup.
- For multi-org architecture, distinguish home org, companion org, standard CRM
  connection, shared data spaces, metadata sync, and user access.
- Data 360 sandboxes receive metadata rather than replicated production Data
  360 records. Seed approved test data, reauthorize integrations, and repeat
  runtime proof after deployment.
- Keep definition state, job state, materialized data, segment publish, and
  destination delivery as separate lifecycle gates across the implementation.

### Packaging, Data Kits, And Deploy

- Data kits are the central package/deploy abstraction for Data 360 metadata.
  The metadata represents definitions, not data.
- When packaging both Data 360 metadata and Salesforce Platform metadata, keep
  them in separate packages and verify current packageability by component.
- Managed package Data 360 feature metadata is locked after deployment; the
  package owner controls redeployment.
- Sandbox-to-production movement uses a DevOps data kit, downloaded
  `package.xml`, `sf project retrieve start --manifest`, and
  `sf project deploy start --manifest`.
- Programmatic data-kit deployment uses the Connect REST deploy-data-kit
  endpoint with `asyncMode=true`. A successful request returns `202 Accepted`
  and a job ID; poll deployment status to `Completed` or `Error`.
- Treat the flow-based single-click deployment method as legacy for new
  programmatic guidance. Standard and DevOps data kits have different request
  bodies, and the target data-space name must match.
- Deployment gotchas to teach the agent: data space prefixes must match between
  source and target, generated key qualifier files can need deletion, missing
  `FieldSrcTrgtRelationship` metadata can block DMO relationship deployments,
  and connector authorization data is not copied, so deployed connectors can be
  inactive until reauthorized.

### Cost And Usage

- Cost is not an afterthought: storage, processed/queried/analyzed records,
  segmentation, activation, and ad audiences can consume credits.
- Query guidance should prefer filtered SQL/SOQL with explicit selected fields
  over broad GET-style retrieval when feasible.
- Ingestion guidance should import only relevant data and aggregate before
  ingestion when raw detail is not required.
- Testing guidance should limit test data volume to what functional validation
  needs.

## Skill Updates Applied

- `data360beast`: routes development questions through the complete Developer
  Center index, lifecycle, API surface, packaging, deployment, and cost gates.
- `sf-datacloud`: add development lifecycle and role/environment selection to
  the default architecture loop.
- `sf-datacloud-connectapi`: add the API surface selection matrix and auth
  distinction between Connect REST/Apex and Data 360 API tenant-direct calls.
- `sf-datacloud-connect` and `sf-datacloud-prepare`: add ingestion API, S3 data
  stream, Salesforce Interactions SDK, and Engagement Mobile SDK as integration
  paths to classify before implementation.
- `docs/data360/implementation-foundation.md`: add org-topology, residency,
  ethical-data, sandbox, and cross-phase proof gates backed by sf-docs Help
  fingerprints.
- `sf-datacloud-connect`, `sf-datacloud-prepare`, and
  `sf-datacloud-harmonize`: add source-eligibility, direct-access/acceleration,
  fanout, and terminal identity-run readbacks distilled from public-safe field
  evidence.
- `sf-datacloud-metadata-agentic`: add data kits, metadata coverage,
  packageability, and component cheat-sheet lookup as required proof points.
- `sf-datacloud-governance`: add Home Org, Companion Org, shared data spaces,
  and companion connections to cross-org governance triage.
- `sf-datacloud-retrieve`: add SOQL-as-narrow-platform-query guidance and keep
  ANSI SQL / Query API as the default for broad Data 360 querying.
- `sf-datacloud-analytics`, `sf-datacloud-segment`, and `sf-datacloud-act`:
  add credit-consumption proof habits for query, segment, activation, and ad
  audience recommendations.

---

_Maintainer-only:_ the raw sf-docs captures and generated manifest stay outside
the public clone. The docs-watch pipeline rebuilds the public index, source
fingerprints, graph, and marker-delimited specialist notes from that local
working set.
