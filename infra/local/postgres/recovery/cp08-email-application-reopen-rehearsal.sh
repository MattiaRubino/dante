#!/usr/bin/env bash
set -Eeuo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd -- "${SCRIPT_DIR}/../../../.." && pwd)"

BOOTSTRAP="${SCRIPT_DIR}/bootstrap-local-recovery.sh"
IMAGE="${DANTE_RECOVERY_IMAGE:-dante-postgres-recovery:18.6-pgbackrest-2.59.1}"
EXPECTED_ALEMBIC="20260904_17"
EXPECTED_TOPOLOGY="88|5|16|76|172|89|270|0|0|0"

ADMIN_SECRET="infra/compose/secrets/postgres_password.local"
MIGRATOR_SECRET="infra/compose/secrets/postgres_recovery_migrator_password.local"
RUNTIME_SECRET="infra/compose/secrets/postgres_recovery_runtime_password.local"
REPORT_REL="infra/compose/secrets/postgres_recovery_cp08_email_report.json.local"
REPORT_PATH="${REPO_ROOT}/${REPORT_REL}"

PORT="${DANTE_CP08_PORT:-55437}"
KEEP_ON_FAILURE="${DANTE_CP08_KEEP_ON_FAILURE:-0}"

RUN_ID="cp08-$(date -u +%Y%m%dT%H%M%SZ)-$$"
PGVOL="${RUN_ID}-pgdata"
REPOVOL="${RUN_ID}-repo"
SOURCE_CONTAINER="${RUN_ID}-source"
RESTORED_CONTAINER="${RUN_ID}-restored"

TMPDIR="$(mktemp -d)"
RECOVERY_LOG="${TMPDIR}/recovery.log"
EXPLICIT_CLEANUP=0


die() {
  echo >&2
  echo "FAIL: $*" >&2
  exit 1
}

cleanup_resources() {
  set +e
  docker rm -f "$SOURCE_CONTAINER" "$RESTORED_CONTAINER" >/dev/null 2>&1 || true
  docker volume rm "$PGVOL" "$REPOVOL" >/dev/null 2>&1 || true
  rm -rf "$TMPDIR" >/dev/null 2>&1 || true
  set -e
}

cleanup() {
  status=$?
  set +e
  if [ "$EXPLICIT_CLEANUP" -ne 1 ]; then
    if [ "$status" -ne 0 ] && [ "$KEEP_ON_FAILURE" = "1" ]; then
      echo
      echo "CP08 failed; disposable resources retained for diagnosis:"
      echo "  source container:   $SOURCE_CONTAINER"
      echo "  restored container: $RESTORED_CONTAINER"
      echo "  PGDATA volume:      $PGVOL"
      echo "  repository volume:  $REPOVOL"
      echo "  tmpdir:             $TMPDIR"
    else
      cleanup_resources
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
  for _ in $(seq 1 90); do
    found="$(repo_find "$pattern")"
    if [ -n "$found" ]; then
      echo "ARCHIVED: $found"
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
}

email_state() {
  local container="$1"
  docker exec --user postgres "$container" psql -X -d dante -Atqc "
SELECT
  coalesce(string_agg(idempotency_key || '=' || dispatch_state_code, ',' ORDER BY idempotency_key),''),
  count(*) FILTER (WHERE sensitive_key_id IS NOT NULL AND sensitive_nonce IS NOT NULL AND sensitive_ciphertext IS NOT NULL),
  count(*) FILTER (WHERE claim_token IS NOT NULL OR claimed_until IS NOT NULL OR next_attempt_at IS NOT NULL)
FROM dante.email_delivery_intent
WHERE operation_scope='$RUN_ID';
SELECT
  count(*) FILTER (WHERE a.result_code='in_progress'),
  count(*) FILTER (WHERE a.result_code='ambiguous'),
  count(*) FILTER (WHERE a.result_code='retryable_failure')
FROM dante.email_delivery_attempt a
JOIN dante.email_delivery_intent i ON i.email_intent_ref=a.email_intent_ref
WHERE i.operation_scope='$RUN_ID';
"
}

cd "$REPO_ROOT"

echo "=== DANTE CP08 — EMAIL / APPLICATION REOPEN AFTER PITR ==="
echo "Provider/network I/O is forbidden in this rehearsal."
echo "Email workers are never started by this harness."

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

for secret in "$ADMIN_SECRET" "$MIGRATOR_SECRET" "$RUNTIME_SECRET"; do
  test -s "$secret" || die "missing $secret"
  git check-ignore -q "$secret" || die "$secret is not ignored"
done
git check-ignore -q "$REPORT_REL" || die "$REPORT_REL is not ignored"

docker image inspect "$IMAGE" >/dev/null 2>&1 || die "bootstrap did not materialize $IMAGE"
docker volume create "$PGVOL" >/dev/null
docker volume create "$REPOVOL" >/dev/null

export DANTE_DATABASE__HOST="127.0.0.1"
export DANTE_DATABASE__PORT="$PORT"
export DANTE_DATABASE__NAME="dante"
export DANTE_ADMIN__USER="postgres"
export DANTE_ADMIN__PASSWORD="$(cat "$ADMIN_SECRET")"
export DANTE_MIGRATOR__PASSWORD="$(cat "$MIGRATOR_SECRET")"
export DANTE_RUNTIME__PASSWORD="$(cat "$RUNTIME_SECRET")"


echo
echo "S1 — START DISPOSABLE SOURCE + PROVISION CURRENT DATABASE"

docker run -d \
  --name "$SOURCE_CONTAINER" \
  -p "127.0.0.1:${PORT}:5432" \
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

wait_ready "$SOURCE_CONTAINER" || die "source did not become ready"
docker exec --user postgres "$SOURCE_CONTAINER" pgbackrest --stanza=dante stanza-create

cd "$REPO_ROOT/apps/backend"
uv run --frozen python -m dante.platform.database.provisioning
uv run --frozen alembic upgrade head
uv run --frozen python -m dante.platform.database.provisioning
uv run --frozen alembic check
cd "$REPO_ROOT"
assert_current_contract "$SOURCE_CONTAINER"
docker exec --user postgres "$SOURCE_CONTAINER" pgbackrest --stanza=dante check


echo
echo "S2 — CREATE RESTORABLE EMAIL WORK: pending + claimed + retryable_failure"

docker exec -i --user postgres "$SOURCE_CONTAINER" psql -X -v ON_ERROR_STOP=1 -d dante <<SQL
BEGIN;
SET LOCAL ROLE dante_owner;

WITH ids AS (
  SELECT uuidv7() AS intent_ref
)
INSERT INTO dante.email_delivery_intent(
  email_intent_ref,purpose_code,stream_code,recipient_address,recipient_comparison_key,
  template_code,template_revision,locale_code,operation_scope,idempotency_key,
  supersession_key,payload_fingerprint,sensitive_key_id,sensitive_nonce,sensitive_ciphertext,
  created_at,updated_at,eligible_at,expires_at,dispatch_state_code,claim_token,claimed_until,
  attempt_count,attempt_limit,next_attempt_at,last_error_code,accepted_at,terminal_at,
  sensitive_wiped_at
)
SELECT intent_ref,'recovery_probe','security','pending@example.com','pending@example.com',
       'recovery_probe','1','en','$RUN_ID','pending',NULL,
       decode(repeat('11',32),'hex'),'cp08-key',decode(repeat('22',12),'hex'),decode(repeat('33',32),'hex'),
       clock_timestamp(),clock_timestamp(),clock_timestamp(),clock_timestamp()+interval '2 hours',
       'pending',NULL,NULL,0,3,NULL,NULL,NULL,NULL,NULL
FROM ids;

WITH ids AS (
  SELECT uuidv7() AS intent_ref, uuidv7() AS claim_ref, uuidv7() AS attempt_ref
), inserted AS (
  INSERT INTO dante.email_delivery_intent(
    email_intent_ref,purpose_code,stream_code,recipient_address,recipient_comparison_key,
    template_code,template_revision,locale_code,operation_scope,idempotency_key,
    supersession_key,payload_fingerprint,sensitive_key_id,sensitive_nonce,sensitive_ciphertext,
    created_at,updated_at,eligible_at,expires_at,dispatch_state_code,claim_token,claimed_until,
    attempt_count,attempt_limit,next_attempt_at,last_error_code,accepted_at,terminal_at,
    sensitive_wiped_at
  )
  SELECT intent_ref,'recovery_probe','security','claimed@example.com','claimed@example.com',
         'recovery_probe','1','en','$RUN_ID','claimed',NULL,
         decode(repeat('44',32),'hex'),'cp08-key',decode(repeat('55',12),'hex'),decode(repeat('66',32),'hex'),
         clock_timestamp(),clock_timestamp(),clock_timestamp(),clock_timestamp()+interval '2 hours',
         'claimed',claim_ref,clock_timestamp()+interval '1 hour',1,3,NULL,NULL,NULL,NULL,NULL
  FROM ids
  RETURNING email_intent_ref
)
INSERT INTO dante.email_delivery_attempt(
  email_attempt_ref,email_intent_ref,attempt_number,provider_code,started_at,finished_at,
  result_code,provider_message_id,error_code
)
SELECT ids.attempt_ref, inserted.email_intent_ref, 1, 'ses', clock_timestamp(), NULL,
       'in_progress', NULL, NULL
FROM ids, inserted;

WITH ids AS (
  SELECT uuidv7() AS intent_ref, uuidv7() AS attempt_ref
), inserted AS (
  INSERT INTO dante.email_delivery_intent(
    email_intent_ref,purpose_code,stream_code,recipient_address,recipient_comparison_key,
    template_code,template_revision,locale_code,operation_scope,idempotency_key,
    supersession_key,payload_fingerprint,sensitive_key_id,sensitive_nonce,sensitive_ciphertext,
    created_at,updated_at,eligible_at,expires_at,dispatch_state_code,claim_token,claimed_until,
    attempt_count,attempt_limit,next_attempt_at,last_error_code,accepted_at,terminal_at,
    sensitive_wiped_at
  )
  SELECT intent_ref,'recovery_probe','security','retryable@example.com','retryable@example.com',
         'recovery_probe','1','en','$RUN_ID','retryable',NULL,
         decode(repeat('77',32),'hex'),'cp08-key',decode(repeat('88',12),'hex'),decode(repeat('99',32),'hex'),
         clock_timestamp(),clock_timestamp(),clock_timestamp(),clock_timestamp()+interval '2 hours',
         'retryable_failure',NULL,NULL,1,3,clock_timestamp()+interval '1 hour',
         'temporary_provider_failure',NULL,NULL,NULL
  FROM ids
  RETURNING email_intent_ref
)
INSERT INTO dante.email_delivery_attempt(
  email_attempt_ref,email_intent_ref,attempt_number,provider_code,started_at,finished_at,
  result_code,provider_message_id,error_code
)
SELECT ids.attempt_ref, inserted.email_intent_ref, 1, 'ses',
       clock_timestamp()-interval '1 second', clock_timestamp(),
       'retryable_failure', NULL, 'temporary_provider_failure'
FROM ids, inserted;

COMMIT;
SQL

SOURCE_PRE="$(email_state "$SOURCE_CONTAINER")"
printf '%s\n' "$SOURCE_PRE"
EXPECTED_PRE=$'claimed=claimed,pending=pending,retryable=retryable_failure|3|2\n1|0|1'
test "$SOURCE_PRE" = "$EXPECTED_PRE" || die "unexpected source fixture state"


echo
echo "S3 — FULL BACKUP CONTAINING SENDABLE EMAIL WORK"

docker exec --user postgres "$SOURCE_CONTAINER" psql -X -d dante -Atqc 'SELECT pg_switch_wal();' >/dev/null
docker exec --user postgres "$SOURCE_CONTAINER" pgbackrest --stanza=dante check
docker exec --user postgres "$SOURCE_CONTAINER" pgbackrest --stanza=dante --type=full backup
B0="$(docker exec --user postgres "$SOURCE_CONTAINER" pgbackrest --stanza=dante --output=json info | python3 -c \
  'import json,sys; data=json.load(sys.stdin); full=[b["label"] for s in data for b in s.get("backup",[]) if b.get("type")=="full"]; print(max(full))')"
test -n "$B0" || die "cannot resolve backup label"


echo
echo "S4 — CREATE PITR TARGET WHILE EMAIL WORK IS STILL SENDABLE"
RESTORE_POINT="${RUN_ID}_EMAIL_SENDABLE"
RESTORE_RESULT="$(docker exec --user postgres "$SOURCE_CONTAINER" psql -X -d dante -Atqc \
  "SELECT pg_create_restore_point('$RESTORE_POINT')::text;")"
test -n "$RESTORE_RESULT" || die "restore point missing"
RESTORE_WAL="$(docker exec --user postgres "$SOURCE_CONTAINER" psql -X -d dante -Atqc \
  "SELECT pg_walfile_name('$RESTORE_RESULT'::pg_lsn);")"
TARGET_TIMELINE="$((16#${RESTORE_WAL:0:8}))"
docker exec --user postgres "$SOURCE_CONTAINER" psql -X -d dante -Atqc 'SELECT pg_switch_wal();' >/dev/null
wait_repo_file "${RESTORE_WAL}-*" || die "restore-point WAL not archived"


echo
echo "S5 — LATER SOURCE HISTORY QUARANTINES EMAIL WORK"
cd "$REPO_ROOT/apps/backend"
SOURCE_RECONCILE_JSON="$(uv run --frozen python -m dante.platform.recovery.email_post_restore)"
cd "$REPO_ROOT"
echo "$SOURCE_RECONCILE_JSON"
SOURCE_POST="$(email_state "$SOURCE_CONTAINER")"
printf '%s\n' "$SOURCE_POST"
EXPECTED_POST=$'claimed=recovery_quarantined,pending=recovery_quarantined,retryable=recovery_quarantined|0|0\n0|1|1'
test "$SOURCE_POST" = "$EXPECTED_POST" || die "source did not reach safe later state"


echo
echo "S6 — SIMULATE COMPLETE PGDATA LOSS"
docker rm -f "$SOURCE_CONTAINER" >/dev/null
docker volume rm "$PGVOL" >/dev/null
docker volume inspect "$REPOVOL" >/dev/null || die "repository disappeared"
docker volume create "$PGVOL" >/dev/null


echo
echo "S7 — RESTORE B0 + PITR TO SENDABLE EMAIL TARGET"
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

normalize_pg18_parent

docker run -d \
  --name "$RESTORED_CONTAINER" \
  -p "127.0.0.1:${PORT}:5432" \
  -v "${PGVOL}:/var/lib/postgresql" \
  -v "${REPOVOL}:/var/lib/pgbackrest:ro" \
  "$IMAGE" \
  postgres \
    -c shared_preload_libraries=pg_stat_statements \
    -c compute_query_id=on >/dev/null

wait_promoted "$RESTORED_CONTAINER" || die "restored target did not promote"
docker logs --timestamps "$RESTORED_CONTAINER" >"$RECOVERY_LOG" 2>&1
assert_current_contract "$RESTORED_CONTAINER"


echo
echo "S8 — PROVE SENDABLE EMAIL WORK PHYSICALLY RESURRECTED WHILE TRAFFIC IS ISOLATED"
RESTORED_PRE="$(email_state "$RESTORED_CONTAINER")"
printf '%s\n' "$RESTORED_PRE"
test "$RESTORED_PRE" = "$EXPECTED_PRE" || die "PITR did not restore expected sendable Email state"
echo "RESTORED SENDABLE EMAIL WORK: PROVEN"
echo "EMAIL WORKERS: NOT STARTED"
echo "PROVIDER I/O: NOT ACTIVATED"


echo
echo "S9 — RUN FAIL-CLOSED EMAIL POST-RESTORE RECONCILIATION"
cd "$REPO_ROOT/apps/backend"
RESTORE_RECONCILE_JSON="$(uv run --frozen python -m dante.platform.recovery.email_post_restore)"
SECOND_RECONCILE_JSON="$(uv run --frozen python -m dante.platform.recovery.email_post_restore)"
cd "$REPO_ROOT"
echo "$RESTORE_RECONCILE_JSON"
echo "$SECOND_RECONCILE_JSON"

python3 - "$RESTORE_RECONCILE_JSON" "$SECOND_RECONCILE_JSON" <<'PY'
import json
import sys
first = json.loads(sys.argv[1])
second = json.loads(sys.argv[2])
assert first == {
    "ambiguous_attempt_count": 1,
    "in_progress_quarantined_attempt_count": 0,
    "quarantined_intent_count": 3,
    "remaining_sendable_intent_count": 0,
    "unsafe_quarantined_intent_count": 0,
}
assert second == {
    "ambiguous_attempt_count": 0,
    "in_progress_quarantined_attempt_count": 0,
    "quarantined_intent_count": 0,
    "remaining_sendable_intent_count": 0,
    "unsafe_quarantined_intent_count": 0,
}
PY

RESTORED_POST="$(email_state "$RESTORED_CONTAINER")"
printf '%s\n' "$RESTORED_POST"
test "$RESTORED_POST" = "$EXPECTED_POST" || die "restored Email state remains unsafe"


echo
echo "S10 — PROVE NO EMAIL WORK CAN BE CLAIMED AFTER RECONCILIATION"
cd "$REPO_ROOT/apps/backend"
CLAIMABLE="$(uv run --frozen python - <<'PY'
import asyncio
import os
from pydantic import SecretStr
from sqlalchemy import func, select
from dante.platform.config.database import DatabaseSettings
from dante.platform.database.mappings.email_delivery import EmailDeliveryIntentRow
from dante.platform.database.runtime import create_database_runtime

async def main() -> None:
    settings = DatabaseSettings(
        host=os.environ["DANTE_DATABASE__HOST"],
        port=int(os.environ["DANTE_DATABASE__PORT"]),
        name=os.environ["DANTE_DATABASE__NAME"],
        user="dante_runtime",
        password=SecretStr(os.environ["DANTE_RUNTIME__PASSWORD"]),
        pool_size=1,
        max_overflow=0,
    )
    runtime = create_database_runtime(settings)
    try:
        async with runtime.session_factory() as session, session.begin():
            count = await session.scalar(
                select(func.count()).select_from(EmailDeliveryIntentRow).where(
                    EmailDeliveryIntentRow.dispatch_state_code.in_(
                        ("pending", "claimed", "retryable_failure")
                    )
                )
            )
            print(int(count or 0))
    finally:
        await runtime.dispose()

asyncio.run(main())
PY
)"
cd "$REPO_ROOT"
test "$CLAIMABLE" = "0" || die "$CLAIMABLE EmailIntent rows remain claimable"


echo
echo "S11 — WRITE LOCAL CP08 EVIDENCE"
export CP08_RUN_ID="$RUN_ID"
export CP08_PROOF_HEAD="$PROOF_HEAD"
export CP08_GIT_BRANCH="$GIT_BRANCH"
export CP08_GIT_UPSTREAM="$GIT_UPSTREAM"
export CP08_IMAGE="$IMAGE"
export CP08_BACKUP="$B0"
export CP08_RESTORE_POINT="$RESTORE_POINT"
export CP08_RESTORE_LSN="$RESTORE_RESULT"
export CP08_RESTORED_PRE="$RESTORED_PRE"
export CP08_RESTORED_POST="$RESTORED_POST"
export CP08_RECONCILE_JSON="$RESTORE_RECONCILE_JSON"

python3 - "$REPORT_PATH" <<'PY'
from datetime import UTC, datetime
import json
import os
from pathlib import Path
import sys

report = {
    "report_version": 1,
    "status": "LOCAL_PASS",
    "scope": "email_application_reopen_after_pitr",
    "completed_at": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
    "run_id": os.environ["CP08_RUN_ID"],
    "git_proof_head": os.environ["CP08_PROOF_HEAD"],
    "git_branch": os.environ["CP08_GIT_BRANCH"],
    "git_upstream": os.environ["CP08_GIT_UPSTREAM"],
    "recovery_image": os.environ["CP08_IMAGE"],
    "database": {
        "postgresql_server_version_num": 180006,
        "alembic_head": "20260904_17",
        "topology": "88|5|16|76|172|89|270|0|0|0",
    },
    "backup": {"label": os.environ["CP08_BACKUP"]},
    "recovery_point": {
        "name": os.environ["CP08_RESTORE_POINT"],
        "lsn": os.environ["CP08_RESTORE_LSN"],
    },
    "pre_reconcile_state": os.environ["CP08_RESTORED_PRE"],
    "post_reconcile_state": os.environ["CP08_RESTORED_POST"],
    "reconciliation": json.loads(os.environ["CP08_RECONCILE_JSON"]),
    "workers_started": False,
    "provider_io_exercised": False,
    "application_email_reopen": "PASS",
    "production_cloud_recovery": "NOT_CLAIMED",
    "measurement_note": "LOCAL rehearsal only; no provider/network send occurred.",
}
path = Path(sys.argv[1])
path.parent.mkdir(parents=True, exist_ok=True)
path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
PY
chmod 600 "$REPORT_PATH"
git check-ignore -q "$REPORT_REL" || die "CP08 report is not ignored"


echo
echo "S12 — CLEANUP DISPOSABLE CP08 RESOURCES"
cleanup_resources
for resource in "$PGVOL" "$REPOVOL"; do
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


echo
echo "=== CP08 EMAIL / APPLICATION REOPEN: PASS ==="
echo "PROOF HEAD:             $PROOF_HEAD"
echo "GIT BRANCH:             $GIT_BRANCH"
echo "GIT UPSTREAM:           $GIT_UPSTREAM"
echo "ALEMBIC:                $EXPECTED_ALEMBIC"
echo "RESTORED SENDABLE WORK: PROVEN"
echo "QUARANTINE + WIPE:      PASS"
echo "CLAIMABLE AFTER:        0"
echo "EMAIL WORKERS:          NOT STARTED BEFORE RECONCILIATION"
echo "PROVIDER I/O:           NOT EXERCISED"
echo "APPLICATION/EMAIL:      REOPEN PASS"
echo "REPORT:                 $REPORT_REL"
