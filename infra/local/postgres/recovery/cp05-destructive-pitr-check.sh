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
TARGET_CONTAINER="dante-postgres-recovery-cp05-pitr"
SCENARIO_FILE="infra/compose/secrets/postgres_recovery_cp05_scenario.local"
RUNTIME_SECRET="infra/compose/secrets/postgres_recovery_runtime_password.local"
EXPECTED_ALEMBIC="20260826_08"
EXPECTED_TOPOLOGY="68|5|14|75|95|68|120|0|0|0"
BASELINE_REF="01993f19-9c00-7000-8000-000000000001"
SOURCE_MARKER="/var/lib/postgresql/CP05_SOURCE_VOLUME_MUST_NOT_SURVIVE"

cd "$REPO_ROOT"

compose() {
  docker compose -p "$PROJECT" -f "$BASE" -f "$OVERLAY" "$@"
}

die() {
  echo "FAIL: $*" >&2
  echo "The pgBackRest repository volume is intentionally never deleted by this harness." >&2
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

echo "=== DANTE CP05 — deterministic destructive PITR ==="

test "$(git branch --show-current)" = "feature/postgres-recovery" || die "wrong Git branch"
test "$(git rev-parse HEAD)" = "$(git rev-parse origin/feature/postgres-recovery)" || die "local HEAD differs from origin"
test -z "$(git status --porcelain)" || die "worktree is not clean"
test -s "$SCENARIO_FILE" || die "missing $SCENARIO_FILE"
test -s "$RUNTIME_SECRET" || die "missing $RUNTIME_SECRET"
git check-ignore -q "$SCENARIO_FILE" || die "$SCENARIO_FILE is not ignored by Git"

# shellcheck disable=SC1090
source "$SCENARIO_FILE"

: "${BASE_BACKUP:?missing BASE_BACKUP}"
: "${TARGET_TIMELINE:?missing TARGET_TIMELINE}"
: "${TIMELINE_HISTORY:?missing TIMELINE_HISTORY}"
: "${SCENARIO_ID:?missing SCENARIO_ID}"
: "${RESTORE_POINT:?missing RESTORE_POINT}"
: "${RESTORE_LSN:?missing RESTORE_LSN}"
: "${RESTORE_WAL:?missing RESTORE_WAL}"
: "${A_REF:?missing A_REF}"
: "${B_REF:?missing B_REF}"
: "${B_WAL:?missing B_WAL}"

test "$A_REF" != "$B_REF" || die "A and B refs match"

docker image inspect "$IMAGE" >/dev/null || die "missing image $IMAGE"
docker volume inspect "$PGVOL" >/dev/null || die "missing $PGVOL"
docker volume inspect "$REPOVOL" >/dev/null || die "missing $REPOVOL"
test "$PGVOL" != "$REPOVOL" || die "PGDATA and repository volumes unexpectedly match"

source_status="$(docker inspect "$SOURCE_CONTAINER" --format '{{.State.Status}}' 2>/dev/null || true)"
test "$source_status" = "running" || die "$SOURCE_CONTAINER is not running"

echo
echo "=== verify source state and complete WAL chain ==="

source_archive_mode="$(docker exec --user postgres "$SOURCE_CONTAINER" psql -X -d dante -Atqc 'SHOW archive_mode;')"
source_in_recovery="$(docker exec --user postgres "$SOURCE_CONTAINER" psql -X -d dante -Atqc 'SELECT pg_is_in_recovery();')"
source_wal="$(docker exec --user postgres "$SOURCE_CONTAINER" psql -X -d dante -Atqc 'SELECT pg_walfile_name(pg_current_wal_lsn());')"
source_timeline_hex="${source_wal:0:8}"
source_timeline="$((16#$source_timeline_hex))"

test "$source_archive_mode" = "on" || die "source archive_mode=$source_archive_mode"
test "$source_in_recovery" = "f" || die "source is unexpectedly in recovery"
test "$source_timeline" = "$TARGET_TIMELINE" || die "source timeline=$source_timeline expected=$TARGET_TIMELINE"

source_counts="$(docker exec --user postgres "$SOURCE_CONTAINER" psql -X -d dante -Atqc "
  SELECT
    count(*) FILTER (WHERE person_ref='${BASELINE_REF}'::uuid),
    count(*) FILTER (WHERE person_ref='${A_REF}'::uuid),
    count(*) FILTER (WHERE person_ref='${B_REF}'::uuid)
  FROM dante.person;
")"
test "$source_counts" = "1|1|1" || die "source baseline|A|B=$source_counts expected=1|1|1"

history_repo="$(repo_find "${TIMELINE_HISTORY}*")"
restore_wal_repo="$(repo_find "${RESTORE_WAL}-*")"
b_wal_repo="$(repo_find "${B_WAL}-*")"
test -n "$history_repo" || die "timeline history missing from repository"
test -n "$restore_wal_repo" || die "restore-point WAL missing from repository"
test -n "$b_wal_repo" || die "post-target B WAL missing from repository"

backup_found="$(
  docker exec --user postgres "$SOURCE_CONTAINER" pgbackrest --stanza=dante --output=json info \
  | python3 -c 'import json,sys; wanted=sys.argv[1]; data=json.load(sys.stdin); labels={b["label"] for s in data for b in s.get("backup",[])}; print("yes" if wanted in labels else "no")' "$BASE_BACKUP"
)"
test "$backup_found" = "yes" || die "base backup $BASE_BACKUP not present"

docker exec --user postgres "$SOURCE_CONTAINER" pgbackrest --stanza=dante check
echo "SOURCE / WAL CHAIN: PASS"

repo_backup_hash_before="$(docker exec --user postgres "$SOURCE_CONTAINER" sha256sum /var/lib/pgbackrest/backup/dante/backup.info | awk '{print $1}')"
repo_archive_hash_before="$(docker exec --user postgres "$SOURCE_CONTAINER" sha256sum /var/lib/pgbackrest/archive/dante/archive.info | awk '{print $1}')"

printf '%s\n' \
  "Base backup:     $BASE_BACKUP" \
  "Scenario:        $SCENARIO_ID" \
  "Restore point:   $RESTORE_POINT" \
  "Restore LSN:     $RESTORE_LSN" \
  "Restore WAL:     $RESTORE_WAL" \
  "A:               $A_REF" \
  "B:               $B_REF" \
  "B WAL:           $B_WAL" \
  "Target timeline: $TARGET_TIMELINE"

echo
echo "=== write source-volume destruction marker ==="
marker_token="cp05-$(date -u +%Y%m%dT%H%M%SZ)-$$"
docker exec --user root "$SOURCE_CONTAINER" sh -lc "printf '%s\n' '$marker_token' > '$SOURCE_MARKER'"
test "$(docker exec --user root "$SOURCE_CONTAINER" cat "$SOURCE_MARKER")" = "$marker_token" || die "cannot verify source marker"

echo "SOURCE MARKER: $marker_token"
echo
echo "THIS WILL DELETE ONLY: $PGVOL"
echo "THIS WILL PRESERVE:    $REPOVOL"
printf 'Type DELETE_RECOVERY_PGDATA_FOR_PITR to continue: '
read -r confirmation
test "$confirmation" = "DELETE_RECOVERY_PGDATA_FOR_PITR" || die "destructive confirmation not provided"

echo
echo "=== destroy only recovery PostgreSQL PGDATA ==="
docker rm -f "$SOURCE_CONTAINER" >/dev/null

if docker ps -aq --filter "volume=$PGVOL" | grep -q .; then
  docker ps -a --filter "volume=$PGVOL"
  die "a container still references $PGVOL"
fi

docker volume rm "$PGVOL"
echo "PGDATA VOLUME DELETED: PASS"
docker volume inspect "$REPOVOL" >/dev/null || die "repository volume disappeared"

repo_backup_hash_after_delete="$(docker run --rm --entrypoint sha256sum -v "${REPOVOL}:/var/lib/pgbackrest:ro" "$IMAGE" /var/lib/pgbackrest/backup/dante/backup.info | awk '{print $1}')"
repo_archive_hash_after_delete="$(docker run --rm --entrypoint sha256sum -v "${REPOVOL}:/var/lib/pgbackrest:ro" "$IMAGE" /var/lib/pgbackrest/archive/dante/archive.info | awk '{print $1}')"
test "$repo_backup_hash_after_delete" = "$repo_backup_hash_before" || die "backup.info changed during PGDATA deletion"
test "$repo_archive_hash_after_delete" = "$repo_archive_hash_before" || die "archive.info changed during PGDATA deletion"
echo "REPOSITORY SURVIVED PGDATA DELETION: PASS"

compose create postgres
compose rm -f postgres
docker volume inspect "$PGVOL" >/dev/null || die "Compose did not recreate $PGVOL"

marker_after_recreate="$(docker run --rm --entrypoint sh -v "${PGVOL}:/var/lib/postgresql" "$IMAGE" -lc "if [ -e '$SOURCE_MARKER' ]; then echo present; else echo absent; fi")"
test "$marker_after_recreate" = "absent" || die "old source marker survived volume replacement"
echo "OLD SOURCE VOLUME ABSENCE: PASS"

echo
echo "=== restore exact FULL and configure named PITR target ==="
restore_start_ns="$(date +%s%N)"
compose run --rm --no-deps \
  --user root \
  --entrypoint /usr/bin/pgbackrest \
  postgres \
  --stanza=dante \
  --set="$BASE_BACKUP" \
  --type=name \
  --target="$RESTORE_POINT" \
  --target-timeline="$TARGET_TIMELINE" \
  --target-action=promote \
  --archive-mode=off \
  --log-level-console=info \
  restore
restore_end_ns="$(date +%s%N)"
physical_restore_seconds="$(python3 - "$restore_start_ns" "$restore_end_ns" <<'PY'
import sys
start, end = map(int, sys.argv[1:])
print(f"{(end-start)/1_000_000_000:.6f}")
PY
)"
echo "PGBACKREST PITR RESTORE COMMAND: PASS"
echo "PHYSICAL_RESTORE_WALL_SECONDS=$physical_restore_seconds"

# PostgreSQL 18 persists /var/lib/postgresql while PGDATA is nested below a version
# directory. A root pgBackRest restore into a newly-created Docker volume can create
# that version parent as root:root. Normalize only the proven parent boundary.
docker run --rm --entrypoint sh -v "${PGVOL}:/var/lib/postgresql" "$IMAGE" -lc '
  set -eu
  chown postgres:postgres /var/lib/postgresql/18
  chmod 0700 /var/lib/postgresql/18
'
parent_state="$(docker run --rm --entrypoint stat -v "${PGVOL}:/var/lib/postgresql:ro" "$IMAGE" -c '%U:%G %a' /var/lib/postgresql/18)"
test "$parent_state" = "postgres:postgres 700" || die "unexpected restored parent state: $parent_state"

auto_conf="$(docker run --rm --entrypoint cat -v "${PGVOL}:/var/lib/postgresql:ro" "$IMAGE" /var/lib/postgresql/18/docker/postgresql.auto.conf)"
printf '%s\n' "$auto_conf" | grep -F "recovery_target_name = '$RESTORE_POINT'" >/dev/null || die "recovery_target_name not generated"
printf '%s\n' "$auto_conf" | grep -F "recovery_target_timeline = '$TARGET_TIMELINE'" >/dev/null || die "recovery_target_timeline not generated"
printf '%s\n' "$auto_conf" | grep -F "recovery_target_action = 'promote'" >/dev/null || die "recovery_target_action=promote not generated"
printf '%s\n' "$auto_conf" | grep -F "archive_mode = 'off'" >/dev/null || die "archive_mode=off not generated"
printf '%s\n' "$auto_conf" | grep -F "restore_command = '/usr/bin/pgbackrest --stanza=dante archive-get %f \"%p\"'" >/dev/null || die "restore_command not generated"
echo "GENERATED PITR SETTINGS: PASS"

echo
echo "=== start PITR target and reach/promote at restore point ==="
docker rm -f "$TARGET_CONTAINER" >/dev/null 2>&1 || true

target_id="$(
  compose run -d \
    --service-ports \
    --name "$TARGET_CONTAINER" \
    postgres \
    postgres \
      -c shared_preload_libraries=pg_stat_statements \
      -c compute_query_id=on
)"
test -n "$target_id" || die "PITR target did not start"

ready=0
for _ in $(seq 1 120); do
  if docker exec "$TARGET_CONTAINER" pg_isready -h 127.0.0.1 -p 5432 -U postgres -d dante >/dev/null 2>&1; then
    ready=1
    break
  fi
  sleep 1
done
[ "$ready" = "1" ] || { docker logs "$TARGET_CONTAINER"; die "PITR PostgreSQL did not become ready"; }

recovery_done=0
for _ in $(seq 1 120); do
  in_recovery="$(docker exec --user postgres "$TARGET_CONTAINER" psql -X -d dante -Atqc 'SELECT pg_is_in_recovery();' 2>/dev/null || true)"
  if [ "$in_recovery" = "f" ]; then
    recovery_done=1
    break
  fi
  sleep 1
done
[ "$recovery_done" = "1" ] || { docker logs "$TARGET_CONTAINER"; die "PITR did not reach/promote at target"; }
echo "PITR TARGET READY / PROMOTED: PASS"

echo
echo "=== assert deterministic A-present / B-absent target ==="

server_version="$(docker exec --user postgres "$TARGET_CONTAINER" psql -X -d dante -Atqc "SELECT current_setting('server_version_num');")"
archive_mode="$(docker exec --user postgres "$TARGET_CONTAINER" psql -X -d dante -Atqc 'SHOW archive_mode;')"
current_wal="$(docker exec --user postgres "$TARGET_CONTAINER" psql -X -d dante -Atqc 'SELECT pg_walfile_name(pg_current_wal_lsn());')"
alembic_head="$(docker exec --user postgres "$TARGET_CONTAINER" psql -X -d dante -Atqc 'SELECT version_num FROM dante.alembic_version;')"

test "$server_version" = "180006" || die "server_version_num=$server_version"
test "$archive_mode" = "off" || die "archive_mode=$archive_mode"
test "$alembic_head" = "$EXPECTED_ALEMBIC" || die "Alembic=$alembic_head"

promoted_timeline_hex="${current_wal:0:8}"
promoted_timeline="$((16#$promoted_timeline_hex))"
expected_promoted_timeline="$((TARGET_TIMELINE + 1))"
test "$promoted_timeline" = "$expected_promoted_timeline" || die "promoted timeline=$promoted_timeline expected=$expected_promoted_timeline"

state_counts="$(docker exec --user postgres "$TARGET_CONTAINER" psql -X -d dante -Atqc "
  SELECT
    count(*) FILTER (WHERE person_ref='${BASELINE_REF}'::uuid),
    count(*) FILTER (WHERE person_ref='${A_REF}'::uuid),
    count(*) FILTER (WHERE person_ref='${B_REF}'::uuid)
  FROM dante.person;
")"
test "$state_counts" = "1|1|0" || die "PITR baseline|A|B=$state_counts expected=1|1|0"
echo "BASELINE PRESENT: PASS"
echo "A PRESENT:        PASS"
echo "B ABSENT:         PASS"

topology="$(docker exec --user postgres "$TARGET_CONTAINER" psql -X -d dante -Atqc "
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

owners="$(docker exec --user postgres "$TARGET_CONTAINER" psql -X -d dante -Atqc "SELECT string_agg(owner, ',' ORDER BY owner) FROM (SELECT DISTINCT pg_get_userbyid(c.relowner) AS owner FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace WHERE n.nspname='dante' AND c.relname<>'alembic_version') x;")"
test "$owners" = "dante_owner" || die "owners=$owners"
roles="$(docker exec --user postgres "$TARGET_CONTAINER" psql -X -d dante -Atqc "SELECT string_agg(rolname, ',' ORDER BY rolname) FROM pg_roles WHERE rolname IN ('dante_owner','dante_migrator','dante_runtime');")"
test "$roles" = "dante_migrator,dante_owner,dante_runtime" || die "roles=$roles"
runtime_alembic="$(docker exec --user postgres "$TARGET_CONTAINER" psql -X -d dante -Atqc "SELECT has_table_privilege('dante_runtime','dante.alembic_version','SELECT');")"
test "$runtime_alembic" = "f" || die "runtime can SELECT alembic_version"
extensions="$(docker exec --user postgres "$TARGET_CONTAINER" psql -X -d dante -Atqc "SELECT string_agg(extname || '=' || extversion, ',' ORDER BY extname) FROM pg_extension WHERE extname IN ('postgis','vector','pg_trgm','unaccent','pg_stat_statements');")"
test "$extensions" = "pg_stat_statements=1.12,pg_trgm=1.6,postgis=3.6.4,unaccent=1.1,vector=0.8.6" || die "extensions=$extensions"

runtime_state="$(docker exec -e PGPASSWORD="$(cat "$RUNTIME_SECRET")" "$TARGET_CONTAINER" psql -X -h 127.0.0.1 -p 5432 -U dante_runtime -d dante -Atqc "
  SELECT
    count(*) FILTER (WHERE person_ref='${A_REF}'::uuid),
    count(*) FILTER (WHERE person_ref='${B_REF}'::uuid)
  FROM dante.person;
")"
test "$runtime_state" = "1|0" || die "runtime A|B=$runtime_state expected=1|0"
echo "CATALOG / ACL / RUNTIME PATH: PASS"

repo_backup_hash_after_restore="$(docker exec --user postgres "$TARGET_CONTAINER" sha256sum /var/lib/pgbackrest/backup/dante/backup.info | awk '{print $1}')"
repo_archive_hash_after_restore="$(docker exec --user postgres "$TARGET_CONTAINER" sha256sum /var/lib/pgbackrest/archive/dante/archive.info | awk '{print $1}')"
test "$repo_backup_hash_after_restore" = "$repo_backup_hash_before" || die "backup.info changed during PITR"
test "$repo_archive_hash_after_restore" = "$repo_archive_hash_before" || die "archive.info changed during PITR"
echo "REPOSITORY METADATA UNCHANGED BY RESTORE: PASS"

echo
echo "=== derive replay/recovery timings from PostgreSQL logs ==="
log_file="$(mktemp)"
trap 'rm -f "$log_file"' EXIT
docker logs --timestamps "$TARGET_CONTAINER" >"$log_file" 2>&1

python3 - "$log_file" <<'PY'
from __future__ import annotations

import re
import sys
from datetime import datetime

path = sys.argv[1]
patterns = {
    "start": ("starting point-in-time recovery", "starting archive recovery"),
    "target": ("recovery stopping at restore point", "recovery stopping after restore point", "recovery stopping before restore point"),
    "ready": ("database system is ready to accept connections",),
}
events: dict[str, datetime] = {}

with open(path, encoding="utf-8", errors="replace") as fh:
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

print(f"REPLAY_TO_TARGET_SECONDS={(events['target']-events['start']).total_seconds():.6f}")
print(f"RECOVERY_TO_READY_SECONDS={(events['ready']-events['start']).total_seconds():.6f}")
print(f"TARGET_TO_READY_SECONDS={(events['ready']-events['target']).total_seconds():.6f}")
PY

echo
echo "=== FINAL PITR EVIDENCE ==="
docker exec --user postgres "$TARGET_CONTAINER" psql -X -d dante -P pager=off -c "
  SELECT
    current_setting('server_version_num') AS server_version_num,
    pg_is_in_recovery() AS in_recovery,
    current_setting('archive_mode') AS archive_mode,
    pg_walfile_name(pg_current_wal_lsn()) AS current_wal;

  SELECT version_num AS alembic_head FROM dante.alembic_version;

  SELECT person_ref,
         CASE
           WHEN person_ref='${BASELINE_REF}'::uuid THEN 'BASELINE'
           WHEN person_ref='${A_REF}'::uuid THEN 'A_PRESENT'
           WHEN person_ref='${B_REF}'::uuid THEN 'B_SHOULD_BE_ABSENT'
         END AS cp05_state
  FROM dante.person
  WHERE person_ref IN ('${BASELINE_REF}'::uuid, '${A_REF}'::uuid, '${B_REF}'::uuid)
  ORDER BY cp05_state;
"

printf '%s\n' \
  "PGDATA destructive replacement          PASS" \
  "old source-volume marker absent        PASS" \
  "repository survived unchanged          PASS" \
  "base FULL exact-set restore             PASS" \
  "target timeline selected                PASS" \
  "named restore point reached             PASS" \
  "target-action promote                  PASS" \
  "new promoted timeline                  PASS" \
  "A present                              PASS" \
  "B absent                               PASS" \
  "PostgreSQL 18.6                        PASS" \
  "Alembic 20260826_08                    PASS" \
  "topology 68/5/14/75/95/68/120         PASS" \
  "DANTE owners / roles / ACL             PASS" \
  "required extensions                    PASS" \
  "dante_runtime sees A and not B         PASS"

echo "=== CP05 DETERMINISTIC PITR: LOCAL PASS CANDIDATE ==="
echo "Leave $TARGET_CONTAINER running with archive_mode=off until evidence is reconciled."