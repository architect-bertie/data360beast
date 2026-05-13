# Identity Resolution and Data Graphs

_Distilled from official Salesforce sources only. Linked from
[../SKILL.md](../SKILL.md)._

<!-- SF_DOC_SYNC_START:identity-resolution-and-graphs -->

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
