# Timeline / Temporal-Operational — Workstream Handoff

- **Status:** B03-D ✅ CLOSED / PROVEN → B03-E NEXT
- **Reconciled:** 2026-09-17
- **Branch:** `feature/timeline-temporal-operational`
- **Current roadmap:** `docs/workstreams/timeline-temporal-operational-roadmap.md`
- **Current live map/ledger:** `docs/workstreams/timeline-temporal-operational-map.md`
- **B03 plan:** `docs/workstreams/timeline-temporal-operational-b03-execution-plan.md`
- **B03-A closure:** `docs/workstreams/timeline-temporal-operational-b03-a-closure-2026-09-16.md`
- **B03-B closure:** `docs/workstreams/timeline-temporal-operational-b03-b-closure-2026-09-17.md`
- **B03-C closure:** `docs/workstreams/timeline-temporal-operational-b03-c-closure-2026-09-17.md`
- **B03-D closure:** `docs/workstreams/timeline-temporal-operational-b03-d-closure-2026-09-17.md`
- **Next implementation gate:** `APPROVE B03-E`
- **CI:** no CI launch is implied or authorized

## 1. Current workstream position

```text
B00 Real Data Spine                              ✅ CLOSED / PROVEN
B01 Activity Core                                ✅ CLOSED / PROVEN
B02 Schedule Core                                ✅ CLOSED / PROVEN
B03 Event Core                                   🟨 B03-A/B/C/D CLOSED / B03-E NEXT
B04 Temporal Constraints + Movement Policy       ⬜
B05 Product Organization                         ⬜
B06 Routine / Recurrence / Occurrence Baseline   ⬜
B07 UI/UX Consolidation v1                       ⬜ planned after B06
B08 Session Runtime                              ⬜
B09 Responsibility / Participation               ⬜
B10 Actual / Outcome / Confirmation / Resolution ⬜
B11 Advanced Recurrence / Conditional / Reminder ⬜
B12 Replanning / Conflict / Solver               ⬜
B13 Provider / Offline / Multi-device             ⬜
B14 Analytics / Statistics / Signals             ⬜
B15 Whole Vertical Closure                       ⬜
```

Current candidate DB:

```text
PostgreSQL 18.6
Alembic     20260917_29
Topology    101|5|31|78|198|119|297|0|0|0
```

## 2. Accepted B03 foundation

B03-A established canonical Event identity/expectation/create/read.

B03-B proved Activity and Event use the same Schedule authority:

```text
Activity ─┐
          ├→ shared ScheduleRef / placement MaterialState / current/history
Event ────┘
```

B03-C activated Event placement lifecycle on that same machinery.

B03-D activated Event-internal Agenda values at `_29` without identity inflation.

## 3. Proven B03 behavior through B03-D

```text
canonical Event identity + expectation
idempotent self-scoped Event create
shared Activity OR Event Schedule authorization
atomic Event + initial Schedule creation
floating-local Event
named-zone-local Event with source/DST semantics
all-day/date-span Event
multi-day Event
Timeline scheduled_activity | scheduled_event union
strict API / TypeScript parser + hydration
minimal truthful Event Create runtime
Event reschedule through shared Schedule revision
postponed/TBD with no current placement and preserved Event/history
Event readability while current placement is absent
stale expected-state conflict protection
guarded Undo through a new MaterialState
idempotent Undo replay
immediate lifecycle after Event create without reload
ordered bounded Event Agenda values
Agenda add/edit/reorder/remove/reload
aggregate Agenda revision/CAS
Agenda operation-id idempotent replay
real Event-detail Agenda editor backed by backend truth
Activity Schedule regression preservation
no event_schedule table/current/history engine
no NativeRef per Agenda part
```

## 4. B03-D proof summary

```text
focused PostgreSQL/API Agenda               2 PASS
DB/Alembic/Dictionary gate                 12 PASS
B03-D affected web gate                     6 files / 19 PASS
@dante/i18n typecheck                       PASS
@dante/web typecheck                        PASS
final B02+B03 backend regression            13 PASS / 2 deselected
final Activity/Schedule/Event web regression 5 files / 26 PASS
```

The DB gate proves `_29` migration authority, current catalog/Dictionary parity, fresh single head and head→base→head roundtrip. The final regression gates prove B03-D did not regress B02 or B03-C.

## 5. Semantic boundaries still binding

```text
Activity != Event
Event != Schedule
Event != Recurrence
Event != Occurrence
Event != Session
Event != Actual
Event != Outcome
Event != Participation
Event != Availability / Capacity Claim
Event identity != provider identity
Agenda part != Activity/Event/Occurrence/Schedule/Session/Actual by default
original Event expectation != current Schedule
current Schedule != future Actual
postponed/TBD Event != Planning Tray Activity
projection != canonical truth
Undo != history rewind
```

## 6. Exact B03-E target

B03-E is **whole-B03 closure**, not a new feature slice.

Required work:

```text
1. run relevant whole-B03 backend/PostgreSQL regressions
2. run relevant broad frontend regressions
3. execute real-stack Chromium Event acceptance
4. execute Firefox critical interaction proof where affected
5. execute manual Event userTest
6. reconcile final Dictionary / SQLAlchemy / Alembic / live catalog evidence
7. close final B03 proof ledger
8. reconcile map / roadmap / handoff / global status docs
```

Expected real-stack scenarios include Event create, reschedule, all-day/date-span, multi-day, reload and interaction with the real Timeline/read model. Agenda must be represented where the accepted user path reaches it.

If B03-E exposes a concrete defect, fix the defect in the owning B03 capability. Otherwise do not widen B03 semantics.

## 7. Explicit stop lines

Do not activate during B03-E:

```text
Event recurrence                           → B06
Temporal Constraints / movement policy     → B04
Life Area / Calendar / Tags                → B05
Session/execution                          → B08
participants / invitation responses        → B09
Actual / Outcome / Confirmation            → B10
reminders / conditional policy             → B11
provider conferencing / sync               → B13
Agenda part independent Schedule           → not authorized
```

## 8. Detailed semantic authority

The full initial functionality/logic map remains binding at:

`docs/workstreams/archive/timeline-temporal-operational-map-ledger-snapshot-2026-09-15.md`

The live map records implementation/proof progress and does not replace the semantic freeze.

## 9. Next gate

```text
APPROVE B03-E
```

No B03-E implementation and no CI run are implied by B03-D closure.