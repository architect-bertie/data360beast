# Activation Target Cards

One card per target type. Use for quick classification before implementation.
Source: Official Salesforce Help and community guides.

---

## Marketing Cloud Engagement

| Field | Value |
|---|---|
| Target type | Marketing Cloud |
| Delivery | Shared Data Extension (SDE) in the selected Business Units |
| Setup | Activation Targets tab → New → Marketing Cloud → Name, data space, Business Units |
| Key facts | Segment activation creates an SDE; BU selection filters contacts; name max 128 chars, no special chars, no leading underscore |
| Permissions | Data Cloud Marketing Admin or Data Cloud Marketing Manager |
| Help | https://help.salesforce.com/s/articleView?id=sf.c360_a_create_marketing_cloud_activation_target.htm&type=5 |

---

## Marketing Cloud Personalization (Interaction Studio)

| Field | Value |
|---|---|
| Target type | Marketing Cloud Personalization |
| Delivery | Dataset within a selected Organization |
| Setup | Activation Targets tab → New → MC Personalization → Name, data space, Organization, Dataset |
| Key facts | Organization and Dataset must exist before target creation |
| Help | https://help.salesforce.com/s/articleView?id=sf.c360_a_create_mc_personalization_activation_target.htm&type=5 |

---

## External Activation (Advertising / Social)

| Field | Value |
|---|---|
| Target type | External Activation Platform |
| Platforms | Meta, LinkedIn, Google Ads, Google DV360, Amazon Ads, TikTok, Pinterest, AppExchange partners |
| Delivery | Audience push via platform-specific API (incremental, direct API) |
| Setup | Activation Targets tab → New → External platform → Name, data space, redirect to platform for OAuth → select Account |
| Key facts | One unique platform account per Activation Target; multiple targets per platform allowed; requires accepting platform ToS |
| Permissions | Data Cloud Marketing Admin or Data Cloud Marketing Manager |
| Help | https://help.salesforce.com/s/articleView?id=sf.c360_a_create_external_activation_platform_activation_target.htm&type=5 |

---

## File Storage (S3, SFTP, GCS, Azure)

| Field | Value |
|---|---|
| Target type | Cloud File Storage |
| Platforms | Amazon S3, SFTP, Google Cloud Storage, Microsoft Azure Blob Storage |
| Delivery | CSV, JSON, or Parquet files; metadata file + data files in a segment folder |
| Setup | Activation Targets tab → New → File Storage platform → Name, data space, connector/bucket details |
| Key facts | Default max file 500 MB / 5000 records (splits into multiple files); S3 needs PutObject/GetObject/ListBucket/DeleteObject/GetBucketLocation permissions; SSE-S3 supported for S3 |
| Help | https://help.salesforce.com/s/articleView?id=sf.c360_a_create_cloud_file_storage_activation_target.htm&type=5 |

---

## Data Cloud (Audience DMO)

| Field | Value |
|---|---|
| Target type | Data Cloud |
| Delivery | Writes segment data to an Audience DMO within Data 360 |
| Setup | Activation Targets tab → New → Data Cloud → Name, data space |
| Key facts | No external delivery; useful for query-based access, centralized segment data, later API integration, Flow, or LWC consumption |
| Help | https://help.salesforce.com/s/articleView?id=sf.c360_a_create_dc_audience_dmo_activation_target.htm&type=5 |

---

## B2C Commerce

| Field | Value |
|---|---|
| Target type | B2C Commerce |
| Delivery | Publishes segment data to Commerce Cloud org |
| Setup | Activation Targets tab → New → B2C Commerce → Name, data space, Connector |
| Help | https://help.salesforce.com/s/articleView?id=sf.c360_a_create_commerce_activation_target.htm&type=5 |

---

## Loyalty Cloud

| Field | Value |
|---|---|
| Target type | Data Cloud (Loyalty) |
| Delivery | Publishes segment data to Loyalty Cloud org |
| Setup | Activation Targets tab → New → Data Cloud (Loyalty) → Name, data space, Connector |
| Help | https://help.salesforce.com/s/articleView?id=sf.c360_a_create_audiences_activation_target.htm&type=5 |

---

## Webhook Data Action Target

| Field | Value |
|---|---|
| Target type | Webhook |
| Delivery | HTTP POST with `DataObjectDataChgEvent` payload on DMO/CIO change |
| Setup | Data Action Targets tab → configure endpoint URL + HMACSHA256 secret |
| Key facts | Near-real-time; secret key validation required; rotate keys at least every 12 months (15-min propagation); idempotency and retry logic recommended |
| Help | https://developer.salesforce.com/docs/data/data-cloud-int/references/webhook-data-action-targets |

---

## Activation Process Summary

| Step | Action | Question answered |
|---|---|---|
| 1 | Create Segment | Who is the audience? |
| 2 | Configure Activation Target | Where does it go? |
| 3 | Create Activation on Segment | How is it published? (attributes, schedule, contact points) |
| 4 | Select Activation Membership | Individual or Unified Individual? |
| 5 | Select Contact Points | Which email/phone/address? (Source Priority Order) |
| 6 | Select Additional Attributes | What personalization data to include? |

---

## Source Priority Order (Contact Points)

When multiple contact points exist for a unified profile, Data 360 uses
Source Priority Order to select one for activation:

| Priority type | Meaning |
|---|---|
| Primary | Uses the Primary Flag field mapped in data streams |
| Any | Default fallback — picks from any available source |
| Personal | Uses the For Personal Use field (value = 1) |
| Business | Uses the For Business Use field (value = 1) |

Configure source priority per activation to control which contact point
is delivered to the target system.

---

_Source: Official Salesforce Help.
Activation is separate from segmentation: segmentation gathers all matching
records; activation picks one record per profile based on contact point
priority and publishes to the target._
