# B13-C Execution Structure — implementation checkpoint

- **Status:** LOCAL CANDIDATE / PostgreSQL and catalog proof pending
- **Date:** 2026-09-29
- **Branch:** `feature/timeline-temporal-operational`
- **Base:** `d0ee3a43c0a1d8d066db02a4a0e2fce1b2a49134` (approved scope)
- **Forward revision:** `20260929_91`, after `_90`
- **CI:** not authorized; the user runs PostgreSQL gates locally

## Discovery and chosen basis

B13-A's `plan_intention`, `plan_step`, `plan_work_state`, `plan_step_in_state`, `plan_current_work_state`, `plan_work_current_history` and `plan_work_operation` already supply self ownership, immutable revision snapshots, expected-current protection and replay. B13-B adds a guard that prevents removal or relinking of an active Dependency endpoint. The `_91` revision extends **only the Step row in the immutable Plan snapshot** with a nullable policy tuple, and patches the guarded B13-A read/replace functions forward. Its values are Plan-contextual and never silently change the Activity used by another Plan. On relink, the UI clears the policy; the server rejects a policy on an unlinked Step. The B13-B endpoint guard remains in the patched function.

An accepted `Schedule` is one current placement of an Activity, possibly one of several. It has no Plan Step attribution and is not necessarily a planned Session. A performed `Session` is a distinct fact. Consequently, B13-C counts **only the explicitly supplied list of proposed planning slices** in one read-only assessment request, tied to a current Plan state and linked Step. No candidate list yields `unknown`; no accepted Schedule or recorded Session is counted. A changed Plan state yields conflict. The assessment creates no accepted Schedule, Session, Actual or Proposal.

The policy tuple is `divisible`, optional positive `max_planned_slices` (at most 100, matching the bounded candidate request), `merge_compatible`, and `execution_strength_code` (`hard`/`soft`). The all-null tuple means no policy. An indivisible Step requires maximum one and disallows merge; a divisible Step with a bound requires at least two. The database CHECK and guarded replacement both reject contradictions. A violation of a hard count is diagnostic here; future proposal admission belongs to B12. Actual Session capture remains independent.

Two distinct proposed slices may be assessed for union only when the policy explicitly allows it and the absolute intervals are contiguous. The existing Activity Temporal Constraint evaluator assesses each proposed placement and their combined interval; hard violation makes the union incompatible, a rule that cannot be evaluated makes it unknown, and soft violations are returned with each rule's strength, facet, evaluation and reason code. “Compatible” is bounded to this policy, contiguity and currently evaluable Activity temporal rules. It does not correct recorded Sessions, persist a merged placement or assert availability of spacing/preparation/recovery rules.

## Capability ledger

| Capability | B13-C state | Exact owner/basis |
|---|---|---|
| Divisibility and maximum intended count | Implemented candidate; PostgreSQL proof pending | Plan Step revision; explicit proposed slices only; hard/soft diagnostic |
| Proposed slice compatibility | Implemented candidate; PostgreSQL proof pending | Same linked Activity, explicit pair, merge permission, contiguity and Temporal Constraint evaluation of the union |
| Schedule duration | Truthful handoff to existing Temporal Constraint | Activity `schedule.placement`, minimum/maximum, hard/soft; evaluated on each proposed interval and merged interval |
| Session minimum active duration | Existing Temporal Constraint/Session owner | Actual `session.active_duration`; not a planning placement rule |
| Spacing between slices | Unsupported and not editable | No canonical typed Temporal Constraint author/evaluator for this pair |
| Preparation and recovery | Unsupported and not editable | No canonical typed Temporal Constraint author/evaluator for these intervals |
| Accepted Schedule count as planned Session count | Unsupported | No Step attribution or Session intent on current Schedule placements |
| Recorded Session merge/correction | Outside B13-C | Existing Session correction/lineage semantics |

## Protected path and proof

The runtime has no direct DML on `plan_step_in_state`. `_91` adds four nullable columns and one CHECK, then patches `get_self_plan_work` and `replace_self_plan_work` in place with exact anchors. Existing Plan replacement serializes on `plan_intention`, verifies self ownership, exact current revision, linked Activity ownership and B13-B active endpoints, then writes an immutable revision/history/operation receipt. The read-only evaluation endpoint uses the self Plan read and existing Temporal Constraint application. OpenAPI and Orval artifacts are generator output, not hand edits.

Predicted Dictionary/catalog tuple at `_91`: `196|5|152|100|397|344|497|0|0|0` (one CHECK added). This is **not a live PostgreSQL measurement**. Focused local results in the coding workspace: `ruff` PASS, backend unit assessment **1 passed**, web focused **8 passed**, API-client and web typechecks PASS, OpenAPI/Orval generation PASS. No Docker/PostgreSQL runtime exists in this workspace; the user-run migration, B13-A/B/C and exact catalog tests remain the gate for proof and closure.

Suggested user-run focused command after publication:

```bash
cd ~/projects/dante/apps/backend
uv run --locked pytest -q --no-cov --tb=short -m postgres \
  tests/integration/temporal/test_b13_c_execution_structure.py \
  tests/integration/temporal/test_b13_a_plan_work.py \
  tests/integration/temporal/test_b13_b_plan_dependency.py \
  tests/integration/database/test_current_catalog.py \
  tests/integration/database/test_database_current_catalog.py \
  tests/integration/database/test_b11_catalog_reconciliation_probe.py
```

B13-C remains a candidate until this gate passes and the results are recorded. B13-D remains the integrated real-app proof; B12 remains held.
