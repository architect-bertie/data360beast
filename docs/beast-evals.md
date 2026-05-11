# Beast Evals

Use these lightweight checks when changing Data360 Beast skills or docs. They
are prompt-level evals, not live org tests, and should fail loudly when an agent
guesses endpoint paths, skips proof, or blurs documented and tested confidence.

## Scoring

Each eval is pass/fail. A change is promotion-ready when every applicable eval
passes and any skipped live validation is explicitly labeled.

| Eval | Prompt | Required Assertions | Fail Conditions |
| --- | --- | --- | --- |
| API payload discipline | "Create a Data 360 segment through the API." | Names API version/data space assumptions, uses OpenAPI or says schema is unverified, requires readback by segment ID and status. | Invents endpoint/body fields, treats create response as health proof. |
| Data space handling | "Run a Query SQL example in a non-default data space." | Calls out data-space parameter/token/ConnectApi overload handling and target-org metadata proof. | Relies on default data space silently. |
| Segment proof | "My query works but segment creation fails." | Separates query plane from segment compiler, checks DMO grain, relationships, Segment On key, status, and count. | Says query success proves segment safety. |
| RAG troubleshooting | "The agent answers without citations." | Checks source object, chunk/index DMO population, retriever output, return fields, prompt grounding, and access policy. | Starts by changing the LLM model or prompt only. |
| Governance proof | "Who can see this DMO field?" | Requires data space, permission set/object access, tags/classification/policy readback, and non-admin user test. | Uses System Admin visibility as runtime proof. |
| Activation proof | "Publish this audience to a destination." | Validates target first, then activation status, publish history, count, and delivery proof. | Assumes visible segment can be activated. |
| Formula syntax | "Add a formula field to a data stream." | Uses Data 360 formula library syntax and exact source field labels. | Uses Query SQL syntax as the formula language. |
| Confidence labeling | "Explain this architecture to a customer." | Separates documented, tested, and inferred parts with caveats and next proof step. | Presents inferred engine behavior as Salesforce contractual fact. |

## Release Gate

Before raising the Beast score, confirm the update adds at least one of:

- a current official docs source or OpenAPI-backed shape
- a reusable proof path with readback fields
- a live-tested recipe with caveats and failure modes
- a guardrail that prevents a known bad assumption
- a machine-readable routing or validation artifact
