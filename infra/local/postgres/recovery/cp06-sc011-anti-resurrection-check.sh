#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd -- "${SCRIPT_DIR}/../../../.." && pwd)"
BRANCH="feature/postgres-recovery"
IMAGE="dante-postgres-recovery:18.6-pgbackrest-2.59.1"
REAL_REPOVOL="dante-postgres-recovery_pgbackrest-repository"
CP05_TARGET="dante-postgres-recovery-cp05-pitr"
CP05_SCENARIO="infra/compose/secrets/postgres_recovery_cp05_scenario.local"
MIGRATOR_SECRET="infra/compose/secrets/postgres_recovery_migrator_password.local"
RUNTIME_SECRET="infra/compose/secrets/postgres_recovery_runtime_password.local"
ADMIN_SECRET="infra/compose/secrets/postgres_password.local"
EXPECTED_HEAD="20260830_09"
EXPECTED_TOPOLOGY="69|5|15|76|97|69|123|0|0|0"
SOURCE_PORT="${DANTE_CP06_SC011_PORT:-55434}"

RUN_ID="cp06-sc011-$(date -u +%Y%m%dT%H%M%SZ)-$$"
SOURCE_PGVOL="${RUN_ID}-source-pg"
BACKUP_REPOVOL="${RUN_ID}-backup-repo"
LEDGER_VOL="${RUN_ID}-ledger"
BOOTSTRAP_CONTAINER="${RUN_ID}-bootstrap"
SOURCE_CONTAINER="${RUN_ID}-source"
RESTORED_CONTAINER="${RUN_ID}-restored"
TMPDIR="$(mktemp -d)"
LEDGER_BUILD="$TMPDIR/ledger-build"
LEDGER_READ="$TMPDIR/ledger-read"

cleanup() {
  set +e
  docker rm -f "$BOOTSTRAP_CONTAINER" "$SOURCE_CONTAINER" "$RESTORED_CONTAINER" >/dev/null 2>&1 || true
  docker volume rm "$SOURCE_PGVOL" "$BACKUP_REPOVOL" "$LEDGER_VOL" >/dev/null 2>&1 || true
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

normalize_pg18_parent() {
  local volume="$1"
  docker run --rm --entrypoint sh -v "${volume}:/var/lib/postgresql" "$IMAGE" -lc '
    set -eu
    test -d /var/lib/postgresql/18/docker
    chown postgres:postgres /var/lib/postgresql/18
    chmod 0700 /var/lib/postgresql/18
  '
}

wait_promoted() {
  local container="$1"
  for _ in $(seq 1 120); do
    status="$(docker inspect "$container" --format '{{.State.Status}}' 2>/dev/null || true)"
    if [ "$status" = "exited" ] || [ "$status" = "dead" ]; then
      docker logs "$container" || true
      return 1
    fi
    state="$(docker exec --user postgres "$container" psql -X -d dante -Atqc 'SELECT pg_is_in_recovery();' 2>/dev/null || true)"
    [ "$state" = "f" ] && return 0
    sleep 1
  done
  return 1
}

wait_ready_not_recovery() {
  local container="$1"
  for _ in $(seq 1 120); do
    status="$(docker inspect "$container" --format '{{.State.Status}}' 2>/dev/null || true)"
    if [ "$status" = "exited" ] || [ "$status" = "dead" ]; then
      docker logs "$container" || true
      return 1
    fi
    state="$(docker exec --user postgres "$container" psql -X -d dante -Atqc "SELECT current_setting('server_version_num') || '|' || pg_is_in_recovery()::text;" 2>/dev/null || true)"
    [ "$state" = "180006|false" ] && return 0
    sleep 1
  done
  return 1
}

copy_ledger_build_to_volume() {
  docker run --rm \
    --entrypoint sh \
    -v "${LEDGER_BUILD}:/source:ro" \
    -v "${LEDGER_VOL}:/dest" \
    "$IMAGE" \
    -lc 'set -eu; mkdir -p /dest/records; cp -a -n /source/records/. /dest/records/'
}

copy_ledger_volume_to_readback() {
  rm -rf "$LEDGER_READ"
  mkdir -p "$LEDGER_READ"
  docker run --rm \
    --entrypoint sh \
    -v "${LEDGER_VOL}:/source:ro" \
    -v "${LEDGER_READ}:/dest" \
    "$IMAGE" \
    -lc 'set -eu; cp -a /source/. /dest/'
}

cd "$REPO_ROOT"
echo "=== DANTE CP06 — SC-011 DEFINITIVE ANTI-RESURRECTION REHEARSAL ==="
echo "All database/backup/ledger mutation occurs on disposable CP06 volumes."

test "$(git branch --show-current)" = "$BRANCH" || die "wrong Git branch"
test "$(git rev-parse HEAD)" = "$(git rev-parse origin/$BRANCH)" || die "local HEAD differs from origin"
test -z "$(git status --porcelain)" || die "worktree is not clean"
docker image inspect "$IMAGE" >/dev/null 2>&1 || die "missing recovery image"
docker volume inspect "$REAL_REPOVOL" >/dev/null 2>&1 || die "missing real recovery repository"
test -s "$CP05_SCENARIO" || die "missing $CP05_SCENARIO"
test -s "$MIGRATOR_SECRET" || die "missing $MIGRATOR_SECRET"
test -s "$RUNTIME_SECRET" || die "missing $RUNTIME_SECRET"
test -s "$ADMIN_SECRET" || die "missing $ADMIN_SECRET"
for secret in "$CP05_SCENARIO" "$MIGRATOR_SECRET" "$RUNTIME_SECRET"; do git check-ignore -q "$secret" || die "$secret is not ignored"; done

# shellcheck disable=SC1090
source "$CP05_SCENARIO"
: "${BASE_BACKUP:?missing BASE_BACKUP}"
: "${A_REF:?missing A_REF}"
: "${B_REF:?missing B_REF}"

real_repo_hash_before="$(docker run --rm --entrypoint sha256sum -v "${REAL_REPOVOL}:/var/lib/pgbackrest:ro" "$IMAGE" /var/lib/pgbackrest/backup/dante/backup.info | awk '{print $1}')"
cp05_state_before="$(docker exec --user postgres "$CP05_TARGET" psql -X -d dante -Atqc "SELECT current_setting('server_version_num'),pg_is_in_recovery(),current_setting('archive_mode'),(SELECT count(*) FROM dante.person WHERE person_ref='${A_REF}'::uuid),(SELECT count(*) FROM dante.person WHERE person_ref='${B_REF}'::uuid);" 2>/dev/null || true)"
test "$cp05_state_before" = "180006|f|off|1|0" || die "unexpected CP05 target state=$cp05_state_before"

create_volume "$SOURCE_PGVOL"
create_volume "$BACKUP_REPOVOL"
create_volume "$LEDGER_VOL"

headline "S1 — BOOTSTRAP DISPOSABLE SOURCE FROM ACCEPTED BACKUP"
docker run --rm \
  --user root --entrypoint /usr/bin/pgbackrest \
  -v "${SOURCE_PGVOL}:/var/lib/postgresql" \
  -v "${REAL_REPOVOL}:/var/lib/pgbackrest:ro" \
  "$IMAGE" \
  --stanza=dante --pg1-path=/var/lib/postgresql/18/docker \
  --repo1-path=/var/lib/pgbackrest --set="$BASE_BACKUP" \
  --type=immediate --target-action=promote --archive-mode=off \
  --log-level-console=info restore
normalize_pg18_parent "$SOURCE_PGVOL"

docker run -d --name "$BOOTSTRAP_CONTAINER" \
  -v "${SOURCE_PGVOL}:/var/lib/postgresql" \
  -v "${REAL_REPOVOL}:/var/lib/pgbackrest:ro" \
  "$IMAGE" postgres -c shared_preload_libraries=pg_stat_statements -c compute_query_id=on >/dev/null
wait_promoted "$BOOTSTRAP_CONTAINER" || die "bootstrap target did not promote"
bootstrap_head="$(docker exec --user postgres "$BOOTSTRAP_CONTAINER" psql -X -d dante -Atqc "SELECT version_num FROM dante.alembic_version;")"
echo "BOOTSTRAP ALEMBIC: $bootstrap_head"
docker rm -f "$BOOTSTRAP_CONTAINER" >/dev/null

headline "S2 — START SOURCE WITH INDEPENDENT EMPTY BACKUP REPOSITORY"
docker run -d --name "$SOURCE_CONTAINER" -p "127.0.0.1:${SOURCE_PORT}:5432" \
  -v "${SOURCE_PGVOL}:/var/lib/postgresql" \
  -v "${BACKUP_REPOVOL}:/var/lib/pgbackrest" \
  "$IMAGE" postgres \
    -c shared_preload_libraries=pg_stat_statements \
    -c compute_query_id=on \
    -c archive_mode=on \
    -c "archive_command=/usr/bin/pgbackrest --stanza=dante archive-push %p" >/dev/null
wait_ready_not_recovery "$SOURCE_CONTAINER" || die "source did not become ready"

docker exec --user postgres "$SOURCE_CONTAINER" pgbackrest --stanza=dante stanza-create

echo "DISPOSABLE SOURCE + INDEPENDENT B0 REPOSITORY: PASS"

headline "S3 — APPLY CURRENT REPOSITORY SCHEMA TO DISPOSABLE SOURCE"
export DANTE_DATABASE__HOST="127.0.0.1"
export DANTE_DATABASE__PORT="$SOURCE_PORT"
export DANTE_DATABASE__NAME="dante"
export DANTE_ADMIN__USER="postgres"
export DANTE_ADMIN__PASSWORD="$(cat "$ADMIN_SECRET")"
export DANTE_MIGRATOR__PASSWORD="$(cat "$MIGRATOR_SECRET")"
export DANTE_RUNTIME__PASSWORD="$(cat "$RUNTIME_SECRET")"

cd "$REPO_ROOT/apps/backend"
uv --version
uv run --frozen alembic upgrade head
uv run --frozen alembic current
uv run --frozen alembic check
cd "$REPO_ROOT"

current_head="$(docker exec --user postgres "$SOURCE_CONTAINER" psql -X -d dante -Atqc 'SELECT version_num FROM dante.alembic_version;')"
test "$current_head" = "$EXPECTED_HEAD" || die "source Alembic=$current_head"
current_topology="$(docker exec --user postgres "$SOURCE_CONTAINER" psql -X -d dante -Atqc "SELECT (SELECT count(*) FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace WHERE n.nspname='dante' AND c.relkind='r' AND c.relname<>'alembic_version'),(SELECT count(*) FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace WHERE n.nspname='dante' AND c.relkind='v'),(SELECT count(*) FROM pg_proc p JOIN pg_namespace n ON n.oid=p.pronamespace WHERE n.nspname='dante'),(SELECT count(*) FROM pg_trigger t JOIN pg_class c ON c.oid=t.tgrelid JOIN pg_namespace n ON n.oid=c.relnamespace WHERE n.nspname='dante' AND NOT t.tgisinternal),(SELECT count(*) FROM pg_index i JOIN pg_class c ON c.oid=i.indrelid JOIN pg_namespace n ON n.oid=c.relnamespace WHERE n.nspname='dante' AND c.relname<>'alembic_version'),(SELECT count(*) FROM pg_constraint c JOIN pg_namespace n ON n.oid=c.connamespace WHERE n.nspname='dante' AND c.contype='f'),(SELECT count(*) FROM pg_constraint c JOIN pg_namespace n ON n.oid=c.connamespace WHERE n.nspname='dante' AND c.contype='c'),(SELECT count(*) FROM pg_type t JOIN pg_namespace n ON n.oid=t.typnamespace WHERE n.nspname='dante' AND t.typtype IN ('d','e')),(SELECT count(*) FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace WHERE n.nspname='dante' AND c.relkind IN ('S','m','p')),(SELECT count(*) FROM pg_policy p JOIN pg_class c ON c.oid=p.polrelid JOIN pg_namespace n ON n.oid=c.relnamespace WHERE n.nspname='dante');")"
test "$current_topology" = "$EXPECTED_TOPOLOGY" || die "source topology=$current_topology"
echo "CURRENT SCHEMA $EXPECTED_HEAD / $EXPECTED_TOPOLOGY: PASS"

headline "S4 — CREATE REAL SESSION MATERIALSTATE + PROTECTED PAYLOAD X"
SESSION_REF="$(docker exec --user postgres "$SOURCE_CONTAINER" psql -X -d dante -Atqc 'SELECT uuidv7();')"
STATE_REF="$(docker exec --user postgres "$SOURCE_CONTAINER" psql -X -d dante -Atqc 'SELECT uuidv7();')"
SUPPRESSION_REF="$(docker exec --user postgres "$SOURCE_CONTAINER" psql -X -d dante -Atqc 'SELECT uuidv7();')"
PROTECTED_START="2026-08-30 12:34:56+00"
PROTECTED_END="2026-08-30 12:35:56+00"

docker exec -i --user postgres "$SOURCE_CONTAINER" psql -X -v ON_ERROR_STOP=1 -d dante <<SQL
BEGIN;
SET LOCAL ROLE dante_owner;
INSERT INTO dante.session(session_ref) VALUES ('$SESSION_REF'::uuid);
INSERT INTO dante.native_address(native_ref,owner_family) VALUES ('$SESSION_REF'::uuid,'session');
INSERT INTO dante.material_state_address(material_state_ref,native_owner_ref,facet_code) VALUES ('$STATE_REF'::uuid,'$SESSION_REF'::uuid,'session.timing');
INSERT INTO dante.session_timing_state(material_state_ref,session_ref,timing_form_code) VALUES ('$STATE_REF'::uuid,'$SESSION_REF'::uuid,'absolute');
INSERT INTO dante.session_timing_absolute(material_state_ref,started_at,start_precision_code,ended_at,end_precision_code) VALUES ('$STATE_REF'::uuid,timestamptz '$PROTECTED_START','exact',timestamptz '$PROTECTED_END','exact');
INSERT INTO dante.native_current_material_state(native_owner_ref,facet_code,material_state_ref) VALUES ('$SESSION_REF'::uuid,'session.timing','$STATE_REF'::uuid);
INSERT INTO dante.session_timing_current_history(session_ref,material_state_ref,current_from_at) VALUES ('$SESSION_REF'::uuid,'$STATE_REF'::uuid,clock_timestamp());
COMMIT;
SQL

shape="$(docker exec --user postgres "$SOURCE_CONTAINER" psql -X -d dante -Atqc "SELECT (SELECT count(*) FROM dante.session WHERE session_ref='$SESSION_REF'::uuid),(SELECT count(*) FROM dante.native_address WHERE native_ref='$SESSION_REF'::uuid),(SELECT count(*) FROM dante.material_state_address WHERE material_state_ref='$STATE_REF'::uuid),(SELECT count(*) FROM dante.session_timing_state WHERE material_state_ref='$STATE_REF'::uuid),(SELECT count(*) FROM dante.session_timing_absolute WHERE material_state_ref='$STATE_REF'::uuid),(SELECT count(*) FROM dante.native_current_material_state WHERE native_owner_ref='$SESSION_REF'::uuid AND material_state_ref='$STATE_REF'::uuid),(SELECT count(*) FROM dante.session_timing_current_history WHERE session_ref='$SESSION_REF'::uuid AND material_state_ref='$STATE_REF'::uuid);")"
test "$shape" = "1|1|1|1|1|1|1" || die "invalid DANTE Session fixture=$shape"
echo "SOURCE SHAPE: $shape"

headline "S5 — TAKE OLD FULL B0 CONTAINING X"
docker exec --user postgres "$SOURCE_CONTAINER" psql -X -d dante -Atqc 'SELECT pg_switch_wal();' >/dev/null
docker exec --user postgres "$SOURCE_CONTAINER" pgbackrest --stanza=dante check
docker exec --user postgres "$SOURCE_CONTAINER" pgbackrest --stanza=dante --type=full backup
B0="$(docker exec --user postgres "$SOURCE_CONTAINER" pgbackrest --stanza=dante --output=json info | python3 -c 'import json,sys; data=json.load(sys.stdin); full=[b["label"] for s in data for b in s.get("backup",[]) if b.get("type")=="full"]; print(max(full))')"
test -n "$B0" || die "cannot resolve B0"
echo "B0=$B0"

headline "S6 — PREPARE IMMUTABLE SUPPRESSION INTENT"
mkdir -p "$LEDGER_BUILD"
cd "$REPO_ROOT/apps/backend"
ACCEPTED_AT="$(uv run --frozen python - "$LEDGER_BUILD" "$SUPPRESSION_REF" "$STATE_REF" <<'PY'
from datetime import UTC, datetime
from pathlib import Path
import sys
from uuid import UUID
from dante.platform.recovery.suppression_ledger import prepare_suppression
root=Path(sys.argv[1])
record=prepare_suppression(root,recovery_suppression_ref=UUID(sys.argv[2]),material_state_ref=UUID(sys.argv[3]),facet_code='session.timing',retirement_code='redacted',accepted_at=datetime.now(UTC))
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
prepared_only_rc=$?
cd "$REPO_ROOT"
set -e
test "$prepared_only_rc" -ne 0 || die "PREPARED without COMMITTED did not block recovery"
echo "PREPARED WITHOUT COMMITTED BLOCKS: PASS"

headline "S7 — CANONICAL RETIREMENT/REDACTION COMMIT"
docker exec -i --user postgres "$SOURCE_CONTAINER" psql -X -v ON_ERROR_STOP=1 -d dante <<SQL
BEGIN;
SET LOCAL ROLE dante_owner;
INSERT INTO dante.material_state_retirement(material_state_ref,retirement_code,retired_at,recovery_suppression_ref)
VALUES ('$STATE_REF'::uuid,'redacted',timestamptz '$ACCEPTED_AT','$SUPPRESSION_REF'::uuid);
DELETE FROM dante.session_timing_absolute WHERE material_state_ref='$STATE_REF'::uuid;
COMMIT;
SQL

post_retirement="$(docker exec --user postgres "$SOURCE_CONTAINER" psql -X -d dante -Atqc "SELECT (SELECT count(*) FROM dante.material_state_retirement WHERE material_state_ref='$STATE_REF'::uuid AND recovery_suppression_ref='$SUPPRESSION_REF'::uuid),(SELECT count(*) FROM dante.session_timing_absolute WHERE material_state_ref='$STATE_REF'::uuid);")"
test "$post_retirement" = "1|0" || die "canonical retirement not committed safely=$post_retirement"

headline "S8 — COMMIT SUPPRESSION EVIDENCE AFTER DB READ-BACK"
cd "$REPO_ROOT/apps/backend"
uv run --frozen python - "$LEDGER_BUILD" "$SUPPRESSION_REF" "$STATE_REF" <<'PY'
from datetime import UTC, datetime
from pathlib import Path
import sys
from uuid import UUID
from dante.platform.recovery.suppression_ledger import commit_after_canonical_verification
commit_after_canonical_verification(Path(sys.argv[1]),recovery_suppression_ref=UUID(sys.argv[2]),verified_material_state_ref=UUID(sys.argv[3]),committed_at=datetime.now(UTC))
PY
cd "$REPO_ROOT"
copy_ledger_build_to_volume

ledger_files="$(docker run --rm --entrypoint sh -v "${LEDGER_VOL}:/ledger:ro" "$IMAGE" -lc 'find /ledger/records -maxdepth 1 -type f -printf "%f\n" | sort')"
printf '%s\n' "$ledger_files"
test "$(printf '%s\n' "$ledger_files" | wc -l)" = "2" || die "ledger does not contain exactly PREPARED+COMMITTED"
rm -rf "$LEDGER_BUILD"
echo "INDEPENDENT COMMITTED LEDGER: PASS"

headline "S9 — DISASTER: DESTROY ONLY DISPOSABLE PGDATA"
docker rm -f "$SOURCE_CONTAINER" >/dev/null
docker volume rm "$SOURCE_PGVOL" >/dev/null
create_volume "$SOURCE_PGVOL"
docker volume inspect "$BACKUP_REPOVOL" >/dev/null || die "B0 repository disappeared"
docker volume inspect "$LEDGER_VOL" >/dev/null || die "suppression ledger disappeared"
echo "PGDATA DESTROYED; B0 + LEDGER SURVIVED: PASS"

headline "S10 — RESTORE EXACT B0 AND PROVE PHYSICAL RESURRECTION"
docker run --rm --user root --entrypoint /usr/bin/pgbackrest \
  -v "${SOURCE_PGVOL}:/var/lib/postgresql" \
  -v "${BACKUP_REPOVOL}:/var/lib/pgbackrest:ro" \
  "$IMAGE" --stanza=dante --pg1-path=/var/lib/postgresql/18/docker \
  --repo1-path=/var/lib/pgbackrest --set="$B0" \
  --type=immediate --target-action=promote --archive-mode=off \
  --log-level-console=info restore
normalize_pg18_parent "$SOURCE_PGVOL"

docker run -d --name "$RESTORED_CONTAINER" \
  -v "${SOURCE_PGVOL}:/var/lib/postgresql" \
  -v "${BACKUP_REPOVOL}:/var/lib/pgbackrest:ro" \
  "$IMAGE" postgres -c shared_preload_libraries=pg_stat_statements -c compute_query_id=on >/dev/null
wait_promoted "$RESTORED_CONTAINER" || die "restored B0 target did not promote"

restored_contract="$(docker exec --user postgres "$RESTORED_CONTAINER" psql -X -d dante -Atqc "SELECT (SELECT version_num FROM dante.alembic_version),(SELECT to_regclass('dante.material_state_retirement') IS NOT NULL),(SELECT count(*) FROM dante.session_timing_absolute WHERE material_state_ref='$STATE_REF'::uuid),(SELECT count(*) FROM dante.material_state_retirement WHERE material_state_ref='$STATE_REF'::uuid);")"
echo "RESTORED head|retirement-table|payload-X|tombstone = $restored_contract"
test "$restored_contract" = "$EXPECTED_HEAD|t|1|0" || die "B0 did not prove current-schema physical resurrection=$restored_contract"
echo "OLD B0 PHYSICALLY RESURRECTED X WHILE TARGET IS ISOLATED: PROVEN"

headline "S11 — LOAD COMMITTED LEDGER FROM INDEPENDENT VOLUME"
copy_ledger_volume_to_readback
cd "$REPO_ROOT/apps/backend"
LEDGER_RECORD="$(uv run --frozen python - "$LEDGER_READ" <<'PY'
from pathlib import Path
import sys
from dante.platform.recovery.suppression_ledger import load_committed_suppressions
records=load_committed_suppressions(Path(sys.argv[1]))
if len(records)!=1:
    raise SystemExit(f'expected exactly one committed suppression, got {len(records)}')
r=records[0]
print('|'.join((r.recovery_suppression_ref,r.material_state_ref,r.facet_code,r.effect,r.retirement_code,r.accepted_at)))
PY
)"
cd "$REPO_ROOT"
IFS='|' read -r L_SUPPRESSION_REF L_STATE_REF L_FACET L_EFFECT L_RETIREMENT L_ACCEPTED_AT <<<"$LEDGER_RECORD"
test "$L_SUPPRESSION_REF" = "$SUPPRESSION_REF" || die "ledger suppression ref mismatch"
test "$L_STATE_REF" = "$STATE_REF" || die "ledger state ref mismatch"
test "$L_FACET" = "session.timing" || die "ledger facet mismatch"
test "$L_EFFECT" = "suppress_payload" || die "ledger effect mismatch"
test "$L_RETIREMENT" = "redacted" || die "ledger retirement mismatch"
echo "COMMITTED LEDGER VALIDATION: PASS"

headline "S12 — RECONCILE RESURRECTED PAYLOAD BEFORE REOPEN"
docker exec -i --user postgres "$RESTORED_CONTAINER" psql -X -v ON_ERROR_STOP=1 -d dante <<SQL
BEGIN;
SET LOCAL ROLE dante_owner;
INSERT INTO dante.material_state_retirement(material_state_ref,retirement_code,retired_at,recovery_suppression_ref)
VALUES ('$L_STATE_REF'::uuid,'$L_RETIREMENT',timestamptz '$L_ACCEPTED_AT','$L_SUPPRESSION_REF'::uuid);
DELETE FROM dante.session_timing_absolute WHERE material_state_ref='$L_STATE_REF'::uuid;
COMMIT;
SQL

final_shape="$(docker exec --user postgres "$RESTORED_CONTAINER" psql -X -d dante -Atqc "SELECT (SELECT count(*) FROM dante.session WHERE session_ref='$SESSION_REF'::uuid),(SELECT count(*) FROM dante.native_address WHERE native_ref='$SESSION_REF'::uuid),(SELECT count(*) FROM dante.material_state_address WHERE material_state_ref='$STATE_REF'::uuid),(SELECT count(*) FROM dante.session_timing_state WHERE material_state_ref='$STATE_REF'::uuid),(SELECT count(*) FROM dante.material_state_retirement WHERE material_state_ref='$STATE_REF'::uuid AND recovery_suppression_ref='$SUPPRESSION_REF'::uuid),(SELECT count(*) FROM dante.session_timing_absolute WHERE material_state_ref='$STATE_REF'::uuid),(SELECT count(*) FROM dante.native_current_material_state WHERE native_owner_ref='$SESSION_REF'::uuid AND material_state_ref='$STATE_REF'::uuid),(SELECT count(*) FROM dante.session_timing_current_history WHERE session_ref='$SESSION_REF'::uuid AND material_state_ref='$STATE_REF'::uuid);")"
test "$final_shape" = "1|1|1|1|1|0|1|1" || die "anti-resurrection continuity failed=$final_shape"
echo "FINAL session|native|state-address|state|tombstone|payload|current|history = $final_shape"

set +e
docker exec --user postgres "$RESTORED_CONTAINER" psql -X -v ON_ERROR_STOP=1 -d dante -c "SET ROLE dante_owner; INSERT INTO dante.session_timing_absolute(material_state_ref,started_at,start_precision_code) VALUES ('$STATE_REF'::uuid,clock_timestamp(),'exact');" >/dev/null 2>&1
reinsert_rc=$?
set -e
test "$reinsert_rc" -ne 0 || die "retired payload reinsertion unexpectedly succeeded"
echo "PAYLOAD REINSERTION AFTER RETIREMENT: REJECTED"

headline "S13 — FINAL CURRENT ACCEPTANCE + NON-INTERFERENCE"
final_head="$(docker exec --user postgres "$RESTORED_CONTAINER" psql -X -d dante -Atqc 'SELECT version_num FROM dante.alembic_version;')"
test "$final_head" = "$EXPECTED_HEAD" || die "final Alembic=$final_head"
final_in_recovery="$(docker exec --user postgres "$RESTORED_CONTAINER" psql -X -d dante -Atqc 'SELECT pg_is_in_recovery();')"
test "$final_in_recovery" = "f" || die "final target still in recovery"
runtime_acl="$(docker exec --user postgres "$RESTORED_CONTAINER" psql -X -d dante -Atqc "SELECT has_table_privilege('dante_runtime','dante.material_state_retirement','SELECT')::text || '|' || has_table_privilege('dante_runtime','dante.material_state_retirement','INSERT')::text || '|' || has_table_privilege('dante_runtime','dante.material_state_retirement','UPDATE')::text || '|' || has_table_privilege('dante_runtime','dante.material_state_retirement','DELETE')::text;")"
test "$runtime_acl" = "true|false|false|false" || die "runtime retirement ACL=$runtime_acl"

real_repo_hash_after="$(docker run --rm --entrypoint sha256sum -v "${REAL_REPOVOL}:/var/lib/pgbackrest:ro" "$IMAGE" /var/lib/pgbackrest/backup/dante/backup.info | awk '{print $1}')"
test "$real_repo_hash_after" = "$real_repo_hash_before" || die "real recovery repository changed"
cp05_state_after="$(docker exec --user postgres "$CP05_TARGET" psql -X -d dante -Atqc "SELECT current_setting('server_version_num'),pg_is_in_recovery(),current_setting('archive_mode'),(SELECT count(*) FROM dante.person WHERE person_ref='${A_REF}'::uuid),(SELECT count(*) FROM dante.person WHERE person_ref='${B_REF}'::uuid);" 2>/dev/null || true)"
test "$cp05_state_after" = "$cp05_state_before" || die "CP05 target changed"
test -z "$(git status --porcelain)" || die "Git worktree changed"

echo
echo "current schema applied to disposable source       PASS"
echo "B0 contains protected canonical payload X        PASS"
echo "PREPARED without COMMITTED blocks                PASS"
echo "canonical retirement removes X                   PASS"
echo "COMMITTED written after canonical verification   PASS"
echo "suppression ledger independent of PGDATA         PASS"
echo "suppression ledger independent of B0 repository  PASS"
echo "old B0 physically resurrects X                   PROVEN"
echo "restored target isolated during reconciliation   PASS"
echo "ledger-driven reconcile removes X                PASS"
echo "NativeRef continuity retained                    PASS"
echo "MaterialStateRef continuity retained             PASS"
echo "current/history continuity retained              PASS"
echo "payload reinsertion rejected                     PASS"
echo "runtime retirement ACL SELECT-only               PASS"
echo "real pgBackRest repository untouched             PASS"
echo "CP05 isolated target untouched                   PASS"
echo "Git worktree untouched                           PASS"
echo
echo "=== SC-011 DEFINITIVE ANTI-RESURRECTION: LOCAL PASS CANDIDATE ==="