---
name: sf-datacloud-connectapi
description: >
  Salesforce Data 360 Connect REST API and Apex ConnectApi development.
  TRIGGER when: the user wants programmatic Data 360 work through REST, OpenAPI,
  Apex ConnectApi.CdpQuery/CdpSegment, Data Graph APIs, Profile APIs, Query APIs,
  endpoint discovery, payload design, or API validation. DO NOT TRIGGER when:
  the task is only declarative Data 360 UI usage with no API or code path.
license: MIT
metadata:
  version: "2.1.0"
  author: "architect-bertie"
  validated: "OpenAPI-first Data360 Beast refresh with proof ledger evidence"
---

# sf-datacloud-connectapi

Use this skill for the **programmatic Data 360 surface**:
- Connect REST API under `/services/data/vXX.X/ssot/...`
- Apex `ConnectApi.CdpQuery*`, `ConnectApi.CdpSegment*`, and related Data 360 classes
- Data 360 Query/Profile/Metadata/Data Graph APIs
- endpoint discovery, payload snippets, local tools, MCP integration, and live validation

## Beast References

Use these first, before guessing:
- Beast preflight: [docs/beast-preflight.md](../../docs/beast-preflight.md)
- Phase proof matrix: [docs/phase-proof-matrix.json](../../docs/phase-proof-matrix.json)
- Proof ledger: [docs/proof-ledger.md](../../docs/proof-ledger.md)
- Public operating model: [docs/operating-model.md](../../docs/operating-model.md)
- Developer Guide index: [docs/data360/developer/index.md](../../docs/data360/developer/index.md)
- Companion MCP installs: [docs/mcp-dependencies.md](../../docs/mcp-dependencies.md)
- Public LLM map: [docs/llms.txt](../../docs/llms.txt)
- Limits source precedence: [docs/data360/limits-source-precedence.md](../../docs/data360/limits-source-precedence.md)
- Local reference: [references/connectapi-overview.md](references/connectapi-overview.md)
- Local reference: [references/connectapi-endpoint-cards.md](references/connectapi-endpoint-cards.md)
- Local reference: [references/project-gotchas.md](references/project-gotchas.md)

When a full OpenAPI or Swagger file is available from the user or official Salesforce docs, use it as the method, path, parameter, schema, response, and version source of truth. Do not require the private local generated catalog.

## Source Hierarchy

1. **OpenAPI catalog** for method/path/parameter/schema/response/version mechanics.
2. **proof ledger** for live-tested payload shapes, commands, gotchas, and proof fields.
3. **Official Salesforce docs via `sf-docs`** for behavior, limits, permissions, setup, and release caveats. Install/configure it from [docs/mcp-dependencies.md](../../docs/mcp-dependencies.md) when missing.
4. **Data 360 MCP** for live operations when its session is healthy: `search -> payload_examples -> execute`. Install/configure it from [docs/mcp-dependencies.md](../../docs/mcp-dependencies.md) when missing.
5. **Target org validation** for actual data spaces, permissions, metadata names, status, and row counts.

Do not use Redoc-rendered Markdown as canonical when the YAML/catalog is available. Do not copy endpoint dumps into this skill.

## When This Skill Owns The Task

Use this skill when the work involves:
- REST payloads for connections, streams, DLOs, DMOs, mappings, graphs, CIs, segments, activations, data actions, search indexes, or queries
- Apex code that calls Data 360 `ConnectApi`
- mapping a product concept to a Connect API endpoint
- building cURL, Postman, MCP, CLI, or local tooling around Data 360 APIs
- deciding between Connect REST, Apex ConnectApi, Query API, Profile API, Metadata API, Data 360 API/Direct API, or data kits

Delegate phase behavior to the relevant Data 360 specialist skill after the endpoint/API surface is identified.

## Portable API Lookup

- If the user supplies `cdp-connect-api-Swagger.yaml` or another official OpenAPI file, search it before writing any method, path, parameter, or payload.
- If no local spec is available, fetch the current official Salesforce Connect API docs on demand and cite the page used.
- Run Beast preflight before create/update calls so target org, data space,
  authorization boundary, and proof target are explicit.
- Use the phase proof matrix to confirm the owning phase, minimum readback, and
  forbidden assumptions before promoting a payload.
- Use [docs/proof-ledger.md](../../docs/proof-ledger.md) and [references/project-gotchas.md](references/project-gotchas.md) for live-tested gotchas.
- Use `scripts/data360_accelerator.py snippet --kind apex-query`, `apex-segment-create`, or `curl-query-sql` for small starter snippets.
- Use `scripts/data360_accelerator.py summarize-postman --postman <collection.json>` only when the user provides a Postman collection.

## API Surface Map

| Need | Preferred Surface |
| --- | --- |
| SQL over Data 360 tables | `ConnectApi.CdpQuery.queryAnsiSqlV2`, `/ssot/query-sql`, `/ssot/queryv2` |
| profile/record retrieval | `/ssot/profile/...` |
| schema and metadata | `/ssot/metadata`, `/ssot/profile/metadata`, Data Model Object endpoints |
| Data Graph metadata/data | `/ssot/data-graphs/...` |
| connection lifecycle | `/ssot/connectors`, `/ssot/connections` |
| streams, DLOs, transforms | `/ssot/data-streams`, `/ssot/data-lake-objects`, `/ssot/data-transforms` |
| calculated insights | `/ssot/calculated-insights`, `/ssot/insight/...` |
| search indexes and retrievers | `/ssot/search-index`, Machine Learning / AI Models endpoints where available |
| segment lifecycle | `/ssot/segments`, `ConnectApi.CdpSegment` |
| activation lifecycle | `/ssot/activation-targets`, `/ssot/activations` |
| data actions | `/ssot/data-action-targets`, `/ssot/data-actions` |
| deployable metadata promotion | Metadata API and data kits |

## Developer Guide API Selection

| Surface | Use When | Watch For |
| --- | --- | --- |
| Connect REST API | Platform-integrated apps need Data 360 resources, Salesforce auth, metadata, profiles, CIs, identity rulesets, segments, Universal ID lookup, or Query APIs | Use OpenAPI for exact path/schema; validate data space and permissions |
| Apex `ConnectApi` | Apex code must query or manipulate supported Data 360 resources from inside Salesforce | Subset of Connect REST; profile and Universal ID lookup are not generally covered |
| Data 360 API / Direct API | Tenant-direct performance matters and the app does not need Salesforce Platform features | Requires Salesforce token -> Data 360 token exchange and tenant-specific endpoint; not all Connect REST resources are available |
| SOQL | Supported platform query paths against Unified Profile, data source, or DMO objects are enough | Narrower than ANSI SQL / Query APIs; check supported keywords and limitations |
| Metadata API | Moving supported Data 360 metadata between orgs or projects | Coverage is partial; verify metadata coverage, data kit membership, and packageability |

## Operating Rules

- Search the OpenAPI catalog before writing any endpoint or payload.
- Check the proof ledger before creating query, segment, activation target, data action, calculated insight, profile, or search-index payloads.
- Use `sf-docs` when behavior, setup, permission, limit, or data-space handling matters.
- Do not assume MCP dependencies are bundled by `npx skills add`; use the documented direct URLs and local install paths when the runtime does not expose the tools.
- Treat the official DMO catalog as a label directory, not proof of runtime API names. Resolve real object/field names through metadata/profile/query introspection.
- Distinguish query success from segment success. Query SQL can pass while DBT segment creation fails.
- Distinguish Data Graph retrieval context from segment/activation criteria. Use graph context for enrichment, not silent activation logic.
- For data spaces, check whether the call needs a query parameter, token exchange body parameter, SQL/Python connector property, or Apex extra parameter such as `ConnectApi.CdpQuery.queryAnsiSqlV2(input, "dataspace_name")`.
- For Data 360 API / Direct API, plan the two-step OAuth exchange: Salesforce
  access token first, then a Data 360 access token plus tenant-specific endpoint.
  Do not reuse Connect REST auth assumptions blindly.
- Validate governed behavior with a non-admin user when policies, masking, or data spaces affect access.
- Prefer existing `sf` CLI auth, then direct `SF_ACCESS_TOKEN` + `SF_INSTANCE_URL`, then connected-app OAuth.

## Hard-Won Rules

1. Discovery queries can use published Calculated Insights; DBT segment creation should use DMO-native SQL.
2. Consent data that only exists on a `__dll` path is not enough for DBT segment enforcement; harmonize it into a DMO-backed shape.
3. Relative date expressions can be fragile in generated DBT segment SQL; prefer absolute timestamp literals built in code.
4. Segment create responses are not health proof. Verify `MarketSegment` status and member counts.
5. Data action and activation APIs often expose `dataspace` as a later-version parameter; check catalog availability before assuming support.
6. DBT segment REST create uses `includeDbt.models.models[]` as input, but readback returns `includeDbt.models[]`.
7. Approximate segment count can fail with `NOT_ACCEPTABLE` when the org feature is disabled; retry exact count with `preferApproxCount=false`.
8. Data 360 MCP can hold an expired session; if it returns `INVALID_SESSION_ID`, use explicit `sf api request rest --target-org <alias>` for live proof.
9. Data 360 API / Direct API can be the performance-oriented tenant path, but it
   is not the universal API. Segments and identity resolution rulesets remain
   Connect REST / ConnectApi territory unless current docs say otherwise.

## Snippet Patterns

Apex query:
- create `ConnectApi.CdpQueryInput`
- set `input.sql`
- call `ConnectApi.CdpQuery.queryAnsiSqlV2(input)` or data-space overload
- parse `rowData`
- keep SQL ANSI/PostgreSQL style, not SOQL

Apex segment:
- create `ConnectApi.CdpSegmentDbtModelInput`
- attach it to `ConnectApi.CdpSegmentDbtInput`
- attach that to `ConnectApi.CdpSegmentInput`
- call `ConnectApi.CdpSegment.createSegment(input)`
- check returned `marketSegmentId`
- verify `MarketSegment` status and counts

Local SQL validation should use the available org tooling in the current IDE or MCP environment. Prefer explicit target org and data space arguments; do not rely on global CLI state.

## Output Format

Report:

1. auth mode chosen
2. API surface used
3. catalog endpoint/schema found
4. proof ledger evidence or payload used, if available
5. docs consulted when behavior matters
6. payload/snippet/tooling produced
7. data space and governance assumptions
8. live validation or unverified gates

## Doc-Synced Notes

<!-- SF_DOC_SYNC_START:data-spaces-api -->
### Data Spaces in API/Connector Usage (do not guess the mechanism)

_Auto-synced from the local sf-docs cached Salesforce Help export (official docs only).

**Sources (sf-docs cached Help):**
- data.c360_a_using_data_cloud_apis_with_data_spaces.htm — Use Data Cloud APIs with Data Spaces

**Source fingerprint:** `914b475541498c62cea77808`

**Notes:**
- Token exchange: include a body parameter named `dataspace` with the data space name to get a Data 360 token scoped to that data space.
- SQL clients: set a driver/user property named `dataspace` to query in a specific data space.
- Python connector: pass an additional connection parameter named `dataspace` with the data space name.
- Connect APIs: pass the data space name as an extra parameter (example shown in the Help page). Validate per-endpoint support in OpenAPI before assuming it exists everywhere.

<!-- SF_DOC_SYNC_END:data-spaces-api -->

<!-- SF_DOC_SYNC_START:limits-api -->
### API limit gate

_Auto-synced from the local sf-docs cached Salesforce Help export (official docs only).

**Sources (sf-docs cached Help):**
- data.c360_a_limits_and_guidelines.htm — Data 360 Limits and Guidelines | Salesforce Help

**Source fingerprint:** `1ce0aa69b0b275b02c26170b`

**Notes:**
- Treat the captured Limits and Guidelines page as a required source before making durable guidance for this phase.
- Separate soft guidelines from hard limits, and call out when a limit can require an Account Executive request or org-specific validation.
- Before writing reusable API guidance, check the API Guidelines and Limits family and OpenAPI catalog together.
- Do not treat a method/path as production-ready until limits, data space mechanics, permissions, and readback proof are named.
- Relevant limit families currently captured include: General Guidelines and Limits, Activation Guidelines and Limits, AI Models (formerly Einstein Studio) Guidelines and Limits, Calculated Insights Guidelines and Limits, Code Extension Guidelines and Limits, Data Actions Guidelines and Limits, Data Explorer Guidelines and Limits, Data Federation Guidelines and Limits, Data Graphs Guidelines and Limits, Data Ingestion Guidelines and Limits, Data Model Object Guidelines and Limits, Data Shares Guidelines and Limits.

<!-- SF_DOC_SYNC_END:limits-api -->
