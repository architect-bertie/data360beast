# Scorecard

Data360 Beast improved the earlier Data 360 skill layer by replacing broad notes
with a source hierarchy, phase router, OpenAPI lookup pattern, and live-tested
recipes.

| Area | Before | Now | Why |
| --- | ---: | ---: | --- |
| Connect API readiness | 5.5 | 9.7 | OpenAPI catalog, endpoint families, lab-tested payload lessons |
| Core Data 360 architecture | 8.0 | 9.5 | Phase router, proof-first delivery loop, and public model-gallery anchor/relationship map |
| Governance and data spaces | 7.5 | 9.0 | Data-space-aware validation and source rules |
| Segment, act, automation | 7.5 | 9.2 | DBT segment, data action, and activation recipes |
| Model and DMO design | 6.5 | 9.4 | Public Data 360 diagrams translated into anchor DMO, grain, relationship, consent, commerce, product, telemetry, and vertical-domain guidance |
| Unstructured retrieval and RAG | 6.8 | 9.5 | Public RAG best-practices PDF distilled into ADL/manual setup, chunking, field roles, hybrid search, retrievers, prompt grounding, Flow/Apex fallbacks, and debug metrics |
| Overall Beast mode | 7.3 | 9.8 | Full specialist skill pack, curated docs, model-gallery map, RAG playbook, manifest, and validation contract |

## Remaining Frontier

- External activation destination recipes need specific enabled targets.
- Search-index creation recipes need enabled assets and repeatable lab setup
  before moving from documented playbook guidance to tested cookbook recipes.
- Model-gallery guidance should be validated against target-org metadata before
  generating org-specific SQL, segments, activations, or Data Graphs.
- Customer-specific architecture patterns should be documented as short recipes,
  not raw scrape dumps.

## Promotion Rule

A recipe should enter the skill only when it has:

1. Official docs or OpenAPI shape.
2. A minimal payload or command.
3. Live readback proof.
4. Caveats and failure modes.
5. A short, reusable explanation.
