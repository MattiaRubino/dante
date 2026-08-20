# ADR-009: Frontend Application and Dependency Boundaries

- Status: **ACCEPTED IN FRONTEND WORKSTREAM / PENDING MAIN INTEGRATION**
- Date: 2026-08-20
- Technology authority: [`ADR-008-frontend-engineering-stack.md`](ADR-008-frontend-engineering-stack.md)
- Structural specification: [`../architecture/frontend-engineering-foundation-part-2.md`](../architecture/frontend-engineering-foundation-part-2.md)
- Inherited repository-layout authority: [`../development/repository-layout-v0.md`](../development/repository-layout-v0.md)

## Context

ADR-008 selected the frontend technology stack. DANTE also needs ownership/dependency rules that survive library upgrades and remain consistent with the already-accepted root repository topology.

Without explicit boundaries, the frontend could still collapse into a client monolith where routes become feature implementations, state authorities duplicate, Web/Mobile leak platform details, shared packages become dumping grounds, frontend policy replaces backend authority or offline mechanisms proliferate without governance.

## Decision

### 1. Inherit root repository layout

Frontend Foundation does not redefine the closed Engineering Foundation root topology.

Reserved ownership remains:

```text
apps/
packages/
infra/
tooling/
tests/system/
docs/
prototypes/
.github/
```

Paths are created only when real content exists.

`infra/` owns infrastructure definitions and never DANTE business logic. Application-specific Web delivery/bootstrap code may be co-located with `apps/web` when it belongs to the Web deployable/toolchain; provider/infrastructure desired state remains under the accepted infrastructure ownership model.

### 2. Application boundaries

Keep sibling deployable boundaries:

```text
apps/backend
apps/web
apps/mobile
```

Web and Mobile are first-class platform-specific clients with selective semantic sharing, not one forced renderer.

### 3. Feature-first architecture

Web and Mobile use vertical `features/<capability>` ownership. Routes/navigation are adapters. Platform integrations are app-local `platform/`; DANTE UI implementations are app-local `ui/`; assembly is `bootstrap/`.

### 4. Public API and acyclic dependency direction

Cross-boundary dependencies use public APIs only. Bootstrap/router are not deep-import backdoors.

Feature dependencies must remain acyclic. Cycles require boundary/orchestration repair rather than import exceptions.

Architecture enforcement is executable through package exports, ESLint/boundary rules, workspace/cycle validation and architecture checks.

### 5. Shared-package extraction

Shared packages are created only for real multi-consumer semantics. Initial genuine shared candidates are design tokens, i18n and time. API client appears only when real OpenAPI exists. Shared feature packages require actual Web+Mobile reuse.

Shared client cores are framework-free by default and may never own canonical Domain/AuthZ/conflict/persistence/accepted-effect/material-history authority.

### 6. Data Authority Matrix

Every persisted/read/write path declares authority before implementation.

Canonical accepted state/effects remain backend/PostgreSQL authority.

PowerSync/SQLite may own synchronized local projections and offline pending state, not canonical acceptance.

TanStack Query owns request/response remote state, not synchronized local projections by default.

React/TanStack Form/Zustand own only bounded client/transient classes.

Offline-eligible operations cross local staging, upload, backend governance and reconciliation; local staging never becomes canonical effect authority.

### 7. Feature data firewall

Feature UI consumes feature-specific data/model boundaries rather than direct architectural coupling to HTTP, PowerSync, query cache or storage implementation. No universal frontend `Repository<T>` is introduced.

### 8. Web/Mobile offline posture

Mobile activates selected PowerSync + encrypted SQLite when materialized.

Web starts online-first. PowerSync Web is available/dormant and may activate later behind the same feature data boundaries.

Browser PWA/service-worker offline behavior is dormant by default and requires explicit design before activation.

### 9. Package-manager layout qualification

pnpm remains selected. Isolated layout is preferred and directly validated with Expo/native dependencies. `nodeLinker: hoisted` is an accepted evidence-driven fallback and does not reopen the monorepo architecture.

### 10. Platform-neutral shared cores

`@dante/i18n`, `@dante/time`, API contracts and shared feature cores remain framework/platform-free by default. React/RN integration belongs to app bootstrap/platform/UI boundaries.

### 11. Runtime configuration

Web uses versioned, Zod-validated public runtime config so one immutable SPA artifact can be promoted across DANTE DEV/UAT/PROD where the platform permits.

A bounded Cloudflare Worker may serve Web delivery/bootstrap config but is not a DANTE BFF/business backend.

### 12. Environment vocabulary

Frontend tooling maps to existing DANTE contexts only:

```text
LOCAL
DEV
UAT
PROD
```

### 13. Platform release activation

Android and iOS are supported architectural targets. Signed build/device/store gates apply when a platform is an activated release target; inactive iOS does not block a Web/Android release.

### 14. Developer topology

One authoritative WSL-backed checkout remains preferred. WSL↔Windows Metro/ADB details are a directly validated tooling adapter, not product architecture.

## Consequences

Positive:

- framework/provider upgrades do not redefine product architecture;
- Web/Mobile stay native to their platforms;
- root path ownership remains consistent with Engineering Foundation;
- feature/package cycles and deep-import backdoors are forbidden;
- state/data authority is explicit;
- offline semantics preserve backend governance;
- shared packages stay small/purposeful;
- adapters can change without feature rewrites;
- architecture violations can fail locally/CI.

Costs:

- public APIs and cycle rules require discipline;
- data authority must be classified before ambiguous implementation;
- some duplication remains until real reuse justifies extraction;
- native/tooling details retain direct-validation obligations.

## Explicit non-decisions

This ADR does not create directories/packages, choose product features, define AuthN token/cookie contracts, define backend routes, activate PowerSync Web, activate a browser PWA/service worker, materialize infrastructure, claim pnpm-isolated/WSL/native PASS, require iOS release activation or claim direct implementation PASS.

## Validation/reopen rule

Materialization executes the carried validation register. A failed native/tooling integration first reopens the affected adapter/layout choice, not the core feature/dependency/data-authority architecture unless evidence proves wider contradiction.

## Relationship to ADR-008

ADR-008 owns technology selection. ADR-009 owns frontend application/package/dependency/data-authority architecture. Neither supersedes the other.
