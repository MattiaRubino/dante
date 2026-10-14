#!/usr/bin/env bash
# Complete DANTE acceptance gate with hardware-aware process concurrency.
# Runs the unmodified 27-group inventory, preserving all test/assertion checks.
# PostgreSQL shards remain dynamically refilled and browser real-stack isolated.
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"
BRANCH="feature/timeline-temporal-operational"
if [[ "$(git branch --show-current)" != "$BRANCH" ]]; then
  echo "STOP: checkout must be on $BRANCH" >&2
  exit 2
fi
if [[ -n "$(git status --porcelain)" ]]; then
  echo "STOP: worktree not clean; the full gate requires an unchanged source SHA." >&2
  git status --short
  exit 2
fi

# Count only CPUs available to the current WSL process, and honor Docker's
# separate CPU and RAM limits. Docker information is deliberately not guessed.
host_cpu="$(nproc 2>/dev/null || printf '4')"
if ! [[ "$host_cpu" =~ ^[0-9]+$ ]] || (( host_cpu < 1 )); then
  host_cpu=4
fi
docker_cpu=0
docker_mem=0
docker_limits="$(docker info --format '{{.NCPU}} {{.MemTotal}}' 2>/dev/null || true)"
read -r docker_cpu docker_mem <<< "$docker_limits"
if ! [[ "$docker_cpu" =~ ^[0-9]+$ ]] || (( docker_cpu < 1 )); then
  docker_cpu="$host_cpu"
fi
if ! [[ "$docker_mem" =~ ^[0-9]+$ ]] || (( docker_mem < 1 )); then
  # Unknown Docker memory: choose the conservative tier, never assume 32GB.
  docker_mem=0
fi
cpus="$host_cpu"
if (( docker_cpu < cpus )); then cpus="$docker_cpu"; fi

# WSL host memory can be more restrictive than Docker's advertised limit.
available_kib="$(awk '/^MemAvailable:/ {print $2; exit}' /proc/meminfo 2>/dev/null || true)"
mem_bytes="$docker_mem"
if [[ "$available_kib" =~ ^[0-9]+$ ]] && (( available_kib > 0 )); then
  available_bytes=$(( available_kib * 1024 ))
  if (( mem_bytes == 0 || available_bytes < mem_bytes )); then
    mem_bytes="$available_bytes"
  fi
fi
mem_gib=$(( mem_bytes / 1073741824 ))

# Group jobs run external processes: Python threads here are a dispatcher,
# not CPU-bound GIL workers. The upper bound is the actual runner limit.
# Eight simultaneous Docker clusters are opt-in automatically only with
# substantial CPU/RAM headroom: seven previously caused two transient
# Docker port failures on a smaller acceptance run.
if (( cpus >= 24 && mem_gib >= 24 )); then
  group_workers=8
  pg_workers=8
  browser_workers=5
elif (( cpus >= 14 && mem_gib >= 12 )); then
  group_workers=8
  pg_workers=7
  browser_workers=4
elif (( cpus >= 10 && mem_gib >= 9 )); then
  group_workers=7
  pg_workers=6
  browser_workers=4
elif (( cpus >= 8 && mem_gib >= 7 )); then
  group_workers=6
  pg_workers=5
  browser_workers=3
elif (( cpus >= 6 && mem_gib >= 5 )); then
  group_workers=5
  pg_workers=4
  browser_workers=3
else
  group_workers=4
  pg_workers=3
  browser_workers=2
fi

# Expert overrides remain bounded by the underlying validated runner.
group_workers="${DANTE_GATE_GROUP_WORKERS:-$group_workers}"
pg_workers="${DANTE_GATE_PG_WORKERS:-$pg_workers}"
browser_workers="${DANTE_GATE_BROWSER_WORKERS:-$browser_workers}"
jobs_per_worker="${DANTE_GATE_PG_JOBS_PER_WORKER:-3}"
if ! [[ "$group_workers" =~ ^[0-9]+$ ]] || (( group_workers < 1 || group_workers > 8 )); then
  echo "STOP: DANTE_GATE_GROUP_WORKERS must be 1..8" >&2; exit 2
fi
if ! [[ "$pg_workers" =~ ^[0-9]+$ ]] || (( pg_workers < 1 || pg_workers > 10 )); then
  echo "STOP: DANTE_GATE_PG_WORKERS must be 1..10" >&2; exit 2
fi
if ! [[ "$browser_workers" =~ ^[0-9]+$ ]] || (( browser_workers < 1 || browser_workers > 6 )); then
  echo "STOP: DANTE_GATE_BROWSER_WORKERS must be 1..6" >&2; exit 2
fi
if ! [[ "$jobs_per_worker" =~ ^[0-9]+$ ]] || (( jobs_per_worker < 2 || jobs_per_worker > 8 )); then
  echo "STOP: DANTE_GATE_PG_JOBS_PER_WORKER must be 2..8" >&2; exit 2
fi

mkdir -p temp
log="temp/FULL_GATE_ADAPTIVE_CONSOLE.log"
{
  echo "SOURCE_SHA=$(git rev-parse HEAD)"
  echo "AVAILABLE_CPUS=$cpus (WSL=$host_cpu, Docker=$docker_cpu)"
  echo "AVAILABLE_MEMORY_GIB=$mem_gib"
  echo "GROUP_WORKERS=$group_workers POSTGRES_WORKERS=$pg_workers"
  echo "PG_JOBS_PER_WORKER=$jobs_per_worker NONAUTH_BROWSER_WORKERS=$browser_workers"
  echo "TOTAL_SIMULTANEOUS_GROUP_AND_PG_WORKERS=$((group_workers + pg_workers))"
  echo "TEST_POLICY=all_27_groups_no_skips_no_retries_for_assertion_failures"
  echo "REAL_STACK=single_worker_after_postgres_isolation"
} | tee "$log"

# Sanity-check the refilling queue and its exact/unique test coverage before
# launching hundreds of real database cases.
python3 tooling/testing/run_parallel_gate.py --self-test 2>&1 | tee -a "$log"

set +e
python3 tooling/testing/run_parallel_gate.py \
  --group-workers "$group_workers" \
  --postgres-workers "$pg_workers" \
  --postgres-jobs-per-worker "$jobs_per_worker" \
  --nonauth-workers "$browser_workers" \
  2>&1 | tee -a "$log"
result=${PIPESTATUS[0]}
set -e

echo "FULL_GATE_EXIT=$result"
if [[ -f temp/LATEST_GATE_DIR.txt ]]; then
  folder="$(cat temp/LATEST_GATE_DIR.txt)"
  if [[ -f "$folder/FULL_GATE_SUMMARY.md" ]]; then
    echo "SUMMARY=$folder/FULL_GATE_SUMMARY.md"
  fi
  if [[ -f "$folder/FULL_GATE_LOGS.tar.gz" ]]; then
    echo "UPLOAD_THIS_ARCHIVE=$folder/FULL_GATE_LOGS.tar.gz"
  fi
fi
exit "$result"
