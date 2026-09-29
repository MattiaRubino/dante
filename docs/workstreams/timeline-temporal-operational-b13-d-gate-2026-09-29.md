# B13-D — local acceptance gate

- **Status:** B13-D CLOSED / user-reported real-app acceptance; post-repair web rerun unreported
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
  src/features/temporal/remote-plan-dependency-data-source.test.ts \
  src/features/home/ui/timeline/timeline-create-bridge-b01.test.tsx

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

## Automated evidence before UX repair — 2026-09-29

The user pulled `c7e298384a2dacc8e7a8dc64405e20a1951f0879` and supplied the local command output. `pnpm generated:check` passed (383 deterministic generated files); API-client and web typechecks passed; the six-file web suite passed **12 tests**; backend OpenAPI/unit selection passed **3 tests in 2.02s**; the seven-file PostgreSQL selection passed **14 tests in 44.24s**; Ruff check passed and both Python files were already formatted. The Vite build emitted an advisory chunk-size warning, with successful exit. This proves the automated candidate gate before the UX repair. Later real-app screenshots and the user's overall acceptance are recorded below.

## UX repair — direct Activity to Plan flow

The first acceptance instruction exposed an unacceptable authoring path: the Plan panel asked the user to inspect a browser attribute and paste an Activity UUID. The repair removes that field. Clicking an unplaced Activity title in the Planning Tray opens and focuses **Plan e Step** and carries the selected Activity. A subsequent real-app screenshot showed that an already authored unlinked Step and an Activity of the same title were still separate, while the first repair offered only a duplicate linked Step. The Plan panel now proposes the matching unlinked Step first, allows selecting another unlinked Step or creating a new one, and states which Steps have no Activity. It also identifies an Activity already linked to the selected Plan. Existing linked Steps retain **Scollega**. This is browser-only and preserves Plan, Step and Activity persistence semantics.

Rerun the command block after pulling this repair. The web selection now contains seven files and is expected to report **16 tests**. The PostgreSQL selection remains **14 tests** unless discovery changes. Then run the real-app walkthrough below using the direct card flow; no browser DevTools, UUID copying or manual technical reference is part of acceptance.

## Real-app walkthrough after automated PASS

In the running local Home app, use a fresh test Plan and two distinct unplaced Activities that you own. Click an Activity title in the Planning Tray to open **Plan e Step** with that Activity selected. Create or select the Plan. If a same-title Step was previously created, choose the proposed **Step esistente** and press **Collega**; otherwise use **+ Aggiungi “…” al Plan**. Repeat from the second Activity card. Both intended Dependency endpoints must explicitly show **Attività collegata**. Extra unlinked test Steps can be removed before creating the Dependency. No identifier needs to be exposed to the user.

1. Open **Plan e Step**. Create an Album Plan, add Record and Mix Steps, link each to its own Activity, then refresh. Check the Plan and both links persist and Step order can be changed.
2. Create an `Actual avvenuto` Dependency from Record to Mix. With no prerequisite Actual, check the displayed evaluation is `sconosciuta`. Reorder the Steps and refresh: the direction remains Record → Mix. Try removing a linked Step while the Dependency is active; check the operation is rejected and the Plan remains intact.
3. Set Mix as divisible, maximum two proposed segments, merge permitted, hard. Save and refresh: the policy remains on Mix. Where the existing Activity Temporal Constraint control is available, configure a hard maximum Schedule duration of 90 minutes on the Mix Activity. Enter three one-hour candidate intervals, with the first two contiguous; verify the hard count diagnostic and, when the duration rule was configured, that their two-hour union is incompatible for the stated rule. No accepted Schedule or Session should be created by assessment.
4. Record an Actual for the Record Activity using its existing product control. Reload the Dependency: its current evaluation should follow the accepted Actual. Correct the Actual where the product supports that path; evaluation should update without changing Mix policy or the proposed planning basis.
5. Retire the Mix policy and Dependency, refresh and confirm the active controls no longer claim those rules. Record any missing path, error, stale view or unexpected mutation precisely.

## Acceptance report — 2026-09-29

Screenshots from the user's local app showed the Album Plan with Record and Mix Steps linked to distinct Activities, then the Record → Mix `Actual avvenuto` Dependency evaluated as `sconosciuta`. After receiving the complete remaining walkthrough, the user reported “ok va chiudiamo”. This is overall user-reported acceptance; the remaining checks were not reported one by one. The post-repair seven-file web rerun (expected 16 tests) has no reported PASS; the earlier 14-pass/1-fail run preceded two fixes. Do not relabel that run as passed. B13-D and parent B13 close on qualified user-reported acceptance; see `docs/workstreams/timeline-temporal-operational-b13-d-closure-2026-09-29.md`.
