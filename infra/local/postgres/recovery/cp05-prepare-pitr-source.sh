#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd -- "${SCRIPT_DIR}/../../../.." && pwd)"
PROJECT="dante-postgres-recovery"
BASE="infra/compose/local.yaml"
OVERLAY="infra/compose/postgres-recovery.override.yaml"
IMAGE="dante-postgres-recovery:18.6-pgbackrest-2.59.1"
PGVOL="dante-postgres-recovery_postgres-data"
REPOVOL="dante-postgres-recovery_pgbackrest-repository"
SOURCE_CONTAINER="dante-postgres-recovery-cp04-restore"
BASE_BACKUP_FILE="infra/compose/secrets/postgres_recovery_cp04_backup_label.local"
SCENARIO_FILE="infra/compose/secrets/postgres_recovery_cp05_scenario.local"
BASELINE_REF="01993f19-9c00-7000-8000-000000000001"

cd "$REPO_ROOT"

compose() {
  docker compose -p "$PROJECT" -f "$BASE" -f "$OVERLAY" "$@"
}

die() {
  echo "FAIL: $*" >&2
  exit 1
}

repo_find() {
  local pattern="$1"
  docker run --rm \
    --entrypoint sh \
    -v "${REPOVOL}:/var/lib/pgbackrest:ro" \
    "$IMAGE" \
    -lc "find /var/lib/pgbackrest/archive/dante -type f -name '$pattern' -print -quit"
}

wait_repo_file() {
  local pattern="$1"
  local label="$2"
  local found=""

  for _ in $(seq 1 60); do
    found="$(repo_find "$pattern")"
    if [ -n "$found" ]; then
      echo "$label: $found"
      return 0
    fi
    sleep 1
  done

  return 1
}

echo "=== DANTE CP05 — prepare deterministic PITR source ==="

test "$(git branch --show-current)" = "feature/postgres-recovery" || die "wrong Git branch"
test "$(git rev-parse HEAD)" = "$(git rev-parse origin/feature/postgres-recovery)" || die "local HEAD differs from origin"
test -z "$(git status --porcelain)" || die "worktree is not clean"
test -s "$BASE_BACKUP_FILE" || die "missing $BASE_BACKUP_FILE"
git check-ignore -q "$SCENARIO_FILE" || die "$SCENARIO_FILE is not ignored by Git"

docker image inspect "$IMAGE" >/dev/null || die "missing image $IMAGE"
docker volume inspect "$PGVOL" >/dev/null || die "missing $PGVOL"
docker volume inspect "$REPOVOL" >/dev/null || die "missing $REPOVOL"
test "$PGVOL" != "$REPOVOL" || die "PGDATA and repository volumes unexpectedly match"

base_backup="$(cat "$BASE_BACKUP_FILE")"
source_status="$(docker inspect "$SOURCE_CONTAINER" --format '{{.State.Status}}' 2>/dev/null || true)"
test "$source_status" = "running" || die "$SOURCE_CONTAINER is not running"

archive_mode="$(docker exec --user postgres "$SOURCE_CONTAINER" psql -X -d dante -Atqc 'SHOW archive_mode;')"
in_recovery="$(docker exec --user postgres "$SOURCE_CONTAINER" psql -X -d dante -Atqc 'SELECT pg_is_in_recovery();')"
current_wal="$(docker exec --user postgres "$SOURCE_CONTAINER" psql -X -d dante -Atqc 'SELECT pg_walfile_name(pg_current_wal_lsn());')"

test "$archive_mode" = "off" || die "expected CP04 isolated target archive_mode=off, got $archive_mode"
test "$in_recovery" = "f" || die "CP04 target is unexpectedly in recovery"

timeline_hex="${current_wal:0:8}"
target_timeline="$((16#$timeline_hex))"
test "$target_timeline" -ge 2 || die "expected a promoted recovery timeline, got $target_timeline"
history_file="${timeline_hex}.history"
history_path="/var/lib/postgresql/18/docker/pg_wal/${history_file}"

docker exec --user postgres "$SOURCE_CONTAINER" test -f "$history_path" \
  || die "missing local timeline history $history_path"

echo "Base backup:      $base_backup"
echo "Current WAL:      $current_wal"
echo "Target timeline:  $target_timeline"
echo "Timeline history: $history_file"

echo
echo "=== restart CP04 restored PGDATA as archiving CP05 primary ==="

docker rm -f "$SOURCE_CONTAINER" >/dev/null

container_id="$(
  compose run -d \
    --service-ports \
    --name "$SOURCE_CONTAINER" \
    postgres \
    postgres \
      -c shared_preload_libraries=pg_stat_statements \
      -c compute_query_id=on \
      -c archive_mode=on \
      -c "archive_command=/usr/bin/pgbackrest --stanza=dante archive-push %p"
)"
test -n "$container_id" || die "CP05 source primary did not start"

ready=0
for _ in $(seq 1 60); do
  if docker exec "$SOURCE_CONTAINER" pg_isready -h 127.0.0.1 -p 5432 -U postgres -d dante >/dev/null 2>&1; then
    ready=1
    break
  fi
  sleep 1
done
[ "$ready" = "1" ] || { docker logs "$SOURCE_CONTAINER"; die "CP05 source primary not ready"; }

archive_mode="$(docker exec --user postgres "$SOURCE_CONTAINER" psql -X -d dante -Atqc 'SHOW archive_mode;')"
archive_command="$(docker exec --user postgres "$SOURCE_CONTAINER" psql -X -d dante -Atqc 'SHOW archive_command;')"
in_recovery="$(docker exec --user postgres "$SOURCE_CONTAINER" psql -X -d dante -Atqc 'SELECT pg_is_in_recovery();')"
current_wal="$(docker exec --user postgres "$SOURCE_CONTAINER" psql -X -d dante -Atqc 'SELECT pg_walfile_name(pg_current_wal_lsn());')"

test "$archive_mode" = "on" || die "archive_mode=$archive_mode"
test "$archive_command" = "/usr/bin/pgbackrest --stanza=dante archive-push %p" || die "unexpected archive_command"
test "$in_recovery" = "f" || die "source is unexpectedly in recovery"
test "${current_wal:0:8}" = "$timeline_hex" || die "timeline changed unexpectedly during restart"

echo "CP05 ARCHIVING PRIMARY: PASS"

echo
echo "=== prove current-timeline WAL and history archive ==="

wal_before="$current_wal"
docker exec --user postgres "$SOURCE_CONTAINER" psql -X -d dante -Atqc 'SELECT pg_switch_wal();' >/dev/null
wait_repo_file "${wal_before}-*" "TIMELINE WAL ARCHIVED" || die "current-timeline WAL was not archived"

history_repo="$(repo_find "${history_file}*")"
if [ -n "$history_repo" ]; then
  echo "TIMELINE HISTORY ALREADY ARCHIVED: $history_repo"
else
  # A timeline history created while the CP04 verification target had archive_mode=off
  # is not queued retroactively when archiving is enabled later. Push that already-existing
  # PostgreSQL history file through pgBackRest explicitly; do not manipulate archive_status.
  docker exec --user postgres "$SOURCE_CONTAINER" \
    pgbackrest --stanza=dante archive-push "$history_path"
  echo "TIMELINE HISTORY MANUAL ARCHIVE-PUSH: PASS"
  wait_repo_file "${history_file}*" "TIMELINE HISTORY ARCHIVED" \
    || die "$history_file is absent from repository"
fi

docker exec --user postgres "$SOURCE_CONTAINER" pgbackrest --stanza=dante check
echo "TIMELINE PGBACKREST CHECK: PASS"

echo
echo "=== create deterministic A / restore-point / B scenario ==="

scenario_id="dante_cp05_$(date -u +%Y%m%dT%H%M%SZ)_$$"
restore_point="${scenario_id}_R1"
a_ref="$(docker exec --user postgres "$SOURCE_CONTAINER" psql -X -d dante -Atqc 'SELECT uuidv7();')"
b_ref="$(docker exec --user postgres "$SOURCE_CONTAINER" psql -X -d dante -Atqc 'SELECT uuidv7();')"

test -n "$a_ref" || die "failed to generate A UUID"
test -n "$b_ref" || die "failed to generate B UUID"
test "$a_ref" != "$b_ref" || die "A and B UUIDs unexpectedly match"

docker exec --user postgres "$SOURCE_CONTAINER" \
  psql -X -v ON_ERROR_STOP=1 -d dante -Atqc "
    SET ROLE dante_owner;
    INSERT INTO dante.person(person_ref) VALUES ('$a_ref'::uuid);
    RESET ROLE;
  "

test "$(docker exec --user postgres "$SOURCE_CONTAINER" psql -X -d dante -Atqc "SELECT count(*) FROM dante.person WHERE person_ref='$a_ref'::uuid;")" = "1" \
  || die "A was not committed"
echo "A COMMIT: PASS"

restore_lsn="$(docker exec --user postgres "$SOURCE_CONTAINER" psql -X -d dante -Atqc "SELECT pg_create_restore_point('$restore_point');")"
test -n "$restore_lsn" || die "restore point was not created"
restore_wal="$(docker exec --user postgres "$SOURCE_CONTAINER" psql -X -d dante -Atqc "SELECT pg_walfile_name('$restore_lsn'::pg_lsn);")"

docker exec --user postgres "$SOURCE_CONTAINER" psql -X -d dante -Atqc 'SELECT pg_switch_wal();' >/dev/null
wait_repo_file "${restore_wal}-*" "RESTORE-POINT WAL ARCHIVED" || die "WAL containing restore point was not archived"

docker exec --user postgres "$SOURCE_CONTAINER" \
  psql -X -v ON_ERROR_STOP=1 -d dante -Atqc "
    SET ROLE dante_owner;
    INSERT INTO dante.person(person_ref) VALUES ('$b_ref'::uuid);
    RESET ROLE;
  "

test "$(docker exec --user postgres "$SOURCE_CONTAINER" psql -X -d dante -Atqc "SELECT count(*) FROM dante.person WHERE person_ref='$b_ref'::uuid;")" = "1" \
  || die "B was not committed"
echo "B COMMIT: PASS"

b_wal="$(docker exec --user postgres "$SOURCE_CONTAINER" psql -X -d dante -Atqc 'SELECT pg_walfile_name(pg_current_wal_lsn());')"
docker exec --user postgres "$SOURCE_CONTAINER" psql -X -d dante -Atqc 'SELECT pg_switch_wal();' >/dev/null
wait_repo_file "${b_wal}-*" "POST-RESTORE-POINT WAL ARCHIVED" || die "WAL containing B was not archived"

docker exec --user postgres "$SOURCE_CONTAINER" pgbackrest --stanza=dante check
echo "POST-SCENARIO PGBACKREST CHECK: PASS"

source_counts="$(docker exec --user postgres "$SOURCE_CONTAINER" psql -X -d dante -Atqc "
  SELECT
    count(*) FILTER (WHERE person_ref='${BASELINE_REF}'::uuid),
    count(*) FILTER (WHERE person_ref='${a_ref}'::uuid),
    count(*) FILTER (WHERE person_ref='${b_ref}'::uuid)
  FROM dante.person;
")"
test "$source_counts" = "1|1|1" || die "source baseline|A|B=$source_counts"

mkdir -p "$(dirname "$SCENARIO_FILE")"
umask 077
cat > "$SCENARIO_FILE" <<EOF
BASE_BACKUP=$base_backup
TARGET_TIMELINE=$target_timeline
TIMELINE_HISTORY=$history_file
SCENARIO_ID=$scenario_id
RESTORE_POINT=$restore_point
RESTORE_LSN=$restore_lsn
RESTORE_WAL=$restore_wal
A_REF=$a_ref
B_REF=$b_ref
B_WAL=$b_wal
EOF
chmod 600 "$SCENARIO_FILE"

test -z "$(git status --porcelain)" || die "tracked/unignored worktree changes appeared"

echo
echo "Scenario:       $scenario_id"
echo "Restore point:  $restore_point"
echo "Restore LSN:    $restore_lsn"
echo "Restore WAL:    $restore_wal"
echo "A:              $a_ref"
echo "B:              $b_ref"
echo "B WAL:          $b_wal"
echo "Scenario file:  $SCENARIO_FILE"
echo "=== CP05 SOURCE PREPARATION: PASS ==="
echo "No PGDATA was deleted."
