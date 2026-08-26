<!-- DANTE-CANONICAL-CONTINUATION document="dante-postgresql-database.md" follows="dante-postgresql-database-part-14.md" -->

# DANTE PostgreSQL Database Architecture & Reference — Part 15

**Status:** CP6-03 ACTIVE / CANONICAL CONTINUATION / DATABASE DICTIONARY READINESS FROZEN  
**Scope:** section 50 onward  
**Authority:** this file is one physical part of the single canonical Database Architecture & Reference and MUST be consumed together with Parts 1–14  
**PRE-SCOPE for this readiness freeze:** `db4dbd762a9f3451ce55f61323807549bab3e32c`  
**Current PostgreSQL architecture:** PostgreSQL 18 major family / current technical patch 18.6  
**CP6-04 real database materialization:** NOT STARTED / NOT AUTHORIZED  

Parts 9–14 already freeze the object inventory, naming, index matrix, privilege matrix, migration/materialization DAG and SQLAlchemy mapping plan. This continuation freezes the repository-native machine-readable Database Dictionary contract that CP6-04 must populate together with the real objects it materializes.

No table/view/routine dictionary entry for a not-yet-materialized DANTE business object is created by this checkpoint. No Python validator, migration, SQLAlchemy mapping or PostgreSQL business object is created here.

---

## 50. Database Dictionary Readiness — FROZEN

### 50.1 Purpose

The Database Dictionary is the machine-readable semantic/structural companion to the human-readable Database Architecture & Reference.

It MUST support automatic reconciliation without becoming a second source of semantic truth.

The accepted authority split is:

```text
Architecture & Reference
→ human-readable database meaning and rationale

Database Dictionary
→ machine-readable current object metadata + semantic traceability

SQLAlchemy MetaData
→ application mapping of tables/constraints/indexes

Alembic
→ deployed application-schema evolution

real PostgreSQL introspection
→ observed materialized database

direct tests
→ executable proof
```

A mismatch between these representations is a defect to investigate.

### 50.2 Serialization and schema dialect

Canonical source format:

```text
JSON
UTF-8
one object entry per standalone DANTE-owned table/view/routine
```

Validation contract:

```text
JSON Schema
Draft 2020-12 dialect
schema version = 1
```

JSON is selected because the Dictionary is primarily machine-consumed, requires deterministic scalar typing, is available through Python's standard library, and does not require introducing a YAML/TOML dependency merely for metadata authoring.

The schema dialect is frozen independently from the eventual Python validator implementation. CP6-04/05 may choose a maintained validator library, but the data contract itself remains Draft 2020-12 unless a later reviewed dictionary-schema migration changes it.

### 50.3 Repository topology

Readiness foundation created by this checkpoint:

```text
docs/database/dictionary/
├── README.md
├── scope.json
└── schema/
    ├── object-v1.schema.json
    └── scope-v1.schema.json
```

Object directories are intentionally absent until they contain real entries.

CP6-04 will create them only with actual content:

```text
docs/database/dictionary/tables/
docs/database/dictionary/views/
docs/database/dictionary/routines/
```

Empty ceremonial object directories are forbidden.

### 50.4 Standalone-entry inventory

The final materialized baseline requires exactly:

```text
TABLE ENTRY FILES       68
VIEW ENTRY FILES         5
ROUTINE ENTRY FILES     14
--------------------------
STANDALONE ENTRIES      87
```

Stable object keys are:

```text
table:dante.<table_name>
view:dante.<view_name>
routine:dante.<routine_name>
```

File names use the exact PostgreSQL object name plus `.json` inside the applicable object-type directory.

Examples after materialization:

```text
dictionary/tables/person.json
dictionary/views/schedule_current_placement.json
dictionary/routines/enforce_native_address_owner.json
```

### 50.5 Embedded object accounting

Not every PostgreSQL object receives a standalone file.

The following objects are represented inside the owning table entry:

```text
primary-key constraints
foreign-key constraints
unique constraints
check constraints
indexes
trigger attachments
```

Baseline embedded-object totals remain:

```text
PHYSICAL INDEXES        95
TRIGGER ATTACHMENTS     75
```

This is deliberate normalization of documentation ownership, not omission.

A trigger attachment is table-owned metadata because its event/timing/deferrability and invariant effect are meaningful only in relation to the table where it fires. The referenced integrity routine remains a standalone routine entry because the routine is an independently owned PostgreSQL object with its own owner/security/ACL contract and may serve multiple attachments.

No standalone trigger/index/constraint micro-file family is introduced in the CP6 baseline.

### 50.6 Ownership-space accounting

`scope.json` is the global machine-readable scope authority.

It MUST distinguish:

#### DANTE-owned objects

```text
68 tables
5 views
14 routines
75 trigger attachments
95 physical indexes
```

#### Technical foundation

```text
dante.alembic_version
roles:
  dante_owner
  dante_migrator
  dante_runtime
```

`dante.alembic_version` is real PostgreSQL schema state but is not a DANTE semantic/business dictionary object and therefore is excluded from the 68-table / 87-entry DANTE-owned counts.

#### Extension-owned capability surface

```text
postgis
vector
pg_trgm
unaccent
pg_stat_statements
```

Objects internally owned by those extensions are excluded from DANTE standalone entries unless a later DANTE-owned object explicitly consumes an extension capability in a way that must be documented on that DANTE object.

Hard rule:

```text
visible through PostgreSQL introspection
!= automatically DANTE-owned
```

This distinction is mandatory for drift tooling so extension support objects do not become false "undocumented DANTE object" failures.

### 50.7 Common object-entry contract

Every standalone object entry contains these ten top-level blocks:

```text
1  object
2  purpose
3  classification
4  semantic_traceability
5  implementation
6  structure
7  state_history
8  lifecycle
9  security
10 proof
```

No required semantic field may disappear merely because PostgreSQL or SQLAlchemy cannot generate it.

### 50.8 Object identity

Every object entry records:

```text
object.key
object.type
object.schema
object.name
object.ownership_class
```

Baseline values are bounded to:

```text
schema            dante
ownership_class   dante_owned
object.type       table | view | routine
```

Dictionary identity is descriptive metadata. It does not create a new database identifier/address family.

### 50.9 Purpose and classification

Human-authored fields:

```text
purpose
classification.persistence_role
classification.canonicality
classification.family
```

These explain why an object exists and what role it plays.

They MUST preserve distinctions such as:

```text
identity != state/history
control != semantic owner
capability surface != base table
integrity routine != business workflow
canonical != provider/derived
```

### 50.10 Semantic traceability

Every entry carries bounded arrays for:

```text
authority_sources
domain_concepts
logical_families
reference_families
material_facets
```

The four reference-family values remain exactly:

```text
NativeRef
ScopedRecordRef
MaterialStateRef
ExternalRef
```

An empty array is valid where a category is genuinely not applicable; omission of the category is not.

### 50.11 Implementation traceability

Every entry records:

```text
introducing_stage          CP6-M01..CP6-M07
actual Alembic revision    null until materialization; exact revision afterward
SQLAlchemy mode
SQLAlchemy module
SQLAlchemy symbol
runtime ACL stage          CP6-M07
```

SQLAlchemy modes are exactly:

```text
orm_row
core_view
none
```

The baseline mapping-plan consequences are:

```text
68 table entries   → orm_row
5 view entries     → core_view
14 routine entries → none
```

The Dictionary MUST NOT pretend that routines or views have ORM row identity when Part 14 explicitly rejected that shape.

### 50.12 Column contract

Each table/view column record can state:

```text
name
postgres_type
nullable
default.kind        none | application | server
default.expression
meaning
semantic_type
value_contract
```

`meaning`, `semantic_type` and `value_contract` are semantic documentation, not generated DDL commentary.

Example distinction:

```text
postgres_type    uuid
semantic_type    NativeRef
```

prevents the machine-readable catalog from collapsing all UUID columns into one semantic identity family.

### 50.13 Keys and foreign references

Primary-key metadata records exact name + ordered columns.

Each FK records:

```text
name
ordered local columns
target schema/table/columns
ON DELETE
ON UPDATE
deferrability / initial mode
reference family where applicable
cardinality
semantic reason
```

The FK structure therefore remains machine-verifiable while preserving why the reference exists.

A heterogeneous NativeRef consumer may physically reference `native_address`; its dictionary record MUST still state the bounded semantic target-family contract rather than describing it as an unconstrained generic UUID relation.

### 50.14 Unique/check constraints

Unique and check constraints remain embedded in their table entry.

Machine-verifiable fields include exact names/columns/expression contract.

Human-authored `reason` explains the invariant.

A generated SQL expression may supplement an expression contract in later tooling, but generated SQL MUST NOT replace the semantic reason.

### 50.15 Index contract

All 95 physical baseline indexes are represented in table entries.

Every index can state:

```text
name
method
unique
keys / expressions
predicate
INCLUDE columns
source
reason
```

`source` is exactly:

```text
primary_key
unique_constraint
explicit_index
```

This preserves the Part-14 reconciliation:

```text
68 PK-backed
2 UNIQUE-backed
25 explicit SQLAlchemy Index objects
= 95 physical PostgreSQL indexes
```

The Dictionary MUST NOT create fake explicit-index records that duplicate backing indexes.

### 50.16 Trigger attachment contract

Every trigger attachment is embedded under its owning table with:

```text
exact name
routine reference
events
timing
constraint-trigger flag
deferrability
initially-deferred flag
integrity-role identifier/description
reason
```

The final baseline must reconcile to:

```text
75 attachments
18 ordinary/immediate
57 deferred constraint triggers
```

A trigger record references the exact standalone routine object via `dante.<routine_name>`.

### 50.17 View contract

A view entry additionally captures:

```text
base relations
predicate contract
CHECK OPTION
whether PostgreSQL treats it as automatically updatable
runtime DML surface
SQLAlchemy Core symbol
```

For the five current views, the accepted baseline remains:

```text
ordinary view
filtered to one exact facet
WITH LOCAL CHECK OPTION
no INSTEAD OF trigger
Core-only SQLAlchemy handle
```

### 50.18 Routine contract

A routine entry additionally records PostgreSQL routine properties required for operational review, including:

```text
function/procedure kind
language
SECURITY INVOKER/DEFINER
volatility
parallel safety
direct runtime EXECUTE posture
```

The CP6 baseline integrity routines remain `SECURITY INVOKER` with no direct `dante_runtime` execution grant under DB-U21.

### 50.19 Material state/history, lifecycle and security

Every entry includes the categories even when a field is not applicable:

```text
state_history
  material_state_behavior
  current_binding
  chronology
  immutability_policy

lifecycle
  retention
  redaction
  retirement_tombstone
  delete_behavior

security
  owner_role
  default_deny_non_owner
  expected_grants
```

Security grants record exact grantee, privilege, optional column list and grant-option posture.

A boolean such as `runtime_can_write` is explicitly insufficient because DB-U21 contains column-level UPDATE and view-specific DML surfaces.

### 50.20 Proof traceability

The Dictionary records proof targets, not mutable CI outcomes.

Per entry:

```text
obligations
test_refs
staged_evidence
```

Do NOT persist fields such as:

```text
tests_passed = true
last_ci_pass = ...
```

inside object entries.

Current PASS/FAIL evidence belongs to CI/evidence records, not the current structural Dictionary.

### 50.21 Mechanically reconciled facts versus human semantic facts

The Dictionary deliberately contains both classes.

Mechanically reconcilable facts include:

```text
object name/type
columns/types/nullability
PK/FK/UQ/CK names and structure
indexes
view structure
routine properties
trigger attachments
object owner
ACL
Alembic revision
SQLAlchemy mapping
```

These SHOULD be compared against SQLAlchemy/Alembic/PostgreSQL in CP6-04/05.

Human-authored semantic facts include:

```text
why object exists
meaning of a column/reference
why a constraint/index exists
semantic owner/facet
current/history interpretation
lifecycle meaning
canonicality boundary
proof rationale
```

These MUST NOT be regenerated from DDL and silently overwritten.

### 50.22 Same-change rule during CP6-04

A materialization batch is incomplete if it creates or structurally changes a DANTE-owned object without updating its Dictionary entry in the same reviewed change.

The first population follows the already-frozen DAG:

```text
M1  +16 table entries
M2  +6 table entries
M3  +15 table entries
M4  +26 table entries
M5  +5 view entries +13 routine entries +66 trigger registrations
M6  +5 table entries +1 routine entry +9 trigger registrations
M7   0 new standalone entries; final ACL values activated/reconciled
```

Final result:

```text
68 tables
5 views
14 routines
75 embedded triggers
95 embedded physical indexes
87 standalone entries
```

### 50.23 Object-entry creation boundary

Readiness does not equal materialization.

Hard rule:

```text
no real DANTE object
→ no object-specific Dictionary entry pretending it exists
```

Therefore this CP6-03 checkpoint creates only the Dictionary contract/schema/scope files.

The 68 table entries, five view entries and fourteen routine entries are created during CP6-04 alongside the actual object materialization stages.

This preserves truthful traceability fields such as the real Alembic revision and avoids a speculative catalog of unimplemented objects.

### 50.24 Validator/tooling boundary

This checkpoint freezes the data contract, not a validator implementation.

CP6-04/05 must provide automated checks sufficient to detect at least:

```text
invalid Dictionary JSON/schema
missing real DANTE object entry
stale Dictionary object entry
object type/name mismatch
column/type/nullability drift
PK/FK/UQ/CK drift
index drift
trigger attachment drift
view drift
routine property drift
owner/ACL drift
SQLAlchemy mapping drift
Alembic revision/head mismatch where applicable
scope-count mismatch
extension-owned false positives
```

No new runtime dependency is required merely by this readiness checkpoint.

### 50.25 Negative Dictionary rules

Forbidden baseline patterns:

```text
one giant untyped catalog JSON blob
YAML implicit typing as machine authority
Dictionary as generated DDL dump only
one file per trigger/index/constraint merely for ceremony
extension-owned PostgreSQL objects promoted to DANTE ownership
technical alembic_version promoted to semantic table
missing semantic meaning because a field is not introspectable
manual structural fact silently disagreeing with PostgreSQL
mutable CI PASS flags stored as object truth
empty tables/views/routines directories before entries exist
object-specific entries before real materialization
```

### 50.26 Readiness acceptance

Database Dictionary readiness is PASS when:

```text
serialization selected                        PASS
schema dialect/version selected               PASS
repository topology selected                  PASS
scope ownership/count contract selected       PASS
standalone object-entry policy selected       PASS
embedded trigger/index/constraint policy      PASS
common entry contract complete                PASS
Table/View/Routine specialization complete    PASS
semantic vs structural ownership explicit     PASS
M1..M7 population order explicit              PASS
CP6-04 same-change rule explicit              PASS
CP6-05 drift obligations explicit             PASS
speculative object entries                    0
new business DDL                              0
new SQLAlchemy business mappings              0
```

---

## 51. Current continuation state

The canonical Database Architecture & Reference is now Parts 1–15 consumed together.

Current checkpoint state:

```text
FINAL ACTUAL POSTGRESQL OBJECT INVENTORY    FROZEN
DB-U08 FINAL NAMING                         CLOSED
DB-U15 FINAL INDEX MATRIX                   CLOSED
DB-U21 FINAL PRIVILEGE MATRIX               CLOSED
GLOBAL DB-U OPEN                            0
MIGRATION / MATERIALIZATION DAG             FROZEN
SQLALCHEMY MAPPING PLAN                     FROZEN
DATABASE DICTIONARY READINESS               READY / PASS

NEXT
DIRECT POSTGRESQL PROOF / TEST PLAN

SECOND FULL TOMBSTONE AUDIT                 NOT YET RUN
GATE 03                                     NOT YET EARNED
CP6-04                                      NOT STARTED / NOT AUTHORIZED
```

Part 15 supersedes older CURRENT/resume statements only where they say Database Dictionary readiness is pending/next or imply object-specific Dictionary entries should exist before the corresponding database objects are materialized.

Historical evidence and all Parts 1–14 remain canonical.