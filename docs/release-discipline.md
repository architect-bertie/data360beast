# Release Discipline

Use this checklist before publishing Data360 Beast skill-pack changes.

## Version Rules

- `manifest.json.version` is the source for release versioning.
- `CHANGELOG.md` must describe public-safe changes under `Unreleased` before a
  PR is opened.
- A tagged release should move `Unreleased` content under a dated version
  heading and update comparison links.
- Docs-only changes can stay in `Unreleased`; skill, script, manifest, or
  proof-contract changes should mention the affected surfaces explicitly.

## Required Checks

Run these before push or PR:

```bash
python3 tools/validate_proof_compliance.py
python3 tools/run_beast_evals.py
python3 tools/skill_install_smoke.py
python3 tools/release_readiness.py
python3 tools/mcp_readiness.py --json
python3 tools/audit_indexed_docs.py
```

When a scenario answer set exists, also run:

```bash
python3 tools/run_beast_evals.py --answers-dir eval-answers
```

## Publishing Gate

Before GitHub-heavy work, run:

```bash
tools/github_readiness.sh
```

Treat `gh auth status` as advisory. The readiness script validates API identity,
repo permission, remote access, and credential-helper wiring without printing
secrets.

## Release Notes Contract

Every release note should identify:

- affected skills or docs;
- source type: official docs, OpenAPI, proof ledger, Labs promotion, or tooling;
- proof impact: routing, validation, eval, helper, or readback;
- public-boundary impact;
- migration or install action, if any.
