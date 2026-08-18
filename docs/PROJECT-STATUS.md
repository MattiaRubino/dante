# Project Status

- Last updated: 2026-08-18
- Current product/app name: **DANTE**
- Previous working/project name: `LifeOS` — legacy/historical references only; same product lineage
- Canonical integrated branch: `main`
- Physical integration: **PR #15 / `main @ e6f191bad947388a44defe2c15f4939345084f58`**
- Former Physical workstream branch: `feature/physical-model` — **MERGED / AUTO-DELETED**
- Physical target architecture: **CLOSED / SELECTED / ACCEPTED**
- Selected canonical primary: **PostgreSQL 18.4**
- PM-13 clean-room architecture/documentation QA: **PASS**
- Direct selected-stack implementation validation: **NOT STARTED**
- Production application code: **NOT STARTED**
- Backend Foundation: **NOT STARTED / DEFERRED**
- Development Profile v0: **NOT STARTED / NEXT SEPARATE OPERATIONAL SCOPE**

## Current stage

```text
PRODUCT / NORTH STAR
CURRENT

CORE DOMAIN MODEL / DOMAIN ATLAS
CLOSED — integrated through PR #10
Whole-Domain PASS WITH HARDENING / POST-WRITE QA PASS

LOGICAL MODEL
CLOSED — integrated through PR #11
Whole-Logical PASS WITH HARDENING / REMOTE QA PASS
WD-03 PASS
WD-05 PASS
WL-H01..WL-H12 active downstream

PRE-PHYSICAL REPOSITORY & ARCHITECTURE COHERENCE
DEFINITIVE CLOSED / FINAL QA PASS
INTEGRATED / POST-MERGE VERIFIED
PR #13 + post-merge alignment PR #14

PHYSICAL MODEL TARGET
CLOSED / SELECTED / ACCEPTED
PM-11 explicit selection COMPLETE
PM-12 Accepted Physical Model COMPLETE
PM-13 clean-room architecture/documentation QA PASS
PM-14 branch closure COMPLETE
INTEGRATED INTO MAIN VIA PR #15
MAIN e6f191bad947388a44defe2c15f4939345084f58
FORMER BRANCH feature/physical-model MERGED / AUTO-DELETED
selected canonical primary PostgreSQL 18.4
selected target companion architecture established

DIRECT SELECTED-STACK IMPLEMENTATION VALIDATION
NOT STARTED
DIRECT HG PASS 0
VERIFIED-RUN SCORE NOT AVAILABLE

BACKEND FOUNDATION / PRODUCTION IMPLEMENTATION
NOT STARTED / DEFERRED

DEVELOPMENT PROFILE v0
NOT STARTED / NEXT SEPARATE OPERATIONAL SCOPE
```

Phase 4 UX remains a separate active product/design workstream on `prototype/phase-4-today-home`.

## Read this first

1. [`README.md`](../README.md)
2. [`docs/README.md`](README.md)
3. this file
4. [`development/agent-operating-manual.md`](development/agent-operating-manual.md)
5. [`development/operating-rules.md`](development/operating-rules.md)
6. [`development/documentation-and-handoff.md`](development/documentation-and-handoff.md)
7. [`development/branching-and-environments.md`](development/branching-and-environments.md)
8. [`development/repository-engineering-safety.md`](development/repository-engineering-safety.md)
9. [`workstreams/physical-model.md`](workstreams/physical-model.md)
10. [`physical-model/README.md`](physical-model/README.md)
11. [`physical-model/pm-11-explicit-selection-v1.md`](physical-model/pm-11-explicit-selection-v1.md)
12. [`physical-model/pm-12-accepted-physical-model-v1.md`](physical-model/pm-12-accepted-physical-model-v1.md)
13. [`physical-model/pm-13-clean-room-qa-v1.md`](physical-model/pm-13-clean-room-qa-v1.md)
14. [`physical-model/recommendation/post-selection-validation-register-v1.md`](physical-model/recommendation/post-selection-validation-register-v1.md)
15. [`architecture/README.md`](architecture/README.md) and Phase-5..10 authority where relevant
16. complete Domain/Logical closure authority where semantics are involved
17. current Git refs / PR state before any new write

Conversation history is secondary to repository truth.

## Accepted/current foundations

- Product/North Star — **CURRENT**.
- Current product/app identity — **DANTE**; `LifeOS` is the previous working/project name retained only where historical/technical continuity requires it.
- Core Domain Model / Domain Atlas — **CLOSED**.
- Logical Model — **CLOSED**; `WL-H01..WL-H12` active downstream.
- Pre-Physical Architecture Baseline — **CURRENT / CLOSED / integrated**.
- Phase 5 requirements — **CURRENT**.
- Phase 6 AI/context/runtime + Integration Hub boundaries — **CURRENT**.
- Phase 7 durable execution contract — **CURRENT**, now physically resolved to Restate for Class-B target runtime.
- Phase 8 governed operation/effect — **CURRENT**.
- Phase 9 search/observability/calendar/solver — **CURRENT**, now physically resolved where selected by PM-11/12.
- Phase 10 benchmark method — **CURRENT / QA PASS / historical method authority for Physical evidence**.
- Phase 11 repository engineering safety — **QA PASS**.
- Phase 12 Pre-Physical clean-room QA — **QA PASS / CLOSED**.
- Physical PM-11 selection — **COMPLETE**.
- Physical PM-12 Accepted Physical Model — **COMPLETE**.
- Physical PM-13 clean-room architecture/documentation QA — **QA PASS**.
- Physical protected-main integration — **COMPLETE via PR #15 / post-merge verified**.
- Web direction — Next.js + React + TypeScript.
- Mobile direction — Expo + React Native + TypeScript.
- Backend direction — Python + FastAPI + Pydantic; modular monolith.

## Domain / Logical closure

```text
DOMAIN
PASS WITH HARDENING
POST-WRITE QA PASS
CLOSED

LOGICAL
PASS WITH HARDENING
REMOTE QA PASS
CLOSED
WD-03 PASS
WD-05 PASS
```

Physical/backend work must consume these models without implicit semantic reopen. Any genuine contradiction requires a separate explicit reopen scope.

## Accepted Physical Model

Current authority:

- [`physical-model/pm-11-explicit-selection-v1.md`](physical-model/pm-11-explicit-selection-v1.md);
- [`physical-model/pm-12-accepted-physical-model-v1.md`](physical-model/pm-12-accepted-physical-model-v1.md);
- [`physical-model/pm-13-clean-room-qa-v1.md`](physical-model/pm-13-clean-room-qa-v1.md);
- [`physical-model/pm-14-closure-v1.md`](physical-model/pm-14-closure-v1.md);
- [`physical-model/result-register-v1.md`](physical-model/result-register-v1.md);
- [`physical-model/recommendation/post-selection-validation-register-v1.md`](physical-model/recommendation/post-selection-validation-register-v1.md);
- [`workstreams/physical-model.md`](workstreams/physical-model.md).

Selected target:

```text
CANONICAL PRIMARY
PostgreSQL 18.4

POSTGRESQL CAPABILITIES
PostGIS 3.6.4
pgvector 0.8.6
native FTS / pg_trgm / unaccent
pg_stat_statements
PgBouncer 1.25.2

OFFLINE / SYNC
PowerSync 1.25.0 Open Edition
encrypted SQLite
PostgreSQL-backed PowerSync sync storage

ASYNC CLASS A
PostgreSQL transactional outbox + bounded worker

DURABLE CLASS B
Restate runtime
Restate self-hosted first-class OR Cloud EU managed option
GLOBAL RESTATE DEPLOYMENT DEFAULT NONE

OBJECT
Cloudflare R2 Standard / EU / private

RECOVERY TARGET
pgBackRest 2.59.0
AWS S3 Standard eu-south-1 recovery repositories
Versioning + Object Lock GOVERNANCE / finite policy-bound retention

SOLVER
OR-Tools 9.15 CP-SAT

OBSERVABILITY
OpenTelemetry + Grafana Alloy 1.18.0 + Grafana Cloud EU
```

Canonical authority remains singular: PostgreSQL.

## Restate deployment qualification

Restate technology is selected, but deployment is conditional:

```text
SELF-HOSTED
FIRST-CLASS

CLOUD EU
ALLOWED MANAGED OPTION

GLOBAL DEFAULT
NONE
```

The later deployment profile decides between them. Current Python use must not assume TypeScript-only client-side journal encryption; journal minimization remains mandatory.

## Direct Physical execution truth

```text
DATABASE INSTANCE
NOT STARTED

FIXTURE/HARNESS
NOT STARTED

DIRECT HG PASS
0

LOW/BASE/HIGH
NOT RUN

RESTORE / MIGRATION / FAILURE INJECTION
NOT RUN

POWERSYNC / RESTATE / OBJECT / SOLVER DIRECT VALIDATION
NOT RUN

VERIFIED-RUN BENCHMARK SCORE
NOT AVAILABLE
```

PM-11/12 selection and PM-13 clean-room QA do not convert these into direct PASS.

## Mandatory implementation-validation carry-forward

The selected target remains conditional on applicable direct implementation/release obligations in:

```text
physical-model/recommendation/post-selection-validation-register-v1.md
```

Key groups:

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

None is direct PASS merely because the target architecture is closed.

## Backend / Development boundary

The Physical target is now integrated into `main` and available as an input to later engineering. It does **not** itself start backend production implementation.

A separate `Development Profile v0` may now be designed to decide:

```text
which selected components are activated immediately
self-hosted vs managed where Physical allows both
free-tier/local development choices
accounts/credentials/environment setup
initial backup/observability activation
upgrade/production triggers
```

That profile must not silently change the accepted target Physical Model.

## Active workstreams

### Physical Model

- **TARGET ARCHITECTURE CLOSED / SELECTED / ACCEPTED**
- **PM-13 QA PASS**
- branch closure evidence complete
- integrated into protected `main` through PR #15
- former `feature/physical-model` branch merged and auto-deleted

### Phase 4 — Home / Today UX

- **IN PROGRESS — separate product/design workstream**
- branch `prototype/phase-4-today-home`

### Backend Foundation

**NOT STARTED / DEFERRED.** It requires its own explicit authorization/gate.

### Development Profile v0

**NOT STARTED.** This is the next separate operational-design discussion after Physical integration.

## Immediate next work

```text
1. open Development Profile v0 as a separate bounded scope
2. decide actual initial activation/deployment/free/local choices against the already-selected target
3. preserve all direct PSV obligations as NOT RUN until directly executed
4. do not start backend production implementation without its own explicit authorization
```