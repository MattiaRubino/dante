# DANTE — World Focus B0 Foundation Review

**Status:** B0 IMPLEMENTATION CANDIDATE — AWAITING FULL GATES  
**Date:** 2026-09-01  
**Branch:** `feature/home-react`  
**Scope:** one complete production-depth World Focus foundation block. No B0 sub-blocks exist. Real backend/API/database/provider/LLM integration remains explicitly out of scope until the final vertical.

---

# 1. B0 objective

B0 establishes the common production foundation that every later World Focus mini-vertical consumes.

The rule is:

> Build the difficult reusable infrastructure now; defer only the business/product semantics that cannot be truthfully implemented before their mini-vertical or before the real backend exists.

B0 is not a visual prototype phase and is not a partial scaffolding pass.

Later mini-verticals must be able to add World Lens, real projections, module families, stable composition, Adaptive, Peek/Insight/Explore, DANTE and customization without reopening foundational ownership, async, validation, security, failure, performance or accessibility architecture.

The only material infrastructure intentionally not implemented is infrastructure that would be fake without a real backend or a real consumer, for example:

- HTTP/API contracts;
- backend-generated runtime schemas;
- DB/Alembic/persistence tables;
- provider SDKs;
- real DANTE Intelligence transport/streaming;
- cross-device sync;
- vendor feature-flag/observability SDKs.

Their seams are preserved now.

---

# 2. Authorities consumed

B0 consumes and does not redefine:

- Product Identity / North Star;
- product discovery simulations;
- multi-actor/collaboration simulation;
- adaptive intelligence / future social direction;
- closed Domain, Logical and Physical authorities;
- current Database/Alembic source of record;
- frontend component architecture;
- frontend/backend integration contract;
- frontend quality gates;
- frozen Home/AppShell boundaries;
- World Focus architecture, scenario oracle, structural contract and WF-G3 geometry;
- `world-focus-platform-contract.md`;
- `world-focus-delivery-methodology.md`;
- current DANTE Intelligence Platform direction.

Permanent consequences:

```text
World != canonical Domain owner
World Focus != DB ontology
frontend projection != canonical truth
AI output != accepted fact
provider state != canonical state
planned != actual
observation != causation
absence != false
UI hiding != authorization
```

No B0 code may create a shortcut around these rules.

---

# 3. Repository and stack baseline

The repository already has an enterprise-grade frontend baseline and B0 extends it rather than replacing it.

Current relevant stack:

```text
React 19.2.x
React DOM 19.2.x
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
@dante/design-tokens
@dante/i18n
@dante/time
```

The root TypeScript contract already enables strictness including:

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

Decision: **no replacement framework and no duplicate tooling stack.**

---

# 4. Feature ownership

Current and target feature-local shape:

```text
apps/web/src/features/world-focus/
├── index.ts
├── model/
├── application/
└── ui/
```

This is deliberately small.

Do not create speculative forests such as:

```text
runtime/
managers/
services/
infrastructure/
core/
plugin-system/
```

without a real future pressure that proves a distinct owner is required.

Layer direction:

```text
model
  -> pure feature semantics/primitives
  -> no UI/application/routes dependency

application
  -> may depend on model
  -> orchestration/boundary primitives
  -> no UI/routes dependency

ui
  -> React/browser presentation
  -> may consume model/application

route
  -> consumes World Focus through public feature API
```

World Focus is a sibling of Home, not a child that may import Home internals.

Dependency Cruiser already mechanically protects these boundaries.

---

# 5. Shared package decision

Do **not** create `packages/world-focus-core` in B0.

Reasons:

- current World Focus contracts are still being validated through the Web product;
- a Web view model must not accidentally become cross-platform canonical truth;
- Mobile may need different composition/presentation semantics;
- extraction is easy later if current model/application modules remain framework-independent.

Re-evaluate only when another deployable needs the **same stable semantic contract**, not merely a similar feature.

---

# 6. State-management decision

No Redux, Zustand, Jotai or XState dependency is added in B0.

The platform contract has several orthogonal state domains rather than one giant application state machine.

Use the narrowest correct owner:

- route state in TanStack Router;
- source-backed state in the future server-state/data layer;
- feature interaction state in local reducer/state primitives;
- transient rendering state locally;
- durable preferences only at an explicitly accepted persistence boundary.

Re-evaluate a state library only when a concrete mini-vertical produces enough independent cross-tree readers/writers or workflow complexity to prove the need.

---

# 7. TanStack Router decision

TanStack Router remains route/lifecycle/load coordinator.

Current official capabilities include:

- typed route/search state;
- parallel loaders;
- intent/viewport/render preloading;
- SWR-style route cache;
- abort signals for outdated loader work;
- deferred data;
- pending/error/not-found boundaries;
- automatic route code splitting.

Do not add TanStack Query in B0.

Re-evaluate with the real backend if World Focus proves it needs important cross-route shared server-state identity, fine-grained invalidation, optimistic cache coordination or long-lived deduplication beyond route ownership.

---

# 8. Runtime-validation foundation

Static TypeScript is not runtime validation.

B0 implements a validator-neutral untrusted-boundary seam:

```text
unknown external payload
-> adapter-owned validator
-> validated frontend application value
-> World Focus
```

The foundation exposes a `WorldFocusBoundaryValidator` / validation-result contract and a machine-identifiable `WorldFocusBoundaryValidationError` that does **not** echo rejected payload contents.

No schema dependency is selected before the real transport contract exists.

Current candidates remain Zod 4, Valibot, ArkType or generated validation from the future API contract.

Selection trigger: first real untrusted transport/configuration boundary or deliberate cross-app schema standard.

---

# 9. Async/concurrency foundation

B0 implements `WorldFocusLatestReadCoordinator` for frontend reads.

Permanent behavior:

```text
request A begins
request B supersedes A
-> A is aborted/invalidated
-> A can never commit into active World state
```

It also accepts an upstream `AbortSignal`, so a future TanStack loader/application lifecycle can cancel obsolete work cleanly.

`release()` marks completed read ownership finished without falsely representing successful completion as cancellation.

Critical distinction:

```text
obsolete frontend read lifetime
!= durable DANTE Intelligence/effect execution lifetime
```

Closing/unmounting a React surface must not implicitly cancel a future durable backend run unless explicit cancellation semantics exist.

No generic retry framework is created. Retry safety remains operation-specific.

---

# 10. Common platform primitives

B0 implements finite typed vocabularies for concepts already accepted by the Platform Contract:

```text
resource status:
loading / ready / empty / partial / stale / error / unavailable

composition stability:
stable / adaptive / ephemeral

composition origin:
system-default / user / dante-proposed / application-derived

interaction depth:
peek / insight / explore

presentation surface:
inline / popover / sidecar / modal / full-screen / route
```

Stability and origin are deliberately independent axes.

The feature-availability primitive distinguishes:

```text
available
disabled
unavailable
```

with machine reason codes and retryability where applicable.

This is the future rollout/kill-switch seam without selecting a feature-flag vendor.

B0 also defines a minimal generic versioned-payload shape without inventing the future layout/module persistence schema.

---

# 11. Safe-content/link foundation

B0 default policy:

```text
text is text
internal navigation uses the router
external URL text is untrusted
no arbitrary HTML/JSX/JavaScript
no arbitrary iframe/embed
no executable URL schemes
no credentials embedded in clickable external URLs
```

The implemented external-link parser accepts only absolute credential-free HTTPS URLs.

Unsafe/unsupported values remain non-clickable data rather than being “fixed” heuristically.

No HTML sanitizer dependency is added because World Focus has no accepted rich-HTML requirement. If rich text becomes real, define the allowed grammar first and then select the sanitizer/renderer against the real CSP/content source.

---

# 12. Error ownership and isolation

Failure boundaries are layered rather than duplicated everywhere.

```text
route/page rendering/loading failure
-> TanStack Router route errorComponent

future module/specialist rendering failure
-> feature-local WorldFocusRenderBoundary in ModuleHost

future Insight surface rendering failure
-> same local boundary pattern when that surface exists
```

B0 implements:

- a localized World Focus route failure surface;
- retry/reset behavior;
- a small feature-local React render boundary for later module/surface isolation.

Security rule: fallback UI does not receive raw error text by default. Operational details may go to a future reporting callback, not directly to user-visible copy.

The existing shell status semantics remain truthful:

```text
loading != error != unavailable
```

Later resource/module types may use the complete status vocabulary without forcing every state onto every component.

---

# 13. Workspace ownership and responsive foundation

`WorldFocusPage` remains the route-level shell/lifecycle owner.

B0 extracts a dedicated `WorldFocusWorkspace` owner for the frozen persistent rectangle.

This prevents future module/composition/Adaptive state from accumulating in `WorldFocusPage`.

The DOM/geometry contract remains unchanged:

```text
AppShell / Topbar
-> WorldFocus shell
   -> visual frame
   -> workspace
   -> shell controls
```

B0 establishes the workspace as a named `inline-size` CSS query container.

Future modules therefore adapt to the space **allocated to them**, not by duplicating viewport/device breakpoints in JavaScript.

No free-coordinate dashboard library is introduced.

Preferred future layout foundation remains CSS Grid/Flex + container queries + logical properties.

---

# 14. Performance/observability foundation

No telemetry vendor/SDK is added in B0.

B0 implements a vendor-neutral best-effort User Timing span and wires the current route to measure:

```text
dante.world-focus.open-to-usable
```

Instrumentation rules:

- timing only;
- no World payload/content in measurement names/details;
- measurement failure cannot break product behavior;
- operational telemetry remains distinct from authoritative audit.

Later mini-verticals may add metrics such as projection latency, lazy module load, Insight first response/completion and customize latency through the same ownership approach.

Performance budgets are measured before becoming blocking numeric product gates.

---

# 15. React Compiler decision

React Compiler 1.x is stable and production-ready, and official React guidance supports incremental adoption for existing applications.

B0 deliberately **does not enable it yet**.

Reason: the current World Focus shell is not representative of the future dense module/composition workload. Measuring Compiler value against an almost-empty workspace would create a false benchmark and an unnecessary build transform.

Re-evaluation trigger:

- first representative dense module composition exists;
- React Profiler/browser evidence shows meaningful rerender pressure;
- compiler can be enabled on a bounded scope and compared with real interaction/build data.

This is a completed B0 technology decision, not unfinished infrastructure.

---

# 16. React Activity / View Transition decision

React 19.2 `<Activity>` is stable but no current B0 hidden subtree proves its value. Re-evaluate for Peek/Insight/Explore state preservation and memory pressure.

React's `<ViewTransition>` component remains outside stable React production APIs; browser-native View Transition APIs are much more widely available, but final VFX/entry transitions are a separate product slice.

B0 does not couple the platform to either feature.

---

# 17. Time, locale and units

Use existing DANTE packages:

```text
@dante/i18n
@dante/time
@dante/design-tokens
```

`@dante/time` remains the application abstraction while native Temporal support is not universal.

Rules:

- stable identifiers are not translated labels;
- semantically meaningful numeric/time/unit values are not flattened to display strings prematurely;
- timezone/currency/unit formatting belongs at validated presentation boundaries;
- travel/cross-timezone cases remain mandatory later tests.

B0 does not invent module-specific value schemas before module verticals exist.

---

# 18. Accessibility foundation

Target remains WCAG 2.2 AA.

B0 adds/retains:

- explicit focus ownership/restoration on World entry/exit;
- keyboard Escape behavior;
- semantic main/workspace labeling;
- visible focus on the new route retry action;
- >=44px current retry target, exceeding WCAG 2.2 minimum target requirements;
- reduced-motion preservation;
- named container responsiveness that does not depend on pointer/device class;
- Playwright + axe regression coverage at wide and compact widths.

Later drag/customization features must provide non-drag alternatives.

Automated axe is necessary but remains complementary to manual keyboard/focus/reading-order review.

---

# 19. Mobile/future platform compatibility

Web and Mobile remain sibling deployables with source isolation.

B0 does not create Web -> Mobile or Mobile -> Web dependencies.

World Focus product semantics remain potentially reusable, but Web DOM/view-model decisions are not promoted to shared canonical contracts before Mobile proves identical needs.

---

# 20. Database / Domain / Intelligence boundary

B0 introduces no backend or persistence semantics.

Forbidden:

```text
canonical World table by implication
WorldItem universal entity
world_id added to canonical owners
frontend SQL/provider access
frontend authorization logic
frontend absence=false coercion
World-Focus-specific LLM orchestration/control plane
```

The future backend remains authoritative for canonical state, disclosure and effects.

The future DANTE Intelligence Platform owns context reconstruction, provider/model routing, governance, capability/tool/effect execution, durable runs and audit.

World Focus will later provide bounded context and presentation adapters only.

---

# 21. Dependencies deliberately not added

B0 adds no new runtime/dev dependency for the platform foundation.

Not added:

```text
XState
Redux / Zustand / Jotai
TanStack Query
react-grid-layout
Zod / Valibot / ArkType yet
react-error-boundary
React Compiler transform yet
feature-flag vendor
observability vendor
HTML sanitizer
runtime plugin loader
generic event bus
generic DI/service locator
```

Each remains eligible only after a concrete requirement proves a net benefit.

---

# 22. Implemented B0 foundation inventory

```text
model/world-focus-platform.ts
  finite shared status vocabulary
  stable/adaptive/ephemeral axis
  origin axis
  interaction-depth/presentation-surface axes
  feature availability seam
  versioned-payload seam
  safe external HTTPS parsing

application/world-focus-foundation.ts
  runtime-validation seam
  non-leaking validation error
  latest-read coordinator
  upstream cancellation integration
  stale-commit prevention
  vendor-neutral User Timing span

ui/world-focus-render-boundary.tsx
  local render isolation primitive
  reset-key behavior
  no raw error leakage to fallback UI

ui/world-focus-workspace.tsx
  persistent workspace ownership seam

ui/world-focus-route-error.tsx
  localized safe route failure + retry

WorldFocusPage
  workspace delegation
  open-to-usable instrumentation

route
  route-level error ownership

CSS
  named inline-size query container
  accessible route-failure treatment
```

Tests cover platform primitives, safe URLs, validation, race invalidation, upstream abort, release semantics, non-blocking instrumentation, render isolation, localized route retry, current shell behavior, container-query readiness, User Timing and axe pressure.

---

# 23. What remains correctly outside B0

The following are **not missing foundation work**. They are product/function verticals whose concrete semantics must be re-researched and implemented one by one:

```text
World Session and real World Lens behavior
real projection/data-source contracts and deterministic scenario adapter
ModuleConfig / ModuleProjection contracts for real module families
ModuleHost/Registry dispatch behavior for real renderers
Initial Composition Resolver
stable composition product behavior
Adaptive ranking/hysteresis/dismissal product behavior
metric/trend/etc module verticals
Peek / Insight / Explore UX
real DANTE context/result/stream integration
Insight promotion
Customize behavior
specialist module verticals
```

They must consume B0 rather than recreate it.

The real backend/API/DB/provider/LLM work remains the final vertical after frontend/product behavior is proven.

---

# 24. External evidence snapshot — 2026-09-01

Current official evidence reviewed for B0 includes:

- React Compiler 1.0 production-ready + incremental adoption guidance;
- TanStack Router current data-loading/preload/cache/cancellation/error-boundary documentation;
- MDN container queries as widely available platform capability;
- browser View Transition API as Baseline 2025 while React wrapper remains outside stable React;
- Zod 4 and Valibot current runtime-validation trade-offs;
- WCAG 2.2;
- existing DANTE TypeScript, i18n/time, test and architecture tooling.

Principle: external products/frameworks inform DANTE-specific decisions; they are not copied as architecture.

---

# 25. B0 gate / exit criteria

B0 closes only when all of the following are true:

1. `model -> application -> ui -> route` dependency direction remains enforceable;
2. World Focus remains isolated from Home internals;
3. common accepted platform vocabularies are finite and typed;
4. unsafe external URLs fail closed;
5. unknown boundary payloads have a runtime-validation seam without library lock-in;
6. superseded/upstream-aborted reads cannot commit;
7. read cancellation is not confused with durable Intelligence execution;
8. route-level rendering failures have a safe localized retry surface;
9. local future module/surface failures have a reusable error-isolation primitive;
10. `WorldFocusPage` is not the future composition/data/AI state dumping ground;
11. workspace is ready for container-based module responsiveness without changing WF-G3 geometry;
12. basic timing instrumentation is measurable and non-blocking;
13. World Focus passes automated accessibility pressure at wide and compact widths;
14. current Home/World Focus navigation, focus, VFX boundary and geometry regressions remain green;
15. format/lint/typecheck/architecture/generated/unit/build/E2E relevant gates pass;
16. no new dependency lacks a proven requirement;
17. no real backend/DB/provider/LLM behavior has been faked;
18. documentation records explicit technology re-evaluation triggers.

Until these gates actually pass, B0 remains **IMPLEMENTATION CANDIDATE**, not CLOSED.
