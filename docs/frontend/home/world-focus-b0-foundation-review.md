# DANTE — World Focus B0 Foundation Review

**Status:** ACTIVE B0 ARCHITECTURE DECISION RECORD  
**Date:** 2026-09-01  
**Branch:** `feature/home-react`  
**Consumes:** `world-focus-platform-contract.md`, `world-focus-delivery-methodology.md`, current frontend production-readiness contracts, current code, current DANTE Product/Domain/Logical/Physical/Database authorities, scenario simulations and current Intelligence Platform direction.

---

# 1. B0 objective

B0 builds the **shared production foundation** that every later World Focus mini-vertical will consume.

It must make later work easier without pre-building later features.

B0 is successful when future blocks can independently add World Lens, projections, modules, composition, Adaptive, Insight, DANTE and customization without:

- putting more global lifecycle into `WorldFocusPage`;
- introducing page-per-World branches;
- inventing a new state/store architecture;
- bypassing feature/public API boundaries;
- adding ad-hoc fetch/provider/database calls;
- inventing persistence semantics;
- duplicating error/loading/race behavior;
- changing frozen shell/geometry;
- introducing a second Intelligence architecture.

---

# 2. Current repository baseline

Current web stack is already strong and should be extended, not replaced:

```text
React 19.2.x
TanStack Router 1.170.x
Vite 8.2.x
TypeScript 6.0.x
ESLint 10.x
eslint-plugin-react-hooks 7.x
Vitest 4.x
Playwright 1.62.x
axe Playwright integration
Turbo
pnpm 11.x
Dependency Cruiser
```

The root TypeScript contract already enables:

```text
strict
noUncheckedIndexedAccess
exactOptionalPropertyTypes
noImplicitOverride
noFallthroughCasesInSwitch
useUnknownInCatchVariables
isolatedModules
verbatimModuleSyntax
```

Existing Dependency Cruiser already enforces:

- no unresolved production imports;
- no circular frontend/shared-package dependencies;
- route -> feature only through public entrypoints;
- web/mobile sibling isolation;
- shared package -> app prohibition;
- production -> prototype prohibition;
- framework-free shared core packages.

Frontend CI already runs contract drift guards, format, lint, typecheck, architecture checks, generated-source checks, tests, production build, E2E, Firefox-sensitive Timeline coverage and mobile-bundle checks.

**Decision:** B0 does not create a second quality/tooling stack.

---

# 3. Current World Focus code baseline

Current feature boundary:

```text
apps/web/src/features/world-focus/
├── index.ts
├── model/
│   ├── fixtures
│   ├── geometry
│   ├── motion preference
│   ├── structure
│   ├── transition
│   └── visual version
└── ui/
    ├── WorldFocusPage
    ├── visual frame / VFX code
    └── CSS
```

This was appropriate for WF1 shell/visual work.

Current `WorldFocusPage` directly owns:

- entry snapshot reading/clearing;
- focus entry/restoration;
- document Escape listener;
- shell state rendering;
- frozen geometry CSS variables;
- visual frame mounting;
- workspace mounting.

The route correctly consumes the feature only through `features/world-focus/index.ts`.

**Finding:** the current page is not yet problematic, but it must not become the owner of future data, composition, AI, adaptive, module and customization state.

---

# 4. B0 architecture target

Feature-local target, introduced only as code becomes real:

```text
world-focus/
├── index.ts                 public feature API
├── model/                   pure feature semantics/config/state primitives
├── application/             use-case/port/orchestration boundary
└── ui/                      React rendering and browser interaction
```

Do **not** create a generic `runtime/`, `manager/`, `services/`, `core/`, `infrastructure/` forest.

Additional directories are justified later only by real code pressure.

## Layer rules

```text
model
  -> no ui
  -> no route
  -> no React/browser dependency unless the semantic object is explicitly web-only

application
  -> may depend on model
  -> no ui
  -> no route
  -> no DOM rendering concerns

ui
  -> may depend on model/application
  -> owns React/browser presentation concerns

route
  -> consumes only public feature API
```

Fixtures remain development/test adapters, not production source semantics.

---

# 5. Shared package vs feature-local code

## Options

### A — create `packages/world-focus-core` now

Possible benefit:

- future Web/Mobile semantic reuse.

Risks:

- prematurely freeze a web-derived view model as cross-platform truth;
- shared package starts accumulating feature-specific presentation semantics;
- mobile may require different composition and interaction projections;
- creates public package API migration cost before the contracts are validated.

### B — keep B0/B1… contracts feature-local until reuse is proven

Benefits:

- faster contract evolution during pre-backend validation;
- no accidental claim that web view models are canonical/cross-platform;
- extraction remains mechanically easy if pure modules and public boundaries stay clean.

**Decision: B.**

Do not create a World Focus shared package in B0.

### Re-evaluation trigger

Extract only when:

1. Mobile or another deployable needs the **same semantic contract**, not merely something similar; and
2. at least one stable contract has survived real Web implementation; and
3. extraction does not force React/DOM assumptions into shared code.

---

# 6. State-management technology review

## Candidate: React local state/reducers

Strengths:

- already present;
- no runtime/dependency cost;
- narrow ownership;
- integrates naturally with feature components;
- adequate for independent state domains.

## Candidate: Zustand/Jotai/Redux

Potentially useful when:

- cross-tree transient state has many independent writers/readers;
- route-independent state must survive broad component movement;
- measured Context/reducer topology becomes structurally awkward.

Current B0 evidence does not show this need.

## Candidate: XState

Strong for explicit complex workflow/statecharts, but current platform contract deliberately has **orthogonal state domains**, not one giant state machine.

Adding XState now would increase abstraction before a real block proves enough transition complexity to justify it.

**Decision:** no state-management dependency in B0.

Use feature-local state/reducer primitives. Re-evaluate by block when a real state domain becomes difficult to express/test.

---

# 7. TanStack Router review

Current TanStack Router provides:

- typed route params/search;
- route loaders;
- parallel loading;
- preload by intent/viewport/render;
- SWR-style route cache;
- loader cancellation via `AbortController`;
- deferred data;
- pending/error/not-found boundaries;
- automatic route code splitting.

Its own documentation explicitly positions the built-in cache as sufficient for many small/medium route-oriented cases and recommends an external cache such as TanStack Query when cross-route shared identity, advanced mutation and fine-grained invalidation become real needs.

**Decision:** keep TanStack Router as route/load coordinator.

Do not add TanStack Query in B0.

### Re-evaluation trigger

Real backend work demonstrates one or more of:

- important cross-route shared server-state identity;
- fine-grained invalidation;
- mutation cache coordination;
- optimistic server-state coordination;
- long-lived dedupe outside route ownership.

---

# 8. Runtime validation review

The frontend/backend integration contract requires runtime validation at untrusted boundaries.

Current B0 has no real network/provider boundary.

Current ecosystem candidates include:

- Zod 4 — mature, broad ecosystem, zero dependencies, strong DX;
- Valibot — modular/tree-shakeable, very small client bundle;
- ArkType — strong type/runtime model and high claimed runtime performance;
- generated contract validation from future API/OpenAPI tooling.

## Risk of choosing now

A manual schema library selected before the real API contract may duplicate or conflict with future generated client validation.

**Decision:** do not add a runtime schema dependency in B0.

Establish the boundary rule instead:

```text
unknown external/transport payload
-> adapter-owned runtime validation
-> validated frontend application projection
-> World Focus application/UI
```

The eventual validator is an adapter implementation detail unless a real cross-feature standard is deliberately selected later.

### Re-evaluation trigger

First real untrusted transport/config boundary or a backend-generated client architecture decision.

---

# 9. React Compiler 2026 review

React Compiler 1.x is stable and production-ready. React recommends incremental adoption for existing codebases and new applications can start with it enabled.

Potential World Focus benefits:

- automatic memoization;
- less manual `useMemo` / `useCallback` / `React.memo` maintenance;
- useful for future module-heavy/dense surfaces;
- compiler-powered linting already aligns with strong Rules-of-React discipline.

Current repository facts:

- React 19.2;
- `eslint-plugin-react-hooks` already current and recommended preset is active;
- Vite uses `@vitejs/plugin-react@6`, whose current React Compiler integration requires an additional Babel/Rolldown plugin path rather than the old inline `babel` option.

Risks:

- additional build transform/dependency;
- existing codebase is not currently compiled;
- compiler changes can expose latent Effect/memoization assumptions;
- benefit must be measured against build cost and actual rerender pressure.

**Decision:** React Compiler is a **B0 production experiment candidate**, not yet a mandatory foundation dependency.

B0 will first establish architecture/test baselines. Then run a bounded World-Focus-only compiler experiment with:

```text
exact compiler/tool versions
world-focus-only or explicit opt-in scope
full unit/E2E/build gates
bundle/build-time comparison
representative rerender/performance comparison
```

Enable it only if behavior remains green and the operational trade-off is favorable.

Do not switch the whole application as a side effect of World Focus work.

---

# 10. React 19.2 Activity review

`<Activity>` is stable in React 19.2 and can preserve hidden UI state while hidden Effects are unmounted/deprioritized.

Potential future uses:

- preserving an expensive Explore/side surface;
- pre-rendering likely next UI;
- restoring transient state.

**Decision:** not a B0 primitive.

No current hidden World Focus subtree has proven the need. Evaluate in B7/B8 against real Peek/Insight/Explore behavior and memory cost.

---

# 11. View Transition technology review

React's `<ViewTransition>` wrapper remains Canary/Experimental.

The browser View Transition API may be useful for future route/visual work, but VFX/entry visual work is explicitly deferred and not part of B0.

**Decision:** no React Canary dependency and no B0 architecture coupled to ViewTransition.

Future visual work may evaluate stable browser-native APIs behind progressive enhancement.

---

# 12. CSS/layout technology review

Preferred foundation:

```text
CSS Grid / Flex
container queries
logical properties
native overflow/scroll behavior
CSS custom properties/tokens
```

No grid-layout/dashboard library in B0.

Reasons:

- current platform contract intentionally avoids free coordinates;
- native layout is smaller, more maintainable and easier to make responsive/accessibility-safe;
- container queries map directly to module presentation based on real allocated space.

`react-grid-layout` or equivalent is re-evaluated only if a validated customization design requires arbitrary 2D dragging/resizing that bounded profiles cannot represent.

---

# 13. Time/Temporal technology review

Native JavaScript `Temporal` remains limited-availability across widely used browsers as of the B0 review.

DANTE already owns `@dante/time`, backed by `temporal-polyfill`, with typed Instant/PlainDate/PlainTime/PlainDateTime/ZonedDateTime/Duration primitives.

**Decision:** World Focus consumes `@dante/time` where time semantics become necessary.

Do not use ad-hoc `Date` parsing or directly depend on native `Temporal` availability.

This preserves Web/Mobile consistency and future migration when native support becomes universal.

---

# 14. Error-boundary strategy

TanStack Router already provides route-level `errorComponent`/CatchBoundary behavior and reset semantics.

React still requires an Error Boundary for isolated rendering failures below the route level.

B0 distinction:

```text
route/page failure
-> TanStack Router route boundary

future module/specialist render failure
-> feature-local module boundary (B3)

future transient Insight render failure
-> interaction-surface boundary when justified (B7)
```

**Decision:** do not add `react-error-boundary` or another dependency in B0 solely for future component boundaries.

Use TanStack Router at route level. Implement the smallest local React boundary when B3 proves the module-host contract.

---

# 15. Async/concurrency foundation

Permanent B0 rules:

- route/application work accepts cancellation where semantics support it;
- stale results never overwrite newer World/Lens/request generations;
- obsolete read work is cancelable;
- durable Intelligence/effect execution lifetime is not equated with React component lifetime;
- no retry loop without operation-specific policy;
- no component performs raw provider/database calls.

Do not create a generic async framework in B0.

The first concrete request-generation helper belongs with B2, when the data/projection adapter exists and can be tested against real race scenarios.

---

# 16. Feature availability / rollout foundation

B0 does not select a feature-flag vendor.

Future availability must be represented as validated capability/configuration availability, not scattered `if (worldName === ...)` branches.

Saved configuration for a disabled capability is not silently deleted.

A future central product feature-flag system can feed the same availability boundary.

No generic flag service is implemented until the app has a real flagging requirement.

---

# 17. Security/rich-content foundation

B0 default rendering policy:

```text
text is text
URLs are untrusted until validated
no arbitrary HTML
no model/provider JSX
no arbitrary iframe/embed
no executable URL scheme
no sensitive payload logging
```

Do not add an HTML sanitizer library while there is no accepted rich-text requirement.

When rich text becomes real, select an allowed grammar and sanitizer/rendering strategy from the actual content source and CSP model.

---

# 18. Localization/time/unit foundation

Use existing shared packages:

```text
@dante/i18n
@dante/time
@dante/design-tokens
```

Do not persist translated labels as identity.

Do not pre-format semantically important numeric/time values too early.

Unit/currency formatting rules are defined by the module/projection blocks that first need them, using typed values rather than arbitrary display strings.

---

# 19. Observability/performance instrumentation foundation

Do not add an observability vendor/SDK in B0.

The browser Performance/User Timing APIs are sufficient for local/product-specific marks when actual measurable paths exist.

Future production telemetry can attach at explicit seams without changing component ownership.

Potential future measurements remain:

```text
route -> usable
critical projection latency
module lazy load
Insight first response / completion
customization latency
long tasks
resource/memory cleanup
```

No event-name registry or telemetry service is implemented until at least one consumer exists.

---

# 20. Accessibility foundation

B0 preserves WCAG 2.2 AA as a non-negotiable platform target.

B0 infrastructure must not make later accessibility hard:

- DOM order follows reading order;
- transient surfaces cannot require pointer-only navigation;
- future drag gets a non-drag operation;
- focus ownership remains explicit;
- reduced motion is maintained;
- no visual-only state semantics;
- container-responsive layout must survive zoom/text pressure.

The existing axe/Playwright infrastructure remains the base.

---

# 21. Mobile/future platform compatibility

Mobile already exists as a sibling deployable with explicit Web/Mobile source isolation.

B0 therefore does not create Web->Mobile or Mobile->Web source dependencies.

World Focus product semantics remain cross-platform-capable, but Web view models and React DOM behavior are not promoted to universal contracts without evidence.

Future shared extraction follows the trigger in section 5.

---

# 22. Database/Domain/Intelligence boundaries carried into B0

B0 cannot introduce:

- canonical `World` owner;
- `WorldItem` universal entity;
- speculative `world_id` on canonical tables;
- direct SQL/provider access;
- frontend authorization semantics;
- frontend inference that absence means false;
- new AI orchestration/control plane.

Current World Focus remains a product/application projection over accepted DANTE realities.

The future Intelligence platform owns model/provider routing, context reconstruction, governance, effect authorization, durable execution and audit.

World Focus owns context selection/presentation only.

---

# 23. B0 code-architecture guard decisions

Add World-Focus-specific Dependency Cruiser guards before later directories expand.

Required guards:

```text
world-focus model -> no world-focus ui
world-focus application -> no world-focus ui
world-focus model/application -> no app routes
world-focus -> no Home internals
other features -> world-focus only through public index when crossing feature boundary
```

Keep the existing route -> feature public-API rule.

Do not introduce global rules that affect unrelated features without first auditing them.

---

# 24. B0 sub-blocks

## B0.1 — Ownership and dependency guards

Implement:

- internal layer boundary rules in Dependency Cruiser;
- explicit no Home-internals dependency;
- cross-feature public-entry guard for World Focus;
- architecture regression evidence.

No product behavior changes.

## B0.2 — Route/page production boundary

Review/implement only foundational route-level concerns that are already justified:

- route error boundary behavior;
- not-found/unavailable semantics appropriate to current fixture phase;
- no duplication with future module boundaries;
- preserve frozen entry/close/focus contract.

No projection loader yet.

## B0.3 — Foundation test harness

Establish B0-level tests for:

- public boundary;
- architectural invariants;
- shell survives route-level failure fallback where testable;
- no regression of current World Focus shell contract.

Do not create giant fixture factories before B2/B3 need them.

## B0.4 — React Compiler / build-performance experiment

After B0.1–B0.3 green:

- exact-pinned compiler integration candidate;
- compile World Focus only or explicit opt-in;
- compare build/bundle/test/runtime behavior;
- adopt or reject with recorded evidence.

## B0.5 — B0 final gate

Run relevant full frontend CI and review:

```text
format
lint
typecheck
architecture
generated checks
unit/component tests
production build
web E2E
mobile compatibility/bundle
```

Then freeze B0 foundation decisions before B1.

---

# 25. B0 explicit non-goals

B0 does **not** implement:

```text
World Lens semantics
real World Session state
projection/data adapter
ModuleConfig / ModuleProjection schema
module registry/host behavior
Initial Composition Resolver
Adaptive ranking/display
universal module components
Peek/Insight/Explore UX
real DANTE streaming
Customize UX
real persistence
real API/backend
DB/Alembic
final VFX
```

Those are later mini-verticals.

---

# 26. External evidence snapshot — 2026-09-01

## React Compiler

Stable 1.x, production-ready, official incremental-adoption guidance. Candidate for measured B0 experiment rather than automatic whole-app enablement.

Official sources:

- `https://react.dev/blog/2025/10/07/react-compiler-1`
- `https://react.dev/learn/react-compiler/incremental-adoption`
- `https://react.dev/learn/react-compiler/installation`

## React 19.2 Activity

Stable and useful for preserving hidden state/pre-rendering; defer until a real transient-surface requirement exists.

- `https://react.dev/reference/react/Activity`

## React ViewTransition

React wrapper remains Canary. Reject as B0 production foundation.

- `https://react.dev/reference/react/ViewTransition`

## TanStack Router

Current loaders support parallel loading, cache/preload, cancellation, deferred work, route error boundaries and automatic code splitting.

- `https://tanstack.com/router/latest/docs/guide/data-loading`
- `https://tanstack.com/router/latest/docs/guide/preloading`

## Runtime validation

Current mature options include Zod 4, Valibot and ArkType. No library is selected before the real transport contract.

- `https://zod.dev/`
- `https://valibot.dev/`
- `https://arktype.io/`

## Temporal

Native Temporal remains limited availability, while DANTE already owns a Temporal polyfill abstraction.

- `https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Temporal`

## Accessibility

WCAG 2.2 AA continues to require non-drag alternatives and minimum pointer target behavior.

- `https://www.w3.org/TR/WCAG22/`

---

# 27. B0 exit criteria

B0 passes only when:

1. World Focus internal ownership/layer direction is explicit;
2. dependency guards prevent the most dangerous future coupling;
3. current frozen World Focus shell remains behaviorally unchanged;
4. route-level failure ownership is explicit and production-safe;
5. no unnecessary state/data/schema/layout dependency has been introduced;
6. React Compiler has been measured and deliberately adopted or rejected/deferred;
7. existing TypeScript/CI/architecture infrastructure remains green;
8. no Home/Access/AppShell/DB/Domain/Intelligence boundary was reopened;
9. later B1–B9 work has clear extension seams without placeholder managers/services;
10. B0 documentation records re-evaluation triggers rather than making technology choices permanent without evidence.

Only then begin B1.
