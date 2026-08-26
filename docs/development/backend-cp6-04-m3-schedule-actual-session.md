# Backend CP6-04 — M3 Schedule / Actual / Session Materialization

- **Status:** CLOSED / DIRECT POSTGRESQL PASS
- **Date:** 2026-08-25
- **Repository:** `MattiaRubino/dante`
- **Branch:** `feature/logical-postgresql`
- **Authorized PRE-SCOPE:** `3f3a51c5c4437dc511d2489ab02e2107e996c696`
- **Checkpoint:** CP6-04 — Whole DANTE Database Materialization
- **Stage:** CP6-M03 — `cp6_schedule_actual_session`
- **Alembic revision:** `20260825_03`
- **Down revision:** `20260825_02`
- **P0 / M1 / M2:** CLOSED / DIRECT POSTGRESQL PASS
- **Runtime business ACL activation:** deferred to CP6-M07

## 1. Purpose

M3 materializes the fifteen frozen companion tables for Schedule placement, Actual
realization and Session timing/history. It does not install the later cross-table
integrity routines/triggers or current views; those remain CP6-M05 responsibilities.

New relations:

```text
Schedule +6
schedule_placement_state
schedule_placement_date_state
schedule_placement_floating_local_state
schedule_placement_named_zone_state
schedule_placement_absolute_state
schedule_placement_current_history

Actual +4
actual_realization_state
actual_realization_timing
actual_realization_session_basis
actual_realization_current_history

Session +5
session_timing_state
session_timing_absolute
session_timing_elapsed
session_timing_pause
session_timing_current_history
```

## 2. Frozen cumulative topology after M3

```text
DANTE tables              37
physical indexes          55
foreign keys              31
CHECK constraints         47
UNIQUE constraints         2
views                      0
integrity routines         0
user trigger attachments   0
runtime business grants    0
```

M3 delta:

```text
tables                     +15
physical indexes           +27
foreign keys               +23
CHECK constraints          +23
ordinary UNIQUE constraints +0
```

The 27 M3 indexes are exactly 15 PK-backed indexes, three partial UNIQUE
open-current-history indexes, one partial UNIQUE open-Session-pause index and eight
DB-U15 structural/FK indexes.

## 3. Temporal representation

The physical types remain the frozen PostgreSQL contract:

```text
civil date span              daterange
floating/named local civil   timestamp without time zone
resolved/absolute instants   timestamptz
elapsed duration             numeric
```

No local civil timestamp is silently converted to UTC. Named-zone rows preserve
`zone_id` plus optional resolved instants. IANA validation/resolution semantics are
not anticipated here; the frozen M5 integrity layer owns them.

Schedule placement forms remain:

```text
date_span
floating_local
named_zone_local
absolute
```

Actual timing extents remain:

```text
instant
start_only
interval
```

Session timing forms remain:

```text
absolute
elapsed_only
```

Session precision remains:

```text
exact
approximate
rounded
```

## 4. Declarative enforcement

M3 adds the exact DB-U24 row-local manifest:

```text
Schedule CHECKs  10
Actual CHECKs     3
Session CHECKs   10
-------------------
M3 CHECKs        23
```

This includes finite-value checks, interval ordering, bounded discriminators,
finite positive elapsed duration and current-history chronology.

All 23 M3 FKs are:

```text
MATCH SIMPLE
ON UPDATE NO ACTION
ON DELETE NO ACTION
NOT DEFERRABLE
VALID
ENFORCED
```

No deferred cross-table semantic invariant is approximated with a fake row-local
CHECK. Those invariants remain M5 trigger/routine work.

## 5. Current-history and pause indexes

M3 creates these four partial UNIQUE invariants:

```text
ux_schedule_placement_current_history_open
  UNIQUE(schedule_ref) WHERE current_until_at IS NULL

ux_actual_realization_current_history_open
  UNIQUE(actual_ref) WHERE current_until_at IS NULL

ux_session_timing_current_history_open
  UNIQUE(session_ref) WHERE current_until_at IS NULL

ux_session_timing_pause_open
  UNIQUE(material_state_ref) WHERE resumed_at IS NULL
```

The eight additional structural indexes are:

```text
ix_schedule_placement_state_schedule_ref
ix_schedule_placement_current_history_material_state_ref
ix_actual_realization_state_actual_ref
ix_actual_realization_session_basis_session_ref
ix_actual_realization_session_basis_timing_state
ix_actual_realization_current_history_material_state_ref
ix_session_timing_state_session_ref
ix_session_timing_current_history_material_state_ref
```

## 6. SQLAlchemy representation

M3 completes the frozen first three mapping families:

```text
schedule.py   7 mappings total
actual.py     5 mappings total
session.py    5 mappings total

cumulative    37 Row mappings
relationship() 0
ORM cascade    0
```

Migration order and mapping-module organization intentionally differ. The migration
creates Session timing state before `actual_realization_session_basis`, because the
latter has an FK to the exact Session timing MaterialStateRef.

## 7. PostgreSQL 18 physical constraint proof

PostgreSQL 18 exposes column NOT NULL constraints as `pg_constraint.contype='n'`.
The M3 proof therefore separates the frozen declarative contract from those physical
catalog rows.

For the fifteen M3 tables:

```text
PK/CHECK/FK/UQ contract rows    61
NOT NULL ('n') rows             45
physical pg_constraint rows    106
```

The acceptance test requires every one of those physical rows to be non-deferrable,
non-deferred, valid and enforced.

## 8. ACL posture

P0 deny-by-default remains active. M3 additionally revokes all relation privileges
on every new table from:

```text
PUBLIC
dante_runtime
dante_migrator
```

M3 activates no final runtime business capability.

The Dictionary records the frozen M7 target only:
- SELECT + INSERT on all fifteen M3 tables;
- `UPDATE(current_until_at)` additionally on the three current-history tables;
- no DELETE and no table-level UPDATE.

## 9. Database Dictionary

M3 creates exactly fifteen table entries in the same change as the real objects and
advances `scope.json` to:

```text
completed_stages   [CP6-M01, CP6-M02, CP6-M03]
tables             37
views               0
routines            0
physical indexes   55
foreign keys       31
CHECK constraints  47
triggers            0
```

The structural test reconciles Dictionary columns, M3 FK/CHECK/index names,
introducing stage and revision against live PostgreSQL.

## 10. Stage-proof maintenance

M2 tests remain permanent stage proofs. They migrate explicitly to `20260825_02`
and now filter SQLAlchemy/Dictionary assertions to the M1+M2 surface, so advancing
the repository head to M3 does not rewrite M2 history.

M3 receives its own direct PostgreSQL lane covering:

```text
exact cumulative topology
PostgreSQL-18 constraint catalog shape
live CHECK/FK/partial-UNIQUE behavior
runtime deny posture
M2 → M3 → M2 boundary
37 SQLAlchemy mappings / zero relationships
Dictionary ↔ PostgreSQL reconciliation
fresh-head / base-round-trip / Alembic drift
```

## 11. Execution evidence

The first direct PostgreSQL 18.6 run was intentionally retained as evidence of the
Dictionary assembly finding:

```text
M3 FIRST DIRECT POSTGRESQL 18.6 RUN
collected      77
deselected     37
selected       40
PASS           39
FAIL            1
elapsed        29.58s

ONLY FAILURE
 test_m3_dictionary_matches_live_stage_and_current_scope

DDL / constraints / FK / partial UNIQUE / ACL / upgrade-downgrade /
SQLAlchemy mappings / Alembic head-drift proofs
PASS
```

After the Dictionary filename/content repair, the complete lane was rerun against
remote commit `27d8a708a6ed33e2a630ce9cb4c86dd1cc4e77b9`:

```text
M3 FINAL DIRECT POSTGRESQL 18.6 RERUN
collected      77
deselected     37
selected       40
PASS           40
FAIL            0
elapsed        50.10s
coverage       93.91%
```

The final rerun proves the complete M1/M2/M3 PostgreSQL lane, including exact M3
topology, live constraints/FKs/partial UNIQUE indexes, runtime deny posture,
M2→M3→M2 migration boundary, 37 relationship-free SQLAlchemy mappings, Dictionary
reconciliation, fresh-head migration, base round-trip, Alembic drift detection,
security/runtime and transaction semantics.

This is local user-executed PostgreSQL evidence, not GitHub Actions CI evidence.
No previous-stage PostgreSQL result is reused as M3 proof.

## 12. Explicit exclusions

M3 does not create or activate:

```text
CP6-M04..CP6-M07 revisions
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

Those exclusions remain valid after closure. M4 is now unblocked but not started by
this closure commit.

## 13. First-run finding and repair

The first direct M3 run proved the live PostgreSQL schema while exposing a
Dictionary assembly defect. Nine already-correct Actual/Session Dictionary blobs
were attached to the wrong filenames during the Git tree assembly. The failure was
therefore a Dictionary filename/content permutation, not a DDL or ORM defect.

Repair scope:

```text
Dictionary JSON files corrected                 9
DDL changes                                     0
SQLAlchemy mapping changes                      0
test weakening                                  0
scope-count changes                             0
```

The repair reattached each existing correct blob to its matching filename:

```text
actual_realization_state
actual_realization_timing
actual_realization_session_basis
actual_realization_current_history
session_timing_state
session_timing_absolute
session_timing_elapsed
session_timing_pause
session_timing_current_history
```

The unchanged acceptance test then passed on the full rerun, confirming the repair
without weakening the proof contract.

## 14. Harness cleanup and closure

After the final green rerun, the disposable harness was checked with:

```text
docker ps -a --filter "name=dante-cp3-pytest"
```

The result contained only the Docker column header and no rows:

```text
residual dante-cp3-pytest containers   0
```

No persistent LOCAL Compose database or `postgres-data` volume was started or
materialized by M3 acceptance.

Final stage disposition:

```text
CP6-M03
CLOSED

DIRECT POSTGRESQL 18.6
40 / 40 PASS
0 FAIL

HARNESS CLEANUP
0 RESIDUAL CONTAINERS

M4
UNBLOCKED / NOT STARTED
```
