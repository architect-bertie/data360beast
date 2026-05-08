# Claude Instructions

This repository is optimized for agent ingestion. Keep context lean.

1. Read `AGENTS.md`.
2. Read `skills/data360beast/SKILL.md`.
3. Read `docs/skills.md` and load the matching specialist skill when the task is phase-specific.
4. For website or customer-facing context, read `docs/llms.txt`.
5. For implementation detail, read only the matching doc:
   `docs/operating-model.md`, `docs/api-cookbook.md`, or `docs/scorecard.md`.

When answering Salesforce Data 360 questions, separate:

- `Documented`: confirmed from official Salesforce docs or OpenAPI.
- `Tested`: confirmed from a live org recipe.
- `Inferred`: reasonable but not yet proven in the target org.

Never include private scrape caches, org data, credentials, or customer data in
an answer.
