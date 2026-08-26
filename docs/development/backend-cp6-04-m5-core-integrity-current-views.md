# CP6-04 M5 — Core Integrity & Current Views

**Stage:** `CP6-M05 / cp6_core_integrity_current_views`  
**Revision:** `20260825_05`  
**Down revision:** `20260825_04`  
**Status:** CLOSED / DIRECT POSTGRESQL 18.6 PASS  

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

SQLAlchemy mappings and the Database Dictionary carry the same final Part-17 expressions.

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

The 66 trigger registrations are embedded in the exact 50 target table entries. M5 creates standalone entries only for objects that physically exist at M5.

## Closure evidence

### Intermediate implementation proof

A direct PostgreSQL 18.6 run against `d2f6543cbd6c632d995e7481d50a895408a69001`, before the final Dictionary/mapping reconciliation, completed green:

```text
54 passed
0 failed
coverage 95.63%
```

This was retained as intermediate evidence rather than rewritten as a synthetic first-pass closure.

### Final repository-consistency proof — authoritative M5 closure gate

Final tested implementation/repository-consistency SHA:

```text
92939004cd2a5437238f2574b47c4f6d3b2ea00a
feat: complete CP6-04 M5 repository consistency
```

User-executed command from `~/projects/dante/apps/backend`:

```text
uv run pytest -m postgres -vv
```

Observed result:

```text
collected 92 items
37 deselected
55 selected
55 passed
0 failed
80.13s
coverage 95.63%
```

The final run explicitly passed:

- all CP6-M01 through CP6-M05 PostgreSQL acceptance tests;
- `test_m5_dictionary_reconciles_stage_objects_and_part17_repairs`;
- M5 topology/routine security;
- ordinary automatically-updatable current views + LOCAL CHECK OPTION;
- isolated SQLAlchemy Core view metadata;
- NativeAddress owner binding rejection;
- IANA timezone rejection with SQLSTATE `22023`;
- all seven Part-17 / DB-U25 CHECK repairs;
- no dynamic PL/pgSQL EXECUTE in M5 routines;
- M5→M4 downgrade boundary;
- fresh database → single repository head;
- head → base → head migration round trip;
- `alembic check` with extensions present;
- role/privilege hardening;
- runtime recovery/readiness behavior;
- transaction/rollback/savepoint behavior.

No PostgreSQL failure remained at closure.

## Closure decision

```text
CP6-M05: CLOSED
Revision: 20260825_05
Direct PostgreSQL 18.6 gate: PASS
Final selected tests: 55/55 PASS
Coverage: 95.63%
Next stage: CP6-M06 occurrence generation
```

The repository-level M5 implementation gate was reconciled to the actual required surface of **77 paths = 22 CREATE + 55 UPDATE + 0 DELETE**, including the necessary SQLAlchemy Part-17 mapping repairs. The exact PRE-SCOPE→candidate compare contained no unexpected path.

The post-test documentation commits do not change migration, mapping, Dictionary, application, provisioning, or test behavior; they record the observed closure and current cross-chat routing only.

## Explicitly out of scope

- CP6-M06 occurrence generation materialization;
- CP6-M07 runtime ACL activation;
- new M5 tables or indexes;
- final persistent local PostgreSQL lifecycle;
- frontend work;
- branch merge/rebase/main integration.
