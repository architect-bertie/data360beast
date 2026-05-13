# Govern and Secure Overview

_Distilled from official Salesforce sources only. Linked from
[../SKILL.md](../SKILL.md)._

<!-- SF_DOC_SYNC_START:govern-and-secure-overview -->

**Sources:**
- data.c360_a_data_gov_capabilities.htm — Data Governance in Data 360
- data.c360_a_getting_started_data_gov.htm — Get Started with Data Governance
- architect.salesforce.com/docs/architect/fundamentals/guide/data360_security_architecture.html — Data 360 Security Architecture (official Architect Guide)
- trailhead.salesforce.com/content/learn/modules/data-cloud-govern-and-secure (official Trailhead)

**Three pillars of Data 360 Governance:**
1. **AI-powered tagging and classification** — organize and identify data
   types across structured and unstructured sources.
2. **Policy-based governance** — ABAC for fine-grained data access.
3. **Data security** — Hyperforce-inherited platform security plus
   customer-managed configuration (IAM, MFA, SSO, audit, masking).

**Shared responsibility model:**
- **Salesforce** secures the platform (Hyperforce on AWS, ISO 27001, SOC
  1/2/3, GDPR readiness, TLS 1.2+, AES-256 at rest, DDoS, patching).
- **Customer** secures data, configurations, and operational processes
  (IAM, governance, integration security, monitoring).

**Secure-by-default (Day 0):**
- New Data 360 orgs start in "Deny All" — zero implicit access.
- All permissions must be explicitly granted.
- Legacy "Allow All" orgs require manual tightening.
- This enforces least privilege by design.

**Identity layer:**
- Federated authentication via SAML 2.0, OIDC, or SCIM with IdPs (Entra
  ID, Okta, Ping Identity).
- SSO + MFA + conditional/risk-based access via the IdP.
- SCIM provisioning for lifecycle: joiners, movers, leavers automatic.

**Standard permission sets (use these, not clones):**

| Role | Primary Responsibility | Access Boundary |
|---|---|---|
| System Administrator | Setup, provisioning, configuration | No access to underlying datasets |
| Data 360 Architect | Ingestion, transforms, identity resolution, modeling | Cannot perform activation |
| Data 360 Activation Manager | Segments, channels, activation | View-only on data models |
| Data 360 User | Consumes analytics and insights | Read-only |
| Data 360 One User | Cross-org access via Companion Org | Governed by shared-space scope |

Standard permission sets auto-update with each release; custom clones do not.

<!-- SF_DOC_SYNC_END:govern-and-secure-overview -->
