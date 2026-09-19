# DANTE Database Dictionary

- **Status:** CURRENT / MATERIALIZED FOR CHECKED-OUT REPOSITORY STATE
- **Schema version:** 1
- **Serialization:** JSON
- **PostgreSQL:** 18.6
- **Protected-main Alembic head:** `20260906_18`
- **Protected-main topology:** `89|5|18|77|173|91|272|0|0|0`
- **Current candidate Alembic head on `feature/timeline-temporal-operational`:** `20260919_36`
- **Current candidate topology:** `109|5|35|87|214|131|312|0|0|0`
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

A mismatch is a defect. Protected `main` remains integration authority; `_36` is candidate truth on the Timeline branch and must not be relabeled as protected-main truth before integration.

## 2. Current checked-out business-schema inventory

The authoritative machine-readable counts are in `scope.json` and currently equal:

```text
tables      109
views         5
routines     35
standalone  149
triggers     87
indexes      214
FKs          131
CHECKs       312
```

No enum/domain, sequence, materialized view, partitioned table or RLS policy exists in the DANTE business-schema inventory.

These counts are live PostgreSQL-backed candidate truth through `_36`. B04-C adds two typed window tables, one governed mutation routine, two deferred totality triggers, their indexes/FKs/CHECKs, and runtime read ACL hardening without adding a new business-schema object in `_36`.

## 3. Frozen CP6 baseline vs current materialization

Frozen CP6 baseline remains historical evidence:

```text
68 tables / 5 views / 14 routines / 87 standalone
75 triggers / 95 indexes / 68 FKs / 120 CHECKs
```

Current candidate materialization is:

```text
109 tables / 5 views / 35 routines / 149 standalone
87 triggers / 214 indexes / 131 FKs / 312 CHECKs
```

`completed_stages` in `scope.json` remains CP6 provenance only. Post-CP6 provenance belongs on the actual object entries; B04 does not rewrite CP6 history.

## 4. Post-CP6 Timeline evolution

```text
B01 / 20260908_19
  activity_intention
  activity_create_operation
  create_self_activity(...)

B02 / 20260909_20 → 20260915_26
  shared Schedule establishment/revision/unschedule/Undo
  complete accepted placement union
  DST/source-intent hardening

B03-A / 20260916_27
  event_expectation
  event_create_operation
  create_self_event(...)

B03-B / 20260917_28
  shared Schedule authorization/capability generalized to Event

B03-D / 20260917_29
  event_agenda_part
  event_agenda_current
  event_agenda_mutation_operation
  create_self_event_with_agenda(...)
  replace_self_event_agenda(...)

B04-A / 20260918_30 → 20260918_33
  temporal_constraint
  temporal_constraint_state
  temporal_constraint_boundary_state
  temporal_constraint_boundary_absolute_state
  temporal_constraint_current_history
  temporal_constraint_mutation_operation
  enforce_temporal_constraint_rule_totality()
  mutate_self_absolute_earliest_start_constraint(...)
  MaterialState / history / replay / runtime-read hardening

B04-B / 20260919_34
  earliest_start + schedule.start
  latest_start + schedule.start
  latest_completion + schedule.completion
  exact deferred kind↔facet totality
  mutate_self_absolute_boundary_constraint(...)

B04-C / 20260919_35 → 20260919_36
  temporal_constraint_window_state
  temporal_constraint_window_absolute_state
  start_within + schedule.start
  completion_within + schedule.completion
  full_placement_contained + schedule.placement
  placement_overlaps + schedule.placement
  exact deferred relation↔facet totality
  mutate_self_absolute_window_constraint(...)
  narrow dante_runtime current-window SELECT ACL
```

The final object tree and `scope.json` counts, not this prose summary, are the structural source of truth.

## 5. Timeline persistence classification

### 5.1 Activity

`dante.activity` remains the CP6 Activity NativeRef owner. B01 adds only the typed dependent descriptor, create receipt and bounded create capability.

### 5.2 Schedule

`dante.schedule` remains the single shared CP6 Schedule owner. B02 reuses the CP6 placement MaterialState/current/history machinery. B03-B activates Event against that same owner. Schedule remains distinct from Temporal Constraint.

### 5.3 Event

`dante.event` remains the CP6 Event NativeRef owner. B03-A adds the minimum expectation/create boundary; B03-D adds ordered internal Agenda truth. Agenda values do not gain NativeRef/Schedule identity by convenience.

### 5.4 Temporal Constraint — B04-A/B/C ✅ CLOSED / PROVEN

Temporal Constraint is materialized as a stable `ScopedRecordRef` LR-05 dependent, not as a NativeRef root and not as Schedule placement.

Canonical shape through B04-C:

```text
temporal_constraint
  └─ temporal_constraint_state
      ├─ temporal_constraint_boundary_state
      │   └─ temporal_constraint_boundary_absolute_state
      └─ temporal_constraint_window_state
          └─ temporal_constraint_window_absolute_state

scoped_current_material_state
       ≈
temporal_constraint_current_history

temporal_constraint_mutation_operation
```

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

All require hard|soft strength and exact typed payload totality. Boundary values are finite absolute instants. Window values are finite explicit endpoints with `ends_at > starts_at`.

Create/revise/retire remain governed by typed mutation routines. Revision appends a new MaterialState; retirement closes currentness and preserves identity/history. Operation identity is not Domain identity.

`enforce_temporal_constraint_rule_totality()` validates the exact family/payload and relation/facet matrix so widened envelope CHECKs do not admit invalid semantic combinations.

Permanent non-collapse remains:

```text
Schedule != Temporal Constraint
Temporal Constraint != Movement Policy
Temporal Constraint != Recurrence
Temporal Constraint != Session / Actual
constraint revision != Schedule revision
deadline != Schedule end
passed deadline != Actual
passed deadline != Outcome / failure
window != placement
preference != accepted Schedule
evaluation != solver decision
violation != automatic mutation
current accepted state != newest row
idempotency key != Domain identity
```

B04-D Movement Policy, B04-E duration/spacing/relative families and B12 solver behavior are not represented as complete by current materialization.

## 6. Proof state

```text
B01 Activity Core                    CLOSED / PROVEN
B02 Schedule Core                    CLOSED / PROVEN
B03 Event Core                       CLOSED / PROVEN
B04-A overall                        CLOSED / PROVEN at 20260918_33
B04-B overall                        CLOSED / PROVEN at 20260919_34
B04-C overall                        CLOSED / PROVEN at 20260919_36
B04 overall                          IN PROGRESS
```

B04-C final reconciliation evidence:

```text
PostgreSQL / application evaluation             9 PASS / 2 deselected
current catalog / Dictionary / ACL             12 PASS
OpenAPI / Temporal API contract                24 PASS
@dante/api-client typecheck                    PASS
@dante/api-client Vitest                       11 PASS
pnpm generated:check                           PASS / 177 deterministic files
```

Observed current topology:

```text
109|5|35|87|214|131|312|0|0|0
```

## 7. Object contract

Every standalone business-schema object records semantic traceability, implementation provenance, exact structure, lifecycle/currentness semantics, ACL and proof obligations. Embedded indexes/FKs/CHECKs/triggers remain attached to their owning tables; routines remain standalone because signature/security/search-path/ACL are independently governed.

Shared CP6 entries keep their original introducing revision/stage when later slices extend bounded dispatchers. Later extension is represented in current semantics/proof rather than falsifying provenance.

## 8. Validation

Required current validation remains:

```text
JSON Schema consistency
filename/object-key agreement
FK/trigger target resolution
scope counts ↔ object tree
Dictionary ↔ SQLAlchemy ↔ Alembic ↔ PostgreSQL
owner/ACL parity
routine search_path/security parity
extension-owned objects excluded correctly
observer technical-role/provisioning/live-ACL parity
```

## 9. Same-change rule

No real object → no ceremonial Dictionary entry. Every real current DANTE business object requires matching Dictionary/Alembic/SQLAlchemy/current-human-reference/direct-PostgreSQL proof in the same reviewed slice.

For Timeline B04+, a DB-affecting slice cannot close while `docs/database/README.md`, `docs/database/timeline-temporal-operational.md`, the Dictionary tree/scope, SQLAlchemy, Alembic, catalog/ACL proof or affected workstream closure evidence disagree.
