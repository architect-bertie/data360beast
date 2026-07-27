# Data 360 Developer Guide Learning Map

This is a local synthesis index for Data360 Beast skill updates. It is derived from official Salesforce Developer docs and should be refreshed before publishing durable guidance.

## Crawl Scope

- Source: https://developer.salesforce.com/docs/data/data-cloud-dev/guide/dc-get-started.html
- Pages indexed: 24
- Source type: developer.salesforce.com guide pages
- Public repo rule: summarize learnings; do not publish raw extracted pages.

## Skill Update Candidates

- `sf-datacloud`: strengthen the end-to-end development lifecycle routing: architecture, object model, API category, environments, lifecycle, packages/data kits, cost, and optimization.
- `sf-datacloud-connectapi`: split API guidance by integration, custom app development, Postman exploration, API end-of-life, and direct developer resources.
- `sf-datacloud-metadata-agentic` and `sf-datacloud-connectapi`: add metadata component cheat-sheet awareness for Data 360 promotion and packaging.
- `sf-deploy` adjacent guidance: Data 360 development uses sandbox/second-org/partner-org patterns plus data kits and 2GP, not a direct copy of standard Platform scratch-org assumptions.
- `sf-datacloud-governance` and `sf-flex-estimator`: incorporate Cost and Usage plus Best Practices for Optimizing Usage as first-class validation gates.

## Page Map

- Get Started with Data 360 Development: With Data 360, you can consolidate and process large volumes of data from various sources and integrate it with Salesforce CRM data, avoiding data silos. Data 360 uses a lakehouse to store your data and connect it with the Salesforce Platform. You can process data at scale, query the data, and create insights from billions of records. Customer data is unified so that you can create rich insights for customer profiles.
- Quick Start: Use this section to understand the prerequisites and steps for integrating with Data 360 APIs.
- Data 360 Architecture: Data 360’s architecture is designed to ingest, process, unify, and activate customer data from various sources. It encompasses several key capabilities, forming a comprehensive platform for managing customer experiences.
- Data 360 Features Brief Overview: If you’re new to Data 360, this section provides a brief overview of what Data 360 is used for. It also provides resources so that you can learn more about Data 360.
- Object Model in Data 360: The Customer 360 Data Model includes different types of data objects.
- Data 360 Development Cycle: Use APIs and SDKs to integrate data, query data, and manipulate calculated insights and profiles.
- Data 360 Data- and Development-Related Jobs: Planning your data strategy and importing and mapping data are part of the prerequisite tasks that you perform before you can create insights and build custom apps. Each of these phases require a different job role.
- Differences Between Developing Apps on Data 360 and the Salesforce Platform: Check out the tools and APIs that are available for custom app development in Data 360, and compare them to those available in the Salesforce Platform.
- Data 360 APIs and SDKs By Category: Check out the various APIs and SDKs that you can use for Data 360, organized by category.
- Data Integration: Learn about the APIs and SDKs available for data integration.
- Custom App Development: Learn about the various APIs available for custom app development.
- Make Data 360 REST API Calls with Postman: Watch the video series to see how to call Data 360 APIs and Data 360 Connect APIs to query data with Postman.
- API End-of-Life Policy: See which REST API versions are supported, unsupported, or unavailable.
- Additional Developer Resources for Data 360: In addition to the resources documented in this guide, there are additional Salesforce REST API resources and metadata types to use when you work with Data 360.
- Data 360 Development Environments: Learn about the development environments that are available for Salesforce partners and customer developers.
- App Development Lifecycle: The app development lifecycle includes planning and gathering requirements, creating the app, testing the app, making iterative changes to fix issues, and performing user-acceptance testing as a final test. The final step for an app developed in-house is the app’s release to production. The final step for an app developed by a Salesforce partner is app distribution to other Data 360 customers who purchase the app.
- Packages and Data Kits: A package is a container to which you can add metadata components. It holds the set of related features, customizations, and schema that comprise your app. When packaging Data 360 metadata, you must add the metadata to a data kit, and then add the data kit to the package. Data kits streamline the package creation and installation process.
- Workflow for Data 360 Second-Generation Managed Packages: Second-generation managed packaging (managed 2GP) for Data 360 is a way for AgentExchange partners to develop, distribute, and manage their Data 360 apps and metadata. You can use managed 2GP packaging to organize your source data, build small modular packages, integrate with your version control system, and better utilize your custom Apex code. To learn more about when to use a 2GP packaging, see Why Switch to Second-Generation Managed Packaging?
- Deploy Data Kit Components by Using Deploy Data Kit Components Flow: Deploy all standard data kit components sequentially to a target org using the Deploy Data Kit Components flow.
- Use CLI to Deploy Changes from a Sandbox to Data 360: As a Salesforce developer, you can move your Data 360 metadata and process definitions for Data 360 features between sandbox orgs or between production orgs. To accomplish this, you use a temporary sandbox org that has Data 360 enabled and provisioned.
- Use the Connect REST API to Deploy Data 360 Data Kits: Use the deploy data kit components Connect REST API endpoint to programmatically deploy components from a specific data kit to a Data 360 instance. The Connect API offers a seamless, asynchronous deployment process for both standard and DevOps data kits. This API replaces the legacy, flow-based single-click deploy method.
- Metadata Components for Data 360 Cheat Sheet: This cheat sheet lists the available metadata components that you can package for each feature set in Data 360.
- Cost and Usage: Your use of certain Data 360 features is metered and results in consumption of credits.
- Best Practices for Optimizing Usage: To stay within your consumption credits, follow best practices to optimize your service and data usage.

## Frequent Headings

- See Also: 7
- Before You Begin: 2
- 1. Create a Salesforce DX Project: 1
- 1. Create a Salesforce DX Project with Manifest: 1
- 2. Authorize Sandbox Org and Production Org: 1
- 2. Create a Scratch Org: 1
- 3. Create a Data Space in the Sandbox Org and Production Org: 1
- 3. Create a Standard Data Kit: 1
- 4. Create a DevOps Data Kit: 1
- 4. Retrieve the Data Kit Metadata Into the Project: 1
- 5. Deploy and Test the Data Kit Metadata in a Scratch Org: 1
- 5. Download the Manifest.XML File: 1
- 6. Package the App: 1
- 6. Retrieve the DevOps Data Kit Metadata: 1
- 7. Deploy the DevOps Data Kit Metadata to the Production Org: 1
- 8. Resolve Deployment Failures: 1
- Accessing Unified Data and Calculated Insights in Data 360: 1
- Activation Platform: 1
- Additional Developer Resources for Data 360: 1
- Amazon S3 Data Stream: 1
- API End-of-Life Policy: 1
- APIs at a Glance: 1
- App Development Lifecycle: 1
- App Development Lifecycle Model for Customer Developers: 1
- App Development Lifecycle Model for Salesforce Partners: 1
- Authenticate to the Data 360 Tenant: 1
- Authenticate to the Salesforce Platform: 1
- Authentication: 1
- Authorization for Data 360 API for the Data Cloud Tenant: 1
- Available Data 360 Components in Data Kits: 1
