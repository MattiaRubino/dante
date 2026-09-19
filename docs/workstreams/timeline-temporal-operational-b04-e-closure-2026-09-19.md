# Timeline / Temporal-Operational — B04-E Closure

- **Status:** ✅ CLOSED / PROVEN
- **Date:** 2026-09-19
- **Branch:** `feature/timeline-temporal-operational`
- **Slice:** B04-E Advanced-family applicability + integration hardening
- **Previous slice:** B04-D Movement Policy ✅ CLOSED / PROVEN
- **Next slice:** B04-F Whole-B04 closure
- **Candidate DB head:** `20260919_41`
- **Candidate topology:** `116|5|43|90|233|153|331|0|0|0`
- **CI:** not used; proof executed locally against real PostgreSQL

## 1. Closure decision

```text
B04-E ✅ CLOSED / PROVEN
B04-F ⬜ NEXT
```

B04-E activated only advanced Temporal Constraint semantics that are truthful against already-canonical facts. It did not pull Session, Actual, Occurrence, generic heterogeneous relation, or solver ownership forward.

## 2. Frozen applicability disposition

### TC-008 — minimum / maximum planned Schedule duration

**Implemented and proven in B04-E.**

```text
subject              self-owned Activity | Event
family               duration
constrained facet    schedule.placement
rule kind            minimum | maximum
strength             hard | soft
value                positive exact duration in microseconds
evaluable candidate  exact absolute Schedule interval
```

Permanent distinction:

```text
planned Schedule duration
!= Activity estimated effort
!= Session elapsed duration
!= Session active duration
!= Actual duration
```

### TC-009 — minimum contiguous Session duration

**Applicability gate closed; runtime deferred to B08 Session Runtime.**

Reopening trigger: canonical Session runtime/ownership exists and the constrained contiguous Session fact can be evaluated directly.

### TC-010 — spacing / recovery

**Applicability gate closed; runtime deferred to B06/B08/B10 according to the anchor.**

Reopening trigger: the required previous Occurrence / Session / Actual anchor is canonical, queryable, and owned by its proper block.

No synthetic Activity/Event `last_at` field was introduced.

### TC-011 — relative before / after

**Applicability gate closed; runtime persistence deferred.**

Reopening trigger: a reviewed bounded reference/relation contract exists for the exact heterogeneous target union and referenced temporal fact.

No `related_id + type`, opaque JSON relationship payload, or generic semantic Relationship root was invented.

## 3. Persistence authority

B04-E introduced:

```text
20260919_40 b04_schedule_duration_constraints
20260919_41 b04_duration_runtime_read_acl
```

New canonical table:

```text
dante.temporal_constraint_duration_state
```

New governed mutation capability:

```text
dante.mutate_self_schedule_duration_constraint(...)
```

Shared routines extended rather than duplicated:

```text
dante.enforce_temporal_constraint_rule_totality()
dante.assert_absolute_schedule_move_hard_admissible(...)
```

The B04-D automatic-move path therefore cannot bypass current hard duration rules.

Runtime receives only the least-privilege read needed by the canonical application read/evaluation path; history/idempotency internals remain private.

## 4. Application/evaluation authority

`TemporalConstraintApplication` remains the single canonical read/evaluation surface for boundary, window and duration rules.

Duration evaluation is deterministic and non-persistent:

```text
minimum: candidate_duration >= required_duration
maximum: candidate_duration <= required_duration
```

Hard violations make a candidate inadmissible. Soft violations remain admissible with an explanation.

Hard-set feasibility now also accounts for duration geometry. For example, a hard minimum duration longer than the available hard placement window is reported as an infeasible planning set; it is not an Outcome or claim about reality.

## 5. Observed proof

### PostgreSQL core / movement integration

```text
4 passed
B04_E_LIVE_TOPOLOGY=116|5|43|90|233|153|331|0|0|0
```

Covered:

```text
create / revise / retire
current/history monotonicity
expected-state CAS
idempotent replay
hard minimum blocks automatic move
soft maximum does not block automatic move
```

### Canonical application / regression

```text
13 passed, 3 deselected
B04_E_LIVE_TOPOLOGY=116|5|43|90|233|153|331|0|0|0
```

Covered:

```text
duration read/evaluation
soft violation explanation
hard maximum rejection
boundary + window + duration composition
hard-set infeasibility from duration/window geometry
runtime duration SELECT ACL
B04-C window evaluator regression
B04-B/A application regression
```

### Final Dictionary / catalog reconciliation

```text
3 passed
DATABASE_CURRENT_TOPOLOGY=116|5|43|90|233|153|331|0|0|0
B04_E_LIVE_TOPOLOGY=116|5|43|90|233|153|331|0|0|0
```

Proves exact parity across:

```text
Dictionary
SQLAlchemy mappings / MetaData
Alembic head 20260919_41
real PostgreSQL 18.6 catalog
runtime ACL
```

## 6. Public API disposition

B04-E did **not** widen the public Temporal HTTP contract. Duration is integrated into the canonical application layer and database truth, but no new public route/model was activated in this slice.

Therefore B04-E does not claim or require OpenAPI/client churn. Whole-B04 B04-F must still run the exact public API inventory/snapshot regression required by the B04 execution plan.

## 7. Permanent non-collapse preserved

```text
Temporal Constraint != Schedule
planned duration != estimated effort
planned duration != Session duration
planned duration != Actual duration
hard violation != impossible reality
evaluation != solver decision
violation != automatic mutation
proposal != accepted effect
constraint revision != Schedule revision
```

## 8. Closure

All B04-E owned implementation and applicability obligations are explicitly resolved.

```text
B04-A ✅ CLOSED / PROVEN
B04-B ✅ CLOSED / PROVEN
B04-C ✅ CLOSED / PROVEN
B04-D ✅ CLOSED / PROVEN
B04-E ✅ CLOSED / PROVEN
B04-F ⬜ NEXT — Whole-B04 closure
```

B04-F owns whole-block regression, public API/OpenAPI inventory verification, applicable product/manual acceptance, and final B04 documentation/closure before B05 may begin.
