# B05-A — Life Area catalog closure record

- **Status:** CLOSED / PROVEN
- **Date:** 2026-09-20
- **Branch head proved:** `2e91fe73546d03b141fc83ae5e731d1242fdc260`
- **Alembic:** `20260920_45`
- **Observed PostgreSQL topology:** `119|5|48|90|239|158|344|0|0|0`
- **CI / Actions:** not run

## Accepted direct evidence

The user pulled the candidate branch, applied all migrations to a fresh PostgreSQL
test database and ran the complete B05-A proof block. The first `_44` run passed
seven selected tests and observed the expected topology, but exposed one generated
CHECK identifier mismatch. Forward revision `_45` renamed that already validated
CHECK without altering rows, predicate or topology. The user then ran:

```bash
uv run --locked pytest -q --no-cov -m postgres \
  tests/integration/database/test_database_current_catalog.py
```

Result: `1 passed in 6.00s`.

## Closed obligations

- LR-12 Life Area is an actor-local product profile, never a NativeRef owner.
- Guarded create/list/rename/reorder/archive/hide-show/appearance operations are
  self-scoped, idempotent and have direct PostgreSQL proof.
- Runtime has only bounded function EXECUTE; raw profile/receipt table access is
  denied.
- Dictionary, SQLAlchemy mappings, Alembic, exact catalog tests, OpenAPI snapshot
  and generated client are synchronized at the proved head.

## Boundary retained

B05-A does not assign Activity/Event items. B05-B owns the typed actor-local
primary-assignment relation, atomic new-item authoring, reassignment and legacy
reconciliation. Archive remains non-destructive; B05-B must reject new assignment
to an archived area while retaining prior assignments for later reads.
