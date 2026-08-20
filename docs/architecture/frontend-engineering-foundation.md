# Frontend Engineering Foundation

- Status: **CURRENT WORKSTREAM SPECIFICATION — PASSO 1 DESIGN COMPLETE / PENDING MAIN INTEGRATION**
- Workstream branch: `feature/frontend-foundation`
- Decision date: 2026-08-20
- Production frontend code: **NOT STARTED**
- Dependencies installed/configured: **NO**
- Direct implementation validation: **NOT STARTED**
- Next boundary: **Passo 2 — frontend structure / ownership / dependency boundaries / local-dev and CI integration**

## 1. Purpose and authority

This document is the current durable technical specification for the DANTE frontend-engineering foundation while the workstream is unmerged.

It consumes, and does not reopen, the closed Product, Domain, Logical, Physical and Engineering Foundation decisions. In particular:

- one existing product monorepo remains authoritative;
- `apps/backend`, `apps/web` and `apps/mobile` remain sibling application boundaries;
- PostgreSQL remains the sole canonical DANTE state/material-history authority;
- PowerSync/SQLite remains a bounded noncanonical local/sync mechanism;
- GitHub Actions remains the repository-wide primary CI/CD control plane;
- frontend technology selection does not authorize product-surface implementation.

After protected-main integration, this document becomes the current frontend technology authority unless a later explicit ADR/specification supersedes a decision.

## 2. Evidence/status discipline

The workstream uses the existing repository truth model:

```text
selected != installed
installed != configured
configured != directly validated
direct scenario PASS != complete system PASS
```

Therefore **SELECTED** below means an accepted architecture choice, not a claim that the integration already runs in DANTE.

For version-sensitive/high-coupling components, materialization must reverify the supported stable line before installation. A failed material validation may reopen the affected technology decision; it does not reopen the whole frontend stack by default.

## 3. Selected platform/toolchain baseline

| Concern | Decision | Status |
| --- | --- | --- |
| frontend language | TypeScript 6.0.x, strict | **SELECTED** |
| future TypeScript line | TypeScript 7 | **TARGET UPGRADE / NOT BASELINE** |
| JS/tooling runtime | Node.js 24 LTS | **SELECTED** |
| package manager | pnpm 11 | **SELECTED** |
| JS/frontend monorepo task orchestration | Turborepo 2.x | **SELECTED** |
| repository CI/CD authority | GitHub Actions | **ALREADY SELECTED / EXTENDED** |
| web rendering platform | React 19.2 + React DOM | **SELECTED** |
| web build/dev | Vite 8 | **SELECTED** |
| web routing | TanStack Router | **SELECTED** |
| mobile rendering platform | React Native 0.86 | **SELECTED** |
| mobile framework | Expo SDK 57 | **SELECTED** |
| mobile routing | Expo Router | **SELECTED** |

Initial compatibility baseline for Expo SDK 57 is React 19.2.x / React Native 0.86 / TypeScript 6.0.x. Do not force TypeScript 7 or Node 26 merely because they are newer; upgrade only after compatibility is directly established.

### 3.1 Web model

`apps/web` is a browser-first React DOM application. Vite is the application build/dev layer. DANTE does not introduce Next.js as a second application-server/backend boundary.

The Web may use server-delivered APIs and synchronized local projections, but FastAPI/application services remain the DANTE backend boundary.

### 3.2 Mobile model

`apps/mobile` is a native React Native application through Expo. Expo development builds, native modules and EAS services are allowed; Expo Go is not the production capability boundary.

Web and Mobile share semantics/contracts/logic where valuable, but do not force one universal renderer or identical UI component implementation.

## 4. State and data ownership

DANTE does not have one universal frontend store. State ownership is explicit:

| State class | Owner / mechanism |
| --- | --- |
| canonical DANTE state/material history | backend + PostgreSQL |
| Web route/path/search state | TanStack Router |
| Mobile navigation state | Expo Router |
| synchronized local projection | PowerSync + SQLite |
| reactive synchronized reads | `@powersync/react` |
| request/response remote state | TanStack Query 5 |
| remote command/mutation lifecycle | TanStack Query + typed API client where applicable |
| form state | TanStack Form |
| runtime/frontend input validation | Zod 4 |
| component-local transient state | React |
| cross-tree transient UI state | Zustand only when a real need exists |

### 4.1 Prohibited state duplication

Do not copy the same authoritative/synchronized entity graph into PowerSync, TanStack Query and Zustand merely for convenience.

```text
PowerSync != canonical database
TanStack Query != local sync database
Zustand != DANTE entity store
Zod != Domain Model
frontend DTO/type != canonical Domain/Logical authority
```

Zustand is a **selected specialist / dormant by default**. It activates only for genuine cross-tree transient UI state that does not belong in URL state, local component state, a form, PowerSync or TanStack Query.

## 5. PowerSync / offline read and write contract

The accepted Physical Model already establishes PostgreSQL as canonical and encrypted SQLite as a noncanonical local working copy. Frontend implementation must preserve that stronger rule.

### 5.1 Read path A — synchronized projection

```text
PostgreSQL canonical
        ↓ approved client-safe projection
PowerSync replication
        ↓
encrypted SQLite
        ↓
PowerSync reactive read
        ↓
UI
```

### 5.2 Read path B — request/response or non-synchronized capability

```text
UI
 ↓
TanStack Query
 ↓
typed FastAPI boundary
 ↓
PostgreSQL canonical and/or bounded external capability
```

### 5.3 Write path A — online governed command

```text
UI
 ↓
typed FastAPI command
 ↓
AuthZ / governance / expected-state validation
 ↓
PostgreSQL canonical commit
 ↓
PowerSync replication where projected
 ↓
local projection reflects accepted state
```

### 5.4 Write path B — offline-eligible operation

```text
UI
 ↓
local pending mutation
 ↓
PowerSync upload queue
 ↓
DANTE backend
 ↓
AuthZ / governance / expected-state / conflict checks
 ↓
canonical commit OR reject/conflict
 ↓
client reconciliation
```

Mandatory invariant:

> **Offline capability is operation-specific. A synchronized table/entity does not imply that every mutation against it is offline-eligible.**

Local arrival order does not define semantic truth. Universal consequential LWW remains forbidden.

### 5.5 React Native database integration

For the PowerSync JavaScript v2 line, the React Native selection is:

```text
@powersync/react-native
+ default OP-SQLite driver integration
+ @op-engineering/op-sqlite
+ SQLCipher
```

Status: **SELECTED / DIRECT VALIDATION REQUIRED**.

The old separate `@powersync/op-sqlite` package is not the target v2 packaging.

### 5.6 Web offline activation

PowerSync Web remains an available selected capability, but **mandatory Web local-database/offline activation is not decided by Passo 1**.

Passo 2 must decide the Web runtime activation boundary from actual requirements. The default must not become “offline everywhere” merely because PowerSync Web exists.

## 6. API contracts and remote-state boundary

### 6.1 OpenAPI/code generation

FastAPI OpenAPI is the transport-contract source. Orval 8 is selected for TypeScript client/type generation.

Status: **SELECTED / DIRECT VALIDATION REQUIRED**.

The exact generated-output placement and whether a particular endpoint receives generated TanStack Query helpers, Zod artifacts or MSW mocks belongs to Passo 2/materialization. Do not generate blanket HTTP query hooks for read models intentionally served from PowerSync local projections.

### 6.2 TanStack Query

TanStack Query 5 owns request/response server state and command/mutation lifecycle where the interaction is genuinely remote/request-based.

It does not become a second cache authority for every PowerSync-backed read.

### 6.3 PowerSync TanStack adapter

`@powersync/tanstack-react-query` is not a Foundation dependency while its relevant integration line is alpha. Reopen only after maturity and demonstrated value.

## 7. Forms and runtime validation

### 7.1 TanStack Form

TanStack Form stable v1 is selected for Web and React Native form state/workflows.

Status: **SELECTED / DIRECT VALIDATION REQUIRED**.

Policy:

- exact patch pin at materialization;
- validate Web usage;
- validate React Native usage;
- validate Zod integration;
- major-version changes require explicit evaluation rather than silent upgrade.

If direct validation reveals a material issue that cannot be reasonably contained, reopen only this decision against React Hook Form.

### 7.2 Zod

Zod 4 is selected for runtime/frontend validation and schema composition where appropriate.

Frontend validation improves UX and boundary safety; backend/domain validation remains authoritative for consequential semantics.

## 8. UI foundation / styling / design tokens

### 8.1 Web

```text
Radix Primitives
+ Tailwind CSS 4.x
+ CSS custom properties
+ DANTE semantic design tokens
```

Radix provides headless accessible Web primitives. Tailwind is an implementation utility, not the design authority.

### 8.2 Mobile

```text
React Native StyleSheet
+ typed DANTE tokens
```

Do not introduce a universal styling framework by default. NativeWind 5/Tamagui/Unistyles are not part of the initial Foundation baseline.

### 8.3 Design-token authority

DANTE token meaning must have one source, not one Web copy and one Mobile copy.

```text
DTCG-compatible semantic tokens
        ↓
Terrazzo 2.x compiler
       / \
      /   \
Web CSS   Native TypeScript
variables tokens
```

DTCG 2025.10 is the selected token interchange model; Terrazzo is a replaceable compiler/tool, not a product-semantic authority.

## 9. Motion, gestures and interaction specialists

| Concern | Decision | Status |
| --- | --- | --- |
| simple Web motion | CSS | **DEFAULT** |
| advanced Web animation | Motion 13 line | **SELECTED SPECIALIST** |
| native animation | Reanimated 4 line | **SELECTED** |
| native gestures | React Native Gesture Handler 3 line | **SELECTED** |
| Web drag/drop | dnd-kit modern React packages | **SELECTED SPECIALIST / DORMANT** |
| virtualization | TanStack Virtual | **SELECTED SPECIALIST / DORMANT** |
| advanced tabular UI | TanStack Table | **SELECTED SPECIALIST / DORMANT** |

Specialists are installed only when a real consumer exists. Do not create placeholder infrastructure/packages for dormant tools.

## 10. Internationalization, time and assets

### 10.1 i18n

```text
i18next 26 line
+ react-i18next
+ i18next-cli/tooling where useful
```

Status: **SELECTED**.

Translations/resources may be shared where semantics are common while platform rendering remains independent.

### 10.2 Date/time semantics

Temporal semantics are selected as the frontend time model, using `@js-temporal/polyfill` while native runtime coverage is insufficient.

DANTE must distinguish concepts such as instant, local date/time, zoned date/time and duration instead of using JavaScript `Date` as a universal semantic container.

### 10.3 Icons/assets

Lucide is selected as the default icon family because it supports both Web and React Native use. Product artwork/brand assets remain normal versioned product assets and are not coupled to the icon library.

## 11. Quality, testing and accessibility

### 11.1 Static quality

```text
ESLint flat config
+ typescript-eslint typed rules
+ eslint-config-expo where applicable
+ Prettier 3
```

ESLint remains the architecture/lint authority rather than replacing the stack with Biome. Passo 2 will define dependency/import boundaries.

### 11.2 Web testing

```text
Vitest 4.x
React Testing Library
Storybook 10.x
Playwright 1.x
axe-core / Storybook a11y / Playwright accessibility checks
```

Playwright is the primary Web E2E/browser/trace/screenshot-regression tool.

### 11.3 Mobile testing

```text
Jest
jest-expo
React Native Testing Library
Maestro for mobile E2E
```

Exact Expo-compatible versions are resolved at materialization with Expo tooling and lockfile pinning.

### 11.4 Visual cloud review

Chromatic is **OPTIONAL / DORMANT**. Local/CI Storybook + Playwright evidence does not require a paid visual-review service from day one.

## 12. Observability

Frontend observability target:

```text
Sentry
Web + Mobile errors/crashes/performance/release/source maps
```

Status: **SELECTED / ACTIVATION VALIDATION REQUIRED**.

Backend observability remains the already selected OpenTelemetry → Grafana Alloy → Grafana Cloud EU path. The frontend is not forced to use browser OpenTelemetry as its primary telemetry SDK merely for symmetry.

Privacy/minimization rules apply: observability must not become a shadow personal-data store.

## 13. Build, delivery and release

### 13.1 Repository orchestration

GitHub Actions remains the primary repository CI/CD orchestrator.

### 13.2 Web delivery

Cloudflare Workers Static Assets is the selected Web delivery target, using current Wrangler/Cloudflare Vite integration where applicable.

Status: **SELECTED DELIVERY TARGET / DIRECT DEPLOYMENT VALIDATION REQUIRED**.

This does not create a second DANTE application backend; FastAPI remains the backend/application boundary.

### 13.3 Mobile services

```text
EAS Build   SELECTED
EAS Submit  SELECTED
EAS Update  SELECTED
```

`EAS Workflows` is **OPTIONAL / DORMANT** because GitHub Actions already owns repository CI/CD orchestration. It may be activated later if mobile-specific orchestration materially reduces complexity.

For the primary Windows development environment, Android can be exercised locally as supported; iOS native build validation uses the accepted cloud/macOS-capable path such as EAS Build rather than pretending Windows can perform a local iOS build.

## 14. Config and secrets

Frontend configuration must be typed/fail-fast where useful, with Zod available for runtime config validation.

Security rule:

> Anything embedded in a Web bundle or shipped application bundle must be treated as public client configuration, not a secret.

Use repository/provider-native secret mechanisms as appropriate:

- GitHub Actions secrets/OIDC for repository automation;
- EAS secrets/credentials for mobile build/release scopes;
- Cloudflare secrets/variables for delivery/runtime scopes;
- no live credential committed to Git.

The exact env-file/config-module structure belongs to Passo 2.

## 15. Direct-validation obligations carried into materialization

Passo 1 is design-complete while the following remain **NOT RUN** until real scaffold/artifacts exist:

1. Node 24 + pnpm + Turbo workspace install/build/typecheck path;
2. Vite 8 + React 19.2 production Web build;
3. Expo SDK 57 development/native build on Android and iOS build path;
4. TypeScript 6 strict compilation across shared/Web/Mobile boundaries;
5. PowerSync JS v2 + OP-SQLite + SQLCipher actual encrypted DB open/write/reopen/read behavior;
6. PowerSync sync + offline-eligible mutation upload + accepted/rejected/conflict reconciliation;
7. TanStack Form exact pinned patch on Web and React Native with Zod;
8. Orval FastAPI OpenAPI → TypeScript/client generation and compilation;
9. DTCG/Terrazzo token generation to Web CSS and Native TypeScript;
10. i18n extraction/type/resource workflow where activated;
11. Vitest/RTL/Playwright and Jest/RNTL/Maestro smoke paths;
12. Sentry source-map/release integration when activated;
13. Cloudflare Web deployment when remote delivery is activated;
14. EAS Build/Submit/Update integration when mobile release infrastructure is activated.

A failure reopens only the affected decision unless evidence demonstrates a wider architectural contradiction.

## 16. Optional/dormant and deferred decisions

### Selected specialists, dormant until a consumer exists

- Zustand;
- dnd-kit;
- TanStack Virtual;
- TanStack Table;
- MSW generation/activation;
- Chromatic;
- EAS Workflows.

### Explicitly not selected for the current baseline

- Next.js for `apps/web`;
- Flutter;
- React Native Web as universal DANTE renderer;
- native Kotlin + Swift as primary mobile strategy;
- Nx as monorepo framework;
- Node 26 Current as baseline;
- TypeScript 7 as initial Expo 57 baseline;
- TanStack Start;
- NativeWind 5 as production baseline;
- Tamagui as universal UI layer;
- Unistyles as initial required styling layer;
- Material UI as DANTE design foundation;
- Redux Toolkit as default global state authority;
- PowerSync TanStack adapter alpha;
- current openapi-typescript line as the TS6 codegen baseline;
- Hey API pre-1.0 as Foundation codegen authority;
- Biome as the Foundation lint/format replacement;
- browser OpenTelemetry as primary frontend observability;
- React Compiler as a required baseline optimization;
- Moment/Day.js as frontend time authority;
- Workers Sites as Web delivery mechanism.

A later measured requirement may reopen a bounded decision through normal architecture governance.

## 17. Passo 1 verdict

```text
FRONTEND TECHNOLOGY SELECTION
DESIGN COMPLETE

selected technologies are architecture decisions,
not blanket direct-PASS claims.

deep/native/security-sensitive/sync-sensitive/high-coupling
integrations carry explicit validation obligations
into Frontend Foundation materialization.

PRODUCTION CODE
NOT STARTED

DEPENDENCIES INSTALLED
NO

DIRECT FRONTEND VALIDATION
NOT STARTED
```

No additional general technology-search phase is required before Passo 2.

## 18. Next boundary — Passo 2

Passo 2 must define, in one coherent architecture pass:

- exact `apps/web` and `apps/mobile` internal structure;
- real shared-package map with actual consumers only;
- dependency direction and forbidden imports;
- API generated-code ownership/placement;
- PowerSync/sync ownership and Web activation boundary;
- state ownership implementation boundaries;
- design-token/UI package boundaries;
- configuration/env ownership;
- test layout and fixtures/mocks;
- local Windows/WSL/Expo development workflow;
- GitHub Actions integration and release boundaries.

Passo 2 is architecture/structure design, not product-surface implementation.
