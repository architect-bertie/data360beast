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
  author: "Codex"
---

# sf-datacloud-governance

Use this skill for the **Data 360 governance and policy enforcement plane**.

Detailed enforcement matrix: [references/policy-enforcement-matrix.md](references/policy-enforcement-matrix.md)

Beast references:
- Public operating model: [docs/operating-model.md](../../docs/operating-model.md)
- Interoperability decision map: [docs/data360/interoperability-decision-map.md](../../docs/data360/interoperability-decision-map.md)
- RAG/search-index playbook: [docs/data360/rag-search-index-retriever-playbook.md](../../docs/data360/rag-search-index-retriever-playbook.md)
- Developer Guide index: [docs/data360/developer/index.md](../../docs/data360/developer/index.md)
- Public API cookbook: [docs/api-cookbook.md](../../docs/api-cookbook.md)
- Public LLM map: [docs/llms.txt](../../docs/llms.txt)
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
