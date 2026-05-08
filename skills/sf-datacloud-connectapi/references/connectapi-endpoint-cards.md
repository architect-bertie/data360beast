# Data 360 Connect API Endpoint Cards

Use an official OpenAPI/Swagger file or a user-provided Postman collection as the source of truth and search it before crafting payloads.

```bash
python3 skills/sf-datacloud-connectapi/scripts/data360_accelerator.py search-endpoints \
  --postman path/to/postman_collection.json \
  --query "Data Streams"
```

## Endpoint Families

| Family | Count | Production Use |
|---|---:|---|
| Connections | 23 | Connector discovery, connection create/update/test, schema management. |
| Data Streams | 6 | Stream lifecycle and run operations. |
| Data Lake Objects | 5 | DLO discovery and lifecycle. |
| Data Transforms | 13 | Batch transform lifecycle and run operations. |
| Data Model Objects | 14 | DMO lifecycle, relationships, and mapping-adjacent work. |
| Identity Resolutions | 6 | Ruleset lifecycle and run-now operations. |
| Query Current / V1 / V2 | 7 | SQL query execution, polling, pagination, and row retrieval. |
| Profile | 6 | Profile metadata and record retrieval. |
| Metadata | 6 | Tenant metadata inventory and relationship discovery. |
| Calculated Insights / Insights | 9 | CI lifecycle, insight metadata, and CI query. |
| Data Graphs | 7 | Graph metadata and graph data retrieval. |
| Segments | 10 | Segment lifecycle, publish, count, and member checks. |
| Activation Targets | 4 | Destination auth/config management. |
| Activations | 7 | Activation lifecycle and data retrieval. |
| Data Action Targets | 5 | Platform Event, webhook, and MCE target setup. |
| Data Actions | 2 | Data action lifecycle. |
| Document AI | 9 | Document/unstructured processing configuration. |
| Search Index | 6 | Search index configuration and retrieval setup. |
| Machine Learning | 17 | AI model / ML lifecycle surfaces. |
| Data Spaces | 7 | Data-space discovery and access-aware routing. |
| Data Kits | 3 | Metadata package/data-kit promotion. |
| Data Clean Room | 13 | Collaboration/audience clean-room operations. |
| Private Network Routes | 4 | Private connectivity operations. |
| Universal ID Lookup | 1 | Source-to-unified lookup. |

## Surface Selection

- Use **Connect API** when mixing Data 360 with Salesforce Platform auth, Apex, Flow, Agentforce, or setup metadata.
- Use **Data 360 API / Direct API** when tenant-side read performance matters and the operation is available there.
- Use **Metadata API and data kits** for deployable Data 360 metadata. Keep Data 360 metadata separate from non-Data 360 metadata in packaging.
- Use **OpenAPI/Postman examples** to confirm URL, method, path variables, and response shape before writing code.

## Production Output

For each endpoint used, document:

1. family and exact method/path
2. auth mode
3. data space parameter
4. payload shape
5. response fields consumed
6. retry/pagination behavior
7. verification query or downstream object check
