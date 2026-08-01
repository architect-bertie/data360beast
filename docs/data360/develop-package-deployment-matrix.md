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
| Is the user deploying a data kit programmatically? | Connect REST with asynchronous job-status readback. |
| Is the user proving a full implementation path? | Beast Labs scenario, then promote distilled proof. |
| Is the user estimating cost or environment replay? | Cost and usage sizing contract. |

## Deployment Surfaces

| Surface | Package/Deploy Habit | Minimum Proof |
| --- | --- | --- |
| Data streams and DLO setup | Confirm whether connector, connection, stream, schema, and DLO metadata are packageable or must be recreated. | Connection readback, stream status, DLO row count. |
| DMOs, mappings, and relationships | Use data kits or supported metadata movement only; resolve target data-space names. | Mapping status, DMO primary key metadata, relationship readback. |
| Identity resolution | Treat rulesets and run state separately. | Ruleset metadata readback and run status/counts. |
| Calculated insights | Package metadata only when supported; run/publish in target. | Syntax check, run status, output CIO query. |
| Code Extension | Develop and validate scripts/functions in a Data 360 sandbox. Move deployments or batch transforms with a DevOps data kit; add referenced DLOs/DMOs when they are not included automatically. | Deployment status, batch-transform or chunking-function run state, output DLO/DMO or chunk readback, and `DataCustomCodeLogs__dll`. |
| Search indexes/retrievers | Packageability and index rebuild behavior are availability-sensitive. | Source DMO/UDMO, chunk/index DMO counts, retriever output. |
| Semantic models | Preserve metric definitions, grain, dimensions, and governed access. | Model readback, metric result, report/dashboard comparison. |
| Segments | Separate definition, count, publish, and membership proof. | Segment status, count, publish history. |
| Activations/data actions | Reauthorize destinations and avoid moving secrets. | Target readback, activation/data action status, delivery proof. |
| Governance policies | Policies depend on data spaces, tags, classifications, users, and custom permissions. | Policy readback and non-admin runtime test. |
| Data kit deployment | Prefer Connect REST asynchronous deployment for programmatic standard or DevOps data-kit deployment; treat the single-click flow path as legacy. | `202 Accepted`, returned job ID, terminal `Completed` or `Error` status, target data space, and component errors. |

## Environment Gates

1. Confirm source and target org aliases explicitly.
2. Confirm API version and Data 360 feature availability.
3. Confirm data spaces and naming drift.
4. Confirm the sandbox is provisioned and seed approved test data because Data
   360 sandbox provisioning copies metadata, not production Data 360 records.
5. Confirm connector credentials are reauthorized locally, not committed.
6. Confirm package/data kit membership is complete.
7. For Connect REST data-kit deployment, require `asyncMode=true`, the correct
   standard or DevOps request shape, and the target data-space name.
8. Deploy or recreate metadata in dependency order.
9. Poll asynchronous jobs to a terminal status and inspect component errors.
10. Run readback proof by returned ID, status, count, metadata, or query.
11. Run governed-user proof when access controls are in scope.
12. Record only distilled evidence in the proof ledger.

## Forbidden Assumptions

- Do not assume raw data is packaged with metadata.
- Do not assume a successful deploy proves processing jobs ran.
- Do not assume data kit coverage includes every Data 360 asset type.
- Do not move credentials, tokens, org metadata dumps, or customer data.
- Do not claim sandbox parity until target-org feature availability, data
  spaces, and limits are checked.
