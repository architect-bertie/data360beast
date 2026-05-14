# Data360 Beast Docs Watch Operating Model

This weekly automation keeps the Beast skill pack aligned with official
Salesforce documentation while preserving the repo's public boundary.

## Pipeline

1. Refresh all indexed Salesforce Help pages from `docs/data360/help/index.md`.
2. Refresh all indexed Salesforce Developer Guide pages from
   `docs/data360/developer/index.md`.
3. Export the local sf-docs cache.
4. Capture oversized Help placeholders with official Help prerendered HTML.
5. Rebuild the Connect API catalog from the local official Swagger file when it
   is present.
6. Audit indexed Help and Developer pages for missing, placeholder, or
   suspiciously small captures.
7. Refresh marker-delimited notes from the official-doc cache. Keep broad
   guidance in docs-side evidence artifacts such as `docs/proof-ledger.md`;
   keep `skills/data360beast/SKILL.md` as a lean router.
8. Validate generated JSON.
9. Run Beast boundary checks for Labs-style language and shim drift.
10. Run `python3 tools/validate_proof_compliance.py` to confirm every SKILL.md
    cites the four proof contracts (`docs/phase-proof-matrix.json`,
    `docs/beast-preflight.md`, `docs/proof-ledger.md`,
    `docs/data360/limits-source-precedence.md`), no banned phrases appear,
    `references/*.md` and `scripts/*.py` pointers resolve, and matrix
    `specialistSkill` entries match `manifest.json`.
11. Run `python3 tools/run_beast_evals.py`,
    `python3 tools/skill_install_smoke.py`,
    `python3 tools/release_readiness.py`, and
    `python3 tools/mcp_readiness.py --json` to validate eval fixtures,
    install layout, release hygiene, and local MCP posture.
12. Commit and push public-safe changes when the git diff is non-empty.

## Labs Promotion Pipeline

Golden scenarios, synthetic journeys, payload experiments, traces, failures,
and future cookbook candidates belong in
[`data360beast-labs`](https://github.com/architect-bertie/data360beast-labs).
The docs-watch job keeps this repo focused on the operating model:

```text
Labs evidence -> public-safe proof ledger entry -> operating-model update -> future cookbook pattern
```

Promotion into Beast is allowed only when evidence can be summarized without raw
customer data, credentials, org metadata dumps, private traces, or bulky payload
readbacks. Beast records the proof, caveat, confidence label, and Labs reference;
Labs keeps the scenario body.

## Oversized Help Pages

Some Help articles are too large for the standard sf-docs Aura extraction path.
When the export contains `Cannot populate due to large Document size`, run:

```bash
node tools/capture_help_prerendered.mjs --placeholders
```

The fallback fetches the same official Salesforce Help article using the
official prerendered HTML response and rewrites only the local raw/summary cache
entries for the oversized pages.

## Public Boundary

Do not commit raw Help or Developer article bodies, generated cache manifests,
generated OpenAPI catalogs, raw Labs payload dumps, org metadata, credentials,
or customer data unless the repository policy changes. The automation commits
small public-safe assets only: specialist skills, curated markdown, pipeline
scripts, proof ledger updates, and operating guidance.

## Skill Update Rule

Skill updates must remain marker-delimited and reproducible. The automation can
refresh `<!-- SF_DOC_SYNC_START:* -->` sections, but broader rewrites require an
explicit doc impact rationale in the report before committing.

## Terminology Guardrails

The job must report and fail before committing if tracked Beast files gain
Labs-style delivery language outside approved boundary/stub contexts:

- `golden path`
- `customer journey`
- `step-by-step`
- `build a complete`
- `solution accelerator`
- `raw payload`
- `raw readback`

The words `cookbook` and `recipe` are allowed only for compatibility stubs,
future-cookbook pipeline language, or explicit Labs boundary language. Prefer
`proof ledger`, `evidence`, `tested caveat`, and `promotion status` in this
repo.

## Structural Guardrails

The job must also report and fail when:

- legacy tool-specific root instruction shims appear in the public repo.
- root `llms.txt` and `docs/llms.txt` diverge without a documented reason.
- `docs/api-cookbook.md` grows beyond compatibility-stub purpose.
- `docs/phase-proof-matrix.json` drops below the 12 expected phases or gains
  customer-journey/golden-scenario sequencing.
- staged files include raw Labs artifacts, payload dumps, org metadata,
  credentials, generated caches, or customer data.
