# Timeline / Temporal-Operational — Workstream Handoff

- **Status:** B04 ✅ CLOSED / PROVEN → B05-A ✅ CLOSED / PROVEN → B05-B active
- **Reconciled:** 2026-09-20
- **Branch:** `feature/timeline-temporal-operational`
- **Current roadmap:** `docs/workstreams/timeline-temporal-operational-roadmap.md`
- **Current live map/ledger:** `docs/workstreams/timeline-temporal-operational-map.md`
- **B04 execution authority:** `docs/workstreams/timeline-temporal-operational-b04-execution-plan.md`
- **B04-E closure:** `docs/workstreams/timeline-temporal-operational-b04-e-closure-2026-09-19.md`
- **B04 whole-block closure:** `docs/workstreams/timeline-temporal-operational-b04-f-closure-2026-09-20.md`
- **B05 execution plan / pre-scope:** `docs/workstreams/timeline-temporal-operational-b05-execution-plan.md`
- **Timeline candidate DB overlay:** `docs/database/timeline-temporal-operational.md`
- **CI:** no CI launch is implied or authorized

## 1. Current workstream position

```text
B00 Real Data Spine                              ✅ CLOSED / PROVEN
B01 Activity Core                                ✅ CLOSED / PROVEN
B02 Schedule Core                                ✅ CLOSED / PROVEN
B03 Event Core                                   ✅ CLOSED / PROVEN
PRE-B04 DB/API GOVERNANCE                        ✅ CLOSED / FROZEN
B04 Temporal Constraints + Movement Policy       ✅ CLOSED / PROVEN
├─ B04-A Temporal Constraint canonical core      ✅ CLOSED / PROVEN
├─ B04-B Boundary / Deadline                     ✅ CLOSED / PROVEN
├─ B04-C Windows / Preferences / Evaluation      ✅ CLOSED / PROVEN
├─ B04-D Movement Policy                         ✅ CLOSED / PROVEN
├─ B04-E Advanced-family applicability           ✅ CLOSED / PROVEN
└─ B04-F Whole-B04 closure                       ✅ CLOSED / PROVEN
B05 Product Organization                         🟡 A1 CREATE/LIST / PROOF PENDING
...
B15 Whole Vertical Closure                       ⬜
```

Current candidate DB:

```text
PostgreSQL 18.6
Alembic source 20260920_46
Expected topology 123|5|54|90|245|170|354|0|0|0 (B05-B direct proof pending)
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
20260920_42 B04-F Schedule hard-constraint guard
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
DATABASE_CURRENT_TOPOLOGY                         116|5|44|90|233|153|331|0|0|0
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

## 9. B04 whole-block closure

Closure authority: `timeline-temporal-operational-b04-f-closure-2026-09-20.md`.

It records compact final PostgreSQL/web proof, Dictionary/Alembic reconciliation and the accepted real-stack manual hard-window flow. `Fascia` remains a B02 coarse Schedule placement, not a B04 constraint.

## 10. Current gate

```text
B04 ✅ CLOSED / PROVEN
B05-A ✅ CLOSED / PROVEN at `_45`
B05-B 🟡 `_46` SOURCE IMPLEMENTED / DIRECT PROOF PENDING
```

B05-A `_43`–`_45` closed with the user's direct `_45` catalog pass. B05-B `_46` creates typed Activity/Event actor-local primary assignment and immutable acceptance receipts, atomically binds new creates, inventories legacy unassigned items and rejects archived areas as new targets. Four assignment/inventory HTTP operations, exact API inventory, OpenAPI/client and direct PostgreSQL tests accompany it. B05-D retains ownership of real frontend grouping/create migration. No CI/Actions are launched.

Local proof to run on the user's PostgreSQL-equipped checkout after pulling `_46`:

```bash
cd ~/projects/dante/apps/backend
uv run --locked pytest -q --no-cov -m postgres \
  tests/integration/temporal/test_b05_life_area_catalog.py \
  tests/integration/temporal/test_b05_primary_life_area_assignment.py \
  tests/integration/database/test_database_current_catalog.py \
  tests/integration/database/test_b04_d_movement_catalog_probe.py \
  tests/integration/database/test_b04_e_duration_catalog_probe.py \
  tests/integration/temporal/test_b01_activity_core.py \
  tests/integration/temporal/test_b03_event_core.py \
  tests/integration/temporal/test_b04_f_constrained_activity_application.py
```

This `_46` command has not yet been run in a PostgreSQL-equipped environment; B05-B is not closed until its direct result is inspected. Any failed topology/ACL/application invariant must be repaired forward before a B05-B closure record is written.
