# DANTE — World Focus Frontend Roadmap

**Status:** CURRENT WORKING ROADMAP — PRE-BACKEND  
**Date:** 2026-09-01  
**Branch:** `feature/home-react`  
**Scope stop:** complete production-grade frontend/product behavior before real backend/API/database/provider/LLM integration.

This roadmap replaces the older `WF0 -> WF8` sequencing. It also records that the broad workspace/module uncertainty research has already been completed; future chats must not restart it from zero.

## 1. Delivery rule

World Focus is built one complete functional/platform slice at a time.

```text
authority + already-closed evidence
-> focused pressure only for genuinely open decisions
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
-> next slice
```

Do not build all models/services first and UI later. Do not open several broad feature tracks in parallel. Do not redo closed reverse engineering merely because a new chat starts.

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

### Workspace/module scenario research — DONE

The original scenario oracle stress-tested the platform against materially different Worlds and explicit future uncertainty, including unknown future Worlds and unknown future specialist modules.

The durable conclusions are retained in:

`world-focus-workspace-scenario-oracle-evidence.md`

Already established:

```text
one workspace platform, not page-per-World
no generic WorldItem / Thing semantic root
finite registered renderer/surface families
unknown specialist surfaces through controlled extension
specialist renderer only when reusable primitives materially lose meaning
stable / adaptive / ephemeral remain distinct
AI cannot silently mutate stable composition
DANTE can drive contextual Insight / Explore / deeper-surface intents
no arbitrary model-generated executable UI
typed source drill-down on demand
large-data projections bounded/aggregated before React
cross-World reuse without canonical duplication
future stable config must support version/evolution semantics
sparse and dense Worlds must share the same platform
```

Do **not** re-run this whole research pass.

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

Engineering is retained. Integrated visual acceptance is deferred until the real workspace orchestration/surface footprint exists.

## 3. CURRENT GATE — World Workspace Platform materialization

This is the only active next World Focus scope.

The target is **inside the frozen rectangular workspace**, not the outer route/sphere/opening/VFX.

### Goal

Materialize the production-grade frontend workspace orchestration already implied and stress-tested by existing research, so chat, contextual DANTE, Insight, Explore, proposals, deeper panels/surfaces and dynamic composition have a coherent shared host.

This is not a license to build a speculative plugin framework or enumerate every future surface.

### Platform responsibilities to materialize as proven necessary

```text
dynamic composition host
finite surface/renderer registry
interaction cursor ownership
selected projection/source references
surface open / close / replace / promote semantics
Insight / Explore / contextual deeper-surface presentation
World contextual DANTE presence/conversation footprint
stable / adaptive / ephemeral coexistence
focus / back / Escape ownership
responsive/mobile surface mapping
surface-local error/degraded behavior
race/generation safety
performance/resource behavior
AI unavailable/degraded presentation
```

### Already fixed; do not reopen

```text
World != page-per-domain
World != dashboard ontology
unknown future modules must extend rather than rewrite
ModuleKind != Domain owner
ModuleKind != World question
no arbitrary AI-generated JSX/HTML/JS
specialist surfaces only when generic primitives lose meaning
AI Insight != stable module automatically
stable content cannot be silently rearranged by adaptive logic
DANTE can request contextual Insight/Explore/deeper presentation
```

### DANTE semantic depth already fixed

```text
P0 QUIET
P1 INVOKE
P2 CONTEXTUAL ENTRY
P3 INSIGHT
P4 PROPOSAL
P5 ACTION / RECEIPT
```

Home AI surface is not the World DANTE surface.

### Still genuinely open

Only concrete presentation/orchestration choices that were never frozen should receive fresh focused research/alternatives:

```text
exact DANTE quiet footprint
composer/invocation placement
conversation expansion geometry
which semantic depth maps to inline / sidecar / overlay / full-workspace
surface coexistence vs exclusivity
focus/back/Escape precedence
responsive/mobile mapping
exact local state model required by those interactions
```

These decisions must be reviewed with the user before visually consequential behavior is frozen, but they do not justify restarting the broad module/workspace architecture study.

### Required pressure during implementation

Use the already identified contrasting cases:

```text
Music
Body
Travel
Finance
Study
Relationships
unknown future World
sparse World
dense World
unknown future specialist surface
quiet DANTE
long conversation
Insight
Explore
Proposal/action presentation
AI unavailable
provider stale/partial where relevant
```

### Exit gate

Workspace platform behavior must pass:

```text
automated gates
assistant real-browser review
user functional review
user visual/interaction review
fixes/rerun
explicit user OK
```

before later content slices treat the workspace contract as frozen.

## 4. B2 integrated acceptance after workspace platform

Once the actual workspace/surface footprint exists:

1. remount/review Continuity within the real dynamic composition area;
2. verify it behaves as one optional composed answer rather than a fixed page section;
3. run user functional + visual review;
4. fix/polish if needed;
5. freeze B2 only after explicit user OK.

Do not redesign Continuity merely to fill empty space.

## 5. Subsequent content vertical selection

Do **not** pre-freeze a long numbered module list now.

After each accepted slice, choose the next highest-value World question from the Product Contract.

Candidate families include:

```text
Situation
Attention / Resolution
Next
Change
Evidence / History
Explore
Act / Decide
Trajectory / Comparison when semantically justified
DANTE Insight/Proposal depth as real interactions mature
```

Selection depends on:

- cross-World usefulness;
- visible user value;
- architecture proof value;
- semantic risk;
- ability to implement truthfully before backend;
- interaction with already frozen workspace/DANTE behavior.

## 6. Dynamic composition maturation

The composition machinery should be completed incrementally through real renderers, not through an abstract dashboard builder.

Permanent rules:

```text
World composition != fixed dashboard template
module kind != Domain meaning
module kind != World question
renderer != canonical owner
```

The system must support:

- stable user-owned content;
- bounded adaptive content;
- ephemeral query/Insight content;
- sparse Worlds;
- different density without per-World page branching;
- responsive behavior based on allocated container space;
- module/surface-local failure isolation;
- controlled specialist extension.

Do not introduce a free-coordinate dashboard/grid system until real customization proves it necessary.

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
unknown future specialist surface
```

If success requires an entire page branch by World identity, the platform has failed.

## 9. Production hardening / pre-backend freeze

Before real backend integration:

### Architecture

- no component direct HTTP;
- no backend DTO/DB leakage;
- no universal `WorldItem`/Thing collapse;
- no parallel World AI runtime;
- no arbitrary runtime executable plugin UI;
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
- conversation/surface expansion does not cause pathological layout/render work;
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

The frontend must not need a product/workspace rewrite merely to connect these capabilities.

## 11. Permanent roadmap rule

This roadmap tracks current sequence and gates, not speculative feature promises.

Whenever a user acceptance or recovered/reverse-engineering result changes sequencing materially, update this roadmap and `world-focus-current-checkpoint.md` immediately so a later chat cannot restart from an obsolete phase plan.
