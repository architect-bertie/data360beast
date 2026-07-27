# Data 360 Developer Guide Skill Update Synthesis

Public source map: [docs/data360/developer/index.md](index.md) lists the 24
official `developer.salesforce.com` Data 360 Developer Guide pages this
synthesis was distilled from.

Official source root:
- https://developer.salesforce.com/docs/data/data-cloud-dev/guide/dc-get-started.html

Indexed scope: 24 official `developer.salesforce.com` Data 360 Developer Guide pages.

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

### Development Lifecycle

- Data 360 development is not a clone of standard Salesforce Platform
  development. Customer developers use Data 360 sandboxes where available, or a
  separate Data 360-enabled test org; second org usage is metered.
- ISV partners use Partner Developer Edition orgs and request Data 360 enablement
  through partner channels.
- The role model matters: data administrator owns data strategy, system
  integrator helps setup and mapping, Salesforce partner builds distributable
  apps, and customer developer builds internal custom apps.

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

## Skill Updates To Make

- `data360beast`: add the developer guide index as a local source map and route
  development questions through lifecycle, API surface, packaging, deploy, and
  cost gates.
- `sf-datacloud`: add development lifecycle and role/environment selection to
  the default architecture loop.
- `sf-datacloud-connectapi`: add the API surface selection matrix and auth
  distinction between Connect REST/Apex and Data 360 API tenant-direct calls.
- `sf-datacloud-connect` and `sf-datacloud-prepare`: add ingestion API, S3 data
  stream, Salesforce Interactions SDK, and Engagement Mobile SDK as integration
  paths to classify before implementation.
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

_Maintainer-only:_ this synthesis is regenerated from a local sf-docs cache
(`docs/data360/developer/manifest.json` and `docs/data360/developer/raw/*.md`)
that lives outside the public clone. The `tools/refresh_skills_from_sf_docs.py`
script and the docs-watch automation pipeline rebuild this file from that
cache; the public clone keeps only the distilled output.
