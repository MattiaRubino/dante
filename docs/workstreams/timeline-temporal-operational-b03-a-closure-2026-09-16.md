# Timeline / Temporal-Operational — B03-A Closure

- **Status:** ✅ CLOSED / PROVEN
- **Date:** 2026-09-16
- **Branch:** `feature/timeline-temporal-operational`
- **Block:** B03 Event Core
- **Slice:** B03-A Event canonical core
- **Alembic head:** `20260916_27`
- **Current topology:** `98|5|29|78|195|115|288|0|0|0`
- **Next slice:** B03-B Shared Schedule + Event Timeline
- **CI:** not launched; not claimed

## 1. Proven scope

B03-A establishes Event as a real self-owned canonical originating owner without activating Schedule/Event UI behavior early.

Implemented and proven:

```text
dante.event                               existing CP6 Event NativeRef owner
+ event_expectation                       typed Event expectation descriptor
+ event_create_operation                  immutable idempotency receipt
+ create_self_event(...)                  bounded SECURITY DEFINER capability
+ EventExpectationRow                     SQLAlchemy mapping
+ EventCreateOperationRow                 SQLAlchemy mapping
+ TemporalEventApplication                backend application boundary
+ POST /api/v1/temporal/events            governed CreateEvent
+ GET  /api/v1/temporal/events/{event_ref} self-scoped detail
```

Permanent boundaries preserved:

```text
Event != Activity
Event != Schedule
operation_id != Event identity
Person != Account != Principal != Actor
Event title/expectation != generic Event metadata JSON
Event create != Event scheduling
```

No `event_schedule`, generic temporal mega-entity, generic status, recurrence, participants, Session, Actual, Outcome, reminders, provider fields or Agenda persistence were introduced in B03-A.

## 2. Persistence authority

Forward migration:

```text
20260916_27_b03_event_core.py
Revises: 20260915_26
```

New current objects:

```text
event_expectation
event_create_operation
create_self_event(uuid,text,text,uuid,text)
```

Runtime authority remains bounded:

```text
dante_runtime: SELECT event_expectation
                EXECUTE create_self_event(...)
                no generic INSERT/UPDATE/DELETE on Event persistence
```

The Event create capability atomically establishes:

```text
Event NativeRef
+ native_address(owner_family='event')
+ event_expectation
+ event_create_operation receipt
```

Same self Person + same operation id + same normalized intent replays safely. Same operation id with a changed intent fingerprint rejects instead of overwriting accepted truth.

The introducing migration refuses destructive downgrade once canonical `event_expectation` rows exist.

## 3. Dictionary / SQLAlchemy / catalog reconciliation

The checked-out candidate state is reconciled at:

```text
Alembic       20260916_27
Tables        98
Views          5
Routines      29
Triggers      78
Indexes       195
Foreign keys  115
CHECKs        288
Types/etc       0
```

Current Dictionary entries include:

```text
tables/event_expectation.json
tables/event_create_operation.json
routines/create_self_event.json
```

`scope.json`, current-catalog tests, SQLAlchemy mappings and Alembic head were advanced in the same B03-A slice.

## 4. Executed evidence

### Event core/API proof

Command:

```text
pytest apps/backend/tests/integration/temporal/test_b03_event_core.py -m postgres -q
```

Result:

```text
2 passed
```

Proves:

- canonical UUIDv7 Event identity;
- title persistence/reload;
- idempotent same-intent replay;
- changed-intent operation-id conflict;
- CSRF requirement;
- self-Person isolation/detail visibility;
- no Activity/Event identity collapse.

### Database reconciliation / migration gate

Combined targeted gate executed:

```text
test_current_catalog.py
test_database_current_catalog.py
test_b03_event_migration.py
test_migrations.py::test_fresh_database_reaches_the_single_repository_head
test_migrations.py::test_repository_head_round_trips_head_base_head
```

Initial result:

```text
10 passed, 1 failed
```

The single failure was a **test-harness privilege defect**, not a product/migration failure: the B03 migration test attempted to read `dante.alembic_version` without entering the same trusted migrator/owner role discipline already used by the canonical migration suite.

The harness was corrected in commit `8dc423adc8f2cf5cf115061192c603d806e923b3` and the failed test was rerun:

```text
1 passed in 7.04s
```

Therefore all targeted B03-A catalog, ACL, migration-head, head→base→head and fail-closed downgrade assertions are green.

## 5. B03-A exit criteria

```text
EventRef exists canonically                         ✅
self ownership is explicit                         ✅
title survives reload                              ✅
replay same intent is safe                         ✅
changed-intent operation reuse rejects             ✅
CreateEvent is bounded by runtime capability       ✅
Dictionary / SQLAlchemy / Alembic / PG reconcile   ✅
canonical Event blocks destructive downgrade       ✅
Schedule/Activity identity collapse absent         ✅
```

B03-A is therefore **CLOSED / PROVEN**.

## 6. Explicit non-claims

B03-A does **not** claim:

- Event has a current Schedule;
- Event appears on Timeline;
- Event Create UI is product-active;
- timed/all-day/multi-day Event is implemented;
- postponed/TBD lifecycle is implemented;
- Event Agenda is implemented;
- Event recurrence is implemented;
- provider/participant/Session/Actual/Outcome semantics are implemented;
- CI has passed.

Those remain owned by later B03 slices / later roadmap blocks.

## 7. Next gate

The next implementation slice is:

```text
B03-B — Shared Schedule + Event Timeline
```

Its job is to prove that the B02 Schedule engine survives a second semantic owner by generalizing typed self-scope from Activity-only to Activity-or-Event, then activating timed/all-day/multi-day Event projection through the shared Schedule owner/current/history machinery.

No B03-C/D/E implementation is authorized by this closure.