# DANTE Database Dictionary

**Status:** CURRENT / MATERIALIZED / CP6 BASELINE CLOSED / POST-CP6 EVOLUTION ACTIVE  
**Schema version:** 1  
**Serialization:** JSON  
**Structural validation dialect:** JSON Schema Draft 2020-12  
**PostgreSQL:** 18.6  
**Current branch Alembic head:** `20260827_10`  
**Frozen CP6 head:** `20260826_08`  

## Purpose

This directory is the machine-readable companion to the human-readable DANTE Database Architecture & Reference.

It does not replace Domain, Logical, Physical, the PostgreSQL Persistence Constitution, Alembic, SQLAlchemy or real PostgreSQL introspection. It provides one structured **current** metadata surface that those authorities can be reconciled against while preserving frozen historical acceptance baselines separately.

The long-lived consistency target is:

```text
Current Database Architecture & Reference
≈ current Database Dictionary
≈ current SQLAlchemy MetaData / mappings
≈ current Alembic head
≈ current real PostgreSQL schema
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
├── tables/       # 72 current entries
├── views/        # 5 current entries
└── routines/     # 15 current entries
```

Object directories exist because real PostgreSQL objects are represented by the current branch schema. Empty ceremonial object directories remain forbidden.

## Frozen baseline vs current materialization

`scope.json` deliberately separates two facts that were identical at CP6 closure but diverge after normal product evolution.

### `expected_baseline`

Immutable CP6 closure benchmark at `20260826_08`:

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

### `current_materialization`

Current `feature/access-auth` inventory after M3 migrations `20260827_09` and `20260827_10`:

```text
72 table entries
5 view entries
15 routine entries
------------------
92 standalone entries

75 trigger attachments
104 physical indexes
71 foreign keys
137 CHECK constraints
```

Post-CP6 schema growth **must not rewrite the CP6 benchmark** merely to keep baseline and current counts equal.

`completed_stages` continues to record the frozen CP6 materialization sequence because those stages describe how the baseline was established. Later object provenance is recorded on each object through `implementation.introducing_stage` and `implementation.alembic_revision`.

Object entry keys remain stable and typed:

```text
table:dante.<name>
view:dante.<name>
routine:dante.<name>
```

The exact PostgreSQL object name is also the JSON filename in the applicable directory.

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

Integrity/security routines remain standalone entries because they are independently owned PostgreSQL objects with their own signature/security/ACL properties and may have multiple trigger attachments or expose a deliberately narrow callable capability.

## Ownership spaces

`scope.json` distinguishes three spaces.

### DANTE-owned

Current business/control/security objects governed by DANTE migrations and the current Database System of Record. This now includes both the frozen CP6 object set and reviewed post-CP6 product evolution such as the M3 Access/Auth tables and bounded Account-security locking routine.

### Technical foundation

Includes:

```text
dante.alembic_version
dante_owner
dante_migrator
dante_runtime
dante_observer
```

`dante.alembic_version` is not a DANTE semantic/business table entry.

`dante_observer` is a technical, statistics-only collector login. It has no
`USAGE` on `dante` or `public`, no DANTE table/view/routine/sequence/type
privileges and no SQLAlchemy mapping because a PostgreSQL role is not an
application persistence object. Its only inherited capability is
`pg_read_all_stats`; collector configuration does not enable the
`pg_stat_statements` collector, so query IDs and SQL text are excluded. A
fail-closed remote-write allowlist additionally drops per-object and future
unreviewed metric families. The exact role/Blueprint/live PostgreSQL proof is
owned by provisioning plus the observability contract tests, not by a fake
Dictionary object entry.

### Extension-owned

The current foundation extension registry remains exactly:

```text
postgis
vector
pg_trgm
unaccent
pg_stat_statements
```

Objects internally created/owned by those extensions are not promoted into DANTE object entries merely because PostgreSQL introspection exposes them.

## Materialization lifecycle in `scope.json`

Lifecycle statuses remain:

```text
readiness_only
→ no materialized DANTE object inventory yet

materializing
→ accepted baseline materialization is in progress

materialized
→ the frozen CP6 materialization completed and the current inventory is fully represented
```

For `materialized`, `completed_stages` remains the exact completed CP6 list:

```text
CP6-M01 .. CP6-M07
```

Current inventory counts are no longer capped to the CP6 totals. They are non-negative evolving values that must reconcile mechanically to current Dictionary entries, mappings and PostgreSQL.

This distinction lets v1 survive normal forward product evolution without pretending later objects were introduced by CP6.

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

Object types remain exactly:

```text
table
view
routine
```

The schema remains intentionally strict (`additionalProperties: false` throughout governed shapes) so accidental metadata fields require reviewed Dictionary-schema evolution rather than silently becoming convention.

### Post-CP6 provenance fields

`object-v1.schema.json` no longer hardcodes:

```text
introducing_stage = CP6-M01..M07 only
runtime_acl_stage = CP6-M07 only
```

Both fields accept governed stage identifiers such as:

```text
CP6-M03
CP6-M07
M3-A
```

This is a compatible generalization of provenance metadata, not permission to rewrite existing CP6 entries. Existing CP6 object entries retain their historical stage values.

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
current object/count inventory
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

Generated DDL must not overwrite human semantic fields.

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

Normal physical table properties reconcile as applicable to:

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

Index metadata identifies whether a physical index originates from:

```text
primary_key
unique_constraint
explicit_index
```

and records PostgreSQL valid/ready/live state. This prevents duplicate documentation of PK/UQ backing indexes as if they were explicit SQLAlchemy `Index` objects.

## View entries

Current views describe:

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

Views are not ORM row entities.

## Routine entries

Current routine entries describe:

```text
routine kind
language
argument types
return type
security mode
volatility
parallel safety
leakproof posture
function_search_path
direct runtime EXECUTE posture
```

The frozen CP6 trigger-function baseline remains `() → trigger`, `plpgsql`, `SECURITY INVOKER`, `VOLATILE`, `PARALLEL UNSAFE`, non-leakproof, with fixed `pg_catalog,dante,pg_temp` search path. `pg_temp` remains explicitly last by the accepted object-hijack hardening contract.

Post-CP6 routines are not forced to impersonate that CP6 trigger-function shape. M3 migration `20260827_10` introduces `dante.acquire_account_security_lock(uuid)`, a `SECURITY DEFINER` bounded security capability owned by `dante_owner`, with the same trusted exact search path, `VOLATILE`, `PARALLEL UNSAFE`, non-leakproof posture, no PUBLIC/migrator EXECUTE and direct `dante_runtime` EXECUTE only.

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

M3 adds no triggers, so the current branch remains at the 75 CP6 attachments unless a later reviewed evolution changes that inventory.

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

Routine entries reconcile exact execution/search-path security. Role-membership topology, owner password posture and credential/SCRAM provisioning remain technical-foundation proof rather than standalone business Dictionary entries.

M3 uses the same model for least-privilege Auth persistence and the bounded Account-security routine: new object entries declare exact runtime table/column/function grants and `test_current_catalog.py` directly reconciles them against PostgreSQL.

## Proof metadata

Object entries contain proof targets:

```text
obligations
test_refs
staged_evidence
```

Do not store mutable outcome flags such as `tests_passed=true` inside current object metadata. Actual PASS/FAIL belongs to test/CI/evidence records.

M3 object entries name their direct proof targets; those targets have now executed successfully at the current backend checkpoint, while the Dictionary itself remains outcome-neutral metadata.

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
frozen CP6 completed-stage record remains valid
current scope counts reconcile to the current entry set
current Dictionary ↔ SQLAlchemy ↔ Alembic ↔ PostgreSQL reconciliation
routine security/search_path facts reconcile where applicable
technical role topology ↔ Blueprint ↔ provisioning ↔ live PostgreSQL reconciliation
extension-owned objects do not become false DANTE drift
```

At the current M3 backend head this means the current reconciliation target is:

```text
72 tables / 5 views / 15 routines / 92 standalone entries
75 triggers / 104 physical indexes / 71 FKs / 137 CHECKs
```

The frozen CP6 acceptance test independently proves its own historical `68/5/14/87 + 75/95 + 68/120` topology by migrating to revision `20260826_08`.

This validator/test tooling is not a new semantic authority.

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

That sequence remains complete and immutable as historical provenance.

M3 then introduces:

```text
20260827_09 / M3-A
+ account
+ email_identity
+ password_credential
+ auth_session
+ 9 physical indexes
+ 3 foreign keys
+ 17 CHECK constraints
+ exact runtime table/column ACL metadata

20260827_10 / M3 backend
+ acquire_account_security_lock(uuid)
+ exact SECURITY DEFINER owner/search-path/EXECUTE metadata
```

Hard boundary remains:

```text
no real DANTE object
→ no object-specific Dictionary entry pretending it exists
```

And current truth requires:

```text
real current DANTE object
→ matching current Dictionary entry required
```

## Schema evolution

`object-v1.schema.json` and `scope-v1.schema.json` are versioned contracts.

The CP6 pre-materialization changes hardened v1 before the first object-entry baseline was accepted. M3 proves that v1 also needs to support **ordinary forward evolution** after that baseline.

The M3 change generalizes only facts that were accidentally frozen to CP6 implementation chronology:

```text
introducing/runtime ACL stage vocabulary
current inventory upper bounds/materialized-count equality
```

It does not reinterpret the shape or meaning of the 87 CP6 entries and therefore does not require a v2 migration.

An actually incompatible metadata meaning/shape change still requires an explicit later Dictionary schema version/migration rather than silent reinterpretation.

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
scope-count mismatch
frozen-baseline mutation presented as current evolution
extension-owned false positives
```

## CP6 final acceptance and current proof boundary

The materialized v1 Dictionary baseline was included in CP6-05 whole-database reconciliation and final direct QA:

```text
Dictionary JSON-Schema validation       PASS at CP6
Dictionary internal integrity           PASS at CP6
Dictionary ↔ SQLAlchemy reconciliation  PASS at CP6
Dictionary ↔ Alembic reconciliation     PASS at CP6
Dictionary ↔ live PostgreSQL            PASS at CP6
final CP6 counts 68/5/14/87 + 75/95/68/120 PASS
```

Those facts remain historical evidence for revision `20260826_08`.

The current M3 Dictionary/database state has also been directly proved against disposable PostgreSQL 18.6 at Alembic `20260827_10`:

```text
current 72/5/15/92 inventory                                PASS
current Dictionary ↔ SQLAlchemy ↔ Alembic ↔ PostgreSQL      PASS
Auth table/column ACL                                       PASS
acquire_account_security_lock routine properties/ACL        PASS
runtime direct Account FOR UPDATE denied                    PASS
real transaction-scoped Account row lock                    PASS
real PostgreSQL marked suite                                PASS / 83 of 83
```

This current database PASS does not imply generated-client/Web/browser M3 closure.

See:

- `../access-auth.md` for the current Access/Auth database meaning;
- `../development/backend-cp6-05-whole-database-qa.md` for retained CP6 acceptance evidence.
