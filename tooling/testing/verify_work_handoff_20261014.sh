#!/usr/bin/env bash
# Consolidated 2026-10-14 post-Work source verification.
# Protect current feature behavior and collect full diagnostics before another
# expensive 27-group Postgres/browser gate.
set -euo pipefail
ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"
BRANCH="feature/timeline-temporal-operational"
if [[ "$(git branch --show-current)" != "$BRANCH" ]]; then
  echo "STOP: wrong branch" >&2
  exit 2
fi
if [[ -n "$(git status --porcelain)" ]]; then
  echo "STOP: uncommitted changes; nothing has been modified" >&2
  git status --short
  exit 2
fi
git pull --ff-only origin "$BRANCH"

D="temp/work-handoff-check-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$D"
git rev-parse HEAD > "$D/START_HEAD.txt"
archive="temp/WORK_HANDOFF_CHECK_LOGS.tar.gz"
archive_logs() {
  cp "$D/SUMMARY.txt" temp/WORK_HANDOFF_CHECK_SUMMARY.txt 2>/dev/null || true
  tar -czf "$archive" -C temp "$(basename "$D")"
  echo "LOGS=$ROOT/$archive"
}
blocked() {
  echo "$1=FAIL; no commit or push" | tee "$D/SUMMARY.txt"
  archive_logs
  exit 2
}

# Formatter-only updates on a clean source tree; never run global eslint --fix
# because it previously damaged legitimate TypeScript/DOM contracts.
(cd apps/backend && uv run --locked ruff format .) > "$D/PYTHON_FORMAT.log" 2>&1 || blocked PYTHON_FORMAT
pnpm format > "$D/REPO_FORMAT.log" 2>&1 || blocked REPO_FORMAT
git diff --check > "$D/DIFF_CHECK.log" 2>&1 || blocked DIFF_CHECK
(cd apps/backend && uv run --locked python -m compileall -q src tests migrations tooling) > "$D/PYTHON_COMPILE.log" 2>&1 || blocked PYTHON_COMPILE
pnpm generated:check > "$D/GENERATED_DRIFT.log" 2>&1 || blocked GENERATED_DRIFT
pnpm typecheck > "$D/REPO_TYPECHECK.log" 2>&1 || blocked REPO_TYPECHECK
pnpm format:check > "$D/REPO_FORMAT_CHECK.log" 2>&1 || blocked REPO_FORMAT_CHECK
(cd apps/backend && uv run --locked ruff format --check .) > "$D/PYTHON_FORMAT_CHECK.log" 2>&1 || blocked PYTHON_FORMAT_CHECK

if ! git diff --quiet; then
  git add -u
  git diff --cached --check
  git diff --cached --stat > "$D/FORMAT_DELTA.txt"
  git commit -m "style(gate): normalize 2026-10-14 Work handoff source repairs"
  git push origin "$BRANCH"
fi
git rev-parse HEAD > "$D/HEAD.txt"

# Independent read-only validators run in parallel. They do not skip any
# lint/type assertions; unlike the full gate these do not use Docker.
set +e
(cd apps/backend && uv run --locked ruff check .) > "$D/RUFF.log" 2>&1 &
ruff_pid=$!
(cd apps/backend && uv run --locked mypy src tests tooling) > "$D/MYPY.log" 2>&1 &
mypy_pid=$!
pnpm lint > "$D/ESLINT.log" 2>&1 &
eslint_pid=$!
pnpm --filter @dante/web test > "$D/WEB_VITEST.log" 2>&1 &
vitest_pid=$!
wait "$ruff_pid"; RUFF=$?
wait "$mypy_pid"; MYPY=$?
wait "$eslint_pid"; ESLINT=$?
wait "$vitest_pid"; WEB_VITEST=$?
set -e

printf 'START_HEAD=%s\nHEAD=%s\nPYTHON_COMPILE=0\nREPO_TYPECHECK=0\nGENERATED_DRIFT=0\nPYTHON_FORMAT=0\nREPO_FORMAT=0\nRUFF=%s\nMYPY=%s\nESLINT=%s\nWEB_VITEST=%s\n' \
  "$(cat "$D/START_HEAD.txt")" "$(cat "$D/HEAD.txt")" \
  "$RUFF" "$MYPY" "$ESLINT" "$WEB_VITEST" | tee "$D/SUMMARY.txt"
tail -n 3 "$D/RUFF.log" || true
tail -n 2 "$D/MYPY.log" || true
tail -n 6 "$D/ESLINT.log" || true
tail -n 12 "$D/WEB_VITEST.log" || true
archive_logs
if (( RUFF || MYPY || ESLINT || WEB_VITEST )); then
  exit 1
fi
echo "STATIC_AND_WEB_UNIT=ALL_GREEN"
