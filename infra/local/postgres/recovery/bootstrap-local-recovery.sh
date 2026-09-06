#!/usr/bin/env bash
set -Eeuo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd -- "${SCRIPT_DIR}/../../../.." && pwd)"

IMAGE="${DANTE_RECOVERY_IMAGE:-dante-postgres-recovery:18.6-pgbackrest-2.59.1}"
SKIP_GIT_FETCH="${DANTE_RECOVERY_SKIP_GIT_FETCH:-0}"

BASE="infra/compose/local.yaml"
OVERLAY="infra/compose/postgres-recovery.override.yaml"
ADMIN_SECRET="infra/compose/secrets/postgres_password.local"
MIGRATOR_SECRET="infra/compose/secrets/postgres_recovery_migrator_password.local"
RUNTIME_SECRET="infra/compose/secrets/postgres_recovery_runtime_password.local"

die() {
  echo "FAIL: $*" >&2
  exit 1
}

require_command() {
  command -v "$1" >/dev/null 2>&1 || die "missing required command: $1"
}

assert_git_safety() {
  cd "$REPO_ROOT"

  local branch upstream remote head upstream_head
  branch="$(git symbolic-ref --quiet --short HEAD 2>/dev/null || true)"
  test -n "$branch" || die "detached HEAD is not accepted"

  upstream="$(git rev-parse --abbrev-ref --symbolic-full-name '@{u}' 2>/dev/null || true)"
  test -n "$upstream" || die "current branch has no upstream"

  test -z "$(git status --porcelain)" || die "worktree is not clean"

  if [ "$SKIP_GIT_FETCH" = "0" ]; then
    remote="$(git config --get "branch.${branch}.remote" || true)"
    test -n "$remote" || die "current branch has no configured remote"
    git fetch --quiet "$remote"
  elif [ "$SKIP_GIT_FETCH" != "1" ]; then
    die "DANTE_RECOVERY_SKIP_GIT_FETCH must be 0 or 1"
  fi

  head="$(git rev-parse HEAD)"
  upstream_head="$(git rev-parse "$upstream")"
  test "$head" = "$upstream_head" || die "local HEAD $head differs from upstream $upstream ($upstream_head)"

  printf '%s\n' "Git branch:   $branch"
  printf '%s\n' "Git upstream: $upstream"
  printf '%s\n' "Git HEAD:     $head"
}

create_secret_if_missing() {
  local path="$1"

  if [ -e "$path" ] || [ -L "$path" ]; then
    test ! -L "$path" || die "$path must not be a symlink"
    test -f "$path" || die "$path exists but is not a regular file"
    test -s "$path" || die "$path exists but is empty; refusing to overwrite"
    echo "Secret: REUSED $path"
  else
    python3 - "$path" <<'PY'
from pathlib import Path
import os
import secrets
import sys

path = Path(sys.argv[1])
path.parent.mkdir(parents=True, exist_ok=True)
value = secrets.token_urlsafe(32) + "\n"
fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
try:
    with os.fdopen(fd, "w", encoding="utf-8") as fh:
        fh.write(value)
        fh.flush()
        os.fsync(fh.fileno())
except Exception:
    try:
        path.unlink()
    except FileNotFoundError:
        pass
    raise
PY
    echo "Secret: CREATED $path"
  fi

  chmod 600 "$path"
  test "$(stat -c '%a' "$path")" = "600" || die "$path mode is not 600"
  git check-ignore -q "$path" || die "$path is not Git-ignored"
  if git ls-files --error-unmatch "$path" >/dev/null 2>&1; then
    die "$path is unexpectedly tracked by Git"
  fi
}

cd "$REPO_ROOT"

echo "=== DANTE — LOCAL RECOVERY BOOTSTRAP ==="
echo "Idempotent repository-level prerequisites only; no PostgreSQL data volume is created."

case "$REPO_ROOT" in
  /mnt/*) die "repository must live on the Linux filesystem, not under /mnt/*" ;;
esac

for cmd in git docker uv python3 stat sha256sum; do
  require_command "$cmd"
done

docker compose version >/dev/null 2>&1 || die "Docker Compose plugin is unavailable"
docker info >/dev/null 2>&1 || die "Docker daemon is unreachable"
test "$(docker info --format '{{.OSType}}')" = "linux" || die "Docker daemon is not running Linux containers"

assert_git_safety

test ! -L infra/compose/secrets || die "infra/compose/secrets must not be a symlink"
mkdir -p infra/compose/secrets
chmod 700 infra/compose/secrets
test "$(stat -c '%a' infra/compose/secrets)" = "700" || die "infra/compose/secrets mode is not 700"

create_secret_if_missing "$ADMIN_SECRET"
create_secret_if_missing "$MIGRATOR_SECRET"
create_secret_if_missing "$RUNTIME_SECRET"

docker compose \
  -p dante-postgres-recovery \
  -f "$BASE" \
  -f "$OVERLAY" \
  config --quiet

echo "Compose recovery topology: VALID"

docker build \
  -t "$IMAGE" \
  infra/local/postgres

docker image inspect "$IMAGE" >/dev/null
postgres_version="$(docker run --rm --entrypoint postgres "$IMAGE" --version)"
pgbackrest_version="$(docker run --rm --entrypoint pgbackrest "$IMAGE" version)"

printf '%s\n' "$postgres_version" | grep -F 'PostgreSQL) 18.6' >/dev/null \
  || die "unexpected PostgreSQL image version: $postgres_version"
test "$pgbackrest_version" = "pgBackRest 2.59.1" \
  || die "unexpected pgBackRest image version: $pgbackrest_version"

echo "Recovery image: $IMAGE"
echo "PostgreSQL:     $postgres_version"
echo "pgBackRest:     $pgbackrest_version"
echo "=== LOCAL RECOVERY BOOTSTRAP: PASS ==="
