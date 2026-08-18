# Physical Model Result Register v1

- Status: **CURRENT — PM-09 COMPLETE / PM-10 NEXT**
- Workstream: `feature/physical-model`
- Primary finalists: **PostgreSQL 18.4 + TypeDB CE 3.12.3**
- Deferred primary challengers: **XTDB 2.1.0 + SurrealDB Community 3.2.3 — NOT REJECTED**
- Current evidence-score leader: **PostgreSQL 18.4**
- Evidence-weighted score: **PostgreSQL 89.25 / TypeDB 80.00**
- Ranking sensitivity: **ROBUST / NOT SENSITIVITY-DEPENDENT**
- Direct execution: **NOT STARTED**
- Verified-run benchmark score: **NOT AVAILABLE**
- Preferred: **NONE**
- Selected: **NONE**

## Result-language rule

```text
OFFICIAL CLAIM != DIRECT EXECUTION
PUBLIC BENCHMARK != LIFEOS BENCHMARK
EVIDENCE-QUALIFIED != DIRECT PASS
EVIDENCE-WEIGHTED SCORE != VERIFIED-RUN SCORE
ADMIT != SELECTED
FINALIST != PREFERRED
PREFERRED != SELECTED
DEFER != REJECT
SECONDARY != CANONICAL
LOCAL != CANONICAL
NOT RUN != PASS
```

## Phase state

```text
PM-00   QA PASS
PM-01   PASS-CONDITIONAL
PM-02   PRIMARY MAPPING COMPLETE
PM-03   STATIC PREFLIGHT COMPLETE / 0 STATIC REJECTS
PM-04A  EVIDENCE SUFFICIENCY COMPLETE / 48 OF 48 CELLS
PM-04B  NOT ADMITTED
PM-05   CORRECTNESS/DESTRUCTIVE EVIDENCE QUALIFICATION COMPLETE
PM-06   SCALE/PERFORMANCE EVIDENCE QUALIFICATION COMPLETE
PM-07   RECOVERY/EVOLUTION/FAILURE EVIDENCE QUALIFICATION COMPLETE
PM-08   SECONDARY/SPECIALIST LANE QUALIFICATION COMPLETE
PM-09   EVIDENCE-WEIGHTED SCORING + SENSITIVITY COMPLETE
PM-10   NEXT
PM-11+  NOT STARTED
```

## Primary finalist state

### P0 PostgreSQL 18.4

```text
PM-05
FINALIST

PM-06
SCALE/PERFORMANCE VIABLE / HIGH CONFIDENCE

PM-07
RECOVERY/EVOLUTION/OPERATIONS MATERIAL ADVANTAGE

PM-08
NATIVE FTS + CONDITIONAL PGVECTOR CONSOLIDATION ADVANTAGE

PM-09
EVIDENCE-WEIGHTED SCORE 89.25 / 100
ROBUST LEADER
ADVANCE PM-10

PREFERRED
NONE

SELECTED
NONE
```

### P1 TypeDB CE 3.12.3

```text
PM-05
FINALIST / PRINCIPAL SEMANTIC CHALLENGER

PM-06
SCALE/PERFORMANCE VIABLE / MEDIUM-HIGH CONFIDENCE

PM-07
RECOVERY/EVOLUTION VIABLE / HIGHER SELF-HOSTED OPERATIONS COST

PM-08
SEMANTIC ADVANTAGE PRESERVED / EXTERNAL SEARCH-VECTOR SPECIALIST MORE LIKELY

PM-09
EVIDENCE-WEIGHTED SCORE 80.00 / 100
NO ACCEPTED SENSITIVITY REVERSAL
ADVANCE PM-10 COMPARATIVE RECORD

PREFERRED
NONE

SELECTED
NONE
```

### Deferred / not rejected

```text
P2 XTDB 2.1.0
DEFER / NOT REJECTED
reopen on decision-dominant bitemporal need or material capability change

P3 SurrealDB Community 3.2.3
DEFER / NOT REJECTED
reopen on decision-dominant multimodel consolidation or material capability change
```

## Direct execution truth

```text
P0 HG-01..HG-12       NOT RUN
P1 HG-01..HG-12       NOT RUN
P2 HG-01..HG-12       NOT RUN
P3 HG-01..HG-12       NOT RUN

DIRECT HG PASS         0
DATABASE DEPLOYMENT    NOT STARTED
HARNESS                 NOT STARTED
LOW/BASE/HIGH           NOT RUN
RESTORE                  NOT RUN
MIGRATION                NOT RUN
FAILURE INJECTION        NOT RUN
GRAPH/SEARCH/VECTOR      NOT RUN
SQLITE                    NOT RUN
BENCHMARK HOST           HOLD / DORMANT
VERIFIED-RUN SCORE       NOT AVAILABLE
```

No PM-09 number may be cited as evidence that a direct hard gate or benchmark tier ran.

## Phase-10 reconciliation

The original Phase-10 execution ledger remains intact. PM-09 adds a second decision ledger:

```text
VERIFIED-RUN BENCHMARK SCORE
requires direct applicable hard-gate PASS + direct artifacts

EVIDENCE-WEIGHTED DECISION SCORE
allowed only after evidence exhaustion and 0 ranking-critical execution-worthy gaps
```

The 100-point dimensions and weights are unchanged.

## PM-09 base score

| Dimension | Weight | PostgreSQL | TypeDB |
|---|---:|---:|---:|
| Semantic mapping simplicity/evolvability | 20 | 8.5 | **9.5** |
| Transaction/concurrency ergonomics | 15 | **9.5** | 7.0 |
| Query/report/traversal | 15 | **9.0** | 8.5 |
| History/current efficiency | 10 | 8.5 | 8.5 |
| Operations/backup/restore/HA | 15 | **9.5** | 6.5 |
| Schema evolution/migration | 10 | **9.0** | 8.0 |
| Performance/resource efficiency | 10 | 8.0 | 8.0 |
| Python/tooling/cost/exit | 5 | **9.5** | 7.0 |
| **TOTAL** | **100** | **89.25** | **80.00** |

Performance remains tied deliberately because no direct LifeOS LOW/BASE/HIGH run exists.

## PM-09 sensitivity

```text
S0 Phase-10 base
PostgreSQL 89.25 / TypeDB 80.00 / PG +9.25

S1 semantic-heavy
PostgreSQL 88.75 / TypeDB 83.00 / PG +5.75

S2 early single-node / semantic-friendly
PostgreSQL 88.75 / TypeDB 81.50 / PG +7.25

S3 operations/recovery-heavy
PostgreSQL 90.00 / TypeDB 77.50 / PG +12.50

S4 strongly TypeDB-friendly accepted stress
PostgreSQL 88.00 / TypeDB 85.25 / PG +2.75
```

Verdict:

```text
RANKING ROBUST
SENSITIVITY-DEPENDENT NO
PERFORMANCE-DEPENDENT NO
```

Adversarial boundary only:

```text
semantic weight 50%
PostgreSQL 87.375
TypeDB      87.500
TypeDB +0.125
```

This is not an accepted LifeOS weighting because it suppresses consistency/recovery/evolution/tooling priorities.

Keeping the seven non-semantic weights proportional to Phase-10, TypeDB reaches break-even only when semantic mapping rises to approximately `58.44%` of the total decision weight.

## Execution reopen register

```text
PM-09 execution-worthy gaps     0
SC-013 reopen                    NO
PM-04B reopen                    NO
benchmark host                   HOLD / DORMANT
```

## PM-08 secondary state carried forward

```text
GRAPH
G0 baseline ADVANCE
Neo4j DEFER / NOT REJECTED

SEARCH/VECTOR
PostgreSQL native FTS ADVANCE as P0 baseline
pgvector 0.8.6 ADMIT-CONDITIONAL
Qdrant 1.18.2 DEFER / TRIGGER ONLY
OpenSearch 3.7 DEFER / TRIGGER ONLY

LOCAL/OFFLINE
SQLite 3.53.4 ADMIT BOUNDED CANDIDATE / NOT CANONICAL

OBJECT/BLOB
NO ENGINE ADMITTED / TRIGGER ONLY
```

## Post-selection proof register

Still mandatory where applicable:

```text
SC-011 old-backup anti-resurrection
SC-030 actual LifeOS V1→V2 evolution
SC-031 destructive restore + semantic verification
SC-032 capacity/backpressure truthful degradation
WL-H12 system-level non-interference
SC-017/018 search/non-interference when active
SC-019 vector recall after real security filter when active
SC-020/021 projection freshness/deletion propagation when active
local/offline sync/reconciliation validation when active
```

## Evidence paths

```text
PM-01
pm-01-technology-landscape-v1.md

PM-02
pm-02-primary-mapping-overview-v1.md
mappings/*

PM-03
pm-03-semantic-hard-gate-preflight-v1.md
preflight/*

PM-04A
pm-04-external-evidence-sufficiency-v1.md
evidence/*

PM-05
pm-05-correctness-evidence-qualification-v1.md
qualification/*-v1.md

PM-06/07
pm-06-07-joint-finalist-qualification-v1.md
pm-06-scale-performance-evidence-v1.md
pm-07-recovery-evolution-evidence-v1.md
qualification/*-pm-06-07-v1.md

PM-08
pm-08-secondary-lanes-v1.md
secondary/*

PM-09
pm-09-scoring-sensitivity-v1.md
scoring/postgresql-18.4-v1.md
scoring/typedb-3.12.3-v1.md
scoring/sensitivity-analysis-v1.md
```

## Next

```text
PM-10
RECOMMENDATION
fresh exact gate required

CURRENT EVIDENCE-SCORE LEADER
PostgreSQL 18.4

PREFERRED NONE
SELECTED NONE
BACKEND NOT STARTED / DEFERRED
```