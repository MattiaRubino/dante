# Documentation Index

This directory is the durable project memory for LifeOS. A new human/AI contributor should be able to resume from repository truth without reconstructing decisions from chat history.

## Start here

Read in this order:

1. [`../README.md`](../README.md)
2. [`PROJECT-STATUS.md`](PROJECT-STATUS.md)
3. [`development/agent-operating-manual.md`](development/agent-operating-manual.md)
4. [`development/operating-rules.md`](development/operating-rules.md)
5. [`development/documentation-and-handoff.md`](development/documentation-and-handoff.md)
6. [`development/branching-and-environments.md`](development/branching-and-environments.md)
7. [`development/repository-engineering-safety.md`](development/repository-engineering-safety.md)
8. [`workstreams/physical-model.md`](workstreams/physical-model.md)
9. [`physical-model/README.md`](physical-model/README.md)
10. [`physical-model/pm-11-explicit-selection-v1.md`](physical-model/pm-11-explicit-selection-v1.md)
11. [`physical-model/pm-12-accepted-physical-model-v1.md`](physical-model/pm-12-accepted-physical-model-v1.md)
12. [`physical-model/pm-13-clean-room-qa-v1.md`](physical-model/pm-13-clean-room-qa-v1.md)
13. [`physical-model/recommendation/post-selection-validation-register-v1.md`](physical-model/recommendation/post-selection-validation-register-v1.md)
14. [`architecture/README.md`](architecture/README.md) and linked Phase-5..10 sources where relevant
15. complete Domain/Logical closure authority where semantics are involved
16. relevant ADRs/evidence/methodologies
17. current Git refs/branch relation to `main`

## Current backend/architecture stage

```text
PRODUCT / NORTH STAR
CURRENT

CORE DOMAIN MODEL / DOMAIN ATLAS
CLOSED — PR #10
Whole-Domain PASS WITH HARDENING / POST-WRITE QA PASS

LOGICAL MODEL
CLOSED — PR #11
Whole-Logical PASS WITH HARDENING / REMOTE QA PASS
WD-03 PASS
WD-05 PASS
WL-H01..WL-H12 active downstream

PRE-PHYSICAL REPOSITORY & ARCHITECTURE COHERENCE
DEFINITIVE CLOSED / FINAL QA PASS
INTEGRATED / POST-MERGE VERIFIED
PR #13 + current-truth alignment PR #14

PHYSICAL MODEL
CLOSED AT TARGET-ARCHITECTURE LEVEL
PM-11 explicit selection COMPLETE
PM-12 Accepted Physical Model COMPLETE
PM-13 clean-room architecture/documentation QA PASS
PM-14 branch closure COMPLETE
INTEGRATED INTO MAIN VIA PR #15
main e6f191bad947388a44defe2c15f4939345084f58
former feature/physical-model MERGED / AUTO-DELETED
selected canonical primary PostgreSQL 18.4
selected target companion architecture established

DIRECT SELECTED-STACK IMPLEMENTATION VALIDATION
NOT STARTED
DIRECT HG PASS 0
VERIFIED-RUN SCORE NOT AVAILABLE

BACKEND PRODUCTION IMPLEMENTATION
NOT STARTED / DEFERRED

DEVELOPMENT PROFILE v0
NOT STARTED / SEPARATE NEXT OPERATIONAL SCOPE
```

Exact Physical handoff: [`workstreams/physical-model.md`](workstreams/physical-model.md).

## Current semantic/model sources

### Product

- [`product/product-identity-and-north-star.md`](product/product-identity-and-north-star.md) — current Product/North Star.

### Domain

The Domain authority is cumulative. Current closure is established by the complete chain, including:

- [`domain/README.md`](domain/README.md);
- [`domain/README-part-20.md`](domain/README-part-20.md);
- [`domain/checkpoints/whole-domain-final-regression-v0-validation-part-7.md`](domain/checkpoints/whole-domain-final-regression-v0-validation-part-7.md);
- [`domain/language-map.md`](domain/language-map.md) + [`domain/language-map-part-22.md`](domain/language-map-part-22.md).

Current Domain state: **CLOSED**.

### Logical

- [`logical-model/whole-logical-model-v1.md`](logical-model/whole-logical-model-v1.md);
- complete `logical-model/decision-and-assumption-register-v1*` chain;
- [`logical-model/checkpoints/whole-logical-v1-remote-qa.md`](logical-model/checkpoints/whole-logical-v1-remote-qa.md).

Current Logical state: **CLOSED**.

Product/UI terminology does not override accepted Domain/Logical semantics.

## Accepted Physical Model sources

Current target authority:

- [`physical-model/README.md`](physical-model/README.md) — Physical index/current state;
- [`physical-model/pm-10-recommendation-v1.md`](physical-model/pm-10-recommendation-v1.md) — recommendation result;
- [`physical-model/pm-11-explicit-selection-v1.md`](physical-model/pm-11-explicit-selection-v1.md) — explicit target-stack selection;
- [`physical-model/pm-12-accepted-physical-model-v1.md`](physical-model/pm-12-accepted-physical-model-v1.md) — accepted Physical target;
- [`physical-model/pm-13-clean-room-qa-v1.md`](physical-model/pm-13-clean-room-qa-v1.md) — clean-room architecture/documentation QA;
- [`physical-model/pm-14-closure-v1.md`](physical-model/pm-14-closure-v1.md) — branch closure evidence;
- [`physical-model/recommendation/post-selection-validation-register-v1.md`](physical-model/recommendation/post-selection-validation-register-v1.md) — mandatory implementation-validation carry-forward;
- [`workstreams/physical-model.md`](workstreams/physical-model.md) — workstream handoff.

Phase-10 method/evidence remains available:

- [`architecture/physical-benchmark-specification.md`](architecture/physical-benchmark-specification.md);
- [`architecture/physical-benchmark-scenario-corpus.md`](architecture/physical-benchmark-scenario-corpus.md);
- [`architecture/physical-benchmark-register.md`](architecture/physical-benchmark-register.md).

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
PowerSync Service 1.25.0 Open Edition
encrypted SQLite
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
AWS S3 Standard eu-south-1 backup repositories
Versioning + Object Lock GOVERNANCE / finite policy-bound retention

SOLVER
OR-Tools 9.15 CP-SAT

OBSERVABILITY
OpenTelemetry + Grafana Alloy 1.18.0 + Grafana Cloud EU
```

Canonical authority is singular: PostgreSQL. PowerSync/SQLite, Restate, R2, S3, solver state and telemetry remain bounded noncanonical mechanisms.

## Restate deployment qualification

Restate technology is selected. Deployment is intentionally conditional:

```text
SELF-HOSTED
FIRST-CLASS

CLOUD EU
ALLOWED MANAGED OPTION

GLOBAL DEFAULT
NONE
```

The later deployment/development profile decides between them using privacy, operability, availability and cost. The current Python path must not assume TypeScript-only client-side journal encryption.

## Current architecture sources

Also read:

- [`architecture/pre-physical-architecture-baseline.md`](architecture/pre-physical-architecture-baseline.md)
- [`architecture/requirements/README.md`](architecture/requirements/README.md) + all four Phase 5 packages
- [`architecture/ai-context-runtime-boundaries.md`](architecture/ai-context-runtime-boundaries.md)
- [`architecture/integration-hub-boundaries.md`](architecture/integration-hub-boundaries.md)
- [`architecture/durable-execution-benchmark.md`](architecture/durable-execution-benchmark.md)
- [`architecture/governed-operation-effect-contract.md`](architecture/governed-operation-effect-contract.md)
- [`architecture/search-observability-calendar-solver-boundaries.md`](architecture/search-observability-calendar-solver-boundaries.md)
- [`development/repository-engineering-safety.md`](development/repository-engineering-safety.md)
- [`architecture/system-overview.md`](architecture/system-overview.md)
- [`architecture/technical-decisions.md`](architecture/technical-decisions.md)

Historical `architecture/domain-model-logical-readiness*` files remain truthful transition/validation evidence, not current architecture specifications.

## Direct Physical evidence truth

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

Selection and clean-room QA do not relabel direct implementation evidence. Applicable obligations remain in the post-selection validation register.

## Phase 5–9 contracts remain active

### AI / context / runtime

```text
canonical state
material history
retrieved context
derived context
live external context
candidate / unresolved state
transient LLM working context
```

Runtime Agent/Principal is not Domain Actor automatically; tool/protocol actions are not canonical governed effects; `ExternalRef != NativeRef`; provider revision != `MaterialStateRef`.

Material consequential AI changes require versioned/reproducible evaluation before promotion.

### Governed operations / effects

Consequential meaning remains independent from route/UI/tool/AuthZ/workflow implementation. Request/runtime/canonical/provider/reconciliation axes remain distinct.

### Search / calendar / solver

Search/index state remains derived and disclosure-aware. Calendar standards/providers remain adapter pressure rather than ontology. OR-Tools results remain candidate state and `UNKNOWN != INFEASIBLE`.

## Repository safety

Effective `lifeos-main-safety` remains the protected-main integration policy. Normal changes reach `main` through pull requests; no direct-main bypass is authorized.

## Documentation architecture rule

```text
CURRENT SPECIFICATION = current truth only
ADR = rationale + explicit supersession/qualification
HISTORICAL / VALIDATION EVIDENCE = truthful chronology
GIT / PR HISTORY = recoverable history
```

A size/tool-limit split preserves the complete logical payload losslessly and is not summary/condensation/hidden semantic rewrite.

## Active parallel workstream

Phase 4 Home/Today remains separate on `prototype/phase-4-today-home`.

## Explicit current boundary

```text
PRE-PHYSICAL
DEFINITIVE CLOSED / INTEGRATED / VERIFIED

PHYSICAL MODEL TARGET
CLOSED / SELECTED / ACCEPTED
INTEGRATED INTO MAIN VIA PR #15

DIRECT IMPLEMENTATION VALIDATION
CARRIED FORWARD / NOT RUN

BACKEND FOUNDATION
NOT STARTED / DEFERRED

DEVELOPMENT PROFILE v0
NOT STARTED / NEXT SEPARATE OPERATIONAL SCOPE
```
