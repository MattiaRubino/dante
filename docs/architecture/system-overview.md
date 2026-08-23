# DANTE System Overview

- Status: **CURRENT ARCHITECTURE OVERVIEW**

## 1. Product and authority

DANTE is a personal operating system whose canonical truth represents real life over time while preserving authority, provenance, uncertainty and distinctions between intention, execution and outcome.

Compass: **Understand life. Shape what comes next.**

Implementation consumes the closed Product, Domain, Logical and Physical models, the closed Engineering Foundation and the closed Frontend Engineering Foundation. Backend scaffold CP1-CP5 is integrated in protected `main`; frontend materialization FM-00..FM-07 is closed/directly validated and is being integrated through READY PR #28.

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

```text
DANTE repository
│
├── apps/backend
│   └── capability-first modular monolith
│
├── apps/web
│   └── React DOM/Vite client
│
├── apps/mobile
│   └── Expo/React Native client
│
├── packages
│   └── genuine multi-consumer semantics/artifacts only
│
├── infra
├── tooling
├── tests/system
├── docs
├── prototypes
└── .github
```

Paths are created only when real content exists. Production implementation remains in this repository.

## 3. Backend architecture and current evidence

Target internal shape remains capability-first:

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
```

FastAPI is an inbound adapter/process host. SQLAlchemy/provider/runtime objects stay outside Domain identity. Capability boundaries are behavior/cohesion based, not one owner/table/route per module.

The production backend scaffold is **CLOSED / DIRECT QA PASS / integrated via PR #24**. Direct evidence includes Python/uv bootstrap, Ruff, mypy strict, 50/50 full backend pytest, PostgreSQL 18.4 acceptance, migrations/privileges, package build, real Uvicorn startup and live/ready health endpoints.

Concrete Logical -> PostgreSQL business mapping remains NOT STARTED.

## 4. Frontend architecture and current evidence

Web and Mobile are sibling governed clients with platform-specific renderers and selective shared semantics.

Conceptual ownership:

```text
Web
bootstrap
routes
features
ui
platform
config

Mobile
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
- public-API-only cross-boundary use;
- feature dependency cycles forbidden;
- Web/Mobile do not import each other's private implementation;
- UI/platform layers do not depend upward on feature internals;
- no generic shared/common/utils dumping grounds;
- production never imports prototypes;
- architecture rules are executable where materialized.

Current dependency graph proof:

```text
36 modules / 45 dependencies / 0 violations
```

Shared packages currently materialized:

```text
@dante/design-tokens
@dante/i18n
@dante/time
```

Frontend materialization is **CLOSED / PASS** at FM-00..FM-07 stated scopes. It directly proved the Web build/E2E path, Android emulator runtime, Android Hermes bundle smoke, shared packages, strict TS, generated drift, unit tests, architecture enforcement, fresh-clone materialization and hosted CI.

## 5. Qualified frontend implementation baseline

```text
Node                      24.19.0
pnpm                      11.22.0
TypeScript                6.0.3 strict
Turborepo                 2.10.11

Web
React / React DOM         19.2.8 / 19.2.8
Vite                      8.2.1
TanStack Router           1.170.31
Playwright                1.62.1

Mobile
Expo SDK                  57.x / clean resolution 57.0.15
React Native              0.86.2
React                     19.2.3
Expo Router               57.x / clean resolution 57.0.15
Gesture Handler           2.32.0
Reanimated                4.5.1

Shared time implementation
temporal-polyfill         1.0.4

Web E2E authority
apps/web/e2e/
```

The Foundation remains architecture authority; later direct materialization evidence qualifies version-specific implementation details. `selected != installed != configured != directly validated` remains mandatory.

## 6. Canonical persistence and client data authority

```text
PostgreSQL 18.4
SOLE CANONICAL PERSISTENCE / MATERIAL-HISTORY AUTHORITY
```

Frontend Data Authority Matrix:

```text
canonical accepted state/effect   backend + PostgreSQL
synced local projection           PowerSync/SQLite when activated
offline pending mutation          local staging only
offline acceptance                backend governance/conflict checks
remote request state              TanStack Query + typed API when activated
online governed command           FastAPI/backend
form draft                        TanStack Form when activated
component transient               React
cross-tree transient              Zustand only when justified
```

An offline operation crosses staging -> upload -> backend accept/reject -> reconciliation. Local arrival/staging does not define semantic truth.

## 7. Frontend data/API boundary

Feature UI consumes feature data/model boundaries rather than architecture-level coupling to HTTP, PowerSync, query cache or storage.

Real FastAPI OpenAPI eventually feeds Orval-generated React-free/auth-storage-agnostic transport code. `@dante/api-client` does not exist until there is real OpenAPI/product transport to generate.

TanStack Query/Form, Orval and PowerSync are selected capabilities, not current product implementation.

## 8. Offline/sync

Selected Physical target remains PowerSync + encrypted SQLite bounded local state.

Mobile may activate PowerSync/OP-SQLite/SQLCipher at the first real offline operation. Web starts online-first; PowerSync Web and browser PWA/service-worker behavior remain dormant.

Local client databases must be identity-scoped; cross-account local-data leakage is forbidden.

## 9. UI/shared semantics

Web owns a DANTE Web UI layer. Mobile owns a separate DANTE Native UI layer. Shared semantic tokens may intentionally render differently per platform.

`@dante/i18n` is framework-free; app bootstrap owns React integration.

`@dante/time` owns Temporal semantics through the directly qualified `temporal-polyfill 1.0.4` implementation.

A full reusable design system, Storybook, visual regression and automated a11y are activation-triggered work, not placeholder baseline infrastructure.

## 10. Configuration/secrets

Backend uses typed pydantic-settings fail-fast configuration.

Frontend shipped configuration is public client configuration, never a secret. Versioned/Zod-validated Web runtime config activates at the first shared DEV/Web deployment boundary.

Remote secret posture remains workload identity -> provider secret manager -> least privilege -> rotation/revocation/audit, with GitHub OIDC preferred where supported.

## 11. Environments

Exactly:

```text
LOCAL -> DEV -> UAT -> PROD
```

They are runtime contexts, not Git branches.

## 12. Async/durable/object/recovery/solver

Class A async: PostgreSQL transactional outbox + bounded worker when required.

Class B: Restate selected/dormant until a real Class-B workflow.

ContentArtifact raw bytes: private R2 when activated; PostgreSQL owns authority/metadata.

Recovery: pgBackRest + WAL/PITR + S3 accepted target at recovery boundary.

Solver: OR-Tools CP-SAT; `UNKNOWN != INFEASIBLE`; solver output remains candidate until governed acceptance.

## 13. Observability

Backend target: OpenTelemetry + Grafana Alloy + Grafana Cloud EU + pg_stat_statements.

Frontend target: Sentry behind bounded app/platform adapters when shared deployment/release makes it useful.

Observability is privacy-minimized operational telemetry, never canonical history or a shadow personal-data store.

## 14. Testing / CI / supply chain

GitHub Actions is repository-wide primary CI/CD authority.

The branch-local protected-main ruleset definition contains:

```text
Backend CI Gate
Dependency Review
Frontend CI Gate
```

`Frontend CI Gate` has directly proved real green, controlled deliberate red, mandatory failure propagation, exact workflow restoration and recovery green. The repository owner confirmed applying its required-check promotion. The available connector does not expose direct ruleset readback, so the administrative setting is classified **OWNER-CONFIRMED APPLIED / DIRECT API READBACK UNAVAILABLE** rather than independently API-verified.

The directly observed pre-reconciliation PR #28 head `bdd6e08cbca4c19989502235855d52a620d29fb5` passed:

```text
Backend Quality
Backend PostgreSQL
Backend CI Gate
Dependency Review
Quality
Web E2E
Mobile Bundle
Frontend CI Gate
```

Any later documentation-only head must independently satisfy the applicable hosted-CI/currentness/mergeability/thread-clean gate before merge authorization.

Dependency Review remains fail-closed at moderate severity. Three exact transitive tooling GHSA exceptions are temporarily accepted until review/removal conditions are met; details live in the integration handoff.

## 15. Developer posture

Canonical development semantics remain Linux/WSL for the authoritative source tree and JS/backend tooling. Windows remains the UI/browser/Android-emulator/JetBrains host where desired.

No divergent Windows/WSL clones and no cross-OS shared `node_modules`.

## 16. Direct evidence boundary

```text
BACKEND SCAFFOLD             DIRECT QA PASS / INTEGRATED
FRONTEND MATERIALIZATION     DIRECT QA PASS AT FM SCOPES
WEB CHROMIUM E2E             PASS
ANDROID EMULATOR RUNTIME     PASS
ANDROID HERMES BUNDLE        PASS
FRONTEND CI GATE CALIBRATION PASS green/red/recovery
PR #28 PRE-RECONCILIATION    GREEN / CURRENT / MERGEABLE / THREAD-CLEAN at bdd6e08...

CONCRETE BUSINESS SCHEMA     NOT STARTED
POWERSYNC PRODUCT FLOW       NOT RUN
ORVAL PRODUCT CLIENT         NOT MATERIALIZED
IOS DIRECT RELEASE PATH      NOT RUN
CODEQL                       NOT ACTIVE
PRODUCTION DEPLOYMENT        NOT STARTED
```

## 17. Current next step

```text
PR #28 exact current head
-> hosted CI green
-> current with main
-> mergeable / review-thread clean
-> separate protected-main merge authorization
```

Backend Concrete Logical -> PostgreSQL remains a separate bounded next workstream. Future product capabilities activate according to the trigger register in `docs/workstreams/frontend-materialization-integration.md`.
