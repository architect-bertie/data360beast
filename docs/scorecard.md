# Scorecard

Data360 Beast improved the earlier Data 360 skill layer by replacing broad notes
with a source hierarchy, phase router, OpenAPI lookup pattern, and live-tested
evidence.

| Area | Before | Now | Why |
| --- | ---: | ---: | --- |
| Connect API readiness | 5.5 | 9.7 | OpenAPI catalog, endpoint families, proof ledger entries, and tested caveats |
| Core Data 360 architecture | 8.0 | 9.5 | Phase router, operating model, proof-first delivery loop, and public model-gallery anchor/relationship map |
| Governance and data spaces | 7.5 | 9.0 | Data-space-aware validation and source rules |
| Segment, act, automation | 7.5 | 9.2 | DBT segment, data action, and activation evidence |
| Model and DMO design | 6.5 | 9.4 | Public Data 360 diagrams translated into anchor DMO, grain, relationship, consent, commerce, product, telemetry, and vertical-domain guidance |
| Unstructured retrieval and RAG | 6.8 | 9.5 | Public RAG best-practices PDF distilled into ADL/manual setup, chunking, field roles, hybrid search, retrievers, prompt grounding, Flow/Apex fallbacks, and debug metrics |
| Deterministic proof routing | 7.0 | 9.6 | Beast preflight, machine-readable phase proof matrix, docs-watch discipline, mutation gate, and prompt-level evals |
| Evidence promotion | 6.0 | 9.4 | Labs boundary, proof ledger status model, public-safe promotion rules, and compatibility stub for old links |
| Operational hardening | 5.0 | 9.3 | Executable eval fixtures, install smoke test, MCP readiness check, release readiness check, phase coverage matrix, cost/usage sizing contract, and develop/package/deploy matrix |
| Overall Beast mode | 7.3 | 9.9 | Full specialist skill pack, curated docs, model-gallery map, RAG playbook, operating model, preflight, proof matrix, validation contract, 64 distilled Help articles, 38 doc-synced blocks, 140+ connector catalog, and per-topic reference files for context hygiene |

Scores are evidence maturity scores. They reflect how reliably an agent can
route to the right source and proof path, not a claim that every Data 360 asset
or destination has been live-tested.

## Remaining Frontier

- External activation destination evidence needs specific enabled targets.
- Search-index creation evidence needs enabled assets and repeatable lab setup
  before moving from documented playbook guidance to tested proof ledger evidence.
- Model-gallery guidance should be validated against target-org metadata before
  generating org-specific SQL, segments, activations, or Data Graphs.
- Customer-specific architecture patterns should be documented as short evidence,
  not raw scrape dumps.
- The operational hardening tools are deterministic checks; they do not replace
  live org playbooks, delivery recipes, or Beast Labs promotion evidence.

## Promotion Rule

Evidence should enter Beast only when it has:

1. Official docs or OpenAPI shape.
2. A minimal payload or command.
3. Live readback proof.
4. Caveats and failure modes.
5. A short, reusable explanation.
6. No raw customer data, credentials, org metadata dumps, or bulky Labs traces.

Before raising any score, run the relevant checks in
[`beast-evals.md`](beast-evals.md). A score increase must add proof, not merely
more prose.
