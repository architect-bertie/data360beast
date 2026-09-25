# Data360 Beast Docs Watch Operating Model

This weekly automation keeps the Beast skill pack aligned with official
Salesforce documentation while preserving the repo's public boundary.

## Pipeline

1. Refresh indexed Salesforce Help pages and follow relevant official Data 360
   child links from the current Help seed to discover unindexed pages.
2. Refresh the Salesforce Developer Guide from its current sidebar so newly
   added official guide pages enter `docs/data360/developer/index.md`.
3. Export the local sf-docs cache.
4. Capture oversized Help placeholders with official Help prerendered HTML.
5. Rebuild the Connect API catalog from the local official Swagger file when it
   is present.
6. Reject Help shells, soft 404s, untitled pages, and suspiciously small
   captures, then audit every indexed Help and Developer page.
7. Refresh marker-delimited notes from the official-doc cache. Keep broad
   guidance in docs-side evidence artifacts such as `docs/proof-ledger.md`;
   keep `skills/data360beast/SKILL.md` as a lean router.
8. Check `forcedotcom/sf-skills` for drift in the approved Data 360 companion
   subset documented in `docs/data360/sf-skills-data360-companion.json`.
   Update the companion markdown/JSON only when upstream changes affect install,
   routing, command behavior, templates, readiness checks, or gotchas. Do not
   vendor upstream skill bodies into Beast.
9. Run
   `python3 skills/data360beast/scripts/install_sf_skills_data360_companion.py --dry-run`
   as the companion installer health check.
10. Validate generated JSON.
11. Run Beast boundary checks for Labs-style language, naming drift, and shim drift.
12. Run `python3 tools/validate_proof_compliance.py` to confirm every SKILL.md
    cites the four proof contracts (`docs/phase-proof-matrix.json`,
    `docs/beast-preflight.md`, `docs/proof-ledger.md`,
    `docs/data360/limits-source-precedence.md`), no banned phrases appear,
    `references/*.md` and `scripts/*.py` pointers resolve, and matrix
    `specialistSkill` entries match `manifest.json`.
13. Run `python3 tools/run_beast_evals.py`,
    `python3 tools/skill_install_smoke.py`,
    `python3 tools/release_readiness.py`, and
    `python3 tools/mcp_readiness.py --json` to validate eval fixtures,
    install layout, release hygiene, and local MCP posture.
14. Commit and push public-safe changes when the git diff is non-empty.

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

## Related Topic Discovery

Review date: 2026-09-25. Include adjacent official documentation when it
describes a direct Data 360 data, governance, query, or integration dependency.
Do not expand discovery to entire neighboring product documentation trees.

| Topic | Decision | Reason and source |
| --- | --- | --- |
| Tableau Semantics | Include | Semantic models operate on Data 360 data and governance. Follow `analytics.c360*` as well as `data.c360*` pages; the current introductory source is [About Tableau Semantics](https://help.salesforce.com/s/articleView?id=analytics.c360_a_sl_get_started.htm&language=en_US&type=5). The old `data.c360_a_sl.htm` seed returned NotFound during live extraction. |
| Agentforce session tracing | Include bounded source | [Session tracing](https://help.salesforce.com/s/articleView?id=ai.generative_ai_session_trace.htm&language=en_US&type=5) stores agent interaction data in Data 360 and informs ingestion, modeling, and analytics. General agent authoring remains outside this crawl. |
| Personalization profile context | Include bounded source | [Get Context](https://help.salesforce.com/s/articleView?id=mktg.persnl_agentforce_configure_get_context_action.htm&language=en_US&type=5) depends on Data 360 profile data graphs and identity roots. General campaign configuration remains outside this crawl. |
| Hosted Data 360 MCP | Include one reference | The [official server reference](https://developer.salesforce.com/docs/platform/hosted-mcp-servers/references/reference/data360-mcp.html) documents the Data 360 API access surface. Do not crawl unrelated hosted servers. |
| Data 360 terminology | Include | The [glossary](https://help.salesforce.com/s/articleView?id=sf.c360_a_glossary_guide.htm&language=en_US&type=5) connects concepts across the indexed phases. |
| Industry sales/service deployments | Defer | Product-specific configurations are not core Data 360 contracts. Add individual sources when an implementation requires their data kit, DMO, or ingestion dependency. |
| General blogs and workshops | Exclude from authoritative index | Use for discovery only; prefer the owning Help or Developer reference for current behavior. |

Help `--refresh` bypasses the sf-docs result cache. The depth-four boundary
still applies; this is bounded discovery, not a claim of exhaustive coverage
of every Salesforce article. Missing pages must not be reported as captured.

The September 25 source crawl captured 419 Help articles (56 absent from the
previous Help index) and inventoried 3,719 Developer pages: 992 content captures
and 2,727 catalog entries. Four previously indexed articles were still live but
not rediscovered: billing for ingestion, transforms, identity resolution, and
model monitoring. They are now explicit fallback seeds for the next run.
The old semantic-layer and credit-reduction IDs returned NotFound.

These counts describe temporary source captures, not an applied index refresh.
Publication stopped at companion drift because upstream commit
`0851d45f78fdfa511bda12446c8cbe7c83c0d352` removed seven approved Data 360
skills. The contract now retains these as retired entries and monitors the
two remaining active companions. The installer and validator use the same
active set. Do not treat future missing companion folders as no drift.

## Oversized Capture Handling

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

Use **Data 360** in Beast-facing docs, UI, manifests, and guidance. Upstream
Salesforce `sf-skills` folder names may remain unchanged only when they are
exact install paths, package metadata, or command-surface references.

## Structural Guardrails

The job must also report and fail when:

- legacy tool-specific root instruction shims appear in the public repo.
- root `llms.txt` and `docs/llms.txt` diverge without a documented reason.
- `docs/data360/sf-skills-data360-companion.json` and
  `docs/data360/sf-skills-data360-companion.md` disagree on the approved
  companion skills or observed upstream source.
- `docs/api-cookbook.md` grows beyond compatibility-stub purpose.
- `docs/phase-proof-matrix.json` drops below the 12 expected phases or gains
  customer-journey/golden-scenario sequencing.
- staged files include raw Labs artifacts, payload dumps, org metadata,
  credentials, generated caches, or customer data.
