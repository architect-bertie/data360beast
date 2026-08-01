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

| ID | Surface | Phase | Proof/Readback | Caveat | Confidence | Labs Reference | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `BEAST-PROOF-001` | Query SQL and Profile API | retrieve | Query/profile surfaces were validated as useful data and metadata proof paths. | Query success does not prove transform, segment, analytics, activation, or orchestration behavior. | tested | none, pre-Labs evidence | promoted |
| `BEAST-PROOF-002` | DBT segment create/read/count | segment | DBT segment create used `includeDbt.models.models[]`; readback can normalize to `includeDbt.models[]`; status/count readback is stronger first proof than members. | Approximate count can fail when the org feature is disabled; member retrieval depends on a delta window. | tested | none, pre-Labs evidence | promoted |
| `BEAST-PROOF-003` | Data action target and data action create | automation | Target/action creation behavior was validated in lab conditions. | Delivery proof is separate from configuration proof; external payloads need explicit approval and governance review. | tested | none, pre-Labs evidence | promoted |
| `BEAST-PROOF-004` | Activation target create/readback | act | Activation target readback by returned ID was reliable in lab testing. | Destination delivery and activation publish proof still depend on enabled target and scenario-specific validation. | tested | none, pre-Labs evidence | promoted |
| `BEAST-PROOF-005` | Search index and calculated insight list surfaces | ai-search, insight | List surfaces were explored and can support discovery. | Creation proof needs enabled assets and repeatable Labs scenarios before promotion. | inferred | future Labs evidence required | candidate |
| `BEAST-PROOF-006` | Data stream formula fields | prepare | Formula fields use Data 360 formula library syntax, not Query SQL. | Exact source labels and function support must be checked in the target stream/setup surface. | documented | none, pre-Labs evidence | promoted |
| `BEAST-PROOF-007` | Pro-code RAG retrieval | ai-search | `vector_search` and `hybrid_search` should be driven from Query SQL or Apex only after metadata confirms index DMO, chunk DMO, source joins, and filter fields. | Hybrid search is not a category lookup engine and can affect cost/latency. | documented | future Labs evidence recommended | documented |

## Promotion Rule

Do not promote Labs material into Beast unless it can be summarized without raw
customer data, credentials, raw org metadata, or bulky generated payload dumps.
When evidence is too scenario-specific, leave it in Labs and link to it only
from a future cookbook candidate.

## Doc-Synced Notes

<!-- SF_DOC_SYNC_START:weekly-watch-gate -->
### Usage and access changelog gate

_Auto-synced from the local sf-docs cached Salesforce Help export (official docs only).

**Sources (sf-docs cached Help):**
- data.c360_a_changelog_usage_and_access.htm — Data 360 Usage and Access Changes | Salesforce Help

**Source fingerprint:** `605fd9a0b6ac010e940b297c`

**Notes:**
- Check this changelog before treating older Beast guidance as durable; it tracks licensing, access, availability, billing, limits, and permission-set documentation changes.
- When a changelog entry touches a phase, update the owning specialist skill and any public-safe markdown map in the same run.
- Most recent captured entry headings: July 7, 2026, June 23, 2026, June 22, 2026, June 12, 2026, June 5, 2026, May 22, 2026, May 19, 2026, May 12, 2026.

<!-- SF_DOC_SYNC_END:weekly-watch-gate -->
