---
name: sf-datacloud-prepare
description: >
  Salesforce Data 360 Prepare phase for streams, DLOs, transforms, and document processing.
  TRIGGER when: the user creates or troubleshoots data streams, data lake objects,
  transforms, unstructured ingest, search index prep, or Document AI ingestion.
license: MIT
metadata:
  version: "2.0.0"
  author: "architect-bertie"
---

# sf-datacloud-prepare

Use this skill for the **ingestion and lake-prep plane**.

Beast references:
- Beast preflight: [docs/beast-preflight.md](../../docs/beast-preflight.md)
- Phase proof matrix: [docs/phase-proof-matrix.json](../../docs/phase-proof-matrix.json)
- Public operating model: [docs/operating-model.md](../../docs/operating-model.md)
- Interoperability decision map: [docs/data360/interoperability-decision-map.md](../../docs/data360/interoperability-decision-map.md)
- RAG/search-index playbook: [docs/data360/rag-search-index-retriever-playbook.md](../../docs/data360/rag-search-index-retriever-playbook.md)
- Limits source precedence: [docs/data360/limits-source-precedence.md](../../docs/data360/limits-source-precedence.md)
- Developer Guide index: [docs/data360/developer/index.md](../../docs/data360/developer/index.md)
- Proof ledger: [docs/proof-ledger.md](../../docs/proof-ledger.md)
- Public LLM map: [docs/llms.txt](../../docs/llms.txt)
- For exact Salesforce behavior, fetch official Help/Developer docs on demand with `sf-docs`.
- For endpoint shape, use OpenAPI from the official spec or the user-supplied Swagger before writing payloads.

## Prefer these Connect API families

- `GET/POST/PATCH/DELETE /ssot/data-streams`
- `POST /ssot/data-streams/:recordIdOrDeveloperName/actions/run`
- `GET/POST/PATCH/DELETE /ssot/data-lake-objects`
- `GET/POST/PUT/DELETE /ssot/data-transforms`
- `POST /ssot/data-transforms/:id/actions/run`
- `GET/POST/PATCH/DELETE /ssot/document-processing/configurations`

## Rules

- Do not jump to harmonization until stream and DLO health is clear.
- Keep dataset category decisions explicit: profile, engagement, or supporting data.
- For data streams, lock in primary key, category, event time, record modified field, refresh mode, and data space before deploy.
- Data stream formula fields use the Data 360 formula library, not Data 360 Query SQL. Use uppercase function names (`IF`, `AND`, `OR`, `UPPER`, `TRIM`, `COALESCE`), `sourceField['Header Label']` with exact case-sensitive raw header labels, `==` and `!=` for equality checks, and array-style `COALESCE([sourceField['Field'], ''])`.
- For boolean formula return types, return boolean literals (`true`, `false`) unless the target field is text. Example: `IF(UPPER(TRIM(COALESCE([sourceField['MailingCountry'], '']))) != 'US', true, false)`.
- Treat DLO work as lakehouse-prep work: validate stream status, DLO field shape, row count, null rate, and transform output before debugging downstream DMO, segment, or activation behavior.
- Direct-access data can be queryable without a manual stream run. Prove the
  federated DLO query separately, and treat acceleration configuration,
  refresh status, and cache freshness as an independent lifecycle.
- Before creating another stream for the same federated source object, inspect
  existing streams and source bindings. Some direct-access surfaces reject a
  duplicate source-object stream rather than creating a second copy.
- For acceleration schedules, send only fields valid for the selected
  frequency and prove the saved configuration. Do not populate hourly-only or
  daily-only fields by analogy.
- For performance or refresh problems, separate source extraction, DLO write, transform execution, and DMO mapping. A downstream query result is not proof that the upstream processing job is healthy.
- Choose ingestion mode from business need: real-time for sub-second operational value, streaming for minute-level incremental freshness, and batch for historical, low-velocity, or cost-sensitive data.
- Use selective fields, filters, incremental refresh, CDC, micro-batching, and source-side aggregation to control storage, network I/O, and processing cost.
- For ingestion limits, including CRM-org counts, CRM custom objects, stream
  counts, file sizes, and usage categories, use current Data 360 Limits and
  Guidelines first. Use Customer Data Platform limits only for explicit legacy
  CDP orgs or labeled comparison.
- The developer guide frames ingestion as bulk, recurring bulk, and small-batch
  streaming patterns. Match that pattern to the source and workload before
  creating DLOs or transforms.
- For web and mobile events, consider Salesforce Interactions SDK and Engagement
  Mobile SDK ingestion paths before inventing custom capture code.
- When raw detail is not required downstream, aggregate before ingestion to
  reduce storage and processing consumption.
- For engagement streams, event time is mandatory and must describe when the engagement occurred.
- Data streams feed DLOs. If a DLO is associated with a data stream, update fields through the stream rather than directly from the DLO tab.
- CRM data streams perform incremental refreshes every 10 minutes after full refresh; full refresh cadence is configurable.
- Do not modify Marketing Cloud Engagement data stream schedules after creation because supporting automations are dynamically managed.
- DMO-sourced batch transforms are restricted to a data space; DLO-sourced batch transforms are not associated with a data space.
- Use lookup when grain must stay one row per left input row; joins can multiply rows when multiple matches exist.
- Validate both row correctness and metric correctness after joins. Joining a
  header-grain measure to multiple detail rows can preserve valid-looking rows
  while inflating sums through fanout.
- Refresh mode decisions can be hard to change later; record the reason for incremental, partial, or full refresh.
- Validate transforms with source row count, output row count, null rate, duplicate rate, and schema drift checks.
- Apply or propagate governance tags to DLOs, DMO outputs, transform outputs, and sensitive fields before downstream consumption.
- Do not mask primary keys, foreign keys, fully qualified keys, event-time fields, or required join/filter fields without validating every query, transform, graph, segment, and activation path.
- Transform preview can enforce RLS differently from runtime execution; compare preview counts with run output before declaring a data issue.
- For unstructured data, curate content before indexing: focused documents,
  headings, explicit Q&A structure, detailed examples, media descriptions,
  split/structured tables, and freshness governance improve retrieval more than
  downstream prompt tweaks.
- Do not treat CSV, JSON, or XML as unstructured merely because it arrived as a
  file. Load structured fields into DLO/DMO shape first, then chunk only
  sentence-level long text fields when RAG is needed.
- For unstructured data, hand off chunking/search index design to [sf-datacloud-unstructured-retrieval](../sf-datacloud-unstructured-retrieval/SKILL.md).
- Use stream reruns for ingestion validation before blaming downstream mappings.
- Prefer programmatic payloads over UI click-memory when the user wants repeatable setup.

## STL batch-transform payload behavior (SSOT REST)

Empirical behavior of the `/ssot/data-transforms` STL payload, beyond what the
doc-synced notes below cover. The UI-facing names in the Join Operations and
Create-a-Batch-Transform docs are not always the tokens the REST payload accepts.
Confidence tags map to [docs/proof-ledger.md](../../docs/proof-ledger.md)
(`BEAST-PROOF-020`–`BEAST-PROOF-026`); these candidate observations come from one authorized org and
are not yet reproduced in Labs. API, SDK and CLI plugin versions were not
recorded unless stated explicitly below; treat them as unknown. These are
reported observations, not portable platform guarantees. Confirm the exact
surface, source/output grain, data-space context and runtime before applying them.

- **`joinType` is an enum, not the UI word.** [tested, `BEAST-PROOF-020`] The
  payload wants `INNER`, `LEFT_OUTER`, `RIGHT_OUTER`, `FULL_OUTER` — not the
  bare "left / right / full / cross" the Join Operations doc lists. A bare
  `LEFT` is rejected with `POST_BODY_PARSE_ERROR` (`LEFT_OUTER` and `INNER`
  confirmed accepted; the `*_OUTER` family is the documented set).
- **API name length.** [tested, `BEAST-PROOF-020`] The observed SSOT REST create rejected
  a transform API name longer than 32 characters, tighter than the 40-char
  figure in the UI-oriented doc note below. Budget the API name at ≤32.
- **`groupings` are bare field-name strings; string literals are single-quoted.**
  [tested, `BEAST-PROOF-020`] `groupings` is an array of plain column-name
  strings (not objects); STL string literals use single quotes (`'US'`), not
  double.
- **Handle join column collisions with `rightQualifier` + `schema.slice`.**
  [tested, `BEAST-PROOF-021`] When left and right inputs share a field name, set
  the join node's `rightQualifier` and add a `schema.slice` with `mode: "DROP"`;
  downstream formulas reference the right-side field as `"qualifier.Field"`.
  Formula alias nodes to rename join keys do not resolve the collision.
- **Validation ≠ activation ≠ runtime dispatch.** [tested, `BEAST-PROOF-022`] A
  payload can validate and activate yet still fail or silently no-op at run — a
  function that validates but will not dispatch, or a formula whose declared
  return type is wrong, surfaces only at execution. Prove with a forced full run
  plus an output readback, never with validation status alone.
- **Observed `outputD360` OVERWRITE retained prior keys on zero output.**
  [tested, `BEAST-PROOF-023`] In the observed `outputD360` case,
  prior keys survived a zero-row OVERWRITE run; this does not establish deletion
  behavior for every run type, DLO/DMO target, or other write APIs.
  That zero-row run reported terminal `SUCCESS`. A successful status alone
  does not establish useful output — check the output row count, not just run status.
- **No chaining surface found in the observed workflow.** [inferred, `BEAST-PROOF-024`] No native chaining surface was
  identified in that investigation; verify current orchestration options, then order dependent transforms with a Flow or an
  external trigger, and when a downstream transform needs run parameters, seed a
  one-row DLO it can read rather than expecting a parent transform to pass state.
- **Metadata and run ops.** [tested, `BEAST-PROOF-025`] `MktDataTransform` is the
  SOQL object for transform metadata; the run-history resource returns a
  `histories[]` array; send `{"shouldForceFullRun": true}` on the run action for
  a deterministic full run.
- **Localize a silent transform failure by graph/output bisection, not whole-payload
  retries.** [tested, `BEAST-PROOF-026`] When a transform validates and activates but
  wedges or fails at run, cut it down to a constant-output scratch probe writing only to
  a separate disposable DLO, then add one node or one source read back per iteration from a
  known-good rung; the terminal-failure-vs-still-running signal localizes the failing
  boundary one variable at a time. This isolates the boundary but does not always pin
  the underlying mechanism, and probe scaffolding must be torn down afterward.

## Code Extension runtime behavior (project evidence)

Empirical behavior of the Python Code Extension toolchain and the `DBT_HIDDEN`
batch transform a deploy auto-creates, beyond the doc-synced implementation gate
below. Confidence tags map to [docs/proof-ledger.md](../../docs/proof-ledger.md)
(`BEAST-PROOF-027`–`BEAST-PROOF-032`); these candidate observations come from one authorized
org and are not yet reproduced in Labs. SDK and CLI plugin versions are unknown.
Keep local-reader observations separate from managed execution; the local
implementation does not establish remote memory behavior or failure causes.

- **Observed deployment entitlement gate and generated transform.** [tested,
  `BEAST-PROOF-027`] The observed `script deploy` required the entitlement
  `CdpCustomCodeDeployment`; a 403 `FUNCTIONALITY_NOT_ENABLED:
  [CdpCustomCodeDeployment]` indicated that gate in the observed org; independently check permissions and packaging. That successful
  deploy registered the extension and created a batch transform
  (`creationSource: "Code Extension"`, `definition.type: "DBT_HIDDEN"`). Run and
  delete go through the same Connect APIs as native transforms; both
  `DELETE /ssot/data-transforms/{name}` and `DELETE /ssot/data-custom-code/{name}`
  worked in that org/version; their broader availability is unverified.
- **Local `script run` alone does not establish value parity.** [tested,
  `BEAST-PROOF-028`] The observed local reader (`SFCLIDataCloudReader` →
  `POST /ssot/query-sql`) returned fewer rows, consistent with a response byte cap — no `done`
  flag, no error. A 178-column DLO of 2,431 rows returned 675 rows at
  `LIMIT 1000` and 682 with no limit, while a 3-column projection returned the
  full 1,000. The inspected local reader issued `SELECT *`; projection after that read
  did not narrow the original request. A separate `ssot/queryv2` query returned
  the requested rows in this test. For parity, reconcile independent counts and
  consume all query batches; `LIMIT` alone does not prove completeness.
- **The inspected local reader eagerly materialized data.** [tested,
  `BEAST-PROOF-029`] The inspected implementation built a PySpark frame from an
  already materialized pandas frame; downstream `.select`/`.filter` could not
  narrow that local pull. SDK/plugin versions and applicability to the managed
  runtime are unknown. Do not conclude that avoiding the object is the only
  memory optimization or that this caused a particular deployed failure.
- **Normalize keys and declare the write schema explicitly.** [tested,
  `BEAST-PROOF-030`] The inspected reader returned sample keys with zero padding, stripped padding,
  or floating-point representation. Verify actual types and normalize keys only
  against the intended source/target contract before joining.
  The investigation reported an all-null column/type-inference failure; declare an explicit `StructType` from the target's field definitions.
  The inspected `Client` exposed no `.spark`; use `SparkSession.builder.getOrCreate()`.
- **The observed failed run exposed no error text.** [tested, `BEAST-PROOF-031`] The observed
  `DBT_HIDDEN` run-history row returned `status: FAILURE` with
  `processedRows: 0` and empty `outputStatus` (identical on v63.0 and v67.0).
  Diagnosis comes from a local `script run` and the `DataCustomCodeLogs__dll` log
  surface, not from a deploy-and-observe loop.
- **Check the payload closure and requirements after `script scan`.**
  [tested, `BEAST-PROOF-032`] The inspected `script scan` rewrote `requirements.txt` as
  `sorted(set(existing).union(imports))` — reading comment lines as requirements
  and writing discovered imports unpinned — and it walks the whole package
  directory, so a module that ships in the payload but is never imported still
  contributes its imports (an unused module importing `snowflake.connector`
  staged `snowflake` into the venv). Ship only the modules the entrypoint
  transitively imports and assert the pin set in CI.

## Prepare helper scripts

All five helpers are retained. Their implementation is checked offline with
synthetic fixtures and mocked clients; live lifecycle certification remains
pending. See [references/prepare-helper-contract.md](references/prepare-helper-contract.md)
for CLI changes, supported shapes, ownership, limits of static checks, and
incomplete-result handling.

- [scripts/stl_ref_check.py](scripts/stl_ref_check.py): check bare and quoted
  formula references, explicit input projections and supported DROP slices.
  Unsupported shapes return INCONCLUSIVE, not a clean pass. Offline.
- [scripts/stl_builder_shape.py](scripts/stl_builder_shape.py): split formula and
  typeCast nodes independently of JSON order, preserve properties, validate
  connectivity, and replace the input only after successful validation. Offline.
- [scripts/stl_activation_bisect.py](scripts/stl_activation_bisect.py): offline
  preview by default. Live creation/run/cleanup requires `--execute` and
  `--environment lab|sandbox`, an explicit org and separate scratch DLO. Uses
  unique owned probes; refuses collisions and production outputs. Timeouts are
  inconclusive and unresolved cleanup requires operator attention.
- [scripts/ce_payload_closure.py](scripts/ce_payload_closure.py): resolve static
  flat/relative/package imports, check drift read-only with `--check`, and replace
  only an empty or marked generated directory. Dynamic imports/resources are not
  certified. Offline.
- [scripts/ce_run_diagnostics.py](scripts/ce_run_diagnostics.py): read transform-
  scoped logs in timestamp order, with optional execution/time filters and
  bounded polling. Requires an explicit org and query data space. Reports scope,
  pagination, truncation and terminal status separately; never treats logs as
  independent output-correctness proof.

This troubleshooting layer complements the lifecycle playbook proposed in
[PR #10](https://github.com/architect-bertie/data360beast/pull/10). It does not
replace deployment, invocation, terminal status, independent output reconciliation,
log, or schedule proof.

## Production Gates

1. connection healthy
2. schema uploaded or discovered
3. stream deployed in correct data space
4. DLO record count matches source expectation
5. DMO mapping path identified
6. transform run completes and output is queryable
7. object and field tags/classifications are applied or propagated
8. target users can view only the intended DLO/DMO/transform output
9. monitoring path exists for failures and late data

## Handoff

When stream output looks right, move to [sf-datacloud-harmonize](../sf-datacloud-harmonize/SKILL.md).
For data spaces, tags, masking, and access policies, use [sf-datacloud-governance](../sf-datacloud-governance/SKILL.md).

## Doc-Synced Notes

<!-- SF_DOC_SYNC_START:prepare-and-model -->
### Prepare and Model Data (Cleansing, Transforms, Modeling Pipeline)

_Distilled from official Salesforce sources only._

**Sources:**
- data.c360_a_prepare_and_model_data.htm — Prepare and Model Data overview
- data.c360_a_cleansing_data.htm — Data Cleansing and Preparation
- data.c360_a_batch_transform_overview.htm — Batch Data Transforms
- data.c360_a_batch_transform_create.htm — Create a Batch Data Transform
- data.c360_a_streaming_transform_overview.htm — Streaming Data Transforms
- data.c360_a_batch_transform_join_operations.htm — Join Operations
- data.c360_a_transform_record_event_flow.htm — Data Transform Record Event Flow
- developer.salesforce.com/docs/data/data-cloud-code-ext/guide/create-batch-transform.html — Code Extension Batch Transform

**The Prepare-and-Model pipeline (canonical order):**
1. **Ingest** raw data into Data Lake Objects (DLOs) via data streams.
2. **Cleanse** with batch or streaming transforms (formula fields,
   normalization, deduplication signals).
3. **Map** DLOs to Data Model Objects (DMOs) using the Customer 360 Data
   Model schema (or Starter Data Bundles for auto-mapped sources).
4. **Resolve identities** to build unified profiles (handoff to harmonize).
5. **Enrich** with calculated insights, data graphs (downstream).

**Streaming Data Transforms:**
- Clean and enrich data in **near real-time** as records enter the system.
- Read records from a source DLO → run SQL query → write to target DLO →
  map to DMO.
- Required ingredients: source DLO, target DLO, SQL query, DMO mapping.
- Use cases: phone normalization (split mobile/home/work into separate
  contact-point records via `UNION`), credit-card fraud detection
  (aggregating across processing systems), email standardization.
- For modifying selected data on a scheduled interval, use a **batch
  transform** instead.
- Streaming transforms feed Streaming Insights for real-time event
  detection.

**Batch Data Transforms:**
- For complex, scheduled transformations across volumes of historical or
  reference data.
- Created from the **Data Transforms** tab → New → Batch Data Transform.
- Naming: alphanumeric + underscore, starts with letter, max 40 chars,
  unique API name.
- Capabilities:
  - Input nodes (read from DLOs/DMOs)
  - Output nodes (write to DLOs/DMOs)
  - Join operations (inner, left, right, full, cross)
  - SQL-based transformation logic
  - Custom code via Code Extension (Beta) — invocable Apex equivalent
    for transforms.
- Permission required: **Data Cloud Architect**.
- Available editions: Developer, Enterprise, Performance, Unlimited.

**Choosing between Batch and Streaming:**
| Factor | Batch | Streaming |
|---|---|---|
| Latency | Scheduled (minutes to hours) | Near real-time |
| Volume | High (millions of records per run) | Per-record |
| Source | DLO/DMO | DLO only |
| Use case | History reshape, periodic enrichment, joins | Live normalization, fraud signals, event flows |
| Pairs with | Calculated Insights, Activations | Streaming Insights, Data Actions |

**Data Cleansing best practices:**
- Cleanse before unification (identity resolution); cleaner inputs produce
  better unified profiles.
- Standardize phone formats (`+1XXXXXXXXXX`), email casing, address
  components before identity match.
- Deduplicate at the source level when possible; identity resolution
  handles cross-source duplication.
- Use formula fields for inline cleansing during ingest; reserve
  transforms for cross-DLO logic.
- Track cleansing decisions in field-level descriptions / tags for
  governance.

**Data Transform Record Event Flow:**
- Lightweight event-driven transformation that fires on individual record
  events (rather than scheduled batch).
- Useful when downstream consumers need per-record cleansing in event
  context.

**Inline transformations (formula fields):**
- Applied during ingest within a data stream definition.
- Use cases: simple casts, concatenation, normalization, conditional
  defaults.
- Reserve heavy logic for batch/streaming transforms.

**Validation gates for the Prepare phase:**
- Source DLO is populated with the expected schema and record count.
- Cleansing rules are documented and traceable.
- Transform definitions exist for every non-trivial cleansing step.
- Target DLO/DMO mapping is verified (no field type mismatches).
- Schedule cadence aligns with downstream identity resolution and CI runs.
<!-- SF_DOC_SYNC_END:prepare-and-model -->

<!-- SF_DOC_SYNC_START:limits-data-ingestion -->
### Data ingestion and transform limit gate

_Auto-synced from the local sf-docs cached Salesforce Help export (official docs only)._

**Sources (sf-docs cached Help):**
- data.c360_a_limits_and_guidelines.htm — Data 360 Limits and Guidelines | Salesforce Help

**Source fingerprint:** `1ce0aa69b0b275b02c26170b`

**Notes:**
- Treat the captured Limits and Guidelines page as a required source before making durable guidance for this phase.
- Separate soft guidelines from hard limits, and call out when a limit can require an Account Executive request or org-specific validation.
- Before recommending stream count, refresh cadence, file volume, transform shape, or retry behavior, check the captured ingestion and transform limit families.
- Prefer smaller probes and explicit readback when a design can affect metered ingestion, processing, or storage.
- Relevant limit families currently captured include: General Guidelines and Limits, Activation Guidelines and Limits, AI Models (formerly Einstein Studio) Guidelines and Limits, Calculated Insights Guidelines and Limits, Code Extension Guidelines and Limits, Data Actions Guidelines and Limits, Data Explorer Guidelines and Limits, Data Federation Guidelines and Limits, Data Graphs Guidelines and Limits, Data Ingestion Guidelines and Limits, Data Model Object Guidelines and Limits, Data Shares Guidelines and Limits.

<!-- SF_DOC_SYNC_END:limits-data-ingestion -->

<!-- SF_DOC_SYNC_START:developer-code-extension -->
### Code Extension implementation gate

_Auto-synced from sf-docs captures of official Salesforce Developer documentation._

**Sources:**
- https://developer.salesforce.com/docs/data/data-cloud-code-ext/guide/use-custom-code.html - Code Extension in Data 360 | Data 360 Code Extension Guide | Salesforce Developers
- https://developer.salesforce.com/docs/data/data-cloud-code-ext/guide/set-up-sdk.html - Set Up Salesforce CLI for Code Extension | Code Extension in Data 360 | Data 360 Code Extension Guide | Salesforce Developers
- https://developer.salesforce.com/docs/data/data-cloud-code-ext/guide/configure-dmo-schema.html - Configure Data Model Object Schema for DMO-DMO Transforms | Code Extension in Data 360 | Data 360 Code Extension Guide | Salesforce Developers
- https://developer.salesforce.com/docs/data/data-cloud-code-ext/guide/query-logs-api.html - Query Code Extension Logs by Using the Query API | Code Extension in Data 360 | Data 360 Code Extension Guide | Salesforce Developers
- https://developer.salesforce.com/docs/data/data-cloud-code-ext/guide/migrate-code-to-prod.html - Migrate Custom Script to Production | Code Extension in Data 360 | Data 360 Code Extension Guide | Salesforce Developers

**Source fingerprint:** `9036b5bba36903a6a01af098`

**Implementation notes:**
- Separate scripts, which run as batch data transforms, from functions, which run in the search-index chunking pipeline.
- Preflight the documented local toolchain and exact runtime versions before scaffold, scan, local run, or deploy.
- For DMO-to-DMO transforms, configure the DMO write schema explicitly; do not assume the CLI scan command can infer it.
- Use `DataCustomCodeLogs__dll` plus deployment and transform status as execution proof; deployment success alone is insufficient.
- Move validated code through a DevOps data kit and include referenced DLOs or DMOs explicitly when the data kit does not add them automatically.

<!-- SF_DOC_SYNC_END:developer-code-extension -->
