#!/usr/bin/env bash
# Full branch test inventory gate. Run in the user's prepared WSL environment.
# Every group runs even if another group fails; artifacts stay in ignored temp/.
set -u

cd "$(dirname "$0")/.." || exit 1
if [ "$(git branch --show-current)" != "feature/timeline-temporal-operational" ]; then
  echo "Expected feature/timeline-temporal-operational"
  exit 1
fi

# Keep complete evidence in the repository work area without modifying Git sources.
output_root="${DANTE_GATE_OUTPUT_ROOT:-$PWD/temp}"
mkdir -p "$output_root" || exit 1
log_dir="$(mktemp -d "$output_root/dante-all-tests.XXXXXX")" || exit 1
declare -a names=()
declare -a results=()

candidate_fingerprint() {
  {
    git diff HEAD --binary
    git ls-files --others --exclude-standard -z | sort -z | xargs -0 -r sha256sum
  } | sha256sum | cut -d' ' -f1
}

source_before="$(candidate_fingerprint)" || exit 1

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
echo "SOURCE_FINGERPRINT=$source_before"
echo "LOG_DIR=$log_dir"
echo "All checks use the current source tree; generated:check snapshots and restores generated sources."
echo "No Git write, CI, deployment, or provider-side acceptance is run."

gate DIFF_CHECK . git diff --check
gate TEST_FILE_NAMES . python3 tooling/check-test-file-names.py
gate TEST_INTEGRITY . python3 tooling/testing/verify_test_integrity.py
gate BACKEND_FORMAT apps/backend uv run --locked ruff format --check .
gate BACKEND_RUFF apps/backend uv run --locked ruff check .
gate BACKEND_MYPY apps/backend uv run --locked mypy src tests tooling
gate REPO_FORMAT . pnpm format:check
gate REPO_ESLINT . pnpm lint
gate REPO_TYPECHECK . pnpm typecheck
gate ARCHITECTURE . pnpm architecture:check
gate GENERATED_DRIFT . pnpm generated:check
gate REPO_BUILD . pnpm build
gate MOBILE_BUNDLE . pnpm mobile:bundle:check
gate OBSERVABILITY_STATIC . pnpm observability:validate
gate BACKEND_NON_POSTGRES apps/backend uv run --locked pytest -q --no-cov --tb=short -m 'not postgres'
gate BACKEND_POSTGRES apps/backend uv run --locked pytest -q --no-cov --tb=short -m postgres
gate EVAL_TOOLING . uv run --project apps/backend --locked pytest -q --no-cov --tb=short tooling/ai-evals/tests
gate OBSERVABILITY_TOOLING . env PYTHONPATH=. uv run --project apps/backend --locked pytest -q --no-cov --tb=short tooling/observability/tests
gate FRONTEND_PROTOTYPE_CONTRACT . python3 tests/prototypes/frontend-preprod-contracts.py
gate WORLD_PROTOTYPE_CONTRACT . python3 tests/prototypes/world-focus-preprod-contracts.py
gate API_CLIENT_TESTS packages/api-client pnpm test
gate I18N_TESTS packages/i18n pnpm test
gate TIME_TESTS packages/time pnpm test
gate WEB_VITEST apps/web pnpm test
gate WEB_BROWSER_FIXTURE apps/web pnpm exec playwright test --config playwright.session-panel.config.ts
gate WEB_BROWSER_NONAUTH apps/web pnpm exec playwright test --config playwright.config.ts
gate WEB_BROWSER_REAL_STACK . python3 tooling/testing/run_real_stack_playwright.py

echo "===== ALL TEST GROUPS ====="
failed=0
for i in "${!names[@]}"; do
  printf '%-23s %s\n' "${names[$i]}" "${results[$i]}"
  if [ "${results[$i]}" -ne 0 ]; then failed=1; fi
done
source_after="$(candidate_fingerprint)" || exit 1
if [ "$source_after" != "$source_before" ]; then
  echo "SOURCE_STABILITY        1 (worktree changed while the gate ran)"
  failed=1
else
  echo "SOURCE_STABILITY        0"
fi
echo "SOURCE_FINGERPRINT=$source_after"
echo "LOG_DIR=$log_dir"
echo "WORKTREE_STATUS:"
git status --short
exit "$failed"
