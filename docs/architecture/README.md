# Architecture Documentation

- Status: **Current navigation — Physical Model target selected/accepted/integrated**
- Last updated: 2026-08-18
- Current product/app name: **DANTE** (`LifeOS` remains a legacy working/project name in historical evidence and technical identifiers)

## Purpose

This directory separates **current architectural truth** from historical transition/validation evidence.

Current specifications describe the architecture as it is understood now. They are not chronological logs. Historical rationale and transition state remain recoverable through Git, ADRs, checkpoints and explicitly historical evidence.

## Current architecture sources

Read these for current architecture state:

1. [`pre-physical-architecture-baseline.md`](pre-physical-architecture-baseline.md) — closed/integrated Pre-Physical bridge and downstream constraints; its Physical-start status is a historical handoff snapshot;
2. [`requirements/README.md`](requirements/README.md) + all four Phase 5 requirement packages;
3. [`ai-context-runtime-boundaries.md`](ai-context-runtime-boundaries.md) — Phase 6 AI/context/runtime contract;
4. [`integration-hub-boundaries.md`](integration-hub-boundaries.md) — Phase 6 provider/integration contract;
5. [`durable-execution-benchmark.md`](durable-execution-benchmark.md) — Phase 7 durable-execution contract/evidence; candidate-status prose is phase-time history and the current Physical resolution is Restate;
6. [`governed-operation-effect-contract.md`](governed-operation-effect-contract.md) — Phase 8 governed-operation/effect contract;
7. [`search-observability-calendar-solver-boundaries.md`](search-observability-calendar-solver-boundaries.md) — Phase 9 pressure contract; selection-status prose is phase-time history where PM-11/12 later resolved the mechanism;
8. [`physical-benchmark-specification.md`](physical-benchmark-specification.md) — Phase 10 benchmark methodology/evidence framework; phase-time Physical-status prose does not override closed PM-11/12 truth;
9. [`physical-benchmark-scenario-corpus.md`](physical-benchmark-scenario-corpus.md) — Phase 10 corpus/scenarios;
10. [`physical-benchmark-register.md`](physical-benchmark-register.md) — historical candidate/direct-execution ledger;
11. [`../physical-model/pm-11-explicit-selection-v1.md`](../physical-model/pm-11-explicit-selection-v1.md) — selected target stack;
12. [`../physical-model/pm-12-accepted-physical-model-v1.md`](../physical-model/pm-12-accepted-physical-model-v1.md) — accepted Physical target architecture;
13. [`../physical-model/pm-13-clean-room-qa-v1.md`](../physical-model/pm-13-clean-room-qa-v1.md) — clean-room architecture/documentation QA;
14. [`../physical-model/recommendation/post-selection-validation-register-v1.md`](../physical-model/recommendation/post-selection-validation-register-v1.md) — implementation-validation carry-forward;
15. [`system-overview.md`](system-overview.md) — current system boundary overview;
16. [`technical-decisions.md`](technical-decisions.md) — current technical decisions;
17. [`../development/repository-engineering-safety.md`](../development/repository-engineering-safety.md) — repository-safety contract;
18. [`../workstreams/physical-model.md`](../workstreams/physical-model.md) — Physical workstream closure/handoff.

## Domain and Logical closure authority

The Domain and Logical Models are closed. Their canonical content/evidence is cumulative; an earlier historical status never overrides a later explicit closure record.

For Domain current closure read:

- [`../domain/README.md`](../domain/README.md);
- [`../domain/README-part-20.md`](../domain/README-part-20.md);
- [`../domain/checkpoints/whole-domain-final-regression-v0-validation-part-7.md`](../domain/checkpoints/whole-domain-final-regression-v0-validation-part-7.md);
- [`../domain/language-map.md`](../domain/language-map.md) + [`../domain/language-map-part-22.md`](../domain/language-map-part-22.md).

Current Domain result:

```text
PASS WITH HARDENING
POST-WRITE QA PASS
CLOSED
```

For Logical closure read:

- [`../logical-model/whole-logical-model-v1.md`](../logical-model/whole-logical-model-v1.md);
- complete `decision-and-assumption-register-v1*` chain;
- [`../logical-model/checkpoints/whole-logical-v1-remote-qa.md`](../logical-model/checkpoints/whole-logical-v1-remote-qa.md).

A physically split/cumulative canonical document is **one logical document**. A size/tool-limit split is a lossless physical partition, never permission to summarize/omit/change semantics.

## Phase 5 requirement package

Current requirement owners remain:

- [`requirements/authn-authz.md`](requirements/authn-authz.md);
- [`requirements/security-privacy-retention-recovery.md`](requirements/security-privacy-retention-recovery.md);
- [`requirements/consistency-side-effects.md`](requirements/consistency-side-effects.md);
- [`requirements/nonfunctional-multidevice-recovery.md`](requirements/nonfunctional-multidevice-recovery.md).

They define requirements/open parameters rather than inventing business targets.

## Phase 6 boundaries

Keep distinct:

```text
canonical state
material history
retrieved context
derived context
live external context
candidate / unresolved state
transient LLM working context
```

Integration modes remain distinct:

```text
canonical import
sync/mirror
live federated read
retrieval/index projection
action/tool integration
```

```text
AI/model/tool/runtime representation != canonical truth/effect by default
provider state != canonical DANTE state
runtime Agent / Principal != Domain Actor automatically
ExternalRef != NativeRef
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

PHYSICAL INTEGRATION COMMIT
e6f191bad947388a44defe2c15f4939345084f58

FORMER BRANCH
feature/physical-model — MERGED / AUTO-DELETED
```

That SHA identifies the Physical integration event; it is **not intended to track the moving current `main` HEAD**.

PM-14 remains historical closure evidence for the pre-merge state and is not rewritten by the later integration event.

## Durable-execution resolution

The Phase-7 contract remains current; its prior candidate ranking is now physically resolved:

```text
BOUNDED ASYNC
PostgreSQL outbox + bounded worker

MATERIAL DURABLE CLASS-B
Restate runtime — SELECTED

RESTATE DEPLOYMENT
self-hosted FIRST-CLASS
Cloud EU ALLOWED MANAGED OPTION
global default NONE
```

Temporal and DBOS remain non-selected historical challengers. Runtime state does not become Domain ontology/history and no workflow runtime creates exactly-once external reality.

Current Restate Cloud client-side journal encryption must not be assumed for the Python path where the capability is currently documented only for TypeScript; journal minimization and later deployment privacy review remain mandatory.

## Search / observability / calendar / solver resolution

The Phase-9 boundary contract remains current; PM-11/12 later resolved its selectable mechanisms as follows:

```text
SEARCH
PostgreSQL native FTS + pg_trgm + unaccent selected
pgvector selected for bounded vector retrieval
no dedicated search/vector server in accepted target

OBSERVABILITY
OpenTelemetry + Grafana Alloy + Grafana Cloud EU target selected
telemetry != canonical/audit ontology

CALENDAR
iCalendar / JSCalendar / provider models = adapter pressure, not ontology

SOLVER
OR-Tools 9.15 CP-SAT selected
UNKNOWN != INFEASIBLE
solver output != accepted canonical effect
```

## Physical direct-evidence truth

The accepted target is evidence-backed but direct selected-stack implementation validation has not run:

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

The authoritative carry-forward register is [`../physical-model/recommendation/post-selection-validation-register-v1.md`](../physical-model/recommendation/post-selection-validation-register-v1.md).

## Repository engineering safety

Current `main` policy requires PR integration, blocks deletion/non-fast-forward, requires review-thread resolution, uses zero approvals while no independent reviewer exists and no required CI checks until stable real contexts exist.

Physical integration used that protected path through PR #15. Future Development Profile/backend/direct-validation writes remain separately gated.

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
Repository engineering safety            QA PASS
Pre-Physical Coherence                   CLOSED / INTEGRATED / VERIFIED

Physical Model target
CLOSED / SELECTED / ACCEPTED
PM-13 clean-room architecture/documentation QA PASS
INTEGRATED INTO MAIN VIA PR #15

Direct selected-stack implementation validation
NOT STARTED / CARRIED FORWARD

Backend production implementation
NOT STARTED / DEFERRED

Development Profile v0
NOT STARTED / NEXT SEPARATE OPERATIONAL SCOPE
```

## Historical transition / validation evidence

The `domain-model-logical-readiness*` chain and Phase-7..10 benchmark records preserve truthful transition/evidence history. They do not override the later PM-11/12 selected/accepted Physical target.

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
