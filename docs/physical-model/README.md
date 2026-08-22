# Physical Model

- Status: **CLOSED AT TARGET-ARCHITECTURE LEVEL — SELECTED / ACCEPTED / INTEGRATED INTO MAIN VIA PR #15**
- Current product/app name: **DANTE** (`LifeOS` is the previous working/project name retained in historical evidence and technical identifiers)
- Former workstream branch: `feature/physical-model` — **MERGED / AUTO-DELETED**
- Physical integration commit: `e6f191bad947388a44defe2c15f4939345084f58` via PR #15
- Main baseline during Physical workstream: `3de84bb49f9cef30e88e9bde4961ed84335daa79`
- Current project progression: **backend CP1–CP5 CLOSED / INTEGRATED / DIRECT QA PASS; CP6 Concrete Persistence Readiness ACTIVE on `feature/logical-postgresql`; CP6-01 CLOSED / GATE 01 PASS; CP6-02 ACTIVE / CANDIDATE / PRE-CLOSURE**
- Physical semantic benchmark/direct HG corpus: **DIRECT HG PASS 0 / VERIFIED-RUN SCORE NOT AVAILABLE**
- Business persistence schema: **NOT IMPLEMENTED**
- Restate initial DEV posture: **DORMANT / NOT ACTIVE until first real Class-B need**
- pgBackRest + AWS S3 initial DEV posture: **DORMANT / NOT ACTIVE until recovery/production boundary or real recovery rehearsal**

## PostgreSQL version truth

The Physical Model selected PostgreSQL as the canonical primary and recorded **PostgreSQL 18.4** as the exact patch available and evaluated at Physical closure. That 18.4 value remains phase-time evidence and is not rewritten.

Current downstream lifecycle truth is:

```text
ARCHITECTURE FAMILY
PostgreSQL 18
sole canonical persistence / material-history authority

PHYSICAL PHASE-TIME EXACT PATCH
PostgreSQL 18.4
historical selection evidence

CP2 / CP3 ORIGINAL DIRECT EVIDENCE
PostgreSQL 18.4
historical exact direct PASS

CURRENT CP6 TECHNICAL PATCH
PostgreSQL 18.6
configuration refresh APPLIED
direct remote foundation regression PASS
Backend CI run 32568664940
HEAD ec3dc795b5e044daa3a77723c94a1b4b5b92865c
```

A compatible maintenance patch inside PostgreSQL 18 is lifecycle maintenance and does not reopen the accepted Physical architecture. A future PostgreSQL major-version change is a separate review boundary.

Historical Physical checkpoint results:

```text
PM-00   QA PASS
PM-01   PASS-CONDITIONAL
PM-02   COMPLETE
PM-03   STATIC COMPLETE / 0 REJECTS
PM-04A  COMPLETE / 0 EXECUTION-WORTHY GAPS
PM-04B  NOT ADMITTED
PM-05   COMPLETE
PM-06   EVIDENCE QUALIFICATION COMPLETE / DIRECT PERFORMANCE NOT RUN
PM-07   EVIDENCE QUALIFICATION COMPLETE / DIRECT DESTRUCTIVE RUNS NOT RUN
PM-08   SECONDARY/SPECIALIST QUALIFICATION COMPLETE
PM-09   EVIDENCE-WEIGHTED SCORING + SENSITIVITY COMPLETE
PM-10   FINAL STACK RECOMMENDATION COMPLETE
PM-11   EXPLICIT TARGET STACK SELECTION COMPLETE
PM-12   ACCEPTED PHYSICAL MODEL COMPLETE
PM-13   CLEAN-ROOM ARCHITECTURE/DOCUMENTATION QA PASS
PM-14   BRANCH / WORKSTREAM CLOSURE COMPLETE
PR #15  PROTECTED-MAIN INTEGRATION COMPLETE
```

## Purpose

This directory contains the evidence, selection and accepted target Physical architecture that translates the CLOSED DANTE Domain + Logical Model into bounded implementation mechanisms without weakening semantic ownership.

The Physical Model is closed. Later backend work consumes it; later implementation progress does not retroactively change the phase-time evidence recorded in PM-00..PM-14.

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

For the accepted Physical target architecture read:

1. [`pm-11-explicit-selection-v1.md`](pm-11-explicit-selection-v1.md) — explicit selected target stack at phase time;
2. [`pm-12-accepted-physical-model-v1.md`](pm-12-accepted-physical-model-v1.md) — accepted Physical ownership/topology contract;
3. [`pm-13-clean-room-qa-v1.md`](pm-13-clean-room-qa-v1.md) — architecture/documentation clean-room QA evidence;
4. [`pm-14-closure-v1.md`](pm-14-closure-v1.md) — historical branch/workstream closure evidence produced before PR #15;
5. [`recommendation/post-selection-validation-register-v1.md`](recommendation/post-selection-validation-register-v1.md) — current direct implementation-validation carry-forward;
6. [`result-register-v1.md`](result-register-v1.md) — Physical result ledger;
7. [`../workstreams/physical-model.md`](../workstreams/physical-model.md) — Physical workstream closure/handoff.

For **current project implementation/runtime status after Physical closure**, use:

```text
../PROJECT-STATUS.md
../ROADMAP.md
../workstreams/logical-postgresql.md
../development/backend-cp6-02-postgresql-persistence-constitution.md
../development/backend-cp3-persistence-contract.md
```

PM-00..PM-14 preserve their phase-time evidence. A historical statement such as `DATABASE DEPLOYMENT NOT STARTED` or `PostgreSQL 18.4 selected target` inside a PM-era record describes the state/version at that checkpoint and must not override later CP2/CP3/CP6 direct implementation truth.

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
POSTGRESQL PATCH REFRESH != PHYSICAL REOPEN
CP3 TECHNICAL QA != BUSINESS-SEMANTIC HG PASS
```

No universal Entity/Thing/EAV/generic-edge canonical shortcut is accepted.

## Accepted target stack

The following is the **accepted Physical phase-time target**. Exact versions are retained as selection evidence; downstream compatible patch maintenance is separately lifecycle-managed.

```text
CANONICAL PRIMARY
PostgreSQL 18.4 phase-time exact patch
Architecture family: PostgreSQL 18

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

PowerSync/logical replication is not currently active. When activated, its runtime boundary must consume then-current PostgreSQL logical-decoding policy; PostgreSQL 18.6 introduced `output_plugin_libraries`, so activation must explicitly review that setting and any current release-note requirements.

## Initial DEV activation posture already fixed

The target stack includes components intentionally selected but dormant in initial DEV.

```text
RESTATE RUNTIME
TARGET = SELECTED
INITIAL DEV = DORMANT / NOT ACTIVE
ACTIVATION TRIGGER = first real Class-B durable-workflow need
DEPLOYMENT MODE = decide only when activation is triggered

pgBackRest + AWS S3 eu-south-1
TARGET = SELECTED PRODUCTION/OFF-SITE RECOVERY
INITIAL DEV = DORMANT / NOT ACTIVE
ACTIVATION TRIGGER = recovery/production boundary
                     OR real recovery-rehearsal requirement
```

`SELECTED != DEPLOYED` remains directly applicable.

The PostgreSQL transactional outbox is selected for bounded Class-A work but is **not** assigned the same formal `DORMANT` status; materialize it only when a real Class-A requirement exists.

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

Because Restate is dormant in initial DEV, self-hosted vs Cloud EU opens only when Restate activation is triggered. For the current Python path, do not assume client-side journal encryption documented only for TypeScript; journal payload minimization remains mandatory.

## Object / recovery semantics

`ContentArtifact` identity, metadata, provenance, Visibility, retention, hashes and locator remain PostgreSQL-owned. R2 stores raw bytes only.

Production recovery target:

```text
PostgreSQL -> pgBackRest -> S3
R2 raw bytes -> separate S3 backup repository
```

This recovery target is selected but not activated in initial DEV. Recovery copies are noncanonical. Restore must preserve deletion/redaction anti-resurrection semantics. Object Lock Compliance is not the default.

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

## Direct execution truth — phase-time vs current project state

### Physical-phase snapshot

At PM-11/12/13/14 closure, the selected stack had not yet been directly implemented. Those historical records correctly retain values such as:

```text
DATABASE DEPLOYMENT      NOT STARTED
FIXTURE/HARNESS           NOT STARTED
DIRECT HG PASS            0
LOW/BASE/HIGH             NOT RUN
RESTORE                   NOT RUN
MIGRATION                 NOT RUN
FAILURE INJECTION         NOT RUN
POWERSYNC                  NOT RUN
RESTATE                    NOT RUN
OBJECT RECOVERY            NOT RUN
SOLVER                     NOT RUN
VERIFIED-RUN SCORE        NOT AVAILABLE
```

### Current project truth after Physical closure

Later backend work directly established the technical PostgreSQL substrate, first on 18.4 and now on current patch 18.6:

```text
BACKEND CP1–CP5                  CLOSED / INTEGRATED / DIRECT QA PASS
POSTGRESQL 18.4                  ORIGINAL CP2/CP3 HISTORICAL DIRECT PASS
CURRENT POSTGRESQL 18.6          CONFIGURED / DIRECT REMOTE QA PASS
18.6 CI RUN                      32568664940
18.6 EXECUTED HEAD               ec3dc795b5e044daa3a77723c94a1b4b5b92865c
POSTGIS 3.6.4                    CURRENT ENVELOPE DIRECT REMOTE QA PASS
PGVECTOR 0.8.6                   CURRENT ENVELOPE DIRECT REMOTE QA PASS
PG_TRGM / UNACCENT               CURRENT ENVELOPE ACCEPTANCE COVERAGE
PG_STAT_STATEMENTS               CURRENT ENVELOPE ACCEPTANCE COVERAGE
SQLALCHEMY / PSYCOPG             MATERIALIZED
ALEMBIC TECHNICAL BASELINE       MATERIALIZED / DIRECT QA PASS
DANTE SCHEMA / ROLE MODEL        MATERIALIZED / DIRECT QA PASS
REAL POSTGRESQL TEST HARNESS     MATERIALIZED / DIRECT QA PASS
BUSINESS PERSISTENCE SCHEMA      NOT IMPLEMENTED
SEMANTIC HG DIRECT PASS          0 unless a qualifying business scenario is actually executed
```

The PostgreSQL 18.6 run directly passed Backend Quality, Backend PostgreSQL and Backend CI Gate; 32 fast tests and 18 real-PostgreSQL tests covered the current 50-test corpus across the two mandatory lanes.

PostgreSQL 18.6 release-note impact review found no current DANTE post-upgrade action because the current boundary has no custom logical-decoding output plugin, `pgcrypto`, business GIN index, `btree_gist` or `ltree` object. This finding is bounded to the current materialized foundation; future capability activation must re-evaluate then-applicable maintenance actions.

CP3/CP6 technical acceptance does not retroactively discharge business-semantic HG/PSV obligations.

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

This remains distinct from direct runtime/database/recovery/business validation.

## Current boundary

```text
PHYSICAL MODEL TARGET
CLOSED / SELECTED / ACCEPTED
INTEGRATED INTO MAIN VIA PR #15
PostgreSQL 18 architecture family
phase-time exact patch 18.4

BACKEND FOUNDATION CP1–CP5
CLOSED / INTEGRATED / DIRECT QA PASS

CURRENT POSTGRESQL TECHNICAL PATCH
18.6 / DIRECT REMOTE FOUNDATION REGRESSION PASS

CONCRETE PERSISTENCE READINESS — CP6
ACTIVE / DESIGN-FIRST
BRANCH feature/logical-postgresql
CP6-01 CLOSED / GATE 01 PASS
CP6-02 ACTIVE / CANDIDATE / PRE-CLOSURE
GATE 02 NOT PASSED

CP6 TERMINAL BOUNDARY
CONCRETE POSTGRESQL FOUNDATION CLOSED / READY
VERTICAL #1 SELECTED / EXACTLY DESIGNED / READY FOR IMPLEMENTATION

VERTICAL #1 BUSINESS IMPLEMENTATION
POST-CP6 / SEPARATELY AUTHORIZED

BUSINESS MIGRATIONS / SQLALCHEMY BUSINESS MAPPINGS / PERSISTENCE ADAPTERS
NOT AUTHORIZED BY CP6

RESTATE
DORMANT UNTIL REAL CLASS-B NEED

pgBackRest + AWS S3
DORMANT UNTIL RECOVERY/PRODUCTION BOUNDARY OR REAL REHEARSAL
```
