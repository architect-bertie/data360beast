---
name: sf-datacloud-unstructured-retrieval
description: >
  Salesforce Data 360 unstructured data, UDLO/UDMO setup, search indexes,
  chunking strategy, hybrid/vector search, retrievers, citations, and RAG
  grounding. TRIGGER when: the user ingests files or web content, configures
  unstructured data, designs chunking, creates search indexes, tunes hybrid
  search, or builds retrievers for Agentforce/Einstein grounding.
license: MIT
metadata:
  version: "1.0.0"
  author: "Codex"
---

# sf-datacloud-unstructured-retrieval

Use this skill for the **unstructured data and retrieval plane**.

Beast references:
- Public operating model: [docs/operating-model.md](../../docs/operating-model.md)
- Public API cookbook: [docs/api-cookbook.md](../../docs/api-cookbook.md)
- Public LLM map: [docs/llms.txt](../../docs/llms.txt)
- For exact Salesforce behavior, fetch official Help/Developer docs on demand with `sf-docs`.
- For endpoint shape, use OpenAPI from the official spec or the user-supplied Swagger before writing payloads.

## Production Workflow

1. Define the retrieval use case before selecting chunking.
2. Confirm supported file formats and connector mode: ingested vs referenced.
3. Create or verify the UDLO and mapped UDMO in the correct data space.
4. Choose search type:
   - vector for semantic similarity
   - hybrid when exact terms, IDs, SKUs, legal phrases, or product names matter
   - Easy Setup creates hybrid search with passage extraction and E5-Large V2 defaults.
5. Select chunk fields that carry semantic meaning: title, heading, body, transcript, summary, description.
6. Avoid chunking low-meaning fields like status, category-only fields, booleans, or IDs; use them as filters instead.
7. Pick chunking:
   - section-aware for HTML/PDF/Markdown/Word with meaningful headings
   - semantic passage extraction for HTML/text where DOM structure matters
   - conversation chunking for call transcripts, chats, and speaker-separated media
   - prepend-field chunking when title/product/category context must travel with every chunk
8. Keep default max token `512` unless tests show truncation or poor retrieval. Increase for long procedures; decrease for FAQ-style snippets.
9. Add pre-filter fields for governance, locale, product, audience, entitlement, publication status, and freshness.
10. Add ranking factors only when they represent real relevance: popularity, recency, helpfulness, conversion, quality score.
11. Create or tune the retriever in Einstein Studio and version it. Only one retriever version is active at a time.
12. Test retrieval with representative questions, inspect citations, then wire the retriever into prompt templates or Agentforce.

## Beast Rules

- Advanced setup controls parser/preprocessing, chunking, vectorization, filter fields, and ranking factors.
- Search index creation produces chunk and index DMOs; include those in governance and monitoring.
- A UDLO maps to at most one UDMO, while multiple UDLOs can map to one UDMO. UDLO-to-UDMO field mappings are read-only.
- Retriever filters are available only when the selected search index has filter fields defined.
- Retriever citations must use populated source URL/heading fields that end users can access.

## Quality Gates

- Data governance and record access have been tested with the actual agent/user profile.
- Search index status is healthy and incremental reindex behavior is understood.
- Chunks include citations and source metadata.
- Top-k retrieval returns relevant chunks for at least 10 realistic prompts.
- Hybrid search has both semantic and keyword precision tests.
- Consumption impact is understood: ingestion, storage, processing, query, and intelligent processing can all bill.

## Anti-Patterns

- Chunking entire records when only a few fields contain useful text.
- Using vector-only retrieval for exact product codes or compliance text.
- Creating one giant global index for content with different access rules.
- Forgetting that reindexing DMO attachments can reprocess all attachments for a changed DMO.
- Using retriever results in an agent without citation and permission checks.
- Building a search index when the creator or consumer lacks access to every required relationship-path DMO, search DMO, index DMO, chunk DMO, and attachment DMO.
- Using one index for content that needs materially different governance policies.

## Handoffs

- Data streams and transforms -> [sf-datacloud-prepare](../sf-datacloud-prepare/SKILL.md)
- Data modeling and UDMO relationships -> [sf-datacloud-harmonize](../sf-datacloud-harmonize/SKILL.md)
- AI model or retriever usage in Einstein Studio -> [sf-datacloud-ai-models](../sf-datacloud-ai-models/SKILL.md)
- Agentforce grounding and behavior -> [sf-ai-agentforce](../sf-ai-agentforce/SKILL.md)
- Governance and access policy behavior -> [sf-datacloud-governance](../sf-datacloud-governance/SKILL.md)

## Output Format

Report:

1. content source and connector mode
2. UDLO/UDMO/data space
3. index type and chunking strategy
4. selected chunk, filter, and ranking fields
5. retriever/version plan
6. test prompts and pass/fail retrieval evidence
7. cost, governance, and reindexing risks
