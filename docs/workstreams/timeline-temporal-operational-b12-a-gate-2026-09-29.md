# B12-A — local proof and product gate

**Status:** candidate; user-run PostgreSQL and real-app proof pending. The user runs local commands; no CI/GitHub Actions.

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

Then perform the five-step walkthrough in the implementation checkpoint and report command output plus what the Home panel displayed. The stage remains open until both are complete.
