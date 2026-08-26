# Physical Model Result Register v1

- Status: **CURRENT PHYSICAL TARGET / RESULT LEDGER — TARGET ARCHITECTURE CLOSED / SELECTED / ACCEPTED / INTEGRATED INTO MAIN VIA PR #15**
- Current product/app name: **DANTE** (`LifeOS` is the previous working/project name retained in historical evidence and technical identifiers)
- Former workstream branch: `feature/physical-model` — **MERGED / AUTO-DELETED**
- Physical integration commit: `e6f191bad947388a44defe2c15f4939345084f58` via PR #15
- Primary finalists: **PostgreSQL 18.4 + TypeDB CE 3.12.3**
- PM-09 evidence-weighted score: **PostgreSQL 89.25 / TypeDB 80.00**
- Ranking sensitivity: **ROBUST / NOT SENSITIVITY-DEPENDENT / NOT PERFORMANCE-DEPENDENT**
- PM-10 Preferred: **PostgreSQL 18.4 / PASS-CONDITIONAL**
- PM-11 Selected: **PostgreSQL 18.4 + bounded companion target stack**
- PM-12 Accepted Physical Model: **ESTABLISHED**
- PM-13 architecture/documentation QA: **PASS**
- PM-14 branch/workstream closure: **COMPLETE**
- Protected-main integration after PM-14: **PR #15 COMPLETE**
- Current project progression after Physical closure: **backend CP1–CP5 CLOSED / INTEGRATED / DIRECT QA PASS; CP6 Concrete Persistence Readiness ACTIVE**
- Physical business-semantic HG direct execution: **PASS 0 / VERIFIED-RUN SCORE NOT AVAILABLE**
- Business persistence schema: **NOT IMPLEMENTED**
- Post-closure traceability maintenance: **2026-08-22 — SC-017/SC-018 labels reconciled to the canonical scenario corpus; no Physical decision or validation obligation changed.**

## Result-language rule

```text
OFFICIAL CLAIM != DIRECT EXECUTION
PUBLIC BENCHMARK != DANTE BENCHMARK
EVIDENCE-QUALIFIED != DIRECT PASS
EVIDENCE-WEIGHTED SCORE != VERIFIED-RUN SCORE
PREFERRED != SELECTED
SELECTED != DEPLOYED
SELECTED != DIRECT PASS
SECONDARY != CANONICAL
LOCAL != CANONICAL
RUNTIME != DOMAIN HISTORY
NOT RUN != PASS
CP3 TECHNICAL QA != BUSINESS-SEMANTIC HG PASS
```

## Physical phase state

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
PM-11   EXPLICIT USER-APPROVED TARGET STACK SELECTION COMPLETE
PM-12   ACCEPTED PHYSICAL MODEL COMPLETE
PM-13   CLEAN-ROOM ARCHITECTURE/DOCUMENTATION QA PASS
PM-14   TARGET-ARCHITECTURE BRANCH / WORKSTREAM CLOSURE COMPLETE
PR #15  PROTECTED-MAIN INTEGRATION COMPLETE
```

## Selected primary

### PostgreSQL 18.4

```text
PM-09 SCORE
89.25 / 100

RANKING
ROBUST

PM-10
PREFERRED / PASS-CONDITIONAL

PM-11
SELECTED — CANONICAL PRIMARY

PM-12
ACCEPTED PHYSICAL MODEL PRIMARY

PM-13
COHERENT / QA PASS
```

Primary reasons remain:

- accepted PM-02 mapping preserves DANTE semantics;
- mature integrity and transaction/concurrency primitives;
- strongest recovery/HA/evolution envelope among finalists;
- reporting, traversal, geospatial, lexical and vector capabilities remain in one primary ecosystem;
- lower permanent operational/topology/exit burden than the TypeDB finalist path.

### TypeDB CE 3.12.3

```text
PM-09 SCORE
80.00 / 100

ROLE
HISTORICAL PRINCIPAL SEMANTIC RUNNER-UP

PM-10
NOT PREFERRED

PM-11
NOT SELECTED
```

TypeDB retains strong relation/role/n-ary semantic fit but is not part of the accepted target architecture.

Prior challengers XTDB 2.1.0 and SurrealDB Community 3.2.3 remain historical evidence only.

## Direct execution truth — distinguish Physical phase from current backend foundation

### Physical-phase business-semantic benchmark snapshot

PM-11/12/13/14 did not execute the selected stack against the DANTE semantic/destructive benchmark corpus:

```text
P0 HG-01..HG-12       NOT RUN
P1 HG-01..HG-12       NOT RUN
P2 HG-01..HG-12       NOT RUN
P3 HG-01..HG-12       NOT RUN

DIRECT SEMANTIC HG PASS  0
LOW/BASE/HIGH            NOT RUN
SEMANTIC RESTORE CORPUS  NOT RUN
REAL BUSINESS V1→V2      NOT RUN
FAILURE INJECTION         NOT RUN
POWERSYNC                  NOT RUN
RESTATE                    NOT RUN
OBJECT RECOVERY            NOT RUN
SOLVER                     NOT RUN
VERIFIED-RUN SCORE        NOT AVAILABLE
```

These remain truthful unexecuted business/system obligations unless later exact artifacts directly discharge them.

### Current technical implementation after Physical closure

Subsequent CP1–CP5 work has directly established a technical backend persistence substrate:

```text
BACKEND CP1–CP5                 CLOSED / INTEGRATED / DIRECT QA PASS
LOCAL POSTGRESQL 18.4           MATERIALIZED / DIRECT QA PASS
POSTGIS 3.6.4                   LOCAL ENVELOPE DIRECT QA PASS
PGVECTOR 0.8.6                  LOCAL ENVELOPE DIRECT QA PASS
PG_TRGM / UNACCENT              LOCAL ENVELOPE DIRECT QA PASS
PG_STAT_STATEMENTS              LOCAL ENVELOPE DIRECT QA PASS
SQLALCHEMY 2 ASYNC              MATERIALIZED
PSYCOPG 3                       MATERIALIZED
ALEMBIC                         MATERIALIZED / TECHNICAL BASELINE PASS
SCHEMA dante                    MATERIALIZED
OWNER/MIGRATOR/RUNTIME ROLES    MATERIALIZED / DIRECT QA PASS
REAL POSTGRESQL TEST HARNESS     MATERIALIZED / DIRECT QA PASS
BUSINESS PERSISTENCE SCHEMA      NOT IMPLEMENTED
VERTICAL #1                      NOT IMPLEMENTED
```

Therefore old PM-era phrases such as `DATABASE DEPLOYMENT NOT STARTED` are historical phase-time evidence, not current project status. CP3 technical QA still does not manufacture semantic HG/PSV PASS.

## PM-09 score retained

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

Sensitivity remains robust. `SC-013` and PM-04B remain closed because the selected ranking is not performance-dependent.

## Selected target stack register

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

ASYNC CLASS A
PostgreSQL transactional outbox + bounded worker

DURABLE CLASS B
Restate runtime
Restate Python SDK 1.0.3
Restate Server 1.7.2 self-hosted/reproducible subject
Restate Cloud EU allowed managed deployment
Restate global deployment default NONE

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

## Restate deployment disposition

```text
RESTATE TECHNOLOGY
SELECTED

SELF-HOSTED
FIRST-CLASS DEPLOYMENT OPTION

CLOUD EU
ALLOWED MANAGED DEPLOYMENT OPTION

GLOBAL DEFAULT
NONE
```

Current Python path must not assume TypeScript-only client-side journal encryption. Journal minimization and the later privacy/operability deployment review remain mandatory carry-forward conditions.

## Technology exclusions

The accepted target excludes:

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
Zero
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
SC-030 actual DANTE V1->V2 evolution
SC-031 destructive restore + semantic verification
SC-032 capacity/backpressure
WL-H12 system-level non-interference
SC-017 search hidden-result non-interference
SC-018 FTS mixed filter/query correctness under applicable Visibility/user/scope filtering
SC-019 filtered vector recall
SC-020/021 projection freshness/deletion propagation
PowerSync replication/offline conflict/local encryption
Restate crash/replay/versioning/governance/deployment privacy
R2/S3 object recovery/deletion
PostGIS/PgBouncer interactions
OR-Tools status/governance corpus
observability privacy
```

`SC-017` and `SC-018` retain their canonical names from the Physical Benchmark Scenario Corpus and are distinct obligations.

All remain `NOT RUN` until the corresponding selected-stack/business artifact exists and is directly executed.

## PM-13 clean-room result

```text
BLOCKING ARCHITECTURE DEFECTS      0
CANONICAL-AUTHORITY CONFLICTS      0
UNAPPROVED TECHNOLOGIES            0
FALSE DIRECT PASS CLAIMS           0
LOST PSV OBLIGATIONS               0
DOMAIN/LOGICAL IMPLICIT REOPENS    0

VERDICT
QA PASS — ARCHITECTURE / DOCUMENTATION COHERENCE
```

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
PM-10  pm-10-recommendation-v1.md + final-stack-* + recommendation/*
PM-11  pm-11-explicit-selection-v1.md
PM-12  pm-12-accepted-physical-model-v1.md
PM-13  pm-13-clean-room-qa-v1.md
PM-14  pm-14-closure-v1.md
```

## Current boundary

```text
PHYSICAL TARGET
CLOSED / SELECTED / ACCEPTED
INTEGRATED INTO MAIN VIA PR #15

SELECTED CANONICAL PRIMARY
PostgreSQL 18.4

SELECTED TARGET COMPANION STACK
ESTABLISHED

PM-13 QA
PASS

PM-14
HISTORICAL PHYSICAL WORKSTREAM CLOSURE COMPLETE

BACKEND FOUNDATION CP1–CP5
CLOSED / INTEGRATED / DIRECT QA PASS

CP6 CONCRETE PERSISTENCE READINESS
ACTIVE / DESIGN-FIRST
feature/logical-postgresql

BUSINESS PERSISTENCE
NOT IMPLEMENTED

CP6 TERMINAL BOUNDARY
CONCRETE POSTGRESQL FOUNDATION CLOSED / READY
VERTICAL #1 SELECTED / EXACTLY DESIGNED / READY FOR IMPLEMENTATION

VERTICAL #1 IMPLEMENTATION
SEPARATE POST-CP6 AUTHORIZED PHASE

DIRECT BUSINESS-SEMANTIC HG PASS
0 unless qualifying scenarios are actually executed
```
