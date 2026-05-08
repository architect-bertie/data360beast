# Codex Instructions

Use `$data360beast` for Salesforce Data 360 and Data Cloud work.

Operational defaults:

- Prefer explicit `--target-org` or org alias inputs over global CLI state.
- Prefer explicit data space selection over implicit default behavior.
- Use OpenAPI or official docs before constructing Connect API payloads.
- Validate create/update operations with readback by returned ID, status, count,
  or metadata.
- Keep generated public docs short and agent-ingestible.

When editing this repo, do not stage ignored local knowledge exports under
`docs/data360/` or local tooling under `tools/` unless the user explicitly asks
to publish them.
