# Physical Model

- Status: **CLOSED AT TARGET-ARCHITECTURE LEVEL — SELECTED / ACCEPTED / INTEGRATED INTO MAIN VIA PR #15**
- Current product/app name: **DANTE** (`LifeOS` is the previous working/project name retained in historical evidence and technical identifiers)
- Former workstream branch: `feature/physical-model` — **MERGED / AUTO-DELETED**
- Physical integration commit: `e6f191bad947388a44defe2c15f4939345084f58` via PR #15
- Main baseline during workstream: `3de84bb49f9cef30e88e9bde4961ed84335daa79`
- PM-00: **QA PASS**
- PM-01: **PASS-CONDITIONAL**
- PM-02: **COMPLETE**
- PM-03: **STATIC COMPLETE / 0 REJECTS**
- PM-04A: **COMPLETE / 0 EXECUTION-WORTHY GAPS**
- PM-04B: **NOT ADMITTED**
- PM-05: **COMPLETE**
- PM-06: **EVIDENCE QUALIFICATION COMPLETE / DIRECT PERFORMANCE NOT RUN**
- PM-07: **EVIDENCE QUALIFICATION COMPLETE / DIRECT DESTRUCTIVE RUNS NOT RUN**
- PM-08: **SECONDARY/SPECIALIST QUALIFICATION COMPLETE**
- PM-09: **EVIDENCE-WEIGHTED SCORING + SENSITIVITY COMPLETE**
- PM-10: **FINAL STACK RECOMMENDATION COMPLETE**
- PM-11: **EXPLICIT TARGET STACK SELECTION COMPLETE**
- PM-12: **ACCEPTED PHYSICAL MODEL COMPLETE**
- PM-13: **CLEAN-ROOM ARCHITECTURE/DOCUMENTATION QA PASS**
- PM-14: **BRANCH / WORKSTREAM CLOSURE COMPLETE**
- Protected-main integration after PM-14: **PR #15 COMPLETE**
- Selected canonical primary: **PostgreSQL 18.4**
- Selected target companion stack: **ESTABLISHED**
- Direct implementation execution: **NOT STARTED / DIRECT HG PASS 0 / VERIFIED-RUN SCORE NOT AVAILABLE**
- Backend Foundation: **NOT STARTED / DEFERRED**
- Development Profile v0: **NOT STARTED / SEPARATE NEXT OPERATIONAL SCOPE**

## Purpose

This directory contains the evidence, selection and accepted target Physical architecture that translates the CLOSED DANTE Domain + Logical Model into bounded implementation mechanisms without weakening semantic ownership.

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
→ final stack audit
→ recommendation
→ explicit selection
→ Accepted Physical Model
→ clean-room QA
→ branch/workstream closure
→ protected-main lifecycle integration via PR #15
```

## Current authority order

For current target architecture read:

1. [`pm-11-explicit-selection-v1.md`](pm-11-explicit-selection-v1.md) — explicit selected target stack;
2. [`pm-12-accepted-physical-model-v1.md`](pm-12-accepted-physical-model-v1.md) — accepted Physical ownership/topology contract;
3. [`pm-13-clean-room-qa-v1.md`](pm-13-clean-room-qa-v1.md) — architecture/documentation clean-room QA evidence;
4. [`pm-14-closure-v1.md`](pm-14-closure-v1.md) — historical branch/workstream closure evidence produced before PR #15;
5. [`recommendation/post-selection-validation-register-v1.md`](recommendation/post-selection-validation-register-v1.md) — mandatory direct implementation-validation carry-forward;
6. [`result-register-v1.md`](result-register-v1.md) — current result ledger;
7. [`../workstreams/physical-model.md`](../workstreams/physical-model.md) — workstream closure/handoff.

PM-01..PM-10 remain evidence/rationale history and must not override later PM-11/12 current selected truth. PM-14 remains truthful historical closure evidence for the state before protected-main integration.

## Non-negotiable barriers

```text
SEMANTIC OWNER != IMPLEMENTATION MECHANISM
ADDRESSABILITY != DOMAIN IDENTITY
STORAGE TOKEN != MaterialStateRef
CANONICAL != PROVIDER / DERIVED / SECURITY STATE
SECONDARY != CANONICAL
LOCAL != CANONICAL
RUNTIME != DOMAIN HISTORY
MISSING != FALSE
EVIDENCE-QUALIFIED != EXECUTED PASS
EVIDENCE-WEIGHTED SCORE != VERIFIED-RUN SCORE
PUBLIC BENCHMARK != DANTE BENCHMARK
FINALIST != PREFERRED
PREFERRED != SELECTED
SELECTED != DEPLOYED
SELECTED != DIRECT PASS
```

No universal Entity/Thing/EAV/generic-edge canonical shortcut is accepted.

## Accepted target stack

```text
CANONICAL PRIMARY
PostgreSQL 18.4

POSTGRESQL CAPABILITIES
PostGIS 3.6.4
pgvector 0.8.6
native FTS
pg_trgm
unaccent
pg_stat_statements
PgBouncer 1.25.2

OFFLINE / SYNC
PowerSync Service 1.25.0 Open Edition
encrypted SQLite
PostgreSQL-backed PowerSync bucket storage
explicit client-safe sync projections

BOUNDED ASYNC
PostgreSQL transactional outbox + bounded worker

DURABLE CLASS-B
Restate runtime
Restate Python SDK 1.0.3
Restate Server 1.7.2 self-hosted/reproducible subject
Restate Cloud EU allowed managed deployment
GLOBAL RESTATE DEPLOYMENT DEFAULT NONE

OBJECT BYTES
Cloudflare R2 Standard
EU jurisdiction
private

RECOVERY TARGET
pgBackRest 2.59.0
AWS S3 Standard eu-south-1
Versioning
Object Lock GOVERNANCE / finite policy-bound retention
separate DB/object backup repositories

SOLVER
OR-Tools 9.15 CP-SAT

OBSERVABILITY
OpenTelemetry
Grafana Alloy 1.18.0
Grafana Cloud EU
pg_stat_statements
```

## Canonical ownership

```text
PostgreSQL
= canonical DANTE truth + material history

PostGIS
= geospatial capability over PostgreSQL state

FTS / pg_trgm / unaccent / pgvector
= derived/query retrieval

SQLite / PowerSync
= bounded local/sync state

Restate
= durable execution runtime

R2
= raw object bytes

S3
= recovery copies

OR-Tools
= candidate solver state

OTel / Grafana
= operational telemetry
```

Canonical persistence authorities: **1 — PostgreSQL**.

## Offline semantics

```text
PostgreSQL canonical
→ approved PowerSync projection
→ encrypted SQLite
→ offline mutation
→ DANTE backend expected-state + governance + AuthZ revalidation
→ PostgreSQL canonical commit if valid
```

Offline is operation-specific. Arrival order does not define truth. Universal consequential last-write-wins is rejected. Visibility/Consent/delete/redaction must propagate to affected local/projection copies.

## Restate deployment semantics

Restate is selected as the Class-B durable-execution technology.

```text
SELF-HOSTED
FIRST-CLASS DEPLOYMENT OPTION

CLOUD EU
ALLOWED MANAGED DEPLOYMENT OPTION

GLOBAL DEFAULT
NONE
```

The later Development/Production profile chooses between them. For the current Python path, do not assume the client-side journal encryption currently documented only for TypeScript; journal payload minimization remains mandatory.

## Object / recovery semantics

`ContentArtifact` identity, metadata, provenance, Visibility, retention, hashes and locator remain PostgreSQL-owned. R2 stores raw bytes only.

Production recovery target:

```text
PostgreSQL -> pgBackRest -> S3
R2 raw bytes -> separate S3 backup repository
```

Recovery copies are noncanonical. Restore must preserve deletion/redaction anti-resurrection semantics. Object Lock Compliance is not the default.

## Solver semantics

```text
OPTIMAL / FEASIBLE / INFEASIBLE / UNKNOWN
= technical solver status
!= accepted DANTE Decision
```

`UNKNOWN != INFEASIBLE`.

## Technology exclusions

The accepted target does not include:

```text
TypeDB / XTDB / SurrealDB as primary
Neo4j
Qdrant
OpenSearch
TimescaleDB
Redis / Valkey
Kafka / RabbitMQ / NATS
Debezium
dedicated event store / universal event sourcing
Temporal
DBOS
Celery + broker
Zero
Electric as full mutation/sync engine
CRDT/local-first canonical authority
MongoDB for PowerSync
large bytea standard object store
public R2
separate vector / graph / search servers
data lake / Spark / Hudi
pg_cron as workflow engine
Object Lock Compliance as default
```

Reintroduction requires an explicit later architecture reopen based on material new requirements/evidence.

## Direct execution truth

Target selection, PM-13 QA, closure and PR #15 integration did **not** execute the selected stack:

```text
DATABASE DEPLOYMENT      NOT STARTED
FIXTURE/HARNESS           NOT STARTED
DIRECT HG PASS            0
LOW/BASE/HIGH            NOT RUN
RESTORE                   NOT RUN
MIGRATION                 NOT RUN
FAILURE INJECTION         NOT RUN
POWERSYNC                  NOT RUN
RESTATE                    NOT RUN
OBJECT RECOVERY            NOT RUN
SOLVER                     NOT RUN
VERIFIED-RUN SCORE        NOT AVAILABLE
```

The full mandatory implementation/release register is [`recommendation/post-selection-validation-register-v1.md`](recommendation/post-selection-validation-register-v1.md).

## Clean-room result

PM-13 found:

```text
BLOCKING ARCHITECTURE DEFECTS      0
CANONICAL-AUTHORITY CONFLICTS      0
UNAPPROVED TECHNOLOGIES            0
FALSE DIRECT PASS CLAIMS           0
LOST PSV OBLIGATIONS               0
DOMAIN/LOGICAL IMPLICIT REOPENS    0
```

Verdict: **QA PASS — architecture/documentation coherence**.

This is not a direct runtime/database/recovery PASS.

## Development Profile v0 boundary

A later separate operational scope will decide:

```text
which selected components are active immediately
self-hosted vs managed where the target permits both
free-tier/local development choices
accounts / credentials / environment setup
initial backup / observability activation
upgrade / production triggers
```

A component being dormant in DEV does not remove it from the accepted target. A DEV deployment choice does not silently change target architecture.

## Current boundary

```text
PHYSICAL MODEL TARGET
CLOSED / SELECTED / ACCEPTED
INTEGRATED INTO MAIN VIA PR #15
PHYSICAL INTEGRATION COMMIT e6f191bad947388a44defe2c15f4939345084f58
FORMER BRANCH feature/physical-model MERGED / AUTO-DELETED

PM-13
QA PASS

PM-14
BRANCH / WORKSTREAM CLOSURE COMPLETE / HISTORICAL PRE-MERGE EVIDENCE

DIRECT IMPLEMENTATION VALIDATION
NOT STARTED / CARRIED FORWARD

NEXT
Development Profile v0

BACKEND
NOT STARTED / DEFERRED
```
