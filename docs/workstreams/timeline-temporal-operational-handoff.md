# Timeline / Temporal-Operational — Workstream Handoff

- **Status:** B10 IN PROGRESS — B10-A Actual / realization candidate prepared; generated client + user-run local gate pending
- **Reconciled:** 2026-09-25
- **Branch:** `feature/timeline-temporal-operational`
- **Roadmap authority:** `docs/workstreams/timeline-temporal-operational-roadmap.md`
- **Live execution ledger:** `docs/workstreams/timeline-temporal-operational-map.md`
- **B10 scope authority:** `docs/workstreams/timeline-temporal-operational-b10-scope-freeze.md`
- **DB overlay:** `docs/database/timeline-temporal-operational.md`
- **Current candidate Alembic frontier:** `20260925_71`
- **Last proven candidate DB frontier:** B09-C / `20260925_69` / `158|5|109|93|303|254|433`
- **CI:** no CI/GitHub Actions unless explicitly authorized; user runs local tests

Read this first after a context reset.

---

# 1. Exact current position

```text
B00–B06 ✅ CLOSED / PROVEN
B08     ✅ CLOSED / USER-REPORTED 2026-09-24
B09     ✅ CLOSED / USER-REPORTED 2026-09-25
  B09-A ✅ CLOSED / PROVEN 2026-09-25
  B09-B ✅ CLOSED / PROVEN 2026-09-25
  B09-C ✅ CLOSED / PROVEN 2026-09-25
  B09-D ✅ CLOSED / USER-REPORTED 2026-09-25
B10     🟨 IN PROGRESS
  B10-A 🟨 CANDIDATE PREPARED — generated client + user local gate pending
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

# 2. Permanent semantic boundaries at the B10 cursor

```text
Person != Account != Actor
Activity != Event != Routine
Routine != Recurrence != Occurrence
Occurrence != Schedule
Schedule != Session != Actual
Session != Actual != Outcome
Actual != Outcome != Confirmation
Expected outcome != Outcome
Responsibility != Participation
planned/intended != happened
projection != canonical truth
current accepted state != latest row
MaterialState != mutable runtime object
idempotency key != Domain identity
Undo != history rewind
Step != Activity
Plan != Activity
Dependency != hierarchy
ordering != dependency
```

PostgreSQL remains canonical authority. API, generated client, frontend, provider, solver and AI are projections/capabilities over that authority and may not create a second truth model.

---

# 3. Closed frontier truth

## B08 — Session Runtime

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

## B09 — Responsibility / Participation

B09 closed on the user's local automated gates and B09-specific real-app walkthrough on 2026-09-25.

Persistence/application sequence:

```text
_66 typed Event expected Participation + Activity/Event Responsibility
_67 guarded authoring/read capabilities
_68 Event Participation SQL ambiguity repair
_69 owner-local native non-Account Person referents
```

Permanent B09 boundaries:

```text
Person != Account
Responsibility != Participation
participant != responsible actor != organizer/owner
expected Participation != Actual Participation / attendance
participation/attendance != Event Actual
owner-local Person label != universal identity
another person's participation != authority over that person's calendar/task system
```

Proven B09-C topology remains:

```text
Alembic  20260925_69
Topology 158|5|109|93|303|254|433
```

B09-D integrated proof and the user-reported real-app walkthrough are recorded in `timeline-temporal-operational-b09-d-closure-2026-09-25.md`.

---

# 4. B10-A active truth — Actual / realization core

Scope authority: `timeline-temporal-operational-b10-scope-freeze.md`.

B10-A is one vertical block. It is **not closed yet** and is not split into independently closable A1/A2/A3/A4/A5 phases.

Canonical owner and state:

```text
dante.actual
  actual_ref
  subject_native_ref  → Activity | Event | Occurrence NativeRef

actual_realization_state
  append-only MaterialState
  realization_occurred boolean

actual_realization_timing
  optional instant | start_only | interval

actual_realization_session_basis
  exact session_ref + exact session_timing_material_state_ref

scoped_current_material_state + actual_realization_current_history
  explicit accepted-current binding/history
```

Critical meaning:

```text
Session END != Actual
Session may be evidence for Actual without sharing Actual identity
absence of Actual = unknown
absence of Actual != realization_occurred=false
Actual != Outcome != Confirmation
current accepted realization != latest row
```

## Implemented candidate

Forward-only migrations:

```text
20260925_70
  guarded self-scoped Actual realization record/current/history capability
  idempotent immutable operation receipt
  append-only MaterialState/current advancement
  timing and exact Session-timing-state basis validation

20260925_71
  exact subject-family hardening at PostgreSQL authority boundary
  Activity UUID cannot be accepted through Event/Occurrence capability and vice versa
  revision-70 generic function remains internal, runtime receives only family-bound signatures
```

Both revisions are now published and immutable. Any acceptance repair requires a new forward-only revision after `_71`.

Backend/API candidate:

```text
ActualApplication.record(...)
ActualApplication.get_for_subject(...)
ActualApplication.history(...)

POST/GET /api/v1/temporal/activities/{activity_ref}/actual
POST/GET /api/v1/temporal/events/{event_ref}/actual
POST/GET /api/v1/temporal/occurrences/{occurrence_ref}/actual
GET      /api/v1/temporal/actuals/{actual_ref}/history
```

OpenAPI inventory freezes all seven operations with stable `temporal_*` operationIds.

Timeline candidate:

```text
Activity / Occurrence → Actual controls alongside Session controls
Event                 → Actual controls alongside Responsibility/Participation

UI states:
  no Actual                     → Stato reale: sconosciuto
  realization_occurred=true     → Stato reale: avvenuto
  realization_occurred=false    → Stato reale: non avvenuto
```

The minimal web authoring surface intentionally writes the realization boolean only. Backend/API support optional timing and exact Session bases, but the web does not invent a timing/evidence UX before it is product-designed.

Focused tests are committed for:

```text
PostgreSQL/application:
  append-only current/history
  exact Session timing-state evidence
  idempotent replay + operation reuse rejection
  stale-current compare-and-set rejection
  Activity/Occurrence family enforcement
  cross-self isolation
  Session existence does not fabricate Actual

Public API:
  Event unknown-before-write
  CSRF
  first write + replay
  operation-id reuse conflict
  exact family rejection
  history

Web:
  unknown != false
  first write expected-current=None
  later compare-and-set uses current MaterialState
  stale rejection reloads authoritative state
```

No assistant-run test result exists for B10-A. Do not describe this candidate as proven until the user supplies local results.

---

# 5. Generated client rule

`packages/api-client/src/generated/*` and the exported OpenAPI file are generated artifacts and are never edited manually.

Canonical command:

```text
pnpm api:generate
```

`tooling/generate-api-client.mjs` exports OpenAPI from the backend and runs Orval. This generation is the first step of the user-run B10-A gate. The branch currently contains source/API changes; the generated B10-A client remains pending until that command is run locally.

---

# 6. Deferred B10 semantics

B10-A must not absorb later realization/result semantics:

```text
Outcome
Confirmation
partial/completed/skipped/not-completed/postponed/replaced/cancelled result vocabulary
finish-early result behavior
automatic Session→Actual inference
automatic Actual→Outcome inference
automatic Outcome→Confirmation inference
confirmation policy behind Home +
broad measurement/result UX
solver/provider/AI authority over realized facts
```

These remain later B10 work. `Expected outcome != Outcome` stays binding.

---

# 7. Roadmap ownership after B10

```text
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

# 8. Collaboration discipline

- user runs tests locally; assistant prepares exact commands
- no CI/GitHub Actions unless explicitly authorized
- push changes frequently
- do not edit historical migrations; use forward-only repair
- distinguish candidate truth from user-proven truth
- generated API client is generated from OpenAPI, never manually edited
- PostgreSQL remains the only canonical authority
- B07 is presentation consolidation, not a place to invent missing semantics

---

# 9. Fresh-chat recovery

```text
1. this handoff
2. timeline-temporal-operational-roadmap.md
3. timeline-temporal-operational-map.md
4. timeline-temporal-operational-b10-scope-freeze.md
5. migrations 20260925_70 and 20260925_71
6. apps/backend/src/dante/modules/temporal/actual_runtime.py
7. apps/backend/src/dante/modules/temporal/actual_api.py
8. B10-A backend/API/web tests
9. docs/database/timeline-temporal-operational.md + Actual Dictionary/mappings
```

**Exact next action:** the user runs the single local B10-A acceptance command: pull the branch, regenerate OpenAPI/Orval with `pnpm api:generate`, run generated/client checks, focused backend PostgreSQL/API/OpenAPI tests and focused web tests/typecheck. B10-A remains open until that user-reported gate passes.
