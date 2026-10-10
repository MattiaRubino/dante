#!/usr/bin/env bash
# Unified user-local acceptance gate for B14 Session independence + three-way
# Home workspace + provisional confirmed Objective input. NO CI.
# Reuses WSL's local PostgreSQL test fixture, does not reset/clean/push.
set +e
cd "$(dirname "$0")/.." || exit 1
if [ "$(git branch --show-current)" != "feature/timeline-temporal-operational" ]; then
  echo "ERR: esegui dal branch feature/timeline-temporal-operational"
  exit 1
fi
LOG_DIR="$(mktemp -d /tmp/dante-b14-workspace.XXXXXX)"
declare -A STATUS
gate() {
  local name="$1"; shift
  "$@" >"$LOG_DIR/$name.log" 2>&1
  STATUS["$name"]=$?
  printf '%-19s %s\n' "$name" "${STATUS[$name]}"
  if [ "${STATUS[$name]}" -ne 0 ]; then
    echo "----- $name: ultime 140 righe -----"
    tail -n 140 "$LOG_DIR/$name.log"
  fi
}
cd apps/backend || exit 1
gate PY_SYNTAX uv run --locked python -m compileall -q \
  src/dante/modules/temporal/session_panel_api.py \
  src/dante/modules/temporal/reality_objective_api.py \
  src/dante/modules/temporal/resolution_queue_api.py \
  src/dante/platform/database/mappings/draft_vault.py \
  migrations/versions/20261010_139_b14_objective_input_draft.py \
  migrations/versions/20261010_140_b14_home_workspace_reads.py \
  migrations/versions/20261010_141_b14_independent_planned_sessions.py \
  tests/integration/temporal/test_b14_objective_input.py \
  tests/integration/temporal/test_b14_home_workspace.py
gate RUFF uv run --locked ruff check \
  src/dante/modules/temporal/session_panel_api.py \
  src/dante/modules/temporal/reality_objective_api.py \
  src/dante/modules/temporal/resolution_queue_api.py \
  src/dante/platform/database/mappings/draft_vault.py \
  migrations/versions/20261010_139_b14_objective_input_draft.py \
  migrations/versions/20261010_140_b14_home_workspace_reads.py \
  migrations/versions/20261010_141_b14_independent_planned_sessions.py \
  tests/test_session_panel.py \
  tests/integration/temporal/test_b14_objective_input.py \
  tests/integration/temporal/test_b14_home_workspace.py \
  tests/integration/temporal/test_b14_session_panel.py \
  tests/integration/database/test_current_catalog.py \
  tests/integration/database/test_database_current_catalog.py
gate PY_UNIT uv run --locked pytest -q --no-cov --tb=short tests/test_session_panel.py
gate POSTGRES uv run --locked pytest -q --no-cov --tb=short -m postgres \
  tests/integration/temporal/test_b14_objective_input.py \
  tests/integration/temporal/test_b14_home_workspace.py \
  tests/integration/temporal/test_b14_session_panel.py \
  tests/integration/temporal/test_b14_session_hierarchy.py \
  tests/integration/temporal/test_b14_planned_session_execution_link.py \
  tests/integration/database/test_current_catalog.py \
  tests/integration/database/test_database_current_catalog.py
cd ../.. || exit 1
gate GENERATE pnpm api:generate
gate GENERATED_CHECK pnpm generated:check
gate API_TYPECHECK pnpm --filter @dante/api-client typecheck
gate WEB_TYPECHECK pnpm --filter @dante/web typecheck
gate WEB_LINT pnpm exec eslint \
  apps/web/src/features/temporal/objective-controls.tsx \
  apps/web/src/features/temporal/objective-controls.test.tsx \
  apps/web/src/features/temporal/remote-reality-objective-data-source.ts \
  apps/web/src/features/home/ui/context-rail/context-rail.tsx \
  apps/web/src/features/home/ui/context-rail/context-rail-work-data-source.ts \
  apps/web/src/features/home/ui/context-rail/context-rail.test.tsx
gate VITEST pnpm --filter @dante/web exec vitest run \
  src/features/temporal/objective-controls.test.tsx \
  src/features/home/ui/context-rail/context-rail.test.tsx \
  src/features/home/ui/timeline/timeline-session-panel.test.tsx \
  src/features/home/ui/timeline/timeline-session-reality.test.ts \
  src/features/temporal/remote-reality-objective-corrections.test.ts
gate BROWSER pnpm --filter @dante/web exec playwright test \
  --config playwright.session-panel.config.ts

echo
echo "===== B14 SESSIONI + TRE VISTE + CONFERMA OBIETTIVI ====="
failed=0
for name in PY_SYNTAX RUFF PY_UNIT POSTGRES GENERATE GENERATED_CHECK \
            API_TYPECHECK WEB_TYPECHECK WEB_LINT VITEST BROWSER; do
  printf '%-19s %s\n' "$name" "${STATUS[$name]:-NON_ESEGUITO}"
  if [ "${STATUS[$name]:-1}" -ne 0 ]; then failed=1; fi
done
echo "LOG_DIR=$LOG_DIR"
echo "----- File modificati (non ripulire) -----"
git status --short
if [ "$failed" -ne 0 ]; then
  echo "CANDIDATO NON VERIFICATO. Conserva i generati e invia output/LOG_DIR."
  exit 1
fi
echo "Gate tecnico verde. Pubblicazione generati e acceptance UI reale ancora necessarie."
