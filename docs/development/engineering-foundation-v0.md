# Engineering Foundation v0

- Status: **ACTIVE BRANCH BASELINE — PENDING FINAL REVIEW / CLOSURE**
- Workstream: `chore/engineering-foundation-v0`
- Established: 2026-08-19
- Scope: production engineering structure before first production code

## 1. Purpose

This specification defines the engineering system in which DANTE production code will be created, tested, versioned, migrated, deployed and operated.

It sits downstream from the closed Product/Domain/Logical/Physical work and upstream from production implementation.

```text
PRODUCT / DOMAIN / LOGICAL / PHYSICAL
already define WHAT DANTE means and the accepted target architecture

ENGINEERING FOUNDATION
now defines HOW the codebase and delivery system are structured

IMPLEMENTATION
comes next
```

This is not another technology-selection benchmark and not a hidden backend implementation phase.

## 2. Quality model

DANTE adopts a production-grade standard from the first implementation commit, but does not copy large-company complexity that exists only because those companies already have thousands of engineers or hundreds of services.

The foundation optimizes for:

1. semantic fidelity to accepted Domain/Logical authority;
2. explicit dependency direction;
3. reproducible developer and CI environments;
4. safe schema evolution;
5. environment isolation;
6. immutable, traceable releases;
7. high-signal automated validation;
8. least-privilege and secret-safe delivery;
9. observable behavior without shadow personal-data stores;
10. straightforward growth from one modular application to later components only where evidence requires it.

A mechanism is not “enterprise” merely because it is complicated. Complexity must pay for a concrete requirement.

## 3. Non-negotiable inherited boundaries

Engineering implementation must preserve, among others:

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

`WL-H01..WL-H12` remain active.

PostgreSQL remains the single canonical persistence authority. PowerSync/SQLite, Restate, R2/S3, solver state and telemetry remain bounded mechanisms with the ownership defined by PM-11/12.

## 4. Repository strategy

### Decision

DANTE uses a **polyglot monorepo**.

Rationale:

- web, mobile and backend evolve against the same governed product semantics;
- API contract changes can be validated atomically with their clients;
- infrastructure, migrations, generated contracts and documentation remain traceable to one commit;
- the current team does not benefit from distributed repository/version coordination;
- a monorepo does not imply a monolithic runtime.

Repository extraction is allowed later only for a measured boundary such as independent release ownership, security isolation, scale/tooling constraints or genuinely independent lifecycle.

### Top-level ownership

```text
apps/        deployable/runnable applications
packages/    genuinely shared TypeScript packages/artifacts
infra/       environment/infrastructure definitions and local dependency topology
tooling/     repository engineering utilities; never product business logic
tests/       cross-application/system black-box validation only
docs/        durable product/architecture/engineering authority
prototypes/  exploratory/non-production work
.github/     GitHub repository automation and integration controls
```

Detailed tree and dependency rules live in `repository-layout-v0.md`.

## 5. Application architecture

### Backend

DANTE starts as one **capability-first modular monolith**.

A module groups behavior that changes together. A Logical owner is not automatically a Python module, table, microservice or route.

Each backend capability keeps its domain/application meaning separate from technical adapters. FastAPI, SQLAlchemy, provider SDKs and transport DTOs remain at technical boundaries rather than becoming the domain model by identity.

The composition root owns concrete dependency wiring.

Cross-module access uses explicit public contracts/application interfaces; modules do not reach into another module's private persistence or internal implementation.

Generic infrastructure abstractions are not allowed merely to reduce line count. In particular:

```text
NO universal generic Repository[T] as a semantic model
NO BaseService CRUD hierarchy
NO service locator
NO global mutable database session
NO framework-coupled domain entities
NO “shared” dumping-ground package
```

### Web and mobile

Web and mobile are independent clients of the governed backend contract.

They may share:

- generated API client/types;
- design tokens;
- pure platform-neutral utilities proven to be genuinely common.

They do **not** share UI components by default. React DOM and React Native have different platform semantics; a shared UI library is extracted only when actual stable reuse exists.

## 6. API contract ownership

Backend HTTP schemas are transport contracts, not Domain identity.

The authoritative transport description is generated from the backend OpenAPI contract. TypeScript client/types are generated from that contract into a dedicated workspace package.

Policy:

```text
backend contract source
→ deterministic OpenAPI generation
→ deterministic TypeScript client generation
→ generated package consumed by web/mobile
→ CI verifies no generation drift
```

Hand-written duplicate request/response types across Python and TypeScript are forbidden where the generated contract can represent them.

Generated code is explicitly marked and never hand-edited.

Mobile clients cannot be assumed to upgrade at the same instant as the backend. Production backend contract changes must therefore remain compatible with every mobile build still inside the supported-client window. Removal of old behavior requires an explicit retirement boundary, not merely a new server deploy.

## 7. Runtime and dependency policy

### Python

```text
production language line        Python 3.14
initial bootstrap interpreter   Python 3.14.7
package/environment manager     uv
manifest                        pyproject.toml
lockfile                        uv.lock / committed
formatter + linter              Ruff
type checker                    mypy / strict baseline
test runner                     pytest
ORM/data access                 SQLAlchemy 2.0 stable line
PostgreSQL driver               psycopg 3
migrations                      Alembic
```

Patch/minor library versions are locked by `uv.lock`; documentation does not duplicate every package patch number. Runtime/package-manager versions used in CI are explicitly pinned and upgraded by reviewed change.

### TypeScript/JavaScript

```text
runtime line                    Node.js 24 LTS
initial bootstrap runtime       Node.js 24.18.0
package manager                 pnpm 11 stable
initial bootstrap package mgr   pnpm 11.20.0
lockfile                        pnpm-lock.yaml / committed
type checking                   TypeScript strict
lint                            ESLint
format                          Prettier
JS workspace task graph         Turborepo
```

Pre-release toolchain majors are not adopted as the default production baseline merely because they exist.

### Dependency update rule

- manifests express intended dependency constraints;
- lockfiles express the exact resolved build;
- CI uses frozen/locked install modes;
- runtime/toolchain upgrades happen in explicit PRs;
- major framework/runtime upgrades require compatibility and migration review;
- security fixes may be expedited but still produce traceable repository history.

## 8. Local development contract

### Canonical server-side semantics

Linux is the canonical server-side execution environment.

For Windows developers, backend/container work uses WSL2/Linux semantics. This keeps filesystem/shell/runtime behavior close to CI/production and avoids platform-specific async/database differences becoming the accidental canonical path.

Web/mobile tooling may run natively on the host OS when platform tooling benefits from it. Repository contracts must remain usable from macOS, Linux and supported Windows development setups.

### Containers

Docker Compose is used for **stateful local dependencies**, not as a requirement to run every application process during the inner development loop.

Typical rule:

```text
PostgreSQL/extensions/PgBouncer/other activated stateful dependencies
→ containers

FastAPI / Next.js / Expo processes
→ native developer process by default for fast reload/debug
```

A deployable server application is packaged as an OCI image when deployment begins. Images are immutable, run as non-root where practical and are identified by digest.

### No fake canonical database

Backend integration tests and development paths that exercise persistence use PostgreSQL. SQLite is not used as a convenience substitute for canonical PostgreSQL behavior.

The encrypted SQLite selected by the Physical Model belongs only to the bounded mobile/offline architecture.

## 9. Database development and migration contract

SQLAlchemy/Alembic are accepted for the implementation baseline against the already-selected PostgreSQL target.

### Hard rules

1. Application startup does not call `metadata.create_all()` to manage deployed schema.
2. Every durable schema change is represented by an Alembic migration.
3. Alembic autogenerate produces a **candidate**, never an automatically trusted migration.
4. Generated migrations are manually reviewed for data loss, lock behavior, constraints, indexes, defaults and rollback implications.
5. Migrations that have been merged/applied are immutable; corrections use new revisions.
6. Schema migration and reference/demo data seeding are separate concerns.
7. Production replicas do not race each other to migrate on startup.
8. Environment deployment runs a single controlled migration/release job before dependent application rollout where required.
9. The empty database -> current head path is continuously tested once migrations exist.
10. UAT rehearses release migrations against representative synthetic data before PROD.
11. Production rollback does not assume that every destructive schema operation can be safely reversed with `alembic downgrade`.
12. Risky changes use expand/migrate/contract sequencing so old and new application versions can coexist during rollout where necessary.

Data migrations that materially transform canonical semantics require explicit implementation/test review; they are not hidden in startup hooks.

## 10. Transaction and persistence discipline

Database sessions/transactions are request/use-case scoped, never global shared state.

Async database access may be used at the application/adapters boundary, while Domain logic remains synchronous/pure unless a real domain computation requires otherwise.

`AsyncSession` is not shared across concurrent tasks. Implicit lazy I/O is avoided; data required by a use case is loaded explicitly.

Consequential writes preserve accepted expected-state, idempotency and multi-owner semantics. Transaction scope is selected by the use case, not by ORM convenience.

Where a Class-A async effect uses the selected PostgreSQL outbox pattern, the outbox record and canonical state transition belong to the same transaction where the accepted semantics require atomicity.

## 11. Environment model

DANTE defines four lifecycle contexts:

```text
LOCAL
individual developer environment; not a remote deployment stage

DEV
shared integration environment for accepted main builds and synthetic/test data

UAT
production-like release-candidate verification, migration rehearsal and acceptance

PROD
real released service and real user data
```

Optional ephemeral preview environments may exist per PR/feature when economically and technically useful. They never become another source of canonical project truth.

Each remote environment has independent state and credentials. No DEV/UAT application receives PROD database credentials by design.

Detailed promotion semantics live in `environments-and-promotion-v0.md`.

## 12. Artifact and release contract

Server/web deployables use an immutable artifact identity containing at minimum:

- source Git commit SHA;
- build identifier;
- artifact/image digest where available;
- application version/release tag when release versioning is active.

The preferred lifecycle is:

```text
commit accepted on main
→ CI builds/tests artifact
→ deploy to DEV
→ select exact artifact as release candidate
→ promote exact artifact to UAT
→ acceptance/migration/E2E gates
→ promote exact artifact to PROD
```

Rebuilding “the same source” separately for PROD is avoided where the platform permits build-once promotion.

Mobile is a deliberate exception: separate signed application identities/configuration may require DEV/UAT/PROD builds. Those builds must remain traceable to the same source commit, locked dependencies and explicit build profile; they are not treated as identical binary artifacts when they are not.

## 13. Configuration and secrets

Configuration is typed, validated on process start and then treated as immutable runtime state.

Backend uses `pydantic-settings`; TypeScript clients use a typed validation boundary appropriate to the selected client stack.

Rules:

```text
client-visible value = PUBLIC by definition
secret = never shipped to browser/mobile bundle
production secret = never committed
real credentials = never placed in .env.example
missing required production config = startup failure
invalid environment combination = startup failure
```

OIDC/federated identity is preferred for CI-to-cloud access where supported. Long-lived cloud access keys are a fallback, not the default.

Full policy lives in `config-and-secrets-v0.md`.

## 14. Testing model

DANTE uses risk-layered testing rather than one undifferentiated test suite.

Required categories as implementation arrives:

```text
unit / pure semantic tests
property/invariant tests where state space matters
architecture dependency tests
PostgreSQL integration tests
migration tests
adapter/provider contract tests
OpenAPI/client-generation drift tests
web component/integration tests
mobile component/integration tests
system/E2E tests
security/static/dependency analysis
performance/recovery/specialist PSV tests at their applicable boundary
```

Coverage percentage is a signal, not semantic proof. A global percentage cannot substitute for explicit invariant, conflict, migration, recovery or non-interference tests. Exact numerical coverage floors may be introduced after the first real implementation establishes meaningful denominators; critical semantic paths are required to have direct tests regardless of aggregate coverage.

## 15. CI/CD model

GitHub Actions is the primary repository CI/CD orchestrator.

PR CI begins with real checks and grows with the codebase. No check becomes a required-main status merely because its future name is documented.

Initial check classes will include, when corresponding code/manifests exist:

- repository/config validation;
- backend format/lint/type/unit;
- backend PostgreSQL integration/migration;
- web lint/type/test/build;
- mobile lint/type/test/build-validation;
- API contract/client drift;
- dependency review;
- CodeQL/static analysis;
- container/IaC checks when those artifacts exist.

PR jobs run with least-privilege token permissions and no production deployment secrets.

Deployment jobs use GitHub Environments to scope approval, environment rules and environment-specific credentials. Deployment concurrency is serialized per environment where concurrent deploys would be unsafe.

Only after a real check exists, emits a stable context and demonstrates that failure should block integration may it be added to the protected-main required-check ruleset.

## 16. Supply-chain baseline

- all package-manager lockfiles are committed;
- CI uses locked/frozen installs;
- third-party GitHub Actions are pinned to immutable commit SHAs where practical;
- dependency review is part of PR security once manifests exist;
- Dependabot/security update automation is enabled for supported active ecosystems after manifests exist;
- CodeQL activates when production source exists;
- secret scanning/push protection remain repository security controls where available;
- build provenance/artifact attestation is introduced for release artifacts once actual deployable artifacts exist;
- generated files state their generator and are regenerated deterministically;
- no downloaded binary or generated artifact is silently committed without ownership/provenance policy.

## 17. Infrastructure-as-code posture

Remote durable infrastructure must be reproducible from versioned infrastructure definitions. Manual console changes cannot become the only representation of production state.

The repository reserves `infra/iac/` for that contract.

The exact compute/runtime provider and exact IaC engine are **not selected by current accepted architecture**, so Engineering Foundation does not invent them merely to make the folder non-empty. The first remote infrastructure implementation must select/pin the IaC engine and provider under an explicit implementation decision while preserving this contract.

This is a deliberate defer, not missing architecture.

## 18. Specialist target activation

Selected Physical components enter implementation when their real capability arrives; they are not re-evaluated from scratch in a separate profile phase.

Examples:

```text
PostGIS
→ when accepted geospatial mappings/queries are implemented

pgvector / FTS
→ when retrieval/search vertical slices arrive

PowerSync + encrypted SQLite
→ when real offline/multi-device implementation begins

R2
→ when real ContentArtifact bytes are implemented

OR-Tools
→ when solver-backed planning capability begins

Restate
→ fixed dormant trigger: first real Class-B durable workflow

pgBackRest + AWS S3
→ fixed dormant trigger: recovery/production boundary or real rehearsal
```

Dormancy never cancels the applicable PSV obligations.

## 19. Deferred decisions

Only decisions that genuinely depend on absent implementation/provider facts are deferred:

```text
compute hosting/provider
exact IaC engine
artifact/container registry provider
exact remote DEV/UAT/PROD sizing
domain-capability module list
exact API route/version surface
exact AuthN/AuthZ mechanism
exact numeric coverage floors
specialist service activation beyond already-fixed triggers
```

A defer is not permission to improvise later. It opens at the implementation boundary that supplies the missing facts.

## 20. Primary-source verification baseline

Version-sensitive engineering choices were checked on 2026-08-19 against current primary documentation, including:

- Python 3.14.7 release: `https://www.python.org/downloads/release/python-3147/`
- uv project/workspace/lock documentation: `https://docs.astral.sh/uv/`
- Ruff documentation: `https://docs.astral.sh/ruff/`
- Node.js release/LTS policy: `https://nodejs.org/en/about/previous-releases`
- pnpm releases/workspace documentation: `https://pnpm.io/workspaces`
- FastAPI larger-application structure: `https://fastapi.tiangolo.com/tutorial/bigger-applications/`
- SQLAlchemy 2.0 async/psycopg documentation: `https://docs.sqlalchemy.org/en/20/`
- Alembic autogeneration guidance: `https://alembic.sqlalchemy.org/en/latest/autogenerate.html`
- Psycopg async documentation: `https://www.psycopg.org/psycopg3/docs/advanced/async.html`
- GitHub Actions deployment environments/OIDC/supply-chain documentation: `https://docs.github.com/en/actions` and `https://docs.github.com/en/code-security`
- Expo monorepo/development-build documentation: `https://docs.expo.dev/guides/monorepos/` and `https://docs.expo.dev/develop/development-builds/introduction/`

These URLs are supporting engineering evidence, not a replacement for repository authority. Exact package/library versions are locked by implementation manifests when scaffolded and must be re-verified at upgrade time.

## 21. Closure condition

Engineering Foundation v0 can close only after the complete specification set is internally coherent, approved current-truth docs no longer point to the superseded standalone Development Profile sequence, exact Git scope QA is clean, and the user accepts the baseline.

Until then:

```text
ENGINEERING FOUNDATION
ACTIVE / NOT CLOSED

BACKEND PRODUCTION CODE
NOT STARTED

DIRECT PSV
NOT RUN
```
