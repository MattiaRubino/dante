# CP6-04 M7 — Runtime ACL Activation

**Stage:** `CP6-M07 / cp6_runtime_acl_activation`  
**Revision:** `20260826_07`  
**Down revision:** `20260826_06`  
**Status:** IMPLEMENTED / DIRECT POSTGRESQL ACCEPTANCE REQUIRED

## Scope

M7 activates the final runtime PostgreSQL capability matrix without changing the frozen structural topology.

Structural surface remains exactly:

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

M7 materializes the final Part-12 / Part-17 privilege contract:

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

## Role-13 runtime-compatibility repair

M6's quota validator still used `SELECT ... FOR UPDATE` on immutable `routine` / `event` owner rows. PostgreSQL requires UPDATE privilege for that row lock, which would contradict the frozen ACL matrix.

M7 therefore forward-repairs the existing `enforce_occurrence_generation_integrity()` definition without changing its name, signature, owner, security posture, trigger attachments or routine count. The incompatible owner-row locks are removed. Accepted occurrence-generation operations use the frozen Part-14 transaction advisory-lock boundary instead:

- Routine: namespaces 4 + 6;
- Event: namespaces 5 + 7;
- one-argument positive signed-bigint key;
- high 7 bits namespace + low 56-bit BLAKE2b digest of UUID bytes;
- deterministic dedupe/sort/acquire under the caller-owned transaction.

`dante/platform/database/locking.py` materializes that already-frozen technical helper. It performs no transaction begin/commit/rollback and creates no persisted object.

M7 downgrade restores the exact M6 owner-row lock definition and revokes all M7 business ACLs.

## Dictionary repair

Part 17 narrowed the five history INSERT grants after the earlier Part-12 matrix. Their Dictionary entries are reconciled in the same M7 candidate to the exact three-column INSERT grant plus `UPDATE(current_until_at)`.

The global `scope.json` remains at accepted M6 until direct PostgreSQL M7 acceptance succeeds. M7 closure will then mark the Dictionary `materialized` and add `CP6-M07` to completed stages.

## Proof requirement

M7 is not CLOSED until a fresh user-executed PostgreSQL 18.6 run of:

```text
uv run pytest -m postgres -vv
```

passes against the published candidate. Required M7 evidence includes exact table/view/column ACL catalogs, direct-routine denial, runtime bounded-current replacement, runtime quota materialization under advisory locks, no owner UPDATE privilege, lock-key golden vectors, M7→M6 downgrade, fresh→head, head→base→head, Alembic drift, provisioning non-broadening, runtime and transaction tests.

## Explicitly out of scope

- persistent LOCAL PostgreSQL materialization;
- frontend;
- protected-main integration;
- product authorization/visibility semantics;
- CP6-05 performance/stress evidence beyond the bounded M7 runtime acceptance required to close CP6-04 materialization.
