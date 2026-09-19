# Timeline / Temporal-Operational — Workstream Handoff

- **Status:** B03 ✅ CLOSED / PROVEN + pre-B04 governance ✅ FROZEN + B04-A/B/C/D ✅ CLOSED / PROVEN → B04-E NEXT
- **Reconciled:** 2026-09-19
- **Branch:** `feature/timeline-temporal-operational`
- **Current roadmap:** `docs/workstreams/timeline-temporal-operational-roadmap.md`
- **Current live map/ledger:** `docs/workstreams/timeline-temporal-operational-map.md`
- **B04 execution authority:** `docs/workstreams/timeline-temporal-operational-b04-execution-plan.md`
- **B04-D closure:** `docs/workstreams/timeline-temporal-operational-b04-d-closure-2026-09-19.md`
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
├─ B04-E Advanced-family applicability           ⬜ NEXT
└─ B04-F Whole-B04 closure                       ⬜
B05 Product Organization                         ⬜
...
B15 Whole Vertical Closure                       ⬜
```

Current candidate DB:

```text
PostgreSQL 18.6
Alembic     20260919_39
Topology    115|5|42|89|232|152|329|0|0|0
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
hard planning violation != impossible reality
Schedule != Session != Actual
Actual != Outcome
```

Pre-B04 DB/API same-change governance remains binding for B04-E/F and later blocks.

## 3. B04-A/B/C carried forward

Temporal Constraint is a stable self-owned Activity/Event `ScopedRecordRef` dependent with immutable rule MaterialState/current/history, CAS/idempotency and typed boundary/window semantics.

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

B04-C evaluation is derived/non-persistent and does not mutate Schedule.

## 4. B04-D semantic closure

Movement Policy is a Schedule-owned governance facet, not a generic domain root.

Canonical state:

```text
facet                     schedule.movement_policy
automatic_movement_code   blocked | automatic
acceptance_path_code      direct | confirmation_required
```

This decomposition intentionally does not copy the prototype `locked | window | confirm | free` enum into kernel truth. Temporal windows stay Temporal Constraints; broad candidate search/replanning stays B12.

## 5. B04-D persistence authority

Candidate chain:

```text
20260919_36 B04-C closure
    ↓
20260919_37 B04-D Movement Policy core
    ↓
20260919_38 B04-D governed absolute Schedule move
    ↓
20260919_39 B04-D proposal-accept replay fix
```

Canonical objects:

```text
schedule_movement_policy_state
schedule_movement_policy_current_history
schedule_movement_policy_mutation_operation
schedule_move_proposal
schedule_move_request_operation
schedule_move_accept_operation
```

Capability/integrity routines:

```text
enforce_schedule_movement_policy_history()
mutate_self_schedule_movement_policy(...)
resolve_self_schedule_movement_policy(...)
assert_absolute_schedule_move_hard_admissible(...)
apply_governed_absolute_schedule_move(...)
request_self_absolute_schedule_move(...)
accept_self_absolute_schedule_move_proposal(...)
```

`material_state_address` now admits `schedule.movement_policy`; shared MaterialState totality enforces exact owner/facet/payload exclusivity.

## 6. B04-D governed behavior

```text
blocked
  → automatic movement rejected

automatic + direct
  → current placement CAS checked
  → current policy checked
  → all current hard Temporal Constraints checked
  → only then may a new placement MaterialState become current

automatic + confirmation_required
  → request produces persistent proposal only
  → no accepted Schedule mutation yet
  → explicit acceptance rechecks placement basis, policy basis and hard constraints
  → accepted effect then appends a new placement MaterialState/current-history episode
```

Soft Temporal Constraint violations do not block an otherwise authorized automatic move. Non-evaluable current hard constraints fail closed.

Proposal creation is not accepted Schedule truth. Proposal acceptance has its own immutable idempotency receipt.

B04-D does not implement candidate search, fallback strategy, optimizer or whole multi-actor Authority semantics.

## 7. B04-D proof

Observed local proof:

```text
Movement Policy + governed move + ACL              7 PASS
whole catalog + Dictionary/SQLAlchemy/Alembic/DB   3 PASS
DATABASE_CURRENT_TOPOLOGY                           115|5|42|89|232|152|329|0|0|0
```

Proof covers:

```text
blocked automation
admissible direct auto-move
confirmation proposal without Schedule mutation
explicit proposal acceptance
stale placement CAS
stale Movement Policy basis
hard constraint rejection
soft preference non-blocking behavior
request/accept replay
history monotonicity
runtime capability ACL
dictionary/catalog/mapping exact parity
```

No public Temporal HTTP endpoint was added, so no OpenAPI/client regeneration is claimed or required for D.

Closure decision:

```text
B04-D Movement Policy ✅ CLOSED / PROVEN
```

## 8. Unsupported / later-owned semantics

B04-D does not activate:

```text
solver candidate generation
optimization/replanning search
fallback strategy
multi-actor grants / complete Authority model
Session/Actual/Outcome inference
date-span/floating/named-zone/coarse automatic move candidates
advanced duration/spacing/relative constraint families
```

## 9. Immediate next gate — B04-E

B04-E must classify and activate only the remaining advanced Temporal Constraint families that are truthful against currently canonical facts/anchors:

```text
TC-008 minimum/maximum planned placement duration
TC-009 minimum contiguous Session duration
TC-010 spacing/recovery
TC-011 relative-before/after
```

Expected discipline:

- planned Schedule duration may be implementable now if constrained specifically to placement duration;
- Session-duration runtime belongs to B08 unless a non-runtime semantic seam is all that can be truthfully closed now;
- spacing anchored on prior Session/Actual/Occurrence must not fabricate a `last_at` field;
- relative constraints require a safe typed reference contract, not generic IDs/JSON;
- each item must close as implemented or explicitly deferred with owner/reopening trigger.

## 10. Current gate

```text
B04-D ✅ CLOSED / PROVEN
B04-E ⬜ NEXT
```

Proceed with B04-E applicability freeze. CI remains separately authorized and should not replace faster local gates.
