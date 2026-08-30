# DANTE — Temporal Frontend Roadmap

**Status:** ACTIVE WORKING ROADMAP — pre-backend temporal vertical  
**Date:** 2026-08-30  
**Branch:** `feature/home-react`  
**Consumes:** `docs/frontend/home/temporal-experience-architecture.md`, current Home contract, closed Domain/Logical/Physical semantics and current frontend production standards  
**Scope stop:** production-grade frontend temporal capability up to, but not including, real backend/API/provider/solver integration

---

## 1. Delivery model

The temporal vertical is delivered in **small production-depth slices**.

The rule is:

```text
one bounded capability
→ implementation to production depth
→ automated gates
→ user visual/manual validation
→ fix/polish
→ freeze
→ next capability
```

Do not open many large temporal features at once.

The assistant owns the technical implementation, architecture, automated tests, accessibility/performance hardening and the concrete manual-test script. The user performs the final visual/manual product pass in the real browser and reports defects, awkward behavior or visual regression. If a slice becomes too large, it must be split into smaller gates without changing the overall roadmap.

A slice is not complete because it renders. It is complete only when the relevant architecture, behavior, error/state handling, keyboard/focus behavior, responsive behavior and tests are closed.

---

## 2. Permanent boundaries

### Visual baseline

The current Home Timeline visual/geometric baseline frozen at the Phase-1 checkpoint remains accepted. Do not redesign it unless a concrete new semantic/interaction requirement, accessibility issue, performance issue or user-reviewed visual defect justifies a change.

### Product surfaces

The frontend temporal capability serves at least:

```text
Home Timeline
Home expanded Timeline
Dedicated full-page temporal workspace
Shared contextual item detail
Resolution handoff
Global/contextual AI and future voice entry
```

These are projections/interaction surfaces over one temporal application capability, not independent products.

### Architecture

Share semantics, state contracts and operations where justified. Do **not** force the Home, day, week, month or agenda renderers into one mega-component.

```text
shared application capability
!= shared DOM/layout/CSS renderer
```

### Backend stop line

The final pre-backend state must expose explicit frontend ports/adapters. The temporary implementation may be local/in-memory/deterministic, but it must represent realistic lifecycle and failures rather than returning fake universal success.

No direct component HTTP, invented endpoint contracts, ORM/database shapes or fake durable-server claims.

---

# 3. Roadmap

## T0 — Temporal contract and scenario oracle

### Goal

Turn the accepted temporal architecture into an executable frontend behavior contract before modifying mature Timeline behavior.

### Work

Define the first canonical frontend scenarios:

1. simple appointment;
2. structured English lesson with subitems;
3. diet/meal program step;
4. workout with execution outcome;
5. call that starts early and/or overruns;
6. movable/flexible activity;
7. recurring occurrence changed only for today;
8. unresolved confirmation;
9. conflict requiring a proposal/replan;
10. equivalent manual vs contextual-AI request.

For each scenario define:

- what the Timeline card shows at rest;
- what appears only on hover/focus/selection;
- quick actions;
- Peek behavior;
- Detail behavior;
- when Resolution is used;
- what state must remain invisible unless relevant;
- semantic intent produced by manual interaction;
- expected failure/conflict cases.

### Exit gate

No UI implementation begins until these scenarios fit the progressive-disclosure model without overloading the Timeline card.

### User validation

Review the scenario behavior and confirm that the proposed interactions match the desired DANTE experience before coding deeper behavior.

---

## T1 — Selection → Peek → Detail foundation

### Goal

Create the first real production-depth interaction layer on top of the frozen Timeline visual baseline.

### Work

Implement:

- stable selected-item state;
- mouse, keyboard and focus selection semantics;
- non-destructive quick inspection/Peek;
- shared Detail-shell entry;
- opener/focus restoration;
- Escape/back semantics;
- responsive behavior;
- correct overlay/sheet/dialog ownership;
- first simple-item Detail profile;
- typed projection-to-detail boundary;
- no persistent mutation yet unless needed only to preserve existing Phase-1 behavior.

Do not build a universal optional-field Detail object. Create a shared shell with bounded profile/capability composition.

### Engineering gate

- format/lint/typecheck;
- component tests;
- keyboard/focus tests;
- existing Timeline regressions remain green;
- no layout regression at accepted Home breakpoints;
- no leaked event listeners/timers/RAF;
- accessibility audit on new interactive surfaces.

### User visual test

Assistant supplies a compact script covering:

- normal width;
- expanded Timeline;
- narrow desktop/tablet breakpoint;
- click vs keyboard open/close;
- repeated selection of different cards;
- long title/subitem content;
- visual hierarchy of Peek/Detail.

After user PASS, freeze T1.

---

## T2 — Temporal application core and truthful local adapter

### Goal

Move Phase-2 interactions off ad-hoc component state and establish the reusable frontend application boundary used by Home and the future full-page workspace.

### Work

Introduce only the abstractions justified by the real flows:

- temporal item projection identity;
- query/read port;
- typed semantic intents;
- operation request/result model;
- local deterministic data-source adapter;
- operation lifecycle sufficient for current scopes;
- draft vs accepted state;
- expected-state/conflict representation;
- undo/recovery contract;
- clock abstraction replacing prototype-only assumptions where appropriate without breaking fixture determinism;
- projection model remains separate from Domain, backend DTO and persistence row.

The local adapter must be able to simulate relevant outcomes, e.g.:

```text
applied
validation rejected
confirmation required
expected-state conflict
pending
known failure
unknown/reconciliation-required where a future external effect warrants it
```

Do not add generic repository/UoW/state-machine libraries merely to look enterprise-grade.

### Exit gate

Existing Phase-1 behavior still works, but the new Phase-2 flows use the shared application boundary instead of component-local mutation shortcuts.

---

## T3 — Create / edit / move vertical

### Goal

Turn Quick Add and edit/move into real frontend workflows while stopping before backend persistence.

### Work

Implement one shared command grammar for:

- Timeline `+`;
- click/coordinate quick create where approved;
- create from current/viewed date context;
- quick create vs expanded create;
- edit time;
- drag/move;
- cross-day move;
- cancel draft;
- validation;
- undo;
- recurrence-scope prompt only when recurrence is actually involved.

Manual controls must produce the same semantic application intents a future AI/voice request will use.

### Product rule

Simple creation must stay fast. Complex structure emerges only when requested or required.

### User visual/manual test

Test creation and move across:

- empty slot;
- overlapping item;
- different day;
- Timeline expanded/collapsed;
- short/long duration;
- invalid end-before-start;
- keyboard path;
- cancel/undo.

Freeze after product PASS.

---

## T4 — Structured Detail profiles and contextual AI surface

### Goal

Prove that temporal cards can represent rich DANTE realities without becoming visually overloaded.

### Initial profiles

Implement at least:

- simple appointment/event;
- Activity/task-like item;
- structured learning session;
- meal/diet step;
- workout/session;
- meeting/work item where the current frontend contract can support it truthfully.

### Shared Detail shell

May expose as applicable:

- title/time/current state;
- relevant quick actions;
- structured subitems;
- materials/notes/links;
- linked program/goal/world navigation hooks as frontend intents;
- planned vs actual summary when relevant;
- history/provenance entry affordance without fabricating backend data;
- contextual DANTE interaction surface.

### AI boundary

Before a production AI provider exists, contextual AI uses deterministic/mock interpretation cases that emit the **same typed candidate/operation contracts** expected later.

It must demonstrate:

```text
user language
→ candidate interpretation
→ validation
→ direct low-risk action OR proposal/preview
→ confirmation if required
→ application result
```

No model output is treated as canonical truth.

### User test

Use diet and English examples as the primary visual/product stress test. Verify that the Detail is rich while the Timeline card remains calm.

---

## T5 — Execution truth, Actual and Resolution

### Goal

Represent the difference between what was planned and what happened without turning Timeline into a status dashboard.

### Work

Add frontend representation/workflows for relevant states such as:

- in progress;
- ended but unconfirmed;
- completed;
- partial;
- skipped;
- not completed;
- postponed;
- replaced;
- cancelled where semantically appropriate;
- planned vs actual timing/duration/value where available.

Implement Resolution handoff for simple confirmations/corrections. Escalate complex cases to Detail/controlled resolution rather than cramming them in the rail.

### Key scenario

A call scheduled 14:00–15:00 may actually run 13:52–15:17. The frontend must preserve the planned schedule and represent actual execution separately where useful.

### User test

Run normal completion, missed confirmation, partial workout and call-overrun scenarios; verify Timeline, Orientation and Resolution do not redundantly show the same message.

---

## T6 — Flexible scheduling, recurrence and conflict/replan

### Goal

Implement the frontend mechanics that distinguish DANTE from ordinary event CRUD.

### Work

Represent and operate on, where required by current product contracts:

- fixed/locked placement;
- movable placement;
- bounded/preferred window;
- deadline-constrained work;
- open/unscheduled work;
- occurrence vs recurrence source scope;
- `this occurrence` / selected linked occurrences / future/source-level change where justified;
- hard constraint vs soft preference presentation;
- conflict states;
- candidate replan;
- affected-item preview;
- accept/modify/reject;
- undo/recovery;
- truthful infeasible/no-fit outcome.

The frontend must support “not everything fits” rather than silently violating a hard constraint.

### Replanning rule

Prefer the smallest valid affected scope and widen only when necessary.

### User test

Primary scenario: call overrun affecting a flexible English session before a fixed appointment. Verify that proposals are understandable and that accepted plan vs candidate proposal are visually distinct.

---

## T7 — Full-page temporal workspace: architecture proof

### Goal

Prove that the shared capability is not Home-specific before finishing every advanced Home behavior.

### First cut

Create a dedicated temporal page/surface with enough functionality to validate the shared architecture, initially:

- full day view;
- first useful week/planning projection;
- shared selection/Detail;
- shared create/edit/move operations;
- unscheduled/flexible planning area if T6 is ready;
- no duplicate store or alternate recurrence rules.

Do not simply stretch the Home Timeline to 100vw.

### Renderer rule

The full-page surface may use different DOM/layout/renderers while consuming the same temporal application capability.

### User visual test

Validate full-page information density, navigation, relation to Home and whether moving between Home and the dedicated page feels like two views of one system.

---

## T8 — Full temporal workspace depth

### Goal

Expand the dedicated workspace only after the architecture proof succeeds.

### Candidate capabilities

Implement based on validated product need:

- richer Day;
- Week;
- Month;
- Agenda/continuous list;
- grouped/focus views;
- multi-select/bulk operations;
- display preferences;
- time-zone controls;
- flexible/unscheduled tray;
- broader planning horizon;
- conflict/load inspection;
- recurrence editing;
- candidate-plan/replan mode.

Longer horizons must change abstraction level. Do not render a year as 365 miniature rich day timelines.

Each major view can be its own slice with its own visual PASS.

---

## T9 — Global AI / future voice convergence

### Goal

Demonstrate that natural-language and future voice interaction are alternative entry paths to the same temporal operations, not parallel application logic.

### Work

Frontend-only capability for representative requests such as:

- create an appointment;
- move English to tomorrow;
- replace today's meal only;
- apply a change to future program instances;
- replan affected flexible items after an overrun;
- ask what requires confirmation.

Global AI can target multiple items; contextual AI inherits selected-item scope. Future voice uses the same command boundary.

Broad/material changes require preview/confirmation according to product policy; low-risk unambiguous actions may use the approved direct path.

No production AI provider is required to close this frontend phase.

---

## T10 — Production hardening and pre-backend freeze

### Goal

Close the frontend temporal vertical at a quality level where backend integration is an adapter/integration phase, not a redesign.

### Required gates

#### Architecture

- no component direct HTTP;
- no backend DTO/persistence leakage;
- no universal `Thing/Event` collapse;
- no duplicate Home/full-page temporal stores;
- stable boundaries and exports;
- dependency-cruiser/architecture checks green.

#### Behavior

- scenario oracle passes;
- create/edit/move/undo;
- Detail profiles;
- Actual/confirmation;
- recurrence scope;
- flexible/unscheduled;
- conflict/proposal/replan;
- AI/manual command equivalence for covered cases.

#### Accessibility

- keyboard reachability;
- focus restoration;
- screen-reader semantics;
- non-color-only state communication;
- WCAG 2.2 AA target;
- reduced motion;
- touch targets/mobile alternatives where applicable.

#### Performance

- dense-day stress;
- multi-day/week stress;
- scroll/zoom/drag remain fluid;
- bounded rendering/windowing where justified;
- no uncontrolled layout thrash;
- listener/observer/RAF/timer cleanup;
- bundle/route-split review;
- memory growth/repeated-open-close checks.

#### Responsive/visual

- agreed desktop matrix;
- expanded/collapsed Home Timeline;
- narrow desktop/tablet;
- mobile behavior where implemented;
- Detail/overlay collision and viewport tests;
- visual regression screenshots.

#### Tests

- unit/model;
- component;
- integration;
- E2E;
- accessibility;
- visual/responsive where applicable;
- generated/build gates.

### Final stop condition

At completion the frontend talks to a temporal port implemented by a truthful local/deterministic adapter.

The next authorized vertical becomes:

```text
frontend temporal ports
        ↓
real API/application adapters
        ↓
backend/domain/database/solver/integration/AI runtime
```

No frontend redesign should be required solely because the real backend replaces the temporary adapter.

---

# 4. Working cadence for each slice

For every T-stage or sub-stage:

### A. Pre-write gate

Because multiple chats may work on `feature/home-react`, immediately before code changes record:

```text
BRANCH
PRE-SCOPE SHA
CREATE
UPDATE
DELETE
PURPOSE
OUT OF SCOPE
```

Recheck branch HEAD immediately before the first write. If it moved, inspect changed paths and re-gate.

### B. Implement to depth

Do not stop at visual parity. Close relevant architecture, behavior, a11y, responsive, performance and tests for that slice.

### C. Automated evidence

Run the appropriate quality gates and report exact results; do not reuse historical PASS as current evidence.

### D. User visual/manual gate

Provide the user with a concise test sequence containing:

- route/state to open;
- viewport(s);
- exact interactions;
- expected visual/behavior result;
- edge cases worth trying.

### E. Fix and freeze

Fix issues found by the user, rerun gates and mark the slice closed before opening the next meaningful capability.

---

# 5. Immediate starting point

Start with **T0 → T1**.

The current Timeline visual baseline is already accepted, so the next concrete design/implementation problem is not another Timeline redesign. It is:

```text
Timeline card
→ selection
→ Peek / quick inspection
→ shared Detail
```

Use the first scenarios in increasing richness:

```text
simple appointment
→ English lesson
→ diet/meal
```

This establishes the interaction grammar before create/edit/replan and before the dedicated full-page workspace consumes it.
