# B11-D — Local automated gate

- **Date:** 2026-09-27
- **Branch:** `feature/timeline-temporal-operational`
- **Status:** READY FOR USER-RUN LOCAL GATE; results pending
- **Scope:** `timeline-temporal-operational-b11-d-scope-2026-09-27.md`
- **Real-app walkthrough:** after this gate, before whole-B11 closure

## Implemented proof

`test_b11_d_whole_block.py` crosses completion-relative Recurrence, dependent Occurrence, Schedule/Reminder, and Actual-backed Condition on one canonical chain. It checks unknown truth before Actual, exact evidence after Actual/correction, stable replay/history, and Reminder due-time derivation after Schedule revision. The user reported this one test passing locally (`1 passed in 7.20s`) at `82f763af`; that is an intermediate checkpoint, not this complete gate.

The Timeline inspector now separates the selected Occurrence's Actual/Condition from the Routine/Event Recurrence owner and remounts subject controls on selection changes. Advanced Recurrence authoring reaches the typed Routine endpoint through an Occurrence. Reminder controls have an uncertain-write replay test that checks operation id and expected MaterialState reuse. The web integration checkpoint is `a89d13e6`.

## Complete local commands

Run from a clean local worktree after pulling the published branch. The PostgreSQL tests provision their own test database. Do not use CI or GitHub Actions.

```bash
cd ~/projects/dante
git pull --ff-only origin feature/timeline-temporal-operational

cd apps/backend
uv run --locked ruff check tests/integration/temporal/test_b11_d_whole_block.py
uv run --locked pytest -q --no-cov \
  tests/test_b11_a_openapi_contract.py \
  tests/test_b11_b_openapi_contract.py \
  tests/test_b11_c_openapi_contract.py
uv run --locked pytest -q --no-cov -m postgres \
  tests/integration/temporal/test_b11_a_advanced_recurrence.py \
  tests/integration/temporal/test_b11_b_conditional_temporal.py \
  tests/integration/temporal/test_b11_b_conditional_temporal_api.py \
  tests/integration/temporal/test_b11_c_schedule_reminder.py \
  tests/integration/temporal/test_b11_d_whole_block.py \
  tests/integration/database/test_database_current_catalog.py \
  tests/integration/database/test_current_catalog.py

cd ~/projects/dante
pnpm generated:check
pnpm --filter @dante/api-client typecheck
pnpm --filter @dante/web typecheck
pnpm --filter @dante/web exec vitest run \
  src/features/temporal/advanced-recurrence-controls.test.tsx \
  src/features/temporal/conditional-temporal-controls.test.tsx \
  src/features/temporal/timeline-truth-inspector.test.tsx \
  src/features/temporal/schedule-reminder-controls.test.tsx \
  src/features/temporal/remote-schedule-reminder-data-source.test.ts \
  src/features/temporal-create/application/temporal-create-runtime-boundary.test.ts
```

Record the actual local results before marking B11-D closed. Only then run the final integrated real-app walkthrough and decide whole-B11 closure.
