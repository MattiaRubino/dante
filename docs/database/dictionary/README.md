# DANTE Database Dictionary

- **Status:** CURRENT / MATERIALIZED FOR CHECKED-OUT REPOSITORY STATE
- **Schema version:** 1
- **Serialization:** JSON
- **PostgreSQL:** 18.6
- **Protected-main Alembic head:** `20260906_18`
- **Protected-main topology:** `89|5|18|77|173|91|272|0|0|0`
- **Current candidate Alembic head on `feature/timeline-temporal-operational`:** `20260919_39`
- **Current candidate topology:** `115|5|42|89|232|152|329|0|0|0`
- **Frozen CP6 head:** `20260826_08`
- **Last reconciled:** 2026-09-19

## 1. Purpose

Machine-readable companion to the current DANTE Database System of Record.

```text
Current checked-out DB Reference
≈ Database Dictionary
≈ SQLAlchemy MetaData / mappings
≈ Alembic
≈ real PostgreSQL
≈ direct tests
```

A mismatch is a defect. Protected `main` remains integration authority; `_39` is candidate truth on the Timeline branch and is not protected-main truth before integration.

## 2. Current checked-out business-schema inventory

Authoritative counts are in `scope.json`:

```text
tables      115
views         5
routines     42
standalone  162
triggers     89
indexes      232
FKs          152
CHECKs       329
```

No enum/domain, sequence, materialized view, partitioned table or RLS policy exists in the DANTE business-schema inventory.

## 3. Post-CP6 Timeline evolution

```text
B01 / 20260908_19
  Activity intention/create capability

B02 / 20260909_20 → 20260915_26
  shared Schedule establishment/revision/unschedule/Undo
  complete accepted placement union
  DST/source-intent hardening

B03 / 20260916_27 → 20260917_29
  Event expectation/shared Schedule authorization/Agenda

B04-A / 20260918_30 → 20260918_33
  Temporal Constraint identity, rule MaterialState/current/history,
  expected-state CAS, idempotency and API activation

B04-B / 20260919_34
  absolute earliest/latest-start/latest-completion boundaries

B04-C / 20260919_35 → 20260919_36
  absolute windows + deterministic evaluation + runtime read ACL

B04-D / 20260919_37 → 20260919_39
  Schedule Movement Policy MaterialState/current/history
  governed automatic move
  confirmation proposal/acceptance
  hard Temporal Constraint enforcement
  replay hardening
```

The object tree and `scope.json`, not this prose summary, are structural source of truth.

## 4. Timeline persistence classification

### 4.1 Activity / Schedule / Event

Existing B01–B03 ownership remains unchanged. `dante.schedule` remains the single shared accepted-placement owner.

### 4.2 Temporal Constraint — B04-A/B/C ✅ CLOSED / PROVEN

Temporal Constraint is a stable `ScopedRecordRef` LR-05 dependent. Boundary and window rule MaterialStates remain independently revisable from Schedule.

Accepted absolute boundary variants:

```text
earliest_start     + schedule.start
latest_start       + schedule.start
latest_completion  + schedule.completion
```

Accepted absolute window variants:

```text
start_within              + schedule.start
completion_within         + schedule.completion
full_placement_contained  + schedule.placement
placement_overlaps        + schedule.placement
```

### 4.3 Movement Policy — B04-D ✅ CLOSED / PROVEN

Movement Policy is a typed Schedule-owned material facet:

```text
schedule.movement_policy
```

Canonical object family:

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

The policy value space is deliberately decomposed rather than copied from prototype UI enum:

```text
automatic_movement_code  blocked | automatic
acceptance_path_code     direct | confirmation_required
```

`material_state_address` now admits `schedule.movement_policy`, and `enforce_material_state_totality()` enforces exact Movement Policy owner/facet/payload exclusivity alongside the previously materialized families.

Movement Policy revision has its own immutable MaterialState/current-history chronology and does not revise Schedule placement.

A confirmation proposal is retained separately from accepted placement truth. Acceptance rechecks current placement, current policy basis and hard Temporal Constraint admissibility before committing a new Schedule placement MaterialState.

## 5. Permanent non-collapse

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
soft preference violation != automatic rejection
evaluation != solver decision
violation != automatic mutation
current accepted state != newest row
idempotency key != Domain identity
```

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

Observed B04-D evidence:

```text
Movement Policy / governed move / ACL tests       7 PASS
whole catalog + B04-D catalog reconciliation      3 PASS
DATABASE_CURRENT_TOPOLOGY                         115|5|42|89|232|152|329|0|0|0
```

## 7. Object contract

Every standalone business-schema object records semantic traceability, implementation provenance, exact structure, lifecycle/currentness semantics, ACL and proof obligations. Embedded indexes/FKs/CHECKs/triggers remain attached to their owning tables; routines remain standalone because signature/security/search-path/ACL are independently governed.

Shared CP6 entries retain original introducing provenance even when later slices extend bounded dispatchers. Later semantics/proof are updated without falsifying historical provenance.

## 8. Validation

Required validation remains:

```text
JSON Schema consistency
filename/object-key agreement
FK/trigger target resolution
scope counts ↔ object tree
Dictionary ↔ SQLAlchemy ↔ Alembic ↔ PostgreSQL
owner/ACL parity
routine search_path/security parity
extension-owned objects excluded correctly
```

## 9. Same-change rule

No real object → no ceremonial Dictionary entry. Every real current DANTE business object requires matching Dictionary/Alembic/SQLAlchemy/current-human-reference/direct-PostgreSQL proof in the same reviewed slice.

B04-E is the next candidate slice; B04-F remains required before B05.
