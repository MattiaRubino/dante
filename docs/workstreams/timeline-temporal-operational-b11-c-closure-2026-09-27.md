# B11-C — Schedule-relative personal Reminder — Technical closure

- **Date:** 2026-09-27
- **Branch:** `feature/timeline-temporal-operational`
- **Status:** CLOSED / PROVEN by user-run local automated gates
- **Scope authority:** `timeline-temporal-operational-b11-c-scope-2026-09-27.md`
- **Persistence head:** Alembic `20260927_86`
- **Whole-B11 status:** IN PROGRESS; integrated real-app walkthrough remains open

## Implemented vertical

The stable self Person/Schedule Reminder owner has append-only configuration MaterialState and explicit accepted-current history. PostgreSQL guarded functions enforce ownership, exact-start Schedule admissibility, compare-and-swap and operation replay, and derive `pending/due/unavailable` without storing a second due-time authority. Backend/API/OpenAPI, generated client, existing-Schedule controls, Create's two-command partial-success retry, and focused tests are present. No delivery job or Actual/Outcome mutation was introduced. The published `_86` migration was not modified.

Implementation checkpoints: persistence/backend/API `9878b441`, existing-Schedule UI `9d806355`, Create retry `e9a0f760`, generated client `d0378e17`. The Dictionary/catalog reconciliation was published at `1c87cc52`, CHECK-name repair at `a332a592`, exact routine signatures and reference docs at `6610982f`, and registration of the five existing B10-D reconciliation mappings at `3fe447af`.

## User-run proof

The user reported the focused B11-C local gate passing: 5 backend and 16 web tests, generator/determinism check, and API-client and web typechecks. The local PostgreSQL `_86` probe passed and measured:

```text
184|5|144|100|370|323|480|0|0|0
```

The first exact whole-catalog run passed 8 tests and failed 2 on five CHECK constraint names. After repair, both tests advanced past the PostgreSQL/Dictionary identifiers and exposed five existing Outcome Reconciliation mappings missing from the registry. Those were registered without changing the migration or tables. The user pulled `3fe447af` and reran:

```text
test_current_database_cross_representation_is_exact                  PASS
test_current_catalog_matches_dictionary_sqlalchemy_and_alembic      PASS
2 passed in 8.90s
```

These results establish the `_86` catalog, Dictionary, SQLAlchemy registry and Alembic head parity required by the B11-B/C verticals. No GitHub Actions or CI tests were used.

## Remaining B11 gate

B11-A, B11-B and B11-C are technically closed. Before closing the parent B11 block, run the integrated real-app walkthrough locally: create an admissible Schedule with Reminder intent, inspect due state on the Timeline, revise or withdraw the Schedule, configure/disable from an existing Schedule, reload to verify canonical state, and exercise the Create partial-success retry without creating the subject twice. Record the observed behavior in the whole-B11 closure evidence. B13/B12/B14 and deferred B07 remain separate roadmap blocks.
