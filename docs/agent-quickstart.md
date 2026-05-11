# Agent Quickstart

Use Data360 Beast when the task touches Salesforce Data 360, Data Cloud, Connect
API, DMO modeling, segmentation, activation, governance, search, semantic
models, calculated insights, or org validation. Installing the repo gives the
agent the Beast router plus the specialist `sf-datacloud-*` skills.

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
3. `docs/beast-preflight.md` for target org, API version, data space,
   authorization boundary, tools, and proof target
4. `docs/phase-proof-matrix.json` for deterministic specialist routing and
   minimum proof targets
5. `docs/skills.md`
6. `docs/mcp-dependencies.md` if companion MCP tools are missing
7. `docs/data360/help/index.md` or `docs/data360/developer/index.md` when you need to locate official docs quickly
8. `docs/data360/model-gallery-implementation-map.md` when choosing DMOs,
   model grain, relationship paths, or Data Graph shape
9. `docs/data360/rag-search-index-retriever-playbook.md` when designing RAG,
   Agentforce Data Libraries, search indexes, chunking, retrievers, prompt
   grounding, or Flow/Apex retrieval paths
10. `docs/llms.txt`
11. The one task-specific doc you need: `operating-model.md`,
   `proof-ledger.md`, `labs-interface.md`, `scorecard.md`, or a phase-specific
   reference.

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

```text
Use Data360 Beast to map this business use case to the right Data 360 model-gallery subject area, anchor DMO, and relationship path.
```

```text
Use Data360 Beast to design a Data 360 RAG pipeline. Compare ADL and manual setup, choose chunking and retriever filters, then give me the validation plan.
```

## Answer Shape

Prefer this contract:

```text
Preflight
Recommendation
Source path: documented | tested | inferred
Payload/command/query
Validation readback
Caveats
Next proof step
```
