#!/usr/bin/env bash
# B14 M5 whole Objective editor gate. User-local PostgreSQL; no CI or auto-commit.
set +e
cd "$(dirname "$0")/.." || exit 1

if [ "$(git branch --show-current)" != "feature/timeline-temporal-operational" ]; then
  echo "ERRORE: esegui il gate sul branch feature/timeline-temporal-operational."
  exit 1
fi

LOG_DIR="$(mktemp -d /tmp/dante-m5-objectives.XXXXXX)"
declare -A RESULT

run_gate() {
  local name="$1"
  shift
  "$@" >"$LOG_DIR/$name.log" 2>&1
  RESULT["$name"]=$?
  printf '%-20s %s\n' "$name" "${RESULT[$name]}"
  if [ "${RESULT[$name]}" -ne 0 ]; then
    echo "----- $name: dettaglio -----"
    tail -n 120 "$LOG_DIR/$name.log"
  fi
  return 0
}

run_gate PULL git pull --ff-only origin feature/timeline-temporal-operational
if [ "${RESULT[PULL]}" -ne 0 ]; then
  echo "Pull fermato per proteggere eventuali modifiche locali. Log: $LOG_DIR"
  exit 1
fi

cd apps/backend || exit 1
run_gate SYNTAX uv run --locked python -m compileall -q \
  migrations/versions/20261009_133_b14_objective_retirement.py \
  src/dante/modules/temporal/reality_objective_api.py \
  src/dante/platform/database/mappings/b14_create_closure.py \
  tests/integration/temporal/test_b14_m5_objective_editor.py
run_gate RUFF uv run --locked ruff check \
  migrations/versions/20261009_133_b14_objective_retirement.py \
  src/dante/modules/temporal/reality_objective_api.py \
  src/dante/platform/database/mappings/b14_create_closure.py \
  tests/integration/temporal/test_b14_m5_objective_editor.py
run_gate POSTGRES uv run --locked pytest -q --no-cov --tb=short -m postgres \
  tests/integration/temporal/test_b14_m5_objective_editor.py \
  tests/integration/temporal/test_b14_m2_objective_corrections.py \
  tests/integration/temporal/test_b14_m2_objective_scope.py \
  tests/integration/temporal/test_b14_activity_edit_snapshot.py \
  tests/integration/database/test_current_catalog.py \
  tests/integration/database/test_database_current_catalog.py

cd ../.. || exit 1
run_gate GENERATE pnpm api:generate
run_gate GENERATED_CHECK pnpm generated:check
run_gate API_TYPECHECK pnpm --filter @dante/api-client typecheck
run_gate WEB_TYPECHECK pnpm --filter @dante/web typecheck
run_gate VITEST pnpm --filter @dante/web exec vitest run \
  src/features/home/ui/timeline/activity-inspector-actions.test.tsx \
  src/features/temporal/remote-activity-edit-settings.test.ts \
  src/features/temporal/objective-controls.test.tsx

echo
echo "===== GATE COMPLETO B14 M5 OBIETTIVI ====="
FAILED=0
for name in PULL SYNTAX RUFF POSTGRES GENERATE GENERATED_CHECK API_TYPECHECK WEB_TYPECHECK VITEST; do
  printf '%-20s %s\n' "$name" "${RESULT[$name]:-NON_ESEGUITO}"
  if [ "${RESULT[$name]:-1}" -ne 0 ]; then FAILED=1; fi
done
echo "LOG_DIR=$LOG_DIR"
git status --short
if [ "$FAILED" -ne 0 ]; then
  echo "CANDIDATO NON PROVATO. Invia il riepilogo e i log dei gate rossi."
  exit 1
fi

echo "GATE TECNICO VERDE. Ora verifica in app il flusso con un solo Salva modifiche."
echo "Controlla il diff generato da pnpm api:generate; nessun commit o push automatico."
