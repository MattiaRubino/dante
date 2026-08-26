# DANTE Database Dictionary

**Status:** CURRENT / MATERIALIZED / CP6 CLOSED  
**Schema version:** 1  
**Serialization:** JSON  
**Structural validation dialect:** JSON Schema Draft 2020-12  
**Current materialization:** CP6-M01..M07 complete; PostgreSQL 18.6; Alembic `20260826_08`  

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

## Current materialized shape

```text
dictionary/
├── README.md
├── scope.json
├── schema/
│   ├── object-v1.schema.json
│   └── scope-v1.schema.json
├── tables/       # 68 entries
├── views/        # 5 entries
└── routines/     # 14 entries
```

Object directories exist because real PostgreSQL objects now exist. Empty ceremonial object directories remain forbidden.

## Current baseline entry and embedded-object counts

The current DANTE-owned Dictionary contains exactly:

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

These values are both the expected baseline and the current materialized values in `scope.json`.

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

The business/control schema contract materialized by CP6 and governed by the current Database System of Record.

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

`expected_baseline` is the current baseline target. `current_materialization` records the actually materialized Dictionary/schema stage.

Lifecycle statuses remain:

```text
readiness_only
→ no CP6 object entries/materialized counts yet

materializing
→ one accepted CP6-M01..M07 prefix is being materialized

materialized
→ exact CP6-M01..M07 completion and final 68/5/14/87 + 75/95 + 68/120 counts
```

The current file is in the final state:

```text
status = materialized
completed_stages = CP6-M01..CP6-M07
standalone_entries = 68 tables + 5 views + 14 routines = 87
embedded_objects = 75 triggers + 95 physical indexes
constraints = 68 FKs + 120 CHECKs
```

`completed_stages` must always be a valid ordered prefix of the frozen migration DAG. JSON Schema bounds values; the DANTE semantic validator proves prefix/order/count coherence.

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

Baseline physical table properties reconcile as applicable to:

```text
persistence        permanent
access_method      heap
partitioned        false
row_security       false
force_row_security false
replica_identity   default
reloptions         [] unless a reviewed evolution says otherwise
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

The five baseline current views describe:

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

The views are not ORM row entities.

## Routine entries

The 14 baseline integrity routines describe:

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

Baseline trigger functions are `() → trigger`, `plpgsql`, `SECURITY INVOKER`, `VOLATILE`, `PARALLEL UNSAFE`, non-leakproof, with fixed `pg_catalog,dante,pg_temp` search path. `pg_temp` is explicitly last by the accepted object-hijack hardening contract.

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

The baseline reconciles to 75 exact enabled attachments: 18 ordinary/immediate and 57 deferred constraint triggers.

## Security

Dictionary security metadata is grant-oriented, not a vague writable/readable boolean.

Each expected grant contains:

```text
grantee
privilege
columns
grant_option
```

This represents column-level UPDATE and view-specific DML truth without broadening it into table-level CRUD.

Routine entries reconcile exact execution-search-path security. Role-membership topology, owner password posture and credential/SCRAM provisioning remain technical-foundation proof rather than standalone business Dictionary entries.

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
routine security/search_path facts reconcile to the accepted baseline
Dictionary ↔ SQLAlchemy ↔ Alembic ↔ PostgreSQL reconciliation
extension-owned objects do not become false DANTE drift
```

This validator is repository/test tooling, not a new semantic authority.

## Materialization and same-change rule

A real structural database change is incomplete unless all affected Dictionary entries are created/updated in the same reviewed change.

The original CP6 materialization followed the frozen DAG:

```text
CP6-M01  +16 table entries
CP6-M02  +6 table entries
CP6-M03  +15 table entries
CP6-M04  +26 table entries
CP6-M05  +5 view +13 routine entries +66 trigger registrations
CP6-M06  +5 table +1 routine entry +9 trigger registrations
CP6-M07   no new standalone entries; reconcile/activate exact ACL values
```

That sequence is now complete. Later structural evolution uses normal reviewed forward migrations plus the same-change Dictionary rule; it does not reopen CP6.

Hard boundary remains:

```text
no real DANTE object
→ no object-specific Dictionary entry pretending it exists
```

The converse is now also current truth:

```text
real baseline object
→ matching current Dictionary entry required
```

## Schema evolution

`object-v1.schema.json` and `scope-v1.schema.json` are versioned contracts.

The pre-materialization Part-16 and Part-18 changes hardened v1 before the first object-entry baseline was accepted. That history remains recoverable in Git and CP6 evidence; it is no longer the current operational state of this README.

Now that the v1 baseline is materialized, incompatible meaning changes require an explicit later Dictionary schema version/migration rather than silent reinterpretation.

## Validation target

Current and future database QA must detect at minimum:

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
routine signature/property/search_path drift
physical table persistence/RLS/partitioning drift
owner/ACL drift
SQLAlchemy mapping drift
Alembic/head traceability drift
scope-count/stage mismatch
extension-owned false positives
```

## CP6 final acceptance

The materialized v1 Dictionary was included in CP6-05 whole-database reconciliation and final direct QA. Final closure verified:

```text
Dictionary JSON-Schema validation       PASS
Dictionary internal integrity           PASS
Dictionary ↔ SQLAlchemy reconciliation  PASS
Dictionary ↔ Alembic reconciliation     PASS
Dictionary ↔ live PostgreSQL            PASS
final counts 68/5/14/87 + 75/95/68/120 PASS
```

See `docs/development/backend-cp6-05-whole-database-qa.md` for the retained acceptance record.
