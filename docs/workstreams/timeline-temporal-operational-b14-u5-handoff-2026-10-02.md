# Timeline / Temporal-Operational — B14 U5 handoff

- **Date:** 2026-10-02
- **Branch:** `feature/timeline-temporal-operational`
- **Status:** DOCUMENTATION / SEMANTIC FREEZE COMPLETE; IMPLEMENTATION WAITING FOR USER UI FREEZE
- **Previous proven code checkpoint:** `5e79f556`
- **Previous user-reported gate:** web typecheck PASS; 7 focused test files / 14 tests PASS
- **CI:** not authorized

## 1. Current truth

The repository currently contains a proven B14/U4 prototype that:

- separates post-create B08 Session controls from B10 realized-truth controls;
- mounts compact B08 runtime actions on eligible Activity cards;
- currently derives eligibility from an active `session.active_duration` constraint.

That code proof remains valid for the code that was tested, but the eligibility inference is now explicitly **provisional** and is not the final Domain model.

The U5 semantic audit concluded that Session capability must become explicit and separate from its temporal constraints.

## 2. Accepted semantics to carry forward

### Activity / Sub-Activity

```text
Root Activity
├── 0..N direct Sub-Activities
└── 0..N Sessions

Sub-Activity
└── 0..N Sessions
```

`Sub-Activity` is a relationship/context over a real Activity identity, not a new identity family and not a Plan Step.

Maximum bounded work depth for v1 is two levels: root + direct child.

### Session

A Session is truthful execution, not a structural child.

```text
Session cannot contain Session
Session END != Activity completion
Session != Actual
```

Create configures Session capability/policy; runtime Session identities are created only by truthful execution/recording paths.

### Reality

Root and child Activity truth are independent:

```text
Actual -> Outcome -> Confirmation -> Reconciliation
```

No implicit parent/child truth cascade.

### Child guard

Future direct-child guard modes:

```text
none
confirm
block
```

Relations may be required/optional. The guard affects admission/acknowledgement only.

### Temporal containment

A child placement must fit inside the canonical parent temporal envelope. The rule applies to Create and later temporal mutation.

Parent/child temporal changes never silently cascade accepted Schedule mutation.

### Event

No Event Sub-Activity or B08 Session runtime is added in U5.

### Plan / Step

B13 remains unchanged and independent. Step is retained; it is not Sub-Activity.

## 3. New authority documents

Read these first before U5 implementation:

```text
docs/domain/decisions/activity-subactivity-session-bounded-v1.md
docs/logical-model/slices/activity-subactivity-session-bounded-v1.md
docs/physical-model/activity-subactivity-session-overlay-v1.md
docs/database/activity-subactivity-session-contract.md
docs/workstreams/timeline-temporal-operational-b14-u5-subactivity-session-scope-2026-10-02.md
```

Then continue to respect the normal authorities:

```text
docs/workstreams/timeline-temporal-operational-roadmap.md
docs/workstreams/timeline-temporal-operational-map.md
docs/workstreams/timeline-temporal-operational-handoff.md
docs/domain/concepts/activity.md
docs/domain/concepts/session.md
docs/domain/concepts/event.md
docs/domain/concepts/plan.md
docs/logical-model/whole-logical-model-v1.md
docs/physical-model/pm-12-accepted-physical-model-v1.md
docs/database/timeline-temporal-operational.md
```

The whole-logical and PM-12 files are frozen historic baselines. Do not rewrite them to hide evolution; use the U5 overlays.

## 4. Explicitly superseded exploratory assumptions

Do not continue these U4 directions:

```text
Sub-Activity = Plan Step + Activity                 NO
Session as a node added beneath Activity in Create  NO
Play/Pause/End controls inside Create               NO
active-duration constraint == Session capability    NO
```

Correct direction:

```text
Sub-Activity = Activity identity + typed direct-parent relation
Session = runtime truth owned by root/child Activity
Create = policy/configuration
card/detail = runtime action
```

## 5. Current code that should be reused, not duplicated

When implementation resumes:

- reuse B08 Session Start/Pause/Resume/End runtime and existing Session history/metrics;
- reuse B10 Activity Actual/Outcome/Confirmation/Reconciliation path for both root and child Activities;
- reuse B04 Schedule/Temporal Constraint authority for temporal admission, adding relationship containment rather than copying constraints;
- preserve B13 Plan/Step and its tests;
- reuse the current compact card Session controls once their visibility comes from explicit execution policy;
- preserve B14 Quick/Advanced draft continuity and existing canonical authoring path.

## 6. Implementation hold point

Do **not** publish DDL or new UI until the user gives the desired UI shape for:

```text
root Activity row
Sub-Activity authoring row(s)
Session capability controls on root/child
reality/completion policy controls
required/optional child semantics
parent child-guard selection
child timing/placement controls
post-create card presentation
```

Once the UI semantics are frozen, implement the whole vertical end-to-end rather than another decorative shell.

## 7. First implementation discovery after UI freeze

Before DDL:

1. re-read current branch head;
2. inspect exact current Alembic head;
3. inspect Activity identity/current-state mappings and guarded authoring functions;
4. inspect B04 Schedule admission/reschedule functions and Temporal Constraint evaluators;
5. inspect B08 Session subject/runtime tables and routines;
6. inspect B10 Activity Actual readers/writers and completion semantics used by the product;
7. inspect B13 mappings/tests to protect Plan/Step regression;
8. choose exact PostgreSQL family/routine names consistent with current patterns;
9. write an implementation checkpoint before migration.

## 8. Required implementation order

```text
DB discovery
-> forward migration + Dictionary/ORM/catalog
-> guarded backend
-> containment + parent mutation guards
-> B10 direct-child completion guard
-> API/OpenAPI/client
-> Create authoring
-> canonical readback/reload
-> card runtime
-> local backend/web gates
-> real user walkthrough
-> live roadmap/map/handoff reconciliation
```

## 9. Test ownership

The user runs all local tests on `~/projects/dante`.

No GitHub Actions/CI.

Do not mark U5 implementation PROVEN until the user reports the requested local gates.
