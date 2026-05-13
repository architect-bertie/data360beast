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
  author: "architect-bertie"
---

# sf-datacloud-unstructured-retrieval

Use this skill for the **unstructured data and retrieval plane**.

Beast references:
- Beast preflight: [docs/beast-preflight.md](../../docs/beast-preflight.md)
- Phase proof matrix: [docs/phase-proof-matrix.json](../../docs/phase-proof-matrix.json)
- Public operating model: [docs/operating-model.md](../../docs/operating-model.md)
- RAG/search-index playbook: [docs/data360/rag-search-index-retriever-playbook.md](../../docs/data360/rag-search-index-retriever-playbook.md)
- Proof ledger: [docs/proof-ledger.md](../../docs/proof-ledger.md)
- Public LLM map: [docs/llms.txt](../../docs/llms.txt)
- Limits source precedence: [docs/data360/limits-source-precedence.md](../../docs/data360/limits-source-precedence.md)
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
- Agentforce grounding and behavior -> `sf-ai-agentforce` companion skill when available
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

## Doc-Synced Notes

<!-- SF_DOC_SYNC_START:search-index-and-retrievers -->
### Search Index + Retriever Setup (UI path)

_Auto-synced from the local sf-docs cached Salesforce Help export (official docs only).

**Sources (sf-docs cached Help):**
- sf.c360_a_search_index_ground_ai.htm (2026-05-11T18:38:46.532Z) — Use Search for AI, Automation, and Analytics
- data.c360_a_hybridsearch_index_create.htm (2026-05-11T18:38:47.245Z) — Create a Hybrid Search Index with Advanced Setup
- data.c360_a_ai_retriever_create.htm (2026-05-11T18:38:48.058Z) — Create an Individual Retriever

**Notes:**
- Hybrid search is intended to combine semantic (vector) and lexical (keyword) matching; choose it when vocabulary precision matters.
- Advanced Setup includes parser/preprocessing choices; some options are available only for certain file types and are mutually exclusive in specific combinations.
- Index configuration can include filter fields and ranking factors; retriever filters depend on filter fields being defined on the index.
- Creating an index can produce related objects (chunk/index DMOs); include them in governance and monitoring.
- Retriever configuration includes selecting the data space, DMO, index, optional filters, return fields, and (optional) citations; activate a version before use in prompts.
<!-- SF_DOC_SYNC_END:search-index-and-retrievers -->

<!-- SF_DOC_SYNC_START:process-content -->
### Process Content: Chunking, UDMO Mapping, Search Indexes, and Retrievers

_Distilled from official Salesforce sources only._

**Sources:**
- data.c360_a_search_index_grounding.htm — Chunk Data
- data.c360_a_search_index_supported_chunking_strategies.htm — Supported Chunking Strategies
- data.c360_a_unstructured_data_map_udlo.htm — Mapping UDLOs to UDMOs
- data.c360_a_search_index_easy_setup_search_index.htm — Easy Setup Search Index
- data.c360_a_hybridsearch_index_create.htm — Hybrid Search Index Advanced Setup
- data.c360_a_search_index_create_vector_index_config.htm — Vector Index Configuration
- data.c360_a_ai_retriever_create.htm — Create an Individual Retriever
- sf.c360_a_search_index_ground_ai.htm — Use Search for AI, Automation, and Analytics

**The unstructured pipeline (UDLO → UDMO → Index → Retriever):**

1. **UDLO (Unstructured Data Lake Object)** — landing container for
   ingested unstructured content from S3, Azure Blob, GCS, Box,
   SharePoint Unstructured, etc.
2. **UDMO (Unstructured Data Model Object)** — harmonized view of UDLO,
   represents the unstructured data model.
3. **Chunk DMO (CDMO)** — generated when a search index is created;
   stores chunked content + vector embeddings + source metadata.
4. **Index DMO** — stores index-level metadata for the search index.
5. **Retriever** — wraps Einstein Search operations for use in prompts,
   flows, and analytics.

**Supported file formats:** HTML, TXT, PDF.

**UDLO-to-UDMO mapping:**
- One UDLO maps to at most one UDMO; multiple UDLOs can map to one UDMO.
- Field-level mappings between UDLOs are auto-generated and read-only.
- UDMOs participate in identity resolution if linked to Individual or
  Party via mapped contact-point or party fields.

**Chunking strategies:**

| Strategy | How it works | Best for |
|---|---|---|
| Semantic-based passage extraction | Uses HTML tag boundaries (`<h1>`, `<h2>`, `<ul>`, `<b>`) as logical chunks | Web content, knowledge articles, structured HTML |
| Window-based passage extraction | Uses block-level tags (`<div>`, `<p>`) or line breaks; falls back to sentence-level if no HTML | Plain text, transcripts, mixed content |

After chunking, content is converted to **vector embeddings** —
numerical representations capturing semantic relationships between
words and phrases — and stored in the search index alongside source
metadata.

**Three search index types:**

| Type | Retrieval | Best for |
|---|---|---|
| Vector Search | Semantic similarity (embedding distance) | Long-form natural-language queries; "find similar concepts" |
| Hybrid Search | Vector + keyword (BM25-style) | Domain vocabulary, product codes, exact-term + semantic balance |
| Enriched Search | Vector + keyword + entity-extracted metadata | Heavy faceted retrieval, structured entity grounding |

**Easy Setup Search Index:**
- Single-screen creation: select source object → select content fields →
  Salesforce auto-chooses defaults (chunking, embedding, index type).
- Suitable for first-time setups and standard content.
- Defaults are conservative; use Advanced Setup for performance tuning.

**Advanced Setup (Hybrid or Vector Search Index):**
1. Search Indexes tab → New → Advanced Setup.
2. Choose Search Type: Vector or Hybrid.
3. Source Object: choose UDMO/DMO (e.g., Knowledge Article, Case).
4. Manage Fields: pick fields to index (Description, Subject, Body) and
   identifier/citation fields to surface to the retriever.
5. Configure parser/preprocessing: HTML stripping, language, file-type
   handling.
6. Configure chunking: strategy + max-chunk-size + overlap.
7. Configure embedding model and dimensionality (defaults usually fine).
8. Add filter fields (required for retriever pre-filtering).
9. Add ranking factors (recency, popularity, custom score).
10. Save and trigger indexing.

**Identifier fields are prepended to every chunk:**
For ADL-backed Knowledge Articles, identifying fields auto-prepend to
each chunk so retrieval surfaces context. Configure these explicitly
to control what the LLM sees.

**Individual Retriever creation:**
1. AI Models / Einstein Studio → Retrievers → New → Individual Retriever.
2. Select Data Space.
3. Select source DMO.
4. Select Search Index (must already exist).
5. Configure return fields:
   - Identifier fields (Subject, Title, ID for citations).
   - Chunk text field (primary content for the LLM).
   - Source URL field for citation links.
6. Optional: Add prefilters (AND-only or OR-only logic; equality,
   inequality, simple comparisons; up to no-code limits).
7. Optional: Configure ranking factors (recency, popularity, weighting).
8. Name (e.g., "Case Retriever"), Save, Activate.
9. Note API name for use in Prompt Builder.

**No-code retriever limits:**
- Max 50 results per call.
- Filter operators: equality, inequality, simple number comparisons.
- Filter logic: all-AND or all-OR (no nested logic).
- No post-retrieval filters.
- For nested filters, custom joins, post-filters, majority-vote
  classification, or record-access checks: use Apex `ConnectApi.CdpQuery`,
  Query SQL `vector_search()`, or `hybrid_search()` SQL functions.

**Use Search for AI, Automation, and Analytics (downstream consumers):**

| Surface | How search index is used |
|---|---|
| Agentforce | Retriever wired into prompt template grounding |
| Prompt Builder | Retriever resolution merges chunks into prompt context |
| Flow Builder | Retriever invocable action returns chunks to flow variables |
| Tableau | JDBC/Connect API access to chunk DMOs and index DMOs |
| Apex | `ConnectApi.CdpQuery.searchVector()` for custom UI |
| Direct SQL | `vector_search()` and `hybrid_search()` SQL functions |

**Grounding workflow:**
1. User question → Agentforce/Prompt Builder.
2. Retriever invoked with question (and any dynamic prefilters).
3. Top-k chunks returned (ranked by embedding similarity + ranking
   factors).
4. Chunks merged into prompt context with citations.
5. LLM generates answer constrained by retrieved content.
6. Citations rendered in response.

**Production checklist:**
- Source object has populated content fields and stable identifiers.
- Chunking strategy matches content shape (HTML → semantic; plain text → window).
- Filter fields exist on the index for governance prefilters.
- Identifier and source URL fields are populated for every record.
- Retriever activated and tested in Prompt Builder with `&c__debug=1`.
- Top-k retrieval validated against 10+ realistic prompts.
- Hybrid search has both semantic and keyword precision tests.
- Non-admin user profile sees expected results (governance proven).
- Reindex cadence aligned with source update frequency.
<!-- SF_DOC_SYNC_END:process-content -->

<!-- SF_DOC_SYNC_START:limits-unstructured-search -->
### Unstructured data and search index limit gate

_Auto-synced from the local sf-docs cached Salesforce Help export (official docs only).

**Sources (sf-docs cached Help):**
- data.c360_a_limits_and_guidelines.htm (2026-05-11T20:20:31.057Z) — Data 360 Limits and Guidelines

**Notes:**
- Treat the captured Limits and Guidelines page as a required source before making durable guidance for this phase.
- Separate soft guidelines from hard limits, and call out when a limit can require an Account Executive request or org-specific validation.
- Before recommending chunking, parser mode, ranking fields, index refresh, or retriever shape, check the unstructured-data and search-index limit family.
- Keep reindexing, embedding, query, storage, and intelligent-processing cost in the design review.
- Relevant limit families currently captured include: General Guidelines and Limits, Activation Guidelines and Limits, Calculated Insights Guidelines and Limits, Code Extension Guidelines and Limits (Beta), Data Actions Guidelines and Limits, Data Explorer Guidelines and Limits, Data Federation Guidelines and Limits, Data Graphs Guidelines and Limits, Data Ingestion Guidelines and Limits, Data Model Object Guidelines and Limits, Data Shares Guidelines and Limits, Data Transforms Guidelines and Limits.
<!-- SF_DOC_SYNC_END:limits-unstructured-search -->
