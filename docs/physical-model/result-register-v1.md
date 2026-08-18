# Physical Model Result Register v1

- Status: **CURRENT — BOOTSTRAP**
- Workstream: `feature/physical-model`
- Benchmark execution: **NOT STARTED**
- Technology selection: **NONE**
- This register starts with every executable result at `NOT RUN`.

## Rule

This file records current Physical execution/disposition state. It does not override the Phase-10 benchmark register's candidate definitions or create selection by prose.

```text
NOT RUN != PASS
PREFERRED != SELECTED
```

A result changes only after evidence is remotely written/linked and the corresponding gate is QA-verified.

# Lane P — Primary canonical persistence

## P0 — PostgreSQL hybrid

```text
REGISTERED ROLE
mandatory preferred baseline

EXACT SUBJECT
NOT FROZEN — PM-01

MAPPING
NOT STARTED

HG-01..HG-12
NOT RUN

CORRECTNESS / DESTRUCTIVE
NOT RUN

LOW
NOT RUN

BASE
NOT RUN

HIGH
NOT RUN

RECOVERY / EVOLUTION
NOT RUN

WEIGHTED SCORE
NOT RUN

SENSITIVITY
NOT RUN

CURRENT DISPOSITION
NOT RUN / NOT SELECTED
```

Conditions/caveats: none accepted yet; PM-01 must pin exact version/edition/topology and official evidence.

Evidence: none yet.

## P1 — TypeDB

```text
REGISTERED ROLE
mandatory challenger

EXACT SUBJECT
NOT FROZEN — PM-01

MAPPING
NOT STARTED

HG-01..HG-12
NOT RUN

CORRECTNESS / DESTRUCTIVE
NOT RUN

LOW
NOT RUN

BASE
NOT RUN

HIGH
NOT RUN

RECOVERY / EVOLUTION
NOT RUN

WEIGHTED SCORE
NOT RUN

SENSITIVITY
NOT RUN

CURRENT DISPOSITION
NOT RUN / NOT SELECTED
```

Conditions/caveats: exact TypeDB version/edition/deployment and cluster/HA/backup capability require PM-01 pinning; no generic brand-level maturity claim is accepted.

Evidence: none yet.

# Lane G — Secondary graph / traversal

## G0 — no specialized graph store

```text
SUBJECT
primary-store query/projection baseline after primary mapping exists

EXECUTION
NOT RUN

CG-01..CG-04
NOT RUN where applicable

G-LANE SCORE
NOT RUN

CURRENT DISPOSITION
BASELINE / NOT RUN
```

## G1 — Neo4j

```text
EXACT SUBJECT
NOT FROZEN — only when G lane execution is admitted

EXECUTION
NOT RUN

CG-01..CG-04
NOT RUN

LOW / BASE / HIGH
NOT RUN

G-LANE SCORE
NOT RUN

NET BENEFIT
NOT RUN

CURRENT DISPOSITION
NOT RUN / NOT SELECTED
```

No graph product becomes canonical truth by winning a traversal benchmark.

# Lane S — Search / semantic retrieval

## S0 — structured + lexical/full-text baseline

```text
SUBJECT
accepted primary architecture native/bounded baseline

EXECUTION
NOT RUN

SEARCH CORRECTNESS
NOT RUN

DISCLOSURE / PROPAGATION
NOT RUN

LOW / BASE / HIGH
NOT RUN

CURRENT DISPOSITION
BASELINE / NOT RUN
```

## S1 — pgvector

```text
ADMISSION CONDITION
PostgreSQL present/applicable in accepted benchmark architecture

EXACT SUBJECT
NOT FROZEN

EXECUTION
NOT RUN

CG-01..CG-04
NOT RUN

RECALL / PRECISION
NOT RUN

FILTERED RECALL
NOT RUN

LOW / BASE / HIGH
NOT RUN

CURRENT DISPOSITION
NOT RUN / NOT SELECTED
```

Vector quality is judged after applicable scope/Visibility filtering, not from unfiltered top-k latency alone.

# Lane E/D — Event / document bounded mechanisms

## ED0 — bounded native mechanisms

```text
STATUS
BASELINE CLASS

EXECUTION
NOT RUN / assessed only where Physical scenarios require it
```

## ED-SPECIALIZED

```text
ADMISSION
NONE

CANDIDATE
NONE

STATUS
NOT ADMITTED
```

A named specialized product requires a separate admission record/gate proving a concrete accepted gap or structural benefit.

# Durable-runtime coupling observations

No durable runtime is selected by this workstream bootstrap.

```text
Restate   NOT SELECTED
Temporal  NOT SELECTED
DBOS      NOT SELECTED
```

Physical evidence may change relative infrastructure coupling/operational economics, but persistence benchmark points cannot be awarded to a runtime and runtime preference cannot select primary persistence.

Known Phase-7 current posture to preserve:

```text
DBOS local/bounded Python        SQLite-capable
DBOS production guidance         PostgreSQL-recommended
DBOS distributed multi-server    PostgreSQL-coupled
```

# Solver / AI / provider interaction

Physical tests may need to persist candidate/derived/provider/runtime-related state, but:

```text
solver output != accepted canonical effect
AI eval/result != canonical LifeOS truth
provider revision != MaterialStateRef
runtime workflow completion != Actual automatically
```

No model/provider/solver/runtime product is selected by this register.

# Evidence checkpoints

## PM-00 Bootstrap

```text
PRE-SCOPE
main @ 3de84bb49f9cef30e88e9bde4961ed84335daa79

BRANCH
feature/physical-model

STATUS
IN PROGRESS — final bootstrap QA pending
```

## PM-01 Candidate/environment freeze

```text
STATUS
NOT STARTED
```

## PM-02 Primary mapping

```text
STATUS
NOT STARTED
```

## PM-03 Hard-gate preflight

```text
STATUS
NOT STARTED
```

## PM-04 Harness/fixtures

```text
STATUS
NOT STARTED
```

## PM-05+ Execution

```text
STATUS
NOT STARTED
```

# Recommendation ledger

| Lane | Candidate | Exact subject | Hard-gate result | Score | Sensitivity | Current disposition | Selected? |
|---|---|---|---|---|---|---|---|
| P | PostgreSQL hybrid | NOT FROZEN | NOT RUN | NOT RUN | NOT RUN | NOT RUN | NO |
| P | TypeDB | NOT FROZEN | NOT RUN | NOT RUN | NOT RUN | NOT RUN | NO |
| G | G0 no-specialized-store | future primary-dependent | NOT RUN | NOT RUN | NOT RUN | BASELINE | NO |
| G | Neo4j | NOT FROZEN | NOT RUN | NOT RUN | NOT RUN | NOT RUN | NO |
| S | S0 structured/FTS | future primary-dependent | NOT RUN | NOT RUN | NOT RUN | BASELINE | NO |
| S | pgvector | conditional / NOT FROZEN | NOT RUN | NOT RUN | NOT RUN | NOT RUN | NO |
| E/D | ED0 bounded native | future primary/runtime-dependent | applicable checks NOT RUN | N/A | NOT RUN | BASELINE CLASS | NO |
| E/D | specialized | NONE | N/A | N/A | N/A | NOT ADMITTED | NO |

# Result mutation protocol

Before changing any candidate from `NOT RUN`:

1. identify exact evidence record/path/artifact;
2. verify the candidate subject/version/edition/topology;
3. verify scenario/mapping revision;
4. update only the applicable result fields;
5. preserve unresolved items as `HOLD`/`NOT RUN` rather than inferring completion;
6. remote-read back the register;
7. record checkpoint in `docs/workstreams/physical-model.md`.

Before writing `PREFERRED`, PM-09/10 evidence must exist.

Before writing `SELECTED`, PM-11 explicit selection gate and user approval are mandatory.