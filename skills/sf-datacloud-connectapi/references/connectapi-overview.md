# Data 360 Connect API Overview

This reference is the local, project-shaped view of Data 360 programmatic development.

## Auth modes

Use one of these:

1. `SF_TARGET_ORG_ALIAS`
   - Best for local development when `sf org display --json` already works.
   - Reuses the current Salesforce CLI session.

2. `SF_ACCESS_TOKEN` + `SF_INSTANCE_URL`
   - Best for automation or wrappers that already have a token.

3. `SF_CLIENT_ID` + `SF_CLIENT_SECRET`
   - Best for a connected-app OAuth flow when no local `sf` session exists.

Inside Apex, none of these are needed; use `ConnectApi` directly.

## Main endpoint families

The bundled Postman collection currently exposes 192 requests across these families:

- Connections
- Data Streams
- Data Lake Objects
- Data Model Objects
- Data Model Object Mappings
- Identity Resolutions
- Data Graphs
- Calculated Insights
- Segments
- Activation Targets / Activations / Data Actions
- Metadata / Profile
- Query / Query V2 / Query SQL
- Search Index
- Document AI

## Choosing the surface

### Query plane

Use this when you need SQL and table access:

- `POST /ssot/queryv2`
- `POST /ssot/query-sql`
- `GET /ssot/query-sql/:queryId`
- `GET /ssot/query-sql/:queryId/rows`
- Apex `ConnectApi.CdpQuery.queryAnsiSqlV2`

### Profile plane

Use this when you need record-centric retrieval from a DMO:

- `GET /ssot/profile/metadata`
- `GET /ssot/profile/metadata/:dataModelName`
- `GET /ssot/profile/:dataModelName`
- `GET /ssot/profile/:dataModelName/:id`
- `GET /ssot/profile/:dataModelName/:id/:childDataModelName`
- `GET /ssot/profile/:dataModelName/:id/calculated-insights/:ciName`

### Schema plane

Use this when you need object definitions or mappings:

- `GET /ssot/data-model-objects`
- `GET /ssot/data-model-objects/:dataModelObjectName`
- `GET /ssot/data-model-object-mappings`
- `GET /ssot/metadata`

### Segment plane

Use this when you need CI or segment lifecycle:

- `GET/POST/PATCH/DELETE /ssot/calculated-insights`
- `POST /ssot/calculated-insights/:apiName/actions/run`
- `GET/POST/PATCH/DELETE /ssot/segments`
- `POST /ssot/segments/:segmentId/actions/publish`
- Apex `ConnectApi.CdpSegment.createSegment`

### Graph plane

Use this when you need contextual retrieval or Customer 360 navigation:

- `POST /ssot/data-graphs`
- `GET /ssot/data-graphs/:dataGraphName`
- `GET /ssot/data-graphs/metadata`
- `GET /ssot/data-graphs/data/:dataGraphEntityName/:id`
- `GET /ssot/data-graphs/data/{{entity}}?lookupKeys=...`

## DMO page caveat

The official DMO catalog page is the canonical place to learn labels, descriptions, and doc pages for standard DMOs, but it does not guarantee the runtime object API name you should query. Resolve runtime names through metadata/profile/query surfaces before writing production SQL.
