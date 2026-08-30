#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd -- "${SCRIPT_DIR}/../../../.." && pwd)"
PROJECT_NAME="dante-postgres-recovery"
BASE_COMPOSE="infra/compose/local.yaml"
RECOVERY_COMPOSE="infra/compose/postgres-recovery.override.yaml"

cd "$REPO_ROOT"

compose() {
  docker compose \
    -p "$PROJECT_NAME" \
    -f "$BASE_COMPOSE" \
    -f "$RECOVERY_COMPOSE" \
    "$@"
}

echo "=== DANTE CP03 — archive failure/recovery proof ==="
compose ps

compose exec --user root postgres sh -lc '
  set -eu

  pg() {
    su -s /bin/sh postgres -c "psql -X -d dante -Atqc \"$1\""
  }

  archive_dir="$(
    find /var/lib/pgbackrest/archive/dante/18-1 \
      -mindepth 1 -maxdepth 1 -type d \
      | sort \
      | tail -n 1
  )"

  test -n "$archive_dir"

  original_mode="$(stat -c "%a" "$archive_dir")"
  original_owner="$(stat -c "%U:%G" "$archive_dir")"

  echo "ARCHIVE DIR:   $archive_dir"
  echo "OWNER:         $original_owner"
  echo "ORIGINAL MODE: $original_mode"

  test "$original_owner" = "postgres:postgres"

  restore_permissions() {
    chmod "$original_mode" "$archive_dir"
  }

  trap restore_permissions EXIT HUP INT TERM

  baseline_archived="$(pg "SELECT archived_count FROM pg_stat_archiver;")"
  baseline_failed="$(pg "SELECT failed_count FROM pg_stat_archiver;")"
  wal_to_fail="$(pg "SELECT pg_walfile_name(pg_current_wal_lsn());")"

  echo "BASE ARCHIVED: $baseline_archived"
  echo "BASE FAILED:   $baseline_failed"
  echo "TARGET WAL:    $wal_to_fail"

  echo "=== INJECT FAILURE ==="
  chmod 0550 "$archive_dir"
  stat -c "%U:%G %a %n" "$archive_dir"

  pg "SELECT pg_switch_wal();" >/dev/null

  failure_seen=0
  i=0

  while [ "$i" -lt 30 ]; do
    failed="$(pg "SELECT failed_count FROM pg_stat_archiver;")"
    last_failed="$(pg "SELECT COALESCE(last_failed_wal, '''''' ) FROM pg_stat_archiver;")"

    echo "failure poll: failed=$failed last_failed=$last_failed"

    if [ "$failed" -gt "$baseline_failed" ]; then
      failure_seen=1
      break
    fi

    i=$((i + 1))
    sleep 1
  done

  if [ "$failure_seen" -ne 1 ]; then
    echo "FAIL: archiver failure was not observed"
    exit 1
  fi

  echo "ARCHIVER FAILURE VISIBILITY: PASS"

  echo "=== RESTORE REPOSITORY ==="
  restore_permissions
  trap - EXIT HUP INT TERM

  stat -c "%U:%G %a %n" "$archive_dir"

  recovery_seen=0
  i=0

  while [ "$i" -lt 30 ]; do
    archived="$(pg "SELECT archived_count FROM pg_stat_archiver;")"
    last_archived="$(pg "SELECT COALESCE(last_archived_wal, '''''' ) FROM pg_stat_archiver;")"

    echo "recovery poll: archived=$archived last_archived=$last_archived"

    if [ "$archived" -gt "$baseline_archived" ] && \
       [ "$last_archived" = "$wal_to_fail" ]; then
      recovery_seen=1
      break
    fi

    i=$((i + 1))
    sleep 1
  done

  if [ "$recovery_seen" -ne 1 ]; then
    echo "FAIL: WAL was not archived after repository recovery"
    exit 1
  fi

  echo "ARCHIVER RECOVERY: PASS"

  echo "=== PHYSICAL WAL ==="
  find /var/lib/pgbackrest/archive/dante \
    -type f \
    -name "${wal_to_fail}-*" \
    -print

  test -n "$(
    find /var/lib/pgbackrest/archive/dante \
      -type f \
      -name "${wal_to_fail}-*" \
      -print \
      -quit
  )"

  echo "PHYSICAL WAL AFTER RECOVERY: PASS"
'

echo
echo "=== FINAL pg_stat_archiver ==="
compose exec --user postgres postgres \
  psql -d dante -P pager=off -c "
    SELECT
      archived_count,
      last_archived_wal,
      last_archived_time,
      failed_count,
      last_failed_wal,
      last_failed_time
    FROM pg_stat_archiver;
  "

echo
echo "=== POST-FAILURE pgBackRest CHECK ==="
compose exec --user postgres postgres \
  pgbackrest --stanza=dante check
echo "POST-FAILURE PGBACKREST CHECK: PASS"

echo
echo "=== FINAL pgBackRest INFO ==="
compose exec --user postgres postgres \
  pgbackrest --stanza=dante info

echo
echo "=== CP03 FAILURE/RECOVERY TEST COMPLETED ==="
