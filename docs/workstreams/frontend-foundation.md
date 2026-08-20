# Workstream — Frontend Engineering Foundation

- Status: **ACTIVE — PASSO 1 DESIGN COMPLETE / PASSO 2 DESIGN COMPLETE / PASSO 3 NEXT**
- Branch: `feature/frontend-foundation`
- Base/PRE-SCOPE at workstream opening: `7a1600c2167f68c9281d3ed77b32a3d954fbd061`
- Passo-1 documentation checkpoint: `dd23b86ba330f6296806297ef5c68acebbee65e6`
- PR: **NONE**
- Product: **DANTE**
- Domain Model: **CLOSED / CONSUMED / NOT REOPENED**
- Logical Model: **CLOSED / CONSUMED / WL-H01..WL-H12 ACTIVE**
- Physical target: **CLOSED / SELECTED / ACCEPTED / CONSUMED**
- Engineering Foundation v0: **CLOSED / ACCEPTED / CONSUMED**
- Production frontend code: **NOT STARTED**
- Dependencies installed/configured: **NO**
- Direct frontend selected-stack validation: **NOT STARTED**

## 1. Purpose

Define the professional production frontend engineering foundation for DANTE with the same evidence/status discipline as the backend, while avoiding artificial phase proliferation.

The workstream has exactly three substantial passes:

```text
PASSO 1
technology selection

PASSO 2
frontend application/package architecture
ownership / dependency direction / dev-test-CI model

PASSO 3
whole-foundation clean review
closure / PR / protected-main integration
```

Only after closure/integration may the production frontend scaffold/materialization begin under a new exact write scope.

## 2. Scope boundary

This workstream decides:

- frontend technologies;
- Web/Mobile engineering architecture;
- shared-package and dependency boundaries;
- state/data/API/sync ownership;
- configuration and environment ownership;
- test/quality/observability/release engineering;
- local developer workflow and CI integration.

It does **not** implement product surfaces, mechanically convert standalone HTML prototypes, change Domain/Logical/Physical semantics, create placeholder packages/directories or manufacture direct validation evidence.

Existing prototypes are UX/visual/interaction evidence only.

## 3. Current durable sources

Read at minimum:

1. `../development/operating-rules.md`;
2. `../development/documentation-and-handoff.md`;
3. `engineering-foundation.md`;
4. `../physical-model/pm-12-accepted-physical-model-v1.md`;
5. `../physical-model/recommendation/post-selection-validation-register-v1.md`;
6. `../architecture/frontend-engineering-foundation.md` — Passo 1;
7. `../architecture/frontend-engineering-foundation-part-2.md` — Passo 2;
8. `../decisions/ADR-008-frontend-engineering-stack.md`;
9. `../decisions/ADR-009-frontend-architecture-boundaries.md`;
10. current Product/Domain/Logical authority as needed.

`main` remains the only integrated source truth. This handoff is branch authority only for newer unmerged Frontend Foundation work.

## 4. Passo 1 — completed in design

Technology selection is design-complete.

Core stack:

```text
Node 24 LTS
TypeScript 6.0.x strict
pnpm 11
Turborepo 2.x

Web
React 19.2
React DOM
Vite 8
TanStack Router

Mobile
React Native 0.86
Expo SDK 57
Expo Router

Data/state
PowerSync + encrypted SQLite
@powersync/react
TanStack Query 5
Zustand specialist/dormant
TanStack Form
Zod 4

API
FastAPI OpenAPI → Orval 8
```

Complete UI/testing/release selections are in the Passo-1 specification.

## 5. Passo 2 — completed in design

The definitive structural direction is now recorded in `frontend-engineering-foundation-part-2.md` and ADR-009.

### 5.1 Repository/application architecture

- one product monorepo;
- sibling `apps/backend`, `apps/web`, `apps/mobile` deployable boundaries;
- no root `infra/` is invented by this Frontend Foundation;
- Web delivery code may be co-located with Web when tool-coupled but remains delivery infrastructure, never business/backend authority;
- no production imports from `prototypes/`.

### 5.2 Feature architecture

- feature-first Web and Mobile;
- route/navigation files are thin adapters;
- `bootstrap` is composition only;
- platform capabilities live under app-local `platform/`;
- DANTE platform UI systems live under app-local `ui/`;
- no generic `common/shared/utils/services/hooks/misc` dumping grounds.

### 5.3 Dependency/public API rules

```text
packages              X→ apps
web                   X→ mobile
mobile                X→ web
ui                    X→ features
platform              X→ features
feature internals     X→ other feature internals
prototypes            X→ production
```

Bootstrap and routers may consume other layers/features only through public APIs. Deep/private cross-boundary imports remain forbidden even from privileged composition layers.

Materialization must enforce boundaries with exports + ESLint/boundary rules + workspace isolation/architecture checks.

### 5.4 Shared packages

Initial real cross-platform package candidates:

```text
@dante/design-tokens
@dante/i18n
@dante/time
```

`@dante/api-client` is created only when real FastAPI OpenAPI exists.

Shared feature packages require real Web+Mobile consumers rather than speculative reuse.

Shared client cores are framework-free by default and may never own canonical Domain invariants, AuthZ/Authority decisions, conflict resolution, persistence semantics, accepted-effect authority or canonical material history.

### 5.5 Workspace posture

- internal packages private/workspace-only;
- `workspace:*` internal dependencies;
- package `exports` controls public surfaces;
- source-first TS packages by default;
- workspace cycles forbidden;
- pnpm isolated layout = **PREFERRED BASELINE / DIRECT VALIDATION REQUIRED**;
- `nodeLinker: hoisted` = evidence-driven native compatibility fallback, not architecture failure.

### 5.6 Data Authority Matrix

Every persisted/read/write path must declare authority before implementation.

```text
canonical accepted effect      backend/PostgreSQL
synced local projection        PowerSync/SQLite noncanonical
offline pending mutation       local staging only
offline acceptance             backend governance/conflict checks
remote request state           TanStack Query + typed API
online governed command        FastAPI/backend
route state                    router
form draft                     TanStack Form
component transient            React
cross-tree transient           Zustand only when justified
```

An offline operation crosses local staging → upload → backend acceptance/rejection → reconciliation. Local staging never becomes canonical authority.

### 5.7 Data firewall

Feature UI does not use direct HTTP/PowerSync/query-cache/storage coupling as its architecture. Feature `data/` boundaries select the correct adapter/path. No universal frontend `Repository<T>` is introduced.

### 5.8 Offline posture

Mobile PowerSync lifecycle initially belongs to `apps/mobile/src/platform/sync/` when materialized.

Web is **online-first**. PowerSync Web remains available/dormant.

Browser PWA/service worker is **DORMANT / NOT BASELINE** and requires an explicit requirement/design before activation.

### 5.9 Identity/session

Local data is identity-scoped; cross-account local-data leakage is forbidden.

Session adapters are app/platform-owned. Frontend Foundation does not invent JWT/cookie/refresh-token contracts before backend security design.

### 5.10 UI/shared semantics

- separate DANTE Web and Native UI implementations;
- shared semantic tokens, platform-specific representations allowed;
- `@dante/i18n` React-free;
- `@dante/time` owns Temporal semantics;
- generated runtime source is deterministic/committed/drift-checked where appropriate.

### 5.11 Config/environments

One canonical vocabulary only:

```text
LOCAL
DEV
UAT
PROD
```

Web public runtime config is versioned + Zod validated + fail-fast. A bounded Cloudflare delivery Worker may serve `/client-config` without becoming a DANTE BFF/backend.

### 5.12 Platform release activation

Android and iOS remain supported architectural targets. Platform-specific signed/device/store gates apply only when that platform is an activated release target.

### 5.13 Testing/CI/developer posture

- unit/component tests co-located;
- Web E2E at app boundary;
- Mobile Maestro at app boundary;
- GitHub Actions remains CI/CD authority;
- Turbo governs JS/frontend task graph only;
- no guessed required checks;
- one authoritative WSL-backed checkout preferred;
- WSL↔Windows Android/Metro bridge = **DIRECT VALIDATION REQUIRED tooling adapter**;
- no divergent Windows/WSL repo clones.

## 6. Decisions not to reopen casually

- React DOM + Vite Web / Expo+RN Mobile;
- platform-specific renderers with selective semantic sharing;
- feature-first/public-API-only architecture;
- no generic shared dumping grounds;
- Data Authority Matrix and backend canonical authority;
- operation-specific offline eligibility;
- feature data firewall;
- small real-consumer shared-package extraction;
- Web online-first / PowerSync Web dormant;
- browser PWA/service-worker dormant;
- identity-scoped local data;
- GitHub Actions primary CI/CD;
- EAS Build/Submit/Update selected services, EAS Workflows optional/dormant;
- direct validation occurs during later materialization rather than a pre-closure mega laboratory.

## 7. Direct-validation register carried forward

Still **NOT RUN**. At materialization validate progressively:

- Node/pnpm/Turbo real workspace;
- preferred pnpm isolated layout + native graph;
- hoisted fallback only if evidence requires it;
- Vite build;
- Expo Android runtime/build and iOS when target activation requires it;
- TS strict package graph;
- exports/import-boundary enforcement;
- Orval against real OpenAPI when available;
- TanStack Form + Zod Web/RN;
- DTCG/Terrazzo outputs;
- PowerSync + OP-SQLite + SQLCipher;
- offline accept/reject/conflict reconciliation;
- identity-scoped DB lifecycle;
- WSL↔Windows Android tooling;
- Web runtime config and Cloudflare delivery when activated;
- selected test stacks;
- Sentry/EAS release integration when activated.

Failure reopens the affected technology/tooling adapter unless evidence proves broader architectural inconsistency.

## 8. Git state

Workstream opened from:

```text
7a1600c2167f68c9281d3ed77b32a3d954fbd061
```

Passo-1 checkpoint:

```text
dd23b86ba330f6296806297ef5c68acebbee65e6
```

No production/frontend materialization belongs to Passo 2.

## 9. Exact next action

```text
PASSO 3
Perform one clean-room whole-Frontend-Foundation review:
Passo 1 technologies
+
Passo 2 architecture/structure
+
closed Product/Domain/Logical/Physical/Engineering constraints.

IF PASS
record closure / prepare PR / protected-main integration.

DO NOT YET
install packages
create production apps/packages scaffold
implement product surfaces
activate Cloudflare/EAS/PowerSync
claim direct validation PASS
```
