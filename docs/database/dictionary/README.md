# DANTE Database Dictionary

- **Status:** CURRENT / MATERIALIZED
- **Schema version:** 1
- **Serialization:** JSON
- **PostgreSQL:** 18.6
- **Alembic head:** `20260904_17`
- **Frozen CP6 head:** `20260826_08`
- **Last reconciled:** 2026-09-05

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

## 2. Current business-schema inventory

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

This is the current Recovery + Access/Auth + shared Email Platform business-schema materialization at `20260904_17`.

Platform Observability adds no Dictionary business object, Alembic revision or SQLAlchemy business mapping.

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

`completed_stages` remains CP6 provenance only. Recovery, Access/Auth and Email provenance is represented per object through `implementation.introducing_stage`, `alembic_revision` and `runtime_acl_stage`.

## 4. Post-CP6 evolution

```text
RECOVERY
20260830_09

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

Recovery does not become a fictitious CP6 stage and Email does not become CP6 provenance.

## 5. Object contract

Every standalone business-schema object records object identity, purpose, classification, semantic traceability, implementation provenance, exact structure, lifecycle/state-history semantics, security/ACL and proof obligations.

Embedded table objects remain PK/FK/UQ/CHECK/index/trigger attachments. Routines remain standalone because signature/security/search-path/ACL are independently governed.

## 6. Shared Email classification

Email delivery objects are `family=email_platform` shared technical infrastructure. Access/Auth is a consumer, not platform owner. They are not MaterialState and are not a generic event-bus/outbox root.

## 7. Operational observer scope

`dante_observer` is deliberately **outside the business-object inventory above**. It is a provisioning-owned PostgreSQL operational role, not a table/view/routine/model and therefore must not be represented as fake Dictionary business materialization.

Its exact security contract is current authority in:

- `../dante-postgresql-database-part-12.md` — Section 46 / `DANTE-OBSERVABILITY-OBSERVER-CONTRACT v1`
- `../README.md` — observer-role routing
- `../../../infra/observability/README.md` — collector usage
- provisioning and live PostgreSQL ACL tests

Required posture remains `LOGIN NOINHERIT`, `pg_read_all_stats` membership with `INHERIT TRUE / SET FALSE / ADMIN FALSE`, `search_path=pg_catalog`, no database `CREATE`/`TEMP`, no DANTE/public business-object access and no DANTE application-role membership.

## 8. Validation

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
observer technical-role/provisioning/live-ACL parity
```

`test_current_catalog.py` and `test_database_current_catalog.py` are current live cross-representation gates. Historical CP6 tests independently prove the frozen CP6 baseline. Platform Observability PostgreSQL acceptance additionally proves the exact observer-role boundary.

## 9. Same-change rule

No real business object → no ceremonial Dictionary entry. Every real current DANTE business object requires a matching Dictionary entry and same-change reconciliation.

Operational-role contracts remain same-change governed through their dedicated technical-role reference, provisioning and live privilege tests rather than by inventing business Dictionary objects.
