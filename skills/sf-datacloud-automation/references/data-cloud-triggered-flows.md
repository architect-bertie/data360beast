# Data Cloud-Triggered Flows

_Distilled from official Salesforce sources only. Linked from
[../SKILL.md](../SKILL.md)._

<!-- SF_DOC_SYNC_START:data-cloud-triggered-flows -->

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
