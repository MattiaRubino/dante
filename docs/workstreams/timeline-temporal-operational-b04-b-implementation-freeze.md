# Timeline / Temporal-Operational — B04-B Absolute Boundary / Deadline Implementation Freeze

- **Status:** FROZEN FOR IMPLEMENTATION
- **Date:** 2026-09-19
- **Branch:** `feature/timeline-temporal-operational`
- **Parent slice:** B04-A Temporal Constraint canonical core ✅ CLOSED / PROVEN
- **Entering candidate head:** Alembic `20260918_33`
- **Entering candidate topology:** `107|5|33|85|212|129|309|0|0|0`
- **Domain authority:** `docs/domain/concepts/temporal-constraint.md` + canonical continuation
- **Logical authority:** `docs/logical-model/slices/time-reality-v1.md`
- **B04 execution authority:** `timeline-temporal-operational-b04-execution-plan.md`
- **CI:** not implicitly authorized

## 1. Goal

B04-B activates the complete **absolute boundary** subset needed for earliest-start, latest-start and latest-completion/deadline while preserving the B04-A identity/current/history/CAS/idempotency machinery.

A Deadline remains a latest-bound Temporal Constraint over an explicit temporal facet. It is not a universal `due_at` field and does not establish Outcome truth merely because time passes.

## 2. Frozen canonical matrix

Supported subjects remain:

```text
Activity | Event
```

Supported rule family:

```text
family          boundary
strength        hard | soft
temporal form   absolute
boundary value  finite timestamptz
```

Only these kind/facet pairs are admitted:

```text
earliest_start     + schedule.start       ✅
latest_start       + schedule.start       ✅
latest_completion  + schedule.completion  ✅
```

Every other boundary-kind / constrained-facet pairing fails closed.

## 3. Binding semantics

```text
earliest_start
schedule.start >= boundary

latest_start
schedule.start <= boundary

latest_completion / deadline
schedule.completion <= boundary
```

Permanent non-collapse:

```text
Temporal Constraint != Schedule
Deadline != Schedule end
Deadline != target date by default
Passing deadline != missed
Passing deadline != failure
Passing deadline != Outcome
constraint revision != Schedule revision
hard planning rule != impossible reality
```

B04-B does not infer Actual completion and does not evaluate whether an Activity/Event actually happened.

## 4. Persistence strategy

Reuse the B04-A canonical owner/state/history family:

```text
temporal_constraint
temporal_constraint_state
temporal_constraint_boundary_state
temporal_constraint_boundary_absolute_state
temporal_constraint_current_history
temporal_constraint_mutation_operation
```

B04-B adds **no new table** for latest-start/deadline. The absolute payload table remains the one absolute boundary value representation.

Forward migration `_34` must:

1. widen `constrained_facet_code` only to `schedule.start | schedule.completion`;
2. widen `boundary_kind_code` only to `earliest_start | latest_start | latest_completion`;
3. harden deferred rule totality so only the frozen kind/facet matrix is accepted;
4. add one governed `mutate_self_absolute_boundary_constraint(...)` routine;
5. retain `mutate_self_absolute_earliest_start_constraint(...)` as the B04-A compatibility capability;
6. preserve runtime direct-DML denial and grant runtime only governed mutation execution/read access already required by the API.

No historical migration is rewritten.

## 5. Application/API strategy

The existing five public Temporal Constraint operations stay stable:

```text
temporal_create_constraint
temporal_get_constraint
temporal_list_constraints_by_subject
temporal_revise_constraint_rule
temporal_retire_constraint
```

No new endpoint is required for B04-B. Request/response `rule` becomes a typed absolute-boundary union preserving explicit `boundary_kind` and `constrained_facet`.

The exact pre-B04 13 operationIds remain frozen; the five B04-A operationIds remain stable.

Any OpenAPI schema change must be reconciled through the canonical generator and committed generated client.

## 6. Fail-closed temporal forms

B04-B does **not** convert or approximate:

```text
date-only
floating-local
named-zone-local
coarse-local-period
```

No conversion such as date-only → midnight UTC or floating-local → device-zone instant is allowed.

## 7. Explicitly out of scope

```text
earliest_completion
windows / preferred windows / forbidden windows      → B04-C
evaluation / explanation / infeasibility             → B04-C
Movement Policy                                       → B04-D
duration / spacing / relative constraints             → B04-E
solver / automatic replanning                          → B12
Actual / Outcome / completion inference                → B10
generic due_at
generic Rule(type,json)
frontend UX
B05+
CI
```

## 8. Required proof before closure

- fresh migration reaches `_34`;
- old B04-A earliest-start behavior remains green;
- latest-start create/revise/read/history/replay works;
- latest-completion/deadline create/revise/read/history/replay works;
- invalid kind/facet pairs are rejected by deferred DB integrity, not only by API validation;
- Activity/Event ownership and self-scope remain unchanged;
- CAS and operation-id changed-intent collision remain intact;
- SQLAlchemy, Dictionary, real catalog, owner/ACL and DB references reconcile to `_34`;
- the same five API operations expose the typed union with unchanged operationIds;
- OpenAPI snapshot / Orval client / generated determinism are green;
- B04-B closure docs identify B04-C as next.
