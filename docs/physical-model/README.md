# Physical Model

- Status: **AUTHORIZED / IN PROGRESS — PM-09 COMPLETE / PM-10 NEXT**
- Branch: `feature/physical-model`
- Main baseline: `3de84bb49f9cef30e88e9bde4961ed84335daa79`
- PM-00: **QA PASS**
- PM-01: **PASS-CONDITIONAL**
- PM-02: **COMPLETE**
- PM-03: **STATIC COMPLETE / 0 REJECTS**
- PM-04A: **COMPLETE / 0 EXECUTION-WORTHY GAPS**
- PM-04B: **NOT ADMITTED**
- PM-05: **COMPLETE**
- PM-06: **EVIDENCE QUALIFICATION COMPLETE / DIRECT PERFORMANCE NOT RUN**
- PM-07: **EVIDENCE QUALIFICATION COMPLETE / DIRECT DESTRUCTIVE RUNS NOT RUN**
- PM-08: **SECONDARY/SPECIALIST QUALIFICATION COMPLETE / NO DIRECT RUN**
- PM-09: **EVIDENCE-WEIGHTED SCORING + SENSITIVITY COMPLETE**
- Primary finalists: **PostgreSQL 18.4 + TypeDB CE 3.12.3**
- Evidence-weighted score: **PostgreSQL 89.25 / TypeDB 80.00**
- Ranking: **ROBUST / NOT SENSITIVITY-DEPENDENT**
- Current evidence-score leader: **PostgreSQL 18.4**
- Preferred: **NONE**
- Selected: **NONE**
- Backend Foundation: **NOT STARTED / DEFERRED**

## Purpose

Turn accepted LifeOS Domain + Logical semantics into a durable, evidence-backed Physical Model without weakening semantics or manufacturing benchmarks that cannot change the decision.

```text
DOMAIN + LOGICAL
fixed semantic authority

PHYSICAL
research
→ candidate-native mapping
→ semantic preflight
→ evidence sufficiency
→ correctness qualification
→ finalist qualification
→ specialist lanes
→ scoring/sensitivity
→ recommendation
→ explicit selection
→ accepted model / clean-room QA / main integration
```

## Non-negotiable barriers

```text
SEMANTIC OWNER != IMPLEMENTATION MECHANISM
ADDRESSABILITY != DOMAIN IDENTITY
STORAGE TOKEN != MaterialStateRef
CANONICAL != PROVIDER / DERIVED / SECURITY STATE
SECONDARY != CANONICAL
LOCAL != CANONICAL
MISSING != FALSE
EVIDENCE-QUALIFIED != EXECUTED PASS
EVIDENCE-WEIGHTED SCORE != VERIFIED-RUN SCORE
PUBLIC BENCHMARK != LIFEOS BENCHMARK
FINALIST != PREFERRED
PREFERRED != SELECTED
DEFER != REJECT
```

No universal Entity/Thing/EAV/generic-edge canonical shortcut may be introduced for implementation convenience.

## Evidence-first execution policy

```text
LOCAL EXECUTION
last-mile evidence only
```

A direct run requires a residual question that remains unresolved, is materially decision-relevant, and can actually be resolved by controlled execution.

Current direct execution state:

```text
benchmark host          HOLD / DORMANT
database deployment     NOT STARTED
fixture/harness          NOT STARTED
LOW/BASE/HIGH            NOT RUN
direct HG PASS           0
restore rehearsal        NOT RUN
migration rehearsal      NOT RUN
failure injection        NOT RUN
verified-run score       NOT AVAILABLE
```

## Two score ledgers

Phase-10 now preserves both:

```text
VERIFIED-RUN BENCHMARK SCORE
requires direct applicable hard-gate PASS and execution artifacts

EVIDENCE-WEIGHTED DECISION SCORE
used by PM-09 after evidence exhaustion and 0 ranking-critical execution gaps
```

The PM-09 score is the second type only. It does not imply any direct hard-gate PASS.

## Primary finalists after PM-09

### PostgreSQL 18.4

```text
ROLE
robust evidence-score leader

PM-09 SCORE
89.25 / 100

SENSITIVITY
ROBUST

PREFERRED
NONE

SELECTED
NONE
```

Why it leads:

- accepted mapping preserves LifeOS semantics without a universal ontology root;
- strong transaction/concurrency ergonomics;
- mature integrity primitives;
- WAL/PITR and full/incremental backup paths;
- physical/logical replication and standby/failover primitives;
- mature migration/evolution paths;
- PM-08 server-topology consolidation via native FTS + conditional pgvector;
- strong Python/tooling/ecosystem and low exit risk.

Performance is **not** a hidden reason for the lead: PM-09 deliberately scores performance `8.0 / 8.0` because LOW/BASE/HIGH were not executed.

### TypeDB CE 3.12.3

```text
ROLE
principal semantic challenger

PM-09 SCORE
80.00 / 100

SEMANTIC DIMENSION
9.5 vs PostgreSQL 8.5

PREFERRED
NONE

SELECTED
NONE
```

Why it remains a serious finalist:

- strongest direct relation/role/n-ary semantic representation;
- strong schema/cardinality semantics;
- credible scale-up and concurrent-query model;
- explicit cross-version export/import evolution path.

Material costs/conditions:

- snapshot-isolation hardening via correctly scoped consistency guards;
- CE single-node topology;
- self-hosted backup implementation is LifeOS-owned;
- documented self-hosted backup paths are non-incremental;
- clustering/horizontal read scaling belong outside CE;
- external search/vector specialist is more likely once advanced retrieval is accepted.

## PM-09 base scoring

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
| **Total** | **100** | **89.25** | **80.00** |

## Sensitivity result

```text
S0 base                         PG +9.25
S1 semantic-heavy               PG +5.75
S2 early single-node            PG +7.25
S3 operations/recovery-heavy    PG +12.50
S4 strongly TypeDB-friendly     PG +2.75
```

```text
RANKING ROBUST
SENSITIVITY-DEPENDENT NO
PERFORMANCE-DEPENDENT NO
SC-013 REOPEN NO
PM-04B REOPEN NO
```

Only a deliberately non-accepted adversarial weighting with semantic mapping at 50% produces a tiny TypeDB lead (`0.125`). Keeping all other original dimensions proportional, semantic mapping must rise to approximately `58.44%` before break-even.

## PM-08 specialist state

```text
GRAPH
no initial graph specialist
Neo4j defer / not rejected

SEARCH/VECTOR
PostgreSQL native FTS baseline
pgvector 0.8.6 admit-conditional
Qdrant 1.18.2 defer / trigger only
OpenSearch 3.7 defer / trigger only

LOCAL/OFFLINE
SQLite 3.53.4 admit bounded candidate / never canonical

OBJECT/BLOB
no engine admitted / trigger only
```

## Post-selection implementation validation

Still mandatory where applicable; none is waived by scoring:

```text
SC-011 old-backup anti-resurrection
SC-030 actual LifeOS V1→V2 mapping evolution
SC-031 semantic backup/restore verification
SC-032 capacity/backpressure behavior
WL-H12 system-level non-interference
search/vector/projection/local validation when those mechanisms become active
```

## Current work products

```text
execution-methodology-v1.md
execution-template-v1.md
acceptance-test-matrix-v1.md
result-register-v1.md

pm-01-technology-landscape-v1.md
pm-02-primary-mapping-overview-v1.md
mappings/*
pm-03-semantic-hard-gate-preflight-v1.md
preflight/*
pm-04-external-evidence-sufficiency-v1.md
evidence/*
pm-05-correctness-evidence-qualification-v1.md
qualification/*
pm-06-07-joint-finalist-qualification-v1.md
pm-06-scale-performance-evidence-v1.md
pm-07-recovery-evolution-evidence-v1.md
pm-08-secondary-lanes-v1.md
secondary/*
pm-09-scoring-sensitivity-v1.md
scoring/*
```

## Roadmap

```text
PM-00  PASS
PM-01  PASS-CONDITIONAL
PM-02  COMPLETE
PM-03  COMPLETE
PM-04A COMPLETE
PM-04B NOT ADMITTED
PM-05  COMPLETE
PM-06  COMPLETE
PM-07  COMPLETE
PM-08  COMPLETE
PM-09  COMPLETE
PM-10  NEXT
PM-11  NOT STARTED
PM-12  NOT STARTED
PM-13  NOT STARTED
PM-14  NOT STARTED
```

## Current exact next step

```text
PM-10
recommendation / evidence conditions / PREFERRED decision
fresh exact write gate required

CURRENT EVIDENCE-SCORE LEADER
PostgreSQL 18.4

PREFERRED NONE
SELECTED NONE
BACKEND NOT STARTED / DEFERRED
```