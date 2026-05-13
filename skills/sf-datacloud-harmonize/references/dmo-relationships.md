# DMO Relationships and Cardinality

_Distilled from official Salesforce sources only. Linked from
[../SKILL.md](../SKILL.md)._

<!-- SF_DOC_SYNC_START:dmo-relationships -->

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
