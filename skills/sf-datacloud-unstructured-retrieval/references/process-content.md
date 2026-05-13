# Process Content: Chunking, UDMO Mapping, Search Indexes, and Retrievers

_Distilled from official Salesforce sources only. Linked from
[../SKILL.md](../SKILL.md)._

<!-- SF_DOC_SYNC_START:process-content -->

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
