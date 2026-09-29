# B12-D — local automated and real-app gate

- **Status:** IMPLEMENTATION CANDIDATE; USER-RUN PROOF PENDING
- **Branch:** `feature/timeline-temporal-operational`
- **Database head:** `20260929_93`; current exact Dictionary/catalog topology `196|5|155|100|397|344|497|0|0|0`
- **CI:** none; user runs in `~/projects/dante`

Run the following as one block. `set -euo pipefail` stops at the first failed command. The PostgreSQL test fixture migrates its test database to head; no separate manual Alembic step is needed.

```bash
set -euo pipefail
cd ~/projects/dante
git pull --ff-only origin feature/timeline-temporal-operational

pnpm generated:check
pnpm --filter @dante/api-client typecheck
pnpm --filter @dante/web typecheck
pnpm --filter @dante/web exec vitest run \
  src/features/temporal/plan-work-panel.test.tsx \
  src/features/temporal/plan-dependency-panel.test.tsx \
  src/features/temporal/plan-conflict-panel.test.tsx \
  src/features/temporal/plan-candidate-panel.test.tsx \
  src/features/temporal/plan-replanning-whole-block.test.tsx

cd apps/backend
uv run --locked ruff check tests/integration/temporal/test_b12_d_whole_block.py
uv run --locked pytest -q --no-cov --tb=short \
  tests/test_b12_a_openapi_contract.py \
  tests/test_b12_b_openapi_contract.py \
  tests/test_b12_b_candidate_solver.py \
  tests/test_b12_c_openapi_contract.py
uv run --locked pytest -q --no-cov --tb=short -m postgres \
  tests/integration/temporal/test_b12_d_whole_block.py \
  tests/integration/temporal/test_b12_a_plan_conflict.py \
  tests/integration/temporal/test_b12_b_plan_candidate.py \
  tests/integration/temporal/test_b12_c_plan_admission.py \
  tests/integration/temporal/test_b04_governed_schedule_move.py \
  tests/integration/temporal/test_b13_a_plan_work.py \
  tests/integration/temporal/test_b13_b_plan_dependency.py \
  tests/integration/temporal/test_b13_c_execution_structure.py \
  tests/integration/database/test_current_catalog.py \
  tests/integration/database/test_database_current_catalog.py \
  tests/integration/database/test_b11_catalog_reconciliation_probe.py
```

Return the entire command output. After it passes, the assistant gives one complete click-only Home/Timeline walkthrough with startup commands and records the user's actual observations. A pending proposal is not accepted Schedule; the final walkthrough and reported result are required before closing B12-D and parent B12.
