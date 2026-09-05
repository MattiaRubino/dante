#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
BACKEND_ROOT="$REPO_ROOT/apps/backend"
EXECUTE_LIVE=0
WITH_POSTGRES=0

usage() {
  cat <<'EOF'
Usage: tooling/ai-evals/run_ai_foundation_closure_gate.sh [--execute-live] [--with-postgres]

Always:
  - requires a clean tracked working tree at start
  - regenerates/checks apps/backend/uv.lock
  - verifies lock regeneration changes no tracked file except apps/backend/uv.lock
  - syncs locked environment
  - Ruff format/lint
  - mypy strict
  - non-PostgreSQL pytest
  - backend build
  - native Gemini runtime dry-run

Optional:
  --execute-live   exactly one synthetic native Gemini Interactions call through ModelAccessRuntime
  --with-postgres  build canonical PostgreSQL image and run postgres-marked acceptance suite

The live smoke reads DANTE_GEMINI_API_KEY or DANTE_EVAL_GEMINI_API_KEY.
No secret value is printed or persisted.
EOF
}

while (($#)); do
  case "$1" in
    --execute-live)
      EXECUTE_LIVE=1
      ;;
    --with-postgres)
      WITH_POSTGRES=1
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      printf 'Unknown argument: %s\n' "$1" >&2
      usage >&2
      exit 2
      ;;
  esac
  shift
done

cd "$REPO_ROOT"

TRACKED_BEFORE="$(git status --porcelain --untracked-files=no)"
if [[ -n "$TRACKED_BEFORE" ]]; then
  echo 'Tracked working tree must be clean before the closure gate:' >&2
  printf '%s\n' "$TRACKED_BEFORE" >&2
  exit 3
fi

if (( EXECUTE_LIVE )) && [[ -z "${DANTE_GEMINI_API_KEY:-}" && -z "${DANTE_EVAL_GEMINI_API_KEY:-}" ]]; then
  echo 'Live closure requested but no Gemini API key is exported in this shell.' >&2
  echo 'Set DANTE_GEMINI_API_KEY or DANTE_EVAL_GEMINI_API_KEY without committing it.' >&2
  exit 4
fi

cd "$BACKEND_ROOT"

echo '=== AI FOUNDATION: lock regenerate/check ==='
uv lock
uv lock --check

cd "$REPO_ROOT"
TRACKED_AFTER_LOCK="$(git diff --name-only)"
if [[ -n "$TRACKED_AFTER_LOCK" && "$TRACKED_AFTER_LOCK" != "apps/backend/uv.lock" ]]; then
  echo 'Unexpected tracked changes after uv lock:' >&2
  printf '%s\n' "$TRACKED_AFTER_LOCK" >&2
  exit 5
fi

cd "$BACKEND_ROOT"

echo '=== AI FOUNDATION: sync ==='
uv sync --locked

echo '=== AI FOUNDATION: ruff format ==='
uv run --locked ruff format --check .

echo '=== AI FOUNDATION: ruff lint ==='
uv run --locked ruff check .

echo '=== AI FOUNDATION: mypy ==='
uv run --locked mypy

echo '=== AI FOUNDATION: fast tests ==='
uv run --locked pytest -m "not postgres"

echo '=== AI FOUNDATION: build ==='
uv build

cd "$REPO_ROOT"

echo '=== AI FOUNDATION: native Gemini dry-run ==='
uv run --project apps/backend --locked \
  python tooling/ai-evals/run_gemini_native_runtime_smoke.py

if (( WITH_POSTGRES )); then
  echo '=== AI FOUNDATION: PostgreSQL image ==='
  docker build --pull --tag dante-postgres-local:18.6 infra/local/postgres

  echo '=== AI FOUNDATION: PostgreSQL acceptance ==='
  cd "$BACKEND_ROOT"
  uv run --locked pytest -m postgres -vv
  cd "$REPO_ROOT"
fi

if (( EXECUTE_LIVE )); then
  echo '=== AI FOUNDATION: exactly one native Gemini live smoke ==='
  uv run --project apps/backend --locked \
    python tooling/ai-evals/run_gemini_native_runtime_smoke.py --execute
else
  echo '=== AI FOUNDATION: live smoke NOT RUN (pass --execute-live to close provider-live gate) ==='
fi

echo
echo '=== AI FOUNDATION GATE COMPLETE ==='
echo "postgres=$WITH_POSTGRES live=$EXECUTE_LIVE"
if [[ -n "$(git diff --name-only)" ]]; then
  echo 'tracked changes produced by gate:'
  git diff --name-only
else
  echo 'tracked changes produced by gate: none'
fi
