# DANTE Database Dictionary

**Status:** CP6-03 READINESS FOUNDATION / HARDENED BY PART 16 / OBJECT ENTRIES NOT YET MATERIALIZED  
**Schema version:** 1  
**Serialization:** JSON  
**Structural validation dialect:** JSON Schema Draft 2020-12  
**Cross-file validation:** DANTE semantic Dictionary validator required before Gate-03 materialization is accepted  

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

## Final baseline entry and embedded-object counts

After complete CP6-04 materialization the expected DANTE-owned Dictionary contains:

```text
68 table entries
5 view entries
14 routine entries
------------------
87 standalone entries

75 trigger attachments
95 physical indexes
68 foreign keys
120 CHECK constraints
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

The 14 integrity routines remain standalone entries because they are independently owned PostgreSQL objects with their own signature/security/ACL properties and may have multiple trigger attachments.

## Ownership spaces

`scope.json` distinguishes three spaces.

### DANTE-owned

The business/control schema contract governed by Parts 1–16.

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

The current foundation extension registry is a strict keyed object with exactly:

```text
postgis
vector
pg_trgm
unaccent
pg_stat_statements
```

Objects internally created/owned by those extensions are not promoted into DANTE object entries merely because PostgreSQL introspection exposes them.

## Materialization lifecycle in scope.json

`expected_baseline` is immutable target truth for this baseline. `current_materialization` records the actually materialized Dictionary/schema stage.

Statuses:

```text
readiness_only
→ no CP6 object entries/materialized counts yet

materializing
→ one accepted CP6-M01..M07 prefix is being materialized

materialized
→ exact CP6-M01..M07 completion and final 68/5/14/87 + 75/95 + 68/120 counts
```

`completed_stages` must be a valid ordered prefix of the frozen migration DAG. JSON Schema bounds values; the DANTE semantic validator proves prefix/order/count coherence.

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

The schema is intentionally strict (`additionalProperties: false` throughout governed shapes) so accidental new metadata fields require reviewed Dictionary-schema evolution rather than silently becoming convention.

## Structural truth and semantic truth

### Mechanically reconcilable

These facts MUST be verified automatically against SQLAlchemy/Alembic/PostgreSQL where applicable:

```text
object name/type
columns/types/nullability/defaults
PK/FK/UQ/CK
constraint deferrability/enforcement/validation
indexes and valid/ready/live state
trigger physical properties
view definition/security/default/CHECK OPTION
routine signature/properties
relation persistence/access method/RLS/partitioning/replica identity
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

A table entry includes exact columns, physical relation properties and embedded:

```text
primary key
foreign keys
unique constraints
check constraints
indexes
trigger attachments
```

Baseline physical table properties are expected to reconcile as applicable to:

```text
persistence       permanent
access_method     heap
partitioned       false
row_security      false
force_row_security false
replica_identity  default
reloptions        [] unless a reviewed evolution says otherwise
```

Foreign-key metadata includes reference-family/cardinality/semantic reason plus MATCH / update-delete action / deferrability / enforcement / validation.

CHECK metadata includes exact expression contract plus enforcement/validation/NO INHERIT state.

Index metadata identifies whether the physical index originates from:

```text
primary_key
unique_constraint
explicit_index
```

and records PostgreSQL valid/ready/live state. This prevents duplicate documentation of PK/UQ backing indexes as if they were explicit SQLAlchemy `Index` objects.

## View entries

The five baseline current views additionally describe:

```text
base relations
exact predicate contract
CHECK OPTION
automatically-updatable posture
runtime DML surface
SQLAlchemy Core handle
security_invoker
security_barrier
view-column defaults
```

Part 16 freezes the exact facet-code default required for INSERT through each view. The views are not ORM row entities.

## Routine entries

The 14 baseline integrity routines additionally describe:

```text
routine kind
language
argument types
return type
security mode
volatility
parallel safety
leakproof posture
function search_path
direct runtime EXECUTE posture
```

Baseline trigger functions are `() → trigger`, `plpgsql`, `SECURITY INVOKER`, `VOLATILE`, `PARALLEL UNSAFE`, non-leakproof, with fixed `pg_catalog,dante` search path.

## Trigger attachments

Each table-owned trigger record includes:

```text
exact name
routine reference
events
timing
ROW/STATEMENT orientation
constraint-trigger flag
deferrability / initially-deferred
enabled mode
UPDATE OF column set
WHEN condition
arguments
invariant role/reason
```

The baseline must reconcile to 75 exact enabled attachments: 18 ordinary/immediate and 57 deferred constraint triggers.

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

## Two-level validation contract

JSON Schema is necessary but intentionally not treated as sufficient.

### Level 1 — Draft 2020-12 structural validation

Proves each JSON document has the governed shape, types, enums, required fields and type-specific object shape.

### Level 2 — DANTE semantic/cross-file validation

Must prove at least:

```text
unique object keys + exact filename/name agreement
exact extension key set
unique columns and embedded object identifiers in applicable scope
all local columns referenced by keys/FKs/indexes/grants/triggers exist
all FK targets and target columns resolve
all trigger routine references resolve
trigger/routine signatures are compatible
object type ↔ SQLAlchemy mode is correct
stage prefix/counts reconcile to CP6-M01..M07
68 tables / 5 views / 14 routines / 87 standalone entries
75 triggers / 95 physical indexes / 68 FKs / 120 CHECKs
Dictionary ↔ SQLAlchemy ↔ Alembic ↔ PostgreSQL reconciliation
extension-owned objects do not become false DANTE drift
```

This validator is repository/test tooling, not a new semantic authority.

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

Therefore CP6-03 still contains no `tables/`, `views/` or `routines/` entries. The 87 standalone object entries are CP6-04 materialization outputs.

## Schema evolution

`object-v1.schema.json` and `scope-v1.schema.json` are versioned contracts.

This Part-16 edit is a **pre-first-entry hardening of v1**: no object-specific v1 record existed yet, so no historical object entry is being reinterpreted or migrated.

After first materialization, incompatible meaning changes require an explicit later Dictionary schema version/migration rather than silent reinterpretation.

## Validation target

CP6-04/05 tooling must detect at minimum:

```text
invalid JSON/schema
semantic/cross-file Dictionary inconsistency
missing real object entry
stale object entry
column/type/nullability/default drift
PK/FK/UQ/CK drift or non-enforced/unvalidated state
index drift or invalid/not-ready/not-live state
trigger attachment/property drift
view definition/security/default drift
routine signature/property drift
physical table persistence/RLS/partitioning drift
owner/ACL drift
SQLAlchemy mapping drift
Alembic/head traceability drift
scope-count/stage mismatch
extension-owned false positives
```

The exact validator implementation is selected in CP6-04/05 as test/repository tooling; the contract itself is now frozen by Part 16.
