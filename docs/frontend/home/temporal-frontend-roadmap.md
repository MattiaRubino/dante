# DANTE — Temporal Frontend Production-Depth Roadmap

**Status:** ACTIVE AUTHORITY — C1 IMPLEMENTATION FULL GREEN / USER MANUAL ACCEPTANCE PENDING  
**Original roadmap date:** 2026-08-31  
**Current-status reconciliation:** 2026-09-02  
**Workstream owner:** `feature/home-timeline`  
**Worktree:** `/home/mattia/projects/dante-timeline`  
**Integration target:** `feature/home-react`  
**Frozen common base:** `98b486a308961022ba0d8f43bb79339518457741` — H0 Whole Home Structural Freeze / CI green  
**F0 closed checkpoint:** `7034b9b0d100709785ebe96e3816aab3e7b1d1f8`  
**C1 implementation candidate:** `f092a3db2fbac28421b73e0629f7b4b83a1b0aec`  
**C1 automated evidence:** Frontend CI `33631013598` / #621 — FULL PASS  
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

If a genuine shared change is required, isolate it, justify it, test it and integrate it intentionally. Shared files are not a place to hide Timeline-specific behavior.

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
Context/group membership != presentation override
visibility != sharing/ACL authority
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

### AI / DANTE intelligence

AI/DANTE interpretation is an external vertical and a separate product surface.

It may eventually:

- interpret natural language;
- produce candidate temporal intents;
- explain uncertainty/alternatives;
- propose plan changes;
- operate on selected-item context;
- request semantic commands through approved application boundaries.

It must **not** be implemented by turning Timeline `+` into a chat or generic intent interpreter.

C1's `TemporalCreateFieldSeed` is a deterministic manual-prefill mechanism for the manual Create flow. It is not the AI input boundary and does not require future DANTE to enter the same form/session.

A future DANTE vertical may reuse compatible downstream application/domain/backend commands where that vertical's own semantics and governance require them. It must not automate the manual form by clicking controls.

### Voice

Voice is an alternative input channel owned by its own future/global vertical.

Voice capture, transcription, interpretation, ambiguity resolution and confirmation are outside Timeline C1. A future voice vertical may eventually converge on appropriate downstream semantic operations; it does not turn C1 into a voice surface.

### Backend / persistence / solver

Real API, PostgreSQL mutations, provider synchronization and production solver integration are outside this roadmap's stop line.

Frontend work must stop at explicit ports/adapters with truthful local behavior. No invented endpoint, ORM row or fake durable-server state.

### Notifications / Review / global Resolution orchestration

Timeline may expose handoff state/intents. Global notification delivery, review scheduling and cross-product Resolution orchestration remain separate capabilities unless explicitly moved into this workstream.

### Goal / Program / World / Project verticals

Timeline may render links/projections and emit navigation/operation intents for these concepts. Their independent CRUD/domain UI belongs to their own verticals.

C1 establishes a typed external-owner handoff registry whose current targets remain explicitly `deferred`; handoff preserves a normalized immutable draft snapshot without fabricating a route or success state.

**Dependency rule:** if another vertical is unavailable, finish the Timeline-owned seam and expose dependency truthfully; do not duplicate the external vertical.

---

# 5. Roadmap

## T1 — Existing Timeline final hardening and freeze

**Current status:** **FROZEN / CLOSED.**

### Goal

Close the accepted Phase-1 Timeline as a genuinely reliable production-grade interaction baseline before expanding capability depth.

T1 is hardening, not redesign.

### Frozen behavior

The baseline protects:

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
- reduced-motion coverage;
- no-op mutation truth.

### Exit gate — satisfied

```text
T1 = FROZEN / PASS
```

Do not weaken `timeline-t1-frozen-contract.md` to accept drift.

---

## F0 — Minimal shared temporal application foundation

**Current status:** **FROZEN / CLOSED** at `7034b9b0d100709785ebe96e3816aab3e7b1d1f8`.

### Goal

Provide only the reusable frontend seams required so later capabilities do not mutate fixture/component state in private incompatible ways.

### Frozen primitives

- stable temporal projection/item identity;
- query/read boundary;
- typed semantic intent/command boundary;
- operation request/result model;
- draft vs accepted projection state;
- validation/error representation;
- expected-state/conflict representation where required;
- Undo/recovery contract;
- clock abstraction;
- deterministic local adapter;
- clean separation of View Model, frontend application model, future DTO and Domain/persistence model.

Permanent F0 non-collapse rules include:

```text
ViewModel != app projection != DTO != DB row
date-only != floating local != zoned exact != absolute instant
source/intention != placement
Schedule != Session != Actual
proposal != accepted effect
pending != success
no-op != mutation
retry != duplicate
Undo != blind overwrite
```

### Exit gate — satisfied

F0 supports real Create without direct component mutation shortcuts and without backend-shaped abstractions.

---

## C1 — `+` / Manual Create to production depth

**Current status:** **IMPLEMENTATION COMPLETE / AUTOMATED FULL PASS / USER MANUAL ACCEPTANCE PENDING.**

**Final implementation candidate:** `f092a3db2fbac28421b73e0629f7b4b83a1b0aec`  
**Automated CI:** `33631013598` / #621 — FULL PASS  
**Expanded authoritative scope:** `temporal-create-c1-scope-amendment.md`  
**Final mapping/evidence:** `temporal-create-c1-traceability.md`

### Goal

Turn Timeline `+` into the highest-quality **manual insertion/authoring** capability useful before backend integration, while preserving a fast common path and DANTE's deeper temporal semantics.

C1 is not a chat, natural-language command surface or AI/voice entry point.

### Manual entry topology

```text
Timeline +
Timeline double-click
Timeline Shift-drag/range
        ↓
deterministic structured manual prefill
        ↓
one shared Create draft/session
        ↓
Quick ↔ Expanded ↔ Full
        ↓
normalize / validate / candidate preview
        ↓
explicit user commit
        ↓
F0 application command
        ↓
deterministic local adapter
```

### Progressive foundation

- title-first Quick Create;
- Event vs Activity distinction;
- date/start/end/duration as applicable;
- all-day/date-span forms;
- Context assignment;
- optional notes;
- Quick vs Expanded vs Full progressive disclosure;
- dirty/cancel/discard behavior;
- deterministic validation;
- keyboard/focus/pointer/touch behavior;
- responsive overlay/full-screen strategy;
- unavailable external capabilities shown truthfully;
- local-adapter operation result and Undo/recovery.

### Activity depth

Activity authors, where applicable:

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
- Context/notes;
- external-owner handoff.

Persistent repetition **does not** live on Activity. CP6 recurrence ownership is Routine/Event; repeated Activity intent therefore hands off to Routine. Do not reintroduce `Activity.repeat` or an Activity recurrence editor.

Flexible Activity intent does not fabricate an accepted exact Schedule.

### Event depth

Event authors:

- timed/all-day multi-day placement;
- start/end/duration;
- floating-local/named-zone time semantics and IANA timezone;
- location/availability/visibility;
- purpose/expected outcome/agenda/decision intent;
- participants/resources/pre-read/conference intent;
- preparation/recovery buffers;
- confirmation/reminder policy;
- all four CP6 recurrence families.

Event recurrence includes:

- calendar daily/weekly/monthly/monthly-ordinal/yearly;
- elapsed interval;
- quota day/week/month/year with frame/week-start/zone;
- cyclic day/week patterns with multiple active positions;
- open/until/count termination.

C1 stores recurrence specification only. Backend M6 owns recurrence evaluator/Occurrence generation and exact governing recurrence-state binding.

### Context / appearance depth

C1 now supports an optional per-item visual override without collapsing it into Context/group semantics.

```text
Context/group membership
→ organization + grouping + filtering
→ inherited default visual tone

appearance override
→ presentation only
→ never changes Context/group/filter membership
```

Manual appearance colors use stable color words independent from Context labels: Purple/Cyan/Green/Amber/Pink/Red and IT equivalents.

### Application hardening

C1 includes:

- deterministic structured manual prefill;
- typed external-owner handoff registry with immutable normalized draft snapshot;
- rich-intent idempotency layered over F0 minimal command idempotency;
- normalized deep-frozen prepared specification at application boundary;
- candidate preview separate from accepted projection;
- provider actions as intent only;
- truthful local Undo/reveal/focus;
- accessibility, i18n and mobile full-screen protection.

### Explicit non-scope

Do not put into C1:

- DANTE/AI interpretation;
- natural-language parsing;
- voice capture/interpretation;
- external-owner CRUD;
- backend persistence;
- provider execution;
- authoritative solver/evaluator;
- Actual/Session runtime.

Future DANTE/voice verticals may share compatible **downstream semantic operations**, not the C1 form as an input framework.

### C1 automated gate — satisfied

CI #621 proves:

- Quality PASS;
- Mobile Bundle PASS;
- full Chromium Web E2E PASS;
- frozen Timeline Firefox contract PASS;
- Frontend CI Gate PASS.

Measured on the implementation candidate:

- architecture: **214 modules / 522 dependencies / zero violations**;
- web unit: **34 files / 183 tests**;
- Home route: **268.40 kB raw / 90.13 kB gzip**.

### C1 freeze criterion — one human gate remains

C1 becomes `FROZEN / CLOSED` only after:

1. final documentation descendant is CI-green;
2. user executes `temporal-create-c1-manual-acceptance.md`;
3. user explicitly approves the complete experience.

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
Context / organization
Appearance where relevant
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
- proper unavailable/error/recovery states under local adapter simulation;
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

**Invariant:** manual editor/drag/keyboard flows use the same downstream semantic operation grammar. Future AI/voice verticals may request compatible operations at that downstream boundary, but they remain separate input surfaces and must not be routed through the manual C1 form.

---

## C4 — Groups, filters, views and user preferences

### Goal

Take the already-useful grouping/view controls from prototype-grade local behavior to product-grade temporal organization.

### Scope

- selected Context/calendar visibility;
- grouped vs unified chronology;
- ordering;
- focus combinations;
- preserved frontend preference boundary;
- hidden-conflict/affected-count awareness;
- empty/filtered states;
- accessible non-color-only recognition;
- dense-day legibility;
- responsive fallback when wide grouped columns are impossible;
- explicit preservation of `appearance override != group/filter membership`.

Sharing is not a calendar group and must not be modeled as one.

---

## C5 — Recurrence and scheduling flexibility

### Goal

Expose DANTE's temporal rules without reducing them to a single `fixed/flexible` switch or simplistic recurrence editor.

C1 owns **initial manual creation-time** scheduling/recurrence authoring. C5 remains responsible for deeper editing/management of existing items and source/occurrence scope.

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
- source Routine/Program/series when owning vertical supports it.

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

Build frontend mechanics required for governed replanning before any production solver/AI is connected.

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

A future solver or AI provider may generate candidates. It does not own application of accepted effects and does not turn C1 manual Create into its UI.

---

## W1 — Dedicated temporal workspace architecture proof

### Goal

Prove temporal application capability is reusable outside Home without stretching the Home Timeline renderer into a giant page.

### First proof

- dedicated route/surface;
- full Day projection;
- first useful Week/planning projection;
- shared selection/Detail;
- shared create/edit/move application commands;
- flexible/unscheduled area when C5/C7 supports it;
- same temporal semantics/store capability;
- different renderer/layout allowed.

### Rule

```text
shared semantics/application capability
!= forced shared DOM/CSS renderer
```

---

## W2 — Dedicated workspace depth

After W1 proves architecture, expand only validated planning needs:

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

Close Timeline-owned downstream contracts for capabilities whose runtime/input surface belongs to another vertical.

May include, when needed:

- AI candidate-intent/result integration **outside C1 manual UI**;
- selected-item context handoff to a DANTE vertical;
- future voice vertical operations;
- Global Search/navigation integration;
- Notification/Review/Resolution handoff;
- Goal/Program/Project/World navigation links;
- external calendar/provider source indicators.

C1's reusable lessons are application command truth, immutable snapshots, validation, preview/accepted separation and typed owner handoff. Its manual prefill seed is **not** automatically the external AI/voice contract.

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
- external-vertical seams explicit;
- manual UI boundaries not generalized into speculative AI frameworks.

### Behavior gates

For implemented capabilities:

- create/edit/move/undo;
- Detail;
- recurrence/flexibility;
- execution/Actual/confirmation;
- conflict/proposal/replan;
- workspace projections;
- downstream semantic consistency across manual and future external callers without forcing shared input UI.

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
- bundle/route-split review based on measurement.

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

At this point no production backend is claimed, no provider integration is fabricated and no future DB/API implementation is invented inside frontend.

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

Current branch lineage starts from H0 frozen base:

`98b486a308961022ba0d8f43bb79339518457741`

Current state:

```text
T1    FROZEN / CLOSED
F0    FROZEN / CLOSED
C1    IMPLEMENTATION COMPLETE
      AUTOMATED FULL PASS (#621)
      DOCUMENTATION DESCENDANT VALIDATION PENDING
      USER MANUAL ACCEPTANCE PENDING
C2    BLOCKED UNTIL EXPLICIT C1 USER PASS
```

Immediate sequence:

1. complete documentation reconciliation on a descendant of implementation candidate `f092a3db...`;
2. require that final documentation descendant to pass Frontend CI completely;
3. user syncs `feature/home-timeline` locally once;
4. user executes the one final protocol in `temporal-create-c1-manual-acceptance.md`;
5. any demonstrated defect reopens only necessary C1 contract;
6. explicit `C1 MANUAL PASS — APPROVED` freezes/closes C1;
7. only then start C2 Card → structured Detail.

The former `T1-A` current-stage instruction, old “do not activate + yet” instruction and any old statement that DANTE/NL/voice must enter through C1 Create are historical and superseded by this roadmap.
