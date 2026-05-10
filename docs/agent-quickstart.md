# Agent Quickstart

Use Data360 Beast when the task touches Salesforce Data 360, Data Cloud, Connect
API, segmentation, activation, governance, search, semantic models, calculated
insights, or org validation. Installing the repo gives the agent the Beast
router plus the specialist `sf-datacloud-*` skills.

## Install

```bash
npx skills add architect-bertie/data360beast
```

## Companion MCP Servers

Install the skill pack first. Then use
[`docs/mcp-dependencies.md`](mcp-dependencies.md) when the task needs:

- official Salesforce docs through `sf-docs`
- live Data 360 org operations through the `data360` MCP server

Direct sources:

- `sf-docs`: https://github.com/kvirtue123/sf-docs-mcp
- `data360`: https://github.com/forcedotcom/d360-mcp-server

## Manual Context

If your IDE does not support skill installation, load these files in order:

1. `AGENTS.md`
2. `skills/data360beast/SKILL.md`
3. `docs/skills.md`
4. `docs/mcp-dependencies.md` if companion MCP tools are missing
5. `docs/data360/help/index.md` or `docs/data360/developer/index.md` when you need to locate official docs quickly
6. `docs/llms.txt`
7. The one task-specific doc you need: `operating-model.md`,
   `api-cookbook.md`, or `scorecard.md`.

## Good Starting Prompts

```text
Use Data360 Beast to design a Data 360 segment and activation flow. Separate documented, tested, and inferred parts.
```

```text
Use Data360 Beast to find the Connect API payload shape for this task, then give me the validation readback plan.
```

```text
Use Data360 Beast to review this Data 360 architecture and identify missing proof points.
```

## Answer Shape

Prefer this contract:

```text
Recommendation
Source path: documented | tested | inferred
Payload/command/query
Validation readback
Caveats
Next proof step
```
