---
name: sf-datacloud-ai-models
description: >
  Salesforce Data 360 AI Models, formerly Einstein Studio, including predictive
  models, bring-your-own models, foundation model configurations, retrievers,
  model outputs, transforms, SQL function usage, and governance. TRIGGER when:
  the user creates, configures, monitors, or deploys AI Models in Data 360.
license: MIT
metadata:
  version: "1.0.0"
  author: "architect-bertie"
---

# sf-datacloud-ai-models

Use this skill for the **AI Models / Einstein Studio plane**.

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

1. Classify the model type:
   - predictive model created in Data 360
   - connected model / BYOM
   - foundation model configuration
   - retriever-backed RAG use case
   - AI model invoked in a transform or SQL function
2. Define target, inputs, output DMO/field, refresh cadence, and downstream consumers.
3. Validate training data quality: null rates, leakage, label balance, date windows, unique categories, and input-variable limits.
4. Keep model inputs tied to governed DMOs or calculated insights.
5. Validate that model creators and consumers have access to every governed input object and field; save-time failures can differ from metadata visibility.
6. For generative model configs, set deterministic hyperparameters for production workflows and define masking/stop sequences.
7. For retrievers, use [sf-datacloud-unstructured-retrieval](../sf-datacloud-unstructured-retrieval/SKILL.md) for index and chunking quality.
8. For RAG generation, choose the LLM from context-window need and reasoning
   difficulty. Retrieval quality, prompt grounding, and model reasoning are
   separate gates.
9. Deploy model outputs into a DMO/calculated insight/transform output that downstream reports, segments, or agents can verify.
10. Monitor performance, drift, usage, and permissions after activation.

## Guardrails

- Do not use PII, protected attributes, or leakage fields without explicit approval and governance.
- Treat tags/classifications as model-card inputs: document sensitive, restricted, excluded, and masked fields.
- Do not put model scores into segmentation or automation until calibration and threshold validation are done.
- For input categories with high cardinality, group or encode deliberately.
- Document whether the model output is a score, class, forecast, sentiment, or generated text.
- Use lower temperature for operational outputs that must be repeatable.
- Do not upgrade the LLM as the first fix for bad RAG. First prove that relevant
  chunks exist, the retriever returns them, and the prompt resolution includes
  usable context.
- For RAG, context window sizing must include system/prompt instructions, user
  query, retrieved chunks, return fields, source metadata, and expected output.
- Stronger reasoning models help when the response must synthesize across
  multiple retrieved chunks, but they cannot recover missing or irrelevant
  retrieval context.
- Predictive AI work must include use case, training data prep, model quality, output consumption path, and monitoring.
- Model outputs should land in queryable DMOs, CIs, transforms, Flow actions, Apex, or REST paths that downstream consumers can validate.
- Retrievers are versioned, select a data space, DMO, and search index, and must be activated before use in prompt templates.
- Retriever calls follow Data 360 governance policies; test with the actual consuming user profile.

## Validation Gates

- Input feature list exists in the target data space.
- Model output is queryable and tied to the right profile/account/product key.
- Thresholds are tested against historical outcomes.
- Downstream flows/data actions/segments are tested with both positive and negative examples.
- A human-readable model card exists: purpose, data, features, output, limitations, owner, monitoring cadence.

## Handoffs

- Feature engineering -> [sf-datacloud-calculated-insights](../sf-datacloud-calculated-insights/SKILL.md)
- Search indexes/retrievers -> [sf-datacloud-unstructured-retrieval](../sf-datacloud-unstructured-retrieval/SKILL.md)
- Data actions / flows from model output -> [sf-datacloud-automation](../sf-datacloud-automation/SKILL.md)
- Semantic metric exposure -> [sf-datacloud-semantic-layer](../sf-datacloud-semantic-layer/SKILL.md)
- Governance and sensitive field policy -> [sf-datacloud-governance](../sf-datacloud-governance/SKILL.md)

## Output Format

Report:

1. model type
2. target/output
3. input features and data sources
4. training/scoring cadence
5. downstream consumers
6. governance and PII controls
7. validation evidence
8. monitoring plan

## Doc-Synced Notes

<!-- SF_DOC_SYNC_START:ai-models-predictive-byom -->
### Predictive AI and BYOM in Data 360

_Distilled from official Salesforce Help, Developer blogs, and product documentation._

**Sources:**
- data.c360_a_ai_use_ai_models.htm — Use AI Models in Data Cloud (section)
- data.c360_a_ai_predictive.htm — Einstein Predictive AI (26k chars)
- developer.salesforce.com/blogs/2024/07/how-to-build-a-predictive-ai-model-in-data-cloud
- developer.salesforce.com/blogs/2023/08/bring-your-own-ai-models-to-salesforce-with-einstein-studio
- developer.salesforce.com/blogs/2024/12/using-ai-model-output-in-data-cloud-with-prediction-jobs
- developer.salesforce.com/blogs/2024/08/how-to-use-data-cloud-ai-model-predictions-in-flow

**Built-in predictive models (Einstein Studio Model Builder):**
- Train a binary classification or regression model from a single DMO using a
  clicks-not-code approach.
- Prepare training data with Batch Data Transforms to create a denormalized DMO
  with the outcome (labeled) column.
- Model Builder auto-selects algorithm (XGBoost default); supports up to 50
  input variables.
- Minimum requirements: at least 400 rows total, 25 rows per outcome value.
- Uses 4-fold cross validation for metrics; threshold is user-adjustable.
- Model versions allow iterating on filter criteria, input features, and
  algorithms; prior versions are preserved.
- Activate a model before creating prediction jobs or using it in flows.

**Prediction Jobs (operationalization):**
- Inference Builder / Prediction Jobs write scores to an auto-created ML
  Prediction DMO connected to a base DMO via relationship.
- Batch mode: one-off predictions for segmentation, analytics, or back-testing.
- Streaming mode: rescores on record creation or update; triggers Data Actions
  or Data Cloud Triggered Flows based on prediction scores.
- Control which field updates trigger rescoring to avoid unnecessary processing.
- Streaming jobs can also run a batch pass to score all existing records.

**BYOM / Connected Models:**
- Connect externally-built models from Amazon SageMaker, Google Vertex AI, or
  Databricks through Einstein Studio.
- Zero-copy data federation eliminates ETL for BYOM scoring; supports real-time,
  streaming, or batch predictions.
- Connected models appear alongside built-in models in the Einstein Studio tab.

**Flow integration:**
- All active Einstein Studio models are available as Data Cloud Actions in any
  Flow type (record-triggered, screen, autolaunched).
- Map model inputs from any flow variable or prior step; inputs need not
  originate from Data Cloud.
- Use decision nodes on prediction scores to drive alerts, escalation, case
  creation, or personalization.

**Model output consumption paths:**
- Prediction DMO → segmentation criteria
- Prediction DMO → Batch Data Transform node → compare actual vs predicted
- Streaming prediction + Data Action → Data Cloud Triggered Flow
- Flow Action → real-time scoring at point of decision
- Prediction DMO → reports, dashboards, Tableau, CRM Analytics

**Explainability:**
- Predictions include top predictors (record-specific variables explaining the
  outcome) and recommendations (actionable steps if variables are marked
  actionable).

**Governance rules:**
- Do not put model scores into segmentation or automation without threshold
  validation and calibration.
- Model creators and consumers must have access to every governed input object
  and field; save-time failures can differ from metadata visibility.
- Training data leakage, PII fields, and protected attributes must be excluded
  unless explicitly approved.
- Document the model card: purpose, data, features, output, limitations, owner,
  monitoring cadence.
- Test governed behavior with a non-admin user when policies, masking, or data
  spaces affect model inputs or outputs.
<!-- SF_DOC_SYNC_END:ai-models-predictive-byom -->
