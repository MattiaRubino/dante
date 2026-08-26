# CP6-04 M6 — Occurrence Generation

**Stage:** `CP6-M06 / cp6_occurrence_generation`  
**Revision:** `20260826_06`  
**Down revision:** `20260825_05`  
**Status:** CLOSED / DIRECT POSTGRESQL 18.6 PASS

## Scope

M6 materializes the final five DANTE-owned business tables and the bounded Role-13 occurrence-generation integrity layer. It does not activate runtime business ACLs; that remains M7.

M6 adds exactly:

- 5 tables: `occurrence_generation`, `occurrence_generation_calendar`, `occurrence_generation_elapsed`, `occurrence_generation_quota`, `occurrence_generation_cyclic`;
- 1 trigger function: `enforce_occurrence_generation_integrity`;
- 9 trigger attachments: 3 immediate `BEFORE` + 6 deferred constraint triggers;
- 8 physical indexes: 5 PK-backed + the source/governing-state, governing-state and quota-period indexes;
- 7 foreign keys;
- 11 CHECK constraints;
- 5 SQLAlchemy ORM row mappings;
- 5 new table Dictionary entries, 1 new routine entry, and the M6 trigger attachment on the existing `occurrence` entry.

Cumulative structural surface after M6:

```text
tables              68
views                5
routines            14
triggers            75
  immediate         18
  deferred          57
physical indexes    95
foreign keys        68
check constraints  120
SQLAlchemy Row maps 68
Core view handles    5
Dictionary entries  87
```

## Role-13 contract

For `origin_code='explicit_extra'`, `governing_recurrence_state_ref` is NULL and no generated-coordinate child exists.

For `origin_code='recurrence_generated'`, the source resolves only to Routine/Event; the governing MaterialStateRef belongs to that exact source and recurrence family; the governing state is current at materialization time; exactly one matching coordinate family exists; coordinate values must match the frozen calendar/elapsed/quota/cyclic recurrence contract; non-quota duplicate generation identity is rejected; quota materialization uses deterministic source locking and exact period/cardinality validation; later recurrence revisions do not rewrite historical provenance.

The routine is a validator only: no external I/O, orchestration, retry loop, transaction control, generic dynamic SQL or runtime-supplied identifiers.

## Security

`enforce_occurrence_generation_integrity()` is `SECURITY INVOKER`, `VOLATILE`, `PARALLEL UNSAFE`, non-leakproof, owned by `dante_owner`, with `search_path=pg_catalog,dante,pg_temp`. Direct EXECUTE remains revoked from PUBLIC, `dante_runtime` and direct `dante_migrator`.

All five M6 tables remain deny-by-default for runtime until M7. M6 activates no business GRANT.

## Migration boundary

Upgrade is `20260825_05 -> 20260826_06`. Downgrade removes the 9 M6 trigger attachments, Role-13 routine and five M6 tables and returns to the exact M5 structural surface.

## Direct PostgreSQL acceptance

Implementation candidate:

```text
00e60df414218638050c0dacad30c01266643ebb
feat: materialize CP6-04 M6 occurrence generation
```

The first direct PostgreSQL 18.6 run reached the complete M6 suite and proved M6 itself green, but exposed two historical M4 tests that incorrectly compared the current repository-wide SQLAlchemy/Dictionary surface to the frozen M4-only 63-table surface. The database, M6 migration and M6 Dictionary were not changed for those failures.

The repair was limited to stage-relative historical assertions in:

```text
apps/backend/tests/integration/database/test_cp6_m4.py
```

Repair commit:

```text
a05ce4fe6e98efa1fcdb7fac095eed93342bc017
```

The user then executed from `apps/backend`:

```text
uv run pytest -m postgres -vv
```

Observed final result:

```text
102 collected
37 deselected
65 selected
65 passed
0 failed
45.17s
coverage 95.86%
```

The qualifying run covers M1-M6 acceptance, final structural counts, M6 routine security, deny-by-default pre-M7 ACL posture, NativeRef source-family rejection, explicit-extra zero-coordinate enforcement, generated-coordinate membership/duplicate rejection, Dictionary reconciliation, M6->M5 downgrade, Alembic fresh/head round trips and drift, privileges, runtime and transactions.

## Closure

`CP6-M06` is CLOSED. The next stage is `CP6-M07 — Runtime ACL Activation`.

## Explicitly out of scope for M6

- CP6-M07 runtime ACL activation;
- persistent local PostgreSQL materialization;
- frontend;
- main integration;
- product workflow/orchestration semantics.
