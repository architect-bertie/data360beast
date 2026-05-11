# Codex Instructions

Use `$data360beast` for Salesforce Data 360 and Data Cloud work, then route to
the matching `sf-datacloud-*` specialist skill when the task is phase-specific.

Operational defaults:

- Run `docs/beast-preflight.md` before non-trivial work to capture target org,
  API version, data space, persona, lifecycle, authorization boundary, tools,
  and proof target.
- Use `docs/phase-proof-matrix.json` to choose specialist skill, source type,
  proof target, and forbidden assumptions.
- Prefer explicit `--target-org` or org alias inputs over global CLI state.
- Prefer explicit data space selection over implicit default behavior.
- Use OpenAPI or official docs before constructing Connect API payloads.
- Use `docs/mcp-dependencies.md` when `sf-docs` or `data360` MCP tools are
  missing from the local runtime.
- Use `docs/data360/rag-search-index-retriever-playbook.md` for RAG,
  Agentforce Data Libraries, search indexes, chunking, retrievers, prompt
  grounding, Flow/Apex retrieval orchestration, or RAG troubleshooting.
- Validate create/update operations with readback by returned ID, status, count,
  or metadata.
- Keep generated public docs short and agent-ingestible.

When editing this repo, do not stage ignored local knowledge exports, generated
docs caches, raw specs, lab metadata, or local tooling unless the user
explicitly asks to publish them.
