# Timeline / Temporal-Operational — Workstream Handoff

- **Status:** B10 IN PROGRESS — B10-A/B10-B/B10-C CLOSED / PROVEN; B10-C post-closure OpenAPI hardening awaiting generated refresh; B10-D not started
- **Reconciled:** 2026-09-26
- **Branch:** `feature/timeline-temporal-operational`
- **Roadmap authority:** `docs/workstreams/timeline-temporal-operational-roadmap.md`
- **Live execution ledger:** `docs/workstreams/timeline-temporal-operational-map.md`
- **B10 scope authority:** `docs/workstreams/timeline-temporal-operational-b10-scope-freeze.md`
- **B10-A closure evidence:** `docs/workstreams/timeline-temporal-operational-b10-a-closure-2026-09-25.md`
- **B10-B closure evidence:** `docs/workstreams/timeline-temporal-operational-b10-b-closure-2026-09-25.md`
- **B10-C scope:** `docs/workstreams/timeline-temporal-operational-b10-c-scope-2026-09-25.md`
- **B10-C closure evidence:** `docs/workstreams/timeline-temporal-operational-b10-c-closure-2026-09-26.md`
- **DB overlay:** `docs/database/timeline-temporal-operational.md`
- **Last proven persistence frontier:** B10-C / Alembic `20260925_79` / topology `167|5|123|93|329|279|446`
- **Original generated B10-C client:** `30f15adf` — 339 files
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
          ↳ post-closure OpenAPI response hardening committed
          ↳ generated OpenAPI/Orval refresh still required
  B10-D ⛔ DO NOT START until generated refresh is checked + committed
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

---

# 4. B10-C post-closure contract hardening

Review found no persistence/domain defect. The defect was only that runtime truth and generated OpenAPI response truth diverged:

```text
runtime new Confirmation  -> 201
runtime replay            -> 200
old generated OpenAPI     -> documented success only as 200
```

Committed source hardening:

```text
1f4c3415  fix(temporal): document B10-C confirmation HTTP outcomes [skip ci]
58947b45  test(temporal): freeze B10-C confirmation response contract [skip ci]
```

The route now declares:

```text
201 ConfirmationResponse  creation
200 ConfirmationResponse  idempotent replay
400/401/403/404/409/422/500 ProblemDetails
```

No migration after `_79` is required.

Generated files are intentionally stale until the user runs repository generation locally. Never hand-edit them.

---

# 5. Exact immediate action before B10-D

From the user's worktree:

```text
cd ~/projects/dante
git pull --ff-only origin feature/timeline-temporal-operational

pnpm api:generate
pnpm generated:check
pnpm --filter @dante/api-client typecheck

cd apps/backend
uv run --locked pytest -q --no-cov \
  tests/test_b10_c_openapi_contract.py \
  tests/test_temporal_openapi_inventory.py
```

If green, commit/push only the generated OpenAPI/client changes produced by the generator, with `[skip ci]` if desired. Do not edit generated files manually.

After that, re-fetch HEAD and reconcile this handoff/closure generated-commit reference. Only then prepare B10-D.

---

# 6. B10-D boundary

B10-D is reconciliation / resolution workflow. It is **not started**.

Before implementation, prepare a modification gate against current Product / Domain / Logical / Physical authority. B10-D must preserve:

```text
Confirmation != Decision / Approval / Authority
conflicting Confirmation history is not deleted
Outcome history is not rewritten as reconciliation
Actual history is not rewritten as reconciliation
latest row != accepted resolution
proposal != accepted effect
no generic Resolution ontology entity unless current authority justifies it
AI/provider does not become canonical authority
```

Do not start coding B10-D from old chat assumptions or stale pre-`_78` Outcome documents.

---

# 7. B10-E boundary

The integrated real-app/manual B10 walkthrough remains intentionally deferred to B10-E after B10-D is closed.

---

# 8. Collaboration discipline

- user runs tests locally; assistant does not use CI/GitHub Actions
- push coherent checkpoints frequently with `[skip ci]`
- published migrations are immutable; persistence fixes are forward-only
- generated API client comes only from repo generator
- PostgreSQL remains canonical truth
- distinguish proven persistence/domain semantics from generated-artifact synchronization
- no manual real-app proof before B10-E
