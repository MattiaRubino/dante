# B11-B — Conditional Temporal Behavior — Scope Gate

- **Date:** 2026-09-27
- **Branch:** `feature/timeline-temporal-operational`
- **Parent block:** B11 Advanced Recurrence / Conditional / Reminder
- **Status:** FROZEN FOR IMPLEMENTATION
- **Persistence predecessor:** `20260926_81`

## 1. Purpose

B11-B adds one bounded conditional temporal capability over canonical temporal truth. It does **not** introduce a generic rules, policy, trigger, workflow, automation, solver or decision engine.

The first and only condition family in B11-B is:

```text
actual_realization
```

It answers a precise question for one self-owned temporal subject:

```text
What does the current accepted Actual realization truth say about this subject?
```

Supported subjects follow the B10-A Actual boundary:

```text
Activity | Event | Occurrence
```

Routine is not a direct B11-B subject because Routine != Occurrence and Actual is not Routine truth.

## 2. Frozen semantic boundaries

```text
conditional != automation engine
evaluation != canonical mutation
proposal != accepted effect
projection != canonical truth
current accepted state != latest row
idempotency key != Domain identity
Session != Actual
absence of Actual != known non-realization
```

PostgreSQL remains the canonical authority. The caller never supplies the condition result as a boolean.

## 3. Canonical condition identity

A Condition is a stable self-scoped temporal intent with its own UUIDv7 identity.

For B11-B its canonical meaning is bounded by:

```text
self Person
+ subject NativeRef
+ family_code = actual_realization
```

The operation id used to create/evaluate a condition is only an idempotency key and never Condition identity.

The Condition does not own or replace Activity, Event, Occurrence, Actual, Schedule, Session or Recurrence truth.

## 4. Evaluation semantics

An evaluation is immutable evidence-bearing truth about the Condition at one evaluation instant.

Result vocabulary:

```text
satisfied
not_satisfied
indeterminate
```

Derived disposition vocabulary:

```text
allow
withhold
```

The mapping is fixed in PostgreSQL:

```text
current accepted Actual realization_occurred = true  -> satisfied     -> allow
current accepted Actual realization_occurred = false -> not_satisfied -> withhold
no current accepted Actual                           -> indeterminate  -> withhold
```

`allow` is a bounded gating/proposal signal only. It does not mutate Schedule, Occurrence, Recurrence, Session, Actual or any other canonical owner.

## 5. Exact evidence pinning

When an accepted Actual exists, every evaluation pins:

```text
actual_ref
actual_realization_material_state_ref
```

The MaterialState must be the exact accepted-current Actual state read during that evaluation.

A later Actual correction:

```text
does not rewrite an older evaluation
does not reinterpret its result
does not move its evidence pointer
```

Re-evaluation after correction creates a new immutable evaluation with the newly accepted exact Actual MaterialState.

For `indeterminate`, both Actual evidence references are absent by definition.

## 6. Idempotency and concurrency

Creation and evaluation use bounded operation ids (`1..200` characters) plus intent fingerprints.

```text
same operation + same intent      -> replay exact prior result
same operation + different intent -> reject
```

Evaluation identity is a UUIDv7 generated independently from the operation id.

PostgreSQL serializes conflicting operations at the self/condition boundary. Runtime code is an adapter over DB authority, not a second evaluator.

## 7. Persistence contract

B11-B requires a forward-only migration after `_81` because it introduces canonical Condition identity and immutable evaluation evidence.

Expected canonical family:

```text
conditional_temporal_intent
conditional_temporal_evaluation
conditional_temporal_operation
```

No mutable `current` pointer is required for evaluation rows because evaluations are immutable observations, not successive MaterialStates of one mutable payload.

## 8. STEP 1 acceptance proof

The PostgreSQL/runtime proof must establish all of the following:

1. create an `actual_realization` Condition for a self-owned Occurrence;
2. with no Actual, evaluate to `indeterminate / withhold` and no Actual evidence refs;
3. ending a Session for that Occurrence still evaluates to `indeterminate / withhold`;
4. after recording `realization_occurred=true`, evaluate to `satisfied / allow` and pin the exact Actual + exact Actual MaterialState;
5. after correcting the same Actual to `realization_occurred=false`, a new evaluation is `not_satisfied / withhold` and pins the corrected MaterialState;
6. the earlier satisfied evaluation remains unchanged and still points to the earlier MaterialState;
7. replay of the same evaluation operation returns the same evaluation identity/result;
8. reuse of an operation id with different intent is rejected;
9. no evaluation performs an implicit effect on Schedule/Occurrence/Recurrence/Session/Actual.

## 9. Explicit exclusions

Out of B11-B:

```text
arbitrary expression language
generic Rule / Policy / Trigger / Workflow entities
generic automation execution
AI-driven condition truth
automatic canonical mutation
notification delivery
Reminder persistence or delivery (B11-C)
solver/replanning behavior (B12)
work decomposition/dependencies (B13)
general visibility/AuthZ expansion (B15)
```

## 10. Closure path

B11-B closes vertically as:

```text
scope
-> PostgreSQL/Alembic
-> SQLAlchemy mapping
-> backend runtime
-> local PostgreSQL proof
-> public API/OpenAPI if exposed
-> generated client
-> web integration where product-visible
-> documentation reconciliation
```

The user runs all tests locally. No GitHub Actions/CI are used for this workstream.
