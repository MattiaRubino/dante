# Backend CP6-04 — M2 Scoped / MaterialState Control Materialization

- **Status:** IMPLEMENTATION CANDIDATE / DIRECT POSTGRESQL EXECUTION PENDING
- **Date:** 2026-08-25
- **Repository:** `MattiaRubino/dante`
- **Branch:** `feature/logical-postgresql`
- **Authorized PRE-SCOPE:** `daf8112f619281989dd8a3acb79ed1865d7d138b`
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
NativeRef eligibility trigger will restrict the accepted concrete family to the
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

## 3. Exact M2 declarative constraints

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

`scope.json` becomes:

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

The M1 acceptance tests are converted from “repository head equals M1” assumptions
to explicit migration-to-`20260825_01` stage tests.

This preserves M1 as a permanent historical materialization proof while allowing
the repository head and Dictionary to advance.

M2 tests similarly target `20260825_02` explicitly so future M3+ growth does not
erase the M2 database boundary.

## 9. Direct PostgreSQL acceptance contract

The M2 lane must prove on real PostgreSQL 18.6:

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
all M2 constraints non-deferrable / valid / enforced

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

## 10. Execution honesty

At candidate-write time:

```text
P0
CLOSED / DIRECT POSTGRESQL PASS

M1
CLOSED / DIRECT POSTGRESQL PASS

M2 CODE / MIGRATION / MAPPINGS / DICTIONARY / TESTS
WRITTEN AS IMPLEMENTATION CANDIDATE

STATIC PYTHON / JSON CONSTRUCTION REVIEW
COMPLETE

REAL POSTGRESQL 18.6 M2 EXECUTION
NOT YET RUN

M2 DIRECT PASS
NOT YET EARNED

M3
NOT STARTED
```

No P0/M1 result is reused as M2 proof.

## 11. Explicit exclusions

M2 does not create or activate:

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

The next mandatory operation is fresh direct execution against the disposable
PostgreSQL 18.6 acceptance boundary. M3 remains blocked until M2 earns a direct
PASS.
