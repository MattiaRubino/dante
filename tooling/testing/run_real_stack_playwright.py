#!/usr/bin/env python3
"""Run all real-stack Playwright projects against separate disposable stacks.

The reference single-worker invocation is deliberately preserved as a fallback.
Every parallel shard owns its HTTP port, PostgreSQL, SMTP capture, user sessions,
and Playwright artifacts. Never parallelize projects on the same stack: some tests
intentionally stop PostgreSQL to assert truthful outage/recovery behavior.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import socket
import subprocess
import sys
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import asdict, dataclass
from pathlib import Path
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parents[2]
WEB = ROOT / "apps" / "web"
PROJECTS = ("chromium", "firefox", "webkit")
COLLECTED_TESTS = re.compile(
    r"^Total:\s*(\d+)\s+tests?\s+in\s+\d+\s+files?\s*$", re.M
)
# Reference successful 2026-11-09 gate: 117 test slots, four intentional skips.
# A new skip requires review; a formerly skipped test becoming active is fine.
MAX_BASELINE_SKIPS = 4


@dataclass(frozen=True, slots=True)
class ShardResult:
    project: str
    port: int
    discovered: int
    recorded: int
    passed: int
    skipped: int
    failed: int
    errors: int
    exit_code: int
    seconds: float


def _free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
        probe.bind(("127.0.0.1", 0))
        return int(probe.getsockname()[1])


def _unique_ports() -> dict[str, int]:
    ports: dict[str, int] = {}
    for project in PROJECTS:
        port = _free_port()
        while port in ports.values():
            port = _free_port()
        ports[project] = port
    return ports


def _plan(project: str, directory: Path) -> int:
    command = (
        "pnpm", "exec", "playwright", "test", "--config",
        "playwright.auth.config.ts", "--project", project, "--list",
    )
    result = subprocess.run(
        command, cwd=WEB, text=True, capture_output=True, check=False,
    )
    output = result.stdout + "\n" + result.stderr
    (directory / f"{project}.inventory.log").write_text(output, encoding="utf-8")
    if result.returncode:
        raise RuntimeError(
            f"Playwright inventory for {project} failed: {result.returncode}"
        )
    matches = COLLECTED_TESTS.findall(output)
    if len(matches) != 1 or int(matches[0]) < 1:
        raise RuntimeError(
            f"Cannot establish a unique positive inventory for {project}"
        )
    return int(matches[0])


def _junit_counts(report: Path) -> tuple[int, int, int, int]:
    """Count concrete JUnit testcases, not summary strings or reporter labels."""
    root = ElementTree.parse(report).getroot()
    cases = root.findall(".//testcase")
    if not cases:
        raise RuntimeError(f"JUnit report contains no testcases: {report}")
    recorded = len(cases)
    skipped = sum(case.find("skipped") is not None for case in cases)
    failed = sum(case.find("failure") is not None for case in cases)
    errors = sum(case.find("error") is not None for case in cases)
    return recorded, skipped, failed, errors


def _validate_coverage(planned: dict[str, int], results: list[ShardResult]) -> None:
    if set(planned) != set(PROJECTS) or set(planned) != {r.project for r in results}:
        raise RuntimeError("Browser inventory differs from the three required projects")
    if len(results) != len(PROJECTS):
        raise RuntimeError("Browser sharding dropped or duplicated a project")
    for result in results:
        if result.recorded != planned[result.project]:
            raise RuntimeError(
                f"{result.project}: collected {planned[result.project]}, "
                f"JUnit recorded {result.recorded}; a test was lost or duplicated"
            )
    if sum(r.skipped for r in results) > MAX_BASELINE_SKIPS:
        raise RuntimeError(
            "Playwright skipped more tests than the known green baseline; "
            "review newly skipped cases before accepting this run"
        )


def _run_project(
    project: str, port: int, discovered: int, directory: Path,
) -> ShardResult:
    shard = directory / project
    shard.mkdir(parents=True, exist_ok=False)
    junit = shard / "junit.xml"
    env = {
        **os.environ,
        "DANTE_E2E_WEB_PORT": str(port),
        "DANTE_E2E_PREBUILT_WEB": "1",
        "PLAYWRIGHT_JUNIT_OUTPUT_FILE": str(junit),
    }
    command = (
        "pnpm", "exec", "playwright", "test", "--config",
        "playwright.auth.config.ts", "--project", project, "--workers=1",
        "--retries=0", "--reporter=line,junit", "--output",
        str(shard / "test-results"),
    )
    started = time.monotonic()
    with (shard / "playwright.log").open("w", encoding="utf-8") as log:
        completed = subprocess.run(
            command, cwd=WEB, env=env, stdout=log, stderr=subprocess.STDOUT,
            check=False,
        )
    seconds = time.monotonic() - started
    try:
        recorded, skipped, failed, errors = _junit_counts(junit)
    except (OSError, ElementTree.ParseError, RuntimeError) as exc:
        # No report is always a failure even if the child returns success.
        (shard / "report-error.txt").write_text(f"{exc}\n", encoding="utf-8")
        recorded, skipped, failed, errors = 0, 0, 0, 1
    return ShardResult(
        project=project, port=port, discovered=discovered, recorded=recorded,
        passed=recorded - skipped - failed - errors, skipped=skipped,
        failed=failed, errors=errors, exit_code=completed.returncode,
        seconds=round(seconds, 2),
    )


def _self_test() -> None:
    import io

    payload = """<testsuites><testsuite tests="3"><testcase name="one"/>
    <testcase name="two"><skipped/></testcase>
    <testcase name="three"><failure/></testcase></testsuite></testsuites>"""
    root = ElementTree.parse(io.StringIO(payload)).getroot()
    cases = root.findall(".//testcase")
    assert len(cases) == 3
    assert sum(c.find("skipped") is not None for c in cases) == 1
    assert sum(c.find("failure") is not None for c in cases) == 1
    planned = {project: 2 for project in PROJECTS}
    valid = [
        ShardResult(project, 10000 + i, 2, 2, 2, 0, 0, 0, 0, 1.0)
        for i, project in enumerate(PROJECTS)
    ]
    _validate_coverage(planned, valid)
    for invalid in (valid[:-1], [*valid[:2], valid[1]]):
        try:
            _validate_coverage(planned, invalid)
        except RuntimeError:
            pass
        else:
            raise AssertionError("Missing/duplicated browser shard must fail")
    bad = [*valid[:2], ShardResult("webkit", 123, 2, 1, 1, 0, 0, 0, 0, 1.0)]
    try:
        _validate_coverage(planned, bad)
    except RuntimeError:
        pass
    else:
        raise AssertionError("Missing JUnit test must fail")
    assert COLLECTED_TESTS.findall("Total: 39 tests in 10 files\n") == ["39"]
    print("PASS: browser shard partition, inventory parity and skip guard")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--workers", type=int,
        default=int(os.environ.get("DANTE_E2E_REAL_STACK_WORKERS", "3")),
        help="Independent browser stacks (1-3; 1 retains the reference runner)",
    )
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        _self_test()
        return 0
    if not 1 <= args.workers <= len(PROJECTS):
        parser.error("--workers must be between 1 and 3")
    if args.workers == 1:
        # Bit-for-bit equivalent selection and startup behavior to the
        # last all-green gate; no new sharding assumptions in fallback.
        port = _free_port()
        env = {**os.environ, "DANTE_E2E_WEB_PORT": str(port)}
        print(f"DANTE_E2E_WEB_PORT={port}; reference serial real-stack", flush=True)
        return subprocess.run(
            [
                "pnpm", "exec", "playwright", "test", "--config",
                "playwright.auth.config.ts",
            ],
            cwd=WEB, env=env, check=False,
        ).returncode

    (ROOT / "temp").mkdir(parents=True, exist_ok=True)
    explicit = os.environ.get("DANTE_E2E_REAL_STACK_ARTIFACTS_DIR")
    directory = (
        Path(explicit).resolve()
        if explicit
        else Path(tempfile.mkdtemp(prefix="dante-realstack-", dir=ROOT / "temp"))
    )
    directory.mkdir(parents=True, exist_ok=True)
    started = time.monotonic()
    report = directory / "summary.json"
    try:
        planned = {project: _plan(project, directory) for project in PROJECTS}
        print(f"REALSTACK: discovered {planned}, total={sum(planned.values())}", flush=True)
        # The production wrapper normally configures these Vite feature flags
        # before building. Preserve exactly the same build contract here.
        build_env = {
            **os.environ,
            "VITE_DANTE_APPLE_ENABLED": "true",
            "VITE_DANTE_PASSKEY_ENABLED": "true",
        }
        with (directory / "web-build.log").open("w", encoding="utf-8") as log:
            build = subprocess.run(
                ["pnpm", "--filter", "@dante/web", "build"],
                cwd=ROOT, env=build_env, stdout=log,
                stderr=subprocess.STDOUT, check=False,
            )
        if build.returncode:
            raise RuntimeError(f"Shared frontend build failed ({build.returncode})")
        ports = _unique_ports()
        completed: dict[str, ShardResult] = {}
        with ThreadPoolExecutor(max_workers=args.workers) as pool:
            futures = {
                pool.submit(_run_project, p, ports[p], planned[p], directory): p
                for p in PROJECTS
            }
            for future in as_completed(futures):
                project = futures[future]
                result = future.result()
                completed[project] = result
                print(
                    f"REALSTACK {project}: exit={result.exit_code} "
                    f"recorded={result.recorded}/{result.discovered} "
                    f"passed={result.passed} skipped={result.skipped} "
                    f"failed={result.failed} errors={result.errors} "
                    f"seconds={result.seconds}", flush=True,
                )
        results = [completed[p] for p in PROJECTS]
        _validate_coverage(planned, results)
        success = all(r.exit_code == 0 and r.failed == 0 and r.errors == 0 for r in results)
        report.write_text(
            json.dumps({
                "workers": args.workers,
                "elapsed_seconds": round(time.monotonic() - started, 2),
                "discovered": sum(planned.values()),
                "recorded": sum(r.recorded for r in results),
                "skipped": sum(r.skipped for r in results),
                "passed": sum(r.passed for r in results),
                "exit_code": 0 if success else 1,
                "projects": [asdict(r) for r in results],
            }, indent=2) + "\n", encoding="utf-8",
        )
        print(f"REALSTACK_REPORT={report}", flush=True)
        return int(not success)
    except (OSError, RuntimeError, subprocess.SubprocessError) as exc:
        (directory / "orchestrator-error.txt").write_text(
            f"{type(exc).__name__}: {exc}\n", encoding="utf-8",
        )
        print(f"REALSTACK ERROR: {exc}", file=sys.stderr, flush=True)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
