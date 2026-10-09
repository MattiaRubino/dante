#!/usr/bin/env bash
# Whole M5 visual-feedback repair gate. Runs ONLY on user's WSL, never GitHub CI.
set +e
cd "$(dirname "$0")/.." || exit 1

if [ "$(git branch --show-current)" != "feature/timeline-temporal-operational" ]; then
  echo "Branch errato: feature/timeline-temporal-operational richiesto."
  exit 1
fi

LOG_DIR="$(mktemp -d /tmp/dante-m5-ui.XXXXXX)"
declare -A RESULT

run_gate() {
  local name="$1"
  shift
  "$@" >"$LOG_DIR/$name.log" 2>&1
  RESULT["$name"]=$?
  printf '%-16s %s\n' "$name" "${RESULT[$name]}"
  if [ "${RESULT[$name]}" -ne 0 ]; then
    echo "----- $name -----"
    tail -n 100 "$LOG_DIR/$name.log"
  fi
  return 0
}

run_gate PULL git pull --ff-only origin feature/timeline-temporal-operational
if [ "${RESULT[PULL]}" -ne 0 ]; then
  echo "Pull interrotto per proteggere il worktree. LOG_DIR=$LOG_DIR"
  exit 1
fi

cd apps/backend || exit 1
run_gate SYNTAX uv run --locked python -m compileall -q \
  src/dante/modules/temporal/activity_replan_api.py \
  tests/integration/temporal/test_b14_activity_replan.py
run_gate RUFF uv run --locked ruff check \
  src/dante/modules/temporal/activity_replan_api.py \
  tests/integration/temporal/test_b14_activity_replan.py
run_gate POSTGRES uv run --locked pytest -q --no-cov --tb=short -m postgres \
  tests/integration/temporal/test_b14_activity_replan.py

cd ../.. || exit 1
run_gate WEB_TYPECHECK pnpm --filter @dante/web typecheck
run_gate VITEST pnpm --filter @dante/web exec vitest run \
  src/features/home/ui/timeline/activity-inspector-actions.test.tsx \
  src/features/temporal/remote-activity-edit-settings.test.ts \
  src/features/temporal-create/application/temporal-create-u2-submit.test.ts

echo
echo "===== GATE M5 UI — UNICO RIEPILOGO ====="
FAILED=0
for name in PULL SYNTAX RUFF POSTGRES WEB_TYPECHECK VITEST; do
  printf '%-16s %s\n' "$name" "${RESULT[$name]:-NON_ESEGUITO}"
  if [ "${RESULT[$name]:-1}" -ne 0 ]; then FAILED=1; fi
done
echo "LOG_DIR=$LOG_DIR"
git status --short
if [ "$FAILED" -ne 0 ]; then
  echo "Candidato non verificato: invia il riepilogo e i log rossi."
  exit 1
fi
echo "Gate tecnico mirato verde. M5 richiede ancora prova reale delle 4 correzioni."
