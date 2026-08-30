# DANTE Database Dictionary

**Status:** CURRENT / MATERIALIZED / CP6 BASELINE CLOSED / M5-A CURRENT MATERIALIZATION PROVEN  
**Schema version:** 1  
**Serialization:** JSON  
**Structural validation dialect:** JSON Schema Draft 2020-12  
**PostgreSQL:** 18.6  
**Current branch Alembic head:** `20260830_12`  
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
├── tables/       # 83 current entries
├── views/        # 5 current entries
└── routines/     # 15 current entries
```

Current standalone object total:

```text
83 tables
5 views
15 routines
-----------
103 standalone Dictionary entries
```

Object directories exist because real PostgreSQL objects are represented by the current branch schema. Empty ceremonial object directories remain forbidden.

---

## Frozen baseline vs current materialization

`scope.json` deliberately separates immutable historical closure benchmarks from current materialization.

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

Current accepted `feature/access-auth` inventory through M5-A revision `20260830_12`:

```text
83 table entries
5 view entries
15 routine entries
------------------
103 standalone entries

75 trigger attachments
156 physical indexes
85 foreign keys
233 CHECK constraints
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

---

## Current Access/Auth Dictionary evolution

M3 introduced:

```text
account
email_identity
password_credential
auth_session
acquire_account_security_lock(uuid)
```

M4 introduced:

```text
password_signup_challenge
password_recovery_challenge
```

M5-A introduced:

```text
external_identity
external_auth_transaction
external_link_challenge
external_signup_challenge
account_profile_bootstrap
apple_auth_grant
webauthn_account
passkey_credential
webauthn_challenge
```

M5-A also evolves current entries for:

```text
email_identity
→ recovery_restriction_code
→ recovery_restriction_observed_at
→ exact current ACL metadata

auth_session
→ composite exact ownership target used by WebAuthn challenge binding
```

M5-A physical implementation hardening is represented in current object metadata, including exact Apple issuer+subject binding, WebAuthn Account/session/userHandle ownership, passkey logical revocation, explicit `cose_algorithm`, backup-state implication and cleanup indexes.

---

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

---

## Ownership spaces

`scope.json` distinguishes three spaces.

### DANTE-owned

Current business/control/security objects governed by DANTE migrations and the current Database System of Record. This includes the frozen CP6 object set and reviewed post-CP6 Access/Auth evolution through M5-A.

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

The current foundation extension registry remains exactly:

```text
postgis
vector
pg_trgm
unaccent
pg_stat_statements
```

Objects internally created/owned by those extensions are not promoted into DANTE object entries merely because PostgreSQL introspection exposes them.

---

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

Current inventory counts are evolving values that must reconcile mechanically to current Dictionary entries, mappings and PostgreSQL.

---

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

Post-CP6 provenance fields accept governed stage identifiers such as:

```text
CP6-M03
CP6-M07
M3-A
M4
M5-A
```

Existing historical entries retain their actual introducing stage; later updates to constraints/ACL/current structure do not rewrite provenance.

---

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

---

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

and records PostgreSQL valid/ready/live state.

---

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

---

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

The frozen CP6 trigger-function baseline remains `() → trigger`, `plpgsql`, `SECURITY INVOKER`, `VOLATILE`, `PARALLEL UNSAFE`, non-leakproof, with fixed `pg_catalog,dante,pg_temp` search path.

`dante.acquire_account_security_lock(uuid)` remains the bounded post-CP6 `SECURITY DEFINER` capability owned by `dante_owner`, with trusted exact search path and direct `dante_runtime` EXECUTE only.

---

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

M3–M5-A add no triggers, so the current branch remains at the 75 CP6 attachments.

---

## Security

Dictionary security metadata is grant-oriented, not a vague writable/readable boolean.

Each expected grant contains:

```text
grantee
privilege
columns
grant_option
```

This represents column-level INSERT/UPDATE and view-specific DML truth without broadening it into table-level CRUD.

M5-A proof specifically requires that `email_identity` keeps column-scoped INSERT while adding the two new nullable recovery columns, and that UPDATE remains limited to the two recovery-restriction fields.

Durable ExternalIdentity/PasskeyCredential entries intentionally expose no runtime DELETE; logical revocation is represented in lifecycle/current-state metadata.

---

## Proof metadata

Object entries contain proof targets:

```text
obligations
test_refs
staged_evidence
```

Do not store mutable outcome flags such as `tests_passed=true` inside current object metadata. Actual PASS/FAIL belongs to test/CI/evidence records.

---

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
extension-owned objects do not become false DANTE drift
```

At the accepted M5-A backend head the current reconciliation target is:

```text
83 tables / 5 views / 15 routines / 103 standalone entries
75 triggers / 156 physical indexes / 85 FKs / 233 CHECKs
```

The frozen CP6 acceptance test independently proves its own historical `68/5/14/87 + 75/95 + 68/120` topology by migrating to revision `20260826_08`.

---

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

Post-CP6 current evolution:

```text
M3 / 20260827_09
+ account
+ email_identity
+ password_credential
+ auth_session

M3 / 20260827_10
+ acquire_account_security_lock(uuid)

M4 / 20260829_11
+ password_signup_challenge
+ password_recovery_challenge

M5-A / 20260830_12
+ 9 multi-authenticator tables
+ EmailIdentity reachability evolution
+ current exact physical/ACL metadata
```

Hard boundary remains:

```text
no real DANTE object
→ no object-specific Dictionary entry pretending it exists

real current DANTE object
→ matching current Dictionary entry required
```

---

## Schema evolution

`object-v1.schema.json` and `scope-v1.schema.json` are versioned contracts.

Ordinary forward product evolution may add governed stage identifiers and increase current inventory counts without rewriting historical CP6 entries.

An incompatible metadata meaning/shape change still requires an explicit later Dictionary schema version/migration rather than silent reinterpretation.

---

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

---

## Current M5-A acceptance boundary

The current M5-A Dictionary/database state has been directly proved against disposable PostgreSQL 18.6 at Alembic `20260830_12`:

```text
current 83/5/15/103 inventory                              PASS
75 triggers / 156 indexes / 85 FKs / 233 CHECKs           PASS
Dictionary ↔ SQLAlchemy ↔ Alembic ↔ PostgreSQL             PASS
Auth table/column ACL                                      PASS
M3/M4 historical database regressions                      PASS
M5 persistence constraint/ownership tests                   8 / 8 PASS
migration head/base/head                                    PASS
Alembic autogenerate drift                                  PASS
real PostgreSQL marked suite                               95 / 95 PASS
```

This persistence PASS does not imply later M5 provider/API/Web/browser closure.

See:

- `../access-auth.md` for current Access/Auth database meaning;
- `../../workstreams/access-auth-m5-live-handoff-2026-08-29.md` for current continuation state;
- `../development/backend-cp6-05-whole-database-qa.md` for retained CP6 acceptance evidence.
