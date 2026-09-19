# Timeline / Temporal-Operational — B04-C Absolute Windows / Preferences / Evaluation Implementation Freeze

- **Status:** FROZEN FOR IMPLEMENTATION
- **Date:** 2026-09-19
- **Branch:** `feature/timeline-temporal-operational`
- **Parent slice:** B04-B Boundary / Deadline constraints ✅ CLOSED / PROVEN
- **Entering candidate head:** `13c02c3f40233f19e2b52bcdb84d2ff5e21c509e`
- **Entering Alembic head:** `20260919_34`
- **Entering candidate topology:** `107|5|34|85|212|129|309|0|0|0`
- **Domain authority:** `docs/domain/concepts/temporal-constraint.md`
- **Logical authority:** `docs/logical-model/slices/time-reality-v1.md`
- **B04 execution authority:** `docs/workstreams/timeline-temporal-operational-b04-execution-plan.md`
- **CI:** not implicitly authorized

## 1. Goal

B04-C activates a complete typed **absolute-window** Temporal Constraint family and a deterministic derived evaluator over current effective boundary + window constraints.

A window is not an interval-shaped Schedule. Its semantics are the combination of:

```text
window geometry
+ required relationship to Schedule
+ hard | soft strength
```

Evaluation remains derived truth. B04-C does not persist `violated`, `overdue`, `invalid`, `infeasible` or similar pseudo-reality state.

## 2. Frozen subjects and temporal form

Supported subjects remain exactly:

```text
Activity | Event
```

Supported temporal representation for the new window family:

```text
absolute only
finite starts_at timestamptz
finite ends_at timestamptz
starts_at < ends_at
```

Unsupported in this slice and required to fail closed:

```text
date-span
floating-local
named-zone-local
coarse-local-period
```

No unsupported representation may be converted into an invented instant.

## 3. Frozen window relationship matrix

```text
start_within
  constrained_facet = schedule.start

completion_within
  constrained_facet = schedule.completion

full_placement_contained
  constrained_facet = schedule.placement

placement_overlaps
  constrained_facet = schedule.placement
```

Every other relationship/facet pairing fails closed in canonical persistence, not only in API validation.

`strength=hard` means validity requirement. `strength=soft` means preference. There is no separate untyped `preferred_window` family.

## 4. Frozen bound semantics

Window geometry is treated as explicit `[starts_at, ends_at]` for point-membership relations:

```text
start_within:
window.starts_at <= schedule.start <= window.ends_at

completion_within:
window.starts_at <= schedule.completion <= window.ends_at

full_placement_contained:
schedule.start >= window.starts_at
AND schedule.completion <= window.ends_at
```

Positive-overlap semantics are distinct:

```text
placement_overlaps:
schedule.start < window.ends_at
AND schedule.completion > window.starts_at
```

Two placements that only touch at one endpoint are not classified as overlapping.

## 5. Persistence strategy

Reuse the existing stable TemporalConstraintRef + immutable MaterialState/current-history/idempotency machinery.

Forward migration `_35` adds:

```text
temporal_constraint_window_state
temporal_constraint_window_absolute_state
mutate_self_absolute_window_constraint(...)
```

The common rule envelope expands only to:

```text
family_code:
boundary | window

constrained_facet_code:
schedule.start | schedule.completion | schedule.placement
```

The deferred totality validator must enforce exactly one family-specific payload and must reject mixed boundary+window payloads.

Forward migration `_36` activates least-privilege runtime reads for the two new current-rule window tables only. History and mutation receipts remain private.

No historical migration is rewritten.

## 6. Revision semantics

TemporalConstraint identity does not encode rule family.

Therefore a stable `TemporalConstraintRef` may move through immutable rule MaterialStates such as:

```text
boundary -> window
window -> boundary
window -> window
```

without changing constraint identity.

Create/revise dispatches to the governed capability matching the new typed rule. Retire dispatches from the family of the expected accepted state so retry/replay remains semantically exact even after current binding is removed.

## 7. Derived evaluation

B04-C evaluates a candidate absolute Schedule interval against **all current effective Temporal Constraints for the subject**, including B04-A/B boundary rules and B04-C window rules.

Per-rule result:

```text
satisfied
violated
not_evaluable
```

with canonical structured reason/discriminator evidence tied to:

```text
constraint_ref
material_state_ref
strength
rule family/kind/relationship
```

Overall candidate result:

```text
admissible
admissible_with_soft_violations
inadmissible
not_evaluable
```

Interpretation:

```text
admissible
  all hard rules satisfied and no soft violation

admissible_with_soft_violations
  all hard rules satisfied and at least one soft rule violated

inadmissible
  at least one hard rule violated

not_evaluable
  required hard evaluation cannot be completed without inventing information
```

Evaluation creates no Actual, Outcome, Confirmation or persisted violation state.

## 8. Hard-set feasibility signal

B04-C exposes a derived hard-set status:

```text
feasible
infeasible
undetermined
```

`infeasible` means no placement in the supported absolute rule algebra can satisfy the current hard set simultaneously. It does not mean reality is impossible and does not authorize movement/replanning.

Where the activated algebra is insufficient for a sound feasibility conclusion, return `undetermined` rather than guessing.

## 9. API strategy

The five B04-A/B CRUD operations stay stable and their typed rule union gains the four absolute-window variants.

B04-C adds exactly one new public Temporal operation:

```text
POST /api/v1/temporal/constraints/evaluate
operation_id = temporal_evaluate_constraints
```

The first candidate placement contract is an explicit absolute interval:

```text
subject_ref
placement:
  temporal_form: absolute
  starts_at
  ends_at
```

No endpoint performs solver search or automatic Schedule movement.

The exact pre-B04 13 operationIds remain frozen and all prior B04 operationIds remain unchanged.

## 10. Non-collapse rules

```text
Window != Schedule
Preference != placement
Evaluation != canonical state transition
Evaluation != solver
Violation != automatic movement
Hard rule violation != Outcome
Infeasible planning set != impossible reality
TemporalConstraint revision != Schedule revision
```

## 11. Explicitly out of scope

```text
date/floating/named-zone/coarse windows
persisted evaluation/violation state
automatic movement / Movement Policy            -> B04-D
duration / spacing / relative constraints       -> B04-E
full constraint frontend UX                     -> B04-F
optimization / candidate search / solver        -> B12
Actual / Outcome / Confirmation inference       -> B10
generic JSON rule payload
generic PostgreSQL range as hidden semantics
B05+
CI
```

## 12. Required proof before closure

- migrations reach `_36` from the accepted `_34` head;
- old B04-A/B boundary behavior remains green;
- all four window relationships persist and read with exact kind/facet semantics;
- invalid relationship/facet and mixed-family payloads fail at deferred DB integrity;
- create/revise/retire preserve CAS, immutable history and idempotent replay;
- runtime can SELECT only the current-rule window tables needed by the application read model;
- current-history and mutation receipts remain directly unreadable by runtime;
- evaluator composes current boundary + window rules and distinguishes hard from soft;
- hard-set infeasibility is derived without creating Outcome or movement;
- SQLAlchemy, Dictionary, real PostgreSQL catalog, owner/ACL and DB references reconcile to the final B04-C head;
- the Temporal API inventory contains exactly the one new semantic operationId;
- OpenAPI snapshot / Orval client / typecheck / client tests / generated determinism are green;
- closure docs identify B04-D as next without opening it.
