# DANTE — Temporal Frontend Production-Depth Roadmap

**Status:** ACTIVE AUTHORITY — C1 AUTOMATED PASS / MANUAL ACCEPTANCE PENDING  
**Updated:** 2026-09-02  
**Workstream owner:** `feature/home-timeline`  
**Worktree:** `/home/mattia/projects/dante-timeline`  
**Integration target:** `feature/home-react`  
**Frozen common base:** `98b486a308961022ba0d8f43bb79339518457741` — H0 Whole Home Structural Freeze  
**F0 closed checkpoint:** `7034b9b0d100709785ebe96e3816aab3e7b1d1f8`  
**C1 final implementation candidate:** `81808814abb4e4998c7bde5b0c6cb8f5f903aa62`  
**C1 automated evidence:** Frontend CI `33613239926` / #536 — FULL PASS  
**Consumes:** `temporal-experience-architecture.md`, `timeline-t1-frozen-contract.md`, H0, Product V1 temporal documents/simulations, closed Domain/Logical/Physical semantics, CP6 PostgreSQL materialization and current frontend production standards  
**Scope stop:** maximum production-depth frontend capability up to explicit backend/API/provider/solver runtime boundaries

## 1. Workstream isolation

```text
feature/home-timeline
→ Home Timeline
→ shared temporal frontend application capability
→ Create / Detail / edit / execution / replan frontend flows
→ future dedicated temporal workspace
→ pre-backend temporal ports/adapters/tests/docs

feature/home-react
→ Mondi / Central Stage / World Focus
→ Home integration line

H0 / shared infrastructure
→ change-controlled integration surface
```

Timeline work must not casually reauthor HomeShell/AppShell, Central Stage, World Focus, global Home geometry, shared design tokens, shared i18n architecture or shared CI rules.

**Permanent rule:** temporal child capabilities consume H0; they do not renegotiate it.

## 2. Product objective

Timeline is not merely a polished calendar component. It is the temporal operating surface of DANTE.

It must preserve recoverable distinctions such as:

```text
Activity != Event
Occurrence != Schedule != Session != Actual
planned/intended != actual reality
recurrence source != generated Occurrence
Proposal != Decision != accepted effect
confirmation/provenance != outcome
calendar/context != sharing
AI output != canonical truth
```

The UI should hide unnecessary complexity through progressive disclosure, not destroy semantics in the application layer.

### Experience benchmark

Aim for:

- Google/Notion Calendar predictability and manual speed;
- Akiflow/Sunsama task-to-time fluency where useful;
- Motion/Reclaim adaptive-planning mechanics only where DANTE semantics justify them;
- Fantastical-class time/timezone maturity where relevant;
- stronger DANTE guarantees around accepted state, constraints, history, reversibility and planned-vs-actual truth.

Borrow interaction quality, not competitor ontology.

## 3. Delivery model

```text
bounded capability
→ product/domain alignment
→ frontend application boundary
→ complete UI states/interactions
→ accessibility/keyboard/touch
→ responsive/i18n
→ performance/cleanup
→ automated regression protection
→ traceability/docs
→ user manual PASS
→ freeze
→ next capability
```

A capability is not complete because a happy path renders.

Applicable production-depth gates include:

- semantic owner and contract;
- normal/empty/disabled/unavailable/validation/error states;
- pending/retry/recovery/reconciliation when meaningful;
- keyboard/focus;
- pointer/touch;
- responsive collision behavior;
- non-color-only communication;
- reduced motion;
- i18n-safe copy/layout;
- deterministic local truth before backend;
- cleanup of listeners/observers/timers/RAF;
- repeated-use/density pressure;
- unit/E2E/Firefox protection;
- no dead/fake/dangling affordance;
- documentation and freeze contract.

Build only abstractions justified by current or already-authoritative next flows.

## 4. External-vertical dependency policy

### DANTE intelligence / AI

AI runtime is an external vertical. Timeline/Create may define typed semantic input/proposal seams but must not implement a private AI stack or present fixtures as intelligence.

C1 now has a source-neutral structured Create seed. Future DANTE interpretation must feed that semantic boundary rather than script UI controls.

### Voice

Voice is an alternative input vertical. It must target the same semantic command/seed boundary; speech capture/provider runtime remains external.

### Backend / persistence / solver

Real API, PostgreSQL writes, production solver, recurrence evaluator and provider synchronization remain beyond the frontend stop line.

No component direct HTTP, fake DTO, fake durable state or browser-side Occurrence generation.

### Notifications / Review / Resolution

Timeline may author or expose intents/handoffs. Delivery/global orchestration remains outside unless explicitly assigned.

### Goal / Program / World / Project / Routine / other owners

Timeline/Create may carry typed owner handoff intent and preserve a draft snapshot. Independent CRUD belongs to the owning vertical.

C1 currently marks all external owner handoffs `deferred` rather than fabricating navigation/success.

---

# 5. Roadmap

## T1 — Existing Timeline hardening and freeze

**Status:** FROZEN / CLOSED.

Protected baseline includes:

- continuous bounded multi-day stream;
- viewed-date navigation / `Ora`;
- semantic zoom/density;
- deterministic overlap geometry;
- custom pointer drag without native ghost;
- first-gesture correctness across focused cards;
- same/cross-day movement;
- duration/day bounds;
- real-mutation Undo;
- no-op mutation truth;
- keyboard movement;
- group filtering/reorder;
- calendar/time popovers and focus restoration;
- reduced-motion imperative navigation;
- responsive H0 behavior;
- Chromium + frozen Firefox contract;
- cleanup guards.

Do not alter T1 merely to simplify later capabilities.

---

## F0 — Shared temporal application foundation

**Status:** FROZEN / CLOSED at `7034b9b0d100709785ebe96e3816aab3e7b1d1f8`.

Provides:

- stable projection/operation/Undo identities;
- clock;
- typed temporal placements including date-span, floating-local, zoned and absolute;
- typed command/result/query boundary;
- immutable drafts/projections;
- deterministic validation;
- exact operation idempotency;
- optimistic revision/expected-state semantics;
- Undo/recovery contract;
- deterministic in-memory workspace;
- subscriber isolation;
- no fake network/storage.

Permanent:

`ViewModel != application projection != DTO != DB row`.

---

## C1 — `+` / Temporal Create to production depth

**Status:** IMPLEMENTATION COMPLETE / AUTOMATED PASS / USER MANUAL ACCEPTANCE PENDING.

**Final implementation candidate:** `81808814abb4e4998c7bde5b0c6cb8f5f903aa62`  
**CI:** #536 / `33613239926` FULL PASS.

The detailed expanded contract is owned by `temporal-create-c1-scope-amendment.md`; exact implementation mapping is in `temporal-create-c1-traceability.md`.

### Final C1 capability

One shared Create system:

```text
Timeline +
double-click
Shift-drag range
future semantic seed callers
        ↓
shared draft
        ↓
Quick ↔ Expanded ↔ Full
        ↓
normalize / validate / preview
        ↓
explicit commit
        ↓
F0 command / local deterministic adapter
```

### Activity

Creation-time authoring covers:

- timed/all-day/unscheduled where appropriate;
- exact expected duration;
- open/window/deadline/preferred scheduling intent;
- movement/replanning policy;
- split/min/max session intent;
- preparation/recovery/spacing;
- fallback policy;
- confirmation/review/reminder intent;
- context/notes;
- external owner handoff.

**Activity does not own recurrence.** Persistent repetition hands off to Routine.

### Event

Creation-time authoring covers:

- timed/all-day multi-day placement;
- floating-local / named-zone time;
- timezone;
- location/availability/visibility;
- purpose/outcome/agenda/decision intent;
- participants/resources/pre-read/conference intent;
- buffers;
- confirmation/reminder policy;
- all four CP6 recurrence families.

Recurrence depth includes calendar daily/weekly/monthly/monthly-ordinal/yearly, elapsed interval, quota per day/week/month/year with frame/week-start/zone, and multi-position cyclic patterns.

### C1 integration seams

- structured source-neutral field seed for future global Create/keyboard/import/DANTE;
- typed owner registry and immutable handoff draft snapshot;
- rich-intent idempotency;
- application-boundary normalized immutable prepared snapshot;
- provider actions remain intent only;
- recurrence evaluator/Occurrence generation remain backend-only.

### C1 automated gate

PASS:

- Quality;
- Mobile Bundle;
- full Chromium E2E;
- frozen Timeline Firefox E2E;
- final Frontend CI Gate.

Measured:

- architecture 199 modules / 477 dependencies / 0 violations;
- web unit 28 files / 168 tests;
- Home route 252.22 kB raw / 86.38 kB gzip.

### C1 final gate

Only `temporal-create-c1-manual-acceptance.md` remains.

Do **not** start C2 before explicit user PASS.

---

## C2 — Card → structured Detail to production depth

**Status:** NEXT AFTER C1 FREEZE — NOT STARTED.

### Goal

Replace the current demonstration Detail with a real DANTE contextual Detail while resting Timeline cards remain calm.

Use a composable Detail shell, not one universal nullable mega-object.

Candidate sections only when semantically applicable:

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

Required behaviors:

- direct card/title entry consistent with frozen T1;
- progressive disclosure;
- shared temporal commands;
- proper loading/unavailable/error states;
- focus ownership/restoration;
- deep keyboard usage;
- responsive panel/sheet/modal behavior;
- long/dense content stress;
- no duplicated information wall.

Freeze criterion: simple appointment remains simple while rich structured items can expose real depth.

---

## C3 — Temporal edit / move / resize

Goal: every placement edit converges on one semantic operation path.

Scope:

- precise time editor;
- drag/cross-day move;
- resize/duration when product-approved;
- keyboard/pointer/touch alternatives;
- snap/precision/day bounds;
- all-day/date-span transitions when legitimate;
- timezone-aware edit;
- validation/conflict preview;
- no-op truth;
- optimistic rollback/recovery;
- Undo.

**Invariant:** drag, editor, keyboard and future DANTE/voice requests converge on the same semantic operation grammar.

---

## C4 — Groups, filters, views and preferences

Scope:

- calendar/life-area visibility;
- grouped vs unified chronology;
- ordering/focus combinations;
- frontend preference boundary;
- hidden-conflict/affected-count awareness;
- filtered/empty states;
- non-color recognition;
- dense-day legibility;
- responsive fallback.

Sharing is not a calendar group.

---

## C5 — Existing-item recurrence and scheduling flexibility

C1 owns initial creation-time authoring. C5 owns later management/edit scope.

Scope includes:

- existing fixed/window/deadline/preferred/open constraints;
- movement/replanning rules;
- occurrence vs source scope;
- this occurrence / selected / future / source changes when authoritative;
- richer recurrence state/history presentation;
- source revision without rewriting historical generated Occurrences.

The UI must distinguish editing one Occurrence from changing its source recurrence.

---

## C6 — Execution, Session, Actual and Confirmation

Goal: represent what happened separately from what was planned.

As applicable:

- in progress;
- unconfirmed after expected time;
- completed/partial/skipped/missed/not-completed;
- postponed/replaced/cancelled;
- reopened/corrected;
- actual start/end/duration;
- actual quantities/measurements;
- confirmation/provenance;
- lightweight direct actions;
- Detail escalation;
- global Resolution handoff.

A passed time window never silently proves completion except under an explicit accepted rule.

---

## C7 — Conflict, proposal and replanning experience

Scope:

- conflict representation;
- hard vs soft constraint;
- candidate plan distinct from accepted plan;
- affected-item preview;
- smallest-valid replan scope;
- infeasible outcome;
- accept/modify/reject;
- confirmation;
- Undo/recovery;
- protected-constraint/consequence explanation;
- future authoritative solver seam.

Solver/AI may generate candidates later; they do not own acceptance/application of effects.

---

## W1 — Dedicated temporal workspace architecture proof

Goal: prove temporal semantics/application capability is reusable outside Home without forcing reuse of the Home DOM/CSS renderer.

First proof:

- dedicated surface/route;
- full Day projection;
- useful Week/planning projection;
- shared selection/Detail;
- shared create/edit/move commands;
- flexible/unscheduled area when later phases support it;
- same application capability/store;
- renderer/layout may differ.

```text
shared semantics/application capability
!= forced shared renderer
```

---

## W2 — Dedicated workspace depth

After W1 proof, expand only validated needs:

- richer Day/Week/Month/Agenda;
- grouped/focus views;
- multi-select/bulk;
- timezone controls;
- flexible/unscheduled tray;
- broader horizon/load inspection;
- recurrence edit;
- proposal/replan mode.

Long horizons must change abstraction rather than render hundreds of miniature rich days.

---

## X1 — External integration seams

Goal: close Timeline-owned contracts for external runtimes.

May include:

- DANTE candidate-intent input;
- contextual selected-item scope;
- voice input;
- Global Search/Create entry;
- Notification/Review/Resolution handoff;
- Goal/Program/Project/World/Routine owner links;
- external calendar/provider indicators.

C1 already proves the seed and owner-handoff patterns. Later seams should extend those patterns rather than invent private integration mechanisms.

Missing verticals remain explicitly unavailable/deferred.

---

## P0 — Production hardening and pre-backend freeze

### Architecture gates

- no component direct HTTP;
- no DTO/persistence leakage;
- no universal Thing/Event collapse;
- no duplicate Home/workspace temporal stores;
- stable public exports;
- architecture/dependency checks green;
- external vertical seams explicit.

### Behavior gates

For implemented capabilities:

- create/edit/move/Undo;
- Detail;
- recurrence/flexibility;
- execution/Actual/confirmation;
- conflict/proposal/replan;
- workspace projections;
- manual/external-command semantic equivalence.

### Accessibility gates

- keyboard reachability;
- deterministic focus ownership/restoration;
- screen-reader semantics;
- non-color-only state;
- WCAG 2.2 AA target;
- reduced motion including JS motion;
- touch targets/mobile alternatives.

### Performance gates

- dense-day/multi-day/week stress;
- fluid scroll/zoom/drag;
- bounded rendering/windowing;
- no uncontrolled layout thrash;
- listener/observer/RAF/timer cleanup;
- repeated-open memory pressure;
- route/bundle review based on measurement.

### Stop condition

```text
React / renderers
        ↓
Temporal frontend application capability
        ↓
Explicit temporal ports
        ↓
Truthful deterministic local adapter
        ║
        ║ STOP — backend vertical begins after explicit gate
        ║
Future backend adapter / API / PostgreSQL / providers / solver
```

No production backend is claimed before that separate vertical.

## 6. Integration discipline

Do not continuously merge `feature/home-timeline` and `feature/home-react` back and forth.

Normal flow:

```text
feature/home-react
→ Mondi/World Focus progresses independently

feature/home-timeline
→ Timeline capability progresses independently

capability reaches accepted frozen checkpoint
→ intentional integration
→ combined H0 + Mondi + Timeline validation
```

Shared changes must be small, explicit and justified. Never reset/discard another workstream to simplify integration.

## 7. Current execution point

```text
T1    FROZEN / CLOSED
F0    FROZEN / CLOSED
C1    IMPLEMENTATION COMPLETE / AUTOMATED PASS
      USER MANUAL ACCEPTANCE PENDING
C2    BLOCKED UNTIL C1 USER PASS
```

Immediate next action:

1. documentation descendant must pass Frontend CI;
2. user performs the single final C1 manual acceptance;
3. explicit PASS freezes C1;
4. only then begin C2.

Do not return to old `T1-A` or “activate + later” instructions from earlier roadmap revisions; those are superseded by the current completed progression recorded here.