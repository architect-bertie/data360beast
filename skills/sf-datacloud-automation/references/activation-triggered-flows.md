# Activation-Triggered Flows

_Distilled from official Salesforce sources only. Linked from
[../SKILL.md](../SKILL.md)._

<!-- SF_DOC_SYNC_START:activation-triggered-flows -->

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
