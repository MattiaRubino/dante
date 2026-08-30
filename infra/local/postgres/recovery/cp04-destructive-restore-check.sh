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
TEST_CONTAINER="dante-postgres-recovery-cp04-restore"
BACKUP_LABEL_FILE="infra/compose/secrets/postgres_recovery_cp04_backup_label.local"
RUNTIME_SECRET="infra/compose/secrets/postgres_recovery_runtime_password.local"
FIXTURE_REF="01993f19-9c00-7000-8000-000000000001"
EXPECTED_ALEMBIC="20260830_09"
EXPECTED_TOPOLOGY="69|5|15|76|97|69|123|0|0|0"
SOURCE_MARKER="/var/lib/postgresql/CP04_SOURCE_VOLUME_MUST_NOT_SURVIVE"

cd "$REPO_ROOT"

compose() {
  docker compose -p "$PROJECT" -f "$BASE" -f "$OVERLAY" "$@"
}

die() {
  echo "FAIL: $*" >&2
  echo "The pgBackRest repository volume is intentionally never deleted by this harness." >&2
  exit 1
}

echo "=== DANTE CP04 — destructive / isolated restore of current database ==="

test "$(git branch --show-current)" = "feature/postgres-recovery" || die "wrong Git branch"
test "$(git rev-parse HEAD)" = "$(git rev-parse origin/feature/postgres-recovery)" || die "local HEAD differs from origin"
test -z "$(git status --porcelain)" || die "worktree is not clean"
test -s "$BACKUP_LABEL_FILE" || die "missing $BACKUP_LABEL_FILE"
test -s "$RUNTIME_SECRET" || die "missing $RUNTIME_SECRET"

docker image inspect "$IMAGE" >/dev/null || die "missing image $IMAGE"
docker volume inspect "$PGVOL" >/dev/null || die "missing $PGVOL"
docker volume inspect "$REPOVOL" >/dev/null || die "missing $REPOVOL"
test "$PGVOL" != "$REPOVOL" || die "PGDATA and repository volumes unexpectedly match"

backup_label="$(cat "$BACKUP_LABEL_FILE")"
backup_found="$(compose exec -T --user postgres postgres pgbackrest --stanza=dante --output=json info | python3 -c 'import json,sys; wanted=sys.argv[1]; data=json.load(sys.stdin); labels={b["label"] for s in data for b in s.get("backup",[])}; print("yes" if wanted in labels else "no")' "$backup_label")"
test "$backup_found" = "yes" || die "backup $backup_label not present"

fixture_before="$(compose exec -T --user postgres postgres psql -X -d dante -Atqc "SELECT count(*) FROM dante.person WHERE person_ref='${FIXTURE_REF}'::uuid;")"
test "$fixture_before" = "1" || die "canonical fixture missing before destruction"

source_head="$(compose exec -T --user postgres postgres psql -X -d dante -Atqc "SELECT version_num FROM dante.alembic_version;")"
test "$source_head" = "$EXPECTED_ALEMBIC" || die "source Alembic=$source_head expected=$EXPECTED_ALEMBIC"

repo_hash_before="$(compose exec -T --user postgres postgres sha256sum /var/lib/pgbackrest/backup/dante/backup.info | awk '{print $1}')"
test -n "$repo_hash_before" || die "cannot hash repository metadata"

marker_token="cp04-$(date -u +%Y%m%dT%H%M%SZ)-$$"
compose exec --user root postgres sh -lc "printf '%s\n' '$marker_token' > '$SOURCE_MARKER'"
test "$(compose exec -T --user root postgres cat "$SOURCE_MARKER")" = "$marker_token" || die "cannot verify source-volume marker"

echo "Backup:            $backup_label"
echo "Fixture:           $FIXTURE_REF"
echo "PGDATA volume:     $PGVOL"
echo "Repository volume: $REPOVOL"
echo "Source marker:     $marker_token"
echo
echo "THIS WILL DELETE ONLY: $PGVOL"
echo "THIS WILL NOT DELETE:  $REPOVOL"
printf 'Type DELETE_RECOVERY_PGDATA to continue: '
read -r confirmation
test "$confirmation" = "DELETE_RECOVERY_PGDATA" || die "destructive confirmation not provided"

compose stop postgres
compose rm -f postgres
if docker ps -aq --filter "volume=$PGVOL" | grep -q .; then
  docker ps -a --filter "volume=$PGVOL"
  die "a container still references $PGVOL"
fi

docker volume rm "$PGVOL"
echo "PGDATA VOLUME DELETED: PASS"
docker volume inspect "$REPOVOL" >/dev/null || die "repository volume disappeared"

repo_hash_after_delete="$(docker run --rm --entrypoint sha256sum -v "${REPOVOL}:/var/lib/pgbackrest:ro" "$IMAGE" /var/lib/pgbackrest/backup/dante/backup.info | awk '{print $1}')"
test "$repo_hash_after_delete" = "$repo_hash_before" || die "repository metadata changed during PGDATA deletion"
echo "REPOSITORY SURVIVED PGDATA DELETION: PASS"

compose create postgres
compose rm -f postgres
docker volume inspect "$PGVOL" >/dev/null || die "Compose did not recreate $PGVOL"

marker_after_recreate="$(docker run --rm --entrypoint sh -v "${PGVOL}:/var/lib/postgresql" "$IMAGE" -lc "if [ -e '$SOURCE_MARKER' ]; then echo present; else echo absent; fi")"
test "$marker_after_recreate" = "absent" || die "old source-volume marker survived volume replacement"
echo "OLD SOURCE VOLUME ABSENCE: PASS"

compose run --rm --no-deps --user root --entrypoint /usr/bin/pgbackrest postgres --stanza=dante --set="$backup_label" --archive-mode=off --log-level-console=info restore
echo "PGBACKREST RESTORE COMMAND: PASS"

docker run --rm --entrypoint sh -v "${PGVOL}:/var/lib/postgresql" "$IMAGE" -lc '
  set -eu
  chown postgres:postgres /var/lib/postgresql/18
  chmod 0700 /var/lib/postgresql/18
  stat -c "%U:%G %u:%g %a %n" /var/lib/postgresql /var/lib/postgresql/18 /var/lib/postgresql/18/docker
'
parent_state="$(docker run --rm --entrypoint stat -v "${PGVOL}:/var/lib/postgresql:ro" "$IMAGE" -c '%U:%G %a' /var/lib/postgresql/18)"
test "$parent_state" = "postgres:postgres 700" || die "unexpected restored parent state: $parent_state"
echo "RESTORE PARENT PERMISSIONS: PASS"

restored_pg_version="$(docker run --rm --entrypoint cat -v "${PGVOL}:/var/lib/postgresql:ro" "$IMAGE" /var/lib/postgresql/18/docker/PG_VERSION)"
test "$restored_pg_version" = "18" || die "restored PG_VERSION=$restored_pg_version"
marker_after_restore="$(docker run --rm --entrypoint sh -v "${PGVOL}:/var/lib/postgresql:ro" "$IMAGE" -lc "if [ -e '$SOURCE_MARKER' ]; then echo present; else echo absent; fi")"
test "$marker_after_restore" = "absent" || die "old marker exists after restore"

docker rm -f "$TEST_CONTAINER" >/dev/null 2>&1 || true
restore_container_id="$(compose run -d --service-ports --name "$TEST_CONTAINER" postgres postgres -c shared_preload_libraries=pg_stat_statements -c compute_query_id=on)"
test -n "$restore_container_id" || die "restore target did not start"

ready=0
for _ in $(seq 1 60); do
  if docker exec "$TEST_CONTAINER" pg_isready -h 127.0.0.1 -p 5432 -U postgres -d dante >/dev/null 2>&1; then
    ready=1
    break
  fi
  sleep 1
done
[ "$ready" = "1" ] || { docker logs "$TEST_CONTAINER"; die "restored PostgreSQL did not become ready"; }

recovery_done=0
for _ in $(seq 1 60); do
  in_recovery="$(docker exec --user postgres "$TEST_CONTAINER" psql -X -d dante -Atqc "SELECT pg_is_in_recovery();" 2>/dev/null || true)"
  if [ "$in_recovery" = "f" ]; then
    recovery_done=1
    break
  fi
  sleep 1
done
[ "$recovery_done" = "1" ] || { docker logs "$TEST_CONTAINER"; die "restored PostgreSQL did not finish recovery"; }
echo "RESTORED POSTGRESQL READY / NOT IN RECOVERY: PASS"

archive_mode="$(docker exec --user postgres "$TEST_CONTAINER" psql -X -d dante -Atqc "SHOW archive_mode;")"
test "$archive_mode" = "off" || die "archive_mode=$archive_mode"
server_version="$(docker exec --user postgres "$TEST_CONTAINER" psql -X -d dante -Atqc "SELECT current_setting('server_version_num');")"
test "$server_version" = "180006" || die "server_version_num=$server_version"
alembic_head="$(docker exec --user postgres "$TEST_CONTAINER" psql -X -d dante -Atqc "SELECT version_num FROM dante.alembic_version;")"
test "$alembic_head" = "$EXPECTED_ALEMBIC" || die "Alembic=$alembic_head"

topology="$(docker exec --user postgres "$TEST_CONTAINER" psql -X -d dante -Atqc "
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

fixture_after="$(docker exec --user postgres "$TEST_CONTAINER" psql -X -d dante -Atqc "SELECT count(*) FROM dante.person WHERE person_ref='${FIXTURE_REF}'::uuid;")"
test "$fixture_after" = "1" || die "canonical fixture not restored exactly once"
retirement_table="$(docker exec --user postgres "$TEST_CONTAINER" psql -X -d dante -Atqc "SELECT to_regclass('dante.material_state_retirement') IS NOT NULL;")"
test "$retirement_table" = "t" || die "current retirement table missing after restore"
runtime_retirement="$(docker exec --user postgres "$TEST_CONTAINER" psql -X -d dante -Atqc "SELECT has_table_privilege('dante_runtime','dante.material_state_retirement','SELECT')::text || '|' || has_table_privilege('dante_runtime','dante.material_state_retirement','INSERT')::text || '|' || has_table_privilege('dante_runtime','dante.material_state_retirement','UPDATE')::text || '|' || has_table_privilege('dante_runtime','dante.material_state_retirement','DELETE')::text;")"
test "$runtime_retirement" = "true|false|false|false" || die "unexpected runtime retirement ACL=$runtime_retirement"
owners="$(docker exec --user postgres "$TEST_CONTAINER" psql -X -d dante -Atqc "SELECT string_agg(owner, ',' ORDER BY owner) FROM (SELECT DISTINCT pg_get_userbyid(c.relowner) AS owner FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace WHERE n.nspname='dante' AND c.relname<>'alembic_version') x;")"
test "$owners" = "dante_owner" || die "owners=$owners"
roles="$(docker exec --user postgres "$TEST_CONTAINER" psql -X -d dante -Atqc "SELECT string_agg(rolname, ',' ORDER BY rolname) FROM pg_roles WHERE rolname IN ('dante_owner','dante_migrator','dante_runtime');")"
test "$roles" = "dante_migrator,dante_owner,dante_runtime" || die "roles=$roles"
runtime_alembic="$(docker exec --user postgres "$TEST_CONTAINER" psql -X -d dante -Atqc "SELECT has_table_privilege('dante_runtime','dante.alembic_version','SELECT');")"
test "$runtime_alembic" = "f" || die "runtime can SELECT alembic_version"
extensions="$(docker exec --user postgres "$TEST_CONTAINER" psql -X -d dante -Atqc "SELECT string_agg(extname || '=' || extversion, ',' ORDER BY extname) FROM pg_extension WHERE extname IN ('postgis','vector','pg_trgm','unaccent','pg_stat_statements');")"
test "$extensions" = "pg_stat_statements=1.12,pg_trgm=1.6,postgis=3.6.4,unaccent=1.1,vector=0.8.6" || die "extensions=$extensions"
repo_hash_after_restore="$(docker exec --user postgres "$TEST_CONTAINER" sha256sum /var/lib/pgbackrest/backup/dante/backup.info | awk '{print $1}')"
test "$repo_hash_after_restore" = "$repo_hash_before" || die "repository metadata hash changed during restore"

runtime_fixture="$(docker exec -e PGPASSWORD="$(cat "$RUNTIME_SECRET")" "$TEST_CONTAINER" psql -X -h 127.0.0.1 -p 5432 -U dante_runtime -d dante -Atqc "SELECT person_ref FROM dante.person WHERE person_ref='${FIXTURE_REF}'::uuid;")"
test "$runtime_fixture" = "$FIXTURE_REF" || die "dante_runtime cannot read restored fixture"

echo "PGDATA destructive replacement            PASS"
echo "old source-volume marker absent          PASS"
echo "repository survived unchanged            PASS"
echo "pgBackRest exact-set restore             PASS"
echo "restore parent permission normalization  PASS"
echo "PostgreSQL 18.6                          PASS"
echo "archive_mode off on isolated target      PASS"
echo "pg_is_in_recovery=false                  PASS"
echo "Alembic $EXPECTED_ALEMBIC                PASS"
echo "topology $EXPECTED_TOPOLOGY              PASS"
echo "material_state_retirement + runtime ACL  PASS"
echo "canonical Person fixture                 PASS"
echo "DANTE owners / roles / ACL               PASS"
echo "required extensions                      PASS"
echo "dante_runtime restored login/read path   PASS"
echo "=== CP04 DESTRUCTIVE / ISOLATED RESTORE: LOCAL PASS CANDIDATE ==="
echo "Leave $TEST_CONTAINER running with archive_mode=off until evidence is reconciled."