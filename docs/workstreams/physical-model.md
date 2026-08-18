# Workstream — Physical Model

- Status: **TARGET ARCHITECTURE CLOSED / SELECTED / ACCEPTED — PM-14 BRANCH CLOSURE COMPLETE / INTEGRATED INTO MAIN VIA PR #15**
- Former workstream branch: `feature/physical-model` — **MERGED / AUTO-DELETED**
- Main integration: `e6f191bad947388a44defe2c15f4939345084f58`
- Main baseline during workstream: `3de84bb49f9cef30e88e9bde4961ed84335daa79`
- Started: 2026-08-18
- Domain: **CLOSED / INTEGRATED / UNCHANGED**
- Logical: **CLOSED / INTEGRATED / WL-H01..WL-H12 ACTIVE / UNCHANGED**
- PM-00: **QA PASS**
- PM-01: **PASS-CONDITIONAL**
- PM-02: **PRIMARY MAPPING DESIGN COMPLETE**
- PM-03: **STATIC PREFLIGHT COMPLETE / 0 STATIC REJECTS**
- PM-04A: **EVIDENCE SUFFICIENCY COMPLETE / 48 OF 48 CELLS / 0 EXECUTION-WORTHY GAPS**
- PM-04B: **NOT ADMITTED / HARNESS NOT STARTED**
- PM-05: **CORRECTNESS/DESTRUCTIVE EVIDENCE QUALIFICATION COMPLETE**
- PM-06: **SCALE/PERFORMANCE EVIDENCE QUALIFICATION COMPLETE / DIRECT RUN NOT EXECUTED**
- PM-07: **RECOVERY/EVOLUTION/FAILURE EVIDENCE QUALIFICATION COMPLETE / DIRECT RUN NOT EXECUTED**
- PM-08: **SECONDARY/SPECIALIST LANE QUALIFICATION COMPLETE**
- PM-09: **EVIDENCE-WEIGHTED SCORING + SENSITIVITY COMPLETE**
- PM-10: **FINAL STACK RECOMMENDATION COMPLETE**
- PM-11: **EXPLICIT USER-APPROVED TARGET STACK SELECTION COMPLETE**
- PM-12: **ACCEPTED PHYSICAL MODEL COMPLETE**
- PM-13: **CLEAN-ROOM ARCHITECTURE/DOCUMENTATION QA PASS**
- PM-14: **BRANCH CLOSURE COMPLETE**
- Selected canonical primary: **PostgreSQL 18.4**
- Direct implementation validation: **NOT STARTED / DIRECT HG PASS 0 / VERIFIED-RUN SCORE NOT AVAILABLE**
- Backend Foundation: **NOT STARTED / DEFERRED**
- Development Profile v0: **NOT STARTED / SEPARATE NEXT OPERATIONAL SCOPE**

## 1. Purpose

Terminal save-game for the Physical Model target-architecture workstream. A new chat/agent must be able to resume from repository truth without reconstructing conversation history.

The workstream selected and accepted the target Physical architecture and integrated it into protected `main` through PR #15. It did **not** implement the production backend, deploy the selected stack, discharge the direct implementation validation register or decide the later Development Profile v0.

## 2. Mandatory continuation bootstrap

For any later work that consumes or reopens the Physical target:

1. verify current `main` and relevant active branch/PR refs;
2. read root `README.md`;
3. read `docs/README.md` and `docs/PROJECT-STATUS.md`;
4. read `docs/development/agent-operating-manual.md`;
5. read `docs/development/operating-rules.md`;
6. read `docs/development/documentation-and-handoff.md`;
7. read `docs/development/branching-and-environments.md`;
8. read `docs/development/repository-engineering-safety.md`;
9. read this file;
10. read `docs/physical-model/README.md`;
11. read `docs/physical-model/pm-11-explicit-selection-v1.md`;
12. read `docs/physical-model/pm-12-accepted-physical-model-v1.md`;
13. read `docs/physical-model/pm-13-clean-room-qa-v1.md`;
14. read `docs/physical-model/pm-14-closure-v1.md` as historical pre-merge closure evidence;
15. read `docs/physical-model/recommendation/post-selection-validation-register-v1.md`;
16. read older PM-01..PM-10 evidence only when rationale/history is material;
17. read complete CLOSED Domain/Logical authority when semantics are involved;
18. verify current external product/version/deployment facts from primary sources where material;
19. issue a fresh exact write gate before repository mutation.

Conversation memory is secondary to repository truth.

## 3. Non-negotiable guardrails

```text
SEMANTIC OWNER != IMPLEMENTATION MECHANISM
DOMAIN TERM != ENGINE
ADDRESSABILITY != DOMAIN IDENTITY
STORAGE TOKEN != MaterialStateRef
CANONICAL != PROVIDER / DERIVED / SECURITY STATE
SECONDARY != CANONICAL
LOCAL != CANONICAL
RUNTIME != DOMAIN HISTORY
MISSING != FALSE
EXTERNAL EVIDENCE != DIRECT LIFEOS RUN
EVIDENCE-WEIGHTED SCORE != VERIFIED-RUN SCORE
PREFERRED != SELECTED
SELECTED != DEPLOYED
SELECTED != DIRECT PASS
NOT RUN != PASS
```

Never introduce by convenience:

```text
universal Entity/Thing root
universal semantic Relationship/edge root
generic EAV/property-bag canonical kernel
provider IDs/revisions as canonical identity/material state
storage/MVCC/system-time/changefeed token as MaterialStateRef
technical AuthZ as Domain Authority/Consent
AI/solver result as accepted canonical effect
universal last-write-wins
local-first canonical authority
runtime workflow state as Domain history
```

`WL-H01..WL-H12` remain active and non-negotiable.

## 4. Historical checkpoints

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

PM-06/07 terminal
1e19793fdb9f51ba510f00ac4c927a6907e28c4b

PM-08 terminal
6aef5537edacff3e315d502a1bd3ede544dc149e

PM-09 terminal
016e4df07df9756d2c03d5582b489eed607aaecc

PM-10 terminal
4a988b115e445c726910ef5c3da7e2629d73eaf1

PROTECTED-MAIN INTEGRATION
PR #15
main e6f191bad947388a44defe2c15f4939345084f58
former feature/physical-model merged / auto-deleted
```

GitHub PR/merge history is the authoritative integration evidence.

## 5. Selection history

PM-01 admitted:

```text
PostgreSQL 18.4
TypeDB CE 3.12.3
XTDB 2.1.0
SurrealDB Community 3.2.3
```

PM-05 narrowed to PostgreSQL + TypeDB. PM-09 evidence score:

```text
PostgreSQL 89.25
TypeDB      80.00

RANKING
ROBUST
NOT SENSITIVITY-DEPENDENT
NOT PERFORMANCE-DEPENDENT
```

PM-10 established PostgreSQL as preferred. PM-11 received explicit user approval and selected the target stack. PM-12 established the Accepted Physical Model. PM-13 independently QA-checked architecture/documentation coherence and passed. PM-14 closed the branch-level target-architecture work. PR #15 integrated the closed result into protected `main`.

## 6. Accepted target stack

### Canonical

```text
PostgreSQL 18.4
SELECTED / ACCEPTED CANONICAL PRIMARY
```

### PostgreSQL capabilities

```text
PostGIS 3.6.4
pgvector 0.8.6
native FTS
pg_trgm
unaccent
pg_stat_statements
PgBouncer 1.25.2
```

### Offline / sync

```text
PowerSync Service 1.25.0 Open Edition
encrypted SQLite local state
PostgreSQL-backed PowerSync bucket storage
explicit client-safe sync projections
```

Offline rule:

```text
SQLite local copy != canonical truth
PowerSync arrival order != conflict resolution
consequential offline mutation -> LifeOS backend revalidation -> PostgreSQL
```

No universal consequential last-write-wins.

### Async / durable

```text
BOUNDED CLASS A
PostgreSQL transactional outbox + bounded worker

MATERIAL CLASS B
Restate runtime
Restate Python SDK 1.0.3
Restate Server 1.7.2 self-hosted/reproducible subject
Restate Cloud EU allowed managed deployment
```

Restate technology is selected; deployment is conditional:

```text
SELF-HOSTED
FIRST-CLASS

CLOUD EU
ALLOWED MANAGED OPTION

GLOBAL DEFAULT
NONE
```

Current client-side journal encryption for Restate Cloud is documented only for TypeScript while LifeOS targets Python. Journal minimization is mandatory; deployment choice remains a later privacy/operability profile decision.

### Object bytes

```text
Cloudflare R2 Standard
EU jurisdiction
private
```

PostgreSQL remains `ContentArtifact` authority. R2 stores raw bytes only.

### Recovery target

```text
pgBackRest 2.59.0
-> AWS S3 Standard eu-south-1
-> Versioning
-> Object Lock GOVERNANCE
-> finite policy-bound retention

R2 object backup
-> separate AWS S3 eu-south-1 repository
```

### Solver

```text
OR-Tools 9.15 CP-SAT
```

Candidate output only until accepted by applicable LifeOS semantics. `UNKNOWN != INFEASIBLE`.

### Observability

```text
OpenTelemetry
Grafana Alloy 1.18.0
Grafana Cloud EU
pg_stat_statements
```

Telemetry remains privacy-minimized operational state.

## 7. Canonical ownership summary

```text
canonical LifeOS truth/material history   PostgreSQL
geospatial capability                     PostGIS
lexical/vector retrieval                  PostgreSQL/pgvector derived state
local/offline state                       encrypted SQLite / noncanonical
sync projections                          PowerSync / noncanonical
bounded async                             PG outbox/worker
long durable execution                    Restate runtime / noncanonical
raw object bytes                          R2
object authority/metadata                 PostgreSQL
recovery copies                           S3 / noncanonical
solver output                             OR-Tools candidate
telemetry                                 OTel/Grafana operational
```

Canonical persistence authorities: **1**.

## 8. Direct execution truth

```text
DATABASE INSTANCE
NOT STARTED

FIXTURE/HARNESS
NOT STARTED

DIRECT HG-01..HG-12
NOT RUN ALL CANDIDATES

DIRECT HG PASS
0

LOW/BASE/HIGH
NOT RUN

RESTORE / MIGRATION / FAILURE INJECTION
NOT RUN

GRAPH / SEARCH / VECTOR / SQLITE / POWERSYNC / RESTATE / OBJECT / SOLVER DIRECT VALIDATION
NOT RUN

BENCHMARK HOST
HOLD / DORMANT

VERIFIED-RUN BENCHMARK SCORE
NOT AVAILABLE
```

Do not convert scoring, recommendation, selection, acceptance, clean-room QA, closure or protected-main integration into direct PASS.

## 9. Post-selection validation obligations

Authoritative register:

```text
docs/physical-model/recommendation/post-selection-validation-register-v1.md
```

It includes:

```text
SC-011 anti-resurrection
SC-030 V1->V2 evolution
SC-031 destructive semantic restore
SC-032 capacity/backpressure
WL-H12 non-interference
search/vector/projection filtering/freshness/deletion
PowerSync replication liveness / conflicts / local encryption
Restate crash/replay/versioning/governance/deployment privacy
R2/S3 object deletion/recovery
PostGIS/PgBouncer compatibility
pgBackRest archive/PITR
OR-Tools status/governance corpus
observability privacy
```

None is a direct PASS today unless separately executed and evidenced.

## 10. Technology exclusions

Not part of the accepted target:

```text
TypeDB/XTDB/SurrealDB primary
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
Electric as full LifeOS mutation/sync engine
CRDT/local-first canonical authority
MongoDB for PowerSync
large bytea as standard object store
public R2
separate vector/graph/search server
data lake/Spark/Hudi
pg_cron as workflow system
Object Lock Compliance as default
```

Reintroduction requires a new explicit architecture decision with material evidence.

## 11. PM-13 clean-room QA

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

## 12. Development Profile v0 boundary

The next separate operational design may decide:

```text
which selected components are active immediately
self-hosted vs managed where Physical permits both
free-tier/local development choices
accounts/credentials/environment setup
initial backup/observability activation
upgrade/production triggers
```

This is not a reopen of the target Physical Model. A selected component may be dormant in DEV without changing the accepted target.

## 13. Protected-main integration result

The closed Physical branch was integrated through the repository-protected path:

```text
feature/physical-model
→ PR #15
→ main e6f191bad947388a44defe2c15f4939345084f58
→ former head branch auto-deleted
```

Remote GitHub state verified the PR as merged and `main` at the merge commit. PM-14 is intentionally preserved as historical evidence of the branch state **before** this external integration action.

## 14. Current resume summary

```text
PHYSICAL MODEL TARGET
CLOSED / SELECTED / ACCEPTED

PROTECTED-MAIN INTEGRATION
COMPLETE VIA PR #15

MAIN
e6f191bad947388a44defe2c15f4939345084f58

FORMER BRANCH
feature/physical-model MERGED / AUTO-DELETED

SELECTED CANONICAL PRIMARY
PostgreSQL 18.4

SELECTED TARGET STACK
ESTABLISHED

PM-13
QA PASS

PM-14
BRANCH CLOSURE COMPLETE / HISTORICAL PRE-MERGE EVIDENCE

DIRECT HG PASS
0

VERIFIED-RUN SCORE
NOT AVAILABLE

BACKEND
NOT STARTED / DEFERRED

DEV-v0
NOT STARTED / NEXT SEPARATE OPERATIONAL SCOPE

NEXT
Development Profile v0
```
