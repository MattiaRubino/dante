# Timeline / Temporal-Operational — Workstream Handoff

- **Status:** B03-C ✅ CLOSED / PROVEN → B03-D NEXT
- **Reconciled:** 2026-09-17
- **Branch:** `feature/timeline-temporal-operational`
- **Current roadmap:** `docs/workstreams/timeline-temporal-operational-roadmap.md`
- **Current live map/ledger:** `docs/workstreams/timeline-temporal-operational-map.md`
- **B02 closure:** `docs/workstreams/timeline-temporal-operational-b02-closure-2026-09-16.md`
- **B03 plan:** `docs/workstreams/timeline-temporal-operational-b03-execution-plan.md`
- **B03-A closure:** `docs/workstreams/timeline-temporal-operational-b03-a-closure-2026-09-16.md`
- **B03-B closure:** `docs/workstreams/timeline-temporal-operational-b03-b-closure-2026-09-17.md`
- **B03-C closure:** `docs/workstreams/timeline-temporal-operational-b03-c-closure-2026-09-17.md`
- **Next implementation gate:** `APPROVE B03-D`
- **CI:** no CI launch is implied or authorized

## 1. Current workstream position

```text
B00 Real Data Spine                              ✅ CLOSED / PROVEN
B01 Activity Core                                ✅ CLOSED / PROVEN
B02 Schedule Core                                ✅ CLOSED / PROVEN
B03 Event Core                                   🟨 B03-A + B03-B + B03-C CLOSED / B03-D NEXT
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

B03-B proved Event uses the same Schedule machinery already proven for Activity:

```text
Activity ─┐
          ├→ shared ScheduleRef / placement MaterialState / current/history
Event ────┘
```

B03-C then activated Event placement lifecycle on that same capability without adding another persistence model.

Current candidate DB:

```text
PostgreSQL 18.6
Alembic     20260917_28
Topology    98|5|29|78|195|115|288|0|0|0
```

`_28` remains the current head. B03-C required no `_29` because the canonical shared lifecycle capability already existed.

## 3. B03-A/B/C accepted result

Implemented and proven:

```text
canonical Event identity + expectation
idempotent self-scoped Event create
shared Activity OR Event Schedule authorization
atomic Event + initial Schedule creation
floating-local Event
named-zone-local Event with explicit DST/source semantics
all-day/date-span Event
multi-day Event
Timeline scheduled_activity | scheduled_event union
strict API / TypeScript parser + hydration
minimal truthful scheduled Event Create runtime
Event reschedule through shared Schedule revision
postponed/TBD with no current placement and preserved Event/history
Event readability while current placement is absent
stale expected-state conflict protection
guarded Undo through a new MaterialState
idempotent Undo replay
immediate lifecycle after Event create without reload
Activity Schedule regression preservation
no event_schedule table/current/history engine
```

## 4. B03-C proof summary

```text
PostgreSQL/backend targeted gate       9 PASS / 2 deselected
Event lifecycle web gate               5 files / 16 PASS
@dante/web typecheck                   PASS
```

The PostgreSQL proof establishes stable EventRef/ScheduleRef through revision, authoritative Timeline relocation, postponed/TBD as no-current-placement rather than deletion, preserved monotonic history, stale CAS rejection and guarded Undo as a new accepted MaterialState.

The frontend proof establishes the same lifecycle boundary for Timeline Event and for an Event immediately after Create. No local fake Event lifecycle was added.

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
original Event expectation != current Schedule
current Schedule != future Actual
postponed/TBD Event != Planning Tray Activity
projection != canonical truth
Undo != history rewind
```

B03-C proves expectation/current-Schedule separation. Actual remains B10-owned and is not implied by any scheduled or historical Event state.

## 6. Exact B03-D target

B03-D owns **Agenda/internal Event parts**.

Required behavior:

```text
Event
└── ordered bounded Agenda/internal parts
```

The implementation must preserve:

```text
Agenda part != Activity
Agenda part != Event
Agenda part != Occurrence
Agenda part != Session
Agenda part != Actual
```

B03-D should introduce only the minimum canonical identity/order/content needed for durable Event Agenda create/read/reload/edit behavior. It must not create a generic temporal-item framework or promote Agenda parts into independent scheduling owners.

Expected scope:

```text
1. re-open Event Agenda Domain/Logical/Physical authority
2. inspect existing persistence before adding schema
3. define bounded canonical Agenda-part identity/order/content
4. Event-owned self-scope and authorization
5. deterministic ordered read model
6. create/update/reorder/remove behavior with explicit concurrency/idempotency where mutations require it
7. frontend Event Agenda integration using real backend truth
8. reload persistence proof
9. PostgreSQL/API/frontend targeted gates
10. Activity/Event/Schedule regressions remain green
```

## 7. Explicit B03-D stop lines

Do not activate while implementing B03-D:

```text
Event recurrence                           → B06
Temporal Constraints / movement policy     → B04
Life Area / Calendar / Tags                → B05
Session/execution                          → B08
participants / invitation responses        → B09
Actual / Outcome / Confirmation            → B10
reminders / conditional policy             → B11
provider conferencing / sync               → B13
Agenda part independent Schedule           → forbidden unless future authority explicitly promotes the part
```

## 8. Remaining B03 slices

```text
B03-D  bounded ordered Agenda/internal parts
B03-E  full closure: PG/API/frontend/E2E/manual/Dictionary/docs
```

## 9. Detailed semantic authority

The initial full functionality/logic map remains binding at:

`docs/workstreams/archive/timeline-temporal-operational-map-ledger-snapshot-2026-09-15.md`

It remains the semantic freeze for functionality, `!=` disambiguations, owner/lifecycle rules and future-block responsibilities. The live map records implementation progress; it does not replace or erase the detailed freeze.

## 10. Next gate

```text
APPROVE B03-D
```

No B03-D/E implementation and no CI run are implied by B03-C closure.