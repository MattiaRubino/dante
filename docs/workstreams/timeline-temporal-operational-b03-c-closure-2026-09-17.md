# Timeline / Temporal-Operational — B03-C Closure Record

- **Status:** ✅ CLOSED / PROVEN
- **Date:** 2026-09-17
- **Branch:** `feature/timeline-temporal-operational`
- **Scope:** Event placement lifecycle
- **DB authority:** PostgreSQL 18.6 / Alembic `20260917_28`
- **Topology:** `98|5|29|78|195|115|288|0|0|0`
- **Parent closures:** B03-A, B03-B
- **CI:** not run; CI remains separately authorized

## 1. Closure decision

B03-C is closed for its bounded scope.

The accepted implementation proves that Event placement lifecycle is expressed through the existing shared Schedule machinery rather than an Event-specific temporal engine.

```text
Event identity
    != Schedule identity

same EventRef
same ScheduleRef
    + append-only placement MaterialState evolution
    + explicit current binding
    + monotonic current-history episodes
```

No `event_schedule`, Event-specific current/history structure, generic owner shortcut or Event-as-Activity collapse was introduced.

## 2. Accepted behavior

B03-C proves the following behavior:

1. a scheduled Event can be rescheduled through the shared Schedule revision operation;
2. `EventRef` and `ScheduleRef` remain stable while placement MaterialState advances;
3. Timeline stops projecting the old placement and projects the new accepted placement;
4. postponed/TBD is represented truthfully by retaining Event and Schedule/history while removing the current accepted placement;
5. postponed/TBD does not fabricate a placeholder date/time and does not convert Event into Planning Tray Activity;
6. Event remains readable when no current placement exists;
7. stale expected-state mutations fail closed with conflict rather than overwrite accepted truth;
8. guarded Undo of postponement creates a new placement MaterialState and re-establishes current state without reopening old history rows;
9. Undo replay is idempotent;
10. frontend Timeline lifecycle controls use the same Schedule mutation boundary for Activity and Event while retaining explicit `scheduled-event` identity;
11. a newly created Event can revise/postpone/undo immediately without requiring a reload;
12. Activity Schedule behavior remains covered by the B02 regression selection.

## 3. Persistence / lifecycle result

B03-C required no new Alembic revision. `_28` already exposes the canonical shared Schedule lifecycle capability for Activity and Event, so adding a new persistence layer would have duplicated established semantics.

The PostgreSQL proof verifies the accepted state sequence:

```text
initial placement MaterialState
→ revised placement MaterialState
→ no current placement (postponed/TBD)
→ restored placement as a new MaterialState
```

Historical placement rows remain monotonic; Undo is not a history rewind.

## 4. Backend/API proof

Dedicated B03-C integration coverage verifies:

```text
POST  /api/v1/temporal/events/scheduled
PATCH /api/v1/temporal/schedules/{schedule_ref}/placement
POST  /api/v1/temporal/schedules/{schedule_ref}/unschedule
POST  /api/v1/temporal/schedules/{schedule_ref}/unschedule/undo
GET   /api/v1/temporal/events/{event_ref}
GET   /api/v1/temporal/timeline/window
```

The lifecycle proof explicitly checks stable Event/Schedule identity, new MaterialState generation, Timeline relocation, Event readability after postponement, absence of a current placement, preserved history, stale CAS conflicts, guarded Undo, monotonic restored history and idempotent Undo replay.

## 5. Frontend proof

The B03 Create runtime now uses the canonical `TemporalScheduleDataSource` for Event lifecycle after creation. It does not implement a local fake lifecycle.

Timeline lifecycle support proves:

```text
scheduled_event
→ shared Schedule revise
→ authoritative Timeline reload

scheduled_event
→ postpone/TBD via shared unschedule
→ authoritative absence from Timeline
→ guarded Undo
→ authoritative restored Event projection
```

UI language remains owner-aware: Activity can be returned to Planning Tray, while Event postponement is represented as Event postponement/TBD rather than Activity semantics.

## 6. Executed closure evidence

### PostgreSQL/backend targeted gate

Executed locally against real PostgreSQL on 2026-09-17:

```text
apps/backend/tests/integration/temporal/test_b03_event_lifecycle.py
apps/backend/tests/integration/temporal/test_b03_shared_schedule_event.py
apps/backend/tests/integration/temporal/test_b02_schedule_forms_precision_dst.py
apps/backend/tests/integration/temporal/test_b02_schedule_unschedule_undo.py

9 passed, 2 deselected in 23.13s
```

### Web targeted gate

Executed locally on 2026-09-17:

```text
src/features/temporal-create/application/temporal-create-b03-runtime.test.ts
src/features/home/ui/timeline/timeline-event-lifecycle-b03.test.tsx
src/features/home/ui/timeline/model/timeline-canonical-revision.test.ts
src/features/home/ui/timeline/timeline-authoritative-event-hydration.test.ts
src/features/temporal/remote-timeline-event-read.test.ts

Test Files  5 passed (5)
Tests       16 passed (16)
```

### Static gate

```text
pnpm --filter @dante/web typecheck
→ tsc --noEmit -p tsconfig.json
→ PASS
```

No CI evidence is claimed.

## 7. Semantic boundaries preserved

```text
Activity != Event
Event != Schedule
postponed/TBD Event != Planning Tray Activity
original Event expectation != current Schedule
current Schedule != future Actual
Schedule != Session != Actual
Undo != DB/history rewind
projection != canonical truth
```

B03-C does not claim Actual/Outcome/Confirmation behavior. The `Event expectation != current Schedule` portion is now proven; Actual remains B10-owned.

## 8. Explicitly deferred

B03-C did not activate:

```text
Agenda/internal parts                    → B03-D
whole-B03 full-stack/manual closure       → B03-E
Temporal Constraints / movement policy   → B04
Product Organization                     → B05
Event recurrence                         → B06
Session runtime                          → B08
participants/invitations                 → B09
Actual/Outcome/Confirmation              → B10
reminders/conditional policy             → B11
provider/conferencing/sync               → B13
```

## 9. Closure state

```text
B03-A  ✅ CLOSED / PROVEN
B03-B  ✅ CLOSED / PROVEN
B03-C  ✅ CLOSED / PROVEN
B03-D  ⬜ NEXT / NOT YET AUTHORIZED
B03-E  ⬜
```

B03 overall remains open until B03-D and B03-E are completed.