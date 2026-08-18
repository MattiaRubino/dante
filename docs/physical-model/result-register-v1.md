# Physical Model Result Register v1

- Status: **CURRENT — PM-06/07 JOINT COMPLETE / PM-08 NEXT**
- Workstream: `feature/physical-model`
- Primary finalists: **PostgreSQL 18.4 + TypeDB CE 3.12.3**
- Deferred challengers: **XTDB 2.1.0 + SurrealDB Community 3.2.3 — NOT REJECTED**
- Direct execution: **NOT STARTED**
- Preferred: **NONE**
- Selected: **NONE**

## Result-language rule

```text
OFFICIAL CLAIM != DIRECT EXECUTION
PUBLIC BENCHMARK != LIFEOS BENCHMARK
EVIDENCE-QUALIFIED != DIRECT PASS
FINALIST != PREFERRED
PREFERRED != SELECTED
DEFER != REJECT
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
PM-08   NEXT
PM-09+  NOT STARTED
```

## Finalist set

```text
P0 PostgreSQL 18.4
ADVANCE
CURRENT OVERALL LEADER

P1 TypeDB CE 3.12.3
ADVANCE
PRINCIPAL SEMANTIC CHALLENGER

P2 XTDB 2.1.0
DEFER / NOT REJECTED

P3 SurrealDB Community 3.2.3
DEFER / NOT REJECTED
```

## PM-06 result

### PostgreSQL

```text
SCALE/PERFORMANCE VIABLE
confidence HIGH
LOW/BASE/HIGH NOT RUN
```

No ranking-critical performance uncertainty remains.

### TypeDB CE

```text
SCALE/PERFORMANCE VIABLE
confidence MEDIUM-HIGH
LOW/BASE/HIGH NOT RUN
```

Material conditions:

- each query currently single-threaded;
- scale-up uses concurrent queries/transactions and resource sizing;
- CE is single-node;
- horizontal scaling belongs to Cloud/Enterprise;
- index/memory/disk overhead must be provisioned deliberately.

### PM-06 comparison

```text
PERFORMANCE REVERSAL SIGNAL
NONE

LOCAL BENCHMARK
NOT ADMITTED
```

TypeDB remains viable; PostgreSQL does not win because of invented throughput numbers. The current lead remains based on aggregate architecture and operations.

## PM-07 result

### PostgreSQL

```text
RECOVERY/EVOLUTION/OPERATIONS
MATERIAL ADVANTAGE
```

Evidence-qualified capabilities include:

- SQL/filesystem/continuous-archive backup families;
- WAL/PITR;
- full/incremental base backup;
- physical/logical replication;
- synchronous/asynchronous standby options;
- failover primitives;
- pg_upgrade;
- logical-replication migration.

### TypeDB CE

```text
RECOVERY/EVOLUTION
VIABLE
HIGHER SELF-HOSTED OPERATIONS COST
```

Evidence-qualified capabilities/conditions include:

- self-hosted backup implementation is user responsibility;
- disk snapshot or export/import are recommended self-hosted paths;
- those documented paths are not incremental;
- export/import is designed for cross-version migration;
- compatible versions may reuse/copy data directories;
- CE is single-node;
- cluster replication/horizontal read scaling/HA are Cloud/Enterprise capabilities.

## Joint comparative conclusion

```text
POSTGRESQL
OVERALL LEAD STRENGTHENED

TYPEDB
SEMANTIC ADVANTAGE PRESERVED
OPERATIONS/RECOVERY/TOPOLOGY DISADVANTAGE MADE EXPLICIT
```

The current decision question entering PM-08/09 is therefore not “which one can run LifeOS?” Both finalists remain viable.

It is:

> Is TypeDB's superior semantic relation/role model worth the additional concurrency-guard, self-hosted backup and CE-topology burden compared with PostgreSQL's stronger overall integrity/operations/recovery ecosystem?

## Scenario carry-forward

```text
SC-011 old-backup anti-resurrection
POST-SELECTION IMPLEMENTATION VALIDATION

SC-013 deep-history scale
REOPEN ONLY IF PM-09 PERFORMANCE-SENSITIVE

SC-030 actual LifeOS V1->V2 mapping evolution
POST-SELECTION IMPLEMENTATION VALIDATION

SC-031 semantic restore verification
POST-SELECTION IMPLEMENTATION VALIDATION

SC-032 capacity/backpressure
POST-SELECTION IMPLEMENTATION VALIDATION
```

None is a direct PASS.

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
BENCHMARK HOST           HOLD / DORMANT
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
qualification/postgresql-18.4-pm-06-07-v1.md
qualification/typedb-3.12.3-pm-06-07-v1.md
```

## Secondary lanes

Still not selected:

```text
GRAPH
G0 primary-store baseline
Neo4j deferred to PM-08

SEARCH/VECTOR
primary-native baseline
pgvector when PostgreSQL applicable
Qdrant/OpenSearch trigger-only

LOCAL/OFFLINE
SQLite bounded future lane
```

PM-08 must demand net value from every additional technology.

## Historical checkpoints

```text
MAIN BASELINE
3de84bb49f9cef30e88e9bde4961ed84335daa79

PM-01 terminal
fac3b5baf1813f886c4773594e6234810e5ba8c6

PM-02 terminal
db127af8c759aacf69b43d0f5a5444b04fd43759

PM-03 terminal
0e4212909bd94de076c9074302a79296d474e53f

PM-04A terminal
44d331f12951e2844186e6f5f885e1bcf1559a3b

PM-05 terminal
9a53c2577e8e25de6de63a830e9bab036521f040

PM-06/07 PRE-SCOPE
9a53c2577e8e25de6de63a830e9bab036521f040
```

The PM-06/07 terminal SHA is determined by remote Git after this write.

## Next

```text
PM-08
SECONDARY/SPECIALIST LANE QUALIFICATION
fresh gate required

PM-09 scoring NOT STARTED
PREFERRED NONE
SELECTED NONE
BACKEND NOT STARTED / DEFERRED
```