# Physical Model Acceptance Test Matrix v1

- Status: **CURRENT — PM-06/07 JOINT COMPLETE / DIRECT EXECUTION NOT STARTED**
- Workstream: `feature/physical-model`
- Finalists: PostgreSQL 18.4, TypeDB CE 3.12.3
- Deferred primary challengers: XTDB 2.1.0, SurrealDB Community 3.2.3 — NOT REJECTED
- Technology selection: **NONE**

## Result-layer rule

```text
PM-03 STATIC PREFLIGHT
!=
PM-04A EVIDENCE SUFFICIENCY
!=
PM-05 SCENARIO QUALIFICATION
!=
PM-06/07 FINALIST QUALIFICATION
!=
DIRECT EXECUTION
```

`EVIDENCE-QUALIFIED != DIRECT PASS` and `NOT RUN != PASS`.

## Current primary disposition

| Candidate | PM-05 | PM-06 | PM-07 | Current disposition |
|---|---|---|---|---|
| PostgreSQL 18.4 | FINALIST | VIABLE / HIGH CONFIDENCE | MATERIAL ADVANTAGE | ADVANCE / overall leader |
| TypeDB CE 3.12.3 | FINALIST | VIABLE / MEDIUM-HIGH | VIABLE / higher ops cost | ADVANCE / semantic challenger |
| XTDB 2.1.0 | DEFER | not in finalist campaign | not in finalist campaign | DEFER / NOT REJECTED |
| SurrealDB 3.2.3 | DEFER | not in finalist campaign | not in finalist campaign | DEFER / NOT REJECTED |

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

### Primary semantic set

```text
SC-001 SC-002 SC-003 SC-009 SC-010 SC-012
SC-014 SC-015 SC-016 SC-022 SC-023 SC-024
```

Current classification: `PRIMARY-EVIDENCE-SUFFICIENT`; direct run not required now.

### System/runtime/provider set

```text
SC-004 SC-005 SC-006 SC-007 SC-008
SC-025 SC-026 SC-027 SC-028 SC-029 SC-033 SC-034
```

Current classification: `SYSTEM-BOUNDARY`.

### Secondary lane set

```text
SC-017 SC-018 SC-019 SC-020 SC-021 SC-035
```

Current classification: `PM-08-SECONDARY`.

## PM-06/07 finalist scenarios

| Scenario | PostgreSQL | TypeDB | Current treatment |
|---|---|---|---|
| SC-011 old-backup anti-resurrection | NOT RUN | NOT RUN | post-selection implementation validation |
| SC-013 deep-history current-state scale | NOT RUN | NOT RUN | reopen only if PM-09 performance-sensitive |
| SC-030 V1→V2 historical-reference evolution | NOT RUN | NOT RUN | post-selection implementation validation |
| SC-031 destructive restore + semantic verification | NOT RUN | NOT RUN | post-selection implementation validation |
| SC-032 capacity/backpressure | NOT RUN | NOT RUN | post-selection implementation validation |

None of these is declared PASS.

## Qualification tiers

| Tier | PostgreSQL | TypeDB |
|---|---|---|
| LOW | NOT RUN | NOT RUN |
| BASE | NOT RUN | NOT RUN |
| HIGH | NOT RUN | NOT RUN |

No direct tier is currently admitted.

## Load profiles

| Profile | PostgreSQL | TypeDB |
|---|---|---|
| LP-01 read-heavy current | NOT RUN | NOT RUN |
| LP-02 mixed interactive | NOT RUN | NOT RUN |
| LP-03 write/conflict burst | NOT RUN | NOT RUN |
| LP-04 history/reporting | NOT RUN | NOT RUN |
| LP-05 projection/search churn | NOT RUN | NOT RUN |

## PM-06 evidence classification

### PostgreSQL

```text
SCALE/PERFORMANCE VIABLE
engine/workload maturity confidence HIGH
no local performance execution-worthy gap
```

### TypeDB

```text
SCALE/PERFORMANCE VIABLE
confidence MEDIUM-HIGH
one query currently single-threaded
CE single-node
resource/index sizing conditions explicit
no local performance execution-worthy gap
```

## PM-07 evidence classification

### PostgreSQL

```text
backup/restore breadth        STRONG
WAL/PITR                      AVAILABLE
incremental base backup       AVAILABLE
physical/logical replication  AVAILABLE
standby/failover primitives   AVAILABLE
upgrade/migration paths       MATURE
```

### TypeDB CE

```text
self-hosted backup owner      USER
backup paths                  snapshot / export-import
incremental backup            NO for documented self-hosted paths
cross-version export/import   AVAILABLE
CE cluster/HA                 NO — single-node subject
Cloud/Enterprise cluster      outside frozen CE subject
```

## Operational register

| Check | PostgreSQL | TypeDB |
|---|---|---|
| exact finalist subject pinned | YES | YES |
| official PM-06 docs reviewed | YES | YES |
| official PM-07 docs reviewed | YES | YES |
| benchmark host frozen | HOLD / DORMANT | HOLD / DORMANT |
| database deployed | NOT RUN | NOT RUN |
| backup created by LifeOS | NOT RUN | NOT RUN |
| destructive restore | NOT RUN | NOT RUN |
| semantic post-restore suite | NOT RUN | NOT RUN |
| anti-resurrection | NOT RUN | NOT RUN |
| V1→V2 LifeOS migration | NOT RUN | NOT RUN |
| failure injection | NOT RUN | NOT RUN |

## Execution admission result

```text
PM-06 execution-worthy gaps     0
PM-07 execution-worthy gaps     0
PM-04B reopened                 NO
benchmark host                  HOLD / DORMANT
```

## Advancement

```text
PostgreSQL
ADVANCE
CURRENT OVERALL LEADER

TypeDB
ADVANCE
PRINCIPAL SEMANTIC CHALLENGER

PREFERRED
NONE

SELECTED
NONE

NEXT
PM-08 secondary/specialist lane qualification
```

Performance cannot compensate for recovery/evolution failure. Secondary technologies cannot hide a primary semantic/integrity weakness.