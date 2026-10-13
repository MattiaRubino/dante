#!/usr/bin/env bash
# Recover the deliberately uncommitted full-gate safe-format run (2026-10-13).
# The original checkout was clean. Preserve the failed autofix in a patch,
# undo ONLY JS/TS ESLint autofixes, re-apply Prettier, then verify and commit
# retained safe Ruff fixes plus Ruff/Prettier formatting.
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"
BRANCH="feature/timeline-temporal-operational"
BASE_SHA="414fe6ed013cad1700695ea6a72c88a1f5d7b159"
ORIGINAL_LOG="temp/full-gate-style-20261013-222500"
RECOVERY_LOG="temp/full-gate-style-recovered-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$RECOVERY_LOG"

if [[ "$(git branch --show-current)" != "$BRANCH" ]]; then
  echo "STOP: wrong branch; no files changed" >&2
  exit 2
fi
if [[ "$(git rev-parse HEAD)" != "$BASE_SHA" ]]; then
  echo "STOP: HEAD differs from the original failed style run; no files changed" >&2
  exit 2
fi
if [[ ! -f "$ORIGINAL_LOG/BASE_HEAD.txt" ]] || \
  [[ "$(cat "$ORIGINAL_LOG/BASE_HEAD.txt")" != "$BASE_SHA" ]] || \
  [[ ! -f "$ORIGINAL_LOG/TYPECHECK.log" ]]; then
  echo "STOP: cannot verify the original clean-checkout style run; no files changed" >&2
  exit 2
fi
if ! git diff --cached --quiet; then
  echo "STOP: staged changes exist; preserve them separately first" >&2
  exit 2
fi
if git diff --quiet; then
  echo "STOP: no failed style worktree to recover" >&2
  exit 2
fi

# Preserve every user-visible byte of the failed attempt before restoration.
git diff --binary > "$RECOVERY_LOG/FAILED_AUTOFIX_BACKUP.patch"
git status --short > "$RECOVERY_LOG/STATUS_BEFORE.txt"
git diff --stat > "$RECOVERY_LOG/CHANGES_BEFORE.txt"

# ESLint's --fix stripped necessary HTMLInputElement/HTMLSelectElement casts
# from tests and narrowed source-kind literals incorrectly, producing many
# TS2339/TS2322 errors. Do not repeat that autofix. The original script
# started from a clean checkout; restoring tracked script-modified JS/TS
# files to HEAD then reformatting preserves all other safe changes.
mapfile -d '' changed_js < <(git diff --name-only -z -- \
  '*.ts' '*.tsx' '*.mts' '*.cts' '*.js' '*.jsx' '*.mjs' '*.cjs')
printf '%s\n' "${changed_js[@]}" > "$RECOVERY_LOG/RESTORED_SCRIPT_MODIFIED_JS_TS.txt"
if (( ${#changed_js[@]} )); then
  git restore --worktree -- "${changed_js[@]}"
fi

pnpm format > "$RECOVERY_LOG/PRETTIER.log" 2>&1
git diff --check > "$RECOVERY_LOG/DIFF_CHECK.log" 2>&1
pnpm format:check > "$RECOVERY_LOG/REPO_FORMAT_CHECK.log" 2>&1
(cd apps/backend && uv run --locked ruff format --check .) \
  > "$RECOVERY_LOG/BACKEND_FORMAT_CHECK.log" 2>&1
pnpm generated:check > "$RECOVERY_LOG/GENERATED_DRIFT.log" 2>&1

# Critical blocking proof: this MUST be green before committing.
set +e
pnpm typecheck > "$RECOVERY_LOG/TYPECHECK.log" 2>&1
TYPECHECK_STATUS=$?
set -e
if [[ "$TYPECHECK_STATUS" != 0 ]]; then
  tar -czf temp/FULL_GATE_RECOVERY_LOGS.tar.gz -C temp "$(basename "$RECOVERY_LOG")"
  echo "STOP: TypeScript remains red; no commit/push; logs temp/FULL_GATE_RECOVERY_LOGS.tar.gz" >&2
  exit "$TYPECHECK_STATUS"
fi

if git diff --quiet; then
  echo "No remaining changes after recovery" >&2
  exit 0
fi

git add -u
git diff --cached --check
git diff --cached --stat > "$RECOVERY_LOG/COMMITTED_FILES.txt"
git commit -m "style(gate): safely apply Ruff fixes and normalize Python and frontend formatting"

# Another assistant commit on origin adds this very recovery script. Rebase
# only after the normalized worktree is safely committed locally.
git pull --rebase origin "$BRANCH"

# Re-confirm the merged commit, never push if its checks have regressed.
pnpm format:check > "$RECOVERY_LOG/POST_REBASE_PRETTIER.log" 2>&1
(cd apps/backend && uv run --locked ruff format --check .) \
  > "$RECOVERY_LOG/POST_REBASE_RUFF_FORMAT.log" 2>&1
pnpm typecheck > "$RECOVERY_LOG/POST_REBASE_TYPECHECK.log" 2>&1
git diff --check
git push origin "$BRANCH"
git rev-parse HEAD | tee "$RECOVERY_LOG/HEAD.txt"

# Diagnose the genuinely remaining source problems without repeatedly
# running long PostgreSQL and browser full gate.
set +e
(cd apps/backend && uv run --locked ruff check .) \
  > "$RECOVERY_LOG/RUFF_REMAINING.log" 2>&1
RUFF=$?
(cd apps/backend && uv run --locked mypy src tests tooling) \
  > "$RECOVERY_LOG/MYPY_REMAINING.log" 2>&1
MYPY=$?
pnpm lint > "$RECOVERY_LOG/ESLINT_REMAINING.log" 2>&1
ESLINT=$?
pnpm --filter @dante/web exec vitest run \
  src/features/temporal-create/ui/temporal-create-top-controls.test.tsx \
  > "$RECOVERY_LOG/OVERNIGHT_VITEST.log" 2>&1
VITEST=$?
set -e
printf 'HEAD=%s\nTYPECHECK=0\nRUFF=%s\nMYPY=%s\nESLINT=%s\nOVERNIGHT_VITEST=%s\n' \
  "$(cat "$RECOVERY_LOG/HEAD.txt")" "$RUFF" "$MYPY" "$ESLINT" "$VITEST" \
  | tee "$RECOVERY_LOG/SUMMARY.txt"
tar -czf temp/FULL_GATE_RECOVERY_LOGS.tar.gz -C temp "$(basename "$RECOVERY_LOG")"
echo "REPAIR_LOGS=$ROOT/temp/FULL_GATE_RECOVERY_LOGS.tar.gz"
echo "BACKUP_PATCH=$ROOT/$RECOVERY_LOG/FAILED_AUTOFIX_BACKUP.patch"
