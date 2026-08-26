# CP6-04 CURRENT LIVE HANDOFF — 2026-08-26

> **CURRENT CROSS-CHAT RESUME — P0/M1/M2/M3/M4/M5/M6/M7 CLOSED / PERSISTENT LOCAL NEXT**  
> This handoff supersedes earlier CP6-04 live handoff status/routing only. Canonical Domain/Logical/Physical models, CP6-01, CP6-02, Gate-03, Database Architecture & Reference Parts 1–18 and the Database Dictionary contract remain authoritative.

**Status:** CURRENT / CROSS-CHAT CONTINUITY / NON-NORMATIVE  
**Repository:** `MattiaRubino/dante`  
**Branch:** `feature/logical-postgresql`  
**Backend worktree:** `~/projects/dante`  
**Frontend worktree:** `~/projects/dante-frontend` — DO NOT TOUCH for this PostgreSQL workstream  
**Current phase:** CP6-04 — Whole DANTE Database Materialization  
**Current materialization:** P0 + M1 + M2 + M3 + M4 + M5 + M6 + M7 CLOSED / DIRECT POSTGRESQL PASS  
**Next step:** explicit persistent LOCAL PostgreSQL materialization and verification  
**Protected `main`:** no merge/rebase/realignment without explicit user gate.

---

## 1. Accepted implementation boundary

Final tested M7 implementation HEAD:

```text
7fb54f267e9e91512001e3ea6c7cc02630097941
fix: escape function definitions for psycopg in M7
```

User-executed command from `~/projects/dante/apps/backend`:

```text
uv run pytest -m postgres -vv
```

Observed on that exact SHA:

```text
108 collected
37 deselected
71 selected
71 passed
0 failed
51.14s
coverage 94.14%
```

The run includes M1–M7 acceptance, final ACL/runtime behavior, M7→M6 downgrade, fresh→head, head→base→head, Alembic drift, privileges, runtime and transaction tests.

Do not rewrite M7 as first-pass green. Preserved history:

1. first M7 candidate: 70/71, Role-6 history record-field bug exposed;
2. first repair: migration blocked by psycopg `%_` placeholder interpretation during function-definition re-emission;
3. second repair at `7fb54f267e9e91512001e3ea6c7cc02630097941`: 71/71 PASS.

---

## 2. Final materialized repository surface

```text
tables              68
views                 5
routines             14
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

Final migration DAG:

```text
P0 provisioning
M1 cp6_native_identity_address
M2 cp6_scoped_material_control
M3 cp6_schedule_actual_session
M4 cp6_recurrence
M5 cp6_core_integrity_current_views
M6 cp6_occurrence_generation
M7 cp6_runtime_acl_activation
```

Database Dictionary scope is `materialized` and completed stages are CP6-M01 through CP6-M07.

---

## 3. Final M7 security/runtime posture

M7 activates the frozen runtime capability matrix:

- SELECT on all 68 DANTE tables;
- table-level INSERT on exactly 49 tables;
- column-level INSERT on exactly five current-history tables;
- 14 no-INSERT tables;
- no table-level runtime UPDATE anywhere;
- only `UPDATE(current_until_at)` on the five current-history tables;
- no runtime DELETE on base tables;
- five bounded current views with exact column-level INSERT/UPDATE;
- DELETE only on Schedule/Actual current views;
- all 14 integrity routines remain directly uncallable by runtime/migrator/PUBLIC;
- `dante.alembic_version` remains inaccessible to runtime;
- occurrence-generation quota concurrency uses the accepted advisory-lock boundary without granting fake UPDATE capability on Routine/Event owners.

Role-6 current-history dispatch was forward-repaired in M7 to use table-first nested branches so trigger records never resolve fields belonging to another history table.

---

## 4. Authority / safety rules

Authority:

```text
live repository + canonical docs > this handoff > chat memory
```

Work only on:

```text
repo:    MattiaRubino/dante
branch:  feature/logical-postgresql
backend: ~/projects/dante
```

Do not create a new branch/worktree/clone. Do not touch the frontend worktree. Do not merge/rebase/realign `main` without explicit user authorization.

Before repository mutation, preserve branch/PRE-SCOPE/path gate discipline and perform post-write compare with zero unexpected paths.

Never claim PASS without observed output. Preserve failed-run and repair evidence.

---

## 5. Persistent LOCAL PostgreSQL is now the next authorized work

Repository LOCAL infrastructure already exists:

```text
infra/compose/local.yaml
infra/local/postgres/Dockerfile
infra/local/postgres/initdb/
```

Current Compose baseline:

```text
PostgreSQL image   dante-postgres-local:18.6
host endpoint      127.0.0.1:5432
database           dante
persistent volume  postgres-data:/var/lib/postgresql
```

The next work is explicit operational materialization, not another schema milestone:

1. ensure/generate LOCAL admin, migrator and runtime secrets without committing them;
2. validate/build/start the existing Compose PostgreSQL service;
3. run application role/schema provisioning against LOCAL;
4. run Alembic fresh→head using `dante_migrator`, never `postgres`/runtime;
5. verify repository head is `20260826_07` and final topology/ACLs are present;
6. smoke backend connection as exact `dante_runtime`;
7. stop/restart Compose without `--volumes` and verify roles/schema/data persist;
8. optionally verify through DBeaver/PyCharm Database Tools on Windows;
9. mark DATABASE OPERATIVE LOCAL;
10. only then consider the explicit gate toward protected `main`.

Do not run acceptance pytest against the ordinary LOCAL cluster: PostgreSQL acceptance uses isolated disposable infrastructure because roles are cluster-global.

---

## 6. Current closure meaning

M1–M7 implementation/materialization is CLOSED. The broader PostgreSQL phase is intentionally not considered operationally finished until persistent LOCAL verification succeeds. No protected-main integration is authorized yet.
