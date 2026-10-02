# Timeline / Temporal-Operational — B14 U5 Sub-Activity + Session semantic scope freeze

- **Status:** PRODUCT / SEMANTIC DIRECTION FROZEN — READY FOR U6 END-TO-END IMPLEMENTATION
- **Date:** 2026-10-02
- **Branch:** `feature/timeline-temporal-operational`
- **Parent cycle:** B14 + B07 Product/UI consolidation
- **Previous proven product checkpoint:** `5e79f556` — user-run web typecheck PASS; 7 focused files / 14 tests PASS
- **Canonical clarification commit:** `792eb8a3768d14edb7a8cc984dbb1836999cfb9a`
- **Next implementation gate:** `docs/workstreams/timeline-temporal-operational-b14-u6-end-to-end-gate-2026-10-02.md`
- **CI:** not authorized; user runs local gates

## 1. Why U5 exists

During the Advanced Activity UI consolidation, the product needed a precise distinction between:

```text
Sub-Activity
Session
planned execution slice
Plan Step
Actual / completion truth
```

The first U4 exploration temporarily treated `+ Sessione` as a child-like Create concept and explored whether B13 Plan Step might stand in for a Sub-Activity.

The deeper Domain/Logical/Physical audit shows that those are different concepts and that the original Activity model had already separated semantic Sub-Activity decomposition from temporal Session splitting.

U5 freezes both the semantic boundary and the product direction required to implement the complete vertical next.

## 2. Compatibility audit

Reviewed authority includes:

```text
docs/domain/concepts/activity.md
docs/domain/concepts/session.md
docs/domain/concepts/event.md
docs/domain/concepts/plan.md
docs/domain/concepts/temporal-constraint.md
docs/domain/decisions/activity-subactivity-session-bounded-v1.md
docs/logical-model/whole-logical-model-v1.md
docs/logical-model/slices/time-reality-v1.md
docs/logical-model/slices/activity-subactivity-session-bounded-v1.md
docs/physical-model/pm-12-accepted-physical-model-v1.md
docs/physical-model/activity-subactivity-session-overlay-v1.md
docs/database/timeline-temporal-operational.md
docs/database/activity-subactivity-session-contract.md
docs/workstreams/timeline-temporal-operational-roadmap.md
docs/workstreams/timeline-temporal-operational-b13-a-scope-2026-09-28.md
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
Session      = truthful bounded episode of actual execution
```

Therefore U5 does not invent a second generic work-item ontology.

## 3. Canonical U5 decisions

### Activity decomposition

```text
Root Activity
├── 0..N direct Sub-Activities
├── 0..N planned execution slices / placements
└── 0..N actual Sessions once execution truth exists

Sub-Activity
├── 0..N planned execution slices / placements
└── 0..N actual Sessions once execution truth exists
```

A Sub-Activity is a real Activity identity in a typed direct-parent relationship.

Bounded v1 depth:

```text
root -> child allowed
root -> child -> child forbidden
```

A child has at most one current parent in this relation.

### Planned execution slice versus Session

The UI may naturally call a future execution slice **Sessione**. Under the hood it is not a B08 Session yet.

Canonical rule:

```text
planned execution slice = Schedule/planning truth
actual execution slice  = Session truth
```

Create/Advanced may therefore display planned Session rows, but must not create future Session records.

A real Session may be materialized only when actual execution is captured through a supported path:

```text
live Start / Play
manual retrospective record
external import
approved inferred capture
```

`Play` is mandatory only for the live path; it is not mandatory for Session semantics in general.

### Session capability

Create configures whether/how an Activity supports Session capture; it does not create a future Session.

Logical capability modes frozen for implementation review:

```text
disabled
record
live
record_and_live
```

Meaning:

```text
disabled         no Session capture surface
record           manual/imported truthful Session recording
live             Play/Pause/Resume/End live capture
record_and_live  both
```

Existing `session.active_duration` remains a Temporal Constraint and is not sufficient as the final capability owner.

### Session lifecycle

```text
Session != Sub-Activity
Session != Schedule
Session != Actual
Session END != Activity completion
Session -> child Session forbidden
```

Pause/resume/active intervals belong to one Session identity.

### Planned slice passes without execution truth

When a planned execution slice expires and no Session or Actual has been recorded:

```text
planned history remains
execution truth remains unknown
```

The system must not automatically infer:

```text
not done
skipped
failed
completed
Actual(false)
Reconciliation
```

A configured follow-up/reality policy may instead surface an item for user review in `Da risolvere`.

### Reality

Root and child Activities independently use B10:

```text
Actual -> Outcome -> Confirmation -> Reconciliation
```

No reality/completion cascade is implicit.

### Parent child guard

Typed modes:

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

### Event

Event remains occurrence-centred and follows the canonical default path:

```text
Event -> Schedule -> Actual event occurrence / attendance / outcome
```

No Sub-Event or Event-owned B08 Session runtime is added by symmetry.

A Session related to an Event is valid only when a genuinely distinct executable episode exists, for example hands-on work during a workshop. Merely attending or the Event occurring does not require a Session duplicate.

The current U6 vertical therefore does not add generic `Sessione` authoring to Event.

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
+ Sessione as a real future Session identity in Create     REJECTED
Session capability inferred solely from active-duration    PROVISIONAL / MUST BE REPLACED
runtime Play/Pause/End controls inside Create              REJECTED
```

Preserved U4 product rule:

```text
Create/Advanced = configure future plan + capability/policy
created card/detail = perform runtime action
```

The proven compact B08 card runtime remains reusable after its visibility source is changed to the explicit Activity execution policy.

## 6. `Da risolvere` is now a real product queue

The right-rail `Da risolvere` surface is no longer treated as a visual mockup.

It becomes the product destination for **open user-resolution work derived from canonical truth and configured policies**.

Important boundary:

```text
Da risolvere item != Reconciliation
```

A real B10 Reconciliation is only one possible reason for a queue item.

The queue may surface typed unresolved conditions such as:

```text
realization review needed / Actual missing under an explicit review policy
Outcome required or outcome review due
Confirmation required / attestation requested
open B10 Reconciliation
planned execution slice passed and configured follow-up asks what happened
other already-implemented vertical states that explicitly require a user decision
```

It must not create negative truth merely because time passed.

Every card must be backed by a real canonical subject/reason and must expose only actions that dispatch to the actual owning vertical. Static fixture/mock rows are removed from the production surface.

The badge count is derived from real open items. After a canonical action resolves the condition, reload must reconstruct the queue without that item unless another unresolved reason still applies.

Queue-specific persistence is not introduced merely to make the panel exist. If later UX requires snooze/dismiss semantics that cannot be derived from owning canonical state, that receives its own explicit review.

## 7. `Da risolvere` product shape frozen for U6

The current right-rail visual composition is retained as the product direction:

```text
Cattura
...
Da risolvere   [count]
  ├── typed status/reason
  ├── subject title
  ├── concise reason
  ├── relevant time/context
  └── direct canonical action(s) / Dettagli
```

Examples of valid action ownership:

```text
"L'hai fatta?" / realization review -> B10 Actual path
Outcome review                         -> B10 Outcome path
Conferma                               -> B10 Confirmation path
Resolve conflict                       -> B10 Reconciliation path
Record execution                       -> B08 Session path when capability allows it
Reschedule / skip / fallback           -> owning Schedule/Occurrence policy path
```

No one generic `resolve=true` command is authorized.

## 8. No implementation claim in this freeze

U5 documentation does not claim:

```text
new tables
new migration
new backend command
new API/OpenAPI/client
new Sub-Activity UI
final Session capability persistence
real Da risolvere read model
```

No code test is required merely to prove Markdown changes. The previous `5e79f556` product gate remains the latest user-reported code proof before U6 implementation.

## 9. Required vertical implementation sequence

The next cycle executes the whole bounded vertical, not another disconnected UI mock:

```text
1. re-read live branch + roadmap/map/handoff + Domain/Logical/Physical/DB authority
2. discover exact current Alembic/database/runtime contracts
3. implement forward-only Activity decomposition + parent guard + explicit execution policy persistence
4. reconcile Dictionary / ORM / catalog / ACL
5. implement guarded backend commands + temporal containment admission
6. integrate B10 independent parent/child reality + child completion guard
7. author future planned execution slices without creating Session truth
8. expose HTTP/OpenAPI/generated client for the new canonical capabilities
9. build Advanced Create root + direct Sub-Activities + planned Session rows + policies
10. reconstruct the full draft/tree from canonical reads after reload
11. switch Timeline/card B08 visibility to explicit execution policy
12. provide live Play/Pause/Resume/End only post-create and only for live-capable Activities
13. keep Event on its Event/B10 path without generic B08 Session symmetry
14. replace mock `Da risolvere` with the real typed resolution queue
15. wire every queue action to the owning canonical vertical
16. run focused backend/web/generated/catalog gates locally by the user
17. perform real-app visual/behavior acceptance
18. reconcile roadmap/map/handoff/consolidation ledger and prepare B15
```

## 10. Mandatory proof themes

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
planned execution slice != Session row
live Play creates actual Session only when execution starts
manual/imported Session remains valid without Play
expired planned slice does not fabricate negative Actual/skip/Reconciliation
explicit Session capability independent of duration constraints
Session cannot nest Session
Event does not gain Session runtime by symmetry
Da risolvere contains no production mock rows
Da risolvere reason/action maps to canonical owning refs and commands
resolved queue state reconstructs correctly after reload
B08/B10/B12/B13 regressions remain green
exact database catalog/dictionary gate
generated client deterministic
web typecheck + focused UI tests
real-app walkthrough
```

## 11. U6 continuation boundary

Product direction is now frozen enough to implement.

The next implementation authority is:

```text
docs/workstreams/timeline-temporal-operational-b14-u6-end-to-end-gate-2026-10-02.md
```

U6 must execute the complete bounded vertical end-to-end. It must not race ahead with frontend-only controls, invent future Session records, collapse `Da risolvere` into B10 Reconciliation, or add Event Session runtime by symmetry.