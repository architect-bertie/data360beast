# Data360 Beast

Salesforce Data 360, made agent-ready.

Data360 Beast is a portable skill pack for teams using Claude, Codex, Cursor,
or another agentic IDE to design, build, and troubleshoot Salesforce Data 360.
It combines a top-level Beast router, 16 specialist Data 360 skills, an explicit
preflight, a machine-readable proof matrix, OpenAPI-first API lookup,
tested evidence, and clean LLM entry points.

Site: <https://architect-bertie.github.io/data360beast/>

## Agent Quick Start

```bash
npx skills add architect-bertie/data360beast
```

Start with:

- [`skills/data360beast/SKILL.md`](skills/data360beast/SKILL.md) for the agent skill.
- [`docs/beast-preflight.md`](docs/beast-preflight.md) for the target-org,
  data-space, tool, authorization, and proof preflight.
- [`docs/phase-proof-matrix.json`](docs/phase-proof-matrix.json) for the
  machine-readable phase, source, proof, and forbidden-assumption matrix.
- [`docs/skills.md`](docs/skills.md) for the full specialist skill map.
- [`docs/mcp-dependencies.md`](docs/mcp-dependencies.md) for optional companion MCP installs.
- [`docs/data360/help/index.md`](docs/data360/help/index.md) and
  [`docs/data360/developer/index.md`](docs/data360/developer/index.md) for
  public-safe official doc indexes.
- [`docs/data360/model-gallery-implementation-map.md`](docs/data360/model-gallery-implementation-map.md)
  for public Data 360 model-gallery learnings, anchor DMOs, relationship paths,
  grain guidance, and live implementation traps.
- [`docs/data360/limits-source-precedence.md`](docs/data360/limits-source-precedence.md)
  for the current Data 360 limits-first rule, Data Services usage follow-through,
  and legacy CDP comparison boundary.
- [`docs/data360/rag-search-index-retriever-playbook.md`](docs/data360/rag-search-index-retriever-playbook.md)
  for RAG architecture, Agentforce Data Libraries, search-index field roles,
  chunking, hybrid/vector search, retriever filters, prompt grounding, and
  troubleshooting.
- [`docs/data360/docs-watch-operating-model.md`](docs/data360/docs-watch-operating-model.md)
  for the weekly official-doc refresh, oversized Help fallback, audit, skill
  sync, and publishing workflow.
- [`docs/proof-ledger.md`](docs/proof-ledger.md) for public-safe evidence,
  caveats, confidence labels, and promotion status.
- [`docs/labs-interface.md`](docs/labs-interface.md) for the boundary between
  this operating-model repo and
  [`data360beast-labs`](https://github.com/architect-bertie/data360beast-labs).
- [`AGENTS.md`](AGENTS.md) for repository-wide agent instructions.
- [`docs/llms.txt`](docs/llms.txt) for the public LLM entry point.
- [`docs/agent-manifest.json`](docs/agent-manifest.json) for machine-readable metadata.

## Companion MCP Services

The skill pack is intentionally portable and does not vendor local MCP servers.
For docs-on-demand and live org work, install the companion services documented
in [`docs/mcp-dependencies.md`](docs/mcp-dependencies.md):

- `sf-docs`: <https://github.com/kvirtue123/sf-docs-mcp>
- `data360`: <https://github.com/forcedotcom/d360-mcp-server>

## GitHub Readiness

For Data360 Beast publishing work, use the repo readiness check before commit,
push, or PR automation:

```bash
tools/github_readiness.sh
```

The check validates `gh` API access, repo write permission, git remote access,
and the GitHub credential helper without printing tokens.

## Full Skill Pack

The repo now ships the Beast router plus specialist skills:

- `data360beast`: top-level router and proof contract.
- `sf-datacloud`: cross-phase orchestration.
- `sf-datacloud-connectapi`: Connect REST API, Apex ConnectApi, OpenAPI lookup.
- `sf-datacloud-connect`: connectors and connections.
- `sf-datacloud-prepare`: data streams, DLOs, transforms.
- `sf-datacloud-harmonize`: DMOs, mappings, identity, data graphs.
- `sf-datacloud-governance`: data spaces, access, policies, masking.
- `sf-datacloud-retrieve`: SQL, profile APIs, metadata lookup.
- `sf-datacloud-calculated-insights`: calculated and streaming insight SQL.
- `sf-datacloud-segment`: segments, counts, publish proof.
- `sf-datacloud-act`: activations and data actions.
- `sf-datacloud-automation`: events, flows, and data actions.
- `sf-datacloud-semantic-layer`: semantic models and metrics.
- `sf-datacloud-ai-models`: AI models and model outputs.
- `sf-datacloud-unstructured-retrieval`: search indexes and retrievers.
- `sf-datacloud-analytics`: reports, dashboards, and analytics.
- `sf-datacloud-metadata-agentic`: metadata semantics for agents.

## What Is Inside

```text
data360beast/
|-- skills/data360beast/SKILL.md
|-- skills/sf-datacloud-connectapi/SKILL.md
|-- skills/sf-datacloud-*/SKILL.md
|-- AGENTS.md
|-- CLAUDE.md
|-- CODEX.md
|-- manifest.json
|-- llms.txt
|-- tools/github_readiness.sh
`-- docs/
    |-- index.html
    |-- llms.txt
    |-- llms-full.txt
    |-- agent-manifest.json
    |-- agent-quickstart.md
    |-- beast-preflight.md
    |-- beast-evals.md
    |-- phase-proof-matrix.json
    |-- mcp-dependencies.md
    |-- skills.md
    |-- operating-model.md
    |-- proof-ledger.md
    |-- labs-interface.md
    |-- api-cookbook.md
    |-- scorecard.md
    `-- data360/
    |-- architecture-engine-map.md
    |-- interoperability-decision-map.md
    |-- docs-watch-operating-model.md
    |-- limits-source-precedence.md
    |-- model-gallery-implementation-map.md
    |-- rag-search-index-retriever-playbook.md
    |-- help/index.md
    `-- developer/index.md
```

## What It Does

- Routes work by Data 360 phase: connect, prepare, harmonize, govern, retrieve,
  insight, semantic layer, AI/search, segment, act, and automation.
- Runs a preflight for target org, API version, data space, persona, asset
  lifecycle, authorization boundary, available tools, and proof target.
- Uses a machine-readable proof matrix to pick the specialist skill, required
  source type, minimum proof target, and forbidden assumptions.
- Uses official Salesforce docs on demand instead of stale pasted docs.
- Publishes public-safe indexes for 77 Help pages and 23 Developer Guide pages
  without publishing raw scraped content.
- Audits the indexed Help and Developer pages weekly and uses official Help
  prerendered HTML to capture oversized pages that the standard sf-docs path
  returns as placeholders.
- Uses OpenAPI shape first for Connect API method, path, params, and schemas.
- Documents companion MCP install paths for `sf-docs` and the official Data 360
  MCP server.
- Captures public Data 360 model-gallery patterns across 14 diagrams so agents
  choose the right DMO anchor, grain, and relationship path before building.
- Captures public-facing Data 360 RAG guidance from a 45-page Salesforce PDF so
  agents can design ADL/manual retrieval, search indexes, chunking, retrievers,
  prompt grounding, Flow/Apex fallbacks, and debug paths with a clear mental
  model.
- Applies tested proof ledger evidence for query, segment, data action, and
  activation work.
- Requires org validation through status, counts, metadata, data space, and
  readback before treating an answer as proven.
- Keeps golden scenarios, synthetic journeys, raw payload experiments, traces,
  and future cookbook candidates in
  [`data360beast-labs`](https://github.com/architect-bertie/data360beast-labs);
  Beast promotes only distilled, public-safe proof ledger evidence.

## Public Boundary

This repository intentionally does not publish raw Salesforce Help exports,
generated documentation caches, lab-specific data, raw Labs payload dumps,
tokens, or org metadata. It publishes the curated operating model, proof ledger,
and agent entry points.

## Status

Current score: **9.8/10 overall evidence maturity** after adding the
RAG/search-index/retriever playbook, preflight contract, phase proof matrix, and
lightweight Beast evals.

Remaining frontier: external activation destinations and search-index creation
evidence still need enabled assets in a live org before promotion into tested
proof ledger evidence.
