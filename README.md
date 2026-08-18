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

PHYSICAL MODEL
CLOSED AT TARGET-ARCHITECTURE LEVEL
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

BACKEND PRODUCTION IMPLEMENTATION
NOT STARTED / DEFERRED

DEVELOPMENT PROFILE v0
NOT STARTED / SEPARATE NEXT OPERATIONAL SCOPE
Restate initial DEV activation DORMANT UNTIL REAL CLASS-B NEED
pgBackRest + AWS S3 initial DEV activation DORMANT UNTIL RECOVERY/PRODUCTION BOUNDARY
```

Phase 4 Home/Today UX continues separately on `prototype/phase-4-today-home`.

For exact current state read [`docs/PROJECT-STATUS.md`](docs/PROJECT-STATUS.md), [`docs/physical-model/pm-12-accepted-physical-model-v1.md`](docs/physical-model/pm-12-accepted-physical-model-v1.md) and [`docs/workstreams/physical-model.md`](docs/workstreams/physical-model.md).

## How to resume work

Read in this order:

1. this README;
2. [`docs/README.md`](docs/README.md);
3. [`docs/PROJECT-STATUS.md`](docs/PROJECT-STATUS.md);
4. [`docs/development/agent-operating-manual.md`](docs/development/agent-operating-manual.md);
5. [`docs/development/operating-rules.md`](docs/development/operating-rules.md);
6. [`docs/development/documentation-and-handoff.md`](docs/development/documentation-and-handoff.md);
7. [`docs/development/branching-and-environments.md`](docs/development/branching-and-environments.md);
8. [`docs/development/repository-engineering-safety.md`](docs/development/repository-engineering-safety.md);
9. [`docs/workstreams/physical-model.md`](docs/workstreams/physical-model.md);
10. [`docs/physical-model/README.md`](docs/physical-model/README.md);
11. [`docs/physical-model/pm-11-explicit-selection-v1.md`](docs/physical-model/pm-11-explicit-selection-v1.md);
12. [`docs/physical-model/pm-12-accepted-physical-model-v1.md`](docs/physical-model/pm-12-accepted-physical-model-v1.md);
13. [`docs/physical-model/pm-13-clean-room-qa-v1.md`](docs/physical-model/pm-13-clean-room-qa-v1.md);
14. [`docs/physical-model/recommendation/post-selection-validation-register-v1.md`](docs/physical-model/recommendation/post-selection-validation-register-v1.md);
15. [`docs/architecture/README.md`](docs/architecture/README.md) and complete Phase-5..10 authority where relevant;
16. complete CLOSED Domain/Logical authority where semantics are involved;
17. relevant ADRs/evidence;
18. verify current Git refs before any write.

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

The Physical workstream consumed the accepted Domain/Logical/Pre-Physical state without reopening it implicitly.

Current Physical authority:

- [`docs/physical-model/README.md`](docs/physical-model/README.md) — Physical index/current state;
- [`docs/physical-model/pm-10-recommendation-v1.md`](docs/physical-model/pm-10-recommendation-v1.md) — final recommendation evidence;
- [`docs/physical-model/pm-11-explicit-selection-v1.md`](docs/physical-model/pm-11-explicit-selection-v1.md) — explicit selected target stack;
- [`docs/physical-model/pm-12-accepted-physical-model-v1.md`](docs/physical-model/pm-12-accepted-physical-model-v1.md) — accepted target Physical Model;
- [`docs/physical-model/pm-13-clean-room-qa-v1.md`](docs/physical-model/pm-13-clean-room-qa-v1.md) — clean-room architecture/documentation QA;
- [`docs/physical-model/pm-14-closure-v1.md`](docs/physical-model/pm-14-closure-v1.md) — closure evidence;
- [`docs/physical-model/recommendation/post-selection-validation-register-v1.md`](docs/physical-model/recommendation/post-selection-validation-register-v1.md) — mandatory direct implementation-validation carry-forward;
- [`docs/workstreams/physical-model.md`](docs/workstreams/physical-model.md) — workstream handoff/closure state.

Phase-10 benchmark authority remains historical/method input:

- [`docs/architecture/physical-benchmark-specification.md`](docs/architecture/physical-benchmark-specification.md)
- [`docs/architecture/physical-benchmark-scenario-corpus.md`](docs/architecture/physical-benchmark-scenario-corpus.md)
- [`docs/architecture/physical-benchmark-register.md`](docs/architecture/physical-benchmark-register.md)

## Accepted Physical target

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
global Restate deployment default NONE

OBJECT BYTES
Cloudflare R2 Standard / EU / private

RECOVERY TARGET
pgBackRest 2.59.0
AWS S3 Standard eu-south-1 off-site recovery repositories
Versioning + Object Lock GOVERNANCE with finite policy-bound retention

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

## Initial DEV activation posture already fixed

Two selected target components are intentionally **not day-1 DEV services**:

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

Development Profile v0 consumes this posture; it does not reopen these as initial activation choices.

## Restate deployment qualification

Restate is selected as the durable-runtime technology. `Restate Cloud EU` is **not** a universal mandatory default.

```text
SELF-HOSTED
FIRST-CLASS OPTION

CLOUD EU
ALLOWED MANAGED OPTION

GLOBAL DEFAULT
NONE
```

Because Restate is dormant in initial DEV, self-hosted vs Cloud EU is not a decision that must be made now. The deployment choice is made only when a real Class-B activation trigger exists, based on privacy, operability, availability and cost at that boundary. For the current Python path, do not assume TypeScript-only client-side journal encryption; journal payload minimization remains mandatory.

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
- Backend: Python + FastAPI + Pydantic; modular monolith first.
- SQLAlchemy + Alembic may now be evaluated/used against the accepted PostgreSQL Physical target inside a separately authorized backend/development scope.

Backend production implementation is **not started**.

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

`main` remains protected by the remotely verified `lifeos-main-safety` policy. Normal integration uses pull requests; no direct-main bypass is authorized.

## Next boundary

```text
PHYSICAL MODEL TARGET
CLOSED / SELECTED / ACCEPTED
INTEGRATED INTO MAIN VIA PR #15

DIRECT IMPLEMENTATION VALIDATION
CARRIED FORWARD

BACKEND PRODUCTION IMPLEMENTATION
NOT STARTED / DEFERRED

DEVELOPMENT PROFILE v0
NEXT SEPARATE OPERATIONAL DESIGN SCOPE
Restate initial DEV posture FIXED = DORMANT UNTIL REAL CLASS-B NEED
pgBackRest + AWS S3 initial DEV posture FIXED = DORMANT UNTIL RECOVERY/PRODUCTION BOUNDARY
```