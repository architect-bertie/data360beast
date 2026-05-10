---
name: sf-datacloud-act
description: >
  Salesforce Data 360 Act phase for activation targets, activations, data
  actions, activation-triggered flows, API activations, and activation
  monitoring. TRIGGER when: the user manages activation targets, activation
  jobs, activation payloads, data action delivery, or downstream activation
  health.
license: MIT
metadata:
  version: "2.0.0"
  author: "Codex"
---

# sf-datacloud-act

Use this skill for the **activation plane**.

Beast references:
- Public operating model: [docs/operating-model.md](../../docs/operating-model.md)
- Developer Guide index: [docs/data360/developer/index.md](../../docs/data360/developer/index.md)
- Public API cookbook: [docs/api-cookbook.md](../../docs/api-cookbook.md)
- Public LLM map: [docs/llms.txt](../../docs/llms.txt)
- For exact Salesforce behavior, fetch official Help/Developer docs on demand with `sf-docs`.
- For endpoint shape, use OpenAPI from the official spec or the user-supplied Swagger before writing payloads.

## Prefer these Connect API families

- `GET/POST/PATCH /ssot/activation-targets`
- `GET/POST/PUT/DELETE /ssot/activations`
- `GET /ssot/activations/:activationId/data`
- `GET/POST /ssot/data-action-targets`
- `GET/POST /ssot/data-actions`

## Rules

- Validate the activation target before debugging the activation job.
- Distinguish segment activation, DMO activation, streaming DMO activation, API activation, and data action orchestration.
- Activation targets store destination authentication and authorization; they are separate from the activation definition/job.
- DMO activation has streaming and batch modes with different destinations and semantics.
- Batch DMO activation supports Profile, Engagement, and Other DMOs, but not Audience DMOs or certain system-generated DMOs.
- BYOL external DMOs must be accelerated for DMO activation.
- Engagement DMO batch activation sends only the last 90 days of records.
- Keep segment creation and downstream activation as separate steps.
- When the user needs external delivery state, inspect the activation target and activation object, not only the segment.
- For activation-triggered flows, document the activation source, payload, flow context, target object, and fault path.
- For data actions, use [sf-datacloud-automation](../sf-datacloud-automation/SKILL.md) for event contract, Flow, webhook, and Platform Event design.
- Monitor activation status, publish status, delivery failures, target auth expiry, rejected rows, and downstream target acceptance.
- Activations, ad audiences, and recurring delivery jobs can affect service
  usage. Validate audience size, publish cadence, target scope, and whether a
  test activation can use a deliberately small sample.
- Treat external target mappings as production contracts. Version them and test them after data model changes.
- Validate access to the Segment On primary key and every underlying DMO/CIO/Data Graph entity used by the activation.
- Do not assume a visible segment can be activated; governed dependent objects can still block activation save or delivery.
- For programmatic payloads, use the OpenAPI endpoint catalog and endpoint search tooling in [sf-datacloud-connectapi](../sf-datacloud-connectapi/SKILL.md).

## Production Gates

1. target authenticated and active
2. segment/DMO source status healthy
3. field mapping validated with sample output
4. consent/governance confirmed
5. test activation delivered to target
6. publish history or activation `LastPublishStatus` checked
7. monitoring and alerting in place
