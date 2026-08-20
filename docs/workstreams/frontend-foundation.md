# Workstream — Frontend Engineering Foundation

- Status: **ACTIVE — PASSO 1 TECHNOLOGY SELECTION DESIGN COMPLETE / PASSO 2 NOT STARTED**
- Branch: `feature/frontend-foundation`
- Base/PRE-SCOPE at workstream opening: `7a1600c2167f68c9281d3ed77b32a3d954fbd061`
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

The workstream has three substantial passes:

```text
PASSO 1
technology selection

PASSO 2
frontend architecture / structure / ownership / dev-test-CI integration

PASSO 3
whole-foundation review / closure / PR / protected-main integration
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

This workstream does **not** implement product surfaces, translate standalone HTML prototypes into production code, change Domain/Logical/Physical semantics, or create placeholder application/package directories before structure is accepted.

Existing prototypes are UX/visual/interaction evidence only.

## 3. Current durable sources

Read at minimum:

1. [`../development/operating-rules.md`](../development/operating-rules.md);
2. [`../development/documentation-and-handoff.md`](../development/documentation-and-handoff.md);
3. [`engineering-foundation.md`](engineering-foundation.md);
4. [`../physical-model/pm-12-accepted-physical-model-v1.md`](../physical-model/pm-12-accepted-physical-model-v1.md);
5. [`../physical-model/recommendation/post-selection-validation-register-v1.md`](../physical-model/recommendation/post-selection-validation-register-v1.md);
6. [`../architecture/frontend-engineering-foundation.md`](../architecture/frontend-engineering-foundation.md);
7. [`../decisions/ADR-008-frontend-engineering-stack.md`](../decisions/ADR-008-frontend-engineering-stack.md);
8. current Product/Domain/Logical authority as needed for semantic constraints.

`main` remains the only integrated source of truth. This handoff is branch authority only for newer unmerged frontend-foundation work.

## 4. Last completed milestone — Passo 1

**Frontend Technology Selection is DESIGN COMPLETE.**

Core selected stack:

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

UI/engineering selections are fully enumerated in the current frontend architecture specification, including Radix/Tailwind, DTCG/Terrazzo tokens, Motion/Reanimated/Gesture Handler, i18next, Temporal, test tooling, Sentry, Cloudflare Web delivery and EAS mobile services.

## 5. Decisions that must not be casually reopened

### Platform

- Web is React DOM + Vite, not Next.js.
- Mobile is React Native + Expo.
- do not force React Native Web/Flutter/universal renderer merely to maximize code-sharing percentage.
- pnpm owns JS workspaces; Turbo orchestrates frontend/JS tasks without becoming a framework over Expo/Vite.

### State ownership

```text
canonical DANTE state     backend/PostgreSQL
synced local projection   PowerSync/SQLite
remote request state      TanStack Query
form state                TanStack Form
component transient       React
cross-tree transient      Zustand only when justified
```

Do not duplicate the same DANTE entity graph across those mechanisms.

### PowerSync writes

Offline eligibility is operation-specific.

```text
synced entity/table
!=
automatically offline-writable operation
```

Online consequential commands cross backend governance directly. Offline-eligible operations may stage locally/upload through PowerSync but must still pass backend expected-state/governance/AuthZ/conflict validation before canonical acceptance.

### React Native PowerSync packaging

Target the PowerSync JS v2 React Native model: `@powersync/react-native` with its default OP-SQLite driver integration, `@op-engineering/op-sqlite` and SQLCipher. Do not plan around the removed old `@powersync/op-sqlite` package.

### CI/release

- GitHub Actions = primary repository CI/CD orchestrator.
- EAS Build/Submit/Update = selected mobile services.
- EAS Workflows = optional/dormant.

### Evidence status

- TanStack Form = **SELECTED / DIRECT VALIDATION REQUIRED**, exact patch pin.
- OP-SQLite/SQLCipher integration = **SELECTED / DIRECT VALIDATION REQUIRED**.
- selected != direct PASS.
- no mega pre-Passo-2 PSV is required; direct validation occurs during materialization of the accepted structure.

## 6. Passo-2 questions — current task

Passo 2 must be performed as one coherent architecture pass, not dozens of micro-phases.

It must decide:

1. exact `apps/web` internal structure;
2. exact `apps/mobile` internal structure;
3. actual shared packages with real consumers only;
4. feature/surface/component/shared boundaries;
5. dependency direction and enforced forbidden imports;
6. generated API contract/client ownership and placement;
7. PowerSync client/sync ownership and Web offline activation boundary;
8. auth/session ownership at client boundaries without inventing backend contracts;
9. config/environment ownership;
10. design-token and platform UI boundaries;
11. time/i18n ownership;
12. error handling/observability boundaries;
13. unit/component/integration/E2E/visual/a11y test layout;
14. local Windows/WSL/Expo development topology;
15. GitHub Actions integration with Web and EAS release services.

Do not create directories/packages simply because they might be useful. A shared package must have a real boundary and consumer.

## 7. Open questions intentionally reserved for Passo 2

- whether Web v1 activates a PowerSync local database or remains online-first initially;
- exact generated-code package/location and generation boundary;
- exact package map under `packages/`;
- exact Web/Mobile feature folder structure;
- exact ESLint/import-boundary rule implementation;
- exact env/config file layout;
- exact CI job graph and cache boundaries;
- exact Windows/WSL placement for Web vs Expo tooling without duplicate repositories.

These do not reopen Passo-1 technology selection.

## 8. Direct-validation register for later materialization

Direct execution remains **NOT RUN**. Carry at minimum:

- Node/pnpm/Turbo workspace real install/build/typecheck;
- Vite production build;
- Expo Android and iOS build path;
- TypeScript strict cross-package compilation;
- PowerSync v2 + OP-SQLite + SQLCipher encrypted open/write/reopen/read;
- offline-eligible mutation upload/accept/reject/conflict reconciliation;
- TanStack Form exact patch on Web + React Native + Zod;
- Orval FastAPI OpenAPI generation + compile;
- design-token compilation to CSS + Native TS;
- selected Web/Mobile test stacks;
- Sentry release/source-map flow when activated;
- Cloudflare delivery when activated;
- EAS Build/Submit/Update when activated.

A failure may reopen only the affected technology decision unless evidence demonstrates wider architectural inconsistency.

## 9. Current Git/write state

Workstream opened from:

```text
7a1600c2167f68c9281d3ed77b32a3d954fbd061
```

The first durable write is documentation-only: current architecture specification + ADR supersession/new ADR + this handoff/current-state alignment. No frontend code or manifests belong to this documentation checkpoint.

## 10. Exact next action

```text
PASSO 2
Design the definitive frontend repository/application/package structure
and ownership/dependency rules as one coherent system.

THEN
review the Passo-2 architecture with the selected stack.

DO NOT YET
install packages
create apps/web or apps/mobile scaffold
create placeholder packages
implement product surfaces
change prototypes
```
