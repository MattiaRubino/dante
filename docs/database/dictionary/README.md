# DANTE Database Dictionary

- **Status:** CURRENT / MATERIALIZED FOR CHECKED-OUT REPOSITORY STATE
- **Schema version:** 1
- **Serialization:** JSON
- **PostgreSQL:** 18.6
- **Protected-main Alembic head:** `20260906_18`
- **Protected-main topology:** `89|5|18|77|173|91|272|0|0|0`
- **Current candidate Alembic head on `feature/timeline-temporal-operational`:** `20260915_26`
- **Current candidate topology:** `96|5|28|78|191|111|285|0|0|0`
- **Frozen CP6 head:** `20260826_08`
- **Last reconciled:** 2026-09-16

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

A mismatch is a defect.

Protected `main` remains integration authority. `_26` is the reconciled candidate truth on `feature/timeline-temporal-operational`; it is not silently relabeled as protected-main truth.

## 2. Current checked-out business-schema inventory

The authoritative machine-readable counts are in `scope.json` and currently equal:

```text
tables       96
views         5
routines     28
standalone  129
triggers     78
indexes      191
FKs          111
CHECKs       285
```

No enum/domain, sequence, materialized view, partitioned table or RLS policy exists in the DANTE business-schema inventory.

## 3. Frozen CP6 baseline vs current materialization

Frozen CP6 baseline remains historical evidence:

```text
68 tables / 5 views / 14 routines / 87 standalone
75 triggers / 95 indexes / 68 FKs / 120 CHECKs
```

Current candidate materialization is:

```text
96 tables / 5 views / 28 routines / 129 standalone
78 triggers / 191 indexes / 111 FKs / 285 CHECKs
```

`completed_stages` in `scope.json` remains CP6 provenance only. Post-CP6 provenance belongs on the actual object entries; no fictitious CP6 stage is invented.

## 4. Post-CP6 Timeline evolution

```text
B01 / 20260908_19
  activity_intention
  activity_create_operation
  create_self_activity(...)

B02-A / 20260909_20
  schedule_establish_operation
  establish_self_floating_schedule(...)

20260909_21
  forward ACL hardening

B02-C / 20260913_22
  schedule_revision_operation
  revise_self_floating_schedule(...)

B02-D / 20260914_23
  schedule_unschedule_operation
  schedule_unschedule_undo_operation
  unschedule_self_schedule(...)
  undo_self_schedule_unschedule(...)

B02 hardening / 20260914_24
  PL/pgSQL disambiguation/hardening without reopening historical migrations

B02-E / 20260915_25
  complete Schedule placement union
  coarse-local-period state/payload
  generic establish/revise/unschedule/Undo capability surfaces

B02-E / 20260915_26
  named-zone DST-gap resolution hardening
  final B02 current-catalog reconciliation
```

The final object tree and `scope.json` counts, not this prose summary, are the structural source of truth.

## 5. Timeline persistence classification

### 5.1 Activity

`dante.activity` remains the CP6 Activity NativeRef owner. B01 adds only the typed dependent descriptor, create receipt and bounded create capability.

### 5.2 Schedule

`dante.schedule` remains the single shared CP6 Schedule owner. B02 reuses the CP6 placement MaterialState/current/history machinery and activates the accepted placement union:

```text
date_span
floating_local
named_zone_local
absolute
coarse_local_period
```

Permanent boundaries:

```text
Activity != Schedule
Event != Schedule
Schedule != Session != Actual
Schedule identity != placement MaterialState
current accepted placement != latest row
operation receipt != canonical Schedule truth
unscheduled != deleted
Undo != DB/history rewind
```

Schedule physical subject eligibility remains:

```text
activity | event | occurrence
```

B02 product-activated Activity. B03 must activate Event by reusing this shared Schedule capability, not by creating `event_schedule`.

## 6. B02 closure evidence

Executed `_26` reconciliation:

```text
scope/object tree ↔ SQLAlchemy ↔ Alembic ↔ PostgreSQL    PASS
current-catalog + migration PostgreSQL gate              20 / 20 PASS
HEAD → base → HEAD round-trip                              1 / 1 PASS
B02 PostgreSQL proof group                                11 PASS / 2 deselected
```

`scope.json` already carries the final `_26` object counts.

## 7. B03 starting point

B03 pre-scope verified:

```text
Event NativeRef owner / EventRow              EXISTS
Event typed product descriptor                MISSING
Event idempotent create receipt/capability    MISSING
Schedule Event physical eligibility           EXISTS
B02 Schedule runtime self-scope                ACTIVITY-DESCRIPTOR BOUND
Timeline Event projection                     MISSING
```

Expected B03 DDL, if exact-head implementation re-read confirms the same gap, is narrowly Event-owned descriptor/control persistence plus bounded capability changes. No generic Event metadata JSON, generic status, generic temporal object or Event-specific Schedule owner is authorized.

## 8. Object contract

Every standalone business-schema object records semantic traceability, implementation provenance, exact structure, lifecycle/currentness semantics, ACL and proof obligations. Embedded indexes/FKs/CHECKs/triggers remain attached to their owning tables; routines remain standalone because signature/security/search-path/ACL are independently governed.

## 9. Validation

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

B03 must extend these same gates for every real new Event object/routine.

## 10. Same-change rule

No real object → no ceremonial Dictionary entry. Every real current DANTE business object requires matching Dictionary/Alembic/SQLAlchemy/current-human-reference/direct-PostgreSQL proof in the same reviewed slice.