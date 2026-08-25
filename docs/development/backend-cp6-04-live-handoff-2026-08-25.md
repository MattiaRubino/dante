# CP6-04 CURRENT LIVE HANDOFF — 2026-08-25

> **CURRENT CROSS-CHAT RESUME — P0/M1/M2/M3/M4 CLOSED / M5 NEXT**  
> This is the current operational handoff for the DANTE PostgreSQL materialization workstream on `feature/logical-postgresql`. It supersedes older CP6-03 handoff/resume text only for current phase/status/routing. It does **not** supersede canonical Database Architecture & Reference Parts 1–18, the Gate-03 ratification, the accepted Domain/Logical/Physical models, or the closed P0/M1/M2/M3/M4 stage records.  
> Snapshot immediately before this handoff write: `93d053a7393f57fc824a733c523332f158901757` (`docs: close CP6-04 M4 after direct PostgreSQL pass`). Because this file is itself committed after that snapshot, a future chat MUST fetch the live branch HEAD and use that live HEAD as the next PRE-SCOPE. Do not reuse `93d053...` as a write gate after this handoff commit.

**Status:** CURRENT / CROSS-CHAT CONTINUITY / NON-NORMATIVE  
**Repository:** `MattiaRubino/dante`  
**Branch:** `feature/logical-postgresql`  
**Backend worktree:** `~/projects/dante`  
**Frontend worktree:** `~/projects/dante-frontend` — DO NOT TOUCH for this PostgreSQL workstream  
**Current phase:** CP6-04 — Whole DANTE Database Materialization  
**Current materialization:** P0 + M1 + M2 + M3 + M4 CLOSED / DIRECT POSTGRESQL PASS  
**Next stage:** CP6-M05 — `cp6_core_integrity_current_views`  
**M5 implementation:** NOT STARTED / NOT WRITTEN  
**M5 gate:** technically reconstructed/reviewed in the prior chat, but must be re-anchored to the live post-handoff HEAD before any write  
**Protected-main realignment:** NOT PART OF THIS HANDOFF / still a separate gate  
**Persistent LOCAL PostgreSQL database:** design exists; do not assume it has been intentionally started/materialized merely because disposable acceptance tests ran

---

# 0. Why this file exists

The prior conversation reached context saturation after closing M4 and reconstructing the exact M5 implementation surface. This file exists so the next conversation can resume without asking the user to restate the project, without rebuilding the database plan from chat memory, and without weakening the repository engineering discipline used throughout CP6.

This handoff is deliberately detailed. The next chat should use it as a routing/resume map, then verify every material claim against the repository before writing.

Authority rule:

```text
repository truth / canonical documents > this handoff > old chat memory
```

If this handoff conflicts with the live repository or a later canonical authority, stop and reconcile rather than guessing.

---

# 1. Mandatory first actions for the next chat

Do these in order before proposing or executing M5 writes:

```text
1. fetch live HEAD of feature/logical-postgresql;
2. confirm the branch contains the M4 closure commit plus this handoff commit and inspect any additional intervening commit;
3. if HEAD moved for any reason beyond this handoff, inspect every intervening path before trusting the prepared M5 gate;
4. DO NOT create a new branch or worktree;
5. DO NOT merge/rebase/realign protected main unless the user opens a separate gate;
6. read this handoff fully;
7. read Gate-03 ratification and the P0/M1/M2/M3/M4 closure records;
8. read docs/database/README.md and ALL canonical Database Reference Parts 1–18 as one accumulated authority;
9. read the CP6-02 Constitution and CP6-01 coverage/closure, including the non-57/cross-cutting ledger;
10. inspect the current migrations, mappings, Dictionary, provisioning, Alembic env and PostgreSQL tests directly;
11. re-verify the exact M5 routine/view/trigger allocation against Parts 9/10/12/13/14/15/16/17/18;
12. restate the M5 gate against the CURRENT live HEAD;
13. wait for explicit user authorization before the first M5 mutation;
14. immediately before first mutation re-check HEAD == approved PRE-SCOPE;
15. after writes perform remote readback + exact PRE-SCOPE→HEAD compare + unexpected paths = 0;
16. require a fresh user-executed real PostgreSQL acceptance run before M5 can close;
17. preserve failed-run/repair evidence if a real finding occurs; never rewrite history into a fake first-pass green result.
```

Never ask the user to repeat information that the repository can answer.

---

# 2. Repository / operating safety rules — mandatory

## 2.1 Branch and worktree boundary

Work only on:

```text
repo:    MattiaRubino/dante
branch:  feature/logical-postgresql
backend: ~/projects/dante
```

The separate frontend worktree is:

```text
~/projects/dante-frontend
```

Do not touch it for this database workstream.

Do not create:

```text
new feature/logical-postgresql-* branches
new clones
new worktrees
new CP6 database branches
```

unless the user explicitly opens a separate repository-management gate.

The user's local backend worktree may contain an untracked `.turbo/`. Never use `git add .` as a convenience.

## 2.2 Exact write-gate protocol

Every repository mutation requires:

```text
BRANCH
feature/logical-postgresql

PRE-SCOPE
<exact live HEAD>

CREATE
<exact paths>

UPDATE
<exact paths>

DELETE
<exact paths>

PURPOSE
<bounded purpose>

EXPLICITLY OUT OF SCOPE
<bounded exclusions>
```

Immediately before first mutation:

```text
live HEAD MUST equal approved PRE-SCOPE
```

If it moved, STOP and re-gate.

After the write:

```text
remote readback
PRE-SCOPE → HEAD compare
commit count
exact unique paths
added / modified / deleted counts
unexpected paths = 0
```

Never claim GitHub CI evidence when only local user-executed tests exist.

## 2.3 Side-effect disclosure

Before telling the user to run a command that changes state, explicitly say:

```text
what it creates/changes
where it lives
whether it is temporary or persistent
how cleanup/removal behaves
```

This is especially mandatory for Docker/PostgreSQL commands.

---

# 3. Authority hierarchy and mandatory reading

Use this practical authority order:

```text
1. live repository code / migrations / tests for implementation truth;
2. closed Domain Model;
3. closed Whole Logical Model;
4. accepted PostgreSQL Physical Model;
5. CP6-01 concrete persistence coverage + closure;
6. CP6-02 PostgreSQL Persistence Constitution + closure + ADR-010;
7. Database Architecture & Reference Parts 1–18 consumed together;
8. Gate-03 ratification / closure records;
9. Database Dictionary contract + current object entries;
10. current CP6-04 P0/M1/M2/M3/M4 closure docs;
11. this handoff for continuity;
12. historical chat memory only as secondary evidence.
```

## 3.1 Operating / repository docs

Read or re-check:

```text
README.md
docs/README.md
docs/PROJECT-STATUS.md
docs/ROADMAP.md

docs/development/agent-operating-manual.md
docs/development/operating-rules.md
docs/development/documentation-and-handoff.md
docs/development/branching-and-environments.md
docs/development/repository-engineering-safety.md
```

Several old entrypoint banners may contain stale CP6-03 resume wording. The authoritative correction is:

```text
docs/development/backend-cp6-03-gate-03-ratification-2026-08-25.md
```

That ratification explicitly says older CP6-03 current banners are narrowly superseded for phase/status/routing only.

## 3.2 CP6-01

```text
docs/development/backend-cp6-01-concrete-persistence-coverage.md
docs/development/backend-cp6-01-concrete-persistence-coverage-part-2.md
docs/development/backend-cp6-01-concrete-persistence-coverage-closure.md
```

Gate 01 is closed. Do not audit only the 57 Domain concepts; the Part-2 non-57/cross-cutting ledger remains part of the persistence contract.

## 3.3 CP6-02

```text
docs/development/backend-cp6-02-postgresql-persistence-constitution.md
docs/development/backend-cp6-02-postgresql-persistence-constitution-closure.md
docs/decisions/ADR-010-postgresql-persistence-constitution.md
```

Gate 02 is closed. Preserve the doctrine around identity, references, MaterialState, history/current truthfulness, temporal semantics, relational constraints, indexes, transactions, migrations, security and QA.

## 3.4 CP6-03 closure and ratification

Read:

```text
docs/development/backend-cp6-03-gate-03-closure.md
docs/development/backend-cp6-03-gate-03-ratification-2026-08-25.md
docs/development/backend-cp6-03-live-handoff-2026-08-25.md   # historical continuity only
```

Final authoritative CP6-03 state:

```text
CP6-03 CLOSED
GATE 03 PASS / RATIFIED
FULL TOMBSTONE + SECURITY REPLAY COMPLETE / CLEAN
GLOBAL DB-U OPEN = 0
```

The ratification records the strict from-zero Parts 1–18 replay and explicitly corrects the earlier premature closure sequencing without rewriting history.

## 3.5 Database Architecture & Reference — read ALL Parts 1–18

```text
docs/database/dante-postgresql-database.md
docs/database/dante-postgresql-database-part-2.md
docs/database/dante-postgresql-database-part-3.md
docs/database/dante-postgresql-database-part-4.md
docs/database/dante-postgresql-database-part-5.md
docs/database/dante-postgresql-database-part-6.md
docs/database/dante-postgresql-database-part-7.md
docs/database/dante-postgresql-database-part-8.md
docs/database/dante-postgresql-database-part-9.md
docs/database/dante-postgresql-database-part-10.md
docs/database/dante-postgresql-database-part-11.md
docs/database/dante-postgresql-database-part-12.md
docs/database/dante-postgresql-database-part-13.md
docs/database/dante-postgresql-database-part-14.md
docs/database/dante-postgresql-database-part-15.md
docs/database/dante-postgresql-database-part-16.md
docs/database/dante-postgresql-database-part-17.md
docs/database/dante-postgresql-database-part-18.md
```

Important late supersessions:

```text
Part 17 / DB-U25
- exact Recurrence selector/phase/range determinism
- duplicate non-quota generation repair
- NULL-safe CHECK repairs
- exact governing-Recurrence membership
- narrowed current-history lifecycle / column-scoped INSERT

Part 18 / DB-U26
- static/bound SQL construction
- trusted search_path pg_catalog,dante,pg_temp
- pg_temp explicitly last
- SCRAM-safe credential handling
- exact runtime/migrator/owner identity and membership graph
- zero baseline generic dynamic PL/pgSQL EXECUTE
- exact routine security posture and negative security proofs
```

Do not implement from Part 13 alone. The final implementation must include the narrow Part 17 and Part 18 hardenings.

## 3.6 Current CP6-04 stage records

Read all of these before M5:

```text
docs/development/backend-cp6-04-p0-provisioning-security.md
docs/development/backend-cp6-04-m1-native-identity-address.md
docs/development/backend-cp6-04-m2-scoped-material-control.md
docs/development/backend-cp6-04-m3-schedule-actual-session.md
docs/development/backend-cp6-04-m4-recurrence.md
```

These are the current direct-materialization evidence records.

## 3.7 Dictionary foundation/current scope

```text
docs/database/dictionary/README.md
docs/database/dictionary/scope.json
docs/database/dictionary/schema/object-v1.schema.json
docs/database/dictionary/schema/scope-v1.schema.json
```

Current `scope.json` after M4 is:

```text
status              materializing
completed stages    CP6-M01..CP6-M04
standalone tables   63
views                0
routines             0
standalone total    63
triggers             0
physical indexes    87
foreign keys        61
CHECK constraints   109
```

Expected final baseline remains:

```text
68 tables
5 views
14 routines
87 standalone Dictionary entries
75 triggers
95 indexes
68 FKs
120 CHECKs
```

---

# 4. Frozen final database target

The final CP6 baseline remains exactly:

```text
DANTE-owned tables                  68
ordinary current views               5
integrity routines                  14
trigger attachments                 75
  immediate                         18
  deferred                          57
physical indexes                    95
foreign keys                        68
named CHECK constraints            120
custom DANTE enum/domain types       0
DANTE sequences                      0
materialized views                   0
RLS policies                         0
```

SQLAlchemy final target:

```text
68 explicit Row mappings
5 Core-only current-view handles
0 baseline relationship()
0 backref/back_populates
0 ORM cascade/delete-orphan
functions/triggers/views migration-owned
NativeRef / ScopedRecordRef / MaterialStateRef remain distinct
```

Dictionary final target:

```text
68 table entries
5 view entries
14 routine entries
87 standalone entries total
75 triggers embedded in owning table entries
95 indexes embedded in owning table entries
FK/CHECK structure embedded in table entries
```

No generic Entity/Thing/Relationship/EAV root is allowed.

---

# 5. Frozen migration/materialization DAG

The canonical chain is:

```text
P0  cp6_provisioning_acl_hardening   non-Alembic prerequisite
 ↓
M1  cp6_native_identity_address      20260825_01
 ↓
M2  cp6_scoped_material_control      20260825_02
 ↓
M3  cp6_schedule_actual_session      20260825_03
 ↓
M4  cp6_recurrence                   20260825_04
 ↓
M5  cp6_core_integrity_current_views 20260825_05   NEXT / NOT WRITTEN
 ↓
M6  cp6_occurrence_generation        future
 ↓
M7  cp6_runtime_acl_activation       future
```

Current Alembic versions directory contains:

```text
20260820_01_cp3_persistence_baseline.py
20260825_01_cp6_native_identity_address.py
20260825_02_cp6_scoped_material_control.py
20260825_03_cp6_schedule_actual_session.py
20260825_04_cp6_recurrence.py
```

There is **no M5 migration yet** at this handoff snapshot.

---

# 6. P0 — CLOSED / direct PostgreSQL PASS

Record:

```text
docs/development/backend-cp6-04-p0-provisioning-security.md
```

P0 is non-Alembic and created zero business DDL. It hardened provisioning/security before M1.

Final security posture includes:

```text
search_path = pg_catalog,dante,pg_temp
runtime session_user/current_user = dante_runtime
migration login = dante_migrator
post SET ROLE current_user = dante_owner
owner = NOLOGIN / no password
only DANTE membership edge = dante_owner granted to dante_migrator
INHERIT false / SET true / ADMIN false
PUBLIC DB CONNECT/TEMP/CREATE denied
runtime DB CONNECT yes, TEMP/CREATE no
migrator DB CONNECT yes, TEMP/CREATE no
runtime dante schema USAGE only
migrator no direct dante schema privilege
PUBLIC/runtime/migrator public-schema posture denied
future runtime defaults deny-by-default
SCRAM-SHA-256 required
cleartext password-bearing SQL removed
```

Important P0 finding/repair:

```text
first real run: 20 PASS / 1 FAIL
finding: PUBLIC EXECUTE on routines survived because PostgreSQL global default privileges cannot be negated by an IN SCHEMA revoke
analogous PUBLIC type USAGE risk found by analysis
repair: global ALTER DEFAULT PRIVILEGES REVOKE EXECUTE ON ROUTINES FROM PUBLIC
        global ALTER DEFAULT PRIVILEGES REVOKE USAGE ON TYPES FROM PUBLIC
final run: 22 / 22 PASS
cleanup: 0 residual disposable containers confirmed
```

Do not regress to per-schema-only PUBLIC routine/type default revokes.

---

# 7. M1 — CLOSED / direct PostgreSQL PASS

Record:

```text
docs/development/backend-cp6-04-m1-native-identity-address.md
```

Revision:

```text
20260825_01
parent 20260820_01
```

Materialized:

```text
15 native identity shells
+ native_address
= 16 tables
16 PK-backed indexes
16 CHECKs
0 business FKs
```

Native identity families:

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

Direct evidence:

```text
28 selected
28 PASS
0 FAIL
22.30s
```

M1 cleanup was not separately asserted in its closure record.

---

# 8. M2 — CLOSED / direct PostgreSQL PASS

Record:

```text
docs/development/backend-cp6-04-m2-scoped-material-control.md
```

Revision:

```text
20260825_02
parent 20260825_01
```

M2 adds:

```text
scoped_address
schedule
actual
material_state_address
native_current_material_state
scoped_current_material_state
```

Cumulative after M2:

```text
22 tables
28 indexes
8 FKs
24 CHECKs
2 UNIQUE constraints
0 views/routines/triggers
```

Important PostgreSQL-18 proof lesson:

```text
PostgreSQL 18 exposes NOT NULL as pg_constraint contype='n'.
```

For M2 physical catalog:

```text
24 p/c/f/u contractual constraints
14 n constraints
38 physical pg_constraint rows
```

First run:

```text
34 selected
33 PASS
1 FAIL
```

Only failure was proof code counting every `pg_constraint` row as if PostgreSQL 18 behaved like older versions. DDL, mappings and Dictionary were correct.

Repair changed only proof/documentation; no DDL repair.

Final rerun:

```text
34 / 34 PASS
0 FAIL
25.75s
```

Rule for later stages: never use naive `pg_constraint` row counts without deliberately accounting for PostgreSQL 18 `contype='n'`.

---

# 9. M3 — CLOSED / direct PostgreSQL PASS

Record:

```text
docs/development/backend-cp6-04-m3-schedule-actual-session.md
```

Revision:

```text
20260825_03
parent 20260825_02
```

Adds 15 tables:

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

Cumulative after M3:

```text
37 tables
55 indexes
31 FKs
47 CHECKs
2 UNIQUE constraints
0 views/routines/triggers
```

M3 physical PostgreSQL-18 constraint proof:

```text
61 p/c/f/u contractual rows
45 n rows
106 physical pg_constraint rows
```

Important M3 operational errors and repairs — preserve these lessons:

### 9.1 Git tree test-file swap

During initial Git tree assembly, `test_cp6_m2.py` and `test_cp6_m3.py` were accidentally attached to the opposite filenames. This was caught by remote readback before asking the user to run tests.

Repair:

```text
only the two test paths were swapped back
no migration/mapping/Dictionary change
```

Lesson: after atomic tree assembly, inspect content identity, not merely path presence/count.

### 9.2 Dictionary filename/content permutation

The first real M3 run was:

```text
40 selected
39 PASS
1 FAIL
```

All database/migration/mapping/security behavior passed. The only failure was Dictionary reconciliation.

Root cause:

```text
9 already-correct Actual/Session Dictionary blobs were attached to the wrong filenames during Git tree assembly.
```

Repair:

```text
9 Dictionary JSON placements corrected
DDL changes 0
SQLAlchemy changes 0
test weakening 0
scope-count changes 0
```

Final rerun against repair commit `27d8a708a6ed33e2a630ce9cb4c86dd1cc4e77b9`:

```text
40 / 40 PASS
0 FAIL
50.10s
coverage 93.91%
```

Harness cleanup after final M3 run:

```text
residual dante-cp3-pytest containers = 0
```

M3 closure commit:

```text
abd97f835f60d5a8a84e386e52151d00538b1f96
```

---

# 10. M4 — CLOSED / direct PostgreSQL PASS

Record:

```text
docs/development/backend-cp6-04-m4-recurrence.md
```

Implementation candidate:

```text
ad561872ddcf10b3e686c7624e16d18ed61c5202
```

Closure commit / pre-handoff snapshot:

```text
93d053a7393f57fc824a733c523332f158901757
```

Revision:

```text
20260825_04
parent 20260825_03
```

M4 adds exactly 26 owner-bound Recurrence tables: 13 Routine + 13 Event. There is no generic `recurrence` root.

Per owner:

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

M4 delta:

```text
+26 tables
+32 indexes
+30 FKs
+62 CHECKs
```

Cumulative after M4:

```text
63 tables
87 indexes
61 FKs
109 CHECKs
2 UNIQUE constraints
0 views
0 routines
0 triggers
0 runtime business grants
```

M4 physical PostgreSQL-18 constraint proof:

```text
118 p/c/f/u contractual rows
82 n rows
200 physical pg_constraint rows
```

Direct user run:

```text
83 collected
37 deselected
46 selected
46 PASS
0 FAIL
34.28s
coverage 95.57%
```

All six M4 tests passed, plus M1/M2/M3 historical stage proofs, fresh database to head, M4 head/base/head, Alembic no-drift, P0 privileges, runtime and transaction semantics.

M4 required no DDL/mapping/test/Dictionary repair after the direct run.

Post-run disposable-container cleanup was **not separately asserted** for M4. Do not claim zero residual containers for that specific run unless separately observed later.

Operational lesson from M4 assembly: there was one transient accidental out-of-scope branch ref move while using the connector. It was immediately reset to the exact approved PRE-SCOPE before final assembly. The final candidate compare was clean:

```text
1 candidate commit
34 paths
30 CREATE
4 UPDATE
0 DELETE
0 unexpected
```

The accidental path is not part of the final M4 branch result. Continue to rely on exact pre-write race checks and post-write compares.

---

# 11. Current real repository/database state after M4

At the pre-handoff snapshot `93d053...`:

```text
P0  CLOSED / DIRECT POSTGRESQL PASS
M1  CLOSED / DIRECT POSTGRESQL PASS
M2  CLOSED / DIRECT POSTGRESQL PASS
M3  CLOSED / DIRECT POSTGRESQL PASS
M4  CLOSED / DIRECT POSTGRESQL PASS
M5  READY TO OPEN / NOT STARTED
M6  NOT STARTED
M7  NOT STARTED
```

Real materialized CP6 objects represented by migrations/metadata/Dictionary:

```text
63 tables
0 views
0 integrity routines
0 user trigger attachments
87 physical indexes
61 FKs
109 CHECKs
2 ordinary UNIQUE constraints
63 Row mappings
```

Runtime business DML remains intentionally inactive because M7 is the only final ACL activation stage.

---

# 12. SQLAlchemy current state

Current mapping package includes:

```text
identity.py
addressing.py
schedule.py
actual.py
session.py
recurrence.py
```

Current cumulative Row mappings:

```text
63
```

Still required:

```text
relationship()             0
backref/back_populates     0
ORM cascade                0
delete-orphan              0
```

M5 does **not** add table Row mappings. It adds Core-only view handles in a new `mappings/views.py` with a separate `VIEW_METADATA` boundary.

The frozen M5 rule is:

```text
MAPPED_TABLES remains 63
VIEW_METADATA contains 5 view handles
ORM mapping for views = 0
```

Do not merge view handles into `Base.metadata` merely to make Alembic discover them as tables.

---

# 13. Local PostgreSQL / Docker model

Compose source:

```text
infra/compose/local.yaml
```

Persistent LOCAL design:

```text
image        dante-postgres-local:18.6
host port    127.0.0.1:5432
DB           dante
volume       postgres-data:/var/lib/postgresql
```

Important distinction:

### Disposable acceptance harness

Command used throughout P0–M4:

```bash
cd ~/projects/dante/apps/backend
uv run pytest -m postgres -vv
```

The integration fixture uses a disposable container named like:

```text
dante-cp3-pytest-...
```

It uses fresh disposable databases and is intended to remove the test container during fixture cleanup.

It does **not** intentionally start or mutate the persistent Compose database or `postgres-data` volume.

### Persistent Compose database

Do not silently start it.

If/when the user deliberately asks to start persistent LOCAL PostgreSQL, disclose first:

```text
docker compose up creates/starts the persistent postgres service
named postgres-data survives normal stop/restart and docker compose down
127.0.0.1:5432 becomes the local inspection endpoint for DBeaver/PyCharm
provisioning + Alembic create the real local roles/security/business schema

docker compose down
→ removes container/network, NOT the named volume

docker compose down -v or explicit volume removal
→ destroys persistent database data
```

Do not conflate disposable acceptance evidence with a persistent LOCAL database having been materialized.

---

# 14. NEXT STAGE — M5 exact frozen contract

M5 canonical planning node:

```text
CP6-M05
scope slug     cp6_core_integrity_current_views
revision       20260825_05
down_revision  20260825_04
class          MIG-A
transactional  YES
```

M5 creates:

```text
0 tables
0 indexes
5 ordinary current views
13 integrity trigger-functions
66 trigger attachments
```

Trigger split:

```text
15 immediate BEFORE ROW
51 deferred CONSTRAINT TRIGGER
```

The final 14th routine and remaining 9 triggers stay in M6 because they depend on Occurrence-generation tables that do not exist before M6.

M5 cumulative target:

```text
tables            63
views              5
routines           13
standalone         81

triggers           66
  immediate        15
  deferred         51

indexes            87
FK                 61
CHECK             109
UNIQUE               2
```

No runtime business privilege activation occurs in M5.

---

# 15. M5 — exact 13 routines

M5 creates these exact functions:

```text
enforce_native_address_owner
enforce_scoped_address_owner
enforce_native_ref_eligibility
enforce_material_state_totality
enforce_current_material_state_binding
enforce_current_history_equivalence
enforce_owner_creation_completeness
enforce_schedule_placement_totality
enforce_actual_realization_basis
enforce_session_timing_totality
enforce_session_pause_consistency
enforce_recurrence_aggregate_integrity
validate_iana_timezone
```

M6 later creates only:

```text
enforce_occurrence_generation_integrity
```

Every M5 routine must follow the frozen Part-18 security posture:

```text
FUNCTION () RETURNS trigger
language       plpgsql
SECURITY       INVOKER
volatility     VOLATILE
parallel       UNSAFE
leakproof      false
owner          dante_owner
search_path    pg_catalog,dante,pg_temp
```

Routine privilege posture:

```text
PUBLIC EXECUTE         NO
dante_runtime EXECUTE  NO
dante_migrator EXECUTE NO
```

Baseline generic dynamic PL/pgSQL `EXECUTE` remains zero. Known DANTE identifiers should be static/schema-qualified; do not create a generic TG_ARGV-driven SQL dispatcher for implementation convenience.

---

# 16. M5 — trigger allocation

Canonical M5 total:

```text
66 attachments
```

## 16.1 Immediate — 15

Role reconciliation:

```text
Role 1   NativeAddress owner          1
Role 2   ScopedAddress owner          1
Role 3   NativeRef eligibility        2   # Schedule + Actual
Role 5   current binding              2
Role 9   Actual exact basis           2
Role 14  IANA timezone                7
                                      --
                                      15
```

The seven M5 timezone attachments are the non-Occurrence targets already present after M4: Schedule named-zone plus Routine/Event boundary, calendar and quota surfaces. The two remaining timezone attachments belong to M6 Occurrence-generation tables.

Immediate triggers are ordinary `BEFORE ... FOR EACH ROW` triggers according to the exact frozen event masks in the canonical trigger manifest.

## 16.2 Deferred — 51

```text
Role 4   MaterialState totality       6
Role 6   current/history equivalence  7
Role 7   owner creation completeness  4
Role 8   Schedule payload totality    5
Role 10  Session timing totality      3
Role 11  Session pause consistency    2
Role 12  Recurrence aggregate        24
                                      --
                                      51
```

These are `CONSTRAINT TRIGGER` / row-level / deferred according to the frozen DB-U08 + Part16/17 contract.

Global trigger properties to preserve:

```text
all 75 final trigger attachments are ROW-level
no trigger args
no WHEN clauses
ORIGIN enabled
exact immediate/deferred event masks from canonical manifest
```

Do not infer event masks from role names alone; re-read the exact trigger manifest before writing SQL.

## 16.3 Diagnostics

Do not assert failures by matching prose strings.

Frozen SQLSTATE families:

```text
Roles 1..3   → 23503
Roles 4..14  → 23514
```

Tests should assert SQLSTATE and stable database object diagnostics where appropriate, not fragile human text.

---

# 17. M5 — five current views

M5 creates exactly:

```text
schedule_current_placement
actual_current_realization
session_current_timing
routine_current_recurrence
event_current_recurrence
```

They are ordinary automatically-updatable views over the bounded current-control surfaces.

Frozen view properties:

```text
WITH LOCAL CHECK OPTION
security_invoker = false
security_barrier = false
INSTEAD OF triggers = 0
owner = dante_owner
```

Each view has the exact fixed facet semantics already frozen, e.g.:

```text
schedule.placement
actual.realization
session.timing
routine.recurrence
event.recurrence
```

Do not invent projections/defaults from this handoff. Read the canonical Part 9/15/16/17 view contract and exact Dictionary schema before implementation.

SQLAlchemy representation:

```text
apps/backend/src/dante/platform/database/mappings/views.py
VIEW_METADATA
Core-only handles
0 ORM entities
```

---

# 18. M5 — stage-proof / testing philosophy

M5 is more critical than M1–M4 because it activates cross-table semantics. Do not force it into an arbitrary six-test template.

The M5 direct PostgreSQL lane should separate at least:

```text
catalog topology / exact counts
routine owner/security/search_path/privileges
view DDL properties and automatic-updatability
view DML / LOCAL CHECK OPTION behavior
immediate owner/ref/binding/basis/timezone invariants
deferred MaterialState/current-history/owner-completeness invariants
Schedule totality
Session timing/pause invariants
Routine/Event Recurrence aggregate invariants
Part17 NULL/phase/range/current-history hardenings as applicable
runtime/PUBLIC/migrator denial posture
M4 -> M5 -> M4 downgrade boundary
Dictionary reconciliation
fresh database -> single repository head
head -> base -> head
Alembic check / no drift
```

The exact number of selected tests is not frozen yet; do not invent an expected `N/N` before the implementation exists.

Historical stage tests must remain meaningful:

```text
M1 proof stays M1
M2 proof stays M2
M3 proof stays M3
M4 proof stays M4
```

`test_cp6_m4.py` therefore needs only stage-stability maintenance where repository-head Dictionary/view/routine growth would otherwise make its M4 assertions falsely fail. Do not change what M4 proved.

---

# 19. Prepared M5 repository gate from the prior chat

The previous chat reconstructed this exact **path surface**. It was not yet written and the user did not authorize M5 implementation before this handoff request.

Because this handoff itself advances the branch, the next chat MUST replace the old PRE-SCOPE with the new live HEAD after verifying the only expected intervening change is this handoff.

Planning gate:

```text
BRANCH
feature/logical-postgresql

PRE-SCOPE
<LIVE POST-HANDOFF HEAD — MUST BE FETCHED>

STAGE
CP6-M05 / cp6_core_integrity_current_views

CREATE 22
UPDATE 53
DELETE 0
TOTAL 75 paths
```

## 19.1 CREATE — 22

```text
apps/backend/migrations/versions/20260825_05_cp6_core_integrity_current_views.py

apps/backend/src/dante/platform/database/mappings/views.py

apps/backend/tests/integration/database/test_cp6_m5.py

docs/database/dictionary/views/schedule_current_placement.json
docs/database/dictionary/views/actual_current_realization.json
docs/database/dictionary/views/session_current_timing.json
docs/database/dictionary/views/routine_current_recurrence.json
docs/database/dictionary/views/event_current_recurrence.json

docs/database/dictionary/routines/enforce_native_address_owner.json
docs/database/dictionary/routines/enforce_scoped_address_owner.json
docs/database/dictionary/routines/enforce_native_ref_eligibility.json
docs/database/dictionary/routines/enforce_material_state_totality.json
docs/database/dictionary/routines/enforce_current_material_state_binding.json
docs/database/dictionary/routines/enforce_current_history_equivalence.json
docs/database/dictionary/routines/enforce_owner_creation_completeness.json
docs/database/dictionary/routines/enforce_schedule_placement_totality.json
docs/database/dictionary/routines/enforce_actual_realization_basis.json
docs/database/dictionary/routines/enforce_session_timing_totality.json
docs/database/dictionary/routines/enforce_session_pause_consistency.json
docs/database/dictionary/routines/enforce_recurrence_aggregate_integrity.json
docs/database/dictionary/routines/validate_iana_timezone.json

docs/development/backend-cp6-04-m5-core-integrity-current-views.md
```

## 19.2 UPDATE — 53

Repository/test/scope files:

```text
apps/backend/tests/integration/database/test_cp6_m4.py
apps/backend/tests/integration/database/test_migrations.py
docs/database/dictionary/scope.json
```

Fifty owning table Dictionary entries because M5 trigger attachments are embedded in the owning table entries:

```text
docs/database/dictionary/tables/native_address.json
docs/database/dictionary/tables/scoped_address.json
docs/database/dictionary/tables/material_state_address.json
docs/database/dictionary/tables/native_current_material_state.json
docs/database/dictionary/tables/scoped_current_material_state.json

docs/database/dictionary/tables/schedule.json
docs/database/dictionary/tables/schedule_placement_state.json
docs/database/dictionary/tables/schedule_placement_date_state.json
docs/database/dictionary/tables/schedule_placement_floating_local_state.json
docs/database/dictionary/tables/schedule_placement_named_zone_state.json
docs/database/dictionary/tables/schedule_placement_absolute_state.json
docs/database/dictionary/tables/schedule_placement_current_history.json

docs/database/dictionary/tables/actual.json
docs/database/dictionary/tables/actual_realization_state.json
docs/database/dictionary/tables/actual_realization_timing.json
docs/database/dictionary/tables/actual_realization_session_basis.json
docs/database/dictionary/tables/actual_realization_current_history.json

docs/database/dictionary/tables/session.json
docs/database/dictionary/tables/session_timing_state.json
docs/database/dictionary/tables/session_timing_absolute.json
docs/database/dictionary/tables/session_timing_elapsed.json
docs/database/dictionary/tables/session_timing_pause.json
docs/database/dictionary/tables/session_timing_current_history.json

docs/database/dictionary/tables/routine.json

docs/database/dictionary/tables/routine_recurrence_state.json
docs/database/dictionary/tables/routine_recurrence_boundary_state.json
docs/database/dictionary/tables/routine_recurrence_calendar_state.json
docs/database/dictionary/tables/routine_recurrence_calendar_wall_time.json
docs/database/dictionary/tables/routine_recurrence_calendar_weekday.json
docs/database/dictionary/tables/routine_recurrence_calendar_month_day.json
docs/database/dictionary/tables/routine_recurrence_calendar_ordinal_weekday.json
docs/database/dictionary/tables/routine_recurrence_calendar_year_month_day.json
docs/database/dictionary/tables/routine_recurrence_elapsed_state.json
docs/database/dictionary/tables/routine_recurrence_quota_state.json
docs/database/dictionary/tables/routine_recurrence_cyclic_state.json
docs/database/dictionary/tables/routine_recurrence_cycle_position.json
docs/database/dictionary/tables/routine_recurrence_current_history.json

docs/database/dictionary/tables/event_recurrence_state.json
docs/database/dictionary/tables/event_recurrence_boundary_state.json
docs/database/dictionary/tables/event_recurrence_calendar_state.json
docs/database/dictionary/tables/event_recurrence_calendar_wall_time.json
docs/database/dictionary/tables/event_recurrence_calendar_weekday.json
docs/database/dictionary/tables/event_recurrence_calendar_month_day.json
docs/database/dictionary/tables/event_recurrence_calendar_ordinal_weekday.json
docs/database/dictionary/tables/event_recurrence_calendar_year_month_day.json
docs/database/dictionary/tables/event_recurrence_elapsed_state.json
docs/database/dictionary/tables/event_recurrence_quota_state.json
docs/database/dictionary/tables/event_recurrence_cyclic_state.json
docs/database/dictionary/tables/event_recurrence_cycle_position.json
docs/database/dictionary/tables/event_recurrence_current_history.json
```

## 19.3 DELETE

```text
0
```

Before accepting this gate as final in the new chat, mechanically recount it and re-read the exact current repository paths. If the canonical trigger manifest proves an owning table outside this prepared set, stop/re-gate rather than silently adding it.

---

# 20. M5 Dictionary target

M5 must advance current materialization to:

```text
completed stages     CP6-M01..CP6-M05
tables               63
views                 5
routines             13
standalone total     81
triggers             66
physical indexes     87
foreign keys         61
CHECK constraints    109
```

M5 creates exactly:

```text
+5 view entries
+13 routine entries
+66 trigger registrations embedded in owning table entries
```

No speculative M6 view/routine/table/trigger entry should appear early.

Dictionary structural fields must be mechanically reconciled against the real PostgreSQL objects; semantic fields remain human-authored from canonical authority.

---

# 21. M5 ACL posture

M5 does not activate runtime business access.

Continue P0 deny-by-default posture:

```text
PUBLIC/direct runtime/direct migrator access remains denied unless the frozen stage contract explicitly requires technical owner behavior
```

The Dictionary may record final M7 expected grants, but live runtime business DML remains inactive until M7.

Do not grant direct runtime EXECUTE on the 13 integrity routines. They are invoked by triggers, not exposed as runtime procedure APIs.

---

# 22. Part-17 hardening — do not lose it in M5 implementation

When implementing recurrence/current-history integrity, explicitly preserve Part 17's second-tombstone repairs.

At minimum re-read and implement exactly:

```text
recurrence selector-family matrix
pattern_anchor presence/absence rules
interval_count phase semantics
exact monthly/yearly selector meaning
anchor_step lattice
wall-time membership
boundary-role cardinality
range_kind restrictions
boundary-kind compatibility
effective membership semantics
expected-count deterministic ordering
quota phase / period coordinate
elapsed exact coordinate
cyclic exact coordinate
governing Recurrence membership
current-history one-way lifecycle / narrowed column-scoped insertion semantics
NULL-safe CHECK-derived assumptions
```

Do not weaken these into broad family-only validation or insertion-order/UUID-order logic.

---

# 23. Part-18 security hardening — do not lose it in M5 implementation

For migration/routine source:

```text
business/user values are bound parameters/data
identifiers are static or exact bounded identifiers
no arbitrary SQL fragments
no generic PL/pgSQL dynamic EXECUTE baseline
schema-qualify DANTE relations/routines where resolution matters
trusted search_path = pg_catalog,dante,pg_temp
pg_temp explicitly last
SECURITY INVOKER only
PUBLIC/runtime/migrator direct routine EXECUTE denied
```

Security testing is construction proof + negative behavior, not a single quote/semicolon payload.

Do not create `SECURITY DEFINER` as a shortcut around ACL design.

---

# 24. Quality bar / implementation methodology

For every M5 block:

```text
A. derive exact behavior from canonical authority;
B. reconcile against current real M1–M4 schema/mappings/Dictionary;
C. prefer declarative constraints where already available; M5 triggers exist only for genuine cross-row/cross-table/deferred semantics;
D. keep every trigger lookup bounded/index-backed;
E. preserve truthful history/current semantics;
F. preserve transaction/commit-time behavior;
G. do not add speculative indexes — M5 index delta is exactly zero;
H. do not invent generic Repository/UoW/BaseService/Recurrence root abstractions;
I. do not activate runtime business grants before M7;
J. encode exact SQLSTATE/object diagnostics rather than fragile error text;
K. make downgrade remove views/triggers/routines in dependency-safe order and return exactly to M4;
L. make old stage proofs stage-stable rather than rewriting history;
M. prove direct PostgreSQL behavior before closure.
```

The user expects large-product engineering quality, not demo-level code. Do not be a yes-man; if the frozen gate contains a real contradiction, stop, show the evidence and repair the gate rather than implementing blindly.

---

# 25. Known anti-patterns / failure modes from this chat

Do not repeat:

```text
1. counting pg_constraint without PostgreSQL-18 contype='n' handling;
2. validating only path names after Git tree assembly — verify file content identity too;
3. weakening tests after a red result instead of finding whether DDL/Dictionary/proof is wrong;
4. assuming a correct JSON blob under the wrong filename is harmless;
5. claiming cleanup/CI that was not separately observed;
6. moving a branch ref without a final race-check;
7. silently starting persistent PostgreSQL or treating disposable tests as persistent materialization;
8. carrying an old PRE-SCOPE across a documentation handoff commit;
9. using chat memory as authority when canonical Parts 17/18 contain narrow supersessions;
10. changing historical M1–M4 meaning merely because repository head grows.
```

---

# 26. What is NOT done yet

As of this handoff:

```text
M5 migration                     NOT CREATED
M5 views                         NOT CREATED
M5 integrity routines            NOT CREATED
M5 trigger attachments           NOT CREATED
M5 Dictionary view entries       NOT CREATED
M5 Dictionary routine entries    NOT CREATED
M5 trigger registrations         NOT CREATED
M5 PostgreSQL direct proof       NOT RUN
M5 closure                       NOT EARNED

M6 occurrence-generation         NOT STARTED
M7 runtime ACL activation        NOT STARTED
CP6-05 whole direct QA/closure   NOT STARTED
protected-main realignment       NOT PERFORMED in this workstream
first product vertical           NOT PART OF current DB materialization step
```

Do not describe M5 as implemented merely because the gate is detailed.

---

# 27. What comes after M5 — only for orientation

M6 is `cp6_occurrence_generation` and will later add:

```text
5 Occurrence-generation tables
8 indexes
final integrity routine enforce_occurrence_generation_integrity
remaining 9 triggers
```

After M6 global baseline becomes:

```text
68 tables
5 views
14 routines
75 triggers
95 indexes
```

M7 then creates no structural object; it activates the exact frozen runtime ACL matrix.

Do not open M6 or M7 before M5 earns its own direct PostgreSQL PASS and formal closure.

---

# 28. Expected next-chat behavior

The first useful response from the next chat should be an **alignment report**, not code.

It should say, after actually reading/inspecting the repo:

```text
- live branch HEAD
- whether only this handoff follows M4 closure or whether anything else moved
- P0/M1/M2/M3/M4 status confirmed
- current Dictionary counts confirmed
- M5 revision/down_revision confirmed
- 13 routines / 5 views / 66 triggers confirmed from canonical docs
- 75-path prepared gate mechanically rechecked
- any discrepancy found
```

Then it should present the re-anchored M5 gate and wait for the user's explicit `vai` before mutation.

Do not start a new branch, do not touch frontend, do not merge main, do not materialize a persistent local DB, and do not silently widen M5.

---

# 29. Compact resume block

```text
REPO
MattiaRubino/dante

BRANCH
feature/logical-postgresql

BACKEND WORKTREE
~/projects/dante

PRE-HANDOFF M4 CLOSURE HEAD
93d053a7393f57fc824a733c523332f158901757

CP6-03
CLOSED / GATE03 PASS / RATIFIED

P0
CLOSED / 22/22 DIRECT POSTGRESQL PASS

M1
CLOSED / 28/28 DIRECT POSTGRESQL PASS

M2
CLOSED / first 33/34 due PG18 proof bug / repaired / final 34/34 PASS

M3
CLOSED / first 39/40 due Dictionary placement / repaired / final 40/40 PASS / cleanup 0 residual containers

M4
CLOSED / 46/46 PASS / 34.28s / coverage 95.57% / cleanup not separately asserted

CURRENT MATERIALIZATION
63 tables
5? NO — views still 0 before M5
13? NO — routines still 0 before M5
66? NO — triggers still 0 before M5
87 indexes
61 FK
109 CHECK
2 UQ
63 Row mappings

NEXT
M5 cp6_core_integrity_current_views
20260825_05
parent 20260825_04

M5 DELTA
0 tables
0 indexes
+5 views
+13 routines
+66 triggers

M5 GATE PREPARED
22 CREATE
53 UPDATE
0 DELETE
75 paths total

M5 WRITE
NOT YET AUTHORIZED / NOT WRITTEN

NEXT CHAT MUST
fetch live HEAD → read this file → read canonical Parts 1–18 + closure docs → recheck 75-path gate → ask/await explicit user vai → implement → exact compare → direct PostgreSQL proof
```
