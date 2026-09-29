# B13-D — local acceptance gate

- **Status:** AUTOMATED LOCAL GATE PASS / real-app walkthrough pending
- **Branch:** `feature/timeline-temporal-operational`
- **Alembic head:** `20260929_92`; no new persistence revision in this candidate
- **Runner:** user worktree `~/projects/dante`; no CI/GitHub Actions

Run after pulling the published B13-D candidate:

```bash
cd ~/projects/dante
git pull --ff-only origin feature/timeline-temporal-operational

pnpm generated:check
pnpm --filter @dante/api-client typecheck
pnpm --filter @dante/web typecheck
pnpm --filter @dante/web exec vitest run \
  src/features/temporal/plan-whole-block.test.tsx \
  src/features/temporal/plan-work-panel.test.tsx \
  src/features/temporal/plan-dependency-panel.test.tsx \
  src/features/temporal/plan-execution-panel.test.tsx \
  src/features/temporal/remote-plan-work-data-source.test.ts \
  src/features/temporal/remote-plan-dependency-data-source.test.ts

cd apps/backend
uv run --locked pytest -q --no-cov --tb=short \
  tests/test_b13_a_openapi_contract.py \
  tests/test_b13_b_openapi_contract.py \
  tests/unit/temporal/test_plan_execution_assessment.py
uv run --locked pytest -q --no-cov --tb=short -m postgres \
  tests/integration/temporal/test_b13_d_whole_block.py \
  tests/integration/temporal/test_b13_a_plan_work.py \
  tests/integration/temporal/test_b13_b_plan_dependency.py \
  tests/integration/temporal/test_b13_c_execution_structure.py \
  tests/integration/database/test_current_catalog.py \
  tests/integration/database/test_database_current_catalog.py \
  tests/integration/database/test_b11_catalog_reconciliation_probe.py
uv run --locked ruff check \
  tests/test_b13_a_openapi_contract.py \
  tests/integration/temporal/test_b13_d_whole_block.py
uv run --locked ruff format --check \
  tests/test_b13_a_openapi_contract.py \
  tests/integration/temporal/test_b13_d_whole_block.py
```

## User-run automated evidence — 2026-09-29

The user pulled `c7e298384a2dacc8e7a8dc64405e20a1951f0879` and supplied the local command output. `pnpm generated:check` passed (383 deterministic generated files); API-client and web typechecks passed; the six-file web suite passed **12 tests**; backend OpenAPI/unit selection passed **3 tests in 2.02s**; the seven-file PostgreSQL selection passed **14 tests in 44.24s**; Ruff check passed and both Python files were already formatted. The Vite build emitted an advisory chunk-size warning, with successful exit. This proves the automated candidate gate only; no real-app result has been reported yet.

## Real-app walkthrough after automated PASS

In the running local Home app, use a fresh test Plan and two distinct Activities that you own. The current Plan UI accepts existing Activity references as UUIDs. For an unplaced Activity card, its `data-temporal-activity-ref` attribute can be inspected in the local browser to get that reference. Record this manual-linking limitation in the walkthrough; do not claim that B07's final linking UX is complete.

1. Open **Plan e Step**. Create an Album Plan, add Record and Mix Steps, link each to its own Activity, then refresh. Check the Plan and both links persist and Step order can be changed.
2. Create an `Actual avvenuto` Dependency from Record to Mix. With no prerequisite Actual, check the displayed evaluation is `sconosciuta`. Reorder the Steps and refresh: the direction remains Record → Mix. Try removing a linked Step while the Dependency is active; check the operation is rejected and the Plan remains intact.
3. Set Mix as divisible, maximum two proposed segments, merge permitted, hard. Save and refresh: the policy remains on Mix. Where the existing Activity Temporal Constraint control is available, configure a hard maximum Schedule duration of 90 minutes on the Mix Activity. Enter three one-hour candidate intervals, with the first two contiguous; verify the hard count diagnostic and, when the duration rule was configured, that their two-hour union is incompatible for the stated rule. No accepted Schedule or Session should be created by assessment.
4. Record an Actual for the Record Activity using its existing product control. Reload the Dependency: its current evaluation should follow the accepted Actual. Correct the Actual where the product supports that path; evaluation should update without changing Mix policy or the proposed planning basis.
5. Retire the Mix policy and Dependency, refresh and confirm the active controls no longer claim those rules. Record any missing path, error, stale view or unexpected mutation precisely.

Do not mark B13-D or parent B13 accepted until the user reports this walkthrough and its observed results. The automated gate only proves the focused repository paths.
