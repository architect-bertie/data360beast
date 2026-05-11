# API Cookbook

This is the public summary of Data360 Beast API lessons. It is intentionally
curated and compact. Raw generated API catalogs and Salesforce Help exports are
not published here.

## API Workflow

1. Confirm target org, API version, data space, and asset lifecycle.
2. Search the Connect API OpenAPI spec for the operation family.
3. Build the smallest valid payload first.
4. Use disposable lab names for create tests.
5. Read back by returned ID.
6. Check status, count, metadata, or query proof.
7. Capture caveats before promoting the recipe.

## Live-Tested Areas

- Data spaces and metadata discovery.
- Query SQL and Profile API.
- DBT segment create, read, and count behavior.
- Data action target and data action create behavior.
- Activation target create and readback.
- Search index and calculated insight list surfaces.

## Gotchas Worth Keeping

- Data stream formula fields are not Query SQL. Use the Data 360 formula
  library syntax: uppercase functions, exact `sourceField['Header Label']`
  references, `==`/`!=` comparisons, and `COALESCE([value, fallback])`.
- Engine-aware triage matters. Query, transform, segment, analytics, activation,
  and orchestration surfaces can validate and execute through different paths,
  so proof must match the surface being debugged.
- Interoperability is a first decision, not an implementation afterthought.
  Choose ingestion, live query, accelerated query, file federation, or hybrid
  from freshness, governance, access pattern, data volume, and cost/I/O.
- DBT segment create used `includeDbt.models.models[]` successfully.
- DBT segment readback can normalize the shape to `includeDbt.models[]`.
- Approximate segment count can fail when the feature is disabled.
- Segment member retrieval depends on a delta window.
- Status and count readback are better first proofs than member retrieval.
- Activation target readback by returned ID was reliable in lab.
- For pro-code RAG, `vector_search` and `hybrid_search` should be driven from
  Query SQL or Apex `ConnectApi.CdpQuery` only after metadata confirms the index
  DMO, chunk DMO, source joins, and filter fields.
- External activation destinations and search-index creation need enabled assets
  before promotion into tested public recipes.

## Agent Rule

Do not invent payload fields. Use OpenAPI for shape, then use this cookbook for
known behavior and caveats.
