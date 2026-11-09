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
import tarfile
import tempfile
import time
import zipfile
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
    }
    command = (
        "pnpm", "exec", "playwright", "test", "--config",
        "playwright.auth.config.ts", "--project", project,
        f"--workers={v2_workers}", "--retries=0", "--reporter=line,junit",
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


def _write_diagnostic_archive(directory: Path) -> Path:
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
    sources = sorted(
        directory.glob("*/test-results/**/trace.zip"),
        key=lambda source: (source.parent.parent.parent.name, source.stat().st_mtime),
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
        "summary.json", "diagnostic-manifest.json", "playwright.log",
        "junit.xml", "web-build.log", "orchestrator-error.txt",
        "report-error.txt", "error-context.md", ".last-run.json",
        "trace-diagnostic.zip", "trace-diagnostic.error.txt",
    }
    files = sorted(
        p for p in directory.rglob("*")
        if p.is_file() and (
            p.name in names or p.name.endswith(".inventory.log")
        )
    )
    archive = directory / "E2E_DIAGNOSTICS.tar.gz"
    with tarfile.open(archive, "w:gz", compresslevel=1) as output:
        for file in files:
            output.add(
                file, arcname=file.relative_to(directory).as_posix(),
                recursive=False,
            )
    return archive


def _v2_selection_isolated(grep: str | None) -> bool:
    """Only known V2 title prefixes may opt into same-stack parallel tests.

    Unlike legacy authentication/browser tests, each V2 case uses its own
    synthetic account and never stops the disposable PostgreSQL service.
    """
    return grep is not None and (
        re.fullmatch(r"V2-[A-Z0-9-]*", grep) is not None
        or re.fullmatch(r"V2-\([A-Z0-9|\-]+\)", grep) is not None
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
    # A filtered inventory must be compared to the same filtered execution,
    # never the original full-suite count.
    assert _plan.__defaults__ == (None,)
    assert _run_project.__defaults__ == (None, 1)
    assert _v2_selection_isolated("V2-")
    assert _v2_selection_isolated("V2-P1-E01")
    assert _v2_selection_isolated("V2-(P1-A01|P2-E04|RT-02)")
    for unsafe in (None, "auth", "V2-P1|other", "V2-.*", "V2-(P1)|Auth"):
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
    with tempfile.TemporaryDirectory(prefix="dante-e2e-archive-test.") as temp:
        root = Path(temp)
        (root / "summary.json").write_text('{"exit_code": 1}\n')
        failure = root / "chromium" / "test-results" / "failed-test"
        failure.mkdir(parents=True)
        (root / "chromium" / "playwright.log").write_text("FAILED\n")
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
                "summary.json", "chromium/playwright.log",
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


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--workers", type=int,
        default=int(os.environ.get("DANTE_E2E_REAL_STACK_WORKERS", "3")),
        help="Independent browser stacks (1-3; 1 retains the reference runner)",
    )
    parser.add_argument(
        "--v2-workers", choices=("1", "2", "auto"), default="1",
        help="Per-browser workers only for isolated V2 titles; auto chooses "
             "1 or 2 using WSL CPU/free RAM. Default 1 preserves full-gate isolation.",
    )
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument(
        "--grep", default=None,
        help="Playwright test-title regex (also filters --list inventory); "
             "default runs the full unfiltered suite",
    )
    args = parser.parse_args()
    if args.self_test:
        _self_test()
        return 0
    if not 1 <= args.workers <= len(PROJECTS):
        parser.error("--workers must be between 1 and 3")
    try:
        per_project = _v2_worker_budget(args.v2_workers, args.grep)
    except ValueError as exc:
        parser.error(str(exc))
    if args.workers == 1 and per_project > 1:
        parser.error("--v2-workers requires independent project stacks (--workers 2 or 3)")
    print(
        f"REALSTACK_CONCURRENCY=stacks:{args.workers} "
        f"per_stack:{per_project} maximum_browsers:{args.workers * per_project}",
        flush=True,
    )
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
    try:
        planned = {
            project: _plan(project, directory, args.grep)
            for project in PROJECTS
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
        ports = _unique_ports()
        completed: dict[str, ShardResult] = {}
        with ThreadPoolExecutor(max_workers=args.workers) as pool:
            futures = {
                pool.submit(
                    _run_project, p, ports[p], planned[p], directory,
                    args.grep, per_project,
                ): p
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
                "v2_workers_per_project": per_project,
                "maximum_concurrent_browsers": args.workers * per_project,
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
    except (OSError, RuntimeError, subprocess.SubprocessError) as exc:
        (directory / "orchestrator-error.txt").write_text(
            f"{type(exc).__name__}: {exc}\n", encoding="utf-8",
        )
        print(f"REALSTACK ERROR: {exc}", file=sys.stderr, flush=True)
        return 2
    finally:
        # Guaranteed diagnostics on success, assertion failures or startup
        # errors. Full-size original traces stay in project directories.
        try:
            archive = _write_diagnostic_archive(directory)
            print(f"REALSTACK_DIAGNOSTICS={archive}", flush=True)
        except (OSError, RuntimeError, zipfile.BadZipFile) as exc:
            print(
                f"REALSTACK DIAGNOSTICS FAILED: {exc}",
                file=sys.stderr, flush=True,
            )


if __name__ == "__main__":
    raise SystemExit(main())
