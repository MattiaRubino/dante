# Timeline / Temporal-Operational — Workstream Handoff

- **Status:** B03-A ✅ CLOSED / PROVEN → B03-B NEXT
- **Reconciled:** 2026-09-16
- **Branch:** `feature/timeline-temporal-operational`
- **Current roadmap:** `docs/workstreams/timeline-temporal-operational-roadmap.md`
- **Current live map/ledger:** `docs/workstreams/timeline-temporal-operational-map.md`
- **B02 closure:** `docs/workstreams/timeline-temporal-operational-b02-closure-2026-09-16.md`
- **B03 plan:** `docs/workstreams/timeline-temporal-operational-b03-execution-plan.md`
- **B03-A closure:** `docs/workstreams/timeline-temporal-operational-b03-a-closure-2026-09-16.md`
- **Next implementation gate:** `APPROVE B03-B`
- **CI:** no CI launch is implied or authorized

## 1. Current workstream position

```text
B00 Real Data Spine                              ✅ CLOSED / PROVEN
B01 Activity Core                                ✅ CLOSED / PROVEN
B02 Schedule Core                                ✅ CLOSED / PROVEN
B03 Event Core                                   🟨 B03-A CLOSED / B03-B NEXT
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

## 2. B03-A accepted result

B03-A establishes Event as a real canonical self-owned originating owner.

Current Event core:

```text
dante.event                               existing Event NativeRef owner
event_expectation                         canonical typed expectation descriptor
event_create_operation                    immutable CreateEvent receipt
create_self_event(...)                    bounded runtime capability
TemporalEventApplication                  backend application boundary
POST /api/v1/temporal/events              governed CreateEvent
GET  /api/v1/temporal/events/{event_ref}  self-scoped detail
```

Current candidate DB:

```text
PostgreSQL 18.6
Alembic     20260916_27
Topology    98|5|29|78|195|115|288|0|0|0
```

B03-A proof:

```text
Event core/API PostgreSQL                         2 PASS
catalog/Dictionary/migration targeted gate       10 PASS
initial harness-only privilege defect             1 FAIL
corrected exact harness proof                     1 PASS
```

The failed assertion was not product behavior: the new migration test queried `dante.alembic_version` without entering the accepted migrator/owner role discipline. Commit `8dc423adc8f2cf5cf115061192c603d806e923b3` corrected the harness and the exact proof passed.

## 3. Semantic boundaries still binding

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
Agenda part != Activity/Event/Occurrence/Session/Actual by default
original expectation != current Schedule != Actual occurrence
```

B03-A did not weaken any of these boundaries.

## 4. Shared Schedule contract for B03-B

B03-B must prove:

```text
Activity ─┐
          ├→ one Schedule owner/current/history capability
Event ────┘
```

Forbidden:

```text
event_schedule table
Event-specific scheduling engine
Event-specific current/history model
generic owner/EAV shortcut that erases Activity/Event meaning
```

Current Schedule physical eligibility already includes:

```text
activity | event | occurrence
```

The remaining implementation gap is runtime/application/read-model activation, not a second temporal model.

## 5. Exact B03-B scope

```text
1. generalize self-subject authorization from Activity-only to typed Activity OR Event
2. preserve Activity path unchanged
3. reuse existing Schedule identity/current/history machinery
4. atomic Event + initial Schedule application operation
5. timed floating-local Event
6. timed named-zone-local Event
7. all-day/date-span Event
8. multi-day Event
9. Timeline backend/API Activity + Event discriminated union
10. TypeScript strict union/parser/rendering
11. activate minimal truthful Event Create surface
12. rerun B02 Activity Schedule regression proof
```

B03-B exit condition:

```text
Activity and Event both use the same Schedule owner/current/history machinery
```

## 6. Explicit B03-B stop lines

Do not activate in B03-B:

```text
Event recurrence                           → B06
Temporal Constraints / movement policy     → B04
Life Area / Calendar / Tags                → B05
Session/execution                          → B08
participants / invitation responses        → B09
Actual / Outcome / Confirmation            → B10
reminders / conditional policy             → B11
provider conferencing / sync               → B13
Agenda durable persistence                 → B03-D
postponed/TBD lifecycle                    → B03-C
```

The existing rich Event frontend prototype must continue to fail closed for unsupported fields. No accepted request may silently discard future-domain intent.

## 7. Remaining B03 slices

```text
B03-B  Shared Schedule + Event Timeline
B03-C  reschedule + postponed/TBD + detail/read + guarded Undo
B03-D  bounded ordered Agenda/internal parts
B03-E  full closure: PG/API/frontend/E2E/manual/Dictionary/docs
```

## 8. Detailed semantic authority

The initial full functionality/logic map remains binding at:

```text
docs/workstreams/archive/timeline-temporal-operational-map-ledger-snapshot-2026-09-15.md
```

It remains the semantic freeze for functionality, `!=` disambiguations, owner/lifecycle rules and future-block responsibilities. The live map records implementation progress; it does not replace or erase the detailed freeze.

## 9. Next gate

```text
APPROVE B03-B
```

No B03-C/D/E implementation and no CI run are implied by B03-A closure.