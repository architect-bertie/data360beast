# Data 360 Code Extension Operating Playbook

Use this playbook for custom Python scripts that run as batch data transforms
and custom functions that run in the search-index chunking pipeline. It
combines the official Salesforce workflow with public-safe proof and recovery
rules learned from authorized lab execution.

## Route the Work First

| Requirement | Code Extension type | Runtime proof |
| --- | --- | --- |
| Transform DLOs or DMOs in a batch | Custom script | Batch-transform run history plus output-object reconciliation |
| Control search-index chunking | Custom function | Search-index build plus chunk/citation validation |

Scripts and functions have different clients, contracts, and invocation
surfaces. Do not use a function as a general DLO/DMO transformation job, and do
not treat a deployed script as executed until its batch transform runs.

Official workflow: [Code Extension in Data 360](https://developer.salesforce.com/docs/data/data-cloud-code-ext/guide/use-custom-code.html).

## Preflight Contract

Before scaffold, scan, local run, deploy, or invocation, prove:

1. Explicit target-org alias, authenticated API version, and target data space.
2. Authorized lifecycle: local, disposable lab, sandbox, or production.
3. Code Extension enabled in Feature Manager and Data Cloud Architect access.
4. BYOK posture. Code Extension is not supported when BYOK is enabled.
5. Exact local toolchain: supported Salesforce CLI and plugin, Python 3.11,
   OpenJDK 17, Data Custom Code SDK, and Docker Desktop.
6. Source and target objects exist with the expected fields, types, primary
   keys, category, and write access.
7. No active job or transform dependency conflicts with the proposed target.
8. Mutation approval, one-run budget, rollback owner, and external-delivery
   boundary.

The CLI invokes `python3` on some paths. Confirm both `python3 --version` and
the exact Python 3.11 executable. Prefer a task-scoped path or virtual
environment; do not change shell profiles solely for a run. Pin Java in the
same task environment for local execution and deployment.

Current setup source: [Set Up Salesforce CLI for Code Extension](https://developer.salesforce.com/docs/data/data-cloud-code-ext/guide/set-up-sdk.html).

## Data and Package Contract

- Scripts must stay in one object family: DLO-to-DLO or DMO-to-DMO.
- Read and write objects must be different; preserve source data.
- For DMO-to-DMO work, configure the output DMO schema manually in
  `config.json`; do not use scan as a substitute for the required
  `dataObjects` definitions.
- Create and validate the output object before local execution. Match the
  output DataFrame exactly to its schema and primary key.
- Keep `payload/entrypoint.py` self-contained or audit the deployment archive
  to prove every imported helper is included and resolvable. A successful
  local run does not prove the remote package contains sibling modules.
- Deploy the generated `payload/` directory, not the project root. Exclude
  local caches, notebooks, tests, credentials, and unrelated files.
- Keep `config.json` explicit: target data space, only required read objects,
  and only intended write objects.

Official DMO schema contract: [Configure DMO Schema](https://developer.salesforce.com/docs/data/data-cloud-code-ext/guide/configure-dmo-schema.html).

## Transformation Rules

For batch scripts:

- Use Spark-native DataFrame operations such as `filter`, `groupBy`, `agg`,
  `join`, and `withColumn`.
- Avoid RDDs, custom Python UDFs, row-by-row loops, driver-side callbacks,
  per-row service calls, side effects, and large `collect()` operations.
- Select only required columns, filter early, aggregate before joins when
  appropriate, and make output deterministic.
- Validate keys before writing: non-null, non-blank, unique, and stable.
- Test nulls, type boundaries, duplicate inputs, fanout, exact output schema,
  one-row-per-key behavior, and idempotent write mode.
- Never print PII, credentials, tokens, customer identifiers, or source rows.

For chunking functions:

- Use the scaffolded typed request/runtime/response contract and return stable
  chunk order, sequence numbers, chunk types, and citations for the same input.
- Validate malformed or missing document elements without relying on mutable
  global state.
- Do not read or write DLOs/DMOs directly and do not call arbitrary external
  APIs from the function. Use only documented platform gateways where a
  supported model call is part of the approved design.
- Keep dependencies pip-installable and package only what the function needs.
- Prove chunk boundaries, context preservation, citation mapping, search-index
  build state, and retrieval output separately.

Official constraints: [Considerations When Writing Code Extension](https://developer.salesforce.com/docs/data/data-cloud-code-ext/guide/considerations-when-writing-custom-code.html).
Function-specific constraints: [Considerations When Writing Custom Chunking Functions](https://developer.salesforce.com/docs/data/data-cloud-code-ext/guide/considerations-when-writing-custom-function.html).

## Local Validation Gates

Run these as separate gates and record each result:

1. Unit tests over synthetic DataFrames.
2. Static guard scan for forbidden imports and execution patterns.
3. `script scan --dry-run` to preview inferred permissions.
4. Mutating `script scan` to update package metadata and dependencies.
5. Assert `config.json` data space and exact read/write object sets.
6. `script run` against the explicit authorized org alias.
7. Query the remote output separately. Local SDK success is local validation,
   not proof that a remote batch transform executed or published rows.

Treat dry-run scan and package-generation readiness separately. A dry-run can
pass while the real scan still lacks a packaging dependency.

## Deployment and Invocation Proof

After `script deploy`:

1. Read back `DataCustomCode` even when the CLI exits nonzero. Deployment can
   complete before a later transform-creation step fails.
2. Require the intended name, version, `CodeType`, deployment status, and
   active status.
3. Discover the associated batch transform before creating another one. Some
   plugin/runtime combinations create it during deployment.
4. If no transform exists, create one from the deployed Code Extension using
   the documented UI or current Connect API shape.
5. Record the transform ID, source and output objects, data space, status, and
   schedule readback.

Tested caveats that require target-version validation:

- A package-version bump did not update an existing Code Extension API name;
  the tested CLI path behaved as create-only and required a unique name.
- One output object was accepted by only one transform at a time.
- A failed automatic transform-creation step left the Code Extension deployed
  and active, so retrying the entire deploy would have created more drift.

Do not generalize those caveats without checking the current plugin, API, and
target org.

Official invocation source: [Create a Batch Transform from Code Extension](https://developer.salesforce.com/docs/data/data-cloud-code-ext/guide/create-batch-transform.html).

## Run, Prove, and Monitor

Immediately before the authorized run, recompute independent source controls.
Submit once, record the request or run identifier, and poll the original run to
a terminal state. Never submit another run because startup remains pending.

Proof requires all of these gates:

- Code Extension deployment readback.
- Batch-transform definition and terminal run history.
- Runtime, run mode, and rows processed.
- Output row count, distinct/non-null keys, schema, and domain controls.
- Independent source or control-query reconciliation.
- Code Extension logs scoped by package, process, execution, or correlation.
- Product-specific schedule readback.

`MktDataTransform` frequency fields alone do not prove that a schedule exists.
Use the Data Transform schedule endpoint and require frequency/type/next-date
readback. Use the Connect API for product control-plane mutations; generic
sObject describe flags do not prove that generic sObject delete or update is
supported.

Current Data Transform operations are defined in the [Data 360 Connect API reference](https://developer.salesforce.com/docs/data/connectapi/references/spec).

## Logs and Sensitive-Data Gate

Query `DataCustomCodeLogs__dll` with its real `__c` field names. Logs can take
up to about ten minutes after execution, so poll the original execution scope
instead of declaring observability missing immediately.

Check for:

- failures and module-import errors;
- PII, credentials, tokens, source values, and customer identifiers;
- execution/package/process correlation;
- platform-generated diagnostics that can contain internal runtime paths.

Separate customer-emitted sensitive content from Salesforce-generated
diagnostics in the proof ledger. Never claim that platform logs are path-free
unless the returned records prove it.

Official log fields and latency: [Query Code Extension Logs](https://developer.salesforce.com/docs/data/data-cloud-code-ext/guide/query-logs-api.html).

## Recovery Rules

- If local validation fails, do not deploy.
- If deployment fails, read back `DataCustomCode` before retrying.
- If transform creation fails, inspect existing transform/output ownership.
- If a run is pending, monitor the same run; do not resubmit.
- If a run fails, preserve run history and logs, diagnose code/schema/package
  shape, then use a new deployment identity or supported update path.
- When authorized to replace a failed transform, use the documented Data
  Transform Connect API, wait for asynchronous deletion to finish, verify the
  output object remains, then create the replacement.
- Retain no schedule or downstream activation unless each was explicitly
  authorized and independently proven.

## Production Migration

Salesforce documents sandbox validation before production migration. Use a
DevOps data kit, include referenced DLOs or DMOs manually, and preserve
dependency order: objects, Code Extension, then batch transform. A direct
production canary is lab evidence, not a replacement for that documented
lifecycle.

Official migration source: [Migrate Custom Script to Production](https://developer.salesforce.com/docs/data/data-cloud-code-ext/guide/migrate-code-to-prod.html).

## Completion Labels

- `proven`: deployment, invocation, terminal run, output reconciliation, logs,
  schedule state, and cleanup/retention are all explicit.
- `done-but-waiting`: one accepted run or log-ingestion window is still open.
- `manual-handoff`: a documented UI-only or unproven automation step remains.
- `blocked-with-reason`: an edition, BYOK, permission, schema, packaging,
  environment, dependency, or strict log-policy gate failed.
