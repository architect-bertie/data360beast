# Connector Implementation Cards

Comprehensive catalog of Data 360 connectors and integrations. Organized by family
for quick classification, with detailed cards for the high-traffic connectors and
a complete A-Z master table at the bottom.

**Source:** [c360-a-thirdparty-connectors.html](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-thirdparty-connectors.html) (Salesforce Developer Guide).

**Status notes:**
- A connector marked "GA / Beta (Zero Copy)" is GA for Batch ingestion but the Zero Copy / Query Federation path is still Beta.
- Beta connectors are gated by the [Beta Services Terms](https://www.salesforce.com/company/legal/agreements/).
- The Apache family is largely Beta (Iceberg is GA).
- Marketing Intelligence connectors are excluded from this skill pack by user policy.

---

## Detailed Cards (High-Traffic Connectors)

### Ingestion API

| Field | Value |
|---|---|
| Direction | Data In |
| Data type | Structured |
| Method | Bulk, Streaming |
| Setup | Upload OAS/YAML schema → create data stream → share dev info |
| Auth | External Client App + OAuth scopes (`cdp_ingest_api`, `api`, `refresh_token`) |
| Key facts | Single connector handles bulk and streaming; schema defines objects and attributes; status transitions from "Needs Data Stream" to "In Use" |
| Sub-pages | Schema requirements, data stream creation, External Client App setup, connector status, partial record update, developer handoff |
| Permissions | System Admin or Data Cloud Architect |
| Dev Guide | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-connect-an-ingestion-source.html |

### MuleSoft Anypoint Connector

| Field | Value |
|---|---|
| Direction | Bidirectional |
| Data type | Structured |
| Method | Batch (Bulk Ingestion API), Streaming (Streaming Ingestion API), Query |
| Setup | Set up Ingestion API first → configure MuleSoft Anypoint Connector |
| Key facts | Eliminates manual REST calls; handles JWT renewal; supports query/profile/CI APIs; pre-built connectors on Anypoint Exchange for SAP, Marketo, Dynamics, Kafka |
| Use cases | CDC streaming, legacy bulk loads, publish insights back to CRM |
| Dev Guide | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-mulesoft.html |

### Amazon S3 Storage

| Field | Value |
|---|---|
| Direction | Bidirectional (Data In + Data Out / Target) |
| Data type | Structured, Unstructured |
| Method | Batch |
| Key facts | Supports ingestion from S3 buckets and activation/export to S3 targets; credential rotation via Metadata API |
| Dev Guide | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-awss3-connector.html |

### Snowflake

| Field | Value |
|---|---|
| Direction | Bidirectional (Data In + Data Share Out) |
| Data type | Structured |
| Method | Zero Copy |
| Key facts | Zero-copy federation — no ETL duplication; live query and data sharing; bidirectional sharing |
| Dev Guide | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-snowflake-connector.html |

### Google BigQuery

| Field | Value |
|---|---|
| Direction | Bidirectional |
| Data type | Structured |
| Method | Zero Copy |
| Key facts | Zero-copy federation; bidirectional sharing; no duplication |
| Dev Guide | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-bigquery-connector.html |

### Databricks

| Field | Value |
|---|---|
| Direction | Data In |
| Data type | Structured |
| Method | Batch, Zero Copy, Query Federation, Data Share |
| Status note | Connector page reports GA across batch + QF + FF + Data Share; some family pages list as Beta — connector page is authoritative |
| Dev Guide | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-databricks-connector.html |

### Amazon Redshift

| Field | Value |
|---|---|
| Direction | Bidirectional |
| Data type | Structured |
| Method | Zero Copy |
| Dev Guide | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-redshift-connector.html |

### Apache Iceberg

| Field | Value |
|---|---|
| Direction | Data In |
| Data type | Structured |
| Method | Zero Copy (file-fed) |
| Status | GA |
| Dev Guide | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-apacheiceberg-connector.html |

### AWS Glue Data Catalog

| Field | Value |
|---|---|
| Direction | Data In |
| Data type | Structured |
| Method | Zero Copy (catalog-level federation) |
| Dev Guide | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-awsglue-connector.html |

### IBM watsonx.data

| Field | Value |
|---|---|
| Direction | Data In |
| Data type | Structured |
| Method | Zero Copy |
| Dev Guide | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-watsonx-connector.html |

### Amazon Kinesis (Streaming)

| Field | Value |
|---|---|
| Direction | Data In |
| Data type | Structured |
| Method | Streaming |
| Dev Guide | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-awskinesisds-connector.html |

### Amazon MSK (Kafka)

| Field | Value |
|---|---|
| Direction | Data In |
| Data type | Structured |
| Method | Streaming |
| Dev Guide | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-amazonkafka-connector.html |

### Salesforce Platform Events

| Field | Value |
|---|---|
| Direction | Data In |
| Data type | Structured |
| Method | Batch |
| Status note | Recently moved to Beta per "What's New" section; gated by Beta Services Terms |
| Dev Guide | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-eventbusconnector-connector.html |

### Web Content (Crawler) and Sitemap

| Field | Value |
|---|---|
| Direction | Data In |
| Data type | Unstructured |
| Method | Batch |
| Key facts | Crawler walks pages from a seed URL; Sitemap variant uses sitemap.xml; both feed UDLO/UDMO path |
| Dev Guide | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-web-content-crawler-connector.html and c360-a-web-content-sitemap-connector.html |

### Cloud Storage (Azure, Google Cloud Storage)

| Field | Value |
|---|---|
| Direction | Bidirectional |
| Data type | Structured, Unstructured |
| Method | Batch |
| Key facts | Both Azure Storage and GCS offer bidirectional batch with structured and unstructured support |
| Dev Guides | Azure: c360-a-azureblob-connector.html; GCS: c360-a-gcs-connector.html |

### SFTP

| Field | Value |
|---|---|
| Direction | Bidirectional |
| Data type | Structured |
| Method | Batch |
| Dev Guide | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-sftp-connector.html |

### MuleSoft Direct (Unstructured)

| Field | Value |
|---|---|
| Direction | Data In |
| Data type | Unstructured |
| Method | Batch |
| Dev Guide | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-mulesoft-direct.html |

---

## Family: Apache (mostly Beta)

| Connector | Status | Direction | Data Type | Method | URL |
|---|---|---|---|---|---|
| Apache Cassandra | Beta | Data In | Structured | Batch + Zero Copy | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-cassandra-connector.html |
| Apache CouchDB | Beta | Data In | Structured | Batch + Zero Copy | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-apachecouchdb-connector.html |
| Apache HBase | Beta | Data In | Structured | Batch + Zero Copy | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-apachehbase-connector.html |
| Apache Hive | Beta | Data In | Structured | Batch + Zero Copy | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-apachehive-connector.html |
| Apache Iceberg | GA | Data In | Structured | Zero Copy (file-fed) | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-apacheiceberg-connector.html |
| Apache Impala | Beta | Data In | Structured | Batch + Zero Copy | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-apacheimpala-connector.html |
| Apache Phoenix | Beta | Data In | Structured | Batch + Zero Copy | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-apachephoenix-connector.html |

---

## Family: Microsoft / Azure

| Connector | Direction | Data Type | Method | URL |
|---|---|---|---|---|
| Azure Analysis Services | Data In | Structured | Batch + Zero Copy | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-azureanalysisservices-connector.html |
| Azure Cosmos DB | Data In | Structured | Batch + Zero Copy | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-azurecosmosdb-connector.html |
| Azure MariaDB | Data In | Structured | Batch | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-azuremariadb-connector.html |
| Azure MySQL | Data In | Structured | Batch + Zero Copy | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-azuremysql-connector.html |
| Azure PostgreSQL | Data In | Structured | Batch + Zero Copy | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-azurepostgres-connector.html |
| Azure SQL Server | Data In | Structured | Batch | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-azuresqlserver-connector.html |
| Azure Storage (Blob) | Bidirectional | Structured + Unstructured | Batch | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-azureblob-connector.html |
| Azure Synapse | Data In | Structured | Batch | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-azuresynapse-connector.html |
| Microsoft 365 Excel Online | Data In | Structured | Batch + Zero Copy | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-excelonline-connector.html |
| Microsoft Advertising | Data In | Structured | Batch + Zero Copy | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-microsoftads-connector.html |
| Microsoft Dynamics 365 | Data In | Structured | Batch + Zero Copy | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-microsoftdynamics365-connector.html |
| Microsoft Fabric | Data In | Structured | Batch | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-microsoftfabric-connector.html |
| Microsoft OneDrive | Data In | Structured | Batch | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-microsoftonedrive-connector.html |
| Microsoft Power BI XMLA | Data In | Structured | Batch + Zero Copy | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-microsoftpowerbixmla-connector.html |
| Microsoft SharePoint Structured | Data In | Structured | Batch | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-microsoftsharepoint-structured-connector.html |
| Microsoft SharePoint Unstructured (Documents) | Data In | Unstructured | Batch | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-microsoftsharepoint-unstructured-connector.html |
| Microsoft SharePoint Unstructured (Site Pages) | Data In | Unstructured | Batch | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-microsoftsharepoint-unstructured-spsa-connector.html |
| Microsoft SQL Server Analysis Services | Data In | Structured | Batch + Zero Copy | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-microsoftanalysisservices-connector.html |
| Microsoft Teams | Data In | Structured | Batch + Zero Copy | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-microsoftteams-connector.html |

---

## Family: Google

| Connector | Direction | Data Type | Method | URL |
|---|---|---|---|---|
| Google Ad Manager | Data In | Structured | Batch + Zero Copy | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-googleadmanager-connector.html |
| Google Ads | Bidirectional | Structured | Batch | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-googleads-connector.html |
| Google Ads Activation | Data Out | Structured | Incremental, Direct API | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-googleadsadaudiences-connector.html |
| Google Analytics | Data In | Structured | Batch | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-googleanalytics-connector.html |
| Google BigQuery | Bidirectional | Structured | Zero Copy | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-bigquery-connector.html |
| Google Campaign Manager | Data In | Structured | Batch + Zero Copy | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-googlecampaignmanager-connector.html |
| Google Cloud Storage | Bidirectional | Structured + Unstructured | Batch | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-gcs-connector.html |
| Google Contacts | Data In | Structured | Batch + Zero Copy | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-googlecontacts-connector.html |
| Google Drive Structured | Data In | Structured | Batch | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-googledrive-structured-connector.html |
| Google Drive Unstructured | Data In | Unstructured | Batch | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-googledrive-unstructured-connector.html |
| Google DV360 Activation | Data Out | Structured | Incremental, Direct API | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-googledv360adaudiences-connector.html |
| Google Sheets | Data In | Structured | Batch | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-googlesheet-connector.html |
| Google Spanner | Data In | Structured | Batch + Zero Copy | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-googlespanner-connector.html |

---

## Family: Amazon / AWS

| Connector | Direction | Data Type | Method | URL |
|---|---|---|---|---|
| Amazon DynamoDB | Data In | Structured | Batch + Zero Copy | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-awsdynamodb-connector.html |
| Amazon Kinesis | Data In | Structured | Streaming | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-awskinesisds-connector.html |
| Amazon Marketplace | Data In | Structured | Batch + Zero Copy | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-amazonmarketplace-connector.html |
| Amazon MSK (Kafka) | Data In | Structured | Streaming | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-amazonkafka-connector.html |
| Amazon Redshift | Bidirectional | Structured | Zero Copy | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-redshift-connector.html |
| Amazon S3 Storage | Bidirectional | Structured + Unstructured | Batch | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-awss3-connector.html |
| AWS Athena | Data In | Structured | Batch | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-awsathena-connector.html |
| AWS Aurora MySQL | Data In | Structured | Batch + Zero Copy | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-awsrdsauroramysql-connector.html |
| AWS Aurora PostgreSQL | Data In | Structured | Batch + Zero Copy | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-awsrdsaurorapostgres-connector.html |
| AWS Glue Data Catalog | Data In | Structured | Zero Copy | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-awsglue-connector.html |
| AWS RDS MariaDB | Data In | Structured | Batch + Zero Copy | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-awsrdsmariadb-connector.html |
| AWS RDS MySQL | Data In | Structured | Batch + Zero Copy | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-awsrdsmysql-connector.html |
| AWS RDS Oracle | Data In | Structured | Batch + Zero Copy | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-awsrdsoracle-connector.html |
| AWS RDS PostgreSQL | Data In | Structured | Batch + Zero Copy | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-awsrdspostgres-connector.html |
| AWS RDS SQL Server | Data In | Structured | Batch + Zero Copy | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-awsrdssqlserver-connector.html |

---

## Family: IBM

| Connector | Direction | Data Type | Method | URL |
|---|---|---|---|---|
| IBM Cloudant | Data In | Structured | Batch | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-cloudant-connector.html |
| IBM Cloud Object Storage | Data In | Structured | Batch | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-ibmcloudobjectstorage-connector.html |
| IBM Db2 | Data In | Structured | Batch | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-db2-connector.html |
| IBM Informix | Data In | Structured | Batch | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-informix-connector.html |
| IBM watsonx.data | Data In | Structured | Zero Copy | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-watsonx-connector.html |

---

## Family: Oracle

| Connector | Direction | Data Type | Method | URL |
|---|---|---|---|---|
| Oracle Eloqua | Data In | Structured | Batch | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-oracleeloqua-connector.html |
| Oracle Fusion Cloud Financials | Data In | Structured | Batch + Zero Copy | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-oraclefusioncloudfinancials-connector.html |
| Oracle Fusion Cloud HCM | Data In | Structured | Batch + Zero Copy | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-oraclefusioncloudhcm-connector.html |
| Oracle Fusion Cloud SCM | Data In | Structured | Batch + Zero Copy | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-oraclescm-connector.html |
| Oracle NetSuite | Data In | Structured | Batch + Zero Copy | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-oraclenetsuite-connector.html |
| Oracle Sales Cloud | Data In | Structured | Batch | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-oraclesalescloud-connector.html |
| Oracle Service Cloud | Data In | Structured | Batch | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-oracleservicecloud-connector.html |

---

## Family: SAP

| Connector | Direction | Data Type | Method | URL |
|---|---|---|---|---|
| SAP ASE | Data In | Structured | Batch + Zero Copy | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-sapase-connector.html |
| SAP Concur | Data In | Structured | Batch + Zero Copy | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-sapconcur-connector.html |
| SAP HANA | Data In | Structured | Batch + Zero Copy | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-saphana-connector.html |
| SAP Hybris | Data In | Structured | Batch + Zero Copy | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-saphybris-connector.html |
| SAP IQ | Data In | Structured | Batch + Zero Copy | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-sapiq-connector.html |
| SAP SuccessFactors | Data In | Structured | Batch + Zero Copy | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-sapsuccessfactors-connector.html |

---

## Family: Salesforce-Native

| Connector | Direction | Data Type | Method | URL |
|---|---|---|---|---|
| Salesforce B2C Commerce Intelligence | Data In | Structured | Batch + Zero Copy | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-b2ce-connector.html |
| Salesforce Platform Events (Beta) | Data In | Structured | Batch | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-eventbusconnector-connector.html |

---

## Family: Activation-Only (Data Out)

All require the Ad Audiences add-on license. All GA, Direct API.

| Connector | Method | URL |
|---|---|---|
| Google Ads Activation | Incremental, Direct API | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-googleadsadaudiences-connector.html |
| Google DV360 Activation | Incremental, Direct API | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-googledv360adaudiences-connector.html |
| LinkedIn Conversion API (CAPI) | Streaming, Direct API | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-linkedincapi-connector.html |
| Pinterest Activation | Incremental, Direct API | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-pinterestadaudiences-connector.html |
| TikTok Ads Manager Activation | Incremental, Direct API | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-tiktokadaudiences-connector.html |

---

## Long-Tail SaaS, Database, and Content (Master A-Z Table)

For everything not detailed above. Source: index page of [c360-a-thirdparty-connectors.html](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-thirdparty-connectors.html).

| Connector | Direction | Data Type | Method | URL |
|---|---|---|---|---|
| Act! CRM | Data In | Structured | Batch + Zero Copy | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-act-connector.html |
| Act-On | Data In | Structured | Batch + Zero Copy | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-acton-connector.html |
| ActiveCampaign | Data In | Structured | Batch + Zero Copy | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-activecampaign-connector.html |
| Acumatica | Data In | Structured | Batch + Zero Copy | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-acumatica-connector.html |
| Adobe Analytics | Data In | Structured | Batch + Zero Copy | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-adobeanalytics-connector.html |
| Adobe Commerce | Data In | Structured | Batch + Zero Copy | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-adobecommerce-connector.html |
| Adobe Experience Manager | Data In | Unstructured | Batch | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-aem-connector.html |
| Adobe Marketo Engage | Data In | Structured | Batch | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-adobemarketoengage-connector.html |
| ADP | Data In | Structured | Batch + Zero Copy | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-adp-connector.html |
| Airtable | Data In | Structured | Batch + Zero Copy | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-airtable-connector.html |
| Asana | Data In | Structured | Batch + Zero Copy | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-asana-connector.html |
| BigCommerce | Data In | Structured | Batch + Zero Copy | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-bigcommerce-connector.html |
| Box | Data In | Unstructured | Batch | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-box-connector.html |
| CockroachDB | Data In | Structured | Batch + Zero Copy | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-cockroachdb-connector.html |
| Confluence (Structured) | Data In | Structured | Batch + Zero Copy | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-confluence-connector.html |
| Confluence Unstructured | Data In | Unstructured | Batch | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-confluence-unstructured-connector.html |
| Demandbase | Data In | Structured | Batch | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-demandbase-connector.html |
| eBay | Data In | Structured | Batch + Zero Copy | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-ebay-connector.html |
| eBay Analytics | Data In | Structured | Batch + Zero Copy | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-ebayanalytics-connector.html |
| Elasticsearch | Data In | Structured | Batch + Zero Copy | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-elasticsearch-connector.html |
| EnterpriseDB | Data In | Structured | Batch + Zero Copy | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-enterprisedb-connector.html |
| Epicor Kinetic | Data In | Structured | Batch + Zero Copy | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-epicorerp-connector.html |
| Facebook | Data In | Structured | Batch | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-facebook-connector.html |
| GitHub | Data In | Unstructured | Batch | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-github-connector.html |
| GraphQL | Data In | Structured | Batch + Zero Copy | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-graphql-connector.html |
| Greenplum | Data In | Structured | Batch + Zero Copy | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-greenplum-connector.html |
| Guru | Data In | Unstructured | Batch | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-guru-connector.html |
| Helpjuice | Data In | Unstructured | Batch | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-helpjuice-connector.html |
| Heroku PostgreSQL | Data In | Structured | Batch + Zero Copy | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-herokupostgres-connector.html |
| HubSpot | Data In | Structured | Batch + Zero Copy | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-hubspot-connector.html |
| Instagram | Data In | Structured | Batch + Zero Copy | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-instagram-connector.html |
| Jira Service Desk | Data In | Structured | Batch + Zero Copy | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-jiraservicedesk-connector.html |
| Jira Structured | Data In (GA Batch / Beta Zero Copy) | Structured | Batch + Zero Copy | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-jira-connector.html |
| Jira Unstructured | Data In | Unstructured | Batch + Zero Copy | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-jira-unstructured-connector.html |
| LinkedIn | Data In (GA Batch / Beta Zero Copy) | Structured | Batch + Zero Copy | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-linkedin-connector.html |
| LinkedIn Ads | Data In (GA Batch / Beta Zero Copy) | Structured | Batch + Zero Copy | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-linkedinads-connector.html |
| LinkedIn Sales Navigator | Data In | Structured | Batch | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-linkedinsalesnavigator-connector.html |
| Mailchimp | Data In | Structured | Batch + Zero Copy | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-mailchimp-connector.html |
| Meta Ads | Bidirectional | Structured | Batch | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-facebookads-connector.html |
| Monday | Data In | Structured | Batch + Zero Copy | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-monday-connector.html |
| MongoDB | Data In | Structured | Batch + Zero Copy | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-mongodb-connector.html |
| Neo4j | Data In | Structured | Batch + Zero Copy | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-neo4j-connector.html |
| OData | Data In | Structured | Batch + Zero Copy | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-odata-connector.html |
| Odoo | Data In | Structured | Batch + Zero Copy | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-odoo-connector.html |
| Paylocity | Data In | Structured | Batch + Zero Copy | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-paylocity-connector.html |
| PayPal | Data In | Structured | Batch + Zero Copy | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-paypal-connector.html |
| Pinterest | Data In | Structured | Batch + Zero Copy | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-pinterest-connector.html |
| Pipedrive | Data In | Structured | Batch + Zero Copy | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-pipedrive-connector.html |
| Redis | Data In | Structured | Batch + Zero Copy | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-redis-connector.html |
| Salesloft | Data In | Structured | Batch + Zero Copy | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-salesloft-connector.html |
| SendGrid | Data In | Structured | Batch + Zero Copy | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-sendgrid-connector.html |
| ServiceNow | Data In | Structured | Batch + Zero Copy | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-servicenow-connector.html |
| ShipStation | Data In | Structured | Batch + Zero Copy | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-shipstation-connector.html |
| Shopify | Data In | Structured | Batch + Zero Copy | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-shopify-connector.html |
| SingleStore | Data In | Structured | Batch + Zero Copy | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-singlestore-connector.html |
| Smartsheet | Data In | Structured | Batch + Zero Copy | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-smartsheet-connector.html |
| Snapchat Ads | Data In | Structured | Batch + Zero Copy | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-snapchatads-connector.html |
| Spark SQL | Data In | Structured | Batch + Zero Copy | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-sparksql-connector.html |
| Splunk | Data In | Structured | Batch + Zero Copy | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-splunk-connector.html |
| Square | Data In | Structured | Batch + Zero Copy | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-square-connector.html |
| Starburst Galaxy | Data In | Structured | Batch + Zero Copy | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-starburstgalaxy-connector.html |
| Streak | Data In | Structured | Batch + Zero Copy | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-streak-connector.html |
| Stripe | Data In | Structured | Batch + Zero Copy | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-stripe-connector.html |
| SugarCRM | Data In | Structured | Batch + Zero Copy | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-sugarcrm-connector.html |
| SuiteCRM | Data In | Structured | Batch + Zero Copy | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-suitecrm-connector.html |
| SurveyMonkey | Data In | Structured | Batch + Zero Copy | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-surveymonkey-connector.html |
| TigerGraph | Data In | Structured | Batch + Zero Copy | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-tigergraph-connector.html |
| Trello | Data In | Structured | Batch + Zero Copy | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-trello-connector.html |
| Trino | Data In | Structured | Batch + Zero Copy | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-trino-connector.html |
| Twilio | Data In | Structured | Batch + Zero Copy | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-twilio-connector.html |
| Veeva Vault | Data In | Structured | Batch + Zero Copy | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-veevavault-connector.html |
| WooCommerce | Data In | Structured | Batch + Zero Copy | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-woocommerce-connector.html |
| WordPress | Data In (GA Batch / Beta Zero Copy) | Structured | Batch + Zero Copy | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-wordpress-connector.html |
| Workday | Data In (GA Batch / Beta Zero Copy) | Structured | Batch + Zero Copy | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-workday-connector.html |
| X Ads (Twitter Ads) | Data In | Structured | Batch + Zero Copy | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-twitterads-connector.html |
| YouTube | Data In | Unstructured | Batch | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-youtube-connector.html |
| YouTube Analytics | Data In | Structured | Batch + Zero Copy | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-youtubeanalytics-connector.html |
| Zendesk | Data In | Structured + Unstructured | Batch + Zero Copy | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-zendesk-connector.html |
| ZoomInfo | Data In | Structured | Batch | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-zoominfo-connector.html |
| Zuora | Data In | Structured | Batch + Zero Copy | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-zuora-connector.html |

---

## Quick-Lookup: Connectors by Use Case

| Need | Recommended Connectors |
|---|---|
| Zero-copy live federation | Snowflake, BigQuery, Redshift, Databricks, Apache Iceberg, AWS Glue, IBM watsonx.data |
| Real-time event streaming | Amazon Kinesis, Amazon MSK (Kafka), Ingestion API streaming mode, Web/Mobile SDKs |
| Bulk batch ingest from databases | RDS family (MySQL, PostgreSQL, Oracle, SQL Server, MariaDB), Aurora, Azure SQL, SAP HANA, Oracle, MongoDB |
| File-based exchange | S3, SFTP, GCS, Azure Storage |
| Unstructured content for RAG | S3, Azure Storage, GCS, Box, GitHub, Confluence Unstructured, SharePoint Unstructured, Web Crawler/Sitemap, MuleSoft Direct |
| Marketing data ingest | Marketo, HubSpot, Mailchimp, Pardot, ActiveCampaign, Adobe Marketo Engage, Demandbase |
| CRM data ingest | Microsoft Dynamics 365, Oracle Sales Cloud, HubSpot, Pipedrive, SugarCRM, SuiteCRM, Act!, Salesloft |
| ERP data ingest | NetSuite, Oracle Fusion (Financials/HCM/SCM), SAP HANA, SAP SuccessFactors, Acumatica, Epicor Kinetic, Workday |
| Advertising activation | Google Ads, Google DV360, LinkedIn CAPI, Meta Ads, Pinterest Activation, TikTok Activation |
| Social media ingest | LinkedIn, LinkedIn Ads, Instagram, Facebook, X Ads, Snapchat Ads, YouTube, YouTube Analytics, Pinterest |
| Survey / feedback | SurveyMonkey, Typeform (via API), Zendesk |
| Support / ITSM | Zendesk, ServiceNow, Jira Service Desk, Jira (Structured/Unstructured) |
| Knowledge bases | Confluence, Guru, Helpjuice, GitHub, SharePoint, Google Drive |
| Beta-only families (use with caution) | Apache (Cassandra/CouchDB/HBase/Hive/Impala/Phoenix), Salesforce Platform Events |

---

_Total: 140+ connectors. Source: official [c360-a-thirdparty-connectors.html](https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-thirdparty-connectors.html). Marketing Intelligence connectors are excluded by user policy. Status (GA/Beta) reflects connector-page authoritative wording when family pages disagree (e.g., Databricks)._
