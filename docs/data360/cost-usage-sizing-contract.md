# Data 360 Cost And Usage Sizing Contract

Use this contract before recommending a Data 360 architecture with material
ingestion, query, insight, segment, activation, RAG, automation, or AI-model
usage. It is a design gate, not a price calculator. Current Salesforce limits,
Digital Wallet data, contracts, and Account Executive guidance remain the
source of truth for billable quantities.

## Source Order

1. Current Data 360 Limits and Guidelines.
2. Data Services Billable Usage Types for Data 360 when the limits page routes
   there.
3. Org Digital Wallet, contract, or Account Executive confirmation.
4. Target-org telemetry from the authorized environment.
5. Legacy Customer Data Platform limits only for explicit CDP scope or labeled
   comparison.

## Required Inputs

| Input | Why It Matters |
| --- | --- |
| Business outcome | Prevents sizing a capability that does not serve the use case. |
| Data spaces | Affects visibility, duplication, data-share strategy, and proof. |
| Source systems | Drives connector, ingest, federation, and source-side cost. |
| Record volume and growth | Drives storage, ingest, query, refresh, and identity costs. |
| Refresh cadence | Batch, streaming, real-time, and reindexing cadences meter differently. |
| Query workload | Interactive, batch, API, report, segment, RAG, and CI workloads stress different paths. |
| Identity and merge rate | Influences profile count, relationship complexity, and validation load. |
| Activation destinations | Can require add-ons, destination limits, and delivery proof. |
| AI/RAG workload | Embedding, indexing, retrieval, prompt, and intelligent-processing costs need separate gates. |
| Environment lifecycle | Lab, sandbox, UAT, and production all consume differently. |

## Phase Cost Gates

| Phase | Cost/Usage Questions | Proof Habit |
| --- | --- | --- |
| Connect | Is this ingestion, live query, accelerated query, file federation, sharing, or hybrid? | Connector type, source-side compute assumption, connection status. |
| Prepare | How many rows/files/objects refresh, and how often? | Stream run status, DLO row count, failed-row sample. |
| Harmonize | How many records map and how many identity candidates are evaluated? | Mapping status, identity run status/counts, relationship metadata. |
| Govern | Do policies require duplicate spaces, masking, or non-admin access tests? | Permission/policy readback and non-admin proof. |
| Retrieve | How often do humans, agents, APIs, and jobs query the data? | Query sample, row limit, selected fields, data-space proof. |
| Insight | How often do CIs run, and at what grain? | Syntax check, run status, output CIO row count. |
| Semantic/Analytics | Are dashboards cached, refreshed, or queried live? | Metric readback, dashboard refresh, governed-user view. |
| AI/Search | How many documents/chunks/indexes/retrieval calls? | Source count, chunk count, retriever result, citation field proof. |
| Segment | How often are audiences counted, refreshed, and published? | Segment status, count, publish history. |
| Act/Automation | How many payloads leave Data 360 and where? | Target readback, run history, destination delivery proof. |
| Develop/Package | How many environments replay setup and consume test usage? | Data kit membership, deploy validation, cleanup proof. |

## Databricks And Zero-Copy Cost Gates

For Databricks or other lakehouse federation, separate Data 360 consumption
from source-side consumption before recommending a pattern:

- Live query can spend source-side SQL warehouse or cluster compute on every
  Data 360 workflow that touches the external object.
- Acceleration can reduce repeated source scans, but it creates refresh,
  storage, and staleness decisions in Data 360.
- File federation cost depends on table format, partition pruning, storage
  region, object-store access, and Data 360 scan behavior.
- Private networking or Private Connect can add network-transfer consumption
  separately from row-accessed or query usage.
- Allowlist success proves reachability only; cost proof still needs query
  shape, selected fields, predicate pushdown, row counts, refresh frequency, and
  source-side warehouse telemetry.

## Output Shape

For customer-facing estimates, report:

```text
Scope
Assumptions
Billable usage families to validate
Hard limits and soft guidelines
Workload drivers by phase
Low/medium/high sensitivity risks
Telemetry or Digital Wallet proof needed
Design changes that reduce usage
```

## Usage Reduction Rules

- Filter and project early; query only required fields.
- Ingest canonical governed cores; federate exploratory or high-volume edges
  when source governance and latency are acceptable.
- Aggregate before ingest when raw event detail is not required downstream.
- Avoid duplicate indexes, duplicate chunks, and category-only vector content.
- Use smaller proof datasets in labs and sandboxes.
- Separate preview, syntax, publish, count, activation, and delivery proof so
  retries do not multiply unnecessary work.
- Do not use external activation or RAG reindexing as a debugging loop without
  a bounded test cohort.

## Machine-Readable Scenario Input

`tools/data360_cost_usage_estimator.py` accepts a JSON file with this shape:

```json
{
  "name": "beastwear-rag-segment-activation",
  "dataSpaces": 2,
  "sourceSystems": 5,
  "monthlyRowsIngested": 5000000,
  "monthlyQueries": 25000,
  "monthlyInsightRuns": 300,
  "monthlySegmentPublishes": 40,
  "monthlyActivationPayloads": 1000000,
  "ragDocuments": 20000,
  "ragAverageChunksPerDocument": 8,
  "environments": 3
}
```

The script emits risk bands and proof questions. It does not emit credit or
dollar values.
