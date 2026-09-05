# DANTE — World Focus Frontend Architecture

**Status:** CURRENT WORKING ARCHITECTURE CONTRACT — PRE-BACKEND  
**Date:** 2026-08-30  
**Branch:** `feature/home-react`  
**Scope:** World Focus application/frontend architecture up to, but not including, real backend/API/database/provider/LLM integration

This document defines the frontend/system architecture that the World Focus implementation must preserve. It is intentionally stricter than a prototype note: it exists to prevent a visually successful surface from accumulating hidden structural debt.

It does **not** redefine Domain, Logical, Physical or Database semantics.

---

# 1. Architecture thesis

World Focus is a reusable application surface for understanding one significant World without collapsing heterogeneous DANTE realities into a new generic entity.

The architecture must support radically different Worlds while keeping one coherent platform capability.

```text
World Focus
= stable application shell
+ controlled dynamic composition
+ typed module registry
+ contextual DANTE AI
+ typed ephemeral insight surfaces
+ user-owned personalization
```

The design goal is not maximum abstraction. The goal is a small set of explicit ownership boundaries that remain valid as World Focus grows.

---

# 2. Non-negotiable semantic boundaries

```text
World != canonical Domain owner
WorldProjection != canonical truth
World widget != canonical source record
World layout != Domain semantics
AI suggestion != accepted state
AI insight != evidence of truth by itself
frontend state != backend accepted effect
provider state != DANTE canonical state
absence != false
```

World Focus may display or compose projections over existing canonical and derived realities, but presentation convenience must never mutate semantic ownership.

The frontend must preserve provenance/freshness/uncertainty whenever the source contract says those facts matter.

---

# 3. Top-level component / capability ownership

Target conceptual structure:

```text
WorldFocusFeature
├── WorldFocusEntry
├── WorldFocusShell
│   ├── WorldIdentityLayer
│   ├── WorldEnterTransition
│   ├── WorldFocusNavigation
│   └── WorldFocusActions
├── WorldCompositionCanvas
│   ├── WorldModuleHost[*]
│   └── WorldModuleRegistry
├── WorldAISurface
├── WorldInsightLayer
│   ├── PeekSurface
│   ├── InsightSurface
│   └── ExploreSurface
├── WorldCustomizeMode
└── application/
    ├── contracts
    ├── state/reducer or equivalent explicit transition ownership
    ├── ports
    ├── local deterministic adapter
    └── scenario fixtures
```

This is an ownership model, not a demand for one file per box.

---

# 4. WorldFocusFeature ownership

Owns:

- route/application entry and exit semantics;
- current World focus identity at the frontend projection level;
- shell-level async state;
- orchestration between composition canvas, AI and insight layer;
- explicit entry source where relevant for back/focus restoration;
- coordination of customization mode;
- top-level error boundary;
- page-level telemetry hooks when later activated.

Must not own:

- direct database knowledge;
- provider SDK calls;
- arbitrary per-World page branches;
- module-specific rendering logic;
- backend authorization decisions.

---

# 5. Navigation / lifecycle contract

World Focus must behave like a real application destination even when entered through an immersive transition.

Required behavior:

- browser back is meaningful;
- refresh/deep-link must have a defined outcome once route-backed implementation lands;
- closing/back must restore the originating application context where possible;
- Home entry must preserve the centered World and Home interaction state rather than rebuilding an unrelated default Home;
- entry from Mondi Overview later returns to Mondi Overview;
- Search/AI entry may have different return source but uses the same World Focus surface.

Do not make route state the source of Domain semantics. Route state is navigation state only.

Exact URL naming remains an implementation design gate.

---

# 6. Transition architecture

One shared `WorldEnterTransition` implementation owns the “enter the World” visual grammar.

A World may provide a bounded theme profile, conceptually:

```text
WorldThemeProfile
- accent role
- ambient intensity
- orbital density
- particle density
- motion character
- texture key from approved catalog
```

The profile is declarative configuration, not executable custom animation code.

Rules:

- animate transform/opacity where possible;
- shared-element geometry should come from the real opener bounds, not hard-coded screen coordinates;
- transition cannot own page data loading truth;
- shell must remain usable if rich effects are disabled;
- no separate WebGL scene per World;
- no effect that blocks navigation completion on slow devices;
- reduced motion bypasses ornamental movement while preserving orientation.

Animation quality is a product layer over correct navigation, never a dependency for correctness.

---

# 7. Projection contracts

The pre-backend frontend should establish stable internal view contracts without pretending they are final backend DTOs.

## 7.1 WorldFocusProjection

Conceptual responsibilities:

```text
WorldFocusProjection
- world presentation identity
- projection status
- composition definition
- module projections
- contextual capabilities available to the frontend
- provenance/freshness summary where relevant
```

It must not expose persistence-row shapes.

## 7.2 WorldModuleProjection

Every rendered module instance must have at least conceptually:

```text
instanceId
kind
status
presentation profile / supported size
validated payload owned by module kind
available frontend semantic intents
data freshness/provenance when applicable
```

`kind` selects an approved registered renderer. It never names arbitrary code supplied by an LLM or remote payload.

## 7.3 WorldLayoutProjection

The layout contract represents presentation configuration only.

Conceptual fields may include:

```text
layout version
module instance ordering/placement
size/profile
pinned state
section/group placement if justified
```

Do not freeze the exact persistence schema during this phase.

## 7.4 InsightProjection

A conversational/AI visual answer uses a typed projection such as:

```text
insight identity for UI lifecycle
presentation kind
scope/time range
validated series/breakdown/value data
source/provenance/freshness
available next interactions
promotable-to-widget flag only when justified
```

The exact union is derived during roadmap scenario work.

---

# 8. Module Registry

The module system is the critical extensibility boundary.

A module registration should conceptually define:

```text
kind
projection validator/schema
renderer
supported presentation sizes
allowed semantic intents
loading/empty/partial/stale/error behavior
a11y behavior
optional lazy loader
```

Registry rules:

- finite approved kinds;
- deterministic lookup;
- unknown kind fails safely and visibly in development/telemetry, never executes remote code;
- module code cannot reach unrelated feature internals;
- specialist modules can be lazy loaded;
- registry itself must not become a service locator for arbitrary application dependencies.

Avoid a single `WorldModule` component with hundreds of optional fields and `switch` logic containing all specialist behavior.

A thin dispatch layer over independently owned module families is preferred.

---

# 9. Universal vs specialist modules

A module is **universal/general** when the visual grammar is semantically useful across many Worlds, e.g. a value+delta, bounded trend, comparison, timeline projection or item list.

A module is **specialist** when the domain/product reality genuinely needs a richer interaction/visual model that would be misleading or materially weaker as a generic module.

Examples that may justify future specialist modules after validation:

```text
travel itinerary
release pipeline
training/workout execution
```

Do not create specialist modules merely because a World has a different color/name.

The scenario gate must prove the need.

---

# 10. Composition engine

The composition engine owns how approved module instances are arranged inside the World Focus canvas.

It must not infer Domain meaning from labels or IDs.

Inputs:

```text
validated composition/layout projection
registered module capabilities
real container geometry
responsive rules
customization state
```

Outputs:

```text
stable deterministic module placement
```

Required properties:

- same input => deterministic layout;
- no dependence on global viewport hacks when container geometry is the owner;
- responsive transitions are reversible;
- stable pinned content does not arbitrarily move because adaptive content changed;
- adaptive content has a bounded region/grammar rather than taking over the user layout;
- ephemeral insight surfaces do not permanently mutate layout unless explicitly promoted.

Do not build a generic website-layout engine unless real product behavior proves it necessary.

---

# 11. Personalization model

World Focus separates three ownership classes.

## PINNED

User-owned stable composition.

Examples:

- chosen statistic;
- important Goal trajectory;
- preferred recent-activity view;
- selected timeline/list module.

DANTE should not reorder/remove these silently.

## ADAPTIVE

Bounded contextual relevance selected by DANTE/application logic from valid projections.

Properties:

- clearly subordinate to stable user-owned layout;
- predictable location/behavior;
- can change because reality changed;
- must preserve source/provenance/confidence semantics where applicable.

## EPHEMERAL

Temporary visual answer spawned by conversation/exploration.

Properties:

- does not become persistent automatically;
- can be dismissed;
- can be refined by follow-up interaction;
- can be promoted to a stable module only through an explicit accepted flow.

---

# 12. Customize mode

Normal consumption mode must remain visually clean.

Editing affordances such as drag handles, resize controls and removal actions should appear only in a deliberate customization state where possible.

Customize mode must define:

- enter/exit semantics;
- keyboard/touch equivalent interactions;
- focus movement during reorder;
- deterministic cancel/apply behavior;
- conflict/error representation once real persistence exists;
- no accidental deletion of underlying canonical records.

During pre-backend development, configuration changes may be held by the local deterministic adapter for scenario testing. They must not be described as durable cross-device product persistence.

---

# 13. DANTE AI boundary

World AI is contextual, not a separate semantic store.

World context may constrain or inform conversational capabilities, but does not mean every query should be limited to records already visually shown on screen.

Frontend responsibilities:

- expose active World context to the future conversational integration boundary;
- render conversation/application lifecycle honestly;
- render typed visual Insight projections;
- emit semantic interaction intents;
- never fabricate backend/AI success.

Future application/backend responsibilities:

- capability selection/validation;
- authorization/disclosure;
- canonical/derived query execution;
- consequence validation;
- provenance/freshness;
- tool execution and result normalization.

No frontend component should construct raw SQL or provider queries.

---

# 14. Insight Layer architecture

Insight is a presentation capability, not a new canonical owner.

The layer should support bounded presentation depths:

```text
peek-sized
insight-sized
explore-sized
```

Selection of depth may be driven by the capability/result, user request or explicit expansion.

The layer must define:

- stacking policy;
- focus trap or non-modal semantics appropriate to each depth;
- Escape/back behavior;
- return focus;
- responsive/mobile transformation;
- loading/partial/stale/error states;
- follow-up query relationship;
- promotion to pinned module where valid.

Do not open unbounded nested modal stacks.

---

# 15. Frontend ports/adapters

The pre-backend phase requires an explicit data source/application port.

Conceptually:

```ts
interface WorldFocusDataSource {
  getWorldFocus(...): Promise<...>
  applyLocalPersonalization(...): Promise<...>
  runScenarioInsight(...): Promise<...>
}
```

Exact TypeScript API must be derived from real flows, not copied from this pseudocode.

Local deterministic adapter requirements:

- realistic async lifecycle;
- deterministic fixtures;
- selectable failure/partial/stale states;
- cancellation-safe behavior where relevant;
- no claim of durable/canonical persistence;
- no fake universal success.

Future backend adapter will satisfy the same frontend application needs through generated API/client contracts.

---

# 16. State model

The page and each module need explicit state semantics.

Minimum pressure set:

```text
loading
ready
partial
stale
empty
error
unavailable
```

Not every module must use every state if semantically impossible.

Rules:

- page-level error is reserved for failure to establish a usable World Focus at all;
- one failed secondary module should degrade locally;
- stale must not be visually indistinguishable from fresh when freshness matters;
- empty != error;
- unavailable != empty;
- unknown/missing != explicit negative.

Async race rule:

When active World or route context changes, obsolete completion must not overwrite the new active World state.

Use request identity/abort/cancellation or equivalent deterministic protection.

---

# 17. Frontend state ownership

Use the narrowest correct owner.

Preferred hierarchy:

```text
backend canonical state                future backend
route/navigation state                 router
remote request lifecycle               query/data layer when real integration justifies it
World Focus application/UI state       feature-local explicit state
module-local transient interaction     component/local reducer
cross-tree transient state             only if a real need justifies Zustand or equivalent
```

Do not introduce a global state library merely because World Focus is complex.

Do not duplicate the same active World/layout state in router + global store + component state without an explicit source-of-truth contract.

---

# 18. Error isolation / resilience

Required:

- page boundary;
- module boundary for failure-prone/lazy specialist modules;
- typed unknown-module fallback;
- lazy-load failure handling;
- controlled retry where useful;
- no infinite retry loops;
- async cleanup on navigation/unmount;
- no leaked event listeners, observers, timers, RAF or animation resources.

AI unavailable must not make the structured World unreadable.

World Focus must remain a first-class GUI even when AI is unavailable.

---

# 19. Performance architecture

Performance is part of correctness for this surface.

## Initial load

- keep World Focus shell/core runtime small;
- do not eagerly import every specialist module;
- do not eagerly import heavyweight chart/map/3D libraries;
- critical visible modules may load first;
- secondary/offscreen modules may lazy load when this improves measured behavior without creating disruptive layout shifts.

## Rendering

- isolate module render ownership;
- stable keys/instance identity;
- memoization only where profiling or clear data-shape stability justifies it;
- avoid top-level context values that rerender the entire World on minor module changes;
- use container layout instead of JS measurement when CSS can own it;
- ResizeObserver only against the real owner container and with cleanup.

## Data pressure

Future integration must support:

- bounded queries by World/use case;
- batching/aggregation where appropriate;
- cursor-based long-list pagination where needed;
- server/query-layer aggregation/downsampling for large time series when appropriate;
- no one-request-per-widget architecture by default;
- cache policy that respects derived-state freshness and consequential revalidation requirements.

## Motion

- transform/opacity preferred;
- avoid forcing synchronous layout per frame;
- animation work released after transition;
- visual effects cannot keep expensive loops alive while static;
- reduced-motion path tested separately.

Measured performance budgets are frozen only after representative browser profiling.

---

# 20. Security / privacy / disclosure carry-forward

Pre-backend frontend cannot enforce authoritative security, but its architecture must not make future enforcement impossible.

Rules:

- frontend hiding != authorization;
- module capability discovery != permission;
- do not cache sensitive future payloads in uncontrolled browser persistence;
- no raw secrets/tokens in view models/logging;
- Insight surfaces must be compatible with recipient/disclosure-filtered projections;
- explanations/aggregates must not assume hidden source data may be exposed;
- telemetry must not log sensitive World payloads by default.

The future backend must implement authorization and WL-H12-style non-interference/disclosure constraints where applicable.

---

# 21. Observability contract for later activation

The architecture should expose natural instrumentation boundaries for later full vertical work, including:

```text
World Focus open latency
projection fetch/build latency
module lazy-load latency/failure
module render/error kind
insight request latency/failure
payload size
cache behavior
long-task / animation issues
```

Do not add an observability framework in the pre-backend frontend merely to satisfy this list. Preserve clean boundaries so instrumentation can be added without rewrites.

---

# 22. Testing architecture

At minimum the pre-backend workstream must support:

## Contract/static

- discriminated module projection validation;
- registry completeness/unknown-kind failure;
- no forbidden cross-feature imports;
- no prototype runtime imports;
- TypeScript strictness/lint/format/architecture gates.

## Component

- each module state family;
- module action emission;
- isolation of module error;
- AI insight rendering;
- customize interactions.

## Integration

- World switch race/cancellation;
- entry/exit/back/focus restoration;
- layout composition determinism;
- insight -> refine -> dismiss/promote flow;
- local adapter failure/partial/stale scenarios.

## Browser/E2E

- Home -> active World -> World Focus -> back;
- AI available/unavailable frontend state;
- keyboard-only operation;
- reduced motion;
- responsive matrix;
- zoom/text pressure;
- customization flow;
- multiple contrasting World fixtures.

## Visual

- transition start/end key states;
- default layouts for scenario Worlds;
- insight depths;
- customize mode;
- error/empty/stale states where visually material.

## Performance

- initial chunk/load regression measurement;
- transition long-task/frame pressure where tooling permits;
- rerender regression for module-local updates;
- no retained observers/listeners after repeated open/close.

Do not claim a gate green unless it was actually executed.

---

# 23. Architecture anti-patterns — hard reject

```text
one giant WorldFocus.tsx
one page component per World
one DB/API endpoint invented per widget
WorldItem universal entity
world_id added blindly to every canonical owner
JSON blob as hidden universal model
LLM-generated JSX/HTML
frontend SQL/provider access
one request per widget by architecture
per-World bespoke animation engines
all modules bundled eagerly
AI required for basic World readability
global store for every local interaction
silent adaptive reordering of pinned content
fake durable persistence in localStorage for data that must later be canonical/cross-device
```

---

# 24. Backend vertical handoff condition

Do not start real backend/database/API integration until the frontend/product gate proves:

1. World Focus works naturally for at least four materially different World scenarios;
2. module grammar is stable enough that backend contracts will not be redesigned immediately;
3. personalization semantics are understood;
4. AI Insight interaction is validated;
5. explicit vs derived World relevance questions have a documented application-level requirement;
6. required backend reads/writes can be listed precisely without speculative tables/endpoints.

At that point create a separate full-vertical architecture/contract derived from the closed Domain/Logical/Physical/Database authorities and this validated frontend requirement set.

The future vertical may change frontend contracts if real integration proves a defect, but it must not silently redefine Domain meaning for convenience.
