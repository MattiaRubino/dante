#!/usr/bin/env bash
# One user-local gate for B14 Draft Vault. No commits, push or CI.
set +e
cd "$(dirname "$0")/.." || exit 1
if [ "$(git branch --show-current)" != "feature/timeline-temporal-operational" ]; then
  echo "ERR: usare il branch feature/timeline-temporal-operational."
  exit 1
fi

LOG_DIR="$(mktemp -d /tmp/dante-draft-vault.XXXXXX)"
declare -A RESULT
run_gate() {
  local name="$1"
  shift
  "$@" >"$LOG_DIR/$name.log" 2>&1
  RESULT["$name"]=$?
  printf '%-20s %s\n' "$name" "${RESULT[$name]}"
  if [ "${RESULT[$name]}" -ne 0 ]; then
    echo "----- $name (ultime 120 righe) -----"
    tail -n 120 "$LOG_DIR/$name.log"
  fi
  return 0
}

cd apps/backend || exit 1
run_gate SYNTAX uv run --locked python -m compileall -q \
  src/dante/modules/temporal/draft_vault_api.py \
  src/dante/platform/database/mappings/draft_vault.py \
  migrations/versions/20261009_134_b14_draft_vault.py \
  tests/integration/temporal/test_b14_draft_vault.py
run_gate RUFF uv run --locked ruff check \
  src/dante/modules/temporal/draft_vault_api.py \
  src/dante/platform/database/mappings/draft_vault.py \
  src/dante/platform/database/mappings/__init__.py \
  src/dante/bootstrap/app.py \
  migrations/versions/20261009_134_b14_draft_vault.py \
  tests/integration/temporal/test_b14_draft_vault.py \
  tests/integration/database/test_current_catalog.py \
  tests/integration/database/test_database_current_catalog.py
run_gate POSTGRES uv run --locked pytest -q --no-cov --tb=short -m postgres \
  tests/integration/temporal/test_b14_draft_vault.py \
  tests/integration/database/test_current_catalog.py \
  tests/integration/database/test_database_current_catalog.py
cd ../.. || exit 1

run_gate GENERATE pnpm api:generate
run_gate GENERATED_CHECK pnpm generated:check
run_gate API_TYPECHECK pnpm --filter @dante/api-client typecheck
run_gate WEB_TYPECHECK pnpm --filter @dante/web typecheck
run_gate WEB_VITEST pnpm --filter @dante/web exec vitest run \
  src/features/temporal-create/application/remote-draft-vault.test.ts \
  src/features/temporal-create/ui/temporal-create-composer.test.tsx \
  src/features/temporal-create/ui/temporal-create-draft-vault.test.tsx \
  src/features/temporal-create/ui/temporal-create-entry-u2.test.tsx \
  src/features/temporal-create/ui/temporal-create-top-u1.test.tsx \
  src/features/home/ui/timeline/timeline-draft-vault.test.tsx \
  src/features/home/ui/timeline/timeline-planning-tray-b01.test.tsx \
  src/features/home/ui/timeline/activity-inspector-actions.test.tsx \
  src/features/home/ui/timeline/event-inspector-actions.test.tsx

echo
echo "==== B14 DRAFT VAULT — GATE UNICO ===="
FAILED=0
for name in SYNTAX RUFF POSTGRES GENERATE GENERATED_CHECK API_TYPECHECK WEB_TYPECHECK WEB_VITEST; do
  printf '%-20s %s\n' "$name" "${RESULT[$name]:-NON_ESEGUITO}"
  if [ "${RESULT[$name]:-1}" -ne 0 ]; then FAILED=1; fi
done
echo "LOG_DIR=$LOG_DIR"
git status --short
if [ "$FAILED" -ne 0 ]; then
  echo "CANDIDATO: verifiche da correggere. Non ripulire il worktree, invia l'esito."
  exit 1
fi
echo "Gate mirato verde. Restano accettazione reale, asset API generati e casi storici."
