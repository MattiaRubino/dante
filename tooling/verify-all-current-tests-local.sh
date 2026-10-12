#!/usr/bin/env bash
# Full branch test inventory gate. Run in the user's prepared WSL environment.
# Every group runs even if another group fails; logs stay outside the repository.
set -u

cd "$(dirname "$0")/.." || exit 1
if [ "$(git branch --show-current)" != "feature/timeline-temporal-operational" ]; then
  echo "Expected feature/timeline-temporal-operational"
  exit 1
fi

log_dir="$(mktemp -d /tmp/dante-all-tests.XXXXXX)" || exit 1
declare -a names=()
declare -a results=()

gate() {
  local name="$1" directory="$2" result
  shift 2
  echo "RUN $name"
  (cd "$directory" && "$@") >"$log_dir/$name.log" 2>&1
  result=$?
  names+=("$name")
  results+=("$result")
  printf '%-23s %s\n' "$name" "$result"
  if [ "$result" -ne 0 ]; then
    tail -n 24 "$log_dir/$name.log"
  fi
}

echo "BRANCH=$(git branch --show-current)"
echo "HEAD=$(git rev-parse HEAD)"
echo "LOG_DIR=$log_dir"
echo "All tests use the current source tree; no generator, cleanup, CI or Git write is run."

gate BACKEND_NON_POSTGRES apps/backend uv run --locked pytest -q --no-cov --tb=short -m 'not postgres'
gate BACKEND_POSTGRES apps/backend uv run --locked pytest -q --no-cov --tb=short -m postgres
gate EVAL_TOOLING . uv run --project apps/backend --locked pytest -q --no-cov --tb=short tooling/ai-evals/tests
gate OBSERVABILITY_TOOLING . uv run --project apps/backend --locked pytest -q --no-cov --tb=short tooling/observability/tests
gate FRONTEND_PROTOTYPE_CONTRACT . python3 tests/prototypes/frontend-preprod-contracts.py
gate WORLD_PROTOTYPE_CONTRACT . python3 tests/prototypes/world-focus-preprod-contracts.py
gate API_CLIENT_TESTS packages/api-client pnpm test
gate I18N_TESTS packages/i18n pnpm test
gate TIME_TESTS packages/time pnpm test
gate WEB_VITEST apps/web pnpm test
gate WEB_BROWSER_FIXTURE apps/web pnpm exec playwright test --config playwright.session-panel.config.ts
gate WEB_BROWSER_NONAUTH apps/web pnpm exec playwright test --config playwright.config.ts
gate WEB_BROWSER_REAL_STACK apps/web pnpm exec playwright test --config playwright.auth.config.ts

echo "===== ALL TEST GROUPS ====="
failed=0
for i in "${!names[@]}"; do
  printf '%-23s %s\n' "${names[$i]}" "${results[$i]}"
  if [ "${results[$i]}" -ne 0 ]; then failed=1; fi
done
echo "LOG_DIR=$log_dir"
echo "WORKTREE_STATUS:"
git status --short
exit "$failed"
