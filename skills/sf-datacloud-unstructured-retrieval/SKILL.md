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
- RAG/search-index playbook: [docs/data360/rag-search-index-retriever-playbook.md](../../docs/data360/rag-search-index-retriever-playbook.md)
- Public API cookbook: [docs/api-cookbook.md](../../docs/api-cookbook.md)
- Public LLM map: [docs/llms.txt](../../docs/llms.txt)
- For exact Salesforce behavior, fetch official Help/Developer docs on demand with `sf-docs`.
- For endpoint shape, use OpenAPI from the official spec or the user-supplied Swagger before writing payloads.

## Production Workflow

1. Start from the RAG runtime path:
   `agent/topic/action -> prompt/flow/apex -> retriever -> search index -> DMO/DLO or UDMO/UDLO`.
2. Choose the setup path:
   - Agentforce Data Library (ADL) when uploaded files or Salesforce Knowledge
     Articles fit the standard fast path.
   - Manual setup when sources, chunking, embeddings, filters, return fields,
     prompt design, or access checks need control.
3. Curate the source content before index work: focused documents, explicit Q&A
   structure, detailed examples, useful titles/headings, media descriptions,
   split/structured tables, and current governed content.
4. Confirm content shape:
   - structured records go to DMOs, and only long-form sentence-level text is
     chunked;
   - documents, transcripts, and files use UDLO/UDMO or ADL file paths;
   - CSV/JSON/XML should be loaded structurally first, not treated as raw
     unstructured content.
5. Select field roles deliberately:
   - index fields: long free text for chunking/vectorization;
   - prepend fields: title, product, source, language, summary, or article type;
   - filter fields: locale, product, entitlement, publication status, data
     source, account/record ID, region, or access cohort;
   - return fields: chunk, source ID, title, URL, article number, and related
     DMO fields needed by the prompt;
   - ranking fields: recency/popularity only when they represent relevance.
6. Index as few fields as possible. If multiple fields repeat the same concept,
   chunk the most detailed field and prepend the compact field.
7. Avoid chunking low-meaning fields like status, category-only fields,
   booleans, numbers, or IDs. Use them as filters, prepend fields, return
   fields, or ranking signals.
8. Choose search type:
   - vector when semantic natural-language similarity is enough;
   - hybrid when exact terms, IDs, SKUs, legal phrases, product names, acronyms,
     or domain jargon matter.
9. Treat hybrid search as a cost/latency tradeoff. Do not use it as a category
   lookup engine; category-only chunks distort semantic ranking.
10. Tune chunking against the use case:
    - smaller chunks for focused retrieval;
    - larger chunks when generation needs surrounding procedure or context;
    - `512` tokens is the conservative ceiling until test evidence says
      otherwise;
    - DMO indexes can use prepend/return fields to reduce chunk bloat;
    - UDMO indexes often rely more heavily on chunk size.
11. Create or tune the retriever in Einstein Studio:
    - set result count, return fields, prefilters, and dynamic prefilters;
    - map dynamic placeholders from prompt inputs or Flow variables;
    - activate and test the intended retriever version before wiring it into
      Prompt Builder, Flow, Apex, or Agentforce.
12. Design the prompt/action scope:
    - one prompt/action with multiple retrievers when most questions need most
      sources;
    - separate prompt/action per source when the agent can reliably choose the
      source;
    - precise topic/action descriptions to avoid out-of-scope RAG calls.
13. Test retrieval with representative questions, inspect prompt resolution,
    verify source metadata/citations, then validate with the actual agent/user
    profile.

## ADL And Manual Defaults

- ADL file content uses `FileUDMO__dlm` metadata, an org-level `FileUDMO_SI`
  search index, and `FileUDMO_SI_index__dlm` vectors.
- `GroundingSourceId__c` identifies the ADL grounding source, and
  `AiGroundingFileRefCustom__dlm` maps files to grounding sources.
- ADL file defaults include hybrid search, `512` token chunks, E5 Large
  Multilingual embeddings, and advanced retrieval mode off. Verify current
  availability before making production claims.
- ADL Knowledge Article indexes are based on `KnowledgeArticleVersion__dlm`;
  index names are prefixed with `KA_`.
- ADL Knowledge Article identifying fields are prepended to every chunk, while
  content fields are chunked and vectorized.
- A search index maps to one source object path. Use separate indexes and
  retrievers for distinct source classes unless the content is intentionally
  mapped into one shared DMO/UDMO with one governance design.

## Beast Rules

- Advanced setup controls parser/preprocessing, chunking, vectorization, filter fields, and ranking factors.
- Search index creation produces chunk and index DMOs; include those in governance and monitoring.
- A UDLO maps to at most one UDMO, while multiple UDLOs can map to one UDMO. UDLO-to-UDMO field mappings are read-only.
- Retriever filters are available only when the selected search index has filter fields defined.
- Retriever citations must use populated source URL/heading fields that end users can access.
- No-code retrievers are bounded: maximum 50 results, simple equality/inequality
  text filters, simple number comparisons, all-AND or all-OR filter logic, and
  no post-retrieval filters.
- Use Apex `ConnectApi.CdpQuery`, Query SQL, `vector_search`, or
  `hybrid_search` when you need nested filters, unsupported operators,
  post-filters, majority-vote classification, custom joins, or record-access
  checks before prompt augmentation.
- Prompt instructions must explicitly require context-only answering, sufficiency
  checks, fallback behavior when content is missing, source ID preservation, and
  entity checks.
- Retrieval quality and LLM generation quality are separate. Fix missing,
  duplicated, or irrelevant chunks before assuming a bigger model solves the
  problem.

## Quality Gates

- Data governance and record access have been tested with the actual agent/user profile.
- Search index status is healthy and incremental reindex behavior is understood.
- Chunks include citations and source metadata.
- Top-k retrieval returns relevant chunks for at least 10 realistic prompts.
- Hybrid search has both semantic and keyword precision tests.
- Prompt Builder resolution proves the retriever hydrates the prompt with the
  expected fields. When available, use resolution-only mode with `&c__debug=1`.
- Index and chunk DMOs have been probed in Query Editor or Data Explorer.
- Dynamic prefilters have been tested with two records or cohorts that share
  similar content to prove isolation.
- Evaluation separates context relevance, faithfulness, and answer relevance.
- Consumption impact is understood: ingestion, storage, processing, query, and intelligent processing can all bill.

## Anti-Patterns

- Chunking entire records when only a few fields contain useful text.
- Using vector-only retrieval for exact product codes or compliance text.
- Creating one giant global index for content with different access rules.
- Creating many similar index fields that cause top-k duplicate chunks from the
  same source record and reduce document recall.
- Chunking categories or picklist labels as if the search index were a keyword
  search engine.
- Calling every retriever for every agent question when the sources are not all
  relevant, bloating prompt resolution and cost.
- Splitting mandatory sources into separate actions and trusting the reasoning
  engine to always chain all of them.
- Upgrading the LLM before proving the retrieved chunks are present, relevant,
  and hydrated into the prompt.
- Forgetting that reindexing DMO attachments can reprocess all attachments for a changed DMO.
- Using retriever results in an agent without citation and permission checks.
- Building a search index when the creator or consumer lacks access to every required relationship-path DMO, search DMO, index DMO, chunk DMO, and attachment DMO.
- Using one index for content that needs materially different governance policies.

## Troubleshooting Chain

1. Agent layer: did the expected topic and action run?
2. ADL layer, when used: did the expected grounding source/retriever get passed?
3. Search index layer: does the index DMO contain vectors and expected source
   records?
4. Retriever layer: is the correct version active, with the expected return
   fields and filters?
5. Prompt layer: does prompt resolution include usable retrieved content?
6. Generation layer: does the LLM follow grounding and fallback instructions?

Use Query Editor probes:

```sql
SELECT * FROM <index_dmo> LIMIT 10
```

```sql
SELECT 'INDEX' AS location, COUNT(DISTINCT SourceRecordId__c) AS source_count
FROM <chunk_dmo>
UNION
SELECT 'DMO' AS location, COUNT(DISTINCT <id_field>) AS source_count
FROM <source_dmo>
ORDER BY location
```

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
