#!/usr/bin/env bash
# One local gate. No pull, commit, push, CI, or persistent application DB mutation.
set +e
cd "$(dirname "$0")/.." || exit 1
PANEL_LOG_DIR="$(mktemp -d /tmp/dante-session-panel.XXXXXX)"
declare -A RESULT
run_gate() {
  local name="$1"
  shift
  "$@" >"$PANEL_LOG_DIR/$name.log" 2>&1
  RESULT["$name"]=$?
  printf '%-18s %s\n' "$name" "${RESULT[$name]}"
  if [ "${RESULT[$name]}" -ne 0 ]; then tail -n 80 "$PANEL_LOG_DIR/$name.log"; fi
}
cd apps/backend || exit 1
run_gate RUFF uv run --locked ruff check \
  src/dante/bootstrap/app.py src/dante/modules/temporal/session_panel_api.py \
  migrations/versions/20261009_135_b14_session_panel_untimed_start.py \
  tests/test_session_panel.py tests/integration/temporal/test_b14_session_panel.py \
  tests/integration/database/test_current_catalog.py tests/integration/database/test_database_current_catalog.py
run_gate SYNTAX uv run --locked python -m compileall -q \
  src/dante/modules/temporal/session_panel_api.py migrations/versions/20261009_135_b14_session_panel_untimed_start.py
run_gate UNIT uv run --locked pytest -q --no-cov --tb=short tests/test_session_panel.py
run_gate POSTGRES uv run --locked pytest -q --no-cov --tb=short -m postgres \
  tests/integration/temporal/test_b14_session_panel.py \
  tests/integration/temporal/test_b14_planned_session_execution_link.py \
  tests/integration/temporal/test_b08_b_session_pause_resume.py \
  tests/integration/temporal/test_b14_activity_replan.py \
  tests/integration/database/test_current_catalog.py \
  tests/integration/database/test_database_current_catalog.py
cd ../.. || exit 1
run_gate GENERATE pnpm api:generate
run_gate GENERATED_CHECK pnpm generated:check
run_gate API_TYPECHECK pnpm --filter @dante/api-client typecheck
run_gate WEB_TYPECHECK pnpm --filter @dante/web typecheck
run_gate PANEL_LINT pnpm exec eslint \
  apps/web/src/features/temporal/use-session-panel.ts \
  apps/web/src/features/home/ui/timeline/timeline-session-panel.tsx \
  apps/web/src/features/home/ui/timeline/timeline-session-panel.test.tsx
run_gate VITEST pnpm --filter @dante/web exec vitest run \
  src/features/home/ui/timeline/timeline-session-panel.test.tsx \
  src/features/home/ui/timeline/timeline-surface.test.tsx \
  src/features/home/ui/timeline/timeline-runtime-detail-controls.test.tsx \
  src/features/temporal/session-subject-controls.test.tsx \
  src/features/temporal/activity-session-card-controls.test.tsx \
  src/features/temporal/activity-planned-sessions-card-detail.test.tsx \
  src/features/temporal/remote-session-data-source.test.ts \
  src/features/home/ui/timeline/activity-inspector-actions.test.tsx \
  src/features/temporal-create/ui/temporal-create-entry-u2.test.tsx
run_gate BROWSER pnpm --filter @dante/web exec playwright test --config playwright.session-panel.config.ts
FAILED=0
for name in RUFF SYNTAX UNIT POSTGRES GENERATE GENERATED_CHECK API_TYPECHECK WEB_TYPECHECK PANEL_LINT VITEST BROWSER; do
  printf '%-18s %s\n' "$name" "${RESULT[$name]:-NON_ESEGUITO}"
  if [ "${RESULT[$name]:-1}" -ne 0 ]; then FAILED=1; fi
done
echo "LOG_DIR=$PANEL_LOG_DIR"
echo "Le prove browser usano API controllate; verificare anche l'app reale dopo la migrazione locale."
exit "$FAILED"
