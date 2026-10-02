# Activity / Sub-Activity / Session — bounded semantic extension v1

- **Status:** SEMANTIC FREEZE — ACCEPTED FOR IMPLEMENTATION
- **Date:** 2026-10-02
- **Workstream:** Timeline / Temporal-Operational B14/B07 consolidation
- **Scope:** Activity decomposition, Session ownership, realized truth boundary
- **Implementation:** NOT YET CLAIMED by this document

## 1. Authority and compatibility verdict

This decision extends the accepted Activity semantics without replacing the existing Activity, Session, Plan/Step, Schedule or Actual models.

The existing Activity baseline already distinguishes semantic Sub-Activity decomposition from temporal Session splitting. The existing B08/B10/B13 vertical additionally freezes:

```text
Activity != Session
Activity != Actual
Session != Actual
Session END != Activity completion
Step != Activity
Plan != Activity
Schedule != Session != Actual
```

The bounded model below is therefore a compatible narrowing/activation of existing Domain meaning, not a new universal work-item ontology.

Important correction to the B14 U4 exploration:

```text
Sub-Activity != Plan Step
```

Plan Step remains B13 internal Plan structure. It is not deleted or repurposed. Activity decomposition receives its own typed Activity-to-Activity relation because the Activity Domain already owns Sub-Activity semantics.

## 2. Canonical concepts

### 2.1 Root Activity

A root Activity is an Activity that is not currently the child of another Activity through the bounded Sub-Activity relation.

It retains the full existing Activity semantics: Schedule, Temporal Constraints, Responsibility, Session execution, Actual/Outcome/Confirmation/Reconciliation and other supported capabilities remain independent concerns.

### 2.2 Sub-Activity

A Sub-Activity is **a real Activity identity participating as the direct semantic child of another Activity**.

It is not:

```text
a Plan Step
a Session
a Schedule slice
a checklist string
a MaterialState embedded in the parent
```

A Sub-Activity therefore retains its own Activity identity and can own or participate in the same supported Activity capabilities, including its own Schedule, Session execution and B10 realized-truth chain.

The word `Sub-Activity` describes the relationship/context, not a second Activity species.

### 2.3 Session

A Session remains a bounded episode of actual execution associated with an executable subject supported by the Session domain.

For this bounded extension:

```text
Root Activity    -> 0..N Sessions
Sub-Activity     -> 0..N Sessions
Session          -> 0 child Sessions
```

Session internal pause/resume intervals or execution phases do not create nested Session identities.

## 3. Bounded decomposition cardinality

The accepted v1 Activity decomposition depth is deliberately bounded:

```text
Root Activity
└── 0..N direct Sub-Activities
```

Forbidden in v1:

```text
Root Activity
└── Sub-Activity
    └── Sub-Activity   ❌
```

Hard invariants:

1. one Activity may have zero or many direct Sub-Activities;
2. one Activity may have at most one direct Sub-Activity parent;
3. a Sub-Activity cannot itself be a parent in the same relation;
4. an Activity cannot parent itself;
5. cycles are impossible by construction and must still be rejected defensively;
6. parent and child must belong to the same authorized/self scope for the self-personal vertical;
7. deleting/archiving/replacing an Activity must not silently rewrite another Activity identity or its history.

The depth bound is a current product/domain constraint, not a claim that arbitrary recursive work trees are universally invalid. A future extension requires an explicit semantic review rather than silently relaxing the invariant.

## 4. Sub-Activity versus Session

The two dimensions remain orthogonal:

```text
Sub-Activity = WHAT meaningful part of the intended action exists
Session      = WHEN a bounded execution episode actually happened
```

Example:

```text
Activity: Prepare presentation
├── Sub-Activity: Research sources
│   ├── Session A
│   └── Session B
├── Sub-Activity: Create slides
│   └── Session C
└── Session D attributed directly to the root Activity
```

Temporal splitting must never manufacture fake Sub-Activities. Semantic decomposition must never be inferred merely because multiple Sessions exist.

## 5. Session capability versus Session identity

Create/configuration may declare that an Activity supports Session-based execution and may configure supported execution policy/constraints.

That configuration is not itself a Session.

```text
Create-time execution policy
!= future Session record
```

A real Session identity is created only when truthful execution is started/recorded/imported through a supported Session path.

The current B14 candidate that infers `Session enabled` solely from the existence of `session.active_duration` is **not sufficient as the final semantic model**. Minimum active duration is one Session constraint, not the identity of the Session capability itself.

## 6. Temporal containment of Sub-Activities

A Sub-Activity is semantically contained by its parent Activity and must not acquire an accepted placement that contradicts the parent temporal envelope.

### 6.1 Exact parent placement

If the parent has a finite accepted interval:

```text
parent_start <= child_start
child_end <= parent_end
```

A child placement outside that interval is invalid.

### 6.2 Date-span / all-day parent envelope

A child placement must be fully contained by the parent civil-date span under the accepted timezone/calendar interpretation.

### 6.3 Parent without a provable finite envelope

If the parent has no accepted placement, a child may remain unplaced. An independently accepted child placement is allowed only when it can be proven to fit a bounded admissible parent window supplied by canonical temporal rules.

If no such bounded parent envelope can be established, the system must not claim containment; the child remains unplaced until a coherent placement can be admitted.

### 6.4 Mutation after creation

Containment is not a Create-only validation.

A later child reschedule outside the parent envelope must be rejected. A parent reschedule/unschedule that would invalidate already accepted child placements must not silently strand or move children. It requires either:

```text
an atomic/coordinated mutation that preserves containment
or
a guarded refusal requiring explicit user resolution
```

No implicit cascade mutation is authorized by this decision.

### 6.5 Constraint inheritance

The containment relation does **not** copy every parent Temporal Constraint onto every child.

The child is evaluated against:

```text
its own applicable constraints
+
the relational parent-containment rule
```

Any future inheritance of another parent rule requires an explicit typed semantic decision.

## 7. Realized truth and completion

### 7.1 Activity and Sub-Activity

Because a Sub-Activity is a real Activity identity, both parent and child can independently participate in the B10 chain:

```text
Actual -> Outcome -> Confirmation -> Reconciliation
```

### 7.2 No implicit reality propagation

The following are forbidden unless a future explicit policy says otherwise:

```text
child Actual/completion -> automatically writes parent Actual      ❌
parent Actual/completion -> automatically writes child Actual      ❌
all children complete    -> automatically fabricates parent Actual ❌
Session END              -> automatically writes Activity Actual    ❌
```

Children can constrain whether a parent completion action is admissible or requires acknowledgement, but they do not manufacture reality for another Activity.

### 7.3 Direct-child completion guard

The bounded model supports a future typed parent policy over **direct children only**:

```text
none     = parent reality/completion is independent
confirm  = unresolved required children produce an explicit acknowledgement gate
block    = unresolved required children prevent the guarded parent completion action
```

A parent-child relation may mark a child as required or optional for this guard. Optional children do not block the parent under `block`.

These policies govern admission of a parent action; they do not mutate children.

## 8. Session truth versus B10 Actual

A Session is already truthful execution history. B10 Actual currently has native subject families:

```text
Activity
Event
Occurrence
```

and explicitly does not treat Session as an Actual identity.

Therefore this extension does not create `Actual(Session)` merely to say that a Session occurred.

A Session may be exact evidence/basis for the Actual of its Activity/Sub-Activity, and Session history may have its own correction/provenance/attestation semantics where supported. That remains distinct from duplicating Session timing into a second Actual owner.

## 9. Event boundary

Event remains occurrence-centred and distinct from Activity.

This bounded Activity-decomposition extension does **not** add:

```text
Event -> Sub-Event
Event -> Session runtime
```

merely for UI symmetry.

Event continues to support its B10 realized-truth chain. Executable work associated with an Event should be modeled through an explicit Event/Activity relationship when that relation is separately reviewed and accepted.

## 10. Plan / Step boundary

B13 remains valid and unchanged:

```text
Plan != Activity
Step != Activity
Dependency != hierarchy
structure membership != Session
```

Plan Step is retained for internal Plan structure, ordering, dependencies and execution intent. It is not the implementation of Activity/Sub-Activity decomposition.

The existence of Activity Sub-Activities does not delete, deprecate or weaken Plan/Step.

## 11. UI projection boundary

The Domain does not require a pre-created Session row to be visible under an Activity.

A product surface may render:

```text
Corsa                         [Play]
```

and create a distinct Session only when execution starts. The same applies to a Sub-Activity.

This is a UI projection convenience, not identity collapse:

```text
Activity != Session
Sub-Activity(Activity) != Session
```

## 12. Current invariants added by this decision

1. Sub-Activity is a real Activity identity in a typed direct-parent relation.
2. Sub-Activity is not a Plan Step.
3. Root Activity may have 0..N direct Sub-Activities.
4. A Sub-Activity has at most one direct parent in this relation.
5. Sub-Activity cannot itself own another Sub-Activity in bounded v1.
6. Root Activity and Sub-Activity may each have 0..N Sessions.
7. Session cannot own a child Session.
8. Session internal pause/active phases are not child Sessions.
9. Parent/child Schedule containment is a persistent admissibility invariant, not a Create-only check.
10. Parent and child B10 truth are independent identities.
11. Completion/reality never cascades implicitly across parent/child.
12. Completion guards may warn/confirm/block without fabricating another subject's Actual.
13. Session END does not establish Activity/Sub-Activity completion.
14. Session capability is not defined merely by minimum-duration constraint presence.
15. Event does not acquire Activity decomposition or B08 Session runtime by symmetry.
16. Plan/Step remains a separate canonical structure and is not repurposed.

## 13. Implementation consequence

This decision authorizes a future vertical implementation, but does not itself claim persistence/API/UI support.

The implementation must proceed through:

```text
Logical relationship contract
-> Physical/PostgreSQL relationship contract
-> forward-only Alembic + Dictionary + ORM/catalog proof
-> guarded backend/application commands
-> HTTP/OpenAPI/generated client where public
-> Create authoring
-> Timeline/card runtime
-> focused local tests
-> real-app acceptance
```

No UI control may be presented as persisted until the corresponding canonical path exists.
