# Documentation Index

This directory is the durable project memory for DANTE. A new human or AI contributor should be able to resume from repository truth without reconstructing decisions from chat history.

> **Naming continuity:** `DANTE` is the current product/app name. `LifeOS` is the previous working/project name and remains valid where it appears in historical evidence, Git history or existing technical/repository identifiers for the same product lineage.

## Start here

Read in this order:

1. [`../README.md`](../README.md)
2. [`PROJECT-STATUS.md`](PROJECT-STATUS.md)
3. [`development/agent-operating-manual.md`](development/agent-operating-manual.md)
4. [`development/operating-rules.md`](development/operating-rules.md)
5. [`development/documentation-and-handoff.md`](development/documentation-and-handoff.md)
6. [`development/branching-and-environments.md`](development/branching-and-environments.md)
7. [`development/repository-engineering-safety.md`](development/repository-engineering-safety.md)
8. [`workstreams/engineering-foundation.md`](workstreams/engineering-foundation.md) when working on the active Foundation branch
9. [`development/engineering-foundation-v0.md`](development/engineering-foundation-v0.md) + its detailed linked sources
10. [`workstreams/physical-model.md`](workstreams/physical-model.md)
11. [`physical-model/README.md`](physical-model/README.md)
12. [`physical-model/pm-11-explicit-selection-v1.md`](physical-model/pm-11-explicit-selection-v1.md)
13. [`physical-model/pm-12-accepted-physical-model-v1.md`](physical-model/pm-12-accepted-physical-model-v1.md)
14. [`physical-model/recommendation/post-selection-validation-register-v1.md`](physical-model/recommendation/post-selection-validation-register-v1.md)
15. [`architecture/README.md`](architecture/README.md) and linked Phase-5..10 current sources where relevant
16. complete Domain/Logical closure authority where semantics are involved
17. relevant ADRs/evidence/methodologies
18. current Git refs/branch relation to `main`

`main` remains the integrated source of accepted truth. The active Engineering Foundation branch may contain newer bounded unmerged truth only inside its approved workstream scope.

## Current project stage

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

PHYSICAL MODEL TARGET
CLOSED / SELECTED / ACCEPTED
PM-11 selection COMPLETE
PM-12 Accepted Physical Model COMPLETE
PM-13 clean-room architecture/documentation QA PASS
PM-14 branch closure COMPLETE
INTEGRATED INTO MAIN VIA PR #15
selected canonical primary PostgreSQL 18.4

DIRECT SELECTED-STACK IMPLEMENTATION VALIDATION
NOT STARTED
DIRECT HG PASS 0
VERIFIED-RUN SCORE NOT AVAILABLE

ENGINEERING FOUNDATION v0
ACTIVE on chore/engineering-foundation-v0
professional development/repository/environment/toolchain/testing/CI baseline
production code still NOT STARTED

STANDALONE DEVELOPMENT PROFILE v0
NO LONGER THE NEXT SEPARATE PHASE
operational concerns are absorbed into Engineering Foundation and the real capability/release boundary that needs them

RESTATE initial DEV
DORMANT UNTIL FIRST REAL CLASS-B NEED

pgBackRest + AWS S3 initial DEV
DORMANT UNTIL RECOVERY/PRODUCTION BOUNDARY OR REAL RECOVERY REHEARSAL
```

Phase 4 Home/Today remains a separate active product/design workstream on `prototype/phase-4-today-home`.

## Engineering Foundation v0

Current active branch sources:

- [`workstreams/engineering-foundation.md`](workstreams/engineering-foundation.md) — operational save-game/status;
- [`development/engineering-foundation-v0.md`](development/engineering-foundation-v0.md) — master engineering contract;
- [`development/repository-layout-v0.md`](development/repository-layout-v0.md) — monorepo/path ownership/generated-artifact contract;
- [`development/application-structure-v0.md`](development/application-structure-v0.md) — backend/web/mobile boundaries;
- [`development/environments-and-promotion-v0.md`](development/environments-and-promotion-v0.md) — LOCAL/DEV/UAT/PROD and release promotion;
- [`development/config-and-secrets-v0.md`](development/config-and-secrets-v0.md) — typed configuration/credentials/secrets;
- [`development/toolchain-and-dx-v0.md`](development/toolchain-and-dx-v0.md) — runtimes/package managers/local developer contract;
- [`development/testing-and-ci-v0.md`](development/testing-and-ci-v0.md) — automated validation/CI/CD/supply-chain contract.

Branch baseline direction:

```text
polyglot monorepo
apps/api + apps/web + apps/mobile
capability-first modular monolith
LOCAL / DEV / UAT / PROD environment model
GitHub Actions primary CI/CD orchestration
GitHub Environments for privileged deployments once workflows exist
Python 3.14 + uv + Ruff + mypy + pytest
SQLAlchemy 2.0 + psycopg 3 + Alembic
Node 24 LTS + pnpm 11 + TypeScript strict + ESLint + Prettier
Turborepo for JS/TS workspace task graph
real PostgreSQL integration testing
migrations separated from application startup
immutable artifact identity/promotion where platform permits
OIDC / least-privilege deployment identity where provider permits
```

This is active engineering design, not an implementation PASS and not production code.

## Current semantic/model authority

### Product

- [`product/product-identity-and-north-star.md`](product/product-identity-and-north-star.md) — current DANTE product/North Star.

### Domain

The Domain authority is cumulative. Current closure includes:

- [`domain/README.md`](domain/README.md) + complete continuation chain;
- [`domain/checkpoints/whole-domain-final-regression-v0-validation-part-7.md`](domain/checkpoints/whole-domain-final-regression-v0-validation-part-7.md);
- [`domain/language-map.md`](domain/language-map.md) + complete continuation chain.

Current Domain state: **CLOSED**.

### Logical

- [`logical-model/whole-logical-model-v1.md`](logical-model/whole-logical-model-v1.md);
- complete `logical-model/decision-and-assumption-register-v1*` chain;
- [`logical-model/checkpoints/whole-logical-v1-remote-qa.md`](logical-model/checkpoints/whole-logical-v1-remote-qa.md).

Current Logical state: **CLOSED**. Product/UI terminology does not override accepted Domain/Logical semantics.

## Accepted Physical Model

Current target authority:

- [`physical-model/README.md`](physical-model/README.md);
- [`physical-model/pm-10-recommendation-v1.md`](physical-model/pm-10-recommendation-v1.md);
- [`physical-model/pm-11-explicit-selection-v1.md`](physical-model/pm-11-explicit-selection-v1.md);
- [`physical-model/pm-12-accepted-physical-model-v1.md`](physical-model/pm-12-accepted-physical-model-v1.md);
- [`physical-model/pm-13-clean-room-qa-v1.md`](physical-model/pm-13-clean-room-qa-v1.md);
- [`physical-model/pm-14-closure-v1.md`](physical-model/pm-14-closure-v1.md) — historical branch-closure evidence;
- [`physical-model/recommendation/post-selection-validation-register-v1.md`](physical-model/recommendation/post-selection-validation-register-v1.md);
- [`workstreams/physical-model.md`](workstreams/physical-model.md).

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
PowerSync Service 1.25.0 Open Edition
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

Canonical authority is singular: PostgreSQL. PowerSync/SQLite, Restate, R2, S3, solver state and telemetry remain bounded noncanonical mechanisms.

## Fixed initial activation posture

```text
Restate runtime
SELECTED TARGET
INITIAL DEV = DORMANT / NOT ACTIVE
ACTIVATE = first real Class-B durable-workflow need
DEPLOYMENT MODE = decide only at activation

pgBackRest + AWS S3 eu-south-1
SELECTED RECOVERY TARGET
INITIAL DEV = DORMANT / NOT ACTIVE
ACTIVATE = recovery/production boundary OR real recovery-rehearsal requirement
```

Engineering Foundation consumes these decisions and does not reopen them. Other selected components enter implementation when their real capability arrives, with applicable PSV obligations preserved.

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

Selection, Foundation design and documentation QA do not relabel direct implementation evidence.

## Current architecture sources

Also read:

- [`architecture/pre-physical-architecture-baseline.md`](architecture/pre-physical-architecture-baseline.md);
- [`architecture/requirements/README.md`](architecture/requirements/README.md) + all four Phase-5 packages;
- [`architecture/ai-context-runtime-boundaries.md`](architecture/ai-context-runtime-boundaries.md);
- [`architecture/integration-hub-boundaries.md`](architecture/integration-hub-boundaries.md);
- [`architecture/durable-execution-benchmark.md`](architecture/durable-execution-benchmark.md);
- [`architecture/governed-operation-effect-contract.md`](architecture/governed-operation-effect-contract.md);
- [`architecture/search-observability-calendar-solver-boundaries.md`](architecture/search-observability-calendar-solver-boundaries.md);
- [`architecture/system-overview.md`](architecture/system-overview.md);
- [`architecture/technical-decisions.md`](architecture/technical-decisions.md);
- [`development/repository-engineering-safety.md`](development/repository-engineering-safety.md).

Historical `architecture/domain-model-logical-readiness*` files and phase-time candidate/status prose remain evidence/history and do not override newer accepted/current truth.

## Active cross-cutting contracts

Keep distinct throughout implementation:

```text
Person != Account != Principal != Actor
Authority != AuthZ decision
Consent != Authority
Visibility != Authority
provider state != canonical DANTE state
derived projection != canonical truth
absence / unknown != false
MaterialStateRef != ETag/MVCC/provider revision
idempotency != semantic identity
AI / solver output != accepted canonical effect
```

AI/context/runtime, Integration Hub, governed-operation/effect, search/calendar/solver and `WL-H01..WL-H12` contracts remain active downstream.

## Repository safety

The remotely verified protected-main policy remains the integration mechanism. Normal changes reach `main` through pull requests. No direct-main bypass, invented required status checks, production secrets or personal production data in tests/evidence are authorized.

## Documentation architecture rule

```text
CURRENT SPECIFICATION = current truth only
ADR = rationale + explicit supersession/qualification
HISTORICAL / VALIDATION EVIDENCE = truthful chronology
GIT / PR HISTORY = recoverable history
```

A size/tool-limit split preserves the complete logical payload losslessly; it is not permission for hidden summarization or semantic rewrite.

## Next boundary

```text
ENGINEERING FOUNDATION v0
ACTIVE / PENDING REVIEW + QA + INTEGRATION

THEN
production repository scaffold
→ backend bootstrap/composition root
→ PostgreSQL local profile + migration harness
→ concrete Logical-to-PostgreSQL schema
→ vertical production implementation

DIRECT PSV
CARRIED FORWARD / NOT RUN
```