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
7. Refresh marker-delimited skill notes from the official-doc cache.
8. Validate generated JSON.
9. Commit and push public-safe changes when the git diff is non-empty.

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
or generated OpenAPI catalogs unless the repository policy changes. The
automation commits small public-safe assets only: skills, curated markdown,
pipeline scripts, and operating guidance.

## Skill Update Rule

Skill updates must remain marker-delimited and reproducible. The automation can
refresh `<!-- SF_DOC_SYNC_START:* -->` sections, but broader rewrites require an
explicit doc impact rationale in the report before committing.
