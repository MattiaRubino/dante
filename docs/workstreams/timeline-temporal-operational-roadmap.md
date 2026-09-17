# Timeline / Temporal-Operational Vertical — Implementation Roadmap

- **Status:** CURRENT EXECUTION ROADMAP — reconciled 2026-09-17
- **Branch/workstream:** `feature/timeline-temporal-operational`
- **Current completed frontier:** B03-C Event placement lifecycle ✅ CLOSED / PROVEN
- **Current active block:** B03 Event Core
- **Next implementation gate:** `APPROVE B03-D`
- **Current candidate DB authority:** PostgreSQL 18.6 / Alembic `20260917_28`
- **Current candidate topology:** `98|5|29|78|195|115|288|0|0|0`
- **Live progress ledger:** `docs/workstreams/timeline-temporal-operational-map.md`
- **B02 closure evidence:** `docs/workstreams/timeline-temporal-operational-b02-closure-2026-09-16.md`
- **B03 plan:** `docs/workstreams/timeline-temporal-operational-b03-execution-plan.md`
- **B03-A closure:** `docs/workstreams/timeline-temporal-operational-b03-a-closure-2026-09-16.md`
- **B03-B closure:** `docs/workstreams/timeline-temporal-operational-b03-b-closure-2026-09-17.md`
- **B03-C closure:** `docs/workstreams/timeline-temporal-operational-b03-c-closure-2026-09-17.md`
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
B03 Event Core                                   🟨 B03-A + B03-B + B03-C CLOSED / B03-D NEXT
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

One shared Schedule identity/current/history machinery is proven for Activity across date-span, floating-local, named-zone-local, absolute and coarse-local-period, including establish/revision/CAS/idempotency/history/unschedule/guarded Undo/DST and real-stack proof.

---

# 3. B03 — Event Core using shared Schedule 🟨

## Objective

Activate Event as a distinct originating owner and prove that the B02 Schedule engine is truly shared rather than Activity-specific.

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

Stable UUIDv7 Event identity, self-Person ownership, persistence/reload, idempotent replay, changed-intent conflict, CSRF/self-scope, Dictionary/SQLAlchemy/Alembic parity and canonical-data downgrade guard are proven.

## B03-B — Shared Schedule + Event Timeline ✅ CLOSED / PROVEN

Implemented at `_28` without changing physical topology counts.

Accepted result:

```text
typed Activity OR Event Schedule self-authorization
single shared Schedule identity/current/history machinery
atomic Event + initial Schedule commit
floating-local Event
named-zone Event with explicit source/resolution semantics
all-day/date-span Event
multi-day Event
Timeline scheduled_activity | scheduled_event union
strict API + TypeScript parser/hydration
minimal truthful scheduled-Event Create surface
Activity Schedule regression preservation
Event Timeline remains read-only for lifecycle mutations until B03-C
```

Proof summary:

```text
PostgreSQL/API targeted selection      18 PASS / 4 FAIL first run
single _28 PL/pgSQL regression         fixed
exact failed selection rerun           4 PASS
Event transport/Timeline web           10 PASS
B03 Create-runtime web                  2 PASS
@dante/web typecheck                    PASS
```

Closure authority: `docs/workstreams/timeline-temporal-operational-b03-b-closure-2026-09-17.md`.

## B03-C — Event placement lifecycle ✅ CLOSED / PROVEN

B03-C activates Event placement lifecycle without adding another temporal engine.

Accepted behavior:

```text
reschedule through the shared Schedule revision capability
stable EventRef + ScheduleRef across revisions
monotonic placement MaterialState evolution
postponed/TBD = Event alive + Schedule/history retained + no current placement
no placeholder date/time
Event remains readable after current placement removal
stale expected-state changes fail closed
guarded Undo creates a new accepted MaterialState
Undo replay remains idempotent
newly-created Event supports lifecycle immediately without reload
Activity Schedule lifecycle remains unchanged
```

No new Alembic revision was needed: `_28` already contains the shared Activity/Event Schedule capability, so B03-C is an application/product activation over established canonical persistence rather than a schema duplication.

Proof summary:

```text
PostgreSQL/backend targeted gate       9 PASS / 2 deselected
Event lifecycle web gate               5 files / 16 PASS
@dante/web typecheck                   PASS
```

Closure authority: `docs/workstreams/timeline-temporal-operational-b03-c-closure-2026-09-17.md`.

The boundary remains explicit:

```text
Event expectation != current Schedule
current Schedule != future Actual
postponed/TBD Event != Planning Tray Activity
Undo != history rewind
```

Actual/Outcome/Confirmation truth remains B10-owned.

## B03-D — Agenda/internal parts ⬜ NEXT

Bounded ordered Event-internal persistence and real frontend create/read/reload. Agenda parts remain internal by default:

```text
Agenda part != Activity
Agenda part != Event
Agenda part != Occurrence
Agenda part != Session
Agenda part != Actual
```

B03-D must prove durable ordering/identity semantics only to the degree required by the accepted Event Agenda product behavior; it must not inflate Agenda parts into generic first-class temporal owners.

## B03-E — Closure ⬜

Whole-B03 PostgreSQL/API/frontend regressions, real-stack Chromium, Firefox where affected, manual Event userTest, Dictionary/SQLAlchemy/Alembic/live-catalog reconciliation and final map/roadmap/handoff closure.

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

Focus: Create IA, Activity/Event/Routine switching, Timeline/all-day lane, Planning Tray, detail/editor surfaces, organization, recurrence UX, responsive/mobile, keyboard/focus and truthful empty/loading/error states.

# 8. B08 — Session Runtime ⬜

Real start/pause/resume/end execution runtime and Session timing. Session remains distinct from Schedule and Actual.

# 9. B09 — Responsibility / Participation ⬜

Actor relations, responsibility and participation/invitation boundaries. Attendance response is not automatically Actual attendance.

# 10. B10 — Actual / Outcome / Confirmation / Resolution ⬜

Record what really happened, resulting Outcome, confirmation/correction and Resolution Queue.

# 11. B11 — Advanced Recurrence / Conditional / Reminder ⬜

Advanced recurrence policy, bounded conditional effects, reminders and review automation.

# 12. B12 — Replanning / Conflict / Solver ⬜

Conflict detection, candidate generation, solver/replanning explanation and governed acceptance; proposal remains distinct from accepted effect.

# 13. B13 — Provider / Offline / Multi-device ⬜

Provider identity/mapping, sync and conferencing boundaries plus offline/multi-device reconciliation.

# 14. B14 — Analytics / Statistics / Signals ⬜

Derived analytics/signals over accepted canonical truth without turning projections/statistics into owners.

# 15. B15 — Whole Vertical Closure ⬜

Cross-block regression, recovery/anti-resurrection, operational hardening, full product acceptance and final documentation reconciliation.

---

# 16. Current gate

```text
B03-A  ✅ CLOSED / PROVEN
B03-B  ✅ CLOSED / PROVEN
B03-C  ✅ CLOSED / PROVEN
B03-D  ⬜ NEXT / requires explicit approval
B03-E  ⬜
```

CI remains separate and requires explicit authorization.