# Salesforce sf-skills Data 360 Companion

Use this reference when Data360 Beast is installed with the optional Salesforce
`sf-skills` Data 360 companion subset.

## Rule

Beast stays the source-of-truth router. `sf-docs` stays the official-doc path.
The Salesforce companion helps with `sf data360` command execution, readiness
checks, templates, and CLI troubleshooting.

## Approved Upstream Skills

- `data360-orchestrate`
- `data360-connect`
- `data360-prepare`
- `data360-harmonize`
- `data360-segment`
- `data360-activate`
- `data360-query`
- `data360-schema-get`
- `data360-code-extension-generate`

## Source Boundary

Use **Data 360** in Beast-facing guidance. Preserve exact upstream names only
for install paths, package references, or command surfaces.

Do not copy upstream skill bodies into Beast. Use
[`docs/data360/sf-skills-data360-companion.md`](../../../docs/data360/sf-skills-data360-companion.md)
and
[`docs/data360/sf-skills-data360-companion.json`](../../../docs/data360/sf-skills-data360-companion.json)
for the public companion contract.
