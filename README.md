# DANTE

DANTE is an adaptive personal operating system for connecting intentions, plans, real time, actual reality, people/resources, evidence, history and adaptive future planning across web, Android and iOS.

> **Product naming:** `DANTE` is the current product/app name. `LifeOS` is the previous working/project name and may remain in historical evidence, Git history and existing technical/repository identifiers. Those legacy references belong to the same product lineage and do not identify a second product.

## Current project state

```text
PRODUCT / NORTH STAR
CURRENT

CORE DOMAIN MODEL / DOMAIN ATLAS
CLOSED — integrated into main via PR #10
Whole-Domain PASS WITH HARDENING / POST-WRITE QA PASS

LOGICAL MODEL
CLOSED — integrated into main via PR #11
Whole-Logical PASS WITH HARDENING / REMOTE QA PASS
WD-03 PASS
WD-05 PASS
WL-H01..WL-H12 active downstream

PRE-PHYSICAL REPOSITORY & ARCHITECTURE COHERENCE
DEFINITIVE CLOSED / FINAL QA PASS — integrated via PR #13
POST-MERGE CURRENT-TRUTH ALIGNMENT — PR #14

PHYSICAL MODEL TARGET
CLOSED / SELECTED / ACCEPTED
PM-11 explicit stack selection COMPLETE
PM-12 Accepted Physical Model COMPLETE
PM-13 clean-room architecture/documentation QA PASS
PM-14 branch closure COMPLETE
INTEGRATED INTO MAIN VIA PR #15
PHYSICAL INTEGRATION COMMIT e6f191bad947388a44defe2c15f4939345084f58
former feature/physical-model MERGED / AUTO-DELETED
selected canonical primary PostgreSQL 18.4
selected target companion stack established

DIRECT PHYSICAL IMPLEMENTATION VALIDATION
NOT STARTED
DIRECT HG PASS 0
VERIFIED-RUN SCORE NOT AVAILABLE

ENGINEERING FOUNDATION v0
ACTIVE on chore/engineering-foundation-v0
repository/application/environment/config/toolchain/testing/CI design
NO production implementation yet

BACKEND / PRODUCTION APPLICATION IMPLEMENTATION
NOT STARTED

STANDALONE DEVELOPMENT PROFILE v0
NO LONGER THE NEXT SEPARATE PHASE
operational concerns absorbed into Engineering Foundation + real capability/release implementation

RESTATE initial DEV
DORMANT UNTIL FIRST REAL CLASS-B NEED

pgBackRest + AWS S3 initial DEV
DORMANT UNTIL RECOVERY/PRODUCTION BOUNDARY OR REAL RECOVERY REHEARSAL
```

Phase 4 Home/Today UX continues separately on `prototype/phase-4-today-home`.

The active Engineering Foundation branch is unmerged work. `main` remains the integrated authority until the workstream is reviewed and merged.

## How to resume current work

Read in this order:

1. this README;
2. [`docs/README.md`](docs/README.md);
3. [`docs/PROJECT-STATUS.md`](docs/PROJECT-STATUS.md);
4. [`docs/development/agent-operating-manual.md`](docs/development/agent-operating-manual.md);
5. [`docs/development/operating-rules.md`](docs/development/operating-rules.md);
6. [`docs/development/documentation-and-handoff.md`](docs/development/documentation-and-handoff.md);
7. [`docs/development/branching-and-environments.md`](docs/development/branching-and-environments.md);
8. [`docs/development/repository-engineering-safety.md`](docs/development/repository-engineering-safety.md);
9. [`docs/workstreams/engineering-foundation.md`](docs/workstreams/engineering-foundation.md) when working on the active Foundation branch;
10. [`docs/development/engineering-foundation-v0.md`](docs/development/engineering-foundation-v0.md) + its linked detailed foundation sources;
11. [`docs/workstreams/physical-model.md`](docs/workstreams/physical-model.md);
12. [`docs/physical-model/README.md`](docs/physical-model/README.md);
13. [`docs/physical-model/pm-11-explicit-selection-v1.md`](docs/physical-model/pm-11-explicit-selection-v1.md);
14. [`docs/physical-model/pm-12-accepted-physical-model-v1.md`](docs/physical-model/pm-12-accepted-physical-model-v1.md);
15. [`docs/physical-model/recommendation/post-selection-validation-register-v1.md`](docs/physical-model/recommendation/post-selection-validation-register-v1.md);
16. [`docs/architecture/README.md`](docs/architecture/README.md) and complete Phase-5..10 authority where relevant;
17. complete CLOSED Domain/Logical authority where semantics are involved;
18. relevant ADRs/evidence;
19. verify current Git refs before any write.

Repository current truth outranks conversation memory and old/historical files.

## Documentation rule

```text
CURRENT SPECIFICATION = current truth only
ADR = rationale + explicit supersession/qualification
HISTORICAL / VALIDATION EVIDENCE = truthful chronology
GIT / PR HISTORY = recoverable history
```

A stale current document may be replaced/deleted only after knowledge coverage proves no meaningful requirement/rationale is lost.

A size/tool-limit split is a **lossless physical partition of the complete logical payload**, never a summary, condensation or hidden semantic rewrite.

## Current model authority

### Product

- [`docs/product/product-identity-and-north-star.md`](docs/product/product-identity-and-north-star.md) — current living product definition.

### Domain

The Domain Atlas is cumulative. Current closure remains:

- [`docs/domain/README.md`](docs/domain/README.md);
- [`docs/domain/README-part-20.md`](docs/domain/README-part-20.md);
- [`docs/domain/checkpoints/whole-domain-final-regression-v0-validation-part-7.md`](docs/domain/checkpoints/whole-domain-final-regression-v0-validation-part-7.md);
- [`docs/domain/language-map.md`](docs/domain/language-map.md) + [`docs/domain/language-map-part-22.md`](docs/domain/language-map-part-22.md).

Current Domain state is **CLOSED**.

### Logical

Read:

- [`docs/logical-model/whole-logical-model-v1.md`](docs/logical-model/whole-logical-model-v1.md);
- complete `docs/logical-model/decision-and-assumption-register-v1*` chain;
- [`docs/logical-model/checkpoints/whole-logical-v1-remote-qa.md`](docs/logical-model/checkpoints/whole-logical-v1-remote-qa.md).

Current Logical state is **CLOSED**.

## Accepted Physical authority

Current Physical authority:

- [`docs/physical-model/README.md`](docs/physical-model/README.md);
- [`docs/physical-model/pm-10-recommendation-v1.md`](docs/physical-model/pm-10-recommendation-v1.md);
- [`docs/physical-model/pm-11-explicit-selection-v1.md`](docs/physical-model/pm-11-explicit-selection-v1.md);
- [`docs/physical-model/pm-12-accepted-physical-model-v1.md`](docs/physical-model/pm-12-accepted-physical-model-v1.md);
- [`docs/physical-model/pm-13-clean-room-qa-v1.md`](docs/physical-model/pm-13-clean-room-qa-v1.md);
- [`docs/physical-model/pm-14-closure-v1.md`](docs/physical-model/pm-14-closure-v1.md) — historical branch closure evidence;
- [`docs/physical-model/recommendation/post-selection-validation-register-v1.md`](docs/physical-model/recommendation/post-selection-validation-register-v1.md);
- [`docs/workstreams/physical-model.md`](docs/workstreams/physical-model.md).

Accepted target:

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
encrypted SQLite local state
PostgreSQL-backed PowerSync sync storage

BOUNDED ASYNC
PostgreSQL transactional outbox + bounded worker

DURABLE CLASS-B
Restate runtime
self-hosted first-class or Cloud EU managed option
global deployment default NONE

OBJECT BYTES
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

Canonical authority remains singular:

```text
PostgreSQL = canonical DANTE truth/material history
PowerSync/SQLite = local/sync projection
Restate = runtime state
R2 = raw bytes
S3 = recovery copy
OR-Tools = candidate solver state
Grafana/OTel = operational telemetry
```

## Initial activation posture already fixed

```text
RESTATE RUNTIME
SELECTED TARGET
INITIAL DEV = DORMANT / NOT ACTIVE
ACTIVATE = first real Class-B durable-workflow need
DEPLOYMENT MODE = decide only when activation is triggered

pgBackRest + AWS S3 eu-south-1
SELECTED RECOVERY TARGET
INITIAL DEV = DORMANT / NOT ACTIVE
ACTIVATE = recovery/production boundary OR real recovery-rehearsal requirement
```

Engineering Foundation consumes this posture and does not reopen it.

Other selected Physical capabilities enter implementation when their real vertical slice requires them; this no longer needs a standalone “Development Profile” phase.

## Engineering Foundation v0

Active branch authority:

- [`docs/workstreams/engineering-foundation.md`](docs/workstreams/engineering-foundation.md);
- [`docs/development/engineering-foundation-v0.md`](docs/development/engineering-foundation-v0.md);
- [`docs/development/repository-layout-v0.md`](docs/development/repository-layout-v0.md);
- [`docs/development/application-structure-v0.md`](docs/development/application-structure-v0.md);
- [`docs/development/environments-and-promotion-v0.md`](docs/development/environments-and-promotion-v0.md);
- [`docs/development/config-and-secrets-v0.md`](docs/development/config-and-secrets-v0.md);
- [`docs/development/toolchain-and-dx-v0.md`](docs/development/toolchain-and-dx-v0.md);
- [`docs/development/testing-and-ci-v0.md`](docs/development/testing-and-ci-v0.md).

Branch baseline direction includes:

```text
polyglot monorepo
capability-first modular monolith
LOCAL / DEV / UAT / PROD environment contract
GitHub Actions CI/CD orchestration
Python 3.14 + uv + Ruff + mypy + pytest
SQLAlchemy 2.0 + psycopg 3 + Alembic
Node 24 LTS + pnpm 11 + TypeScript strict + ESLint + Prettier
Turborepo for JS/TS workspace task graph
real PostgreSQL integration testing
controlled migrations separate from app startup
immutable artifact promotion where platform permits
OIDC / least-privilege secret posture
```

This is **active unmerged engineering design**, not production implementation and not a direct-validation PASS.

## Direct evidence truth

Physical target selection/acceptance did not manufacture direct execution evidence:

```text
DATABASE DEPLOYMENT      NOT STARTED
FIXTURE/HARNESS           NOT STARTED
DIRECT HG PASS            0
LOW/BASE/HIGH            NOT RUN
RESTORE/MIGRATION         NOT RUN
FAILURE INJECTION         NOT RUN
POWERSYNC                 NOT RUN
RESTATE                   NOT RUN
OBJECT RECOVERY           NOT RUN
SOLVER                    NOT RUN
VERIFIED-RUN SCORE        NOT AVAILABLE
```

Direct selected-stack obligations remain in the post-selection validation register and move forward into implementation/release gates.

## Current technical direction — not implementation authorization

- Web: Next.js + React + TypeScript.
- Mobile: Expo + React Native + TypeScript.
- Backend: Python + FastAPI + Pydantic; capability-first modular monolith.
- Engineering Foundation branch selects SQLAlchemy 2.0 stable + psycopg 3 + Alembic as the backend persistence/migration baseline against accepted PostgreSQL.

Production application code is still **not started**.

### AI / context / runtime

AI remains behind a replaceable/provider-neutral gateway and bounded Context Builder.

```text
canonical state
material history
retrieved context
derived context
live external context
candidate / unresolved state
transient LLM working context
```

AI output/tool invocation does not become canonical truth/effect by itself. Runtime Agent/Principal is not Domain Actor automatically. Generic AI memory is not a second canonical truth store.

Material consequential AI changes require versioned/reproducible evaluation before promotion.

### Integration Hub

Five modes remain distinct: canonical import, sync/mirror, live federated read, retrieval/index projection and action/tool integration.

`ExternalRef != NativeRef`; provider revision != `MaterialStateRef`; provider state/effect != canonical DANTE state/effect automatically. MCP/A2A/future protocols remain adapters.

### Governed operations / effects

```text
route / UI button / tool / AuthZ action / workflow step
!= canonical governed operation/effect
request accepted != effect complete
provider acknowledgement != canonical completion automatically
workflow completed != Actual automatically
technical cancellation != Domain cancellation automatically
```

## Repository safety

`main` remains protected by the remotely verified repository-safety policy. Normal integration uses pull requests; no direct-main bypass is authorized.

## Next boundary

```text
ENGINEERING FOUNDATION v0
ACTIVE / MUST BE REVIEWED + QA'D + INTEGRATED

THEN
production repository scaffold
→ backend bootstrap/composition root
→ PostgreSQL local profile + migration harness
→ concrete Logical-to-PostgreSQL schema implementation
→ vertical production slices

BACKEND / PRODUCTION APPLICATION CODE
NOT STARTED YET

DIRECT PSV
CARRIED FORWARD / NOT RUN
```