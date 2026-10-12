#!/usr/bin/env bash
set +e

cd "$(dirname "$0")/.." || exit 1
LOG_DIR="$(mktemp -d /tmp/dante-b14-oct12.XXXXXX)"
declare -A STATUS

gate() {
  local name="$1"
  shift
  "$@" >"$LOG_DIR/$name.log" 2>&1
  STATUS["$name"]=$?
  printf '%-17s %s\n' "$name" "${STATUS[$name]}"
  if [ "${STATUS[$name]}" -ne 0 ]; then
    tail -n 90 "$LOG_DIR/$name.log"
  fi
}

cd apps/backend || exit 1
gate RUFF uv run --locked ruff check \
  src/dante/modules/temporal/routine_occurrence_materialization.py \
  tests/test_routine_occurrence_untimed_template.py \
  tests/integration/temporal/test_b14_recurring_untimed_planned_session.py
gate PY_UNIT uv run --locked pytest -q --no-cov --tb=short \
  tests/test_routine_occurrence_untimed_template.py
gate POSTGRES uv run --locked pytest -q --no-cov --tb=short -m postgres \
  tests/integration/temporal/test_b14_recurring_untimed_planned_session.py
cd ../.. || exit 1

gate WEB_TYPECHECK pnpm --filter @dante/web typecheck
gate WEB_LINT pnpm exec eslint \
  apps/web/src/features/home/ui/timeline/activity-edit-panel.tsx \
  apps/web/src/features/home/ui/timeline/activity-objective-row.tsx \
  apps/web/src/features/home/ui/timeline/timeline-session-reality.ts \
  apps/web/src/features/home/ui/timeline/timeline-session-reality.test.ts \
  apps/web/src/features/home/ui/timeline/timeline-surface.tsx \
  apps/web/src/features/home/ui/timeline/timeline-surface.test.tsx \
  apps/web/src/features/temporal/remote-activity-edit-settings.ts \
  apps/web/src/features/temporal/activity-session-card-controls.tsx \
  apps/web/src/features/temporal/activity-session-card-controls.test.tsx \
  apps/web/src/features/temporal-create/application/temporal-create-u2-submit.ts \
  apps/web/src/features/temporal-create/application/temporal-create-u2-submit.test.ts \
  apps/web/src/features/temporal-create/application/remote-recurring-authoring.ts
gate VITEST pnpm --filter @dante/web exec vitest run \
  src/features/temporal-create/application/temporal-create-u2-submit.test.ts \
  src/features/temporal/activity-session-card-controls.test.tsx \
  src/features/home/ui/timeline/timeline-session-reality.test.ts \
  src/features/home/ui/timeline/timeline-surface.test.tsx

echo "LOG_DIR=$LOG_DIR"
failed=0
for name in RUFF PY_UNIT POSTGRES WEB_TYPECHECK WEB_LINT VITEST; do
  if [ "${STATUS[$name]:-1}" -ne 0 ]; then failed=1; fi
done
if [ "$failed" -ne 0 ]; then
  echo 'CANDIDATO NON VERIFICATO: invia il riepilogo e i log rossi.'
  exit 1
fi
echo 'Gate mirato verde; accettazione nella app reale ancora aperta.'
