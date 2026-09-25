# Salesforce sf-skills Data 360 Companion

Data360 Beast is the Data 360 source-of-truth brain and execution router.
Salesforce
[`forcedotcom/sf-skills`](https://github.com/forcedotcom/sf-skills) can be
installed beside Beast as a Data 360 execution and debugging companion.

This companion is intentionally a **Data 360-only subset**. It does not install
the full Salesforce skill library unless the user explicitly asks for that
outside the Beast install path.

## Authority Rules

- Beast owns source hierarchy, proof labels, official-doc routing, limits
  precedence, OpenAPI discipline, public-safe Labs promotion, and confidence.
- `sf-docs` remains the official-doc path for current Salesforce Help and
  Developer documentation.
- The Salesforce `sf-skills` companion helps plan practical `sf data360`
  command workflows, readiness checks, templates, and CLI gotchas.
- Actual org actions happen through approved CLI, MCP, API, metadata, or helper
  tools after Beast preflight confirms authorization.
- Do not treat `forcedotcom/sf-skills` as official Data 360 documentation.
- Do not vendor upstream `sf-skills` bodies into this repo.

## Naming Policy

Use **Data 360** in Beast-facing docs, UI, manifests, and guidance.

Keep upstream names unchanged only when referencing exact Salesforce skill
folders, install paths, package metadata, or command surfaces. Current upstream
Data 360 companion folders use the `data360-*` domain-first convention.

## Install

Install Data360 Beast first:

```bash
npx skills add architect-bertie/data360beast
```

Then install the Data 360 companion subset:

```bash
python3 skills/data360beast/scripts/install_sf_skills_data360_companion.py
```

Preview without writing:

```bash
python3 skills/data360beast/scripts/install_sf_skills_data360_companion.py --dry-run
```

The installer writes to `$CODEX_HOME/skills` when `CODEX_HOME` is set, or
`$HOME/.codex/skills` otherwise. It refuses to write into the VS Code
Agentforce Vibes extension package or local `node_modules` package folders.

## Approved Companion Skills

| Beast phase | Beast specialist | Upstream companion skill |
| --- | --- | --- |
| Retrieve schema | `sf-datacloud-retrieve` | `data360-schema-get` |
| Develop/package | `sf-datacloud` | `data360-code-extension-generate` |

## Operating Loop

Upstream removed `data360-orchestrate`, `data360-connect`, `data360-prepare`,
`data360-harmonize`, `data360-segment`, `data360-activate`, and `data360-query`
in commit `0851d45f78fdfa511bda12446c8cbe7c83c0d352`. These are recorded as
retired in the JSON contract and are no longer installed or required by drift
checks. Existing local copies are left untouched and may be stale. Beast's
own phase specialists remain available; this change does not remove Salesforce
product capabilities or establish a replacement CLI workflow.

Use the same four layers as Beast:

1. **Think** with Beast preflight, phase routing, `sf-docs`, OpenAPI, Beast
   specialists, and the matching Salesforce `sf-skills` companion guidance.
2. **Act** with approved MCP, API, CLI, metadata, or helper tools only after
   the org, data space, permissions, tools, and mutation approval are clear.
3. **Prove** with returned ID, status, count, metadata, query result, log,
   event, or delivery signal.
4. **Learn** by promoting only distilled public-safe evidence into Beast; keep
   scenario bodies and org-connected experiments in Labs.

The companion should help produce an execution-ready path for an authorized,
compatible Data 360 org. If authorization, feature availability, permissions,
or required tools are missing, stop with a blocked-with-reason result instead
of guessing.

## Upstream Watch

The weekly docs watch should check
[`forcedotcom/sf-skills`](https://github.com/forcedotcom/sf-skills) for drift
in the approved companion skills only. Update
[`sf-skills-data360-companion.json`](sf-skills-data360-companion.json) and this
document when upstream changes affect install, routing, command behavior,
templates, readiness checks, or gotchas.

Current observed upstream:

- Repository: <https://github.com/forcedotcom/sf-skills>
- Package: `@salesforce/afv-skills`
- Version: `1.58.0`
- Commit: `d4a9aa448c7b743c1f1da41f41aa9723a6621232`
- Observed: 2026-09-25
