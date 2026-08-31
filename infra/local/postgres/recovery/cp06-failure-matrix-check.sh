#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd -- "${SCRIPT_DIR}/../../../.." && pwd)"
BRANCH="feature/postgres-recovery"
IMAGE="dante-postgres-recovery:18.6-pgbackrest-2.59.1"
REAL_REPOVOL="dante-postgres-recovery_pgbackrest-repository"
CP05_TARGET="dante-postgres-recovery-cp05-pitr"
SCENARIO_FILE="infra/compose/secrets/postgres_recovery_cp05_scenario.local"
CURRENT_HEAD="20260830_09"
CURRENT_TOPOLOGY="69|5|15|76|97|69|123|0|0|0"

RUN_ID="cp06-failure-$(date -u +%Y%m%dT%H%M%SZ)-$$"
EMPTY_REPOVOL="${RUN_ID}-empty-repo"
INVALIDSET_PGVOL="${RUN_ID}-invalidset-pg"
IMPOSSIBLE_PGVOL="${RUN_ID}-impossible-pg"
IMPOSSIBLE_CONTAINER="${RUN_ID}-impossible"
MISSING_REPOVOL="${RUN_ID}-missingwal-repo"
MISSING_PGVOL="${RUN_ID}-missingwal-pg"
MISSING_CONTAINER="${RUN_ID}-missingwal"
CORRUPT_REPOVOL="${RUN_ID}-corrupt-repo"
CORRUPT_PGVOL="${RUN_ID}-corrupt-pg"
STALE_PGVOL="${RUN_ID}-stale-pg"
STALE_CONTAINER="${RUN_ID}-stale"
TMPDIR="$(mktemp -d)"

cleanup() {
  set +e
  docker rm -f "$IMPOSSIBLE_CONTAINER" "$MISSING_CONTAINER" "$STALE_CONTAINER" >/dev/null 2>&1 || true
  docker volume rm \
    "$EMPTY_REPOVOL" "$INVALIDSET_PGVOL" "$IMPOSSIBLE_PGVOL" \
    "$MISSING_REPOVOL" "$MISSING_PGVOL" \
    "$CORRUPT_REPOVOL" "$CORRUPT_PGVOL" \
    "$STALE_PGVOL" >/dev/null 2>&1 || true
  rm -rf "$TMPDIR"
}
trap cleanup EXIT

die() {
  echo
  echo "FAIL: $*" >&2
  exit 1
}

headline() {
  echo
  echo "================================================================"
  echo "$*"
  echo "================================================================"
}

create_volume() {
  docker volume create "$1" >/dev/null
}

clone_repo() {
  local destination="$1"
  create_volume "$destination"
  docker run --rm \
    --entrypoint sh \
    -v "${REAL_REPOVOL}:/source:ro" \
    -v "${destination}:/dest" \
    "$IMAGE" \
    -lc 'set -eu; cp -a /source/. /dest/'
}

restore_to_volume() {
  local pgvol="$1"
  local repovol="$2"
  shift 2
  docker run --rm \
    --user root \
    --entrypoint /usr/bin/pgbackrest \
    -v "${pgvol}:/var/lib/postgresql" \
    -v "${repovol}:/var/lib/pgbackrest:ro" \
    "$IMAGE" \
    --stanza=dante \
    --pg1-path=/var/lib/postgresql/18/docker \
    --repo1-path=/var/lib/pgbackrest \
    "$@" restore
}

normalize_pg18_parent() {
  local volume="$1"
  docker run --rm --entrypoint sh -v "${volume}:/var/lib/postgresql" "$IMAGE" -lc '
    set -eu
    test -d /var/lib/postgresql/18/docker
    chown postgres:postgres /var/lib/postgresql/18
    chmod 0700 /var/lib/postgresql/18
  '
}

pg_control_absent() {
  local volume="$1"
  test "$(docker run --rm --entrypoint sh -v "${volume}:/var/lib/postgresql:ro" "$IMAGE" -lc 'if [ -e /var/lib/postgresql/18/docker/global/pg_control ]; then echo present; else echo absent; fi')" = "absent"
}

start_restored_container() {
  local container="$1"
  local pgvol="$2"
  local repovol="$3"
  docker run -d \
    --name "$container" \
    -v "${pgvol}:/var/lib/postgresql" \
    -v "${repovol}:/var/lib/pgbackrest:ro" \
    "$IMAGE" \
    postgres -c shared_preload_libraries=pg_stat_statements -c compute_query_id=on >/dev/null
}

expect_container_failure() {
  local container="$1"
  local log_file="$2"
  local max_seconds="${3:-90}"
  for _ in $(seq 1 "$max_seconds"); do
    status="$(docker inspect "$container" --format '{{.State.Status}}' 2>/dev/null || true)"
    if [ "$status" = "exited" ] || [ "$status" = "dead" ]; then
      docker logs "$container" >"$log_file" 2>&1 || true
      exit_code="$(docker inspect "$container" --format '{{.State.ExitCode}}')"
      test "$exit_code" != "0" || die "$container exited successfully when failure was expected"
      return 0
    fi
    sleep 1
  done
  docker logs "$container" >"$log_file" 2>&1 || true
  return 1
}

wait_promoted() {
  local container="$1"
  for _ in $(seq 1 90); do
    status="$(docker inspect "$container" --format '{{.State.Status}}' 2>/dev/null || true)"
    [ "$status" = "exited" ] && { docker logs "$container" || true; return 1; }
    state="$(docker exec --user postgres "$container" psql -X -d dante -Atqc 'SELECT pg_is_in_recovery();' 2>/dev/null || true)"
    [ "$state" = "f" ] && return 0
    sleep 1
  done
  return 1
}

cd "$REPO_ROOT"
echo "=== DANTE CP06 — VERSIONED FAILURE-INJECTION MATRIX ==="

test "$(git branch --show-current)" = "$BRANCH" || die "wrong Git branch"
test "$(git rev-parse HEAD)" = "$(git rev-parse origin/$BRANCH)" || die "local HEAD differs from origin"
test -z "$(git status --porcelain)" || die "worktree is not clean"
docker image inspect "$IMAGE" >/dev/null 2>&1 || die "missing image $IMAGE"
docker volume inspect "$REAL_REPOVOL" >/dev/null 2>&1 || die "missing real pgBackRest repository"
test -s "$SCENARIO_FILE" || die "missing $SCENARIO_FILE"
git check-ignore -q "$SCENARIO_FILE" || die "$SCENARIO_FILE is not ignored"

# shellcheck disable=SC1090
source "$SCENARIO_FILE"
: "${BASE_BACKUP:?missing BASE_BACKUP}"
: "${TARGET_TIMELINE:?missing TARGET_TIMELINE}"
: "${RESTORE_POINT:?missing RESTORE_POINT}"
: "${RESTORE_WAL:?missing RESTORE_WAL}"
: "${A_REF:?missing A_REF}"
: "${B_REF:?missing B_REF}"

repo_hash_before="$(docker run --rm --entrypoint sha256sum -v "${REAL_REPOVOL}:/var/lib/pgbackrest:ro" "$IMAGE" /var/lib/pgbackrest/backup/dante/backup.info | awk '{print $1}')"
cp05_state_before="$(docker exec --user postgres "$CP05_TARGET" psql -X -d dante -Atqc "SELECT current_setting('server_version_num'),pg_is_in_recovery(),current_setting('archive_mode'),(SELECT count(*) FROM dante.person WHERE person_ref='${A_REF}'::uuid),(SELECT count(*) FROM dante.person WHERE person_ref='${B_REF}'::uuid);" 2>/dev/null || true)"
test "$cp05_state_before" = "180006|f|off|1|0" || die "unexpected CP05 target state=$cp05_state_before"

echo "REAL repository is read-only for all negative scenarios"

headline "N1 — WRONG STANZA"
N1_LOG="$TMPDIR/n1.log"
set +e
docker run --rm --user postgres --entrypoint /usr/bin/pgbackrest \
  -v "${REAL_REPOVOL}:/var/lib/pgbackrest:ro" "$IMAGE" \
  --stanza=dante_does_not_exist --repo1-path=/var/lib/pgbackrest info >"$N1_LOG" 2>&1
n1_rc=$?
set -e
cat "$N1_LOG"
if grep -Eiq 'DbConnectError|no database found|/var/run/postgresql' "$N1_LOG"; then die "N1 failed for DB connectivity rather than stanza/repository"; fi
if grep -Eiq 'status:[[:space:]]*ok' "$N1_LOG"; then die "wrong stanza reported status ok"; fi
if [ "$n1_rc" -eq 0 ] && ! grep -Eiq 'error|missing|stanza|does not exist|invalid|unable' "$N1_LOG"; then die "N1 did not expose a clear negative result"; fi
echo "N1 WRONG STANZA: PASS"

headline "N2 — EMPTY REPOSITORY"
create_volume "$EMPTY_REPOVOL"
N2_LOG="$TMPDIR/n2.log"
set +e
docker run --rm --user postgres --entrypoint /usr/bin/pgbackrest \
  -v "${EMPTY_REPOVOL}:/var/lib/pgbackrest:ro" "$IMAGE" \
  --stanza=dante --repo1-path=/var/lib/pgbackrest info >"$N2_LOG" 2>&1
n2_rc=$?
set -e
cat "$N2_LOG"
if grep -Eiq 'DbConnectError|no database found|/var/run/postgresql' "$N2_LOG"; then die "N2 failed for DB connectivity rather than repository"; fi
if grep -Eiq 'status:[[:space:]]*ok' "$N2_LOG"; then die "empty repository reported status ok"; fi
if [ "$n2_rc" -eq 0 ] && ! grep -Eiq 'error|missing|stanza|archive.info|backup.info|repository|unable|does not exist' "$N2_LOG"; then die "N2 did not expose a clear negative result"; fi
echo "N2 EMPTY REPOSITORY: PASS"

headline "N3 — NON-EXISTENT BACKUP SET"
create_volume "$INVALIDSET_PGVOL"
N3_LOG="$TMPDIR/n3.log"
set +e
restore_to_volume "$INVALIDSET_PGVOL" "$REAL_REPOVOL" --set=20990101-000000F --archive-mode=off --log-level-console=info >"$N3_LOG" 2>&1
n3_rc=$?
set -e
cat "$N3_LOG"
test "$n3_rc" -ne 0 || die "invalid backup set restored"
pg_control_absent "$INVALIDSET_PGVOL" || die "aborted invalid-set restore left bootable pg_control"
echo "N3 INVALID BACKUP SET FAIL-CLOSED: PASS"

headline "N4 — IMPOSSIBLE PITR TARGET"
create_volume "$IMPOSSIBLE_PGVOL"
IMPOSSIBLE_TARGET="${RUN_ID}_RESTORE_POINT_DOES_NOT_EXIST"
restore_to_volume "$IMPOSSIBLE_PGVOL" "$REAL_REPOVOL" \
  --set="$BASE_BACKUP" --type=name --target="$IMPOSSIBLE_TARGET" \
  --target-timeline="$TARGET_TIMELINE" --target-action=promote \
  --archive-mode=off --log-level-console=info
normalize_pg18_parent "$IMPOSSIBLE_PGVOL"
start_restored_container "$IMPOSSIBLE_CONTAINER" "$IMPOSSIBLE_PGVOL" "$REAL_REPOVOL"
N4_LOG="$TMPDIR/n4.log"
expect_container_failure "$IMPOSSIBLE_CONTAINER" "$N4_LOG" 90 || { cat "$N4_LOG"; die "impossible PITR target did not fail closed"; }
cat "$N4_LOG"
grep -Eiq 'recovery ended before configured recovery target was reached|recovery target|restore point|fatal|could not restore file|archive-get' "$N4_LOG" || die "N4 diagnostics unclear"
echo "N4 IMPOSSIBLE PITR TARGET FAIL-CLOSED: PASS"

headline "N5 — MISSING REQUIRED WAL ON CLONED REPOSITORY"
clone_repo "$MISSING_REPOVOL"
missing_match="$(docker run --rm --entrypoint sh -v "${MISSING_REPOVOL}:/repo:ro" "$IMAGE" -lc "find /repo/archive/dante -type f -name '${RESTORE_WAL}-*' -print -quit")"
test -n "$missing_match" || die "cannot locate required WAL in cloned repository"
docker run --rm --entrypoint sh -v "${MISSING_REPOVOL}:/repo" "$IMAGE" -lc "rm -f '$missing_match'"
create_volume "$MISSING_PGVOL"
restore_to_volume "$MISSING_PGVOL" "$MISSING_REPOVOL" \
  --set="$BASE_BACKUP" --type=name --target="$RESTORE_POINT" \
  --target-timeline="$TARGET_TIMELINE" --target-action=promote \
  --archive-mode=off --log-level-console=info
normalize_pg18_parent "$MISSING_PGVOL"
start_restored_container "$MISSING_CONTAINER" "$MISSING_PGVOL" "$MISSING_REPOVOL"
N5_LOG="$TMPDIR/n5.log"
expect_container_failure "$MISSING_CONTAINER" "$N5_LOG" 90 || { cat "$N5_LOG"; die "missing-WAL target did not fail closed"; }
cat "$N5_LOG"
grep -Eiq "${RESTORE_WAL}|archive-get|could not restore file|recovery ended before configured recovery target was reached|fatal" "$N5_LOG" || die "N5 diagnostics unclear"
echo "N5 MISSING REQUIRED WAL FAIL-CLOSED: PASS"

headline "N6 — CORRUPTED BACKUP ARTIFACT ON CLONE"
clone_repo "$CORRUPT_REPOVOL"
corrupt_candidate="$(docker run --rm --entrypoint sh -v "${CORRUPT_REPOVOL}:/repo:ro" "$IMAGE" -lc "find '/repo/backup/dante/${BASE_BACKUP}' -type f ! -name 'backup.manifest' ! -name 'backup.manifest.copy' -printf '%s %p\n' 2>/dev/null | sort -nr | head -n 1 | cut -d' ' -f2-")"
test -n "$corrupt_candidate" || die "no backup artifact candidate found"
docker run --rm --entrypoint sh -v "${CORRUPT_REPOVOL}:/repo" "$IMAGE" -lc "printf 'CP06_CORRUPTED_CLONE\n' > '$corrupt_candidate'"
create_volume "$CORRUPT_PGVOL"
N6_LOG="$TMPDIR/n6.log"
set +e
restore_to_volume "$CORRUPT_PGVOL" "$CORRUPT_REPOVOL" --set="$BASE_BACKUP" --archive-mode=off --log-level-console=info >"$N6_LOG" 2>&1
n6_rc=$?
set -e
cat "$N6_LOG"
test "$n6_rc" -ne 0 || die "corrupted artifact restored successfully"
pg_control_absent "$CORRUPT_PGVOL" || die "aborted corrupt restore left bootable pg_control"
echo "N6 CORRUPTED ARTIFACT FAIL-CLOSED: PASS"

headline "N7 — BOOTABLE STALE DATABASE MUST FAIL CURRENT ACCEPTANCE"
create_volume "$STALE_PGVOL"
restore_to_volume "$STALE_PGVOL" "$REAL_REPOVOL" \
  --set="$BASE_BACKUP" --type=immediate --target-action=promote \
  --archive-mode=off --log-level-console=info
normalize_pg18_parent "$STALE_PGVOL"
start_restored_container "$STALE_CONTAINER" "$STALE_PGVOL" "$REAL_REPOVOL"
wait_promoted "$STALE_CONTAINER" || { docker logs "$STALE_CONTAINER" || true; die "stale physical target did not become bootable/promoted"; }

stale_runtime="$(docker exec --user postgres "$STALE_CONTAINER" psql -X -d dante -Atqc "SELECT current_setting('server_version_num'),pg_is_in_recovery(),current_setting('archive_mode');")"
echo "STALE TARGET RUNTIME: $stale_runtime"
test "$stale_runtime" = "180006|f|off" || die "unexpected stale runtime=$stale_runtime"

stale_head="$(docker exec --user postgres "$STALE_CONTAINER" psql -X -d dante -Atqc "SELECT CASE WHEN to_regclass('dante.alembic_version') IS NULL THEN 'ABSENT' ELSE (SELECT version_num FROM dante.alembic_version LIMIT 1) END;" 2>/dev/null || echo ABSENT)"
stale_retirement="$(docker exec --user postgres "$STALE_CONTAINER" psql -X -d dante -Atqc "SELECT to_regclass('dante.material_state_retirement') IS NOT NULL;" 2>/dev/null || echo f)"
echo "STALE TARGET ALEMBIC: $stale_head"
echo "STALE TARGET material_state_retirement: $stale_retirement"

if [ "$stale_head" = "$CURRENT_HEAD" ] && [ "$stale_retirement" = "t" ]; then
  stale_topology="$(docker exec --user postgres "$STALE_CONTAINER" psql -X -d dante -Atqc "SELECT (SELECT count(*) FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace WHERE n.nspname='dante' AND c.relkind='r' AND c.relname<>'alembic_version'),(SELECT count(*) FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace WHERE n.nspname='dante' AND c.relkind='v'),(SELECT count(*) FROM pg_proc p JOIN pg_namespace n ON n.oid=p.pronamespace WHERE n.nspname='dante'),(SELECT count(*) FROM pg_trigger t JOIN pg_class c ON c.oid=t.tgrelid JOIN pg_namespace n ON n.oid=c.relnamespace WHERE n.nspname='dante' AND NOT t.tgisinternal),(SELECT count(*) FROM pg_index i JOIN pg_class c ON c.oid=i.indrelid JOIN pg_namespace n ON n.oid=c.relnamespace WHERE n.nspname='dante' AND c.relname<>'alembic_version'),(SELECT count(*) FROM pg_constraint c JOIN pg_namespace n ON n.oid=c.connamespace WHERE n.nspname='dante' AND c.contype='f'),(SELECT count(*) FROM pg_constraint c JOIN pg_namespace n ON n.oid=c.connamespace WHERE n.nspname='dante' AND c.contype='c'),(SELECT count(*) FROM pg_type t JOIN pg_namespace n ON n.oid=t.typnamespace WHERE n.nspname='dante' AND t.typtype IN ('d','e')),(SELECT count(*) FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace WHERE n.nspname='dante' AND c.relkind IN ('S','m','p')),(SELECT count(*) FROM pg_policy p JOIN pg_class c ON c.oid=p.polrelid JOIN pg_namespace n ON n.oid=c.relnamespace WHERE n.nspname='dante');")"
  test "$stale_topology" != "$CURRENT_TOPOLOGY" || die "selected BASE_BACKUP is no longer stale enough to prove N7"
fi

echo "N7 BOOTABLE STALE TARGET REJECTED BY CURRENT CONTRACT: PASS"

headline "FINAL NON-INTERFERENCE"
repo_hash_after="$(docker run --rm --entrypoint sha256sum -v "${REAL_REPOVOL}:/var/lib/pgbackrest:ro" "$IMAGE" /var/lib/pgbackrest/backup/dante/backup.info | awk '{print $1}')"
test "$repo_hash_after" = "$repo_hash_before" || die "real repository metadata changed"
cp05_state_after="$(docker exec --user postgres "$CP05_TARGET" psql -X -d dante -Atqc "SELECT current_setting('server_version_num'),pg_is_in_recovery(),current_setting('archive_mode'),(SELECT count(*) FROM dante.person WHERE person_ref='${A_REF}'::uuid),(SELECT count(*) FROM dante.person WHERE person_ref='${B_REF}'::uuid);" 2>/dev/null || true)"
test "$cp05_state_after" = "$cp05_state_before" || die "CP05 target changed"
test -z "$(git status --porcelain)" || die "Git worktree changed"

echo
echo "N1 wrong stanza                              PASS"
echo "N2 empty/unavailable repository              PASS"
echo "N3 invalid backup set / no bootable PGDATA  PASS"
echo "N4 impossible PITR target fail-closed       PASS"
echo "N5 missing required WAL fail-closed         PASS"
echo "N6 corrupted cloned artifact fail-closed    PASS"
echo "N7 bootable stale target rejected            PASS"
echo "real recovery repository untouched          PASS"
echo "CP05 isolated target untouched              PASS"
echo "Git worktree untouched                      PASS"
echo
echo "READINESS FINDING: pg_isready/read-only readiness is not a traffic-open gate."
echo "=== CP06 FAILURE MATRIX: LOCAL PASS CANDIDATE ==="