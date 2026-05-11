# Beast Preflight

Run this preflight before non-trivial Salesforce Data 360 work. The goal is to
make the agent name its operating envelope before it gives advice, writes a
payload, or mutates an org.

## Required Envelope

Capture these facts when they are available:

| Field | Why It Matters |
| --- | --- |
| Business goal | Keeps routing tied to the outcome, not just the nearest API. |
| Target org or alias | Prevents accidental reliance on global CLI state. |
| API version | Data 360 API shapes and data-space parameters can be versioned. |
| Data space | Data space affects visibility, names, tokens, API parameters, and proof. |
| User persona | Admin visibility is not proof of governed runtime behavior. |
| Asset lifecycle | Disposable lab asset, sandbox implementation, or production change. |
| Authorization boundary | Docs-only, metadata read, live validation, create/update, or production mutation. |

If a field is unknown and the task can still proceed, state the assumption and
label downstream proof as `inferred` or `docs-unverified` as appropriate.

## Tool Inventory

Check available proof tools before choosing the path:

| Tool Or Source | Use For | If Missing |
| --- | --- | --- |
| User-provided files | Org-specific schemas, OpenAPI, examples, exports | Ask only if required; otherwise label as inferred. |
| `sf-docs` | Current official Help and Developer docs | Use indexed pages to locate sources and label docs as not freshly fetched. |
| OpenAPI or Swagger | Method, path, params, body, response, version mechanics | Avoid exact payload claims or mark path/schema as unverified. |
| `data360` MCP | Authorized live Data 360 operations | Use `sf` CLI or explain that live proof is unavailable. |
| `sf` CLI auth | Org metadata, API requests, deployment/readback | Do not imply target-org validation. |
| Specialist skill | Phase-specific guardrails and failure modes | Fall back to `data360beast` and the proof matrix. |

## Proof Plan

Before output, choose one proof target:

- `docs-only guidance`: official docs or OpenAPI support, no org proof.
- `payload generation`: exact method/path/schema plus smallest valid payload.
- `metadata discovery`: object, field, data space, and relationship readback.
- `live validation`: returned ID, status, count, metadata, data space, or query result.
- `troubleshooting`: symptom, surface, likely layer, proof probe, and next branch.
- `customer explanation`: recommendation, proof level, caveats, and next proof step.

## Mutation Gate

Do not create, update, publish, activate, deploy, or delete assets unless the
user has authorized that class of action. For approved live work, prefer
disposable lab assets and read back by returned ID before claiming success.

Production-sensitive changes need an explicit callout when they touch:

- production data spaces or activations
- external destinations or webhooks
- permissions, masking, tags, classifications, or data access policies
- customer data, PII, raw contact fields, or entitlement fields
- high-volume ingest, refresh cadence, or metered query workloads

## Preflight Line

For substantial answers, include or internally satisfy this line:

```text
Preflight: org=<alias|none>, api=<version|unknown>, data space=<name|unknown>, tools=<sf-docs:data360:sf:openapi>, proof=<target>, confidence=<documented|tested|inferred>
```

If the final answer is intentionally brief, preserve the same facts in the
answer body instead of printing the line mechanically.
