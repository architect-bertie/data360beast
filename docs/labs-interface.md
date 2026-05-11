# Data360 Beast Labs Interface

[`data360beast-labs`](https://github.com/architect-bertie/data360beast-labs) is
the proving ground for Data360 Beast. This repository stays focused on the
operating model; Labs owns scenario-rich experimentation.

## Repository Boundary

| Need | Use | Output |
| --- | --- | --- |
| Choose the right Data 360 phase, source, proof, or confidence label | `data360beast` | Operating guidance, proof target, specialist routing |
| Find public-safe tested behavior | `data360beast` | Proof ledger entry |
| Simulate a full RAG, CDP, segment, activation, or analytics scenario | `data360beast-labs` | Scenario assets, payloads, traces, readbacks |
| Explore a risky payload or ambiguous API surface | `data360beast-labs` | Candidate evidence or failure trace |
| Promote a stable lesson | Both | Labs evidence distilled into Beast proof ledger |

## Promotion Pipeline

```text
Labs scenario -> candidate evidence -> proof ledger -> operating-model update -> future cookbook pattern
```

Labs material can be promoted only when it has:

- official docs or OpenAPI source
- exact surface and phase
- data-space assumptions
- public-safe proof/readback
- caveat or failure mode
- confidence label
- Labs reference

## What Stays In Labs

- golden-path walkthroughs
- synthetic customer journeys
- end-to-end implementation sequences
- raw payload drafts
- run traces and screenshots
- failure investigations
- candidate cookbook drafts

## What Can Enter Beast

- distilled proof entries
- operating-model updates
- specialist skill caveats
- source hierarchy improvements
- validation and promotion rules

Do not commit Labs artifacts, raw org metadata, customer data, credentials, or
bulky payload dumps into Beast.
