# Project Status

- Last updated: 2026-08-19
- Current product/app name: **DANTE**
- Previous working/project name: `LifeOS` — legacy/historical references only; same product lineage
- Canonical integrated branch: `main`
- Current bounded engineering branch: `chore/engineering-foundation-v0`
- Engineering Foundation PRE-SCOPE: `ebc3616956faeabd99d90f5f32458b284be218e4`
- Physical integration: **PR #15 / integration commit `e6f191bad947388a44defe2c15f4939345084f58`**
- Physical target architecture: **CLOSED / SELECTED / ACCEPTED**
- Selected canonical primary: **PostgreSQL 18.4**
- Direct selected-stack implementation validation: **NOT STARTED / DIRECT HG PASS 0**
- Production application code: **NOT STARTED**
- Engineering Foundation v0: **ACTIVE / UNMERGED / PENDING FINAL REVIEW + QA**
- Standalone Development Profile v0: **RETIRED AS NEXT SEPARATE PHASE; operational concerns absorbed downstream**
- Initial DEV Restate posture: **DORMANT / NOT ACTIVE until first real Class-B durable-workflow need**
- Initial DEV pgBackRest + AWS S3 posture: **DORMANT / NOT ACTIVE until recovery/production boundary or real recovery rehearsal**

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
selected canonical primary PostgreSQL 18.4
selected target companion architecture established

DIRECT SELECTED-STACK IMPLEMENTATION VALIDATION
NOT STARTED
DIRECT HG PASS 0
VERIFIED-RUN SCORE NOT AVAILABLE

ENGINEERING FOUNDATION v0
ACTIVE / UNMERGED
branch chore/engineering-foundation-v0
professional repository/application/environment/config/toolchain/testing/CI baseline
production code NOT STARTED

BACKEND / PRODUCTION APPLICATION IMPLEMENTATION
NOT STARTED
NEXT ONLY AFTER FOUNDATION REVIEW/CLOSURE/INTEGRATION

STANDALONE DEVELOPMENT PROFILE v0
NO LONGER NEXT
its operational concerns are handled by Engineering Foundation
and by the real capability/release implementation boundary that needs them
```

Phase 4 UX remains a separate active product/design workstream on `prototype/phase-4-today-home`.

## Authority and branch truth

`main` remains the only integrated accepted source of truth. The active Engineering Foundation branch may contain newer unmerged truth only within its explicitly approved workstream scope.

Conversation history remains secondary to repository truth.

## Read this first

1. [`README.md`](../README.md)
2. [`docs/README.md`](README.md)
3. this file
4. [`development/agent-operating-manual.md`](development/agent-operating-manual.md)
5. [`development/operating-rules.md`](development/operating-rules.md)
6. [`development/documentation-and-handoff.md`](development/documentation-and-handoff.md)
7. [`development/branching-and-environments.md`](development/branching-and-environments.md)
8. [`development/repository-engineering-safety.md`](development/repository-engineering-safety.md)
9. [`workstreams/engineering-foundation.md`](workstreams/engineering-foundation.md) for the active branch
10. [`development/engineering-foundation-v0.md`](development/engineering-foundation-v0.md) + all linked detailed foundation sources
11. [`workstreams/physical-model.md`](workstreams/physical-model.md)
12. [`physical-model/pm-11-explicit-selection-v1.md`](physical-model/pm-11-explicit-selection-v1.md)
13. [`physical-model/pm-12-accepted-physical-model-v1.md`](physical-model/pm-12-accepted-physical-model-v1.md)
14. [`physical-model/recommendation/post-selection-validation-register-v1.md`](physical-model/recommendation/post-selection-validation-register-v1.md)
15. [`architecture/README.md`](architecture/README.md) and Phase-5..10 authority where relevant
16. complete Domain/Logical closure authority when semantics are involved
17. current Git refs / PR state before any write

## Accepted/current foundations

- Product/North Star — **CURRENT**.
- DANTE identity — **CURRENT**.
- Core Domain Model / Domain Atlas — **CLOSED**.
- Logical Model — **CLOSED**; `WL-H01..WL-H12` active downstream.
- Pre-Physical Architecture Baseline — **CLOSED / integrated / verified**.
- Phase 5 requirements — **CURRENT**.
- Phase 6 AI/context/runtime + Integration Hub boundaries — **CURRENT**.
- Phase 7 durable execution contract — **CURRENT / physically resolved to Restate for Class-B target runtime**.
- Phase 8 governed operation/effect — **CURRENT**.
- Phase 9 search/observability/calendar/solver — **CURRENT / mechanisms resolved where selected**.
- Phase 10 benchmark method — **CURRENT METHOD / historical decision-evidence authority**.
- Repository engineering safety — **QA PASS at its verified scope**.
- Physical target — **CLOSED / SELECTED / ACCEPTED / integrated**.
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

Engineering/implementation work consumes these models without implicit semantic reopen. Any genuine contradiction requires an explicit bounded reopen.

## Accepted Physical Model

Current authority:

- [`physical-model/pm-11-explicit-selection-v1.md`](physical-model/pm-11-explicit-selection-v1.md);
- [`physical-model/pm-12-accepted-physical-model-v1.md`](physical-model/pm-12-accepted-physical-model-v1.md);
- [`physical-model/pm-13-clean-room-qa-v1.md`](physical-model/pm-13-clean-room-qa-v1.md);
- [`physical-model/pm-14-closure-v1.md`](physical-model/pm-14-closure-v1.md) — historical closure evidence;
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
self-hosted first-class OR Cloud EU managed option
global deployment default NONE

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

## Fixed initial DEV posture

```text
RESTATE
SELECTED TARGET
INITIAL DEV = DORMANT / NOT ACTIVE
ACTIVATE = first real Class-B durable-workflow need
DEPLOYMENT MODE = decide only when activation trigger exists

pgBackRest + AWS S3 eu-south-1
SELECTED RECOVERY TARGET
INITIAL DEV = DORMANT / NOT ACTIVE
ACTIVATE = recovery/production boundary OR real recovery rehearsal
```

Engineering Foundation does not reopen either decision. Other selected components enter implementation when the capability that actually needs them is built.

## Engineering Foundation v0 — active branch

Purpose: establish the professional engineering system before the first production implementation commit.

Current branch sources:

```text
docs/workstreams/engineering-foundation.md
docs/development/engineering-foundation-v0.md
docs/development/repository-layout-v0.md
docs/development/application-structure-v0.md
docs/development/environments-and-promotion-v0.md
docs/development/config-and-secrets-v0.md
docs/development/toolchain-and-dx-v0.md
docs/development/testing-and-ci-v0.md
```

Branch baseline decisions include:

```text
REPOSITORY
polyglot monorepo
apps/api + apps/web + apps/mobile
precise shared packages only

BACKEND
capability-first modular monolith
explicit composition root
no generic CRUD/service-locator kernel

ENVIRONMENTS
LOCAL + DEV + UAT + PROD
optional ephemeral previews
no environment Git branches

TOOLCHAIN
Python 3.14 line + uv + Ruff + mypy + pytest
SQLAlchemy 2.0 stable + psycopg 3 + Alembic
Node 24 LTS + pnpm 11 + TypeScript strict + ESLint + Prettier
Turborepo for JS/TS task graph

DELIVERY
GitHub Actions primary CI/CD orchestration
GitHub Environments for privileged deployment once workflows exist
locked dependencies
real PostgreSQL integration testing
controlled migrations separate from app startup
immutable artifact identity/promotion where possible
OIDC/least privilege where provider supports it
```

Exact compute hosting, IaC engine and provider-specific deployment mechanics remain deliberately deferred until the first real remote-infrastructure implementation because accepted architecture has not selected them.

Foundation is **ACTIVE**, not yet `CLOSED` or integrated.

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

Engineering Foundation documentation does not convert any direct obligation to PASS.

## Mandatory implementation-validation carry-forward

The post-selection register remains mandatory. Key groups include:

```text
SC-011 anti-resurrection
SC-030 V1->V2 evolution
SC-031 destructive semantic restore
SC-032 capacity/backpressure
WL-H12 non-interference
search/vector/projection filtering/freshness/deletion
PowerSync replication/conflicts/local encryption
Restate crash/replay/versioning/governance/privacy after activation
R2/S3 object deletion/recovery
PostGIS/PgBouncer compatibility
pgBackRest archive/PITR
OR-Tools status/governance corpus
observability privacy
```

A failed applicable direct validation can reopen the affected Physical decision; it cannot weaken Domain/Logical semantics to manufacture a PASS.

## Active workstreams

### Engineering Foundation v0

- **ACTIVE / UNMERGED**
- branch `chore/engineering-foundation-v0`
- production code **NOT STARTED**
- final user review + exact remote QA still required before closure/integration

### Phase 4 — Home / Today UX

- **IN PROGRESS — separate product/design workstream**
- branch `prototype/phase-4-today-home`

### Physical Model

- **CLOSED / SELECTED / ACCEPTED / integrated**
- former branch merged and auto-deleted
- direct PSV remains carried forward

## Immediate next work

```text
1. complete Engineering Foundation current-doc alignment
2. exact remote scope/readback/coherence QA
3. user review/acceptance
4. protected PR integration if accepted
5. then start real production implementation through a fresh exact scope:
   repository scaffold
   -> backend bootstrap/composition root
   -> PostgreSQL local profile + migration harness
   -> concrete Logical-to-PostgreSQL schema
   -> vertical production slices
```

No production code is authorized by this active documentation scope alone.