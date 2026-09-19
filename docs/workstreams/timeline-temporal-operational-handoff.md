# Timeline / Temporal-Operational — Workstream Handoff

- **Status:** B03 ✅ CLOSED / PROVEN + pre-B04 governance ✅ FROZEN + B04-A/B/C/D/E ✅ CLOSED / PROVEN → B04-F ACTIVE
- **Reconciled:** 2026-09-19
- **Branch:** `feature/timeline-temporal-operational`
- **Current roadmap:** `docs/workstreams/timeline-temporal-operational-roadmap.md`
- **Current live map/ledger:** `docs/workstreams/timeline-temporal-operational-map.md`
- **B04 execution authority:** `docs/workstreams/timeline-temporal-operational-b04-execution-plan.md`
- **B04-E closure:** `docs/workstreams/timeline-temporal-operational-b04-e-closure-2026-09-19.md`
- **Timeline candidate DB overlay:** `docs/database/timeline-temporal-operational.md`
- **CI:** no CI launch is implied or authorized

## 1. Current workstream position

```text
B00 Real Data Spine                              ✅ CLOSED / PROVEN
B01 Activity Core                                ✅ CLOSED / PROVEN
B02 Schedule Core                                ✅ CLOSED / PROVEN
B03 Event Core                                   ✅ CLOSED / PROVEN
PRE-B04 DB/API GOVERNANCE                        ✅ CLOSED / FROZEN
B04 Temporal Constraints + Movement Policy       🟡 IN PROGRESS
├─ B04-A Temporal Constraint canonical core      ✅ CLOSED / PROVEN
├─ B04-B Boundary / Deadline                     ✅ CLOSED / PROVEN
├─ B04-C Windows / Preferences / Evaluation      ✅ CLOSED / PROVEN
├─ B04-D Movement Policy                         ✅ CLOSED / PROVEN
├─ B04-E Advanced-family applicability           ✅ CLOSED / PROVEN
└─ B04-F Whole-B04 closure                       🟡 ACTIVE
B05 Product Organization                         ⬜
...
B15 Whole Vertical Closure                       ⬜
```

Current candidate DB:

```text
PostgreSQL 18.6
Alembic     20260919_41
Topology    116|5|43|90|233|153|331|0|0|0
```

## 2. Binding foundation carried forward

Permanent distinctions remain:

```text
Schedule != Temporal Constraint
Schedule != Movement Policy
Temporal Constraint != Movement Policy
Movement Policy != Authority itself
Movement Policy != solver result
proposal != accepted effect
policy revision != Schedule revision
constraint revision != Schedule revision
planned Schedule duration != Activity estimated effort
planned Schedule duration != Session duration
planned Schedule duration != Actual duration
hard planning violation != impossible reality
Schedule != Session != Actual
Actual != Outcome
```

Pre-B04 DB/API same-change governance remains binding for B04-F and later blocks.

## 3. B04-A/B/C carried forward

Temporal Constraint is a stable self-owned Activity/Event `ScopedRecordRef` dependent with immutable rule MaterialState/current/history, CAS/idempotency and typed boundary/window/duration semantics.

Accepted boundary matrix:

```text
earliest_start     → schedule.start
latest_start       → schedule.start
latest_completion  → schedule.completion
```

Accepted window matrix:

```text
start_within              → schedule.start
completion_within         → schedule.completion
full_placement_contained  → schedule.placement
placement_overlaps        → schedule.placement
```

Accepted duration matrix:

```text
minimum → schedule.placement
maximum → schedule.placement
```

Evaluation is derived/non-persistent and does not mutate Schedule.

## 4. B04-D carried forward

Movement Policy is a Schedule-owned governance facet:

```text
facet                     schedule.movement_policy
automatic_movement_code   blocked | automatic
acceptance_path_code      direct | confirmation_required
```

Automatic movement is supplied-candidate governance, not candidate search. A confirmation proposal is not accepted Schedule truth.

## 5. B04-E closure authority

B04-E activated TC-008 planned Schedule duration and closed applicability for TC-009/010/011 without pulling later-owned facts forward.

Candidate chain:

```text
20260919_39 B04-D closure
    ↓
20260919_40 B04-E planned Schedule duration constraints
    ↓
20260919_41 B04-E duration runtime-read ACL
```

Canonical B04-E object/capability:

```text
temporal_constraint_duration_state
mutate_self_schedule_duration_constraint(...)
```

Shared routines extended:

```text
enforce_temporal_constraint_rule_totality()
assert_absolute_schedule_move_hard_admissible(...)
```

Thus hard duration rules participate in canonical application evaluation and in B04-D governed automatic movement.

## 6. B04-E applicability dispositions

```text
TC-008 min/max planned Schedule duration   IMPLEMENTED / PROVEN
TC-009 contiguous Session duration         runtime deferred B08
TC-010 spacing/recovery                    deferred B06/B08/B10 by anchor
TC-011 relative before/after               deferred until reviewed bounded relation/reference persistence
```

Forbidden shortcuts remain absent:

```text
fake Activity/Event last_at
generic related_id + type
generic JSON rule payload
generic semantic Relationship root
```

## 7. B04-E proof

Observed local proof:

```text
core duration + movement integration             4 PASS
application/evaluator/regression                13 PASS / 3 deselected
whole catalog + Dictionary/SQLAlchemy/Alembic/DB 3 PASS
DATABASE_CURRENT_TOPOLOGY                         116|5|43|90|233|153|331|0|0|0
```

No public Temporal HTTP endpoint was added in B04-E; no OpenAPI/client churn is claimed for E.

Closure decision:

```text
B04-E Advanced-family applicability ✅ CLOSED / PROVEN
```

## 8. Unsupported / later-owned semantics

B04-E does not activate:

```text
Session contiguous-duration runtime
previous Session/Actual/Occurrence spacing runtime
arbitrary heterogeneous relative-reference persistence
solver candidate generation
optimization/replanning search
multi-actor grants / complete Authority model
```

## 9. Immediate active gate — B04-F

B04-F is whole-block closure. It must not add a new constraint family merely to produce more implementation work.

Required proof/reconciliation:

```text
whole B04 PostgreSQL/backend regressions
Activity/Event/Schedule integration regression
hard vs soft evaluation
Deadline passage != Outcome
Movement Policy + proposal/acceptance enforcement
duration integration
exact Temporal public API inventory
OpenAPI snapshot/export parity and generated-client check
frontend Create/edit/read/explanation audit against backend truth
real-stack/manual userTest only where product behavior cannot be proven automatically
Dictionary / SQLAlchemy / Alembic parity
final DB docs/map/roadmap/handoff/B04 closure record
```

Prototype-only UI fields are not proof.

## 10. Current gate

```text
B04-E ✅ CLOSED / PROVEN
B04-F 🟡 ACTIVE
```

Proceed with compact whole-B04 proof inventory and avoid redundant micro-test reruns. CI remains separately authorized and should not replace faster local gates.
