---
name: sf-datacloud-harmonize
description: >
  Salesforce Data 360 Harmonize phase for DMOs, mappings, identity resolution,
  profile resolution, and Data Graphs. TRIGGER when: the user works with DMOs,
  mappings, relationships, identity resolution, unified profiles, or data graphs.
license: MIT
metadata:
  version: "2.0.0"
  author: "architect-bertie"
---

# sf-datacloud-harmonize

Use this skill for the **schema and unification plane**.

Beast references:
- Beast preflight: [docs/beast-preflight.md](../../docs/beast-preflight.md)
- Phase proof matrix: [docs/phase-proof-matrix.json](../../docs/phase-proof-matrix.json)
- Public operating model: [docs/operating-model.md](../../docs/operating-model.md)
- Data 360 model-gallery implementation map: [docs/data360/model-gallery-implementation-map.md](../../docs/data360/model-gallery-implementation-map.md)
- Proof ledger: [docs/proof-ledger.md](../../docs/proof-ledger.md)
- Public LLM map: [docs/llms.txt](../../docs/llms.txt)
- Limits source precedence: [docs/data360/limits-source-precedence.md](../../docs/data360/limits-source-precedence.md)
- For exact Salesforce behavior, fetch official Help/Developer docs on demand with `sf-docs`.
- For endpoint shape, use OpenAPI from the official spec or the user-supplied Swagger before writing payloads.

## Prefer these Connect API families

- `GET/POST/PATCH/DELETE /ssot/data-model-objects`
- `GET/POST/DELETE /ssot/data-model-object-mappings`
- `PATCH /ssot/data-model-object-mappings/.../field-mappings/...`
- `GET/POST /ssot/data-model-objects/:dataModelObjectName/relationships`
- `GET/POST/PATCH/DELETE /ssot/identity-resolutions`
- `POST /ssot/identity-resolutions/:identityResolution/actions/run-now`
- `GET/POST/DELETE /ssot/data-graphs`
- `GET /ssot/data-graphs/metadata`
- `GET /ssot/data-graphs/data/...`
- semantic layer and metadata quality handoff

## Rules

- Resolve runtime DMO/profile names through metadata before writing query or segment logic.
- For model design, load the model-gallery implementation map when choosing
  between Case, Party, Privacy, Engagement, Email Engagement, Google Analytics,
  Product, Sales Order, Financial Services, Healthcare Provider, Vehicle Charger
  and Telematics, Student Financial Aid, or GenAI Audit and Feedback subject
  areas.
- Pick the anchor DMO before designing joins, insights, segments, or graphs.
  Common anchors include Unified Individual, Individual, Account, Account
  Contact, Contact Point plus Consent, Engagement Action, Sales Order, Sales
  Order Product, Product, Case, Asset, and vertical-domain objects.
- Only mapped fields and objects with relationships can be used for segmentation and activation.
- Profile and Other DMOs require primary key mapping; Engagement DMOs require primary key and event datetime mapping.
- For party-area modeling, Party is the reference to `Individual.Id`; map at least one contact point channel for unification and activation.
- Do not treat `Individual`, `Account`, `Account Contact`, `Party`, contact
  point DMOs, and unified DMOs as synonyms. They represent different grains.
- Do not model consent as a single boolean on `Individual`; consent is scoped by
  party, contact point, channel, purpose, brand, status, legal basis, and action.
- Prefer standard C360 DMOs and starter mappings when they match the business concept; customize only when the standard model cannot represent the domain cleanly.
- Model grain explicitly: profile, engagement, transaction, product, account, case, content, or support object.
- Define relationship cardinality before allowing calculated insights, segments, data graphs, or reports to join across objects.
- Relationship cardinality cannot be changed after creation. A bad cardinality choice becomes a downstream segment/activation problem.
- Standard relationships become active only when both participating fields are mapped.
- Treat identity resolution as asynchronous; verify resulting unified shapes after runs.
- For identity resolution, validate source counts, match/consolidation rate, over-grouping, under-grouping, outlier unified profiles, and contact point quality before trusting segments.
- Verify governance access to unified result and unified link DMOs before downstream reports, graphs, segments, or agents consume identity outputs.
- Use Data Graph for retrieval and enrichment, and only turn graph signals into activation criteria when those signals are represented in segment-safe schema.
- Data Graphs must have a primary DMO, live in a data space, and should include only fields needed for retrieval/agent context.
- Include calculated insights or streaming insights in a Data Graph only when they are based on a DMO also included in the graph.
- Data Graph users can need access to ID/value/fragment DMOs and graph inputs. Masking or deny FLS on graph fields can hide or break the graph.
- Keep Data Graph keys and relationship fields unmasked unless a governed replacement path is tested.
- The current project pattern is: graph context improves proposal quality, but activation rebuilds from DMO-safe criteria.
- Prepare descriptions and relationship semantics with [sf-datacloud-metadata-agentic](../sf-datacloud-metadata-agentic/SKILL.md) when Agentforce or AI Models will consume the metadata.

## Handoff

- For query validation -> [sf-datacloud-retrieve](../sf-datacloud-retrieve/SKILL.md)
- For CIs -> [sf-datacloud-calculated-insights](../sf-datacloud-calculated-insights/SKILL.md)
- For segments -> [sf-datacloud-segment](../sf-datacloud-segment/SKILL.md)
- For semantic models -> [sf-datacloud-semantic-layer](../sf-datacloud-semantic-layer/SKILL.md)
- For tags, masking, RLS, and graph access failures -> [sf-datacloud-governance](../sf-datacloud-governance/SKILL.md)

## Doc-Synced Notes

<!-- SF_DOC_SYNC_START:dmo-and-mapping -->
### DMOs, DLOs, and Field Mapping

_Distilled from official Salesforce sources only._

**Sources:**
- data.c360_a_data_model_objects.htm — Data Model Objects (DMOs)
- data.c360_a_data_lake_objects.htm — Data Objects (DLOs)
- data.c360_a_data_model_object_relationships.htm — DMO Relationships
- data.c360_a_data_mapping.htm — Data Mapping
- data.c360_a_required_data_mappings.htm — Required Mappings
- data.c360_a_map_custom_data_model_objects.htm — Map Custom DMOs
- data.c360_a_map_data_model_objects_in_a_data_space.htm — Map DMOs in Data Space
- data.c360_a_normalized_and_denormalized_data.htm — Normalized vs Denormalized
- developer.salesforce.com/docs/data/data-cloud-ref/guide/c360dm-model-data.htm — Model Data in Data Cloud
- developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-datamodelobjects.html — Standard DMO catalog

**DLO vs DMO (the two-tier model):**
- **Data Lake Object (DLO)** — raw storage container; preserves source
  schema; ingested via data streams.
- **Data Model Object (DMO)** — harmonized, schema-conformed view that
  aligns with the Customer 360 Data Model (or custom).
- DMOs are physical OR virtual views over DLOs.

**DMO categories (drives downstream behavior):**
| Category | Purpose | Example DMOs | Activation eligibility |
|---|---|---|---|
| Profile | Person/account-level identity | Individual, Account, Account Contact | Activation primary |
| Engagement | Time-series interaction | Email Engagement, Web Engagement, Product Browse | Activation, last-90-day batch |
| Other | Reference/lookup data | Product, Location, Campaign | Activation supported, not Audience |
| Audience | Segment-output DMOs | Segment Membership, Activation membership | Activation NOT supported as source |

**Standard DMOs (most-used):**
- Identity: Individual, Account, Account Contact, Party, Party Identification
- Contact Points: Email, Phone, Address, App, Digital ID, Social
- Engagement: Email Engagement, Device Application Engagement, Website
  Engagement, Product Browse Engagement, Product Order Engagement
- Consent: Consent Log, Subscription Management, Privacy Communication Consent
- Service: Case, Service Appointment, Knowledge Article

**Field mapping (Help-side and API):**
- Maps `sourceFieldDeveloperName` (DLO field) → `targetFieldDeveloperName` (DMO field).
- Required mappings vary by DMO (e.g., `ssot__SourceSystemId__c`,
  `ssot__DataSourceId__c`, name fields).
- Connect API: `POST /ssot/data-stream-mappings` to create mapping payload.
- UI: Data Streams tab → Edit stream → Mapping section → drag-drop fields.

**Starter Data Bundles:**
- Salesforce-defined data stream definitions that automatically map
  source objects to standard DMOs after deployment.
- Available for Salesforce CRM, Service Cloud, Marketing Cloud, B2C Commerce.
- Customizable post-deployment.

**Custom DMOs:**
- Created via UI or `config.json` schema definition with name, label,
  category, fields (name, label, data type).
- Used when standard DMOs don't fit the source domain.
- Custom DMOs participate in identity resolution if mapped to Individual
  or Party correctly.

**DMO-to-DMO transforms:**
- Read from source DMO → SQL transform → write to target DMO.
- Schema configured via `config.json` in Code Extension.
- Useful for derived attributes, scoring, or pivot operations.

**Mapping in Data Spaces:**
- DMOs can be mapped per data space — same logical DMO can have
  different DLO sources in EU vs AMER spaces.
- Map Data Model Objects in a Data Space via the Data Streams UI within
  the data-space context.
- Required for multi-region governance compliance.

**Normalized vs Denormalized:**
- **Normalized** — multiple related DMOs joined via foreign keys.
  Example: Individual + Contact Point Email + Address.
- **Denormalized** — flattened DMO with all attributes inline. Better
  for query performance, worse for governance (mask one field, mask
  everything).
- Choose normalized for governance/identity-resolution, denormalized for
  high-frequency analytical queries (build via batch transform).
<!-- SF_DOC_SYNC_END:dmo-and-mapping -->

<!-- SF_DOC_SYNC_START:dmo-relationships -->
### DMO Relationships and Cardinality

_Distilled from official Salesforce sources only._

**Sources:**
- data.c360_a_data_model_object_relationships.htm — DMO Relationships
- developer.salesforce.com/docs/data/data-cloud-dev/guide/dc-object-model.html — Object Model in Data 360
- developer.salesforce.com/docs/platform/data-models/guide/salesforce-data-model-notation — Salesforce Data Model Notation

**Supported cardinality:**
- **One-to-One (1:1)** — single record relates to exactly one record.
  Example: Individual ↔ Individual Identity Link, Individual ↔ Account
  Manager, Individual ↔ Party.
- **Many-to-One (N:1)** — multiple records relate to a single record.
  Example: Account → Individual, Contact Point Email → Individual,
  Marketing Engagement → Individual.

**Note:** The visual Segment Canvas does not reliably handle
composite-key joins because relationships support one field. Prefer
single-field primary keys for segment-safe DMOs.

**Relationship definition components:**
| Component | Role |
|---|---|
| Primary Key | Unique identifier on the object (e.g., Individual ID for Individual DMO) |
| Foreign Key | Field in the related object that points to the primary |
| Related Field | The field in the related object the relationship connects through |

**Defining relationships:**
- UI: Data Modeler → DMO → Relationships tab → Add relationship.
- API: `POST /ssot/data-model-object-relationships` with source/target
  DMO names, primary key, foreign key, cardinality.
- Relationships are required for join paths in segments, calculated
  insights, and data graphs.

**Common identity DMO relationship examples (Individual DMO):**

*One-to-One:*
- Individual ↔ Individual Identity Link (via Individual ID)
- Individual ↔ Account Manager (via Individual ID)
- Individual ↔ Party (via Party ID)
- Consent ↔ Individual (Contact ID → Individual ID)

*Many-to-One:*
- Account → Individual (Account ID → Individual ID)
- Contact Point Address → Individual (Party → Individual ID)
- Contact Point Email → Individual (Party → Individual ID)
- Contact Point Phone → Individual (Party → Individual ID)
- Marketing Engagement → Individual (Contact ID → Individual ID)
- Person Life Event → Individual (Individual ID → Individual ID)
<!-- SF_DOC_SYNC_END:dmo-relationships -->

<!-- SF_DOC_SYNC_START:identity-resolution-and-graphs -->
### Identity Resolution and Data Graphs

_Distilled from official Salesforce sources only._

**Sources:**
- data.c360_a_identity_resolution.htm — Identity Resolution overview
- data.c360_a_data_graphs.htm — Data Graphs

**Identity Resolution Rulesets:**
A ruleset combines match rules + reconciliation rules to produce
**Unified Individual** records from multiple source profiles.

**Match Rules — pick which records to merge:**
1. Select object: Individual, Contact Point Email/Phone/Address, Device,
   Party Identification.
2. Select field and attributes.
3. Choose match method:
   - **Exact** — character-for-character match, no typos allowed.
   - **Fuzzy** — similar match (typos, spelling variants); available for
     first name.
   - **Normalized** — same content regardless of formatting; available
     for email, phone, address.
4. Combine multiple match rules across standard and custom attributes.

**Reconciliation Rules — pick which value wins on a unified field:**
| Method | Behavior |
|---|---|
| Last Updated | Most recently updated value across sources |
| Most Frequent | Most common value across all source records |
| Source Sequence | Rank sources by preference; first match wins |

Apply at object level (default) or override per field.

**Implementation cadence:**
- Up to **2 rulesets per org** can be active simultaneously.
- First publish: unified profiles materialize within ~24 hours.
- Subsequent ruleset edits: reprocessed daily.
- Test rulesets with synthetic profiles before production publish.

**Outputs of Identity Resolution:**
- Unified Individual DMO populated with reconciled records.
- Unified Link Indexes maintain source-to-unified mappings.
- Unified Contact Point DMOs (Email, Phone, Address) per profile.

**Data Graphs:**
Visual representation of relationships between DMOs that can be deployed
to support services like Agentforce, prompts, segments, and activations.

**Real-Time Data Graphs:**
- Capture essential relationships for sub-second AI/agent interactions.
- Visual builder shows all DMO relationships before deployment.
- Selectively expose subsets of the unified profile for performance and
  governance.
- Required for real-time segments and Agentforce grounding.

**Building a Data Graph:**
1. Data Graphs tab → New.
2. Select root DMO (typically Unified Individual or Account).
3. Add related DMOs along defined relationships.
4. Select fields to expose (governance: minimize PII).
5. Configure as standard or real-time.
6. Deploy.

**Governance interactions:**
- Masking applied to a field used in a Data Graph can block graph access.
- Field-level security on primary or fully qualified keys can break
  graph traversal.
- Validate graph behavior with non-admin users for the Agentforce/RAG
  consumer.

**Pre-flight before going to Segment/CI/Agentforce:**
- Ruleset published; unified count > 0.
- Match rule false-positive rate sampled (spot-check unified records).
- Source priority order documented.
- Real-time data graph exists if real-time activation/segmentation needed.
- Governance tags propagated to unified DMOs.
<!-- SF_DOC_SYNC_END:identity-resolution-and-graphs -->

<!-- SF_DOC_SYNC_START:limits-modeling-identity-graphs -->
### Modeling, identity, and graph limit gate

_Auto-synced from the local sf-docs cached Salesforce Help export (official docs only).

**Sources (sf-docs cached Help):**
- data.c360_a_limits_and_guidelines.htm (2026-05-11T20:20:31.057Z) — Data 360 Limits and Guidelines

**Notes:**
- Treat the captured Limits and Guidelines page as a required source before making durable guidance for this phase.
- Separate soft guidelines from hard limits, and call out when a limit can require an Account Executive request or org-specific validation.
- Before choosing DMO shape, relationship paths, identity rulesets, or Data Graph shape, check limits for DMOs, identity resolution, and Data Graphs.
- Escalate unclear relationship, key, or graph-volume assumptions into metadata probes instead of baking them into skill guidance.
- Relevant limit families currently captured include: General Guidelines and Limits, Activation Guidelines and Limits, Calculated Insights Guidelines and Limits, Code Extension Guidelines and Limits (Beta), Data Actions Guidelines and Limits, Data Explorer Guidelines and Limits, Data Federation Guidelines and Limits, Data Graphs Guidelines and Limits, Data Ingestion Guidelines and Limits, Data Model Object Guidelines and Limits, Data Shares Guidelines and Limits, Data Transforms Guidelines and Limits.
<!-- SF_DOC_SYNC_END:limits-modeling-identity-graphs -->
