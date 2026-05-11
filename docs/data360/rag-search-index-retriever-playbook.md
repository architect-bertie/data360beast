# Data 360 RAG Search Index And Retriever Playbook

This public-safe playbook distills a 45-page Salesforce public-facing PDF,
`Agentforce and RAG: Best Practices for Better Agents`, plus its architecture
diagrams. Treat it as an implementation aid, not as official Salesforce
documentation. Fetch current Help/Developer docs and validate in the target org
before making limit, availability, or production behavior claims.

## Mental Model

Data 360 RAG has two distinct loops:

1. Offline preparation: load content, chunk it, vectorize it, and store the
   vectors plus chunk metadata in search-index DMOs.
2. Online usage: receive a query, vectorize the query, retrieve matching chunks,
   hydrate the prompt with retrieved context, generate the answer, and return it
   through the consuming surface.

For Agentforce, the runtime path is:

```text
agent -> topic -> action -> prompt template -> retriever -> search index -> DMO/DLO or UDMO/UDLO
```

Flow and Apex can sit beside prompt templates when orchestration, access checks,
advanced filters, or custom SQL are required.

## ADL Or Manual Setup

Use Agentforce Data Libraries when the use case fits the opinionated fast path:
Salesforce Knowledge Articles and uploaded files, default assets, and standard
agent action behavior. ADL creates the data streams, objects, mappings, vector
store/search index, retriever, prompt template, and agent action with defaults.

Use manual setup when the source is not covered by ADL or when the design needs
control over source DMO/UDMO, chunking, search type, embedding model, prefilters,
return fields, prompt structure, or agent action boundaries.

ADL file path patterns to remember:

- Files land through `FileUDMO__dlm` metadata, not as raw files in the object.
- ADL file content shares an org-level search index named `FileUDMO_SI`.
- The index DMO is `FileUDMO_SI_index__dlm`.
- `GroundingSourceId__c` identifies the ADL grounding source.
- `AiGroundingFileRefCustom__dlm` maps uploaded files to the grounding source.
- Default file-index behavior is hybrid search, `512` token chunks, E5 Large
  Multilingual embeddings, and advanced retrieval mode off.

ADL Knowledge Article path patterns:

- Knowledge indexing is based on `KnowledgeArticleVersion__dlm`.
- Search index names are prefixed with `KA_`.
- Identifying fields are prepended to every chunk.
- Content fields are chunked and vectorized after prepending.
- ADL settings become retriever query-template filters and return-field choices.

A search index maps to one source object path. For multiple source classes, use
separate indexes/retrievers unless the source content is intentionally mapped
into one shared DMO/UDMO with one governance and retrieval design.

## Content Curation Rules

Shape source content before tuning the index. Good retrieval starts upstream.

- Put structured records into DMOs and only chunk long-form, sentence-level text.
- Use UDMO/UDLO paths for documents, transcribed media, and long-form files.
- Do not treat CSV, JSON, or XML as unstructured just because it is in a file.
  Load it structurally first, then chunk only meaningful long text.
- Write detailed explanations, concrete examples, and focused documents that
  align with likely user questions.
- Use titles, headings, subheadings, and HTML heading hierarchy where possible.
- Spread Knowledge Article content across meaningful fields such as question,
  description, resolution, exceptions, and summary.
- Annotate images and video with alt text or descriptions because media itself
  is not chunked or vectorized.
- Convert complex tables to explicit JSON or HTML; split long tables and repeat
  headers so chunk boundaries keep context.
- Govern freshness. RAG over stale content creates polished stale answers.

## Field Roles

Every field in a RAG design should have a job:

- Index fields: long text that is chunked and vectorized for semantic matching.
- Prepend fields: short context copied into each chunk, such as title, product,
  language, article type, or summary.
- Filter fields: indexed metadata used by retriever prefilters, such as locale,
  product, entitlement, publication status, data source, account, region, or
  record ID.
- Return fields: chunk, source ID, title, URL, article number, related DMO
  fields, or other values the prompt/action needs after retrieval.
- Ranking fields: recency and popularity signals only when they represent real
  business relevance.

Index as few fields as possible. If title, summary, and description repeat the
same concept, chunk the detailed field and prepend the compact field. Too many
similar index fields can cause the top-k to be filled by duplicate chunks from
the same source record, reducing recall across documents.

Never chunk category-only fields, booleans, IDs, or picklist labels by
themselves. Use them as prepend fields, filter fields, or return fields.

## Chunking Strategy

Chunking is a tradeoff between retrieval precision and answer sufficiency.

- Smaller focused chunks improve matching when each chunk is a clean factoid.
- Larger chunks help the LLM answer when the answer needs surrounding procedure,
  constraints, or context.
- UDMO-based indexes usually rely more on chunk size because fewer structured
  metadata fields are available for augmentation.
- DMO-based indexes can compensate with prepend fields, return fields, related
  DMO fields, or, in pro-code paths, original-record augmentation.
- Keep `512` tokens as the conservative ceiling unless tests show a different
  size performs better for the source content.

Field prepending is available for DMO-based indexes. Use it to carry the title,
product, source, language, or article context into every chunk. It is especially
useful when the chunk body starts mid-procedure or assumes the reader has seen a
heading.

Chunk enrichment is a roadmap/availability-sensitive design knob. When
available, question-style enrichment can improve Q&A recall by embedding
generated questions while augmenting with the corresponding plain chunk.
Metadata-style enrichment can add generated keywords, entities, topics, title,
summary, and sentiment. Expect better retrieval for hard content, but higher
index size, cost, and latency.

## Hybrid Search Or Vector Search

Use vector search when the query and content are mostly natural-language
semantic matches.

Use hybrid search when exact words also matter: product names, model numbers,
SKUs, legal terms, abbreviations, brand terminology, domain jargon, or support
phrases. Hybrid search combines vector and keyword rankings and reranks the
result set.

Do not use hybrid search as a category lookup engine. Category-only chunks have
too little semantic context and can distort vector ranking. If a category is
important, make it a filter or prepend field.

Hybrid search can improve quality but increases latency and Data 360 credit
consumption because both vector and keyword indexes participate. Make hybrid a
measured choice, not a reflex.

## Retriever Design

Retrievers bridge search indexes and prompt templates. Design them as explicit
contracts:

- Search string source: user question, transformed query, case/email/conversation
  summary, or flow variable.
- Result count: enough recall for the prompt, but small enough for context
  window, latency, and Einstein Request cost.
- Return fields: only the fields the prompt/action can use.
- Prefilters: language, product, publication status, entitlement, geography,
  account, record ID, or other hard constraints.
- Dynamic prefilters: placeholders mapped at runtime from prompt inputs or Flow
  variables, such as `Account_ID = $placeholder`.
- Versioning: activate and test the intended retriever version before wiring it
  into Prompt Builder, Flow, or Agentforce.

Prefilters are stronger than post-filters when the goal is guaranteed
constrained retrieval because the top-k is selected inside the filtered set.
Post-filters can be useful but require Apex/SQL/Flow orchestration because
no-code retrievers do not support them directly.

No-code retriever limitations to watch:

- Maximum 50 results.
- Text filters are equality or inequality.
- Number filters are equality, greater-than, or less-than.
- Filter logic is all-AND or all-OR, with no nesting.
- No post-retrieval filters.

Use pro-code retrieval with Apex `ConnectApi.CdpQuery`, Query SQL,
`vector_search`, or `hybrid_search` when you need nested filters, unsupported
operators, post-filters, access checks, majority-vote classification, or custom
join logic.

## Multi-Source Agent Architecture

There are two main patterns for multiple retrieval sources.

One prompt/action with multiple retrievers:

- Use when most questions need most sources.
- All retrievers run when the action is called.
- Watch prompt bloat, context-window failures, latency, and cost.

Separate prompt/action per source:

- Use when the agent can reliably classify which source is needed.
- Put precise scope in topic and action descriptions.
- Do not rely on the reasoning engine to always chain many separate RAG actions
  for one answer. If all sources are mandatory, group them.

Hybrid grouping is often best: group sources that are usually needed together,
and separate sources with distinct scope.

## Prompt And Answer Contract

The prompt should tell the LLM how to use retrieved context, not merely append
context after a question.

Use instructions that require the model to:

- Analyze the question.
- Inspect retrieved knowledge.
- Decide whether the retrieved context is sufficient.
- Answer only from retrieved context.
- Return a known fallback when the answer is not present.
- Preserve source IDs, article IDs, or source references when available.
- Keep the answer concise and in the requested language.
- Check that the entities in the question are represented in the context.
- Distinguish facts from assumptions when the use case needs it.

For debugging, use Prompt Builder resolution-only mode when available by adding
`&c__debug=1` to inspect retriever output without paying for unnecessary answer
generation.

## Flow And Apex Patterns

Use Flow as the orchestrator when RAG is a pipeline rather than a single prompt:

- detect language before retrieval;
- transform a case, email, or conversation into a cleaner retrieval query;
- call a retriever with dynamic prefilters;
- post-process retriever JSON into Flow-supported types with Apex;
- call one or more prompt templates after retrieval;
- perform access checks or business-rule filters before generation.

Use Apex when the retrieval query itself must be custom SQL, when the user
needs record-access verification before augmentation, or when retriever output
must be reshaped for downstream Flow or prompt usage.

## Record-Scoped RAG

For "search within this record's documents" use cases:

1. Ingest the relevant record, file link, and file version objects.
2. Map them to the required SSOT DMOs and relationships.
3. Create the search index on the source DMO and include attachments where the
   setup supports it.
4. Add a filter field for the record key.
5. Create a custom retriever with a dynamic prefilter for the record key.
6. Map the placeholder from the prompt template or Flow input.
7. Test with two records that have overlapping document language to prove the
   filter is doing real isolation.

## LLM And Embedding Choice

For embeddings:

- E5-Large V2 is the conservative default for English-only content.
- Multilingual E5-Large is preferred for multilingual content and can preserve
  semantic similarity across languages.
- Low-resource languages need direct evaluation because embedding quality can
  vary by training coverage.
- Availability of OpenAI Ada 002 and enriched chunking behavior should be
  verified in current docs and the target org.

For generation:

- Context window must fit instructions, retrieved chunks, return fields, user
  query, and response format.
- Reasoning capability matters when the answer requires synthesis across
  multiple retrieved chunks.
- Retrieval quality and LLM reasoning are separate. Do not upgrade the LLM to
  compensate for missing or irrelevant chunks until retrieval is tested.

## Debug Chain

When a RAG answer fails, move layer by layer:

1. Agent layer: did the right topic and action run?
2. ADL layer, when used: did the correct grounding source/retriever get passed?
3. Search index layer: does the index DMO contain vectors and expected records?
4. Retriever layer: does the right version return the expected fields?
5. Prompt layer: does prompt resolution include usable retrieved content?
6. Generation layer: does the model obey grounding and fallback instructions?

Useful index checks:

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

## Evaluation Signals

Use the three-metric diagnosis:

- Context relevance: are the retrieved chunks relevant to the query?
- Faithfulness: is the answer grounded in the retrieved chunks?
- Answer relevance: does the answer satisfy the user question?

Interpretation:

- High faithfulness and low context relevance usually means retrieval/indexing
  is the problem.
- Low faithfulness and high context relevance usually means prompt or generation
  is the problem.
- High faithfulness and high context relevance with low answer relevance often
  means recall is incomplete or the prompt did not synthesize enough context.

## Implementation Checklist

Before production, verify:

- Source content is curated, current, and governed.
- DMO versus UDMO path is deliberate.
- Index fields are meaningful long text.
- Metadata is assigned as prepend, filter, return, or ranking fields.
- Hybrid search has a reason and a cost/latency test.
- Chunk size is tested with representative questions.
- Dynamic prefilters isolate record, language, product, entitlement, and data
  space where required.
- Retriever output has source metadata for citations or traceability.
- Prompt fallback behavior works when no relevant content exists.
- Actual non-admin agent/user profiles see only intended content.
- Query Editor or Data Explorer proves index and chunk population.
- Prompt resolution proves the retriever hydrates the prompt.
- Context relevance, faithfulness, and answer relevance are tracked during
  tuning.
