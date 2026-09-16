# Timeline / Temporal-Operational Vertical — Implementation Roadmap

- **Status:** CURRENT EXECUTION ROADMAP — reconciled 2026-09-16
- **Branch/workstream:** `feature/timeline-temporal-operational`
- **Current completed frontier:** B02 Schedule Core ✅ CLOSED / PROVEN
- **Next implementation block:** B03 Event Core — not started
- **Current candidate DB authority:** PostgreSQL 18.6 / Alembic `20260915_26`
- **Live progress ledger:** `docs/workstreams/timeline-temporal-operational-map.md`
- **B02 closure evidence:** `docs/workstreams/timeline-temporal-operational-b02-closure-2026-09-16.md`
- **Historical frozen roadmap:** `docs/workstreams/archive/timeline-temporal-operational-roadmap-freeze-2026-09-07.md`
- **Historical map/ledger snapshot:** `docs/workstreams/archive/timeline-temporal-operational-map-ledger-snapshot-2026-09-15.md`

The archived files preserve the pre-reconciliation wording and numbering for historical traceability only. This file is the current sequencing authority.

---

# 0. Fixed execution contract

Implementation remains slice-over-layer:

```text
semantic capability
→ current persistence inspection
→ DDL only if a real gap exists
→ backend/application operation/query
→ API/transport
→ frontend integration
→ read model/projection
→ automated tests
→ manual userTest where applicable
→ live ledger update
→ documentation reconciliation
```

Permanent rules:

```text
Domain != Logical != Physical != API DTO != frontend ViewModel
projection != canonical truth
planned/intended != happened
Activity != Event != Routine
Schedule != Temporal Constraint != Recurrence
Schedule != Session != Actual
Session != Actual != Outcome
Routine != Recurrence != Occurrence
provider identity != DANTE identity
proposal != accepted effect
pending != success
idempotency key != Domain identity
current != latest row
Undo != history rewind
```

A block is `✅ CLOSED / PROVEN` only after its applicable semantic, persistence, backend, frontend, test, manual and documentation gates are reconciled.

No runtime mock may replace backend truth after B00.

---

# 1. Current ordered roadmap

```text
B00 Real Data Spine                              ✅ CLOSED / PROVEN
B01 Activity Core                                ✅ CLOSED / PROVEN
B02 Schedule Core                                ✅ CLOSED / PROVEN
B03 Event Core                                   ⬜ NEXT
B04 Temporal Constraints + Movement Policy       ⬜
B05 Product Organization                         ⬜
B06 Routine / Recurrence / Occurrence Baseline   ⬜
B07 UI/UX Consolidation v1                       ⬜ NEW CHECKPOINT
B08 Session Runtime                              ⬜
B09 Responsibility / Participation               ⬜
B10 Actual / Outcome / Confirmation / Resolution ⬜
B11 Advanced Recurrence / Conditional / Reminder ⬜
B12 Replanning / Conflict / Solver               ⬜
B13 Provider / Offline / Multi-device             ⬜
B14 Analytics / Statistics / Signals             ⬜
B15 Whole Vertical Closure                       ⬜
```

Dependency thesis:

```text
REAL DATA SPINE
      ↓
ACTIVITY CORE
      ↓
SCHEDULE CORE
      ↓
EVENT CORE
      ↓
TEMPORAL CONSTRAINTS + PRODUCT ORGANIZATION
      ↓
ROUTINE / RECURRENCE / OCCURRENCE BASELINE
      ↓
UI/UX CONSOLIDATION v1
      ↓
SESSION RUNTIME
      ↓
ACTOR RELATIONS / PARTICIPATION
      ↓
ACTUAL / OUTCOME / CONFIRMATION / RESOLUTION
      ↓
ADVANCED RECURRENCE / CONDITIONAL POLICY / REMINDERS
      ↓
REPLANNING / CONFLICT / SOLVER
      ↓
PROVIDER / OFFLINE / MULTI-DEVICE
      ↓
ANALYTICS / SIGNALS
      ↓
WHOLE-VERTICAL CLOSURE
```

The UI/UX checkpoint is deliberately after B06: by then Activity, Event, Routine, Schedule, Constraints, organization, recurrence and Occurrence are known enough to redesign the creation/planning experience without repeatedly rebuilding the same surfaces.

---

# 2. Completed blocks

## B00 — Real Data Spine ✅

Established the real end-to-end product path:

```text
production web
→ authenticated backend
→ DanteContext / self Person
→ PostgreSQL
→ truthful normalized temporal read path
```

Normal runtime no longer relies on fake Timeline cards or fake persistence. Real empty/error/retry behavior and disposable full-stack E2E were proven.

## B01 — Activity Core ✅

Activated one canonical Activity owner with:

- stable identity;
- bounded descriptive/actionable state;
- governed idempotent create;
- real Planning Tray projection;
- valid unplaced state;
- reload/refetch identity stability;
- no generic `done`, `status`, `repeat`, `due_at` shortcuts.

Activity remains separate from Schedule, Session, Actual and Outcome.

## B02 — Schedule Core ✅

B02 is fully closed by `timeline-temporal-operational-b02-closure-2026-09-16.md`.

Activated Schedule for Activity with all accepted placement forms:

```text
date_span
floating_local
named_zone_local
absolute
coarse_local_period
```

Proven behavior includes:

- Planning Tray → Timeline placement;
- accepted Schedule creation;
- exact revision/move;
- cross-form revision;
- explicit current MaterialState binding;
- monotonic history;
- stable Schedule identity;
- unschedule without deletion;
- guarded Undo without DB rewind;
- idempotency and reuse conflict;
- expected-state/CAS conflict;
- DST/local-day semantics;
- named-zone source intent retention;
- coarse precision without fabricated exact clock time;
- cross-midnight one-Schedule identity;
- real Chromium and Firefox full-stack proof;
- Database Dictionary / SQLAlchemy / Alembic `_26` reconciliation.

B02 does not create Session/Actual truth and does not authorize Event behavior.

---

# 3. B03 — Event Core using shared Schedule

## Objective

Implement Event as a distinct originating owner and prove B02 Schedule is genuinely shared rather than Activity-specific.

## Required product/semantic scope

- Event identity/expectation;
- timed Event;
- all-day/date-span Event;
- multi-day Event;
- current Schedule + historical expectation;
- postponed/TBD with no fake placeholder Schedule;
- Agenda/internal Event parts at their accepted level;
- preparation/follow-up relations only where semantically justified;
- Place/conference intent only through accepted relation/profile ownership;
- ordinary attendance `!= Session`;
- Event `!= Availability/Capacity Claim`.

## Shared-capability rule

```text
Activity ─┐
          ├→ one shared Schedule capability
Event ────┘
```

No `event_schedule` duplicate engine.

## Exit condition

Activity and Event are both real originating owners and Schedule survives two semantic owners without ontology or persistence duplication.

---

# 4. B04 — Temporal Constraints + Movement Policy

## Objective

Represent the difference between:

```text
Schedule            = accepted temporal assignment
Temporal Constraint = valid/preferred temporal space
Movement Policy     = governance for changing accepted placement
```

Initial scope includes earliest/latest bounds, deadlines with explicit constrained facet, hard/soft windows, duration/spacing constraints where required, and truthful conflict explanation.

Reality may violate a planning constraint; recording Actual must not be rejected merely to protect planner assumptions.

## Exit condition

Planning has typed admissibility/preference and movement governance suitable for later recurrence/replanning.

---

# 5. B05 — Product Organization: Calendar / Life Area + Tags

## Objective

Replace prototype grouping assumptions with real user-controlled product organization while preserving Domain separation.

Required boundaries:

```text
Life Area != Goal
Life Area != Plan
Life Area != Tag
Life Area != Place
Life Area != provider calendar
Context/grouping != appearance
```

Scope includes lifecycle of Life Areas, primary organization relation, secondary Tags, grouping/filtering, and accessible appearance metadata.

## Exit condition

Real temporal owners can be organized into user-defined areas such as Work, Health, Study or Photography without ontology shortcuts.

---

# 6. B06 — Routine + Recurrence + Occurrence baseline

## Objective

Activate Routine and the four CP6-materialized recurrence families end-to-end, with backend-governed Occurrence identity/materialization.

Baseline recurrence families:

```text
calendar_wall_clock
elapsed_interval
quota_per_period
cyclic_positional
```

Required distinctions include:

```text
Routine != Recurrence != Occurrence
this occurrence != this-and-future
skip occurrence != pause routine != end routine
structural exclusion != generated-and-skipped
browser recurrence preview != canonical generation
```

Occurrence identity must survive reschedule and retain its governing recurrence MaterialState where applicable.

## Exit condition

Routine and recurring Event generate/query/render real backend-governed Occurrences with correct series-edit boundaries.

---

# 7. B07 — UI/UX Consolidation v1

## Why this checkpoint exists

This is an explicit product-quality checkpoint inserted after B06. It does **not** reopen Domain/Logical/Physical semantics and does not permit replacing governed operations with frontend-only state.

By this point the primary creation/planning vocabulary is available:

```text
Activity
Event
Routine
Schedule
Temporal Constraints
Life Area / Calendar
Tags
Recurrence
Occurrence
Planning Tray
Timeline
```

That is the first stable point where a serious product UI can be designed without immediately being invalidated by missing macro concepts.

## Target

Bring the temporal product surface to roughly **60–70% mature product quality**, not final visual polish.

## Scope

### Information architecture

- simplify the Create hierarchy;
- progressive disclosure instead of showing every temporal control at once;
- clear separation of primary fields, planning, organization and advanced options;
- distinct Activity/Event/Routine authoring while reusing shared components where semantics match.

### Timeline / Planning Tray

- visual hierarchy and density;
- coherent cards and detail affordances;
- all-day/date-span/coarse/exact visual treatment;
- Planning Tray usability;
- overlap/readability;
- consistent loading/empty/error/conflict states.

### Design system consolidation

- typography hierarchy;
- spacing/layout tokens;
- inputs/selectors/buttons;
- modal/drawer/editor patterns;
- icons and state affordances;
- responsive breakpoints;
- mobile behavior;
- no semantic dependence on color alone.

### Interaction/accessibility

- preserve frozen T1/F0 behavior;
- keyboard/focus grammar;
- pointer behavior in Chromium/Firefox;
- accessible labels/states;
- responsive/mobile acceptance.

## Hard boundary

```text
new UI
→ existing governed application operations
→ existing API contracts
→ canonical backend/database truth
```

The redesign must not invent new canonical meaning in ViewModel-only fields.

## Exit condition

Activity/Event/Routine creation, planning, recurrence, organization, Timeline and Planning Tray feel like one coherent product and provide a stable UI system for Session/Actual work.

This is **not** the final UI pass. A second consolidation naturally follows B10 when execution/resolution surfaces exist; final polish remains part of B15.

---

# 8. B08 — Session Runtime

## Objective

Make actual execution episodes real without conflating execution with plan or completion.

Scope includes:

- manual retrospective Session;
- spontaneous Session;
- start/pause/resume/end;
- Activity/Occurrence execution context;
- correction;
- split/merge with lineage;
- timing precision/provenance;
- overlap where semantically valid;
- stale-running handling;
- idempotent and expected-state-safe controls.

Permanent rule:

```text
Schedule = planned
Session  = executed episode
Session end != Activity/Occurrence completed
```

---

# 9. B09 — Responsibility / Participation / actor relations

## Objective

Introduce exact actor relations without ambiguous `assigned_to`/generic participant blobs.

Keep distinct:

```text
requester
responsible/accountable actor
expected performer
actual performer
Event participation response
Actual attendance
Acknowledgement
```

Also preserve `Person != Account != Principal != Actor`.

---

# 10. B10 — Actual + Outcome + Confirmation + Resolution Queue

## Objective

Close the expectation → reality → result → attestation loop.

```text
Schedule / expectation
        ↓
Session(s)
        ↓
Actual
        ↓
Outcome
        ↓
Confirmation where required
```

This is the block that gives user controls such as `Fatto`, `Parziale`, `Saltato`, `Posticipato`, `Sostituito`, `Conferma`, `Correggi` their real canonical meaning rather than mapping them to one generic status boolean.

`Da risolvere` becomes a derived Resolution Queue, not a notification feed or status table.

---

# 11. B11 — Advanced Recurrence + Conditional Policy + reminders

## Objective

Add recurrence forms that depend on real execution/reality facts and bounded conditional response behavior.

Includes completion-relative and anchor-stream-relative recurrence where physically justified, conditional activation semantics, review cadence, reminder intent and explicitly authorized automatic effects.

Reminder intent remains separate from external delivery success.

---

# 12. B12 — Replanning / Conflict / Solver

## Objective

Implement explainable, constraint-aware replanning after real Schedule, Constraints, policies and history exist.

The solver works on canonical current truth and emits candidates:

```text
candidate proposal != accepted Schedule
```

Apply requires authorization and expected-state revalidation. Hidden data must not leak through explanations.

---

# 13. B13 — Provider integration + Offline / Multi-device

## Objective

Synchronize external systems and disconnected clients with established DANTE semantics rather than designing DANTE around provider schemas.

Includes provider Event/Occurrence mapping, tombstones, reconciliation, unsupported recurrence handling, imported Session provenance, offline replay, multi-device expected-state conflicts and device clock drift.

No silent last-write-wins.

---

# 14. B14 — Analytics / Statistics / Signals

## Objective

Expose reproducible user-facing statistics derived from mature canonical temporal history.

Examples:

- scheduled vs actual duration;
- active/paused time;
- early/late/overrun/underrun;
- Schedule revision patterns;
- Occurrence/Actual coverage;
- Routine adherence;
- Life Area/tag time allocation;
- overlap-aware wall-clock statistics;
- day/week/month/year trends with correct timezone boundaries.

No universal productivity/success score without future explicit semantics.

---

# 15. B15 — Whole Vertical Closure

## Objective

Prove the entire temporal-operational vertical as one coherent production-quality capability.

Closure includes:

- master `!=` sweep;
- no generic ontology shortcuts;
- backend/PostgreSQL/API/frontend/full-stack regression;
- timezone/DST;
- idempotency/concurrency;
- recurrence/Occurrence history;
- Session multi-device/offline for activated surfaces;
- privacy/visibility/non-interference;
- provider/reconciliation;
- recovery/anti-resurrection;
- query/performance review;
- Alembic/SQLAlchemy/Dictionary parity;
- ACL proof;
- desktop/mobile/accessibility acceptance;
- documentation drift audit;
- final UI polish.

---

# 16. Numbering reconciliation

The UI/UX checkpoint was inserted on 2026-09-16 after B06. Historical dated documents created before this decision may contain the old numbering; their labels describe historical planning state only.

Current crosswalk:

```text
OLD B07 Session Runtime                     → CURRENT B08
OLD B08 Responsibility / Participation      → CURRENT B09
OLD B09 Actual / Outcome / Confirmation     → CURRENT B10
OLD B10 Advanced Recurrence / Conditional   → CURRENT B11
OLD B11 Replanning / Solver                 → CURRENT B12
OLD B12 Provider / Offline / Multi-device   → CURRENT B13
OLD B13 Analytics / Signals                 → CURRENT B14
OLD B14 Whole Vertical Closure              → CURRENT B15
```

Current canonical documentation must use the new numbering. Historical snapshots are explicitly under `docs/workstreams/archive/` and are not current execution authority.

---

# 17. Current execution state

```text
B00 REAL DATA SPINE                           ✅ CLOSED / PROVEN
B01 ACTIVITY CORE                             ✅ CLOSED / PROVEN
B02 SCHEDULE CORE                             ✅ CLOSED / PROVEN
DATABASE / DICTIONARY                         ✅ reconciled through Alembic _26 for B02
B02 MANUAL userTest                           ✅ APPROVED — 2026-09-15
B02-E FULL-STACK CHROMIUM                     ✅ 2 / 2 PASS — 2026-09-16
B02-E FULL-STACK FIREFOX                      ✅ 2 / 2 PASS — 2026-09-16
B03 EVENT CORE                                ⬜ NOT STARTED
NEXT EXECUTION GATE                           B03 PRE-SCOPE / authority re-open
```

B03 is the next roadmap target, but this roadmap update itself does not authorize B03 implementation.