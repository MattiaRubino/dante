# Workstream — Frontend Engineering Foundation

- Status: **ACTIVE — PASSO 1 DESIGN COMPLETE / PASSO 2 DESIGN COMPLETE / PASSO 3 CLEAN REVIEW IN PROGRESS**
- Branch: `feature/frontend-foundation`
- Base/PRE-SCOPE at workstream opening: `7a1600c2167f68c9281d3ed77b32a3d954fbd061`
- Passo-1 checkpoint: `dd23b86ba330f6296806297ef5c68acebbee65e6`
- Passo-2 initial checkpoint: `0269672b6f1cd085fa935d400b774b098feb4c69`
- PR: **NONE**
- Product: **DANTE**
- Domain: **CLOSED / CONSUMED / NOT REOPENED**
- Logical: **CLOSED / CONSUMED / WL-H01..WL-H12 ACTIVE**
- Physical: **CLOSED / SELECTED / ACCEPTED / CONSUMED**
- Engineering Foundation v0: **CLOSED / ACCEPTED / CONSUMED**
- Production frontend code: **NOT STARTED**
- Dependencies installed/configured: **NO**
- Direct frontend validation: **NOT STARTED**

## 1. Workstream contract

Exactly three substantial passes:

```text
PASSO 1  technology selection
PASSO 2  application/package/ownership architecture
PASSO 3  whole-foundation clean review + closure/integration preparation
```

Only after closure and protected-main integration may a new bounded scope materialize the production frontend scaffold and run direct validations.

This workstream does not implement product surfaces, mechanically convert prototypes, weaken Domain/Logical/Physical semantics, create empty ceremonial directories or manufacture direct PASS evidence.

## 2. Current authorities

Read:

1. development operating/safety/handoff rules;
2. closed Engineering Foundation and repository layout;
3. accepted Physical target and validation register;
4. `../architecture/frontend-engineering-foundation.md`;
5. `../architecture/frontend-engineering-foundation-part-2.md`;
6. ADR-008;
7. ADR-009;
8. current Product/Domain/Logical authority as required.

`main` remains integrated truth; this branch is authority only for newer unmerged Frontend Foundation decisions.

## 3. Passo 1 — design complete

Selected core:

```text
Node 24 LTS
TypeScript 6.0.x strict
pnpm 11
Turborepo 2.x

Web
React 19.2 + React DOM
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

Complete UI/testing/release selections remain in the Passo-1 specification.

## 4. Passo 2 — design complete after clean-review repair

### Repository ownership

Frontend consumes the closed repository topology rather than replacing it:

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

These are ownership reservations; empty paths are not created without real content.

### Application architecture

- Web/Mobile feature-first;
- route/navigation files thin adapters;
- bootstrap composition only;
- platform capabilities app-local;
- DANTE UI implementations app-local;
- no generic dumping-ground folders.

### Dependency rules

```text
packages              X→ apps
web                   X→ mobile
mobile                X→ web
ui                    X→ features
platform              X→ features
feature internals     X→ other feature internals
production            X→ prototypes
feature cycles        FORBIDDEN
```

Bootstrap/router consume other layers/features only through public APIs.

### Shared packages

Initial real candidates:

```text
@dante/design-tokens
@dante/i18n
@dante/time
```

API client only with real OpenAPI. Shared feature packages only after real Web+Mobile reuse. Shared client cores are framework-free by default and never own canonical backend/domain authority.

### Workspace posture

- private/workspace-only internal packages;
- `workspace:*`;
- package exports;
- source-first TypeScript by default;
- workspace/feature cycles forbidden;
- pnpm isolated preferred + direct validation;
- evidence-driven `nodeLinker: hoisted` fallback accepted.

### Data Authority Matrix

```text
canonical accepted effect   backend/PostgreSQL
synced local projection     PowerSync/SQLite noncanonical
offline pending mutation    local staging only
offline acceptance          backend governance/conflict checks
remote request state        TanStack Query + typed API
online governed command     FastAPI/backend
route state                 router
form draft                  TanStack Form
component transient         React
cross-tree transient        Zustand only when justified
```

Offline operation = local staging → upload → backend accept/reject → reconciliation. Local staging never becomes canonical authority.

### Data firewall

Feature UI uses feature data/model boundaries; no direct HTTP/PowerSync/query-cache/storage architecture and no universal frontend `Repository<T>`.

### Offline/session

- Mobile PowerSync app-owned initially under platform sync;
- Web online-first;
- PowerSync Web dormant;
- browser PWA/service worker dormant;
- local data identity-scoped;
- app-local session adapters;
- no invented JWT/cookie contract.

### UI/shared semantics

- distinct DANTE Web and Native UI systems;
- shared semantic tokens with platform-specific output allowed;
- `@dante/i18n` React-free;
- `@dante/time` owns Temporal semantics;
- generated runtime source deterministic/committed/drift checked when appropriate.

### Config/environments

Exactly:

```text
LOCAL
DEV
UAT
PROD
```

Web public runtime config versioned + Zod validated + fail-fast. App-coupled Cloudflare Worker may serve bounded bootstrap config but is not business/backend authority.

### Platform release

Android/iOS are supported architectural targets; signed/device/store gates apply when each platform is activated for release.

### Testing/CI/developer posture

- co-located unit/component tests;
- app-level Web E2E/Maestro;
- GitHub Actions authority;
- Turbo JS/frontend graph only;
- no guessed required-check names;
- one authoritative WSL-backed checkout preferred;
- WSL↔Windows Android/Metro adapter direct-validation required;
- no divergent source clones.

## 5. Passo-3 findings so far

Clean review identified and repaired two non-technology issues before closure:

1. **repository-layout contradiction** — the first Passo-2 draft omitted the already-accepted `infra/`, `tooling/`, `tests/system` root ownership. Corrected to consume `repository-layout-v0.md` rather than redefine root topology;
2. **feature-cycle gap** — public cross-feature imports were permitted but acyclicity was not explicit. Feature dependency cycles are now forbidden/enforceable.

Global current-truth/navigation files were also stale from Engineering Foundation and are aligned in the same repair scope.

No Product/Domain/Logical/Physical semantic reopen resulted from these repairs.

## 6. Decisions not to reopen casually

- React DOM/Vite Web and Expo/RN Mobile;
- platform-specific renderers with semantic sharing;
- feature-first/public-API-only/acyclic architecture;
- inherited root path ownership;
- small real-consumer shared package policy;
- Data Authority Matrix + backend canonical authority;
- feature data firewall;
- operation-specific offline eligibility;
- Web online-first, PowerSync Web dormant, browser SW/PWA dormant;
- identity-scoped local data;
- GitHub Actions primary CI/CD;
- direct validation belongs to later materialization, not a pre-closure mega laboratory.

## 7. Direct-validation register

Still **NOT RUN**. Carry forward at minimum:

- Node/pnpm/Turbo workspace;
- isolated native graph + evidence-driven hoisted fallback;
- Vite production build;
- Expo/RN for activated targets;
- strict TS graph;
- exports/import/cycle enforcement;
- Orval against real OpenAPI when available;
- TanStack Form/Zod Web+RN;
- DTCG/Terrazzo outputs;
- PowerSync/OP-SQLite/SQLCipher;
- offline accept/reject/conflict reconciliation;
- identity-scoped DB lifecycle;
- WSL↔Windows Android tooling;
- Web runtime config/Cloudflare when activated;
- selected tests;
- Sentry/EAS integrations when activated.

Failure first reopens the affected adapter/technology unless evidence proves wider contradiction.

## 8. Current Git state

```text
OPENING BASE
7a1600c2167f68c9281d3ed77b32a3d954fbd061

PASSO 1 CHECKPOINT
dd23b86ba330f6296806297ef5c68acebbee65e6

PASSO 2 INITIAL CHECKPOINT
0269672b6f1cd085fa935d400b774b098feb4c69
```

## 9. Exact next action

```text
COMPLETE PASSO 3 CLEAN REVIEW

IF BLOCKERS == 0
record Frontend Foundation design/architecture closure
prepare PR integration scope

DO NOT YET
create production scaffold
install packages
implement product surfaces
claim direct implementation PASS
create/merge PR without explicit authorization
```
