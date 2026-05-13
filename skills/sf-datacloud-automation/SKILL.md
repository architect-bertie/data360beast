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

<!-- SF_DOC_SYNC_START:data-cloud-triggered-flows -->
### Data Cloud-Triggered Flows

_Distilled from official Salesforce Developer blog, Trailhead, and Help._

**Sources:**
- developer.salesforce.com/blogs/2024/08/automate-your-workflow-with-data-cloud-triggered-flows-and-invocable-actions
- trailhead.salesforce.com/content/learn/modules/data-cloud-in-flows/trigger-flows-from-data-cloud
- flow_concepts_trigger_data_cloud.htm — Flow Concepts: Data Cloud Trigger

**What they are:**
Data Cloud-triggered flows automate actions based on **near real-time data
changes** occurring within Data 360. Unlike record-triggered flows that fire
on CRM DML, these fire on DMO or CIO record changes inside Data Cloud.

**Trigger sources:**
- A Data Model Object (DMO) record is created or updated.
- A Calculated Insight Object (CIO) result changes.

**How to create:**
1. Flow Builder → New Flow → select **Data Cloud-Triggered Flow**.
2. Choose the triggering DMO or CIO.
3. Configure entry conditions (field criteria on the data cloud object).
4. Build the flow canvas with actions:
   - Create/Update CRM records (Account, Contact, Lead, etc.).
   - Send notifications (email, Slack, custom notification).
   - Publish platform events.
   - Call invocable Apex actions.
   - Make HTTP callouts (external service actions).
5. Add fault paths for error handling.
6. Activate the flow.

**Architecture pattern — Invocable Actions (reusable):**
- Write an `@InvocableMethod` Apex class once.
- Invoke from multiple Data Cloud-triggered flows without duplication.
- Useful for callouts (credit checks, identity verification, enrichment).
- The action appears in Flow Builder under "Action" elements.

**Example end-to-end:**
1. Data ingested via Ingestion API into a DMO.
2. Data Cloud-triggered flow fires on new record.
3. Decision element checks consent field.
4. If true: invocable action creates a CRM Lead + publishes a platform event.
5. A platform-event-triggered flow calls an external credit agency API.
6. Credit score written back to the CRM Lead record.

**Key constraints:**
- Near real-time (seconds to low minutes), not synchronous.
- Handles large data volumes via event-driven architecture.
- Must handle duplicate/replay events (idempotent design).
- Debug logs require special enablement for Data Cloud platform events.
- Cannot access all standard Flow features (e.g., screen elements not
  applicable); restricted to automation elements.
- System context by default; secure CRM target objects via OLS/FLS.

**Best practices:**
- Keep trigger conditions narrow to avoid unnecessary flow executions.
- Use decision elements early to exit fast when criteria are not met.
- Test with positive, negative, duplicate, late-arriving, and
  permission-denied scenarios.
- Monitor flow interview counts and throttling limits.
- Chain complex logic through platform events rather than deeply nested
  subflows to maintain scalability.
<!-- SF_DOC_SYNC_END:data-cloud-triggered-flows -->

<!-- SF_DOC_SYNC_START:activation-triggered-flows -->
### Activation-Triggered Flows

_Distilled from official Salesforce sources only._

**Sources:**
- platform.automate_flow_build_create_activation_triggered_flow.htm — Create an Activation-Triggered Flow
- data.c360_a_create_data_cloud_activation.htm — Create a Data Cloud Activation
- data.c360_a_api_activation.htm — API Activation
- trailhead.salesforce.com/content/learn/modules/data-cloud-in-flows — Utilizing Data Cloud with Flow Builder for Automation
- blogs.mulesoft.com/news/activate-data-360-segments-with-mulesoft-for-flow-integration-connectors — official MuleSoft blog (Salesforce-owned)

**What they are:**
Activation-Triggered Flows fire automatically when a **Data 360 segment
publishes** or a **Batch DMO activation** runs. They bridge data
activation and downstream system action without custom code.

**How they work (three-part model):**
1. **Activation Target** — defines the delivery destination (where
   audience records go).
2. **Activation Setup** — select Data 360 attributes, link a segment or
   DMO, choose the activation target, and select a data space.
3. **Activation-Triggered Flow** — in Flow Builder, configure the
   Data 360 activation as the **start node** and define downstream
   actions.

**How to create (five steps):**
1. Create your Activation Target in Data 360.
2. Point your activation to the target when setting up the segment
   activation.
3. In Flow Builder, build an Activation-Triggered Flow linked to your
   Data 360 activation as the start node.
4. Add Action elements using MuleSoft Integration Connectors, External
   Services, or other invocable actions.
5. Map your Data 360 fields to the connector's schema; save and
   activate the Flow.

**Two integration architecture options:**
- **Option 1 — Platform Named Credentials + External Service** —
  simple REST integrations, lightweight API calls, internal Salesforce
  or external systems.
- **Option 2 — MuleSoft Integration Connectors in Flow** — structured
  connectors and enterprise APIs to systems like Adobe Marketo,
  HubSpot, Oracle NetSuite, and custom APIs.

Connectors leverage **Platform Named Credentials** for secure
authentication without manual credential handling.

**Example use case (Win-Back to External System):**
1. Win-Back Account segment publishes.
2. Activation-Triggered Flow processes the activation.
3. Flow pushes audience into Marketo/HubSpot via MuleSoft connector.
4. CRM records updated based on engagement responses.
5. Sales tasks created automatically for follow-up.

**Key constraints:**
- Requires an Activation Target to be configured and active.
- Segment must be published, OR batch DMO activation must run.
- High-scale flow execution; payload may contain large audiences.
- Same fault-path and idempotency best practices as Data Cloud-triggered flows.
- Governed by activation publish limits and flow interview limits.

**Distinction from Data Cloud-triggered flows:**
| Aspect | Data Cloud-Triggered | Activation-Triggered |
|---|---|---|
| Fires on | DMO/CIO record change | Segment publish or batch DMO activation |
| Timing | Near-real-time (per record) | At publish cadence (batch) |
| Primary user | Data engineers, architects | Marketers, activation ops |
| Payload size | Single record context | Full audience / activation set |
| Typical target | CRM record, platform event | External system, marketing platform |
<!-- SF_DOC_SYNC_END:activation-triggered-flows -->

<!-- SF_DOC_SYNC_START:flow-orchestrated-activations -->
### API Activations and Flow-Orchestrated Multi-Channel Engagement

_Distilled from official Salesforce sources only._

**Sources:**
- data.c360_a_api_activation.htm — API Activation
- platform.automate_flow_build_create_activation_triggered_flow.htm — Create an Activation-Triggered Flow
- trailhead.salesforce.com/content/learn/modules/data-cloud-in-flows — Data Cloud in Flows
- trailhead.salesforce.com/content/learn/modules/advanced-segmentation-in-data-360/manage-segment-lookback-schedules-and-publish — Optimize Segment Lookback and Publishing
- blogs.mulesoft.com/news/activate-data-360-segments-with-mulesoft-for-flow-integration-connectors — MuleSoft for Flow Integration Connectors (official)

**API Activations:**
- Special activation target type that exposes a segment's audience to
  Apex, Flow, and external callers via the Data 360 Profile and
  Activation Read APIs.
- Useful when a Flow must trigger an activation independent of the
  segment publish schedule.
- Activation results are available to the calling Flow synchronously
  for membership-based decisions or audience-driven processing.

**Multi-Channel Orchestration via Flow:**
Activation-Triggered Flows enable marketers to design multi-step
engagement paths inside Flow Builder. The pattern combines:

- **Activation Target** as the delivery point per channel (email, ads,
  CRM update, SMS).
- **Wait Elements** to pause between channels (time-based or event-based).
- **Decision Elements** to branch based on engagement signals from
  downstream systems (e.g., email opened, ad clicked).
- **Sub-Flows** to package reusable channel logic.
- **API Activations** invoked from inside the flow to push audiences to
  additional channels mid-orchestration.

**Implementation pattern (multi-channel):**
1. Design Flow with a Data 360 activation as the start element.
2. Insert wait conditions based on time or engagement events.
3. Add decision blocks to check engagement status from downstream system
   feedback (CRM updates, MC engagement events, custom platform events).
4. Invoke API Activations or MuleSoft connectors for each next channel.
5. Define exit criteria (converted, unsubscribed, sequence complete).
6. Test with a small audience before launching at scale.
7. Monitor via Flow run history to see where audiences exit and which
   paths perform best.

**Common use cases:**
- **Re-engagement:** email → wait 5 days → if no engagement → retarget
  via ads connector.
- **Onboarding:** welcome email → wait 24h → if no setup activity →
  follow-up email → still no action → ads with setup benefit.
- **Cart abandonment:** email → wait 6h → if no return → dynamic
  product ads via Google Ads or Meta Ads activation.

**Relationship to Marketing Cloud Engagement Journey Builder:**
- Flow-based orchestration complements Journey Builder rather than
  replacing it.
- Use Journey Builder for template-based visual journeys when MC
  Engagement is the primary execution channel.
- Use Flow when orchestration needs advanced logic (complex loops,
  branching, sub-flows, multiple non-MC channels) or when external
  systems beyond MC are part of the path.
- Both operate on the same Data 360 activations and segments.

**Status (as of writing):**
- Activation-Triggered Flows are GA.
- API Activations are GA.
- MuleSoft for Flow Integration Connectors are GA per the MuleSoft
  product page.
- Always confirm GA/Beta status against the latest Help and Release
  Notes for the target org's release.
<!-- SF_DOC_SYNC_END:flow-orchestrated-activations -->

<!-- SF_DOC_SYNC_START:flow-creation-editing -->
### Creating and Editing Flows (Flow Builder Essentials)

_Distilled from official Salesforce Help and Trailhead._

**Sources:**
- platform.automate_with_salesforce_flow.htm — Automate with Salesforce Flow
- platform.flow.htm — Flow Builder
- trailhead.salesforce.com/content/learn/modules/data-cloud-in-flows

**Flow Builder navigation:**
- Setup → Process Automation → Flows → New Flow.
- Choose flow type: Screen Flow, Record-Triggered, Schedule-Triggered,
  Platform Event-Triggered, **Data Cloud-Triggered**, **Activation-Triggered**.
- Canvas-based drag-and-drop editor.

**Core elements:**
| Element | Purpose |
|---|---|
| Start | Trigger definition (object, conditions, timing) |
| Assignment | Set variable values |
| Decision | Branch logic (if/else) |
| Get Records | SOQL query (CRM) |
| Create/Update/Delete Records | CRM DML |
| Action | Invocable Apex, External Service, MuleSoft connector, HTTP callout |
| Sub-Flow | Reusable flow invocation |
| Loop | Iterate over collections |
| Fault | Error handling path |

**Editing existing flows:**
- Open via Setup → Flows → select the flow.
- Use "Save As" for versioning before changes.
- Activate/Deactivate flows independently.
- Flow versions: only one active version per flow; previous versions
  remain for rollback.

**Best practices for Data Cloud flows:**
- Test in sandbox; promote via change sets or SFDX source deploy.
- Use descriptive API names matching the trigger source (e.g.,
  `DC_ChurnRisk_CIO_Update`).
- Document entry conditions, expected throughput, and fault behavior.
- Leverage flow debug mode and Data Cloud event replay for testing.
- Enable debug logs for Data Cloud platform events when troubleshooting.
- Keep action count per interview low to stay within execution limits.
<!-- SF_DOC_SYNC_END:flow-creation-editing -->

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
