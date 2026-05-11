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
  author: "Codex"
---

# sf-datacloud-semantic-layer

Use this skill for the **semantic model and metric governance plane**.

Beast references:
- Public operating model: [docs/operating-model.md](../../docs/operating-model.md)
- Proof ledger: [docs/proof-ledger.md](../../docs/proof-ledger.md)
- Public LLM map: [docs/llms.txt](../../docs/llms.txt)
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
