# DANTE System Overview

- Status: **CURRENT ARCHITECTURE OVERVIEW**

## 1. Product and authority

DANTE is a personal operating system whose canonical truth represents real life over time while preserving authority, provenance, uncertainty and distinctions between intention, execution and outcome.

Compass: **Understand life. Shape what comes next.**

Implementation consumes closed Product/Domain/Logical/Physical models, closed Engineering Foundation and the closed branch-local Frontend Foundation pending protected-main integration.

Core invariants include:

```text
Person != Account != Principal != Actor
Authority != AuthZ decision
Consent != Authority
Visibility != Authority
provider state != canonical DANTE state
derived projection != canonical truth
absence/unknown != false
MaterialStateRef != ETag/MVCC/provider revision
idempotency != semantic identity
AI/solver output != accepted canonical effect
client local state != canonical accepted effect
```

WL-H01..WL-H12 remain active.

## 2. Repository/application topology

One product monorepo with accepted ownership:

```text
DANTE repository
│
├── apps/backend
│   └── capability-first modular monolith
│
├── apps/web
│   └── React DOM/Vite client; feature-first
│
├── apps/mobile
│   └── Expo/React Native client; feature-first
│
├── packages
│   └── only genuine multi-consumer contracts/artifacts
│
├── infra
│   └── LOCAL/future remote infrastructure definitions
│
├── tooling
├── tests/system
├── docs
├── prototypes
└── .github
```

Paths are materialized only when real content exists. Production implementation continues in the existing repository; a new production repo is not planned.

## 3. Backend architecture

Target internal shape:

```text
apps/backend/src/dante
├── bootstrap
├── kernel
├── platform
└── modules/<capability>
    ├── domain
    ├── application
    ├── ports
    └── adapters
        ├── inbound/http
        └── outbound/persistence|integrations
```

FastAPI is an inbound adapter/process host. SQLAlchemy/provider/runtime objects stay outside Domain identity. Capability boundaries are behavior/cohesion based, not one owner/table/route per module.

## 4. Frontend architecture

Web and Mobile are sibling governed clients with platform-specific renderers and selective shared semantics.

Web conceptual internals:

```text
bootstrap
routes
features
ui
platform
config
```

Mobile conceptual internals:

```text
app/          Expo Router adapters
src/bootstrap
src/features
src/ui
src/platform
src/config
```

Structural rules:

- feature-first;
- routes/navigation are thin adapters;
- public-API-only cross-boundary imports;
- feature dependency cycles forbidden;
- Web/Mobile do not import each other's private implementation;
- UI/platform layers do not depend upward on feature internals;
- no generic shared/common/utils dumping grounds;
- production never imports prototypes;
- architecture rules become executable checks when materialized.

Shared packages are extracted only for real multi-consumer semantics. Initial real candidates are design tokens, i18n and time. Shared client cores remain framework-free by default and never own backend/domain authority.

## 5. Canonical persistence and client data authority

```text
PostgreSQL 18.4
SOLE CANONICAL PERSISTENCE / MATERIAL-HISTORY AUTHORITY
```

Selected DB capabilities remain PostGIS, pgvector, native FTS, pg_trgm, unaccent, pg_stat_statements and PgBouncer target posture.

Frontend Data Authority Matrix:

```text
canonical accepted state/effect   backend + PostgreSQL
synced local projection           PowerSync/SQLite noncanonical
offline pending mutation          local staging only
offline acceptance                backend governance/conflict checks
remote request state              TanStack Query + typed API
online governed command           FastAPI/backend
form draft                        TanStack Form
component transient               React
cross-tree transient              Zustand only when justified
```

An offline operation crosses staging → upload → backend accept/reject → reconciliation. Local arrival/staging does not define semantic truth.

## 6. Frontend data/API boundary

Feature UI consumes feature data/model boundaries rather than direct architecture-level coupling to HTTP, PowerSync, query cache or storage implementation.

Real FastAPI OpenAPI eventually feeds Orval-generated React-free/auth-storage-agnostic transport code. Generated code is derivative, deterministic and drift checked where committed.

## 7. Offline/sync

Selected Physical target remains PowerSync + encrypted SQLite bounded local state.

Mobile activates that path when materialized, with PowerSync runtime initially owned by the Mobile platform adapter.

Web starts online-first; PowerSync Web is available/dormant.

Browser PWA/service-worker offline behavior is dormant/not baseline.

Local client databases are identity scoped; cross-account local-data leakage is forbidden.

## 8. UI/shared semantics

Web owns a DANTE UI layer over selected Web primitives/styling. Mobile owns a separate DANTE Native UI layer. Shared semantic design tokens may intentionally render differently per platform.

`@dante/i18n` is framework-free; app bootstrap wires React integration/platform detection/persistence.

`@dante/time` owns Temporal-based semantic time handling.

## 9. Configuration/secrets

Backend uses typed pydantic-settings fail-fast configuration.

Frontend public config is typed/validated and contains no secrets.

Web runtime config is versioned and Zod validated so one SPA artifact can be promoted across environments where the delivery platform permits. An app-coupled Cloudflare Worker may serve bounded bootstrap config but is not a DANTE BFF/business backend.

Remote secret posture remains workload identity → provider secret manager → least privilege → rotation/revocation/audit, with GitHub OIDC preferred where supported.

## 10. Environments

Exactly:

```text
LOCAL → DEV → UAT → PROD
```

They are runtime contexts, not Git branches. Frontend/mobile tool profile/channel names map to the same four contexts.

## 11. Async/durable/object/recovery/solver

Class A async: PostgreSQL transactional outbox + bounded worker.

Class B: Restate selected/dormant until a real Class-B workflow.

ContentArtifact raw bytes: private Cloudflare R2 when activated; PostgreSQL owns authority/metadata.

Recovery: pgBackRest + WAL/PITR + AWS S3 accepted target at recovery boundary.

Solver: OR-Tools CP-SAT; `UNKNOWN != INFEASIBLE`; solver output remains candidate until governed acceptance.

## 12. Observability

Backend: OpenTelemetry + Grafana Alloy + Grafana Cloud EU + pg_stat_statements target.

Frontend: Sentry behind bounded app/platform observability adapters when activated.

All observability is privacy-minimized operational telemetry, never canonical history or a shadow personal-data store.

## 13. Testing/CI/release

GitHub Actions is repository-wide primary CI/CD authority.

Backend validation remains risk-layered with real PostgreSQL evidence.

Frontend validation progressively covers lint/dependency/cycle boundaries, strict TS, unit/component, generated drift, Web E2E, Mobile tests and release/device validation for activated targets.

Status checks become required only after real stable emitted contexts are observed.

Android and iOS are supported architectural targets; platform-specific signed/device/store gates apply only when each platform is activated for release.

## 14. Developer posture

Canonical backend semantics remain Linux. Primary Windows posture is one authoritative WSL-backed repository checkout with JetBrains/PyCharm UI on Windows as desired.

Frontend keeps one authoritative checkout; WSL↔Windows Metro/ADB specifics are a direct-validation tooling adapter. Divergent Windows/WSL source clones are forbidden.

## 15. Direct evidence boundary

Architecture/design closure is not implementation proof.

```text
BACKEND SCAFFOLD          NOT STARTED
FRONTEND SCAFFOLD         NOT STARTED
DATABASE DEPLOYMENT       NOT STARTED
CONCRETE SCHEMA           NOT STARTED
DIRECT HG                 NOT RUN
FRONTEND DIRECT TEST      NOT RUN
PSV                       NOT RUN
RESTORE REHEARSAL         NOT RUN
```

## 16. Current next step

```text
prepare protected-main integration for the closed Frontend Foundation
↓
PR/merge only with explicit authorization and expected-head safety
↓
post-merge main readback
↓
after integration open new production frontend materialization/direct-validation scope
```

Backend production scaffold remains a separate not-started scope.
