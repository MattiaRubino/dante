# DANTE — World Focus Frontend Roadmap

**Status:** CURRENT WORKING ROADMAP — PRE-BACKEND  
**Date:** 2026-09-01  
**Branch:** `feature/home-react`  
**Scope stop:** complete production-grade frontend/product behavior before real backend/API/database/provider/LLM integration.

This roadmap replaces the older `WF0 -> WF8` sequencing. That sequence is no longer current because WR0-WR2 materially changed the product model and the implementation method moved to complete question-driven mini-verticals.

## 1. Delivery rule

World Focus is built one complete functional vertical at a time.

```text
authority + semantics
-> simulations / reverse engineering
-> external product + technology research where relevant
-> architecture decision
-> complete frontend implementation
-> responsive / accessibility / security / performance / state / errors
-> automated gates
-> real-browser review
-> user functional + visual review
-> fixes
-> explicit user acceptance
-> freeze
-> next vertical
```

Do not build all models/services first and UI later. Do not open several broad feature tracks in parallel.

## 2. Completed / established foundation

### Structural foundation — FROZEN

```text
WF0 structural contract
WF-G3 geometry contract
```

World Focus is a real `/worlds/:worldId` route below the shared AppShell/Topbar, with one rectangular persistent workspace and separate visual-frame geometry.

### B0 — production foundation — CLOSED

Established:

- feature ownership/layering;
- runtime-validation seam;
- latest-read/race/cancellation foundation;
- safe external-link handling;
- route/local render isolation;
- workspace/container-query foundation;
- timing/performance seam;
- accessibility foundation;
- ornamental WebGL degradation policy;
- explicit dependency non-adoptions;
- backend/provider/LLM stop line.

### WR0-WR2 — World product/context reverse engineering — CLOSED

Established:

- World as a user-recognizable continuity context;
- World-worthiness criteria;
- Home vs World vs Explore/Search boundaries;
- World Output Grammar;
- question-driven rather than widget-driven composition;
- four-layer World context model;
- purpose-scoped authorized DANTE context;
- coherent projection/DANTE basis;
- cross-World expansion rules;
- DANTE presentation depth semantics P0-P5;
- AI-unavailable first-open requirement;
- no new Domain/Logical/Physical/DB/Intelligence structural gap.

### B1 — Orientation — CLOSED FOR SEQUENCING

Kept:

- World identity/orientation;
- route-owned active World;
- route lifecycle/state boundaries;
- responsive/a11y shell behavior.

Removed after product falsification:

- universal visible time Lens;
- Lens-only session model;
- `?time=` contract and related fixtures/tests.

### B2 — Continuity / Resume — IMPLEMENTED / AUTOMATED PASS

Proves the first real question-driven World projection:

> **What is in motion and where can I continue?**

Engineering is retained. Integrated user visual acceptance is deferred until the next structural product gate establishes DANTE's actual footprint inside the workspace.

## 3. CURRENT GATE — World contextual DANTE presence / spatial UX

This is the only active next World Focus scope.

### Goal

Determine how DANTE physically and interactively exists inside World Focus **without copying Home**, before additional dynamic content is composed around a false full-width workspace assumption.

### Already fixed semantically

WR2 already defines:

```text
P0 QUIET
P1 INVOKE
P2 CONTEXTUAL ENTRY
P3 INSIGHT
P4 PROPOSAL
P5 ACTION / RECEIPT
```

and:

```text
World identity
World relevance
interaction cursor/session when needed
authorized purpose-scoped DANTE context
```

Do not reopen these merely to solve geometry.

### Must be reverse-engineered before code

- persistent vs transient DANTE presence;
- quiet footprint;
- composer/invocation placement;
- long-conversation mode;
- sidecar/dock/overlay/full-surface alternatives;
- layout-consuming versus overlay states;
- minimum remaining dynamic-content area;
- content reflow/continuity during expansion;
- contextual selection/deictic interaction;
- conversation versus Insight;
- conversation versus Explore;
- Proposal/confirmation/action receipt states;
- World switch/run binding;
- desktop/laptop/tablet/mobile;
- keyboard/focus/SR/touch/reduced motion;
- AI unavailable/degraded state;
- pre-backend shell now versus real runtime later.

### Required product pressure

At minimum:

```text
Music
Body
Travel
Finance
Study
Relationships
sparse World
dense World
quiet DANTE
long conversation
Insight
Proposal/action
```

### Exit gate

No production World DANTE UI is written until the reverse engineering/alternatives are reviewed with the user.

After implementation, the DANTE footprint must pass automated gates and the user's real-browser functional/visual review before the roadmap advances.

## 4. B2 integrated acceptance after DANTE footprint

Once the contextual DANTE shell/space contract is frozen:

1. remount/review Continuity within the real remaining dynamic-content area;
2. verify it behaves as one optional composed answer rather than a fixed page section;
3. run user functional + visual review;
4. fix/polish if needed;
5. freeze B2 only after explicit user OK.

Do not redesign Continuity merely to fill empty space.

## 5. Subsequent content vertical selection

Do **not** pre-freeze a long numbered module list now.

After each accepted vertical, choose the next highest-value World question from the Product Contract and re-run the delivery methodology.

Current candidate families include:

```text
Situation
Attention / Resolution
Next
Change
Evidence / History
Explore
Act / Decide
Trajectory / Comparison when semantically justified
DANTE Insight/Proposal depth when the contextual surface supports it
```

Selection depends on:

- cross-World usefulness;
- visible user value;
- architecture proof value;
- semantic risk;
- ability to implement truthfully before backend;
- interaction with already frozen composition/DANTE behavior.

A candidate can be skipped or reordered when new evidence proves another dependency/value path.

## 6. Dynamic composition milestone

As real output verticals accumulate, implement only the composition machinery proven necessary by those real renderers.

Permanent rules:

```text
World composition != fixed dashboard template
module kind != Domain meaning
module kind != World question
renderer != canonical owner
```

The composition system must eventually support:

- stable user-owned content;
- bounded adaptive content;
- ephemeral query/Insight content;
- sparse Worlds;
- different density without per-World page branching;
- responsive behavior based on allocated container space;
- module-local failure isolation.

Do not introduce a free-coordinate dashboard/grid system until real interaction proves it is necessary.

## 7. Personalization milestone

Only after several real modules/compositions prove the model, implement deliberate customization.

Required semantics:

```text
View
-> Customize Draft
-> Apply / Cancel
```

Removing a module never deletes canonical source reality.

Future persisted config requires versioning/concurrency semantics rather than silent last-write-wins.

DANTE proposals for stable configuration remain proposals until accepted under product policy.

## 8. Contrasting complete Worlds milestone

Before pre-backend freeze, validate several materially different complete-ish Worlds using the same platform:

```text
Music
Travel
Finance
Study or Body
Relationships / qualitative pressure
unknown future World
```

Pressure:

```text
empty
1-2 useful answers
4-8
12
20 potential modules/answers
fresh/partial/stale/provider unavailable
AI unavailable
multi-actor/privacy
large history
same canonical reality in multiple Worlds
```

If success requires an entire page branch by World identity, the platform has failed.

## 9. Production hardening / pre-backend freeze

Before real backend integration:

### Architecture

- no component direct HTTP;
- no backend DTO/DB leakage;
- no universal `WorldItem`/Thing collapse;
- no parallel World AI runtime;
- no duplicate global state when local/route/application ownership is sufficient;
- architecture checks green.

### Behavior

- World opens usefully without LLM;
- dynamic composition remains truthful/sparse;
- DANTE contextual interaction is coherent with visible basis;
- late async results cannot cross World/session generations;
- local failures do not collapse the full World;
- unknown Worlds fail sparse/safe;
- provider/AI failure does not rewrite canonical truth.

### Accessibility

- WCAG 2.2 AA target;
- keyboard/focus restoration;
- screen-reader semantics;
- non-color-only states;
- reduced motion;
- touch/mobile alternatives;
- drag alternatives if customization later introduces drag.

### Performance

- bounded first-open payload/rendering;
- no request-per-widget architecture;
- no all-life-data load;
- heavy specialist code lazy where justified;
- dense World stress;
- DANTE expansion/conversation does not cause pathological layout/render work;
- resource/listener/RAF cleanup;
- ornamental VFX degrades before interaction quality.

### Tests

- static/architecture;
- unit/component;
- integration;
- E2E;
- a11y;
- responsive/visual where appropriate;
- race/failure injection;
- relevant performance/resource regression.

## 10. Final backend vertical

Only after frontend/product freeze, replace deterministic/local adapters with real application/API adapters and integrate authoritative backend capabilities.

The backend vertical may include as justified:

- real projection/read APIs;
- authorization/disclosure enforcement;
- persistence/config sync;
- DANTE Context Builder/runtime integration;
- streaming and durable Run/Task semantics;
- provider/tool/effect integration;
- audit/reconciliation;
- backend contract tests.

The frontend must not need a product/layout rewrite merely to connect these capabilities.

## 11. Permanent roadmap rule

This roadmap tracks **current sequence and gates**, not speculative feature promises.

Whenever a user acceptance or reverse-engineering result changes the sequence materially, update this roadmap and `world-focus-current-checkpoint.md` immediately so a later chat cannot restart from an obsolete phase plan.
