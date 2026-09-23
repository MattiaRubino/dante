# Timeline / Temporal-Operational — Workstream Handoff

- **Status:** B04 ✅ CLOSED / PROVEN → B05 ✅ CLOSED / PROVEN → B06 ✅ CLOSED / PROVEN → POST-B06 SEQUENCING DECISION
- **Reconciled:** 2026-09-23
- **Branch:** `feature/timeline-temporal-operational`
- **Current roadmap:** `docs/workstreams/timeline-temporal-operational-roadmap.md`
- **Current live map/ledger:** `docs/workstreams/timeline-temporal-operational-map.md`
- **B04 execution authority:** `docs/workstreams/timeline-temporal-operational-b04-execution-plan.md`
- **B04-E closure:** `docs/workstreams/timeline-temporal-operational-b04-e-closure-2026-09-19.md`
- **B04 whole-block closure:** `docs/workstreams/timeline-temporal-operational-b04-f-closure-2026-09-20.md`
- **B05 execution plan / pre-scope:** `docs/workstreams/timeline-temporal-operational-b05-execution-plan.md`
- **B05-D closure:** `docs/workstreams/timeline-temporal-operational-b05-d-closure-2026-09-21.md`
- **B05 whole-block closure:** `docs/workstreams/timeline-temporal-operational-b05-e-closure-2026-09-21.md`
- **B06 execution authority:** `docs/workstreams/timeline-temporal-operational-b06-execution-plan.md`
- **B06-A closure:** `docs/workstreams/timeline-temporal-operational-b06-a-closure-2026-09-21.md`
- **B06-B closure:** `docs/workstreams/timeline-temporal-operational-b06-b-closure-2026-09-22.md`
- **B06-C implementation freeze:** `docs/workstreams/timeline-temporal-operational-b06-c-implementation-freeze.md`
- **B06-C closure:** `docs/workstreams/timeline-temporal-operational-b06-c-closure-2026-09-22.md`
- **B06-D implementation freeze:** `docs/workstreams/timeline-temporal-operational-b06-d-implementation-freeze.md`
- **B06-D closure:** `docs/workstreams/timeline-temporal-operational-b06-d-closure-2026-09-23.md`
- **B06 whole-block closure:** `docs/workstreams/timeline-temporal-operational-b06-e-closure-2026-09-23.md`
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
B05 Product Organization                         ✅ CLOSED / PROVEN
B06 Routine / Recurrence / Occurrence Baseline   ✅ CLOSED / PROVEN
B07 UI/UX Consolidation v1                       ⬜
B08 Session Runtime                              ⬜
...
B15 Whole Vertical Closure                       ⬜
```

Current candidate DB:

```text
PostgreSQL 18.6
Alembic source 20260923_57
Proven topology 145|5|88|92|285|223|408|0|0|0 (whole B06 proven)
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
Routine != Recurrence != Occurrence
Occurrence != Schedule
projection != canonical truth
```

Pre-B04 DB/API same-change governance remains binding for all later blocks.

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

The current vertical still does not pull forward:

```text
Session contiguous-duration runtime
Actual / Outcome / Confirmation
arbitrary heterogeneous relative-reference persistence
solver candidate generation
optimization/replanning search
provider/offline synchronization
multi-actor grants / complete Authority model
```

## 9. B04/B05 closure carried forward

B04 whole-block authority is `timeline-temporal-operational-b04-f-closure-2026-09-20.md`. B05 whole-block authority is `timeline-temporal-operational-b05-e-closure-2026-09-21.md`.

`Fascia` remains a B02 coarse Schedule placement, not a B04 constraint. Life Area/Tags remain actor-local product organization, not new Domain roots.

## 10. B06 closed authority

```text
B06-A Routine source core                         ✅ CLOSED / PROVEN at `_51`
B06-B Recurrence authoring                        ✅ CLOSED / PROVEN at `_54`
B06-C canonical Occurrence checkpoint             ✅ CLOSED / PROVEN at `_55`
B06-D shared Schedule / Timeline / functional UI  ✅ CLOSED / PROVEN at `_57`
B06-E whole-block closure                         ✅ CLOSED / PROVEN at `_57`
B06 whole block                                   ✅ CLOSED / PROVEN
```

B06 reuses the existing Schedule authority for materialized Occurrences. It does not create `occurrence_schedule`, rewrite provenance or convert repeated Activity into Routine. Timeline is checkpoint-before-read; `GET` remains read-only. Expected and scheduled Occurrence projections obey one-item precedence, quota/cyclic truth stays untimed unless explicitly scheduled, and source organization is inherited rather than cloned.

The local D proof discovered and closed two least-privilege defects rather than widening runtime grants: `_57` exposes unscheduled expected Occurrences through `list_self_expected_occurrences_in_window(uuid,date,date,text)`, scheduled provenance reuses `get_self_occurrence`, and Routine presentation reuses `list_self_routines`. The proven `_57` topology is `145|5|88|92|285|223|408|0|0|0`.

User-run B06-D evidence:

```text
focused Occurrence Schedule PostgreSQL test   1 PASS
backend + catalog gate                       11 PASS
web TypeScript typecheck                      PASS
focused web Vitest files                     4 PASS
focused web Vitest tests                    18 PASS
```

B06-E then reconciled the prior slice evidence and completed the final local sanity/walkthrough:

```text
generated:check                             PASS
API-client typecheck                        PASS
web typecheck                               PASS
focused B06/runtime Vitest                  6 files / 37 tests PASS
persistent local dogfood real-stack        accepted
created Timeline/Event/recurring state      survives F5
remaining B06 blocker                       none
```

Whole-block closure authority is `timeline-temporal-operational-b06-e-closure-2026-09-23.md`.

## 11. Current gate

```text
B04 ✅ CLOSED / PROVEN
B05 ✅ CLOSED / PROVEN
B06 ✅ CLOSED / PROVEN at `_57`
B07 ⬜ NOT STARTED
B08 ⬜ NOT STARTED
```

The workstream is intentionally parked at a **post-B06 sequencing decision**. The documented order still places B07 before B08, but no B07 skip/deferral is recorded here. If B07 is deliberately deferred in favor of B08, that decision must be discussed and written into the roadmap/handoff before B08 implementation starts. No CI/Actions are authorized by this handoff.
