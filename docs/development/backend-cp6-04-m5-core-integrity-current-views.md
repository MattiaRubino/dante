# CP6-04 M5 — Core Integrity & Current Views

**Stage:** `CP6-M05 / cp6_core_integrity_current_views`  
**Revision:** `20260825_05`  
**Down revision:** `20260825_04`  
**Status:** IMPLEMENTED / FINAL REPOSITORY-CONSISTENCY POSTGRESQL RE-RUN REQUIRED  

## Scope

M5 materializes the bounded database-local integrity layer over the 63-table M4 surface. It does not add business tables, indexes, runtime ACL activation, orchestration, workflow or external side effects.

M5 adds exactly:

- 13 `dante` PL/pgSQL trigger functions;
- 66 row triggers: 15 immediate `BEFORE` triggers and 51 deferred constraint triggers;
- 5 ordinary automatically-updatable current-facet views with `WITH LOCAL CHECK OPTION`;
- the DB-U25 forward-only repair of seven already-named CHECK constraints, with downgrade restoring the historical M4 expressions;
- five SQLAlchemy Core view handles in isolated `VIEW_METADATA`;
- Database Dictionary materialization for the five views, thirteen routines and all 66 trigger attachments.

M5 leaves the structural table/index/FK/CHECK counts at the post-M4 totals except that the seven repaired CHECK expressions are the final Part-17 forms:

```text
tables              63
views                 5
routines             13
triggers             66
physical indexes     87
foreign keys         61
check constraints   109
```

## Security contract

All thirteen functions are owned by `dante_owner`, `SECURITY INVOKER`, `VOLATILE`, `PARALLEL UNSAFE`, non-leakproof, use function `search_path = pg_catalog,dante,pg_temp`, and expose no direct EXECUTE to `PUBLIC`, `dante_runtime` or direct `dante_migrator`.

The five current views are owned by `dante_owner`, remain `security_invoker=false` / `security_barrier=false`, expose exactly three columns, fix their material facet through predicate + view-column default, and use `WITH LOCAL CHECK OPTION`. Runtime business ACL activation remains exclusively M7.

## DB-U25 repairs carried by revision 20260825_05

The migration repairs, without renaming or changing counts:

1. `ck_session_timing_absolute_end_precision` — explicit NULL-safe end/precision pairing;
2. Routine/Event `*_calendar_state_step_unit` — explicit non-null step unit for `anchor_step`;
3. Routine/Event `*_quota_state_week_start` — explicit non-null week start for weekly quota periods;
4. Routine/Event `*_elapsed_state_elapsed_positive` — finite positive elapsed seconds with maximum six fractional decimal places.

`downgrade 20260825_05 -> 20260825_04` restores the exact historical M4 CHECK expressions after dropping M5 views, triggers and routines dependency-safely.

## Integrity responsibilities

The M5 trigger layer covers:

- NativeAddress and ScopedAddress owner binding;
- NativeRef eligibility;
- MaterialState address/envelope totality;
- current MaterialState binding;
- current/history equivalence and one-way history lifecycle;
- owner creation completeness;
- Schedule placement payload totality;
- Actual exact realization basis;
- Session timing totality and pause consistency;
- Routine/Event Recurrence aggregate integrity, including Part-17 selector/anchor/range/phase/quota/cyclic rules;
- IANA timezone validation and named-zone local/resolved round-trip checks.

Triggers are validators only. They do not perform business workflow, retries, orchestration, external I/O or hidden lifecycle mutation.

## Dictionary state after M5

```text
completed stages     CP6-M01..CP6-M05
standalone entries   81 = 63 tables + 5 views + 13 routines
embedded triggers    66
physical indexes     87
foreign keys         61
check constraints   109
```

The 66 trigger registrations are embedded in the exact 50 target table entries. M5 creates standalone entries only for objects that now physically exist.

## Proof state

A direct PostgreSQL 18.6 run against the implementation candidate at `d2f6543cbd6c632d995e7481d50a895408a69001` completed green before the final Dictionary/mapping reconciliation: **54 passed / 0 failed / coverage 95.63%**. That run covered the migration chain, M1-M5 PostgreSQL tests, M5 routine/view/integrity behavior, downgrade boundary and Alembic drift checks.

Because this document is committed together with the final repository-consistency reconciliation, **M5 is not declared CLOSED by this record until the post-reconciliation `uv run pytest -m postgres -vv` run is observed green**. The closure update must record the resulting commit SHA and exact observed test result; no synthetic PASS count is permitted.

## Explicitly out of scope

- CP6-M06 occurrence generation materialization;
- CP6-M07 runtime ACL activation;
- new tables or indexes;
- final persistent local PostgreSQL lifecycle;
- frontend work;
- branch merge/rebase/main integration.
