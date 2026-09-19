# DANTE Database Dictionary

- **Status:** CURRENT / MATERIALIZED FOR CHECKED-OUT REPOSITORY STATE
- **Schema version:** 1
- **Serialization:** JSON
- **PostgreSQL:** 18.6
- **Protected-main Alembic head:** `20260906_18`
- **Protected-main topology:** `89|5|18|77|173|91|272|0|0|0`
- **Current candidate Alembic head on `feature/timeline-temporal-operational`:** `20260919_34`
- **Current candidate topology:** `107|5|34|85|212|129|309|0|0|0`
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

A mismatch is a defect. Protected `main` remains integration authority; `_34` is candidate truth on the Timeline branch and must not be relabeled as protected-main truth before integration.

## 2. Current checked-out business-schema inventory

The authoritative machine-readable counts are in `scope.json` and currently equal:

```text
tables      107
views         5
routines     34
standalone  146
triggers     85
indexes      212
FKs          129
CHECKs       309
```

No enum/domain, sequence, materialized view, partitioned table or RLS policy exists in the DANTE business-schema inventory.

These counts are live PostgreSQL-backed candidate truth. `_34` adds `mutate_self_absolute_boundary_constraint(...)`; all other structural counts remain unchanged from `_33`.

## 3. Frozen CP6 baseline vs current materialization

Frozen CP6 baseline remains historical evidence:

```text
68 tables / 5 views / 14 routines / 87 standalone
75 triggers / 95 indexes / 68 FKs / 120 CHECKs
```

Current candidate materialization is:

```text
107 tables / 5 views / 34 routines / 146 standalone
85 triggers / 212 indexes / 129 FKs / 309 CHECKs
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
```

The final object tree and `scope.json` counts, not this prose summary, are the structural source of truth.

## 5. Timeline persistence classification

### 5.1 Activity

`dante.activity` remains the CP6 Activity NativeRef owner. B01 adds only the typed dependent descriptor, create receipt and bounded create capability.

### 5.2 Schedule

`dante.schedule` remains the single shared CP6 Schedule owner. B02 reuses the CP6 placement MaterialState/current/history machinery. B03-B activates Event against that same owner. Schedule remains distinct from Temporal Constraint.

### 5.3 Event

`dante.event` remains the CP6 Event NativeRef owner. B03-A adds the minimum expectation/create boundary; B03-D adds ordered internal Agenda truth. Agenda values do not gain NativeRef/Schedule identity by convenience.

### 5.4 Temporal Constraint — B04-A/B04-B ✅ CLOSED / PROVEN

Temporal Constraint is materialized as a stable `ScopedRecordRef` LR-05 dependent, not as a NativeRef root and not as Schedule placement.

Canonical shape:

```text
temporal_constraint
  └─ temporal_constraint_state                immutable MaterialState revision
      └─ temporal_constraint_boundary_state   boundary kind / temporal form
          └─ temporal_constraint_boundary_absolute_state

scoped_current_material_state                 accepted current rule
       ≈
temporal_constraint_current_history           retained currentness chronology

temporal_constraint_mutation_operation        technical idempotency/CAS receipt
```

Accepted B04-B absolute variants:

```text
earliest_start     + schedule.start
latest_start       + schedule.start
latest_completion  + schedule.completion
```

All require hard|soft strength, `absolute` temporal form and finite `timestamptz` payload.

Create/revise/retire are governed by `mutate_self_absolute_boundary_constraint(...)` for the B04-B union. `mutate_self_absolute_earliest_start_constraint(...)` remains present for B04-A compatibility. Revision appends a new MaterialState; retirement closes currentness and preserves identity/history. Operation identity is not Domain identity.

`enforce_temporal_constraint_rule_totality()` now validates the exact kind↔facet matrix, so widened column CHECKs do not permit semantically invalid combinations.

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
current accepted state != newest row
idempotency key != Domain identity
```

B04-C+ windows/preferences/evaluation, Movement Policy, duration/spacing/relative families and solver behavior are not represented as complete by current materialization.

## 6. Proof state

```text
B01 Activity Core                    CLOSED / PROVEN
B02 Schedule Core                    CLOSED / PROVEN
B03 Event Core                       CLOSED / PROVEN
B04-A overall                        CLOSED / PROVEN at 20260918_33
B04-B overall                        CLOSED / PROVEN at 20260919_34
B04 overall                          IN PROGRESS
```

B04-B final reconciliation evidence:

```text
API / typed union / inventory                 13 PASS
PostgreSQL/application/catalog                22 PASS / 1 deselected
OpenAPI export/inventory/API                  21 PASS
@dante/api-client typecheck                   PASS
@dante/api-client Vitest                      11 PASS
pnpm generated:check                          PASS / 163 deterministic files
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
