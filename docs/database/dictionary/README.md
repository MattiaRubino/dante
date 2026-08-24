# DANTE Database Dictionary

**Status:** CP6-03 READINESS FOUNDATION / OBJECT ENTRIES NOT YET MATERIALIZED  
**Schema version:** 1  
**Serialization:** JSON  
**Validation dialect:** JSON Schema Draft 2020-12  

## Purpose

This directory is the machine-readable companion to the human-readable DANTE Database Architecture & Reference.

It does not replace Domain, Logical, Physical, the PostgreSQL Persistence Constitution, Alembic, SQLAlchemy or real PostgreSQL introspection. It provides one structured current metadata surface that those authorities can be reconciled against.

The long-lived consistency target is:

```text
Database Architecture & Reference
≈ Database Dictionary
≈ SQLAlchemy MetaData / mappings
≈ Alembic head
≈ real PostgreSQL schema
```

A mismatch is a defect to investigate.

## Current readiness-only shape

```text
dictionary/
├── README.md
├── scope.json
└── schema/
    ├── object-v1.schema.json
    └── scope-v1.schema.json
```

The following directories deliberately do not exist yet:

```text
tables/
views/
routines/
```

They are created in CP6-04 only when the first real object entries exist. Empty ceremonial object directories are forbidden.

## Final baseline entry counts

After complete CP6-04 materialization the expected DANTE-owned Dictionary contains:

```text
68 table entries
5 view entries
14 routine entries
------------------
87 standalone entries
```

Object entry keys are stable and typed:

```text
table:dante.<name>
view:dante.<name>
routine:dante.<name>
```

The exact PostgreSQL object name is also the JSON file name in the applicable directory.

## Embedded objects

The Dictionary is object-complete without creating a separate file for every PostgreSQL sub-object.

Embedded in the owning table entry:

```text
primary keys
foreign keys
unique constraints
check constraints
indexes
trigger attachments
```

Final baseline reconciliation target:

```text
95 physical indexes
75 trigger attachments
```

The 14 integrity routines remain standalone entries because they are independently owned PostgreSQL objects with their own security/ACL properties and may have multiple trigger attachments.

## Ownership spaces

`scope.json` distinguishes three spaces.

### DANTE-owned

The business/control schema contract governed by Parts 1–15.

### Technical foundation

Includes:

```text
dante.alembic_version
dante_owner
dante_migrator
dante_runtime
```

`dante.alembic_version` is not a DANTE semantic/business table entry.

### Extension-owned

Current foundation extensions:

```text
postgis
vector
pg_trgm
unaccent
pg_stat_statements
```

Objects internally created/owned by those extensions are not promoted into DANTE object entries merely because PostgreSQL introspection exposes them.

## Object schema

Every standalone entry has ten required top-level blocks:

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

Object types are exactly:

```text
table
view
routine
```

The schema is intentionally strict (`additionalProperties: false` throughout the governed shapes) so accidental new metadata fields require a reviewed dictionary-schema evolution rather than silently becoming convention.

## Structural truth and semantic truth

### Mechanically reconcilable

These facts SHOULD be verified automatically against SQLAlchemy/Alembic/PostgreSQL where applicable:

```text
object name/type
columns/types/nullability
PK/FK/UQ/CK
indexes
view structure
routine properties
trigger attachments
owner
ACL
Alembic revision
SQLAlchemy mapping
```

### Human-authored semantic metadata

These facts MUST remain reviewed semantic documentation:

```text
why the object exists
what a column/reference means
why a constraint/index exists
semantic owner/facet
current/history interpretation
lifecycle meaning
canonicality boundary
proof rationale
```

Generated DDL must not overwrite the human semantic fields.

## Table entries

A table entry includes the exact column contract and embedded:

```text
primary key
foreign keys
unique constraints
check constraints
indexes
trigger attachments
```

Foreign-key metadata includes reference-family/cardinality/semantic reason in addition to the physical target.

Index metadata identifies whether the physical index originates from:

```text
primary_key
unique_constraint
explicit_index
```

This prevents duplicate documentation of PK/UQ backing indexes as if they were explicit SQLAlchemy `Index` objects.

## View entries

The five baseline current views additionally describe:

```text
base relations
predicate contract
CHECK OPTION
automatically-updatable posture
runtime DML surface
SQLAlchemy Core handle
```

They are not ORM row entities.

## Routine entries

The 14 baseline integrity routines additionally describe:

```text
routine kind
language
security mode
volatility
parallel safety
direct runtime EXECUTE posture
```

Trigger attachments refer to the exact routine by schema-qualified name.

## Security

Dictionary security metadata is grant-oriented, not a vague writable/readable boolean.

Each expected grant contains:

```text
grantee
privilege
columns
grant_option
```

This can represent DB-U21 column-level UPDATE and view-specific DML truth without broadening it into table-level CRUD.

## Proof metadata

Object entries contain proof targets:

```text
obligations
test_refs
staged_evidence
```

Do not store mutable outcome flags such as `tests_passed=true` inside current object metadata. Actual PASS/FAIL belongs to test/CI/evidence records.

## Materialization rule

A real structural database change is incomplete unless all affected Dictionary entries are created/updated in the same reviewed change.

First materialization follows the frozen DAG:

```text
CP6-M01  +16 table entries
CP6-M02  +6 table entries
CP6-M03  +15 table entries
CP6-M04  +26 table entries
CP6-M05  +5 view +13 routine entries +66 trigger registrations
CP6-M06  +5 table +1 routine entry +9 trigger registrations
CP6-M07   no new standalone entries; reconcile/activate exact ACL values
```

Hard boundary:

```text
no real DANTE object
→ no object-specific Dictionary entry pretending it exists
```

Therefore CP6-03 creates only this readiness contract. The 87 standalone object entries are CP6-04 materialization outputs.

## Schema evolution

`object-v1.schema.json` and `scope-v1.schema.json` are versioned contracts.

Changing their meaning is a reviewed Dictionary schema evolution. Existing object files must not be silently reinterpreted under incompatible semantics.

A later schema version should be introduced explicitly and migrated/reconciled rather than modifying historical meaning by convention.

## Validation target

CP6-04/05 tooling must be able to detect at minimum:

```text
invalid JSON/schema
missing real object entry
stale object entry
column/type/nullability drift
PK/FK/UQ/CK drift
index drift
trigger drift
view drift
routine drift
owner/ACL drift
SQLAlchemy mapping drift
Alembic/head traceability drift
scope-count mismatch
extension-owned false positives
```

The exact Python validator dependency/implementation is not selected by this readiness checkpoint.