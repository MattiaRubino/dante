# B12-D — local automated and real-app gate

- **Status:** ORIGINAL AUTOMATED GATE PASSED; CLICK-PATH REPAIR RECHECK AND REAL-APP PROOF PENDING
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
  src/features/temporal/remote-plan-replanning-setup-data-source.test.ts \
  src/features/temporal/plan-replanning-whole-block.test.tsx

cd apps/backend
uv run --locked ruff check \
  src/dante/modules/temporal/movement_policy_api.py \
  tests/test_b12_d_movement_policy_api.py \
  tests/test_temporal_openapi_inventory.py \
  tests/integration/temporal/test_b12_d_whole_block.py
uv run --locked ruff format --check \
  src/dante/modules/temporal/movement_policy_api.py \
  tests/test_b12_d_movement_policy_api.py
uv run --locked pytest -q --no-cov --tb=short \
  tests/test_b12_d_movement_policy_api.py \
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

Return the entire command output. A pending proposal is not accepted Schedule; the real-app walkthrough and reported result are required before closing B12-D and parent B12.

## Automated evidence on the original candidate — user worktree, 2026-09-30

The user pulled commit `758914479f80bea378e431b31900ee3d890366f4` and supplied the complete command transcript: generated sources deterministic (397 files), both typechecks passed, five web files **11 tests passed**, Ruff passed, backend OpenAPI/solver selection **9 passed**, and focused PostgreSQL/catalog selection **20 passed in 41.19s**. This proof covers the original integrated candidate, not the later click-path repair.

## Click-path repair and affected recheck

The original integration test established the Movement Policy and hard constraint directly through Python, while the user could not configure those for an already placed Mix Activity through the Home panel. The repair adds a self-scoped, CSRF-protected, CAS-based Schedule Movement Policy API and exposes two controls under **Regole per Mix**: **Inizio non prima di → Imposta vincolo hard** using the existing Temporal Constraint API, and **Consenti spostamento con conferma**. The panel rereads candidates after each write; no UUID entry or browser tools are required. There is no new database schema.

The authoring environment has Node and frontend dependencies but no working project Python 3.14 interpreter, so the OpenAPI snapshot was assembled from the existing FastAPI contract conventions and the Orval client was generated locally. The user's `pnpm generated:check` is the deterministic verification of that snapshot against the runtime export. Local web and API-client typechecks, targeted web tests and Ruff passed. The new backend API contract test and the PostgreSQL regression require the user-run gate above. Do not record them as passed before receiving that output.

## Real-app walkthrough after the repaired gate

Run the existing disposable stack from the repository root in a second terminal:

```bash
cd ~/projects/dante
docker compose -f infra/compose/local.yaml build postgres
export DANTE_E2E_CONTROL_ID=temporal-b12-d-usertest
uv run --project apps/backend python tooling/run-access-auth-stack.py
```

Wait for `DANTE Access/Auth full-stack ready`, open `https://127.0.0.1:4173`, accept the local development certificate, and sign in as `synthetic.user@example.com` with password `correct horse battery staple`. The database is disposable for this run. Keep the terminal open until the walkthrough ends.

1. In Home, use **+** on Timeline to create `B12D Record` as an **unplaced Activity**. Create `B12D Mix` as an unplaced Activity too, choosing **named-zone time** and `Europe/Rome` before submitting. Click the Record title in **Attività da collocare** to open **Plan e Step**, choose **Nuovo Plan**, name it `B12D Album`, and press **Crea Plan**. Add the selected Record Activity using **+ Aggiungi … al Plan**. Repeat from Mix and add Mix to the same Plan. Confirm both Steps say **Attività collegata**.
2. From **Attività da collocare**, use **Colloca** to schedule Record on **2 October 2026, 08:00–08:30**, and Mix on **2 October 2026, 10:00–11:00**, in the app's displayed local time. Open **Plan e Step**, select `B12D Album`, create the **Actual avvenuto** Dependency with prerequisite Record and dependent Mix. The evaluation should be **sconosciuta**.
3. In **Conflitti del Plan**, press **Analizza conflitti** and then **Cerca alternative vicine per Mix**. The prerequisite is unknown, so no reviewed movement is available. The panel first shows **Rendi fisso questo orario**: press it and wait for the confirmation, then press **Analizza conflitti** again. Under **Regole per Mix**, set **Inizio non prima di** to **2 October 2026, 11:00** and press **Imposta vincolo hard**. Press **Consenti spostamento con conferma**. Neither write moves Mix.
4. In Timeline, open **Realtà / Outcome**, choose `B12D Record` under **Elemento per stato reale**, press **Segna avvenuto** and wait for **Stato reale: avvenuto**. Return to **Plan e Step**, reload the Dependency if needed: Record → Mix must be **soddisfatta**. Press **Analizza conflitti** again; Mix should report the hard temporal violation. Search alternatives for Mix. Expect a candidate at or after 11:00, with the current 10:00–11:00 Schedule unchanged.
5. Press **Rivedi questa alternativa** for the 11:00–12:00 option if offered, and verify old/new intervals and the capacity warning. Press **Richiedi questo spostamento**. Expect **Proposta in attesa: la Schedule non è cambiata**. Then press **Conferma lo spostamento**. Expect **Spostamento registrato** and the new current Schedule. Reload Home and Timeline: Mix appears at the confirmed interval, Record → Mix remains directed and satisfied, and the linked Steps persist. If the bounded solver offers a different valid option, note its displayed interval and use it consistently.
6. Report the exact button or message if a step differs. Stop the stack with `Ctrl+C` in its terminal after the observation; this removes the disposable database.
