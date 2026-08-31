#!/usr/bin/env bash
set -Eeuo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd -- "${SCRIPT_DIR}/../../../.." && pwd)"

BOOTSTRAP="${SCRIPT_DIR}/bootstrap-local-recovery.sh"
IMAGE="${DANTE_RECOVERY_IMAGE:-dante-postgres-recovery:18.6-pgbackrest-2.59.1}"
EXPECTED_ALEMBIC="20260830_09"
EXPECTED_TOPOLOGY="69|5|15|76|97|69|123|0|0|0"
EXPECTED_EXTENSIONS="pg_stat_statements=1.12,pg_trgm=1.6,postgis=3.6.4,unaccent=1.1,vector=0.8.6"

ADMIN_SECRET="infra/compose/secrets/postgres_password.local"
MIGRATOR_SECRET="infra/compose/secrets/postgres_recovery_migrator_password.local"
RUNTIME_SECRET="infra/compose/secrets/postgres_recovery_runtime_password.local"
REPORT_REL="infra/compose/secrets/postgres_recovery_cp07_report.json.local"
REPORT_PATH="${REPO_ROOT}/${REPORT_REL}"

SOURCE_PORT="${DANTE_CP07_SOURCE_PORT:-55436}"
KEEP_ON_FAILURE="${DANTE_CP07_KEEP_ON_FAILURE:-0}"

RUN_ID="cp07-$(date -u +%Y%m%dT%H%M%SZ)-$$"
PGVOL="${RUN_ID}-pgdata"
REPOVOL="${RUN_ID}-repo"
LEDGER_VOL="${RUN_ID}-ledger"
SOURCE_CONTAINER="${RUN_ID}-source"
RESTORED_CONTAINER="${RUN_ID}-restored"

REAL_RECOVERY_REPOVOL="dante-postgres-recovery_pgbackrest-repository"
CP05_TARGET="dante-postgres-recovery-cp05-pitr"
PROTECTED_VOLUMES=(
  "dante-local_postgres-data"
  "dante-local_pgbackrest-repository"
  "dante-postgres-recovery_postgres-data"
  "dante-postgres-recovery_pgbackrest-repository"
)

TMPDIR="$(mktemp -d)"
LEDGER_BUILD="${TMPDIR}/ledger-build"
LEDGER_READ="${TMPDIR}/ledger-read"
RECOVERY_LOG="${TMPDIR}/recovery.log"

SUCCESS=0
EXPLICIT_CLEANUP=0

die() {
  echo
  echo "FAIL: $*" >&2
  exit 1
}

seconds_between_ns() {
  python3 - "$1" "$2" <<'PY'
import sys
start, end = map(int, sys.argv[1:])
print(f"{(end-start)/1_000_000_000:.6f}")
PY
}

volume_fingerprint() {
  local volume="$1"
  if docker volume inspect "$volume" >/dev/null 2>&1; then
    docker volume inspect "$volume" | sha256sum | awk '{print $1}'
  else
    printf '%s\n' "MISSING"
  fi
}

container_fingerprint() {
  local container="$1"
  if docker inspect "$container" >/dev/null 2>&1; then
    docker inspect "$container" --format '{{.Id}}|{{.State.Status}}|{{.Created}}'
  else
    printf '%s\n' "MISSING"
  fi
}

repo_info_hash() {
  local volume="$1"
  local relative="$2"
  if ! docker volume inspect "$volume" >/dev/null 2>&1; then
    printf '%s\n' "MISSING_VOLUME"
    return
  fi
  docker run --rm --entrypoint sh -v "${volume}:/repo:ro" "$IMAGE" -lc \
    "if [ -f '/repo/${relative}' ]; then sha256sum '/repo/${relative}' | awk '{print \$1}'; else echo MISSING_FILE; fi"
}

cleanup_resources() {
  set +e
  docker rm -f "$SOURCE_CONTAINER" "$RESTORED_CONTAINER" >/dev/null 2>&1 || true
  docker volume rm "$PGVOL" "$REPOVOL" "$LEDGER_VOL" >/dev/null 2>&1 || true
  rm -rf "$TMPDIR" >/dev/null 2>&1 || true
  set -e
}

cleanup() {
  status=$?
  set +e
  if [ "$EXPLICIT_CLEANUP" -ne 1 ]; then
    if [ "$status" -ne 0 ] && [ "$KEEP_ON_FAILURE" = "1" ]; then
      echo
      echo "CP07 failed; disposable resources retained for diagnosis:"
      echo "  source container:   $SOURCE_CONTAINER"
      echo "  restored container: $RESTORED_CONTAINER"
      echo "  PGDATA volume:      $PGVOL"
      echo "  repository volume:  $REPOVOL"
      echo "  ledger volume:      $LEDGER_VOL"
      echo "  tmpdir:             $TMPDIR"
    else
      docker rm -f "$SOURCE_CONTAINER" "$RESTORED_CONTAINER" >/dev/null 2>&1 || true
      docker volume rm "$PGVOL" "$REPOVOL" "$LEDGER_VOL" >/dev/null 2>&1 || true
      rm -rf "$TMPDIR" >/dev/null 2>&1 || true
    fi
  fi
  exit "$status"
}
trap cleanup EXIT

wait_ready() {
  local container="$1"
  for _ in $(seq 1 120); do
    status="$(docker inspect "$container" --format '{{.State.Status}}' 2>/dev/null || true)"
    if [ "$status" = "exited" ] || [ "$status" = "dead" ]; then
      docker logs "$container" || true
      return 1
    fi
    if docker exec "$container" pg_isready -h 127.0.0.1 -p 5432 -U postgres -d dante >/dev/null 2>&1; then
      return 0
    fi
    sleep 1
  done
  return 1
}

wait_promoted() {
  local container="$1"
  for _ in $(seq 1 120); do
    status="$(docker inspect "$container" --format '{{.State.Status}}' 2>/dev/null || true)"
    if [ "$status" = "exited" ] || [ "$status" = "dead" ]; then
      docker logs "$container" || true
      return 1
    fi
    state="$(docker exec --user postgres "$container" psql -X -d dante -Atqc \
      "SELECT current_setting('server_version_num') || '|' || pg_is_in_recovery()::text;" 2>/dev/null || true)"
    if [ "$state" = "180006|false" ]; then
      return 0
    fi
    sleep 1
  done
  return 1
}

repo_find() {
  local pattern="$1"
  docker run --rm --entrypoint sh -v "${REPOVOL}:/var/lib/pgbackrest:ro" "$IMAGE" \
    -lc "find /var/lib/pgbackrest/archive/dante -type f -name '$pattern' -print -quit 2>/dev/null || true"
}

wait_repo_file() {
  local pattern="$1"
  local label="$2"
  local found=""
  for _ in $(seq 1 90); do
    found="$(repo_find "$pattern")"
    if [ -n "$found" ]; then
      echo "$label: $found"
      return 0
    fi
    sleep 1
  done
  return 1
}

normalize_pg18_parent() {
  docker run --rm --entrypoint sh -v "${PGVOL}:/var/lib/postgresql" "$IMAGE" -lc '
    set -eu
    test -d /var/lib/postgresql/18/docker
    chown postgres:postgres /var/lib/postgresql/18
    chmod 0700 /var/lib/postgresql/18
  '
}

copy_ledger_build_to_volume() {
  docker run --rm \
    --user root \
    --entrypoint sh \
    -v "${LEDGER_BUILD}:/source:ro" \
    -v "${LEDGER_VOL}:/dest" \
    "$IMAGE" \
    -lc 'set -eu; mkdir -p /dest/records; cp -a -n /source/records/. /dest/records/'
}

copy_ledger_volume_to_readback() {
  local host_uid host_gid
  host_uid="$(id -u)"
  host_gid="$(id -g)"
  rm -rf "$LEDGER_READ"
  mkdir -p "$LEDGER_READ"
  docker run --rm \
    --user root \
    --entrypoint sh \
    -e HOST_UID="$host_uid" \
    -e HOST_GID="$host_gid" \
    -v "${LEDGER_VOL}:/source:ro" \
    -v "${LEDGER_READ}:/dest" \
    "$IMAGE" \
    -lc 'set -eu; cp -a /source/. /dest/; chown -R "$HOST_UID:$HOST_GID" /dest'
}

assert_current_contract() {
  local container="$1"

  server_version="$(docker exec --user postgres "$container" psql -X -d dante -Atqc \
    "SELECT current_setting('server_version_num');")"
  test "$server_version" = "180006" || die "server_version_num=$server_version"

  head="$(docker exec --user postgres "$container" psql -X -d dante -Atqc \
    "SELECT version_num FROM dante.alembic_version;")"
  test "$head" = "$EXPECTED_ALEMBIC" || die "Alembic=$head"

  topology="$(docker exec --user postgres "$container" psql -X -d dante -Atqc "
SELECT
  (SELECT count(*) FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace WHERE n.nspname='dante' AND c.relkind='r' AND c.relname<>'alembic_version'),
  (SELECT count(*) FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace WHERE n.nspname='dante' AND c.relkind='v'),
  (SELECT count(*) FROM pg_proc p JOIN pg_namespace n ON n.oid=p.pronamespace WHERE n.nspname='dante'),
  (SELECT count(*) FROM pg_trigger t JOIN pg_class c ON c.oid=t.tgrelid JOIN pg_namespace n ON n.oid=c.relnamespace WHERE n.nspname='dante' AND NOT t.tgisinternal),
  (SELECT count(*) FROM pg_index i JOIN pg_class c ON c.oid=i.indrelid JOIN pg_namespace n ON n.oid=c.relnamespace WHERE n.nspname='dante' AND c.relname<>'alembic_version'),
  (SELECT count(*) FROM pg_constraint c JOIN pg_namespace n ON n.oid=c.connamespace WHERE n.nspname='dante' AND c.contype='f'),
  (SELECT count(*) FROM pg_constraint c JOIN pg_namespace n ON n.oid=c.connamespace WHERE n.nspname='dante' AND c.contype='c'),
  (SELECT count(*) FROM pg_type t JOIN pg_namespace n ON n.oid=t.typnamespace WHERE n.nspname='dante' AND t.typtype IN ('d','e')),
  (SELECT count(*) FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace WHERE n.nspname='dante' AND c.relkind IN ('S','m','p')),
  (SELECT count(*) FROM pg_policy p JOIN pg_class c ON c.oid=p.polrelid JOIN pg_namespace n ON n.oid=c.relnamespace WHERE n.nspname='dante');
")"
  test "$topology" = "$EXPECTED_TOPOLOGY" || die "topology=$topology"

  owners="$(docker exec --user postgres "$container" psql -X -d dante -Atqc \
    "SELECT string_agg(owner, ',' ORDER BY owner) FROM (SELECT DISTINCT pg_get_userbyid(c.relowner) AS owner FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace WHERE n.nspname='dante' AND c.relname<>'alembic_version') x;")"
  test "$owners" = "dante_owner" || die "owners=$owners"

  roles="$(docker exec --user postgres "$container" psql -X -d dante -Atqc \
    "SELECT string_agg(rolname, ',' ORDER BY rolname) FROM pg_roles WHERE rolname IN ('dante_owner','dante_migrator','dante_runtime');")"
  test "$roles" = "dante_migrator,dante_owner,dante_runtime" || die "roles=$roles"

  runtime_alembic="$(docker exec --user postgres "$container" psql -X -d dante -Atqc \
    "SELECT has_table_privilege('dante_runtime','dante.alembic_version','SELECT');")"
  test "$runtime_alembic" = "f" || die "runtime can SELECT alembic_version"

  retirement_acl="$(docker exec --user postgres "$container" psql -X -d dante -Atqc \
    "SELECT has_table_privilege('dante_runtime','dante.material_state_retirement','SELECT')::text || '|' || has_table_privilege('dante_runtime','dante.material_state_retirement','INSERT')::text || '|' || has_table_privilege('dante_runtime','dante.material_state_retirement','UPDATE')::text || '|' || has_table_privilege('dante_runtime','dante.material_state_retirement','DELETE')::text;")"
  test "$retirement_acl" = "true|false|false|false" || die "retirement ACL=$retirement_acl"

  extensions="$(docker exec --user postgres "$container" psql -X -d dante -Atqc \
    "SELECT string_agg(extname || '=' || extversion, ',' ORDER BY extname) FROM pg_extension WHERE extname IN ('postgis','vector','pg_trgm','unaccent','pg_stat_statements');")"
  test "$extensions" = "$EXPECTED_EXTENSIONS" || die "extensions=$extensions"
}

cd "$REPO_ROOT"

echo "=== DANTE CP07 — WHOLE LOCAL OPERATOR RECOVERY REHEARSAL ==="
echo "Disposable-only PostgreSQL / repository / suppression-ledger topology."
echo "Remote/cloud provider: TBD / not activated / not exercised."

test -x "$BOOTSTRAP" || die "missing executable recovery bootstrap: $BOOTSTRAP"
bash "$BOOTSTRAP"

GIT_BRANCH="$(git symbolic-ref --quiet --short HEAD 2>/dev/null || true)"
test -n "$GIT_BRANCH" || die "detached HEAD is not accepted"
GIT_UPSTREAM="$(git rev-parse --abbrev-ref --symbolic-full-name '@{u}' 2>/dev/null || true)"
test -n "$GIT_UPSTREAM" || die "current branch has no upstream"
test -z "$(git status --porcelain)" || die "worktree is not clean"
PROOF_HEAD="$(git rev-parse HEAD)"
UPSTREAM_HEAD="$(git rev-parse "$GIT_UPSTREAM")"
test "$PROOF_HEAD" = "$UPSTREAM_HEAD" || die "local HEAD differs from upstream $GIT_UPSTREAM"

docker image inspect "$IMAGE" >/dev/null 2>&1 || die "recovery bootstrap did not materialize image $IMAGE"
for secret in "$ADMIN_SECRET" "$MIGRATOR_SECRET" "$RUNTIME_SECRET"; do
  test -s "$secret" || die "missing $secret"
  git check-ignore -q "$secret" || die "$secret is not ignored"
done
git check-ignore -q "$REPORT_REL" || die "$REPORT_REL is not ignored"

for volume in "${PROTECTED_VOLUMES[@]}"; do
  test "$volume" != "$PGVOL" || die "disposable PGDATA collides with protected volume"
  test "$volume" != "$REPOVOL" || die "disposable repo collides with protected volume"
  test "$volume" != "$LEDGER_VOL" || die "disposable ledger collides with protected volume"
done

declare -A PROTECTED_BEFORE
for volume in "${PROTECTED_VOLUMES[@]}"; do
  PROTECTED_BEFORE["$volume"]="$(volume_fingerprint "$volume")"
done

REAL_BACKUP_INFO_BEFORE="$(repo_info_hash "$REAL_RECOVERY_REPOVOL" "backup/dante/backup.info")"
REAL_ARCHIVE_INFO_BEFORE="$(repo_info_hash "$REAL_RECOVERY_REPOVOL" "archive/dante/archive.info")"
CP05_BEFORE="$(container_fingerprint "$CP05_TARGET")"

RUN_STARTED_NS="$(date +%s%N)"

docker volume create "$PGVOL" >/dev/null
docker volume create "$REPOVOL" >/dev/null
docker volume create "$LEDGER_VOL" >/dev/null

echo
echo "S1 — START HEALTHY DISPOSABLE POSTGRESQL"

docker run -d \
  --name "$SOURCE_CONTAINER" \
  -p "127.0.0.1:${SOURCE_PORT}:5432" \
  -e POSTGRES_DB=dante \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD_FILE=/run/secrets/postgres_password \
  --mount "type=bind,source=${REPO_ROOT}/${ADMIN_SECRET},target=/run/secrets/postgres_password,readonly" \
  -v "${PGVOL}:/var/lib/postgresql" \
  -v "${REPOVOL}:/var/lib/pgbackrest" \
  "$IMAGE" \
  postgres \
    -c shared_preload_libraries=pg_stat_statements \
    -c compute_query_id=on \
    -c archive_mode=on \
    -c "archive_command=/usr/bin/pgbackrest --stanza=dante archive-push %p" >/dev/null

wait_ready "$SOURCE_CONTAINER" || die "healthy source did not become ready"

docker exec --user postgres "$SOURCE_CONTAINER" pgbackrest --stanza=dante stanza-create
echo "HEALTHY SOURCE + INDEPENDENT REPOSITORY: PASS"

echo
echo "S2 — PROVISION CURRENT DANTE DATABASE"

export DANTE_DATABASE__HOST="127.0.0.1"
export DANTE_DATABASE__PORT="$SOURCE_PORT"
export DANTE_DATABASE__NAME="dante"
export DANTE_ADMIN__USER="postgres"
export DANTE_ADMIN__PASSWORD="$(cat "$ADMIN_SECRET")"
export DANTE_MIGRATOR__PASSWORD="$(cat "$MIGRATOR_SECRET")"
export DANTE_RUNTIME__PASSWORD="$(cat "$RUNTIME_SECRET")"

cd "$REPO_ROOT/apps/backend"
uv run --frozen python -m dante.platform.database.provisioning
uv run --frozen alembic upgrade head
uv run --frozen python -m dante.platform.database.provisioning
uv run --frozen alembic current
uv run --frozen alembic check
cd "$REPO_ROOT"

assert_current_contract "$SOURCE_CONTAINER"
docker exec --user postgres "$SOURCE_CONTAINER" pgbackrest --stanza=dante check
echo "CURRENT STRUCTURAL / SECURITY CONTRACT: PASS"

echo
echo "S3 — CREATE REAL PROTECTED MATERIALSTATE X"

SESSION_REF="$(docker exec --user postgres "$SOURCE_CONTAINER" psql -X -d dante -Atqc 'SELECT uuidv7();')"
STATE_REF="$(docker exec --user postgres "$SOURCE_CONTAINER" psql -X -d dante -Atqc 'SELECT uuidv7();')"
SUPPRESSION_REF="$(docker exec --user postgres "$SOURCE_CONTAINER" psql -X -d dante -Atqc 'SELECT uuidv7();')"
A_REF="$(docker exec --user postgres "$SOURCE_CONTAINER" psql -X -d dante -Atqc 'SELECT uuidv7();')"
B_REF="$(docker exec --user postgres "$SOURCE_CONTAINER" psql -X -d dante -Atqc 'SELECT uuidv7();')"

PROTECTED_START="2026-08-31 08:00:00+00"
PROTECTED_END="2026-08-31 08:01:00+00"

docker exec -i --user postgres "$SOURCE_CONTAINER" psql -X -v ON_ERROR_STOP=1 -d dante <<SQL
BEGIN;
SET LOCAL ROLE dante_owner;
INSERT INTO dante.session(session_ref) VALUES ('$SESSION_REF'::uuid);
INSERT INTO dante.native_address(native_ref,owner_family) VALUES ('$SESSION_REF'::uuid,'session');
INSERT INTO dante.material_state_address(material_state_ref,native_owner_ref,facet_code)
VALUES ('$STATE_REF'::uuid,'$SESSION_REF'::uuid,'session.timing');
INSERT INTO dante.session_timing_state(material_state_ref,session_ref,timing_form_code)
VALUES ('$STATE_REF'::uuid,'$SESSION_REF'::uuid,'absolute');
INSERT INTO dante.session_timing_absolute(
  material_state_ref,started_at,start_precision_code,ended_at,end_precision_code
)
VALUES (
  '$STATE_REF'::uuid,timestamptz '$PROTECTED_START','exact',
  timestamptz '$PROTECTED_END','exact'
);
INSERT INTO dante.native_current_material_state(native_owner_ref,facet_code,material_state_ref)
VALUES ('$SESSION_REF'::uuid,'session.timing','$STATE_REF'::uuid);
INSERT INTO dante.session_timing_current_history(session_ref,material_state_ref,current_from_at)
VALUES ('$SESSION_REF'::uuid,'$STATE_REF'::uuid,clock_timestamp());
COMMIT;
SQL

X_SHAPE="$(docker exec --user postgres "$SOURCE_CONTAINER" psql -X -d dante -Atqc "
SELECT
  (SELECT count(*) FROM dante.session WHERE session_ref='$SESSION_REF'::uuid),
  (SELECT count(*) FROM dante.material_state_address WHERE material_state_ref='$STATE_REF'::uuid),
  (SELECT count(*) FROM dante.session_timing_state WHERE material_state_ref='$STATE_REF'::uuid),
  (SELECT count(*) FROM dante.session_timing_absolute WHERE material_state_ref='$STATE_REF'::uuid),
  (SELECT count(*) FROM dante.native_current_material_state WHERE material_state_ref='$STATE_REF'::uuid),
  (SELECT count(*) FROM dante.session_timing_current_history WHERE material_state_ref='$STATE_REF'::uuid);
")"
test "$X_SHAPE" = "1|1|1|1|1|1" || die "protected X fixture shape=$X_SHAPE"
echo "PROTECTED X MATERIALIZED: PASS"

echo
echo "S4 — CREATE FULL B0 CONTAINING X"

docker exec --user postgres "$SOURCE_CONTAINER" psql -X -d dante -Atqc 'SELECT pg_switch_wal();' >/dev/null
docker exec --user postgres "$SOURCE_CONTAINER" pgbackrest --stanza=dante check

BACKUP_START_NS="$(date +%s%N)"
docker exec --user postgres "$SOURCE_CONTAINER" pgbackrest --stanza=dante --type=full backup
BACKUP_END_NS="$(date +%s%N)"
BACKUP_SECONDS="$(seconds_between_ns "$BACKUP_START_NS" "$BACKUP_END_NS")"

B0="$(docker exec --user postgres "$SOURCE_CONTAINER" pgbackrest --stanza=dante --output=json info | python3 -c \
  'import json,sys; data=json.load(sys.stdin); full=[b["label"] for s in data for b in s.get("backup",[]) if b.get("type")=="full"]; print(max(full))')"
test -n "$B0" || die "cannot resolve B0"

BACKUP_SIZE_BYTES="$(docker exec --user root "$SOURCE_CONTAINER" sh -lc "du -sb '/var/lib/pgbackrest/backup/dante/$B0' | awk '{print \$1}'")"
test "$BACKUP_SIZE_BYTES" -gt 0 || die "invalid B0 size"

echo "B0=$B0"
echo "BACKUP_SECONDS=$BACKUP_SECONDS"
echo "BACKUP_SIZE_BYTES=$BACKUP_SIZE_BYTES"

echo
echo "S5 — A / RESTORE POINT / B"

docker exec --user postgres "$SOURCE_CONTAINER" psql -X -v ON_ERROR_STOP=1 -d dante -Atqc "
SET ROLE dante_owner;
INSERT INTO dante.person(person_ref) VALUES ('$A_REF'::uuid);
RESET ROLE;
"
test "$(docker exec --user postgres "$SOURCE_CONTAINER" psql -X -d dante -Atqc \
  "SELECT count(*) FROM dante.person WHERE person_ref='$A_REF'::uuid;")" = "1" || die "A not committed"

RESTORE_POINT="${RUN_ID}_R1"
RESTORE_RESULT="$(docker exec --user postgres "$SOURCE_CONTAINER" psql -X -d dante -Atqc \
  "SELECT pg_create_restore_point('$RESTORE_POINT')::text || '|' || extract(epoch from clock_timestamp())::text;")"
IFS='|' read -r RESTORE_LSN RESTORE_POINT_EPOCH <<<"$RESTORE_RESULT"
test -n "$RESTORE_LSN" || die "restore point LSN missing"
RESTORE_WAL="$(docker exec --user postgres "$SOURCE_CONTAINER" psql -X -d dante -Atqc \
  "SELECT pg_walfile_name('$RESTORE_LSN'::pg_lsn);")"
TARGET_TIMELINE="$((16#${RESTORE_WAL:0:8}))"

docker exec --user postgres "$SOURCE_CONTAINER" psql -X -d dante -Atqc 'SELECT pg_switch_wal();' >/dev/null
wait_repo_file "${RESTORE_WAL}-*" "RESTORE-POINT WAL ARCHIVED" || die "restore-point WAL not archived"

docker exec --user postgres "$SOURCE_CONTAINER" psql -X -v ON_ERROR_STOP=1 -d dante -Atqc "
SET ROLE dante_owner;
INSERT INTO dante.person(person_ref) VALUES ('$B_REF'::uuid);
RESET ROLE;
"
test "$(docker exec --user postgres "$SOURCE_CONTAINER" psql -X -d dante -Atqc \
  "SELECT count(*) FROM dante.person WHERE person_ref='$B_REF'::uuid;")" = "1" || die "B not committed"

echo "A BEFORE TARGET: PASS"
echo "B AFTER TARGET:  PASS"

echo
echo "S6 — PREPARED SUPPRESSION INTENT"

mkdir -p "$LEDGER_BUILD"
cd "$REPO_ROOT/apps/backend"
ACCEPTED_AT="$(uv run --frozen python - "$LEDGER_BUILD" "$SUPPRESSION_REF" "$STATE_REF" <<'PY'
from datetime import UTC, datetime
from pathlib import Path
import sys
from uuid import UUID
from dante.platform.recovery.suppression_ledger import prepare_suppression

record = prepare_suppression(
    Path(sys.argv[1]),
    recovery_suppression_ref=UUID(sys.argv[2]),
    material_state_ref=UUID(sys.argv[3]),
    facet_code="session.timing",
    retirement_code="redacted",
    accepted_at=datetime.now(UTC),
)
print(record.accepted_at)
PY
)"
cd "$REPO_ROOT"
copy_ledger_build_to_volume

set +e
cd "$REPO_ROOT/apps/backend"
uv run --frozen python - "$LEDGER_BUILD" <<'PY'
from pathlib import Path
import sys
from dante.platform.recovery.suppression_ledger import load_committed_suppressions
load_committed_suppressions(Path(sys.argv[1]))
PY
PREPARED_ONLY_RC=$?
cd "$REPO_ROOT"
set -e
test "$PREPARED_ONLY_RC" -ne 0 || die "PREPARED-only ledger did not block"
echo "PREPARED-ONLY RECOVERY BLOCK: PASS"

echo
echo "S7 — CANONICAL RETIREMENT + COMMITTED SUPPRESSION"

docker exec -i --user postgres "$SOURCE_CONTAINER" psql -X -v ON_ERROR_STOP=1 -d dante <<SQL
BEGIN;
SET LOCAL ROLE dante_owner;
INSERT INTO dante.material_state_retirement(
  material_state_ref,retirement_code,retired_at,recovery_suppression_ref
)
VALUES (
  '$STATE_REF'::uuid,'redacted',timestamptz '$ACCEPTED_AT','$SUPPRESSION_REF'::uuid
);
DELETE FROM dante.session_timing_absolute WHERE material_state_ref='$STATE_REF'::uuid;
COMMIT;
SQL

SOURCE_RETIREMENT="$(docker exec --user postgres "$SOURCE_CONTAINER" psql -X -d dante -Atqc "
SELECT
  (SELECT count(*) FROM dante.material_state_retirement WHERE material_state_ref='$STATE_REF'::uuid),
  (SELECT count(*) FROM dante.session_timing_absolute WHERE material_state_ref='$STATE_REF'::uuid);
")"
test "$SOURCE_RETIREMENT" = "1|0" || die "canonical source retirement=$SOURCE_RETIREMENT"

cd "$REPO_ROOT/apps/backend"
uv run --frozen python - "$LEDGER_BUILD" "$SUPPRESSION_REF" "$STATE_REF" <<'PY'
from datetime import UTC, datetime
from pathlib import Path
import sys
from uuid import UUID
from dante.platform.recovery.suppression_ledger import commit_after_canonical_verification

commit_after_canonical_verification(
    Path(sys.argv[1]),
    recovery_suppression_ref=UUID(sys.argv[2]),
    verified_material_state_ref=UUID(sys.argv[3]),
    committed_at=datetime.now(UTC),
)
PY
cd "$REPO_ROOT"
copy_ledger_build_to_volume
rm -rf "$LEDGER_BUILD"

FINAL_WAL="$(docker exec --user postgres "$SOURCE_CONTAINER" psql -X -d dante -Atqc \
  'SELECT pg_walfile_name(pg_current_wal_lsn());')"
docker exec --user postgres "$SOURCE_CONTAINER" psql -X -d dante -Atqc 'SELECT pg_switch_wal();' >/dev/null
wait_repo_file "${FINAL_WAL}-*" "FINAL SOURCE WAL ARCHIVED" || die "final source WAL not archived"
docker exec --user postgres "$SOURCE_CONTAINER" pgbackrest --stanza=dante check

SOURCE_FINAL="$(docker exec --user postgres "$SOURCE_CONTAINER" psql -X -d dante -Atqc "
SELECT
  (SELECT count(*) FROM dante.person WHERE person_ref='$A_REF'::uuid),
  (SELECT count(*) FROM dante.person WHERE person_ref='$B_REF'::uuid),
  (SELECT count(*) FROM dante.material_state_retirement WHERE material_state_ref='$STATE_REF'::uuid),
  (SELECT count(*) FROM dante.session_timing_absolute WHERE material_state_ref='$STATE_REF'::uuid);
")"
test "$SOURCE_FINAL" = "1|1|1|0" || die "source final A|B|tombstone|X=$SOURCE_FINAL"
echo "SOURCE FINAL A|B|TOMBSTONE|X = $SOURCE_FINAL"

LATEST_ARCHIVE_MTIME="$(docker run --rm --entrypoint sh -v "${REPOVOL}:/repo:ro" "$IMAGE" -lc \
  "find /repo/archive/dante -type f -printf '%T@\n' | sort -nr | head -n1")"
test -n "$LATEST_ARCHIVE_MTIME" || die "cannot determine latest archive mtime"

echo
echo "S8 — SIMULATE COMPLETE PGDATA LOSS"

SOURCE_MARKER="/var/lib/postgresql/CP07_SOURCE_MUST_NOT_SURVIVE"
MARKER_TOKEN="${RUN_ID}-destroyed"
docker exec --user root "$SOURCE_CONTAINER" sh -lc "printf '%s\n' '$MARKER_TOKEN' > '$SOURCE_MARKER'"

REPO_BACKUP_HASH_BEFORE="$(docker exec --user root "$SOURCE_CONTAINER" sha256sum \
  /var/lib/pgbackrest/backup/dante/backup.info | awk '{print $1}')"
REPO_ARCHIVE_HASH_BEFORE="$(docker exec --user root "$SOURCE_CONTAINER" sha256sum \
  /var/lib/pgbackrest/archive/dante/archive.info | awk '{print $1}')"

DISASTER_EPOCH="$(python3 - <<'PY'
import time
print(f"{time.time():.6f}")
PY
)"
RESTORE_POINT_AGE_SECONDS="$(python3 - "$RESTORE_POINT_EPOCH" "$DISASTER_EPOCH" <<'PY'
import sys
print(f"{float(sys.argv[2])-float(sys.argv[1]):.6f}")
PY
)"
WAL_ARCHIVE_FRESHNESS_SECONDS="$(python3 - "$LATEST_ARCHIVE_MTIME" "$DISASTER_EPOCH" <<'PY'
import sys
print(f"{max(0.0, float(sys.argv[2])-float(sys.argv[1])):.6f}")
PY
)"

DESTRUCTION_START_NS="$(date +%s%N)"
docker rm -f "$SOURCE_CONTAINER" >/dev/null
docker volume rm "$PGVOL" >/dev/null
docker volume inspect "$REPOVOL" >/dev/null || die "repository disappeared"
docker volume inspect "$LEDGER_VOL" >/dev/null || die "ledger disappeared"

docker volume create "$PGVOL" >/dev/null
MARKER_AFTER="$(docker run --rm --entrypoint sh -v "${PGVOL}:/var/lib/postgresql" "$IMAGE" -lc \
  "if [ -e '$SOURCE_MARKER' ]; then echo present; else echo absent; fi")"
test "$MARKER_AFTER" = "absent" || die "old PGDATA marker survived volume replacement"
echo "COMPLETE DISPOSABLE PGDATA LOSS: PROVEN"
echo "REPOSITORY + LEDGER SURVIVED: PASS"

echo
echo "S9 — RESTORE B0 + PITR TO R1"

RESTORE_START_NS="$(date +%s%N)"
docker run --rm \
  --user root \
  --entrypoint /usr/bin/pgbackrest \
  -v "${PGVOL}:/var/lib/postgresql" \
  -v "${REPOVOL}:/var/lib/pgbackrest:ro" \
  "$IMAGE" \
  --stanza=dante \
  --pg1-path=/var/lib/postgresql/18/docker \
  --repo1-path=/var/lib/pgbackrest \
  --set="$B0" \
  --type=name \
  --target="$RESTORE_POINT" \
  --target-timeline="$TARGET_TIMELINE" \
  --target-action=promote \
  --archive-mode=off \
  --log-level-console=info \
  restore
RESTORE_END_NS="$(date +%s%N)"
PHYSICAL_RESTORE_SECONDS="$(seconds_between_ns "$RESTORE_START_NS" "$RESTORE_END_NS")"

normalize_pg18_parent

RECOVERY_START_NS="$(date +%s%N)"
docker run -d \
  --name "$RESTORED_CONTAINER" \
  -v "${PGVOL}:/var/lib/postgresql" \
  -v "${REPOVOL}:/var/lib/pgbackrest:ro" \
  "$IMAGE" \
  postgres \
    -c shared_preload_libraries=pg_stat_statements \
    -c compute_query_id=on >/dev/null

wait_promoted "$RESTORED_CONTAINER" || die "restored PITR target did not promote"
RECOVERY_READY_NS="$(date +%s%N)"
RECOVERY_WALL_SECONDS="$(seconds_between_ns "$RECOVERY_START_NS" "$RECOVERY_READY_NS")"

docker logs --timestamps "$RESTORED_CONTAINER" >"$RECOVERY_LOG" 2>&1
TIMING_OUTPUT="$(python3 - "$RECOVERY_LOG" <<'PY'
from __future__ import annotations
from datetime import datetime
import re
import sys

patterns = {
    "start": ("starting point-in-time recovery", "starting archive recovery"),
    "target": (
        "recovery stopping at restore point",
        "recovery stopping after restore point",
        "recovery stopping before restore point",
    ),
    "ready": ("database system is ready to accept connections",),
}
events: dict[str, datetime] = {}
with open(sys.argv[1], encoding="utf-8", errors="replace") as fh:
    for raw in fh:
        line = raw.rstrip("\n")
        lower = line.lower()
        match = re.match(r"^(\S+)\s+(.*)$", line)
        if not match:
            continue
        stamp, _message = match.groups()
        try:
            ts = datetime.fromisoformat(stamp.replace("Z", "+00:00"))
        except ValueError:
            continue
        for key, needles in patterns.items():
            if key not in events and any(needle in lower for needle in needles):
                events[key] = ts

missing = [key for key in ("start", "target", "ready") if key not in events]
if missing:
    raise SystemExit(f"missing recovery timing events: {','.join(missing)}")
print(f"{(events['target']-events['start']).total_seconds():.6f}|"
      f"{(events['ready']-events['start']).total_seconds():.6f}|"
      f"{(events['ready']-events['target']).total_seconds():.6f}")
PY
)"
IFS='|' read -r REPLAY_TO_TARGET_SECONDS LOG_RECOVERY_TO_READY_SECONDS TARGET_TO_READY_SECONDS <<<"$TIMING_OUTPUT"

echo "PHYSICAL_RESTORE_SECONDS=$PHYSICAL_RESTORE_SECONDS"
echo "REPLAY_TO_TARGET_SECONDS=$REPLAY_TO_TARGET_SECONDS"
echo "RECOVERY_TO_READY_SECONDS=$LOG_RECOVERY_TO_READY_SECONDS"

echo
echo "S10 — PROVE PITR STATE + PHYSICAL RESURRECTION WHILE ISOLATED"

assert_current_contract "$RESTORED_CONTAINER"

PRE_RECONCILE="$(docker exec --user postgres "$RESTORED_CONTAINER" psql -X -d dante -Atqc "
SELECT
  (SELECT count(*) FROM dante.person WHERE person_ref='$A_REF'::uuid),
  (SELECT count(*) FROM dante.person WHERE person_ref='$B_REF'::uuid),
  (SELECT count(*) FROM dante.material_state_retirement WHERE material_state_ref='$STATE_REF'::uuid),
  (SELECT count(*) FROM dante.session_timing_absolute WHERE material_state_ref='$STATE_REF'::uuid);
")"
test "$PRE_RECONCILE" = "1|0|0|1" || die "pre-reconcile A|B|tombstone|X=$PRE_RECONCILE"
echo "A PRESENT / B ABSENT: PASS"
echo "OLD X PHYSICALLY RESURRECTED / TOMBSTONE ABSENT: PROVEN"

echo
echo "S11 — LOAD LEDGER + RECONCILE BEFORE REOPEN"

RECONCILE_START_NS="$(date +%s%N)"
copy_ledger_volume_to_readback

cd "$REPO_ROOT/apps/backend"
LEDGER_RECORD="$(uv run --frozen python - "$LEDGER_READ" <<'PY'
from pathlib import Path
import sys
from dante.platform.recovery.suppression_ledger import load_committed_suppressions

records = load_committed_suppressions(Path(sys.argv[1]))
if len(records) != 1:
    raise SystemExit(f"expected exactly one committed suppression, got {len(records)}")
r = records[0]
print("|".join((
    r.recovery_suppression_ref,
    r.material_state_ref,
    r.facet_code,
    r.effect,
    r.retirement_code,
    r.accepted_at,
)))
PY
)"
cd "$REPO_ROOT"

IFS='|' read -r L_SUPPRESSION_REF L_STATE_REF L_FACET L_EFFECT L_RETIREMENT L_ACCEPTED_AT <<<"$LEDGER_RECORD"
test "$L_SUPPRESSION_REF" = "$SUPPRESSION_REF" || die "ledger suppression ref mismatch"
test "$L_STATE_REF" = "$STATE_REF" || die "ledger state ref mismatch"
test "$L_FACET" = "session.timing" || die "ledger facet mismatch"
test "$L_EFFECT" = "suppress_payload" || die "ledger effect mismatch"
test "$L_RETIREMENT" = "redacted" || die "ledger retirement mismatch"

docker exec -i --user postgres "$RESTORED_CONTAINER" psql -X -v ON_ERROR_STOP=1 -d dante <<SQL
BEGIN;
SET LOCAL ROLE dante_owner;
INSERT INTO dante.material_state_retirement(
  material_state_ref,retirement_code,retired_at,recovery_suppression_ref
)
VALUES (
  '$L_STATE_REF'::uuid,'$L_RETIREMENT',timestamptz '$L_ACCEPTED_AT','$L_SUPPRESSION_REF'::uuid
);
DELETE FROM dante.session_timing_absolute WHERE material_state_ref='$L_STATE_REF'::uuid;
COMMIT;
SQL

RECONCILE_END_NS="$(date +%s%N)"
RECONCILIATION_SECONDS="$(seconds_between_ns "$RECONCILE_START_NS" "$RECONCILE_END_NS")"

FINAL_SHAPE="$(docker exec --user postgres "$RESTORED_CONTAINER" psql -X -d dante -Atqc "
SELECT
  (SELECT count(*) FROM dante.session WHERE session_ref='$SESSION_REF'::uuid),
  (SELECT count(*) FROM dante.native_address WHERE native_ref='$SESSION_REF'::uuid),
  (SELECT count(*) FROM dante.material_state_address WHERE material_state_ref='$STATE_REF'::uuid),
  (SELECT count(*) FROM dante.session_timing_state WHERE material_state_ref='$STATE_REF'::uuid),
  (SELECT count(*) FROM dante.material_state_retirement WHERE material_state_ref='$STATE_REF'::uuid),
  (SELECT count(*) FROM dante.session_timing_absolute WHERE material_state_ref='$STATE_REF'::uuid),
  (SELECT count(*) FROM dante.native_current_material_state WHERE material_state_ref='$STATE_REF'::uuid),
  (SELECT count(*) FROM dante.session_timing_current_history WHERE material_state_ref='$STATE_REF'::uuid);
")"
test "$FINAL_SHAPE" = "1|1|1|1|1|0|1|1" || die "final anti-resurrection shape=$FINAL_SHAPE"

set +e
docker exec --user postgres "$RESTORED_CONTAINER" psql -X -v ON_ERROR_STOP=1 -d dante -c \
  "SET ROLE dante_owner; INSERT INTO dante.session_timing_absolute(material_state_ref,started_at,start_precision_code) VALUES ('$STATE_REF'::uuid,clock_timestamp(),'exact');" \
  >/dev/null 2>&1
REINSERT_RC=$?
set -e
test "$REINSERT_RC" -ne 0 || die "retired payload reinsertion unexpectedly succeeded"
echo "LEDGER RECONCILIATION: PASS"
echo "PAYLOAD REINSERTION: REJECTED"

echo
echo "S12 — FINAL STRUCTURAL / RUNTIME / REOPEN GATE"

ACCEPTANCE_START_NS="$(date +%s%N)"
assert_current_contract "$RESTORED_CONTAINER"

FINAL_IN_RECOVERY="$(docker exec --user postgres "$RESTORED_CONTAINER" psql -X -d dante -Atqc \
  'SELECT pg_is_in_recovery();')"
test "$FINAL_IN_RECOVERY" = "f" || die "final target still in recovery"

RUNTIME_STATE="$(docker exec -e PGPASSWORD="$(cat "$RUNTIME_SECRET")" "$RESTORED_CONTAINER" \
  psql -X -h 127.0.0.1 -p 5432 -U dante_runtime -d dante -Atqc "
SELECT
  (SELECT count(*) FROM dante.person WHERE person_ref='$A_REF'::uuid),
  (SELECT count(*) FROM dante.person WHERE person_ref='$B_REF'::uuid),
  (SELECT count(*) FROM dante.material_state_retirement WHERE material_state_ref='$STATE_REF'::uuid);
")"
test "$RUNTIME_STATE" = "1|0|1" || die "runtime A|B|tombstone=$RUNTIME_STATE"

ACCEPTANCE_END_NS="$(date +%s%N)"
ACCEPTANCE_SECONDS="$(seconds_between_ns "$ACCEPTANCE_START_NS" "$ACCEPTANCE_END_NS")"
RECOVERY_ACCEPTED_NS="$ACCEPTANCE_END_NS"
DESTRUCTION_TO_ACCEPTED_SECONDS="$(seconds_between_ns "$DESTRUCTION_START_NS" "$RECOVERY_ACCEPTED_NS")"

REPO_BACKUP_HASH_AFTER="$(docker run --rm --entrypoint sha256sum -v "${REPOVOL}:/repo:ro" "$IMAGE" \
  /repo/backup/dante/backup.info | awk '{print $1}')"
REPO_ARCHIVE_HASH_AFTER="$(docker run --rm --entrypoint sha256sum -v "${REPOVOL}:/repo:ro" "$IMAGE" \
  /repo/archive/dante/archive.info | awk '{print $1}')"
test "$REPO_BACKUP_HASH_AFTER" = "$REPO_BACKUP_HASH_BEFORE" || die "disposable backup.info changed during restore"
test "$REPO_ARCHIVE_HASH_AFTER" = "$REPO_ARCHIVE_HASH_BEFORE" || die "disposable archive.info changed during restore"

for volume in "${PROTECTED_VOLUMES[@]}"; do
  after="$(volume_fingerprint "$volume")"
  test "$after" = "${PROTECTED_BEFORE[$volume]}" || die "protected volume metadata changed: $volume"
done

REAL_BACKUP_INFO_AFTER="$(repo_info_hash "$REAL_RECOVERY_REPOVOL" "backup/dante/backup.info")"
REAL_ARCHIVE_INFO_AFTER="$(repo_info_hash "$REAL_RECOVERY_REPOVOL" "archive/dante/archive.info")"
CP05_AFTER="$(container_fingerprint "$CP05_TARGET")"

test "$REAL_BACKUP_INFO_AFTER" = "$REAL_BACKUP_INFO_BEFORE" || die "real recovery backup.info changed"
test "$REAL_ARCHIVE_INFO_AFTER" = "$REAL_ARCHIVE_INFO_BEFORE" || die "real recovery archive.info changed"
test "$CP05_AFTER" = "$CP05_BEFORE" || die "retained CP05 target changed"
test -z "$(git status --porcelain)" || die "Git worktree changed"

echo "DATABASE LOCAL REOPEN: PASS"
echo "DERIVED STORE GATE: NOT_ACTIVATED / NO FALSE PASS"
echo "OBJECT STORE GATE:  NOT_ACTIVATED / NO FALSE PASS"
echo "REMOTE PROVIDER:     TBD / NOT ACTIVATED"

echo
echo "S13 — WRITE LOCAL EVIDENCE REPORT"

export CP07_RUN_ID="$RUN_ID"
export CP07_PROOF_HEAD="$PROOF_HEAD"
export CP07_GIT_BRANCH="$GIT_BRANCH"
export CP07_GIT_UPSTREAM="$GIT_UPSTREAM"
export CP07_RECOVERY_IMAGE="$IMAGE"
export CP07_B0="$B0"
export CP07_BACKUP_SECONDS="$BACKUP_SECONDS"
export CP07_BACKUP_SIZE_BYTES="$BACKUP_SIZE_BYTES"
export CP07_RESTORE_POINT="$RESTORE_POINT"
export CP07_RESTORE_LSN="$RESTORE_LSN"
export CP07_RESTORE_WAL="$RESTORE_WAL"
export CP07_RESTORE_POINT_AGE_SECONDS="$RESTORE_POINT_AGE_SECONDS"
export CP07_WAL_ARCHIVE_FRESHNESS_SECONDS="$WAL_ARCHIVE_FRESHNESS_SECONDS"
export CP07_PHYSICAL_RESTORE_SECONDS="$PHYSICAL_RESTORE_SECONDS"
export CP07_RECOVERY_WALL_SECONDS="$RECOVERY_WALL_SECONDS"
export CP07_REPLAY_TO_TARGET_SECONDS="$REPLAY_TO_TARGET_SECONDS"
export CP07_LOG_RECOVERY_TO_READY_SECONDS="$LOG_RECOVERY_TO_READY_SECONDS"
export CP07_TARGET_TO_READY_SECONDS="$TARGET_TO_READY_SECONDS"
export CP07_RECONCILIATION_SECONDS="$RECONCILIATION_SECONDS"
export CP07_ACCEPTANCE_SECONDS="$ACCEPTANCE_SECONDS"
export CP07_DESTRUCTION_TO_ACCEPTED_SECONDS="$DESTRUCTION_TO_ACCEPTED_SECONDS"
export CP07_SESSION_REF="$SESSION_REF"
export CP07_STATE_REF="$STATE_REF"
export CP07_SUPPRESSION_REF="$SUPPRESSION_REF"
export CP07_A_REF="$A_REF"
export CP07_B_REF="$B_REF"

python3 - "$REPORT_PATH" <<'PY'
from __future__ import annotations
from datetime import UTC, datetime
import json
import os
from pathlib import Path
import sys

def f(name: str) -> float:
    return float(os.environ[name])

def i(name: str) -> int:
    return int(os.environ[name])

report = {
    "report_version": 1,
    "status": "LOCAL_PASS",
    "scope": "whole_local_postgresql_operator_recovery",
    "completed_at": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
    "run_id": os.environ["CP07_RUN_ID"],
    "git_proof_head": os.environ["CP07_PROOF_HEAD"],
    "git_branch": os.environ["CP07_GIT_BRANCH"],
    "git_upstream": os.environ["CP07_GIT_UPSTREAM"],
    "recovery_image": os.environ["CP07_RECOVERY_IMAGE"],
    "database": {
        "postgresql_server_version_num": 180006,
        "alembic_head": "20260830_09",
        "topology": "69|5|15|76|97|69|123|0|0|0",
    },
    "backup": {
        "label": os.environ["CP07_B0"],
        "duration_seconds": f("CP07_BACKUP_SECONDS"),
        "repository_size_bytes": i("CP07_BACKUP_SIZE_BYTES"),
        "wal_archive_freshness_at_disaster_seconds": f("CP07_WAL_ARCHIVE_FRESHNESS_SECONDS"),
    },
    "recovery_point": {
        "name": os.environ["CP07_RESTORE_POINT"],
        "lsn": os.environ["CP07_RESTORE_LSN"],
        "wal": os.environ["CP07_RESTORE_WAL"],
        "age_at_disaster_seconds": f("CP07_RESTORE_POINT_AGE_SECONDS"),
        "deterministic_state": "A_present_B_absent",
        "lost_fixture_count": 1,
    },
    "timings": {
        "physical_restore_seconds": f("CP07_PHYSICAL_RESTORE_SECONDS"),
        "recovery_process_wall_seconds": f("CP07_RECOVERY_WALL_SECONDS"),
        "replay_to_target_seconds": f("CP07_REPLAY_TO_TARGET_SECONDS"),
        "recovery_to_ready_seconds": f("CP07_LOG_RECOVERY_TO_READY_SECONDS"),
        "target_to_ready_seconds": f("CP07_TARGET_TO_READY_SECONDS"),
        "semantic_reconciliation_seconds": f("CP07_RECONCILIATION_SECONDS"),
        "structural_security_acceptance_seconds": f("CP07_ACCEPTANCE_SECONDS"),
        "pgdata_loss_to_database_local_reopen_seconds": f("CP07_DESTRUCTION_TO_ACCEPTED_SECONDS"),
    },
    "anti_resurrection": {
        "pre_reconcile": "A=1|B=0|tombstone=0|payload_X=1",
        "physical_resurrection": "PROVEN",
        "post_reconcile": "session=1|native=1|state_address=1|state=1|tombstone=1|payload_X=0|current=1|history=1",
        "payload_reinsertion": "REJECTED",
        "session_ref": os.environ["CP07_SESSION_REF"],
        "material_state_ref": os.environ["CP07_STATE_REF"],
        "recovery_suppression_ref": os.environ["CP07_SUPPRESSION_REF"],
    },
    "fixtures": {
        "A_ref": os.environ["CP07_A_REF"],
        "B_ref": os.environ["CP07_B_REF"],
    },
    "reopen": {
        "database_local": "PASS",
        "derived_state": "NOT_ACTIVATED_NO_FALSE_PASS",
        "object_store": "NOT_ACTIVATED_NO_FALSE_PASS",
        "production_cloud": "NOT_CLAIMED",
    },
    "remote_backup_provider": {
        "decision": "TBD",
        "activated": False,
        "exercised": False,
    },
    "non_interference": {
        "normal_local_volumes": "PASS",
        "real_recovery_repository": "PASS",
        "retained_cp05_target": "PASS",
        "git_worktree": "PASS",
    },
    "measurement_note": "LOCAL rehearsal observations only; not production RPO/RTO targets.",
}

path = Path(sys.argv[1])
path.parent.mkdir(parents=True, exist_ok=True)
path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
PY
chmod 600 "$REPORT_PATH"

python3 - "$REPORT_PATH" <<'PY'
import json
from pathlib import Path
import sys
data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
assert data["status"] == "LOCAL_PASS"
assert data["reopen"]["database_local"] == "PASS"
assert data["remote_backup_provider"]["decision"] == "TBD"
assert data["remote_backup_provider"]["activated"] is False
assert data["non_interference"]["real_recovery_repository"] == "PASS"
print(json.dumps(data, indent=2, sort_keys=True))
PY

echo
echo "S14 — CLEANUP DISPOSABLE CP07 RESOURCES"

cleanup_resources

for resource in "$PGVOL" "$REPOVOL" "$LEDGER_VOL"; do
  if docker volume inspect "$resource" >/dev/null 2>&1; then
    die "disposable volume survived cleanup: $resource"
  fi
done
for container in "$SOURCE_CONTAINER" "$RESTORED_CONTAINER"; do
  if docker inspect "$container" >/dev/null 2>&1; then
    die "disposable container survived cleanup: $container"
  fi
done
EXPLICIT_CLEANUP=1

RUN_ENDED_NS="$(date +%s%N)"
WHOLE_RUN_SECONDS="$(seconds_between_ns "$RUN_STARTED_NS" "$RUN_ENDED_NS")"

SUCCESS=1

echo
echo "=== CP07 WHOLE LOCAL OPERATOR RECOVERY: PASS ==="
echo "PROOF HEAD:                         $PROOF_HEAD"
echo "GIT BRANCH:                         $GIT_BRANCH"
echo "GIT UPSTREAM:                       $GIT_UPSTREAM"
echo "RECOVERY IMAGE:                     $IMAGE"
echo "BACKUP:                             $B0"
echo "BACKUP_SECONDS:                     $BACKUP_SECONDS"
echo "BACKUP_SIZE_BYTES:                  $BACKUP_SIZE_BYTES"
echo "RESTORE_POINT_AGE_SECONDS:          $RESTORE_POINT_AGE_SECONDS"
echo "WAL_ARCHIVE_FRESHNESS_SECONDS:      $WAL_ARCHIVE_FRESHNESS_SECONDS"
echo "PHYSICAL_RESTORE_SECONDS:           $PHYSICAL_RESTORE_SECONDS"
echo "REPLAY_TO_TARGET_SECONDS:           $REPLAY_TO_TARGET_SECONDS"
echo "RECOVERY_TO_READY_SECONDS:          $LOG_RECOVERY_TO_READY_SECONDS"
echo "SEMANTIC_RECONCILIATION_SECONDS:    $RECONCILIATION_SECONDS"
echo "STRUCTURAL_ACCEPTANCE_SECONDS:      $ACCEPTANCE_SECONDS"
echo "PGDATA_LOSS_TO_LOCAL_REOPEN_SECONDS:$DESTRUCTION_TO_ACCEPTED_SECONDS"
echo "WHOLE_HARNESS_SECONDS:              $WHOLE_RUN_SECONDS"
echo "DATABASE LOCAL REOPEN:              PASS"
echo "REMOTE BACKUP PROVIDER:             TBD / NOT ACTIVATED"
echo "REPORT:                             $REPORT_REL"
