# Backend CP6-04 — M2 Scoped / MaterialState Control Materialization

- **Status:** CLOSED / DIRECT POSTGRESQL PASS
- **Date:** 2026-08-25
- **Repository:** `MattiaRubino/dante`
- **Branch:** `feature/logical-postgresql`
- **Authorized PRE-SCOPE:** `daf8112f619281989dd8a3acb79ed1865d7d138b`
- **Implementation candidate HEAD:** `69e6f75d6b883c07833e7a78881d741f15503dbd`
- **Repair authorized PRE-SCOPE:** `69e6f75d6b883c07833e7a78881d741f15503dbd`
- **Repair candidate HEAD:** `ab79458f8a17d390ff6298ff8ae535c0c89e0c20`
- **Checkpoint:** CP6-04 — Whole DANTE Database Materialization
- **Stage:** CP6-M02 — `cp6_scoped_material_control`
- **Alembic revision:** `20260825_02`
- **Down revision:** `20260825_01`
- **P0 prerequisite:** CLOSED / DIRECT POSTGRESQL PASS
- **M1 prerequisite:** CLOSED / DIRECT POSTGRESQL PASS
- **Runtime business ACL activation:** deferred to CP6-M07

## 1. Purpose

M2 materializes the scoped-owner address space and the shared MaterialState/current
control layer frozen by CP6-03. It also introduces the stable Schedule and Actual
owner rows because both are scoped owners whose subject NativeRefs depend on M1.

M2 creates exactly six new tables:

```text
dante.scoped_address
dante.schedule
dante.actual
dante.material_state_address
dante.native_current_material_state
dante.scoped_current_material_state
```

Cumulative topology after M2:

```text
DANTE tables              22
physical indexes          28
foreign keys               8
CHECK constraints         24
UNIQUE constraints         2
views                      0
integrity routines         0
user trigger attachments   0
runtime business grants    0
```

M2 does not materialize Schedule placement payload/history, Actual realization
payload/history, Session timing, Recurrence, Occurrence generation, current views,
integrity routines or runtime ACL activation.

## 2. Exact table contract

### scoped_address

```text
scoped_ref      uuid PRIMARY KEY
scoped_family   text NOT NULL
```

`scoped_family` is exactly:

```text
schedule
actual
```

### schedule

```text
schedule_ref         uuid PRIMARY KEY
subject_native_ref   uuid NOT NULL
```

`subject_native_ref` references `dante.native_address(native_ref)`. The later
NativeRef eligibility trigger restricts the accepted concrete family to the
frozen `activity | event | occurrence` set; M2 does not anticipate that trigger.

### actual

```text
actual_ref           uuid PRIMARY KEY
subject_native_ref   uuid NOT NULL
```

It uses the same NativeAddress anchor and later bounded family validation as
Schedule.

### material_state_address

```text
material_state_ref   uuid PRIMARY KEY
native_owner_ref     uuid NULL
scoped_owner_ref     uuid NULL
facet_code           text NOT NULL
```

Exactly one of `native_owner_ref` / `scoped_owner_ref` must be non-null.

The facet vocabulary is exactly:

```text
schedule.placement
actual.realization
session.timing
routine.recurrence
event.recurrence
```

### native_current_material_state

```text
native_owner_ref    uuid NOT NULL
facet_code          text NOT NULL
material_state_ref  uuid NOT NULL

PRIMARY KEY(native_owner_ref, facet_code)
UNIQUE(material_state_ref)
```

Allowed facets:

```text
session.timing
routine.recurrence
event.recurrence
```

### scoped_current_material_state

```text
scoped_owner_ref    uuid NOT NULL
facet_code          text NOT NULL
material_state_ref  uuid NOT NULL

PRIMARY KEY(scoped_owner_ref, facet_code)
UNIQUE(material_state_ref)
```

Allowed facets:

```text
schedule.placement
actual.realization
```

The two shared current tables remain direct-runtime deny surfaces. M5 later
creates the five bounded current views and M7 activates their exact ACLs.

## 3. Exact declarative constraint contract

M2 adds eight CHECK constraints:

```text
ck_scoped_address_scoped_family
ck_schedule_uuidv7
ck_actual_uuidv7
ck_material_state_address_uuidv7
ck_material_state_address_one_owner
ck_material_state_address_facet_code
ck_native_current_material_state_facet_code
ck_scoped_current_material_state_facet_code
```

M2 adds eight FKs, all:

```text
MATCH SIMPLE
ON UPDATE NO ACTION
ON DELETE NO ACTION
NOT DEFERRABLE
ENFORCED
VALID
```

Exact names:

```text
fk_schedule_subject_native_ref_native_address
fk_actual_subject_native_ref_native_address
fk_material_state_address_native_owner_ref_native_address
fk_material_state_address_scoped_owner_ref_scoped_address
fk_native_current_material_state_owner_address
fk_native_current_material_state_state_address
fk_scoped_current_material_state_owner_address
fk_scoped_current_material_state_state_address
```

The two exact UNIQUE constraints are:

```text
uq_native_current_material_state_material_state_ref
uq_scoped_current_material_state_material_state_ref
```

The six M2 primary keys, eight CHECKs, eight FKs and two UNIQUE constraints are
the exact 24 CP6 declarative constraints owned by the frozen M2 contract.

### PostgreSQL 18 NOT NULL catalog representation

The first direct PostgreSQL 18.6 run exposed an important catalog fact for proof
code: PostgreSQL 18 represents table `NOT NULL` constraints as `pg_constraint`
rows with `contype = 'n'`.

For the six M2 tables, the physical catalog therefore contains:

```text
CP6 declarative p/c/f/u constraints   24
PostgreSQL 18 NOT NULL constraints    14
----------------------------------------
pg_constraint M2 rows                 38
```

The 14 `n` rows do not change the CP6 frozen count of 24 named PK/CHECK/FK/UQ
constraints for M2. They are PostgreSQL 18's physical representation of the
already-declared column nullability contract.

The repaired proof therefore checks the two sets separately and also verifies
the complete 38-row physical M2 set is non-deferrable, non-deferred, validated
and enforced.

## 4. Exact M2 index delta

M2 adds 12 physical indexes:

```text
6 PK-backed indexes
2 UNIQUE-constraint-backed indexes
4 explicit indexes
```

The four explicit indexes are:

```text
ix_schedule_subject_native_ref
ix_actual_subject_native_ref

ix_material_state_address_native_owner_ref_facet_code
  (native_owner_ref, facet_code)
  WHERE native_owner_ref IS NOT NULL

ix_material_state_address_scoped_owner_ref_facet_code
  (scoped_owner_ref, facet_code)
  WHERE scoped_owner_ref IS NOT NULL
```

Cumulative count:

```text
M1 16
M2 12
-----
   28
```

No discriminator-only index is added to `scoped_family` or `facet_code`.

## 5. SQLAlchemy representation

M2 extends the frozen central mapping package without introducing relationships.

New mappings:

```text
addressing.py
  ScopedAddressRow
  MaterialStateAddressRow
  NativeCurrentMaterialStateRow
  ScopedCurrentMaterialStateRow

schedule.py
  ScheduleRow

actual.py
  ActualRow
```

Cumulative mappings after M2:

```text
22 row mappings
0 relationship()
0 backref/back_populates
0 ORM cascade
0 delete-orphan
```

`NativeRef`, `ScopedRecordRef` and `MaterialStateRef` remain distinct Python
reference types over PostgreSQL `uuid`.

## 6. Defense-in-depth ACL posture

P0 remains the source of deny-by-default future-object defaults.

M2 additionally revokes all relation privileges on each newly created relation
from:

```text
PUBLIC
dante_runtime
dante_migrator
```

before migration commit.

M2 activates no final DB-U21 runtime business capability. The Dictionary records
the final M7 expectations, but the live M2 database remains deny-by-default.

## 7. Database Dictionary same-change rule

M2 creates exactly six new table entries:

```text
schedule.json
actual.json
scoped_address.json
material_state_address.json
native_current_material_state.json
scoped_current_material_state.json
```

`scope.json` records:

```text
status                   materializing
completed_stages         [CP6-M01, CP6-M02]
tables                   22
views                     0
routines                  0
standalone total         22
triggers                   0
physical indexes         28
foreign keys               8
check constraints        24
```

No M3+ object-specific Dictionary entry is created.

## 8. Stage-proof maintenance

The M1 acceptance tests use explicit migration-to-`20260825_01` stage boundaries
rather than assuming the repository head remains M1.

M2 tests similarly target `20260825_02` explicitly so future M3+ growth does not
erase the M2 database boundary.

The PostgreSQL 18 `NOT NULL` catalog finding is handled in proof code only. No
M2 migration, mapping or Dictionary repair was warranted by that finding.

## 9. Direct PostgreSQL acceptance contract

The M2 lane proves on real PostgreSQL 18.6:

```text
single repository head = 20260825_02
fresh → head
head → base → head
Alembic check = no DANTE drift

M1 stage remains independently reproducible

M2 exact cumulative topology:
22 tables
28 indexes
24 CHECKs
8 FKs
2 UNIQUE constraints
0 views
0 routines
0 user triggers

all DANTE tables owned by dante_owner

M2 physical pg_constraint:
24 p/c/f/u contract constraints
14 PostgreSQL-18 NOT NULL ('n') constraints
38 physical rows total
all non-deferrable / non-deferred / valid / enforced

UUIDv7 rejection on Schedule / Actual / MaterialState
scoped-family vocabulary enforced
exactly-one MaterialState owner enforced
facet vocabularies enforced
real FK rejection enforced

runtime DML remains denied on all six M2 relations

M1 → M2 → M1 round-trip preserves the M1 boundary

22 SQLAlchemy mappings
0 ORM relationships

22 current Dictionary table entries
Dictionary ↔ PostgreSQL column reconciliation
M2 Dictionary FK/CHECK/stage/revision reconciliation
```

## 10. First real PostgreSQL 18.6 execution

User-executed local command:

```text
uv run pytest -m postgres -vv
```

Observed result:

```text
collected   71
deselected  37
selected    34

PASS        33
FAIL         1

elapsed     25.56s
```

The only failure was:

```text
test_cp6_m2.py::test_m2_materializes_exact_cumulative_topology
```

All of the following passed in that same run:

```text
M1 historical stage proof
M2 live constraint/FK behavior
M2 runtime deny posture
M2 upgrade/downgrade boundary
M2 SQLAlchemy mapping
M2 Dictionary reconciliation
fresh-head migration
M2 base round-trip
Alembic drift check
migrator identity enforcement
P0 security/privilege lane
runtime lane
transaction lane
```

The failed assertion expected 24 rows when selecting every `pg_constraint` row
belonging to an M2 table. The live PostgreSQL 18.6 catalog returned 38 because
it also exposed 14 `NOT NULL` constraints as `contype = 'n'`.

This was a proof-code defect, not evidence of unexpected M2 business DDL.

## 11. Repair decision

Repair scope:

```text
apps/backend/tests/integration/database/test_cp6_m2.py
docs/development/backend-cp6-04-m2-scoped-material-control.md
```

No migration, mapping, Dictionary or ACL file changed.

The repaired topology assertion requires:

```text
M2 p/c/f/u rows    24
M2 n rows          14
M2 total rows      38

constraint kinds exactly:
p c f u n

all 38:
NOT DEFERRABLE
NOT DEFERRED
VALID
ENFORCED
```

## 12. Direct PostgreSQL 18.6 rerun — PASS

After the proof-code repair, the user executed the complete disposable PostgreSQL
lane again with:

```text
uv run pytest -m postgres -vv
```

Observed result:

```text
collected   71
deselected  37
selected    34

PASS        34
FAIL         0

elapsed     25.75s
```

The rerun passed every M1, M2, migration, privilege, runtime and transaction test,
including the repaired PostgreSQL-18 physical constraint proof.

Closure status:

```text
P0
CLOSED / DIRECT POSTGRESQL PASS

M1
CLOSED / DIRECT POSTGRESQL PASS

M2 DDL / MAPPINGS / DICTIONARY
UNCHANGED AFTER FIRST RUN

FIRST REAL POSTGRESQL 18.6 M2 RUN
33 PASS / 1 FAIL

ROOT CAUSE
POSTGRESQL 18 NOT NULL CATALOG REPRESENTATION IN PROOF CODE

M2 TEST REPAIR
COMPLETE

DIRECT POSTGRESQL 18.6 RERUN
34 PASS / 0 FAIL

M2
CLOSED / DIRECT POSTGRESQL PASS

M3
READY TO OPEN / NOT STARTED
```

The first-run failure remains retained as historical evidence; it is not erased or
relabelled. M2 earns closure only from the fresh complete rerun.

## 13. Explicit exclusions

M2 did not create or activate:

```text
CP6-M03..CP6-M07 revisions
Schedule placement payload/history tables
Actual realization payload/history tables
Session timing/history tables
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

The next materialization stage is CP6-M03 `cp6_schedule_actual_session`. It must
remain a separate explicitly scoped repository change and earn its own direct
PostgreSQL acceptance before M4 can begin.
