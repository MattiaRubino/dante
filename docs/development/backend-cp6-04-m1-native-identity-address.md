# Backend CP6-04 — M1 Native Identity + NativeAddress Materialization

- **Status:** CLOSED / DIRECT POSTGRESQL PASS
- **Date:** 2026-08-25
- **Repository:** `MattiaRubino/dante`
- **Branch:** `feature/logical-postgresql`
- **Authorized PRE-SCOPE:** `c806943e4d6ac700485d5eb07c98a1f3cc8cdf87`
- **Implementation candidate HEAD:** `85e8d64029d1365823473f43b13f7c98ce1e34e6`
- **Closure authorized PRE-SCOPE:** `85e8d64029d1365823473f43b13f7c98ce1e34e6`
- **Checkpoint:** CP6-04 — Whole DANTE Database Materialization
- **Stage:** CP6-M01 — `cp6_native_identity_address`
- **Alembic revision:** `20260825_01`
- **Down revision:** `20260820_01`
- **P0 prerequisite:** CLOSED / DIRECT POSTGRESQL PASS
- **Runtime business ACL activation:** deferred to CP6-M07
- **M2 status:** NOT STARTED / READY TO OPEN AS A SEPARATE GATE

## 1. Purpose

M1 is the first CP6 business-schema materialization stage. It consumes the frozen
CP6-03 object inventory, naming, migration DAG, SQLAlchemy mapping plan,
Dictionary contract and DB-U24 implementation hardening without inventing later
M2..M7 structure.

The stage creates exactly:

```text
15 native identity-shell tables
1 NativeAddress control table
16 PK-backed physical indexes
16 named CHECK constraints
0 business FKs
0 views
0 routines
0 triggers
0 custom DANTE enum/domain types
0 DANTE sequences
0 runtime business grants
```

## 2. Exact M1 table inventory

```text
dante.person
dante.living_referent
dante.asset
dante.place
dante.content_artifact
dante.collective
dante.possibility
dante.goal
dante.plan
dante.activity
dante.event
dante.routine
dante.occurrence
dante.session
dante.observation
dante.native_address
```

Each native identity shell contains only its exact NativeRef PK. M1 does not add
generic `name`, `status`, timestamps, soft-delete flags or metadata payloads.

`native_address` contains exactly:

```text
native_ref    uuid PRIMARY KEY
owner_family  text NOT NULL
```

with the frozen fifteen-family bounded CHECK.

## 3. P0 fail-closed preflight

`20260825_01` executes a read-only live-catalog preflight before its first CP6
business DDL statement.

It proves the material P0 boundary including:

```text
dante schema owner = dante_owner
PUBLIC has no dante schema USAGE/CREATE
dante_runtime has dante USAGE and no CREATE
dante_runtime is not a member of dante_owner
PUBLIC database CONNECT/TEMPORARY are revoked
dante_owner future-object defaults contain no dante_runtime grants
PUBLIC future-routine EXECUTE is globally revoked
PUBLIC future-type/domain USAGE is globally revoked
runtime cannot read dante.alembic_version
```

If any predicate is false, M1 raises before creating the first business table.

The direct test lane deliberately reintroduces one legacy broad
`dante_runtime` default-table grant and proves that M1 aborts with zero CP6
business tables created.

## 4. UUIDv7 and bounded owner-family enforcement

The fifteen identity roots use application-issued UUIDv7 NativeRefs and each
receives the exact PostgreSQL 18 CHECK:

```text
uuid_extract_version(<native_ref>) IS NOT DISTINCT FROM 7
```

Exact CHECK names are the frozen `ck_<table>_uuidv7` set.

`native_address` receives:

```text
ck_native_address_owner_family
```

with exactly:

```text
person
living_referent
asset
place
content_artifact
collective
possibility
goal
plan
activity
event
routine
occurrence
session
observation
```

The later owner-existence/family dispatcher trigger is not anticipated in M1;
it remains part of the frozen later integrity stage.

## 5. Defense-in-depth ACL posture

All 16 relations are created while Alembic is explicitly running as
`current_user = dante_owner`.

Before the migration commits, M1 explicitly revokes all relation privileges from:

```text
PUBLIC
dante_runtime
dante_migrator
```

This is defense-in-depth on top of P0 deny-by-default future-object defaults.

M1 intentionally activates no runtime business capability. The DB-U21 final
table grants remain metadata expectations in the Dictionary and are materialized
only by CP6-M07.

## 6. SQLAlchemy representation

M1 introduces the frozen central mapping infrastructure:

```text
dante.platform.database.references
dante.platform.database.mappings.identity
dante.platform.database.mappings.addressing
```

Exactly 16 table mappings exist after M1:

```text
identity.py   15
addressing.py  1  (NativeAddressRow)
```

Baseline relationship posture remains:

```text
relationship()         0
backref/back_populates 0
ORM cascade            0
delete-orphan          0
```

`NativeRef`, `ScopedRecordRef` and `MaterialStateRef` are distinct Python
`NewType` wrappers over `uuid.UUID`. M1 uses NativeRef; the other two reference
types are established now because they belong to the single frozen database
reference typing boundary, not to a product vertical.

UUIDv7 issuance helpers are application-side and no PostgreSQL sequence/server
default is introduced.

## 7. Alembic metadata authority

Alembic imports the registered mapping package before assigning
`target_metadata`.

A fail-fast registration check requires the registered mapped tables and
`Base.metadata` tables to match exactly.

The canonical migration chain after M1 is:

```text
20260820_01  cp3_persistence_baseline
      ↓
20260825_01  cp6_native_identity_address
```

No branch/merge revision is introduced.

## 8. Database Dictionary same-change materialization

M1 creates exactly sixteen table entries under:

```text
docs/database/dictionary/tables/
```

Each entry records:

```text
real object identity
CP6-M01 introducing stage
Alembic revision 20260825_01
SQLAlchemy module/symbol
columns and semantic reference type
PK
CHECK
PK-backed physical index
final DB-U21 expected runtime grants
owner/default-deny posture
proof obligations
```

`scope.json` moves from `readiness_only` to `materializing` and records:

```text
completed_stages       [CP6-M01]
tables                  16
views                    0
routines                 0
standalone total        16
triggers                  0
physical indexes        16
foreign keys              0
check constraints       16
```

No speculative M2+ Dictionary entry is created.

## 9. Direct PostgreSQL acceptance contract

The M1 PostgreSQL lane proves:

```text
single repository head = 20260825_01
fresh → head
head → base → head
Alembic check reports no DANTE drift
P0 broadened-default negative case aborts before business DDL

exact 16-table M1 topology
all 16 tables owned by dante_owner
16 PK constraints
16 CHECK constraints
16 PK-backed indexes
0 business FK/UQ
0 views
0 routines
0 user triggers

non-v7 identity rejection
valid UUIDv7 acceptance
invalid native owner_family rejection

runtime SELECT/INSERT/UPDATE/DELETE remain denied at M1

16 SQLAlchemy mappings
0 ORM relationships

16 Dictionary entries
Dictionary scope = CP6-M01 cumulative counts
Dictionary columns reconcile to live PostgreSQL
```

## 10. Direct PostgreSQL 18.6 execution evidence

The existing backend worktree was fast-forwarded to the M1 implementation
candidate and the PostgreSQL lane was executed locally against the repository's
real `dante-postgres-local:18.6` Docker image.

User-executed command and observed result:

```text
uv run pytest -m postgres -vv

collected
65

deselected
37

selected
28

PASS
28

FAIL
0

elapsed
22.30s
```

The six M1-specific tests all passed:

```text
test_m1_materializes_exact_stage_topology                         PASS
test_m1_constraints_enforce_uuidv7_and_owner_family               PASS
test_m1_runtime_business_dml_remains_denied                       PASS
test_m1_fails_before_business_ddl_when_p0_defaults_are_broadened  PASS
test_m1_sqlalchemy_mapping_is_exact_and_relationship_free         PASS
test_m1_dictionary_matches_materialized_stage                     PASS
```

The existing P0/migration/runtime/transaction PostgreSQL tests also remained
green in the same run.

This is direct local PostgreSQL/Docker acceptance evidence supplied from the
actual execution. It is not represented as GitHub Actions CI evidence.

Container cleanup for this particular M1 run is not asserted in this record
until separately observed/confirmed; the acceptance harness is still designed
to remove its disposable container in fixture cleanup.

## 11. M1 closure decision

M1 has earned direct PASS.

```text
P0
CLOSED / DIRECT POSTGRESQL PASS

M1 CODE / MIGRATION / MAPPINGS / DICTIONARY / TESTS
WRITTEN

REAL POSTGRESQL 18.6 M1 EXECUTION
28 PASS / 0 FAIL

M1 DIRECT PASS
EARNED

M1
CLOSED

M2
NOT STARTED / READY TO OPEN AS A SEPARATE GATE
```

No previous P0 or CP3 result is reused as M1 proof, and no GitHub CI run is
claimed for this local acceptance evidence.

## 12. Explicit exclusions

M1 did not create or activate:

```text
CP6-M02..CP6-M07 revisions
schedule / actual
scoped_address
material_state_address
native/scoped current material-state controls
Schedule/Actual/Session companion-state tables
Routine/Event Recurrence tables
Occurrence-generation tables
current views
integrity routines
trigger attachments
runtime business ACLs
product persistence adapters
business APIs
frontend/mobile behavior
new worktrees
additional persistent databases
protected-main merge/rebase/realignment
```

## 13. Next mandatory operation

The next materialization stage is a separate reviewed gate:

```text
CP6-M02
cp6_scoped_material_control
```

It may materialize only the frozen M2 six-table control/scoped-address surface,
its exact indexes/constraints/mappings/Dictionary entries and corresponding
direct PostgreSQL tests. M3..M7 remain out of scope until their own stages.
