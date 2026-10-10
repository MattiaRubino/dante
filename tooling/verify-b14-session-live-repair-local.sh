#!/usr/bin/env bash
# B14 live Session: one targeted repair gate after the first full gate.
# No pull, CI, commit, push, reset, clean or persistent application DB writes.
set +e
cd "$(dirname "$0")/.." || exit 1
if [ "$(git branch --show-current)" != "feature/timeline-temporal-operational" ]; then
  echo "ERR: branch errato."
  exit 1
fi
LOG_DIR="$(mktemp -d /tmp/dante-session-live-repair.XXXXXX)"
declare -A RESULTS
run_gate() {
  local key="$1"; shift
  "$@" >"$LOG_DIR/$key.log" 2>&1
  RESULTS["$key"]=$?
  printf '%-19s %s\n' "$key" "${RESULTS[$key]}"
  if [ "${RESULTS[$key]}" -ne 0 ]; then
    echo "=== $key — dettaglio ==="
    tail -n 145 "$LOG_DIR/$key.log"
  fi
}
cd apps/backend || exit 1
run_gate PY_SYNTAX uv run --locked python -m compileall -q \
  migrations/versions/20261010_138_b14_live_session_end.py \
  tests/integration/temporal/test_b14_session_hierarchy.py \
  tests/integration/temporal/test_b14_planned_session_execution_link.py \
  tests/integration/temporal/test_b08_b_session_pause_resume.py
run_gate RUFF uv run --locked ruff check \
  migrations/versions/20261010_138_b14_live_session_end.py \
  tests/integration/temporal/test_b14_session_hierarchy.py \
  tests/integration/temporal/test_b14_planned_session_execution_link.py \
  tests/integration/temporal/test_b08_b_session_pause_resume.py \
  tests/integration/database/test_current_catalog.py \
  tests/integration/database/test_database_current_catalog.py
run_gate POSTGRES uv run --locked pytest -q --no-cov --tb=short -m postgres \
  tests/integration/temporal/test_b14_session_hierarchy.py \
  tests/integration/temporal/test_b14_session_panel.py \
  tests/integration/temporal/test_b14_planned_session_execution_link.py \
  tests/integration/temporal/test_b08_b_session_pause_resume.py \
  tests/integration/temporal/test_b14_activity_replan.py \
  tests/integration/database/test_current_catalog.py \
  tests/integration/database/test_database_current_catalog.py
cd ../.. || exit 1
# Backend HTTP schema unchanged since the user's prior successful GENERATE.
# Keep all seven local generated Orval assets exactly as they are.
run_gate WEB_TYPECHECK pnpm --filter @dante/web typecheck
run_gate WEB_LINT pnpm exec eslint \
  apps/web/src/features/temporal/use-session-panel.ts \
  apps/web/src/features/home/ui/timeline/timeline-session-panel.test.tsx
run_gate VITEST pnpm --filter @dante/web exec vitest run \
  src/features/home/ui/timeline/timeline-session-panel.test.tsx
run_gate BROWSER pnpm --filter @dante/web exec playwright test \
  --config playwright.session-panel.config.ts

echo
echo "===== B14 SESSIONI — REPAIR GATE ====="
FAILED=0
for name in PY_SYNTAX RUFF POSTGRES WEB_TYPECHECK WEB_LINT VITEST BROWSER; do
  printf '%-19s %s\n' "$name" "${RESULTS[$name]:-NON_ESEGUITO}"
  if [ "${RESULTS[$name]:-1}" -ne 0 ]; then FAILED=1; fi
done
echo "LOG_DIR=$LOG_DIR"
git status --short
if [ "$FAILED" -ne 0 ]; then
  echo "RIPARAZIONE NON VERIFICATA: non cancellare i file API generati."
  exit 1
fi
echo "Gate tecnico mirato verde; pubblicazione Orval e accettazione reale ancora aperte."
