#!/usr/bin/env bash
# One-shot verification of the post-d8914007 source fixes. Does not run the
# long 27-group PostgreSQL/browser gate until the static debt is addressed.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"

EXPECTED_BRANCH="feature/timeline-temporal-operational"
if [[ "$(git branch --show-current)" != "$EXPECTED_BRANCH" ]]; then
  echo "STOP: wrong branch" >&2
  exit 2
fi
if [[ -n "$(git status --porcelain)" ]]; then
  echo "STOP: uncommitted local changes; nothing touched" >&2
  git status --short
  exit 2
fi
git pull --ff-only origin "$EXPECTED_BRANCH"

D="temp/static-repair-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$D"
git rev-parse HEAD > "$D/BASE_HEAD.txt"

(cd apps/backend && uv run --locked ruff format .) > "$D/RUFF_FORMAT.log" 2>&1
pnpm format > "$D/PRETTIER_FORMAT.log" 2>&1
git diff --check > "$D/DIFF_CHECK.log" 2>&1
(cd apps/backend && uv run --locked ruff format --check .) > "$D/RUFF_FORMAT_CHECK.log" 2>&1
pnpm format:check > "$D/PRETTIER_CHECK.log" 2>&1
pnpm generated:check > "$D/GENERATED_CHECK.log" 2>&1
# Source repairs span SQLAlchemy and historical migrations; compile all Python
# files before pushing formatter adjustments, even while mypy still has debt.
(cd apps/backend && uv run --locked python -m compileall -q src tests migrations tooling) \
  > "$D/PYTHON_COMPILE.log" 2>&1 || {
  echo "PYTHON_COMPILE=RED; no commit or push" | tee "$D/SUMMARY.txt"
  tar -czf temp/STATIC_REPAIR_LOGS.tar.gz -C temp "$(basename "$D")"
  echo "LOGS=~/projects/dante/temp/STATIC_REPAIR_LOGS.tar.gz"
  exit 2
}
pnpm typecheck > "$D/TYPECHECK.log" 2>&1 || {
  echo "TYPECHECK=RED; no commit or push" | tee "$D/SUMMARY.txt"
  tar -czf temp/STATIC_REPAIR_LOGS.tar.gz -C temp "$(basename "$D")"
  echo "LOGS=~/projects/dante/temp/STATIC_REPAIR_LOGS.tar.gz"
  exit 2
}

if [[ -n "$(git status --porcelain)" ]]; then
  git add -u
  git diff --cached --check
  git diff --cached --stat > "$D/FORMATTED_FILES.txt"
  git commit -m "style(gate): normalize verified source fixes after d8914007"
  git push origin "$EXPECTED_BRANCH"
fi
git rev-parse HEAD > "$D/HEAD.txt"

# Capture precise, unsuppressed errors in parallel, not 27 unrelated groups.
set +e
(cd apps/backend && uv run --locked ruff check .) > "$D/RUFF.log" 2>&1 &
RUFF_PID=$!
(cd apps/backend && uv run --locked mypy src tests tooling) > "$D/MYPY.log" 2>&1 &
MYPY_PID=$!
pnpm lint > "$D/ESLINT.log" 2>&1 &
ESLINT_PID=$!
wait "$RUFF_PID"
RUFF=$?
wait "$MYPY_PID"
MYPY=$?
wait "$ESLINT_PID"
ESLINT=$?
set -e

printf 'HEAD=%s\nTYPECHECK=0\nRUFF=%s\nMYPY=%s\nESLINT=%s\n' \
  "$(cat "$D/HEAD.txt")" "$RUFF" "$MYPY" "$ESLINT" \
  | tee "$D/SUMMARY.txt"
tail -n 3 "$D/RUFF.log" || true
tail -n 2 "$D/MYPY.log" || true
tail -n 5 "$D/ESLINT.log" || true

tar -czf temp/STATIC_REPAIR_LOGS.tar.gz -C temp "$(basename "$D")"
echo "LOGS=~/projects/dante/temp/STATIC_REPAIR_LOGS.tar.gz"
