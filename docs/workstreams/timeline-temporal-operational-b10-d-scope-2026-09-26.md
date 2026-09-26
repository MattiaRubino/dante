# Timeline / Temporal-Operational — B10-D reconciliation scope

Status: **CLOSED / PROVEN — 2026-09-26**.

This document freezes the B10-D modification contract that was implemented and proven. It extends the proven Actual → Outcome → Confirmation chain without introducing a generic ontology-level `Resolution` or a second truth model.

Closure evidence: `docs/workstreams/timeline-temporal-operational-b10-d-closure-2026-09-26.md`.

## 1. Semantic purpose

B10-D owns explicit, reconstructible reconciliation of contextual Confirmation evidence around one exact Outcome disposition MaterialState.

```text
Reconciliation != Outcome
Reconciliation != Confirmation
Reconciliation != Verification
Reconciliation != Authority
Reconciliation != universal truth
Resolution != deletion or rewrite of prior evidence
Decision != proof that something happened
```

A reconciliation may select one attestation, accept multiple attestations for the purpose, remain unresolved, defer, or escalate. It never rewrites Actual, Outcome or Confirmation history.

## 2. Authority boundary

For B10-D, the **Outcome owner is the only resolver**.

```text
can see != can confirm
can confirm != can resolve
can resolve != universal truth
confirmer != automatic resolver
```

Resolver identity is state data, not reconciliation identity. Confirmation participation does not grant Authority.

## 3. Stable identity

```text
(outcome_disposition_material_state_ref, purpose_code)
```

`outcome_ref` is constrained to the target Outcome disposition state. `resolved_by_person_ref` belongs to each reconciliation MaterialState and is not part of stable identity.

An Outcome correction produces a different target MaterialState and therefore a different reconciliation identity. No resolution silently transfers to the corrected Outcome state.

## 4. Reconciliation state

Each accepted reconciliation MaterialState records:

```text
reconciliation_ref
outcome_ref
outcome_disposition_material_state_ref
purpose_code
material_state_ref
action_code
resolved_by_person_ref
```

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

Selected evidence is also considered evidence.

## 5. Exact evidence pinning

Reconciliation evidence pins exact Confirmation attestation MaterialStates, not only stable Confirmation owners:

```text
confirmation_ref
confirmation_attestation_material_state_ref
role_code = considered | selected
```

Every referenced Confirmation attestation state must target the exact `outcome_disposition_material_state_ref` being reconciled.

A later Confirmation correction does not reinterpret an older reconciliation state. Historical reconciliation evidence remains pinned to the exact attestation state considered/selected at that time.

Evidence is normalized relational data; no canonical JSON-array truth column exists.

## 6. Implemented persistence

Forward-only Alembic revision:

```text
20260926_80
dante.outcome_reconciliation
dante.outcome_reconciliation_state
dante.outcome_reconciliation_evidence
dante.outcome_reconciliation_current_history
dante.outcome_reconciliation_operation
facet: outcome.reconciliation
```

`_80` extends the required ScopedAddress family/facet/current-state/CP6 MaterialState owner-dispatch and totality contracts. `_79` and all earlier published revisions remain immutable.

Corrections append a new MaterialState, close the prior current-history interval, preserve prior evidence rows and require exact `expected_material_state_ref`.

Idempotency operation receipts remain separate from Domain identity and include normalized evidence intent in the fingerprint.

## 7. Public capability

```text
POST /api/v1/temporal/outcomes/{outcome_ref}/reconciliations
GET  /api/v1/temporal/outcomes/{outcome_ref}/reconciliations
GET  /api/v1/temporal/reconciliations/{reconciliation_ref}/history
```

Write contract:

```text
operation_id
outcome_disposition_material_state_ref
expected_material_state_ref
purpose_code
action_code
evidence[]:
  confirmation_ref
  confirmation_attestation_material_state_ref
  role_code
```

The authenticated self must own the Outcome to write, list, or read reconciliation history in B10-D.

Creation/replay contract:

```text
201 new accepted reconciliation state
200 idempotent replay
409 operation reuse or stale expected-current state
```

## 8. Proof status — CLOSED

### Persistence/runtime/API gate

User-run local PostgreSQL proof on 2026-09-26:

```text
4 passed in 14.94s
```

Covered:

```text
empty owner-scoped list
non-owner cannot write/list/history
confirmer participation does not grant resolver authority
first reconciliation
idempotent replay
operation-id reuse with changed intent rejected
correction preserves stable identity
stale expected-current rejected
exact evidence MaterialState pinning
evidence must belong to exact target Outcome MaterialState
Confirmation correction does not reinterpret old reconciliation
Outcome correction does not transfer old reconciliation
unresolved action
select requires exactly one selected evidence
accept_multiple requires at least two selected evidence
history chronology and one open current interval
no universal resolved=true / truth=true boolean
```

### Generated/client/web/final regression gate

Generated client commit:

```text
cebfb557196d3fc0f412262a1d12feae9291b875
```

User-run final gate on 2026-09-26:

```text
@dante/web typecheck                                      PASS
Confirmation controls                                    3 passed
Reconciliation controls                                  3 passed
web total                                                6 passed / 2 files
pnpm generated:check                                     PASS — 345 files deterministic/current
@dante/api-client typecheck                              PASS
B10-D + B10-C + temporal OpenAPI inventory backend gate  6 passed in 3.07s
```

No CI/GitHub Actions were used.

## 9. Explicitly out of scope

```text
generic Resolution ontology entity
generic Decision engine
full Verification model
generic Provenance model
AI/provider authority
generic policy engine
full B15 Visibility/AuthZ model
automatic reconciliation when confirmations conflict
mutation/deletion of prior Outcome or Confirmation history
```

The integrated B10 manual proof remains in B10-E.

## 10. Closed cursor

```text
B10-A CLOSED / PROVEN
B10-B CLOSED / PROVEN
B10-C CLOSED / PROVEN
B10-D CLOSED / PROVEN
  D1 scope freeze                 ✅
  D2 persistence + backend core   ✅
  D3 public API/generated client  ✅
  D4 web controls                 ✅
  D5 focused regression closure   ✅
B10-E NEXT — final integration + one real-app proof
```

User runs all local tests. Do not use GitHub Actions/CI. Generated API-client sources are produced only by repository generation tooling and are never hand edited.
