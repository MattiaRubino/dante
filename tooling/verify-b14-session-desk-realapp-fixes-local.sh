#!/usr/bin/env bash
# B14 follow-up: targeted Session desk UI/Stop proof after real-app feedback.
# No pull/CI/commit/push/reset/clean, no API-client regeneration.
set +e
cd "$(dirname "$0")/.." || exit 1
if [ "$(git branch --show-current)" != "feature/timeline-temporal-operational" ]; then
  echo "ERR: branch atteso feature/timeline-temporal-operational"
  exit 1
fi
LOG_DIR="$(mktemp -d /tmp/dante-session-desk-realapp.XXXXXX)"
declare -A STATUS
gate() {
  local label="$1"; shift
  "$@" > "$LOG_DIR/$label.log" 2>&1
  STATUS["$label"]=$?
  printf '%-19s %s\n' "$label" "${STATUS[$label]}"
  if [ "${STATUS[$label]}" -ne 0 ]; then
    echo "----- $label -----"
    tail -n 135 "$LOG_DIR/$label.log"
  fi
}
cd apps/backend || exit 1
gate PY_SYNTAX uv run --locked python -m compileall -q \
  src/dante/modules/temporal/session_panel_api.py \
  tests/test_session_panel.py \
  tests/integration/temporal/test_b14_session_panel.py \
  tests/integration/temporal/test_b14_session_hierarchy.py
gate RUFF uv run --locked ruff check \
  src/dante/modules/temporal/session_panel_api.py \
  tests/test_session_panel.py \
  tests/integration/temporal/test_b14_session_panel.py \
  tests/integration/temporal/test_b14_session_hierarchy.py
gate PY_UNIT uv run --locked pytest -q --no-cov --tb=short tests/test_session_panel.py
gate POSTGRES uv run --locked pytest -q --no-cov --tb=short -m postgres \
  tests/integration/temporal/test_b14_session_panel.py \
  tests/integration/temporal/test_b14_session_hierarchy.py
cd ../.. || exit 1

gate WEB_TYPECHECK pnpm --filter @dante/web typecheck
gate WEB_LINT pnpm exec eslint \
  apps/web/src/features/home/ui/timeline/timeline-session-panel.tsx \
  apps/web/src/features/home/ui/timeline/timeline-surface.tsx \
  apps/web/src/features/home/ui/timeline/timeline-session-panel.test.tsx \
  apps/web/src/features/temporal/use-session-panel.ts \
  apps/web/tests-browser/session-panel/session-panel.spec.ts
gate VITEST pnpm --filter @dante/web exec vitest run \
  src/features/home/ui/timeline/timeline-session-panel.test.tsx
gate BROWSER pnpm --filter @dante/web exec playwright test \
  --config playwright.session-panel.config.ts
echo
echo "===== B14 SESSION DESK / REAL APP FIXES ====="
failed=0
for name in PY_SYNTAX RUFF PY_UNIT POSTGRES WEB_TYPECHECK WEB_LINT VITEST BROWSER; do
  printf '%-19s %s\n' "$name" "${STATUS[$name]:-NON_ESEGUITO}"
  if [ "${STATUS[$name]:-1}" -ne 0 ]; then failed=1; fi
done
echo "LOG_DIR=$LOG_DIR"
git status --short
if [ "$failed" -ne 0 ]; then
  echo "FIX NON VERIFICATA — conservare tutti i file generati."
  exit 1
fi
echo "Gate mirato verde. Verifica della Home reale ancora richiesta."
