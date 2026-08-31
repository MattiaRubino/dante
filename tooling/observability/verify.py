#!/usr/bin/env python3
"""Run the deterministic source-closure gates for DANTE observability."""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

_REPO_ROOT = Path(__file__).resolve().parents[2]
_BACKEND_ROOT = _REPO_ROOT / "apps" / "backend"


@dataclass(frozen=True, slots=True)
class Check:
    name: str
    command: tuple[str, ...]
    working_directory: Path = _REPO_ROOT


def _checks(scope: Literal["all", "web", "backend"]) -> list[Check]:
    checks = [
        Check(
            "Static observability contracts",
            (sys.executable, "tooling/observability/validate.py"),
        )
    ]
    if scope in {"all", "web"}:
        checks.extend(
            [
                Check(
                    "Web observability formatting",
                    (
                        "corepack",
                        "pnpm",
                        "exec",
                        "prettier",
                        "--check",
                        "apps/web/src/platform/observability",
                        "package.json",
                    ),
                ),
                Check(
                    "Web observability lint",
                    (
                        "corepack",
                        "pnpm",
                        "exec",
                        "eslint",
                        "apps/web/src/platform/observability",
                    ),
                ),
                Check(
                    "Web observability tests",
                    ("corepack", "pnpm", "--filter", "@dante/web", "test"),
                ),
                Check(
                    "Web typecheck",
                    ("corepack", "pnpm", "--filter", "@dante/web", "typecheck"),
                ),
                Check(
                    "Web production build and bundle budget",
                    ("corepack", "pnpm", "--filter", "@dante/web", "build"),
                ),
            ]
        )
    if scope in {"all", "backend"}:
        checks.extend(
            [
                Check(
                    "Backend locked environment",
                    ("uv", "sync", "--locked"),
                    _BACKEND_ROOT,
                ),
                Check(
                    "Backend Ruff format",
                    ("uv", "run", "--locked", "ruff", "format", "--check", "."),
                    _BACKEND_ROOT,
                ),
                Check(
                    "Backend Ruff lint",
                    ("uv", "run", "--locked", "ruff", "check", "."),
                    _BACKEND_ROOT,
                ),
                Check(
                    "Backend mypy strict",
                    ("uv", "run", "--locked", "mypy"),
                    _BACKEND_ROOT,
                ),
                Check(
                    "Backend regression tests",
                    ("uv", "run", "--locked", "pytest", "-m", "not postgres"),
                    _BACKEND_ROOT,
                ),
                Check("Backend package build", ("uv", "build"), _BACKEND_ROOT),
            ]
        )
    return checks


def _parse_scope() -> Literal["all", "web", "backend"]:
    parser = argparse.ArgumentParser(
        description=(
            "Run repository-owned observability source gates without starting services "
            "or reading credentials."
        )
    )
    parser.add_argument(
        "--scope",
        choices=("all", "web", "backend"),
        default="all",
        help="gate family to run (default: all)",
    )
    return parser.parse_args().scope


def main() -> int:
    """Run every selected check in a stable, fail-fast order."""
    scope = _parse_scope()
    checks = _checks(scope)
    required_tools = {check.command[0] for check in checks}
    missing_tools = sorted(tool for tool in required_tools if shutil.which(tool) is None)
    if missing_tools:
        print(
            f"observability verification failed: missing tools: {', '.join(missing_tools)}",
            file=sys.stderr,
        )
        return 2

    environment = os.environ.copy()
    environment["COREPACK_ENABLE_DOWNLOAD_PROMPT"] = "0"
    for index, check in enumerate(checks, start=1):
        print(f"\n[{index}/{len(checks)}] {check.name}", flush=True)
        result = subprocess.run(
            check.command,
            cwd=check.working_directory,
            env=environment,
            check=False,
        )
        if result.returncode != 0:
            print(
                f"observability verification failed at: {check.name}",
                file=sys.stderr,
            )
            return result.returncode

    print(f"\nobservability source verification ({scope}): PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
