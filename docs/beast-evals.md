# Beast Evals

Use these lightweight checks when changing Data360 Beast skills or docs. They
are prompt-level evals, not live org tests, and should fail loudly when an agent
guesses endpoint paths, skips proof, or blurs documented and tested confidence.

The machine-readable fixtures live in [`beast-evals.json`](beast-evals.json).
Run the deterministic harness with:

```bash
python3 tools/run_beast_evals.py
```

When an agent or CI job has generated answers, put one Markdown or text file per
eval ID in an answers directory and run:

```bash
python3 tools/run_beast_evals.py --answers-dir eval-answers
```

The runner checks required proof-habit terms, forbidden shortcuts, and
confidence labels. It does not call an LLM and does not replace human review.

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
| Databricks zero-copy networking | "Customer wants Data 360 zero copy to Databricks but cannot whitelist Data 360 IPs." | Separates query federation from file federation, distinguishes Private Connect for Data 360 from Salesforce Private Connect, maps allowlisting to Databricks and storage enforcement points, and labels AWS private-routing claims by source/proof level. | Treats all zero-copy modes the same, says allowlisting is only for setup, or promises Databricks-on-AWS PrivateLink without current docs or tenant proof. |
| Runtime target discovery | "Generate a Data360 Beast implementation plan for a lab org whose local Salesforce CLI default points at a different org." | Uses explicit target org, authenticated/spec API version, target data-space readback, sanitized discovery, and a capability matrix caveat. | Relies on the local default org, hard-codes v66, uses stale `--url --json` flags, or logs org identifiers as public-safe proof. |
| Calculated insight control reconciliation | "A calculated insight is ACTIVE and the last run says SUCCESS. Can I use it for activation?" | Requires CIO output, job status, data space, row/aggregate proof, and an independent control query. | Treats ACTIVE or last-run SUCCESS as output correctness proof. |
| Segment membership surface | "A segment shows 4,027 members but my membership DMO query returns zero rows." | Distinguishes latest and history membership DMOs, segment member count, publish status, and data-space scope. | Treats every membership table as equivalent or segment count alone as member proof. |
| Code Extension remote proof | "My Data 360 Code Extension script passes local run and deploy says success. Is the feature proven?" | Requires explicit org/data space, `DataCustomCode` readback, terminal batch-transform history, independently reconciled output, delayed logs, and product schedule readback. | Treats local or deploy success as remote output proof, an initially empty log query as final, or generic frequency metadata as schedule proof. |

## Release Gate

Before raising the Beast score, confirm the update adds at least one of:

- a current official docs source or OpenAPI-backed shape
- a reusable proof path with readback fields
- a proof ledger entry with caveats and failure modes
- a guardrail that prevents a known bad assumption
- a machine-readable routing or validation artifact

Release-ready changes should also pass:

```bash
python3 tools/validate_proof_compliance.py
python3 tools/skill_install_smoke.py
python3 tools/release_readiness.py
```
