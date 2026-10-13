#!/usr/bin/env python3
"""Parallel full DANTE gate; the sequential reference runner is unchanged."""

from __future__ import annotations

import argparse
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from contextlib import redirect_stdout
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import tarfile
import tempfile
import time
from typing import TextIO

ROOT = Path(__file__).resolve().parents[2]
GATE = ROOT / "tooling/verify-all-current-tests-local.sh"
BRANCH = "feature/timeline-temporal-operational"
PG_TIMINGS = ROOT / "temp/POSTGRES_MODULE_TIMINGS.json"
GROUP_TIMINGS = ROOT / "temp/GATE_GROUP_TIMINGS.json"

READ_ONLY = (
    "DIFF_CHECK", "TEST_FILE_NAMES", "TEST_INTEGRITY", "BACKEND_FORMAT",
    "BACKEND_RUFF", "BACKEND_MYPY", "REPO_FORMAT", "REPO_ESLINT",
    "ARCHITECTURE", "OBSERVABILITY_STATIC", "BACKEND_NON_POSTGRES",
    "EVAL_TOOLING", "OBSERVABILITY_TOOLING", "FRONTEND_PROTOTYPE_CONTRACT",
    "WORLD_PROTOTYPE_CONTRACT", "I18N_TESTS", "TIME_TESTS",
)
SERIAL_BUILD = (
    "REPO_TYPECHECK", "GENERATED_DRIFT", "REPO_BUILD", "MOBILE_BUNDLE",
)
PACKAGE_TESTS = ("API_CLIENT_TESTS", "WEB_VITEST")
POSTGRES = "BACKEND_POSTGRES"
BROWSER = (
    "WEB_BROWSER_FIXTURE", "WEB_BROWSER_NONAUTH", "WEB_BROWSER_REAL_STACK",
)
EXPECTED = frozenset((*READ_ONLY, *SERIAL_BUILD, *PACKAGE_TESTS, POSTGRES, *BROWSER))


@dataclass(frozen=True)
class Task:
    name: str
    cwd: Path
    command: tuple[str, ...]


@dataclass(frozen=True)
class Result:
    name: str
    code: int
    seconds: float


def inventory() -> dict[str, Task]:
    """Read actual commands from the original gate and require exact parity."""
    tasks: dict[str, Task] = {}
    for line in GATE.read_text(encoding="utf-8").splitlines():
        if not re.match(r"^gate [A-Z][A-Z0-9_]+ ", line):
            continue
        parts = shlex.split(line)
        if len(parts) < 4:
            raise ValueError(f"Invalid gate declaration: {line}")
        _, name, relative_dir, *cmd = parts
        if name in tasks:
            raise ValueError(f"Duplicate test group: {name}")
        cwd = (ROOT / relative_dir).resolve()
        if not cwd.is_dir():
            raise ValueError(f"Missing gate directory: {cwd}")
        tasks[name] = Task(name, cwd, tuple(cmd))
    if set(tasks) != EXPECTED:
        raise ValueError(
            "Original inventory changed; reassess parallel isolation. "
            f"Added={sorted(set(tasks) - EXPECTED)} "
            f"Missing={sorted(EXPECTED - set(tasks))}"
        )
    return tasks


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def execute(
    task: Task, folder: Path, *, environment: dict[str, str] | None = None,
) -> Result:
    started = time.monotonic()
    with (folder / f"{task.name}.log").open("w", encoding="utf-8") as output:
        try:
            result = subprocess.run(
                task.command, cwd=task.cwd, stdout=output,
                stderr=subprocess.STDOUT, check=False,
                env={**os.environ, **environment} if environment else None,
            )
            code = result.returncode
        except OSError as exc:
            output.write(f"Unable to execute test group: {exc}\n")
            code = 2
    return Result(task.name, code, time.monotonic() - started)


def phase(
    names: tuple[str, ...], tasks: dict[str, Task], folder: Path, workers: int,
) -> list[Result]:
    print(f"PHASE: {', '.join(names)} (parallel={workers})", flush=True)
    completed: dict[str, Result] = {}
    with ThreadPoolExecutor(max_workers=workers) as pool:
        submitted = {
            pool.submit(execute, tasks[n], folder): n
            for n in _prioritize_groups(names)
        }
        for future in as_completed(submitted):
            name = submitted[future]
            try:
                result = future.result()
            except Exception as exc:
                (folder / f"{name}.log").write_text(
                    f"Orchestrator failed: {exc!r}\n", encoding="utf-8",
                )
                result = Result(name, 2, 0.0)
            completed[name] = result
            print(
                f"{'PASS' if result.code == 0 else 'FAIL'} {name}: "
                f"code={result.code}, {result.seconds:.1f}s", flush=True,
            )
    return [completed[name] for name in names]


def docker_prerequisites(folder: Path) -> bool:
    """Docker outage must not be misreported as an absent PostgreSQL image."""
    try:
        status = subprocess.run(
            ["docker", "info", "--format", "{{.ServerVersion}}"],
            cwd=ROOT, capture_output=True, text=True, timeout=30, check=False,
        )
        if status.returncode:
            raise RuntimeError(status.stderr.strip() or "Docker daemon stopped")
        image = subprocess.run(
            ["docker", "image", "inspect", "dante-postgres-local:18.6"],
            cwd=ROOT, capture_output=True, text=True, check=False,
        )
        if image.returncode:
            with (folder / "POSTGRES_IMAGE_BUILD.log").open("w") as log:
                result = subprocess.run(
                    ["docker", "compose", "-f", "infra/compose/local.yaml",
                     "build", "postgres"], cwd=ROOT, stdout=log,
                    stderr=subprocess.STDOUT, check=False,
                )
            if result.returncode:
                raise RuntimeError("PostgreSQL image build failed: see build log")
        return True
    except (OSError, subprocess.TimeoutExpired, RuntimeError) as exc:
        (folder / "POSTGRES_PREREQUISITE.log").write_text(
            f"Docker prerequisite failure: {exc}\n", encoding="utf-8",
        )
        print(f"DOCKER PREREQUISITE FAILED: {exc}", flush=True)
        return False


def postgres_collection(task: Task, folder: Path) -> list[str]:
    collected = subprocess.run(
        ("uv", "run", "--locked", "pytest", "--collect-only", "-q",
         "--no-cov", "-m", "postgres"),
        cwd=task.cwd, capture_output=True, text=True, check=False,
    )
    raw = collected.stdout + "\n" + collected.stderr
    (folder / "BACKEND_POSTGRES_COLLECT.log").write_text(raw, encoding="utf-8")
    if collected.returncode:
        raise RuntimeError(f"PostgreSQL collection exited {collected.returncode}")
    nodes = [
        line.strip() for line in collected.stdout.splitlines()
        if line.startswith("tests/") and "::" in line
    ]
    if not nodes or len(set(nodes)) != len(nodes):
        raise RuntimeError("Empty or duplicate PostgreSQL collection")
    matches = [int(x) for x in re.findall(r"(\d+) selected", raw)]
    if matches and matches[-1] != len(nodes):
        raise RuntimeError("Selected node count differs from collection total")
    return nodes


def _load_timings(path: Path) -> dict[str, float]:
    """Historical timings influence order only; never selection or acceptance."""
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError, TypeError):
        return {}
    if not isinstance(raw, dict):
        return {}
    return {
        key: float(value)
        for key, value in raw.items()
        if isinstance(key, str)
        and isinstance(value, (int, float))
        and not isinstance(value, bool)
        and 0 < float(value) < 100_000
    }


def shard_modules(
    nodes: list[str], workers: int, jobs_per_worker: int = 3,
    timings: dict[str, float] | None = None,
) -> list[list[str]]:
    """Build module-atomic, duration-balanced jobs for a refilling worker pool.

    Each module is exactly once in the entire queue, preserving its existing
    pytest order and module/session fixture semantics. Historical runtimes
    (when available) replace inaccurate test-count-only weighting. The next
    queued job is automatically assigned to the next free worker.
    """
    by_file: dict[str, list[str]] = defaultdict(list)
    for node in nodes:
        by_file[node.partition("::")[0]].append(node)
    count = min(len(by_file), workers * jobs_per_worker)
    if count == 0:
        raise RuntimeError("No selected PostgreSQL modules")
    weights = timings or {}
    result: list[list[str]] = [[] for _ in range(count)]
    totals = [0.0] * count

    def cost(module: str, cases: list[str]) -> float:
        return weights.get(module, float(len(cases)))

    # Largest/slowest modules are scheduled first. Greedy least-loaded packing
    # keeps each job similar in observed cost without breaking module fixtures.
    modules = sorted(
        by_file.items(), key=lambda item: (-cost(*item), item[0]),
    )
    for module, tests in modules:
        target = min(range(count), key=lambda i: (totals[i], i))
        result[target].extend(tests)
        totals[target] += cost(module, tests)
    if not all(result):
        raise RuntimeError("Empty PostgreSQL work item")
    flattened = [node for job in result for node in job]
    if len(flattened) != len(nodes) or set(flattened) != set(nodes):
        raise RuntimeError("PostgreSQL work queue lost or duplicated tests")
    return result


_PYTEST_DURATION = re.compile(
    r"^\\s*(\\d+(?:\\.\\d+)?)s\\s+(?:setup|call|teardown)\\s+"
    r"(tests/[^\\s:]+\\.py)(?:::|\\s|$)"
)


def _observed_module_timings(
    plans: dict[str, list[str]], folder: Path,
) -> dict[str, float]:
    """Extract actual per-module pytest setup/call/teardown durations."""
    totals: dict[str, float] = defaultdict(float)
    for name in plans:
        lines = (folder / f"{name}.log").read_text(
            encoding="utf-8", errors="replace",
        ).splitlines()
        for line in lines:
            match = _PYTEST_DURATION.match(line)
            if match:
                totals[match.group(2)] += float(match.group(1))
    return dict(totals)


def _prioritize_groups(names: tuple[str, ...]) -> tuple[str, ...]:
    """Dispatch previously slow independent checks first, avoiding long tails."""
    measured = _load_timings(GROUP_TIMINGS)
    fallback = {
        "BACKEND_NON_POSTGRES": 42.0,
        "REPO_ESLINT": 40.0,
        "WEB_VITEST": 32.0,
        "REPO_FORMAT": 12.0,
        "BACKEND_MYPY": 3.0,
    }
    return tuple(sorted(
        names, key=lambda name: (-measured.get(name, fallback.get(name, 1.0)), name),
    ))


def self_test_scheduler() -> None:
    """Validate coverage, no duplicates, module ordering and a deeper queue."""
    nodes = [
        f"tests/integration/database/test_module_{module:02d}.py::case_{case:02d}"
        for module in range(24)
        for case in range((module % 9) + 1)
    ]
    for capacity in (1, 5, 10):
        chunks = shard_modules(nodes, capacity)
        assert len(chunks) == min(24, capacity * 3)
        seen = [node for chunk in chunks for node in chunk]
        assert len(seen) == len(set(seen)) == len(nodes)
        assert set(seen) == set(nodes)
        owners = {}
        for index, chunk in enumerate(chunks):
            for node in chunk:
                module = node.partition("::")[0]
                if module in owners:
                    assert owners[module] == index
                owners[module] = index
                case_nodes = [n for n in chunk if n.startswith(module + "::")]
                assert case_nodes == [n for n in nodes if n.startswith(module + "::")]
        assert len(owners) == 24
    # Duration estimates rebalance jobs but never alter module ownership.
    profiled = shard_modules(nodes, 3, timings={
        "tests/integration/database/test_module_00.py": 1_000.0,
    })
    assert profiled[0][0].startswith("tests/integration/database/test_module_00.py::")
    assert set(node for job in profiled for node in job) == set(nodes)
    assert _PYTEST_DURATION.match("1.25s setup tests/integration/foo/test_bar.py::test_a")
    assert not _PYTEST_DURATION.match("55 passed in 1.25s")
    assert docker_only_interruption(
        2, "Disposable PostgreSQL could not start: ports are not available"
    )
    assert docker_only_interruption(
        2, "Disposable PostgreSQL became unavailable during database cleanup"
    )
    assert not docker_only_interruption(
        1, "FAILED tests/integration/test_real_rule.py"
    )
    assert not docker_only_interruption(
        2, "FAILED tests/integration/test_real_rule.py\\nDisposable PostgreSQL could not start"
    )
    print("PASS: dynamic scheduler and infrastructure-only retries preserve coverage")


def docker_only_interruption(code: int, output: str) -> bool:
    """Retry an unexecuted/interrupted cluster, never an assertion failure."""
    if code != 2 or "FAILED tests/" in output:
        return False
    return any(signal in output for signal in (
        "Disposable PostgreSQL could not start",
        "Disposable PostgreSQL became unavailable during database cleanup",
        "PostgreSQL acceptance cluster did not become ready",
    ))


def postgres_phase(
    task: Task, folder: Path, workers: int, jobs_per_worker: int = 3,
) -> Result:
    start = time.monotonic()
    log = folder / "BACKEND_POSTGRES.log"
    try:
        all_nodes = postgres_collection(task, folder)
        shards = shard_modules(
            all_nodes, workers, jobs_per_worker, _load_timings(PG_TIMINGS),
        )
    except Exception as exc:
        log.write_text(f"PostgreSQL collection failed: {exc}\n", encoding="utf-8")
        return Result(POSTGRES, 2, time.monotonic() - start)

    plans = {
        f"BACKEND_POSTGRES_SHARD_{i:02d}": tests
        for i, tests in enumerate(shards, 1)
    }
    (folder / "BACKEND_POSTGRES_SHARD_PLAN.json").write_text(
        json.dumps(plans, indent=2) + "\n", encoding="utf-8",
    )
    commands = {
        name: Task(name, task.cwd, (
            "uv", "run", "--locked", "pytest", "-q", "--no-cov",
            "--tb=short", "--durations=0", "-m", "postgres", *tests,
        ))
        for name, tests in plans.items()
    }
    print(
        f"POSTGRES: {len(all_nodes)} tests; {len(commands)} queued jobs, "
        f"max {workers} simultaneous isolated PostgreSQL containers",
        flush=True,
    )
    # Executor work queue is deliberately longer than its pool. Completing
    # one job immediately starts the next, avoiding fixed-shard long tails.
    results = phase(tuple(commands), commands, folder, workers)
    # Docker Desktop can reject simultaneous loopback port mappings or
    # restart a disposable cluster under load. Retry *only* precisely
    # classified infrastructure interruptions once, serially, after the
    # parallel queue drains. The exact module nodes and assertions rerun;
    # the original failure log is retained alongside the recovery log.
    recovered: list[Result] = []
    for original in results:
        output = (folder / f"{original.name}.log").read_text(
            encoding="utf-8", errors="replace",
        )
        if not docker_only_interruption(original.code, output):
            recovered.append(original)
            continue
        retry_name = f"{original.name}_RETRY_01"
        print(
            f"DOCKER INFRASTRUCTURE ONLY: retry {original.name} once in "
            "isolation without relaxing any selected tests", flush=True,
        )
        repeat = execute(
            Task(retry_name, commands[original.name].cwd,
                 commands[original.name].command),
            folder,
        )
        recovered.append(Result(
            original.name, repeat.code, original.seconds + repeat.seconds,
        ))
        print(
            f"{'PASS' if repeat.code == 0 else 'FAIL'} {retry_name}: "
            f"code={repeat.code}, {repeat.seconds:.1f}s",
            flush=True,
        )
    results = recovered
    observed = _observed_module_timings(plans, folder)
    if observed:
        merged = {**_load_timings(PG_TIMINGS), **observed}
        PG_TIMINGS.parent.mkdir(parents=True, exist_ok=True)
        PG_TIMINGS.write_text(
            json.dumps(merged, indent=2, sort_keys=True) + "\\n",
            encoding="utf-8",
        )
    (folder / "BACKEND_POSTGRES_SHARD_TIMINGS.json").write_text(
        json.dumps([
            {
                "name": r.name, "seconds": r.seconds,
                "exit_code": r.code, "tests": len(plans[r.name]),
                "modules": sorted({n.partition("::")[0] for n in plans[r.name]}),
            }
            for r in results
        ], indent=2) + "\\n", encoding="utf-8",
    )
    lines = [
        f"Collected PostgreSQL tests: {len(all_nodes)}",
        f"Dynamic PostgreSQL jobs: {len(commands)}",
        f"Maximum simultaneous disposable clusters: {workers}",
    ]
    for r in results:
        path = folder / f"{r.name}.log"
        tail = path.read_text(encoding="utf-8", errors="replace").splitlines()[-15:]
        lines += [f"{r.name}: {len(plans[r.name])} tests, exit={r.code}",
                  *tail, ""]
    log.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return Result(
        POSTGRES, 0 if all(r.code == 0 for r in results) else 1,
        time.monotonic() - start,
    )


def keep_browser_evidence(name: str, folder: Path) -> None:
    source = ROOT / "apps/web/test-results"
    if not source.is_dir():
        return
    dest = folder / f"{name}_BROWSER_ARTIFACTS"
    files = [*sorted(source.rglob("error-context.md")),
             *sorted(source.rglob("trace.zip"))[:3]]
    for file in files:
        target = dest / file.relative_to(source)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(file, target)


def final_report(
    tasks: dict[str, Task], outcomes: list[Result], folder: Path,
    sha: str, start: float,
) -> int:
    by_name = {result.name: result for result in outcomes}
    stable = git("rev-parse", "HEAD") == sha and not git("status", "--porcelain")
    success = stable and len(by_name) == len(tasks) and all(
        r.code == 0 for r in outcomes
    )
    lines = [
        "# DANTE full parallel gate", "",
        f"- SHA: {sha}",
        f"- Captured (UTC): {datetime.now(UTC).isoformat()}",
        f"- Groups: {len(by_name)}/{len(tasks)}",
        f"- Source stability: {'PASS' if stable else 'FAIL'}",
        f"- Elapsed: {time.monotonic() - start:.1f}s", "",
        "| Group | Exit | Seconds |", "| --- | ---: | ---: |",
    ]
    for name in tasks:
        r = by_name.get(name)
        if r is None:
            lines.append(f"| {name} | NOT RUN | — |")
        else:
            lines.append(f"| {name} | {r.code} | {r.seconds:.1f} |")
    lines += ["", "## Failing groups", ""]
    for name, r in by_name.items():
        if r.code != 0:
            log = (folder / f"{name}.log").read_text(
                encoding="utf-8", errors="replace",
            ).splitlines()
            signals = [line[:500] for line in log if re.search(
                r"FAILED|ERROR|Traceback|error:|Error:|assert", line,
            )]
            lines += [f"### {name}", "~~~text", *(signals[:25] or log[-15:]),
                      "~~~", ""]
    text = "\n".join(lines) + "\n"
    (folder / "FULL_GATE_SUMMARY.md").write_text(text, encoding="utf-8")
    (ROOT / "temp/LATEST_GATE_SUMMARY.md").write_text(text, encoding="utf-8")
    (ROOT / "temp/LATEST_GATE_DIR.txt").write_text(str(folder) + "\n")
    manifest = {
        "sha": sha, "source_stable": stable, "exit_code": int(not success),
        "groups": [
            {"name": name, "exit_code": by_name[name].code if name in by_name else None,
             "seconds": by_name[name].seconds if name in by_name else None}
            for name in tasks
        ],
    }
    (folder / "FULL_GATE_REPORT.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8",
    )
    GROUP_TIMINGS.write_text(
        json.dumps({r.name: r.seconds for r in outcomes}, indent=2) + "\n",
        encoding="utf-8",
    )
    sys.stdout.flush()
    archive = folder / "FULL_GATE_LOGS.tar.gz"
    with tarfile.open(archive, "w:gz") as out:
        for file in sorted(folder.rglob("*")):
            if file.is_file() and file != archive:
                out.add(file, arcname=file.relative_to(folder))
    print(f"GROUPS={len(by_name)}/{len(tasks)}", flush=True)
    print(f"SOURCE_STABILITY={int(not stable)}", flush=True)
    print(f"FULL_GATE_EXIT={int(not success)}", flush=True)
    print(f"SUMMARY={folder / 'FULL_GATE_SUMMARY.md'}", flush=True)
    print(f"ARCHIVE={archive}", flush=True)
    return int(not success)


class _Tee:
    def __init__(self, terminal: TextIO, log: TextIO) -> None:
        self.terminal = terminal
        self.log = log

    def write(self, text: str) -> None:
        self.terminal.write(text)
        self.log.write(text)

    def flush(self) -> None:
        self.terminal.flush()
        self.log.flush()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--group-workers", type=int, default=3,
        help="Independent concurrent groups (1-8; default 3)",
    )
    parser.add_argument(
        "--postgres-workers", type=int, default=5,
        help="Independent PostgreSQL clusters (1-10; default 5)",
    )
    parser.add_argument(
        "--postgres-jobs-per-worker", type=int, default=4,
        help="Queue depth per worker for balancing module durations (2-8; default 4)",
    )
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if not 1 <= args.group_workers <= 8:
        parser.error("--group-workers must be between 1 and 8")
    if not 1 <= args.postgres_workers <= 10:
        parser.error("--postgres-workers must be between 1 and 10")
    if not 2 <= args.postgres_jobs_per_worker <= 8:
        parser.error("--postgres-jobs-per-worker must be between 2 and 8")
    if args.postgres_workers >= 8:
        print(
            "WARNING: 8-10 PostgreSQL workers run 8-10 real PostGIS "
            "containers; sufficient Docker RAM and CPU are required.",
            flush=True,
        )

    tasks = inventory()
    if args.self_test:
        self_test_scheduler()
        return 0
    stages = [
        ("Independent read-only", READ_ONLY, args.group_workers),
        ("Build and generated sources", SERIAL_BUILD, 1),
        ("Package tests", PACKAGE_TESTS, args.group_workers),
        ("Isolated PostgreSQL work queue", (POSTGRES,), args.postgres_workers),
        ("Browser shared outputs", BROWSER, 1),
    ]
    if args.dry_run:
        for label, names, count in stages:
            print(f"{label}: groups={len(names)}, concurrency={count}")
            for name in names:
                print(f"  {name}: {' '.join(tasks[name].command)}")
        print(f"TOTAL={len(tasks)}; original sequential gate untouched")
        return 0

    if git("branch", "--show-current") != BRANCH or git("status", "--porcelain"):
        print(f"STOP: a clean checkout of {BRANCH} is required", file=sys.stderr)
        return 2
    sha = git("rev-parse", "HEAD")
    started = time.monotonic()
    output = ROOT / "temp"
    output.mkdir(exist_ok=True)
    folder = Path(tempfile.mkdtemp(prefix="dante-parallel-gate.", dir=output))
    with (folder / "CONSOLE.log").open("w", encoding="utf-8") as console:
        with redirect_stdout(_Tee(sys.stdout, console)):
            print(f"HEAD={sha} LOG_DIR={folder}", flush=True)
            if not docker_prerequisites(folder):
                return 2
            outcomes: list[Result] = []
            # PostgreSQL has its own bounded, dynamically refilled pool.
            # Start it alongside independent groups: it continues working
            # while shorter groups finish and while build checks run in
            # their separate serial writer lane. No other gate writes to
            # its disposable clusters.
            with ThreadPoolExecutor(max_workers=1) as postgres_dispatcher:
                pg_future = postgres_dispatcher.submit(
                    postgres_phase, tasks[POSTGRES], folder,
                    args.postgres_workers, args.postgres_jobs_per_worker,
                )
                outcomes.extend(phase(READ_ONLY, tasks, folder, args.group_workers))
                outcomes.extend(phase(SERIAL_BUILD, tasks, folder, 1))
                outcomes.extend(phase(PACKAGE_TESTS, tasks, folder, args.group_workers))
                try:
                    outcomes.append(pg_future.result())
                except Exception as exc:
                    (folder / "BACKEND_POSTGRES.log").write_text(
                        f"PostgreSQL orchestrator failure: {exc!r}\n",
                        encoding="utf-8",
                    )
                    outcomes.append(Result(POSTGRES, 2, 0.0))
            for name in BROWSER:
                result = execute(tasks[name], folder)
                outcomes.append(result)
                print(
                    f"{'PASS' if result.code == 0 else 'FAIL'} "
                    f"{name} code={result.code} {result.seconds:.1f}s", flush=True,
                )
                try:
                    keep_browser_evidence(name, folder)
                except OSError as exc:
                    (folder / f"{name}_BROWSER_CAPTURE_ERROR.log").write_text(
                        f"Browser diagnostic copy failed: {exc}\n", encoding="utf-8",
                    )
            return final_report(tasks, outcomes, folder, sha, started)


if __name__ == "__main__":
    sys.exit(main())
