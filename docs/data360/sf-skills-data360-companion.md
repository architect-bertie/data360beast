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
folders, install paths, package metadata, or command surfaces. That is why the
companion installs upstream folder names such as `orchestrating-datacloud` even
though Beast-facing prose says Data 360.

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
| Cross-phase | `sf-datacloud` | `orchestrating-datacloud` |
| Connect | `sf-datacloud-connect` | `connecting-datacloud` |
| Prepare | `sf-datacloud-prepare` | `preparing-datacloud` |
| Harmonize | `sf-datacloud-harmonize` | `harmonizing-datacloud` |
| Segment | `sf-datacloud-segment` | `segmenting-datacloud` |
| Act | `sf-datacloud-act` | `activating-datacloud` |
| Retrieve | `sf-datacloud-retrieve` | `retrieving-datacloud` |
| Retrieve schema | `sf-datacloud-retrieve` | `getting-datacloud-schema` |
| Develop/package | `sf-datacloud` | `developing-datacloud-code-extension` |

## Operating Loop

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
- Version: `1.9.0`
- Commit: `c0deadad628bf8730c27a2782db358f064b1888a`
- Observed: 2026-05-14
