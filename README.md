# Data360 Beast

Salesforce Data 360, made agent-ready.

Data360 Beast is a portable skill pack for teams using Claude, Codex, Cursor,
or another agentic IDE to design, build, and troubleshoot Salesforce Data 360.
It combines a top-level Beast router, 16 specialist Data 360 skills, an explicit
delivery loop, OpenAPI-first API lookup, live-tested recipes, and clean LLM
entry points.

Site: <https://architect-bertie.github.io/data360beast/>

## Agent Quick Start

```bash
npx skills add architect-bertie/data360beast
```

Start with:

- [`skills/data360beast/SKILL.md`](skills/data360beast/SKILL.md) for the agent skill.
- [`docs/skills.md`](docs/skills.md) for the full specialist skill map.
- [`docs/mcp-dependencies.md`](docs/mcp-dependencies.md) for optional companion MCP installs.
- [`AGENTS.md`](AGENTS.md) for repository-wide agent instructions.
- [`docs/llms.txt`](docs/llms.txt) for the public LLM entry point.
- [`docs/agent-manifest.json`](docs/agent-manifest.json) for machine-readable metadata.

## Companion MCP Services

The skill pack is intentionally portable and does not vendor local MCP servers.
For docs-on-demand and live org work, install the companion services documented
in [`docs/mcp-dependencies.md`](docs/mcp-dependencies.md):

- `sf-docs`: <https://github.com/kvirtue123/sf-docs-mcp>
- `data360`: <https://github.com/forcedotcom/d360-mcp-server>

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
`-- docs/
    |-- index.html
    |-- llms.txt
    |-- llms-full.txt
    |-- agent-manifest.json
    |-- agent-quickstart.md
    |-- mcp-dependencies.md
    |-- skills.md
    |-- operating-model.md
    |-- api-cookbook.md
    |-- scorecard.md
    `-- data360/
        |-- architecture-engine-map.md
        `-- interoperability-decision-map.md
```

## What It Does

- Routes work by Data 360 phase: connect, prepare, harmonize, govern, retrieve,
  insight, semantic layer, AI/search, segment, act, and automation.
- Uses official Salesforce docs on demand instead of stale pasted docs.
- Uses OpenAPI shape first for Connect API method, path, params, and schemas.
- Documents companion MCP install paths for `sf-docs` and the official Data 360
  MCP server.
- Applies live-tested cookbook lessons for query, segment, data action, and
  activation work.
- Requires org validation through status, counts, metadata, data space, and
  readback before treating an answer as proven.

## Public Boundary

This repository intentionally does not publish raw Salesforce Help exports,
generated documentation caches, lab-specific data, tokens, or org metadata. It
publishes the curated operating model and agent entry points.

## Status

Current score: **9.6/10 overall** after publishing the full specialist skill pack.

Remaining frontier: external activation destinations and search-index creation
recipes require enabled assets in a live org before promotion into the skill.
