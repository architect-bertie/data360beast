# Data360 Beast Proof Ledger

This ledger is the public-safe evidence layer for Data360 Beast. It is not a
golden path, scenario walkthrough, or cookbook. It records what has been proven,
where the proof came from, what caveats matter, and whether the evidence is
ready to inform the operating model.

Future cookbook material is developed in
[`data360beast-labs`](https://github.com/architect-bertie/data360beast-labs).
Only distilled, public-safe evidence graduates back into this ledger.

## Promotion Status

| Status | Meaning |
| --- | --- |
| `lab-only` | Evidence exists only in Labs or local work and is not ready for Beast. |
| `candidate` | Promising result, but missing source, readback, caveat, or repeatability. |
| `documented` | Supported by official Salesforce docs or OpenAPI, without target-org proof. |
| `tested` | Validated in an explicitly authorized org with public-safe readback evidence. |
| `promoted` | Stable enough to influence Beast operating guidance or a specialist skill. |
| `retired` | Superseded by current docs, API behavior, or a stronger proof entry. |

## Entry Contract

Every promoted entry must include:

| Field | Required Content |
| --- | --- |
| `id` | Stable evidence ID, such as `BEAST-PROOF-001`. |
| `source` | Official docs, OpenAPI, Labs evidence, or live validation source. |
| `surface` | API, skill, phase, object layer, query plane, or tool. |
| `phase` | Beast phase from `phase-proof-matrix.json`. |
| `data-space assumptions` | Data space scope or reason it is not applicable. |
| `proof/readback` | Returned ID, status, count, metadata, query result, or failure response. |
| `caveat` | Where the evidence does not apply or needs target-org validation. |
| `confidence` | `documented`, `tested`, or `inferred`. |
| `labs reference` | Labs issue, scenario, PR, or `none` for pre-Labs evidence. |
| `promotion status` | One of the statuses above. |

## Current Evidence

| ID | Source | Surface | Phase | Data-Space Assumptions | Proof/Readback | Caveat | Confidence | Labs Reference | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `BEAST-PROOF-001` | Pre-Labs authorized-org validation | Query SQL and Profile API | retrieve | Resolve and report the target data space. | Query/profile surfaces returned usable data and metadata readbacks. | Query success does not prove transform, segment, analytics, activation, or orchestration behavior. | tested | none, pre-Labs evidence | promoted |
| `BEAST-PROOF-002` | Pre-Labs OpenAPI and authorized-org validation | DBT segment create/read/count | segment | Segment On DMO and API requests must resolve in the same data space. | DBT segment create used `includeDbt.models.models[]`; readback normalized to `includeDbt.models[]`; status/count readback was stronger first proof than members. | Approximate count can fail when the org feature is disabled; member retrieval depends on a delta window. | tested | none, pre-Labs evidence | promoted |
| `BEAST-PROOF-003` | Pre-Labs authorized-org validation | Data action target and data action create | automation | Target/action assets and source events must resolve in the intended data space. | Target/action creation returned IDs and readable configuration. | Delivery proof is separate from configuration proof; external payloads need explicit approval and governance review. | tested | none, pre-Labs evidence | promoted |
| `BEAST-PROOF-004` | Pre-Labs authorized-org validation | Activation target create/readback | act | Activation target and source segment must be visible in the same authorized context. | Activation target readback by returned ID was reliable. | Destination delivery and activation publish proof still depend on the enabled target and downstream system. | tested | none, pre-Labs evidence | promoted |
| `BEAST-PROOF-005` | Pre-Labs API exploration | Search index and calculated insight list surfaces | ai-search | Discover assets in the target data space before choosing an index or insight. | List surfaces supported asset discovery. | Creation and execution proof need enabled assets and repeatable Labs evidence. | inferred | future Labs evidence required | candidate |
| `BEAST-PROOF-006` | Official Salesforce Help | Data stream formula fields | prepare | Formula source and output DLO are data-space scoped. | Formula fields use the Data 360 formula library syntax rather than Query SQL. | Exact source labels and function support must be checked in the target stream/setup surface. | documented | none, pre-Labs evidence | promoted |
| `BEAST-PROOF-007` | Official Salesforce Help and Developer documentation | Pro-code RAG retrieval | ai-search | Resolve source DMO/UDMO, index DMO, chunk DMO, and retriever in the target data space. | `vector_search` and `hybrid_search` can be driven from Query SQL or Apex after metadata confirms joins and filter fields. | Hybrid search is not a category lookup engine and can affect cost and latency. | documented | future Labs evidence recommended | documented |
| `BEAST-PROOF-008` | Labs zero-copy interoperability evidence | Federated streams and mixed DLO queries | connect | Connection, stream, DLO, and query must use the same intended data space. | Direct-access streams were queryable without a manual run; acceleration settings read back independently; federated and ingested DLOs joined successfully. | Query success did not guarantee metric correctness: joining order headers to lines inflated header measures through fanout. | tested | [zero-copy gauntlet](https://github.com/architect-bertie/data360beast-labs/blob/main/labs/beastwear-lab/proof/zero-copy-gauntlet-2026-05-21.md) | promoted |
| `BEAST-PROOF-009` | Labs connector and mapping evidence | Connector readiness chain | connect | Prove the selected connection and resulting objects in the target data space. | A healthy connection was insufficient; readiness required source-object discovery, source permissions, stream/DLO creation, DLO query, DMO mapping, and DMO query. | Connector-specific grants, network paths, and source table eligibility remain source-platform dependent. | tested | [segment and activation proof](https://github.com/architect-bertie/data360beast-labs/blob/main/labs/beastwear-lab/proof/segment-activation-proof-2026-05-13.md) | promoted |
| `BEAST-PROOF-010` | Labs identity-resolution evidence | Identity ruleset lifecycle | harmonize | Source and unified DMOs must be resolved in the ruleset data space. | A published ruleset produced empty unified DMOs while the job was still in progress; rows appeared only after terminal job completion. | Ruleset IDs, supported match objects, and rule strength validation are org-sensitive. | tested | [identity and standard model proof](https://github.com/architect-bertie/data360beast-labs/blob/main/labs/beastwear-lab/proof/identity-mc-standard-proof-2026-05-14.md) | promoted |
| `BEAST-PROOF-011` | Labs calculated-insight evidence | Calculated insight lifecycle | insight | Source DMOs and output CIO must resolve in the target data space. | Insight definitions were active before output existed; terminal run success plus CIO row queries proved materialization. | Preview, save, run, and output retrieval are separate gates and can fail independently. | tested | [identity and standard model proof](https://github.com/architect-bertie/data360beast-labs/blob/main/labs/beastwear-lab/proof/identity-mc-standard-proof-2026-05-14.md) | promoted |
| `BEAST-PROOF-012` | Labs segment failure evidence and official DBT validation docs | Query-to-segment alignment | segment | Query, Segment On DMO, and segment must use the same data space and grain. | Queries returned filtered counts while malformed segment definitions counted the entire anchor, including a query expected to return zero. | Never publish from query proof alone; compare expected query count, segment count, membership, and publish state. | tested | [segment and activation proof](https://github.com/architect-bertie/data360beast-labs/blob/main/labs/beastwear-lab/proof/segment-activation-proof-2026-05-13.md) | promoted |
| `BEAST-PROOF-013` | Labs activation evidence | Segment publish, activation, and delivery | act | Segment, activation target, activation, and destination authorization must align to the target data space and channel. | Target status, segment publish job, activation definition, and downstream delivery were observable as separate states. | `ACTIVE`, a successful publish call, or `PUBLISHING` does not prove destination delivery. | tested | [segment and activation proof](https://github.com/architect-bertie/data360beast-labs/blob/main/labs/beastwear-lab/proof/segment-activation-proof-2026-05-13.md) | promoted |
| `BEAST-PROOF-014` | Labs Marketing Cloud and identity evidence | Marketing Cloud stream readiness | connect | Map the correct enterprise/root business unit and activation business unit to the intended data space. | Business-unit mapping was a hard prerequisite; standard stream creation used root-level context and platform-managed refresh behavior. | Discovery can be empty even when a known standard object is creatable; behavior must be verified in the target tenant. | tested | [identity and standard model proof](https://github.com/architect-bertie/data360beast-labs/blob/main/labs/beastwear-lab/proof/identity-mc-standard-proof-2026-05-14.md) | promoted |
| `BEAST-PROOF-015` | Local project evidence plus official Databricks Integration Guide | Databricks file-federation source eligibility | connect | The connection and direct-access stream are data-space scoped; catalog and storage permissions are external. | A default-storage managed table was rejected for external access; the corrected design requires an externally accessible, supported table/storage path plus catalog and object-store grants. | The exact table-kind error is Databricks-specific and needs a public Labs reproduction before becoming a universal rule. | tested | future Labs reproduction required | candidate |
| `BEAST-PROOF-016` | Beastlab full-spin runtime validation | Desired-state runtime target discovery | develop-package | Target org alias and target data space must be explicit; do not rely on local Salesforce CLI defaults. | Runtime planning failed to verify data spaces when it used stale `sf api request rest --url --json` flags and a hard-coded v66 path; the corrected runtime uses the authenticated/spec API version and reads back `default` without storing org identifiers. | Capability support still means target org plus target data-space reachability unless a specialist adapter proves the individual surface. | tested | local Beastlab full spin 2026-08-01 | promoted |
| `BEAST-PROOF-017` | Beastlab full-spin Query SQL validation | Calculated insight output reconciliation | insight | Source DMO and CIO output must resolve in the same data space. | `CI_Beastwear_Channel_Revenue__cio` totals matched an independent aggregate query over `BEASTWEAR_Order__dlm` by channel, order count, and revenue. | Existing successful CI job metadata alone is not enough; output rows and a control query are separate proof gates. | tested | local Beastlab full spin 2026-08-01 | promoted |
| `BEAST-PROOF-018` | Beastlab full-spin segment validation | Segment membership latest/history proof | segment | Segment status, publish status, membership DMO, and data space must be reported together. | A published Beastwear segment reported 4,027 members; its latest membership DMO contained 4,027 rows while the history DMO contained 0 rows for the same spot check. | Do not assume every membership DMO has current members; prove whether the requested check needs latest, history, or publish-status fields. | tested | local Beastlab full spin 2026-08-01 | promoted |

## Promotion Rule

Do not promote Labs material into Beast unless it can be summarized without raw
customer data, credentials, raw org metadata, or bulky generated payload dumps.
When evidence is too scenario-specific, leave it in Labs and link to it only
from a future cookbook candidate.

## Doc-Synced Notes

<!-- SF_DOC_SYNC_START:weekly-watch-gate -->
### Usage and access changelog gate

_Auto-synced from the local sf-docs cached Salesforce Help export (official docs only)._

**Sources (sf-docs cached Help):**
- data.c360_a_changelog_usage_and_access.htm — Data 360 Usage and Access Changes | Salesforce Help

**Source fingerprint:** `605fd9a0b6ac010e940b297c`

**Notes:**
- Check this changelog before treating older Beast guidance as durable; it tracks licensing, access, availability, billing, limits, and permission-set documentation changes.
- When a changelog entry touches a phase, update the owning specialist skill and any public-safe markdown map in the same run.
- Most recent captured entry headings: July 7, 2026, June 23, 2026, June 22, 2026, June 12, 2026, June 5, 2026, May 22, 2026, May 19, 2026, May 12, 2026.

<!-- SF_DOC_SYNC_END:weekly-watch-gate -->
