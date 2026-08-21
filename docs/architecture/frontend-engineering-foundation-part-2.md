# Frontend Engineering Foundation — Part 2: Application Architecture and Structure

- Status: **CURRENT SPECIFICATION — PASSO 2 DESIGN COMPLETE / PASSO 3 FINAL REVIEW PASS / INTEGRATED VIA PR #22**
- Historical workstream branch: `feature/frontend-foundation` — **MERGED / AUTO-DELETED**
- Decision date: 2026-08-20
- Companion technology specification: [`frontend-engineering-foundation.md`](frontend-engineering-foundation.md)
- Repository-layout authority: [`../development/repository-layout-v0.md`](../development/repository-layout-v0.md)
- Decision ADR: [`../decisions/ADR-009-frontend-architecture-boundaries.md`](../decisions/ADR-009-frontend-architecture-boundaries.md)
- Production frontend code: **NOT STARTED**
- Direct implementation validation: **NOT STARTED**

## 1. Purpose

This document fixes the durable Web/Mobile application, package, ownership and dependency architecture after Passo 1 selected the frontend technology stack.

The goal is not to freeze library versions forever. The goal is to keep future framework/provider upgrades local so they do not force a frontend architectural rewrite.

This specification consumes and does not reopen the accepted Product, Domain, Logical, Physical, Engineering Foundation and repository-layout authorities.

Status discipline:

```text
selected != installed
installed != configured
configured != directly validated
architecture accepted != implementation evidence
```

## 2. Repository topology and ownership

The repository root topology was already accepted by Engineering Foundation v0. Frontend Foundation **extends the deferred internals of `apps/web`, `apps/mobile` and real frontend packages; it does not redefine the root topology**.

Accepted conceptual repository shape:

```text
dante/
├── apps/
│   ├── backend/
│   ├── web/
│   └── mobile/
├── packages/
├── infra/
│   ├── local/
│   ├── compose/
│   └── iac/
├── tooling/
├── tests/
│   └── system/
├── docs/
├── prototypes/
├── .github/
├── package.json
├── pnpm-workspace.yaml
├── pnpm-lock.yaml
├── turbo.json
├── tsconfig.base.json
├── eslint.config.mjs
└── prettier.config.mjs
```

The shape is an ownership contract, **not** authorization to create empty directories. Paths are materialized only when real content exists.

Root ownership remains:

- `apps/*` — deployable applications;
- `packages/*` — only genuine shared artifacts/contracts;
- `infra/*` — infrastructure definitions, never DANTE business logic;
- `tooling/*` — deterministic repository engineering utilities only;
- `tests/system/*` — true black-box/cross-application/deployed-system validation only;
- `docs/*` — durable project authority;
- `prototypes/*` — non-production evidence/oracle.

Production apps/packages must never import from `prototypes/`.

### 2.1 Web-delivery code versus infrastructure authority

A small Cloudflare Worker tightly coupled to the Web deployable may be physically co-located under `apps/web/worker/` when Wrangler/Vite deployment makes that the cleanest application delivery unit.

Semantic ownership remains bounded:

```text
apps/web/worker
application-specific Web delivery/bootstrap adapter

infra/*
provider/infrastructure desired-state ownership when materialized
```

The Web Worker may expose bounded public bootstrap configuration such as `/client-config`; it must not become a DANTE BFF, business backend, canonical-state owner, persistence layer or general user-data processing service.

## 3. Web application boundary

Target internal shape when real content exists:

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
├── worker/                    # only when Web delivery adapter is materialized
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

Responsibilities:

- `bootstrap/` — composition root, providers, startup ordering, validated config and application assembly;
- `routes/` — TanStack Router adapters, typed path/search state, guards, preload/orchestration and feature entry selection;
- `features/` — vertical client capabilities;
- `ui/` — DANTE Web design-system implementation;
- `platform/` — browser/session/observability/browser integration and optional future Web sync adapters;
- `config/` — typed public runtime config schema/access;
- `worker/` — bounded Web delivery/bootstrap adapter only.

Route files do not own product rules, direct persistence semantics, feature-private data adapters, canonical mutation decisions or large feature UI implementations.

`routeTree.gen.ts` is generated, committed runtime source, never hand edited and drift checked.

## 4. Mobile application boundary

Target internal shape when real content exists:

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

Responsibilities:

- `app/` — Expo Router navigation adapters only;
- `src/bootstrap/` — app/runtime/provider composition;
- `src/features/` — native feature implementations;
- `src/ui/` — DANTE Native design system;
- `src/platform/` — native/device/session/PowerSync/secure-storage/observability integrations;
- `src/config/` — typed public mobile config validation.

Expo route files consume feature public APIs rather than feature internals.

## 5. Feature-first architecture

A feature may grow into:

```text
features/<feature>/
├── index.ts
├── model/
├── data/
└── ui/
```

Subdirectories are optional and appear only when complexity justifies them.

- `index.ts` — feature public API;
- `model/` — view/input/client workflow models and pure client logic;
- `data/` — feature-specific API/Query/PowerSync/governed-command adapters;
- `ui/` — platform-specific feature presentation.

Do not create repository-wide dumping grounds such as generic `common/`, `shared/`, `helpers/`, `utils/`, `services/`, `hooks/` or `misc/` without a precise owner and responsibility.

Hooks live with the feature/platform/UI system that owns their semantics.

## 6. Dependency direction, public APIs and cycles

Architecture is executable policy, not naming convention.

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

Forbidden directions:

```text
packages                X→ apps
web                     X→ mobile
mobile                  X→ web
ui                      X→ features
platform                X→ features
feature A internals     X→ feature B internals
production              X→ prototypes
infra                   X→ application-source ownership
```

Cross-feature use may occur only through feature public APIs and must remain acyclic.

```text
FEATURE DEPENDENCY CYCLES
FORBIDDEN
```

If feature A and feature B require each other, the design must be repaired by moving orchestration to an appropriate higher owner/capability or extracting a genuinely shared lower-level semantic boundary. Cycles are not solved with deep-import exceptions.

### 6.1 Public-API-only privileged layers

```text
bootstrap
may know all authorized layers
ONLY through public APIs

routes
may know features
ONLY through feature public APIs
```

Deep/private cross-boundary imports remain forbidden even in composition/router code.

### 6.2 Enforcement

Materialization enforces boundaries using the appropriate combination of:

- package `exports`;
- ESLint flat config;
- typed lint rules where useful;
- `eslint-plugin-boundaries` or an equivalent accepted architecture-rule mechanism;
- restricted/deep-import rules;
- pnpm workspace isolation;
- feature/package cycle detection;
- architecture tests/checks.

A violation fails locally/CI rather than remaining a review-only convention.

## 7. Shared-package policy

Shared packages exist only for real multi-consumer semantics.

Initial cross-platform package candidates with genuine Web+Mobile use:

```text
@dante/design-tokens
@dante/i18n
@dante/time
```

`@dante/api-client` is created only when real FastAPI OpenAPI exists.

Shared feature packages are extracted only after actual cross-platform reuse exists:

```text
packages/features/<capability>
→ @dante/feature-<capability>
```

Code that merely looks reusable is not sufficient reason to extract a package.

### 7.1 Frontend shared brain is not backend authority

A shared frontend feature core may contain platform-neutral client logic such as:

- pure state machines;
- frontend workflow logic;
- normalization/transformation;
- view-oriented calculations;
- draft/input schemas;
- frontend validation and UX policy.

It may never own:

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

Frontend validation improves UX/client-boundary safety. Backend/application validation governs consequential acceptance.

### 7.2 Framework-free shared core default

Shared core packages are framework/platform-free by default. They do not depend on React, React Native, Expo, Vite, DOM APIs, platform storage, PowerSync implementation or TanStack Query implementation unless a later package-specific decision demonstrates that dependency belongs there.

## 8. Workspace/package semantics

Internal packages are private, workspace-only and not independently published by default.

Internal dependencies use `workspace:*`.

Package public surfaces use `package.json` `exports`; private/deep imports are forbidden.

Shared packages are source-first TypeScript by default so Vite/Metro can consume workspace source without forcing a mini publish/build pipeline for every package.

Independent package versioning/Changesets is not introduced without a real distribution/ownership requirement.

Workspace cycles are forbidden and validated.

## 9. pnpm dependency-layout posture

```text
pnpm isolated dependency layout
PREFERRED BASELINE
DIRECT VALIDATION REQUIRED
```

Accepted fallback:

```text
nodeLinker: hoisted
ALLOWED
ONLY when concrete native/toolchain evidence requires it
```

An evidence-driven linker fallback does not reopen pnpm or the monorepo architecture.

Supply-chain posture at materialization includes:

- committed lockfile;
- frozen lockfile in CI;
- explicit accepted pnpm release-age policy;
- no blanket dependency lifecycle-script approval;
- native dependency review;
- grouped/controlled dependency update PRs rather than blind native auto-merge.

## 10. Data Authority Matrix

Every persisted/read/write path declares authority before implementation. Ambiguous authority blocks implementation until classified.

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

Local staging is never canonical effect authority.

Forbidden by default:

```text
same DANTE entity graph
owned simultaneously by
PowerSync + TanStack Query cache + Zustand + ad-hoc fetch state
```

## 11. Feature data firewall

Feature UI consumes feature-specific data/model boundaries rather than being architecturally coupled directly to HTTP, PowerSync, query-cache or storage internals.

```text
feature UI
   ↓
feature data/model boundary
   ↓
PowerSync | TanStack Query | governed command | bounded adapter
```

No generic frontend `Repository<T>` abstraction is introduced. Queries/commands remain capability/operation specific.

## 12. API/codegen boundary

When real FastAPI OpenAPI exists:

```text
FastAPI
↓ OpenAPI
Orval
↓
@dante/api-client
```

Target package:

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
- package is React/router free;
- generated client does not own session storage, env reading or canonical error policy;
- app boundaries supply transport/session configuration;
- do not generate blanket Query ownership for PowerSync-backed reads;
- feature `data/` adapters map transport/sync errors into feature-meaningful states.

## 13. Generated-source policy

Runtime/reviewable generated source is committed where appropriate, including:

- TanStack `routeTree.gen.ts`;
- Orval generated transport code;
- generated Web/Native design-token outputs;
- generated i18n key/type metadata when activated.

```text
source authority
→ deterministic generator
→ generated source committed
→ CI regeneration
→ clean diff required
```

Generated output never becomes semantic authority merely because it is committed.

## 14. PowerSync/offline ownership

### Mobile

Initial PowerSync runtime ownership:

```text
apps/mobile/src/platform/sync/
```

It owns database lifecycle, PowerSync connection, OP-SQLite/SQLCipher integration, upload connector, sync status and identity-scoped DB lifecycle. Feature-specific query/operation semantics stay inside feature data boundaries.

Do not create `packages/sync` for one consumer.

### Web

```text
online-first baseline
PowerSync Web local database = AVAILABLE / DORMANT
```

Future activation requires a concrete requirement and direct browser validation. Feature data boundaries must permit activation without feature/UI restructuring.

### Browser PWA/service worker

```text
PWA / browser service worker
DORMANT / NOT BASELINE
```

Do not create a second browser offline/cache lifecycle as a generic optimization. Activation requires explicit product/runtime, cache, session and update design.

Cloudflare Workers and browser Service Workers are separate concepts.

## 15. Identity-scoped local data

Cross-account local-data leakage is architecturally forbidden.

Local DB namespace/key/lifecycle is scoped to the accepted authenticated identity/principal context.

Safe identity switching must support a sequence equivalent to:

```text
stop sync
close DB
clear identity-sensitive memory
change identity scope
open correct DB/key
resume appropriate sync
```

Exact logout retention/wipe policy waits for the real AuthN/security contract. Reusing one user's local data as another user's view is never acceptable.

## 16. Auth/session boundary

Frontend Foundation does not invent JWT/cookie/refresh-token/provider contracts before backend security design.

App-local adapters:

```text
apps/web/src/platform/session/
apps/mobile/src/platform/session/
```

Features consume session public capability, not storage mechanics.

`@dante/api-client` is auth-storage agnostic. Zustand is not session authority. Mobile sensitive credentials/tokens, if needed, use platform secure storage rather than ordinary plain/async storage.

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

DANTE UI layers shield features from low-level vendor primitives where practical.

```text
Web UI     → Radix / Tailwind / CSS vars / Motion / Lucide
Mobile UI  → RN primitives / StyleSheet / Reanimated / Gesture Handler / Lucide Native
```

## 18. Design-token authority

`@dante/design-tokens` owns one semantic token source and deterministic platform outputs.

```text
packages/design-tokens/
├── tokens/
│   ├── primitives.*
│   ├── semantic.*
│   └── platform overrides when justified
└── generated/
    ├── web.css
    └── native.ts
```

```text
shared semantic token
!=
identical pixel value Web/Mobile
```

Meaning is shared; platform representation may differ deliberately.

## 19. i18n ownership

`@dante/i18n` is framework-free.

It owns supported locales, resource contracts/resources, keys/types, fallback rules and common semantic messages.

It does not own React integration, `react-i18next` bootstrap, browser/native detection or persistence/storage.

Web/Mobile bootstrap wires React integration and platform detection/persistence. Core UX resources are bundle-available rather than network-required.

## 20. Time ownership

`@dante/time` is the semantic frontend time boundary and distinguishes Temporal concepts such as Instant, PlainDate, PlainTime, ZonedDateTime and Duration.

JavaScript `Date` is not the universal DANTE semantic time type. Transport strings are mapped at data boundaries, not parsed ad hoc in components.

## 21. Environment vocabulary

Frontend uses the existing DANTE vocabulary only:

```text
LOCAL
DEV
UAT
PROD
```

Tool-specific profile/channel names map to these contexts. No parallel permanent frontend environment taxonomy exists.

## 22. Web runtime public configuration

One immutable Web SPA artifact can be promoted across DEV/UAT/PROD where the delivery platform permits while environment-specific **public** configuration is supplied at runtime.

A bounded `/client-config` endpoint may be served by the app-coupled delivery Worker.

The config is versioned and validated before normal bootstrap.

Conceptual contract:

```text
schemaVersion
environment
apiBaseUrl
powerSyncEndpoint?   # only when activated
sentryDsn?           # public DSN when activated
release metadata
```

Rules:

- Zod validates the whole config;
- unsupported schema version fails clearly before normal operation;
- components do not read scattered `import.meta.env` config;
- client config is public and contains no secrets;
- delivery Worker has no business/API authority.

## 23. Mobile configuration and release activation

EAS technical profiles/channels map to DANTE LOCAL/DEV/UAT/PROD semantics.

```text
Android
SUPPORTED ARCHITECTURAL TARGET

iOS
SUPPORTED ARCHITECTURAL TARGET
```

Signed-build/device/store gates are mandatory when that platform is an activated release target. An inactive iOS release does not block a Web/Android release; activating iOS later requires no architectural rewrite.

EAS Update remains runtime-compatibility governed; OTA never delivers code incompatible with the installed native runtime.

## 24. Observability/error boundary

Sentry stays behind bootstrap/error-boundary/platform-observability integrations and a small set of authorized instrumentation points.

Feature UI consumes semantic errors rather than raw HTTP/PowerSync/vendor errors as its core contract.

Privacy defaults:

- minimize personal/sensitive payloads;
- no telemetry shadow personal-data store;
- Session Replay off until explicit privacy/product activation;
- source-map/release validation when Sentry activation becomes real.

## 25. Testing architecture

Unit/component tests are co-located with their owner where practical.

```text
Thing.ts
Thing.test.ts
Thing.tsx
Thing.test.tsx
Thing.stories.tsx
```

Application-level E2E lives at the app boundary:

```text
apps/web/tests/e2e/
apps/mobile/.maestro/
```

PR baseline progressively includes applicable lint/boundaries, strict typecheck, unit/component tests, generated drift, Storybook/a11y, critical Web E2E, mobile Jest/RNTL and Expo/tooling smoke checks.

Accepted-main/DEV/scheduled tiers add broader browser/integration/native/resilience checks when applicable.

UAT/release applies browser/release, signed build, device E2E, source-map/update compatibility and applicable security/privacy/performance/recovery gates for activated targets.

Cloud build success alone is not runtime QA.

## 26. CI/CD architecture

GitHub Actions remains repository-wide CI/CD authority.

Frontend workflow responsibilities are separated conceptually, e.g. quality, Web E2E, Mobile quality, contract/codegen, Web deployment and Mobile release. These labels are not pre-authorized required-check names.

A status check becomes required only after its real emitted context is observed and its failure genuinely must block merge.

Turbo orchestrates the JS/frontend task graph only, never backend/Python authority.

Remote Turbo cache stays dormant until measured benefit justifies it.

## 27. Developer topology

Preferred posture:

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

WSL↔Windows Metro/ADB mechanics are a tooling adapter, not product architecture. Adapt that bridge if direct evidence requires it without creating divergent Windows/WSL source trees.

Hard rule:

```text
one authoritative checkout
no divergent Windows + WSL source trees
no shared cross-OS node_modules environment
```

Activated iOS builds use an accepted macOS-capable/cloud path.

## 28. Direct-validation carry-forward

Passo 2 is design-complete. Validation remains for post-integration materialization.

At minimum validate progressively:

1. Node 24 + pnpm 11 + Turbo real workspace;
2. preferred isolated dependency layout with Expo/native graph;
3. hoisted fallback only if evidence requires it;
4. Vite/React production build;
5. Expo/RN build/runtime for activated mobile targets;
6. strict cross-package TypeScript;
7. package exports/public API enforcement;
8. ESLint dependency/cycle boundaries;
9. deterministic design-token generation;
10. real OpenAPI → Orval generation/compile when API exists;
11. TanStack Form pinned patch on Web + RN + Zod;
12. TanStack Query remote path;
13. PowerSync + OP-SQLite + SQLCipher encrypted lifecycle;
14. offline upload/accept/reject/conflict reconciliation;
15. identity-scoped local DB lifecycle;
16. WSL Metro ↔ Windows Android tooling;
17. versioned Web runtime config bootstrap;
18. Cloudflare Web delivery when activated;
19. selected Web/Mobile test stacks;
20. Sentry/EAS release integrations when activated.

A material failure reopens the affected technology/tooling adapter/boundary unless evidence demonstrates wider contradiction.

## 29. Passo-2 verdict

```text
PASSO 2
DESIGN COMPLETE / INTEGRATED VIA PR #22

REPOSITORY-LAYOUT CONSISTENCY      PASS
APPLICATION BOUNDARIES             ACCEPTED
FEATURE-FIRST ARCHITECTURE         ACCEPTED
DEPENDENCY DIRECTION               ACCEPTED
PUBLIC-API-ONLY RULE               ACCEPTED
FEATURE CYCLES                     FORBIDDEN
SHARED-PACKAGE POLICY              ACCEPTED
DATA AUTHORITY MATRIX              ACCEPTED
API/CODEGEN BOUNDARY               ACCEPTED
POWERSYNC OWNERSHIP                ACCEPTED
WEB ONLINE-FIRST / PWA DORMANT     ACCEPTED
CONFIG/ENVIRONMENT MODEL           ACCEPTED
UI/TOKEN/I18N/TIME BOUNDARIES      ACCEPTED
TEST/CI/RELEASE ARCHITECTURE       ACCEPTED
DEVELOPER POSTURE                  SELECTED / VALIDATION REQUIRED

PRODUCTION CODE                    NOT STARTED
SCAFFOLD                           NOT STARTED
DEPENDENCIES INSTALLED             NO
DIRECT VALIDATION                  NOT STARTED
```

The next boundary is a fresh bounded frontend materialization/scaffold/direct-validation workstream. No additional general architecture-selection pass is required unless concrete contradictory evidence or a materially changed requirement appears.
