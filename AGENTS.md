# Agent Instructions

Use this repository as an agent-facing operating kit for Salesforce Data 360
work. The goal is field-ready answers with a proof path, not a static mirror of
Salesforce documentation.

## Start Here

1. Load `skills/data360beast/SKILL.md`.
2. Run `docs/beast-preflight.md` for non-trivial work: target org, API version,
   data space, persona, asset lifecycle, authorization boundary, available
   tools, and proof target.
3. Use `docs/phase-proof-matrix.json` to select the specialist skill, required
   sources, minimum proof, and forbidden assumptions.
4. Use `docs/skills.md` to route into the specialist `sf-datacloud-*` skills.
5. Use `docs/mcp-dependencies.md` to install companion MCP servers when docs-on-demand or live Data 360 operations are needed.
6. Use `docs/data360/help/index.md` and `docs/data360/developer/index.md` for public-safe maps of indexed official docs.
7. Use `docs/data360/rag-search-index-retriever-playbook.md` for RAG, search index, chunking, retriever, and prompt-grounding work.
8. Use `docs/llms.txt` for a compact public map.
9. Use `docs/agent-manifest.json` when a machine-readable entry point is easier.
10. Use `docs/operating-model.md`, `docs/api-cookbook.md`, and
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
