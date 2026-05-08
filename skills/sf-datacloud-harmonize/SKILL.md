---
name: sf-datacloud-harmonize
description: >
  Salesforce Data 360 Harmonize phase for DMOs, mappings, identity resolution,
  profile resolution, and Data Graphs. TRIGGER when: the user works with DMOs,
  mappings, relationships, identity resolution, unified profiles, or data graphs.
license: MIT
metadata:
  version: "2.0.0"
  author: "Codex"
---

# sf-datacloud-harmonize

Use this skill for the **schema and unification plane**.

Beast references:
- Public operating model: [docs/operating-model.md](../../docs/operating-model.md)
- Public API cookbook: [docs/api-cookbook.md](../../docs/api-cookbook.md)
- Public LLM map: [docs/llms.txt](../../docs/llms.txt)
- For exact Salesforce behavior, fetch official Help/Developer docs on demand with `sf-docs`.
- For endpoint shape, use OpenAPI from the official spec or the user-supplied Swagger before writing payloads.

## Prefer these Connect API families

- `GET/POST/PATCH/DELETE /ssot/data-model-objects`
- `GET/POST/DELETE /ssot/data-model-object-mappings`
- `PATCH /ssot/data-model-object-mappings/.../field-mappings/...`
- `GET/POST /ssot/data-model-objects/:dataModelObjectName/relationships`
- `GET/POST/PATCH/DELETE /ssot/identity-resolutions`
- `POST /ssot/identity-resolutions/:identityResolution/actions/run-now`
- `GET/POST/DELETE /ssot/data-graphs`
- `GET /ssot/data-graphs/metadata`
- `GET /ssot/data-graphs/data/...`
- semantic layer and metadata quality handoff

## Rules

- Resolve runtime DMO/profile names through metadata before writing query or segment logic.
- Only mapped fields and objects with relationships can be used for segmentation and activation.
- Profile and Other DMOs require primary key mapping; Engagement DMOs require primary key and event datetime mapping.
- For party-area modeling, Party is the reference to `Individual.Id`; map at least one contact point channel for unification and activation.
- Prefer standard C360 DMOs and starter mappings when they match the business concept; customize only when the standard model cannot represent the domain cleanly.
- Model grain explicitly: profile, engagement, transaction, product, account, case, content, or support object.
- Define relationship cardinality before allowing calculated insights, segments, data graphs, or reports to join across objects.
- Relationship cardinality cannot be changed after creation. A bad cardinality choice becomes a downstream segment/activation problem.
- Standard relationships become active only when both participating fields are mapped.
- Treat identity resolution as asynchronous; verify resulting unified shapes after runs.
- For identity resolution, validate source counts, match/consolidation rate, over-grouping, under-grouping, outlier unified profiles, and contact point quality before trusting segments.
- Verify governance access to unified result and unified link DMOs before downstream reports, graphs, segments, or agents consume identity outputs.
- Use Data Graph for retrieval and enrichment, and only turn graph signals into activation criteria when those signals are represented in segment-safe schema.
- Data Graphs must have a primary DMO, live in a data space, and should include only fields needed for retrieval/agent context.
- Include calculated insights or streaming insights in a Data Graph only when they are based on a DMO also included in the graph.
- Data Graph users can need access to ID/value/fragment DMOs and graph inputs. Masking or deny FLS on graph fields can hide or break the graph.
- Keep Data Graph keys and relationship fields unmasked unless a governed replacement path is tested.
- The current project pattern is: graph context improves proposal quality, but activation rebuilds from DMO-safe criteria.
- Prepare descriptions and relationship semantics with [sf-datacloud-metadata-agentic](../sf-datacloud-metadata-agentic/SKILL.md) when Agentforce or AI Models will consume the metadata.

## Handoff

- For query validation -> [sf-datacloud-retrieve](../sf-datacloud-retrieve/SKILL.md)
- For CIs -> [sf-datacloud-calculated-insights](../sf-datacloud-calculated-insights/SKILL.md)
- For segments -> [sf-datacloud-segment](../sf-datacloud-segment/SKILL.md)
- For semantic models -> [sf-datacloud-semantic-layer](../sf-datacloud-semantic-layer/SKILL.md)
- For tags, masking, RLS, and graph access failures -> [sf-datacloud-governance](../sf-datacloud-governance/SKILL.md)
