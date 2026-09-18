# Prepare helper contract

These helpers support diagnosis and local preparation. Their regression tests
use synthetic files and mocked clients. They are not live-org certification.

## Scratch bisection

`stl_activation_bisect.py body.json --org <alias> --scratch-dlo <separate-DLO>
--cuts <first> <later>` prints an offline JSON preview. It does not resolve CLI
authentication or call Salesforce. Add `--execute --environment lab|sandbox` only
inside an explicitly authorized disposable boundary. Production execution is
unsupported. The scratch DLO must already exist; its schema and intended use
must be verified by the operator. The helper never creates or deletes that DLO.

Use `--api-version <version>` to pin the surface. During explicit execution only,
the helper can read the authenticated CLI version; an absent/invalid version
stops execution instead of falling back. An environment flag declares the
operator's boundary; it is not proof of an org's lifecycle or permissions.
DLO and DMO data-space semantics must be established before running. An existing
`dataSpaceName` is preserved; the helper does not invent one for DLO transforms.

Each invocation uses unique names. Existing names are never replaced. A create
must return an ID, and readback must match that ID and the invocation marker
before cancellation or deletion. A missing ID, uncertain POST, ownership
mismatch or failed cleanup produces `UNRESOLVED CLEANUP`; retain that name and
resolve it manually in the authorized org. Do not rerun with a destructive reset.

Probe graphs must have exactly one output to the separate scratch DLO. Output
cuts, other write actions, source/output target reuse, unsupported graph actions,
missing sources and cycles are rejected. The original graph remains unchanged.

Activation `ERROR` is a failed probe that can inform bisection. Timeouts are
inconclusive. Bisection assumes monotonic failure across the supplied cuts;
reported boundaries are observations, not proof of root cause, output values,
or production readiness. All-passing cuts do not prove the original output is
the culprit. Request subprocesses have a 60-second timeout; polling windows
exclude time already spent inside a request.

## Static Python closure

`ce_payload_closure.py --source <source-dir> --payload <root-module-dir>
--closure-dir <generated-dir> --roots <entrypoint> [--package-name <name>]`
builds the static Python closure. `--package-name` defaults to the generated
directory name. Static flat, relative and package-qualified imports are
supported; required package initializers and nested module paths are retained.
Flat import users must still arrange an appropriate Python module search path.

`--check` compares without writing. Missing local modules, unsupported dynamic
imports, wildcard local imports and unsafe paths fail instead of producing an
apparently complete payload. This is not a general Python dependency resolver:
reflection, runtime code generation, package resources and external dependencies
remain outside the guarantee. Pin and verify third-party requirements separately.

Writing requires an empty destination or the helper's `.beast-closure.json`
ownership marker. Existing unmarked content or files outside that marker's
inventory are preserved by refusing the write. For a legacy unmarked generated
copy, use a new empty destination, review it, and retire the old copy separately.
Never point the destination at the source, payload root or an ancestor of either.
Inputs are parsed first, output is staged beside the destination, and failed
replacement restores the old generated directory. Do not edit the generated
directory concurrently with a build.

## STL offline helpers

`stl_builder_shape.py` preserves source properties, splits multi-field nodes,
rewires in a second pass, and validates connectivity before atomic replacement.
Schema operations are applied to the tail of a split chain. Input ordering and
generated-name collisions cannot remove graph edges. These checks do not prove
that a particular Builder version accepts the resulting graph.

`stl_ref_check.py` recognizes single-quoted string literals, doubled quotes,
ordinary and qualified quoted identifiers, bare identifiers, comments and
function calls. It checks explicit load-field projections and `schema.slice`
with `mode: DROP`, string `fields`, and optional `ignoreMissingFields`.
`schema.fields` is treated as type metadata, not a projection. Missing load
metadata, other slice modes, unknown actions, unequal append schemas and
nonempty grain extraction definitions return `INCONCLUSIVE` (exit 2). Missing
references return exit 1; supported checks with no missing reference return 0.
Neither result establishes full SQL syntax validity or runtime dispatch.

## Scoped Code Extension diagnostics

`ce_run_diagnostics.py <transform> --org <alias> --data-space <space>` takes a
single read-only snapshot. Optional flags are `--api-version`, `--execution-id`,
`--since`, `--until`, `--limit` (default 50, maximum 1000), `--wait-seconds`
(default 0, maximum 3600), and `--poll-seconds` (default 15). Time filters require
ISO timestamps with timezones. The old unrestricted `--where` is removed.

The query always filters `ProcessDefinitionName__c` and orders `Timestamp__c`
descending. Execution and time filters further narrow the result. Values are
escaped; undocumented string escape forms are rejected. Query pagination is
followed within the row budget, with a separate 100-page guard; uncertain or
capped results are labeled incomplete/truncated. Hitting the requested limit is
conservatively labeled truncated even when the limited query itself is complete.
Query data-space context is carried on initial and subsequent batches.

The JSON report retains `transform`, `run`, and `logs`, adding correlation scope,
terminal status, completeness, truncation, errors and timeout. History represents
the latest transform run. Supplying an execution ID scopes logs but does not prove
they match that history row. `complete` means a terminal history snapshot and
available, uncapped, fully retrieved log query; it never means lifecycle or
output correctness is proven. Missing schema or permissions are reported without
falling back to an unscoped `SELECT *`. Exit 2 signals an incomplete report.

Keep log reports local: messages may contain customer information or secrets.
Do not commit raw logs to Beast.

Official sources:

- [Code Extension log fields and delayed availability](https://developer.salesforce.com/docs/data/data-cloud-code-ext/guide/query-logs-api.html)
- [Salesforce Query v2 and query-batch API](https://www.postman.com/salesforce-developers/salesforce-developers/documentation/wgh5wpn/salesforce-data-360-connect-apis)
- [DLO output-node write modes](https://help.salesforce.com/s/articleView?id=data.c360_a_batch_transform_output_node_dlo.htm&language=en_US&type=5)

## Candidate evidence and pending lifecycle work

Prepare observations use `BEAST-PROOF-020` through `BEAST-PROOF-032`, all with
candidate promotion status. SDK/plugin versions remain unknown; some entries
record API versions. Local reader inspection does not establish managed runtime
behavior. Promotion still requires a synthetic Labs reproduction, version and
data-space envelope, exact surface, and readback, without raw customer artifacts.

The lifecycle evidence ID reserved for
[PR #10](https://github.com/architect-bertie/data360beast/pull/10) is independent
of these candidate entries. That playbook remains the complementary lifecycle
contract; PR #12 does not merge or modify it.
