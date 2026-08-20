# Frontend Engineering Foundation — Part 2: Application Architecture and Structure

- Status: **CURRENT WORKSTREAM SPECIFICATION — PASSO 2 DESIGN COMPLETE / PENDING PASSO 3 REVIEW**
- Workstream branch: `feature/frontend-foundation`
- Decision date: 2026-08-20
- Companion technology specification: [`frontend-engineering-foundation.md`](frontend-engineering-foundation.md)
- Decision ADR: [`../decisions/ADR-009-frontend-architecture-boundaries.md`](../decisions/ADR-009-frontend-architecture-boundaries.md)
- Production frontend code: **NOT STARTED**
- Direct implementation validation: **NOT STARTED**

## 1. Purpose

This document fixes the durable application/package architecture for the DANTE Web and Mobile clients after Passo 1 selected the frontend technology stack.

The objective is not to predict every future library. The objective is to make library upgrades, provider substitutions and platform evolution local rather than architectural rewrites.

This specification consumes and does not reopen:

- Product/North Star;
- closed Domain Model;
- closed Logical Model and WL-H01..WL-H12;
- accepted Physical Model;
- closed Engineering Foundation v0;
- Passo-1 frontend technology decisions in `frontend-engineering-foundation.md` and ADR-008.

Key status discipline remains:

```text
selected != installed
installed != configured
configured != directly validated
architecture accepted != implementation evidence
```

## 2. Repository target map

The production repository remains one DANTE monorepo.

Conceptual target:

```text
dante/
├── apps/
│   ├── backend/
│   ├── web/
│   └── mobile/
├── packages/
├── prototypes/
├── docs/
├── .github/
├── package.json
├── pnpm-workspace.yaml
├── pnpm-lock.yaml
├── turbo.json
├── tsconfig.base.json
├── eslint.config.mjs
└── prettier.config.mjs
```

This is an **authorized shape**, not authorization to create every path immediately.

Rules:

- directories/packages are materialized only when they have real content and consumers;
- `apps/backend`, `apps/web`, `apps/mobile` are sibling deployable application boundaries;
- this Frontend Foundation does not invent a root `infra/` directory that does not yet exist;
- future infrastructure layout remains owned by the relevant infrastructure/backend governance scope;
- bounded Web-delivery code may be physically co-located with the Web app when toolchain coupling makes that the cleanest deployable unit, while remaining semantically delivery infrastructure rather than product/business logic;
- `prototypes/` is evidence/oracle only and production code must not import from it.

## 3. Web application boundary

Target internal shape when materialized:

```text
apps/web/
├── src/
│   ├── bootstrap/
│   ├── routes/
│   ├── routeTree.gen.ts
│   ├── features/
│   ├── ui/
│   ├── platform/
│   └── config/
├── worker/
├── tests/
│   └── e2e/
├── .storybook/
├── public/
├── index.html
├── vite.config.ts
├── wrangler.jsonc
├── tsconfig.json
└── package.json
```

### 3.1 Web responsibilities

- `bootstrap/` is the composition root: providers, startup ordering, runtime config validation and app assembly;
- `routes/` contains TanStack Router route adapters, guards, search/path validation, preload/orchestration and feature entry selection;
- `features/` contains vertical client capabilities;
- `ui/` owns DANTE Web design-system implementation;
- `platform/` owns browser-specific capabilities such as session adapter, observability adapter, browser integrations and optional future sync adapter;
- `config/` owns typed public runtime configuration interfaces/validation;
- `worker/` may own Cloudflare delivery/bootstrap endpoints but **must not** become a DANTE BFF, business backend, canonical-state owner or user-data processing layer.

### 3.2 Router rule

Route files are adapters, not feature implementations.

They may own:

- route parameters;
- typed URL/search state;
- navigation guards;
- preload/orchestration;
- feature entry composition.

They must not own:

- product business rules;
- direct database semantics;
- feature-private data adapters;
- large UI implementations;
- canonical mutation decisions.

`routeTree.gen.ts` is generated, committed runtime source, never hand edited and subject to deterministic drift checks.

## 4. Mobile application boundary

Target internal shape when materialized:

```text
apps/mobile/
├── app/
├── src/
│   ├── bootstrap/
│   ├── features/
│   ├── ui/
│   ├── platform/
│   └── config/
├── assets/
├── .maestro/
├── app.config.ts
├── eas.json
├── tsconfig.json
└── package.json
```

### 4.1 Mobile responsibilities

- `app/` contains Expo Router navigation adapters only;
- `src/bootstrap/` owns provider/runtime composition;
- `src/features/` contains native feature implementations;
- `src/ui/` owns DANTE Native design-system implementation;
- `src/platform/` owns device/native capabilities, session adapter, PowerSync lifecycle, secure-storage adapters, observability adapters and native integrations;
- `src/config/` owns typed public mobile configuration validation.

Expo Router files must remain thin navigation adapters and consume feature public APIs rather than feature internals.

## 5. Feature-first architecture

A feature may grow conceptually into:

```text
features/<feature>/
├── index.ts
├── model/
├── data/
└── ui/
```

These subdirectories are **not mandatory boilerplate**. A small feature stays small.

Meaning:

- `index.ts` is the feature public API;
- `model/` owns view/input/client workflow models and pure feature logic;
- `data/` owns the feature-specific boundary to API, TanStack Query, PowerSync or governed command adapters;
- `ui/` owns platform-specific feature presentation.

Forbidden generic dumping-ground directories include repository-wide `common/`, `shared/`, `helpers/`, `utils/`, `services/`, `hooks/` or `misc/` without a concrete owner/boundary.

A hook belongs to the feature/platform/UI system that owns its semantics.

## 6. Dependency direction and public APIs

Architecture is enforced, not merely documented.

High-level direction:

```text
bootstrap
   ↓
routes / Expo route adapters
   ↓
features
  ↙   ↘
 ui   platform
   \   /
 packages
```

Mandatory forbidden directions:

```text
packages                X→ apps
web                     X→ mobile
mobile                  X→ web
ui                      X→ features
platform                X→ features
feature A internals     X→ feature B internals
prototypes              X→ production apps/packages
```

### 6.1 Public-API-only rule

The privileged layers are not backdoors.

```text
bootstrap
may know all authorized layers
ONLY through their public APIs

routes
may know features
ONLY through feature public APIs
```

Therefore this is permitted:

```ts
import { ProfileFeature } from "@/features/profile";
```

and deep/private cross-boundary imports are forbidden even from bootstrap or route code.

### 6.2 Enforcement

Materialization must enforce the architecture through a combination of:

- package `exports`;
- ESLint flat config;
- typed rules where useful;
- `eslint-plugin-boundaries` or equivalent accepted boundary enforcement;
- restricted/deep-import rules;
- pnpm workspace isolation;
- architecture tests/checks.

A boundary violation must become a local/CI failure, not a review convention only.

## 7. Shared-package policy

Shared packages exist only for real cross-application semantics.

Initial package candidates with genuine Web+Mobile consumers:

```text
@dante/design-tokens
@dante/i18n
@dante/time
```

`@dante/api-client` is created only when real FastAPI OpenAPI exists.

Shared feature packages are extracted only after real cross-platform reuse exists:

```text
packages/features/<capability>
→ @dante/feature-<capability>
```

Code that merely *looks reusable* is not sufficient reason to extract a package.

### 7.1 Shared feature-core prohibition

A shared frontend feature core may contain only platform-neutral client logic such as:

- pure state machines;
- frontend workflow logic;
- normalization/transformation;
- view-oriented calculations;
- draft/input schemas;
- frontend validation and UX policy.

It must not own:

```text
canonical Domain invariants
canonical Authority decisions
AuthZ decisions
canonical conflict resolution
canonical persistence semantics
accepted-effect authority
canonical material-history truth
```

Mandatory invariant:

```text
frontend shared brain
!=
DANTE backend/domain/application authority
```

Frontend validation improves UX and client-boundary safety. Backend/application validation remains authoritative for consequential acceptance.

### 7.2 Shared core framework posture

Shared core packages are framework-free by default.

They must not depend on React, React Native, Expo, Vite, DOM APIs, platform storage, PowerSync implementation or TanStack Query implementation unless a later package-specific architecture decision proves that dependency belongs there.

## 8. Workspace/package semantics

Internal packages are:

```text
private
workspace-only
not independently published by default
```

Internal dependencies use `workspace:*`.

Package public surfaces use `package.json` `exports`; deep imports into internal paths are forbidden.

Internal shared packages are source-first TypeScript by default: Vite/Metro consume workspace source directly rather than forcing a mini build/publish pipeline for every internal package.

Independent package versioning/Changesets is not introduced without a real distribution/ownership requirement.

Workspace cycles are forbidden and must fail validation.

## 9. pnpm dependency-layout posture

Selected baseline:

```text
pnpm isolated dependency layout
PREFERRED BASELINE
DIRECT VALIDATION REQUIRED
```

Because native React Native dependencies can have resolution/layout constraints, the accepted fallback is:

```text
nodeLinker: hoisted
ALLOWED FALLBACK
ONLY when concrete native/toolchain evidence requires it
```

Changing the linker because of proven native compatibility constraints does **not** reopen the monorepo architecture or package-manager decision.

Supply-chain posture at materialization includes:

- committed lockfile;
- frozen lockfile in CI;
- explicit `minimumReleaseAge`/strict policy as accepted for pnpm 11;
- no blanket approval of dependency lifecycle scripts;
- explicit native dependency review;
- grouped/controlled dependency updates rather than blind native auto-merge.

## 10. Data Authority Matrix

Every persisted/read/write path must declare its authority class before implementation. Ambiguous authority blocks implementation until classified.

| State/effect class | Authority/owner | Client mechanism |
| --- | --- | --- |
| canonical accepted DANTE state/effect | backend + PostgreSQL | never client authority |
| synchronized read projection | noncanonical local SQLite projection | PowerSync reactive reads |
| offline pending mutation | local pending/staging only | SQLite + PowerSync upload |
| offline canonical acceptance | backend | governance/AuthZ/expected-state/conflict checks |
| non-synchronized remote query | backend or bounded external source | TanStack Query + typed API |
| online governed command | backend | typed FastAPI command/mutation lifecycle |
| route/navigation state | client router | TanStack Router / Expo Router |
| form draft state | client | TanStack Form |
| component transient state | client | React |
| cross-tree transient UI | client | Zustand only when justified |

### 10.1 No universal single-class fiction

An offline-eligible operation intentionally crosses several stages:

```text
local pending state
↓
PowerSync upload
↓
backend governance/conflict validation
↓
canonical commit OR rejection
↓
reconciliation
```

Therefore operation classification must preserve the distinction between **local staging** and **canonical effect authority**.

### 10.2 No duplicated authority

Forbidden by default:

```text
same DANTE entity graph
owned simultaneously by
PowerSync + TanStack Query cache + Zustand + ad-hoc fetch state
```

A feature's `data/` boundary chooses the appropriate path while hiding implementation mechanics from feature UI.

## 11. Feature data firewall

Feature UI must not directly import or depend on transport/sync internals as its primary architecture.

Target:

```text
feature UI
   ↓
feature data/model public boundary
   ↓
┌───────────────┬────────────────┬──────────────────┐
│               │                │                  │
PowerSync       TanStack Query   governed command  other bounded adapter
│               │                │
SQLite          FastAPI          FastAPI
```

Do not create a generic frontend `Repository<T>` abstraction. Use capability/operation-specific queries and commands with concrete meaning.

## 12. API/codegen boundary

When real FastAPI OpenAPI exists:

```text
FastAPI
  ↓ OpenAPI
Orval
  ↓
@dante/api-client
```

Target package shape:

```text
packages/api-client/
├── src/
│   ├── generated/
│   └── index.ts
├── orval.config.ts
└── package.json
```

Rules:

- generated code is never hand edited;
- the package is React-free and router-free;
- the generated client does not own session storage, environment reading or canonical error policy;
- callers inject/configure transport/session capabilities at app boundaries;
- do not generate blanket TanStack Query ownership for data intentionally served through PowerSync;
- feature `data/` adapters map transport/sync errors into feature-meaningful states.

## 13. Generated-source policy

Generated artifacts that are required runtime/reviewable source are committed when appropriate, including:

- TanStack `routeTree.gen.ts`;
- Orval generated transport code;
- generated Web/Native design-token outputs;
- generated i18n key/type metadata where activated.

Policy:

```text
source authority
→ deterministic generator
→ generated source committed
→ CI regeneration
→ git diff must be empty
```

No generated artifact becomes semantic authority merely because it is committed.

## 14. PowerSync and offline ownership

### 14.1 Mobile

Mobile PowerSync runtime is initially app-owned:

```text
apps/mobile/src/platform/sync/
```

It owns infrastructure concerns such as:

- database lifecycle;
- PowerSync connection lifecycle;
- OP-SQLite/SQLCipher integration;
- upload connector;
- sync status;
- identity-scoped local-database lifecycle.

Feature-specific queries/operations remain in feature `data/` boundaries.

Do **not** create `packages/sync` for one consumer. Extract only if a second real runtime shares meaningful implementation.

### 14.2 Web

Web baseline is:

```text
online-first
PowerSync Web local database = AVAILABLE / DORMANT
```

Activation requires a concrete product/runtime requirement and direct browser validation. Feature data boundaries must permit later activation without feature/UI restructuring.

### 14.3 Browser PWA/service worker

```text
PWA / browser service worker
DORMANT / NOT BASELINE
```

Do not introduce a second browser offline/cache lifecycle simply as a generic performance enhancement. Activation requires an explicit product/runtime requirement and cache/session/update design.

Cloudflare Worker delivery infrastructure is a separate concept from browser Service Workers.

## 15. Local-data identity isolation

Cross-account local-data leakage is architecturally forbidden.

Local DB namespace/key/lifecycle must be scoped to the authenticated identity/principal context accepted by the eventual security contract.

Account/session switching must support a safe sequence equivalent to:

```text
stop synchronization
close local database
clear in-memory identity-sensitive state
change identity scope
open the correct database/key
resume appropriate synchronization
```

Exact logout retention/wipe policy remains dependent on the accepted AuthN/security contract, but one user's local data must never become another user's local view by reuse accident.

## 16. Auth/session boundary

Frontend Foundation does not invent JWT/cookie/refresh-token/provider contracts before backend AuthN/AuthZ design exists.

Each app owns a platform session adapter:

```text
apps/web/src/platform/session/
apps/mobile/src/platform/session/
```

Features consume a session capability/public API, not storage mechanics.

Rules:

- `@dante/api-client` remains auth-storage agnostic;
- Zustand is not session authority;
- mobile secrets/tokens, if required, use appropriate platform secure storage rather than ordinary async/plain storage;
- Web security choices are made with the real backend/session contract, not guessed now.

## 17. UI/design-system ownership

Web:

```text
apps/web/src/ui/
├── primitives/
├── components/
├── theme/
└── motion/
```

Mobile:

```text
apps/mobile/src/ui/
├── primitives/
├── components/
├── theme/
└── motion/
```

Platform UI layers shield feature code from direct dependence on low-level libraries where practical.

Typical ownership:

```text
Web UI     → Radix / Tailwind / CSS vars / Motion / Lucide
Mobile UI  → RN primitives / StyleSheet / Reanimated / Gesture Handler / Lucide Native
```

Features consume DANTE UI components/primitives rather than spreading vendor primitives throughout feature code.

## 18. Design-token authority

`@dante/design-tokens` owns one semantic token source and deterministic platform outputs.

Conceptual shape:

```text
packages/design-tokens/
├── tokens/
│   ├── primitives.*
│   ├── semantic.*
│   └── platform overrides when justified
├── generated/
│   ├── web.css
│   └── native.ts
└── compiler/config
```

Important rule:

```text
shared semantic token
!=
identical pixel value on Web and Mobile
```

Meaning is shared; platform representation may differ deliberately.

## 19. i18n ownership

`@dante/i18n` is framework-free.

It owns:

- supported locales;
- translation resources/contracts;
- keys/types;
- fallback rules;
- common semantic messages.

It does **not** own:

- React integration;
- `react-i18next` bootstrap;
- browser/native language detection;
- persistence/storage.

Web/Mobile bootstrap layers wire `react-i18next` and platform detection/persistence as needed.

Base resources required for core UX should be bundle-available rather than requiring network access to render the application language.

## 20. Time ownership

`@dante/time` is the semantic frontend time boundary.

Use Temporal concepts according to meaning:

- Instant;
- PlainDate;
- PlainTime;
- ZonedDateTime;
- Duration.

JavaScript `Date` is not the universal DANTE semantic time type.

Transport strings are converted/mapped at data boundaries rather than through ad-hoc component-level parsing.

## 21. Environment vocabulary

DANTE uses exactly the existing lifecycle vocabulary:

```text
LOCAL
DEV
UAT
PROD
```

Frontend tools may have technical profile/channel names, but documentation and deployment meaning map back to those four contexts.

No separate permanent frontend environment taxonomy is created.

## 22. Web runtime public configuration

The Web delivery target supports one immutable SPA artifact promoted across environments while environment-specific **public** configuration is supplied at runtime.

Conceptual flow:

```text
same Web artifact
↓
DEV
↓
UAT
↓
PROD
```

A bounded delivery endpoint such as `/client-config` may be served by the co-located Cloudflare Worker.

The configuration is versioned and validated before application bootstrap.

Minimum contract shape conceptually includes:

```text
schemaVersion
environment
apiBaseUrl
powerSyncEndpoint?   # only when activated
sentryDsn?           # public DSN when activated
release metadata
```

Rules:

- Zod validates the entire config at bootstrap;
- unsupported `schemaVersion` fails clearly before normal app operation;
- components do not read scattered `import.meta.env` values as application configuration;
- client configuration is public by definition and contains no secrets;
- Worker delivery code does not become business/API authority.

## 23. Mobile configuration/release contexts

Expo/EAS technical profiles/channels map to DANTE `LOCAL/DEV/UAT/PROD` semantics.

Platform release activation is independent:

```text
Android
SUPPORTED ARCHITECTURAL TARGET

 iOS
SUPPORTED ARCHITECTURAL TARGET
```

A platform's signed-build/device/store gates are mandatory only when that platform is an activated release target.

Not releasing iOS initially does not block an accepted Web/Android release. Activating iOS later does not require a frontend architecture redesign.

EAS Update runtime compatibility remains governed; OTA must never deliver JS/assets incompatible with the installed native runtime.

## 24. Observability/error boundary

Sentry remains behind app/platform integration boundaries rather than being imported arbitrarily throughout feature code.

Preferred ownership:

```text
bootstrap
error boundaries
platform/observability
few authorized instrumentation points
```

Feature UI consumes semantic error states, not raw HTTP/PowerSync/vendor error objects as its core contract.

Privacy defaults:

- minimize personal/sensitive payloads;
- no observability shadow personal-data store;
- Session Replay remains off until an explicit privacy/product review activates it;
- release/source-map validation occurs when Sentry activation becomes real.

## 25. Testing architecture

Unit/component tests are co-located with their owner where practical:

```text
Thing.ts
Thing.test.ts

Thing.tsx
Thing.test.tsx
Thing.stories.tsx
```

Application-level tests live at their application boundary:

```text
apps/web/tests/e2e/
apps/mobile/.maestro/
```

Risk/cost tiers:

### PR baseline

- lint/boundaries;
- TypeScript strict typecheck;
- unit/component tests;
- generated-code drift;
- Storybook build/a11y where activated;
- critical Web E2E;
- mobile Jest/RNTL;
- Expo/tooling diagnostics/export smoke where applicable.

### Accepted-main/DEV/scheduled

- broader browser matrix;
- integration/contract checks;
- Android native validation where applicable;
- higher-cost resilience/performance scenarios when real code warrants them.

### UAT/release

- release browser matrix;
- signed build for each activated mobile target;
- runtime/device E2E for each activated target;
- deployment/source-map/update compatibility validation;
- applicable security/privacy/performance/recovery gates.

Cloud build success alone is not runtime QA.

## 26. CI/CD architecture

GitHub Actions remains the repository-wide primary control plane.

Frontend workflow responsibilities are separated rather than accumulated into one monolithic workflow. Intended categories may include:

```text
frontend quality
Web E2E
Mobile quality
frontend contract/codegen
Web deployment
Mobile release
```

These are responsibilities, **not pre-authorized required-check names**.

A check becomes required only after it exists, runs on the relevant PRs, emits a stable observed context and genuinely must block merge under the existing repository rule.

Turborepo orchestrates the JS/frontend task graph only. It does not become the backend/Python orchestration authority.

Remote Turbo cache remains dormant until measured CI/developer benefit justifies activation; initial posture uses local/CI caching without unnecessary vendor coupling.

## 27. Developer topology

Primary supported developer posture:

```text
one authoritative Git checkout in WSL filesystem

WSL2
- Git tree
- Node/pnpm/Turbo
- Vite
- Metro/Expo CLI
- Python/uv/backend
- Docker CLI

Windows
- JetBrains/PyCharm UI
- browser
- Android Studio/emulator
- device tooling
```

Status:

```text
SELECTED DEVELOPER POSTURE
DIRECT VALIDATION REQUIRED
```

The WSL↔Windows Android/ADB/Metro bridge is a tooling adapter, not a product architecture invariant. If direct validation requires a different bridge/networking approach, adapt that boundary without creating divergent Windows/WSL source-of-truth clones.

Hard rule:

```text
one authoritative checkout
no divergent Windows + WSL source trees
no shared cross-OS node_modules environment
```

Local iOS build is not expected on Windows; activated iOS build uses an accepted macOS-capable/cloud path such as EAS.

## 28. Direct-validation carry-forward

Passo 2 is design-complete. Direct validation remains intentionally deferred to materialization after Foundation closure/integration.

At minimum validate progressively:

1. Node 24 + pnpm 11 + Turbo real workspace;
2. preferred isolated dependency layout with Expo/native graph;
3. documented hoisted fallback only if direct evidence requires it;
4. Vite/React production build;
5. Expo/RN Android build/runtime and iOS build/runtime when target activation requires it;
6. TypeScript strict cross-package compilation;
7. package `exports` and forbidden-import enforcement;
8. ESLint architecture boundaries;
9. deterministic token generation to Web CSS + Native TS;
10. real FastAPI OpenAPI → Orval generation/compile when API exists;
11. TanStack Form exact pinned patch on Web + RN + Zod;
12. TanStack Query remote path;
13. PowerSync + OP-SQLite + SQLCipher encrypted open/write/reopen/read;
14. offline upload/accept/reject/conflict reconciliation;
15. identity-scoped local DB lifecycle;
16. WSL Metro ↔ Windows Android tooling;
17. versioned Web runtime config bootstrap;
18. Cloudflare Web delivery when activated;
19. selected Web/Mobile test stacks;
20. Sentry/EAS release integrations when activated.

A material failure reopens the affected technology/tooling adapter or boundary only unless evidence proves a wider architectural contradiction.

## 29. Passo-2 verdict

```text
PASSO 2
DESIGN COMPLETE

APPLICATION BOUNDARIES             ACCEPTED IN WORKSTREAM
FEATURE-FIRST ARCHITECTURE         ACCEPTED IN WORKSTREAM
DEPENDENCY DIRECTION               ACCEPTED IN WORKSTREAM
PUBLIC-API-ONLY RULE               ACCEPTED IN WORKSTREAM
SHARED-PACKAGE POLICY              ACCEPTED IN WORKSTREAM
DATA AUTHORITY MATRIX              ACCEPTED IN WORKSTREAM
API/CODEGEN BOUNDARY               ACCEPTED IN WORKSTREAM
POWER SYNC OWNERSHIP               ACCEPTED IN WORKSTREAM
WEB ONLINE-FIRST / PWA DORMANT     ACCEPTED IN WORKSTREAM
CONFIG/ENVIRONMENT MODEL           ACCEPTED IN WORKSTREAM
UI/TOKEN/I18N/TIME BOUNDARIES      ACCEPTED IN WORKSTREAM
TEST/CI/RELEASE ARCHITECTURE       ACCEPTED IN WORKSTREAM
DEVELOPER POSTURE                  SELECTED / VALIDATION REQUIRED

PRODUCTION CODE                    NOT STARTED
SCAFFOLD                           NOT STARTED
DEPENDENCIES INSTALLED             NO
DIRECT VALIDATION                  NOT STARTED
```

Next boundary is **Passo 3 — whole Frontend Foundation clean review, closure decision and protected-main integration preparation**.
