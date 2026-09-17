# DANTE Database Dictionary

- **Status:** CURRENT / MATERIALIZED FOR CHECKED-OUT REPOSITORY STATE
- **Schema version:** 1
- **Serialization:** JSON
- **PostgreSQL:** 18.6
- **Protected-main Alembic head:** `20260906_18`
- **Protected-main topology:** `89|5|18|77|173|91|272|0|0|0`
- **Current candidate Alembic head on `feature/timeline-temporal-operational`:** `20260917_29`
- **Current candidate topology:** `101|5|31|78|198|119|297|0|0|0`
- **Frozen CP6 head:** `20260826_08`
- **Last reconciled:** 2026-09-17

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

A mismatch is a defect. Protected `main` remains integration authority; `_29` is candidate truth on the Timeline branch.

## 2. Current checked-out business-schema inventory

The authoritative machine-readable counts are in `scope.json` and currently equal:

```text
tables      101
views         5
routines     31
standalone  137
triggers     78
indexes      198
FKs          119
CHECKs       297
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
101 tables / 5 views / 31 routines / 137 standalone
78 triggers / 198 indexes / 119 FKs / 297 CHECKs
```

`completed_stages` in `scope.json` remains CP6 provenance only. Post-CP6 provenance belongs on the actual object entries.

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
  event_create_operation accepted initial Agenda replay snapshot
```

The final object tree and `scope.json` counts, not this prose summary, are the structural source of truth.

## 5. Timeline persistence classification

### 5.1 Activity

`dante.activity` remains the CP6 Activity NativeRef owner. B01 adds only the typed dependent descriptor, create receipt and bounded create capability.

### 5.2 Schedule

`dante.schedule` remains the single shared CP6 Schedule owner. B02 reuses the CP6 placement MaterialState/current/history machinery. Physical subject eligibility remains:

```text
activity | event | occurrence
```

B03-B activates Event against that same Schedule owner. No `event_schedule` exists.

### 5.3 Event

`dante.event` remains the CP6 Event NativeRef owner. B03-A adds the minimum expectation/create boundary; B03-D adds only ordered internal Agenda truth.

```text
Event
└── ordered Agenda/internal parts
```

Agenda parts are normalized ordered values owned by Event. They do not receive their own NativeRef and do not become Activity/Event/Occurrence/Session/Actual merely because they are editable or reorderable.

`event_agenda_current` is an aggregate CAS revision boundary for the Event Agenda. `event_agenda_mutation_operation` is technical idempotency/control state. Neither is a second Event identity nor a temporal MaterialState substitute.

Permanent boundaries:

```text
Activity != Event
Event != Schedule
Event != Recurrence != Occurrence
Event != Session != Actual != Outcome
Agenda part != Activity/Event/Occurrence/Session/Actual
Event identity != operation/idempotency identity
provider identity != DANTE Event identity
```

## 6. B03-D proof state

Executed real PostgreSQL/API Agenda proof:

```text
apps/backend/tests/integration/temporal/test_b03_event_agenda.py
2 / 2 PASS
```

The test proves create plus initial Agenda, add/edit/reorder/remove through whole-Agenda CAS replacement, idempotent replay, stale-revision rejection, reload, CSRF and authenticated self-scope isolation.

B03-D is not promoted to CLOSED/PROVEN until current-catalog/Dictionary/Alembic/migration and real frontend gates are also green.

## 7. Object contract

Every standalone business-schema object records semantic traceability, implementation provenance, exact structure, lifecycle/currentness semantics, ACL and proof obligations. Embedded indexes/FKs/CHECKs/triggers remain attached to their owning tables; routines remain standalone because signature/security/search-path/ACL are independently governed.

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
