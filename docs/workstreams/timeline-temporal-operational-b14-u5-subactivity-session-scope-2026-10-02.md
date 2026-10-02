# Timeline / Temporal-Operational — B14 U5 Sub-Activity + Session semantic scope freeze

- **Status:** SEMANTIC/DOCUMENTATION FREEZE COMPLETE — IMPLEMENTATION HELD FOR USER UI DIRECTION
- **Date:** 2026-10-02
- **Branch:** `feature/timeline-temporal-operational`
- **Parent cycle:** B14 + B07 Product/UI consolidation
- **Previous proven product checkpoint:** `5e79f556` — user-run web typecheck PASS; 7 focused files / 14 tests PASS
- **CI:** not authorized; user runs local gates

## 1. Why U5 exists

During the Advanced Activity UI consolidation, the product needed a precise distinction between:

```text
Sub-Activity
Session
Plan Step
Actual / completion truth
```

The first U4 exploration temporarily treated `+ Sessione` as a child-like Create concept and explored whether B13 Plan Step might stand in for a Sub-Activity.

The deeper Domain/Logical/Physical audit shows that those are different concepts and that the original Activity model had already separated semantic Sub-Activity decomposition from temporal Session splitting.

U5 therefore freezes the canonical semantics before any additional UI or DDL work.

## 2. Compatibility audit

Reviewed authority includes:

```text
docs/domain/concepts/activity.md
docs/domain/concepts/session.md
docs/domain/concepts/event.md
docs/domain/concepts/plan.md
docs/domain/concepts/temporal-constraint.md
docs/logical-model/whole-logical-model-v1.md
docs/logical-model/slices/time-reality-v1.md
docs/physical-model/pm-12-accepted-physical-model-v1.md
docs/database/timeline-temporal-operational.md
docs/workstreams/timeline-temporal-operational-roadmap.md
docs/workstreams/timeline-temporal-operational-b13-a-scope-2026-09-28.md
docs/workstreams/timeline-temporal-operational-b13-a-closure-2026-09-28.md
docs/workstreams/timeline-temporal-operational-b13-c-scope-2026-09-29.md
B08/B10/B13 implemented boundaries and current B14 U4 handoff
```

Verdict:

```text
COMPATIBLE as a bounded activation/extension of existing Activity semantics
```

The accepted Activity Domain already distinguishes:

```text
Sub-Activity = semantic decomposition of intended action
Session      = temporal decomposition / truthful execution episode
```

Therefore U5 does not invent a second generic work-item ontology.

## 3. Canonical U5 decisions

### Activity decomposition

```text
Root Activity
├── 0..N direct Sub-Activities
└── 0..N Sessions

Sub-Activity
└── 0..N Sessions
```

A Sub-Activity is a real Activity identity in a typed direct-parent relationship.

Bounded v1 depth:

```text
root -> child allowed
root -> child -> child forbidden
```

A child has at most one current parent in this relation.

### Session

```text
Session != Sub-Activity
Session != Schedule
Session != Actual
Session END != Activity completion
Session -> child Session forbidden
```

Pause/resume/active intervals belong to one Session identity.

### Reality

Root and child Activities independently use B10:

```text
Actual -> Outcome -> Confirmation -> Reconciliation
```

No reality/completion cascade is implicit.

### Parent child guard

Future typed modes:

```text
none
confirm
block
```

Each direct relation may be `required` or `optional` for that guard.

The gate governs admission/acknowledgement; it does not write child or parent truth automatically.

### Temporal containment

A child accepted placement must fit inside the canonical parent envelope.

This applies during Create and subsequent reschedule/mutation.

No frontend-only validation and no silent cascade rescheduling are accepted.

### Session capability

Create configures whether/how an Activity supports Session capture; it does not create a future Session.

Logical capability modes frozen for implementation review:

```text
disabled
record
live
record_and_live
```

Existing `session.active_duration` remains a Temporal Constraint and is not sufficient as the final capability owner.

### Event

No Sub-Event or Event-owned B08 Session runtime is added by symmetry.

Event retains B10 realized truth. Event/Activity work linkage, if needed, is a separate typed review.

### Plan / Step

B13 is preserved:

```text
Step != Activity
Plan != Activity
```

Plan Step is not Sub-Activity and is not removed.

## 4. Canonical documentation created in U5

```text
docs/domain/decisions/activity-subactivity-session-bounded-v1.md
docs/logical-model/slices/activity-subactivity-session-bounded-v1.md
docs/physical-model/activity-subactivity-session-overlay-v1.md
docs/database/activity-subactivity-session-contract.md
```

The frozen whole-logical and PM-12 historical baselines are intentionally not rewritten. Additive current overlays document the accepted extension.

## 5. U4 assumptions explicitly superseded

These exploratory U4 ideas are no longer the target semantic model:

```text
Sub-Activity implemented as Plan Step + Activity link      SUPERSEDED
+ Sessione as a structural child in Create                 SUPERSEDED
Session capability inferred solely from active-duration    PROVISIONAL / MUST BE REPLACED
runtime Play/Pause/End controls inside Create              REJECTED
```

Preserved U4 product rule:

```text
Create/Advanced = configure capability/policy
created card/detail = perform runtime action
```

The proven compact B08 card runtime remains reusable after its visibility source is changed to the explicit Activity execution policy.

## 6. No implementation claim in this freeze

U5 documentation does not claim:

```text
new tables
new migration
new backend command
new API/OpenAPI/client
new Sub-Activity UI
final Session capability persistence
```

No code test is required merely to prove Markdown creation. The previous `5e79f556` product gate remains the latest user-reported code proof before U5 implementation.

## 7. Required vertical implementation sequence after user UI direction

Once the user freezes the desired UI behavior, implementation proceeds vertically:

```text
1. live persistence discovery against current Alembic/database head
2. forward-only Activity decomposition + policies migration
3. Dictionary / ORM / catalog / ACL reconciliation
4. guarded backend commands + temporal containment admission
5. B10 parent/child completion guard integration
6. HTTP/OpenAPI/generated client
7. Create authoring for root + direct children + execution policy
8. canonical reads / reload reconstruction
9. Timeline/card Session runtime from explicit policy
10. parent/child reality controls on correct Activity refs
11. focused backend/web regression gates
12. real-app user acceptance
13. roadmap/map/handoff reconciliation and B15 preparation
```

## 8. Mandatory proof themes

The implementation cannot close without proving at least:

```text
depth <= 2
one parent maximum
no self/cycle/duplicate/cross-scope relation
required/optional state + deterministic order
history/current-state/CAS/idempotent replay
atomic/retry-safe root + child authoring
exact temporal containment
parent mutation guard
no implicit B10 cascade
Session END != completion
explicit Session capability independent of duration constraints
Session cannot nest Session
B08/B10/B12/B13 regressions remain green
exact database catalog/dictionary gate
generated client deterministic
web typecheck + focused UI tests
real-app walkthrough
```

## 9. Continuation boundary

U5 stops here deliberately.

The next input is the user's UI model for how Activity, direct Sub-Activities, Session capability and reality/completion policy are configured and rendered.

No persistence or UI implementation should race ahead of that product decision.
