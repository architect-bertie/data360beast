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

Target discovery uses the authenticated org API version unless the spec supplies
one explicitly. Data-space discovery must use the current positional
`sf api request rest` command shape:

```bash
sf api request rest --target-org <alias> --method GET /services/data/v<api>/ssot/data-spaces
```

The capability matrix only proves target-org and target data-space reachability.
Specialist adapters must add their own stream, DMO, CI, segment, activation,
search, semantic, automation, or packaging readbacks before a phase is treated
as surface-proven.

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
