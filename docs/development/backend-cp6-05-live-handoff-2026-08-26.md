# CP6-05 FINAL LIVE HANDOFF — 2026-08-26

> **CURRENT CROSS-CHAT RESUME — CP6 CLOSED / CONCRETE POSTGRESQL DATABASE PASS**  
> This handoff is the current non-normative cross-chat resume for the completed PostgreSQL workstream. It supersedes earlier CP6-03/04 handoff **status/routing prose only**. Historical derivation, failed runs, repair evidence, canonical Domain/Logical/Physical authority, Database Architecture & Reference Parts 1–19, Database Dictionary, CP6-01/02/03 closure records and applied Alembic history remain preserved.

**Status:** CURRENT / CROSS-CHAT CONTINUITY / CP6 CLOSED  
**Repository:** `MattiaRubino/dante`  
**Branch:** `feature/logical-postgresql`  
**Backend worktree:** `~/projects/dante`  
**Frontend worktree:** `~/projects/dante-frontend` — DO NOT TOUCH for this workstream  
**Accepted implementation HEAD:** `22bbc078391d52c43665474bf465593d6225106e`  
**Persistent LOCAL PostgreSQL:** 18.6 / revision `20260826_08`  
**Protected `main`:** not yet aligned or merged; separate explicit gate required.

---

## 1. Final CP6 state

```text
CP6-00  COMPLETE
CP6-01  CLOSED / GATE 01 PASS
CP6-02  CLOSED / GATE 02 PASS
CP6-03  CLOSED / GATE 03 PASS
CP6-04  CLOSED / MATERIALIZATION PASS
CP6-05  CLOSED / DIRECT QA PASS

CP6      CLOSED / CONCRETE POSTGRESQL DATABASE PASS
```

The first product vertical remains a separate post-CP6 phase.

---

## 2. Final accepted database surface

```text
tables              68
ordinary views       5
integrity routines  14
triggers             75
  immediate          18
  deferred           57
physical indexes     95
foreign keys         68
check constraints   120
SQLAlchemy Row maps  68
Core view handles     5
Dictionary entries   87
```

No universal Entity/Thing/Relationship/EAV root was introduced.

Canonical reference families remain distinct:

```text
NativeRef
ScopedRecordRef
MaterialStateRef
ExternalRef
```

Scoped owners remain Schedule/Actual only. Baseline MaterialState facets remain:

```text
schedule.placement
actual.realization
session.timing
routine.recurrence
event.recurrence
```

---

## 3. Final migration state

Historical CP6 materialization DAG:

```text
P0 provisioning/security
M1 20260825_01 cp6_native_identity_address
M2 20260825_02 cp6_scoped_material_control
M3 20260825_03 cp6_schedule_actual_session
M4 20260825_04 cp6_recurrence
M5 20260825_05 cp6_core_integrity_current_views
M6 20260826_06 cp6_occurrence_generation
M7 20260826_07 cp6_runtime_acl_activation
```

Final forward-only CP6-05 correction:

```text
20260826_08 cp6_final_qa_hardening
```

`20260826_08` is not a Dictionary materialization stage and does not rewrite M1..M7 history. Applied migrations remain immutable under MIG-02.

Persistent LOCAL is now:

```text
PostgreSQL              18.6
Alembic revision         20260826_08
volume                   postgres-data retained
host                     127.0.0.1:5432
database                 dante
```

---

## 4. Final security/runtime posture

Application roles:

```text
dante_owner      NOLOGIN / password NULL
dante_migrator   LOGIN NOINHERIT
dante_runtime    LOGIN NOINHERIT
```

Exact DANTE membership graph:

```text
dante_owner → dante_migrator
INHERIT FALSE
SET TRUE
ADMIN FALSE
```

No other DANTE-role membership edge exists.

Runtime posture includes:

- SELECT on all 68 DANTE tables;
- table-level INSERT on exactly 49 tables;
- column INSERT on the five current-history tables;
- 14 no-INSERT tables;
- no table-level UPDATE;
- only `UPDATE(current_until_at)` on the five current-history tables;
- no base-table DELETE;
- five bounded current views with exact column-level INSERT/UPDATE;
- DELETE only on Schedule/Actual current views;
- all 14 integrity routines directly uncallable by runtime/migrator/PUBLIC;
- runtime denied access to `dante.alembic_version`;
- trusted `search_path = pg_catalog,dante,pg_temp`;
- SCRAM-safe login credentials;
- transaction-scoped advisory locking for recurrence/occurrence-generation concurrency.

---

## 5. CP6-05 substantive correction

The only substantive final database defect found by CP6-05 clean-room QA was the missing independent source occurrence-generation advisory lock in Role-13.

The forward migration `20260826_08` repaired it without changing topology:

- `recurrence_generated` resolves Routine/Event source family;
- it independently acquires the exact source occurrence-generation xact advisory lock;
- application lock acquisition remains compatible/reentrant;
- concurrent duplicate generation without the application lock is serialized and one conflicting transaction is rejected with SQLSTATE `23514`;
- no fake UPDATE, row-lock table, new routine, new index or new semantic owner was introduced.

The advisory key contract is frozen as:

```text
domain prefix = b"dante-lock-v2"
input         = prefix || UUID canonical 16 raw bytes
hash          = SHA-256
digest56      = first 7 bytes, unsigned big-endian
lock_key      = (namespace_code << 56) | digest56
```

---

## 6. Final direct acceptance evidence

Exact implementation candidate:

```text
22bbc078391d52c43665474bf465593d6225106e
```

Quality / build:

```text
uv 0.12.5                         PASS
locked environment                PASS
ruff format --check               PASS — 44 files formatted
ruff check                        PASS
mypy strict                       PASS — 40 source files
fast pytest                       37 / 37 PASS
uv build                          PASS — wheel + sdist
```

Disposable real PostgreSQL 18.6 acceptance:

```text
113 collected
37 deselected
76 selected
76 passed
0 failed
54.89s
coverage 95.40% evidence only
```

Persistent LOCAL acceptance:

```text
pre-revision                      20260826_07
provisioning/security             PASS
upgrade                           20260826_07 → 20260826_08
alembic check                     PASS
final topology                    68|5|14|75|95|68|120
final role/security posture       PASS
```

Closure tail:

```text
Dictionary JSON-Schema            PASS
compose down/up without volumes   PASS
revision survives restart         20260826_08
topology survives restart         68|5|14|75|95|68|120
GET /health/live                  200 {"status":"ok"}
GET /health/ready                 200 {"status":"ready"}
repository candidate guard        PASS
```

The final closure evidence is recorded in `docs/development/backend-cp6-05-whole-database-qa.md`.

---

## 7. Historical failure/repair evidence must remain truthful

Do not rewrite CP6 as first-pass green.

Preserved materialization/QA history includes, among other evidence:

- P0 first proof failed one global-default check and passed after repair;
- M2 first proof exposed catalog NOT-NULL representation mismatch and passed after proof repair;
- M3 filename/content permutation was repaired before 40/40 PASS;
- M7 first candidate passed 70/71 and exposed a Role-6 history dispatcher bug;
- first M7 repair then hit psycopg `%_` placeholder interpretation;
- second M7 repair reached 71/71 PASS;
- CP6-05 final audit found Role-13 concurrency defense plus proof/documentation defects;
- backend final quality initially failed Ruff lint/format and then mypy typing before all official quality gates became green;
- the final exact candidate passed all disposable PostgreSQL and persistent-LOCAL closure evidence.

Failed evidence is evidence and remains part of the project history.

---

## 8. Authority and continuation rules

Authority order remains:

```text
live repository + applied migrations/tests
→ closed Domain
→ closed Whole Logical
→ accepted Physical
→ CP6-01
→ CP6-02 / ADR-010
→ Database Architecture & Reference Parts 1–19
→ Database Dictionary
→ CP6-05 final closure evidence
→ this handoff
→ chat memory
```

Workstream safety remains:

```text
repo:      MattiaRubino/dante
branch:    feature/logical-postgresql
worktree:  ~/projects/dante
```

Do not create another PostgreSQL feature branch/worktree merely because CP6 is closed. Do not touch `~/projects/dante-frontend` from this workstream.

---

## 9. Exact next phase — protected-main alignment preparation

CP6 implementation is closed on `feature/logical-postgresql`, but protected `main` is not yet integrated.

The next operation is a **separately gated integration-preparation phase**, not new database development.

Before any merge/rebase/ref move:

1. fetch and identify exact live protected-`main` HEAD;
2. compare `main...feature/logical-postgresql` from the real merge-base;
3. inventory commits and changed paths;
4. determine whether `main` moved in overlapping backend/database/documentation paths while CP6 was in progress;
5. perform a semantic conflict/risk review, not just a textual conflict check;
6. verify migration DAG/head relation and ensure no competing Alembic history exists on `main`;
7. determine the protected repository integration mechanism (PR/checks/ruleset);
8. construct an exact integration gate with source SHA, target SHA and allowed action;
9. only after explicit user authorization perform the alignment/merge;
10. re-run the required integrated CI/post-merge proof before declaring `main` aligned.

No merge/rebase/realignment to `main` is authorized by this handoff itself.

---

## 10. Resume sentence

A fresh session should resume from:

```text
CP6 is CLOSED on feature/logical-postgresql.
Accepted implementation HEAD = 22bbc078391d52c43665474bf465593d6225106e.
Persistent LOCAL PostgreSQL 18.6 is at 20260826_08 and directly verified.
Next work = protected-main alignment PREPARATION ONLY.
First action = read live main, merge-base, branch diff, migration DAG and repository protection state.
Do not merge/rebase/realign until a new explicit user gate authorizes it.
```
