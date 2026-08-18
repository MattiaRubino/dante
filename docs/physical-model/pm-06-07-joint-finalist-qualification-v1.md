# PM-06 + PM-07 Joint Finalist Qualification v1

- Status: **COMPLETE — EVIDENCE-FIRST / DIRECT EXECUTION NOT RUN**
- Workstream: `feature/physical-model`
- PRE-SCOPE: `9a53c2577e8e25de6de63a830e9bab036521f040`
- Finalists: **PostgreSQL 18.4 / TypeDB CE 3.12.3**
- Benchmark host: **HOLD / DORMANT**
- Local/server execution: **NOT ADMITTED**
- Preferred: **NONE**
- Selected: **NONE**

## Purpose

Operate PM-06 and PM-07 as one evidence campaign while preserving separate result layers:

```text
PM-06
scale / performance / resource / saturation evidence

PM-07
recovery / backup / restore / evolution / failure / operations evidence
```

The campaign exists to answer one question:

> Can scale/performance or recovery/evolution evidence materially reverse the PostgreSQL-vs-TypeDB finalist ordering established by PM-05?

## Method

Evidence priority:

```text
1. exact-version/edition official documentation
2. reproducible public benchmark evidence with limitations disclosed
3. production architecture/scale evidence
4. known structural topology/resource constraints
5. LifeOS mapping consequences
6. direct execution only for a residual ranking-critical question
```

Direct execution admission requires all of:

```text
unresolved after external evidence
+ material to recommendation
+ test can actually resolve it
+ result could change ranking or an acceptance condition
```

## Exact finalist subjects

### P0 PostgreSQL

```text
PostgreSQL 18.4
self-hosted single-node qualification subject
psycopg 3.3.4
PostgreSQL License
```

### P1 TypeDB

```text
TypeDB Community Edition 3.12.3
self-hosted single-node qualification subject
official driver 3.12.3
Community Edition / zero direct license cost
```

Cloud/Enterprise capabilities do not silently count as CE capabilities.

## PM-06 result

```text
POSTGRESQL
SCALE/PERFORMANCE VIABLE
confidence HIGH on engine maturity / broad workload envelope

TYPEDB CE
SCALE/PERFORMANCE VIABLE
confidence MEDIUM-HIGH for finalist viability
single-query execution currently single-threaded
scale-up depends on concurrent queries/transactions and resource sizing
CE horizontal scaling unavailable

DIRECT LOW/BASE/HIGH
NOT RUN

PERFORMANCE REVERSAL SIGNAL
NONE FOUND
```

No credible evidence says TypeDB is too slow for LifeOS, and no credible evidence says a laptop CRUD benchmark would choose the architecture responsibly. Therefore PM-06 does not admit local execution.

## PM-07 result

```text
POSTGRESQL
RECOVERY/EVOLUTION/OPERATIONS ADVANTAGE
confidence HIGH

TYPEDB CE
RECOVERY/EVOLUTION VIABLE
but higher self-hosted operational burden
confidence MEDIUM-HIGH

DIRECT RESTORE
NOT RUN

DIRECT MIGRATION
NOT RUN

FAILURE INJECTION
NOT RUN
```

PostgreSQL has mature native paths for SQL/file/continuous-archive backup, WAL/PITR, full/incremental base backup, physical/logical replication, standby/failover options, `pg_upgrade`, and logical-replication migration.

TypeDB self-hosted backup implementation is user-owned; documented options are disk snapshots or export/import and are not incremental. TypeDB CE is single-node. Cluster replication/horizontal read scaling belongs to TypeDB Cloud/Enterprise. TypeDB export/import is explicitly designed for cross-version migration and provides a credible evolution path, but with greater operational burden for the accepted zero-cost CE subject.

## LifeOS scenario carry-forward

### SC-013 — deep-history current-state scale

```text
STATUS
NO DIRECT RUN ADMITTED

WHY
both finalists are viable; current evidence gives no ranking-critical performance uncertainty

REOPEN
only if PM-09 sensitivity becomes materially performance-dependent
```

### SC-011 — redaction + old-backup anti-resurrection

```text
STATUS
POST-SELECTION IMPLEMENTATION VALIDATION
NOT EXECUTED PASS
```

This is primarily a LifeOS restore/reconciliation policy proof. Running it twice before selection would not erase the documented operational difference between finalists.

### SC-030 — V1 -> V2 evolution with historical references

```text
STATUS
POST-SELECTION IMPLEMENTATION VALIDATION
NOT EXECUTED PASS
```

Both finalists have viable engine evolution paths. The remaining proof is the actual selected LifeOS mapping migration.

### SC-031 — backup/restore semantic verification

```text
STATUS
POST-SELECTION IMPLEMENTATION VALIDATION
NOT EXECUTED PASS
```

Engine backup capability is evidence-qualified; semantic verification belongs to the selected implementation.

### SC-032 — capacity/backpressure

```text
STATUS
POST-SELECTION IMPLEMENTATION VALIDATION / OBSERVABILITY
NOT EXECUTED PASS
```

No current residual capacity question is capable of choosing PostgreSQL vs TypeDB more reliably than the already-known topology/operability evidence.

## Comparative conclusion

```text
POSTGRESQL
OVERALL LEAD STRENGTHENED

TYPEDB
SEMANTIC ADVANTAGE PRESERVED
OVERALL GAP WIDENS ON OPERATIONS/RECOVERY/TOPOLOGY
```

Why PostgreSQL strengthens its lead:

1. no semantic hard blocker found in the accepted mapping;
2. strong integrity and Serializable primitives;
3. mature backup/PITR/replication/failover ecosystem in the zero-cost self-hosted subject;
4. broad upgrade/migration options;
5. fewer special operational conditions for a canonical primary;
6. no evidence that TypeDB performance advantage is needed to compensate.

Why TypeDB remains a serious finalist:

1. strongest relation/role/n-ary semantic expression;
2. schema constraints map naturally to important LifeOS relation semantics;
3. scale-up path and concurrent-query model remain viable;
4. export/import gives a credible cross-version migration mechanism;
5. it could still win if PM-09 demonstrates that semantic simplicity/evolvability materially outweighs its operational/concurrency burden.

## Execution admission result

```text
PM-06 LOCAL PERFORMANCE RUNS       0 ADMITTED
PM-07 DESTRUCTIVE RUNS             0 ADMITTED
PM-04B REOPEN                      NO
BENCHMARK HOST                     HOLD / DORMANT
DIRECT LOW/BASE/HIGH              NOT RUN
DIRECT RESTORE                    NOT RUN
DIRECT MIGRATION                  NOT RUN
DIRECT FAILURE INJECTION          NOT RUN
```

## Source ledger

PostgreSQL official:

- https://www.postgresql.org/docs/18/backup.html
- https://www.postgresql.org/docs/18/continuous-archiving.html
- https://www.postgresql.org/docs/18/app-pgbasebackup.html
- https://www.postgresql.org/docs/18/high-availability.html
- https://www.postgresql.org/docs/current/warm-standby.html
- https://www.postgresql.org/docs/18/upgrading.html
- https://www.postgresql.org/docs/18/pgupgrade.html

TypeDB official:

- https://typedb.com/docs/core-concepts/typedb/vertical-scaling/
- https://typedb.com/docs/core-concepts/typedb/horizontal-scaling/
- https://typedb.com/docs/maintenance-operation/typedb-backups/
- https://typedb.com/docs/maintenance-operation/database-export-import/
- https://typedb.com/docs/maintenance-operation/typedb-upgrades/

Exact TypeDB 3.12.3 release evidence is also retained through the official `typedb/typedb` release notes reviewed during this gate.

## Boundary

This result is **not PM-09 scoring**, does not create `PREFERRED`, and does not select PostgreSQL.

```text
FINALISTS
PostgreSQL + TypeDB

CURRENT COMPARATIVE LEADER
PostgreSQL

PREFERRED
NONE

SELECTED
NONE

NEXT
PM-08 secondary/specialist lanes after fresh gate
```