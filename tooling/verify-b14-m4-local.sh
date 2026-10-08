#!/usr/bin/env bash
# One user-local B14 M4 acceptance gate. No CI/Actions, no shell takeover.
set +e
cd "$(dirname "$0")/.." || exit 1

if [ "$(git branch --show-current)" != "feature/timeline-temporal-operational" ]; then
  echo "ERRORE: seleziona feature/timeline-temporal-operational prima del gate."
  exit 1
fi

LOG_DIR="$(mktemp -d /tmp/dante-m4-whole.XXXXXX)"
declare -A RESULT
run_gate() {
  local name="$1"
  shift
  "$@" >"$LOG_DIR/$name.log" 2>&1
  RESULT["$name"]=$?
  printf '%-19s %s\n' "$name" "${RESULT[$name]}"
  if [ "${RESULT[$name]}" -ne 0 ]; then
    echo "----- $name: estratto errore -----"
    if [ "$name" = "POSTGRES" ]; then
      sed -n '/short test summary info/,$p' "$LOG_DIR/$name.log" | head -n 80
    fi
    tail -n 70 "$LOG_DIR/$name.log"
  fi
  return 0
}

run_gate PULL git pull --ff-only origin feature/timeline-temporal-operational
if [ "${RESULT[PULL]}" -ne 0 ]; then
  echo "Pull non riuscito: nessun gate eseguito. Log: $LOG_DIR"
  exit 1
fi

cd apps/backend || exit 1
run_gate SYNTAX uv run --locked python -m compileall -q \
  migrations/versions/20261008_128_b14_m4_event_profile.py \
  src/dante/modules/temporal/event.py \
  src/dante/modules/temporal/event_api.py \
  tests/integration/temporal/test_b14_m4_event_profile.py

run_gate RUFF uv run --locked ruff check \
  migrations/versions/20261008_128_b14_m4_event_profile.py \
  src/dante/modules/temporal/event.py \
  src/dante/modules/temporal/event_api.py \
  src/dante/platform/database/mappings/event.py \
  tests/integration/temporal/test_b14_m4_event_profile.py \
  tests/integration/temporal/test_b03_event_core.py \
  tests/integration/temporal/test_b14_m3_residual_editor.py \
  tests/integration/database/test_current_catalog.py \
  tests/integration/database/test_database_current_catalog.py

run_gate UNIT uv run --locked pytest -q --no-cov --tb=short \
  tests/test_b14_occurrence_edit_scope.py \
  tests/test_b14_activity_replan.py

run_gate POSTGRES uv run --locked pytest -q --no-cov --tb=short -m postgres \
  tests/integration/temporal/test_b14_m4_event_profile.py \
  tests/integration/temporal/test_b03_event_core.py \
  tests/integration/temporal/test_b05_primary_life_area_assignment.py \
  tests/integration/temporal/test_b14_activity_inspector.py \
  tests/integration/temporal/test_b14_activity_edit_snapshot.py \
  tests/integration/temporal/test_b14_activity_replan.py \
  tests/integration/temporal/test_b14_m1_edit_inventory.py \
  tests/integration/temporal/test_b14_m1_scoped_profile_edit.py \
  tests/integration/temporal/test_b14_m2_objective_corrections.py \
  tests/integration/temporal/test_b14_m2_objective_scope.py \
  tests/integration/temporal/test_b14_m3_residual_editor.py \
  tests/integration/temporal/test_b14_m3_b_instance_scope_boundary.py \
  tests/integration/database/test_current_catalog.py \
  tests/integration/database/test_database_current_catalog.py

cd ../.. || exit 1
run_gate GENERATE pnpm api:generate
run_gate GENERATED_CHECK pnpm generated:check
run_gate API_TYPECHECK pnpm --filter @dante/api-client typecheck
run_gate WEB_TYPECHECK pnpm --filter @dante/web typecheck
run_gate VITEST pnpm --filter @dante/web exec vitest run \
  src/features/home/ui/timeline/event-inspector-actions.test.tsx \
  src/features/home/ui/timeline/timeline-authoritative-event-hydration.test.ts \
  src/features/home/ui/timeline/timeline-event-agenda-editor.test.tsx \
  src/features/home/ui/timeline/activity-inspector-actions.test.tsx \
  src/features/temporal-create/application/event-duplicate-seed.test.ts \
  src/features/temporal-create/application/activity-duplicate-seed.test.ts \
  src/features/temporal/remote-event-agenda-data-source.test.ts \
  src/features/temporal/remote-event-profile-data-source.test.ts \
  src/features/temporal/remote-event-life-area-settings.test.ts \
  src/features/temporal/remote-event-recurrence-guard.test.ts \
  src/features/temporal/remote-activity-edit-settings.test.ts \
  src/features/temporal/remote-recurring-profile-edit.test.ts

echo
echo "===== RIEPILOGO UNICO B14 M4 ====="
FAILED=0
for name in PULL SYNTAX RUFF UNIT POSTGRES GENERATE GENERATED_CHECK API_TYPECHECK WEB_TYPECHECK VITEST; do
  printf '%-19s %s\n' "$name" "${RESULT[$name]:-NON_ESEGUITO}"
  if [ "${RESULT[$name]:-1}" -ne 0 ]; then FAILED=1; fi
done
echo "LOG_DIR=$LOG_DIR"
git status --short
if [ "$FAILED" -ne 0 ]; then
  echo "M4 NON VERIFICATO: incolla riepilogo ed errori; non pubblicare il client."
  exit 1
fi
echo "M4 GATE LOCALE VERDE. Non equivale ancora all'accettazione visuale M5/B15."
if ! git diff --cached --quiet; then
  echo "Ci sono modifiche già staged: pubblicazione client automatica saltata."
  exit 0
fi
git add -- packages/api-client/openapi/dante-v1.openapi.json packages/api-client/src/generated
if ! git diff --cached --check; then
  echo "Diff client generato non valido: commit/push saltati."
  exit 1
fi
if ! git diff --cached --quiet; then
  git commit -m "chore(b14-m4): publish verified generated Event profile client [skip ci]"
  if [ "$?" -ne 0 ]; then exit 1; fi
  git push origin feature/timeline-temporal-operational
  if [ "$?" -ne 0 ]; then
    echo "Il client è committato localmente ma il push è fallito: risolvere senza force."
    exit 1
  fi
fi
echo "M4_CLIENT_PUBLISH=OK"
echo "===== FINE; IL TERMINALE RESTA APERTO ====="
