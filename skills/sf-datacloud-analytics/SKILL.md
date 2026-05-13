---
name: sf-datacloud-analytics
description: >
  Salesforce Data 360 reports, dashboards, report types, reportability of DMOs
  and calculated insights, dashboard limits, consumption insights, and semantic
  model analytics. TRIGGER when: the user creates, reviews, packages, or debugs
  Data 360 reports, dashboards, report types, KPI dashboards, or analytics built
  on DMOs, CIOs, or semantic models.
license: MIT
metadata:
  version: "1.0.0"
  author: "architect-bertie"
---

# sf-datacloud-analytics

Use this skill for the **Data 360 reports and dashboards plane**.

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

## Production Workflow

1. Identify the analytics source:
   - single DMO
   - related DMOs through a custom report type
   - calculated insight object
   - semantic data model
   - consumption / billing dashboard
2. Confirm reportability, data space access, and folder permissions.
3. Pick the report grain and grouping before building charts.
4. For calculated insights:
   - measures are aggregates
   - dimensions are groupings
   - reports are summary-style
   - non-aggregatable measures require all required dimensions
   - details-only export and row-level formulas are restricted
5. Build dashboards from validated reports, not directly from untested query assumptions.
6. Test dashboards with a business user and a non-admin user.
7. After policy changes, refresh dashboards or clear cache before concluding governance is wrong.
8. Package/report distribution uses semantic model or Data 360 packaging rules where applicable.

## Design Rules

- Use the semantic layer when multiple teams need one governed KPI definition.
- Use calculated insights when the report metric needs heavy joins, windows, or multidimensional measures.
- Query Editor validates SQL and data assumptions; Data Explorer validates DLOs, DMOs, CIOs, and data graphs before reports consume them.
- Profile Explorer is the validation surface for unified profile views and related Lightning apps.
- Treat Tableau Semantics as the governed source for metrics used across reports, Tableau Next, AI, and apps.
- Treat analytics as its own serving path. Query Editor success is a useful control, but reports, dashboards, semantic models, Tableau-style consumption, cache, refresh cadence, and target-user governance must be validated directly.
- Avoid dashboards that mix incompatible grains without clear labels.
- Keep row counts, refresh cadence, and credit/usage implications visible to admins.
- Treat query, report, dashboard, and semantic model design as credit-sensitive:
  filter early, select only necessary fields, avoid high-cardinality scans, and
  validate expected consumption impact when the workload is large or recurring.
- For executive dashboards, include metric owner and data freshness.

## Validation Gates

- Report totals match a control query or source system export.
- Filters and dashboard components preserve the intended grain.
- Data space and governance policies are verified with target users.
- Admin report-builder visibility is not treated as runtime access proof.
- Dashboard loads acceptably and avoids excessive high-cardinality groupings.
- Calculated insight reports follow CI report limitations.

## Handoffs

- Metric modeling -> [sf-datacloud-semantic-layer](../sf-datacloud-semantic-layer/SKILL.md)
- CI-backed reports -> [sf-datacloud-calculated-insights](../sf-datacloud-calculated-insights/SKILL.md)
- Permission troubleshooting -> `sf-permissions` companion skill when available
- Data 360 policy behavior -> [sf-datacloud-governance](../sf-datacloud-governance/SKILL.md)

## Output Format

Report:

1. source object/model
2. report type
3. grain and groupings
4. measures/KPIs
5. dashboard components
6. permission/folder setup
7. validation query/results
8. limits and consumption notes
