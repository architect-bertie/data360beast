# Agent Quickstart

Use Data360 Beast when the task touches Salesforce Data 360, Data Cloud, Connect
API, segmentation, activation, governance, search, semantic models, calculated
insights, or org validation.

## Install

```bash
npx skills add architect-bertie/data360beast
```

## Manual Context

If your IDE does not support skill installation, load these files in order:

1. `AGENTS.md`
2. `skills/data360beast/SKILL.md`
3. `docs/llms.txt`
4. The one task-specific doc you need: `operating-model.md`,
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
