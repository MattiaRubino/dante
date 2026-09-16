# Timeline / Temporal-Operational Vertical — Implementation Roadmap

- **Status:** CURRENT EXECUTION ROADMAP — reconciled 2026-09-16
- **Branch/workstream:** `feature/timeline-temporal-operational`
- **Current completed frontier:** B02 Schedule Core ✅ CLOSED / PROVEN
- **Current active block:** B03 Event Core — B03-A ✅ CLOSED / PROVEN
- **Next implementation gate:** `APPROVE B03-B`
- **Current candidate DB authority:** PostgreSQL 18.6 / Alembic `20260916_27`
- **Current candidate topology:** `98|5|29|78|195|115|288|0|0|0`
- **Live progress ledger:** `docs/workstreams/timeline-temporal-operational-map.md`
- **B02 closure evidence:** `docs/workstreams/timeline-temporal-operational-b02-closure-2026-09-16.md`
- **B03 plan:** `docs/workstreams/timeline-temporal-operational-b03-execution-plan.md`
- **B03-A closure:** `docs/workstreams/timeline-temporal-operational-b03-a-closure-2026-09-16.md`
- **Detailed semantic freeze:** `docs/workstreams/archive/timeline-temporal-operational-map-ledger-snapshot-2026-09-15.md`

The archived semantic freeze preserves the complete functionality and logic inventory. This document is the current sequencing authority.

---

# 0. Fixed execution contract

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
current accepted state != latest row
Undo != history rewind
```

A block closes only after its applicable semantic, persistence, backend, frontend, test, manual and documentation gates are reconciled.

---

# 1. Current ordered roadmap

```text
B00 Real Data Spine                              ✅ CLOSED / PROVEN
B01 Activity Core                                ✅ CLOSED / PROVEN
B02 Schedule Core                                ✅ CLOSED / PROVEN
B03 Event Core                                   🟨 B03-A CLOSED / B03-B NEXT
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

Dependency chain:

```text
REAL DATA SPINE
→ ACTIVITY CORE
→ SCHEDULE CORE
→ EVENT CORE
→ TEMPORAL CONSTRAINTS + PRODUCT ORGANIZATION
→ ROUTINE / RECURRENCE / OCCURRENCE BASELINE
→ UI/UX CONSOLIDATION v1
→ SESSION RUNTIME
→ ACTOR RELATIONS / PARTICIPATION
→ ACTUAL / OUTCOME / CONFIRMATION / RESOLUTION
→ ADVANCED RECURRENCE / CONDITIONAL POLICY / REMINDERS
→ REPLANNING / CONFLICT / SOLVER
→ PROVIDER / OFFLINE / MULTI-DEVICE
→ ANALYTICS / SIGNALS
→ WHOLE-VERTICAL CLOSURE
```

The UI/UX checkpoint deliberately remains after B06: Activity, Event, Routine, Schedule, Constraints, organization, Recurrence and Occurrence will then be known enough to redesign the planning experience once rather than repeatedly.

---

# 2. Completed blocks

## B00 — Real Data Spine ✅

Real authenticated frontend → backend → DanteContext/self Person → PostgreSQL path, truthful empty/error/retry behavior and disposable full-stack proof are established.

## B01 — Activity Core ✅

Canonical Activity identity, typed actionable-intention descriptor, governed idempotent create, Planning Tray/read projection and reload identity stability are established without generic Task/status/completion shortcuts.

## B02 — Schedule Core ✅

One shared Schedule identity/current/history machinery is proven for Activity across:

```text
date_span
floating_local
named_zone_local
absolute
coarse_local_period
```

B02 covers establish, revision, CAS, idempotency, history, Planning Tray placement, move/resize/editor, unschedule, guarded Undo, local-day/range query, DST/source-intent semantics and real Chromium/Firefox proof. Schedule remains distinct from Session/Actual.

---

# 3. B03 — Event Core using shared Schedule 🟨

## Objective

Activate Event as a distinct originating owner and prove that the B02 Schedule engine is truly shared rather than Activity-specific.

Target:

```text
Activity ─┐
          ├→ one shared Schedule owner/current/history capability
Event ────┘
```

No `event_schedule` duplicate engine is authorized.

## B03-A — Event canonical core ✅ CLOSED / PROVEN

Implemented at `_27`:

```text
event_expectation
event_create_operation
create_self_event(...)
TemporalEventApplication
POST /api/v1/temporal/events
GET  /api/v1/temporal/events/{event_ref}
```

Proven:

```text
stable UUIDv7 Event identity          ✅
self-Person ownership                 ✅
title persistence/reload              ✅
idempotent same-intent replay         ✅
changed-intent conflict               ✅
CSRF/self-scope isolation             ✅
Dictionary/SQLAlchemy/Alembic parity  ✅
canonical-data downgrade guard        ✅
```

B03-A did not activate Event Schedule, Timeline, UI or Agenda behavior.

## B03-B — Shared Schedule + Event Timeline ⬜ NEXT

Goal: prove Schedule survives a second semantic owner.

Required scope:

```text
1. typed self-subject authorization: Activity OR Event
2. no generic EAV/owner shortcut
3. no Event-specific Schedule tables
4. atomic Event + initial Schedule application operation
5. timed floating-local Event
6. timed named-zone Event
7. all-day/date-span Event
8. multi-day Event
9. Timeline backend/API Activity/Event discriminated union
10. strict TypeScript union/parser/rendering
11. activate minimal truthful Event Create surface
12. rerun Activity Schedule regressions
```

Exit proof:

```text
Activity and Event both use the same Schedule identity/current/history machinery
```

## B03-C — Event placement lifecycle ⬜

Reschedule through shared Schedule revision, postponed/TBD with no fake placeholder Schedule, stable Event identity, detail/read after Schedule absence, guarded Undo and historical expectation reconstruction.

## B03-D — Agenda/internal parts ⬜

Bounded ordered Event-internal persistence and real frontend create/read/reload. Agenda parts remain internal by default:

```text
Agenda part != Activity
Agenda part != Event
Agenda part != Occurrence
Agenda part != Session
Agenda part != Actual
```

## B03-E — Closure ⬜

PostgreSQL/API/frontend regressions, Activity+Event shared Schedule proof, real-stack Chromium, Firefox where affected, manual Event userTest, Dictionary/SQLAlchemy/Alembic/live-catalog reconciliation and map/roadmap/handoff closure.

Deferred beyond B03 remain explicit:

```text
Event recurrence                   → B06
Temporal Constraints               → B04
Life Area / Calendar / Tags        → B05
Session/execution                  → B08
participants / invitations         → B09
Actual / Outcome / Confirmation    → B10
reminders / conditional policy     → B11
provider conferencing / sync       → B13
```

---

# 4. B04 — Temporal Constraints + Movement Policy ⬜

Introduce temporal constraints as truth distinct from Schedule placement; establish movement/replanning policy foundations without silently mutating accepted plans.

# 5. B05 — Product Organization ⬜

Activate Calendar/Life Area, Tags and accepted grouping/context semantics without turning presentation organization into canonical temporal truth.

# 6. B06 — Routine / Recurrence / Occurrence Baseline ⬜

Activate Routine as originating owner, Recurrence as policy, Occurrence as generated instance, with strict `Routine != Recurrence != Occurrence` boundaries and accepted Event recurrence only here.

# 7. B07 — UI/UX Consolidation v1 ⬜

Dedicated product-quality checkpoint after B06. Target: roughly 60–70% polished planning experience while preserving established contracts.

Focus:

```text
Create information architecture
Activity / Event / Routine switching
Timeline + all-day lane
Planning Tray
cards/detail/drawers
Schedule editor
Life Area / Tags
Recurrence UX
spacing/type/component hierarchy
responsive/mobile
keyboard/focus
empty/loading/error states
```

This is a UI/application refactor, not permission to rewrite Domain/Persistence semantics.

# 8. B08 — Session Runtime ⬜

Real start/pause/resume/end execution runtime and Session timing. Session remains distinct from Schedule and Actual.

# 9. B09 — Responsibility / Participation ⬜

Actor relations, responsibility and participation/invitation boundaries. Attendance response is not automatically Actual attendance.

# 10. B10 — Actual / Outcome / Confirmation / Resolution ⬜

Record what really happened, resulting Outcome, confirmation/correction and Resolution Queue. This is where truthful product controls such as done/partial/not-done/confirm become canonically meaningful rather than decorative booleans.

# 11. B11 — Advanced Recurrence / Conditional / Reminder ⬜

Advanced recurrence policy, bounded conditional effects, reminders and review automation.

# 12. B12 — Replanning / Conflict / Solver ⬜

Conflict detection, candidate generation, solver/replanning explanation and governed acceptance; proposal remains distinct from accepted effect.

# 13. B13 — Provider / Offline / Multi-device ⬜

Provider identity/mapping, sync and conferencing boundaries plus offline/multi-device reconciliation. Provider state never becomes DANTE identity by convenience.

# 14. B14 — Analytics / Statistics / Signals ⬜

Derived analytics/signals over accepted canonical truth without turning projections/statistics into owners.

# 15. B15 — Whole Vertical Closure ⬜

Cross-block regression, recovery/anti-resurrection, operational hardening, full product acceptance and final documentation reconciliation.

---

# 16. Current gate

```text
B03-A  ✅ CLOSED / PROVEN
B03-B  ⬜ requires explicit approval
```

CI remains separate and requires explicit authorization.