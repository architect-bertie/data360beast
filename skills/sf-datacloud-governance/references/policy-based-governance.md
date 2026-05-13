# Policy-Based Governance (ABAC + RBAC)

_Distilled from official Salesforce sources only. Linked from
[../SKILL.md](../SKILL.md)._

<!-- SF_DOC_SYNC_START:policy-based-governance -->

**Sources:**
- data.c360_a_policy_based_governance_dg.htm — Policy-Based Governance in Data 360
- architect.salesforce.com/docs/architect/fundamentals/guide/data360_security_architecture.html — ABAC architecture detail (PIP/PDP/PEP)

**RBAC vs ABAC (different layers, complementary):**
- **RBAC** governs platform/capability access — who can use Data Spaces,
  process creation, admin tooling. Implemented via permission sets.
- **ABAC** governs data access enforcement — who can read which objects,
  fields, rows. Evaluates user attributes + data attributes at runtime.
- RBAC says "Anna can use the Marketing data space"; ABAC says "Anna can
  read Customer.Email but not Customer.SSN, and only EU rows."

**ABAC architecture (CEDAR-based, distributed governance fabric):**
- **Policy Information Point (PIP)** — houses policy definitions, enriched
  metadata, tags, classifications, lineage.
- **Policy Decision Point (PDP)** — interprets CEDAR policies, evaluates
  user + resource attributes deterministically.
- **Policy Enforcement Point (PEP)** — enforces decisions at runtime
  across APIs, UI queries, CRM enrichment, GenAI RAG pipelines.

ABAC in Data 360 is configured, not built — populate native components,
no custom enforcement code required.

**Three policy types:**
1. **Data access policies** — control object/field/row visibility.
   Example: "Wealth Management Data" tagged objects only visible to that
   department.
2. **Dynamic data masking policies** — obscure sensitive data at query
   time without altering stored values. Example: show last 4 of SSN to
   service agents.
3. **Record-level security (RLS) policies** — restrict by record.
   Example: regional managers see only their store's data.

**Layered access boundaries:**
- **Object-Level Security (OLS)** — outermost; whole DMO/DLO access.
- **Field-Level Security (FLS)** — specific fields within an object.
- **Record-Level Security (RLS)** — individual records by attribute.
- **Dynamic Data Masking (DDM)** — query-time obfuscation, complements ABAC.

**Rules of precedence and propagation:**
- Deny policies always override allow policies.
- Tag classifications propagate downstream along data lineage (DLO → DMO).
- Tag propagation preserves sensitivity across transforms.
- Policies apply consistently across Agentforce, analytics, segmentation.

**Best practices:**
- Keep policies simple; avoid duplication.
- Reuse tags and categories rather than creating new ones per policy.
- Test policies early with real non-admin user roles, not just Policy Builder.
- Validate masked-field interactions with joins, primary keys, graphs,
  Boolean fields, and dashboards (see "Policy Gotchas" in SKILL.md).

<!-- SF_DOC_SYNC_END:policy-based-governance -->
