# Data 360 Documentation Delta Review

Reviewed: 2026-09-25
Baseline: `bcbf1693d8f95e6f5a2a0acf40b706c86679457f`
Current inventory: 4186 official pages (467 Help; 3,719 Developer).

- Added: 224 pages (100 Help, 124 Developer).
- Changed content hashes: 331 pages.
- No longer present: 3 URLs.
- Developer inventory: 992 content captures and 2,727 catalog-only references.

Hash changes identify source impact; they do not prove semantic changes or validate live-org behavior. Discovery remains bounded to the configured official sources and depth-four Help links. Raw article bodies are not published.

Related-topic decisions are recorded in [the operating model](docs-watch-operating-model.md). Included sources cover Tableau Semantics, Agentforce session tracing, profile context, hosted Data 360 MCP, and terminology. General workshops and unrelated product setup remain outside the authoritative crawl.

## Claim Source Coverage

The following existing official claim sources are absent from this bounded graph. This is a coverage gap, not proof that their URLs or claims are invalid:

- KC-003: https://help.salesforce.com/s/articleView?id=data.c360_a_data_model_object_relationships.htm&language=en_US&type=5
- KC-013: https://developer.salesforce.com/docs/data/data-cloud-query-guide/references/data-cloud-query-api-reference/c360a-api-queryservices-overview.html

Local-source claims and official-source captures have not been re-certified against an org by this documentation refresh.

## Added Pages

| Title | Source type | Capture status | Official source |
| --- | --- | --- | --- |
| Read Zero-Copy Data in Code Extension / Code Extension in Data 360 / Data 360 Code Extension Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-code-ext/guide/read-zero-copy-sources.html) |
| Call Predictive Models in Batch Transform Scripts / Code Extension in Data 360 / Data 360 Code Extension Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-code-ext/guide/use-predictive-model-in-custom-script.html) |
| AccountScoreAdjustment DLO Mappings | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-accountscoreadjustment_dmo_mappings.html) |
| AuthorizationTierDefinition DLO Mappings | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-authorizationtierdefinition_dmo_mappings.html) |
| AuthTierDataUsePurpose DLO Mappings | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-authtierdatausepurpose_dmo_mappings.html) |
| BnftAuthTierDef DLO Mappings | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-bnftauthtierdef_dmo_mappings.html) |
| BusinessUnitChnlTypeRate DLO Mappings | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-businessunitchnltyperate_dmo_mappings.html) |
| CampaignCohort DLO Mappings | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-campaigncohort_dmo_mappings.html) |
| CampaignCohortAttribute DLO Mappings | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-campaigncohortattribute_dmo_mappings.html) |
| CampaignCohortCampaignRanking DLO Mappings | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-campaigncohortcampaignranking_dmo_mappings.html) |
| CampaignPartyAsgnt DLO Mappings | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-campaignpartyasgnt_dmo_mappings.html) |
| CmpnPartyAsgntConsideration DLO Mappings | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-cmpnpartyasgntconsideration_dmo_mappings.html) |
| ContactScoreAdjustment DLO Mappings | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-contactscoreadjustment_dmo_mappings.html) |
| Contract DLO Mappings | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-contract_dmo_mappings.html) |
| EventPlan DLO Mappings | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-eventplan_dmo_mappings.html) |
| Knowledge__DataCategorySelection DLO Mappings | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-knowledge__datacategoryselection_dmo_mappings.html) |
| Knowledge__ka DLO Mappings | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-knowledge__ka_dmo_mappings.html) |
| Knowledge__kav DLO Mappings | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-knowledge__kav_dmo_mappings.html) |
| LeadScoreAdjustment DLO Mappings | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-leadscoreadjustment_dmo_mappings.html) |
| Action Candidate DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-actioncandidatedmo-dmo.html) |
| Ai Agent Tag Assoc Log DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-aiagenttagassoclogdmo-dmo.html) |
| Authorization Tier Definition DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-authorizationtierdefinitiondmo-dmo.html) |
| Auth Tier Data Use Purpose DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-authtierdatausepurposedmo-dmo.html) |
| Bnft Auth Tier Def DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-bnftauthtierdefdmo-dmo.html) |
| Budget Mng Event Type DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-budgetmanagedeventtypedmo-dmo.html) |
| Business Unit Chnl Type Rate DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-businessunitchnltyperatedmo-dmo.html) |
| Buying Committee Campaign DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-buyingcommitteecampaigndmo-dmo.html) |
| Buying Committee Content DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-buyingcommitteecontentdmo-dmo.html) |
| Buying Committee DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-buyingcommitteedmo-dmo.html) |
| Buying Committee Member DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-buyingcommitteememberdmo-dmo.html) |
| Buying Committee Product DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-buyingcommitteeproductdmo-dmo.html) |
| Buying Committee Role DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-buyingcommitteeroledmo-dmo.html) |
| Buying Comte Mbr Role Asgnt DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-buyingcomtembrroleasgntdmo-dmo.html) |
| Campaign Cohort Attribute DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-campaigncohortattributedmo-dmo.html) |
| Campaign Cohort Campaign Ranking DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-campaigncohortcampaignrankingdmo-dmo.html) |
| Campaign Cohort DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-campaigncohortdmo-dmo.html) |
| Campaign Party Asgnt DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-campaignpartyasgntdmo-dmo.html) |
| Care Gap Campaign DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-caregapcampaigndmo-dmo.html) |
| Cmpn Party Asgnt Consideration DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-cmpnpartyasgntconsiderationdmo-dmo.html) |
| Conv Billing Outcome Ptcp Agent DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-convbillingoutcomeptcpagentdmo-dmo.html) |
| Conversation Billing Outcome DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-conversationbillingoutcomedmo-dmo.html) |
| Field History DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-datamodelobjfieldvalhistdmo-dmo.html) |
| Event Mgmt Appvl Item Rule Grp DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-eventmgmtappvlitemrulegrpdmo-dmo.html) |
| Event Mgmt Rule DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-eventmgmtruledmo-dmo.html) |
| Event Mgmt Rule Group DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-eventmgmtrulegroupdmo-dmo.html) |
| Event Mgmt Rule Grp Asgn Rule DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-eventmgmtrulegrpasgnruledmo-dmo.html) |
| Event Mgmt Status DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-eventmgmtstatusdmo-dmo.html) |
| Glb Tenant Consumption Insights DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-glbtenantconsumptioninsightsdmo-dmo.html) |
| Glb Tenant Entitlement Transaction DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-glbtenantentitlementtransactiondmo-dmo.html) |
| Mng Event Capacity Rsv DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-managedeventcapacityrsvdmo-dmo.html) |
| Mng Event Session Participant DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-managedeventsessionptcpdmo-dmo.html) |
| Mng Event Supplier Product DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-managedeventsupplierproductdmo-dmo.html) |
| Mng Event Territory DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-managedeventterritorydmo-dmo.html) |
| Program Product DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-programproductdmo-dmo.html) |
| Rbt Pgm Rbt Typ Accrual Src Trxn DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-rbtpgmrbttypaccrualsrctrxndmo-dmo.html) |
| Rbt Pgm Rbt Typ Payout Src Trxn DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-rbtpgmrbttyppayoutsrctrxndmo-dmo.html) |
| Software License DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-softwarelicensedmo-dmo.html) |
| Software License Pstn Snpsht DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-softwarelicensepstnsnpshtdmo-dmo.html) |
| Software License Usage DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-softwarelicenseusagedmo-dmo.html) |
| Software License Use Metric DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-softwarelicenseusemetricdmo-dmo.html) |
| Staged Sftwr License Usage DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-stagedsftwrlicenseusagedmo-dmo.html) |
| Staged Software License DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-stagedsoftwarelicensedmo-dmo.html) |
| Supplier Product Location DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-supplierproductlocationdmo-dmo.html) |
| Supplier Product Relation DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-supplierproductrelationdmo-dmo.html) |
| Tax Document DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-taxdocumentdmo-dmo.html) |
| Tax Document Item DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-taxdocumentitemdmo-dmo.html) |
| Tax Filing Assessment DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-taxfilingassessmentdmo-dmo.html) |
| Tax Filing Assessment Document DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-taxfilingassessmentdocumentdmo-dmo.html) |
| Tax Filing Assessment Line Item DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-taxfilingassessmentlineitemdmo-dmo.html) |
| Tax Filing Assessment Line Itm Doc DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-taxfilingassessmentlineitmdocdmo-dmo.html) |
| Tax Filing Document DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-taxfilingdocumentdmo-dmo.html) |
| Tax Filing Line Item DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-taxfilinglineitemdmo-dmo.html) |
| Tax Filing Line Item Document DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-taxfilinglineitemdocumentdmo-dmo.html) |
| Tax Filing Participant DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-taxfilingparticipantdmo-dmo.html) |
| Tax Filing Payment Instrument DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-taxfilingpaymentinstrumentdmo-dmo.html) |
| Tax Filing Tax Account DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-taxfilingtaxaccountdmo-dmo.html) |
| Tax Payment DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-taxpaymentdmo-dmo.html) |
| Tax Refund DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-taxrefunddmo-dmo.html) |
| SoftwareLicense DLO Mappings | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-softwarelicense_dmo_mappings.html) |
| SoftwareLicenseConnector DLO Mappings | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-softwarelicenseconnector_dmo_mappings.html) |
| SoftwareLicenseUsage DLO Mappings | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-softwarelicenseusage_dmo_mappings.html) |
| SoftwareLicenseUsageConnector DLO Mappings | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-softwarelicenseusageconnector_dmo_mappings.html) |
| VideoCallTranscript DLO Mappings | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-videocalltranscript_dmo_mappings.html) |
| CMS Advanced | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/CmsAdvanced.html) |
| CMS Base Search | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/CmsBaseSearch.html) |
| Create a Flare Unstructured Data Lake Object (UDLO) / Data 360 Integrations / Data 360 Integration Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-create-a-flare-udlo.html) |
| Create a Heretto Unstructured Data Lake Object / Data 360 Integrations / Data 360 Integration Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-create-a-heretto-udlo.html) |
| Create a IXIA CCMS Unstructured Data Lake Object / Data 360 Integrations / Data 360 Integration Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-create-a-ixia-ccms-udlo.html) |
| Create a SFTP Unstructured Data Lake Object / Data 360 Integrations / Data 360 Integration Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-create-a-sftp-unstructured-udlo.html) |
| Create a Tridion Unstructured Data Lake Object / Data 360 Integrations / Data 360 Integration Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-create-a-tridion-udlo.html) |
| Create a OneNote Unstructured Data Lake Object / Data 360 Integrations / Data 360 Integration Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-create-microsoftonenote-udlo.html) |
| CrowdStrike Connector / Data 360 Integrations / Data 360 Integration Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-crowdstrike-connector.html) |
| DigitSec Connector / Data 360 Integrations / Data 360 Integration Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-digitsec-connector.html) |
| Flare Connector Limitations / Data 360 Integrations / Data 360 Integration Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-flare-connector-limitations.html) |
| Flare Connector / Data 360 Integrations / Data 360 Integration Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-flare-connector.html) |
| Heretto Connector Limitations / Data 360 Integrations / Data 360 Integration Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-heretto-connector-limitations.html) |
| Heretto Connector / Data 360 Integrations / Data 360 Integration Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-heretto-connector.html) |
| IXIA CCMS Connector Limitations / Data 360 Integrations / Data 360 Integration Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-ixia-ccms-connector-limitations.html) |
| IXIA CCMS Connector / Data 360 Integrations / Data 360 Integration Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-ixia-ccms-connector.html) |
| LY Ads Activation Connector / Data 360 Integrations / Data 360 Integration Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-lyadsadaudiences-connector.html) |
| Set Up a Connection to LY Ads / Data 360 Integrations / Data 360 Integration Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-lyadsadaudiences-setup.html) |
| MadCap Software Integration / Data 360 Integrations / Data 360 Integration Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-madcap-integration.html) |
| Microsoft OneNote Unstructured Connector / Data 360 Integrations / Data 360 Integration Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-microsoftonenote-connector.html) |
| Okta Connector / Data 360 Integrations / Data 360 Integration Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-okta-connector.html) |
| Prepare Your OneNote Unstructured Connection / Data 360 Integrations / Data 360 Integration Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-prepare-microsoftonenote-connection.html) |
| Prepare Your Flare Connection / Data 360 Integrations / Data 360 Integration Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-prepare-your-flare-connection.html) |
| Prepare Your Heretto Connection / Data 360 Integrations / Data 360 Integration Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-prepare-your-heretto-connection.html) |
| Prepare Your IXIA CCMS Connection / Data 360 Integrations / Data 360 Integration Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-prepare-your-ixia-ccms-connection.html) |
| Prepare Your SFTP Unstructured Connection / Data 360 Integrations / Data 360 Integration Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-prepare-your-sftp-unstructured-connection.html) |
| Prepare Your Tridion Connection / Data 360 Integrations / Data 360 Integration Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-prepare-your-tridion-connection.html) |
| Reddit Ads Activation Connector / Data 360 Integrations / Data 360 Integration Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-redditadaudiences-connector.html) |
| Set Up a Connection to Reddit Ads Manager / Data 360 Integrations / Data 360 Integration Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-redditadaudiences-setup.html) |
| Set Up a Flare Connection / Data 360 Integrations / Data 360 Integration Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-set-up-flare-connection.html) |
| Set Up a Heretto Connection / Data 360 Integrations / Data 360 Integration Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-set-up-heretto-connection.html) |
| Set Up a IXIA CCMS Connection / Data 360 Integrations / Data 360 Integration Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-set-up-ixia-ccms-connection.html) |
| Set Up a OneNote Unstructured Connection / Data 360 Integrations / Data 360 Integration Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-set-up-microsoftonenote-connection.html) |
| Set Up a SFTP Unstructured Connection / Data 360 Integrations / Data 360 Integration Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-set-up-sftp-unstructured-connection.html) |
| Set Up a Tridion Connection / Data 360 Integrations / Data 360 Integration Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-set-up-tridion-connection.html) |
| SFTP Unstructured Connector Limitations / Data 360 Integrations / Data 360 Integration Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-sftp-unstructured-connector-limitations.html) |
| Secure File Transfer Protocol (SFTP) Unstructured Connector / Data 360 Integrations / Data 360 Integration Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-sftp-unstructured-connector.html) |
| Tridion Connector Limitations / Data 360 Integrations / Data 360 Integration Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-tridion-connector-limitations.html) |
| Tridion Connector / Data 360 Integrations / Data 360 Integration Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-tridion-connector.html) |
| Update a Web or Mobile App Data Stream / Data 360 Integrations / Data 360 Integration Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-update-mobile-web-datastream.html) |
| Data 360 / Reference / Hosted MCP Servers / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/platform/hosted-mcp-servers/references/reference/data360-mcp.html) |
| Agentforce Session Tracing | help | captured | [Source](https://help.salesforce.com/s/articleView?id=ai.generative_ai_session_trace.htm&language=en_US&type=5) |
| About Tableau Semantics | help | captured | [Source](https://help.salesforce.com/s/articleView?id=analytics.c360_a_sl_get_started.htm&language=en_US&type=5) |
| Identity Boost for Ad Audiences Partners | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_ad_audiences_identity_boost.htm&language=en_US&type=5) |
| Add Calculated Insights to a Data Graph | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_add_calculated_insights_to_a_data_graph.htm&language=en_US&type=5) |
| Configure a Key Qualifier Field | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_add_or_view_key_qualifier.htm&language=en_US&type=5) |
| Get Trusted AI Responses with Retriever Citations | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_ai_citations_retriever.htm&language=en_US&type=5) |
| Create an Individual Retriever | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_ai_retriever_create.htm&language=en_US&type=5) |
| Retriever Support in Data Cloud One | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_ai_retriever_data_cloud_one.htm&language=en_US&type=5) |
| Create an Ensemble Retriever | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_ai_retriever_ensemble_create.htm&language=en_US&type=5) |
| Billing Considerations for Testing Retrievers | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_ai_retriever_test_billing.htm&language=en_US&type=5) |
| Test an Individual Retriever | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_ai_retriever_test_create.htm&language=en_US&type=5) |
| Test an Ensemble Retriever | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_ai_retriever_test_ensemble.htm&language=en_US&type=5) |
| Retriever Metrics and Results | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_ai_retriever_test_metrics.htm&language=en_US&type=5) |
| Customize, Test, and Validate Retrievers with Retriever Playground | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_ai_retriever_test.htm&language=en_US&type=5) |
| Activate or Deactivate a Retriever Version | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_ai_retriever_version_activate.htm&language=en_US&type=5) |
| Edit or Delete a Retriever Version | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_ai_retriever_version_edit.htm&language=en_US&type=5) |
| Manage Retrievers | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_ai_retriever_version.htm&language=en_US&type=5) |
| Applying Filters in the Data Graph | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_apply_filters_dg.htm&language=en_US&type=5) |
| Authoring Methods for Insights | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_authoring_methods_for_insights.htm&language=en_US&type=5) |
| Billing Considerations for Data Graphs | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_billing_considerations_for_data_graphs.htm&language=en_US&type=5) |
| Build and Manage Data Graphs | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_build_and_manage_data_graphs.htm&language=en_US&type=5) |
| Zero Copy Data Federation | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_byol_data_federation.htm&language=en_US&type=5) |
| Check Connector Status | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_check_connector_status.htm&language=en_US&type=5) |
| Clone a Data Graph | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_clone_a_data_graph.htm&language=en_US&type=5) |
| Configure the Data 360 Engagement Timeline Widget | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_configure_engagement_timeline_widget.htm&language=en_US&type=5) |
| Connect Salesforce CRM Orgs to Data 360 | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_connect_salesforce_orgs.htm&language=en_US&type=5) |
| Controlling External User Access in Data 360 | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_control_external_user_access.htm&language=en_US&type=5) |
| Identity Boost | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_crc_identity_boost.htm&language=en_US&type=5) |
| Create a Data Graph from a Data Kit | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_create_a_data_graph_data_kit.htm&language=en_US&type=5) |
| Data Refresh Process for Extraction | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_crm_data_refresh_process_for_extraction.htm&language=en_US&type=5) |
| Considerations for Data Kits in Data 360 | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_data_cloud_datakit_consideration.htm&language=en_US&type=5) |
| Data Graph Refresh History | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_data_graph_refresh_history.htm&language=en_US&type=5) |
| Data Kits | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_data_package_kits.htm&language=en_US&type=5) |
| Create and Publish a Standard Data Kit | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_data_stream_bundle_package_kits.htm&language=en_US&type=5) |
| Attribute Data Query Costs to Agentforce Sessions and API Requests | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_data_usage_correlation_identifier.htm&language=en_US&type=5) |
| Delete a Data Graph | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_delete_a_data_graph.htm&language=en_US&type=5) |
| Data Drift in High-Frequency Data Graph Refreshes | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_dg_data_drift.htm&language=en_US&type=5) |
| Control Data Graph Access | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_dg_granular_gov.htm&language=en_US&type=5) |
| Reapply Tags for a Data Graph | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_dg_reapply_tags.htm&language=en_US&type=5) |
| Fully Qualified Keys in Data Objects | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_dlo_dmo_key_qualifiers.htm&language=en_US&type=5) |
| Billing Considerations for Document AI | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_document_ai_billing_considerations.htm&language=en_US&type=5) |
| Edit a Data Graph | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_edit_a_data_graph.htm&language=en_US&type=5) |
| Enable Data 360 Data Q&A Agent | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_enable_data_qna_agent.htm&language=en_US&type=5) |
| View the Number of Successfully Synced Pages per Connector Run | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_find_how_many_pages_synced_successfully.htm&language=en_US&type=5) |
| Find How Many Records of a Specific Type Synced Successfully | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_find_how_many_records_of_a_specific_type_synced_successfully.htm&language=en_US&type=5) |
| List Which Pages Synced Successfully | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_find_which_pages_synced_successfully.htm&language=en_US&type=5) |
| Hybrid Search Autodrop Best Practices | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_hybridsearch_autodrop_best_practices.htm&language=en_US&type=5) |
| Hybrid Search Query Expressions for Autodrop | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_hybridsearch_autodrop_query.htm&language=en_US&type=5) |
| Hybrid Search Autodrop Results | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_hybridsearch_autodrop.htm&language=en_US&type=5) |
| Hybrid Search Best Practices | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_hybridsearch_best_practices.htm&language=en_US&type=5) |
| Hybrid Search Fusion Ranking | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_hybridsearch_fusion_ranking.htm&language=en_US&type=5) |
| Hybrid Search Query Expressions | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_hybridsearch_query_expressions.htm&language=en_US&type=5) |
| Influence Hybrid Search Relevance Ranking | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_hybridsearch_relevance_configuration.htm&language=en_US&type=5) |
| Filter Source Records for Identity Resolution | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_identity_resolution_filter_records.htm&language=en_US&type=5) |
| Authoring Considerations for Insights | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_insights_considerations.htm&language=en_US&type=5) |
| Install Standard Data Bundles Powered by Data Kits | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_install_standard_data_bundles_powered_by_data_kits.htm&language=en_US&type=5) |
| Manage Data Returned in Data Graphs | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_limit_child_records_data_graph.htm&language=en_US&type=5) |
| Managing Insights | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_managing_insights.htm&language=en_US&type=5) |
| Add Filters to a Segment | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_marketing_agent_add_filters.htm&language=en_US&type=5) |
| Build a Segment by Describing It | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_marketing_agent_build_segment.htm&language=en_US&type=5) |
| Data 360 Marketing Agent Considerations and Troubleshooting | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_marketing_agent_considerations.htm&language=en_US&type=5) |
| About the Data 360 Marketing Agent | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_marketing_agent.htm&language=en_US&type=5) |
| Data 360 Governance Mergeback with DevOps Data Kits | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_mergeback_devops_datakits.htm&language=en_US&type=5) |
| Monitor the Status of Unstructured Connectors Data Ingestion | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_monitor_the_status_of_unstructured_connectors_data_ingestion.htm&language=en_US&type=5) |
| Generate Research Reports with Deep Research | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_notebook_ai_deep_research.htm&language=en_US&type=5) |
| Activation Type and Target Compatibility | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_publish_schedule_activation_target_compatibility.htm&language=en_US&type=5) |
| Record Caching and User Session Length in Real-Time Data Graphs | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_record_caching_in_rt_data_graphs.htm&language=en_US&type=5) |
| Redeploy a Data Kit When Its Data Graph Is Deployed | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_redeploy_datakit_for_dg.htm&language=en_US&type=5) |
| Refresh a Data Graph | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_refresh_a_data_graph.htm&language=en_US&type=5) |
| Retrieval Response with Enriched Search Index | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_retrieval_response_enriched_index.htm&language=en_US&type=5) |
| Retriever Filters Reference | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_retriever_filter_reference.htm&language=en_US&type=5) |
| Citations for Content Chunks | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_search_index_chunk_citations.htm&language=en_US&type=5) |
| Chunk DMO | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_search_index_chunk_dmo.htm&language=en_US&type=5) |
| Create a Search Index Configuration from a Data Kit | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_search_index_create_index_config_data_kit.htm&language=en_US&type=5) |
| Delete Search Index Configurations | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_search_index_delete_index_config.htm&language=en_US&type=5) |
| Create a Search Index Configuration with Easy Setup | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_search_index_easy_setup_search_index.htm&language=en_US&type=5) |
| Edit Search Index Configurations | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_search_index_edit_search_index.htm&language=en_US&type=5) |
| Add a Search Index Configuration to a Data Kit | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_search_index_in_data_kit.htm&language=en_US&type=5) |
| Index DMO | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_search_index_index_dmo.htm&language=en_US&type=5) |
| How the Max Token Setting Affects Chunking | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_search_index_max_token_setting.htm&language=en_US&type=5) |
| Vector Search Query Expressions and Pre-Filtering | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_search_index_query_prefilters.htm&language=en_US&type=5) |
| Rebuild a Search Index Configuration | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_search_index_rebuild_search_index.htm&language=en_US&type=5) |
| Retrieving Content with Vector Search | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_search_index_retrieve_content.htm&language=en_US&type=5) |
| SFR-v2-small Embedding Model Reference | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_search_index_sfr_v2_small.htm&language=en_US&type=5) |
| Search Index Types in Data 360 | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_search_index_types.htm&language=en_US&type=5) |
| View Search Index Status and Process History | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_search_index_view_search_index.htm&language=en_US&type=5) |
| Session Extension in Real-Time Data Graphs | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_sess_ext_data_graphs.htm&language=en_US&type=5) |
| Set Up an Amazon S3 Target Connection | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_set_up_an_amazon_s3_target_connection.htm&language=en_US&type=5) |
| Streaming Data Graphs | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_streaming_dg.htm&language=en_US&type=5) |
| Content Object Data Mappings | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_unstructured_data_connect_content_data_mappings.htm&language=en_US&type=5) |
| Ingest File Attachments from Salesforce CRM Objects into Data 360 | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_unstructured_data_connect_content_document.htm&language=en_US&type=5) |
| Update a Data Kit in Data 360 | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_update_a_data_kit_in_customer_data_platform.htm&language=en_US&type=5) |
| Use Data Cloud APIs with Data Spaces | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_using_data_cloud_apis_with_data_spaces.htm&language=en_US&type=5) |
| View Data Graph Properties and JSON Structure | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_view_data_graph_metadata.htm&language=en_US&type=5) |
| Deploy Data Kit Components in Data 360 | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_deploy_data_kit_components.htm&language=en_US&type=5) |
| Uninstall a Deployed Data Kit in Data 360 | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_uninstall_data_kit.htm&language=en_US&type=5) |
| Configure Personalization: Get Context Action | help | captured | [Source](https://help.salesforce.com/s/articleView?id=mktg.persnl_agentforce_configure_get_context_action.htm&language=en_US&type=5) |
| Data Services Billable Usage Types for Data 360 | help | captured | [Source](https://help.salesforce.com/s/articleView?id=sf.c360_a_data_usage_types.htm&language=en_US&type=5) |
| Data 360 Glossary of Terms | help | captured | [Source](https://help.salesforce.com/s/articleView?id=sf.c360_a_glossary_guide.htm&language=en_US&type=5) |
| Use Search for AI, Automation, and Analytics | help | captured | [Source](https://help.salesforce.com/s/articleView?id=sf.c360_a_search_index_ground_ai.htm&language=en_US&type=5) |

## Changed Source Hashes

| Title | Source type | Capture status | Official source |
| --- | --- | --- | --- |
| Data 360 Connect API / Data 360 Connect REST API / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/connectapi/references) |
| Write and Validate Custom Script / Code Extension in Data 360 / Data 360 Code Extension Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-code-ext/guide/author-custom-script.html) |
| Quick Start / Code Extension in Data 360 / Data 360 Code Extension Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-code-ext/guide/quickstart.html) |
| Metadata Components for Data 360 Cheat Sheet / Get Started with Data 360 Development / Data 360 Developer Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-dev/guide/component-cheatsheet.html) |
| Data 360 Extensibility Readiness Matrix / Model Data in Data 360 / Data 360 DMO and Mapping Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360a-api-isv-readiness-data.html) |
| Affiliation DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-affiliation-dmo.html) |
| Agent Service Presence DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-agent-service-presence-dmo.html) |
| Agent Work DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-agent-work-dmo.html) |
| Agent Work Skill DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-agent-work-skill-dmo.html) |
| Applicant DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-applicant-dmo.html) |
| Asset Service Level Objective Consequence DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-asset-service-level-objective-consequence-dmo.html) |
| Asset Service Level Objective DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-asset-service-level-objective-dmo.html) |
| Authorization Form Consent DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-authorization-form-consent-dmo.html) |
| Authorization Form Data Use DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-authorization-form-data-use-dmo.html) |
| Authorization Form DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-authorization-form-dmo.html) |
| Authorization Form Text DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-authorization-form-text-dmo.html) |
| Master Product DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-base-product-dmo.html) |
| Benefit Action DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-benefit-action-dmo.html) |
| Benefit Type DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-benefit-type-dmo.html) |
| Brand DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-brand-dmo.html) |
| Card Account DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-card-account-dmo.html) |
| Case Update DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-case-update-dmo.html) |
| Case DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-case.html) |
| Communication Subscription Channel Type DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-communication-subscription-channel-type-dmo.html) |
| Communication Subscription Consent DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-communication-subscription-consent-dmo.html) |
| Communication Subscription DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-communication-subscription-dmo.html) |
| Communication Subscription Timing DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-communication-subscription-timing-dmo.html) |
| Consent Action DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-consent-action-dmo.html) |
| Consent Status DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-consent-status-dmo.html) |
| Contact Point App DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-contact-point-app-dmo.html) |
| Contact Point Digital ID DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-contact-point-digitalId-dmo.html) |
| Contact Point Social DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-contact-point-social-dmo.html) |
| Conversation Entry Transcript Excerpt DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-conversation-entry-transcript-excerpt-dmo.html) |
| Conversation Reason Category DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-conversation-reason-category-dmo.html) |
| Conversation Reason DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-conversation-reason-dmo.html) |
| Conversation Reason Report Definition DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-conversation-reason-report-definition-dmo.html) |
| Conversation Reason Report Segment Def DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-conversation-reason-report-segment-def-dmo.html) |
| Data Use Legal Basis DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-data-use-legal-basis-dmo.html) |
| Data Use Purpose Consent Action DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-data-use-purpose-consent-action-dmo.html) |
| Data Use Purpose DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-data-use-purpose-dmo.html) |
| SSOT DMOs / Model Data in Data 360 / Data 360 DMO and Mapping Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-datamodelobjects.html) |
| Deposit Account DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-deposit-account-dmo.html) |
| Device Application Engagement DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-device-application-engagement-dmo.html) |
| Device Application Template DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-device-application-template-dmo.html) |
| Device DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-device-dmo.html) |
| Email Message DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-email-message-dmo.html) |
| Email Publication DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-email-publication-dmo.html) |
| Email Template DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-email-template-dmo.html) |
| Engagement Analysis Text Direct Feedback DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-engagement-analysis-text-direct-feedback-dmo.html) |
| Engagement Analysis Text DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-engagement-analysis-text-dmo.html) |
| Engagement Analysis Text Participant DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-engagement-analysis-text-participant-dmo.html) |
| Engagement Analysis Text Session DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-engagement-analysis-text-session-dmo.html) |
| Engagement Channel Type Consent DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-engagement-channel-type-consent-dmo.html) |
| Engagement Channel Type DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-engagement-channel-type-dmo.html) |
| Engagement Topic DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-engagement-topic-dmo.html) |
| Financial Account Balance DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-financial-account-balance-dmo.html) |
| Financial Account DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-financial-account-dmo.html) |
| Financial Account Fee DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-financial-account-fee-dmo.html) |
| Financial Account Interest Rate DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-financial-account-interest-rate-dmo.html) |
| Financial Account Limit DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-financial-account-limit-dmo.html) |
| Financial Account Party DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-financial-account-party-dmo.html) |
| Financial Account Transaction DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-financial-account-transaction-dmo.html) |
| Financial Application DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-financial-application-dmo.html) |
| Financial Application Item DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-financial-application-item-dmo.html) |
| Financial Application Item Proposal DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-financial-application-item-proposal-dmo.html) |
| Financial Customer DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-financial-customer-dmo.html) |
| Financial Goal DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-financial-goal-dmo.html) |
| Financial Goal Funding DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-financial-goal-funding-dmo.html) |
| Financial Goal Party DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-financial-goal-party-dmo.html) |
| Financial Holding DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-financial-holding-dmo.html) |
| Financial Plan DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-financial-plan-dmo.html) |
| Financial Security DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-financial-security-dmo.html) |
| Flow DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-flow-dmo.html) |
| Flow Element DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-flow-element-dmo.html) |
| Flow Element Run DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-flow-element-run-dmo.html) |
| Flow Run DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-flow-run-dmo.html) |
| Flow Version DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-flow-version-dmo.html) |
| Flow Version Occurrence DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-flow-version-occurrence-dmo.html) |
| Goods Product DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-goods-product-dmo.html) |
| Insurance Policy DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-insurance-policy-dmo.html) |
| Interest Tag Definition DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-interest-tag-definition-dmo.html) |
| Investment Account DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-investment-account-dmo.html) |
| Knowledge Article Engagement DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-knowledge-article-engagement-dmo.html) |
| Lead DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-lead-dmo.html) |
| Loan Account DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-loan-account-dmo.html) |
| Loyalty Benefit DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-loyalty-benefit-dmo.html) |
| Loyalty Benefit Type DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-loyalty-benefit-type-dmo.html) |
| Loyalty Journal Subtype DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-loyalty-journal-subtype-dmo.html) |
| Loyalty Journal Type DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-loyalty-journal-type-dmo.html) |
| Loyalty Ledger DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-loyalty-ledger-dmo.html) |
| Loyalty Member Currency DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-loyalty-member-currency-dmo.html) |
| Loyalty Member Tier DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-loyalty-member-tier-dmo.html) |
| Loyalty Partner Product DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-loyalty-partner-product-dmo.html) |
| Loyalty Program Currency DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-loyalty-program-currency-dmo.html) |
| Loyalty Program DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-loyalty-program-dmo.html) |
| Loyalty Program Member Promotion DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-loyalty-program-member-promotion-dmo.html) |
| Loyalty Program Partner DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-loyalty-program-partner-dmo.html) |
| Loyalty Tier Benefit DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-loyalty-tier-benefit-dmo.html) |
| Loyalty Tier DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-loyalty-tier-dmo.html) |
| Loyalty Tier Group DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-loyalty-tier-group-dmo.html) |
| Loyalty Transaction Journal DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-loyalty-transaction-journal-dmo.html) |
| Market Journey Activity DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-market-journey-activity-dmo.html) |
| Market Segment DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-market-segment-dmo.html) |
| Member Benefit DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-member-benefit-dmo.html) |
| Message Engagement DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-message-engagement-dmo.html) |
| Model Data in Data 360 / Data 360 DMO and Mapping Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-model-data.html) |
| Network Usage DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-network-usage-dmo.html) |
| Operating Hours DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-operating-hours-dmo.html) |
| Opportunity DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-opportunity-dmo.html) |
| Opportunity Product DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-opportunity-product-dmo.html) |
| Order Delivery Method DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-order-delivery-method-dmo.html) |
| Party Consent DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-party-consent-dmo.html) |
| Party Expense DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-party-expense-dmo.html) |
| Party Financial Asset DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-party-financial-asset-dmo.html) |
| Party Financial Liability DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-party-financial-liability-dmo.html) |
| Party Income DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-party-income-dmo.html) |
| Party Interest Tag DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-party-interest-tag-dmo.html) |
| Payment Method DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-payment-method-dmo.html) |
| Person Life Event DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-person-life-event-dmo.html) |
| Privacy Consent Log DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-privacy-consent-log-dmo.html) |
| Product Browse Engagement DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-product-browse-engagement-dmo.html) |
| Product Catalog Category DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-product-catalog-category-dmo.html) |
| Product Catalog DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-product-catalog-dmo.html) |
| Product Category DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-product-category-dmo.html) |
| Product Category Product DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-product-category-product-dmo.html) |
| Product Order Engagement DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-product-order-engagement-dmo.html) |
| Promotion DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-promotion-dmo.html) |
| Promotion Loyalty Partner Product DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-promotion-loyalty-partner-product-dmo.html) |
| Record Alert DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-record-alert-dmo.html) |
| Sales Store DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-sales-store-dmo.html) |
| Service Presence Status DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-service-presence-status-dmo.html) |
| Shopping Cart Engagement DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-shopping-cart-engagement-dmo.html) |
| Shopping Cart Event Type DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-shopping-cart-event-type-dmo.html) |
| Shopping Cart Product Engagement DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-shopping-cart-product-engagement-dmo.html) |
| Account Contact DMO / Model Data in Data 360 / Data 360 DMO and Mapping Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-accountcontactdmo-dmo.html) |
| Account DMO / Model Data in Data 360 / Data 360 DMO and Mapping Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-accountdmo-dmo.html) |
| Contact Point Address DMO / Model Data in Data 360 / Data 360 DMO and Mapping Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-contactpointaddressdmo-dmo.html) |
| Contact Point Consent DMO / Model Data in Data 360 / Data 360 DMO and Mapping Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-contactpointconsentdmo-dmo.html) |
| Contact Point Email DMO / Model Data in Data 360 / Data 360 DMO and Mapping Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-contactpointemaildmo-dmo.html) |
| Contact Point Phone DMO / Model Data in Data 360 / Data 360 DMO and Mapping Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-contactpointphonedmo-dmo.html) |
| Email Engagement DMO / Model Data in Data 360 / Data 360 DMO and Mapping Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-emailengagementdmo-dmo.html) |
| Standard DMOs / Model Data in Data 360 / Data 360 DMO and Mapping Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-entity-interface-dmos-introduction.html) |
| Individual DMO / Model Data in Data 360 / Data 360 DMO and Mapping Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-individualdmo-dmo.html) |
| Loyalty Program Member DMO / Model Data in Data 360 / Data 360 DMO and Mapping Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-loyaltyprogrammemberdmo-dmo.html) |
| Party DMO / Model Data in Data 360 / Data 360 DMO and Mapping Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-partydmo-dmo.html) |
| Party Identification DMO / Model Data in Data 360 / Data 360 DMO and Mapping Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-partyidentificationdmo-dmo.html) |
| Product DMO / Model Data in Data 360 / Data 360 DMO and Mapping Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-productdmo-dmo.html) |
| Sales Order DMO / Model Data in Data 360 / Data 360 DMO and Mapping Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-salesorderdmo-dmo.html) |
| Sales Order Product DMO / Model Data in Data 360 / Data 360 DMO and Mapping Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-salesorderproductdmo-dmo.html) |
| Skill DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-skill-dmo.html) |
| SMS Publication DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-sms-publication-dmo.html) |
| SMS Template DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-sms-template-dmo.html) |
| Software Application DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-software-application-dmo.html) |
| Standard DLO to DMO Mappings / Model Data in Data 360 / Data 360 DMO and Mapping Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-standard_mappings.html) |
| Survey DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-survey-dmo.html) |
| Survey Invitation DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-survey-invitation-dmo.html) |
| Survey Question DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-survey-question-dmo.html) |
| Survey Question Response DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-survey-question-response-dmo.html) |
| Survey Question Section DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-survey-question-section-dmo.html) |
| Survey Response DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-survey-response-dmo.html) |
| Survey Subject DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-survey-subject-dmo.html) |
| Survey Version DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-survey-version-dmo.html) |
| User DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-user-dmo.html) |
| User Group DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-user-group-dmo.html) |
| Voucher Definition DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-voucher-definition-dmo.html) |
| Voucher DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-voucher-dmo.html) |
| Web Search Engagement DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-web-search-engagement-dmo.html) |
| Website Engagement DMO | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-website-engagement-dmo.html) |
| Standard Data Bundles / Model Data in Data 360 / Data 360 DMO and Mapping Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/file-based-data-kits-introduction.html) |
| Adobe Analytics Custom Connector for MI / Data 360 Integrations / Data 360 Integration Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-adobeanalyticsmi-custom-connector.html) |
| Adobe Experience Manager Connector / Data 360 Integrations / Data 360 Integration Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-aem-connector.html) |
| AWS Aurora MySQL Connector / Data 360 Integrations / Data 360 Integration Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-awsrdsauroramysql-connector.html) |
| AWS Aurora PostgreSQL Connector / Data 360 Integrations / Data 360 Integration Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-awsrdsaurorapostgres-connector.html) |
| AWS RDS MariaDB Connector / Data 360 Integrations / Data 360 Integration Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-awsrdsmariadb-connector.html) |
| AWS RDS MySQL Connector / Data 360 Integrations / Data 360 Integration Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-awsrdsmysql-connector.html) |
| Amazon (AWS) RDS Oracle Connector / Data 360 Integrations / Data 360 Integration Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-awsrdsoracle-connector.html) |
| AWS RDS PostgreSQL Connector / Data 360 Integrations / Data 360 Integration Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-awsrdspostgres-connector.html) |
| AWS RDS SQL Server Connector / Data 360 Integrations / Data 360 Integration Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-awsrdssqlserver-connector.html) |
| Configure Amazon S3 Bucket Policies and Permissions / Data 360 Integrations / Data 360 Integration Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-awss3-bucket-policies.html) |
| Set Up Unstructured Data from Azure Storage / Data 360 Integrations / Data 360 Integration Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-azure-udlo.html) |
| Azure MySQL Connector / Data 360 Integrations / Data 360 Integration Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-azuremysql-connector.html) |
| Azure PostgreSQL Connector / Data 360 Integrations / Data 360 Integration Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-azurepostgres-connector.html) |
| Box Connector / Data 360 Integrations / Data 360 Integration Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-box-connector.html) |
| Confluence Unstructured Connector Limitations and Troubleshooting / Data 360 Integrations / Data 360 Integration Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-confluence-unstructured-connector-limitations.html) |
| Confluence Unstructured Connector / Data 360 Integrations / Data 360 Integration Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-confluence-unstructured-connector.html) |
| Create an Adobe Analytics Data Stream / Data 360 Integrations / Data 360 Integration Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-create-adobeanalytics-data-stream.html) |
| Create a Asana Data Stream / Data 360 Integrations / Data 360 Integration Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-create-asana-data-stream.html) |
| Create an Unstructured Data Connection from the Web Content Crawler / Data 360 Integrations / Data 360 Integration Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-create-crawler-udlo.html) |
| Create an eBay Analytics Data Stream / Data 360 Integrations / Data 360 Integration Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-create-ebayanalytics-data-stream.html) |
| Create a Facebook Data Stream / Data 360 Integrations / Data 360 Integration Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-create-facebook-data-stream.html) |
| Create a Google Analytics Data Stream / Data 360 Integrations / Data 360 Integration Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-create-googleanalytics-data-stream.html) |
| Create a Google Campaign Manager Data Stream / Data 360 Integrations / Data 360 Integration Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-create-googlecampaignmanager-data-stream.html) |
| Create a Google Contacts Data Stream / Data 360 Integrations / Data 360 Integration Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-create-googlecontacts-data-stream.html) |
| Create a Google Drive Unstructured Data Lake Object / Data 360 Integrations / Data 360 Integration Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-create-googledrive-unstructured-udlo.html) |
| Create a Instagram Data Stream / Data 360 Integrations / Data 360 Integration Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-create-instagram-data-stream.html) |
| Create a Mailchimp Data Stream / Data 360 Integrations / Data 360 Integration Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-create-mailchimp-data-stream.html) |
| Create a Microsoft Advertising Data Stream / Data 360 Integrations / Data 360 Integration Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-create-microsoftads-data-stream.html) |
| Create a Microsoft Teams Data Stream / Data 360 Integrations / Data 360 Integration Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-create-microsoftteams-data-stream.html) |
| Create a Pinterest Data Stream / Data 360 Integrations / Data 360 Integration Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-create-pinterest-data-stream.html) |
| Create a Pipedrive Data Stream / Data 360 Integrations / Data 360 Integration Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-create-pipedrive-data-stream.html) |
| Create a SendGrid Data Stream / Data 360 Integrations / Data 360 Integration Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-create-sendgrid-data-stream.html) |
| Create an Unstructured Data Connection from the Web Content Sitemap / Data 360 Integrations / Data 360 Integration Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-create-sitemap-udlo.html) |
| Create a Starburst Galaxy Data Stream / Data 360 Integrations / Data 360 Integration Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-create-starburstgalaxy-data-stream.html) |
| Create a Streak Data Stream / Data 360 Integrations / Data 360 Integration Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-create-streak-data-stream.html) |
| Create a Stripe Data Stream / Data 360 Integrations / Data 360 Integration Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-create-stripe-data-stream.html) |
| Create a Trello Data Stream / Data 360 Integrations / Data 360 Integration Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-create-trello-data-stream.html) |
| Create a Twilio Data Stream / Data 360 Integrations / Data 360 Integration Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-create-twilio-data-stream.html) |
| Data 360 Integrations / Data 360 Integration Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-data-cloud-integrations.html) |
| Facebook Connector / Data 360 Integrations / Data 360 Integration Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-facebook-connector.html) |
| GitHub Connector / Data 360 Integrations / Data 360 Integration Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-github-connector.html) |
| Google Integration / Data 360 Integrations / Data 360 Integration Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-google-integration.html) |
| Google Drive Unstructured Limitations and Troubleshooting / Data 360 Integrations / Data 360 Integration Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-googledrive-unstructured-connector-limitations.html) |
| Google Drive Unstructured Connector / Data 360 Integrations / Data 360 Integration Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-googledrive-unstructured-connector.html) |
| Guru Connector / Data 360 Integrations / Data 360 Integration Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-guru-connector.html) |
| Helpjuice Connector / Data 360 Integrations / Data 360 Integration Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-helpjuice-connector.html) |
| Heroku PostgreSQL Connector / Data 360 Integrations / Data 360 Integration Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-herokupostgres-connector.html) |
| HubSpot Connector Objects (hubspot Schema) / Data 360 Integrations / Data 360 Integration Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-hubspot-objects-hubspot.html) |
| Jira Structured Connector Objects / Data 360 Integrations / Data 360 Integration Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-jira-objects.html) |
| Jira Unstructured Connector / Data 360 Integrations / Data 360 Integration Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-jira-unstructured-connector.html) |
| Microsoft Integration / Data 360 Integrations / Data 360 Integration Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-microsoft-integration.html) |
| Microsoft Fabric Connector / Data 360 Integrations / Data 360 Integration Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-microsoftfabric-connector.html) |
| Create External Credentials for the Microsoft OneDrive Connector / Data 360 Integrations / Data 360 Integration Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-microsoftonedrive-cred.html) |
| Create External Credentials for the SharePoint Structured Connector / Data 360 Integrations / Data 360 Integration Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-microsoftsharepoint-cred.html) |
| Microsoft SharePoint Structured Connector / Data 360 Integrations / Data 360 Integration Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-microsoftsharepoint-structured-connector.html) |
| SharePoint Unstructured (Documents) Limitations and Troubleshooting / Data 360 Integrations / Data 360 Integration Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-microsoftsharepoint-unstructured-connector-limitations.html) |
| Microsoft SharePoint Unstructured (Documents) Connector / Data 360 Integrations / Data 360 Integration Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-microsoftsharepoint-unstructured-connector.html) |
| Microsoft SharePoint Unstructured (Site Pages & Site Assets) Connector / Data 360 Integrations / Data 360 Integration Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-microsoftsharepoint-unstructured-spsa-connector.html) |
| Prepare Your Google Drive Unstructured Data Connection / Data 360 Integrations / Data 360 Integration Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-prepare-googledrive-unstructured-connection.html) |
| Amazon Redshift Connector / Data 360 Integrations / Data 360 Integration Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-redshift-connector.html) |
| Set Up an Azure PostgreSQL Connection / Data 360 Integrations / Data 360 Integration Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-set-up-azurepostgres-connection.html) |
| Set Up a Google BigQuery Data Federation Connection / Data 360 Integrations / Data 360 Integration Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-set-up-bigquery-connection.html) |
| Set Up a Google Drive Structured Connection / Data 360 Integrations / Data 360 Integration Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-set-up-googledrive-connection.html) |
| Set Up a Google Drive Unstructured Connection / Data 360 Integrations / Data 360 Integration Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-set-up-googledrive-unstructured-connection.html) |
| Set Up a Google Sheets Connection / Data 360 Integrations / Data 360 Integration Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-set-up-googlesheet-connection.html) |
| Set Up a Microsoft OneDrive Connection / Data 360 Integrations / Data 360 Integration Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-set-up-microsoftonedrive-connection.html) |
| Set Up a SharePoint Structured Connection / Data 360 Integrations / Data 360 Integration Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-set-up-microsoftsharepoint-connection.html) |
| Connect a Website or Mobile App to Data 360 / Data 360 Integrations / Data 360 Integration Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-set-up-mobile-web-connection.html) |
| Set Up a Snowflake File Federation Connection / Data 360 Integrations / Data 360 Integration Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-set-up-snowflake-file-federation-connection.html) |
| Set Up a Zuora Connection / Data 360 Integrations / Data 360 Integration Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-set-up-zuora-connection.html) |
| Secure File Transfer Protocol (SFTP) Structured Connector / Data 360 Integrations / Data 360 Integration Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-sftp-connector.html) |
| Starburst Galaxy Connector / Data 360 Integrations / Data 360 Integration Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-starburstgalaxy-connector.html) |
| Data 360 Connectors and Integrations / Data 360 Integrations / Data 360 Integration Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-thirdparty-connectors.html) |
| Connect a Website with Google Analytics 4 / Data 360 Integrations / Data 360 Integration Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-web-connector-ga4.html) |
| Web Content (Crawler) Connector / Data 360 Integrations / Data 360 Integration Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-web-content-crawler-connector.html) |
| Web Content (Sitemap) Connector / Data 360 Integrations / Data 360 Integration Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-web-content-sitemap-connector.html) |
| YouTube Connector / Data 360 Integrations / Data 360 Integration Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-youtube-connector.html) |
| Zendesk Connector / Data 360 Integrations / Data 360 Integration Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-zendesk-connector.html) |
| Set Up a Starburst Galaxy Connection / Data 360 Integrations / Data 360 Integration Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-set-up-starburstgalaxy-connection.html) |
| Filter Your Query Results / Get Started With Data 360 SQL / Data 360 Query Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-query-guide/guide/filter-query-results.html) |
| Set up and Configure JDBC / Get Started with Data 360 JDBC / Data 360 Query Guide / Salesforce Developers | developer | captured | [Source](https://developer.salesforce.com/docs/data/data-cloud-query-guide/guide/jdbc-setup.html) |
| Activation for Data 360 Segments | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_activation_for_a_segment.htm&language=en_US&type=5) |
| Activation Record Home in Data 360 | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_activations_publish_history.htm&language=en_US&type=5) |
| Create an Activation for File Storage Target | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_add_activation_target.htm&language=en_US&type=5) |
| General Set Up Tasks in Data 360 | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_admin_maintenance_tasks.htm&language=en_US&type=5) |
| Create, Connect, and Activate Models | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_ai_create_connect_activate_models.htm&language=en_US&type=5) |
| Predictive AI | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_ai_predictive.htm&language=en_US&type=5) |
| Retrieve Data | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_ai_retriever.htm&language=en_US&type=5) |
| Billing Considerations for Predictive AI | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_ai_usage_inference.htm&language=en_US&type=5) |
| Use AI Models | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_ai_use_ai_models.htm&language=en_US&type=5) |
| Get Predictions, Prescriptions, and Top Predictors | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_ai_utilize.htm&language=en_US&type=5) |
| Billing Considerations for Data Federation | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_billing_considerations_for_data_federation.htm&language=en_US&type=5) |
| Billing Considerations for Data Ingestion | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_billing_considerations_for_data_ingestion.htm&language=en_US&type=5) |
| Billing Considerations for Data Transforms | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_billing_considerations_for_data_transforms.htm&language=en_US&type=5) |
| Billing Considerations for Identity Resolution | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_billing_considerations_for_identity_resolution.htm&language=en_US&type=5) |
| Billing Considerations for Insights | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_billing_considerations_for_insights.htm&language=en_US&type=5) |
| Billing Considerations for Intelligent Context | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_billing_considerations_for_intelligent_context.htm&language=en_US&type=5) |
| Billing Considerations for Multi-Currency Usage | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_billing_considerations_for_multi_currency.htm&language=en_US&type=5) |
| Billing Considerations for Segmentation | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_billing_considerations_for_segmentation.htm&language=en_US&type=5) |
| Category | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_category.htm&language=en_US&type=5) |
| Data 360 Usage and Access Changes | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_changelog_usage_and_access.htm&language=en_US&type=5) |
| Set Up a Data Cloud One Companion Connection | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_companion_connection_setup.htm&language=en_US&type=5) |
| Data Cloud One Companion Connection Statuses | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_companion_connection_statuses.htm&language=en_US&type=5) |
| Data 360 Features on Companion Orgs | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_companion_org_data_cloud_features.htm&language=en_US&type=5) |
| Set Up an External Activation Platform | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_connect_external_activation_platform.htm&language=en_US&type=5) |
| Data Source Configuration in Data 360 | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_connection_tasks.htm&language=en_US&type=5) |
| Data 360 Limits and Guidelines | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_considerations_and_guidelines.htm&language=en_US&type=5) |
| Filtering Using Containers and Attributes | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_container_basics.htm&language=en_US&type=5) |
| Create a Copy Field Enrichment | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_create_a_copy_field_enrichment.htm&language=en_US&type=5) |
| Create a Data Graph | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_create_a_data_graph.htm&language=en_US&type=5) |
| Create a Direct-DMO Related List Enrichment | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_create_a_related_list_direct_dmo_enrichment.htm&language=en_US&type=5) |
| Create a File Storage Activation Target | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_create_cloud_file_storage_activation_target.htm&language=en_US&type=5) |
| Create an Activation for an External Platform | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_create_external_activation_platform_activations.htm&language=en_US&type=5) |
| CRM Connector Streaming | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_crm_connector_streaming.htm&language=en_US&type=5) |
| Considerations for Data Cloud One in a Sandbox Org | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_data_cloud_one_sandboxes.htm&language=en_US&type=5) |
| Version Mismatch Errors in Data Cloud One Orgs | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_data_cloud_one_version_mismatch.htm&language=en_US&type=5) |
| Data 360 in a Sandbox | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_data_cloud_sandbox.htm&language=en_US&type=5) |
| Data Governance in Data 360 | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_data_gov_capabilities.htm&language=en_US&type=5) |
| Understand Data Spaces in Companion Orgs | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_data_spaces_in_companion_orgs.htm&language=en_US&type=5) |
| Data Streams in Data 360 | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_data_streams.htm&language=en_US&type=5) |
| Data Target Configuration in Data 360 | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_data_target_configuration_in_data_cloud.htm&language=en_US&type=5) |
| Data Services Billable Usage Types for Data 360 | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_data_usage_types.htm&language=en_US&type=5) |
| Data Builds the Foundation for Marketing | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_datacloud_mktgnext.htm&language=en_US&type=5) |
| Better Together: Data and AI | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_dc_ai.htm&language=en_US&type=5) |
| Data 360 Thought Leadership Content | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_dc_blogs.htm&language=en_US&type=5) |
| About Data 360 Releases | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_dc_releases.htm&language=en_US&type=5) |
| Data 360 Resources | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_dc_resources.htm&language=en_US&type=5) |
| Docling Parser | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_docling_parser.htm&language=en_US&type=5) |
| Manage Document AI Configurations | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_document_ai_manage_configs.htm&language=en_US&type=5) |
| Create a Document Schema Configuration Manually | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_document_ai_new_config_manual.htm&language=en_US&type=5) |
| Create a Document Schema Configuration Without a Source Object | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_document_ai_new_config_no_source.htm&language=en_US&type=5) |
| Document AI | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_document_ai.htm&language=en_US&type=5) |
| AI and Data Usage in Data 360 | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_einstein_data_usage_in_data_cloud.htm&language=en_US&type=5) |
| Salesforce CRM Permissions | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_enable_user_permissions_external_salesforce_org.htm&language=en_US&type=5) |
| Enrich Your Org with 360 Data and Insights | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_enrich_your_org_with_data_and_insights.htm&language=en_US&type=5) |
| Understand Enriched Index Costs | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_enriched_index_billing_considerations.htm&language=en_US&type=5) |
| Billing Considerations for Data 360 Enrichments | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_enrichment_considerations_cost.htm&language=en_US&type=5) |
| Enrichment Considerations | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_enrichment_considerations.htm&language=en_US&type=5) |
| Enrichment Troubleshooting | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_enrichment_troubleshooting.htm&language=en_US&type=5) |
| File Name Examples for File Storage Activation | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_file_name_examples.htm&language=en_US&type=5) |
| Optimize Identity Resolution | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_identity_resolution_optimize.htm&language=en_US&type=5) |
| Create Identity Resolution Rulesets | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_identity_resolution_ruleset_create.htm&language=en_US&type=5) |
| Create an Intelligent Context Configuration | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_intelligent_context_create_configuration.htm&language=en_US&type=5) |
| Intelligent Context in Data 360 | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_intelligent_context.htm&language=en_US&type=5) |
| Customer Data Platform Limits and Guidelines | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_limits_and_guidelines_cdp.htm&language=en_US&type=5) |
| Data 360 Limits and Guidelines | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_limits_and_guidelines.htm&language=en_US&type=5) |
| Manage AI Notebooks | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_notebook_ai_manage_notebooks.htm&language=en_US&type=5) |
| Explore and Research Content with Notebook AI | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_notebook_ai_research_analyze.htm&language=en_US&type=5) |
| Private Connect for Data 360 | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_private_connect_data_cloud.htm&language=en_US&type=5) |
| Get Started with Data 360 | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_product_considerations.htm&language=en_US&type=5) |
| Query Data in Data 360 | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_query_data_in_dc.htm&language=en_US&type=5) |
| Optimize Queries with Secondary Indexes | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_query_secondary_indexes.htm&language=en_US&type=5) |
| Search Index Reference | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_search_index_reference.htm&language=en_US&type=5) |
| Chunking Strategies | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_search_index_supported_chunking_strategies.htm&language=en_US&type=5) |
| Create Segments in Data 360 | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_segments.htm&language=en_US&type=5) |
| Set Up a CRM Salesforce Org Connection | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_set_up_crm_connection.htm&language=en_US&type=5) |
| Set Up and Turn On Data 360 | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_setup_provision.htm&language=en_US&type=5) |
| Fiscal Calendar Options for Data 360 Queries | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_standard_fiscal_calendar_setup.htm&language=en_US&type=5) |
| Billing Considerations for Unstructured Data and Search Index | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_unstructured_data_billing_considerations.htm&language=en_US&type=5) |
| Unstructured Data File Formats and Connectors | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_unstructured_data_connect.htm&language=en_US&type=5) |
| Segment Time Zone | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_update_segment_time_zone.htm&language=en_US&type=5) |
| Data 360 Standard Permission Sets | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_userpermissions.htm&language=en_US&type=5) |

## No Longer Present

| Title | Source type | Capture status | Official source |
| --- | --- | --- | --- |
| Q2 DLO Mappings | developer | cataloged | [Source](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-q2_dmo_mappings.html) |
| Reduce Credit Consumption in Data 360 | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_reduce_credit_consumption.htm&language=en_US&type=5) |
| Build a Semantic Model | help | captured | [Source](https://help.salesforce.com/s/articleView?id=data.c360_a_sl.htm&language=en_US&type=5) |
