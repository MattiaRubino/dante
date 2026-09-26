# Timeline / Temporal-Operational — B10 scope freeze

Status: **B10-A / B10-B / B10-C / B10-D CLOSED / PROVEN; B10-E NEXT**.

This document is the current B10 semantic and execution authority. It freezes the proven Actual → Outcome → Confirmation → Reconciliation chain without redefining the canonical Domain / Logical / Physical model.

## 1. Permanent B10 boundaries

```text
Schedule != Session != Actual
Session != Actual != Outcome
Actual != Outcome != Confirmation
Expected outcome != Outcome
Outcome != Observation
Outcome != lifecycle / operational state
Confirmation != Authority
Confirmation != Verification
Confirmation != Decision / Approval
Confirmation != universal truth
Reconciliation != Confirmation
Reconciliation != Outcome
Reconciliation != universal truth
Resolution != deletion / rewrite of prior evidence
planned/intended != happened
proposal != accepted effect
projection != canonical truth
current accepted state != latest row
MaterialState != mutable runtime object
idempotency key != Domain identity
Undo != history rewind
```

PostgreSQL remains canonical authority. API, generated client, frontend, provider, solver and AI are projections/capabilities and may not create a second truth model.

## 2. Proven execution frontier

```text
B10-A Actual          CLOSED / PROVEN  2026-09-25
B10-B Outcome         CLOSED / PROVEN  2026-09-25
B10-C Confirmation    CLOSED / PROVEN  2026-09-26
B10-D Reconciliation  CLOSED / PROVEN  2026-09-26
B10-E Integration     NEXT
```

Persistence frontier:

```text
20260925_74  B10-A Actual
20260925_75  initial B10-B Outcome capability
20260925_76  canonical Outcome disposition reconciliation
20260925_77  Outcome ScopedAddress owner-dispatch repair
20260925_78  Outcome MaterialState totality-dispatch repair
20260925_79  B10-C Confirmation capability + dispatch
20260926_80  B10-D Reconciliation capability + exact evidence pinning
```

Published revisions are immutable. Any future persistence correction uses a new forward-only migration.

Last proven persistence frontier:

```text
Alembic  20260926_80
```

The last explicitly recorded whole-topology count remains the B10-C `_79` count `167|5|123|93|329|279|446`; B10-D closure proof establishes `_80` behavior but does not invent an unrecorded topology count.

## 3. B10-A — Actual / realization core — CLOSED / PROVEN

Actual is the stable scoped reality owner for Activity, Event or Occurrence realization.

```text
Session END != Actual
absence of Actual = unknown
known realization_occurred=false != absence of Actual
Session evidence != Actual identity
current accepted realization != latest row
Actual != Outcome != Confirmation
```

Canonical family:

```text
dante.actual
dante.actual_realization_state
dante.actual_realization_current_history
dante.actual_realization_operation
facet: actual.realization
```

Closure evidence: `timeline-temporal-operational-b10-a-closure-2026-09-25.md`.

## 4. B10-B — Outcome disposition — CLOSED / PROVEN

The temporary `_75` vocabulary/result representation is superseded. Do not reintroduce `vocabulary_code`, `result_code`, `outcome.result`, Outcome identity per vocabulary, or `/outcomes/{vocabulary_code}` routes.

Canonical model:

```text
one stable Outcome per Actual
Outcome identity != disposition MaterialState
Outcome disposition is contextual, not a universal enum
Outcome disposition is pinned to one exact Actual realization MaterialState
Actual correction does not reinterpret an older Outcome disposition
current accepted Outcome state != latest row
idempotency receipt != Outcome identity
absence of Outcome != success / failure / skipped
Outcome != Confirmation
```

Canonical physical family:

```text
dante.outcome
dante.outcome_disposition_state
dante.outcome_disposition_current_history
dante.outcome_disposition_operation
facet: outcome.disposition
```

Closure evidence: `timeline-temporal-operational-b10-b-closure-2026-09-25.md`.

## 5. B10-C — Confirmation — CLOSED / PROVEN

Confirmation is an optional contextual attestation by one confirmer toward one exact Outcome disposition MaterialState for one purpose.

```text
Confirmation != Outcome
Confirmation != Authority != Verification
absence of Confirmation != false / rejected / untrusted
0..N Confirmation per exact Outcome disposition MaterialState
identity = (target Outcome MS, confirmer Person, purpose)
stance_code is contextual, not confirmed=true
Outcome correction does not transfer old Confirmation
contrasting Confirmations from different actors remain representable
current accepted Confirmation state != latest row
idempotency receipt != Confirmation identity
no automatic Confirmation from Outcome / Actual / Session / click
```

Canonical physical family:

```text
dante.confirmation
dante.confirmation_attestation_state
dante.confirmation_attestation_current_history
dante.confirmation_attestation_operation
facet: confirmation.attestation
```

Public surface:

```text
POST /api/v1/temporal/outcomes/{outcome_ref}/confirmations
GET  /api/v1/temporal/outcomes/{outcome_ref}/confirmations
GET  /api/v1/temporal/confirmations/{confirmation_ref}/history
```

The B10-C post-closure public-contract hardening is closed. Runtime/OpenAPI/generated truth includes `201` creation, `200` idempotent replay and bounded ProblemDetails failures.

Closure evidence: `timeline-temporal-operational-b10-c-closure-2026-09-26.md`.

## 6. B10-D — Reconciliation / resolution workflow — CLOSED / PROVEN

B10-D owns explicit, reconstructible reconciliation of contextual Confirmation evidence around one exact Outcome disposition MaterialState.

Canonical identity:

```text
(outcome_disposition_material_state_ref, purpose_code)
```

Authority boundary:

```text
Outcome owner is the only resolver in B10-D
can see != can confirm
can confirm != can resolve
resolver identity is state data, not reconciliation identity
```

Canonical family:

```text
dante.outcome_reconciliation
dante.outcome_reconciliation_state
dante.outcome_reconciliation_evidence
dante.outcome_reconciliation_current_history
dante.outcome_reconciliation_operation
facet: outcome.reconciliation
```

Evidence pins exact Confirmation attestation MaterialStates:

```text
confirmation_ref
confirmation_attestation_material_state_ref
role_code = considered | selected
```

Outcome correction does not transfer reconciliation. Confirmation correction does not reinterpret older reconciliation evidence. Corrections append a new MaterialState and preserve prior evidence/history.

Approved contextual actions:

```text
unresolved
select
accept_multiple
defer
escalate
```

Action/evidence rules:

```text
unresolved       -> zero or more considered evidence; zero selected
select           -> exactly one selected evidence
accept_multiple  -> at least two selected evidence
defer            -> zero selected evidence
escalate         -> zero selected evidence
```

Public surface:

```text
POST /api/v1/temporal/outcomes/{outcome_ref}/reconciliations
GET  /api/v1/temporal/outcomes/{outcome_ref}/reconciliations
GET  /api/v1/temporal/reconciliations/{reconciliation_ref}/history
```

Generated client:

```text
cebfb557196d3fc0f412262a1d12feae9291b875
345 files deterministic/current
```

Final user-run closure proof:

```text
web typecheck PASS
Confirmation + Reconciliation web tests 6/6 PASS
pnpm generated:check PASS
@dante/api-client typecheck PASS
B10-D/B10-C/OpenAPI inventory backend tests 6/6 PASS in 3.07s
```

Earlier PostgreSQL/runtime/API + direct B10-C regression proof:

```text
4 passed in 14.94s
```

Scope authority: `timeline-temporal-operational-b10-d-scope-2026-09-26.md`.
Closure evidence: `timeline-temporal-operational-b10-d-closure-2026-09-26.md`.

## 7. B10-E boundary — NEXT

B10-E is integration/acceptance of already-proven A/B/C/D behavior. It does not create a new semantic layer merely to make the walkthrough pass.

Required integrated chain:

```text
Session → Actual → Outcome → Confirmation → Reconciliation
```

Required negative invariants include:

```text
Session END does not fabricate Actual
Actual does not fabricate Outcome
Outcome does not fabricate Confirmation
Confirmation does not grant reconciliation authority
Reconciliation does not rewrite Outcome or Confirmation history
absence at any layer is not silently converted into a negative fact
```

B10-E owns:

```text
focused whole-B10 automated regression
single integrated real-app/manual walkthrough
documentation reconciliation
whole-B10 close decision
```

After B10-E closes, advance to B11.

## 8. Explicitly outside B10

```text
generic Resolution ontology entity
generic Decision engine
full Verification model
generic Provenance model
AI/provider canonical authority
generic policy engine
full B15 Visibility/AuthZ model
mutation/deletion of historical Outcome / Confirmation / Reconciliation evidence
```

## 9. Collaboration and generation discipline

```text
user runs local tests
do not use GitHub Actions / CI
published migrations are immutable
generated client is produced only by repository tooling
never hand-edit generated sources
repository HEAD is source of truth before modification
```
