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
- If data spaces are involved, confirm where the connection, stream, and resulting DLOs are scoped.
- For external lakehouses, choose the interoperability pattern before creating assets: ingestion for canonical governance, live query for maximum freshness, accelerated query for frequent reads with stale tolerance, file federation for large object-store/open-table workloads, or hybrid for governed core plus fresh edge.
- Capture source-system cost and governance assumptions for federated connections. Query federation can depend on external compute and source-side policies; file federation depends on storage access, table format, partitioning, and Data 360 compute.
- Classify integration path before implementation: built-in Salesforce connector,
  external connector, Ingestion API bulk/streaming, Amazon S3 data stream,
  Salesforce Interactions SDK for web behavior, Engagement Mobile SDK for
  mobile events, MuleSoft, or zero-copy/federation.
- For API-driven ingestion, confirm OAuth scope requirements and whether the
  work is bulk historical load, recurring bulk load, or small-batch streaming.

## Validation gate

Connection work is not done until connector metadata is understood, auth is healthy, schema is discovered or uploaded, the integration pattern is explicit, and the next Data Stream/DLO/federated-query step is clear.
