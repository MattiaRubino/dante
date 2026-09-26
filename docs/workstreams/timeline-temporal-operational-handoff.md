# Timeline / Temporal-Operational — Workstream Handoff

- **Status:** B10 IN PROGRESS — B10-A/B10-B/B10-C CLOSED / PROVEN; B10-D not started
- **Reconciled:** 2026-09-26
- **Branch:** `feature/timeline-temporal-operational`
- **Roadmap authority:** `docs/workstreams/timeline-temporal-operational-roadmap.md`
- **Live execution ledger:** `docs/workstreams/timeline-temporal-operational-map.md`
- **B10 scope authority:** `docs/workstreams/timeline-temporal-operational-b10-scope-freeze.md`
- **B10-A closure evidence:** `docs/workstreams/timeline-temporal-operational-b10-a-closure-2026-09-25.md`
- **B10-B closure evidence:** `docs/workstreams/timeline-temporal-operational-b10-b-closure-2026-09-25.md`
- **B10-C approved scope:** `docs/workstreams/timeline-temporal-operational-b10-c-scope-2026-09-25.md`
- **B10-C closure evidence:** `docs/workstreams/timeline-temporal-operational-b10-c-closure-2026-09-26.md`
- **DB overlay:** `docs/database/timeline-temporal-operational.md`
- **Last proven frontier:** B10-C / Alembic `20260925_79` / topology `167|5|123|93|329|279|446`
- **Generated client:** regenerated locally and checked (339 files); not yet committed
- **CI:** no CI/GitHub Actions unless explicitly authorized; user runs local tests

Read this first after a context reset. Repository HEAD remains the source of truth; re-fetch it before any write.

---

# 1. Exact current position

```text
B00–B06 ✅ CLOSED / PROVEN
B08     ✅ CLOSED / USER-REPORTED 2026-09-24
B09     ✅ CLOSED / USER-REPORTED 2026-09-25
B10     🟨 IN PROGRESS
  B10-A ✅ CLOSED / PROVEN 2026-09-25
  B10-B ✅ CLOSED / PROVEN 2026-09-25
  B10-C ✅ CLOSED / PROVEN 2026-09-26
  B10-D ⬜ NEXT — reconciliation / resolution workflow, not started
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

---

# 2. Permanent semantic boundaries

```text
Person != Account != Actor
Activity != Event != Routine
Routine != Recurrence != Occurrence
Occurrence != Schedule
Schedule != Session != Actual
Session != Actual != Outcome
Actual != Outcome != Confirmation
Expected outcome != Outcome
Outcome != Observation
Outcome != lifecycle / operational state
Confirmation != Authority != Verification
Responsibility != Participation
planned/intended != happened
projection != canonical truth
current accepted state != latest row
MaterialState != mutable runtime object
idempotency key != Domain identity
Undo != history rewind
```

PostgreSQL is canonical authority. API, generated client, frontend, provider, solver and AI are projections/capabilities and may not create a second truth model.

---

# 3. Last proven frontier — B10-C Confirmation

B10-C is CLOSED / PROVEN. B10-B remains CLOSED / PROVEN at `20260925_78` / `163|5|119|93|317|268|440`.

```text
Alembic  20260925_79
Topology 167|5|123|93|329|279|446
Generated check 339 files, uncommitted
```

```text
Confirmation != Outcome
0..N Confirmation per exact Outcome disposition MaterialState
identity = (target MS, confirmer, purpose)
stance_code is contextual, not confirmed=true
Outcome correction does not transfer old Confirmation
current accepted Confirmation state != latest row
absence of Confirmation != false
```

---

# 4. Proven B10-C truth — Confirmation

B10-C is CLOSED / PROVEN. Closure evidence: `docs/workstreams/timeline-temporal-operational-b10-c-closure-2026-09-26.md`.

Published immutable B10-B chain remains `_75`–`_78`. B10-C adds:

```text
20260925_79  Confirmation capability + scoped family/facet + dispatch
```

Canonical B10-C model:

```text
Confirmation != Outcome
0..N Confirmation per Outcome disposition MaterialState
pin = exact outcome_disposition_material_state_ref
identity = (target MS, confirmer, purpose)
stance_code is contextual, not confirmed=true
Outcome correction does not move old Confirmation
current accepted Confirmation state != latest row
idempotency receipt != Confirmation identity
no automatic Confirmation
```

Canonical physical family:

```text
dante.confirmation
dante.confirmation_attestation_state
dante.confirmation_attestation_current_history
dante.confirmation_attestation_operation
facet: confirmation.attestation
```

Public routes:

```text
POST /api/v1/temporal/outcomes/{outcome_ref}/confirmations
GET  /api/v1/temporal/outcomes/{outcome_ref}/confirmations
GET  /api/v1/temporal/confirmations/{confirmation_ref}/history
```

Write records confirmer as authenticated self and does not require Outcome ownership. List is Outcome-owner scoped and returns 0..N. History is visible to confirmer or Outcome owner.

Generated OpenAPI/Orval artifacts were regenerated locally and passed the determinism check. They remain uncommitted. Never hand-edit generated files.

---

# 5. B10-C surfaces in this candidate

```text
apps/backend/migrations/versions/20260925_79_b10_c_confirmation_capability.py
apps/backend/src/dante/platform/database/mappings/confirmation.py
apps/backend/src/dante/platform/database/mappings/addressing.py
apps/backend/src/dante/modules/temporal/confirmation_runtime.py
apps/backend/src/dante/modules/temporal/confirmation_api.py
docs/database/dictionary/**
apps/web/src/features/temporal/remote-confirmation-data-source.ts
apps/web/src/features/temporal/confirmation-controls.tsx
apps/backend/tests/integration/temporal/test_b10_c_confirmation.py
apps/backend/tests/integration/temporal/test_b10_c_confirmation_api.py
apps/web/src/features/temporal/confirmation-controls.test.tsx
```

---

# 6. B10-C explicitly does not own

```text
B10-D reconciliation / resolution workflow
generic Resolution ontology entity
automatic Outcome -> Confirmation
AI/provider as human confirmer or canonical authority
integrated real-app walkthrough
```

---

# 7. Proof / collaboration discipline

- user runs tests locally; assistant does not use CI/GitHub Actions
- published migrations are immutable; fixes are forward-only
- distinguish implemented/candidate truth from user-proven truth
- generated API client comes from OpenAPI generator only
- do not request manual real-app testing before B10-E
- do not start B10-D until the user approves that gate

---

# 8. Fresh-chat recovery order

```text
1. docs/workstreams/timeline-temporal-operational-handoff.md
2. docs/workstreams/timeline-temporal-operational-b10-c-closure-2026-09-26.md
3. docs/workstreams/timeline-temporal-operational-b10-b-closure-2026-09-25.md
4. docs/workstreams/timeline-temporal-operational-roadmap.md
5. docs/workstreams/timeline-temporal-operational-map.md
6. docs/domain/concepts/confirmation.md + confirmation-part-2.md
7. migration 20260925_79
8. confirmation mappings / runtime / API
9. web Confirmation data source + controls
10. docs/database/timeline-temporal-operational.md + Dictionary/scope
```

**Exact next action:** the generated Confirmation client is in the worktree and checked. Commit it only when the user asks. Do not start B10-D until the user approves that gate.
