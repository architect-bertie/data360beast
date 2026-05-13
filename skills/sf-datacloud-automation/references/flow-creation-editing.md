# Creating and Editing Flows (Flow Builder Essentials)

_Distilled from official Salesforce sources only. Linked from
[../SKILL.md](../SKILL.md)._

<!-- SF_DOC_SYNC_START:flow-creation-editing -->

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
