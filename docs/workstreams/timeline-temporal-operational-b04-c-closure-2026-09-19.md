# Timeline / Temporal-Operational — B04-C Closure Evidence

- **Status:** ✅ CLOSED / PROVEN
- **Date:** 2026-09-19
- **Branch:** `feature/timeline-temporal-operational`
- **Scope:** B04-C Windows / Preferences / Evaluation
- **Implementation freeze:** `timeline-temporal-operational-b04-c-implementation-freeze.md`
- **Previous closure:** `timeline-temporal-operational-b04-b-closure-2026-09-19.md`
- **Generated contract commit:** `5268d9dd239ab344337cadd1dfdf312dd46ffe42`
- **Alembic authority:** `20260919_36`
- **Accepted topology:** `109|5|35|87|214|131|312|0|0|0`
- **CI:** not launched; local proof only, per workstream operating rule

## 1. Closure decision

B04-C is CLOSED / PROVEN for the approved absolute-window and deterministic-evaluation slice.

This closure does not open or pre-authorize B04-D Movement Policy, B04-E advanced-family applicability, B04-F whole-B04 closure or B05+ work.

## 2. Canonical semantics proven

B04-C extends Temporal Constraint without collapsing it into Schedule placement, solver output or reality state.

Permanent non-collapse remains:

```text
TemporalConstraint != Schedule
window != placement
preference != accepted Schedule
evaluation != solver decision
violation != automatic mutation
violation != Actual
violation != Outcome / failure
INFEASIBLE != reality state
```

Activated subject and shared rule limits:

```text
subject        self-owned Activity | Event
family         window
strength       hard | soft
temporal form  absolute
range          finite starts_at < ends_at
```

Activated window relation matrix:

```text
start_within              + schedule.start       ✅
completion_within         + schedule.completion  ✅
full_placement_contained  + schedule.placement   ✅
placement_overlaps        + schedule.placement   ✅
```

Frozen relation semantics:

```text
start_within:
  window.start <= schedule.start <= window.end

completion_within:
  window.start <= schedule.completion <= window.end

full_placement_contained:
  schedule.start >= window.start
  AND schedule.completion <= window.end

placement_overlaps:
  schedule.start < window.end
  AND schedule.completion > window.start
```

Endpoint-only touching is not positive overlap.

## 3. Persistence authority

Forward migration chain added by B04-C:

```text
20260919_35 b04_absolute_window_constraints
20260919_36 b04_window_runtime_read_acl
```

B04-C adds the typed window payload surface:

```text
temporal_constraint_window_state
temporal_constraint_window_absolute_state
mutate_self_absolute_window_constraint(...)
```

The existing `temporal_constraint_state` family/facet envelope is widened only to the admitted B04-C algebra. Deferred totality rejects invalid family/payload or relation/facet combinations.

Runtime read ACL is granted only to the current-rule window tables required by the canonical application read model. History/receipt surfaces remain private except through governed capabilities.

Accepted live PostgreSQL topology:

```text
109 tables
5 views
35 routines
87 triggers
214 physical indexes
131 foreign keys
312 CHECK constraints
0 enums/domains
0 sequences
0 materialized views
0 partitioned tables
0 RLS policies
```

Compact topology:

```text
109|5|35|87|214|131|312|0|0|0
```

## 4. Current / history / CAS / idempotency

B04-C preserves the B04-A/B state model:

```text
TemporalConstraint ScopedRecordRef identity remains stable
rule revisions append MaterialState
accepted current rule is explicit
current-history is retained
expected-state CAS protects revise/retire
operation receipt enforces idempotency
retire removes current rule without deleting identity/history
```

Revision may move between admitted typed boundary/window families through a new MaterialState without changing `constraint_ref` identity.

## 5. Derived evaluation authority

B04-C adds deterministic backend evaluation of a candidate absolute interval against current effective Temporal Constraints for the subject.

Per-rule result:

```text
satisfied
violated
not_evaluable
```

Overall result:

```text
admissible
admissible_with_soft_violations
inadmissible
not_evaluable
```

Hard-set status:

```text
feasible
infeasible
undetermined
```

Evaluation is derived and non-persistent. No `violated`, `overdue`, `infeasible` or similar reality state is stored as canonical domain truth.

B04-C evaluation composes the already-accepted absolute boundary rules from B04-A/B with the new absolute windows. It performs no candidate search, optimization, automatic movement or solver-owned replanning.

## 6. Public API / generated contract

Existing Temporal Constraint CRUD operationIds remain stable.

B04-C adds exactly one public operation:

```text
POST /api/v1/temporal/constraints/evaluate
temporal_evaluate_constraints
```

The create/revise/read rule contract is extended as a typed discriminated union for the four admitted window variants. Unsupported temporal forms remain fail-closed and are not silently converted to absolute instants.

Generated OpenAPI / Orval client authority:

```text
5268d9dd239ab344337cadd1dfdf312dd46ffe42
feat(temporal): generate B04-C window evaluation client
```

## 7. Observed local proof

### PostgreSQL / application / ACL

```text
B04-C runtime ACL + window core + evaluation + boundary regression
9 PASS / 2 deselected
```

The runtime-read hardening was proven after `_36`.

### Current catalog / Dictionary / topology

```text
B04_C_LIVE_TOPOLOGY=109|5|35|87|214|131|312|0|0|0
B04_LIVE_TOPOLOGY=109|5|35|87|214|131|312|0|0|0
DATABASE_CURRENT_TOPOLOGY=109|5|35|87|214|131|312|0|0|0
12 PASS
```

### API / OpenAPI

```text
24 PASS
```

This includes OpenAPI export parity, exact Temporal inventory and boundary/window API contract coverage after the B04-C union change.

### Generated client

```text
@dante/api-client typecheck  PASS
@dante/api-client Vitest     11 PASS
generated:check              PASS / 177 deterministic files
```

## 8. Out of scope retained

B04-C does not claim support for:

```text
date-span window constraints
floating-local window constraints
named-zone-local window constraints
coarse-local-period window constraints
persisted evaluation/violation state
automatic movement
Movement Policy
advanced duration / spacing / relative families
solver / candidate search / optimization
Actual / Outcome inference
full product constraint-management UX
```

Those remain owned by later approved blocks.

## 9. Documentation / DB reconciliation decision

Closure requires all current representations to agree on:

```text
Alembic head      20260919_36
Topology          109|5|35|87|214|131|312|0|0|0
B04-A             CLOSED / PROVEN
B04-B             CLOSED / PROVEN
B04-C             CLOSED / PROVEN
Next gate         B04-D PRE-SCOPE only
```

The workstream roadmap, live map, handoff, DB System of Record, Timeline candidate overlay and Dictionary README are reconciled with this closure in the same documentation commit.

## 10. Next gate

```text
B04-D Movement Policy  ⬜ NEXT
```

B04-D requires a fresh semantic/implementation freeze before any write. B04-C closure does not authorize B04-D persistence, enum shape, mutation path, API, frontend behavior or solver coupling.
