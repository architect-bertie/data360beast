# Data360 Beast

Salesforce Data 360, made agent-ready.

Data360 Beast is a compact operating kit for teams using Claude, Codex, Cursor,
or another agentic IDE to design, build, and troubleshoot Salesforce Data 360.
It combines an explicit delivery loop, OpenAPI-first API lookup, live-tested
recipes, and clean LLM entry points.

Site: <https://architect-bertie.github.io/data360beast/>

## Agent Quick Start

```bash
npx skills add architect-bertie/data360beast
```

Start with:

- [`skills/data360beast/SKILL.md`](skills/data360beast/SKILL.md) for the agent skill.
- [`AGENTS.md`](AGENTS.md) for repository-wide agent instructions.
- [`docs/llms.txt`](docs/llms.txt) for the public LLM entry point.
- [`docs/agent-manifest.json`](docs/agent-manifest.json) for machine-readable metadata.

## What Is Inside

```text
data360beast/
|-- skills/data360beast/SKILL.md
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
    |-- operating-model.md
    |-- api-cookbook.md
    `-- scorecard.md
```

## What It Does

- Routes work by Data 360 phase: connect, prepare, harmonize, govern, retrieve,
  insight, semantic layer, AI/search, segment, act, and automation.
- Uses official Salesforce docs on demand instead of stale pasted docs.
- Uses OpenAPI shape first for Connect API method, path, params, and schemas.
- Applies live-tested cookbook lessons for query, segment, data action, and
  activation work.
- Requires org validation through status, counts, metadata, data space, and
  readback before treating an answer as proven.

## Public Boundary

This repository intentionally does not publish raw Salesforce Help exports,
generated documentation caches, lab-specific data, tokens, or org metadata. It
publishes the curated operating model and agent entry points.

## Status

Current score: **9.4/10 overall**.

Remaining frontier: external activation destinations and search-index creation
recipes require enabled assets in a live org before promotion into the skill.
