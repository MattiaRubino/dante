# DANTE — Temporal Frontend Production-Depth Roadmap

**Status:** ACTIVE AUTHORITY — C1 AUTOMATED PASS / USER MANUAL ACCEPTANCE PENDING  
**Original roadmap date:** 2026-08-31  
**Current-status reconciliation:** 2026-09-02  
**Workstream owner:** `feature/home-timeline`  
**Worktree:** `/home/mattia/projects/dante-timeline`  
**Integration target:** `feature/home-react`  
**Frozen common base:** `98b486a308961022ba0d8f43bb79339518457741` — H0 Whole Home Structural Freeze / CI green  
**F0 closed checkpoint:** `7034b9b0d100709785ebe96e3816aab3e7b1d1f8`  
**C1 implementation candidate:** `81808814abb4e4998c7bde5b0c6cb8f5f903aa62`  
**C1 automated evidence:** Frontend CI `33613239926` / #536 — FULL PASS  
**Consumes:** `temporal-experience-architecture.md`, `timeline-t1-frozen-contract.md`, H0, Product V1 temporal documents and simulations, closed Domain/Logical/Physical semantics, CP6 PostgreSQL materialization, current frontend production standards  
**Scope stop:** maximum production-depth frontend capability up to, but not including, real backend/API/provider/solver integration

---

## 1. Authority and workstream isolation

This document is the operational authority for Timeline work after the split from the general Home branch.

Historical temporal documents may still mention `feature/home-react` because they were authored before the split. That metadata is historical only. It does **not** assign temporal implementation work back to the Mondi/Home workstream.

Current ownership is:

```text
feature/home-timeline
→ Home Timeline
→ shared temporal frontend application capability
→ temporal Detail/create/edit/execution/replan frontend flows
→ future dedicated temporal workspace
→ pre-backend temporal ports/adapters/tests/docs

feature/home-react
→ Mondi / Central Stage / World Focus workstream
→ Home integration line

H0 / shared infrastructure
→ change-controlled integration surface
```

The Timeline workstream must not use Mondi/World Focus files as a convenience dependency and must not casually modify:

- HomeShell/AppShell ownership;
- Central Stage or World Focus;
- global Home geometry;
- global design tokens;
- shared i18n architecture;
- CI/shared architecture rules;
- H0 contracts.

If a genuine shared change is required, it is isolated, justified, tested and intentionally propagated/integrated. Shared files are not a place to hide Timeline-specific behavior.

**Permanent rule:** child capabilities consume the H0 Home skeleton; they do not renegotiate it.

---

## 2. Product objective

The target is not merely a polished calendar component.

The Timeline must become a production-grade temporal operating surface that can expose DANTE's richer semantics without making simple actions complicated.

The frontend must preserve recoverability of distinctions already established by Product/Domain/DB, including:

```text
Occurrence != Schedule != Session != Actual
planned/intended != actual reality
recurrence source != generated occurrence
Proposal != Decision != accepted effect
confirmation/provenance != outcome
calendar/life area != sharing
AI output != canonical truth
```

The UI may use simpler language and progressive disclosure. The application layer must not collapse these distinctions in a way that forces a later rewrite.

### Experience benchmark

The desired combination is:

- Google/Notion Calendar-level predictability and manual speed;
- Akiflow/Sunsama-level task-to-time operational fluency;
- Motion/Reclaim-class adaptive planning mechanics where DANTE semantics permit them;
- Fantastical-class temporal/time-zone maturity where relevant;
- stronger DANTE guarantees around accepted state, constraints, provenance, reversibility and planned-vs-actual truth.

Do not copy competitors feature-for-feature. Borrow mature interaction patterns only when they improve DANTE's own product model.

---

## 3. Delivery model — one capability to maximum useful depth

After the common foundation is strong enough, work proceeds **capability by capability**, not as one enormous abstract architecture project.

```text
bounded capability
→ product/domain alignment
→ frontend application boundary
→ complete UI states/interactions
→ accessibility + keyboard + touch strategy
→ responsive + i18n
→ performance/cleanup
→ automated regression protection
→ user visual/manual PASS
→ freeze
→ next capability
```

A capability is not complete because its happy path renders.

For every capability, production-depth means all applicable items below are closed:

- semantic contract and ownership;
- normal, empty, disabled/unavailable, validation and error states;
- pending/retry/recovery/reconciliation states when meaningful;
- keyboard and focus behavior;
- pointer/touch behavior where applicable;
- responsive/viewport collision behavior;
- non-color-only state communication;
- reduced-motion behavior;
- i18n-safe content/layout;
- deterministic local behavior before backend exists;
- listener/observer/timer/RAF cleanup;
- dense/repeated-use performance pressure;
- unit/component/E2E/Firefox gates as relevant;
- no dead code, fake success, dangling feature flag or misleading affordance;
- documentation and frozen regression contract when behavior is accepted.

**Architecture rule:** build only abstractions justified by current or already-authoritative next flows. Do not build a speculative enterprise framework merely to look sophisticated.

---

## 4. External-vertical dependency policy

Some temporal experiences depend on capabilities owned elsewhere. They must not block the Timeline foundation, and they must not be faked inside this branch.

### AI / contextual intelligence

AI provider/runtime is an external vertical.

Timeline may define and consume typed temporal intents, candidate interpretations, proposal/preview contracts and integration ports. Until the AI vertical exists, only deterministic fixtures/test doubles may exercise those contracts.

Do **not** implement a private Timeline AI stack or present mock model output as production intelligence.

C1 now provides the first concrete source-neutral structured seed contract. A future DANTE interpreter, global Create, keyboard entry or import path must feed that semantic boundary and the same Create session; it must not automate the UI by clicking controls.

### Voice

Voice is an alternative input channel owned by its future/global vertical. Timeline exposes the same semantic command boundary used by manual controls. It does not implement speech capture/provider logic here.

### Backend / persistence / solver

Real API, PostgreSQL mutations, provider synchronization and production solver integration are outside this roadmap's stop line.

Frontend work must stop at explicit ports/adapters with truthful local behavior. No invented endpoint, ORM row or fake durable-server state.

### Notifications / Review / global Resolution orchestration

Timeline may expose handoff state/intents. Global notification delivery, review scheduling and cross-product Resolution orchestration remain separate capabilities unless explicitly moved into this workstream.

### Goal / Program / World / Project verticals

Timeline may render links/projections and emit navigation/operation intents for these concepts. Their independent CRUD/domain UI belongs to their own verticals.

C1 additionally establishes a typed external-owner handoff registry whose current targets remain explicitly `deferred`; handoff preserves a normalized immutable draft snapshot without fabricating a route or success state.

**Dependency rule:** if another vertical is unavailable, finish the Timeline-owned seam and expose the dependency truthfully; do not duplicate the external vertical.

---

# 5. Roadmap

## T1 — Existing Timeline final hardening and freeze

**Current status:** **FROZEN / CLOSED.** The audit scope below is retained as historical/operational evidence of the gate that was executed; it is not a current TODO list.

### Goal

Close the accepted Phase-1 Timeline as a genuinely reliable production-grade interaction baseline before expanding capability depth.

T1 is hardening, not redesign.

### Already protected

The current baseline already includes substantial real behavior:

- continuous bounded multi-day stream;
- viewed-date navigation and `Ora` behavior;
- semantic zoom/density mapping;
- deterministic compact overlaps;
- content-driven bounded card sizing;
- direct title/time/subitem action regions;
- focus/deselect-first grammar;
- custom first-gesture pointer drag without native drag ghost;
- same-day/cross-day movement;
- duration preservation and day bounds;
- Undo for move/time edit;
- keyboard movement;
- group filters/reorder;
- expanded group/event/header geometry and horizontal sync;
- calendar and time popovers with focus restoration;
- responsive Home behavior;
- Chromium + Firefox critical interaction coverage;
- RAF/timer/listener cleanup guards;
- reduced-motion CSS coverage.

### Historical audit scope — completed

Only demonstrated defects or missing production guarantees were permitted to reopen T1. The first hardening slice was:

**T1-A — mutation truth and motion/accessibility edge cases**

- no-op time edits must not create a fake mutation/Undo;
- boundary-clamped no-op moves must not create fake mutation state;
- feedback/Undo must describe the effect that actually occurred;
- imperative smooth scrolling must respect reduced-motion preference;
- add focused regression tests for these cases.

A final destructive audit then covered pointer, keyboard, viewport boundaries, repeated use and cleanup. The resulting T1/T1-A/T1-B contracts are now frozen and continue to be regression-tested, including the Firefox interaction contract.

### T1 exit gate — satisfied

```text
T1 = FROZEN / PASS
```

The gate required:

- no known correctness defect in accepted behavior;
- Timeline model/component tests green;
- lint/typecheck/build green;
- Timeline Playwright green;
- Firefox critical contract green;
- accepted responsive/H0 geometry unchanged;
- user visual/manual acceptance for observable corrections.

Do not weaken `timeline-t1-frozen-contract.md` to accept drift.

---

## F0 — Minimal shared temporal application foundation

**Current status:** **FROZEN / CLOSED** at `7034b9b0d100709785ebe96e3816aab3e7b1d1f8`.

### Goal

Create only the reusable frontend seams required so every later capability does not mutate fixture/component state in its own private way.

### Required primitives

Introduced and frozen incrementally:

- stable temporal projection/item identity;
- query/read boundary;
- typed semantic intent/command boundary;
- operation request/result model;
- draft vs accepted projection state;
- validation/error representation;
- expected-state/conflict representation where required;
- undo/recovery contract;
- clock abstraction;
- deterministic local adapter;
- clean separation of View Model, frontend application model, future DTO and Domain/persistence model.

The local adapter supports truthful operation outcomes needed by current flows and preserves the permanent non-collapse rules around idempotency, expected state, no-op and Undo.

### Exit gate — satisfied

F0 supports real Create without direct component mutation shortcuts and without backend-shaped abstractions.

---

## C1 — `+` / Create to production depth

**Current status:** **IMPLEMENTATION COMPLETE / AUTOMATED PASS / USER MANUAL ACCEPTANCE PENDING.**

**Final implementation candidate:** `81808814abb4e4998c7bde5b0c6cb8f5f903aa62`  
**Automated CI:** `33613239926` / #536 — FULL PASS  
**Expanded authoritative scope:** `temporal-create-c1-scope-amendment.md`  
**Final mapping/evidence:** `temporal-create-c1-traceability.md`

### Goal

Turn the Timeline `+` into the first fully closed capability while preserving a fast common path and the complete useful pre-backend authoring depth.

The original roadmap scope below began with the smallest truthful grammar, but the user-approved amendment expanded the C1 **completion** boundary before freeze. The original progressive principle remains valid; the current final capability is broader.

### Original progressive foundation — retained

- quick create from current/viewed temporal context;
- Event vs Activity where product semantics require the distinction;
- title;
- date;
- start/end or duration;
- all-day/date-span form where applicable;
- calendar/life-area assignment where current contracts support it;
- optional notes/context that belong to creation rather than another vertical;
- quick vs expanded creation;
- dirty/cancel/discard behavior;
- deterministic validation;
- keyboard/focus/pointer/touch behavior;
- responsive overlay/sheet strategy;
- unavailable external capabilities shown truthfully;
- local-adapter operation result and Undo/recovery where appropriate.

Do not put external owner CRUD, AI runtime, voice capture or backend persistence inside C1. Add only truthful integration seams.

### Final amended C1 depth now implemented

One shared draft/application lifecycle serves Quick, Expanded and Full Create plus contextual Timeline invocation.

**Activity** now authors, where applicable:

- timed/all-day/unscheduled forms;
- exact expected duration;
- open/bounded-window/deadline/preferred scheduling intent;
- earliest/deadline boundaries;
- movement/replanning policy;
- indivisible/splittable execution intent;
- minimum/max session intent;
- preparation/recovery/spacing;
- partial/early-finish/compatible-merge intent;
- fallback policy;
- confirmation/review/reminder intent;
- context/notes;
- external owner handoff.

Persistent repetition **does not** live on Activity. CP6 recurrence ownership is Routine/Event; therefore repeated Activity intent hands off to Routine. Do not reintroduce `Activity.repeat` or an Activity recurrence editor.

**Event** now authors:

- timed/all-day multi-day placement;
- start/end/duration;
- floating-local/named-zone time semantics and IANA timezone;
- location/availability/visibility;
- purpose/expected outcome/agenda/decision intent;
- participants/resources/pre-read/conference intent;
- preparation/recovery buffers;
- confirmation/reminder policy;
- all four CP6 recurrence families.

Event recurrence includes calendar daily/weekly/monthly/monthly-ordinal/yearly, elapsed interval, quota day/week/month/year with frame/week-start/zone, cyclic patterns with multiple active positions, and open/until/count termination.

C1 stores recurrence specification only. Backend M6 owns recurrence evaluator/Occurrence generation and exact governing recurrence-state binding.

**Integration/application hardening** now includes:

- source-neutral structured seed for future global Create/keyboard/import/governed DANTE interpretation;
- typed external-owner handoff registry with immutable normalized draft snapshot;
- rich-intent idempotency layered over F0 minimal command idempotency;
- normalized deep-frozen prepared specification at the application boundary to prevent prepare/execute mutation drift;
- candidate preview separate from accepted projection;
- provider actions as intent only;
- truthful local Undo/reveal/focus;
- accessibility, i18n and mobile full-screen protection.

### C1 automated gate — satisfied

CI #536 proves:

- Quality PASS;
- Mobile Bundle PASS;
- full Chromium Web E2E PASS;
- frozen Timeline Firefox contract PASS;
- Frontend CI Gate PASS.

Measured on the implementation candidate:

- architecture: 199 modules / 477 dependencies / zero violations;
- web unit: 28 files / 168 tests;
- Home route: 252.22 kB raw / 86.38 kB gzip.

### C1 freeze criterion — one human gate remains

The supported temporal objects can be created quickly on the happy path and safely under supported validation/cancel/input paths without fake persistence/provider claims. Automated engineering is complete.

C1 becomes `FROZEN / CLOSED` only after the user executes `temporal-create-c1-manual-acceptance.md` and explicitly approves the complete experience.

Do **not** start C2 before that PASS.

---

## C2 — Card → structured Detail to production depth

**Current status:** **NEXT AFTER C1 FREEZE / NOT STARTED.**

### Goal

Replace the current demonstration Detail with a real DANTE contextual detail experience while keeping resting Timeline cards calm.

### Architecture

Use a composable Detail shell, not one universal object with dozens of nullable fields.

Candidate capability sections, rendered only when semantically applicable:

```text
Identity / title
Temporal placement
Calendar / context
Notes / materials
Structured subitems
Recurrence
Scheduling constraints
Execution
Actual / confirmation
Linked Goal / Program / Project / World
History / provenance
Contextual command handoff
```

External vertical sections remain integration hooks until their owner exists.

### Required behaviors

- direct card/title entry according to frozen interaction grammar;
- progressive disclosure;
- edit affordances routed through shared temporal commands;
- proper loading/unavailable/error states even under local adapter simulation;
- focus ownership/restoration;
- deep keyboard usability;
- responsive modal/panel/sheet behavior;
- long-content and dense structured-item stress;
- no duplicated information wall.

### Freeze criterion

Simple appointment remains simple; structured learning/workout/program-occurrence examples can become rich without making every card or Detail instance equally complex.

---

## C3 — Temporal edit / move / resize to production depth

### Goal

Unify every manual placement change behind one semantic operation path.

### Scope

- precise time editor;
- drag move;
- cross-day move;
- resize/duration adjustment when product-approved;
- keyboard equivalents;
- pointer/touch alternatives;
- snap/precision behavior;
- day bounds;
- all-day/date-span transition only when semantically supported;
- timezone-aware edit when a named-zone item requires it;
- validation/conflict preview;
- no-op correctness;
- optimistic local interaction + rollback/recovery contract;
- Undo.

**Invariant:** drag, editor, keyboard and future AI/voice requests must converge on the same semantic operation grammar.

---

## C4 — Groups, filters, views and user preferences

### Goal

Take the already-useful grouping/view controls from prototype-grade local behavior to product-grade temporal organization.

### Scope

- selected calendar/life-area visibility;
- grouped vs unified chronology;
- ordering;
- focus combinations;
- preserved frontend preference boundary;
- hidden-conflict/affected-count awareness;
- empty/filtered states;
- accessible non-color-only recognition;
- dense-day legibility;
- responsive fallback when wide grouped columns are impossible.

Sharing is not a calendar group and must not be modeled as one.

---

## C5 — Recurrence and scheduling flexibility

### Goal

Expose DANTE's temporal rules without reducing them to a single `fixed/flexible` switch or a simplistic recurrence editor.

C1 now owns **initial creation-time** scheduling/recurrence authoring. C5 remains responsible for deeper editing/management of existing items and source/occurrence scope.

### Scope as applicable

Temporal constraint:

- fixed instant/block;
- bounded window;
- deadline-constrained;
- preferred window;
- open scheduling.

Movement/structure:

- locked;
- movable;
- confirmation-required;
- replannable;
- indivisible/splittable where supported;
- minimum duration/spacing/recovery constraints where relevant.

Recurrence/source scope:

- this occurrence;
- selected linked occurrences when justified;
- future occurrences;
- source routine/program/series when the owning vertical supports it.

The UI must distinguish an occurrence edit from changing the originating recurrence source. Source revisions must not rewrite historical generated-Occurrence provenance.

---

## C6 — Execution, Session, Actual and Confirmation

### Goal

Represent what happened separately from what was planned.

### Scope

As applicable to item type:

- in progress;
- ended but unconfirmed;
- completed;
- partial;
- skipped;
- missed/not completed;
- postponed;
- replaced;
- cancelled;
- reopened/corrected;
- actual start/end/duration;
- actual quantities/measurements;
- confirmation/provenance display;
- lightweight direct actions;
- Detail escalation for richer correction;
- Resolution handoff without duplicating the global Resolution vertical.

A time window passing must never silently imply completion unless an explicit user-approved rule exists elsewhere.

---

## C7 — Conflict, proposal and replanning experience

### Goal

Build the frontend mechanics required for governed replanning before any production solver/AI is connected.

### Scope

- conflict detection representation from deterministic/local inputs;
- hard constraint vs soft preference;
- candidate plan/proposal visually distinct from accepted plan;
- affected-item preview;
- smallest-valid-scope replanning grammar;
- infeasible/no-fit outcome;
- accept / modify / reject;
- confirmation where material;
- Undo/recovery;
- explanation of protected constraints and consequences.

A solver or AI provider may later generate candidates. It does not own the application of accepted effects.

---

## W1 — Dedicated temporal workspace architecture proof

### Goal

Prove the temporal application capability is reusable outside Home without stretching the Home Timeline renderer into a giant page.

### First proof

- dedicated route/surface;
- full Day projection;
- first useful Week/planning projection;
- shared selection/Detail;
- shared create/edit/move commands;
- flexible/unscheduled area when C5/C7 supports it;
- same temporal store/application capability;
- different renderer/layout allowed.

### Rule

```text
shared semantics/application capability
!= forced shared DOM/CSS renderer
```

---

## W2 — Dedicated workspace depth

After W1 proves the architecture, expand only validated planning needs:

- richer Day;
- Week;
- Month;
- Agenda/continuous list;
- grouped/focus views;
- multi-select/bulk operations;
- time-zone controls;
- flexible/unscheduled tray;
- broader horizon/load inspection;
- recurrence edit;
- candidate-plan/replan mode.

Long horizons change abstraction level. Do not render a year as hundreds of miniature rich Timeline days.

---

## X1 — External integration seams

### Goal

Close Timeline-owned contracts for capabilities whose runtime belongs to another vertical.

May include, when needed:

- AI candidate-intent input;
- contextual AI selected-item scope;
- future voice input;
- Global Search/Create command entry;
- Notification/Review/Resolution handoff;
- Goal/Program/Project/World navigation links;
- external calendar/provider source indicators.

C1 has already established reusable seed/handoff patterns. Later integrations should extend these shared contracts rather than create private command mechanisms.

### Exit rule

The Timeline side of each seam is complete and tested. Missing external verticals remain explicitly unavailable/deferred; no private duplicate implementation is created here.

---

## P0 — Production hardening and pre-backend freeze

### Goal

Reach the point where backend integration is predominantly adapter/integration work, not a frontend redesign.

### Architecture gates

- no component direct HTTP;
- no backend DTO/persistence leakage;
- no universal `Thing/Event` collapse;
- no duplicate Home/workspace temporal stores;
- stable public boundaries/exports;
- architecture/dependency checks green;
- external-vertical seams explicit.

### Behavior gates

For implemented capabilities:

- create/edit/move/undo;
- Detail;
- recurrence/flexibility;
- execution/Actual/confirmation;
- conflict/proposal/replan;
- workspace projections;
- manual/external-command semantic equivalence at the shared boundary.

### Accessibility gates

- keyboard reachability;
- deterministic focus ownership/restoration;
- screen-reader semantics;
- non-color-only state communication;
- WCAG 2.2 AA target;
- reduced motion including imperative JS motion;
- touch targets/mobile alternatives where applicable.

### Performance gates

- dense-day stress;
- multi-day/week stress;
- fluid scroll/zoom/drag;
- bounded rendering/windowing where justified;
- no uncontrolled layout thrash;
- listener/observer/RAF/timer cleanup;
- memory growth/repeated-open-close pressure;
- bundle/route-split review.

### Responsive/visual gates

- accepted desktop pressure matrix;
- expanded/collapsed Home Timeline;
- compressed/compact Home modes;
- overlay/detail collision tests;
- dedicated-workspace responsive matrix;
- visual regression where stable enough to freeze.

### Final stop condition

```text
React / renderers
        ↓
Temporal frontend application capability
        ↓
Explicit temporal ports
        ↓
Truthful deterministic local adapter
        ║
        ║  STOP — backend vertical starts after explicit gate
        ║
Future backend adapter / API / PostgreSQL / providers / solver
```

At this point no production backend is claimed, no provider integration is fabricated and no future DB/API implementation is invented inside the frontend.

---

## 6. Integration discipline with `feature/home-react`

Do not continuously merge the two workstreams back and forth.

Normal flow:

```text
feature/home-react
→ Mondi / World Focus progresses independently

feature/home-timeline
→ Timeline progresses independently

Timeline capability reaches a green/frozen integration checkpoint
→ intentionally integrate into feature/home-react
→ run combined H0 + Mondi + Timeline CI/E2E
```

If a shared change is needed earlier, isolate it as a small explicit change rather than dragging unrelated work across branches.

Unexpected movement of either branch must be inspected before integration. Never reset/discard the other workstream to simplify a merge.

---

## 7. Current execution point

Current branch lineage starts from the H0 frozen base:

`98b486a308961022ba0d8f43bb79339518457741`

Current state:

```text
T1    FROZEN / CLOSED
F0    FROZEN / CLOSED
C1    IMPLEMENTATION COMPLETE
      AUTOMATED PASS
      USER MANUAL ACCEPTANCE PENDING
C2    BLOCKED UNTIL EXPLICIT C1 USER PASS
```

Immediate sequence:

1. keep the documentation/traceability descendant CI-green;
2. user executes the one final protocol in `temporal-create-c1-manual-acceptance.md`;
3. any demonstrated defect reopens only the necessary C1 contract;
4. explicit `C1 MANUAL PASS — APPROVED` freezes/closes C1;
5. only then start C2 Card → structured Detail.

The former `T1-A` current-stage instruction and “do not activate + yet” instruction are historical and fully superseded by this progression.