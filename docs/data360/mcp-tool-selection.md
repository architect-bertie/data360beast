# Data 360 MCP Tool Selection

Use this guide when choosing **action and proof tools** for Data360 Beast.
Thinking happens first with Beast preflight, official docs, OpenAPI, specialist
skills, and optional Salesforce `sf-skills` companion guidance. MCPs, APIs, and
CLI commands act only after the org, data space, permissions, tools, and
mutation approval are clear.

The repo does not vendor MCP servers; install and configure them locally when
the proof target requires them.

## Recommendation

| Need | Preferred Tool |
| --- | --- |
| Fresh official Salesforce Help or Developer docs | `sf-docs` |
| Broad Data 360 Connect API operations, payload examples, and API families | `data360` (`forcedotcom/d360-mcp-server`) |
| Fast Query SQL, list tables, and describe table operations | `datacloud-mcp-query` (`forcedotcom/datacloud-mcp-query`) |
| One-off REST call with existing org auth | `sf api request rest --target-org <alias>` |
| Choosing `sf data360` command playbooks, readiness checks, templates, and CLI gotchas before action | Salesforce `sf-skills` Data 360 companion subset |

The Salesforce `sf-skills` companion is not an MCP server and does not replace
`sf-docs`. Use it in the Think layer after Beast phase routing when the task
needs execution guidance for `sf data360` command workflows. The actual action
still happens through CLI, MCP, API, metadata, or helper tools. See
[`sf-skills-data360-companion.md`](sf-skills-data360-companion.md).

## `datacloud-mcp-query` Evaluation

Repository: <https://github.com/forcedotcom/datacloud-mcp-query>

As of 2026-05-14, GitHub metadata shows:

- owner: `forcedotcom`
- license: Apache-2.0
- default branch: `main`
- latest observed commit: `76e7664`
- latest observed push: 2026-04-20
- README-advertised tools: `query`, `list_tables`, and `describe_table`
- README-advertised auth: `SF_ORG_ALIAS` through Salesforce CLI, or OAuth PKCE
  with `SF_CLIENT_ID` and `SF_CLIENT_SECRET`
- open PRs: two older PRs, including security-fix and gRPC/token-exchange work

Decision: **use it as an optional query-plane accelerator, not as a replacement
for `d360-mcp-server`.**

Why:

- It is useful for SQL discovery loops: query, list tables, and describe table.
- It aligns with the retrieve phase and can be easier than broad API wrappers
  when the task is only Data 360 SQL/metadata discovery.
- It does not cover the full Connect API surface needed for segments,
  activations, data actions, search indexes, connector lifecycle, or payload
  examples.
- The open PRs and recent async-crash fix mean agents should stay
  version-aware and avoid assuming every runtime/client mode is stable.

## Install Posture

`datacloud-mcp-query` is recommended when:

- the user repeatedly runs Query SQL or table metadata probes;
- a lab or sandbox has stable `sf` CLI auth;
- the task needs fast live readback without broader API mutation.

It is optional when:

- the task is docs-only;
- `data360` MCP already provides the needed operation;
- the user is doing activation, segment, connector, or data-action payload work.

## Proof Rules

- Always pass or state the target org alias.
- Always state the data space assumption.
- Treat query success as retrieve-plane proof only.
- Do not use Query SQL proof to claim transform, segment, activation,
  analytics, or orchestration health.
- If the server crashes or returns session/auth errors, fall back to explicit
  `sf` CLI REST calls or the broader `data360` MCP and label the proof path.
