# Agent Instructions

Use this repository as an agent-facing operating kit for Salesforce Data 360
work. The goal is field-ready answers with a proof path, not a static mirror of
Salesforce documentation.

## Start Here

1. Load `skills/data360beast/SKILL.md`.
2. Use `docs/skills.md` to route into the specialist `sf-datacloud-*` skills.
3. Use `docs/mcp-dependencies.md` to install companion MCP servers when docs-on-demand or live Data 360 operations are needed.
4. Use `docs/llms.txt` for a compact public map.
5. Use `docs/agent-manifest.json` when a machine-readable entry point is easier.
6. Use `docs/operating-model.md`, `docs/api-cookbook.md`, and
   `docs/scorecard.md` only when the task needs those details.

## Source Order

1. User-provided org, files, target API version, and target data space.
2. Official Salesforce docs fetched on demand.
3. User-supplied or locally available Data 360 Connect API OpenAPI spec.
4. Data360 Beast cookbook and scorecard.
5. Live org validation, when authorized.

## Rules

- Do not treat this repository as official Salesforce documentation.
- Do not hallucinate endpoint paths, fields, limits, or permissions.
- Do not publish or request raw Salesforce Help caches, tokens, org metadata, or
  customer data.
- Do not assume MCP servers are bundled with this repo. If `sf-docs` or
  `data360` is missing, use `docs/mcp-dependencies.md` for the install source
  and keep credentials local.
- If live validation is not available, label the answer as inferred or
  documentation-derived.
- Prefer concise, actionable outputs: source used, payload or command, expected
  readback, and known caveats.
