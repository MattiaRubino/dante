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
  - regenerates/checks apps/backend/uv.lock
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

cd "$BACKEND_ROOT"

echo '=== AI FOUNDATION: lock regenerate/check ==='
uv lock
uv lock --check

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
echo 'Inspect git status: uv.lock is expected to change if dependency metadata was stale.'
