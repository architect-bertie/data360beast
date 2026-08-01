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
  author: "architect-bertie"
---

# sf-datacloud-act

Use this skill for the **activation plane**.

Activation target catalog: [references/activation-target-cards.md](references/activation-target-cards.md)

Beast references:
- Beast preflight: [docs/beast-preflight.md](../../docs/beast-preflight.md)
- Phase proof matrix: [docs/phase-proof-matrix.json](../../docs/phase-proof-matrix.json)
- Public operating model: [docs/operating-model.md](../../docs/operating-model.md)
- Developer Guide index: [docs/data360/developer/index.md](../../docs/data360/developer/index.md)
- Proof ledger: [docs/proof-ledger.md](../../docs/proof-ledger.md)
- Public LLM map: [docs/llms.txt](../../docs/llms.txt)
- Limits source precedence: [docs/data360/limits-source-precedence.md](../../docs/data360/limits-source-precedence.md)
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

## Doc-Synced Notes

<!-- SF_DOC_SYNC_START:act-activation-lifecycle -->
### Activation Lifecycle and Orchestration

_Distilled from official Salesforce Help, Developer docs, and community guides._

**Sources:**
- data.c360_a_act_on_data.htm — Act on Your Data
- data.c360_a_activation_targets.htm — Activation Targets
- data.c360_a_activation.htm — Activations
- data.c360_a_create_data_cloud_activation.htm — Create an Activation

**Activation vs Data Actions:**
- Activations send segments + profile attributes to external platforms
  (marketer-facing audience delivery).
- Data Actions send near-real-time events to trigger automation on DMO/CIO
  change (architect/data-specialist-facing orchestration).

**Activation process (six steps):**
1. Create Segment → Who is the audience?
2. Configure Activation Target → Where does it go?
3. Create Activation on Segment → How is it published? (attributes, schedule)
4. Select Activation Membership → Individual or Unified Individual?
5. Select Contact Points → Which email/phone? (Source Priority Order)
6. Select Additional Attributes → What personalization data to include?

**Activation target types (see catalog for full cards):**
- Marketing Cloud Engagement (SDE)
- Marketing Cloud Personalization (Dataset)
- External Activation Platform (Meta, LinkedIn, Google Ads, Amazon, DV360, TikTok, Pinterest)
- File Storage (S3, SFTP, GCS, Azure)
- Data Cloud Audience DMO
- B2C Commerce
- Loyalty Cloud
- Webhook (data-action target — near-real-time HTTP POST)

**Source Priority Order for Contact Points:**
- Primary → uses Primary Flag field in data streams
- Any → default fallback from any source
- Personal → For Personal Use field = 1
- Business → For Business Use field = 1
- Configure per activation to control which contact point value is delivered.

**Key constraints:**
- One unique platform account per External Activation Target; multiple
  targets per platform allowed.
- Only Data Cloud Marketing Admin or Marketing Manager can create targets.
- File storage default max 500 MB / 5000 records (splits automatically).
- S3 requires specific IAM permissions and supports SSE-S3 encryption.
- Webhook targets require HMACSHA256 validation; rotate keys ≤ 12 months.
- DMO activation batch mode covers Profile, Engagement, and Other DMOs
  (not Audience or certain system-generated DMOs).
- Engagement DMO batch activation sends only last 90 days of records.
<!-- SF_DOC_SYNC_END:act-activation-lifecycle -->

<!-- SF_DOC_SYNC_START:limits-activation -->
### Activation limit gate

_Auto-synced from the local sf-docs cached Salesforce Help export (official docs only)._

**Sources (sf-docs cached Help):**
- data.c360_a_limits_and_guidelines.htm — Data 360 Limits and Guidelines | Salesforce Help

**Source fingerprint:** `1ce0aa69b0b275b02c26170b`

**Notes:**
- Treat the captured Limits and Guidelines page as a required source before making durable guidance for this phase.
- Separate soft guidelines from hard limits, and call out when a limit can require an Account Executive request or org-specific validation.
- Before recommending activation targets, DMO activation, API activation, or publish schedule, check activation and data-action limit families.
- Call out whether a target is internal, external, file-based, API-based, or event-driven because limits and proof differ.
- Relevant limit families currently captured include: General Guidelines and Limits, Activation Guidelines and Limits, AI Models (formerly Einstein Studio) Guidelines and Limits, Calculated Insights Guidelines and Limits, Code Extension Guidelines and Limits, Data Actions Guidelines and Limits, Data Explorer Guidelines and Limits, Data Federation Guidelines and Limits, Data Graphs Guidelines and Limits, Data Ingestion Guidelines and Limits, Data Model Object Guidelines and Limits, Data Shares Guidelines and Limits.

<!-- SF_DOC_SYNC_END:limits-activation -->
