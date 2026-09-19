# DANTE Database System of Record

- **Status:** CURRENT / AUTHORITATIVE DATABASE REFERENCE
- **Last reconciled:** 2026-09-19
- **PostgreSQL:** 18.6
- **Protected-main Alembic head:** `20260906_18`
- **Protected-main topology:** `89|5|18|77|173|91|272|0|0|0`
- **Timeline candidate branch:** `feature/timeline-temporal-operational`
- **Timeline candidate Alembic head:** `20260919_39`
- **Timeline candidate topology:** `115|5|42|89|232|152|329|0|0|0`
- **Timeline candidate DB overlay:** `timeline-temporal-operational.md`
- **Persistence doctrine:** `../development/backend-cp6-02-postgresql-persistence-constitution.md`
- **Persistence ADR:** `../decisions/ADR-010-postgresql-persistence-constitution.md`
- **Timeline workstream authority:** `../workstreams/timeline-temporal-operational-map.md`
- **B04-D closure:** `../workstreams/timeline-temporal-operational-b04-d-closure-2026-09-19.md`

## 1. Authority model

```text
Product / Domain / Logical / Physical
→ PostgreSQL Persistence Constitution / ADR-010
→ current human DB reference + Dictionary semantic contract
→ Alembic forward evolution
→ SQLAlchemy mappings / MetaData
→ real PostgreSQL catalog
→ direct tests
```

Permanent invariant:

```text
CURRENT DB REFERENCE
≈ DATABASE DICTIONARY
≈ SQLALCHEMY
≈ ALEMBIC
≈ REAL POSTGRESQL
≈ DIRECT TESTS
```

Protected `main` remains integration authority. Candidate truth is never relabeled as protected-main truth before merge/readback.

## 2. Current Timeline migration graph

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
20260919_37 B04-D Schedule Movement Policy core
    ↓
20260919_38 B04-D governed Schedule move + confirmation proposal/acceptance
    ↓
20260919_39 B04-D proposal-accept replay fix [current candidate head]
```

No accepted historical migration was edited, rebased, renumbered or flattened.

## 3. Current candidate topology

```text
115 tables
5 views
42 routines
89 triggers
232 physical indexes
152 foreign keys
329 CHECK constraints
0 enums/domains
0 sequences
0 materialized views
0 partitioned tables
0 RLS policies
```

This topology was read directly from PostgreSQL 18.6 at `_39` and reconciled with `dictionary/scope.json`, SQLAlchemy mappings, Alembic and whole-catalog tests.

## 4. Timeline persistence classification

### B01 Activity

`dante.activity` remains the CP6 Activity NativeRef owner. B01 adds only the typed intention/create control surface.

### B02 Schedule

`dante.schedule` remains the single shared Schedule owner. Accepted placement truth is MaterialState/current/history and remains distinct from policy, constraint and reality.

### B03 Event

`dante.event` remains a distinct NativeRef owner while reusing shared Schedule authority. Agenda values remain Event-internal ordered content.

### B04-A/B/C Temporal Constraint ✅ CLOSED / PROVEN

Temporal Constraint is a stable `ScopedRecordRef` LR-05 dependent, not a NativeRef root and not Schedule placement.

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

Rules retain independent immutable MaterialState/current/history and expected-state CAS. Hard/soft evaluation is derived; evaluation is not solver output and does not mutate Schedule.

### B04-D Movement Policy ✅ CLOSED / PROVEN

Movement Policy is a typed Schedule-owned rule facet, not a new generic entity and not a Temporal Constraint.

Canonical policy state:

```text
facet                  schedule.movement_policy
automatic_movement     blocked | automatic
acceptance_path        direct | confirmation_required
owner                  accepted Schedule
scope                  self-Person Activity/Event schedules
```

Persistence/control:

```text
schedule_movement_policy_state
schedule_movement_policy_current_history
schedule_movement_policy_mutation_operation
schedule_move_proposal
schedule_move_request_operation
schedule_move_accept_operation

enforce_schedule_movement_policy_history()
mutate_self_schedule_movement_policy(...)
resolve_self_schedule_movement_policy(...)
assert_absolute_schedule_move_hard_admissible(...)
apply_governed_absolute_schedule_move(...)
request_self_absolute_schedule_move(...)
accept_self_absolute_schedule_move_proposal(...)
```

B04-D preserves the following operational distinction:

```text
blocked
  → automatic movement rejected

automatic + direct
  → admissible absolute candidate may commit immediately

automatic + confirmation_required
  → request creates proposal only
  → accepted Schedule changes only after explicit proposal acceptance
```

Every automatic commit/accept path re-checks current placement CAS, current Movement Policy basis and hard Temporal Constraint admissibility before accepted Schedule mutation.

`proposal != accepted effect` remains structural truth: `schedule_move_proposal` does not create a new current placement MaterialState by itself.

Soft Temporal Constraint violations do not block an otherwise authorized automatic move. Hard violations or non-evaluable hard rules fail closed.

B04-D exposes no new public Temporal HTTP endpoint, so OpenAPI/client artifacts intentionally do not churn in this slice.

## 5. Permanent non-collapse invariants

```text
Activity != Event
Event != Schedule
Schedule != Temporal Constraint
Schedule != Movement Policy
Temporal Constraint != Movement Policy
Movement Policy != Authority itself
Movement Policy != solver result
proposal != accepted effect
policy revision != Schedule revision
constraint revision != Schedule revision
hard planning violation != impossible reality
window != placement
preference != accepted Schedule
evaluation != solver decision
violation != automatic mutation
Schedule != Session != Actual
Actual != Outcome
current accepted state != newest row
idempotency key != Domain identity
```

B12 still owns broad candidate generation / optimization / solver semantics. B04-D only governs whether a supplied candidate may alter accepted Schedule truth.

## 6. Proof state

```text
B01 Activity Core                    CLOSED / PROVEN
B02 Schedule Core                    CLOSED / PROVEN
B03 Event Core                       CLOSED / PROVEN
B04-A                                CLOSED / PROVEN at 20260918_33
B04-B                                CLOSED / PROVEN at 20260919_34
B04-C                                CLOSED / PROVEN at 20260919_36
B04-D Movement Policy                CLOSED / PROVEN at 20260919_39
B04 overall                          IN PROGRESS
```

Observed B04-D local evidence:

```text
Movement Policy + governed move + ACL proof       7 PASS
whole catalog + B04-D catalog/ACL reconciliation  3 PASS
DATABASE_CURRENT_TOPOLOGY                         115|5|42|89|232|152|329|0|0|0
```

Proof covers blocked automation, direct admissible move, confirmation proposal/accept, stale placement/policy state, idempotent replay, hard rejection, soft non-blocking behavior, history monotonicity, runtime capability ACL and exact Dictionary/SQLAlchemy/Alembic/PostgreSQL parity.

## 7. Current next boundary

B04-D is closed. Next is **B04-E Advanced-family applicability**. Duration/spacing/relative families must activate only where current canonical owners/anchors permit truthful semantics; Session/Actual/Occurrence/Solver-dependent behavior remains deferred to its owning block.

B04-F whole-B04 closure remains required before B05 begins.
