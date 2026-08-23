# DANTE Architecture Index

- Status: **CURRENT**

## 1. Architecture state

```text
Domain Model                  CLOSED
Logical Model                 CLOSED
Pre-Physical coherence        CLOSED
Physical target               CLOSED / ACCEPTED
Engineering Foundation v0     CLOSED / ACCEPTED
Frontend Foundation           CLOSED / ACCEPTED / integrated via PR #22
Backend scaffold              CLOSED / DIRECT QA PASS / integrated via PR #24
Frontend materialization      CLOSED / PASS — FM-00..FM-07
Frontend integration          ACTIVE — PR #28
Concrete business schema      NOT STARTED
Product verticals             NOT STARTED
```

`main` remains the integrated source authority. The active integration branch contains newer bounded frontend integration truth until PR #28 merges.

## 2. Current architecture entry points

- `system-overview.md` — current system/component/authority overview
- `technical-decisions.md` — current decision register and implementation qualifications
- `frontend-engineering-foundation.md` — design-time frontend technology specification
- `frontend-engineering-foundation-part-2.md` — frontend application/package/dependency/data-authority specification
- `../decisions/ADR-008-frontend-engineering-stack.md` — frontend technology ADR + materialization qualification
- `../decisions/ADR-009-frontend-architecture-boundaries.md` — frontend architecture ADR + materialization qualification
- `../workstreams/frontend-materialization.md` — closed direct frontend evidence
- `../workstreams/frontend-materialization-integration.md` — active integration/future-activation authority
- `../workstreams/backend-scaffold.md` — closed backend CP1-CP5 evidence
- `../development/repository-engineering-safety.md` — repository/CI/ruleset safety authority

## 3. Current system direction

One DANTE product monorepo with sibling application boundaries:

```text
apps/backend
apps/web
apps/mobile
```

and supporting ownership under `packages/`, `infra/`, `tooling/`, `tests/system/`, `docs/`, `prototypes/`, `.github/`.

Backend is a capability-first modular monolith. PostgreSQL 18.4 remains the sole canonical persistence/material-history authority.

Web and Mobile are platform-specific clients with selective semantic sharing. The frontend cannot replace backend canonical effect, AuthZ, conflict-resolution or material-history authority.

## 4. Frontend architecture — accepted and materially proven

Structural rules:

- feature-first Web/Mobile;
- route/navigation files are thin adapters;
- cross-boundary use through public APIs;
- dependency cycles forbidden;
- Web and Mobile do not import each other's private/platform implementation;
- app-local UI/platform ownership;
- shared packages only for genuine multi-consumer semantics;
- shared cores framework/platform-free by default;
- production never imports prototypes;
- architecture rules become executable checks instead of documentation-only wishes.

The current materialized graph directly passes:

```text
36 modules
45 dependencies
0 architecture violations
```

Initial genuine shared packages are:

```text
@dante/design-tokens
@dante/i18n
@dante/time
```

Do not create `@dante/api-client` until real FastAPI OpenAPI exists; do not create shared feature packages before real Web+Mobile reuse exists.

## 5. Data authority

```text
canonical accepted state/effect   backend + PostgreSQL
synced local projection           PowerSync/SQLite when activated
offline pending mutation          local staging only
offline acceptance                backend governance/conflict checks
remote request state              TanStack Query + typed API when activated
form draft                        TanStack Form when activated
component transient               React
cross-tree transient              Zustand only when justified
```

Mobile selected offline/sync infrastructure is not active merely because it is selected. Web remains online-first until a product requirement justifies browser-local sync/offline activation.

## 6. Materialization qualification

The Frontend Foundation remains the design authority. Later direct evidence qualifies implementation-specific/version-specific details.

Current qualified implementation baseline:

```text
Node                      24.19.0
pnpm                      11.22.0
TypeScript                6.0.3
Web React / React DOM     19.2.8 / 19.2.8
Vite                      8.2.1
Expo SDK                  57.x / clean resolve 57.0.15
React Native              0.86.2
Mobile React              19.2.3
Gesture Handler           2.32.0
temporal-polyfill         1.0.4
Web E2E directory         apps/web/e2e/
```

Older design-time wording such as Gesture Handler “3 line” or `@js-temporal/polyfill` does not override the later directly validated implementation. This is a bounded qualification, not a wholesale architecture reselection.

## 7. Direct evidence boundary

Directly proven:

```text
BACKEND SCAFFOLD                 PASS at CP1-CP5 stated scopes
FRONTEND MATERIALIZATION        PASS at FM-00..FM-07 stated scopes
WEB PRODUCTION BUILD            PASS
WEB CHROMIUM E2E                PASS
ANDROID HERMES BUNDLE           PASS
ANDROID EMULATOR RUNTIME        PASS
FRONTEND HOSTED CI              PASS
COMBINED PR #28 CI              PASS on candidate a91fbfc...
```

Not yet proven/activated:

```text
CONCRETE BUSINESS SCHEMA        NOT STARTED
POWERSYNC PRODUCT FLOW          NOT RUN
ORVAL PRODUCT API CLIENT        NOT MATERIALIZED
TANSTACK QUERY/FORM PRODUCT USE NOT MATERIALIZED
IOS DIRECT RELEASE VALIDATION   NOT RUN
CODEQL                          NOT ACTIVE
PRODUCTION DEPLOYMENT           NOT STARTED
```

## 8. Remaining bounded deferrals

- exact backend AuthN/AuthZ protocol;
- concrete API routes/versioning;
- first product feature inventory;
- PowerSync Web / browser PWA activation;
- remote backend compute/IaC;
- release/provider infrastructure;
- specialist scale infrastructure.

Activation triggers are recorded in `../workstreams/frontend-materialization-integration.md`.

## 9. Architecture reopen discipline

Closed Domain/Logical/Physical/Engineering/Frontend Foundation decisions are not casually reselected.

A material validation failure first reopens the affected technology/adapter/boundary. A wider architecture reopening requires concrete evidence of a wider contradiction.

## 10. Next architecture/engineering boundary

```text
complete PR #28 integration hardening
-> calibrate Frontend CI Gate
-> protected-main integration
-> activate first product vertical boundaries only as consumed
```

Backend Concrete Logical -> PostgreSQL remains a separate fresh bounded workstream.