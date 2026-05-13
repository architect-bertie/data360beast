---
name: sf-datacloud-governance
description: >
  Salesforce Data 360 governance for data spaces, Enhanced Security Data Spaces,
  tags, classifications, taxonomies, RBAC, ABAC, OLS/FLS/RLS data access
  policies, dynamic data masking, custom permissions, policy enforcement, and
  governed behavior across query, Data Graphs, CIs, segments, transforms,
  search indexes, identity resolution, activations, flows, reports, and
  Agentforce. TRIGGER when: the user designs, audits, debugs, or implements
  Data 360 access control, masking, sensitive data handling, policy behavior,
  or governance-ready metadata.
license: MIT
metadata:
  version: "1.0.0"
  author: "architect-bertie"
---

# sf-datacloud-governance

Use this skill for the **Data 360 governance and policy enforcement plane**.

Detailed enforcement matrix: [references/policy-enforcement-matrix.md](references/policy-enforcement-matrix.md)

Beast references:
- Beast preflight: [docs/beast-preflight.md](../../docs/beast-preflight.md)
- Phase proof matrix: [docs/phase-proof-matrix.json](../../docs/phase-proof-matrix.json)
- Public operating model: [docs/operating-model.md](../../docs/operating-model.md)
- Interoperability decision map: [docs/data360/interoperability-decision-map.md](../../docs/data360/interoperability-decision-map.md)
- RAG/search-index playbook: [docs/data360/rag-search-index-retriever-playbook.md](../../docs/data360/rag-search-index-retriever-playbook.md)
- Developer Guide index: [docs/data360/developer/index.md](../../docs/data360/developer/index.md)
- Proof ledger: [docs/proof-ledger.md](../../docs/proof-ledger.md)
- Public LLM map: [docs/llms.txt](../../docs/llms.txt)
- Limits source precedence: [docs/data360/limits-source-precedence.md](../../docs/data360/limits-source-precedence.md)
- For exact Salesforce behavior, fetch official Help/Developer docs on demand with `sf-docs`.
- For endpoint shape, use OpenAPI from the official spec or the user-supplied Swagger before writing payloads.

## Source Priority

1. Current org configuration and live user-profile tests.
2. Official Salesforce Help and developer docs.
3. Data360 Beast OpenAPI catalog and official Salesforce API surfaces.
4. Field guides and implementation PDFs, treated as useful but verified before production claims.

## Governance Model

- Data spaces define the outer visibility scope; granular governance comes from policies.
- Assigning a data space through a permission set does not automatically grant access to the data.
- RBAC grants base feature/setup access and object/field access within a data space through permission sets.
- ABAC grants or denies access based on data attributes, tags, classifications, and user attributes such as custom permissions.
- OLS, FLS, and RLS data access policies control object, field, and record visibility.
- Dynamic data masking is query-time protection. It changes what unauthorized users see without changing stored values.
- Deny policies win over allow policies.
- Policy changes can take a few minutes to become active; test after propagation.
- Feature permissions inside a data space can restrict access, but they cannot grant more than the permission set object permissions allow.
- The default Allow All/day-zero policy can keep broad access in place. Plan it deliberately before switching to granular ABAC.
- Users with admin-style permissions can sometimes see metadata while runtime access still fails.
- For interoperability decisions, explicitly state where governance is enforced: Data 360, the external source, or both.
- Use ingestion when Data 360 must own canonical governance, lineage, auditability, and operational activation. Use federation only when source-side RLS, masking, identity mapping, and audit controls are acceptable and tested.
- For cross-org architecture, distinguish Data 360 Home Org, Companion Org,
  shared data spaces, companion connections, Data Cloud One, and API-based
  exchange. Governance ownership can move depending on which pattern is used.

## Production Workflow

1. Confirm Enhanced Security Data Spaces and Data Governance UI availability.
2. Inventory data spaces, users, permission sets, custom permissions, DMOs, DLOs, CIOs, data graphs, search indexes, semantic models, segments, activations, and flows.
3. Decide whether each user group needs broad RBAC, granular ABAC, masking, or a hybrid.
4. Define a small taxonomy first:
   - sensitivity: public, internal, confidential, restricted
   - privacy/regulatory: PII, PHI, PCI, GDPR, HIPAA, CCPA, custom obligations
   - usage: active, hidden, deprecation candidate, analytics, activation, agent-safe
5. Prefer standard/preconfigured taxonomies where they fit. Add custom taxonomies only for business-specific policy intent.
6. Apply object-level tags for broad domains and field-level tags for sensitive attributes.
7. Keep primary keys, foreign keys, fully qualified keys, and critical join/filter keys unmasked unless there is a proven alternative design.
8. Create custom permissions in custom permission sets for policy cohorts. Do not rely on standard permission sets or clones for custom permissions.
9. Create scoped policies:
   - OLS for object visibility
   - FLS deny for sensitive fields
   - RLS for row access by region, owner, hierarchy, or mapping table
   - dynamic masking for partial visibility
10. Test with real non-admin users in every consumption surface, not only in Policy Builder.
11. For federated data, validate source-side RLS/masking with the mapped enterprise identity and compare behavior with Data 360 user access.
12. For Home Org / Companion Org designs, validate data-space sharing,
    companion connection permissions, metadata visibility, and target user
    access in each org boundary.

## Tags, Classifications, and Propagation

- Tags describe object or field meaning, sensitivity, usage, or business domain.
- Tags can have one parent and multiple child tags; do not assume deeper hierarchy support.
- Assigning a child tag can apply the parent. Assigning only a parent does not automatically enforce policies tied to child tags.
- Avoid periods in tag names.
- AI tag suggestions use metadata such as names and types, not customer data; a steward still reviews before applying.
- Data Cloud can propagate tags downstream to generated objects from process definitions such as data streams, calculated insights, segments, and identity resolution.
- CI dimensions derived from formulas may not inherit source tags automatically. Retag the CIO when needed.
- Tags used by policies become lifecycle dependencies; plan delete/edit governance.

## Policy Gotchas

- `SELECT *` can return only allowed fields; explicitly selecting a denied field should fail.
- Query-time masking does not block create/edit if the user can access the underlying object and field.
- RLS is query-layer security and is not enforced in every creation/runtime path.
- RLS with joins can return wrong or empty results if the join key is masked.
- Masking Boolean fields can make values appear false.
- Masking fields used in a Data Graph can block graph access.
- FLS on primary key or fully qualified key fields can break Data Explorer, Profile Explorer, joins, related lists, graphs, and query paths.
- Segment creation can consider all records even when RLS would limit a user's query results.
- Scheduled high-scale flows can enforce policies captured at flow creation, but RLS is not enforced when the flow is triggered on schedule.
- Copy Field Enrichment runs in system mode; apply CRM security after enrichment.
- Dashboard policy changes may require refresh or cache clearing before they are visible.
- Accelerated-query caches can introduce freshness and governance interpretation questions. Validate cache refresh timing, source policy behavior, and target user access before claiming a governed result.

## Agentic Governance Rules

- Treat governance metadata as part of the agent contract.
- Mark fields as agent-safe, agent-internal, restricted, PII, join-only, or activation-only.
- Never expose names, emails, phones, addresses, source IDs, or raw profile keys unless the use case explicitly allows it and policy permits it.
- For Agentforce actions, document which user context is used and which Data 360 policies are expected to apply.
- For RAG, design filter fields and dynamic prefilters as governance controls,
  not just relevance controls: language, entitlement, publication status,
  account/record ID, geography, product, and data source often prevent the agent
  from seeing the wrong chunk.
- Validate search index, chunk DMO, index DMO, retriever, prompt, Flow, Apex, and
  Agentforce behavior with the actual non-admin consuming user.
- Validate agent answers with a non-admin user profile and policy-restricted fixtures.

## Validation Gates

- Data space assignment is correct.
- Permission sets and custom permissions match intended user cohorts.
- Tags and classifications exist on every protected object/field.
- Allow All/day-zero posture is explicitly documented.
- OLS/FLS/RLS/masking policies are active and scoped to the right data spaces.
- Query Editor, Data Explorer, Profile Explorer, reports, semantic model, Data Graph, CI, segment, activation, flow, and agent tests behave as expected.
- Restricted fields are not used as hidden join keys unless explicitly unmasked.
- Process definitions and generated outputs are retagged or tag-propagated.

## Handoffs

- Data spaces, DLOs, streams, transforms -> [sf-datacloud-prepare](../sf-datacloud-prepare/SKILL.md)
- DMOs, identity resolution, Data Graphs -> [sf-datacloud-harmonize](../sf-datacloud-harmonize/SKILL.md)
- Query behavior -> [sf-datacloud-retrieve](../sf-datacloud-retrieve/SKILL.md)
- Calculated insights -> [sf-datacloud-calculated-insights](../sf-datacloud-calculated-insights/SKILL.md)
- Segments and member counts -> [sf-datacloud-segment](../sf-datacloud-segment/SKILL.md)
- Search indexes and retrievers -> [sf-datacloud-unstructured-retrieval](../sf-datacloud-unstructured-retrieval/SKILL.md)
- Semantic metrics and dashboards -> [sf-datacloud-semantic-layer](../sf-datacloud-semantic-layer/SKILL.md)
- Activations and data actions -> [sf-datacloud-act](../sf-datacloud-act/SKILL.md)
- Agent-ready metadata -> [sf-datacloud-metadata-agentic](../sf-datacloud-metadata-agentic/SKILL.md)

## Output Format

Report:

1. governance scope and data spaces
2. user cohorts and custom permissions
3. taxonomy, tags, and classifications
4. policies and masking rules
5. feature-specific enforcement risks
6. validation tests by user profile and surface
7. production gaps and remediation

## Doc-Synced Notes

<!-- SF_DOC_SYNC_START:data-spaces -->
### Data Spaces (visibility boundary)

_Auto-synced from the local sf-docs cached Salesforce Help export (official docs only).

**Sources (sf-docs cached Help):**
- data.c360_a_data_spaces.htm (2026-05-11T18:36:14.319Z) — About Data Spaces

**Notes:**
- Treat a data space as a logical partition; it scopes data, metadata, and processes for teams (brand/region/department).
- Data space assignment via permission sets controls what users can work on in that context; it is not the same thing as granting data access (policies still matter).
<!-- SF_DOC_SYNC_END:data-spaces -->

<!-- SF_DOC_SYNC_START:permission-sets -->
### Standard Permission Sets (operational reminders)

_Auto-synced from the local sf-docs cached Salesforce Help export (official docs only).

**Sources (sf-docs cached Help):**
- data.c360_a_userpermissions.htm (2026-05-11T18:33:50.890Z) — Data 360 Standard Permission Sets

**Notes:**
- Standard Data 360 permission sets can change over time; avoid custom clones unless you have a specific reason and a review process.
- System Administrator profile can have broad data space definition access; validate governed runtime behavior with a non-admin user when proving policies.
<!-- SF_DOC_SYNC_END:permission-sets -->

<!-- SF_DOC_SYNC_START:govern-and-secure-overview -->
### Govern and Secure Overview

_Distilled from official Salesforce sources only._

**Sources:**
- data.c360_a_data_gov_capabilities.htm — Data Governance in Data 360
- data.c360_a_getting_started_data_gov.htm — Get Started with Data Governance
- architect.salesforce.com/docs/architect/fundamentals/guide/data360_security_architecture.html — Data 360 Security Architecture (official Architect Guide)
- trailhead.salesforce.com/content/learn/modules/data-cloud-govern-and-secure (official Trailhead)

**Three pillars of Data 360 Governance:**
1. **AI-powered tagging and classification** — organize and identify data
   types across structured and unstructured sources.
2. **Policy-based governance** — ABAC for fine-grained data access.
3. **Data security** — Hyperforce-inherited platform security plus
   customer-managed configuration (IAM, MFA, SSO, audit, masking).

**Shared responsibility model:**
- **Salesforce** secures the platform (Hyperforce on AWS, ISO 27001, SOC
  1/2/3, GDPR readiness, TLS 1.2+, AES-256 at rest, DDoS, patching).
- **Customer** secures data, configurations, and operational processes
  (IAM, governance, integration security, monitoring).

**Secure-by-default (Day 0):**
- New Data 360 orgs start in "Deny All" — zero implicit access.
- All permissions must be explicitly granted.
- Legacy "Allow All" orgs require manual tightening.
- This enforces least privilege by design.

**Identity layer:**
- Federated authentication via SAML 2.0, OIDC, or SCIM with IdPs (Entra
  ID, Okta, Ping Identity).
- SSO + MFA + conditional/risk-based access via the IdP.
- SCIM provisioning for lifecycle: joiners, movers, leavers automatic.

**Standard permission sets (use these, not clones):**
| Role | Primary Responsibility | Access Boundary |
|---|---|---|
| System Administrator | Setup, provisioning, configuration | No access to underlying datasets |
| Data 360 Architect | Ingestion, transforms, identity resolution, modeling | Cannot perform activation |
| Data 360 Activation Manager | Segments, channels, activation | View-only on data models |
| Data 360 User | Consumes analytics and insights | Read-only |
| Data 360 One User | Cross-org access via Companion Org | Governed by shared-space scope |

Standard permission sets auto-update with each release; custom clones do not.
<!-- SF_DOC_SYNC_END:govern-and-secure-overview -->

<!-- SF_DOC_SYNC_START:policy-based-governance -->
### Policy-Based Governance (ABAC + RBAC)

_Distilled from official Salesforce sources only._

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
  Boolean fields, and dashboards (see "Policy Gotchas" above).
<!-- SF_DOC_SYNC_END:policy-based-governance -->

<!-- SF_DOC_SYNC_START:tagging-and-classification -->
### Tagging and Classification

_Distilled from official Salesforce sources only._

**Sources:**
- data.c360_a_using_tagging_and_classification_dg.htm — Data Tagging and Classification in Data 360
- developer.salesforce.com/docs/data/data-cloud-query-guide/references/dc-sql-reference/ai-classify.html — AI_CLASSIFY SQL function

**Hierarchy structure (parent-child taxonomy):**
- Tags organize in a multilevel parent-child structure.
- Example: parent "Personal Information" → children "Email Address",
  "Phone Number", "Postal Address".
- Assigning a child tag automatically applies the parent tag — policies
  attached to the parent inherit.
- Tags support one parent, multiple children; no deeper hierarchy.

**Standard sensitivity levels:**
- Public, Internal, Confidential, Restricted.

**Standard compliance categories:**
- PII (Personally Identifiable Information)
- HIPAA (Health)
- GDPR (EU privacy)
- PCI DSS (payment card)
- Plus custom categories for org-specific obligations.

**AI-driven "Suggest Tags":**
- LLM-based metadata analyzer reads object/field names and descriptions.
- Recommends relevant tags at scale.
- Uses metadata only — does NOT read customer data.
- Reduces manual tagging burden; steward must still review before applying.
- Available as the AI_CLASSIFY SQL function for batch classification jobs.

**Industry use cases:**
- Healthcare: HIPAA categorization on patient data.
- Retail: PII + region-specific data sensitivity.
- Finance: encrypted financial data classification.
- Communications: customer interaction sensitivity.

**Tag governance:**
- Tags used in policies become lifecycle dependencies — plan delete/edit
  governance carefully.
- Avoid periods in tag names.
- CI dimensions derived from formulas may not auto-inherit source tags;
  retag the CIO when needed.
- Tags propagate downstream from DLO → DLO → DMO via data streams,
  calculated insights, segments, and identity resolution.
<!-- SF_DOC_SYNC_END:tagging-and-classification -->

<!-- SF_DOC_SYNC_START:data-spaces-detailed -->
### Data Spaces (Detailed Boundary Model)

_Distilled from official Salesforce sources only._

**Sources:**
- data.c360_a_data_spaces.htm — About Data Spaces
- data.c360_a_data_spaces_feature_access.htm — Manage Feature Access for Data Space-Aware Features
- data.c360_a_data_access_levels_setting.htm — Manage Data Cloud Data Access Levels
- architect.salesforce.com/docs/architect/fundamentals/guide/data360_security_architecture.html — Data Spaces in security architecture

**Purpose:**
Logical segregation of enterprise data domains, enabling multi-brand,
multi-region, or multi-tenant operation within a single Data 360 instance.
Maps to business domains (Sales, Marketing, Service) or regulatory
boundaries (EU, AMER, APAC).

**Properties:**
- Each data space acts as a virtual boundary for visible data collections.
- Access is explicitly granted; no implicit cross-space visibility.
- Federated ownership: each business unit governs independently while
  maintaining centralized oversight.
- Provides the first layer of governance — structural clarity and
  accountability — before fine-grained ABAC kicks in.

**Feature access in data spaces:**
- Some features are "data-space-aware" (segments, activations, CIs, data
  graphs); others are global.
- Feature permissions inside a data space cannot grant more than the
  permission set's object permissions allow.
- Manage feature access via the Data Space Permissions UI.

**Data access levels:**
- Granular controls: view, edit, manage at object level within a space.
- Required for non-admin profiles to perform any DML.
- Layered with OLS/FLS/RLS for full enforcement.

**Multi-org patterns (Data Cloud One, Companion Org):**
- Data 360 Home Org: holds the canonical Data 360 instance.
- Companion Org: connected Salesforce CRM org consuming Data 360 data.
- Data Cloud One: connect multiple CRM orgs to one Data 360 instance.
- Governance ownership shifts across these patterns — document where
  policy is enforced for each cross-org flow.
<!-- SF_DOC_SYNC_END:data-spaces-detailed -->
