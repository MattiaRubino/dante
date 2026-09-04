# DANTE Database Dictionary

- **Status:** CURRENT / MATERIALIZED / INTEGRATION CANDIDATE
- **Schema version:** 1
- **Serialization:** JSON
- **PostgreSQL:** 18.6
- **Candidate Alembic head:** `20260904_17`
- **Frozen CP6 head:** `20260826_08`

## 1. Purpose

Machine-readable companion to the current DANTE Database System of Record.

```text
Current DB Reference
≈ Database Dictionary
≈ SQLAlchemy MetaData / mappings
≈ Alembic
≈ real PostgreSQL
≈ direct tests
```

A mismatch is a defect.

## 2. Current inventory

```text
tables       88
views         5
routines     16
standalone  109
triggers     76
indexes      172
FKs           89
CHECKs       270
```

This includes protected-main Recovery plus Access/Auth and the shared Email Platform under the candidate merge head.

## 3. Frozen CP6 baseline vs current materialization

`expected_baseline` remains exactly:

```text
68 tables / 5 views / 14 routines / 87 standalone
75 triggers / 95 indexes / 68 FKs / 120 CHECKs
```

`current_materialization` is:

```text
88 tables / 5 views / 16 routines / 109 standalone
76 triggers / 172 indexes / 89 FKs / 270 CHECKs
```

`completed_stages` is intentionally only `CP6-M01..CP6-M07`. Recovery, Access/Auth and Email provenance is represented per object through `implementation.introducing_stage`, `alembic_revision` and `runtime_acl_stage`.

## 4. Post-CP6 evolution

```text
RECOVERY
20260830_09
  material_state_retirement
  enforce_material_state_retirement

ACCESS/AUTH
20260827_09
20260827_10
20260829_11
20260830_12
20260831_13

SHARED EMAIL PLATFORM
20260903_14
20260903_15
20260904_16

CONVERGENCE
20260904_17
  no-DDL Alembic merge revision
```

Recovery does not become a fictitious CP6-M08 and Email does not become CP6 provenance.

## 5. Object contract

Every standalone object records object identity, purpose, classification, semantic traceability, implementation provenance, exact structure, lifecycle/state-history semantics, security/ACL and proof obligations.

Embedded table objects remain PK/FK/UQ/CHECK/index/trigger attachments. Routines remain standalone because signature/security/search-path/ACL are independently governed.

## 6. Shared Email classification

Email delivery objects are `family=email_platform` shared technical infrastructure. Access/Auth is a consumer, not platform owner. They are not MaterialState and are not a generic event bus/outbox root.

## 7. Validation

Required:

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

`test_current_catalog.py` and `test_database_current_catalog.py` are current live cross-representation gates. Historical CP6 tests independently prove the frozen CP6 baseline.

## 8. Same-change rule

No real object → no ceremonial Dictionary entry. Every real current DANTE object requires a matching Dictionary entry and same-change reconciliation.
