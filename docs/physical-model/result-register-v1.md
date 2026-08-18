# Physical Model Result Register v1

- Status: **CURRENT — PM-10 COMPLETE / PM-11 NEXT**
- Workstream: `feature/physical-model`
- Primary finalists: **PostgreSQL 18.4 + TypeDB CE 3.12.3**
- PM-09 evidence-weighted score: **PostgreSQL 89.25 / TypeDB 80.00**
- Ranking sensitivity: **ROBUST / NOT SENSITIVITY-DEPENDENT / NOT PERFORMANCE-DEPENDENT**
- PM-10 Preferred: **PostgreSQL 18.4 / PASS-CONDITIONAL**
- PM-10 Companion stack: **RECOMMENDED / PASS-CONDITIONAL**
- Direct execution: **NOT STARTED**
- Verified-run benchmark score: **NOT AVAILABLE**
- Selected: **NONE**

## Result-language rule

```text
OFFICIAL CLAIM != DIRECT EXECUTION
PUBLIC BENCHMARK != LIFEOS BENCHMARK
EVIDENCE-QUALIFIED != DIRECT PASS
EVIDENCE-WEIGHTED SCORE != VERIFIED-RUN SCORE
PREFERRED != SELECTED
SECONDARY != CANONICAL
LOCAL != CANONICAL
RUNTIME != DOMAIN HISTORY
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
PM-10   FINAL STACK RECOMMENDATION COMPLETE
PM-11   NEXT / EXPLICIT SELECTION
PM-12+  NOT STARTED
```

## Primary recommendation

### PostgreSQL 18.4

```text
PM-09 SCORE
89.25 / 100

RANKING
ROBUST

PM-10
PREFERRED / PASS-CONDITIONAL

SELECTED
NONE
```

Primary reasons:

- accepted PM-02 mapping preserves LifeOS semantics;
- mature integrity and transaction/concurrency primitives;
- strongest self-hosted backup/recovery/HA/evolution envelope;
- reporting, traversal, geospatial, lexical and vector capabilities can remain in one primary ecosystem;
- lower operational/topology/exit burden than the TypeDB finalist path.

### TypeDB CE 3.12.3

```text
PM-09 SCORE
80.00 / 100

ROLE
PRINCIPAL SEMANTIC RUNNER-UP

PM-10
NOT PREFERRED

SELECTED
NONE
```

TypeDB retains the strongest pure relation/role/n-ary semantic fit. It is not preferred because the accepted LifeOS whole-system priority set gives material weight to concurrency, recovery, operations, evolution and topology simplicity.

### Prior challengers

```text
XTDB 2.1.0
not in PM-10 recommended primary stack
historical evidence retained

SurrealDB Community 3.2.3
not in PM-10 recommended primary stack
historical evidence retained
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
SQLITE/POWERSYNC         NOT RUN
RESTATE                  NOT RUN
OBJECT RECOVERY          NOT RUN
SOLVER                    NOT RUN
BENCHMARK HOST           HOLD / DORMANT
VERIFIED-RUN SCORE       NOT AVAILABLE
```

No PM-09 or PM-10 disposition is evidence that a direct hard gate ran.

## Phase-10 reconciliation retained

```text
VERIFIED-RUN BENCHMARK SCORE
requires direct applicable hard-gate PASS + direct artifacts

EVIDENCE-WEIGHTED DECISION SCORE
allowed after evidence exhaustion and 0 ranking-critical execution-worthy gaps
```

The Phase-10 hard gates and 100-point weights remain unchanged.

## PM-09 base score retained

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

Sensitivity remains robust. `SC-013` and PM-04B remain closed because the recommendation is not performance-dependent.

## PM-10 companion stack register

```text
POSTGRESQL-ADJACENT
PostGIS 3.6.4
pgvector 0.8.6
native FTS
pg_trgm
unaccent
pg_stat_statements
PgBouncer 1.25.2

OFFLINE / SYNC
PowerSync Service 1.25.0 Open Edition
encrypted SQLite local state
PostgreSQL-backed PowerSync bucket storage
explicit client-safe sync projections

ASYNC
PostgreSQL transactional outbox + bounded worker
Restate Cloud EU for Class-B durable execution
Restate Python SDK 1.0.3
Restate Server 1.7.2 reproducible local/self-hosted subject

OBJECT
Cloudflare R2 Standard / EU jurisdiction / private

BACKUP
pgBackRest 2.59.0 -> AWS S3 eu-south-1
R2 object backup -> separate AWS S3 eu-south-1 bucket

SOLVER
OR-Tools 9.15 CP-SAT

OBSERVABILITY
OpenTelemetry
Grafana Alloy 1.18.0
Grafana Cloud EU
pg_stat_statements
```

## State-ownership register

```text
canonical truth                 PostgreSQL
material history               PostgreSQL
geospatial query               PostGIS over PostgreSQL data
lexical search                 PostgreSQL derived/query state
vector retrieval               pgvector derived state
local/offline state            encrypted SQLite / noncanonical
sync buckets/projections       PowerSync / noncanonical / rebuildable
bounded async                  PG outbox/worker runtime
long durable execution         Restate runtime
raw object bytes               R2
object metadata/authority      PostgreSQL
DB backup                      pgBackRest/S3 recovery copy
object backup                  S3 recovery copy
solver output                  OR-Tools candidate/derived state
telemetry                      OTel/Grafana operational state
```

## Technology exclusions

PM-10 explicitly excludes from the proposed accepted stack:

```text
TypeDB/XTDB/SurrealDB as primary
Neo4j
Qdrant
OpenSearch
TimescaleDB
Redis/Valkey
Kafka
RabbitMQ
NATS
Debezium
dedicated event store
universal event sourcing
Temporal
DBOS
Celery + broker
Zero sync
Electric as full mutation/sync engine
CRDT/local-first canonical authority
MongoDB for PowerSync
large bytea object storage
public R2
separate vector/graph/search servers
data lake/Spark/Hudi
pg_cron as workflow system
Object Lock Compliance as default
```

Reintroduction requires a later explicit architecture decision.

## Post-selection proof register

The authoritative expanded register is:

```text
docs/physical-model/recommendation/post-selection-validation-register-v1.md
```

Core obligations include:

```text
SC-011 old-backup anti-resurrection
SC-030 actual LifeOS V1->V2 evolution
SC-031 destructive restore + semantic verification
SC-032 capacity/backpressure
WL-H12 system-level non-interference
SC-017/018 search non-interference
SC-019 filtered vector recall
SC-020/021 projection freshness/deletion propagation
PowerSync replication/offline conflict/local encryption
Restate crash/replay/versioning/governance
R2/S3 object recovery/deletion
PostGIS/PgBouncer interactions
OR-Tools status/governance corpus
observability privacy
```

All remain `NOT RUN` until direct selected-stack artifacts exist.

## Evidence paths

```text
PM-01  pm-01-technology-landscape-v1.md
PM-02  pm-02-primary-mapping-overview-v1.md + mappings/*
PM-03  pm-03-semantic-hard-gate-preflight-v1.md + preflight/*
PM-04A pm-04-external-evidence-sufficiency-v1.md + evidence/*
PM-05  pm-05-correctness-evidence-qualification-v1.md + qualification/*
PM-06/07 pm-06-07-joint-finalist-qualification-v1.md + related records
PM-08  pm-08-secondary-lanes-v1.md + secondary/*
PM-09  pm-09-scoring-sensitivity-v1.md + scoring/*
PM-10  pm-10-recommendation-v1.md
       final-stack-audit-v1.md
       final-stack-capability-matrix-v1.md
       final-stack-simulation-v1.md
       recommendation/*
```

## Next

```text
PM-10 COMPLETE

PREFERRED
PostgreSQL 18.4 / PASS-CONDITIONAL

COMPANION STACK
RECOMMENDED / PASS-CONDITIONAL

SELECTED
NONE

NEXT
PM-11 explicit selection

BACKEND
NOT STARTED / DEFERRED
```
