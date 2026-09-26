# Timeline / Temporal-Operational — Workstream Handoff

- **Status:** B10 IN PROGRESS — B10-A/B10-B/B10-C CLOSED / PROVEN; B10-D persistence/runtime/API locally proven; generated-client gate active
- **Reconciled:** 2026-09-26
- **Branch:** `feature/timeline-temporal-operational`
- **Roadmap authority:** `docs/workstreams/timeline-temporal-operational-roadmap.md`
- **Live execution ledger:** `docs/workstreams/timeline-temporal-operational-map.md`
- **B10 scope authority:** `docs/workstreams/timeline-temporal-operational-b10-scope-freeze.md`
- **B10-A closure evidence:** `docs/workstreams/timeline-temporal-operational-b10-a-closure-2026-09-25.md`
- **B10-B closure evidence:** `docs/workstreams/timeline-temporal-operational-b10-b-closure-2026-09-25.md`
- **B10-C scope:** `docs/workstreams/timeline-temporal-operational-b10-c-scope-2026-09-25.md`
- **B10-C closure evidence:** `docs/workstreams/timeline-temporal-operational-b10-c-closure-2026-09-26.md`
- **B10-D scope:** `docs/workstreams/timeline-temporal-operational-b10-d-scope-2026-09-26.md`
- **DB overlay:** `docs/database/timeline-temporal-operational.md`
- **Last locally proven persistence frontier:** B10-D / Alembic `20260926_80`
- **B10-C generated client baseline:** `57303315`
- **B10-D generated client:** pending repository generation tooling
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
          ↳ post-closure OpenAPI hardening + generated refresh CLOSED / PROVEN
  B10-D 🟨 ACTIVE
          D1 scope freeze                 ✅
          D2 persistence + backend core   ✅ local PostgreSQL proof
          D3 public API/generated client  🟨 OpenAPI source frozen; generated refresh next
          D4 web controls                 ⬜
          D5 focused regression closure   ⬜
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
Confirmation != Decision / Approval
Reconciliation != universal truth
Reconciliation != Confirmation != Outcome
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

# 3. Proven B10 chain

## B10-A — Actual

```text
Alembic  20260925_74
Topology 159|5|115|93|305|258|435
```

Core truth:

```text
Session END != Actual
absence of Actual = unknown
known realization_occurred=false != absence of Actual
current accepted realization != latest row
Actual != Outcome != Confirmation
```

## B10-B — Outcome

Canonical current persistence is `_76`–`_78`, not the temporary `_75` vocabulary/result shape.

```text
one stable Outcome per Actual
facet: outcome.disposition
Outcome disposition pinned to exact Actual realization MaterialState
current accepted Outcome state != latest row
Outcome != Confirmation
```

Physical family:

```text
dante.outcome
dante.outcome_disposition_state
dante.outcome_disposition_current_history
dante.outcome_disposition_operation
```

Public routes:

```text
POST /api/v1/temporal/actuals/{actual_ref}/outcome
GET  /api/v1/temporal/actuals/{actual_ref}/outcome
GET  /api/v1/temporal/outcomes/{outcome_ref}/history
```

Proven frontier: `20260925_78` / `163|5|119|93|317|268|440`.

Never reintroduce `vocabulary_code`, `result_code`, `outcome.result` or Outcome identity per vocabulary.

## B10-C — Confirmation

```text
Confirmation != Outcome
0..N Confirmation per exact Outcome disposition MaterialState
identity = (target MS, confirmer, purpose)
stance_code is contextual, not confirmed=true
Outcome correction does not transfer old Confirmation
current accepted Confirmation state != latest row
absence of Confirmation != false
no automatic Confirmation
```

Physical family:

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

Proven persistence frontier: `20260925_79` / `167|5|123|93|329|279|446`.

Public contract:

```text
201 ConfirmationResponse  creation
200 ConfirmationResponse  idempotent replay
400/401/403/404/409/422/500 ProblemDetails
```

Generated refresh: `57303315`.

## B10-D — Reconciliation

Approved scope:

```text
identity = (outcome_disposition_material_state_ref, purpose_code)
Outcome owner is the only resolver in this slice
Confirmation participation does not grant resolution authority
evidence pins exact Confirmation attestation MaterialStates
Outcome correction does not transfer reconciliation
Confirmation correction does not reinterpret old reconciliation
current accepted reconciliation state != latest arbitrary row
```

Physical family in `_80`:

```text
dante.outcome_reconciliation
dante.outcome_reconciliation_state
dante.outcome_reconciliation_evidence
dante.outcome_reconciliation_current_history
dante.outcome_reconciliation_operation
facet: outcome.reconciliation
```

Public routes:

```text
POST /api/v1/temporal/outcomes/{outcome_ref}/reconciliations
GET  /api/v1/temporal/outcomes/{outcome_ref}/reconciliations
GET  /api/v1/temporal/reconciliations/{reconciliation_ref}/history
```

Actions:

```text
unresolved
select
accept_multiple
defer
escalate
```

Local proof executed by user on 2026-09-26:

```text
B10-D persistence test
B10-D API test
B10-C persistence regression
B10-C API regression

4 passed in 14.94s
```

Therefore `_80` + reconciliation runtime/API + direct Confirmation regression are locally proven. Do not mark B10-D CLOSED yet.

---

# 4. Exact next step — D3 generated client

Source OpenAPI contract is now frozen by:

```text
apps/backend/tests/test_b10_d_openapi_contract.py
apps/backend/tests/test_temporal_openapi_inventory.py
```

Required next gate:

```text
1. pull current branch
2. run B10-D OpenAPI/inventory tests
3. run pnpm api:generate
4. run pnpm generated:check
5. run @dante/api-client typecheck
6. inspect generated diff for reconciliation models/operations
7. commit ONLY generated OpenAPI/client artifacts
8. push generated checkpoint
```

Generated files must never be manually edited.

Expected generated operations:

```text
temporalRecordOutcomeReconciliation
temporalListOutcomeReconciliations
temporalListOutcomeReconciliationHistory
```

The exact generated symbol casing is determined by Orval; verify actual output instead of guessing file names.

After generated refresh is proven and pushed, advance to **D4 web controls**. Do not perform the integrated manual B10 walkthrough before B10-E.

---

# 5. B10-E boundary

The integrated real-app/manual B10 walkthrough remains intentionally deferred to B10-E after B10-D is closed.

---

# 6. Collaboration discipline

- user runs tests locally; assistant does not use CI/GitHub Actions
- push coherent checkpoints frequently with `[skip ci]`
- published migrations are immutable; persistence fixes are forward-only
- generated API client comes only from repo generator
- PostgreSQL remains canonical truth
- distinguish proven persistence/domain semantics from generated-artifact synchronization
- no manual real-app proof before B10-E