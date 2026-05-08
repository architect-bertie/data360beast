---
name: sf-datacloud-connect
description: >
  Salesforce Data 360 Connect phase for connectors and connection lifecycle.
  TRIGGER when: the user works on connectors, connections, connection schema,
  connection test flows, or source-object discovery.
license: MIT
metadata:
  version: "2.0.0"
  author: "Codex"
---

# sf-datacloud-connect

Use this skill for the **connection plane**.

Beast references:
- Public operating model: [docs/operating-model.md](../../docs/operating-model.md)
- Public API cookbook: [docs/api-cookbook.md](../../docs/api-cookbook.md)
- Public LLM map: [docs/llms.txt](../../docs/llms.txt)
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
2. inspect existing connections
3. test before creating when possible
4. upload or verify schema for ingestion-style connectors
5. hand off to Prepare once the connection is healthy

## Rules

- Prefer REST payload inspection over guessing connector parameters.
- Reuse the OpenAPI catalog through [sf-datacloud-connectapi](../sf-datacloud-connectapi/SKILL.md); Postman is optional comparison only.
- For local development, CLI-auth or direct access token is usually faster than creating a new connected app.
- Review source prerequisites before creating streams. Help docs separate source configuration from stream setup.
- Inspect connector metadata and test the connection before handing off to Prepare.
- If data spaces are involved, confirm where the connection, stream, and resulting DLOs are scoped.

## Validation gate

Connection work is not done until connector metadata is understood, auth is healthy, schema is discovered or uploaded, and the next Data Stream/DLO step is explicit.
