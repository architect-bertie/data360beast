# Changelog

All notable changes to data360beast. Versions track `manifest.json.version`.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added
- `tools/validate_proof_compliance.py` lint that asserts every SKILL.md cites
  the four proof contracts (`docs/phase-proof-matrix.json`,
  `docs/beast-preflight.md`, `docs/proof-ledger.md`,
  `docs/data360/limits-source-precedence.md`), forbids the docs-watch
  banned-phrase list, and verifies `references/*.md` and `scripts/*.py`
  pointers resolve.
- `CHANGELOG.md` (this file) at repo root.

### Changed
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
