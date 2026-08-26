# CP6-04 M7 — Runtime ACL Activation

**Stage:** `CP6-M07 / cp6_runtime_acl_activation`  
**Revision:** `20260826_07`  
**Down revision:** `20260826_06`  
**Status:** CLOSED / DIRECT POSTGRESQL PASS

## Final accepted surface

M7 activates the final runtime PostgreSQL capability matrix without changing the frozen structural topology:

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

## Runtime ACL matrix

The accepted M7 runtime contract is:

- `SELECT` on all 68 DANTE-owned tables;
- table-level `INSERT` on exactly 49 tables;
- column-scoped `INSERT(owner_ref, material_state_ref, current_from_at)` on the five current-history tables;
- no `INSERT` on the exact 14 no-create baseline tables;
- zero table-level runtime `UPDATE`;
- `UPDATE(current_until_at)` only on the five current-history tables;
- zero runtime `DELETE` on base tables;
- five bounded current views expose exact column-scoped INSERT/UPDATE;
- `DELETE` is granted only on Schedule/Actual current views;
- direct base current-control mutation remains denied;
- direct EXECUTE on all 14 integrity routines remains denied to runtime, migrator and PUBLIC;
- runtime remains denied all access to `dante.alembic_version`.

## Runtime-compatibility repairs accepted in M7

### Role-13 occurrence-generation locking

M6 quota validation used `SELECT ... FOR UPDATE` on immutable Routine/Event owner rows. That would require UPDATE privilege and violate the final ACL matrix. M7 therefore keeps owner rows immutable and moves accepted occurrence-generation operations to the frozen Part-14 transaction advisory-lock boundary. Routine/function count, signatures, owner and security posture remain unchanged.

### Role-6 current-history dispatcher

The first direct M7 runtime replacement run exposed a real PL/pgSQL record-dispatch bug in `enforce_current_history_equivalence()`: combined `TG_TABLE_NAME='x' AND NEW.<table-specific-field>` expressions could resolve a field that does not exist for another history trigger record. M7 forward-repairs this into a table-first nested dispatcher so each branch references only fields valid for that history table. The invariant is unchanged.

### psycopg function-definition re-emission

The first Role-6 repair then exposed a migration-driver issue: `pg_get_functiondef()` returned a function containing `LIKE '%_current_history'`; re-emitting that definition through psycopg treated `%_` as an invalid placeholder. M7 now escapes percent signs only at the driver re-emission boundary. Database semantics are unchanged.

## Dictionary repair

Part 17 narrowed the five history INSERT grants after the earlier Part-12 matrix. Their Dictionary entries are reconciled to the exact three-column INSERT grant plus `UPDATE(current_until_at)`. Global Dictionary scope is promoted to `materialized` only after the final direct PostgreSQL PASS.

## Acceptance evidence

Final accepted implementation HEAD:

```text
7fb54f267e9e91512001e3ea6c7cc02630097941
```

User-executed command from `apps/backend`:

```text
uv run pytest -m postgres -vv
```

Final observed result:

```text
108 collected
37 deselected
71 selected
71 passed
0 failed
51.14s
coverage 94.14%
```

The accepted run includes:

- M1–M6 regression acceptance;
- exact M7 table/view/column ACL catalogs;
- direct routine denial;
- bounded current recurrence replacement as `dante_runtime`;
- runtime quota occurrence generation using advisory locks without owner UPDATE;
- lock-key contract/golden behavior;
- M7→M6 downgrade restoration;
- fresh database → single repository head;
- head→base→head round trip;
- Alembic drift check;
- provisioning privilege hardening/non-broadening;
- runtime connection/recovery/readiness tests;
- real transaction commit/rollback/flush/savepoint tests.

## Preserved failed-run history

M7 was not a synthetic first-pass green stage:

1. first candidate: `70 passed / 1 failed`; bounded recurrence replacement exposed the Role-6 record-field bug;
2. first repair: migration failed before acceptance because psycopg interpreted `%_` in the reconstructed function definition as an invalid placeholder;
3. second repair at `7fb54f267e9e91512001e3ea6c7cc02630097941`: `71/71 PASS`.

The failed evidence is intentionally retained because both failures identified implementation defects; tests were not weakened to obtain green status.

## Next boundary

M7 is CLOSED. Repository schema/ACL materialization M1–M7 is complete. The PostgreSQL workstream is not yet considered operationally finished: next comes explicit persistent LOCAL PostgreSQL materialization, fresh→head migration, backend/runtime smoke, volume/restart persistence verification and optional DBeaver inspection before the explicit gate toward protected `main`.
