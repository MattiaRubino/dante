#!/usr/bin/env bash
# DANTE full-gate style repair: only built-in safe auto-fixes, no rule suppression.
# Run from any directory. Writes evidence to ignored temp/, then pushes one
# atomic style commit only after typecheck, generated drift, and formatting pass.
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"

BRANCH="feature/timeline-temporal-operational"
if [[ "$(git branch --show-current)" != "$BRANCH" ]]; then
  echo "STOP: expected branch $BRANCH" >&2
  exit 2
fi
if [[ -n "$(git status --porcelain)" ]]; then
  echo "STOP: checkout must be clean; preserve your local edits first" >&2
  git status --short
  exit 2
fi

LOG_DIR="temp/full-gate-style-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$LOG_DIR"
git rev-parse HEAD > "$LOG_DIR/BASE_HEAD.txt"

echo "SAFE AUTO-FIX START $(cat "$LOG_DIR/BASE_HEAD.txt")"
echo "Logs: $ROOT/$LOG_DIR"

# Ruff's default --fix applies safe edits only. The remaining diagnostics are
# preserved and must be fixed in source, not disabled or excluded from the gate.
set +e
(cd apps/backend && uv run --locked ruff check . --fix)   > "$LOG_DIR/RUFF_SAFE_FIX.log" 2>&1
RUFF_REMAINING=$?
set -e

(cd apps/backend && uv run --locked ruff format .)   > "$LOG_DIR/RUFF_FORMAT.log" 2>&1
pnpm format > "$LOG_DIR/PRETTIER_FORMAT.log" 2>&1

# Do not apply ESLint --fix automatically in this bulk formatting pass.
# ESLint's assertion-removal autofix has demonstrably stripped essential
# DOM input typing and occurrence source-kind literals and broke tsc.
# Keep its diagnostic-only report for a deliberate source-level repair.
ESLINT_REMAINING="diagnostic-only"
pnpm lint > "$LOG_DIR/ESLINT_SAFE_FIX.log" 2>&1 || true

# Normalize formatter output without ESLint rewriting TypeScript semantics.
pnpm format > "$LOG_DIR/PRETTIER_AFTER_LINT.log" 2>&1

git diff --check > "$LOG_DIR/DIFF_CHECK.log" 2>&1 || {
  echo "STOP: whitespace check failed; changes are not committed" >&2
  exit 2
}
pnpm format:check > "$LOG_DIR/REPO_FORMAT_CHECK.log" 2>&1 || {
  echo "STOP: Prettier gate still red; changes are not committed" >&2
  exit 2
}
(cd apps/backend && uv run --locked ruff format --check .)   > "$LOG_DIR/BACKEND_FORMAT_CHECK.log" 2>&1 || {
  echo "STOP: Python formatting gate still red; changes are not committed" >&2
  exit 2
}
pnpm generated:check > "$LOG_DIR/GENERATED_DRIFT.log" 2>&1 || {
  echo "STOP: generated sources drifted; changes are not committed" >&2
  exit 2
}
pnpm typecheck > "$LOG_DIR/TYPECHECK.log" 2>&1 || {
  echo "STOP: repository typecheck failed; changes are not committed" >&2
  exit 2
}

printf 'BASE_HEAD=%s\nRUFF_UNFIXED_EXIT=%s\nESLINT_UNFIXED_EXIT=%s\n'   "$(cat "$LOG_DIR/BASE_HEAD.txt")" "$RUFF_REMAINING" "$ESLINT_REMAINING"   | tee "$LOG_DIR/SUMMARY.txt"

if [[ -z "$(git status --porcelain)" ]]; then
  echo "No source changes required. No commit." | tee -a "$LOG_DIR/SUMMARY.txt"
  exit 0
fi

# Only stage tracked changes, never local data, .env, or any scratch logs.
git add -u
git diff --cached --stat > "$LOG_DIR/CHANGED_FILES.txt"
git commit -m "style(gate): apply safe Ruff fixes and normalize tracked source formatting"
git push origin "$BRANCH"
git rev-parse HEAD | tee "$LOG_DIR/NEW_HEAD.txt"
echo "STYLE_AUTOFIX_COMMIT=$(cat "$LOG_DIR/NEW_HEAD.txt")"   | tee -a "$LOG_DIR/SUMMARY.txt"

# Keep diagnostic evidence in temp/ for later targeted Ruff/ESLint repairs.
echo "Unfixed Ruff and ESLint diagnostics remain in $LOG_DIR."

# Keep one compact, inspectable diagnostic bundle for the next source-level
# repair pass. Re-check only static errors plus the formerly red overnight
# clock tests; the long PostgreSQL/browser gate is intentionally not rerun.
set +e
(cd apps/backend && uv run --locked ruff check .)   > "$LOG_DIR/RUFF_REMAINING.log" 2>&1
RUFF_GATE=$?
(cd apps/backend && uv run --locked mypy src tests tooling)   > "$LOG_DIR/MYPY_REMAINING.log" 2>&1
MYPY_GATE=$?
pnpm lint > "$LOG_DIR/ESLINT_REMAINING.log" 2>&1
ESLINT_GATE=$?
pnpm --filter @dante/web exec vitest run   src/features/temporal-create/ui/temporal-create-top-controls.test.tsx   > "$LOG_DIR/OVERNIGHT_VITEST.log" 2>&1
VITEST_GATE=$?
set -e

printf 'RUFF_GATE=%s\nMYPY_GATE=%s\nESLINT_GATE=%s\nOVERNIGHT_VITEST=%s\n'   "$RUFF_GATE" "$MYPY_GATE" "$ESLINT_GATE" "$VITEST_GATE"   | tee -a "$LOG_DIR/SUMMARY.txt"
tar -czf temp/FULL_GATE_REPAIR_LOGS.tar.gz -C temp "$(basename "$LOG_DIR")"
echo "REPAIR_LOGS=$ROOT/temp/FULL_GATE_REPAIR_LOGS.tar.gz"
echo "Do not interpret this commit as a green full gate."
