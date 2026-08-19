# Workstream — Engineering Foundation v0

- Status: **ACTIVE — DESIGN BASELINE IN PROGRESS**
- Branch: `chore/engineering-foundation-v0`
- Approved PRE-SCOPE: `ebc3616956faeabd99d90f5f32458b284be218e4`
- Started: 2026-08-19
- Product: **DANTE**
- Domain Model: **CLOSED / CONSUMED / NOT REOPENED**
- Logical Model: **CLOSED / CONSUMED / WL-H01..WL-H12 ACTIVE**
- Physical Model target: **CLOSED / SELECTED / ACCEPTED / CONSUMED**
- Production application code: **NOT STARTED**
- Direct selected-stack implementation validation: **NOT STARTED / DIRECT HG PASS 0**

## 1. Purpose

Engineering Foundation v0 is the final bounded engineering-design workstream before DANTE begins production application implementation.

It defines **how DANTE will be engineered**, not new product semantics and not a replacement for the closed Domain, Logical or Physical models.

The workstream freezes the professional development baseline for:

- repository and monorepo topology;
- application/module boundaries;
- LOCAL / DEV / UAT / PROD environment semantics;
- configuration and secret handling;
- runtime/package/toolchain version policy;
- database-development and migration workflow;
- testing architecture;
- CI/CD, artifact and promotion discipline;
- developer experience and standard execution conventions;
- generated/local artifact policy;
- supply-chain and repository integration controls.

The quality bar is production-grade engineering suitable for a growing multi-client product. Complexity is admitted only when it enforces a real boundary, reproducibility, safety or operability requirement.

## 2. Explicit non-goals

This workstream does **not** implement or design the concrete business/database payload.

```text
NO production application code
NO concrete PostgreSQL tables/columns/schema mapping
NO migration implementation
NO API route/DTO implementation
NO Auth implementation
NO business use-case implementation
NO Domain / Logical / Physical reopen
NO selected Physical technology replacement
NO PowerSync implementation
NO R2 implementation
NO OR-Tools implementation
NO Restate activation
NO AWS recovery activation
NO direct PSV PASS claims
NO Phase-4 frontend production integration
```

A foundation decision may define where/how a future implementation belongs without implementing that capability now.

## 3. Inherited decisions that are not open

Engineering Foundation consumes the following accepted direction:

```text
WEB
Next.js + React + TypeScript

MOBILE
Expo + React Native + TypeScript

BACKEND
Python + FastAPI + Pydantic
modular monolith first

CANONICAL PERSISTENCE
PostgreSQL 18.4

REST OF PHYSICAL TARGET
PM-11 / PM-12 selected stack
```

Two initial activation decisions remain fixed:

```text
RESTATE
SELECTED TARGET
INITIAL DEV = DORMANT / NOT ACTIVE
ACTIVATE = first real Class-B durable-workflow need
DEPLOYMENT MODE = decide only at activation

pgBackRest + AWS S3 eu-south-1
SELECTED RECOVERY TARGET
INITIAL DEV = DORMANT / NOT ACTIVE
ACTIVATE = recovery/production boundary
           OR real recovery-rehearsal requirement
```

Engineering Foundation must not turn either item back into a day-1 choice.

## 4. Engineering principles

The foundation applies these rules:

1. **Trunk-based integration** — protected `main` is the only integrated truth; short-lived bounded branches merge by PR.
2. **Monorepo, not distributed drift** — web, mobile, API, shared contracts, infrastructure definition and durable documentation remain in one repository unless a later measured boundary justifies extraction.
3. **Modular monolith before services** — internal module boundaries are enforceable without paying distributed-system cost before it is necessary.
4. **Capability-first structure** — business capabilities own their vertical implementation; technical layers do not become a repository-wide dumping ground.
5. **Explicit composition root** — dependency wiring happens at the edge, not through hidden globals/service locators.
6. **One canonical truth** — implementation convenience never creates another DANTE semantic authority.
7. **Build reproducibly** — runtimes, package managers, dependencies and generated artifacts are versioned/locked.
8. **Build once, promote** — deployable artifacts are immutable and promoted across environments wherever the platform permits.
9. **Environment isolation** — DEV/UAT/PROD have separate state, identities and credentials; Git branches do not represent environments.
10. **Secrets external to Git** — clients never receive secrets; deployed secrets use environment-scoped secret stores/federated identity where possible.
11. **Real dependency testing** — PostgreSQL semantics are tested against PostgreSQL, not replaced by SQLite for backend integration convenience.
12. **Migrations are release artifacts** — schema evolution is reviewed, rehearsed and executed separately from application startup.
13. **CI is authoritative** — local hooks may accelerate feedback but cannot be the only quality gate.
14. **Security is part of build/release** — dependency review, SAST, secret/supply-chain controls and least privilege activate with real source/manifests rather than as decorative configuration.
15. **No enterprise cosplay** — Kubernetes, microservices, brokers, Bazel-scale build systems, release branches and other heavy mechanisms require evidence of a real need.

## 5. Current branch decision baseline

The branch-level baseline currently selects the following foundation direction, pending final workstream review/closure:

```text
REPOSITORY
polyglot monorepo
apps/api + apps/web + apps/mobile
packages for genuinely shared TypeScript artifacts only
infra for compose/IaC/policy definitions
tooling for repository tooling
tests/system for cross-application black-box tests

BACKEND
capability-first modular monolith
clean domain/application/adapters boundaries inside modules
explicit platform + bootstrap/composition root
no generic CRUD/repository/service-locator kernel

ENVIRONMENTS
LOCAL + shared DEV + UAT + PROD
optional ephemeral PR previews
no environment branches

CI/CD
GitHub Actions primary orchestration
GitHub Environments for deployment control
immutable artifact identity by digest/build/SHA
same artifact promoted UAT -> PROD where technically possible

BACKEND TOOLCHAIN
Python 3.14 line; bootstrap pin 3.14.7
uv + committed uv.lock
Ruff
mypy strict
pytest
SQLAlchemy 2.0 stable line + psycopg 3 + Alembic

JS TOOLCHAIN
Node.js 24 LTS line; bootstrap pin 24.18.0
pnpm 11 stable; bootstrap pin 11.20.0
TypeScript strict
ESLint + Prettier
Turborepo for JS/TS task graph and local cache

LOCAL SERVER-SIDE SEMANTICS
Linux is canonical
Windows backend development uses WSL2/Linux semantics
stateful dependencies use Docker Compose
apps normally run natively in the developer environment for fast feedback

MOBILE
Expo development builds for production-grade development
Expo Go is not the canonical production development environment
Maestro selected for native E2E when mobile E2E activates

INFRASTRUCTURE
remote durable infrastructure must be reproducible as code
exact compute provider and IaC engine remain deferred until first remote-infrastructure implementation because neither is currently selected by accepted architecture
```

## 6. Durable specification set

The detailed branch sources are:

- `docs/development/engineering-foundation-v0.md` — master foundation contract and decision register;
- `docs/development/repository-layout-v0.md` — repository topology, path ownership and generated-artifact rules;
- `docs/development/application-structure-v0.md` — backend/web/mobile modular structure and dependency boundaries;
- `docs/development/environments-and-promotion-v0.md` — LOCAL/DEV/UAT/PROD and promotion contract;
- `docs/development/config-and-secrets-v0.md` — configuration, credentials and secret contract;
- `docs/development/toolchain-and-dx-v0.md` — runtime/toolchain/versioning/local-development contract;
- `docs/development/testing-and-ci-v0.md` — test architecture, CI/CD and supply-chain gates.

## 7. Workstream lifecycle

Engineering Foundation is intentionally compact in discussion but complete in durable documentation.

Closure requires:

```text
repository layout coherent                  PASS
application dependency rules coherent      PASS
environment/promotion model coherent        PASS
config/secrets contract coherent            PASS
toolchain/version policy coherent           PASS
database/migration workflow coherent        PASS
testing/CI model coherent                   PASS
current global docs aligned                 PASS
Domain/Logical/Physical implicit reopen     0
production implementation paths created     0
false direct-validation PASS claims         0
approved PRE-SCOPE delta exact              PASS
remote readback / compare QA                PASS
user acceptance                             REQUIRED
```

## 8. Next boundary after closure

After Engineering Foundation closes and integrates, the next work is real implementation:

```text
repository scaffold
→ backend bootstrap/composition root
→ PostgreSQL local development profile + migration harness
→ concrete Logical-to-PostgreSQL schema implementation
→ persistence/application vertical slices
→ API/client contracts
→ specialist Physical capabilities as their real use-cases arrive
```

This sequence does not create a new standalone “Development Profile v0” phase. Operational decisions are implemented under the Engineering Foundation contract and the capability/release boundary that actually needs them.

## 9. Current continuation state

```text
BRANCH
chore/engineering-foundation-v0

APPROVED PRE-SCOPE
ebc3616956faeabd99d90f5f32458b284be218e4

CURRENT TASK
establish complete Engineering Foundation v0 documentation
then align approved current-truth files

PRODUCTION CODE
NOT AUTHORIZED / NOT STARTED

DIRECT PSV
NOT RUN / unchanged
```
