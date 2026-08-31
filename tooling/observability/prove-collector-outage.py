#!/usr/bin/env python3
"""Prove that a bounded Alloy outage does not make the backend unavailable.

This is an operator acceptance probe, not a chaos experiment. It stops only the
optional Alloy Compose service, checks the already-running backend three times,
then restores Alloy in a finally block. It deliberately does not touch
PostgreSQL volumes, application data or Grafana Cloud credentials.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from urllib.error import URLError
from urllib.request import Request, urlopen

_REPO_ROOT = Path(__file__).resolve().parents[2]
_DEFAULT_COMPOSE_FILE = _REPO_ROOT / "infra" / "compose" / "local.yaml"
_DEFAULT_BACKEND_READY_URL = "http://127.0.0.1:8000/health/ready"
_DEFAULT_ALLOY_READY_URL = "http://127.0.0.1:12345/-/ready"
_REQUIRED_BACKEND_SUCCESSES = 3


class AcceptanceFailure(RuntimeError):
    """One failed, operator-actionable acceptance precondition or observation."""


@dataclass(frozen=True, slots=True)
class Settings:
    """Explicit, bounded inputs for the reversible collector-outage proof."""

    compose_file: Path
    backend_ready_url: str
    alloy_ready_url: str
    timeout_seconds: float


def _parse_args() -> Settings:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--allow-alloy-outage",
        action="store_true",
        help="required acknowledgement before this command stops the Alloy service",
    )
    parser.add_argument(
        "--compose-file",
        type=Path,
        default=_DEFAULT_COMPOSE_FILE,
        help="LOCAL Compose file containing the optional alloy service",
    )
    parser.add_argument(
        "--backend-ready-url",
        default=_DEFAULT_BACKEND_READY_URL,
        help="already-running backend readiness endpoint",
    )
    parser.add_argument(
        "--alloy-ready-url",
        default=_DEFAULT_ALLOY_READY_URL,
        help="Alloy readiness endpoint used before and after the proof",
    )
    parser.add_argument(
        "--timeout-seconds",
        type=float,
        default=5.0,
        help="per-request HTTP timeout (default: 5; must be in (0, 30])",
    )
    args = parser.parse_args()
    if not args.allow_alloy_outage:
        parser.error("pass --allow-alloy-outage to run the reversible outage proof")
    if not 0 < args.timeout_seconds <= 30:
        parser.error("--timeout-seconds must be greater than 0 and at most 30")
    compose_file = args.compose_file.resolve()
    if not compose_file.is_file():
        parser.error(f"Compose file does not exist: {compose_file}")
    return Settings(
        compose_file=compose_file,
        backend_ready_url=args.backend_ready_url,
        alloy_ready_url=args.alloy_ready_url,
        timeout_seconds=args.timeout_seconds,
    )


def _compose(settings: Settings, *arguments: str) -> None:
    command = (
        "docker",
        "compose",
        "-f",
        str(settings.compose_file),
        "--profile",
        "observability",
        *arguments,
    )
    result = subprocess.run(command, check=False)
    if result.returncode != 0:
        raise AcceptanceFailure(
            f"Compose command failed ({result.returncode}): {' '.join(command)}"
        )


def _require_healthy(url: str, timeout_seconds: float, label: str) -> None:
    request = Request(url, method="GET")
    try:
        with urlopen(request, timeout=timeout_seconds) as response:  # noqa: S310
            status = response.status
    except URLError as error:
        raise AcceptanceFailure(
            f"{label} is unreachable: {url} ({error.reason})"
        ) from error
    if not 200 <= status < 300:
        raise AcceptanceFailure(f"{label} returned HTTP {status}: {url}")


def _assert_alloy_service_exists(settings: Settings) -> None:
    command = (
        "docker",
        "compose",
        "-f",
        str(settings.compose_file),
        "--profile",
        "observability",
        "config",
        "--services",
    )
    result = subprocess.run(command, check=False, capture_output=True, text=True)
    if result.returncode != 0:
        raise AcceptanceFailure(
            "Compose cannot render the configured observability profile"
        )
    if "alloy" not in result.stdout.splitlines():
        raise AcceptanceFailure("Compose profile has no exact alloy service to stop")


def _prove_backend_stays_ready(settings: Settings) -> None:
    for attempt in range(1, _REQUIRED_BACKEND_SUCCESSES + 1):
        _require_healthy(
            settings.backend_ready_url,
            settings.timeout_seconds,
            f"backend readiness while Alloy is stopped (attempt {attempt})",
        )
        if attempt < _REQUIRED_BACKEND_SUCCESSES:
            time.sleep(1)


def main() -> int:
    """Run the proof and always attempt to restore the stopped collector."""
    settings = _parse_args()
    stopped = False
    primary_failure: Exception | None = None
    try:
        _assert_alloy_service_exists(settings)
        _require_healthy(
            settings.backend_ready_url,
            settings.timeout_seconds,
            "backend readiness",
        )
        _require_healthy(
            settings.alloy_ready_url,
            settings.timeout_seconds,
            "Alloy readiness",
        )
        print("Preflight PASS: backend and Alloy are healthy.")
        _compose(settings, "stop", "alloy")
        stopped = True
        print("Alloy stopped. Checking backend readiness without the collector path.")
        _prove_backend_stays_ready(settings)
        print(
            "Isolation PASS: backend stayed ready for all three checks while Alloy was stopped."
        )
    except Exception as error:
        primary_failure = error
    finally:
        if stopped:
            try:
                _compose(settings, "start", "alloy")
                _require_healthy(
                    settings.alloy_ready_url,
                    settings.timeout_seconds,
                    "Alloy readiness after restoration",
                )
                print("Restoration PASS: Alloy is healthy again.")
            except Exception as restore_error:
                if primary_failure is None:
                    primary_failure = restore_error
                else:
                    print(f"Restoration failure: {restore_error}", file=sys.stderr)
    if primary_failure is not None:
        print(f"Collector-outage acceptance failed: {primary_failure}", file=sys.stderr)
        return 1
    print("Collector-outage acceptance: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
