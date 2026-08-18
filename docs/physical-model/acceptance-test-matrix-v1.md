# Physical Model Acceptance Test Matrix v1

- Status: **CURRENT — PM-09 COMPLETE / PM-10 NEXT / DIRECT EXECUTION NOT STARTED**
- Workstream: `feature/physical-model`
- Finalists: PostgreSQL 18.4, TypeDB CE 3.12.3
- Deferred primary challengers: XTDB 2.1.0, SurrealDB Community 3.2.3 — NOT REJECTED
- Current evidence-score leader: **PostgreSQL 18.4**
- Preferred: **NONE**
- Selected: **NONE**

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
PM-08 SPECIALIST QUALIFICATION
!=
PM-09 EVIDENCE-WEIGHTED DECISION SCORE
!=
VERIFIED-RUN BENCHMARK SCORE
!=
DIRECT EXECUTION
```

`EVIDENCE-QUALIFIED != DIRECT PASS`, `EVIDENCE SCORE != VERIFIED-RUN SCORE`, and `NOT RUN != PASS`.

## Primary disposition

| Candidate | PM-05 | PM-06 | PM-07 | PM-08 implication | PM-09 evidence score | Current disposition |
|---|---|---|---|---|---:|---|
| PostgreSQL 18.4 | FINALIST | VIABLE / HIGH | MATERIAL ADVANTAGE | FTS + conditional pgvector consolidation | **89.25** | ROBUST LEADER / ADVANCE PM-10 |
| TypeDB CE 3.12.3 | FINALIST | VIABLE / MEDIUM-HIGH | VIABLE / higher ops cost | external search/vector more likely | **80.00** | PRINCIPAL SEMANTIC CHALLENGER / ADVANCE PM-10 record |
| XTDB 2.1.0 | DEFER | not in finalist campaign | not in finalist campaign | no PM-08 reopening | — | DEFER / NOT REJECTED |
| SurrealDB 3.2.3 | DEFER | not in finalist campaign | not in finalist campaign | no PM-08 reopening | — | DEFER / NOT REJECTED |

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

## Direct benchmark tiers

| Tier | PostgreSQL | TypeDB |
|---|---|---|
| LOW | NOT RUN | NOT RUN |
| BASE | NOT RUN | NOT RUN |
| HIGH | NOT RUN | NOT RUN |

Verified-run weighted score: `NOT AVAILABLE` for both.

## PM-05 scenario qualification carried forward

### Primary semantic set

```text
SC-001 SC-002 SC-003 SC-009 SC-010 SC-012
SC-014 SC-015 SC-016 SC-022 SC-023 SC-024
```

Classification: `PRIMARY-EVIDENCE-SUFFICIENT`; direct run not required for current ranking.

### System/runtime/provider set

```text
SC-004 SC-005 SC-006 SC-007 SC-008
SC-025 SC-026 SC-027 SC-028 SC-029 SC-033 SC-034
```

Classification: `SYSTEM-BOUNDARY`.

## PM-06/07 carry-forward

| Scenario | PostgreSQL | TypeDB | Current treatment |
|---|---|---|---|
| SC-011 old-backup anti-resurrection | NOT RUN | NOT RUN | post-selection implementation validation |
| SC-013 deep-history current-state scale | NOT RUN | NOT RUN | PM-09 reopen test = NO |
| SC-030 V1→V2 historical-reference evolution | NOT RUN | NOT RUN | post-selection implementation validation |
| SC-031 destructive restore + semantic verification | NOT RUN | NOT RUN | post-selection implementation validation |
| SC-032 capacity/backpressure | NOT RUN | NOT RUN | post-selection implementation validation |

None is declared PASS.

## PM-08 secondary matrix

| Lane / candidate | Status | Direct run | Selection meaning |
|---|---|---|---|
| G0 primary-store graph baseline | ADVANCE | NOT RUN | baseline only |
| Neo4j | DEFER / NOT REJECTED | NOT RUN | no initial graph specialist |
| PostgreSQL native FTS | ADVANCE as P0 baseline | NOT RUN | primary-native capability |
| pgvector 0.8.6 | ADMIT-CONDITIONAL | NOT RUN | only if PostgreSQL selected + vector need accepted |
| Qdrant 1.18.2 | DEFER / TRIGGER ONLY | NOT RUN | no initial service |
| OpenSearch 3.7 | DEFER / TRIGGER ONLY | NOT RUN | no initial service |
| SQLite 3.53.4 | ADMIT bounded local/offline candidate | NOT RUN | never canonical authority |
| object/blob engine | DEFER / TRIGGER ONLY | NOT RUN | no engine admitted |

## PM-09 fixed dimensions

| Dimension | Weight | PostgreSQL grade | TypeDB grade |
|---|---:|---:|---:|
| Semantic mapping simplicity / evolvability | 20 | 8.5 | **9.5** |
| Transaction / concurrency ergonomics | 15 | **9.5** | 7.0 |
| Query / reporting / traversal | 15 | **9.0** | 8.5 |
| History + current-state efficiency | 10 | 8.5 | 8.5 |
| Operations / backup / restore / HA | 15 | **9.5** | 6.5 |
| Schema evolution / migration | 10 | **9.0** | 8.0 |
| Performance / resource efficiency | 10 | 8.0 | 8.0 |
| Python / tooling / cost / exit risk | 5 | **9.5** | 7.0 |
| **Evidence-weighted score** | **100** | **89.25** | **80.00** |

Performance is intentionally tied because direct LOW/BASE/HIGH were not executed.

## PM-09 sensitivity

| Scenario | PostgreSQL | TypeDB | Result |
|---|---:|---:|---|
| S0 Phase-10 base | 89.25 | 80.00 | PG +9.25 |
| S1 semantic-heavy | 88.75 | 83.00 | PG +5.75 |
| S2 early single-node / semantic-friendly | 88.75 | 81.50 | PG +7.25 |
| S3 operations/recovery-heavy | 90.00 | 77.50 | PG +12.50 |
| S4 strongly TypeDB-friendly accepted stress | 88.00 | 85.25 | PG +2.75 |

```text
RANKING ROBUST
SENSITIVITY-DEPENDENT NO
PERFORMANCE-DEPENDENT NO
SC-013 REOPEN NO
PM-04B REOPEN NO
```

Adversarial boundary only:

```text
semantic 50%
PostgreSQL 87.375
TypeDB      87.500
```

Not an accepted LifeOS weighting.

Continuous break-even with original non-semantic proportions: semantic mapping approximately `58.44%`.

## Post-selection validation obligations

Still mandatory where applicable:

```text
SC-011
SC-030
SC-031
SC-032
WL-H12
SC-017/018 when search active
SC-019 when vector active
SC-020/021 when projections active
local/offline reconciliation when local role active
```

## Execution admission result

```text
PM-09 ranking-critical execution gaps  0
PM-04B reopened                        NO
benchmark host                          HOLD / DORMANT
verified-run score                      NOT AVAILABLE
```

## Advancement

```text
PostgreSQL
ADVANCE PM-10
EVIDENCE-WEIGHTED ROBUST LEADER

TypeDB
ADVANCE PM-10 COMPARATIVE RECORD
PRINCIPAL SEMANTIC CHALLENGER

PREFERRED
NONE

SELECTED
NONE

NEXT
PM-10 recommendation
```