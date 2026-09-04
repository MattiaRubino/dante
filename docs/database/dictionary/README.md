# DANTE Database Dictionary

**Status:** CURRENT / MATERIALIZED  
**Schema version:** 1  
**Serialization:** JSON  
**Validation:** JSON Schema Draft 2020-12 + DANTE cross-representation validation  
**Current PostgreSQL:** 18.6  
**Current Alembic head:** `20260830_09`  

## Purpose

The Dictionary is the machine-readable companion to the current DANTE Database Architecture & Reference. It must describe the same database that Alembic, SQLAlchemy and real PostgreSQL materialize; a mismatch is a defect.

```text
Database Architecture & Reference
≈ Database Dictionary
≈ SQLAlchemy MetaData / mappings
≈ Alembic head
≈ real PostgreSQL schema
```

## Current materialized shape

```text
69 table entries
5 view entries
15 routine entries
------------------
89 standalone entries

76 trigger attachments
97 physical indexes
69 foreign keys
123 CHECK constraints
```

`dante.alembic_version` remains technical foundation and is not counted as a DANTE semantic/business table. Extension-owned objects remain outside DANTE object entries.

Current materialization stages are exactly:

```text
CP6-M01
CP6-M02
CP6-M03
CP6-M04
CP6-M05
CP6-M06
CP6-M07
RECOVERY-CP06
```

`RECOVERY-CP06` is an explicit post-CP6 database evolution stage. It is not a fictitious `CP6-M08` and does not reopen the closed CP6 materialization DAG.

## Recovery lifecycle evolution

The current database includes `dante.material_state_retirement` and `dante.enforce_material_state_retirement()`.

The lifecycle contract for all five materialized MaterialState facets is now:

```text
live MaterialStateRef
→ protected payload present under the facet-specific invariant
→ accepted retirement/redaction
→ protected payload removed
→ material_state_retirement committed
→ NativeRef / ScopedRecordRef ownership, MaterialStateRef address and required history remain truthful
```

The five covered facets are:

```text
schedule.placement
actual.realization
session.timing
routine.recurrence
event.recurrence
```

A retired MaterialStateRef must not regain protected facet payload. The existing facet validators plus the retirement validator enforce this at the database boundary.

`recovery_suppression_ref` is a technical UUIDv7 linking canonical PostgreSQL retirement to independently durable disaster-recovery suppression evidence. It is not a Domain identity or a fifth DANTE reference family.

## Recovery suppression boundary

PostgreSQL remains canonical. The recovery suppression ledger is a technical disaster-recovery control only.

The accepted protocol is:

```text
write immutable PREPARED
→ commit canonical PostgreSQL retirement/redaction
→ read back canonical retirement
→ write immutable COMMITTED referencing SHA-256(PREPARED)
```

Recovery handling is fail-closed:

```text
valid PREPARED + COMMITTED
→ eligible for deterministic suppression reconciliation

PREPARED without COMMITTED
COMMITTED without PREPARED
hash mismatch / malformed record
→ recovery BLOCKED
```

The independently durable suppression evidence may not expire while any retained database backup/WAL/object version can still resurrect the protected payload.

## Object schema

Every standalone entry keeps the strict blocks:

```text
object
purpose
classification
semantic_traceability
implementation
structure
state_history
lifecycle
security
proof
```

`additionalProperties: false` remains the default throughout governed shapes. `implementation.introducing_stage` is a closed vocabulary and currently allows only CP6-M01..M07 plus `RECOVERY-CP06`.

## Structural truth vs semantic truth

Mechanically reconciled facts include columns/types/nullability/defaults, PK/FK/UQ/CHECK, indexes, triggers, views, routines, owner/ACL, Alembic revision, SQLAlchemy mapping and exact PostgreSQL object properties.

Human-authored facts include purpose, semantic owner/facet, lifecycle meaning, canonicality, invariants and proof rationale. Generated DDL must not silently overwrite those semantic fields.

## Security

DANTE-owned objects remain owned by `dante_owner` and default-deny non-owner access. The recovery retirement table grants `dante_runtime` SELECT only; runtime receives no INSERT/UPDATE/DELETE and no direct EXECUTE on the retirement validator.

## Same-change rule

A structural database change is incomplete unless Alembic, SQLAlchemy, Dictionary, current human-readable database reference and direct database tests are reconciled in the same reviewed change.

Current validation must prove at least:

```text
69 tables / 5 views / 15 routines
76 triggers / 97 physical indexes
69 FKs / 123 CHECKs
Dictionary JSON-Schema validity
Dictionary internal/cross-file integrity
Dictionary ↔ SQLAlchemy
Dictionary ↔ Alembic head 20260830_09
Dictionary ↔ live PostgreSQL 18.6
owner / ACL / extension posture
retirement/redaction lifecycle invariants
SC-011 anti-resurrection recovery behavior
```

Git retains superseded database/document history. This README and the Dictionary describe current truth.
