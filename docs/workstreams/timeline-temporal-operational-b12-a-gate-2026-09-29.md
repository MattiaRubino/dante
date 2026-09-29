# B12-A — local automated proof gate

**Status:** PASSED in the user's local worktree on 2026-09-29. No CI/GitHub Actions. Real-app acceptance belongs to B12-D.

From `~/projects/dante` after pulling `feature/timeline-temporal-operational`:

```bash
cd ~/projects/dante
git pull --ff-only origin feature/timeline-temporal-operational
pnpm generated:check
pnpm --filter @dante/api-client typecheck
pnpm --filter @dante/web typecheck
pnpm --filter @dante/web exec vitest run \
  src/features/temporal/plan-conflict-panel.test.tsx \
  src/features/temporal/plan-work-panel.test.tsx
cd apps/backend
uv run --locked pytest -q --no-cov --tb=short tests/test_b12_a_openapi_contract.py
uv run --locked ruff check \
  src/dante/bootstrap/app.py \
  src/dante/modules/temporal/plan_conflict.py \
  src/dante/modules/temporal/plan_conflict_api.py \
  tests/test_b12_a_openapi_contract.py \
  tests/integration/temporal/test_b12_a_plan_conflict.py
uv run --locked pytest -q --no-cov --tb=short -m postgres \
  tests/integration/temporal/test_b12_a_plan_conflict.py \
  tests/integration/temporal/test_b13_d_whole_block.py \
  tests/integration/database/test_current_catalog.py \
  tests/integration/database/test_database_current_catalog.py \
  tests/integration/database/test_b11_catalog_reconciliation_probe.py
```

Reported result at `db6a568`: generated check **389**, both typechecks PASS, web **4 passed / 2 files**, OpenAPI contract **1 passed**, Ruff PASS, PostgreSQL/catalog **11 passed in 26.14s**. B12-A is closed on this focused automated evidence. The integrated product check runs at B12-D before closing B12.
