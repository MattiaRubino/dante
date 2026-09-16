# DANTE Database Dictionary

- **Status:** CURRENT / MATERIALIZED FOR CHECKED-OUT REPOSITORY STATE
- **Schema version:** 1
- **Serialization:** JSON
- **PostgreSQL:** 18.6
- **Protected-main Alembic head:** `20260906_18`
- **Protected-main topology:** `89|5|18|77|173|91|272|0|0|0`
- **Current candidate Alembic head on `feature/timeline-temporal-operational`:** `20260916_27`
- **Current candidate topology:** `98|5|29|78|195|115|288|0|0|0`
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

A mismatch is a defect. Protected `main` remains integration authority; `_27` is candidate truth on the Timeline branch.

## 2. Current checked-out business-schema inventory

The authoritative machine-readable counts are in `scope.json` and currently equal:

```text
tables       98
views         5
routines     29
standalone  132
triggers     78
indexes      195
FKs          115
CHECKs       288
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
98 tables / 5 views / 29 routines / 132 standalone
78 triggers / 195 indexes / 115 FKs / 288 CHECKs
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

### 5.3 Event

`dante.event` remains the CP6 Event NativeRef owner. B03-A adds:

```text
event_expectation
event_create_operation
create_self_event(...)
```

This is intentionally not an Event mega-profile. Temporal placement remains Schedule; recurrence remains Recurrence; participation, execution and realized truth remain their own later owners.

Permanent boundaries:

```text
Activity != Event
Event != Schedule
Event != Recurrence != Occurrence
Event != Session != Actual != Outcome
Event identity != operation/idempotency identity
provider identity != DANTE Event identity
```

## 6. Current B03-A proof state

Executed application/PostgreSQL proof:

```text
apps/backend/tests/integration/temporal/test_b03_event_core.py
2 / 2 PASS
```

Current-catalog/Dictionary/Alembic/migration gates must also pass before B03-A is promoted to CLOSED/PROVEN.

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