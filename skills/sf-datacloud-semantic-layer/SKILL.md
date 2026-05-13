---
name: sf-datacloud-semantic-layer
description: >
  Salesforce Data 360 Semantic Layer and C360 Semantic Model development,
  logical views, dimensions, measures, metrics, shared dimensions, semantic
  data models, and metric governance. TRIGGER when: the user creates or edits
  the semantic layer, semantic models, metrics, dimensions, logical views, or
  asks how reports, dashboards, AI, or automation should use governed metrics.
license: MIT
metadata:
  version: "1.0.0"
  author: "architect-bertie"
---

# sf-datacloud-semantic-layer

Use this skill for the **semantic model and metric governance plane**.

Beast references:
- Beast preflight: [docs/beast-preflight.md](../../docs/beast-preflight.md)
- Phase proof matrix: [docs/phase-proof-matrix.json](../../docs/phase-proof-matrix.json)
- Public operating model: [docs/operating-model.md](../../docs/operating-model.md)
- Proof ledger: [docs/proof-ledger.md](../../docs/proof-ledger.md)
- Public LLM map: [docs/llms.txt](../../docs/llms.txt)
- Limits source precedence: [docs/data360/limits-source-precedence.md](../../docs/data360/limits-source-precedence.md)
- For exact Salesforce behavior, fetch official Help/Developer docs on demand with `sf-docs`.
- For endpoint shape, use OpenAPI from the official spec or the user-supplied Swagger before writing payloads.

## Production Workflow

1. Start from business questions and define canonical metrics before building views.
2. Identify the grain of every fact: transaction, daily snapshot, profile, account, case, campaign, order, product.
3. Identify shared dimensions: Individual, Unified Individual, Account, Product, User, Date, Region, Channel.
4. Resolve source DMOs and calculated insights with exact API names and data spaces.
5. Build logical views only when they solve a real modeling issue: union, dedupe, conformed join, calculated field, or standardized naming.
6. Define measures with explicit aggregation, filters, time semantics, and null/currency handling.
7. Define dimensions with stable IDs plus human-readable labels.
8. Create metric names and descriptions that match business language, not source-system jargon.
9. Test metric totals against independent control queries and source-system reports.
10. Package Data 360 semantic metadata through data kits when promoting between orgs.

## Modeling Rules

- Do not expose multiple conflicting definitions of revenue, customer, conversion, active user, or engagement.
- Every metric must have an owner, grain, refresh expectation, and permitted consumer list.
- Every metric must state whether governance can change its visible dimensions, rollups, or row set for a non-admin user.
- Prefer calculated insights for reusable heavy metrics, then expose those metrics semantically.
- Keep logical views understandable; if a view hides several business rules, document them as metric assumptions.
- For cross-cloud C360 Semantic Model work, preserve shared dimensions so Sales, Service, Marketing, and Commerce can roll up consistently.
- Treat Tableau Semantics as the governed business metric contract on top of Data 360 data.
- Semantic models are Salesforce metadata. API names are fixed after creation.
- Use relationships before logical views unless joins, unions, dedupe, or custom SQL are truly needed.
- Do not remove required primary key fields or calculated insight fields from semantic models.
- A Semantic Model must consist of one or more data objects with relationships
  and semantic definitions tailored for a specific analytical use case.
- Semantic Definitions are reusable and composable across Semantic Models and
  other Data 360 concepts. They can be extended or overridden at different
  levels to allow flexibility while keeping a mutual baseline.
- Distinguish definition types: Dimensions (basic or hierarchical), Calculated
  Dimensions (formula-based grouping), Measures (numerical with default
  aggregation), Calculated Measures (runtime formula across tables),
  Relationships (physical or logical joins with cardinality), Metrics (business
  KPIs tracked over time), and Logical Views (multi-table joins).
- Use the Tableau Semantics Authoring API to create and customize Semantic
  Models and definitions programmatically; use the Semantic Query API to answer
  business questions with customizable queries based on Semantic Models.
- A Logical View connects multiple tables via specific join types to preserve
  granularity while enabling cross-object calculations.
- Calculated Measures are evaluated at runtime according to query context and
  can reference measures and dimensions from different source tables. Use them
  for cross-object KPIs that cannot be pre-computed in a single CI.
- Treat Metrics as the business-user-facing artifact: they are derived from
  measures, carry time-tracking behavior, and should enforce consistent
  semantics across all consumers (Tableau, reports, AI, apps).
- When building C360 Semantic Models, verify that relationships in the semantic
  layer match the governed relationships in the DMO model; semantic override of
  a relationship must document the business reason.
- Keep API name discipline: API names are fixed after creation. Plan naming
  conventions before the first semantic model publish.

## Validation Gates

- Metric value matches control query within an agreed tolerance.
- Filters and time dimensions produce expected totals.
- Permissions and data space policies are tested with a non-admin user.
- Restricted CI dimensions, masked fields, and RLS policies are tested against semantic metric results.
- Reports/dashboards can consume the semantic model without duplicate rows or unexpected fanout.
- AI/Agentforce consumers receive definitions and do not invent metrics.

## Handoffs

- Calculated insight metric authoring -> [sf-datacloud-calculated-insights](../sf-datacloud-calculated-insights/SKILL.md)
- Reports and dashboards -> [sf-datacloud-analytics](../sf-datacloud-analytics/SKILL.md)
- DMO modeling and identity -> [sf-datacloud-harmonize](../sf-datacloud-harmonize/SKILL.md)
- Governance and policy behavior -> [sf-datacloud-governance](../sf-datacloud-governance/SKILL.md)

## Output Format

Report:

1. business metric
2. grain
3. fact source
4. shared dimensions
5. measures and formulas
6. logical views
7. validation query/results
8. governance and packaging notes

## Doc-Synced Notes

<!-- SF_DOC_SYNC_START:tableau-semantics-design -->
### Tableau Semantics Design and Build Guidance

_Distilled from official Salesforce Help and Developer docs._

**Sources:**
- analytics.tua_ai_sm_design.htm — Design a Semantic Model
- analytics.tua_ai_build_guide.htm — Build Guide for Semantic Models
- analytics.tua_ai_optimize_model.htm — Optimize a Semantic Model
- analytics.tua_data_sdm.htm — Semantic Data Model (SDM) section
- data.c360_a_sl.htm — Build a Semantic Model in Data 360
- data.c360_a_sl_data_models_create_new.htm — Create a Semantic Model in Tableau Semantics
- data.c360_a_sl_get_started.htm — Get Started with Tableau Semantics
- data.c360_a_sl_C360SDM_considerations.htm — Understand the C360 Semantic Model
- Tableau Semantics Layer APIs Developer Guide (developer.salesforce.com)

**Design principles:**
- Start from business questions and stakeholder needs, not from the data model.
- Define canonical metrics before building views or models.
- A Semantic Model is first-class Salesforce metadata integrated across Data 360
  for analytical and data-driven experiences.
- Semantic Models group Semantic Definitions; they override, enrich, or rename
  definitions from the lake layer for business-user consumption.
- Dimensions can be Basic (attributes) or Hierarchical; always include a human-
  readable label alongside the stable ID.
- Measures require Default aggregation type (SUM, AVG, COUNT, MIN, MAX, or
  custom), data type (number, currency, duration), and optional filters.
- Relationships in the semantic layer are flexible connections via common fields;
  they preserve granularity and have cardinality metadata. They can be physical
  (mirroring DMO relationships) or logical (semantic-layer-only).
- Metrics are business KPIs tracked over time, derived from one or more
  measures; they carry behavior that applies consistently across all queries.
- Logical Views are multi-table objects joined in the semantic layer; use them
  only for union, dedupe, conformed join, calculated field, or standardized
  naming scenarios.
- Tableau Semantics APIs comprise two surfaces: the Authoring API (CRUD for
  models and definitions) and the Semantic Query API (answer business questions
  via customizable queries).

**Optimization guidance:**
- Remove unused definitions to reduce model complexity.
- Use Calculated Measures for cross-table runtime formulas rather than
  duplicating aggregation logic in calculated insights.
- Keep metric descriptions and time semantics up to date so downstream
  consumers (reports, dashboards, AI, Tableau Next) reference a single truth.
- Test with non-admin users to validate governance affects metric visibility.
- Version semantic models through data kits for deployment; keep separate from
  platform metadata packaging unless officially supported.
<!-- SF_DOC_SYNC_END:tableau-semantics-design -->
