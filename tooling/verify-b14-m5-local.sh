#!/usr/bin/env bash
# One local gate for the Activity Edit / planned Session M5 repair block.
set +e
cd "$(dirname "$0")/.." || exit 1

if [ "$(git branch --show-current)" != "feature/timeline-temporal-operational" ]; then
  echo "ERRORE: seleziona feature/timeline-temporal-operational."
  exit 1
fi

LOG_DIR="$(mktemp -d /tmp/dante-m5-whole.XXXXXX)"
declare -A RESULT
run_gate() {
  local name="$1"
  shift
  "$@" >"$LOG_DIR/$name.log" 2>&1
  RESULT["$name"]=$?
  printf '%-19s %s\n' "$name" "${RESULT[$name]}"
  if [ "${RESULT[$name]}" -ne 0 ]; then
    echo "----- $name: estratto errore -----"
    if [ "$name" = POSTGRES ]; then
      sed -n '/short test summary info/,$p' "$LOG_DIR/$name.log" | head -n 80
    fi
    tail -n 70 "$LOG_DIR/$name.log"
  fi
  return 0
}

run_gate PULL git pull --ff-only origin feature/timeline-temporal-operational
if [ "${RESULT[PULL]}" -ne 0 ]; then
  echo "Pull non riuscito; nessun test eseguito. Log: $LOG_DIR"
  exit 1
fi

cd apps/backend || exit 1
run_gate SYNTAX uv run --locked python -m compileall -q \
  migrations/versions/20261009_131_b14_place_unplaced_planned_schedule.py \
  migrations/versions/20261009_132_b14_retire_planned_schedule.py \
  src/dante/modules/temporal/activity_edit_snapshot_api.py \
  src/dante/modules/temporal/activity_replan_api.py
run_gate RUFF uv run --locked ruff check \
  migrations/versions/20261009_131_b14_place_unplaced_planned_schedule.py \
  migrations/versions/20261009_132_b14_retire_planned_schedule.py \
  src/dante/modules/temporal/activity_edit_snapshot_api.py \
  src/dante/modules/temporal/activity_replan_api.py \
  src/dante/platform/database/mappings/schedule.py \
  tests/integration/temporal/test_b14_activity_replan.py \
  tests/integration/temporal/test_b14_u2_authoring.py \
  tests/integration/database/test_current_catalog.py \
  tests/integration/database/test_database_current_catalog.py
run_gate UNIT uv run --locked pytest -q --no-cov --tb=short \
  tests/test_b14_activity_replan.py \
  tests/test_b14_occurrence_edit_scope.py
run_gate POSTGRES uv run --locked pytest -q --no-cov --tb=short -m postgres \
  tests/integration/temporal/test_b14_activity_replan.py \
  tests/integration/temporal/test_b14_u2_authoring.py \
  tests/integration/temporal/test_b14_activity_edit_snapshot.py \
  tests/integration/temporal/test_b14_m2_objective_corrections.py \
  tests/integration/temporal/test_b14_m2_objective_scope.py \
  tests/integration/database/test_current_catalog.py \
  tests/integration/database/test_database_current_catalog.py

cd ../.. || exit 1
run_gate GENERATE pnpm api:generate
run_gate GENERATED_CHECK pnpm generated:check
run_gate API_TYPECHECK pnpm --filter @dante/api-client typecheck
run_gate WEB_TYPECHECK pnpm --filter @dante/web typecheck
run_gate VITEST pnpm --filter @dante/web exec vitest run \
  src/features/temporal/objective-controls.test.tsx \
  src/features/temporal/activity-session-card-controls.test.tsx \
  src/features/temporal/remote-activity-edit-settings.test.ts \
  src/features/home/ui/timeline/activity-inspector-actions.test.tsx \
  src/features/home/ui/timeline/event-inspector-actions.test.tsx \
  src/features/home/ui/timeline/timeline-inspector-reality.test.tsx \
  src/features/temporal-create/application/temporal-create-u2-submit.test.ts \
  src/features/temporal-create/ui/temporal-create-entry-u2.test.tsx

echo
echo "===== RIEPILOGO UNICO B14 M5 ====="
FAILED=0
for name in PULL SYNTAX RUFF UNIT POSTGRES GENERATE GENERATED_CHECK API_TYPECHECK WEB_TYPECHECK VITEST; do
  printf '%-19s %s\n' "$name" "${RESULT[$name]:-NON_ESEGUITO}"
  if [ "${RESULT[$name]:-1}" -ne 0 ]; then FAILED=1; fi
done
echo "LOG_DIR=$LOG_DIR"
git status --short
if [ "$FAILED" -ne 0 ]; then
  echo "M5 NON VERIFICATO: invia il riepilogo e i log dei gate rossi."
  exit 1
fi
echo "M5 gate tecnico locale verde; restano i controlli reali dell'interfaccia."
