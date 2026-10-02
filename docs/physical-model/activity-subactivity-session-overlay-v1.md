# Physical overlay — bounded Activity decomposition and Session capability v1

- **Status:** PHYSICAL CONTRACT FREEZE — IMPLEMENTATION NOT YET CLAIMED
- **Date:** 2026-10-02
- **Domain authority:** `docs/domain/decisions/activity-subactivity-session-bounded-v1.md`
- **Logical authority:** `docs/logical-model/slices/activity-subactivity-session-bounded-v1.md`
- **Accepted Physical baseline:** `docs/physical-model/pm-12-accepted-physical-model-v1.md`
- **Purpose:** additive PostgreSQL-oriented overlay; PM-12 remains the accepted baseline

## 1. Physical verdict

The bounded Activity decomposition does not require a new universal entity hierarchy or graph store.

PostgreSQL remains canonical. Existing Activity, Session, Schedule, Actual, Outcome, Confirmation and Plan/Step persistence remain separate.

The smallest justified physical addition is:

```text
one governed Activity-to-Activity decomposition relation family
one governed parent decomposition-policy family
one governed Activity Session-capability family
relationship-aware temporal admission/read helpers
```

No `sub_activity` identity table is introduced. Child identity is the existing Activity identity.

## 2. Candidate relation family

Physical naming is frozen for the implementation candidate as:

```text
activity_decomposition
activity_decomposition_state
activity_decomposition_current_history
activity_decomposition_operation
```

`activity_decomposition` owns stable relationship identity.

Minimum identity columns:

```text
decomposition_ref        uuid PK
self_person_ref          uuid NOT NULL
parent_activity_ref      uuid NOT NULL
child_activity_ref       uuid NOT NULL
created_at               timestamptz NOT NULL
```

Minimum state payload:

```text
decomposition_ref
requirement_code         required | optional
presentation_order       bounded integer
material_state_ref / accepted-state binding according to existing repository pattern
recorded_at / actor / provenance fields required by the accepted material-state pattern
```

The implementation may normalize state payload further if required by the existing MaterialState substrate, but it must not move relation semantics into arbitrary JSON.

## 3. Relation constraints

Database/guarded-operation proof must enforce:

```text
parent_activity_ref <> child_activity_ref
same self_person_ref for parent and child
no duplicate current parent/child relation
one current parent maximum for a child Activity
an Activity that is a current child cannot also be a current parent
```

Both Activity refs must resolve to existing Activities in the same authorized self scope.

Because accepted/current history is material, historical retired relations may coexist with current state. Uniqueness applies to accepted-current semantics, not by deleting history.

Defensive cycle detection remains required even though the depth-2 rule should make a valid cycle impossible.

## 4. Parent decomposition policy family

Candidate physical family:

```text
activity_decomposition_policy
activity_decomposition_policy_state
activity_decomposition_policy_current_history
activity_decomposition_policy_operation
```

Stable identity is scoped to the parent Activity.

Current state includes:

```text
child_guard_mode = none | confirm | block
```

The policy does not contain child completion state and does not duplicate B10 Actual/Outcome/Confirmation.

Its guarded evaluator reads accepted-current direct child relations and the canonical realized truth of required child Activities.

## 5. Activity Session-capability family

The current U4 candidate infers Session capability from an active `session.active_duration` minimum constraint. That remains a useful constraint signal but is not a sufficient capability owner.

Candidate physical family:

```text
activity_execution_policy
activity_execution_policy_state
activity_execution_policy_current_history
activity_execution_policy_operation
```

Current state carries a typed Session capture mode:

```text
disabled
record
live
record_and_live
```

The first implementation may expose a supported subset, but the database contract must reject unknown/contradictory values rather than store decorative configuration.

Temporal Constraints continue to own Session duration/spacing/preparation/recovery semantics. This policy does not duplicate those numeric rules.

## 6. No nested Session relation

Do not add:

```text
session.parent_session_ref
session_child
session_hierarchy
```

for this vertical.

Existing Session timing/pause/history tables remain the truth for internal execution segmentation.

## 7. B10 subject reuse

No new Sub-Activity Actual subject family is required.

A child is already an Activity identity, so the existing B10 Activity path remains authoritative.

Do not add `Session` as an Actual subject merely for this feature. Existing Session basis/evidence records remain the integration mechanism between Session truth and Activity Actual truth.

## 8. Temporal containment admission

Containment must be enforced through guarded domain/database capabilities that already resolve Schedule and Temporal Constraint authority.

Raw frontend comparison is insufficient.

Required capability shape:

```text
assess_subactivity_temporal_containment(
  self_person_ref,
  parent_activity_ref,
  child_activity_ref or proposed child placement
)

result:
  admissible
  inadmissible + reason
  missing_basis + reason
```

Schedule admission/reschedule paths for a child Activity must call the containment guard before accepting a placement.

Parent Schedule mutation must also read current children and refuse or require coordinated review when the submitted mutation would invalidate one or more accepted child placements.

No trigger should silently move a Schedule.

## 9. Exact containment cases

At minimum the implementation must prove:

```text
absolute interval parent + absolute interval child
civil date-span/all-day parent + child placement
parent bounded hard window + child proposed placement
parent without finite admissible envelope
```

For an exact parent interval:

```text
parent_start <= child_start
child_end <= parent_end
```

Timezone/DST comparison must use the existing accepted temporal representation and not a frontend-local reinterpretation.

## 10. Mutation capabilities

Runtime roles do not receive direct mutation authority over the new canonical tables.

Guarded operations are required for:

```text
create child Activity + relation
attach existing Activity as direct child when admitted
revise required/optional + order state
reorder siblings
retire/detach relation
set/revise/retire parent guard policy
set/revise/retire Activity execution policy
read current parent/children
assess temporal containment
```

Create-parent-with-children must be transactionally atomic where practical or use stable refs/idempotent receipts so retry cannot duplicate partial trees.

## 11. History / CAS / idempotency

The new families follow existing repository doctrine:

```text
stable semantic identity != operation receipt
accepted current state != latest row
MaterialState history is append-only where used
expected current MaterialState protects consequential correction
replay returns the original accepted result
conflicting reuse of operation id fails deterministically
```

Detaching/reordering does not rewrite Activity history.

## 12. ACL boundary

The self-personal implementation must prove:

```text
foreign parent Activity rejected
foreign child Activity rejected
cross-self relation rejected
foreign policy mutation rejected
raw runtime DML denied where repository governance requires guarded functions
```

## 13. Dictionary / ORM / catalog obligations

When implemented, every new physical object must be reconciled through:

```text
forward-only Alembic
Dictionary tables/routines/scope entries
SQLAlchemy mappings
current catalog expectations
ACL inventory
OpenAPI inventory where public
```

Published migrations remain immutable.

## 14. Required indexes / bounded reads

At minimum the physical implementation must support bounded indexed reads for:

```text
current children by parent Activity
current parent by child Activity
current policy by parent Activity
current execution policy by Activity
current decomposition relation by relation_ref
```

Sibling ordering must be deterministic.

## 15. No-go shortcuts

Forbidden:

```text
new universal work_item table
generic graph edge table for this relation
Sub-Activity represented as Plan Step
child state embedded as JSON inside parent Activity
Session capability inferred only from duration constraint
frontend-only containment enforcement
silent cascade Schedule mutation
implicit parent/child Actual propagation
Session nesting table
```

## 16. Implementation gate

DDL is not authorized by this document alone. Before the forward migration is written, implementation discovery must confirm exact current Activity/MaterialState/Schedule helper names and choose the smallest relation/policy representation consistent with the live `_head` database.

The resulting migration must be forward-only and locally proven against the exact catalog before UI is declared functional.
