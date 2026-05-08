# Data 360 Policy Enforcement Matrix

Use this reference when debugging why a Data 360 object, process definition, query, dashboard, graph, segment, activation, or flow is visible but fails at runtime.

## Access Layers

- Data spaces: broad object/data boundary.
- Permission sets: feature access, data space assignment, object/field access for RBAC.
- Custom permissions: user attributes for ABAC policies.
- Tags and classifications: data attributes for ABAC, masking, and data access policies.
- Data access policies: OLS, FLS, RLS.
- Dynamic masking policies: redaction, nullification, datetime rounding, numeric rounding.

## General Query Behavior

- Object access is evaluated by policy.
- Field access is evaluated at query time.
- `SELECT *` can omit fields the user cannot access.
- Explicit references to inaccessible fields fail.
- Querying an inaccessible object fails.
- View All/Modify All object permissions do not override query policy enforcement in the query path.
- Users can create or edit masked fields when they have object/field access; masking affects retrieval.

## Data Explorer and Profile Explorer

- Metadata can appear to admins or users with broad permissions, but query/runtime access can still fail.
- FLS on primary key or fully qualified key fields can fail queries even when the key is not selected.
- Profile Explorer searches on fields restricted by RLS can return no visible data.
- Data Explorer has stricter graph and CI visibility exceptions than raw query APIs.

## Calculated Insights

- Creating a CI can show metadata to broad-permission users, but save/validate fails if referenced objects or fields are blocked.
- Manually referenced restricted fields fail validation.
- RLS is not enforced when creating calculated insights.
- Users must have access to the underlying DMO, DLO, and CIO to view the CI process definition.
- Tags can propagate from DMO to CIO when dimension fields exactly match source fields.
- Formula-derived dimensions may not automatically inherit tags.
- FLS on a CI dimension can cause aggregatable metrics to roll up and non-aggregatable metrics to be restricted.

## Segmentation

- Object and field enforcement applies while creating segments.
- Segment creation can fail if the user lacks access to the Segment On DMO.
- RLS is not enforced during segment creation, so created segments can include records that a user could not query directly.
- Segment definitions and waterfall references can be visible in limited ways while underlying definitions remain restricted.
- Activations shown on a segment record are filtered by access to related dependent objects.

## Data Graphs

- Creating a graph requires access to the primary DMO and required date fields for engagement recency logic.
- Querying a graph requires access to ID and value DMOs and their fields; check current org behavior for underlying DMO/CIO enforcement.
- Consuming graph definitions can require access to ID, value, fragment DMOs, and underlying inputs.
- If a field used in a graph is governed by masking or deny FLS, the graph can be hidden or inaccessible.
- Draft graphs can appear even when underlying generated objects do not exist yet, then fail when opened.

## Data Streams, DLOs, DMOs, and Transforms

- Data stream deployments can create outputs the initiating user cannot view afterward.
- Users can only select permitted DLOs, DMOs, fields, and relationships.
- After creating a DLO or DMO, users still need access to view it.
- Transforms enforce object and field access in authoring and preview.
- Transform preview requires consistent data space selection across joined inputs.
- RLS can affect transform preview but not runtime execution, so preview counts can differ from processed counts.
- Manually referenced restricted fields in transform expressions or SQL fail validation.

## Search Indexes and Unstructured Retrieval

- Search index creation enforces object and field access.
- Users generally need access to all DMOs in the relationship path.
- Users must have access to search, index, chunk, and attachment DMOs.
- Retriever or Agentforce consumers must be tested with the actual user profile and content-access policies.

## Identity Resolution

- Users must have access to unified result and unified link DMOs in addition to DMOs used by the identity rule to consume identity process definitions.
- Governance can make generated unified objects invisible even when a run succeeds.
- Retag generated identity outputs or rely on verified propagation before downstream use.

## Activation, Data Actions, and Flows

- Activation creation can fail if the creator lacks access to the Segment On primary key.
- Activation consumption can require access to all underlying CIOs, DMOs, graph entities, or segment inputs.
- Data actions are visible only when users can access all related objects.
- Data action target lists filter out inaccessible actions.
- Scheduled high-scale flows enforce policies captured at flow creation, but RLS is not enforced on scheduled trigger execution.
- Copy Field Enrichment runs in system mode and then depends on CRM security.

## Reports, Dashboards, Semantic Models, and Core Apps

- Runtime policies are enforced even when a builder can see metadata.
- Report/dashboard policy changes may require refresh or cache clearing.
- Semantic model metrics must be validated with a non-admin user.
- Related lists honor policies at consumption.
- Copy Field Enrichment copies records in system mode; secure target CRM fields/objects separately.

## Implementation Checklist

1. Confirm Enhanced Security Data Spaces.
2. Identify user cohorts and custom permissions.
3. Define tag/classification taxonomy.
4. Tag object-level domains and field-level sensitive attributes.
5. Protect sensitive fields with FLS or masking.
6. Leave keys and relationship fields unmasked unless proven safe.
7. Add RLS only where row filtering is actually enforced for the target path.
8. Validate every target surface with a non-admin user.
9. Retag generated objects and process outputs.
10. Document exceptions where creation/runtime runs in system context.
