# Database contract — bounded Activity / Sub-Activity / Session vertical

- **Status:** DATABASE CONTRACT FREEZE — NO DDL PUBLISHED BY THIS DOCUMENT
- **Date:** 2026-10-02
- **Branch:** `feature/timeline-temporal-operational`
- **Domain authority:** `docs/domain/decisions/activity-subactivity-session-bounded-v1.md`
- **Logical authority:** `docs/logical-model/slices/activity-subactivity-session-bounded-v1.md`
- **Physical overlay:** `docs/physical-model/activity-subactivity-session-overlay-v1.md`
- **Database baseline:** existing Timeline / Temporal-Operational PostgreSQL model; exact Alembic head must be re-read immediately before implementation

## 1. Purpose

This document freezes the database-facing invariants and implementation obligations for the bounded Activity decomposition selected during B14/B07 product consolidation.

It does not publish tables, routines or a migration. It defines what the eventual forward-only implementation must prove before the UI may claim the capability is canonical.

## 2. Existing authority preserved

The implementation must not collapse or reinterpret existing canonical families:

```text
Activity != Event != Routine
Schedule != Session != Actual
Session != Actual != Outcome
Actual != Outcome != Confirmation
Step != Activity
Plan != Activity
Dependency != hierarchy
```

Existing B04 Schedule/Temporal Constraint, B08 Session, B10 realized-truth and B13 Plan/Step persistence remain authoritative for their concepts.

No published migration is rewritten.

## 3. New database responsibilities

The implementation needs three independent governed concerns:

```text
A. Activity decomposition relation
B. parent decomposition/completion guard policy
C. Activity Session-capture capability policy
```

They must not be collapsed into one untyped settings JSON payload.

## 4. Activity decomposition relation

Candidate family from the Physical overlay:

```text
activity_decomposition
activity_decomposition_state
activity_decomposition_current_history
activity_decomposition_operation
```

The child remains an existing Activity identity. There is no second `sub_activity` identity table.

### 4.1 Stable relation identity

A stable decomposition relation identifies the semantic edge:

```text
parent Activity -> direct child Activity
```

The accepted-current relation state carries at least:

```text
required | optional
presentation order
accepted/current lifecycle state
provenance/actor metadata required by current repository conventions
```

### 4.2 Hard invariants

The protected mutation path must reject:

```text
parent == child
missing parent Activity
missing child Activity
cross-self / foreign relation
second current parent for the same child
duplicate current parent-child relation
a child that is already a current child becoming a parent
cycles / depth > 2
conflicting operation replay
stale expected-current mutation where CAS applies
```

History is preserved; rejection must not be implemented by deleting older state.

## 5. Parent child-guard policy

Candidate family:

```text
activity_decomposition_policy
activity_decomposition_policy_state
activity_decomposition_policy_current_history
activity_decomposition_policy_operation
```

Current typed value:

```text
none
confirm
block
```

The policy reads required direct children only.

It must not persist a duplicate `completed` boolean for Activity. The guarded evaluator consumes canonical B10 realized truth and returns an admission/diagnostic result for the parent completion/reality command.

Expected semantics:

```text
none
  no child gate

confirm
  unresolved required child -> acknowledgement required

block
  unresolved required child -> guarded parent action rejected
```

Acknowledgement under `confirm` allows the parent action only; it does not mutate child Actual/Outcome/Confirmation.

## 6. Activity Session-capture capability

Candidate family:

```text
activity_execution_policy
activity_execution_policy_state
activity_execution_policy_current_history
activity_execution_policy_operation
```

Typed logical modes:

```text
disabled
record
live
record_and_live
```

A first implementation may publish a smaller supported subset, but:

```text
Session capability != session.active_duration constraint
```

The existing duration constraint remains a Temporal Constraint. Its presence cannot be the final canonical switch that decides whether an Activity owns Session runtime controls.

## 7. Session hierarchy prohibition

This vertical must not add a Session-parent relation.

Forbidden physical shortcuts:

```text
parent_session_ref
session_hierarchy
session_child
```

Pause/resume/active intervals remain state/history of one Session identity.

## 8. Temporal containment database boundary

A direct Sub-Activity placement is admissible only when its temporal placement is contained in the canonical parent envelope.

This is an admission invariant, not a UI hint.

### 8.1 Exact finite interval

For comparable accepted instants:

```text
parent_start <= child_start
child_end <= parent_end
```

### 8.2 Civil date-span / all-day envelope

Child placement must be fully contained within the parent civil-date span under the accepted timezone/calendar semantics.

### 8.3 Parent with no accepted exact placement

If canonical hard windows expose a bounded admissible parent envelope, the child may be admitted only when the submitted child placement is provably contained.

If no finite containing basis can be established:

```text
unplaced child        allowed
independently placed child  rejected / not admitted
```

### 8.4 Runtime mutation

The same invariant applies after creation.

Child reschedule outside the parent envelope is rejected.

Parent reschedule/unschedule that would invalidate accepted child placement is not allowed to silently mutate children. The guarded path must return a typed resolution requirement or accept an explicitly coordinated atomic operation.

## 9. Guarded routine contract

Exact routine names are chosen only after re-reading the live database head, but the final database surface must provide protected capabilities equivalent to:

```text
create/attach direct child
create child Activity + attach relation atomically/idempotently
read current children
read current parent
revise required/optional state
reorder direct children
retire/detach relation
set/revise/retire child-guard policy
set/revise/retire Activity execution policy
assess child temporal containment
assess parent Schedule mutation against current children
```

Runtime roles must not receive raw DML authority where the existing governance model requires guarded functions.

## 10. Create transaction / replay rule

Authoring a root plus new children in one user submission must not produce a partially duplicated tree on retry.

For example:

```text
A
├── B
└── C
```

A failure after creating B must not make a retry create A/B twice.

The implementation must use one of:

```text
single transactional guarded authoring command
or
stable preallocated refs + idempotent operation receipts with deterministic retry
```

The selected mechanism must be explicit in the implementation checkpoint and tested.

## 11. B10 integration

A Sub-Activity is an Activity identity, therefore existing B10 Activity subject semantics are reused.

Do not introduce:

```text
sub_activity Actual subject family
Session Actual subject merely to represent Session occurrence
```

Required database invariant:

```text
child truth mutation never writes parent truth
parent truth mutation never writes child truth
Session END never writes Activity completion/Actual by implication
```

The child-guard evaluator is read/admission logic, not cascade mutation.

## 12. Event boundary

This contract adds no Event hierarchy and no Event Session runtime.

No tables/routines for `event_decomposition`, `sub_event` or Event-owned B08 Session capture are authorized by this freeze.

A future Event/Activity typed relationship requires separate authority.

## 13. B13 regression boundary

B13 Plan/Step remains canonical and independent.

The implementation must not:

```text
reuse Plan Step rows as Sub-Activity relation rows
migrate Step into Activity decomposition
remove Step
reinterpret Plan ordering as Activity hierarchy
```

Existing optional Step -> Activity links continue to mean Plan structure references a real Activity.

## 14. Forward migration obligations

When implementation begins, the migration must be forward-only and must reconcile all applicable repository inventories:

```text
Alembic
Dictionary table/routine/scope documents
SQLAlchemy mappings
catalog expected topology
CHECK/UNIQUE/FK/index inventory
ACL/grants
guarded routine ownership/search_path rules
OpenAPI inventory when public endpoints are introduced
```

No generated client file is hand-edited.

## 15. Required PostgreSQL proof matrix

At minimum the local integration gate must prove:

```text
create root Activity with no child
attach one child
attach multiple ordered children
create child + relation idempotent replay
self-parent rejected
duplicate edge rejected
second parent rejected
child-as-parent / depth > 2 rejected
foreign/cross-self parent rejected
foreign/cross-self child rejected
required/optional revision preserved
reorder preserves identity/history
detach preserves both Activity identities/history
stale expected-current rejected
exact temporal containment accepted
left-boundary equality accepted
right-boundary equality accepted
child starts before parent rejected
child ends after parent rejected
all-day/date-span containment
unplaced child under unplaced parent
placed child with missing parent envelope rejected
parent reschedule preserving children accepted
parent mutation invalidating child placement guarded/rejected
child B10 truth does not mutate parent
parent B10 truth does not mutate child
Session END does not complete root or child
Session capability exists independently of duration constraint
B13 Plan/Step regression remains green
exact Dictionary/catalog/ORM/Alembic inventory remains green
```

## 16. Web/API proof expectations after persistence exists

Only after the database/backend path exists may the public vertical expose editable controls.

Then prove:

```text
OpenAPI generation deterministic
api-client generated check/typecheck
Create submits root + bounded children without dropped fields
reload reconstructs hierarchy from canonical reads
card runtime shows Session actions only from explicit execution policy
root and child B10 controls address distinct Activity refs
containment failures surface typed product errors
no decorative control silently ignored
```

## 17. Current implementation status

As of this freeze:

```text
Domain decision       documented
Logical contract      documented
Physical overlay      documented
Database contract     documented here
DDL / Alembic         NOT YET IMPLEMENTED
backend/API           NOT YET IMPLEMENTED for decomposition/policies
UI vertical           NOT YET IMPLEMENTED for canonical Sub-Activity
```

The existing B14 Session-card prototype remains technically proven in its previous gate but its capability inference from `session.active_duration` is explicitly provisional and must be replaced before claiming final canonical behavior.
