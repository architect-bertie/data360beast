# Salesforce sf-skills Data 360 Companion

Use this reference when Data360 Beast is installed with the optional Salesforce
`sf-skills` Data 360 companion subset.

## Rule

Beast stays the source-of-truth router. `sf-docs` stays the official-doc path.
The Salesforce companion helps with `sf data360` command execution, readiness
checks, templates, and CLI troubleshooting.

## Approved Upstream Skills

- `data360-schema-get`
- `data360-code-extension-generate`

## Retired Companions

Upstream removed `data360-orchestrate`, `data360-connect`, `data360-prepare`,
`data360-harmonize`, `data360-segment`, `data360-activate`, and `data360-query`
in commit `0851d45f78fdfa511bda12446c8cbe7c83c0d352`. They are no longer active
install or execution routes. Existing local copies are left untouched and may
be stale.

Use Beast's `sf-datacloud` specialist for cross-phase work and the matching
`sf-datacloud-*` specialist from [the skill crosswalk](../../../docs/skills.md)
for other phases. Schema retrieval and Code Extension work retain the two
companions above. Retirement does not remove product capabilities or establish
a replacement CLI workflow; execution still requires Beast preflight,
authorization, and operation-specific readback.

## Source Boundary

Use **Data 360** in Beast-facing guidance. Preserve exact upstream names only
for install paths, package references, or command surfaces.

Do not copy upstream skill bodies into Beast. Use
[`docs/data360/sf-skills-data360-companion.md`](../../../docs/data360/sf-skills-data360-companion.md)
and
[`docs/data360/sf-skills-data360-companion.json`](../../../docs/data360/sf-skills-data360-companion.json)
for the public companion contract.
