# Timeline / Temporal-Operational — Candidate Database Overlay

- **Status:** CURRENT CANDIDATE DATABASE AUTHORITY
- **Reconciled:** 2026-09-19
- **Branch:** `feature/timeline-temporal-operational`
- **Protected-main baseline:** `20260906_18` / `89|5|18|77|173|91|272|0|0|0`
- **Candidate head:** `20260919_39`
- **Candidate topology:** `115|5|42|89|232|152|329|0|0|0`
- **Whole-DB SoR:** `README.md`
- **Machine-readable authority:** `dictionary/`
- **Persistence doctrine:** `../development/backend-cp6-02-postgresql-persistence-constitution.md`
- **B04-D closure authority:** `../workstreams/timeline-temporal-operational-b04-d-closure-2026-09-19.md`

## 1. Purpose and authority boundary

This file is the human-readable database overlay for Timeline candidate-only persistence. Candidate truth becomes protected-main truth only after integration gates and protected-main merge/readback.

## 2. Candidate evolution

```text
20260906_18 protected-main baseline
    ↓
20260908_19 B01 Activity core
    ↓
20260909_20 → 20260915_26 B02 Schedule core / closure
    ↓
20260916_27 → 20260917_29 B03 Event core / closure
    ↓
20260918_30 → 20260918_33 B04-A Temporal Constraint core / API activation
    ↓
20260919_34 B04-B absolute boundary / deadline
    ↓
20260919_35 → 20260919_36 B04-C absolute windows / runtime-read ACL
    ↓
20260919_37 B04-D Movement Policy core
    ↓
20260919_38 B04-D governed absolute Schedule move
    ↓
20260919_39 B04-D proposal-accept replay fix
```

## 3. Temporal Constraint authority through B04-C

Accepted absolute boundary matrix:

```text
earliest_start     + schedule.start
latest_start       + schedule.start
latest_completion  + schedule.completion
```

Accepted absolute window matrix:

```text
start_within              + schedule.start
completion_within         + schedule.completion
full_placement_contained  + schedule.placement
placement_overlaps        + schedule.placement
```

Temporal Constraint remains independent canonical rule truth. B04-C evaluation is derived, non-persistent, and distinguishes hard validity from soft preference without performing automatic movement.

## 4. B04-D Movement Policy authority ✅ CLOSED / PROVEN

Movement Policy is represented as a typed `schedule.movement_policy` MaterialState facet owned by an accepted Schedule. It is not a generic Movement root, not a Temporal Constraint, and not Authority itself.

Canonical policy state:

```text
automatic_movement_code  blocked | automatic
acceptance_path_code     direct | confirmation_required
```

Canonical persistence/control:

```text
schedule_movement_policy_state
schedule_movement_policy_current_history
schedule_movement_policy_mutation_operation
schedule_move_proposal
schedule_move_request_operation
schedule_move_accept_operation
```

Runtime capability surface:

```text
mutate_self_schedule_movement_policy(...)
resolve_self_schedule_movement_policy(...)
request_self_absolute_schedule_move(...)
accept_self_absolute_schedule_move_proposal(...)
```

Internal non-runtime helpers:

```text
enforce_schedule_movement_policy_history()
assert_absolute_schedule_move_hard_admissible(...)
apply_governed_absolute_schedule_move(...)
```

Enforcement semantics:

```text
blocked
  → no automatic move

automatic + direct
  → commit only if candidate is hard-admissible and placement CAS still matches

automatic + confirmation_required
  → persist proposal only
  → explicit acceptance rechecks placement, policy and hard constraints before commit
```

Proposal state never becomes accepted Schedule truth by creation alone. Policy revision appends its own MaterialState/current-history and does not revise Schedule placement.

Hard constraint violation or non-evaluable hard constraint fails closed. Soft constraint violation does not block an otherwise authorized automatic move.

No public Temporal HTTP API was added in B04-D, therefore OpenAPI and generated API-client artifacts are intentionally unchanged.

## 5. Current candidate topology

```text
Alembic     20260919_39
Tables      115
Views       5
Routines    42
Triggers    89
Indexes     232
FKs         152
CHECKs      329
Enums       0
Domains     0
Sequences   0
Materialized/partitioned 0
RLS         0
```

## 6. Non-collapse invariants

```text
Schedule != Temporal Constraint
Schedule != Movement Policy
Temporal Constraint != Movement Policy
Movement Policy != solver result
Movement Policy != Authority itself
proposal != accepted effect
policy revision != Schedule revision
constraint revision != Schedule revision
hard planning violation != impossible reality
evaluation != solver decision
violation != automatic mutation
Schedule != Session != Actual
Actual != Outcome
```

B12 owns candidate search/optimization/replanning. B04-D only governs acceptance of a supplied candidate against current policy and hard constraints.

## 7. Proof state

```text
B01 ✅ CLOSED / PROVEN
B02 ✅ CLOSED / PROVEN
B03 ✅ CLOSED / PROVEN
B04  🟡 IN PROGRESS
├─ B04-A ✅ CLOSED / PROVEN
├─ B04-B ✅ CLOSED / PROVEN
├─ B04-C ✅ CLOSED / PROVEN
├─ B04-D ✅ CLOSED / PROVEN
├─ B04-E ⬜ NEXT
└─ B04-F ⬜
```

Observed B04-D evidence:

```text
Movement Policy / governed move / ACL tests       7 PASS
whole catalog + B04-D catalog reconciliation      3 PASS
DATABASE_CURRENT_TOPOLOGY                         115|5|42|89|232|152|329|0|0|0
```

## 8. Next persistence boundary

B04-E is next. Advanced duration/spacing/relative families activate only where current canonical anchors support truthful evaluation. Session-, Actual-, Occurrence- or solver-dependent semantics remain deferred to their owning blocks.

B04-F whole-B04 closure remains required before B05.
