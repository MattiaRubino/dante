#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd -- "${SCRIPT_DIR}/../../../.." && pwd)"
PROJECT="dante-postgres-recovery"
BASE="infra/compose/local.yaml"
OVERLAY="infra/compose/postgres-recovery.override.yaml"
ADMIN_SECRET="infra/compose/secrets/postgres_password.local"
MIGRATOR_SECRET="infra/compose/secrets/postgres_recovery_migrator_password.local"
RUNTIME_SECRET="infra/compose/secrets/postgres_recovery_runtime_password.local"
BACKUP_LABEL_FILE="infra/compose/secrets/postgres_recovery_cp04_backup_label.local"
FIXTURE_REF="01993f19-9c00-7000-8000-000000000001"
EXPECTED_HEAD="20260826_08"
EXPECTED_TOPOLOGY="68|5|14|75|95|68|120|0|0|0"

cd "$REPO_ROOT"

compose() {
  docker compose -p "$PROJECT" -f "$BASE" -f "$OVERLAY" "$@"
}

die() {
  echo "FAIL: $*" >&2
  exit 1
}

generate_secret() {
  python3 - <<'PY'
import secrets
print(secrets.token_urlsafe(32))
PY
}

echo "=== DANTE CP04 — materialize canonical database + dedicated FULL ==="

test "$(git branch --show-current)" = "feature/postgres-recovery" || die "wrong Git branch"
test "$(git rev-parse HEAD)" = "$(git rev-parse origin/feature/postgres-recovery)" || die "local HEAD differs from origin"
test -z "$(git status --porcelain)" || die "worktree is not clean"
test -f "$ADMIN_SECRET" || die "missing $ADMIN_SECRET"

compose ps
mkdir -p infra/compose/secrets
umask 077

[ -s "$MIGRATOR_SECRET" ] || generate_secret > "$MIGRATOR_SECRET"
[ -s "$RUNTIME_SECRET" ] || generate_secret > "$RUNTIME_SECRET"
chmod 600 "$MIGRATOR_SECRET" "$RUNTIME_SECRET"

for secret_path in "$MIGRATOR_SECRET" "$RUNTIME_SECRET" "$BACKUP_LABEL_FILE"; do
  git check-ignore -q "$secret_path" || die "$secret_path is not ignored by Git"
done

export DANTE_DATABASE__HOST="127.0.0.1"
export DANTE_DATABASE__PORT="55432"
export DANTE_DATABASE__NAME="dante"
export DANTE_ADMIN__USER="postgres"
export DANTE_ADMIN__PASSWORD="$(cat "$ADMIN_SECRET")"
export DANTE_MIGRATOR__PASSWORD="$(cat "$MIGRATOR_SECRET")"
export DANTE_RUNTIME__PASSWORD="$(cat "$RUNTIME_SECRET")"

cd "$REPO_ROOT/apps/backend"
uv --version
uv run --frozen python -m dante.platform.database.provisioning
uv run --frozen alembic upgrade head
uv run --frozen python -m dante.platform.database.provisioning
uv run --frozen alembic current
uv run --frozen alembic check
cd "$REPO_ROOT"

echo "=== Seed deterministic canonical Person fixture ==="
compose exec --user postgres postgres psql -X -v ON_ERROR_STOP=1 -d dante -P pager=off -c "
  SELECT uuid_extract_version('${FIXTURE_REF}'::uuid) AS fixture_uuid_version;
  SET ROLE dante_owner;
  INSERT INTO dante.person(person_ref)
  VALUES ('${FIXTURE_REF}'::uuid)
  ON CONFLICT (person_ref) DO NOTHING;
  RESET ROLE;
  SELECT person_ref FROM dante.person WHERE person_ref='${FIXTURE_REF}'::uuid;
"

fixture_count="$(compose exec -T --user postgres postgres psql -X -d dante -Atqc "SELECT count(*) FROM dante.person WHERE person_ref='${FIXTURE_REF}'::uuid;")"
test "$fixture_count" = "1" || die "fixture not materialized exactly once"

head="$(compose exec -T --user postgres postgres psql -X -d dante -Atqc "SELECT version_num FROM dante.alembic_version;")"
test "$head" = "$EXPECTED_HEAD" || die "Alembic head=$head"

topology="$(compose exec -T --user postgres postgres psql -X -d dante -Atqc "
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

owners="$(compose exec -T --user postgres postgres psql -X -d dante -Atqc "SELECT string_agg(owner, ',' ORDER BY owner) FROM (SELECT DISTINCT pg_get_userbyid(c.relowner) AS owner FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace WHERE n.nspname='dante' AND c.relname<>'alembic_version') x;")"
test "$owners" = "dante_owner" || die "owners=$owners"

roles="$(compose exec -T --user postgres postgres psql -X -d dante -Atqc "SELECT string_agg(rolname, ',' ORDER BY rolname) FROM pg_roles WHERE rolname IN ('dante_owner','dante_migrator','dante_runtime');")"
test "$roles" = "dante_migrator,dante_owner,dante_runtime" || die "roles=$roles"

runtime_alembic="$(compose exec -T --user postgres postgres psql -X -d dante -Atqc "SELECT has_table_privilege('dante_runtime','dante.alembic_version','SELECT');")"
test "$runtime_alembic" = "f" || die "dante_runtime can SELECT dante.alembic_version"

extensions="$(compose exec -T --user postgres postgres psql -X -d dante -Atqc "SELECT string_agg(extname || '=' || extversion, ',' ORDER BY extname) FROM pg_extension WHERE extname IN ('postgis','vector','pg_trgm','unaccent','pg_stat_statements');")"
test "$extensions" = "pg_stat_statements=1.12,pg_trgm=1.6,postgis=3.6.4,unaccent=1.1,vector=0.8.6" || die "extensions=$extensions"

echo "MATERIALIZED DATABASE ACCEPTANCE: PASS"
compose exec --user postgres postgres pgbackrest --stanza=dante check
echo "PGBACKREST CHECK: PASS"
compose exec --user postgres postgres pgbackrest --stanza=dante --type=full backup
echo "FULL BACKUP: PASS"
compose exec --user postgres postgres pgbackrest --stanza=dante info

latest_label="$(compose exec -T --user postgres postgres pgbackrest --stanza=dante --output=json info | python3 -c 'import json,sys; data=json.load(sys.stdin); labels=[b["label"] for s in data for b in s.get("backup",[])]; print(max(labels))')"
printf '%s\n' "$latest_label" > "$BACKUP_LABEL_FILE"
chmod 600 "$BACKUP_LABEL_FILE"

test -z "$(git status --porcelain)" || die "tracked/unignored worktree changes appeared"

echo "CP04 BACKUP LABEL: $latest_label"
echo "CP04 FIXTURE REF:  $FIXTURE_REF"
echo "=== CP04 MATERIALIZATION + BACKUP COMPLETE — NO PGDATA DELETED ==="