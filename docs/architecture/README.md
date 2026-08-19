# Architecture Documentation

- Status: **Current navigation — Physical target accepted; Engineering Foundation v0 active**
- Last updated: 2026-08-19
- Current product/app name: **DANTE** (`LifeOS` remains a legacy working/project name in historical evidence and technical identifiers)

## Purpose

This directory separates **current architectural truth** from historical transition/validation evidence.

Current specifications describe architecture as it is understood now. They are not chronological logs. Historical rationale and transition state remain recoverable through Git, ADRs, checkpoints and explicitly historical evidence.

Engineering Foundation is downstream engineering architecture: it does not reopen Product/Domain/Logical/Physical semantics.

## Current architecture/engineering sources

Read these for current state:

1. [`pre-physical-architecture-baseline.md`](pre-physical-architecture-baseline.md) — closed/integrated Pre-Physical bridge; embedded start-state status is historical after later closure;
2. [`requirements/README.md`](requirements/README.md) + all four Phase-5 requirement packages;
3. [`ai-context-runtime-boundaries.md`](ai-context-runtime-boundaries.md) — Phase-6 AI/context/runtime contract;
4. [`integration-hub-boundaries.md`](integration-hub-boundaries.md) — Phase-6 provider/integration contract;
5. [`durable-execution-benchmark.md`](durable-execution-benchmark.md) — Phase-7 durable-execution contract/evidence; current Physical resolution is Restate;
6. [`governed-operation-effect-contract.md`](governed-operation-effect-contract.md) — Phase-8 governed-operation/effect contract;
7. [`search-observability-calendar-solver-boundaries.md`](search-observability-calendar-solver-boundaries.md) — Phase-9 pressure contract;
8. [`physical-benchmark-specification.md`](physical-benchmark-specification.md) + scenario/register — Phase-10 methodology/evidence;
9. [`../physical-model/pm-11-explicit-selection-v1.md`](../physical-model/pm-11-explicit-selection-v1.md) — selected target stack;
10. [`../physical-model/pm-12-accepted-physical-model-v1.md`](../physical-model/pm-12-accepted-physical-model-v1.md) — accepted Physical target;
11. [`../physical-model/pm-13-clean-room-qa-v1.md`](../physical-model/pm-13-clean-room-qa-v1.md) — clean-room architecture/documentation QA;
12. [`../physical-model/recommendation/post-selection-validation-register-v1.md`](../physical-model/recommendation/post-selection-validation-register-v1.md) — direct implementation-validation carry-forward;
13. [`system-overview.md`](system-overview.md) — current whole-system boundary overview;
14. [`technical-decisions.md`](technical-decisions.md) — current technical summary;
15. [`../workstreams/engineering-foundation.md`](../workstreams/engineering-foundation.md) — active Foundation handoff;
16. [`../development/engineering-foundation-v0.md`](../development/engineering-foundation-v0.md) + all linked detailed Foundation sources;
17. [`../development/repository-engineering-safety.md`](../development/repository-engineering-safety.md);
18. [`../workstreams/physical-model.md`](../workstreams/physical-model.md) — Physical closure/handoff.

## Domain and Logical closure authority

Domain and Logical Models are closed. Their canonical content/evidence is cumulative; an earlier historical status never overrides later explicit closure.

Current Domain result:

```text
PASS WITH HARDENING
POST-WRITE QA PASS
CLOSED
```

Current Logical result:

```text
PASS WITH HARDENING
REMOTE QA PASS
CLOSED
WD-03 PASS
WD-05 PASS
WL-H01..WL-H12 active downstream
```

A physically split/cumulative canonical document is **one logical document**. A size/tool-limit split is a lossless physical partition, never permission to summarize/omit/change semantics.

## Phase 5–9 boundaries remain active

Implementation must preserve the existing distinctions, including:

```text
canonical state
material history
retrieved context
derived context
live external context
candidate / unresolved state
transient LLM working context
```

Integration Hub modes remain distinct:

```text
canonical import
sync/mirror
live federated read
retrieval/index projection
action/tool integration
```

Hard examples:

```text
Person != Account != Principal != Actor
Authority != AuthZ decision
Consent != Authority
Visibility != Authority
AI/model/tool/runtime representation != canonical truth/effect by default
provider state != canonical DANTE state
runtime Agent / Principal != Domain Actor automatically
ExternalRef != NativeRef
MaterialStateRef != provider revision / ETag / MVCC token
idempotency != semantic identity
absence / unknown != false
```

Material consequential AI changes require versioned/reproducible evaluation before promotion. Eval evidence is not canonical truth/authorization.

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
encrypted SQLite
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
Restate = execution runtime
R2 = raw bytes
S3 = recovery copy
OR-Tools = candidate state
OTel/Grafana = telemetry
```

## Physical integration state

```text
PHYSICAL TARGET
CLOSED / SELECTED / ACCEPTED

PROTECTED-MAIN INTEGRATION
COMPLETE VIA PR #15

FORMER BRANCH
feature/physical-model — MERGED / AUTO-DELETED
```

`pm-14-closure-v1.md` remains historical pre-merge closure evidence and is not rewritten by downstream work.

## Durable-execution resolution

```text
BOUNDED ASYNC
PostgreSQL outbox + bounded worker

MATERIAL DURABLE CLASS-B
Restate runtime — SELECTED

INITIAL DEV
DORMANT / NOT ACTIVE
ACTIVATE = first real Class-B durable-workflow need

AT ACTIVATION
self-hosted FIRST-CLASS
Cloud EU ALLOWED MANAGED OPTION
global default NONE
```

Self-hosted vs Cloud EU is **not a current day-1 decision**. It opens only when the fixed activation trigger exists. Runtime state does not become Domain ontology/history and no workflow runtime creates exactly-once external reality.

Current Python use must not assume TypeScript-only Restate client-side journal encryption; journal minimization remains mandatory when Restate activates.

## Recovery activation resolution

```text
pgBackRest + AWS S3 eu-south-1
SELECTED RECOVERY TARGET

INITIAL DEV
DORMANT / NOT ACTIVE

ACTIVATE
recovery/production boundary
OR real recovery-rehearsal requirement
```

This dormant posture is already fixed and Engineering Foundation does not reopen it.

## Search / observability / calendar / solver resolution

```text
SEARCH
PostgreSQL native FTS + pg_trgm + unaccent
pgvector for bounded vector retrieval
no dedicated search/vector server

OBSERVABILITY
OpenTelemetry + Grafana Alloy + Grafana Cloud EU target
telemetry != canonical/audit ontology

CALENDAR
iCalendar / JSCalendar / providers = adapter pressure, not ontology

SOLVER
OR-Tools 9.15 CP-SAT
UNKNOWN != INFEASIBLE
solver output != accepted canonical effect
```

## Engineering Foundation v0

Engineering Foundation is the active final pre-implementation engineering-design scope.

Branch baseline:

```text
REPOSITORY
polyglot monorepo
apps/api + apps/web + apps/mobile
precise shared packages only

BACKEND
capability-first modular monolith
explicit composition root
application/domain independent from FastAPI/SQLAlchemy/provider adapters by identity

ENVIRONMENTS
LOCAL + DEV + UAT + PROD
optional ephemeral preview environments
no environment Git branches

DATABASE ENGINEERING
SQLAlchemy 2.0 stable + psycopg 3 + Alembic
real PostgreSQL integration testing
migration release job separate from app startup
expand/migrate/contract when compatibility requires it

TOOLCHAIN
Python 3.14 + uv + Ruff + mypy + pytest
Node 24 LTS + pnpm 11 + strict TypeScript + ESLint + Prettier
Turborepo for JS/TS task graph

DELIVERY
GitHub Actions primary CI/CD orchestration
GitHub Environments for privileged deployment once real workflows exist
immutable artifact/release identity
build-once promotion where platform permits
secrets external / least privilege / OIDC where supported
```

No production code is created by this design branch. Exact compute host/IaC engine remain deferred until real remote infrastructure implementation supplies the missing provider facts.

The previously proposed standalone Development Profile is no longer a separate next phase; its valid operational concerns are now covered by Foundation and by capability/release implementation.

## Physical direct-evidence truth

```text
DATABASE DEPLOYMENT      NOT STARTED
FIXTURE/HARNESS           NOT STARTED
DIRECT HG PASS            0
LOW/BASE/HIGH             NOT RUN
RESTORE/MIGRATION         NOT RUN
FAILURE INJECTION         NOT RUN
POWERSYNC                 NOT RUN
RESTATE                   NOT RUN
OBJECT RECOVERY           NOT RUN
SOLVER                    NOT RUN
VERIFIED-RUN SCORE        NOT AVAILABLE
```

The authoritative carry-forward register is [`../physical-model/recommendation/post-selection-validation-register-v1.md`](../physical-model/recommendation/post-selection-validation-register-v1.md).

## Repository engineering safety

Current `main` policy requires protected PR integration, blocks destructive/non-fast-forward updates, requires review-thread resolution and does not invent required CI contexts before real stable checks exist.

Engineering Foundation selects GitHub Actions as future primary CI/CD orchestration, but no status check becomes a protected-main requirement until its real emitted context and blocking value are verified.

## Current stage boundary

```text
Product / North Star                      CURRENT
Domain Model / Domain Atlas              CLOSED
Logical Model                            CLOSED
Phase 5 requirements                     CURRENT
Phase 6 boundaries                       CURRENT
Phase 7 durable-execution contract       CURRENT / PHYSICAL MECHANISM RESOLVED
Phase 8 governed-effect contract         CURRENT
Phase 9 pressure contract                CURRENT / PHYSICAL MECHANISMS RESOLVED WHERE SELECTED
Phase 10 benchmark method                CURRENT METHOD / HISTORICAL DECISION-EVIDENCE AUTHORITY
Repository engineering safety            QA PASS at verified scope
Pre-Physical Coherence                   CLOSED / INTEGRATED / VERIFIED

Physical Model target
CLOSED / SELECTED / ACCEPTED / INTEGRATED

Direct selected-stack implementation validation
NOT STARTED / CARRIED FORWARD

Engineering Foundation v0
ACTIVE / UNMERGED / PENDING FINAL REVIEW + QA

Backend / production implementation
NOT STARTED
NEXT AFTER FOUNDATION ACCEPTANCE/INTEGRATION
```

## Historical transition / validation evidence

The `domain-model-logical-readiness*` chain and Phase-7..10 benchmark records preserve truthful transition/evidence history. They do not override later PM-11/12 selected Physical truth or current Engineering Foundation execution direction.

## Documentation rule

```text
CURRENT SPECIFICATION = current truth only
HISTORICAL / VALIDATION EVIDENCE = truthful chronology
ADR = rationale + explicit supersession/qualification
GIT / PR HISTORY = recoverable history
```

Before replacing/deleting stale current documentation prove:

```text
unclassified meaningful content = 0
valid requirement lost = 0
current truth represented = PASS
rationale worth retaining mapped = PASS
references/navigation repaired = PASS
```