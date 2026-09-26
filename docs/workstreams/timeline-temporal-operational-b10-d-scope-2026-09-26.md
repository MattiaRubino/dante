# Timeline / Temporal-Operational — B10-D reconciliation scope

Status: **APPROVED / IN PROGRESS** — gate approved 2026-09-26.

This document freezes the B10-D modification contract before persistence/API/UI implementation. It extends the proven Actual → Outcome → Confirmation chain without introducing a generic ontology-level `Resolution` or a second truth model.

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

For the first B10-D slice, the **Outcome owner is the only resolver**.

```text
can see != can confirm
can confirm != can resolve
can resolve != universal truth
confirmer != automatic resolver
```

Resolver identity is state data, not reconciliation identity. This deliberately avoids turning Confirmation participation into Authority before B15.

## 3. Stable identity

B10-D introduces a narrowly scoped Outcome-reconciliation owner only if persisted history is required. The approved stable identity is:

```text
(outcome_disposition_material_state_ref, purpose_code)
```

`outcome_ref` is carried and database-constrained to the target Outcome disposition state. `resolved_by_person_ref` belongs to each reconciliation MaterialState and is not part of stable identity.

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

Approved contextual actions for this slice:

```text
unresolved
select
accept_multiple
defer
escalate
```

They are workflow semantics for one purpose, not universal truth values.

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

A later Confirmation correction does not reinterpret an older reconciliation state. Historical reconciliation evidence remains pinned to the exact attestation state that was considered/selected at that time.

Evidence is normalized relational data; no canonical JSON-array truth column is introduced.

## 6. Persistence candidate

The approved B10-D persistence shape is a new forward-only revision after `_79`, expected as `_80` if implementation validation does not expose a contradiction:

```text
dante.outcome_reconciliation
dante.outcome_reconciliation_state
dante.outcome_reconciliation_evidence
dante.outcome_reconciliation_current_history
dante.outcome_reconciliation_operation
facet: outcome.reconciliation
```

The revision must also extend, in the same migration, the required ScopedAddress family/facet/current-state/CP6 MaterialState owner-dispatch and totality contracts. `_79` and all earlier published revisions remain immutable.

Corrections append a new MaterialState, close the prior current-history interval, preserve prior evidence rows, and require an exact `expected_material_state_ref`.

Idempotency operation receipts remain separate from Domain identity and include a complete intent fingerprint, including normalized evidence intent.

## 7. Public capability

Minimal public surface:

```text
POST /api/v1/temporal/outcomes/{outcome_ref}/reconciliations
GET  /api/v1/temporal/outcomes/{outcome_ref}/reconciliations
GET  /api/v1/temporal/reconciliations/{reconciliation_ref}/history
```

Candidate write contract:

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

The authenticated self must own the Outcome to write, list, or read reconciliation history in the first B10-D slice.

Creation/replay follows the established B10 pattern:

```text
201 new accepted reconciliation state
200 idempotent replay
409 operation reuse or stale expected-current state
```

## 8. Required invariants / proof cases

The implementation proof must cover at least:

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
defer/escalate select nothing
history chronology and one open current interval
current accepted reconciliation state != latest arbitrary row
no universal `resolved=true` / `truth=true` boolean
OpenAPI inventory/response contract
ScopedAddress/MaterialState/CP6 totality remains valid
```

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
B10 integrated manual proof before B10-E
```

## 10. Execution cursor

```text
B10-A CLOSED / PROVEN
B10-B CLOSED / PROVEN
B10-C CLOSED / PROVEN
B10-D APPROVED / IN PROGRESS
  D1 scope freeze                 <- this document
  D2 persistence + backend core   <- next
  D3 public API/generated client
  D4 web controls
  D5 focused regression closure
B10-E final integration + one real-app proof
```

User runs all local tests. Do not use GitHub Actions/CI. Generated API-client sources are produced only by repository generation tooling and are never hand edited.