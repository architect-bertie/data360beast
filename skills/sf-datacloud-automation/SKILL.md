---
name: sf-datacloud-automation
description: >
  Salesforce Data 360 automation with data actions, data action targets,
  DataObjectDataChgEvent, Data Cloud-triggered flows, activation-triggered
  flows, API activations, Flow orchestration, and event payload design. TRIGGER
  when: the user creates or debugs Data 360 triggered automation or downstream
  flows from DMO, calculated insight, engagement, segment, activation, or data
  action events.
license: MIT
metadata:
  version: "1.0.0"
  author: "architect-bertie"
---

# sf-datacloud-automation

Use this skill for the **Data 360 event automation plane**.

Beast references:
- Beast preflight: [docs/beast-preflight.md](../../docs/beast-preflight.md)
- Phase proof matrix: [docs/phase-proof-matrix.json](../../docs/phase-proof-matrix.json)
- Public operating model: [docs/operating-model.md](../../docs/operating-model.md)
- Proof ledger: [docs/proof-ledger.md](../../docs/proof-ledger.md)
- Public LLM map: [docs/llms.txt](../../docs/llms.txt)
- Limits source precedence: [docs/data360/limits-source-precedence.md](../../docs/data360/limits-source-precedence.md)
- For exact Salesforce behavior, fetch official Help/Developer docs on demand with `sf-docs`.
- For endpoint shape, use OpenAPI from the official spec or the user-supplied Swagger before writing payloads.

## Production Workflow

1. Choose the automation source:
   - data action on DMO or calculated insight change
   - streaming insight data action
   - segment-triggered flow
   - activation-triggered flow
   - API activation invoked from Flow
   - platform event subscriber
   - webhook subscriber
2. Choose the target:
   - Salesforce Platform Event / Flow
   - Marketing Cloud Engagement
   - webhook
   - supported activation target
3. Design the payload:
   - stable identifiers
   - minimal PII
   - idempotency key
   - event timestamp
   - source object and data space
   - correlation ID
   - selected data graph enrichment when allowed
4. Define trigger conditions and throttling before turning it on.
5. Build the Flow with fault paths, duplicate handling, and replay-safe logic.
6. Test with positive, negative, duplicate, late, and permission-denied cases.
7. Monitor delivery, failures, downstream retries, and usage.

## Rules

- Keep segment creation, segment publish, activation, and downstream flow separate in the architecture.
- Data actions are near-real-time event orchestration; activations are audience/data delivery.
- Data actions monitor DMO and CIO changes and publish to Salesforce Platform Event, Marketing Cloud Engagement, or webhook targets.
- Salesforce Platform Event data action targets publish the standard `DataObjectDataChgEvent`.
- Flow automations can chain ingestion, segmentation, activation, identity resolution, and calculated insights; keep each status gate explicit.
- Use data graph attributes for payload enrichment only when governance and access checks permit it.
- Webhook targets need secret validation and retry/idempotency design.
- Do not put raw profile IDs, email addresses, phone numbers, or addresses into external payloads unless explicitly approved.
- API activations are useful when Flow must trigger an activation independent of a segment publish schedule.
- For scheduled high-scale flows, document that policies can be captured at flow creation and RLS is not enforced on scheduled trigger execution.
- Copy/enrichment-style automations can run in system context; secure the target CRM objects and fields separately.
- Use control events for monitoring: Data Stream import status, MarketSegment status/publish status, Activation publish status, CI run status, Identity Resolution counts, metadata change events, and SearchIndexJobStatusEvent.

## Validation Gates

- Data action or activation target is active and authenticated.
- The exact event payload is captured and documented.
- Flow runs in the correct context and has object/field permissions.
- Duplicate event handling is tested.
- External target confirms receipt and signature/secret validation.
- Failure alerting exists.

## Handoffs

- Activation target setup and activation jobs -> [sf-datacloud-act](../sf-datacloud-act/SKILL.md)
- Flow implementation -> `sf-flow` companion skill when available
- Integration/webhook security -> `sf-integration` companion skill when available
- Data graph enrichment -> [sf-datacloud-harmonize](../sf-datacloud-harmonize/SKILL.md)
- Governance, masking, RLS, and policy context -> [sf-datacloud-governance](../sf-datacloud-governance/SKILL.md)

## Output Format

Report:

1. trigger source
2. target
3. payload contract
4. flow/event architecture
5. permissions and governance
6. test cases
7. monitoring and retry plan

## Doc-Synced Notes

### Extended Doc-Synced References

Heavy flow-pattern detail lives in companion reference files. Pull these
when the user is designing or debugging a specific flow shape:

- [references/data-cloud-triggered-flows.md](references/data-cloud-triggered-flows.md) —
  per-record DMO/CIO trigger pattern, invocable actions, end-to-end
  example, near-real-time constraints.
- [references/activation-triggered-flows.md](references/activation-triggered-flows.md) —
  segment-publish / batch-DMO trigger, three-part Activation Target +
  Activation Setup + Flow model, MuleSoft vs External Services
  integration architecture, Win-Back example.
- [references/api-activations-and-orchestration.md](references/api-activations-and-orchestration.md) —
  API Activation target type, multi-channel orchestration pattern,
  re-engagement / onboarding / cart abandonment use cases, Journey
  Builder relationship.
- [references/flow-creation-editing.md](references/flow-creation-editing.md) —
  Flow Builder navigation, core elements table, version management,
  Data 360 flow naming and testing best practices.

<!-- SF_DOC_SYNC_START:limits-data-actions -->
### Data action and event limit gate

_Auto-synced from the local sf-docs cached Salesforce Help export (official docs only).

**Sources (sf-docs cached Help):**
- data.c360_a_limits_and_guidelines.htm (2026-05-11T20:20:31.057Z) — Data 360 Limits and Guidelines

**Notes:**
- Treat the captured Limits and Guidelines page as a required source before making durable guidance for this phase.
- Separate soft guidelines from hard limits, and call out when a limit can require an Account Executive request or org-specific validation.
- Before recommending data actions, Flow delivery, webhook delivery, or event subscribers, check data-action limits and Platform Event delivery implications.
- Distinguish home-org platform delivery from external subscriber delivery when discussing allocation pressure.
- Relevant limit families currently captured include: General Guidelines and Limits, Activation Guidelines and Limits, Calculated Insights Guidelines and Limits, Code Extension Guidelines and Limits (Beta), Data Actions Guidelines and Limits, Data Explorer Guidelines and Limits, Data Federation Guidelines and Limits, Data Graphs Guidelines and Limits, Data Ingestion Guidelines and Limits, Data Model Object Guidelines and Limits, Data Shares Guidelines and Limits, Data Transforms Guidelines and Limits.
<!-- SF_DOC_SYNC_END:limits-data-actions -->
