# Data 360 Implementation Foundation

Use this contract before creating connections, streams, mappings, identity
rules, insights, segments, activations, or agent-facing retrieval assets. It
turns implementation orientation into decisions and proof gates without
duplicating the phase-specific specialist skills.

## Outcome And Scope Gate

- Name the business outcome, consuming personas, decision or action, expected
  freshness, and measurable success condition.
- Inventory source systems, data owners, data quality, identity keys, consent,
  contact points, suppression signals, sensitive fields, retention rules, and
  activation destinations.
- Confirm edition, licenses, permissions, expected usage, current limits, data
  spaces, and environment lifecycle before estimating or building.
- Choose the data movement pattern for each source: ingestion, live query,
  accelerated query, file federation, data share, or a justified hybrid.

## Org Topology Gate

- Decide whether the Data 360 home org is an existing Salesforce org or a
  dedicated org. Make the tradeoff explicit: shared platform administration
  and features versus separation of duties and Data 360-only administration.
- Decide whether one Data 360 instance can satisfy the organization's control,
  residency, data-model, testing, and growth requirements. Do not assume that
  centralization is correct merely because multiple source orgs can connect.
- For multi-org designs, distinguish the home org, each companion org, the
  standard Salesforce CRM connection created with a companion connection,
  shared data spaces, metadata visibility, user permissions, and connection
  health.
- Record the hosting region and cross-region source/data-transfer assumptions.
  Legal and policy review owns residency decisions; technical connectivity is
  not residency approval.

## Ethical Data Gate

- Record the permitted purpose and customer value for every sensitive or
  person-level data family.
- Collect and retain only the attributes needed for the approved outcome.
- Treat preference, consent, suppression, and deletion behavior as executable
  requirements that must survive identity resolution and activation.
- Classify sensitive data, define protected user cohorts, and test masking and
  access with non-admin users on every consuming surface.
- For activation and sharing partners, document custody, reuse, retention,
  deletion, and onward-transfer obligations before enabling delivery.

## Sandbox And Promotion Gate

- Data 360 sandboxes contain metadata, not replicated production Data 360
  records. Seed representative synthetic or approved test data and prove the
  expected DLO, DMO, identity, insight, segment, and activation behavior there.
- Complete Data 360 provisioning in the sandbox before enabling dependent
  Agentforce or Einstein features.
- Treat source credentials, connector authorization, data-space assignments,
  and target authorization as environment-specific. A successful metadata
  deployment does not prove those runtime dependencies.
- Package supported Data 360 metadata with data kits, validate dependencies in
  the target environment, reauthorize connectors and targets, and repeat the
  phase readbacks after deployment.
- Data Cloud One sandbox topology has additional ordering and connectivity
  restrictions. In particular, do not design a companion connection between a
  sandbox org and a production org.

## Implementation Proof Chain

1. **Connect:** connector metadata, source eligibility, authentication, object
   discovery, and source-side grants are proven.
2. **Prepare:** stream or federation definition, DLO visibility, refresh or
   acceleration behavior, counts, freshness, and rejected records are proven.
3. **Harmonize:** grain, keys, mappings, relationships, identity job completion,
   unified outputs, and data-space access are proven.
4. **Retrieve and insight:** query semantics, joins, metric grain, insight run
   completion, and materialized outputs are proven independently.
5. **Segment and act:** query expectation, segment count, publish state,
   activation configuration, delivery state, and destination readback are
   separate proof gates.
6. **Operate:** monitoring, usage, policy behavior, retention, environment
   promotion, and rollback ownership are documented.

## Doc-Synced Evidence

<!-- SF_DOC_SYNC_START:implementation-foundation -->
### Implementation foundation evidence

_Auto-synced from the local sf-docs cached Salesforce Help export (official docs only)._

**Sources (sf-docs cached Help):**
- data.c360_a_product_considerations.htm — Get Started with Data 360
- data.c360_a_data_cloud_architecture_strategy.htm — Data 360 Architecture Strategy
- data.c360_a_data_gov_capabilities.htm — Data Governance in Data 360
- data.c360_a_data_cloud_sandbox_create.htm — Create a Data 360 Sandbox
- data.c360_a_data_cloud_one_sandboxes.htm — Considerations for Data Cloud One in a Sandbox Org
- data.c360_a_companion_connections.htm — Data Cloud One Companion Connections

**Source fingerprint:** `8a513361822d69f4f59e4a20`

**Notes:**
- Choose business outcomes, source/data strategy, users, permissions, limits, and topology before asset creation.
- Treat home-org placement, instance count, control, growth, region, and residency as explicit architecture decisions.
- In multi-org designs, distinguish standard CRM connections from Data Cloud One companion connections and prove shared data spaces, metadata visibility, permissions, and health.
- Apply purpose limitation, data minimization, sensitivity handling, preference/consent enforcement, and partner custody review as implementation gates.
- Data 360 sandboxes receive metadata rather than replicated production Data 360 data; provision the sandbox, seed approved test data, reauthorize environment-specific integrations, and repeat runtime readbacks after deployment.
- Respect Data Cloud One sandbox ordering and topology restrictions, including the prohibition on connecting a sandbox org to a production org.

<!-- SF_DOC_SYNC_END:implementation-foundation -->

## Routing

- Cross-phase implementation: [`sf-datacloud`](../../skills/sf-datacloud/SKILL.md)
- Interoperability choice: [`interoperability-decision-map.md`](interoperability-decision-map.md)
- Governance and data spaces: [`sf-datacloud-governance`](../../skills/sf-datacloud-governance/SKILL.md)
- Packaging and promotion: [`develop-package-deployment-matrix.md`](develop-package-deployment-matrix.md)
- Phase readbacks: [`phase-proof-matrix.json`](../phase-proof-matrix.json)
- Distilled field evidence: [`proof-ledger.md`](../proof-ledger.md)
