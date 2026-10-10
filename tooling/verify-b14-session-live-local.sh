#!/usr/bin/env bash
# ONE consolidated user-local B14 Session execution gate.
# No pull, commit, push, GitHub Actions, or persistent user database mutation.
set +e
cd "$(dirname "$0")/.." || exit 1
if [ "$(git branch --show-current)" != "feature/timeline-temporal-operational" ]; then
  echo "ERR: usare feature/timeline-temporal-operational."
  exit 1
fi
LOG_DIR="$(mktemp -d /tmp/dante-session-live.XXXXXX)"
declare -A RESULT
run_gate() {
  local name="$1"
  shift
  "$@" >"$LOG_DIR/$name.log" 2>&1
  RESULT["$name"]=$?
  printf '%-20s %s\n' "$name" "${RESULT[$name]}"
  if [ "${RESULT[$name]}" -ne 0 ]; then
    echo "----- $name (ultime 110 righe) -----"
    tail -n 110 "$LOG_DIR/$name.log"
  fi
  return 0
}

cd apps/backend || exit 1
run_gate PY_SYNTAX uv run --locked python -m compileall -q \
  src/dante/modules/temporal/session_runtime.py \
  src/dante/modules/temporal/session_panel_api.py \
  migrations/versions/20261010_136_b14_session_hierarchy.py \
  migrations/versions/20261010_137_b14_session_visuals.py \
  migrations/versions/20261010_138_b14_live_session_end.py \
  tests/test_session_panel.py \
  tests/integration/temporal/test_b14_session_hierarchy.py
run_gate RUFF uv run --locked ruff check \
  src/dante/modules/temporal/session_runtime.py \
  src/dante/modules/temporal/session_panel_api.py \
  migrations/versions/20261010_136_b14_session_hierarchy.py \
  migrations/versions/20261010_137_b14_session_visuals.py \
  migrations/versions/20261010_138_b14_live_session_end.py \
  tests/test_session_panel.py \
  tests/integration/temporal/test_b14_session_hierarchy.py \
  tests/integration/temporal/test_b14_session_panel.py \
  tests/integration/database/test_current_catalog.py \
  tests/integration/database/test_database_current_catalog.py
run_gate PY_UNIT uv run --locked pytest -q --no-cov --tb=short \
  tests/test_session_panel.py
run_gate POSTGRES uv run --locked pytest -q --no-cov --tb=short -m postgres \
  tests/integration/temporal/test_b14_session_hierarchy.py \
  tests/integration/temporal/test_b14_session_panel.py \
  tests/integration/temporal/test_b14_planned_session_execution_link.py \
  tests/integration/temporal/test_b08_b_session_pause_resume.py \
  tests/integration/temporal/test_b14_planned_session_execution_link.py \
  tests/integration/temporal/test_b14_activity_replan.py \
  tests/integration/database/test_current_catalog.py \
  tests/integration/database/test_database_current_catalog.py
cd ../.. || exit 1

# OpenAPI/Orval are generated once after the backend schemas are aligned.
# These generated files are kept in the user's WSL for exact publication
# after green verification; NEVER reset/clean generated outputs.
run_gate GENERATE pnpm api:generate
run_gate GENERATED_CHECK pnpm generated:check
run_gate API_TYPECHECK pnpm --filter @dante/api-client typecheck
run_gate WEB_TYPECHECK pnpm --filter @dante/web typecheck
run_gate WEB_LINT pnpm exec eslint \
  apps/web/src/features/temporal/use-session-panel.ts \
  apps/web/src/features/home/ui/timeline/timeline-session-panel.tsx \
  apps/web/src/features/home/ui/timeline/timeline-session-reality.ts \
  apps/web/src/features/home/ui/timeline/timeline-session-reality.test.ts \
  apps/web/src/features/home/ui/timeline/timeline-session-panel.test.tsx \
  apps/web/src/features/home/ui/timeline/timeline-day-stream.tsx
run_gate VITEST pnpm --filter @dante/web exec vitest run \
  src/features/home/ui/timeline/timeline-session-panel.test.tsx \
  src/features/home/ui/timeline/timeline-session-reality.test.ts \
  src/features/home/ui/timeline/timeline-surface.test.tsx \
  src/features/home/ui/timeline/timeline-runtime-detail-controls.test.tsx \
  src/features/temporal/session-subject-controls.test.tsx \
  src/features/temporal/activity-session-card-controls.test.tsx \
  src/features/temporal/activity-planned-sessions-card-detail.test.tsx \
  src/features/temporal/remote-session-data-source.test.ts \
  src/features/home/ui/timeline/activity-inspector-actions.test.tsx \
  src/features/temporal-create/ui/temporal-create-entry-u2.test.tsx
run_gate BROWSER pnpm --filter @dante/web exec playwright test \
  --config playwright.session-panel.config.ts

echo
echo "===== B14 LIVE SESSION — GATE UNICO ====="
FAILED=0
for name in PY_SYNTAX RUFF PY_UNIT POSTGRES GENERATE GENERATED_CHECK \
            API_TYPECHECK WEB_TYPECHECK WEB_LINT VITEST BROWSER; do
  printf '%-20s %s\n' "$name" "${RESULT[$name]:-NON_ESEGUITO}"
  if [ "${RESULT[$name]:-1}" -ne 0 ]; then FAILED=1; fi
done
echo "LOG_DIR=$LOG_DIR"
git status --short
if [ "$FAILED" -ne 0 ]; then
  echo "CANDIDATO NON VERIFICATO: invia i log rossi, non ripulire i file generati."
  exit 1
fi
echo "Gate tecnico mirato verde. UI e comportamento reale da accettare separatamente."
