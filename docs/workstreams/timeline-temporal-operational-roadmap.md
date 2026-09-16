# Timeline / Temporal-Operational Vertical — Implementation Roadmap

- **Status:** CURRENT EXECUTION ROADMAP — reconciled 2026-09-16
- **Branch/workstream:** `feature/timeline-temporal-operational`
- **Current completed frontier:** B02 Schedule Core ✅ CLOSED / PROVEN
- **Current active block:** B03 Event Core — PRE-SCOPE ✅ COMPLETE / implementation pending
- **Next implementation gate:** `APPROVE B03-A`
- **Current candidate DB authority:** PostgreSQL 18.6 / Alembic `20260915_26`
- **Live progress ledger:** `docs/workstreams/timeline-temporal-operational-map.md`
- **B02 closure evidence:** `docs/workstreams/timeline-temporal-operational-b02-closure-2026-09-16.md`
- **B03 execution plan:** `docs/workstreams/timeline-temporal-operational-b03-execution-plan.md`
- **Historical frozen roadmap:** `docs/workstreams/archive/timeline-temporal-operational-roadmap-freeze-2026-09-07.md`
- **Historical map/ledger snapshots:** `docs/workstreams/archive/`

Archived files preserve historical wording/numbering only. This file is the current sequencing authority.

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

A block is `✅ CLOSED / PROVEN` only after its applicable semantic, persistence, backend, frontend, test, manual and documentation gates are reconciled. No runtime mock may replace backend truth after B00.

---

# 1. Current ordered roadmap

```text
B00 Real Data Spine                              ✅ CLOSED / PROVEN
B01 Activity Core                                ✅ CLOSED / PROVEN
B02 Schedule Core                                ✅ CLOSED / PROVEN
B03 Event Core                                   🟨 PRE-SCOPE COMPLETE / B03-A NEXT
B04 Temporal Constraints + Movement Policy       ⬜
B05 Product Organization                         ⬜
B06 Routine / Recurrence / Occurrence Baseline   ⬜
B07 UI/UX Consolidation v1                       ⬜
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

Activated one canonical Activity owner with stable identity, bounded descriptive/actionable state, governed idempotent create, real Planning Tray projection, valid unplaced state and reload/refetch identity stability. No generic `done`, `status`, `repeat` or `due_at` shortcut was introduced.

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

Proven behavior includes Planning Tray placement, accepted Schedule creation, revision/move, cross-form revision, explicit current MaterialState binding, monotonic history, stable Schedule identity, unschedule, guarded Undo, idempotency, CAS conflicts, DST/local-day semantics, named-zone source-intent retention, coarse precision, cross-midnight identity, Chromium/Firefox full-stack proof and Database Dictionary / SQLAlchemy / Alembic `_26` reconciliation.

B02 does not create Session/Actual truth.

---

# 3. B03 — Event Core using shared Schedule 🟨

## Objective

Implement Event as a distinct originating owner and prove B02 Schedule is genuinely shared rather than Activity-specific.

PRE-SCOPE is complete in `timeline-temporal-operational-b03-execution-plan.md`.

### Verified reuse

```text
Event NativeRef / EventRow                        EXISTS
Schedule Event physical eligibility              EXISTS
shared Schedule MaterialState/current/history    EXISTS / B02 PROVEN
frontend Event authoring prototype               EXISTS
```

### Verified gaps

```text
Event typed expectation descriptor               MISSING
Event idempotent create capability               MISSING
B02 Schedule runtime self-scope                  ACTIVITY-DESCRIPTOR BOUND
Timeline backend/API Event projection            MISSING
frontend Timeline Event protocol                 MISSING
Event Agenda canonical persistence               MISSING
```

## Required semantic scope

- Event identity/expectation;
- timed Event;
- all-day/date-span Event;
- multi-day Event;
- current Schedule + historical expectation;
- postponed/TBD with no fake placeholder Schedule;
- Agenda/internal Event parts at their accepted level;
- preparation/follow-up only where exact relation semantics are activated;
- ordinary attendance `!= Session`;
- Event `!= Availability/Capacity Claim`.

## Shared-capability rule

```text
Activity ─┐
          ├→ one shared Schedule capability
Event ────┘
```

No `event_schedule` duplicate engine.

## B03 implementation slices

```text
B03-A  Event canonical core
       typed Event expectation + create operation/capability + self ownership

B03-B  Shared Schedule + Event Timeline
       Activity/Event typed self-scope + atomic scheduled Event + timed/all-day/multi-day

B03-C  Event placement lifecycle
       reschedule + postponed/TBD + Event read/detail + guarded Undo

B03-D  Agenda/internal parts
       bounded ordered Event-internal persistence + real frontend integration

B03-E  closure
       PostgreSQL/API/frontend/E2E/manual + DB/Dictionary/docs reconciliation
```

Rich prototype concepts owned by later blocks remain fail-closed: recurrence B06, constraints B04, organization B05, Session B08, Participation B09, Actual/Outcome/Confirmation B10, reminders/policy B11 and providers B13.

## Current gate

```text
APPROVE B03-A
```

PRE-SCOPE completion itself does not authorize DDL/product implementation.

## Exit condition

Activity and Event are both real originating owners and Schedule survives two semantic owners without ontology or persistence duplication.

---

# 4. B04 — Temporal Constraints + Movement Policy

Represent the difference between accepted Schedule, valid/preferred temporal space and governance for changing placement. Initial scope covers typed earliest/latest bounds, deadlines with explicit facet, hard/soft windows, duration/spacing constraints where required and truthful conflict explanation. Reality may violate planning rules; Actual must remain recordable.

---

# 5. B05 — Product Organization: Calendar / Life Area + Tags

Replace prototype grouping assumptions with user-controlled product organization while preserving `Life Area != Goal/Plan/Tag/Place/provider calendar` and `Context/grouping != appearance`.

---

# 6. B06 — Routine + Recurrence + Occurrence baseline

Activate Routine and the four CP6-materialized recurrence families:

```text
calendar_wall_clock
elapsed_interval
quota_per_period
cyclic_positional
```

Backend owns canonical Occurrence generation/materialization; `Routine != Recurrence != Occurrence`, `this occurrence != this-and-future`, and browser preview never becomes canonical generation.

---

# 7. B07 — UI/UX Consolidation v1

Explicit 60–70% product-quality checkpoint after B06. It consolidates Create, Timeline, Planning Tray, cards/editors, responsive/mobile behavior, typography/spacing/components and progressive disclosure while preserving the governed backend/application contracts.

This is not final polish; a later consolidation follows execution/resolution surfaces and final polish belongs to B15.

---

# 8. B08 — Session Runtime

Make actual execution episodes real: manual/spontaneous Session, start/pause/resume/end, Activity/Occurrence context, correction, split/merge, timing precision, overlap, stale-running handling, idempotency and expected-state-safe controls.

```text
Schedule = planned
Session  = executed episode
Session end != Activity/Occurrence completed
```

---

# 9. B09 — Responsibility / Participation / actor relations

Introduce exact requester/responsible/expected performer/actual performer/Event participation/attendance relations without ambiguous `assigned_to` or participant blobs. Preserve `Person != Account != Principal != Actor`.

---

# 10. B10 — Actual + Outcome + Confirmation + Resolution Queue

Close expectation → reality → result → attestation. This is where user controls such as `Fatto`, `Parziale`, `Saltato`, `Posticipato`, `Sostituito`, `Conferma` and `Correggi` receive real canonical meaning instead of one generic status boolean. `Da risolvere` is derived, not a status table.

---

# 11. B11 — Advanced Recurrence + Conditional Policy + reminders

Add recurrence forms dependent on real execution/reality facts, bounded conditional activation, review cadence, reminder intent and explicitly authorized automatic effects. Reminder intent remains distinct from delivery success.

---

# 12. B12 — Replanning / Conflict / Solver

Implement explainable constraint-aware replanning on canonical current truth. Solver output is a candidate, never accepted Schedule until authorized and expected-state revalidated.

---

# 13. B13 — Provider integration + Offline / Multi-device

Synchronize external systems and disconnected clients with established DANTE semantics. Includes provider Event/Occurrence mapping, tombstones, reconciliation, imported Session provenance, offline replay, multi-device conflicts and device-clock drift. No silent last-write-wins.

---

# 14. B14 — Analytics / Statistics / Signals

Expose reproducible statistics from mature canonical history: scheduled vs actual duration, active/paused time, deviations, Schedule revisions, Occurrence/Actual coverage, Routine adherence, Life Area/tag allocation, overlap-aware time and timezone-correct trends. No universal productivity score without explicit semantics.

---

# 15. B15 — Whole Vertical Closure

Prove the entire temporal-operational vertical coherently: master `!=` sweep, no generic shortcuts, full backend/PostgreSQL/API/frontend/E2E regression, timezone/DST, idempotency/concurrency, recurrence history, Session multi-device/offline, privacy, providers, recovery, performance/query plans, DB parity/ACL, desktop/mobile/accessibility, documentation drift and final UI polish.

---

# 16. Numbering reconciliation

The UI/UX checkpoint was inserted on 2026-09-16 after B06. Current crosswalk:

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

Current canonical documentation uses the new numbering. Historical snapshots under `docs/workstreams/archive/` are evidence only.

---

# 17. Current execution state

```text
B00 REAL DATA SPINE                           ✅ CLOSED / PROVEN
B01 ACTIVITY CORE                             ✅ CLOSED / PROVEN
B02 SCHEDULE CORE                             ✅ CLOSED / PROVEN
DATABASE / DICTIONARY                         ✅ reconciled through Alembic _26 for B02
B03 PRE-SCOPE                                 ✅ COMPLETE — 2026-09-16
B03 EVT-001 authority re-open                 ✅ DONE
B03 IMPLEMENTATION                            ⬜ PENDING APPROVAL
NEXT EXECUTION GATE                           APPROVE B03-A
```

No B03 code/DDL or CI launch is authorized merely by this roadmap reconciliation.