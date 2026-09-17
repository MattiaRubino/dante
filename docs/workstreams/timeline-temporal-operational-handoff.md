# Timeline / Temporal-Operational — Workstream Handoff

- **Status:** B03-B ✅ CLOSED / PROVEN → B03-C NEXT
- **Reconciled:** 2026-09-17
- **Branch:** `feature/timeline-temporal-operational`
- **Current roadmap:** `docs/workstreams/timeline-temporal-operational-roadmap.md`
- **Current live map/ledger:** `docs/workstreams/timeline-temporal-operational-map.md`
- **B02 closure:** `docs/workstreams/timeline-temporal-operational-b02-closure-2026-09-16.md`
- **B03 plan:** `docs/workstreams/timeline-temporal-operational-b03-execution-plan.md`
- **B03-A closure:** `docs/workstreams/timeline-temporal-operational-b03-a-closure-2026-09-16.md`
- **B03-B closure:** `docs/workstreams/timeline-temporal-operational-b03-b-closure-2026-09-17.md`
- **Next implementation gate:** `APPROVE B03-C`
- **CI:** no CI launch is implied or authorized

## 1. Current workstream position

```text
B00 Real Data Spine                              ✅ CLOSED / PROVEN
B01 Activity Core                                ✅ CLOSED / PROVEN
B02 Schedule Core                                ✅ CLOSED / PROVEN
B03 Event Core                                   🟨 B03-A + B03-B CLOSED / B03-C NEXT
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

## 2. Accepted B03 foundation

B03-A established Event as a real canonical self-owned originating owner:

```text
dante.event
event_expectation
event_create_operation
create_self_event(...)
TemporalEventApplication
POST /api/v1/temporal/events
GET  /api/v1/temporal/events/{event_ref}
```

B03-B then proved Event can use the same Schedule machinery already proven for Activity:

```text
Activity ─┐
          ├→ shared ScheduleRef / placement MaterialState / current/history
Event ────┘
```

Current candidate DB:

```text
PostgreSQL 18.6
Alembic     20260917_28
Topology    98|5|29|78|195|115|288|0|0|0
```

`_28` changes governed Schedule routine definitions/authorization but does not create a second Event scheduling schema.

## 3. B03-B accepted result

Implemented and proven:

```text
typed Activity OR Event Schedule self-scope
atomic Event + initial Schedule application
floating-local Event
named-zone-local Event with explicit DST disambiguation
all-day/date-span Event
multi-day Event
Timeline scheduled_activity | scheduled_event union
strict API / TypeScript parser + hydration
minimal truthful scheduled Event Create runtime
Activity Schedule regression preservation
no event_schedule table/current/history engine
```

Event lifecycle mutation remains intentionally read-only in B03-B. The Timeline can render Event, but reschedule/unschedule/Undo UI capability is not activated for Event until B03-C.

## 4. B03-B proof summary

```text
PostgreSQL/API targeted selection      18 PASS / 4 FAIL first run
single _28 PL/pgSQL regression         fixed by af16b700
exact failed selection rerun           4 PASS
Event transport/Timeline web           10 PASS
B03 Create-runtime web                  2 PASS
@dante/web typecheck                    PASS
```

The first failure set exposed a real `_28` regression: redefining `unschedule_self_schedule(...)` had lost B02 PL/pgSQL strict disambiguation. The fix restored `#variable_conflict error` and qualified history-column references, preserving both runtime behavior and historical migration round-trip expectations.

Frontend closure also caught and fixed an Activity/Event lifecycle narrowing issue: Event projections remain read-only for lifecycle mutation in B03-B rather than accidentally acquiring B03-C semantics.

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
Agenda part != Activity/Event/Occurrence/Session/Actual by default
original expectation != current Schedule != Actual occurrence
projection != canonical truth
```

## 6. Exact B03-C target

B03-C owns **Event placement lifecycle**.

Required behavior:

```text
same stable Event identity
+ current Schedule may be revised or absent
+ Schedule history remains monotonic
+ original expectation remains distinct from current placement
```

Scope:

```text
1. Event reschedule through shared Schedule revision
2. postponed/TBD Event without placeholder date/time
3. Event remains readable when no current Schedule exists
4. detail/read surfaces expose current placement state truthfully
5. guarded Event Undo creates a new accepted placement MaterialState
6. no history rewind / resurrection shortcut
7. frontend lifecycle actions activate only after backend capability is proven
8. Activity path remains unchanged
```

Postponed/TBD must satisfy:

```text
Event identity retained
historical Schedule retained
no current accepted Schedule
no fabricated placeholder date/time
postponed/TBD Event != Planning Tray Activity
```

## 7. Explicit B03-C stop lines

Do not activate while implementing B03-C:

```text
Agenda durable persistence                 → B03-D
Event recurrence                           → B06
Temporal Constraints / movement policy     → B04
Life Area / Calendar / Tags                → B05
Session/execution                          → B08
participants / invitation responses        → B09
Actual / Outcome / Confirmation            → B10
reminders / conditional policy             → B11
provider conferencing / sync               → B13
```

## 8. Remaining B03 slices

```text
B03-C  Event placement lifecycle
B03-D  bounded ordered Agenda/internal parts
B03-E  full closure: PG/API/frontend/E2E/manual/Dictionary/docs
```

## 9. Detailed semantic authority

The initial full functionality/logic map remains binding at:

`docs/workstreams/archive/timeline-temporal-operational-map-ledger-snapshot-2026-09-15.md`

It remains the semantic freeze for functionality, `!=` disambiguations, owner/lifecycle rules and future-block responsibilities. The live map records implementation progress; it does not replace or erase the detailed freeze.

## 10. Next gate

```text
APPROVE B03-C
```

No B03-C/D/E implementation and no CI run are implied by B03-B closure.