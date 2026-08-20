# DANTE System Overview

- Status: **CURRENT ARCHITECTURE OVERVIEW**

## 1. Product and authority

DANTE is a personal operating system whose canonical truth represents real life over time while preserving authority, provenance, uncertainty and distinctions between intention, execution and outcome.

Compass: **Understand life. Shape what comes next.**

Implementation consumes closed Product/Domain/Logical/Physical models, closed Engineering Foundation and the closed branch-local Frontend Foundation pending integration.

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
├── apps/backend     capability-first modular monolith
├── apps/web         React DOM/Vite client; feature-first
├── apps/mobile      Expo/React Native client; feature-first
├── packages         genuine multi-consumer contracts/artifacts only
├── infra            LOCAL/future remote infrastructure definitions
├── tooling
├── tests/system
├── docs
├── prototypes
└── .github
```

Paths are materialized only when real content exists. Production continues in the existing repository.

## 3. Backend architecture

`apps/backend/src/dante` uses bootstrap/kernel/platform/capability modules with Domain/application/ports/adapters separation. FastAPI is an inbound adapter/process host; SQLAlchemy/provider/runtime objects stay outside Domain identity; capability boundaries are behavior/cohesion based.

## 4. Frontend architecture

Web and Mobile are sibling governed clients with platform-specific renderers and selective shared semantics.

Web: bootstrap, routes, features, ui, platform, config.

Mobile: Expo `app/` route adapters plus `src/bootstrap`, `features`, `ui`, `platform`, `config`.

Rules:

- feature-first;
- routes/navigation thin adapters;
- public-API-only imports;
- feature dependency cycles forbidden;
- no Web↔Mobile private implementation imports;
- UI/platform layers do not depend upward on feature internals;
- no generic shared/common/utils dumping grounds;
- production never imports prototypes;
- architecture rules become executable checks when materialized.

Shared packages appear only for real multi-consumer semantics. Shared client cores are framework-free by default and never own backend/domain authority.

## 5. Canonical persistence and client data authority

PostgreSQL 18.4 is sole canonical persistence/material-history authority.

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

Offline operation crosses staging → upload → backend accept/reject → reconciliation. Local arrival/staging never defines semantic truth.

## 6. Frontend data/API boundary

Feature UI consumes feature data/model boundaries rather than direct architecture-level coupling to HTTP, PowerSync, query cache or storage internals.

Real FastAPI OpenAPI feeds Orval-generated React-free/auth-storage-agnostic transport code when it exists. Generated code is derivative/deterministic/drift checked where committed.

## 7. Offline/sync

Mobile activates PowerSync + encrypted SQLite when materialized, initially app-owned by the Mobile platform adapter.

Web starts online-first; PowerSync Web is available/dormant. Browser PWA/service-worker offline behavior is dormant/not baseline.

Local client DBs are identity scoped; cross-account local-data leakage is forbidden.

## 8. UI/shared semantics

Web owns DANTE Web UI; Mobile owns separate DANTE Native UI. Shared semantic tokens may render differently per platform.

`@dante/i18n` is framework-free; app bootstrap wires React integration/detection/persistence. `@dante/time` owns Temporal-based semantic time handling.

## 9. Configuration/secrets

Backend uses typed pydantic-settings. Frontend public config is typed/validated and contains no secrets.

Web runtime config is versioned/Zod validated so one SPA artifact can be promoted where delivery permits. An app-coupled Cloudflare Worker may serve bounded bootstrap config but is not a DANTE BFF/business backend.

Remote secret posture remains workload identity → provider secret manager → least privilege → rotation/revocation/audit.

## 10. Environments

Exactly `LOCAL → DEV → UAT → PROD`; runtime contexts, not Git branches. Frontend/mobile provider profiles map to the same contexts.

## 11. Async/durable/object/recovery/solver

Class A async remains PostgreSQL transactional outbox + bounded worker. Restate is selected/dormant for Class B. ContentArtifact bytes use private R2 when activated with PostgreSQL authority. Recovery and solver target postures remain unchanged.

## 12. Observability

Backend: OpenTelemetry + Grafana Alloy + Grafana Cloud EU + pg_stat_statements target.

Frontend: Sentry behind bounded app/platform adapters when activated.

Telemetry remains privacy-minimized and noncanonical.

## 13. Testing/CI/release

GitHub Actions is repository-wide CI/CD authority.

Frontend validation progressively covers lint/dependency/cycle boundaries, strict TS, unit/component, generated drift, Web E2E, Mobile tests and release/device validation for activated targets.

Status checks become required only after real stable emitted contexts are observed.

Android/iOS are supported architectural targets; platform-specific release gates apply when activated.

## 14. Developer posture

Canonical backend semantics remain Linux. Primary Windows posture is one authoritative WSL-backed checkout. Frontend shares the checkout; WSL↔Windows Metro/ADB is a direct-validation tooling adapter. Divergent source clones are forbidden.

## 15. Direct evidence boundary

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
PR/merge only with explicit authorization
↓
after integration open new production frontend materialization/direct-validation scope
```

Backend production scaffold remains a separate not-started scope.
