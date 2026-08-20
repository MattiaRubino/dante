# ADR-009: Frontend Application and Dependency Boundaries

- Status: **ACCEPTED IN FRONTEND WORKSTREAM / PENDING MAIN INTEGRATION**
- Date: 2026-08-20
- Technology authority: [`ADR-008-frontend-engineering-stack.md`](ADR-008-frontend-engineering-stack.md)
- Current structural specification: [`../architecture/frontend-engineering-foundation-part-2.md`](../architecture/frontend-engineering-foundation-part-2.md)

## Context

ADR-008 selected the frontend technology stack, but a durable DANTE frontend also requires stable ownership and dependency boundaries that survive library upgrades.

Without explicit structure, the selected tools could still collapse into a client monolith where:

- route files become feature implementations;
- PowerSync, TanStack Query, Zustand and ad-hoc fetch state duplicate ownership;
- Web and Mobile import each other's platform details;
- shared packages become generic dumping grounds;
- frontend validation accidentally grows into backend/domain authority;
- generated clients own session/config semantics;
- browser/mobile offline mechanisms proliferate without one authority model.

The closed Physical and Engineering Foundations already require singular canonical authority, operation-specific offline capability, one product monorepo and real rather than cosmetic architecture controls.

## Decision

### 1. Application boundaries

Keep three sibling deployable application boundaries:

```text
apps/backend
apps/web
apps/mobile
```

Web and Mobile are first-class platform-specific clients. They share semantics/contracts selectively but not one forced renderer or universal UI implementation.

### 2. Feature-first application architecture

Web and Mobile use vertical `features/<capability>` ownership rather than global technical dumping grounds.

Routes/navigation are adapters. Platform integrations live in app-local `platform/` boundaries. DANTE UI systems live in app-local `ui/` boundaries. App assembly lives in `bootstrap/`.

### 3. Public API and dependency direction

Cross-boundary dependencies use public APIs only.

Even bootstrap and router layers may not deep-import feature internals.

Architecture enforcement is executable through package exports, ESLint/boundary rules, workspace isolation and architecture checks.

### 4. Shared-package extraction

Shared packages are created only for real cross-application consumers.

Initial real shared semantics are design tokens, i18n and time. The API client is created only once real OpenAPI exists. Shared feature packages are extracted only after actual Web+Mobile reuse exists.

Shared client code is framework-free by default and may never own canonical Domain/AuthZ/conflict/persistence/accepted-effect authority.

### 5. Data Authority Matrix

Every data/read/write path declares its authority before implementation.

Canonical accepted state/effects remain backend/PostgreSQL authority.

PowerSync/SQLite may own synchronized local projections and offline pending state but not canonical acceptance.

TanStack Query owns request/response remote state, not synchronized local projections by default.

React/TanStack Form/Zustand own only their bounded client/transient classes.

An offline-eligible operation intentionally crosses local staging, upload, backend governance and reconciliation; local staging is never confused with canonical effect authority.

### 6. Feature data firewall

Feature UI consumes feature-specific data/model boundaries rather than directly coupling its architecture to HTTP, PowerSync, query-cache or storage implementation.

No universal frontend `Repository<T>` abstraction is introduced.

### 7. Web and Mobile offline posture

Mobile activates the selected PowerSync + encrypted SQLite architecture when materialized.

Web starts online-first. PowerSync Web remains available/dormant and may activate later without changing feature architecture.

Browser PWA/service-worker offline behavior is also dormant by default and requires an explicit requirement/design before activation.

### 8. Package-manager layout qualification

pnpm remains selected. Isolated dependency layout is the preferred baseline and must be directly validated with Expo/native dependencies.

`nodeLinker: hoisted` is an accepted evidence-driven fallback and does not reopen the monorepo architecture.

### 9. Platform-neutral shared cores

`@dante/i18n`, `@dante/time`, API contracts and shared feature cores remain framework/platform-free by default. React/React Native integration belongs to app bootstrap/platform/UI boundaries.

### 10. Runtime configuration

Web uses a versioned, Zod-validated public runtime configuration boundary so one immutable SPA artifact can be promoted across DANTE DEV/UAT/PROD where the delivery platform permits.

A bounded Cloudflare Worker may serve Web delivery/bootstrap config but is not a DANTE BFF or business backend.

### 11. Environment vocabulary

Frontend tooling maps to the existing DANTE lifecycle vocabulary only:

```text
LOCAL
DEV
UAT
PROD
```

No parallel frontend environment taxonomy is created.

### 12. Platform release activation

Android and iOS are supported architectural targets. Signed build/device/store QA gates apply when that platform is an activated release target; an inactive iOS release does not block a Web/Android release.

### 13. Developer topology

One authoritative WSL-backed checkout remains the preferred developer posture. WSL↔Windows Metro/ADB details are a directly validated tooling adapter, not a product architecture invariant.

## Consequences

Positive:

- library upgrades do not redefine product architecture;
- Web/Mobile remain independently native to their platforms;
- state/data authority is explicit;
- offline semantics preserve backend governance;
- feature internals remain locally owned;
- shared packages stay small and purposeful;
- vendor/platform adapters can change without feature rewrites;
- architecture violations can fail locally/CI.

Costs:

- public APIs and import rules require discipline;
- data-path classification must happen before ambiguous implementation;
- code may remain duplicated temporarily until real reuse justifies extraction;
- some tooling/native integration details remain direct-validation obligations.

## Explicit non-decisions

This ADR does not:

- create directories or packages;
- choose concrete product features;
- define AuthN token/cookie contracts;
- define backend API routes;
- activate PowerSync Web;
- activate a browser PWA/service worker;
- create root infrastructure layout;
- claim pnpm isolated/native compatibility has already passed;
- claim WSL/Android tooling has already passed;
- require iOS release activation;
- claim any direct implementation PASS.

## Validation/reopen rule

Materialization must execute the carried validation register. A failed native/tooling integration may reopen the affected adapter/layout choice without reopening the core feature/dependency/data-authority architecture unless evidence demonstrates a wider contradiction.

## Supersession

This ADR does not supersede ADR-008. ADR-008 owns technology selection; ADR-009 owns frontend application/package/dependency/data-authority architecture. Together with the two frontend engineering specifications they form the current unmerged Frontend Foundation design authority.
