# Timeline / Temporal-Operational — Workstream Handoff

- **Status:** B09 🟨 IN PROGRESS — B09-A/B closed; B09-C next, B09-D pending; real-stack testing remains B15 scope
- **Reconciled:** 2026-09-25
- **Branch:** `feature/timeline-temporal-operational`
- **Roadmap authority:** `docs/workstreams/timeline-temporal-operational-roadmap.md`
- **Live execution ledger:** `docs/workstreams/timeline-temporal-operational-map.md`
- **DB overlay:** `docs/database/timeline-temporal-operational.md`
- **Current candidate Alembic frontier:** `20260925_68`
- **Last proven candidate DB frontier:** B09-B / `20260925_68` / `156|5|106|93|301|251|426`
- **CI:** no CI/GitHub Actions unless explicitly authorized; user runs local tests

Read this first after a context reset.

---

# 1. Exact current position

```text
B00–B06 ✅ CLOSED / PROVEN
B08     ✅ CLOSED / USER-REPORTED 2026-09-24
B09     🟨 IN PROGRESS
  B09-A ✅ CLOSED / PROVEN 2026-09-25
  B09-B ✅ CLOSED / PROVEN 2026-09-25
  B09-C ⬜ NEXT — exact scope to reconcile
  B09-D ⬜ AFTER B09-C — exact scope to reconcile
B10     ⬜ NOT STARTED
B11     ⬜ NOT STARTED
B13     ⬜ NOT STARTED
B12     ⬜ NOT STARTED
B14     ⬜ NOT STARTED
B07     ⏸ DEFERRED UNTIL B14
B15     ⬜ NOT STARTED
```

Execution order remains:

```text
B09 → B10 → B11 → B13 → B12 → B14 → B07 → B15
```

Historical identifiers are not renumbered.

---

# 2. B08 closure truth

B08 closed from the user's local automated output and real-app walkthrough on 2026-09-24.

Migration chain:

```text
_58 typed Session subject + START/READ/END
_59 exact Activity/Occurrence subject-family enforcement
_60 immutable END MaterialState + exact replay receipt
_62 pause/resume
_63 transition replay repair
_64 runtime metrics
_65 Activity TC-009 soft minimum on one Session active duration
```

Permanent B08 boundaries:

```text
START does not create fake Schedule
END does not complete Activity
END does not resolve Occurrence
END does not create Actual or Outcome
pause does not create a new Session
Session elapsed != active duration
TC-009 does not aggregate Sessions, count pauses, block transitions or mutate Schedule/Actual/Outcome
```

---

# 3. B09-A closure truth

B09-A was implemented in commit `aba642bc8a722eeb822b7bbfa34644b59ca19cad` and locally proven by the user on 2026-09-25.

Alembic:

```text
20260925_66
revises 20260924_65
forward-only
```

Typed persistence introduced:

```text
event_expected_participation
  event_ref → Event
  participant_person_ref → Person
  requirement_code ∈ {required, optional}

activity_responsibility
  activity_ref → Activity
  responsible_person_ref → Person

event_responsibility
  event_ref → Event
  responsible_person_ref → Person
```

The persistence substrate proves the intended B09-A boundaries:

```text
Person != Account
Responsibility != Participation
required/optional expected Participation is not attendance
Activity Responsibility != Event Responsibility by storage ownership
runtime cannot mutate/read the new tables directly
```

The B09-A PostgreSQL test also proves that participant Persons need no `account_application_context` row, invalid `requirement_code='accepted'` is rejected, and the simple current Responsibility subset enforces one holder per Activity/Event.

User-run command result on 2026-09-25:

```text
tests/integration/temporal/test_b09_responsibility_participation_persistence.py
tests/integration/database/test_current_catalog.py
tests/integration/database/test_database_current_catalog.py

10 passed in 18.33s
```

Current proven candidate frontier:

```text
Alembic  20260925_66
Topology 153|5|99|93|298|242|419
```

B09-A deliberately does not claim:

```text
invitation workflow
accept/decline/tentative response history
Actual Participation / attendance
attendance intervals
Responsibility transfer / claim / hand-off
public API mutation
Home + / Timeline authoring integration
provider attendee identity or authority over another person's external calendar/task state
```

Those remain outside B09-A by design.

---

# 4. B09-B closure truth

B09-B adds guarded authoring over the `_66` relation substrate. `_68` qualifies Event column references inside the Participation functions. The user ran the local automated proof on 2026-09-25. This closes B09-B only: B09-C and B09-D remain. Real-stack validation remains the B15 whole-vertical test scope.

```text
generated:check PASS
api-client typecheck PASS
web typecheck PASS
responsibility-controls.test.tsx: 4 passed
pytest B09-B + B09-A persistence + both catalog suites + OpenAPI inventory: 18 passed in 25.22s
```

Implemented by Alembic `20260925_67`:

```text
activity_responsibility_operation
event_responsibility_operation
event_expected_participation_operation

_self_referenceable_person
set_self_activity_responsibility
set_self_event_responsibility
set_self_event_expected_participation
get_self_activity_responsibility
get_self_event_responsibility
list_self_event_expected_participation
```

Public surface:

```text
PUT/GET /api/v1/temporal/activities/{activity_ref}/responsibility
PUT/GET /api/v1/temporal/events/{event_ref}/responsibility
PUT/GET /api/v1/temporal/events/{event_ref}/expected-participation
```

Preserved rules:

```text
raw relation tables are not runtime mutation surfaces
Person identity is independent from Account identity
the public holder/participant vocabulary is only "self" in this slice
_self_referenceable_person is the single later widening seam
Responsibility != Participation
expected Participation != response != Actual Participation
expected Participation does not establish Event Actual
Responsibility does not imply attendance
participant authoring does not grant control over another person's calendar/task system
```

Home `+` required/optional participant textareas remain B14. They collect free-text emails, not Person refs; B09-B does not invent email-to-Person identity. Timeline detail is the truthful B09 authoring surface for self Responsibility and self expected Participation.

User-run commands that passed:

```text
cd apps/backend
pytest tests/integration/temporal/test_b09_b_responsibility_authoring.py \
  tests/integration/temporal/test_b09_responsibility_participation_persistence.py \
  tests/integration/database/test_current_catalog.py \
  tests/integration/database/test_database_current_catalog.py \
  tests/test_temporal_openapi_inventory.py

cd apps/web
pnpm exec vitest run src/features/temporal/responsibility-controls.test.tsx
```

---

# 5. Roadmap amendment after Create audit

## B13 — Work Structure / Decomposition / Dependencies

Needed for cases such as:

```text
English lesson → speaking / writing / grammar
work item → internal steps
Plan → several independently meaningful Activities
Activity A → dependency → Activity B
```

B13 must distinguish:

```text
internal Step != Activity
composite work != generic sub-item hierarchy
Dependency != hierarchy
ordering != dependency
child Schedule != parent Schedule
child Session != parent Session
```

B13 executes before B12 so replanning/solver logic sees real dependency structure.

## B14 — Temporal Create Completeness Gate

Every editable Home `+` field must be exactly one of:

```text
A. canonically persisted and behaviorally proven
B. truthful handoff to the owning vertical/capability
C. explicitly presentation/read-only
D. hidden/removed until supported
```

Never leave:

```text
editable field → value collected → silently ignored or normally rejected because implementation is absent
```

---

# 6. Remaining B09 and reserved ownership afterward

```text
B10
  Actual / Outcome / Confirmation / Resolution
  confirmation policy
  partial completion / finish-early realization semantics
  Expected outcome != Outcome

B11
  advanced recurrence / conditional behavior
  truthful resolution of the Create reminder field

B13
  internal steps / composition / dependencies
  execution-structure policy foundation

B12
  preferred windows / movement / fallback
  conflict detection and dependency-aware replanning
  deterministic solver proposals

B14
  field-by-field Create truthfulness gate

B07
  final UI/UX consolidation only after B14

B15
  whole-vertical regression + semantic red-team closure
```

---

# 7. Collaboration discipline

- user runs tests locally; assistant prepares exact commands
- no CI/GitHub Actions unless explicitly authorized
- push changes frequently
- do not edit historical migrations; use forward-only repair
- distinguish candidate truth from proven/protected-main truth
- generated API client is generated from OpenAPI, never manually edited
- B07 is presentation consolidation, not a place to invent missing semantics

---

# 8. Fresh-chat recovery

```text
1. this handoff
2. timeline-temporal-operational-roadmap.md
3. timeline-temporal-operational-map.md
4. docs/database/timeline-temporal-operational.md
5. B09-A migration/mapping/test
6. current Logical Model / PostgreSQL blueprint sections relevant to Responsibility / Participation
```

**Exact next action:** reconcile the deliverables of B09-C and B09-D against `timeline-temporal-operational-post-b06-scope-decision-2026-09-23.md` plus the accepted Product / Domain / Logical / Physical authority; then begin B09-C. B10 follows B09-D. The user's real-stack test stays in B15; do not invent attendance semantics inside B09.
