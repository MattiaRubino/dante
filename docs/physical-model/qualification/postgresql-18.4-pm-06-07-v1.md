# PostgreSQL 18.4 — PM-06/07 Finalist Qualification v1

- Status: **PRIMARY FINALIST / OVERALL LEAD STRENGTHENED**
- Subject: PostgreSQL 18.4 / self-hosted single-node qualification subject / psycopg 3.3.4
- Direct execution: **NOT RUN**
- Preferred: **NONE**
- Selected: **NONE**

## PM-06 scale/performance

```text
VIABILITY            HIGH CONFIDENCE
LOW/BASE/HIGH        NOT RUN
LOCAL BENCHMARK      NOT ADMITTED
REVERSAL SIGNAL      NONE
```

The accepted LifeOS mapping has no known scale property requiring full-history replay for normal current-state access. PostgreSQL's indexing, query planning, transaction and replication ecosystem provides a mature path for the relevant workload families without semantic collapse.

A laptop benchmark would currently produce host-specific numbers without an accepted SLA and would not answer the architectural question.

## PM-07 recovery/evolution

```text
BACKUP BREADTH       STRONG
PITR                 NATIVE WAL/ARCHIVE PATH
INCREMENTAL BASE     SUPPORTED
REPLICATION          PHYSICAL + LOGICAL
STANDBY/FAILOVER     SUPPORTED PRIMITIVES
MAJOR UPGRADE        pg_upgrade / dump-restore / logical replication paths
DIRECT RESTORE       NOT RUN
DIRECT MIGRATION     NOT RUN
```

PostgreSQL 18 documents SQL dump, filesystem backup and continuous archiving/PITR as distinct backup families. `pg_basebackup` supports full and incremental base backups. Streaming replication is asynchronous by default and can be configured synchronously; standby/failover primitives are mature.

## LifeOS-specific remaining obligations

- heterogeneous address anchors must remain technical only;
- transaction strength must be chosen per consequential invariant;
- RLS is a useful mechanism but not a complete WL-H12 proof;
- old-backup anti-resurrection remains post-selection implementation validation;
- actual LifeOS V1→V2 mapping migration remains post-selection implementation validation;
- semantic post-restore verification remains post-selection implementation validation.

## Cost / topology

PostgreSQL remains zero-license-cost under the PostgreSQL License. Core self-hosted replication/standby/recovery primitives do not require a paid database edition. Production HA still requires infrastructure and operations; this is not treated as free infrastructure.

## Comparative judgment

PostgreSQL's main disadvantage versus TypeDB remains lower semantic-native expressiveness for relation/role/n-ary modeling. Its advantage is that the accepted LifeOS mapping preserves those semantics while retaining materially stronger integrity, operations, recovery, ecosystem and topology maturity.

```text
PM-06 VERDICT
ADVANCE

PM-07 VERDICT
ADVANCE — MATERIAL OPERATIONS/RECOVERY ADVANTAGE

CURRENT COMPARATIVE POSITION
#1 / OVERALL LEAD STRENGTHENED

PREFERRED
NONE

SELECTED
NONE
```

## Reopen/direct-test trigger

Direct performance or destructive qualification should be reopened only if PM-09 becomes sensitivity-dependent on a concrete metric, or if implementation evidence contradicts the current engine/mapping assumptions.

## Primary official sources

- https://www.postgresql.org/docs/18/backup.html
- https://www.postgresql.org/docs/18/continuous-archiving.html
- https://www.postgresql.org/docs/18/app-pgbasebackup.html
- https://www.postgresql.org/docs/18/high-availability.html
- https://www.postgresql.org/docs/current/warm-standby.html
- https://www.postgresql.org/docs/18/upgrading.html
- https://www.postgresql.org/docs/18/pgupgrade.html
