# Physical Model Acceptance Test Matrix v1

- Status: **CURRENT — PM-08 COMPLETE / PM-09 NEXT / DIRECT EXECUTION NOT STARTED**
- Workstream: `feature/physical-model`
- Finalists: PostgreSQL 18.4, TypeDB CE 3.12.3
- Deferred primary challengers: XTDB 2.1.0, SurrealDB Community 3.2.3 — NOT REJECTED
- Preferred: **NONE**
- Selected: **NONE**

## Result-layer rule

```text
PM-03 STATIC PREFLIGHT
!= PM-04A EVIDENCE SUFFICIENCY
!= PM-05 SCENARIO QUALIFICATION
!= PM-06/07 FINALIST QUALIFICATION
!= PM-08 SECONDARY-LANE QUALIFICATION
!= DIRECT EXECUTION
```

`EVIDENCE-QUALIFIED != DIRECT PASS`, `ADMIT != SELECTED`, and `NOT RUN != PASS`.

## Current primary disposition

| Candidate | PM-05 | PM-06 | PM-07 | PM-08 implication | Current disposition |
|---|---|---|---|---|---|
| PostgreSQL 18.4 | FINALIST | VIABLE / HIGH | MATERIAL OPS/RECOVERY ADVANTAGE | FTS native + pgvector conditional; fewer likely server technologies | ADVANCE / overall leader |
| TypeDB CE 3.12.3 | FINALIST | VIABLE / MEDIUM-HIGH | VIABLE / higher ops cost | likely external search/vector specialist when required | ADVANCE / semantic challenger |
| XTDB 2.1.0 | DEFER | not finalist campaign | not finalist campaign | no PM-08 reopen | DEFER / NOT REJECTED |
| SurrealDB 3.2.3 | DEFER | not finalist campaign | not finalist campaign | no PM-08 reopen | DEFER / NOT REJECTED |

## Direct hard-gate status

No direct LifeOS database correctness/destructive run has occurred.

| Gate | PostgreSQL | TypeDB | XTDB | SurrealDB |
|---|---|---|---|---|
| HG-01 | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| HG-02 | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| HG-03 | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| HG-04 | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| HG-05 | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| HG-06 | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| HG-07 | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| HG-08 | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| HG-09 | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| HG-10 | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| HG-11 | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| HG-12 | NOT RUN | NOT RUN | NOT RUN | NOT RUN |

Direct HG PASS count: `0`.

## PM-05 scenario qualification

```text
PRIMARY-EVIDENCE-SUFFICIENT
SC-001 SC-002 SC-003 SC-009 SC-010 SC-012
SC-014 SC-015 SC-016 SC-022 SC-023 SC-024

SYSTEM-BOUNDARY
SC-004 SC-005 SC-006 SC-007 SC-008
SC-025 SC-026 SC-027 SC-028 SC-029 SC-033 SC-034
```

No direct PASS is implied.

## PM-06/07 finalist scenarios

| Scenario | PostgreSQL | TypeDB | Current treatment |
|---|---|---|---|
| SC-011 old-backup anti-resurrection | NOT RUN | NOT RUN | post-selection implementation validation |
| SC-013 deep-history current-state scale | NOT RUN | NOT RUN | reopen only if PM-09 performance-sensitive |
| SC-030 V1→V2 historical-reference evolution | NOT RUN | NOT RUN | post-selection implementation validation |
| SC-031 destructive restore + semantic verification | NOT RUN | NOT RUN | post-selection implementation validation |
| SC-032 capacity/backpressure | NOT RUN | NOT RUN | post-selection implementation validation |

## PM-08 secondary-lane matrix

| Lane / candidate | Status | Authority role | Direct execution | Reopen/activation rule |
|---|---|---|---|---|
| G0 primary-store graph baseline | ADVANCE | primary-native queries only | NOT RUN | baseline |
| Neo4j | DEFER / NOT REJECTED | secondary projection only if later admitted | NOT RUN | concrete graph workload materially beats primary baseline |
| PostgreSQL native FTS | ADVANCE as P0 baseline | query/index mechanism inside primary | NOT RUN | applicable when PostgreSQL remains primary candidate |
| pgvector 0.8.6 | ADMIT-CONDITIONAL | derived vector mechanism inside PostgreSQL | NOT RUN | PostgreSQL selected + accepted vector retrieval requirement |
| Qdrant 1.18.2 | DEFER / NOT REJECTED | secondary search/vector projection only | NOT RUN | large/independent/advanced vector retrieval trigger |
| OpenSearch 3.7 | DEFER / NOT REJECTED | secondary search projection only | NOT RUN | large/advanced dedicated search trigger |
| SQLite 3.53.4 | ADMIT BOUNDED ROLE | client/local/offline only | NOT RUN | exact client implementation deferred |
| Object/blob engine | DEFER / TRIGGER ONLY | external bounded object persistence if later admitted | NOT RUN | concrete object-size/volume/security/durability requirement |

## Cross-lane hard gates

| Gate | Initial state | PM-08 treatment |
|---|---|---|
| CG-01 secondary not canonical truth | EVIDENCE-QUALIFIED | explicit invariant for every admitted/deferred lane |
| CG-02 deletion/correction/access propagation | NOT RUN | post-selection validation where a projection exists |
| CG-03 non-interference filtering/ranking | NOT RUN | post-selection search/system validation; cannot weaken scope filters |
| CG-04 freshness/material basis | NOT RUN | required projection contract; post-selection validation where applicable |

## PM-08 scenario disposition

| Scenario | PM-08 disposition |
|---|---|
| SC-017 hidden-result non-interference | post-selection search/system validation |
| SC-018 FTS mixed filter/query | post-selection search implementation validation |
| SC-019 vector recall after security filter | reopen before selection only if vector path becomes ranking/performance-sensitive; otherwise implementation validation |
| SC-020 stale index source | post-selection projection validation when projection exists |
| SC-021 deletion propagation | post-selection projection validation when projection exists |
| SC-035 graph projection divergence/rebuild | not applicable to initial stack; reopen if graph projection is later admitted |

None is declared direct PASS.

## Qualification tiers and load profiles

```text
LOW / BASE / HIGH
NOT RUN PostgreSQL
NOT RUN TypeDB

LP-01..LP-05
NOT RUN PostgreSQL
NOT RUN TypeDB
```

No direct tier is currently admitted.

## Operational/direct register

| Check | PostgreSQL | TypeDB |
|---|---|---|
| exact finalist subject pinned | YES | YES |
| PM-06/07 evidence reviewed | YES | YES |
| PM-08 specialist implication reviewed | YES | YES |
| benchmark host frozen | HOLD / DORMANT | HOLD / DORMANT |
| database deployed | NOT RUN | NOT RUN |
| direct backup/restore | NOT RUN | NOT RUN |
| semantic post-restore suite | NOT RUN | NOT RUN |
| V1→V2 LifeOS migration | NOT RUN | NOT RUN |
| failure injection | NOT RUN | NOT RUN |

## Execution admission result

```text
PM-06 execution-worthy gaps     0
PM-07 execution-worthy gaps     0
PM-08 execution-worthy gaps     0
PM-04B reopened                 NO
benchmark host                  HOLD / DORMANT
```

## PM-08 architecture pressure carried to PM-09

```text
POSTGRESQL PATH
canonical primary
+ native FTS
+ pgvector conditional inside same database
+ SQLite bounded local/offline if needed
=> likely zero additional server engines initially

TYPEDB PATH
canonical primary
+ stronger semantic relation model
+ likely external search/vector service when accepted retrieval capability requires it
+ SQLite bounded local/offline if needed
=> probable additional server topology/operations cost
```

This is a PM-09 scoring/sensitivity input, not a selection.

## Advancement

```text
PostgreSQL
ADVANCE
CURRENT OVERALL LEADER

TypeDB
ADVANCE
PRINCIPAL SEMANTIC CHALLENGER

PM-08
COMPLETE

PREFERRED
NONE

SELECTED
NONE

NEXT
PM-09 scoring + sensitivity
```

Performance cannot compensate for recovery/evolution failure. Secondary technologies cannot hide a primary semantic/integrity weakness.