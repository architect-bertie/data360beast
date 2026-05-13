# Data Spaces (Detailed Boundary Model)

_Distilled from official Salesforce sources only. Linked from
[../SKILL.md](../SKILL.md)._

<!-- SF_DOC_SYNC_START:data-spaces-detailed -->

**Sources:**
- data.c360_a_data_spaces.htm — About Data Spaces
- data.c360_a_data_spaces_feature_access.htm — Manage Feature Access for Data Space-Aware Features
- data.c360_a_data_access_levels_setting.htm — Manage Data Cloud Data Access Levels
- architect.salesforce.com/docs/architect/fundamentals/guide/data360_security_architecture.html — Data Spaces in security architecture

**Purpose:**
Logical segregation of enterprise data domains, enabling multi-brand,
multi-region, or multi-tenant operation within a single Data 360 instance.
Maps to business domains (Sales, Marketing, Service) or regulatory
boundaries (EU, AMER, APAC).

**Properties:**
- Each data space acts as a virtual boundary for visible data collections.
- Access is explicitly granted; no implicit cross-space visibility.
- Federated ownership: each business unit governs independently while
  maintaining centralized oversight.
- Provides the first layer of governance — structural clarity and
  accountability — before fine-grained ABAC kicks in.

**Feature access in data spaces:**
- Some features are "data-space-aware" (segments, activations, CIs, data
  graphs); others are global.
- Feature permissions inside a data space cannot grant more than the
  permission set's object permissions allow.
- Manage feature access via the Data Space Permissions UI.

**Data access levels:**
- Granular controls: view, edit, manage at object level within a space.
- Required for non-admin profiles to perform any DML.
- Layered with OLS/FLS/RLS for full enforcement.

**Multi-org patterns (Data Cloud One, Companion Org):**
- Data 360 Home Org: holds the canonical Data 360 instance.
- Companion Org: connected Salesforce CRM org consuming Data 360 data.
- Data Cloud One: connect multiple CRM orgs to one Data 360 instance.
- Governance ownership shifts across these patterns — document where
  policy is enforced for each cross-org flow.

<!-- SF_DOC_SYNC_END:data-spaces-detailed -->
