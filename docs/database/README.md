# DANTE Database System of Record

- **Status:** CURRENT / AUTHORITATIVE DATABASE REFERENCE
- **Last reconciled:** 2026-09-21
- **PostgreSQL:** 18.6
- **Protected-main Alembic head:** `20260906_18`
- **Protected-main topology:** `89|5|18|77|173|91|272|0|0|0`
- **Timeline candidate branch:** `feature/timeline-temporal-operational`
- **Timeline candidate Alembic head (source):** `20260921_51`
- **Timeline candidate expected topology:** `135|5|68|90|263|201|381|0|0|0` (B06-A candidate; pending direct proof)
- **Timeline candidate DB overlay:** `timeline-temporal-operational.md`
- **Persistence doctrine:** `../development/backend-cp6-02-postgresql-persistence-constitution.md`
- **Persistence ADR:** `../decisions/ADR-010-postgresql-persistence-constitution.md`
- **Timeline workstream authority:** `../workstreams/timeline-temporal-operational-map.md`
- **B04-E closure:** `../workstreams/timeline-temporal-operational-b04-e-closure-2026-09-19.md`

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
20260919_39 B04-D proposal-accept replay fix
    ↓
20260919_40 B04-E planned Schedule duration constraints
    ↓
20260919_41 B04-E duration runtime-read ACL
    ↓
20260920_42 B04-F Schedule hard-constraint guard
    ↓
20260920_43 B05-A Life Area initial create/list schema
    ↓
20260920_44 B05-A full actor-local Life Area lifecycle
    ↓
20260920_45 B05-A validated receipt CHECK name reconciliation [direct catalog proof PASSED]
    ↓
20260920_46 B05-B typed primary Life Area assignment [16 direct PostgreSQL tests PASSED]
    ↓
20260920_47 B05-C secondary actor-local Tags and typed Activity/Event edges [26 direct PostgreSQL tests PASSED]
20260921_48 B05-D postponed Event discovery/replan capability [24 PostgreSQL/API/catalog + 41 selected web tests PASSED]
20260921_49 B06-A Routine source core, lifecycle and typed product organization [candidate superseded by _50]
20260921_50 B06-A atomic initial Routine/Recurrence companion correction [pending direct proof]
20260921_51 B06-A qualified Routine source/Life Area command repair [pending direct proof]
```

No accepted historical migration was edited, rebased, renumbered or flattened.

## 3. Current candidate topology

```text
135 tables
5 views
68 routines
90 triggers
263 physical indexes
201 foreign keys
381 CHECK constraints
0 enums/domains
0 sequences
0 materialized views
0 partitioned tables
0 RLS policies
```

The `_42` topology was read directly from PostgreSQL 18.6 during B04-F closure. `_45` closed B05-A. The user ran 16 selected PostgreSQL tests at `_46`, including whole-catalog reconciliation, closing B05-B. The user ran 26 selected PostgreSQL tests at `_47`, including whole-catalog reconciliation, closing B05-C. The topology is an expected value asserted by the passing catalog test, not a separate manual PostgreSQL inventory.

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

```text
facet                  schedule.movement_policy
automatic_movement     blocked | automatic
acceptance_path        direct | confirmation_required
owner                  accepted Schedule
scope                  self-Person Activity/Event schedules
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

Every automatic commit/accept path checks current placement CAS, current Movement Policy basis and current hard Temporal Constraint admissibility before accepted Schedule mutation.

`proposal != accepted effect` remains structural truth.

### B04-E Advanced-family applicability ✅ CLOSED / PROVEN

B04-E activates only **TC-008 planned Schedule duration** and explicitly closes applicability for the remaining advanced families without inventing later-owned truth.

Canonical duration rule:

```text
subject              Activity | Event
family               duration
constrained facet    schedule.placement
kind                  minimum | maximum
strength              hard | soft
value                 positive exact microseconds
first evaluable form exact absolute Schedule interval
```

New canonical object/capability:

```text
temporal_constraint_duration_state
mutate_self_schedule_duration_constraint(...)
```

Existing shared integrity/evaluation seams are extended rather than duplicated:

```text
enforce_temporal_constraint_rule_totality()
assert_absolute_schedule_move_hard_admissible(...)
TemporalConstraintApplication
```

Therefore hard duration rules participate in both canonical evaluation and B04-D automatic-move enforcement.

Permanent distinction:

```text
planned Schedule duration
!= Activity estimated effort
!= Session elapsed/active duration
!= Actual duration
```

Applicability dispositions:

```text
TC-009 contiguous Session duration  → runtime deferred B08
TC-010 spacing/recovery             → deferred B06/B08/B10 by anchor
TC-011 relative before/after        → deferred until reviewed bounded reference/relation persistence exists
```

No fake Activity/Event `last_at`, no generic `related_id + type`, and no generic JSON rule payload were introduced.

B04-E exposed no new public Temporal HTTP endpoint, so OpenAPI/client artifacts did not churn in that slice. B04-F subsequently closed the whole-block public API inventory/snapshot regression.

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
planned duration != estimated effort
planned duration != Session duration
planned duration != Actual duration
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

B12 still owns broad candidate generation / optimization / solver semantics.

## 6. Proof state

```text
B01 Activity Core                    CLOSED / PROVEN
B02 Schedule Core                    CLOSED / PROVEN
B03 Event Core                       CLOSED / PROVEN
B04-A                                CLOSED / PROVEN at 20260918_33
B04-B                                CLOSED / PROVEN at 20260919_34
B04-C                                CLOSED / PROVEN at 20260919_36
B04-D Movement Policy                CLOSED / PROVEN at 20260919_39
B04-E Advanced-family applicability  CLOSED / PROVEN at 20260919_41
B04-F Whole-B04 closure              CLOSED / PROVEN at 20260920_42
B04 overall                          CLOSED / PROVEN
B05-A Life Area full lifecycle        CLOSED / PROVEN at `_45`
B05-B primary assignment             CLOSED / PROVEN at `_46` (16 selected tests)
B05-C secondary Tags                 CLOSED / PROVEN at `_47` (26 selected tests)
```

Observed B04-E local evidence:

```text
core duration + movement integration             4 PASS
application/evaluator/regression                13 PASS / 3 deselected
whole catalog + B04-E catalog/ACL                3 PASS
DATABASE_CURRENT_TOPOLOGY                        116|5|44|90|233|153|331|0|0|0
```

Proof covers duration lifecycle/current/history/CAS/idempotency, hard minimum/maximum behavior, soft violation explanation, boundary/window/duration composition, duration/window infeasibility, automatic-move enforcement, runtime least-privilege ACL and exact Dictionary/SQLAlchemy/Alembic/PostgreSQL parity.

## 7. Current next boundary

B04-F and B05 are closed with their recorded proof. `_46` keeps explicit legacy-unassigned Activity/Event items and revokes runtime access to bare create helpers. `_47` adds a distinct Tag catalog and independent many-valued typed Activity/Event edges, with immutable acceptance receipts and bounded runtime functions. `_48` adds a bounded Event-only postponed discovery/replan capability without fabricating placement truth. The user's B05-D gate passed 24 PostgreSQL/API/catalog tests and 41 selected web tests; the B05-E real-stack walkthrough is complete. B04 Schedule truth is unchanged.
