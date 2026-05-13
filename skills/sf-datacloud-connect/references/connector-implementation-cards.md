# Connector Implementation Cards

One card per connector category. Use for quick pattern classification before
implementation. Source: Data 360 Integration Guide (developer.salesforce.com).

---

## Ingestion API

| Field | Value |
|---|---|
| Direction | Data In |
| Data type | Structured |
| Method | Bulk, Streaming |
| Setup | Upload OAS/YAML schema → create data stream → share dev info |
| Auth | External Client App + OAuth scopes (`cdp_ingest_api`, `api`, `refresh_token`) |
| Key facts | Single connector handles both bulk and streaming; schema defines objects and attributes; status transitions from "Needs Data Stream" to "In Use" |
| Sub-pages | Schema requirements, data stream creation, External Client App setup, connector status, partial record update, developer handoff |
| Permissions | System Admin or Data Cloud Architect |
| Dev Guide | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-connect-an-ingestion-source.html |

---

## MuleSoft Anypoint Connector

| Field | Value |
|---|---|
| Direction | Bidirectional |
| Data type | Structured |
| Method | Batch (Bulk Ingestion API), Streaming (Streaming Ingestion API), Query |
| Setup | Set up Ingestion API first → configure MuleSoft Anypoint Connector |
| Key facts | Eliminates manual REST calls; handles JWT renewal; supports query/profile/CI APIs for data out; pre-built connectors on Anypoint Exchange for SAP, Marketo, Dynamics, Kafka, etc. |
| Use cases | CDC streaming, legacy bulk loads, publish insights back to CRM |
| Dev Guide | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-mulesoft.html |

---

## Amazon S3 Storage

| Field | Value |
|---|---|
| Direction | Bidirectional (Data In + Data Out/Target) |
| Data type | Structured, Unstructured |
| Method | Batch |
| Key facts | Supports ingestion from S3 buckets and activation/export to S3 targets; credential rotation via Metadata API |
| Dev Guide | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-awss3-connector.html |

---

## Snowflake

| Field | Value |
|---|---|
| Direction | Bidirectional (Data In + Data Share Out) |
| Data type | Structured |
| Method | Zero Copy |
| Key facts | Zero-copy federation — no ETL duplication; live query and data sharing; bidirectional sharing available |
| Dev Guide | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-snowflake-connector.html |

---

## Google BigQuery

| Field | Value |
|---|---|
| Direction | Bidirectional |
| Data type | Structured |
| Method | Zero Copy |
| Key facts | Zero-copy federation; bidirectional data sharing; no data duplication |
| Dev Guide | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-bigquery-connector.html |

---

## Databricks

| Field | Value |
|---|---|
| Direction | Data In |
| Data type | Structured |
| Method | Batch, Zero Copy |
| Key facts | Supports both traditional batch ingest and zero-copy federation |
| Dev Guide | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-databricks-connector.html |

---

## Amazon Redshift

| Field | Value |
|---|---|
| Direction | Bidirectional |
| Data type | Structured |
| Method | Zero Copy |
| Key facts | Zero-copy bidirectional connector |
| Dev Guide | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-redshift-connector.html |

---

## Apache Iceberg

| Field | Value |
|---|---|
| Direction | Data In |
| Data type | Structured |
| Method | Zero Copy |
| Key facts | Open table format federation; file-based zero-copy without traditional ETL |
| Dev Guide | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-apacheiceberg-connector.html |

---

## AWS Glue Data Catalog

| Field | Value |
|---|---|
| Direction | Data In |
| Data type | Structured |
| Method | Zero Copy |
| Key facts | Metadata-catalog-level federation; connects Data 360 to the Glue catalog layer |
| Dev Guide | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-awsglue-connector.html |

---

## IBM watsonx.data

| Field | Value |
|---|---|
| Direction | Data In |
| Data type | Structured |
| Method | Zero Copy |
| Key facts | Zero-copy federation into Data 360 from watsonx lakehouse |
| Dev Guide | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-watsonx-connector.html |

---

## Amazon Kinesis (Streaming)

| Field | Value |
|---|---|
| Direction | Data In |
| Data type | Structured |
| Method | Streaming |
| Key facts | Real-time event streaming ingestion |
| Dev Guide | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-awskinesisds-connector.html |

---

## Amazon MSK (Kafka)

| Field | Value |
|---|---|
| Direction | Data In |
| Data type | Structured |
| Method | Streaming |
| Key facts | Kafka-based streaming ingestion from Amazon MSK |
| Dev Guide | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-amazonkafka-connector.html |

---

## Salesforce Platform Events

| Field | Value |
|---|---|
| Direction | Data In |
| Data type | Structured |
| Method | Batch |
| Key facts | Ingests Salesforce Platform Events into Data 360 |
| Dev Guide | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-eventbusconnector-connector.html |

---

## Web and Mobile App Connectors

| Field | Value |
|---|---|
| Direction | Data In |
| Data type | Structured (engagement events) |
| Method | Streaming (SDK) |
| Key facts | Salesforce Interactions SDK (web behavior), Engagement Mobile SDK (mobile events); captures profile, engagement, and browsing activity |
| Dev Guide | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-mobile-web-app-connector.html |

---

## Web Content (Crawler)

| Field | Value |
|---|---|
| Direction | Data In |
| Data type | Unstructured |
| Method | Batch |
| Key facts | Crawls web pages for unstructured content ingestion into UDLO/UDMO path |
| Dev Guide | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-web-content-crawler-connector.html |

---

## Web Content (Sitemap)

| Field | Value |
|---|---|
| Direction | Data In |
| Data type | Unstructured |
| Method | Batch |
| Key facts | Uses sitemap.xml to discover and ingest pages as unstructured content |
| Dev Guide | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-web-content-sitemap-connector.html |

---

## Cloud Storage (Azure, Google Cloud Storage)

| Field | Value |
|---|---|
| Direction | Bidirectional |
| Data type | Structured, Unstructured |
| Method | Batch |
| Key facts | Azure Storage and Google Cloud Storage offer bidirectional batch with structured and unstructured support |
| Dev Guides | Azure: c360-a-azureblob-connector.html, GCS: c360-a-gcs-connector.html |

---

## SFTP

| Field | Value |
|---|---|
| Direction | Bidirectional |
| Data type | Structured |
| Method | Batch |
| Key facts | File-based batch exchange; can serve as both ingestion source and activation target |
| Dev Guide | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-sftp-connector.html |

---

## Activation-Only Connectors (Data Out)

| Connector | Method | Key facts |
|---|---|---|
| Google Ads Activation | Incremental, Direct API | Audience push to Google Ads |
| Google DV360 Activation | Incremental, Direct API | Audience push to Display & Video 360 |
| TikTok Ads Manager Activation | Incremental | Segment activation to TikTok |
| LinkedIn Conversion API (CAPI) | Streaming, Direct API | Real-time conversion events to LinkedIn |
| Pinterest Activation | Incremental, Direct API | Audience push to Pinterest |

---

## MuleSoft Direct

| Field | Value |
|---|---|
| Direction | Data In |
| Data type | Unstructured |
| Method | Batch |
| Key facts | Ingests unstructured content through MuleSoft Direct path |
| Dev Guide | https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-mulesoft-direct.html |

---

## Connector Classification Summary

| Category | Examples | Direction | Method |
|---|---|---|---|
| Zero Copy Federation | Snowflake, BigQuery, Redshift, Databricks, Iceberg, AWS Glue, watsonx.data | Bidirectional or Data In | Zero Copy |
| Streaming Ingestion | Kinesis, MSK, Ingestion API (streaming mode), Web/Mobile SDKs | Data In | Streaming |
| Bulk Batch | Ingestion API (bulk mode), S3, SFTP, Cloud Storage, 150+ third-party connectors | Data In | Batch |
| Unstructured | S3, Azure Storage, GCS, Box, GitHub, Confluence, SharePoint, Web Crawler/Sitemap, MuleSoft Direct | Data In | Batch |
| Activation (Data Out) | Google Ads, DV360, TikTok, LinkedIn CAPI, Pinterest, SFTP, S3, Azure, GCS | Data Out | Incremental/Batch/Streaming |
| Bidirectional | Snowflake, BigQuery, Redshift, S3, SFTP, Azure Storage, GCS, Google Ads, Meta Ads | Both | Varies |

---

_Total connectors in the catalog: 140+ (excluding Marketing Intelligence).
Source: https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-thirdparty-connectors.html_
