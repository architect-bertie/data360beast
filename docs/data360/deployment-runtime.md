# Data360 Beast Deployment Runtime

The runtime converts a portable desired-state implementation specification into
a dependency-ordered plan, a local run journal, and target-surface proof.

## Commands

```bash
python3 skills/data360beast/scripts/data360beast.py preflight --spec implementation.json
python3 skills/data360beast/scripts/data360beast.py plan --spec implementation.json
python3 skills/data360beast/scripts/data360beast.py knowledge query --goal "segment activation" --phase act
```

`apply` refuses mutation unless `--execute` is supplied. Production also
requires `--approve-production` and a specification policy that grants the
mutation. Browser-only work is a manual handoff outside a lab environment.

## Portability Contract

Specifications name an org alias and environment but do not contain tokens,
org identifiers, passwords, or source-system credentials. The runtime discovers
the org and data spaces, creates a capability matrix, and records only
sanitized results under `$DATA360BEAST_HOME/runs/`.

## Resource Contract

Each resource has an ID, phase, executor, dependencies, desired state, proof
target, and rollback mode. The planner rejects cycles and unknown dependencies.
Supported portable mutation requests use explicit `sf api request rest` shapes;
all other surfaces remain blocked or manual until an adapter and proof contract
exist.

## Certification

The Beastwear pack is a public support matrix, not evidence of universal target
availability. A path is certified only after repeated synthetic-lab
reproductions, cleanup, public-safe attestation, and target-surface proof.
