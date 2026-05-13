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

## Doc-Synced Notes

<!-- SF_DOC_SYNC_START:analyze-data -->
### Analyze Data from Data 360

_Distilled from official Salesforce sources only._

**Sources:**
- Help "Analyze Data from Data 360" section
- developer.salesforce.com/docs/data/data-cloud-dev/guide/dc-cost-usage.html — Cost and Usage
- developer.salesforce.com/docs/data/data-cloud-query-guide/references — Query Data in Data 360

**Two report types in Data 360:**

| Type | Source | Best for |
|---|---|---|
| Standard Report | One DMO, semantic model, or CIO | Single-source analysis (Engagement, Account, CI metric) |
| Custom Report | Up to **4 related DMOs** | Joined views (Individual + Engagement + Order + Product) |

Beyond 4 DMOs, push the join into a Calculated Insight or Semantic Model
and report on the result.

**Reportable surfaces (priority order):**
1. **Semantic Model metrics** — best for governed cross-team KPIs.
2. **Calculated Insights** — best for heavy joins, windows, custom logic.
3. **Standard DMOs** — Profile, Engagement, Other categories all
   reportable with appropriate licensing.
4. **Data Lake Objects (DLOs)** — limited reporting surface; prefer DMO.

**Dashboard limits to know (Salesforce platform-wide):**
- Dashboard component cap: **1,000 groupings per component**.
- Report viewer rows: **2,000 rows displayed**.
- Summary/Matrix grouping cap: **2,000 groupings**.
- Analytics REST API: **2,000-row limit** per call.
- Calculated Insights API: **4,999 rows** per query call (different limit).

**Analytics tool integration:**

| Tool | How it consumes Data 360 |
|---|---|
| Data 360 Reports & Dashboards | Native reporting on DMOs/CIs/semantic models — no external license |
| Tableau Next | Personalized contextual insights, deep Data 360 integration |
| Tableau (legacy) | JDBC + Tableau Semantics; full visualization platform |
| CRM Analytics | "Direct Data for Data 360" — real-time queries, no preload |
| Power BI XMLA | XMLA endpoint via the Microsoft Power BI XMLA Connector |
| Custom apps | Connect API + Query API for embedded analytics |

**KPI Dashboards (consumption insights):**
- Data 360 emits credit consumption events across these usage families:
  - **Analyze and Predict** — batch + streaming CIs.
  - **Act** — data queries (reports, dashboards), streaming actions.
  - **Segment and Activate** — segment processing, activations.
- A single feature can consume from multiple usage types simultaneously.
- Reference the Data 360 Billable Usage Types page in Help and the Data
  360 Limits and Guidelines page when sizing dashboard refresh cadence.
- Build a dedicated "Data 360 Consumption" dashboard early — make
  credit usage visible to admins before scaling.

**Standard DMOs heavily used in dashboards:**
- Engagement: Email Engagement, Web Engagement, Product Browse, Order
- Profile: Individual, Account, Contact Point Email/Phone/Address
- Service: Case, Service Appointment
- Consent: Consent Log, Communication Subscription Consent

**Best practices:**
- Build the validation query in Query Editor first; compare to the
  report total before publishing.
- Filter early — top-of-report filters reduce credit consumption more
  than dashboard-level filters.
- Avoid `SELECT *` in custom report types; explicit fields preserve FLS
  and reduce credit usage.
- Tag every published dashboard with metric owner, data freshness, and
  refresh cadence.
- For executive dashboards, prefer semantic-model-backed reports — the
  metric definition is governed and shared.
- Test dashboards with a business user AND a non-admin user; admin view
  is not governance proof.

**Calculated Insight report restrictions:**
- Non-aggregatable CI measures require all CI required dimensions to be
  present in the report grouping.
- Detail-only export from a CI report can be restricted.
- Row-level formulas on CI fields can be restricted; build derived
  measures in the CI itself.

**Semantic Model analytics:**
- Tableau Semantics provides metric governance — same metric definition
  across Tableau, Tableau Next, AI prompts, and CRM Analytics.
- Use it for "single source of truth" KPIs.
- See [sf-datacloud-semantic-layer](../sf-datacloud-semantic-layer/SKILL.md)
  for authoring details.
<!-- SF_DOC_SYNC_END:analyze-data -->
