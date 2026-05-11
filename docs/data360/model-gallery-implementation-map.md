# Data 360 Model Gallery Implementation Map

Last reviewed: 2026-05-11

This map summarizes public Salesforce Data Model Gallery diagrams for Data 360
and turns them into implementation guidance for DMO mapping, identity,
relationships, calculated insights, data graphs, segmentation, activation, and
agentic metadata. It is not a replacement for the official diagrams or runtime
metadata. Use it as a routing and design aid, then validate exact object names,
fields, relationships, data space, and limits in the target org.

Primary sources:
- Salesforce Developer Data Model Gallery: https://developer.salesforce.com/docs/platform/data-models/guide/data-cloud-category.html
- Data 360 object model: https://developer.salesforce.com/docs/data/data-cloud-dev/guide/dc-object-model.html
- Data 360 standard DMO reference: https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-datamodelobjects.html
- DMO relationship behavior: https://help.salesforce.com/s/articleView?id=data.c360_a_data_model_object_relationships.htm&language=en_US&type=5

## Source Diagrams

| Diagram | Public URL | Primary implementation use |
| --- | --- | --- |
| Case | https://developer.salesforce.com/docs/platform/data-models/guide/case.html | Service support graph anchored on Case, Account Contact, Account, and Individual. |
| Data 360 Overview | https://developer.salesforce.com/docs/platform/data-models/guide/data-cloud-overview.html | Cross-cloud C360 backbone for party, engagement, consent, sales, service, commerce, loyalty, device, and product. |
| Email Engagement | https://developer.salesforce.com/docs/platform/data-models/guide/email-engagement.html | Email/journey event modeling, scoring, content, channel, and message lineage. |
| Engagement Overview | https://developer.salesforce.com/docs/platform/data-models/guide/engagement.html | General event-grain engagement architecture across web, order, cart, product, app, message, voice, and channel. |
| Financial Services Overview | https://developer.salesforce.com/docs/platform/data-models/guide/data-cloud-financial-services-overview.html | Financial account, party, household, applicant, balances, transactions, holdings, liabilities, and product. |
| Generative AI Audit and Feedback | https://developer.salesforce.com/docs/platform/data-models/guide/generative-ai-audit-feedback-dmos.html | AI request/response, generation, citations, feedback, content quality, and audit lineage. |
| Google Analytics | https://developer.salesforce.com/docs/platform/data-models/guide/data-cloud-google-analytics.html | Web/app behavior mapped to engagement actions, content, campaign, product, and personalization logs. |
| Healthcare Provider Relationship Management | https://developer.salesforce.com/docs/platform/data-models/guide/data-cloud-healthcare-provider-relationship-management.html | Provider, practitioner, facility, taxonomy, specialty, territory, NPI, credentials, visit, sample, and product graph. |
| Party Overview | https://developer.salesforce.com/docs/platform/data-models/guide/party-overview.html | Identity, account-contact, contact points, party relationships, devices, apps, person profile context, and unified links. |
| Privacy Overview | https://developer.salesforce.com/docs/platform/data-models/guide/privacy-overview.html | Consent graph across contact point, party, channel, purpose, legal basis, brand, status, and consent actions. |
| Product | https://developer.salesforce.com/docs/platform/data-models/guide/product.html | Product dimension, category, catalog, master/goods/bundle product, brand, channel, and product-to-transaction links. |
| Sales Order | https://developer.salesforce.com/docs/platform/data-models/guide/sales-order.html | Commerce transaction model: header, line, delivery, tax, price adjustment, payment, coupon, promotion, and revisions. |
| Student Financial Aid Inquiry | https://developer.salesforce.com/docs/platform/data-models/guide/data-360-student-financial-aid-inquiry.html | Learner-centered application, benefit, disbursement, hold, required document, standing, and cost summary model. |
| Vehicle Charger and Telematics | https://developer.salesforce.com/docs/platform/data-models/guide/data-cloud-vehicle-charger-telematics.html | Asset/product/location model for chargers plus charging sessions, telematics events, faults, warranty, and summaries. |

## Core Cross-Model Patterns

### 1. Party And Identity Are The Spine

Common hubs:
- `ssot__Individual__dlm`
- `UnifiedIndividual__dlm` or org-specific unified individual DMO
- `IndividualIdentityLink__dlm` or org-specific unified link DMO
- `ssot__Account__dlm`
- `ssot__AccountContact__dlm`
- `ssot__Party__dlm`
- `ssot__PartyIdentification__dlm`
- contact point DMOs such as email, phone, address, app, digital ID, and OTT

Implementation guidance:
- Treat `Individual`, `Account`, and `Account Contact` as different business
  grains, not interchangeable customer labels.
- Use `Account Contact` when the relationship between a person and an
  organization matters, such as buyer, employee, provider contact, case contact,
  or billing/shipping contact.
- Use unified DMOs for customer-level aggregation only after identity rules have
  been validated. Keep source `Individual` IDs for lineage and explainability.
- Map at least one usable contact point channel when unification, consent,
  segmentation, or activation is expected.

### 2. Contact Point And Consent Are Separate Graphs

Common hubs:
- `ssot__ContactPointEmail__dlm`
- `ssot__ContactPointPhone__dlm`
- `ssot__ContactPointAddress__dlm`
- `ssot__ContactPointApp__dlm`
- `ssot__ContactPointConsent__dlm`
- `ssot__PartyConsent__dlm`
- `ssot__CommunicationSubscriptionConsent__dlm`
- `ssot__EngagementChannelTypeConsent__dlm`
- `ssot__DataUsePurpose__dlm`
- `ssot__DataUseLegalBasis__dlm`
- `ssot__ConsentStatus__dlm`

Implementation guidance:
- Do not model consent as a boolean field on `Individual`. Consent is scoped by
  party, contact point, channel, purpose, brand, status, legal basis, and action.
- Activation eligibility should check the consent path needed for the exact
  destination and channel.
- Treat contact point identity links as operationally important. If a person is
  unified but contact points are not, activation and messaging can still fail or
  target the wrong channel.

### 3. Engagement Is Event-Grain

Common hubs:
- `ssot__EngagementAction__dlm`
- `ssot__ChannelEngagement__dlm`
- `ssot__EmailEngagement__dlm`
- `ssot__WebsiteEngagement__dlm`
- `ssot__WebSearchEngagement__dlm`
- `ssot__ProductBrowse__dlm`
- `ssot__ProductOrderEngagement__dlm`
- `ssot__ShoppingCartEngagement__dlm`
- `ssot__ShoppingCartProductEngagement__dlm`
- `ssot__DeviceApplicationEngagement__dlm`
- `ssot__Message__dlm`
- `ssot__VoiceCall__dlm`

Implementation guidance:
- Engagement DMOs require primary key and event datetime mapping. Without event
  time, downstream windows, recency, streaming logic, and rapid-publish behavior
  become unreliable.
- Keep event facts separate from dimensions such as campaign, journey, content,
  product, contact point, device, and channel.
- Use calculated or streaming insights for reusable rollups such as last
  engagement date, frequency, conversion rate, channel preference, and product
  affinity. Do not repeatedly rebuild those metrics inside every segment.

### 4. Commerce Separates Header, Line, Money, Delivery, And Change History

Common hubs:
- `ssot__SalesOrder__dlm`
- `ssot__SalesOrderProduct__dlm`
- `ssot__SalesOrderPaymentSummary__dlm`
- `ssot__PaymentMethod__dlm`
- `ssot__SalesOrderDeliveryGroup__dlm`
- `ssot__SalesOrderChangeLog__dlm`
- `ssot__SalesOrderPriceAdjustment__dlm`
- `ssot__SalesOrderProductPriceAdjustment__dlm`
- `ssot__SalesOrderProductTax__dlm`
- `ssot__Promotion__dlm`
- `ssot__Coupon__dlm`

Implementation guidance:
- Preserve order header grain and line-item grain. Customer revenue, order
  counts, and product affinity often need both.
- Keep tax, price adjustment, coupon, promotion, payment, and delivery group
  data as separate children when the business needs auditability or exact margin
  calculation.
- If the source has revisions, decide whether the current order and change
  order records both need to be represented.

### 5. Product Is A Shared Dimension, Not A Text Attribute

Common hubs:
- `ssot__Product__dlm`
- `ssot__MasterProduct__dlm`
- `ssot__GoodsProduct__dlm`
- `ssot__BundleProduct__dlm`
- `ssot__ProductCategory__dlm`
- `ssot__ProductCategoryProduct__dlm`
- `ssot__ProductCatalog__dlm`
- `ssot__Brand__dlm`
- `ssot__SalesChannel__dlm`

Implementation guidance:
- Do not flatten product category, brand, catalog, and master product into a
  single product text field when downstream analytics need hierarchy.
- Use product hierarchy to power calculated insights such as category revenue,
  affinity, browse-to-buy, churn risk, and recommendation context.
- Validate whether the org uses standard product DMOs or custom product-like
  DMOs before writing SQL or segment logic.

### 6. Service And Asset Models Connect People, Organizations, Products, And Things

Common hubs:
- `ssot__Case__dlm`
- `ssot__WorkOrder__dlm`
- `ssot__Asset__dlm`
- `ssot__Location__dlm`
- `ssot__Product__dlm`
- `ssot__Account__dlm`
- `ssot__AccountContact__dlm`

Implementation guidance:
- Service models often need both the affected thing and the human/business
  context. For a case, that can mean case, account, account contact, individual,
  product, asset, and location.
- For Data Graphs, keep the graph scoped around the service action: e.g. "case
  triage context" should include current case facts, related contact/account,
  key asset/product facts, and recent relevant events, not every service field.

### 7. Vertical Models Extend The Same Backbone

Financial services:
- Anchor on `Financial Account`, `Account`, `Party`, `Financial Account Party`,
  balances, transactions, fees, holdings, liabilities, household/group party,
  applicants, and applications.
- Implementation risk is confusing financial account ownership, applicant
  relationship, household membership, and account-contact roles.

Healthcare provider relationship management:
- Anchor on provider/practitioner/service organization/facility, account,
  account contact, party identifier, NPI, taxonomy, specialty, territory,
  service, product/sample, visit, credentials, and facility location.
- Implementation risk is flattening provider, facility, and practitioner into
  one provider row; the diagram models them as related but distinct grains.

Vehicle charger and telematics:
- Anchor on product definitions, physical asset/equipment, charger base,
  connector, location, account/contact, charging session, telematics event,
  fault/category/type/priority, warranty, access type, and performance summary.
- Implementation risk is treating high-volume telemetry events, sessions, and
  summaries as one table. They serve different workloads.

Student financial aid inquiry:
- Anchor on `Individual`, application, learner financial aid application,
  benefit assignment, benefit, benefit disbursement, disbursement period, hold,
  required document, financial aid standing, cost item, and cost summary.
- Implementation risk is losing the relationship between applicant, benefit
  decision, document blockers, disbursement timing, and cost summary.

Generative AI audit and feedback:
- Anchor on gateway request, gateway response, generation, app generation,
  object-record citation reference, content quality, feedback, feedback detail,
  content category, and request tags.
- Implementation risk is keeping raw prompt/response logs without linking them
  to citations, feedback, quality signals, app context, and governance.

## Anchor Selection Guide

Pick the anchor DMO before designing joins, insights, segments, or graphs.

| Business question | Likely anchor | Why |
| --- | --- | --- |
| Who is this customer across sources? | Unified Individual | Customer-level answer after identity resolution. |
| What did this source person do? | Individual | Source-level lineage and engagement facts. |
| Which organization is responsible? | Account | B2B, household, facility, provider org, seller, or billing context. |
| What is the person's role at the organization? | Account Contact | Person-account relationship grain. |
| Can we contact them on this channel? | Contact Point plus Consent | Activation must respect channel, purpose, brand, and status. |
| What happened in a journey or web/app session? | Engagement Action or Channel Engagement | Event-level behavior with channel/process context. |
| What was bought? | Sales Order and Sales Order Product | Header plus line-item transaction grain. |
| Which product/category drove behavior? | Product and Product Category | Shared product dimension. |
| What is the support problem? | Case | Service case grain with account/contact path. |
| What physical thing is involved? | Asset | Asset/product/location/warranty/telematics context. |
| What AI output was generated and why? | GenAI Generation | Audit, citation, response, feedback, and quality context. |

## Live Implementation Playbook

1. Identify the business outcome, not just the source table name.
2. Choose the model-gallery subject area that most closely matches the use case.
3. Choose the anchor DMO and the relationship path needed for the outcome.
4. Resolve exact runtime DMO and field API names in the target data space.
5. Map DLOs to standard DMOs when the business grain matches.
6. Create custom DMOs only when the standard DMO cannot represent the grain
   cleanly.
7. Decide cardinality before relationship creation. Cardinality has downstream
   segment and activation implications and cannot be changed after creation.
8. Verify standard relationship activation by confirming both relationship
   fields are mapped.
9. Run identity resolution and inspect unified profile/link quality before using
   unified DMOs for metrics or activation.
10. Create calculated or streaming insights for reusable measures. Keep metric
    grain, time window, and dimensions explicit.
11. Create Data Graphs for retrieval and Agentforce context, not as hidden
    activation logic.
12. Test the exact downstream surface: query, CI, segment, activation, data
    action, report, graph, retriever, or agent. Success in one surface is not
    proof for another.

## Agentic Metadata Rules

Every agent-facing object description should include:
- business purpose
- grain
- source system or source family
- owner
- refresh expectation
- join keys and relationship role
- governed/sensitive fields
- whether the object is safe for query, segment, activation, report, graph,
  retriever, or agent output

Every relationship description should include:
- parent/child role
- cardinality
- join key
- fanout risk
- whether it is identity-critical, segment-safe, activation-safe, or graph-only

Every metric description should include:
- formula
- grain
- dimensions
- time window
- null behavior
- validation source
- authoritative vs exploratory status

## Anti-Patterns To Catch Early

- Treating `Individual`, `Account`, `Account Contact`, `Party`, and `Unified
  Individual` as synonyms.
- Modeling contact consent as a single boolean field.
- Flattening product hierarchy into product name or SKU only.
- Joining order header to order line without handling fanout.
- Reusing query SQL proof as segment, activation, or analytics proof.
- Creating custom relationships without checking active relationship limits.
- Masking relationship keys, graph ID/value fields, CI dimensions, or activation
  identifiers before testing downstream behavior.
- Building Data Graphs with broad object dumps instead of task-specific fields.
- Using Data Graph signals for activation without materializing equivalent
  segment-safe DMO or CI criteria.
- Publishing agent metadata with labels but no grain, sensitivity, freshness, or
  relationship semantics.
