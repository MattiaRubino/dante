# B11-D — Local automated gate

- **Date:** 2026-09-27
- **Branch:** `feature/timeline-temporal-operational`
- **Status:** PASSED LOCALLY — B11-D CLOSED / PROVEN
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

The reported local results below close B11-D. Run the final integrated real-app walkthrough before deciding whole-B11 closure.

## Reported local results

The user pulled `13f860a1` and ran the complete command set on 2026-09-27:

```text
B11-A/B/C OpenAPI contract                    7 passed
B11-A/B/C/D + exact catalog PostgreSQL       14 passed
Generated sources                            PASS; 364 files deterministic/current
API client typecheck                          PASS
Web typecheck                                 PASS
Web focused gate                             6 files, 24 passed
Ruff B11-D test                               PASS after I001 import-order repair
```

The sole initial Ruff finding was I001 import order in the B11-D test. Its repair was published at `c685d519`; the user pulled branch head `37ce469a` and reported `All checks passed!` for the exact Ruff command on 2026-09-27. The preceding PostgreSQL/OpenAPI/web/client results were not rerun for that import-order-only edit. The `react-i18next` warning was non-failing. Closure evidence: `timeline-temporal-operational-b11-d-closure-2026-09-27.md`.
