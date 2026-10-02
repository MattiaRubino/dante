# Logical slice — bounded Activity decomposition and Session capability v1

- **Status:** LOGICAL CONTRACT FREEZE — ACCEPTED FOR IMPLEMENTATION
- **Date:** 2026-10-02
- **Domain authority:** `docs/domain/decisions/activity-subactivity-session-bounded-v1.md`
- **Whole-logical baseline:** `docs/logical-model/whole-logical-model-v1.md`
- **Scope:** additive logical overlay; does not rewrite the accepted whole-logical snapshot

## 1. Purpose

This slice maps the bounded Activity/Sub-Activity/Session Domain decision into logical identities, relations, policies and guards without introducing a universal work-item root.

The accepted whole-logical representation remains authoritative. This slice adds the minimum logical structures required by the active Timeline / Temporal-Operational vertical.

## 2. Preserved logical identities

No new Sub-Activity identity family is introduced.

```text
Activity      = existing native Activity identity
Sub-Activity  = Activity identity + current typed parent relation
Session       = existing Session identity
Actual        = existing Actual identity
Plan / Step   = existing B13 identities/structure
```

Therefore:

```text
SubActivityRef does not exist as a second identity namespace
```

The child is addressed by its ordinary `ActivityRef` everywhere outside the relation context.

## 3. Activity decomposition relation

Introduce one typed, independently addressable relationship family conceptually named:

```text
ActivityDecomposition
```

The exact physical/table naming is deferred to the Physical/PostgreSQL implementation contract.

Logical fields:

```text
relationship_ref
scope / owner context
parent_activity_ref
child_activity_ref
requirement_code        required | optional
presentation_order      bounded deterministic order when user-visible
current material state / lifecycle binding
provenance / actor / operation receipt as required by existing patterns
```

The relation means exactly:

> child Activity is a direct semantic Sub-Activity of parent Activity.

It does not imply Dependency, Schedule precedence, Actual propagation, responsibility propagation or Plan membership.

## 4. Relationship invariants

The accepted bounded v1 relation enforces:

```text
parent_ref != child_ref
child has <= 1 current parent
parent may have 0..N current children
child may have 0 current children while it is itself a child
child that has a current parent may not be a current parent
same authorized/self scope
no duplicate current parent/child edge
no cycle
```

Because depth is bounded to root + direct child, the `child cannot parent` invariant is stronger than generic cycle prevention.

Ordering is presentation/decomposition order only:

```text
ordering != Dependency
```

## 5. Relationship lifecycle

The relation has lifecycle/history separate from both Activity identities.

Changing parent membership must not mutate the child Activity identity. Reordering children must not rewrite Activity state. Retiring/detaching a relation must not delete either Activity.

Expected-current/CAS and idempotent operation semantics follow the repository's accepted current-history patterns where material.

A correction or detach operation preserves historical evidence that the relation previously existed.

## 6. Parent completion guard policy

A parent Activity may carry a bounded decomposition-completion policy, logically distinct from Actual/Outcome itself.

Conceptual policy:

```text
child_guard_mode
  none
  confirm
  block
```

Meaning:

```text
none
  direct-child state does not gate the guarded parent completion action

confirm
  unresolved required direct children require explicit acknowledgement

block
  unresolved required direct children make that parent completion action inadmissible
```

The guard reads only current required **direct children**. It does not recursively traverse arbitrary work trees because bounded v1 has no grandchildren.

The policy does not write Actual for parent or child. It returns an admission/diagnostic result consumed by the command surface that records parent reality/completion.

## 7. Required versus optional child

`requirement_code` belongs to the parent-child relationship, not to the child Activity globally.

The same Activity meaning must not become globally "required" merely because one parent relation requires it.

For bounded v1 a child has at most one parent, but keeping requirement semantics on the relation preserves the correct ontology and avoids future migration pain.

## 8. Temporal containment logical guard

Introduce a relationship-derived temporal admissibility rule:

```text
SubActivityContainment(parent_activity_ref, child_activity_ref)
```

This is not a copied Temporal Constraint row on the child.

Evaluation basis:

1. resolve accepted/current parent temporal authority;
2. resolve proposed/current child placement;
3. if parent has an exact finite interval, require full containment;
4. if parent has a bounded civil-date span, require full civil-date containment;
5. if parent is unplaced but canonical hard windows provide a bounded envelope, admit only a child placement provably inside an admissible parent envelope;
6. otherwise the child may remain unplaced, but an independently accepted child placement must not be claimed valid without a provable containing basis.

Result is typed and reasoned:

```text
admissible
inadmissible(reason)
unknown_or_missing_basis(reason)
```

A hard authoring/admission command must fail closed for a placement when containment cannot be proven.

## 9. Coordinated parent mutation guard

Parent reschedule/unschedule operations must evaluate current child placements before acceptance.

Possible outcomes:

```text
safe
  all current child placements remain contained

requires_coordinated_change
  one or more child placements would become invalid

inadmissible
  mutation cannot be accepted under the submitted operation
```

No logical rule authorizes silent child rescheduling, unscheduling or deletion.

A later solver may propose coordinated changes, but proposal != accepted effect.

## 10. Activity Session capability policy

The logical model requires an explicit Activity execution capability when the product lets a user choose whether/how an Activity exposes Session execution.

The presence of a duration constraint is not enough.

Conceptual policy:

```text
session_capture_mode
  disabled
  record
  live
  record_and_live
```

Semantics:

```text
disabled         no Activity-owned Session capture surface
record           truthful manual/imported Session recording may be attached
live             live Start/Pause/Resume/End runtime may create Sessions
record_and_live  both supported
```

The exact initially implemented subset may be narrower, but unsupported values must not be editable or silently stored.

Session Temporal Constraints remain separate typed rules, for example minimum active duration.

```text
session capability != session.active_duration constraint
```

## 11. Session ownership / subject link

For this bounded Activity slice:

```text
Activity -> 0..N Sessions
```

A Sub-Activity uses the same relation because it is an Activity identity.

No recursive Session containment relation is introduced:

```text
Session -> Session  ❌
```

Pause/resume intervals, phases and metrics remain internal Session state/history, not child Session identities.

Cross-Activity multi-attribution of one Session is not introduced by this slice; existing Session attribution semantics remain authoritative until separately reviewed.

## 12. Realized truth projection

Parent and child Activities independently address B10:

```text
ActivityRef -> Actual -> Outcome -> Confirmation -> Reconciliation
```

No new B10 subject family is needed for Sub-Activity because the child already has an ActivityRef.

Session remains evidence/basis/runtime truth, not an Actual identity:

```text
Session evidence -> may support Activity Actual
Session -> Actual identity                         ❌
```

## 13. Event logical boundary

No Event decomposition or Event Session capability is added by this slice.

```text
Event -> Actual/Outcome/Confirmation/Reconciliation  existing
Event -> Sub-Activity                                not introduced
Event -> B08 Session runtime                         not introduced
```

A future Event/Activity relation must be typed and separately accepted.

## 14. Plan / Step logical boundary

B13 remains independent:

```text
Plan -> Step structure
Activity -> ActivityDecomposition relation
```

Neither relation substitutes for the other.

A Plan Step may continue to reference an Activity. That does not make the Step the parent of the Activity's Sub-Activities and does not merge the two structures.

## 15. Query/read requirements

The implementation must support bounded deterministic reads for:

```text
children(parent_activity_ref)
parent(child_activity_ref)
activity decomposition policy(parent_activity_ref)
Activity Session capability(activity_ref)
containment evaluation(parent, child/proposed placement)
```

A normal Activity read must remain valid even when no decomposition relation/policy exists.

## 16. Mutation requirements

Guarded operations must cover at least:

```text
attach child Activity
create-and-attach child Activity atomically or idempotently
update required/optional relation state
reorder direct children
retire/detach child relation
set/revise/retire parent child-guard policy
set/revise/retire Activity Session capability
validate child placement against parent
validate parent temporal mutation against children
```

Where Create authors parent + new children in one user action, retry safety must prevent duplicate parent, child or relation identities.

## 17. Explicit non-collapse rules

```text
Sub-Activity relation != Plan Step
Sub-Activity relation != Dependency
Sub-Activity relation != Session
Sub-Activity relation != Schedule
Session capability != Session identity
Session capability != duration constraint
child complete != parent Actual
parent complete != child Actual
Session END != Activity completion
ordering != dependency
containment != arbitrary constraint inheritance
```

## 18. Implementation acceptance preconditions

Before public UI is enabled, the physical/backend implementation must prove:

1. depth <= 2 and unique-parent invariants;
2. no self/cycle/duplicate/cross-scope relation;
3. history/current-state determinism;
4. idempotent create/replay and expected-current guards;
5. exact temporal containment admission and guarded parent reschedule behavior;
6. no implicit reality cascade;
7. explicit Session capability independent of Session duration constraints;
8. root and child Activity B10 paths remain independent;
9. B13 Plan/Step regressions remain green;
10. B08/B10/B12 existing regressions remain green.
