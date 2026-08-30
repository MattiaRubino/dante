# DANTE — World Focus Frontend Roadmap

**Status:** ACTIVE WORKING ROADMAP — PRE-BACKEND  
**Date:** 2026-08-30  
**Branch:** `feature/home-react`  
**Consumes:** `world-focus-handoff.md`, `world-focus-architecture.md`, Home contract, closed Domain/Logical/Physical semantics, current Database SOR and frontend production-readiness contracts  
**Scope stop:** production-grade World Focus frontend up to, but not including, real backend/API/database/provider/LLM integration

---

# 1. Delivery model

World Focus is delivered in bounded production-depth slices.

```text
scenario/contract
-> implementation
-> automated gates
-> user visual/manual review
-> fix/polish
-> freeze
-> next slice
```

Do not open the full feature at once.

A slice is not complete because it looks good in one screenshot. It closes only when architecture ownership, interaction behavior, async states, responsive behavior, accessibility, reduced motion, performance pressure and relevant tests are addressed.

The user performs the final product/visual review in the real browser. The implementation side owns technical quality, tests and the concrete validation script.

---

# 2. Frozen baseline / exclusions

The accepted Home Mondi/Sintesi geometry and interaction baseline must not be reopened while building World Focus unless an actual integration defect proves a bounded change is required.

Current exclusions:

```text
NO real backend/API
NO database/Alembic changes
NO provider integration
NO real LLM/tool execution
NO new Domain World entity
NO Mondi Overview full design in this roadmap
NO arbitrary generated UI
NO redesign of Timeline / Orientation / Context Rail
```

The Home change required to enter World Focus must remain minimal and preserve the accepted carousel behavior.

---

# 3. Roadmap overview

```text
WF0  Scenario oracle + product grammar
WF1  Route/shell/entry transition foundation
WF2  Frontend application contracts + deterministic adapter
WF3  Module registry + composition canvas
WF4  Contrasting World compositions
WF5  Contextual DANTE AI + Insight Layer
WF6  Personalization / widgets / customization
WF7  Resilience + responsive + accessibility + performance hardening
WF8  Pre-backend freeze + full-vertical requirements handoff
```

Do not skip WF0 merely because the visual idea is already attractive.

---

# WF0 — Scenario oracle + product grammar

## Goal

Determine what World Focus must be capable of representing before freezing module/API-like frontend contracts.

## Required scenario Worlds

Use at least four materially different cases:

### Musica

Pressure to cover:

- active creative work;
- Goals/Plans/Activities;
- sessions/time invested;
- content artifacts/versions;
- release-like product profile/pipeline pressure;
- imported/derived performance Signals;
- contextual AI questions.

### Viaggi

Pressure to cover:

- Possibility -> planned trip evolution;
- Places;
- Events/Schedules;
- bookings/documents;
- participants/partial participation pressure;
- costs;
- changes/external/provider state;
- itinerary specialist-pressure test.

### Finanza

Pressure to cover:

- numbers/monetary values;
- time range;
- trend;
- comparison;
- breakdown;
- provenance/reconciliation pressure;
- user request -> visual Insight -> optional pinned widget.

This scenario is not permission to invent a specialist financial Domain model that is not currently accepted.

### Studio or Corpo

Pressure to cover:

- Goal trajectory;
- Plan/Routine/Activity;
- Sessions;
- Observations;
- planned vs actual;
- trend without inventing causation;
- current/recent/progress-oriented view.

## For each scenario define

- what the user wants to understand on open;
- which information deserves default foreground;
- what can remain secondary/on demand;
- what DANTE may adaptively surface;
- what should remain pinned/user-owned;
- 5–10 realistic AI questions;
- which questions deserve prose, Peek, Insight or Explore;
- which temporary visual results could sensibly become persistent widgets;
- which visual modules appear reusable across Worlds;
- where a specialist module is genuinely justified;
- empty/partial/stale/error cases;
- data that must not be inferred from absence;
- privacy/disclosure pressure where relevant.

## Deliverables

- scenario fixture specification;
- first candidate module-family table;
- rejected module/generalization list;
- default World Focus information-hierarchy hypothesis;
- first transition/theme profiles for scenario Worlds.

## Exit gate

WF0 passes only if the same World Focus architecture can represent all scenario Worlds **without one full-page branch per World**.

If the module system requires a giant generic blob to fit them all, WF0 also fails.

## User gate

Review the scenario outputs and confirm that the World Focus feels like “understand this part of my life”, not a generic analytics dashboard or a folder browser.

---

# WF1 — Route / shell / entry transition foundation

## Goal

Create the reusable World Focus application surface and prove correct entry/exit lifecycle before adding rich modules.

## Work

Implement:

- application route/state destination for one focused World;
- entry from the currently centered Home World;
- browser history/back behavior;
- return-to-opener semantics;
- stable World Focus shell;
- World identity/presentation header layer;
- close/back control;
- initial empty composition canvas;
- shared-element/world-entry transition foundation;
- one parameterized animation/theme profile contract;
- reduced-motion equivalent;
- route refresh/deep-link behavior appropriate to current fixture architecture;
- shell loading/error/unavailable states.

## Animation scope

Start with the smallest high-quality shared implementation:

```text
sphere geometry handoff
+ scale/field expansion
+ orbital/geometric layer
+ background transition
```

Only add richer particle/galaxy behavior after profiling.

World variation uses configuration, not bespoke components.

## Engineering gate

- format/lint/typecheck;
- route tests;
- Home regression tests;
- browser back/re-entry tests;
- focus restoration;
- reduced-motion test;
- no leaked RAF/listeners/observers;
- no accepted Home geometry regression.

## User visual test

Validate:

- Home -> Musica -> back;
- Home -> Viaggi -> back;
- repeated open/close;
- AI expanded/collapsed Home before entry;
- normal and reduced motion;
- compact and large desktop.

Freeze shell/entry ownership after PASS.

---

# WF2 — Frontend application contracts + deterministic adapter

## Goal

Move World Focus off ad-hoc component fixture reads and establish the production frontend integration boundary before module complexity grows.

## Work

Define only the contracts required by WF0/WF1:

- World focus projection identity;
- World presentation/theme profile;
- page projection status;
- module projection discriminant/base lifecycle;
- frontend semantic intents;
- layout projection/version placeholder contract at frontend level;
- Insight projection lifecycle shell;
- World Focus data-source/application port;
- deterministic local adapter;
- async request identity/cancellation;
- fixture scenario selector for tests/development.

The local adapter must support truthful state pressure:

```text
loading
ready
partial
stale
empty
error
unavailable
```

and configurable latency/failure for tests.

## Hard rules

- no invented HTTP endpoint;
- no backend DTO naming disguised as frontend model;
- no localStorage presented as canonical durable World state;
- no direct imports from prototype fixture HTML/JS;
- no generic repository/UoW abstraction unless a real frontend flow requires it.

## Exit gate

The shell can load/switch scenario Worlds entirely through the explicit application/data-source boundary, and stale completion from World A cannot overwrite active World B.

---

# WF3 — Module registry + composition canvas

## Goal

Build the extensibility engine that allows different Worlds to feel native without page-per-World branching.

## First module set

Derive from WF0. A likely initial set may include a subset of:

```text
metric / number+delta
trend
comparison
breakdown
small timeline / upcoming
Goal trajectory
planned vs actual
bounded item collection
recent reality
```

This list is not pre-approved merely because it appears here.

## Work

Implement:

- typed discriminated module union or equivalent bounded contracts;
- schema/runtime validation where fixture/untrusted boundaries justify it;
- finite module registry;
- module host/error isolation;
- supported size/presentation profiles;
- loading/empty/partial/stale/error rendering contract;
- deterministic composition canvas;
- responsive container ownership;
- lazy specialist-module hook without requiring a specialist module yet;
- accessibility base contract for modules;
- stable instance identity and rerender isolation.

## Reject

- giant optional-property module;
- renderer lookup from arbitrary string to dynamic remote code;
- one generic “card” that erases meaningful visual differences;
- each module owning page-level spacing/columns;
- global CSS screen-coordinate patches.

## Engineering gate

- registry unit tests;
- unknown-kind safe failure;
- per-module state tests;
- deterministic layout tests;
- error-boundary isolation;
- responsive container tests;
- bundle/lazy-load inspection for specialist boundary.

---

# WF4 — Contrasting World compositions

## Goal

Prove the architecture with real-feeling complete compositions, not isolated components.

## Work

Build at least the four WF0 scenario Worlds using only the shared shell/composition/registry architecture.

For each:

- default pinned composition;
- one bounded adaptive area/example;
- realistic current/recent data;
- relevant empty/partial variant;
- no fake canonical claims;
- theme/ambient variation through shared profile;
- responsive composition.

Where a specialist module appears necessary, implement **at most one** first and validate the extension contract before adding more.

## Exit gate

Pass criteria:

```text
no page-level world-name branching
no duplicated shell
no duplicated transition engine
no layout hacks per World
shared modules still look semantically appropriate
specialist extension does not contaminate registry/core
```

## User gate

Review all scenario Worlds side-by-side and decide:

- whether the default information hierarchy works;
- which modules feel useful vs dashboard-noise;
- whether adaptive content is too intrusive;
- whether World-specific ambience is worth keeping.

Freeze the first stable module grammar only after this review.

---

# WF5 — Contextual DANTE AI + Insight Layer

## Goal

Prove the key interaction:

```text
ask DANTE about this World
-> receive a useful visual answer when visual explanation is better than prose
```

without real LLM/backend integration.

## Work

Implement:

- World-aware AI surface shell;
- typed conversational request intent for deterministic scenarios;
- fixture/local response adapter;
- Peek presentation depth;
- Insight presentation depth;
- Explore presentation depth if WF0 proves it necessary;
- follow-up/refinement lifecycle;
- close/back/focus semantics;
- loading/error/unavailable states;
- typed InsightProjection -> approved renderer mapping;
- provenance/freshness display pressure where relevant;
- explicit no-AI structured World behavior.

## Scenario examples

Finanza:

```text
"Mostrami le spese dell'ultimo mese"
-> breakdown/trend Insight

"Solo fotografia"
-> refined Insight

"Confrontalo con gli ultimi tre mesi"
-> comparison update
```

Viaggi:

```text
"Cosa manca ancora?"
-> bounded checklist/status-style Insight if semantically justified
```

Musica:

```text
"Su cosa ho speso più tempo questo mese?"
-> time-distribution Insight
```

The local adapter returns deterministic typed results. Do not simulate free-form LLM intelligence as production truth.

## Hard reject

```text
AI returns JSX
AI returns HTML
AI chooses arbitrary executable component path
AI builds SQL
AI directly mutates pinned layout
```

## Exit gate

AI visual answers feel native to World Focus and the same typed presentation system supports manual/non-AI entry in principle.

---

# WF6 — Personalization / widgets / customization

## Goal

Allow the user to shape the stable World without turning the product into an unrestricted dashboard builder.

## Work

Implement:

- deliberate Customize mode;
- add-module/widget flow from approved catalog;
- pin/unpin where semantics allow;
- reorder;
- bounded resize/presentation profile if justified;
- remove-from-World without deleting source reality;
- cancel/apply behavior;
- keyboard/touch reorder equivalent;
- clear pinned vs adaptive vs ephemeral treatment;
- promote a valid ephemeral Insight into a pinned module configuration;
- layout version field at frontend contract level;
- local adapter-only persistence for the active scenario lifecycle as needed for testing, explicitly non-canonical/non-cross-device.

## Product rules

- normal mode stays clean;
- editing chrome is not permanently visible;
- DANTE does not silently reorder pinned items;
- `Add to World` saves a view/configuration intent, not a result snapshot by default;
- user must understand what will remain after customization.

## Exit gate

A user can ask for an Insight, decide it is useful, promote it into the World, rearrange the stable layout and remove it again without affecting underlying canonical scenario data.

---

# WF7 — Resilience / responsive / accessibility / performance hardening

## Goal

Take the complete pre-backend surface to production frontend quality.

## Responsive matrix

Establish an explicit matrix covering representative:

- compact desktop;
- accepted desktop;
- large desktop;
- tablet/narrow where current application strategy permits;
- mobile behavior if this web scope supports it rather than inventing native-mobile parity.

Also pressure:

- long labels;
- many modules;
- minimal modules;
- Peek/Insight/Explore open;
- Customize mode;
- AI unavailable;
- module error/stale state.

## Accessibility

Prove:

- keyboard-only entry, navigation and exit;
- focus return;
- module headings/landmarks semantics;
- accessible drag/reorder alternative;
- insight surface modal/non-modal semantics;
- reduced motion;
- 200%+ zoom/text pressure as applicable;
- axe automated checks plus manual focus/reading-order review;
- no color-only state.

## Performance

Measure before freezing numeric budgets.

Profile at least:

- route chunk and first open;
- repeated open/close resource cleanup;
- transition main-thread pressure;
- module lazy load;
- module-local update rerender scope;
- many-module scenario;
- Insight open/refine/close;
- memory/observer/listener cleanup.

Then freeze realistic budgets/regression checks in the quality contract.

## Reliability

Inject:

- delayed World load;
- World load failure;
- one module failure;
- lazy module failure;
- stale result;
- active World switch during load;
- AI unavailable;
- Insight failure;
- customization operation rejection in local adapter.

No single secondary failure may destroy an otherwise usable World Focus.

## Full frontend gate

Run applicable repository commands, expected to include the current equivalents of:

```text
format check
lint
typecheck
architecture checks
generated checks
unit/component tests
build
E2E
visual/accessibility checks
```

Use exact repository scripts at execution time. Do not copy stale command names blindly.

Do not claim green without execution evidence.

---

# WF8 — Pre-backend freeze + full-vertical requirements handoff

## Goal

Freeze the validated frontend/product model and produce the exact requirements the later backend vertical must satisfy.

## Required outputs

### World requirement map

Document:

- what identifies a user-configured World at product level;
- what is explicit configuration vs derived relevance;
- what may be shown from canonical relations without duplication;
- what World personalization must survive cross-device/session;
- what history/audit is materially required vs ordinary preference state.

Do not invent tables yet.

### Query/projection requirements

For every stable module/Insight family list:

- required semantic inputs;
- bounded scope/time range;
- freshness expectation;
- provenance requirement;
- authorization/disclosure pressure;
- pagination/aggregation needs;
- expected failure/partial behavior.

### Mutation requirements

List only validated writes, e.g. if retained:

- create/configure/archive product World profile;
- pin/unpin module configuration;
- reorder/resize layout;
- accept a DANTE suggestion;
- create a stable widget configuration from an Insight.

Distinguish these from mutations of underlying Goal/Event/etc.

### AI capability requirements

List the validated typed capability families and consequence boundaries.

### Performance requirements

Carry measured frontend behavior forward so backend projection design can avoid one-request-per-widget / excessive payload architectures.

## Backend gate

Only after WF8 is user/architecture accepted may the next workstream design:

```text
persistence consequences
application services/queries
projection builders
AuthZ/disclosure
API/OpenAPI
generated client
backend adapter
real AI/tool capability execution
full-stack tests
```

The backend vertical starts by re-reading current protected semantic/database authorities; it must not simply materialize the frontend fixture schema as tables.

---

# 4. Documentation rule

At each freeze point update only the authorities whose meaning actually changed.

World Focus durable documents:

```text
world-focus-handoff.md
world-focus-architecture.md
world-focus-frontend-roadmap.md
```

When Home entry behavior changes, update the Home contract/registry as applicable.

When shared application-shell/routing behavior changes, update its owning documentation rather than hiding the change in World Focus docs.

Open questions remain explicitly marked OPEN until resolved. Never rewrite an unresolved question as an accepted fact merely because code temporarily chose one implementation.

---

# 5. Immediate next action

Start **WF0 only**.

No code for the full-screen surface should be written until the scenario oracle has produced a first bounded information/module grammar and the user has reviewed it.

The first concrete deliverable is therefore the four-World scenario matrix and the candidate/rejected module set, followed by the smallest World Focus shell contract needed for WF1.
