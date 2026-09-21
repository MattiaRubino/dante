# Timeline / Temporal-Operational — Candidate Database Overlay

- **Status:** CURRENT CANDIDATE DATABASE AUTHORITY
- **Reconciled:** 2026-09-21
- **Branch:** `feature/timeline-temporal-operational`
- **Protected-main baseline:** `20260906_18` / `89|5|18|77|173|91|272|0|0|0`
- **Candidate source head:** `20260921_50` (B06-A candidate; pending direct proof)
- **Candidate expected topology:** `135|5|68|90|263|201|381|0|0|0` (B06-A candidate; pending direct proof)
- **Whole-DB SoR:** `README.md`
- **Machine-readable authority:** `dictionary/`
- **Persistence doctrine:** `../development/backend-cp6-02-postgresql-persistence-constitution.md`
- **B04-E closure authority:** `../workstreams/timeline-temporal-operational-b04-e-closure-2026-09-19.md`
- **B04 whole-block closure authority:** `../workstreams/timeline-temporal-operational-b04-f-closure-2026-09-20.md`
- **B05 pre-scope (no DDL):** `../workstreams/timeline-temporal-operational-b05-execution-plan.md`

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
20260919_37 → 20260919_39 B04-D Movement Policy / governed move / replay fix
    ↓
20260919_40 B04-E planned Schedule duration constraints
    ↓
20260919_41 B04-E duration runtime-read ACL
    ↓
20260920_42 B04-F Schedule hard-constraint guard
    ↓
20260920_43 B05-A self-scoped Life Area catalog create/list
20260920_44 B05-A full Life Area lifecycle
20260920_45 B05-A receipt CHECK catalog name reconciliation
20260920_46 B05-B typed actor-local Activity/Event primary Life Area assignment
20260920_47 B05-C secondary actor-local product Tags and typed item associations
20260921_48 B05-D actor-scoped postponed Event discovery and governed replan composition
20260921_49 B06-A Routine source core, lifecycle and typed Life Area/Tag organization
20260921_50 B06-A mandatory atomic initial Routine/Recurrence companion correction
```

## 3. Temporal Constraint authority through B04-E

Accepted boundary matrix:

```text
earliest_start     + schedule.start
latest_start       + schedule.start
latest_completion  + schedule.completion
```

Accepted window matrix:

```text
start_within              + schedule.start
completion_within         + schedule.completion
full_placement_contained  + schedule.placement
placement_overlaps        + schedule.placement
```

Accepted duration matrix:

```text
minimum + schedule.placement
maximum + schedule.placement
```

Duration is exact planned Schedule placement duration only. It does not collapse estimated Activity effort, Session duration or Actual duration.

Temporal Constraint evaluation remains derived/non-persistent and now composes boundary + window + duration rules in the same canonical application evaluator.

Hard-set feasibility also accounts for duration geometry; planning-set infeasibility is not Outcome/reality.

## 4. B04-D Movement Policy authority ✅ CLOSED / PROVEN

Movement Policy is a typed `schedule.movement_policy` MaterialState facet owned by an accepted Schedule.

```text
automatic_movement_code  blocked | automatic
acceptance_path_code     direct | confirmation_required
```

Automatic direct movement and proposal acceptance both fail closed unless current hard Temporal Constraints are evaluable and satisfied.

## 5. B04-E applicability authority ✅ CLOSED / PROVEN

Implemented:

```text
TC-008 minimum / maximum planned Schedule duration
```

Deferred with explicit owner/reopening trigger:

```text
TC-009 contiguous Session duration  → B08
TC-010 spacing / recovery           → B06/B08/B10 by anchor
TC-011 relative before / after      → reviewed bounded relation/reference persistence required
```

No fake previous-time field, generic relationship root, `related_id + type`, or generic JSON rule payload was introduced.

B04-D movement admissibility is extended through hard duration rules by the same internal guard.

B04-E adds no public Temporal HTTP route; OpenAPI/client artifacts intentionally remain unchanged in E. Whole-B04 B04-F closed the exact public API/OpenAPI regression.

## 6. Current candidate topology

```text
Alembic     20260921_50
Tables      135
Views       5
Routines    68
Triggers    90
Indexes     263
FKs         201
CHECKs      381
Enums       0
Domains     0
Sequences   0
Materialized/partitioned 0
RLS         0
```

## 7. Proof state

```text
B01 ✅ CLOSED / PROVEN
B02 ✅ CLOSED / PROVEN
B03 ✅ CLOSED / PROVEN
B04  ✅ CLOSED / PROVEN
├─ B04-A ✅ CLOSED / PROVEN
├─ B04-B ✅ CLOSED / PROVEN
├─ B04-C ✅ CLOSED / PROVEN
├─ B04-D ✅ CLOSED / PROVEN
├─ B04-E ✅ CLOSED / PROVEN
└─ B04-F ✅ CLOSED / PROVEN
B05-A ✅ CLOSED / PROVEN at `_45`
B05-B ✅ CLOSED / PROVEN at `_46` (16 selected PostgreSQL tests)
B05-C ✅ CLOSED / PROVEN at `_47` (26 selected PostgreSQL tests)
```

Observed B04-E evidence:

```text
core duration + movement integration             4 PASS
application/evaluator/regression                13 PASS / 3 deselected
whole catalog + B04-E catalog reconciliation     3 PASS
DATABASE_CURRENT_TOPOLOGY                         116|5|44|90|233|153|331|0|0|0
```

## 8. Next persistence boundary

B05-A `_43`–`_45` established the LR-12 catalog and passed the user's direct `_45` catalog proof. `_46` adds two typed actor/item primary-area relations and two immutable assignment-receipt relations. Six guarded routines create/assign/list and inventory legacy unassigned rows. New Activity/Event creation requires a primary area in the same transaction; original unassigned create routines lose direct runtime EXECUTE. Archived targets reject new assignments, existing assignments remain discoverable. Neither B04 Schedule truth nor pre-B05 item rows are rewritten. `_46` passed 16 direct PostgreSQL tests; `_47` passed 26 selected tests. `_48` adds bounded Event-only postponed discovery/replan without fabricating Schedule truth, and B05-D's user-run 24 PostgreSQL/API/catalog plus 41 selected web-test gate passed. B05-E's completed real-stack manual walkthrough closes B05; no persistence topology changes were required.
