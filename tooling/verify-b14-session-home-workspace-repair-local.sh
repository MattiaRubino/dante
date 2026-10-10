#!/usr/bin/env bash
# B14 workspace repair gate — rerun only checks affected by the red 2026-10-10 gate.
# No CI, no generation, no commit/push/reset/clean; keep local Orval artifacts.
set +e
cd "$(dirname "$0")/.." || exit 1
if [ "$(git branch --show-current)" != "feature/timeline-temporal-operational" ]; then
  echo "ERR: expected feature/timeline-temporal-operational"
  exit 1
fi
LOG_DIR="$(mktemp -d /tmp/dante-b14-workspace-repair.XXXXXX)"
declare -A STATUS
gate() {
  local name="$1"; shift
  "$@" > "$LOG_DIR/$name.log" 2>&1
  STATUS["$name"]=$?
  printf '%-20s %s\n' "$name" "${STATUS[$name]}"
  if [ "${STATUS[$name]}" -ne 0 ]; then
    echo "----- $name: tail (full log $LOG_DIR/$name.log) -----"
    tail -n 180 "$LOG_DIR/$name.log"
  fi
}
cd apps/backend || exit 1
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
gate POSTGRES uv run --locked pytest -q --no-cov --tb=short -m postgres \
  tests/integration/temporal/test_b14_objective_input.py \
  tests/integration/temporal/test_b14_home_workspace.py \
  tests/integration/temporal/test_b14_session_panel.py \
  tests/integration/temporal/test_b14_session_hierarchy.py \
  tests/integration/temporal/test_b14_planned_session_execution_link.py \
  tests/integration/database/test_current_catalog.py \
  tests/integration/database/test_database_current_catalog.py
cd ../.. || exit 1
gate WEB_TYPECHECK pnpm --filter @dante/web typecheck
gate WEB_LINT pnpm exec eslint \
  apps/web/src/features/temporal/objective-controls.tsx \
  apps/web/src/features/temporal/objective-controls.test.tsx \
  apps/web/src/features/temporal/remote-reality-objective-data-source.ts \
  apps/web/src/features/home/ui/context-rail/context-rail.tsx \
  apps/web/src/features/home/ui/context-rail/context-rail-work-data-source.ts \
  apps/web/src/features/home/ui/context-rail/context-rail.test.tsx
gate VITEST_CHANGED pnpm --filter @dante/web exec vitest run \
  src/features/temporal/objective-controls.test.tsx \
  src/features/home/ui/context-rail/context-rail.test.tsx

echo
echo "===== B14 HOME WORKSPACE — ONLY REPAIR GATE ====="
failed=0
for name in RUFF POSTGRES WEB_TYPECHECK WEB_LINT VITEST_CHANGED; do
  printf '%-20s %s\n' "$name" "${STATUS[$name]:-NON_ESEGUITO}"
  if [ "${STATUS[$name]:-1}" -ne 0 ]; then failed=1; fi
done
echo "LOG_DIR=$LOG_DIR"
echo "----- Existing uncommitted files (PRESERVE) -----"
git status --short
if [ "$failed" -ne 0 ]; then
  echo "CANDIDATE NOT ACCEPTED; keep generated API files, send summary + red logs."
  exit 1
fi
echo "Targeted repair gate green; real-app UX acceptance and API artifact publication still open."
