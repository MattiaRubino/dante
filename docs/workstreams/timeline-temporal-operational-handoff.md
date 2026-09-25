# Timeline / Temporal-Operational — Workstream Handoff

- **Status:** B10 IN PROGRESS — B10-A CLOSED / PROVEN; B10-B Outcome gate pending
- **Reconciled:** 2026-09-25
- **Branch:** `feature/timeline-temporal-operational`
- **Roadmap authority:** `docs/workstreams/timeline-temporal-operational-roadmap.md`
- **Live execution ledger:** `docs/workstreams/timeline-temporal-operational-map.md`
- **B10 scope authority:** `docs/workstreams/timeline-temporal-operational-b10-scope-freeze.md`
- **B10-A closure evidence:** `docs/workstreams/timeline-temporal-operational-b10-a-closure-2026-09-25.md`
- **DB overlay:** `docs/database/timeline-temporal-operational.md`
- **Current / last proven candidate Alembic frontier:** `20260925_74`
- **Current / last proven topology:** `159|5|115|93|305|258|435`
- **Generated B10-A client commit:** `780c612dfbb48457784f0ef61cb2394c760f9e3d`
- **CI:** no CI/GitHub Actions unless explicitly authorized; user runs local tests

Read this first after a context reset.

---

# 1. Exact current position

```text
B00–B06 ✅ CLOSED / PROVEN
B08     ✅ CLOSED / USER-REPORTED 2026-09-24
B09     ✅ CLOSED / USER-REPORTED 2026-09-25
B10     🟨 IN PROGRESS
  B10-A ✅ CLOSED / PROVEN 2026-09-25
  B10-B ⬜ NEXT — Outcome gate approval pending
  B10-C ⬜ Confirmation
  B10-D ⬜ Reconciliation / resolution workflow
  B10-E ⬜ Final integration + single real-app proof
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

Within B10 the agreed execution discipline is:

```text
B10-A whole block → user local automated gate → close
B10-B whole block → user local automated gate → close
B10-C whole block → user local automated gate → close
B10-D whole block → user local automated gate → close
B10-E integration/regression → user local automated gate → one real-app proof → close B10
```

Do not split A/B/C/D into user-facing micro-subphases. Do not request manual real-app testing before B10-E.

---

# 2. Permanent semantic boundaries at the B10-B cursor

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

B09-D closure evidence: `timeline-temporal-operational-b09-d-closure-2026-09-25.md`.

---

# 4. B10-A closed truth — Actual / realization core

B10-A is one closed vertical block. It is not split into independently closable A1/A2/A3/A4/A5 phases.

Canonical owner/state:

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

Final migration chain:

```text
20260925_70 guarded self-scoped Actual realization authoring/read + idempotency receipt
20260925_71 exact Activity/Event/Occurrence subject-family authority
20260925_72 CP6 Actual/scoped-address owner creation-order repair
20260925_73 canonical family-aware write/read signatures
20260925_74 current-history qualification + canonical bounded receipt FK name
```

Final proven frontier:

```text
Alembic  20260925_74
Topology 159|5|115|93|305|258|435
```

Public surface:

```text
POST/GET /api/v1/temporal/activities/{activity_ref}/actual
POST/GET /api/v1/temporal/events/{event_ref}/actual
POST/GET /api/v1/temporal/occurrences/{occurrence_ref}/actual
GET      /api/v1/temporal/actuals/{actual_ref}/history
```

Timeline states:

```text
no Actual                     → Stato reale: sconosciuto
realization_occurred=true     → Stato reale: avvenuto
realization_occurred=false    → Stato reale: non avvenuto
```

The minimal web authoring surface writes realization truth without inventing Outcome or Confirmation semantics.

User-run final local PostgreSQL/application/catalog acceptance on 2026-09-25:

```text
14 passed in 25.06s
POSTGRES TEST EXIT: 0
```

Earlier generation/client/web/OpenAPI steps were already green. Generated OpenAPI/Orval artifacts were committed and pushed as:

```text
780c612dfbb48457784f0ef61cb2394c760f9e3d
feat(api-client): generate B10-A Actual contracts
```

No CI/GitHub Actions were used. No B10-A manual real-app proof was performed; by explicit policy that proof belongs to B10-E.

---

# 5. B10-B next truth — Outcome

B10-B has not started. Before touching implementation, present a gate containing only the proposed changes/files/areas. The user approves that modification surface first.

B10-B must derive exact Outcome semantics from current repository Product/Domain/Logical/Physical authority before adding persistence. Do not infer a generic status model from UI labels alone.

Binding boundaries:

```text
Actual != Outcome
Expected outcome != Outcome
Outcome != Confirmation
Session END != Outcome
absence of Outcome != implicit success/failure
```

Potential result vocabulary such as:

```text
completed
partial
skipped
not-completed
postponed
replaced
cancelled
```

is not automatically a flat enum. Verify existing domain/DB authority and current semantics before selecting the physical representation.

Finish-early / partial-completion behavior belongs to B10-B only where repository authority supports it. Confirmation remains B10-C. Reconciliation workflow remains B10-D.

---

# 6. Generated client rule

`packages/api-client/src/generated/*` and the exported OpenAPI file are generated artifacts and are never edited manually.

Canonical generator:

```text
pnpm api:generate
```

For B10-B, generation happens only after backend/OpenAPI work is complete. User runs the final local gate; assistant does not run tests.

---

# 7. Later B10 semantics

```text
B10-C Confirmation
  Confirmation != Actual
  Confirmation != Outcome

B10-D reconciliation / resolution workflow
  do not invent a generic Resolution ontology entity without repository authority

B10-E final integration + acceptance
  run final automated regressions
  perform the single real-app B10 walkthrough
  reconcile docs
  close B10
```

---

# 8. Roadmap ownership after B10

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

# 9. Collaboration discipline

- user runs tests locally; assistant prepares exact commands
- no CI/GitHub Actions unless explicitly authorized
- push changes frequently
- published migrations are immutable; use forward-only repair
- distinguish candidate truth from user-proven truth
- generated API client is generated from OpenAPI, never manually edited
- PostgreSQL remains the only canonical authority
- gate = proposed modification/file surface for user approval, not acceptance criteria
- B07 is presentation consolidation, not a place to invent missing semantics

---

# 10. Fresh-chat recovery

```text
1. this handoff
2. timeline-temporal-operational-roadmap.md
3. timeline-temporal-operational-map.md
4. timeline-temporal-operational-b10-scope-freeze.md
5. timeline-temporal-operational-b10-a-closure-2026-09-25.md
6. migrations 20260925_70 → 20260925_74
7. apps/backend/src/dante/modules/temporal/actual_runtime.py
8. apps/backend/src/dante/modules/temporal/actual_api.py
9. B10-A backend/API/web tests
10. docs/database/timeline-temporal-operational.md + Actual Dictionary/mappings
```

**Exact next action:** present and obtain approval for the B10-B Outcome change/file gate. Do not implement B10-B before that approval.