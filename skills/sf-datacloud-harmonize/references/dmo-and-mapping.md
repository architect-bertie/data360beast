# DMOs, DLOs, and Field Mapping

_Distilled from official Salesforce sources only. Linked from
[../SKILL.md](../SKILL.md)._

<!-- SF_DOC_SYNC_START:dmo-and-mapping -->

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
