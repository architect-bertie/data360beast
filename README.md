# Data360 Beast

Salesforce Data 360, made agent-ready.

Data360 Beast is an agent-facing execution kit for teams that design, build,
troubleshoot, validate, and improve Salesforce Data 360.
It combines a top-level Beast router, 16 specialist Data 360 skills, an explicit
preflight, a machine-readable proof matrix, OpenAPI-first API lookup,
tested evidence, and clean project-owned agent entry points.

Architecture anchor:

```text
Think with Beast, docs, OpenAPI, and skills.
Act with MCPs, APIs, and CLI.
Prove with readback.
Learn through Labs and the proof ledger.
```

Beast is not only a knowledge system; it is an execution system rooted in
proven knowledge with proof and learning loops. The skill outcome should be
execution-ready for the target org, not just advice.

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
- [`docs/phase-coverage-matrix.json`](docs/phase-coverage-matrix.json) for
  machine-readable coverage by phase, source, proof, helper, and frontier.
- [`docs/operating-model.md`](docs/operating-model.md) for the plain-English
  Think -> Act -> Prove -> Learn architecture and execution outcome contract.
- [`docs/skills.md`](docs/skills.md) for the full specialist skill map.
- [`docs/mcp-dependencies.md`](docs/mcp-dependencies.md) for companion MCP installs (**strongly recommended** — without these the agent cannot fetch official docs on demand or execute live org operations).
- [`docs/data360/sf-skills-data360-companion.md`](docs/data360/sf-skills-data360-companion.md)
  for the optional Salesforce `sf-skills` Data 360 companion subset that adds
  `sf data360` execution playbooks, readiness checks, templates, and CLI
  gotchas after Beast is installed.
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
- [`docs/data360/cost-usage-sizing-contract.md`](docs/data360/cost-usage-sizing-contract.md)
  for qualitative cost and usage sizing.
- [`docs/data360/implementation-foundation.md`](docs/data360/implementation-foundation.md)
  for outcome, org-topology, residency, ethical-data, sandbox, and cross-phase
  proof gates.
- [`docs/data360/deployment-runtime.md`](docs/data360/deployment-runtime.md)
  for portable desired-state planning, execution approval, run journals, and
  certification contracts.
- [`docs/data360/knowledge/claims.json`](docs/data360/knowledge/claims.json)
  for source-backed architectural claims, caveats, proof status, and ownership.
- [`docs/data360/develop-package-deployment-matrix.md`](docs/data360/develop-package-deployment-matrix.md)
  for data kit, packageability, deployment, and readback gates.
- [`docs/data360/code-extension-operating-playbook.md`](docs/data360/code-extension-operating-playbook.md)
  for Code Extension toolchain, package, transform, run, output, log, recovery,
  and migration proof.
- [`docs/data360/mcp-tool-selection.md`](docs/data360/mcp-tool-selection.md)
  for choosing between `sf-docs`, `data360`, `datacloud-mcp-query`, and direct
  `sf` REST calls.
- [`docs/release-discipline.md`](docs/release-discipline.md) for validation and
  publishing discipline.
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
- `datacloud-mcp-query`: <https://github.com/forcedotcom/datacloud-mcp-query>
  for optional retrieve-plane SQL/list/describe work

## Salesforce sf-skills Data 360 Companion

Beast stays the source-of-truth brain: `sf-docs` for current official
Salesforce documentation, OpenAPI/Data 360 MCP/direct REST for API shape and
readback, proof labels for confidence, and Labs for promoted evidence.

Install the optional Salesforce `sf-skills` Data 360 companion subset when the
agent also needs `sf data360` command playbooks, readiness classifiers,
templates, and runtime troubleshooting:

```bash
python3 skills/data360beast/scripts/install_sf_skills_data360_companion.py --dry-run
python3 skills/data360beast/scripts/install_sf_skills_data360_companion.py
```

The installer fetches only the nine approved Data 360-relevant folders from
[`forcedotcom/sf-skills`](https://github.com/forcedotcom/sf-skills). It does
not vendor upstream skill bodies into this repo and refuses to write into VS
Code Agentforce Vibes `globalStorage` or local `node_modules` package folders.

## GitHub Readiness

For Data360 Beast publishing work, use the repo readiness check before commit,
push, or PR automation:

```bash
tools/github_readiness.sh
```

The check validates `gh` API access, repo write permission, git remote access,
and the GitHub credential helper without printing tokens.

## Validation Tools

```bash
python3 tools/validate_proof_compliance.py
python3 tools/run_beast_evals.py
python3 tools/skill_install_smoke.py
python3 tools/release_readiness.py
python3 tools/mcp_readiness.py --json
python3 skills/data360beast/scripts/install_sf_skills_data360_companion.py --dry-run
```

Use `tools/data360_cost_usage_estimator.py <scenario.json>` for qualitative
cost/usage sizing. It produces risk bands and proof questions, not credit or
dollar estimates.

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
|-- skills/data360beast/scripts/install_sf_skills_data360_companion.py
|-- skills/sf-datacloud-connectapi/SKILL.md
|-- skills/sf-datacloud-*/SKILL.md
|-- AGENTS.md
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
    |-- beast-evals.json
    |-- phase-proof-matrix.json
    |-- phase-coverage-matrix.json
    |-- mcp-dependencies.md
    |-- release-discipline.md
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
    |-- implementation-foundation.md
    |-- cost-usage-sizing-contract.md
    |-- develop-package-deployment-matrix.md
    |-- code-extension-operating-playbook.md
    |-- limits-source-precedence.md
    |-- mcp-tool-selection.md
    |-- model-gallery-implementation-map.md
    |-- rag-search-index-retriever-playbook.md
    |-- sf-skills-data360-companion.md
    |-- sf-skills-data360-companion.json
    |-- help/index.md
    `-- developer/index.md
```

## What It Does

- Produces execution-ready paths for authorized, compatible Data 360 orgs after
  preflight confirms org, data space, permissions, available tools, and mutation
  approval.
- Routes work by Data 360 phase: connect, prepare, harmonize, govern, retrieve,
  insight, semantic layer, AI/search, segment, act, and automation.
- Runs a preflight for target org, API version, data space, persona, asset
  lifecycle, authorization boundary, available tools, and proof target.
- Uses a machine-readable proof matrix to pick the specialist skill, required
  source type, minimum proof target, and forbidden assumptions.
- Uses a machine-readable phase coverage matrix to expose source, proof,
  helper, and frontier coverage by phase.
- Uses official Salesforce docs on demand instead of stale pasted docs.
- Publishes public-safe indexes for Salesforce Help and all approved Data 360 Developer Center guide families
  without publishing raw scraped content.
- Audits the indexed Help and Developer pages weekly and uses official Help
  prerendered HTML to capture oversized pages that the standard sf-docs path
  returns as placeholders.
- Uses OpenAPI shape first for Connect API method, path, params, and schemas.
- Documents companion MCP install paths for `sf-docs` and the official Data 360
  MCP server, plus optional `datacloud-mcp-query` for retrieve-plane SQL work.
- Documents and installs an optional Salesforce `sf-skills` Data 360 companion
  subset for `sf data360` execution playbooks, while keeping `sf-docs` as the
  official-doc truth path and Beast as the proof router.
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
- Uses a learning loop: reusable public-safe lessons can strengthen Beast docs,
  specialist skills, and proof ledger entries; scenario-heavy work stays in
  Labs until distilled.
- Adds executable validation helpers for prompt evals, install smoke tests,
  MCP readiness, release readiness, proof compliance, and cost/usage sizing.
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

Current score: **9.9/10 overall evidence maturity** after Phase 3 — Full
Coverage Sweep. The skill pack now distills 64 official Salesforce Help
articles into 38 doc-synced blocks across 17 specialist skills, catalogs
140+ Data 360 connectors, and ships per-topic reference files for the
heaviest doc-synced content so each `SKILL.md` stays context-cheap.

Remaining frontier: external activation destinations and search-index creation
evidence still need enabled assets in a live org before promotion into tested
proof ledger evidence.
