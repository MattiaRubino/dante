#!/usr/bin/env python3
"""Run every DANTE gate and package all failures for one batch diagnosis."""

from __future__ import annotations

import os
import re
import subprocess
import sys
import tarfile
import tempfile
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GATE = ROOT / "tooling" / "verify-all-current-tests-local.sh"
BRANCH = os.environ.get("DANTE_GATE_BRANCH") or "feature/timeline-temporal-operational"


def _git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def main() -> int:
    if _git("branch", "--show-current") != BRANCH:
        print(f"STOP: expected branch {BRANCH}", file=sys.stderr)
        return 2
    if dirty := _git("status", "--porcelain"):
        print("STOP: dirty worktree; refusing mixed-revision evidence", file=sys.stderr)
        print(dirty, file=sys.stderr)
        return 2

    sha = _git("rev-parse", "HEAD")
    output_root = ROOT / "temp"
    output_root.mkdir(exist_ok=True)
    # Check the daemon before checking cached images. Stopped Docker is
    # an environment prerequisite failure, not a missing-image assertion.
    try:
        daemon = subprocess.run(
            ["docker", "info", "--format", "{{.ServerVersion}}"],
            cwd=ROOT, capture_output=True, text=True, check=False, timeout=30,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired) as exc:
        print(f"STOP: Docker unavailable: {exc}", file=sys.stderr)
        print("Start Docker Desktop / WSL Docker and rerun.", file=sys.stderr)
        return 2
    if daemon.returncode != 0:
        print("STOP: Docker daemon is not accessible from WSL.", file=sys.stderr)
        print("Start Docker and verify docker info, then rerun.", file=sys.stderr)
        return 2

    # Build only when the daemon is live and the exact local image is missing.
    required_image = "dante-postgres-local:18.6"
    inspection = subprocess.run(
        ["docker", "image", "inspect", required_image],
        cwd=ROOT, capture_output=True, text=True, check=False,
    )
    if inspection.returncode != 0:
        print(f"POSTGRES_IMAGE_MISSING={required_image}", flush=True)
        build_log = output_root / "POSTGRES_IMAGE_BUILD.log"
        with build_log.open("w", encoding="utf-8") as log:
            build = subprocess.run(
                ["docker", "compose", "-f", "infra/compose/local.yaml",
                 "build", "postgres"],
                cwd=ROOT, stdout=log, stderr=subprocess.STDOUT, check=False,
            )
        print(f"POSTGRES_IMAGE_BUILD_LOG={build_log}", flush=True)
        if build.returncode != 0:
            print("STOP: test PostgreSQL image build failed.", file=sys.stderr)
            return 2
        print(f"POSTGRES_IMAGE_BUILT={required_image}", flush=True)
    with tempfile.NamedTemporaryFile(
        prefix="dante-full-console-", suffix=".log",
        dir=output_root, delete=False,
    ) as output:
        console = Path(output.name)
    print(f"CANDIDATE={sha}\nCONSOLE_LOG={console}", flush=True)
    with console.open("w", encoding="utf-8") as log:
        child = subprocess.Popen(
            ["bash", str(GATE)], cwd=ROOT, stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT, text=True, errors="replace", bufsize=1,
        )
        assert child.stdout is not None
        for line in child.stdout:
            print(line, end="", flush=True)
            log.write(line)
        status = child.wait()

    output = console.read_text(encoding="utf-8", errors="replace")
    match = re.search(r"(?m)^LOG_DIR=(\S+)$", output)
    if match is None or not (directory := Path(match.group(1))).is_dir():
        print(f"ERROR: gate log directory unavailable; inspect {console}", file=sys.stderr)
        return 2

    expected = re.findall(r"(?m)^gate\s+([A-Z][A-Z0-9_]+)\s", GATE.read_text())
    if not expected:
        print("ERROR: authoritative runner has no recognizable groups", file=sys.stderr)
        return 2
    summary = output.rsplit("===== ALL TEST GROUPS =====", 1)
    rows: dict[str, int] = {}
    if len(summary) == 2:
        rows = {name: int(code) for name, code in re.findall(
            r"(?m)^([A-Z][A-Z0-9_]+)\s+([0-9]+)\s*$", summary[1]
        )}
    failures = [name for name in expected if rows.get(name) != 0]
    stability = rows.get("SOURCE_STABILITY")
    report = [
        "# DANTE full gate — one-run report", "",
        f"- Commit: {sha}",
        f"- UTC: {datetime.now(UTC).isoformat()}",
        f"- Gate exit: {status}",
        f"- Groups reported: {sum(name in rows for name in expected)}/{len(expected)}",
        f"- Source stability: {stability if stability is not None else 'UNKNOWN'}", "",
        "| Group | Exit |", "| --- | ---: |",
    ]
    report.extend(f"| {name} | {rows.get(name, 'NOT RUN')} |" for name in expected)
    report.extend(["", "## Failures (full original logs included in archive)", ""])
    for name in failures:
        file = directory / f"{name}.log"
        report.append(f"### {name} — {rows.get(name, 'not reported')}")
        if not file.is_file():
            report.extend(["Group log missing; inspect CONSOLE.log.", ""])
            continue
        lines = file.read_text(encoding="utf-8", errors="replace").splitlines()
        signals = [s.strip()[:500] for s in lines if re.search(
            r"^FAILED\s|^ERROR\s|^E\s{2,}|AssertionError|Traceback|error:|\bFAILED\b",
            s,
        )]
        report.extend(["~~~text", *(signals[:25] or lines[-20:]), "~~~", ""])
    if stability != 0:
        report.append("Source stability FAILED or unknown; inspect CONSOLE.log.")

    summary_text = "\n".join(report) + "\n"
    (directory / "FULL_GATE_SUMMARY.md").write_text(
        summary_text, encoding="utf-8"
    )
    console.replace(directory / "CONSOLE.log")
    # Stable path for copy/paste; each run keeps its own immutable snapshot.
    (output_root / "LATEST_GATE_SUMMARY.md").write_text(
        summary_text, encoding="utf-8"
    )
    (output_root / "LATEST_GATE_DIR.txt").write_text(
        str(directory) + "\n", encoding="utf-8"
    )
    archive = directory / "FULL_GATE_LOGS.tar.gz"
    with tarfile.open(archive, "w:gz") as bundle:
        for file in sorted(directory.iterdir()):
            if file != archive:
                bundle.add(file, arcname=file.name)

    print("===== COMPLETE GATE BATCH =====")
    print(f"CHECKS={len(expected)} REPORTED={sum(name in rows for name in expected)}")
    print(f"FAILED_GROUPS={','.join(failures) if failures else 'none'}")
    print(f"SOURCE_STABILITY={stability}")
    print(f"FULL_GATE_EXIT={status}")
    print(f"SUMMARY={directory / 'FULL_GATE_SUMMARY.md'}")
    print(f"LATEST_SUMMARY={output_root / 'LATEST_GATE_SUMMARY.md'}")
    print(f"CONSOLE_LOG={directory / 'CONSOLE.log'}")
    print(f"ARCHIVE={archive}")
    print("The archive contains all group logs; review sensitive data before sharing.")
    return status or (1 if failures or stability != 0 else 0)


if __name__ == "__main__":
    sys.exit(main())
