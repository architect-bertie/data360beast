# Tagging and Classification

_Distilled from official Salesforce sources only. Linked from
[../SKILL.md](../SKILL.md)._

<!-- SF_DOC_SYNC_START:tagging-and-classification -->

**Sources:**
- data.c360_a_using_tagging_and_classification_dg.htm — Data Tagging and Classification in Data 360
- developer.salesforce.com/docs/data/data-cloud-query-guide/references/dc-sql-reference/ai-classify.html — AI_CLASSIFY SQL function

**Hierarchy structure (parent-child taxonomy):**
- Tags organize in a multilevel parent-child structure.
- Example: parent "Personal Information" → children "Email Address",
  "Phone Number", "Postal Address".
- Assigning a child tag automatically applies the parent tag — policies
  attached to the parent inherit.
- Tags support one parent, multiple children; no deeper hierarchy.

**Standard sensitivity levels:**
- Public, Internal, Confidential, Restricted.

**Standard compliance categories:**
- PII (Personally Identifiable Information)
- HIPAA (Health)
- GDPR (EU privacy)
- PCI DSS (payment card)
- Plus custom categories for org-specific obligations.

**AI-driven "Suggest Tags":**
- LLM-based metadata analyzer reads object/field names and descriptions.
- Recommends relevant tags at scale.
- Uses metadata only — does NOT read customer data.
- Reduces manual tagging burden; steward must still review before applying.
- Available as the AI_CLASSIFY SQL function for batch classification jobs.

**Industry use cases:**
- Healthcare: HIPAA categorization on patient data.
- Retail: PII + region-specific data sensitivity.
- Finance: encrypted financial data classification.
- Communications: customer interaction sensitivity.

**Tag governance:**
- Tags used in policies become lifecycle dependencies — plan delete/edit
  governance carefully.
- Avoid periods in tag names.
- CI dimensions derived from formulas may not auto-inherit source tags;
  retag the CIO when needed.
- Tags propagate downstream from DLO → DLO → DMO via data streams,
  calculated insights, segments, and identity resolution.

<!-- SF_DOC_SYNC_END:tagging-and-classification -->
