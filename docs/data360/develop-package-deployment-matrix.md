# Develop, Package, And Deploy Matrix

Use this matrix when Data 360 work moves from design into reusable metadata,
data kits, packaging, sandbox validation, or production deployment. Scenario
walkthroughs and org traces stay in Beast Labs; this file defines the
public-safe proof contract.

## First Decision

| Question | Route |
| --- | --- |
| Is the user creating or validating an API payload? | `sf-datacloud-connectapi` plus OpenAPI. |
| Is the user moving supported metadata between orgs? | Data kits and Metadata API coverage checks. |
| Is the user proving a full implementation path? | Beast Labs scenario, then promote distilled proof. |
| Is the user estimating cost or environment replay? | Cost and usage sizing contract. |

## Deployment Surfaces

| Surface | Package/Deploy Habit | Minimum Proof |
| --- | --- | --- |
| Data streams and DLO setup | Confirm whether connector, connection, stream, schema, and DLO metadata are packageable or must be recreated. | Connection readback, stream status, DLO row count. |
| DMOs, mappings, and relationships | Use data kits or supported metadata movement only; resolve target data-space names. | Mapping status, DMO primary key metadata, relationship readback. |
| Identity resolution | Treat rulesets and run state separately. | Ruleset metadata readback and run status/counts. |
| Calculated insights | Package metadata only when supported; run/publish in target. | Syntax check, run status, output CIO query. |
| Search indexes/retrievers | Packageability and index rebuild behavior are availability-sensitive. | Source DMO/UDMO, chunk/index DMO counts, retriever output. |
| Semantic models | Preserve metric definitions, grain, dimensions, and governed access. | Model readback, metric result, report/dashboard comparison. |
| Segments | Separate definition, count, publish, and membership proof. | Segment status, count, publish history. |
| Activations/data actions | Reauthorize destinations and avoid moving secrets. | Target readback, activation/data action status, delivery proof. |
| Governance policies | Policies depend on data spaces, tags, classifications, users, and custom permissions. | Policy readback and non-admin runtime test. |

## Environment Gates

1. Confirm source and target org aliases explicitly.
2. Confirm API version and Data 360 feature availability.
3. Confirm data spaces and naming drift.
4. Confirm connector credentials are reauthorized locally, not committed.
5. Confirm package/data kit membership is complete.
6. Deploy or recreate metadata in dependency order.
7. Run readback proof by returned ID, status, count, metadata, or query.
8. Run governed-user proof when access controls are in scope.
9. Record only distilled evidence in the proof ledger.

## Forbidden Assumptions

- Do not assume raw data is packaged with metadata.
- Do not assume a successful deploy proves processing jobs ran.
- Do not assume data kit coverage includes every Data 360 asset type.
- Do not move credentials, tokens, org metadata dumps, or customer data.
- Do not claim sandbox parity until target-org feature availability, data
  spaces, and limits are checked.
