# CP6-04 CURRENT LIVE HANDOFF — 2026-08-26

> **CURRENT CROSS-CHAT RESUME — P0/M1/M2/M3/M4/M5 CLOSED / M6 NEXT**  
> This handoff supersedes `backend-cp6-04-live-handoff-2026-08-25.md` only for current phase/status/routing. It does **not** supersede the accepted Domain/Logical/Physical models, CP6-01, CP6-02, Gate-03, Database Architecture & Reference Parts 1–18, the Database Dictionary contract, or any closed stage record.

**Status:** CURRENT / CROSS-CHAT CONTINUITY / NON-NORMATIVE  
**Repository:** `MattiaRubino/dante`  
**Branch:** `feature/logical-postgresql`  
**Backend worktree:** `~/projects/dante`  
**Frontend worktree:** `~/projects/dante-frontend` — DO NOT TOUCH for this PostgreSQL workstream  
**Current phase:** CP6-04 — Whole DANTE Database Materialization  
**Current materialization:** P0 + M1 + M2 + M3 + M4 + M5 CLOSED / DIRECT POSTGRESQL PASS  
**Next stage:** CP6-M06 — occurrence generation materialization  
**Persistent LOCAL PostgreSQL database:** do not start/touch implicitly; disposable PostgreSQL acceptance infrastructure is separate.

---

## 1. Live closure point

The final M5 implementation/repository-consistency candidate was:

```text
92939004cd2a5437238f2574b47c4f6d3b2ea00a
feat: complete CP6-04 M5 repository consistency
```

The user then executed from `~/projects/dante/apps/backend`:

```text
uv run pytest -m postgres -vv
```

Observed result on that exact SHA:

```text
92 collected
37 deselected
55 selected
55 passed
0 failed
80.13s
coverage 95.63%
```

The run included M1–M5 PostgreSQL acceptance, M5 Dictionary reconciliation, migration fresh→head, head→base→head, Alembic drift check, privileges, runtime, and transaction tests.

This handoff is committed after the tested SHA. Therefore the **next chat MUST fetch live branch HEAD and use that live HEAD as the next PRE-SCOPE**. Do not reuse `92939004...` as a future write gate.

---

## 2. M5 CLOSED state

Revision:

```text
20260825_05
cp6_core_integrity_current_views
DOWN: 20260825_04
```

M5 final materialized surface:

```text
tables              63
views                 5
routines             13
triggers             66
  immediate          15
  deferred           51
physical indexes     87
foreign keys         61
check constraints   109
SQLAlchemy Row maps  63
Core view handles     5
Dictionary standalone entries 81
```

M5 adds no business tables and no runtime ACL activation.

### M5 views

```text
schedule_current_placement
actual_current_realization
session_current_timing
routine_current_recurrence
event_current_recurrence
```

They are ordinary automatically-updatable PostgreSQL views, three columns each, fixed facet predicate/default, `WITH LOCAL CHECK OPTION`, `security_invoker=false`, `security_barrier=false`, owned by `dante_owner`, with no INSTEAD OF triggers. SQLAlchemy uses isolated `VIEW_METADATA`; the views are not ORM entities.

### M5 routines

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

All are `SECURITY INVOKER`, `VOLATILE`, `PARALLEL UNSAFE`, non-leakproof, owned by `dante_owner`, with function `search_path = pg_catalog,dante,pg_temp`; direct EXECUTE remains denied to PUBLIC/runtime/direct migrator.

### DB-U25 repairs carried by M5

M5 forward-repairs seven already-named CHECK constraints without changing counts:

1. `ck_session_timing_absolute_end_precision` — explicit NULL-safe end/precision pairing;
2. Routine/Event `*_calendar_state_step_unit` — `step_unit_code IS NOT NULL` for `anchor_step`;
3. Routine/Event `*_quota_state_week_start` — `week_start IS NOT NULL` for weekly quota periods;
4. Routine/Event `*_elapsed_state_elapsed_positive` — finite positive value plus `elapsed_seconds = trunc(elapsed_seconds, 6)`.

Downgrade M5→M4 restores the historical M4 CHECK expressions after removing M5 views/triggers/routines.

The SQLAlchemy mappings and Dictionary are aligned with these final Part-17 forms.

---

## 3. Authority / safety rules remain mandatory

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

Do not create a new branch/worktree/clone. New chat != new branch. Do not touch `~/projects/dante-frontend`. Do not merge/rebase/realign `main` without an explicit user gate.

Before every repository mutation, state and freeze:

```text
BRANCH
PRE-SCOPE
CREATE
UPDATE
DELETE
PURPOSE
EXPLICITLY OUT OF SCOPE
```

Immediately before mutation re-check live HEAD == PRE-SCOPE. If it moved, stop and inspect. After mutation perform remote readback and exact PRE-SCOPE→HEAD compare; unexpected paths must be zero.

Never claim a test PASS that was not actually observed. Preserve failed-run/repair history instead of rewriting it into a synthetic first-pass green result.

---

## 4. Canonical model reminders

Do not collapse the model while moving into M6:

- 57 Domain concepts are not 57 persistence roots/tables;
- native owners remain exactly: `person, living_referent, asset, place, content_artifact, collective, possibility, goal, plan, activity, event, routine, occurrence, session, observation`;
- reference families remain `NativeRef`, `ScopedRecordRef`, `MaterialStateRef`, `ExternalRef`;
- scoped owner families remain Schedule/Actual only;
- baseline MaterialState facets remain `schedule.placement`, `actual.realization`, `session.timing`, `routine.recurrence`, `event.recurrence`;
- Recurrence remains owner-bound to Routine/Event; there is no independent `dante.recurrence` root;
- PostgreSQL remains the sole canonical persistence/material-history authority;
- no generic Entity/Thing/EAV/generic relationship/generic rule/fact/version roots;
- current state is explicit, never inferred as latest timestamp/UUID;
- current history remains one-way lifecycle;
- runtime business ACL activation remains M7.

---

## 5. M6 routing

M6 is the next authorized design stage, but **no M6 write is implied by this handoff**.

The frozen final migration DAG remains:

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

M6 is the occurrence-generation layer. The accepted baseline expects M6 to add the remaining five tables and the final occurrence-generation integrity routine/trigger layer; exact table/index/FK/CHECK/trigger names and the write-path gate MUST be re-read from Parts 9–18 and the current Dictionary before mutation rather than reconstructed from memory.

Before M6 implementation, the next chat must at minimum:

1. fetch live branch HEAD;
2. read this handoff and the M5 closure record;
3. inspect revision `20260825_05`, current mappings, Dictionary scope and PostgreSQL tests;
4. re-read canonical Parts 9/10/11/12/13/14/15/16/17/18 for the exact M6 surface;
5. produce an exact M6 write gate against the live HEAD;
6. wait for the user's explicit authorization before first M6 mutation;
7. require a fresh real PostgreSQL acceptance run before M6 can close.

---

## 6. Explicitly still out of scope

- CP6-M07 runtime ACL activation;
- frontend work;
- protected-main integration;
- silently starting/materializing persistent local PostgreSQL;
- workflow/orchestration/product-layer semantics not frozen by the database architecture.

M5 is CLOSED. Resume from M6 only after live HEAD verification and an explicit M6 gate.
