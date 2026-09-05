#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
BACKEND_ROOT="$REPO_ROOT/apps/backend"
WITH_POSTGRES=0

usage() {
  cat <<'EOF'
Usage: tooling/ai-evals/run_ai_foundation_closure_gate.sh [--with-postgres]

Always (deterministic / zero provider calls):
  - requires a clean tracked working tree at start
  - verifies apps/backend/uv.lock without regenerating it
  - syncs the locked backend environment
  - backend Ruff format/lint
  - backend mypy strict
  - backend non-PostgreSQL pytest
  - AI eval tooling Ruff format/lint
  - AI eval tooling deterministic pytest
  - backend build
  - native Gemini runtime DRY-RUN only

Optional:
  --with-postgres  build the canonical PostgreSQL image and run postgres-marked acceptance tests

This closure gate intentionally performs no paid provider calls. Native Gemini development
qualification is recorded separately and must not be repeated merely to close the branch.
EOF
}

while (($#)); do
  case "$1" in
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

cd "$BACKEND_ROOT"

echo '=== AI FOUNDATION: verify locked dependency graph ==='
uv lock --check

echo '=== AI FOUNDATION: sync locked environment ==='
uv sync --locked

echo '=== AI FOUNDATION: backend ruff format ==='
uv run --locked ruff format --check .

echo '=== AI FOUNDATION: backend ruff lint ==='
uv run --locked ruff check .

echo '=== AI FOUNDATION: backend mypy ==='
uv run --locked mypy

echo '=== AI FOUNDATION: backend fast tests ==='
uv run --locked pytest -m "not postgres"

cd "$REPO_ROOT"

echo '=== AI FOUNDATION: eval tooling ruff format ==='
uv run --project apps/backend --locked ruff format --check \
  --config apps/backend/pyproject.toml tooling/ai-evals

echo '=== AI FOUNDATION: eval tooling ruff lint ==='
# S105 is a single tooling-only false positive: TrialVerdict.PASS = "PASS" is an enum value,
# not a credential. All other selected Ruff rules remain active for the whole eval-tooling tree.
uv run --project apps/backend --locked ruff check \
  --config apps/backend/pyproject.toml --ignore S105 tooling/ai-evals

echo '=== AI FOUNDATION: eval tooling deterministic tests ==='
uv run --project apps/backend --locked pytest tooling/ai-evals/tests

cd "$BACKEND_ROOT"

echo '=== AI FOUNDATION: backend build ==='
uv build

cd "$REPO_ROOT"

echo '=== AI FOUNDATION: native Gemini runtime dry-run (zero provider calls) ==='
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

echo
echo '=== AI FOUNDATION DETERMINISTIC GATE COMPLETE ==='
echo "postgres=$WITH_POSTGRES provider_calls=0"

TRACKED_AFTER="$(git status --porcelain --untracked-files=no)"
if [[ -n "$TRACKED_AFTER" ]]; then
  echo 'Gate unexpectedly changed tracked files:' >&2
  printf '%s\n' "$TRACKED_AFTER" >&2
  exit 6
fi

echo 'tracked changes produced by gate: none'
