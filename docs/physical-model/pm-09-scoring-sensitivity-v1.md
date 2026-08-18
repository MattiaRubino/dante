# PM-09 Evidence-Weighted Scoring + Sensitivity v1

- Status: **PM-09 COMPLETE — EVIDENCE-WEIGHTED DECISION SCORING / NOT VERIFIED-RUN BENCHMARK SCORING**
- Workstream: `feature/physical-model`
- PRE-SCOPE: `6aef5537edacff3e315d502a1bd3ede544dc149e`
- Primary finalists: **PostgreSQL 18.4 / TypeDB CE 3.12.3**
- Direct hard-gate execution: **NOT RUN**
- Direct HG PASS count: **0**
- LOW/BASE/HIGH benchmark tiers: **NOT RUN**
- Preferred: **NONE**
- Selected: **NONE**

## Purpose

Convert the accumulated PM-01 through PM-08 evidence into a transparent comparative decision score and stress-test the ranking without fabricating execution evidence.

PM-09 preserves two separate ledgers:

```text
EVIDENCE-WEIGHTED DECISION SCORE
comparative decision aid produced from qualified evidence

!=

VERIFIED-RUN BENCHMARK SCORE
requires direct hard-gate PASS and direct benchmark artifacts
```

The first ledger is produced here. The second remains unavailable because direct execution was not admitted by PM-04A/PM-05/PM-06/PM-07/PM-08.

## Why scoring is allowed without pretending execution

The evidence-first process established all of the following before PM-09:

```text
PM-04A execution-worthy gaps            0
PM-05 execution-worthy gaps             0
PM-06 performance reversal signal       NONE
PM-07 execution-worthy gaps             0
PM-08 execution-worthy gaps             0
PM-04B harness                           NOT ADMITTED
benchmark host                           HOLD / DORMANT
```

Therefore PM-09 may compare known capability, mapping and operational evidence while preserving every unexecuted proof as `NOT RUN`.

This does not convert evidence qualification into hard-gate PASS.

## Fixed dimensions and weights

The original Phase-10 100-point dimensions are preserved unchanged:

| Dimension | Weight |
|---|---:|
| Semantic mapping simplicity / evolvability | 20 |
| Transaction / concurrency ergonomics | 15 |
| Query / reporting / traversal | 15 |
| History + current-state efficiency | 10 |
| Operations / backup / restore / HA maturity | 15 |
| Schema evolution / migration | 10 |
| Performance / resource efficiency | 10 |
| Python / tooling / cost / exit risk | 5 |
| **Total** | **100** |

Dimension grades use a 0–10 evidence scale. Weighted points are `grade × weight / 10`.

## Base scoring

| Dimension | Weight | PostgreSQL | TypeDB |
|---|---:|---:|---:|
| Semantic mapping simplicity / evolvability | 20 | 8.5 | **9.5** |
| Transaction / concurrency ergonomics | 15 | **9.5** | 7.0 |
| Query / reporting / traversal | 15 | **9.0** | 8.5 |
| History + current-state efficiency | 10 | 8.5 | 8.5 |
| Operations / backup / restore / HA | 15 | **9.5** | 6.5 |
| Schema evolution / migration | 10 | **9.0** | 8.0 |
| Performance / resource efficiency | 10 | 8.0 | 8.0 |
| Python / tooling / cost / exit | 5 | **9.5** | 7.0 |
| **Evidence-weighted total** | **100** | **89.25** | **80.00** |

```text
BASE DELTA
PostgreSQL +9.25
```

## Evidence interpretation by dimension

### Semantic mapping simplicity / evolvability

```text
PostgreSQL 8.5
TypeDB      9.5
```

TypeDB wins this dimension. Its relation/role/cardinality/n-ary model is the most semantically direct finalist mapping. PostgreSQL preserves accepted LifeOS semantics but needs more explicit technical relational structures and bounded heterogeneous reference-address anchors.

Evidence basis:

- `pm-02-primary-mapping-overview-v1.md`
- `mappings/postgresql-18.4-v1.md`
- `mappings/typedb-3.12.3-v1.md`
- PM-03 through PM-05 semantic qualification records.

### Transaction / concurrency ergonomics

```text
PostgreSQL 9.5
TypeDB      7.0
```

PostgreSQL exposes a stronger direct concurrency/transaction posture for LifeOS consequential operations. TypeDB remains viable but carries snapshot-isolation hardening and complete consistency-guard coverage as a persistent implementation/operability condition.

### Query / reporting / traversal

```text
PostgreSQL 9.0
TypeDB      8.5
```

TypeDB remains excellent for relationship-native queries. PostgreSQL has the broader aggregate LifeOS query/reporting envelope and PM-08 showed that recursive traversal, lexical search and conditional vector retrieval can remain within the same server technology.

### History + current-state efficiency

```text
PostgreSQL 8.5
TypeDB      8.5
```

Both finalist mappings support explicit current/material-history design without lifetime replay for normal reads. No evidence currently justifies a comparative advantage large enough to score differently.

`SC-013` remains unexecuted and is not used to create a hidden performance advantage.

### Operations / backup / restore / HA

```text
PostgreSQL 9.5
TypeDB      6.5
```

This is the largest evidence-backed gap. PM-07 established PostgreSQL's stronger self-hosted backup/recovery/replication/failover/topology envelope. TypeDB CE remains viable but is single-node, self-hosted backup orchestration is LifeOS-owned, documented self-hosted paths are non-incremental, and clustering/HA/horizontal read scaling belong outside the frozen CE subject.

### Schema evolution / migration

```text
PostgreSQL 9.0
TypeDB      8.0
```

Both are viable. TypeDB has credible redefine/export-import/cross-version paths. PostgreSQL has multiple mature migration/upgrade paths and lower aggregate operational uncertainty for the frozen self-hosted subject.

### Performance / resource efficiency

```text
PostgreSQL 8.0
TypeDB      8.0
```

Intentional tie.

PM-06 established viability for both finalists but did not produce direct LifeOS throughput/latency measurements. Therefore PM-09 does not invent a performance winner.

### Python / tooling / cost / exit risk

```text
PostgreSQL 9.5
TypeDB      7.0
```

Both frozen primary subjects have zero direct license cost. PostgreSQL receives the advantage from ecosystem/tooling maturity, lower topology coupling and PM-08 consolidation pressure: native FTS plus conditional pgvector can avoid a second server engine, while TypeDB is more likely to need an external search/vector specialist once accepted lexical/vector retrieval becomes material.

## Sensitivity scenarios

All scenarios preserve a total weight of 100.

### S0 — Phase-10 base

```text
semantic      20
transaction   15
query         15
history       10
operations    15
evolution     10
performance   10
tooling        5
```

Result:

```text
PostgreSQL 89.25
TypeDB      80.00
Delta       +9.25 PostgreSQL
```

### S1 — Semantic-heavy

```text
semantic      30
transaction   10
query         20
history       10
operations    10
evolution     10
performance    5
tooling        5
```

Result:

```text
PostgreSQL 88.75
TypeDB      83.00
Delta       +5.75 PostgreSQL
```

### S2 — Early single-node / semantic-friendly

```text
semantic      25
transaction   15
query         15
history       10
operations    10
evolution     10
performance   10
tooling        5
```

Result:

```text
PostgreSQL 88.75
TypeDB      81.50
Delta       +7.25 PostgreSQL
```

### S3 — Operations/recovery-heavy

```text
semantic      15
transaction   15
query         10
history       10
operations    25
evolution     10
performance   10
tooling        5
```

Result:

```text
PostgreSQL 90.00
TypeDB      77.50
Delta       +12.50 PostgreSQL
```

### S4 — Strongly TypeDB-friendly accepted stress

```text
semantic      40
transaction   10
query         20
history       10
operations     5
evolution      5
performance    5
tooling        5
```

Result:

```text
PostgreSQL 88.00
TypeDB      85.25
Delta       +2.75 PostgreSQL
```

PostgreSQL remains ahead even after semantic weight is doubled and operations/recovery is sharply de-emphasized.

## Adversarial boundary

A deliberately distorted boundary scenario is also recorded:

```text
semantic      50
transaction    5
query         20
history       10
operations     5
evolution      5
performance    2.5
tooling        2.5
```

Result:

```text
PostgreSQL 87.375
TypeDB      87.500
Delta       +0.125 TypeDB
```

This is **not an accepted LifeOS decision weighting** because it effectively suppresses consistency/operations/recovery/evolution/tooling priorities already frozen upstream. It exists only to locate the comparative boundary.

Holding the non-semantic Phase-10 dimensions proportional to their original relative weights, semantic mapping must reach approximately **58.44%** of the total weight for TypeDB to reach break-even.

## Sensitivity verdict

```text
RANKING
ROBUST

SENSITIVITY-DEPENDENT
NO

PERFORMANCE-DEPENDENT
NO

SC-013 REOPEN
NO

PM-04B REOPEN
NO
```

The accepted sensitivity space does not reverse the ranking.

## Primary comparative conclusion

```text
P0 PostgreSQL 18.4
EVIDENCE-WEIGHTED SCORE 89.25 / 100
ROBUST LEADER
ADVANCE TO PM-10
NOT YET PREFERRED
NOT SELECTED

P1 TypeDB CE 3.12.3
EVIDENCE-WEIGHTED SCORE 80.00 / 100
PRINCIPAL SEMANTIC CHALLENGER
ADVANCE TO PM-10 COMPARATIVE RECORD
NOT PREFERRED
NOT SELECTED
```

PostgreSQL does not win because of invented performance numbers. TypeDB's semantic advantage is explicitly preserved and scored higher. PostgreSQL leads because transaction ergonomics, operations/recovery/topology, evolution/tooling and specialist-consolidation advantages collectively exceed the semantic delta.

## Direct-execution truth

```text
DIRECT HG-01..HG-12     NOT RUN
DIRECT HG PASS          0
LOW/BASE/HIGH           NOT RUN
RESTORE                 NOT RUN
MIGRATION               NOT RUN
FAILURE INJECTION       NOT RUN
GRAPH/VECTOR/SEARCH     NOT RUN
BENCHMARK HOST          HOLD / DORMANT
VERIFIED-RUN SCORE      NOT AVAILABLE
```

## Carry-forward conditions

Post-selection implementation validation remains mandatory where applicable:

```text
SC-011 old-backup anti-resurrection
SC-030 actual LifeOS V1->V2 evolution
SC-031 destructive restore + semantic verification
SC-032 capacity/backpressure truthful degradation
WL-H12 system-level non-interference
SC-017/018 search/non-interference when search path active
SC-019 vector recall after real security filter when vector active
SC-020/021 projection freshness/deletion propagation when projection active
local/offline reconciliation validation when local role active
```

## Next

```text
PM-09 COMPLETE subject to remote QA
PM-10 RECOMMENDATION NEXT after fresh exact gate
PREFERRED NONE
SELECTED NONE
BACKEND NOT STARTED / DEFERRED
```