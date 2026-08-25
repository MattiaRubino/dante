# Backend CP6-04 — M4 Routine / Event Recurrence Materialization

- **Status:** IMPLEMENTATION CANDIDATE / DIRECT POSTGRESQL RUN PENDING
- **Date:** 2026-08-25
- **Repository:** `MattiaRubino/dante`
- **Branch:** `feature/logical-postgresql`
- **Authorized PRE-SCOPE:** `abd97f835f60d5a8a84e386e52151d00538b1f96`
- **Checkpoint:** CP6-04 — Whole DANTE Database Materialization
- **Stage:** CP6-M04 — `cp6_recurrence`
- **Alembic revision:** `20260825_04`
- **Down revision:** `20260825_03`
- **P0 / M1 / M2 / M3:** CLOSED / DIRECT POSTGRESQL PASS
- **Runtime business ACL activation:** deferred to CP6-M07

## 1. Purpose

M4 materializes the frozen owner-bound Routine/Event Recurrence aggregate.
There is no independent `dante.recurrence` root. The two owner families remain
structurally symmetric while retaining exact Routine/Event identity and MaterialState
facets.

M4 creates exactly 26 tables: 13 Routine recurrence tables and 13 Event recurrence
tables.

## 2. Frozen cumulative topology after M4

```text
DANTE tables              63
physical indexes          87
foreign keys              61
CHECK constraints        109
UNIQUE constraints         2
views                      0
integrity routines         0
user trigger attachments   0
runtime business grants    0
```

M4 delta:

```text
tables                    +26
physical indexes          +32
foreign keys              +30
CHECK constraints         +62
ordinary UNIQUE            +0
```

The 32 M4 indexes are exactly 26 PK-backed indexes, two partial UNIQUE
open-current-history indexes and four DB-U15 owner/history indexes.

## 3. Exact Recurrence families

Each owner (`routine`, `event`) receives exactly:

```text
recurrence_state
recurrence_boundary_state
recurrence_calendar_state
recurrence_calendar_wall_time
recurrence_calendar_weekday
recurrence_calendar_month_day
recurrence_calendar_ordinal_weekday
recurrence_calendar_year_month_day
recurrence_elapsed_state
recurrence_quota_state
recurrence_cyclic_state
recurrence_cycle_position
recurrence_current_history
```

The accepted physical family discriminator remains:

```text
calendar_wall_clock
elapsed_interval
quota_per_period
cyclic_positional
```

The accepted range contract remains:

```text
open
until_boundary
expected_count
```

No baseline DDL is introduced for completion-relative or anchor-stream-relative
semantics.

## 4. Declarative enforcement

DB-U24 contributes exactly 31 row-local CHECK constraints per owner:

```text
state        3
boundary     4
calendar     5
selectors    6
elapsed      3
quota        6
cyclic       3
history      1
----------------
per owner   31
M4 total    62
```

Cross-table aggregate semantics deliberately remain M5 work. M4 does not fake them
with weaker row-local CHECKs.

All 30 M4 foreign keys are:

```text
MATCH SIMPLE
ON UPDATE NO ACTION
ON DELETE NO ACTION
NOT DEFERRABLE
VALID
ENFORCED
```

## 5. PostgreSQL 18 physical-constraint proof

PostgreSQL 18 exposes column NOT NULL constraints through
`pg_constraint.contype='n'`. For the 26 M4 tables the acceptance proof therefore
separates contractual constraints from physical NOT NULL rows:

```text
PK/CHECK/FK/UQ contract rows   118
NOT NULL ('n') rows             82
physical pg_constraint rows    200
```

Every physical row must be non-deferrable, non-deferred, valid and enforced.

## 6. Index contract

New partial UNIQUE indexes:

```text
ux_routine_recurrence_current_history_open
ux_event_recurrence_current_history_open
```

Both are `UNIQUE(owner_ref) WHERE current_until_at IS NULL`.

New DB-U15 structural indexes:

```text
ix_routine_recurrence_state_routine_ref
ix_event_recurrence_state_event_ref
ix_routine_recurrence_current_history_material_state_ref
ix_event_recurrence_current_history_material_state_ref
```

No GiST/GIN/BRIN/hash/vector/spatial index is introduced.

## 7. SQLAlchemy representation

M4 creates `recurrence.py` with exactly 26 explicit Row mappings.

```text
cumulative Row mappings   63
relationship()             0
backref/back_populates     0
ORM cascade                0
```

The mapping remains infrastructure only. It does not create an ORM domain graph or
an independent `RecurrenceRow`.

## 8. Database Dictionary

M4 creates one Dictionary table entry for each of the 26 physical tables in the
same change as the objects and advances `scope.json` to:

```text
completed_stages  [CP6-M01, CP6-M02, CP6-M03, CP6-M04]
tables            63
views              0
routines           0
physical indexes  87
foreign keys      61
CHECK constraints 109
triggers           0
```

Dictionary entries record the frozen M7 target ACL only. M4 itself activates no
runtime business privileges.

## 9. Stage-proof maintenance

The M3 acceptance file remains a permanent M3 proof. Its mapping and Dictionary
assertions are made stage-filtered, following the already-established M2 pattern,
so repository-head growth to M4 does not rewrite M3 history.

M4 receives its own PostgreSQL lane covering:

```text
exact cumulative topology
PostgreSQL-18 constraint catalog shape
live CHECK/FK/partial-UNIQUE behavior
runtime deny posture
M3 -> M4 -> M3 boundary
63 SQLAlchemy mappings / zero relationships
Dictionary <-> PostgreSQL reconciliation
fresh-head / base-round-trip / Alembic drift
```

## 10. ACL posture

P0 deny-by-default remains in force. M4 revokes all relation privileges on every
new table from:

```text
PUBLIC
dante_runtime
dante_migrator
```

M7 is still the only runtime ACL activation stage.

## 11. Execution honesty

Current evidence:

```text
P0  CLOSED / DIRECT POSTGRESQL PASS
M1  CLOSED / DIRECT POSTGRESQL PASS
M2  CLOSED / DIRECT POSTGRESQL PASS
M3  CLOSED / DIRECT POSTGRESQL PASS

M4  IMPLEMENTATION CANDIDATE
DIRECT POSTGRESQL RUN PENDING
M5  NOT STARTED / BLOCKED
```

No GitHub Actions CI evidence is claimed. The next admissible evidence is a direct
user-executed `uv run pytest -m postgres -vv` run against the disposable
PostgreSQL 18.6 acceptance harness after this candidate is published.

## 12. Explicit exclusions

M4 does not create or activate:

```text
CP6-M05..CP6-M07 revisions
current views
integrity routines
trigger attachments
Occurrence-generation tables
runtime business ACLs
generic Recurrence root/repository/service abstraction
product persistence adapters
business APIs
frontend/mobile behavior
new worktrees
additional persistent databases
protected-main merge/rebase/realignment
```
