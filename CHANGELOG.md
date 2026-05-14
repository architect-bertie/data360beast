# Changelog

All notable changes to data360beast. Versions track `manifest.json.version`.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added (Operational Hardening)
- Executable Beast eval harness: `docs/beast-evals.json` plus
  `tools/run_beast_evals.py` for deterministic prompt-answer checks around
  endpoint discipline, data spaces, proof separation, RAG troubleshooting,
  governance proof, activation proof, formula syntax, and confidence labels.
- Portable install/layout smoke test: `tools/skill_install_smoke.py`.
- MCP readiness check: `tools/mcp_readiness.py`, covering `sf-docs`,
  `data360`, and optional `datacloud-mcp-query`.
- Machine-readable phase coverage matrix:
  `docs/phase-coverage-matrix.json`.
- Cost and usage sizing contract:
  `docs/data360/cost-usage-sizing-contract.md` plus
  `tools/data360_cost_usage_estimator.py`.
- Develop/package/deploy proof matrix:
  `docs/data360/develop-package-deployment-matrix.md`.
- MCP tool-selection guide:
  `docs/data360/mcp-tool-selection.md`, including the decision to treat
  `forcedotcom/datacloud-mcp-query` as an optional retrieve-plane accelerator,
  not a replacement for `forcedotcom/d360-mcp-server`.
- Release discipline guide and validator:
  `docs/release-discipline.md` plus `tools/release_readiness.py`.

### Changed (Post-Phase-3 De-Clutter)
- Extracted long doc-synced blocks from the four largest skill files into
  per-topic reference files under each skill's `references/` directory,
  keeping `SF_DOC_SYNC_*` markers inside the new files so the doc-watch
  pipeline still locates them. Net `SKILL.md` size dropped by ~734 lines:
  - `sf-datacloud-governance/SKILL.md` 389 → 207 lines (-182). Bodies of
    `govern-and-secure-overview`, `policy-based-governance`,
    `tagging-and-classification`, and `data-spaces-detailed` now live in
    matching `references/<topic>.md` files.
  - `sf-datacloud-automation/SKILL.md` 373 → 138 lines (-235). Bodies of
    `data-cloud-triggered-flows`, `activation-triggered-flows`,
    `flow-orchestrated-activations`, and `flow-creation-editing` moved
    to `references/`. Skill keeps the limit-gate block inline.
  - `sf-datacloud-unstructured-retrieval/SKILL.md` 379 → 255 lines (-124).
    Body of the long `process-content` block moved to
    `references/process-content.md`. Skill keeps `search-index-and-retrievers`
    and `limits-unstructured-search` inline.
  - `sf-datacloud-harmonize/SKILL.md` 314 → 121 lines (-193). Bodies of
    `dmo-and-mapping`, `dmo-relationships`, and
    `identity-resolution-and-graphs` moved to `references/<topic>.md`.
- Compliance lint still passes: 17 skills compliant, 0 failures, 8
  warnings (no change from pre-extraction state).

### Added (Phase 3 — Full Coverage Sweep)
- **Phase 3A:** complete connector catalog. `references/connector-implementation-cards.md`
  expanded from ~18 detailed cards to a full A-Z inventory of 140+ Data 360
  connectors organized by 10 families (Apache, Microsoft/Azure, Google,
  Amazon/AWS, IBM, Oracle, SAP, Salesforce-native, Activation-only,
  Long-tail SaaS), with GA/Beta status, direction, data type, ingestion
  method, and authoritative dev guide URL per connector. Beta-for-Zero-Copy
  split-status entries flagged for Jira Structured, LinkedIn, LinkedIn Ads,
  WordPress, Workday.
- **Phase 3B:** distilled Govern and Secure (7 articles) into
  `sf-datacloud-governance` SKILL.md as four new doc-synced blocks
  (overview, policy-based governance, tagging and classification,
  data-spaces detail). Distilled Connect Data Help-side (5 articles) into
  `sf-datacloud-connect` SKILL.md as `connect-data-help-side` block
  covering Data Sources, Data Streams, Schedules, refresh modes.
- **Phase 3C:** distilled Prepare and Model (7 articles) into
  `sf-datacloud-prepare` SKILL.md as `prepare-and-model` block (cleansing,
  batch + streaming transforms, formula fields). Distilled DMO/mapping
  (8 articles) and identity-resolution/data-graphs (2 articles) into
  `sf-datacloud-harmonize` SKILL.md as three blocks
  (`dmo-and-mapping`, `dmo-relationships`, `identity-resolution-and-graphs`).
- **Phase 3D:** distilled Query and Generate Insights (3 articles) into
  `sf-datacloud-retrieve` SKILL.md as `explore-and-query` block. Distilled
  Insights authoring (3 articles) into `sf-datacloud-calculated-insights`
  SKILL.md as `insights-authoring` block (CI vs Streaming, dimensions,
  measures, aggregate functions).
- **Phase 3E:** distilled Process Content + Use Search (6 articles) into
  `sf-datacloud-unstructured-retrieval` SKILL.md as `process-content` block
  (UDLO/UDMO mapping, chunking strategies, three index types, easy and
  advanced setup, individual retriever creation, downstream consumers).
- **Phase 3F:** distilled Analyze Data into `sf-datacloud-analytics`
  SKILL.md as `analyze-data` block (report types, dashboard limits, KPI
  consumption insights). Distilled Build and Share Functionality / Data
  Kits into `sf-datacloud-metadata-agentic` SKILL.md as
  `data-kits-and-packaging` block (Standard vs DevOps kits, Two-Package
  Rule, packageable components, 2GP workflow).
- **Phase 3G:** distilled About / Get Started / Plan Data Strategy /
  Editions / Lifecycle into `sf-datacloud` router SKILL.md as
  `about-and-get-started` block (orientation-only; deep mechanics remain
  in specialists).

### Changed (Phase 3)
- **Phase 3H:** re-sourced `activation-triggered-flows` and
  `flow-orchestrated-activations` (now `api-activations-and-flow-orchestrated`)
  blocks in `sf-datacloud-automation` SKILL.md from official Help, Trailhead,
  and MuleSoft (Salesforce-owned) sources only. Removed all
  `salesforceblogger.com` citations.
- Removed remaining community-blog citations (`salesforcegeek.in`,
  `davidpalencia.com`) from `sf-datacloud-segment` SKILL.md,
  `sf-datacloud-act` SKILL.md, and
  `sf-datacloud-act/references/activation-target-cards.md` to align with
  the strict-official source policy.
- Skill pack now meets a uniform doc-synced quality bar: every one of the
  16 specialist skills has at least one substantive doc-synced block
  beyond the limit-gate block.

### Added (pre-Phase-3 work in Unreleased)
- `tools/validate_proof_compliance.py` lint that asserts every SKILL.md cites
  the four proof contracts (`docs/phase-proof-matrix.json`,
  `docs/beast-preflight.md`, `docs/proof-ledger.md`,
  `docs/data360/limits-source-precedence.md`), forbids the docs-watch
  banned-phrase list, and verifies `references/*.md` and `scripts/*.py`
  pointers resolve.
- `CHANGELOG.md` (this file) at repo root.

### Changed (pre-Phase-3 work in Unreleased)
- All 14 specialist SKILL.md files now reference the phase proof matrix and
  Beast preflight in their `Beast references` block.
- `docs/data360/docs-watch-operating-model.md` pipeline gains a step 10 that
  invokes the new compliance lint before commit.
- `docs/data360/developer/skill-update-synthesis.md` preamble points at the
  public Developer Guide index; the local sf-docs cache references move into
  a maintainer-only footer.
- `skills/data360beast/SKILL.md` Labs boundary text avoids the `raw payload`
  banned phrase, aligning with `manifest.json.labs.purpose`.

## [1.4.0] - 2026-05-12

### Added
- `docs/data360/limits-source-precedence.md` defining current-Data-360-first
  answering hierarchy with Data Services Billable Usage Types follow-through
  and explicit legacy CDP scoping.
- `tools/github_readiness.sh` publishing gate (origin remote, write
  permission, default branch, credential helper).

### Changed
- Beast operating model and proof ledger refocused around proof contracts,
  preflight, and the 12-phase matrix.
- Project-owned agent surface cleanup: removed legacy tool-specific root
  shims; `manifest.json`, `AGENTS.md`, and `llms.txt` are now the single
  governance triad.

## [1.3.0] - 2026-05-11

### Added
- RAG/search-index/retriever depth: `docs/data360/rag-search-index-retriever-playbook.md`
  and the expanded `sf-datacloud-unstructured-retrieval` SKILL.md.
- Beast proof routing: `docs/phase-proof-matrix.json`, `docs/proof-ledger.md`,
  `docs/beast-preflight.md`, `docs/beast-evals.md`, `docs/labs-interface.md`.

## [1.2.0] - 2026-05-11

### Added
- `docs/data360/model-gallery-implementation-map.md` translating the 14 public
  Salesforce Data Model Gallery diagrams into anchor-DMO and grain guidance
  for harmonize work.

## [1.1.0] - 2026-05-08 to 2026-05-10

### Added
- Full 16-specialist Data 360 skill pack publication.
- `docs/mcp-dependencies.md` (sf-docs and data360 MCP install guides) and
  `docs/data360/interoperability-decision-map.md`.
- `docs/data360/architecture-engine-map.md` engine-aware triage.
- `docs/data360/help/index.md` (77 Help pages) and
  `docs/data360/developer/index.md` (23 Developer Guide pages).
- Data 360 formula field syntax guidance in `sf-datacloud-prepare`.

## [1.0.0] - 2026-05-08

### Added
- Initial agent-ready release: top-level `data360beast` Beast router skill,
  GitHub Pages site, README, manifest, and licensing.

[Unreleased]: https://github.com/architect-bertie/data360beast/compare/main...HEAD
[1.4.0]: https://github.com/architect-bertie/data360beast/releases/tag/v1.4.0
[1.3.0]: https://github.com/architect-bertie/data360beast/releases/tag/v1.3.0
[1.2.0]: https://github.com/architect-bertie/data360beast/releases/tag/v1.2.0
[1.1.0]: https://github.com/architect-bertie/data360beast/releases/tag/v1.1.0
[1.0.0]: https://github.com/architect-bertie/data360beast/releases/tag/v1.0.0
