# DANTE Database Dictionary

- **Status:** CURRENT / MATERIALIZED FOR CHECKED-OUT REPOSITORY STATE
- **Schema version:** 1
- **Serialization:** JSON
- **PostgreSQL:** 18.6
- **Protected-main Alembic head:** `20260906_18`
- **Protected-main topology:** `89|5|18|77|173|91|272|0|0|0`
- **Current candidate Alembic head on `feature/timeline-temporal-operational`:** `20260918_32`
- **Current candidate topology:** `107|5|33|85|212|129|309|0|0|0`
- **Frozen CP6 head:** `20260826_08`
- **Last reconciled:** 2026-09-18

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

A mismatch is a defect. Protected `main` remains integration authority; `_32` is candidate truth on the Timeline branch and must not be relabeled as protected-main truth before integration.

## 2. Current checked-out business-schema inventory

The authoritative machine-readable counts are in `scope.json` and currently equal:

```text
tables      107
views         5
routines     33
standalone  145
triggers     85
indexes      212
FKs          129
CHECKs       309
```

No enum/domain, sequence, materialized view, partitioned table or RLS policy exists in the DANTE business-schema inventory.

The `_32` counts above are not arithmetic projections: they were read directly from a PostgreSQL 18.6 database migrated to the candidate head by `test_b04_temporal_constraint_catalog.py`.

## 3. Frozen CP6 baseline vs current materialization

Frozen CP6 baseline remains historical evidence:

```text
68 tables / 5 views / 14 routines / 87 standalone
75 triggers / 95 indexes / 68 FKs / 120 CHECKs
```

Current candidate materialization is:

```text
107 tables / 5 views / 33 routines / 145 standalone
85 triggers / 212 indexes / 129 FKs / 309 CHECKs
```

`completed_stages` in `scope.json` remains CP6 provenance only. Post-CP6 provenance belongs on the actual object entries; B04-A does not rewrite CP6 history.

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
  Event + Schedule atomic create/read/Timeline support

B03-C
  no DDL: Event placement lifecycle reuses the shared Schedule mutation family

B03-D / 20260917_29
  event_agenda_part
  event_agenda_current
  event_agenda_mutation_operation
  create_self_event_with_agenda(...)
  replace_self_event_agenda(...)

B04-A / 20260918_30 → 20260918_32
  temporal_constraint
  temporal_constraint_state
  temporal_constraint_boundary_state
  temporal_constraint_boundary_absolute_state
  temporal_constraint_current_history
  temporal_constraint_mutation_operation
  enforce_temporal_constraint_rule_totality()
  mutate_self_absolute_earliest_start_constraint(...)
  bounded shared dispatcher extension for temporal_constraint.rule
  MaterialState cross-family totality hardening
  current-history table-first dispatch hardening
```

The final object tree and `scope.json` counts, not this prose summary, are the structural source of truth.

## 5. Timeline persistence classification

### 5.1 Activity

`dante.activity` remains the CP6 Activity NativeRef owner. B01 adds only the typed dependent descriptor, create receipt and bounded create capability.

### 5.2 Schedule

`dante.schedule` remains the single shared CP6 Schedule owner. B02 reuses the CP6 placement MaterialState/current/history machinery. B03-B activates Event against that same owner. Schedule remains distinct from Temporal Constraint.

### 5.3 Event

`dante.event` remains the CP6 Event NativeRef owner. B03-A adds the minimum expectation/create boundary; B03-D adds only ordered internal Agenda truth. Agenda values do not gain NativeRef/Schedule identity by convenience.

### 5.4 Temporal Constraint — B04-A candidate core

Temporal Constraint is now materialized as a stable `ScopedRecordRef` LR-05 dependent, not as a NativeRef root and not as Schedule placement.

B04-A activates one complete typed rule path:

```text
subject             Activity | Event, self-owned
facet               temporal_constraint.rule
family              boundary
kind                earliest_start
constrained facet   schedule.start
strength            hard | soft
temporal form       absolute
value               finite timestamptz
```

Canonical shape:

```text
temporal_constraint
  └─ temporal_constraint_state                immutable MaterialState revision
      └─ temporal_constraint_boundary_state   boundary/absolute discriminator
          └─ temporal_constraint_boundary_absolute_state

scoped_current_material_state                 accepted current rule
       ≈
temporal_constraint_current_history           retained currentness chronology

temporal_constraint_mutation_operation        technical idempotency/CAS receipt
```

Create/revise/retire are governed by `mutate_self_absolute_earliest_start_constraint(...)`. Revision appends a new MaterialState; retirement closes currentness and preserves constraint/history. Operation identity is not Domain identity.

Permanent non-collapse remains:

```text
Schedule != Temporal Constraint
Temporal Constraint != Movement Policy
Temporal Constraint != Recurrence
Temporal Constraint != Session / Actual
constraint revision != Schedule revision
current accepted state != newest row
idempotency key != Domain identity
```

B04-B+ boundary forms, deadlines, windows/preferences, movement policy, duration/spacing/relative families and solver behavior are not represented as complete by this B04-A materialization.

## 6. Proof state

```text
B01 Activity Core                    CLOSED / PROVEN
B02 Schedule Core                    CLOSED / PROVEN
B03 Event Core                       CLOSED / PROVEN
B04-A A1 DDL / mappings              PROVEN
B04-A A2 PostgreSQL / catalog / ACL  PROVEN
B04-A A3 CAS / idempotency           PROVEN
B04-A A4 Dictionary/docs             MATERIALIZED; current-catalog proof pending
B04-A A5 application / API           NOT STARTED
B04-A overall                        IN PROGRESS
```

Current B04-A evidence includes the focused Temporal Constraint PostgreSQL suite, shared current-history dispatch regression, broad Temporal/CP6 regression and the dedicated `_32` catalog/ACL proof. A4 is not marked closed until the reconciled Dictionary/current-catalog tests run green against this object tree.

## 7. Object contract

Every standalone business-schema object records semantic traceability, implementation provenance, exact structure, lifecycle/currentness semantics, ACL and proof obligations. Embedded indexes/FKs/CHECKs/triggers remain attached to their owning tables; routines remain standalone because signature/security/search-path/ACL are independently governed.

Shared CP6 entries keep their original introducing revision/stage when B04-A extends a bounded dispatcher. The B04-A extension is represented in current semantics/proof rather than falsifying provenance.

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
