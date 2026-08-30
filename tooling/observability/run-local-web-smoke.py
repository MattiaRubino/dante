#!/usr/bin/env python3
"""Run the LOCAL Web/Faro smoke surface against an already-running DANTE stack."""

from __future__ import annotations

import argparse
import os
import shutil
import signal
import socket
import ssl
import subprocess
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
import urllib.response
from collections.abc import Sequence
from contextlib import closing
from pathlib import Path
from types import FrameType

_REPO_ROOT = Path(__file__).resolve().parents[2]
_WEB_ORIGIN = "https://127.0.0.1:4173"
_WEB_PORT = 4173
_DEFAULT_BACKEND_ORIGIN = "http://127.0.0.1:8000"
_DEFAULT_ALLOY_READY_URL = "http://127.0.0.1:12345/-/ready"
_DEFAULT_FARO_COLLECTOR_URL = "http://127.0.0.1:12347/collect"
_STARTUP_TIMEOUT_SECONDS = 30.0


class SmokePreflightError(RuntimeError):
    """A local dependency is not safe or ready for the smoke run."""


class _NoRedirectHandler(urllib.request.HTTPRedirectHandler):
    def redirect_request(
        self,
        request: urllib.request.Request,
        file_pointer: object,
        code: int,
        message: str,
        headers: object,
        new_url: str,
    ) -> None:
        _ = request, file_pointer, code, message, headers, new_url


def _require_executable(name: str) -> None:
    if shutil.which(name) is None:
        raise SmokePreflightError(f"Required executable is unavailable: {name}")


def _assert_loopback_origin(value: str, *, label: str) -> str:
    try:
        parsed = urllib.parse.urlsplit(value)
    except ValueError as error:
        raise SmokePreflightError(f"{label} must be a valid absolute URL") from error

    if parsed.scheme not in {"http", "https"} or parsed.hostname not in {
        "127.0.0.1",
        "localhost",
        "::1",
    }:
        raise SmokePreflightError(f"{label} must use an HTTP(S) loopback origin")
    if parsed.username or parsed.password or parsed.query or parsed.fragment:
        raise SmokePreflightError(
            f"{label} cannot contain credentials, query parameters or a fragment"
        )
    return value.rstrip("/")


def _open_local_request(
    request: urllib.request.Request, *, allow_self_signed: bool = False
) -> urllib.response.addinfourl:
    handlers: list[urllib.request.BaseHandler] = [_NoRedirectHandler()]
    if urllib.parse.urlsplit(request.full_url).scheme == "https":
        context = ssl._create_unverified_context() if allow_self_signed else None
        handlers.append(urllib.request.HTTPSHandler(context=context))
    opener = urllib.request.build_opener(*handlers)
    return opener.open(request, timeout=3)


def _request_status(url: str, *, allow_self_signed: bool = False) -> int:
    request = urllib.request.Request(url, method="GET")
    try:
        with _open_local_request(
            request, allow_self_signed=allow_self_signed
        ) as response:
            return response.status
    except urllib.error.HTTPError as error:
        return error.code
    except (OSError, urllib.error.URLError) as error:
        raise SmokePreflightError(f"Endpoint is unreachable: {url}") from error


def _require_healthy(url: str, *, label: str) -> None:
    status = _request_status(url)
    if status != 200:
        raise SmokePreflightError(f"{label} returned HTTP {status}; expected 200")


def _require_faro_cors(collector_url: str) -> None:
    request = urllib.request.Request(
        collector_url,
        method="OPTIONS",
        headers={
            "Origin": _WEB_ORIGIN,
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "content-type,x-faro-session-id",
        },
    )
    try:
        with _open_local_request(request) as response:
            status = response.status
            allowed_origin = response.headers.get("Access-Control-Allow-Origin")
    except urllib.error.HTTPError as error:
        status = error.code
        allowed_origin = error.headers.get("Access-Control-Allow-Origin")
    except (OSError, urllib.error.URLError) as error:
        raise SmokePreflightError(
            f"Faro collector is unreachable: {collector_url}"
        ) from error
    if status not in {200, 204} or allowed_origin != _WEB_ORIGIN:
        raise SmokePreflightError(
            "Faro collector CORS preflight did not allow the exact smoke origin; "
            "check DANTE_FARO_ORIGIN_SECONDARY and restart Alloy"
        )


def _require_available_port(port: int) -> None:
    try:
        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as listener:
            listener.bind(("127.0.0.1", port))
    except OSError as error:
        raise SmokePreflightError(
            f"Loopback port {port} is already in use; stop the existing Web preview first"
        ) from error


def _git_release_sha() -> str:
    result = subprocess.run(
        ["git", "rev-parse", "--short=12", "HEAD"],
        cwd=_REPO_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def _generate_tls_material(directory: Path) -> tuple[Path, Path]:
    cert_path = directory / "dante-observability-smoke-cert.pem"
    key_path = directory / "dante-observability-smoke-key.pem"
    subprocess.run(
        [
            "openssl",
            "req",
            "-x509",
            "-newkey",
            "rsa:2048",
            "-nodes",
            "-keyout",
            str(key_path),
            "-out",
            str(cert_path),
            "-days",
            "1",
            "-subj",
            "/CN=127.0.0.1",
            "-addext",
            "subjectAltName=IP:127.0.0.1",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    key_path.chmod(0o600)
    return cert_path, key_path


def _web_environment(
    *,
    backend_origin: str,
    collector_url: str,
    cert_path: Path,
    key_path: Path,
) -> dict[str, str]:
    clean_environment = {
        key: value
        for key, value in os.environ.items()
        if not key.startswith("VITE_") and not key.startswith("DANTE_E2E_")
    }
    return {
        **clean_environment,
        "DANTE_E2E_API_TARGET": backend_origin,
        "DANTE_E2E_TLS_CERT": str(cert_path),
        "DANTE_E2E_TLS_KEY": str(key_path),
        "VITE_DANTE_ENV": "local",
        "VITE_DANTE_RELEASE_SHA": _git_release_sha(),
        "VITE_DANTE_BUILD_ID": "local-faro-smoke",
        "VITE_DANTE_OBSERVABILITY_ENABLED": "true",
        "VITE_DANTE_FARO_COLLECTOR_URL": collector_url,
        "VITE_DANTE_FARO_SESSION_SAMPLE_RATE": "1.0",
        "VITE_DANTE_FARO_RESPECT_GPC": "true",
    }


def _wait_for_preview(process: subprocess.Popen[str]) -> None:
    deadline = time.monotonic() + _STARTUP_TIMEOUT_SECONDS
    last_error: Exception | None = None
    while time.monotonic() < deadline:
        if process.poll() is not None:
            raise SmokePreflightError(
                f"Web preview exited during startup with status {process.returncode}"
            )
        try:
            if _request_status(_WEB_ORIGIN, allow_self_signed=True) == 200:
                return
        except SmokePreflightError as error:
            last_error = error
        time.sleep(0.2)
    raise SmokePreflightError(
        f"Web preview did not become ready within {_STARTUP_TIMEOUT_SECONDS:.0f}s"
    ) from last_error


def _stop_process(process: subprocess.Popen[str] | None) -> None:
    if process is None or process.poll() is not None:
        return
    process.terminate()
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait(timeout=5)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Build and serve the DANTE Web Faro smoke surface. Backend and Alloy must "
            "already be healthy. No Grafana secret is read by this command."
        )
    )
    parser.add_argument("--backend-origin", default=_DEFAULT_BACKEND_ORIGIN)
    parser.add_argument("--alloy-ready-url", default=_DEFAULT_ALLOY_READY_URL)
    parser.add_argument("--faro-collector-url", default=_DEFAULT_FARO_COLLECTOR_URL)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    for executable in ("corepack", "git", "openssl"):
        _require_executable(executable)

    backend_origin = _assert_loopback_origin(
        args.backend_origin, label="backend origin"
    )
    alloy_ready_url = _assert_loopback_origin(
        args.alloy_ready_url, label="Alloy ready URL"
    )
    collector_url = _assert_loopback_origin(
        args.faro_collector_url, label="Faro collector URL"
    )
    _require_available_port(_WEB_PORT)
    _require_healthy(f"{backend_origin}/health/ready", label="DANTE backend readiness")
    _require_healthy(alloy_ready_url, label="Alloy readiness")
    _require_faro_cors(collector_url)

    stop_requested = False

    def request_stop(_signum: int, _frame: FrameType | None) -> None:
        nonlocal stop_requested
        stop_requested = True

    previous_sigint = signal.signal(signal.SIGINT, request_stop)
    previous_sigterm = signal.signal(signal.SIGTERM, request_stop)
    preview_process: subprocess.Popen[str] | None = None

    try:
        with tempfile.TemporaryDirectory(
            prefix="dante-observability-smoke-"
        ) as directory:
            cert_path, key_path = _generate_tls_material(Path(directory))
            environment = _web_environment(
                backend_origin=backend_origin,
                collector_url=collector_url,
                cert_path=cert_path,
                key_path=key_path,
            )
            subprocess.run(
                ["corepack", "pnpm", "--filter", "@dante/web", "build"],
                cwd=_REPO_ROOT,
                env=environment,
                check=True,
            )

            preview_process = subprocess.Popen(
                [
                    "corepack",
                    "pnpm",
                    "--filter",
                    "@dante/web",
                    "exec",
                    "vite",
                    "preview",
                    "--host",
                    "127.0.0.1",
                    "--port",
                    str(_WEB_PORT),
                    "--strictPort",
                ],
                cwd=_REPO_ROOT,
                env=environment,
                text=True,
            )
            _wait_for_preview(preview_process)
            print("DANTE Web/Faro smoke surface is ready:")
            print(f"  {_WEB_ORIGIN}")
            print(
                "Accept the one-day LOCAL certificate warning, navigate once, then wait 15s."
            )
            print(
                "If Global Privacy Control is enabled, telemetry is intentionally suppressed."
            )
            print("Press Ctrl+C here after checking Grafana Logs and Tempo.")

            while not stop_requested:
                if preview_process.poll() is not None:
                    raise SmokePreflightError(
                        f"Web preview exited unexpectedly with status {preview_process.returncode}"
                    )
                time.sleep(0.25)
    finally:
        _stop_process(preview_process)
        signal.signal(signal.SIGINT, previous_sigint)
        signal.signal(signal.SIGTERM, previous_sigterm)

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (SmokePreflightError, subprocess.CalledProcessError) as error:
        raise SystemExit(f"observability Web smoke failed: {error}") from error
