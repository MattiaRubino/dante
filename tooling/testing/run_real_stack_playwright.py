#!/usr/bin/env python3
"""Run all real-stack Playwright projects against separate disposable stacks.

The reference single-worker invocation is deliberately preserved as a fallback.
Every parallel shard owns its HTTP port, PostgreSQL, SMTP capture, user sessions,
and Playwright artifacts. Never parallelize projects on the same stack: some tests
intentionally stop PostgreSQL to assert truthful outage/recovery behavior.
"""

from __future__ import annotations

import argparse
import ast
import json
import os
import re
import signal
import socket
import subprocess
import sys
import tarfile
import tempfile
import time
import zipfile
from concurrent.futures import FIRST_COMPLETED, ThreadPoolExecutor, wait
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


@dataclass(frozen=True, slots=True)
class ChromiumRun:
    name: str
    grep: str
    invert: bool
    shard: str | None
    workers: int


LEGACY_CHROMIUM = ChromiumRun("chromium-legacy", "V2-", True, None, 1)
V2_TITLE_ID = re.compile(r"^(V2-[A-Z0-9-]+)(?:\s|$)")
# Approximate seconds per journey from the 117-case interrupted Chromium run.
# These weights only distribute work; live --list and JUnit prove coverage.
V2_PHASE_SECONDS = {"P1": 35, "P2": 75, "P3": 110}


class GateTimeout(RuntimeError):
    """The bounded full Chromium run ended before its inventory completed."""


def _chromium_args(run: ChromiumRun) -> tuple[str, ...]:
    return (
        "--grep-invert" if run.invert else "--grep", run.grep,
        *(("--shard", run.shard) if run.shard else ()),
        *(("--fully-parallel",) if run.workers > 1 else ()),
    )


def _chromium_inventory(output: str) -> set[str]:
    """Use Playwright's listed case identities to prove exact shard coverage."""
    return {
        line.strip() for line in output.splitlines()
        if line.strip().startswith("[chromium] › ")
    }


def _balanced_chromium_runs(full: set[str]) -> tuple[ChromiumRun, ...]:
    """Balance estimated journey time instead of Playwright's test count.

    Every V2 test keeps its own Playwright/account identity and each run has
    its own disposable stack. Unknown future V2 IDs receive a conservative
    default weight; the full inventory equality still guards new test cases.
    """
    cases: dict[str, int] = {}
    for title in full:
        name = title.rsplit(" › ", 1)[-1]
        if not name.startswith("V2-"):
            continue
        match = V2_TITLE_ID.match(name)
        if match is None or match.group(1) in cases:
            raise RuntimeError("V2 case titles must have unique stable IDs")
        case_id = match.group(1)
        phase = case_id.split("-", 2)[1]
        cases[case_id] = V2_PHASE_SECONDS.get(phase, 90)
    if len(cases) < 2:
        raise RuntimeError("Cannot distribute fewer than two V2 cases")
    bins: list[list[str]] = [[], []]
    seconds = [0, 0]
    for case_id, weight in sorted(cases.items(), key=lambda item: (-item[1], item[0])):
        index = min(range(2), key=lambda i: (seconds[i], len(bins[i])))
        bins[index].append(case_id)
        seconds[index] += weight
    runs = [LEGACY_CHROMIUM]
    for index, selected in enumerate(bins, start=1):
        suffixes = "|".join(re.escape(case_id[3:]) for case_id in sorted(selected))
        runs.append(ChromiumRun(
            f"chromium-v2-{index}", rf"\bV2-(?:{suffixes})\b", False, None, 2,
        ))
    return tuple(runs)


def _plan_chromium(run: ChromiumRun, directory: Path) -> tuple[int, set[str]]:
    command = (
        "pnpm", "exec", "playwright", "test", "--config",
        "playwright.auth.config.ts", "--project", "chromium", "--list",
        *_chromium_args(run),
    )
    result = subprocess.run(command, cwd=WEB, text=True, capture_output=True,
                            check=False)
    output = result.stdout + "\n" + result.stderr
    (directory / f"{run.name}.inventory.log").write_text(output, encoding="utf-8")
    matches = COLLECTED_TESTS.findall(output)
    cases = _chromium_inventory(output)
    if result.returncode or len(matches) != 1 or not cases or len(cases) != int(matches[0]):
        raise RuntimeError(f"Cannot establish exact Playwright inventory for {run.name}")
    return int(matches[0]), cases


def _validate_chromium_partition(
    full: set[str], inventories: dict[str, set[str]],
    runs: tuple[ChromiumRun, ...],
) -> None:
    if not full or set(inventories) != {run.name for run in runs}:
        raise RuntimeError("Chromium run is missing an inventory")
    union: set[str] = set()
    for run in runs:
        cases = inventories[run.name]
        if not cases or union.intersection(cases):
            raise RuntimeError(f"Chromium inventory overlaps or is empty: {run.name}")
        union.update(cases)
    if union != full:
        raise RuntimeError(
            f"Chromium partition differs from full inventory: "
            f"missing={len(full - union)}, unexpected={len(union - full)}"
        )


def _launch_chromium(
    run: ChromiumRun, port: int, directory: Path,
) -> tuple[subprocess.Popen[bytes], object, float]:
    shard = directory / run.name
    shard.mkdir(parents=True, exist_ok=False)
    env = {
        **os.environ,
        "DANTE_E2E_WEB_PORT": str(port),
        "DANTE_E2E_PREBUILT_WEB": "1",
        "PLAYWRIGHT_JUNIT_OUTPUT_FILE": str(shard / "junit.xml"),
        "DANTE_E2E_PER_STACK_WORKERS": str(run.workers),
        "DANTE_E2E_PROGRESS_JSONL": str(shard / "progress.jsonl"),
    }
    command = (
        "pnpm", "exec", "playwright", "test", "--config",
        "playwright.auth.config.ts", "--project", "chromium",
        f"--workers={run.workers}", "--retries=0",
        "--reporter=line,junit,./e2e/auth/temporal-progress-reporter.ts",
        "--output", str(shard / "test-results"),
        *_chromium_args(run),
    )
    log = (shard / "playwright.log").open("w", encoding="utf-8")
    try:
        process = subprocess.Popen(
            command, cwd=WEB, env=env, stdout=log, stderr=subprocess.STDOUT,
            start_new_session=True,
        )
    except BaseException:
        log.close()
        raise
    return process, log, time.monotonic()


def _finish_chromium(
    run: ChromiumRun, port: int, discovered: int, directory: Path,
    exit_code: int, started: float,
) -> ShardResult:
    shard = directory / run.name
    try:
        recorded, skipped, failed, errors = _junit_counts(shard / "junit.xml")
    except (OSError, ElementTree.ParseError, RuntimeError) as exc:
        (shard / "report-error.txt").write_text(f"{exc}\n", encoding="utf-8")
        recorded, skipped, failed, errors = 0, 0, 0, 1
    return ShardResult(
        project=run.name, port=port, discovered=discovered,
        recorded=recorded, passed=recorded - skipped - failed - errors,
        skipped=skipped, failed=failed, errors=errors, exit_code=exit_code,
        seconds=round(time.monotonic() - started, 2),
    )


def _free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
        probe.bind(("127.0.0.1", 0))
        return int(probe.getsockname()[1])


def _unique_ports(projects: tuple[str, ...] = PROJECTS) -> dict[str, int]:
    ports: dict[str, int] = {}
    for project in projects:
        port = _free_port()
        while port in ports.values():
            port = _free_port()
        ports[project] = port
    return ports


def _selector(grep: str | None) -> tuple[str, ...]:
    """Identical filtered inventory and Playwright execution arguments."""
    return ("--grep", grep) if grep is not None else ()


def _plan(project: str, directory: Path, grep: str | None = None) -> int:
    command = (
        "pnpm", "exec", "playwright", "test", "--config",
        "playwright.auth.config.ts", "--project", project, "--list",
        *_selector(grep),
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


def _validate_coverage(
    planned: dict[str, int],
    results: list[ShardResult],
    projects: tuple[str, ...] = PROJECTS,
) -> None:
    # The full gate always requires all three projects. An explicit
    # --project chromium local smoke still checks exact inventory parity,
    # but intentionally does not claim cross-browser acceptance.
    expected = set(projects)
    if (
        not expected or len(expected) != len(projects) or
        not expected.issubset(PROJECTS) or
        set(planned) != expected or
        set(r.project for r in results) != expected
    ):
        raise RuntimeError("Browser inventory differs from the explicitly selected projects")
    if len(results) != len(projects):
        raise RuntimeError("Browser sharding dropped or duplicated a selected project")
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
    grep: str | None = None, v2_workers: int = 1,
) -> ShardResult:
    shard = directory / project
    shard.mkdir(parents=True, exist_ok=False)
    junit = shard / "junit.xml"
    env = {
        **os.environ,
        "DANTE_E2E_WEB_PORT": str(port),
        "DANTE_E2E_PREBUILT_WEB": "1",
        "PLAYWRIGHT_JUNIT_OUTPUT_FILE": str(junit),
        "DANTE_E2E_PER_STACK_WORKERS": str(v2_workers),
        "DANTE_E2E_PROGRESS_JSONL": str(shard / "progress.jsonl"),
    }
    command = (
        "pnpm", "exec", "playwright", "test", "--config",
        "playwright.auth.config.ts", "--project", project,
        f"--workers={v2_workers}", "--retries=0",
        "--reporter=line,junit,./e2e/auth/temporal-progress-reporter.ts",
        "--output", str(shard / "test-results"),
        *(("--fully-parallel",) if v2_workers > 1 else ()),
        *_selector(grep),
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


def _write_diagnostic_archive(directory: Path, *, include_traces: bool = True) -> Path:
    """Package the actual Playwright evidence automatically and compactly.

    Keep each original trace.zip untouched for the local trace viewer.
    Diagnostic copies omit only repetitive JPEG screencast frames; action
    history, network requests and snapshots remain for failure analysis.
    """
    reduced = directory / "diagnostic-traces"
    inventory: list[dict[str, object]] = []
    omitted_origins: list[str] = []
    traces_per_project: dict[str, int] = {}
    # Full matrices may have hundreds of failures. Cap upload-oriented trace
    # reduction to the first six per browser; retain every raw trace on disk.
    # An interrupted run must return control promptly, even when Playwright
    # left thousands of trace resources behind. They remain available locally.
    sources = (
        sorted(directory.glob("*/test-results/**/trace.zip"),
               key=lambda source: (source.parent.parent.parent.name,
                                   source.stat().st_mtime))
        if include_traces else []
    )
    for source in sources:
        relative = source.relative_to(directory)
        project = relative.parts[0]
        count = traces_per_project.get(project, 0)
        if count >= 6:
            omitted_origins.append(relative.as_posix())
            continue
        traces_per_project[project] = count + 1
        target = reduced / relative.with_name("trace-diagnostic.zip")
        target.parent.mkdir(parents=True, exist_ok=True)
        skipped = 0
        bytes_skipped = 0
        try:
            with zipfile.ZipFile(source) as raw, zipfile.ZipFile(
                target, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=1,
            ) as slim:
                for entry in raw.infolist():
                    if entry.is_dir():
                        continue
                    if (
                        entry.filename.startswith("resources/page@")
                        and entry.filename.endswith((".jpeg", ".jpg"))
                    ):
                        skipped += 1
                        bytes_skipped += entry.file_size
                        continue
                    slim.writestr(entry, raw.read(entry))
        except (OSError, zipfile.BadZipFile, RuntimeError) as exc:
            target.unlink(missing_ok=True)
            target.with_suffix(".error.txt").write_text(
                f"{type(exc).__name__}: {exc}\n", encoding="utf-8",
            )
        inventory.append({
            "original": relative.as_posix(),
            "original_bytes": source.stat().st_size,
            "diagnostic": (
                target.relative_to(directory).as_posix()
                if target.exists() else None
            ),
            "omitted_screencast_frames": skipped,
            "omitted_screencast_bytes": bytes_skipped,
        })
    (directory / "diagnostic-manifest.json").write_text(
        json.dumps({
            "format": "dante-e2e-compact-v1",
            "original_traces_retained_on_disk": True,
            "traces": inventory,
            "raw_traces_not_in_compact_archive": omitted_origins,
        }, indent=2) + "\n", encoding="utf-8",
    )
    names = {
        "summary.json", "partial-summary.json", "progress.jsonl",
        "diagnostic-manifest.json", "playwright.log",
        "junit.xml", "web-build.log", "orchestrator-error.txt",
        "report-error.txt", "error-context.md", ".last-run.json",
        "trace-diagnostic.zip", "trace-diagnostic.error.txt",
    }
    if include_traces:
        files = sorted(
            p for p in directory.rglob("*")
            if p.is_file() and (p.name in names or p.name.endswith(".inventory.log"))
        )
    else:
        files = sorted(
            p for parent in (directory, *directory.iterdir()) if parent.is_dir()
            for p in parent.iterdir()
            if p.is_file() and (p.name in names or p.name.endswith(".inventory.log"))
        )
        # Read only the immediate result directory for each case. A partial
        # run needs its failure snapshots, but recursive trace traversal is
        # what made the previous Ctrl+C appear to hang.
        files.extend(sorted(directory.glob("*/test-results/*/error-context.md")))
    archive = directory / "E2E_DIAGNOSTICS.tar.gz"
    with tarfile.open(archive, "w:gz", compresslevel=1) as output:
        for file in files:
            output.add(
                file, arcname=file.relative_to(directory).as_posix(),
                recursive=False,
            )
    return archive


def _write_partial_progress(directory: Path, *, interrupted: bool) -> Path:
    """Persist observed per-test results even when Playwright's JUnit is absent.

    A signal may stop a long V2 campaign before JUnit finalization. Only tests
    with an onTestEnd record are counted; unexecuted tests stay unclassified.
    This report is diagnostic and never satisfies the green coverage gate.
    """
    by_project: list[dict[str, object]] = []
    for progress in sorted(directory.glob("*/progress.jsonl")):
        records: list[dict[str, object]] = []
        malformed = 0
        for line in progress.read_text(encoding="utf-8").splitlines():
            try:
                value = json.loads(line)
            except json.JSONDecodeError:
                malformed += 1
                continue
            if not isinstance(value, dict) or value.get("status") not in {
                "passed", "failed", "timedOut", "skipped", "interrupted",
            }:
                malformed += 1
                continue
            records.append(value)
        by_project.append({
            "project": progress.parent.name,
            "completed": len(records),
            "passed": sum(
                row["status"] == "passed" and row.get("outcome") == "expected"
                for row in records
            ),
            "failed": sum(
                row["status"] in {"failed", "timedOut", "interrupted"}
                or row.get("outcome") == "unexpected"
                for row in records
            ),
            "skipped": sum(row["status"] == "skipped" for row in records),
            "malformed_records": malformed,
            "cases": records,
        })
    result = directory / "partial-summary.json"
    result.write_text(
        json.dumps({
            "format": "dante-e2e-progress-v1",
            "complete": False,
            "interrupted": interrupted,
            "counts_are_only_observed": True,
            "not_an_acceptance_result": True,
            "projects": by_project,
        }, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return result


def _v2_selection_isolated(grep: str | None) -> bool:
    """Only known V2 title prefixes may opt into same-stack parallel tests.

    Unlike legacy authentication/browser tests, each V2 case uses its own
    synthetic account and never stops the disposable PostgreSQL service.
    """
    return grep is not None and (
        re.fullmatch(r"V2-[A-Z0-9-]*", grep) is not None
        or re.fullmatch(r"V2-\([A-Z0-9|\-]+\)", grep) is not None
        or re.fullmatch(r"V2-[A-Z0-9-]+\([A-Z0-9|\-]+\)", grep) is not None
    )


def _v2_worker_budget(setting: str, grep: str | None) -> int:
    if setting == "1":
        return 1
    if not _v2_selection_isolated(grep):
        raise ValueError(
            "Parallel tests on one stack require an exclusively V2- "
            "title selection; legacy tests may restart PostgreSQL."
        )
    if setting == "2":
        return 2
    if setting != "auto":
        raise ValueError("v2-workers must be auto, 1 or 2")
    # Evaluate available (not total) WSL memory at launch. Cap the extra
    # worker to two per stack because signin capacity is two per stack.
    cores = os.cpu_count() or 1
    try:
        memory = Path("/proc/meminfo").read_text(encoding="utf-8")
        available_kib = int(re.search(
            r"^MemAvailable:\s*(\d+) kB", memory, re.M,
        ).group(1))
    except (OSError, AttributeError, ValueError):
        available_kib = 0
    return 2 if cores >= 6 and available_kib >= 8 * 1024 * 1024 else 1


def _assert_disposable_postgres_removal_contract() -> None:
    """Guard disposable E2E PostgreSQL against anonymous-volume leaks."""
    source = ROOT / "tooling" / "serve-access-auth-stack.py"
    tree = ast.parse(source.read_text(encoding="utf-8"), filename=str(source))
    docker_calls = [
        call for call in ast.walk(tree)
        if isinstance(call, ast.Call) and
        isinstance(call.func, ast.Name) and call.func.id == "_docker"
    ]
    commands: list[tuple[str, ...]] = []
    for call in docker_calls:
        tokens = tuple(
            arg.value for arg in call.args
            if isinstance(arg, ast.Constant) and isinstance(arg.value, str)
        )
        if tokens and tokens[0] in {"run", "rm"}:
            commands.append(tokens)
    started = [tokens for tokens in commands if tokens[0] == "run"]
    removals = [tokens for tokens in commands if tokens[0] == "rm"]
    if not (
        len(started) == 1 and
        "--rm" not in started[0] and
        len(removals) == 2 and
        all({"--force", "--volumes"} <= set(tokens) for tokens in removals)
    ):
        raise AssertionError(
            "Restartable E2E PostgreSQL cannot use docker run --rm; "
            "both startup-failure and final cleanup must use "
            "docker rm --force --volumes."
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
    # Single-browser developer smoke must be isolated and accounted for:
    # one selected project, one exact JUnit inventory, no implied coverage
    # of Firefox/WebKit. The three-browser gate must still reject it.
    _validate_coverage(
        {"chromium": 2}, valid[:1], ("chromium",),
    )
    try:
        _validate_coverage({"chromium": 2}, valid[:1])
    except RuntimeError:
        pass
    else:
        raise AssertionError("Full browser gate must never pass on one project")
    try:
        _validate_coverage(
            {"chromium": 2}, valid[:1], ("chromium", "chromium"),
        )
    except RuntimeError:
        pass
    else:
        raise AssertionError("A browser cannot appear twice in the selection")
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
    _assert_disposable_postgres_removal_contract()
    # A filtered inventory must be compared to the same filtered execution,
    # never the original full-suite count.
    assert _plan.__defaults__ == (None,)
    assert _run_project.__defaults__ == (None, 1)
    assert _v2_selection_isolated("V2-")
    assert _v2_selection_isolated("V2-P1-E01")
    assert _v2_selection_isolated("V2-(P1-A01|P2-E04|RT-02)")
    assert _v2_selection_isolated("V2-P1-(E10|E15|A08|A19)")
    assert _v2_worker_budget("2", "V2-P1-(E10|E15|A08|A19)") == 2
    for unsafe in (
        None, "auth", "V2-P1|other", "V2-.*", "V2-(P1)|Auth",
        "V2-P1-(E10|A08)|Auth", "V2-P1-(E10|.*)",
    ):
        assert not _v2_selection_isolated(unsafe)
        try:
            _v2_worker_budget("2", unsafe)
        except ValueError:
            pass
        else:
            raise AssertionError("Non-V2 tests must never share one stack concurrently")
    assert _v2_worker_budget("1", None) == 1
    assert _v2_worker_budget("2", "V2-P1-A01") == 2
    assert _selector(None) == ()
    assert _selector(r"V2-P3-(E01|A01)") == (
        "--grep", r"V2-P3-(E01|A01)",
    )
    full = {
        "[chromium] › case-a",
        "[chromium] › V2-P1-E01 creates Event",
        "[chromium] › V2-P2-A01 edits Activity",
        "[chromium] › V2-P3-EFIRST converts Event",
        "[chromium] › V2-RT-01 records Actual",
    }
    runs = _balanced_chromium_runs(full)
    assert _chromium_args(runs[0]) == ("--grep-invert", "V2-")
    assert all(run.shard is None and run.workers == 2 for run in runs[1:])
    inventories = {
        runs[0].name: {"[chromium] › case-a"},
        **{
            run.name: {
                title for title in full if re.search(run.grep, title)
            }
            for run in runs[1:]
        },
    }
    _validate_chromium_partition(full, inventories, runs)
    for damaged in (
        {**inventories, runs[2].name: set()},
        {**inventories, runs[2].name: inventories[runs[1].name]},
    ):
        try:
            _validate_chromium_partition(full, damaged, runs)
        except RuntimeError:
            pass
        else:
            raise AssertionError("Missing or duplicated Chromium cases must fail")
    try:
        _balanced_chromium_runs({"[chromium] › V2-P1-E01", "[chromium] › V2-P1-E01 duplicate"})
    except RuntimeError:
        pass
    else:
        raise AssertionError("Duplicate V2 IDs must fail before browser startup")
    weighted = {
        f"[chromium] › V2-{phase}-E{index:02d} journey"
        for phase, count in (("P1", 40), ("P2", 40), ("P3", 20))
        for index in range(1, count + 1)
    }
    balanced = _balanced_chromium_runs(weighted)
    estimated = [
        sum(
            V2_PHASE_SECONDS[title.rsplit(" › ", 1)[-1].split("-", 2)[1]]
            for title in weighted if re.search(run.grep, title)
        )
        for run in balanced[1:]
    ]
    assert abs(estimated[0] - estimated[1]) <= max(V2_PHASE_SECONDS.values())
    with tempfile.TemporaryDirectory(prefix="dante-e2e-archive-test.") as temp:
        root = Path(temp)
        (root / "summary.json").write_text('{"exit_code": 1}\n')
        failure = root / "chromium" / "test-results" / "failed-test"
        failure.mkdir(parents=True)
        (root / "chromium" / "playwright.log").write_text("FAILED\n")
        (root / "chromium" / "progress.jsonl").write_text(
            json.dumps({"title": "V2-P1-A02", "status": "passed", "outcome": "expected"})
            + "\n"
            + json.dumps({"title": "V2-P2-E01", "status": "failed", "outcome": "unexpected"})
            + "\n",
            encoding="utf-8",
        )
        snapshot = json.loads(_write_partial_progress(root, interrupted=True).read_text())
        assert snapshot["complete"] is False
        assert snapshot["not_an_acceptance_result"] is True
        assert snapshot["projects"][0]["completed"] == 2
        assert snapshot["projects"][0]["passed"] == 1
        assert snapshot["projects"][0]["failed"] == 1
        progress_line = _progress_line(root, 10, time.monotonic())
        assert "2/10 (20.0%)" in progress_line
        assert "passed=1 failed=1" in progress_line
        (root / "chromium" / "junit.xml").write_text(
            "<testsuite><testcase><failure/></testcase></testsuite>\n"
        )
        (failure / "error-context.md").write_text("button absent\n")
        with zipfile.ZipFile(failure / "trace.zip", "w") as trace:
            trace.writestr("0-trace.trace", "action=click\n")
            trace.writestr("0-trace.network", "status=200\n")
            trace.writestr("resources/page@100.jpeg", b"video-frame")
        archive = _write_diagnostic_archive(root)
        assert archive.exists()
        with tarfile.open(archive, "r:gz") as bundle:
            member_names = set(bundle.getnames())
            reduced_name = (
                "diagnostic-traces/chromium/test-results/"
                "failed-test/trace-diagnostic.zip"
            )
            assert {
                "summary.json", "partial-summary.json",
                "chromium/progress.jsonl", "chromium/playwright.log",
                "chromium/junit.xml", reduced_name,
            } <= member_names
            assert "chromium/test-results/failed-test/error-context.md" in member_names
            member = bundle.extractfile(reduced_name)
            assert member is not None
            with zipfile.ZipFile(io.BytesIO(member.read())) as reduced_zip:
                assert "0-trace.trace" in reduced_zip.namelist()
                assert "0-trace.network" in reduced_zip.namelist()
                assert "resources/page@100.jpeg" not in reduced_zip.namelist()
        assert (failure / "trace.zip").exists()
        interrupted_archive = _write_diagnostic_archive(root, include_traces=False)
        with tarfile.open(interrupted_archive, "r:gz") as bundle:
            assert "partial-summary.json" in bundle.getnames()
            assert "chromium/test-results/failed-test/error-context.md" in bundle.getnames()
            assert all("trace-diagnostic" not in name for name in bundle.getnames())
        # Even a broad RED matrix may only add six reduced traces per browser
        # to the upload, without deleting any original browser evidence.
        for i in range(6):
            extra = root / "chromium" / "test-results" / f"extra-{i}"
            extra.mkdir(parents=True)
            with zipfile.ZipFile(extra / "trace.zip", "w") as trace:
                trace.writestr("0-trace.trace", "additional failing action")
        _write_diagnostic_archive(root)
        index = json.loads((root / "diagnostic-manifest.json").read_text())
        assert len(index["traces"]) == 6
        assert len(index["raw_traces_not_in_compact_archive"]) == 1
        for i in range(6):
            assert (root / "chromium" / "test-results" / f"extra-{i}" /
                    "trace.zip").exists()
    print("PASS: browser sharding, coverage, and auto-packaged E2E diagnostics")


def _progress_counts(directory: Path) -> tuple[int, int, int]:
    completed = passed = failed = 0
    for path in directory.glob("*/progress.jsonl"):
        for line in path.read_text(encoding="utf-8").splitlines():
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            completed += 1
            passed += row.get("status") == "passed" and row.get("outcome") == "expected"
            failed += row.get("status") in {"failed", "timedOut", "interrupted"}
    return completed, passed, failed


def _progress_line(directory: Path, total: int, started: float) -> str:
    completed, passed, failed = _progress_counts(directory)
    return (
        f"REALSTACK_PROGRESS: {completed}/{total} "
        f"({completed / total * 100:.1f}%) completed, "
        f"passed={passed} failed={failed}, "
        f"elapsed={round(time.monotonic() - started)}s"
    )


def _run_full_chromium(directory: Path, report: Path, started: float,
                       max_minutes: int) -> int:
    total = _plan("chromium", directory)
    full = _chromium_inventory(
        (directory / "chromium.inventory.log").read_text(encoding="utf-8")
    )
    if len(full) != total:
        raise RuntimeError("Full Chromium inventory has duplicate or missing case IDs")
    runs = _balanced_chromium_runs(full)
    inventories: dict[str, set[str]] = {}
    planned: dict[str, int] = {}
    for run in runs:
        planned[run.name], inventories[run.name] = _plan_chromium(run, directory)
    _validate_chromium_partition(full, inventories, runs)
    print(
        f"REALSTACK_CHROMIUM: all {total} cases, three isolated stacks, "
        "five Chromium workers maximum; weighted V2 distribution "
        f"{planned[runs[1].name]}/{planned[runs[2].name]}; one aggregate report",
        flush=True,
    )
    build_env = {
        **os.environ,
        "VITE_DANTE_APPLE_ENABLED": "true",
        "VITE_DANTE_PASSKEY_ENABLED": "true",
    }
    with (directory / "web-build.log").open("w", encoding="utf-8") as log:
        build = subprocess.run(
            ["pnpm", "--filter", "@dante/web", "build"],
            cwd=ROOT, env=build_env, stdout=log, stderr=subprocess.STDOUT,
            check=False,
        )
    if build.returncode:
        raise RuntimeError(f"Shared frontend build failed ({build.returncode})")

    ports = _unique_ports(tuple(run.name for run in runs))
    active: dict[str, tuple[subprocess.Popen[bytes], object, float]] = {}
    results: dict[str, ShardResult] = {}
    deadline = started + max_minutes * 60
    next_update = time.monotonic() + 20
    try:
        for run in runs:
            active[run.name] = _launch_chromium(run, ports[run.name], directory)
        while active:
            for run in runs:
                item = active.get(run.name)
                if item is None:
                    continue
                process, log, launched = item
                code = process.poll()
                if code is None:
                    continue
                log.close()
                del active[run.name]
                result = _finish_chromium(run, ports[run.name], planned[run.name],
                                          directory, code, launched)
                results[run.name] = result
                print(
                    f"REALSTACK {run.name}: {result.recorded}/{result.discovered} "
                    f"passed={result.passed} failed={result.failed} "
                    f"errors={result.errors} elapsed={result.seconds}s",
                    flush=True,
                )
            now = time.monotonic()
            if now >= next_update:
                print(_progress_line(directory, total, started), flush=True)
                next_update = now + 20
            if active and now >= deadline:
                raise GateTimeout(
                    f"Chromium gate exceeded {max_minutes} minutes; "
                    "partial results and logs have been saved"
                )
            if active:
                time.sleep(1)
    finally:
        # Stop each complete process group: Playwright, its web server and
        # the stack's Python cleanup handler all receive SIGTERM.
        previous_sigint = signal.signal(signal.SIGINT, signal.SIG_IGN)
        try:
            for process, _, _ in active.values():
                if process.poll() is None:
                    try:
                        os.killpg(process.pid, signal.SIGTERM)
                    except ProcessLookupError:
                        pass
            for process, log, _ in active.values():
                try:
                    process.wait(timeout=12)
                except subprocess.TimeoutExpired:
                    try:
                        os.killpg(process.pid, signal.SIGKILL)
                    except ProcessLookupError:
                        pass
                    process.wait(timeout=3)
                finally:
                    log.close()
        finally:
            signal.signal(signal.SIGINT, previous_sigint)
    ordered = [results[run.name] for run in runs]
    for result in ordered:
        if result.recorded != planned[result.project]:
            raise RuntimeError(
                f"{result.project}: JUnit recorded {result.recorded}/"
                f"{planned[result.project]} cases"
            )
    if sum(r.skipped for r in ordered) > MAX_BASELINE_SKIPS:
        raise RuntimeError("Chromium gate introduced unexpected skipped cases")
    if sum(r.recorded for r in ordered) != total:
        raise RuntimeError("Chromium gate dropped or duplicated cases")
    success = all(r.exit_code == 0 and r.failed == 0 and r.errors == 0 for r in ordered)
    report.write_text(
        json.dumps({
            "selected_projects": ["chromium"],
            "mode": "full-chromium-isolated",
            "maximum_concurrent_browsers": 5,
            "elapsed_seconds": round(time.monotonic() - started, 2),
            "discovered": total,
            "recorded": sum(r.recorded for r in ordered),
            "skipped": sum(r.skipped for r in ordered),
            "passed": sum(r.passed for r in ordered),
            "failed": sum(r.failed for r in ordered),
            "errors": sum(r.errors for r in ordered),
            "exit_code": 0 if success else 1,
            "projects": [asdict(r) for r in ordered],
        }, indent=2) + "\n", encoding="utf-8",
    )
    print(f"REALSTACK_REPORT={report}", flush=True)
    return int(not success)


def _recover_last_run() -> int:
    explicit = os.environ.get("DANTE_E2E_REAL_STACK_ARTIFACTS_DIR")
    if explicit:
        candidates = [Path(explicit).resolve()]
    else:
        candidates = list((ROOT / "temp").glob("dante-realstack-*"))
    candidates = [
        candidate for candidate in candidates
        if candidate.is_dir() and list(candidate.glob("*/progress.jsonl"))
    ]
    if not candidates:
        raise RuntimeError("No existing real-stack progress found under temp/")
    directory = max(
        candidates,
        key=lambda candidate: max(
            path.stat().st_mtime for path in candidate.glob("*/progress.jsonl")
        ),
    )
    partial = _write_partial_progress(directory, interrupted=True)
    archive = _write_diagnostic_archive(directory, include_traces=False)
    print(f"REALSTACK_RECOVERED_FROM={directory}", flush=True)
    print(f"REALSTACK_PARTIAL={partial}", flush=True)
    print(f"REALSTACK_DIAGNOSTICS={archive}", flush=True)
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--workers", type=int,
        default=int(os.environ.get("DANTE_E2E_REAL_STACK_WORKERS", "3")),
        help="Independent browser stacks (1-3; 1 retains the reference runner)",
    )
    parser.add_argument(
        "--project", choices=PROJECTS, default=None,
        help="Run only this browser for developer smoke; default retains "
             "all three required browser projects for acceptance.",
    )
    parser.add_argument(
        "--v2-workers", choices=("1", "2", "auto"), default="1",
        help="Per-browser workers only for isolated V2 titles; auto chooses "
             "1 or 2 using WSL CPU/free RAM. Default 1 preserves full-gate isolation.",
    )
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument(
        "--recover-last", action="store_true",
        help="Package progress, JUnit, logs and error contexts from the last "
             "interrupted real-stack run without launching tests",
    )
    parser.add_argument(
        "--fast-chromium", action="store_true",
        help="One complete Chromium invocation, internally isolated and "
             "parallel, with one coverage-checked report",
    )
    parser.add_argument(
        "--max-minutes", type=int, default=45,
        help="Hard limit for --fast-chromium; return partial diagnostics "
             "instead of running indefinitely (default: 45)",
    )
    parser.add_argument(
        "--grep", default=None,
        help="Playwright test-title regex (also filters --list inventory); "
             "default runs the full unfiltered suite",
    )
    args = parser.parse_args()
    if args.self_test:
        _self_test()
        return 0
    if args.recover_last:
        try:
            return _recover_last_run()
        except (OSError, RuntimeError) as exc:
            print(f"REALSTACK RECOVERY FAILED: {exc}", file=sys.stderr)
            return 2
    if not 1 <= args.workers <= len(PROJECTS):
        parser.error("--workers must be between 1 and 3")
    if args.max_minutes < 1:
        parser.error("--max-minutes must be positive")
    if args.fast_chromium and (args.project != "chromium" or args.grep is not None):
        parser.error("--fast-chromium requires --project chromium and no --grep")
    try:
        per_project = _v2_worker_budget(args.v2_workers, args.grep)
    except ValueError as exc:
        parser.error(str(exc))
    selected_projects = (args.project,) if args.project is not None else PROJECTS
    stack_count = min(args.workers, len(selected_projects))
    if args.workers == 1 and per_project > 1 and args.project is None:
        parser.error(
            "--v2-workers >1 with --workers 1 requires an explicit "
            "--project chromium/firefox/webkit smoke selection"
        )
    if not args.fast_chromium:
        print(
            f"REALSTACK_CONCURRENCY=stacks:{stack_count} "
            f"per_stack:{per_project} maximum_browsers:{stack_count * per_project}",
            flush=True,
        )
    if args.workers == 1 and args.project is None and not args.fast_chromium:
        # Bit-for-bit equivalent selection and startup behavior to the
        # last all-green gate; no new sharding assumptions in fallback.
        port = _free_port()
        env = {**os.environ, "DANTE_E2E_WEB_PORT": str(port)}
        print(f"DANTE_E2E_WEB_PORT={port}; reference serial real-stack", flush=True)
        return subprocess.run(
            [
                "pnpm", "exec", "playwright", "test", "--config",
                "playwright.auth.config.ts",
                *_selector(args.grep),
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
    interrupted = False
    try:
        if args.fast_chromium:
            return _run_full_chromium(directory, report, started, args.max_minutes)
        planned = {
            project: _plan(project, directory, args.grep)
            for project in selected_projects
        }
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
        ports = _unique_ports(selected_projects)
        completed: dict[str, ShardResult] = {}
        with ThreadPoolExecutor(max_workers=stack_count) as pool:
            futures = {
                pool.submit(
                    _run_project, p, ports[p], planned[p], directory,
                    args.grep, per_project,
                ): p
                for p in selected_projects
            }
            remaining = set(futures)
            while remaining:
                ready, remaining = wait(
                    remaining, timeout=20, return_when=FIRST_COMPLETED,
                )
                print(_progress_line(directory, sum(planned.values()), started), flush=True)
                for future in ready:
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
        results = [completed[p] for p in selected_projects]
        _validate_coverage(planned, results, selected_projects)
        success = all(r.exit_code == 0 and r.failed == 0 and r.errors == 0 for r in results)
        report.write_text(
            json.dumps({
                "workers": stack_count,
                "selected_projects": list(selected_projects),
                "v2_workers_per_project": per_project,
                "maximum_concurrent_browsers": stack_count * per_project,
                "grep": args.grep,
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
    except KeyboardInterrupt:
        interrupted = True
        (directory / "orchestrator-error.txt").write_text(
            "Interrupted by operator; only completed per-test records are recoverable.\n",
            encoding="utf-8",
        )
        print("REALSTACK INTERRUPTED: observed tests saved as partial diagnostics", flush=True)
        return 130
    except GateTimeout as exc:
        interrupted = True
        (directory / "orchestrator-error.txt").write_text(
            f"{type(exc).__name__}: {exc}\n", encoding="utf-8",
        )
        print(f"REALSTACK TIMEOUT: {exc}", file=sys.stderr, flush=True)
        return 124
    except (OSError, RuntimeError, subprocess.SubprocessError) as exc:
        (directory / "orchestrator-error.txt").write_text(
            f"{type(exc).__name__}: {exc}\n", encoding="utf-8",
        )
        print(f"REALSTACK ERROR: {exc}", file=sys.stderr, flush=True)
        return 2
    finally:
        # Guaranteed diagnostics on success, SIGINT, failures or startup
        # errors. JUnit absence never turns observed test records into PASS.
        # Full-size original traces stay in project directories.
        try:
            _write_partial_progress(directory, interrupted=interrupted)
            archive = _write_diagnostic_archive(directory, include_traces=not interrupted)
            print(f"REALSTACK_DIAGNOSTICS={archive}", flush=True)
        except (OSError, RuntimeError, zipfile.BadZipFile, KeyboardInterrupt) as exc:
            print(
                f"REALSTACK DIAGNOSTICS FAILED: {exc}",
                file=sys.stderr, flush=True,
            )


if __name__ == "__main__":
    raise SystemExit(main())
