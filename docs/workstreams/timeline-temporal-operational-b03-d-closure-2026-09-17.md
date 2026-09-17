# Timeline / Temporal-Operational — B03-D Event Agenda Closure

- **Status:** ✅ CLOSED / PROVEN
- **Date:** 2026-09-17
- **Branch:** `feature/timeline-temporal-operational`
- **Alembic head:** `20260917_29`
- **Candidate topology:** `101|5|31|78|198|119|297|0|0|0`
- **Parent slice:** B03-C Event placement lifecycle
- **Next slice:** B03-E whole-B03 closure
- **CI:** not used; all accepted evidence below was executed locally

## 1. Closed scope

B03-D activates **Event Agenda/internal parts** as bounded ordered Event-owned values without promoting Agenda parts into independent temporal owners.

Accepted semantic shape:

```text
Event
└── ordered Agenda/internal parts
```

Permanent non-collapse retained:

```text
Agenda part != Activity
Agenda part != Event
Agenda part != Occurrence
Agenda part != Schedule
Agenda part != Session
Agenda part != Actual
Agenda part != Outcome
```

Individual Agenda parts therefore receive no NativeRef, ScheduleRef, MaterialStateRef, Session identity or Actual identity merely because they are editable/reorderable.

## 2. Canonical persistence

B03-D introduces Alembic `_29` with three narrow structures:

```text
event_agenda_part
  (event_ref, position, content)

event_agenda_current
  (event_ref, revision, updated_at)

event_agenda_mutation_operation
  (self_person_ref, operation_id, intent_fingerprint,
   event_ref, expected_revision, resulting_revision,
   accepted_agenda_parts, created_at)
```

and two bounded capabilities:

```text
create_self_event_with_agenda(...)
replace_self_event_agenda(...)
```

The existing `create_self_event(...)` remains the canonical Event-create primitive and remains compatible with Agenda-empty creation. B03-D does not duplicate Event identity creation.

Agenda rows are normalized relational values, not a generic JSON mega-field. `position` is explicit one-based order; content is trimmed, non-empty and bounded; maximum Agenda cardinality is 100.

## 3. Concurrency and idempotency

Agenda mutation is governed at **Event-Agenda aggregate level**, not by inventing identity/version objects for every Agenda part.

Accepted mutation contract:

```text
EventRef
+ operation_id
+ expected_revision
+ complete ordered Agenda value list
```

Rules proven:

- initial Agenda aggregate revision is truthfully `0`;
- each accepted replacement advances the aggregate revision exactly once;
- stale `expected_revision` fails closed;
- same operation id + same normalized intent replays the accepted result;
- same operation id + changed intent conflicts;
- mutation receipt is technical idempotency/concurrency evidence, not Event domain identity;
- replacement is atomic for add/edit/reorder/remove;
- reload rereads canonical backend truth.

## 4. Backend/API

Event read now exposes ordered Agenda truth and aggregate revision.

Agenda mutation uses:

```text
PUT /api/v1/temporal/events/{event_ref}/agenda
```

with CSRF, authenticated self scope, `expected_revision` CAS and operation-id replay semantics.

The PostgreSQL capability validates that the authenticated self Person owns the Event expectation. Cross-self mutation is rejected.

## 5. Frontend/product behavior

The Event detail surface now contains a real Agenda editor backed by the canonical Event read/mutation API.

Accepted behavior:

```text
read ordered Agenda
add item
edit item
move up/down / reorder
remove item
reload authoritative state
stale-CAS conflict → reload backend truth
```

The frontend does not claim local optimistic state as canonical truth. After a conflict/error it reloads the current Event Agenda from the backend.

The B03 Create runtime accepts Agenda as the only B03-D rich Event field newly activated; unrelated rich Event prototype fields remain fail-closed/deferred.

## 6. Database/Dictionary authority

Current candidate authority after `_29`:

```text
Alembic head      20260917_29
Tables            101
Views               5
Routines            31
Triggers            78
Indexes             198
Foreign keys        119
CHECK constraints   297
Exclusion             0
Materialized views    0
Sequences             0
```

Dictionary, SQLAlchemy mappings, current-catalog expectations and Alembic head tests were advanced to the same materialization.

The `_29` migration has dedicated proof for empty head→parent→head behavior and fail-closed downgrade when canonical Agenda state exists.

## 7. Executed proof

### 7.1 Focused PostgreSQL/API Agenda gate

```text
apps/backend/tests/integration/temporal/test_b03_event_agenda.py
2 PASS
```

This covers create, add, edit, reorder, remove, replay, stale CAS, reload, CSRF and self isolation.

### 7.2 DB / Alembic / Dictionary gate

Executed selection:

```text
test_b03_event_agenda_migration.py
test_current_catalog.py
test_database_current_catalog.py
test_fresh_database_reaches_the_single_repository_head
test_repository_head_round_trips_head_base_head
```

Result:

```text
12 PASS in 19.59s
```

### 7.3 B03-D web proof

Executed Agenda transport/editor/Create and affected Event tests:

```text
6 test files / 19 PASS
@dante/i18n typecheck PASS
@dante/web typecheck PASS
```

A single test-only Vitest typing issue was found (`toMatchObject` generic argument), fixed, and web typecheck was rerun green. No product/runtime defect was hidden by that fix.

### 7.4 Final regression gate

Backend/PostgreSQL B02 + B03-A/B/C/D selection:

```text
13 PASS / 2 deselected in 25.34s
```

Web Activity/Schedule + Event lifecycle/Agenda selection:

```text
5 test files / 26 PASS
```

Therefore B03-D did not regress the already-closed Activity shared-Schedule lifecycle or Event placement lifecycle.

## 8. Stop lines preserved

B03-D does **not** activate:

```text
Event recurrence                       → B06
Temporal Constraints/movement policy   → B04
Life Area / Calendar / Tags            → B05
Session/execution                      → B08
participants/invitations               → B09
Actual / Outcome / Confirmation        → B10
reminders / conditional policy         → B11
provider conferencing / sync           → B13
Agenda-part independent Schedule       → not authorized
```

Purpose, expected outcome, generic notes/resources and other prototype-only Event metadata remain outside the B03-D canonical contract unless a later owning slice explicitly activates them.

## 9. Closure decision

B03-D is **CLOSED / PROVEN** because the accepted Agenda semantics, canonical persistence, application/API boundary, real frontend behavior, concurrency/idempotency semantics, migration/Dictionary authority and impacted regressions are all green.

No additional B03-D implementation is required.

The only remaining B03 slice is:

```text
B03-E  whole-B03 closure
        real-stack E2E + manual Event acceptance
        + relevant full regression/reconciliation gates
```

B03-E must not reopen B03-D semantics unless an executed closure gate reveals a concrete defect.