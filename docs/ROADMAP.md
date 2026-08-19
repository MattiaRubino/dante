# DANTE Roadmap

- Last updated: 2026-08-19
- Purpose: current delivery/architecture-stage sequence, not a calendar commitment

## Completed foundations

### Product / North Star

Accepted current DANTE identity/North Star and supporting product studies are integrated.

```text
CURRENT PRODUCT / APP NAME
DANTE

PREVIOUS WORKING / PROJECT NAME
LifeOS

LEGACY REFERENCES
Historical evidence, Git history and existing technical/repository identifiers
may still use LifeOS for the same product lineage.
```

### Core Domain Model / Domain Atlas

**CLOSED — integrated into `main` via PR #10.**

```text
Whole-Domain PASS WITH HARDENING
POST-WRITE QA PASS
```

### Logical Model

**CLOSED — integrated into `main` via PR #11.**

```text
Whole-Logical PASS WITH HARDENING
REMOTE QA PASS
WD-03 PASS
WD-05 PASS
WL-H01..WL-H12 active downstream
```

### Pre-Physical Repository & Architecture Coherence

**DEFINITIVE CLOSED / FINAL QA PASS / integrated / post-merge verified.**

```text
Phase 0–11         QA PASS
Phase 12           QA PASS / CLOSED
Independent audit  PASS
PR #13             Pre-Physical integration
PR #14             post-merge current-truth alignment
```

### Physical Model target architecture

**CLOSED / SELECTED / ACCEPTED / INTEGRATED INTO `main` VIA PR #15.**

```text
PM-00..PM-14 target-architecture work COMPLETE at stated statuses
PM-11 explicit user-approved selection COMPLETE
PM-12 Accepted Physical Model COMPLETE
PM-13 clean-room architecture/documentation QA PASS
PM-14 branch closure COMPLETE
PR #15 protected-main integration COMPLETE
```

Selected canonical primary:

```text
PostgreSQL 18.4
```

Selected companion target:

```text
PostGIS 3.6.4
pgvector 0.8.6
PostgreSQL native FTS / pg_trgm / unaccent
pg_stat_statements
PgBouncer 1.25.2
PowerSync 1.25.0 Open Edition
encrypted SQLite
PostgreSQL transactional outbox + bounded worker
Restate runtime
Cloudflare R2 Standard EU/private
pgBackRest 2.59.0
AWS S3 Standard eu-south-1 recovery target
OR-Tools 9.15 CP-SAT
OpenTelemetry + Grafana Alloy 1.18.0 + Grafana Cloud EU
```

Canonical persistence authority remains **one: PostgreSQL**.

## Fixed initial activation posture

```text
RESTATE
SELECTED TARGET
INITIAL DEV = DORMANT / NOT ACTIVE
ACTIVATE ON FIRST REAL CLASS-B DURABLE-WORKFLOW NEED
SELF-HOSTED vs CLOUD EU DECIDED ONLY AT ACTIVATION

pgBackRest + AWS S3 eu-south-1
SELECTED RECOVERY TARGET
INITIAL DEV = DORMANT / NOT ACTIVE
ACTIVATE AT RECOVERY/PRODUCTION BOUNDARY
OR WHEN A REAL RECOVERY-REHEARSAL REQUIREMENT EXISTS
```

These are settled day-1 decisions and are not reopened by later implementation planning.

## Direct Physical evidence truth retained

Target closure/integration and Engineering Foundation design do not mean direct implementation execution occurred.

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

The post-selection validation register remains mandatory at the applicable implementation/release boundaries.

## Current engineering track — Engineering Foundation v0

**ACTIVE / UNMERGED on `chore/engineering-foundation-v0`.**

This is the final bounded engineering-design workstream before production implementation.

It defines and freezes:

```text
polyglot monorepo / path ownership
capability-first modular-monolith structure
web/mobile/backend dependency boundaries
LOCAL / DEV / UAT / PROD lifecycle
configuration / secret / credential rules
runtime / package / dependency versioning
PostgreSQL development and migration workflow
test taxonomy / architecture enforcement
GitHub Actions CI/CD model
artifact identity / promotion
supply-chain controls
developer bootstrap / DX conventions
```

Current branch specification set:

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

### Foundation baseline direction

```text
REPOSITORY
polyglot monorepo
apps/api + apps/web + apps/mobile
precise shared TypeScript packages only

BACKEND
Python + FastAPI + Pydantic
capability-first modular monolith
explicit composition root
SQLAlchemy 2.0 stable + psycopg 3 + Alembic

PYTHON TOOLCHAIN
Python 3.14 line
uv + committed lockfile
Ruff + mypy strict + pytest

JS TOOLCHAIN
Node 24 LTS
pnpm 11 + committed lockfile
TypeScript strict + ESLint + Prettier
Turborepo for JS/TS task graph

LOCAL
Linux semantics canonical for backend
Windows backend path through WSL2/Linux
Docker Compose for stateful dependencies
real PostgreSQL for persistence/integration testing

DELIVERY
GitHub Actions primary CI/CD orchestration
GitHub Environments for privileged deployment once workflows exist
immutable release identity by commit/build/digest
build once/promote same server/web artifact where platform permits
mobile builds remain explicitly environment/signing-profile specific

SECURITY / SUPPLY CHAIN
secrets external to Git
OIDC/short-lived deployment identity where supported
least privilege
locked dependencies
CodeQL/dependency review/attestation activated with real source/artifacts, not placeholders
```

No production code is created by this workstream.

## Standalone Development Profile v0 — sequence decision

The previously proposed standalone Development Profile is **no longer a separate next stage**.

Its useful concerns have been absorbed into:

1. Engineering Foundation for durable development/environment/configuration rules; and
2. the real implementation/release boundary that has enough facts to activate a selected component.

This avoids a speculative pass over every selected technology merely to decide whether it is installed on day one.

The accepted Physical target remains unchanged.

## Production implementation — next after Foundation closure

Production application code remains:

```text
NOT STARTED
```

After Engineering Foundation receives final review, exact remote QA and protected-main integration, the delivery sequence becomes:

```text
1. production repository scaffold
   - create real apps/packages/infra/tooling manifests only where used
   - pin runtimes/package managers/lockfiles
   - establish first real CI contexts

2. backend bootstrap
   - FastAPI process/composition root
   - typed config
   - logging/observability baseline
   - module/dependency enforcement

3. PostgreSQL development foundation
   - pinned LOCAL PostgreSQL 18.4 profile
   - required selected extensions for implemented slices
   - SQLAlchemy/psycopg wiring
   - Alembic migration harness
   - real PostgreSQL integration-test harness

4. concrete Logical -> PostgreSQL implementation
   - owner/reference mappings
   - constraints/indexes/history
   - transaction/expected-state semantics
   - migration chain

5. first vertical production slices
   - application use case
   - persistence
   - governed backend contract
   - tests
   - generated client contract where applicable

6. specialist Physical capabilities as real use-cases arrive
   - PostGIS/search/pgvector
   - PowerSync/SQLite
   - R2
   - OR-Tools
   - Restate only at fixed Class-B trigger
   - recovery target at fixed recovery/production trigger
```

This is the transition from architecture/design into normal production engineering.

## Active parallel product/design track

### Phase 4 — UX prototype/product-structure validation

Separate workstream on `prototype/phase-4-today-home`.

It may continue independently but does not redefine accepted Domain/Logical/Physical/backend engineering authority.

## Upstream constraints that remain active

Later engineering must preserve:

- CLOSED Domain Atlas and final closure/language authority;
- CLOSED Whole Logical Model + complete decision register + `WL-H01..WL-H12`;
- accepted Physical Model ownership/topology boundaries;
- Phase 5 AuthN/AuthZ, security/privacy/retention/recovery, consistency/side-effects and NFR/multi-device/recovery requirements;
- Phase 6 AI/context/runtime and Integration Hub boundaries;
- consequential AI behavior-change evaluation requirement;
- Phase 7 durable-execution contract as physically resolved by PM-11/12;
- Phase 8 governed operation/effect contract;
- Phase 9 search/observability/calendar/solver contract as physically resolved where selected;
- calendar/provider adapter separation;
- selected-stack direct validation obligations;
- repository engineering safety;
- Engineering Foundation rules once accepted/integrated.

```text
SEMANTIC OWNER != IMPLEMENTATION MECHANISM
DOMAIN TERM != ENGINE
ADDRESSABILITY != DOMAIN IDENTITY
STORAGE COINCIDENCE != SEMANTIC EQUIVALENCE
SELECTED != DIRECT PASS
SELECTED != DEPLOYED
```

## AI evaluation posture

Material consequential changes to model/version/provider, prompt/instruction layer, Context Builder policy, tool/action schema, tool-selection policy or fallback/routing policy require versioned/reproducible evaluation before promotion.

```text
eval result != canonical DANTE truth
eval PASS != Authority / governed-effect authorization
```

## Repository engineering safety

`main` remains protected by the verified repository-safety policy. Normal integration uses the protected PR path. No direct-main bypass, no invented required checks and no production secrets/personal data in test/evidence artifacts.

Engineering Foundation selects GitHub Actions as the future primary CI/CD orchestration mechanism, but **no required status check is added until a real workflow emits a stable verified context whose failure should block merge**.

## Immediate sequence

```text
1. complete Engineering Foundation v0 documentation/current-truth alignment
2. exact scope/readback/coherence QA
3. user acceptance
4. protected PR integration
5. start production repository scaffold under a fresh exact implementation scope
6. continue backend/database vertical implementation
7. discharge applicable PSV obligations as the corresponding capabilities/release boundaries become real
```