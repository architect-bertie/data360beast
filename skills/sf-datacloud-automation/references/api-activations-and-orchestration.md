# API Activations and Flow-Orchestrated Multi-Channel Engagement

_Distilled from official Salesforce sources only. Linked from
[../SKILL.md](../SKILL.md)._

<!-- SF_DOC_SYNC_START:flow-orchestrated-activations -->

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
