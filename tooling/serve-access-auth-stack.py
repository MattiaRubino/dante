from __future__ import annotations

import asyncio
import os
import secrets
import shutil
import signal
import socket
import subprocess
import tempfile
import threading
import time
import uuid
from base64 import urlsafe_b64encode
from datetime import UTC, datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from types import FrameType
from typing import override
from uuid import uuid7

import psycopg
import uvicorn
from access_auth_smtp_capture import start_smtp_capture
from alembic import command
from alembic.config import Config
from dante.auth.email import normalize_email
from dante.auth.passwords import PasswordKdf
from dante.bootstrap.app import create_app
from dante.platform.config.auth import AuthSettings, SmtpSecurity
from dante.platform.config.database import DatabaseSettings
from dante.platform.config.settings import Environment, Settings
from dante.platform.database.provisioning import (
    ProvisioningSettings,
    provision_database,
)
from pydantic import SecretStr
from sqlalchemy import URL

_POSTGRES_IMAGE = "dante-postgres-local:18.6"
_REPO_ROOT = Path(__file__).resolve().parents[1]
_BACKEND_ROOT = _REPO_ROOT / "apps" / "backend"
_WEB_ORIGIN = "https://127.0.0.1:4173"
_WEB_PORT = 4173
_DATABASE_NAME = "dante_e2e"
_EMAIL = "synthetic.user@example.com"
_PASSWORD = "correct horse battery staple"
_PEPPER_KEY_ID = "e2e-password-v1"
_OTP_KEY_ID = "e2e-signup-otp-v1"
_PEPPER = urlsafe_b64encode(b"p" * 32).rstrip(b"=").decode("ascii")
_CSRF_KEY = urlsafe_b64encode(b"c" * 32).rstrip(b"=").decode("ascii")
_OTP_KEY = urlsafe_b64encode(b"o" * 32).rstrip(b"=").decode("ascii")
_SMTP_CONTROL_LABEL = "dante.e2e.smtp_control_port"
_EMAIL_RUNTIME_LABEL = "loopback SMTP capture"


class _HibpHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        if not self.path.startswith("/range/"):
            self.send_response(404)
            self.end_headers()
            return

        payload = f"{'0' * 35}:0\r\n".encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    @override
    def log_message(self, _format: str, *args: object) -> None:
        _ = args


def _run(
    args: list[str],
    *,
    cwd: Path | None = None,
    env: dict[str, str] | None = None,
    check: bool = True,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        cwd=cwd,
        env=env,
        check=check,
        text=True,
        capture_output=True,
    )


def _docker(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return _run(["docker", *args], check=check)


def _free_loopback_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listener:
        listener.bind(("127.0.0.1", 0))
        return int(listener.getsockname()[1])


def _require_executable(name: str) -> None:
    if shutil.which(name) is None:
        raise RuntimeError(f"Required executable is unavailable: {name}")


def _wait_for_postgres(*, port: int, password: str) -> None:
    deadline = time.monotonic() + 60
    last_error: Exception | None = None
    while time.monotonic() < deadline:
        try:
            with psycopg.connect(
                host="127.0.0.1",
                port=port,
                dbname=_DATABASE_NAME,
                user="postgres",
                password=password,
                connect_timeout=1,
            ) as connection:
                row = connection.execute("SHOW server_version_num").fetchone()
                if row is not None and row[0] == "180006":
                    return
        except psycopg.Error as error:
            last_error = error
            time.sleep(0.25)

    raise RuntimeError(
        "Disposable PostgreSQL did not become ready as PostgreSQL 18.6. "
        f"Last connection error: {last_error!r}"
    )


def _create_extensions(*, port: int, password: str) -> None:
    with psycopg.connect(
        host="127.0.0.1",
        port=port,
        dbname=_DATABASE_NAME,
        user="postgres",
        password=password,
        autocommit=True,
    ) as connection:
        connection.execute("CREATE EXTENSION postgis VERSION '3.6.4'")
        connection.execute("CREATE EXTENSION vector VERSION '0.8.6'")
        connection.execute("CREATE EXTENSION pg_trgm")
        connection.execute("CREATE EXTENSION unaccent")
        connection.execute("CREATE EXTENSION pg_stat_statements")


def _provision_database(
    *,
    port: int,
    admin_password: str,
    migrator_password: str,
    runtime_password: str,
    observer_password: str,
) -> None:
    asyncio.run(
        provision_database(
            ProvisioningSettings(
                host="127.0.0.1",
                port=port,
                name=_DATABASE_NAME,
                admin_user="postgres",
                admin_password=SecretStr(admin_password),
                migrator_password=SecretStr(migrator_password),
                runtime_password=SecretStr(runtime_password),
                observer_password=SecretStr(observer_password),
                connect_timeout_seconds=2,
            )
        )
    )


def _migrate_database(*, port: int, migrator_password: str) -> None:
    config = Config(toml_file=str(_BACKEND_ROOT / "pyproject.toml"))
    config.attributes["database_url"] = URL.create(
        "postgresql+psycopg",
        username="dante_migrator",
        password=migrator_password,
        host="127.0.0.1",
        port=port,
        database=_DATABASE_NAME,
    )
    command.upgrade(config, "head")


def _auth_settings(hibp_base_url: str, smtp_port: int) -> AuthSettings:
    return AuthSettings(
        canonical_web_origin=_WEB_ORIGIN,
        password_current_pepper_key_id=_PEPPER_KEY_ID,
        password_peppers={_PEPPER_KEY_ID: SecretStr(_PEPPER)},
        csrf_key=SecretStr(_CSRF_KEY),
        signup_otp_current_key_id=_OTP_KEY_ID,
        signup_otp_keys={_OTP_KEY_ID: SecretStr(_OTP_KEY)},
        smtp_host="127.0.0.1",
        smtp_port=smtp_port,
        smtp_security=SmtpSecurity.PLAIN,
        smtp_from_address="no-reply@dante.test",
        smtp_timeout_seconds=2,
        email_queue_capacity=128,
        email_worker_count=2,
        email_shutdown_drain_seconds=5,
        session_max_age_seconds=3_600,
        session_idle_timeout_seconds=900,
        kdf_max_concurrency=2,
        kdf_max_queue_depth=4,
        kdf_queue_timeout_seconds=2,
        signin_rate_capacity=100,
        signin_rate_window_seconds=60,
        signup_rate_capacity=50,
        signup_source_rate_capacity=200,
        recovery_rate_capacity=50,
        recovery_source_rate_capacity=200,
        reauth_rate_capacity=50,
        hibp_base_url=hibp_base_url,
        hibp_timeout_seconds=1,
        hibp_max_connections=4,
    )


async def _hash_password(auth_settings: AuthSettings) -> tuple[str, str]:
    kdf = PasswordKdf(
        pepper_ring=auth_settings.password_pepper_bytes,
        current_pepper_key_id=auth_settings.password_current_pepper_key_id,
        max_concurrency=1,
        max_queue_depth=0,
        queue_timeout_seconds=2,
    )
    await kdf.start()
    try:
        return await kdf.hash_new_password(_PASSWORD)
    finally:
        await kdf.aclose()


def _seed_account(
    *,
    port: int,
    migrator_password: str,
    auth_settings: AuthSettings,
) -> None:
    verifier, pepper_key_id = asyncio.run(_hash_password(auth_settings))
    normalized_email = normalize_email(_EMAIL)
    now = datetime.now(UTC)

    with psycopg.connect(
        host="127.0.0.1",
        port=port,
        dbname=_DATABASE_NAME,
        user="dante_migrator",
        password=migrator_password,
        connect_timeout=2,
    ) as connection:
        connection.execute("SET ROLE dante_owner")
        connection.execute("SET search_path TO pg_catalog,dante,pg_temp")
        account_ref = uuid7()
        connection.execute(
            """
            INSERT INTO dante.account(
                account_ref, status_code, created_at, disabled_at
            )
            VALUES (%s, 'active', %s, NULL)
            """,
            (account_ref, now),
        )
        connection.execute(
            """
            INSERT INTO dante.email_identity(
                email_identity_ref,
                account_ref,
                address,
                comparison_key,
                created_at,
                verified_at
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (
                uuid7(),
                account_ref,
                normalized_email.address,
                normalized_email.comparison_key,
                now,
                now,
            ),
        )
        connection.execute(
            """
            INSERT INTO dante.password_credential(
                password_credential_ref,
                account_ref,
                verifier,
                pepper_key_id,
                created_at,
                updated_at
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (uuid7(), account_ref, verifier, pepper_key_id, now, now),
        )
        connection.commit()


def _runtime_settings(
    *,
    port: int,
    runtime_password: str,
    auth_settings: AuthSettings,
) -> Settings:
    return Settings(
        env=Environment.LOCAL,
        release_sha="fullstack-e2e",
        build_id="fullstack-e2e",
        debug=False,
        database=DatabaseSettings(
            host="127.0.0.1",
            port=port,
            name=_DATABASE_NAME,
            user="dante_runtime",
            password=SecretStr(runtime_password),
            connect_timeout_seconds=1,
            pool_size=5,
            max_overflow=5,
            pool_timeout_seconds=5,
            readiness_timeout_seconds=2,
        ),
        auth=auth_settings,
    )


def _start_api(settings: Settings, port: int) -> tuple[uvicorn.Server, threading.Thread]:
    server = uvicorn.Server(
        uvicorn.Config(
            create_app(settings),
            host="127.0.0.1",
            port=port,
            log_level="warning",
            access_log=False,
        )
    )
    thread = threading.Thread(target=server.run, daemon=True)
    thread.start()

    deadline = time.monotonic() + 30
    while time.monotonic() < deadline:
        if server.started:
            return server, thread
        if not thread.is_alive():
            raise RuntimeError("FastAPI full-stack server exited during startup.")
        time.sleep(0.05)
    raise RuntimeError("FastAPI full-stack server did not become ready.")


def _generate_tls_material(directory: Path) -> tuple[Path, Path]:
    cert_path = directory / "dante-e2e-cert.pem"
    key_path = directory / "dante-e2e-key.pem"
    _run(
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
        ]
    )
    return cert_path, key_path


def _build_web() -> None:
    build = _run(["pnpm", "--filter", "@dante/web", "build"], cwd=_REPO_ROOT)
    if build.stdout:
        print(build.stdout, end="")
    if build.stderr:
        print(build.stderr, end="")


def _start_preview(*, api_port: int, cert_path: Path, key_path: Path) -> subprocess.Popen[str]:
    env = os.environ.copy()
    env["DANTE_E2E_API_TARGET"] = f"http://127.0.0.1:{api_port}"
    env["DANTE_E2E_TLS_CERT"] = str(cert_path)
    env["DANTE_E2E_TLS_KEY"] = str(key_path)
    return subprocess.Popen(
        [
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
        env=env,
        text=True,
    )


def _stop_process(process: subprocess.Popen[str] | None) -> None:
    if process is None or process.poll() is not None:
        return
    process.terminate()
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait(timeout=5)


def main() -> None:
    for executable in ("docker", "openssl", "pnpm"):
        _require_executable(executable)

    image_check = _docker("image", "inspect", _POSTGRES_IMAGE, check=False)
    if image_check.returncode != 0:
        raise RuntimeError(
            "Required image dante-postgres-local:18.6 is unavailable. "
            "Build it with `docker compose -f infra/compose/local.yaml build postgres`."
        )

    stop_event = threading.Event()

    def request_stop(_signum: int, _frame: FrameType | None) -> None:
        stop_event.set()

    signal.signal(signal.SIGTERM, request_stop)
    signal.signal(signal.SIGINT, request_stop)

    postgres_port = _free_loopback_port()
    api_port = _free_loopback_port()
    admin_password = secrets.token_urlsafe(32)
    migrator_password = secrets.token_urlsafe(32)
    runtime_password = secrets.token_urlsafe(32)
    observer_password = secrets.token_urlsafe(32)
    container_name = f"dante-fullstack-{uuid.uuid4().hex[:12]}"

    hibp_server = ThreadingHTTPServer(("127.0.0.1", 0), _HibpHandler)
    hibp_thread = threading.Thread(target=hibp_server.serve_forever, daemon=True)
    hibp_thread.start()
    hibp_port = int(hibp_server.server_address[1])
    hibp_base_url = f"http://127.0.0.1:{hibp_port}"
    smtp_capture = start_smtp_capture()

    api_server: uvicorn.Server | None = None
    api_thread: threading.Thread | None = None
    preview_process: subprocess.Popen[str] | None = None
    container_started = False

    try:
        _docker(
            "run",
            "--detach",
            "--name",
            container_name,
            "--label",
            f"{_SMTP_CONTROL_LABEL}={smtp_capture.control_port}",
            "--publish",
            f"127.0.0.1:{postgres_port}:5432",
            "--env",
            f"POSTGRES_DB={_DATABASE_NAME}",
            "--env",
            "POSTGRES_USER=postgres",
            "--env",
            f"POSTGRES_PASSWORD={admin_password}",
            _POSTGRES_IMAGE,
            "postgres",
            "-c",
            "shared_preload_libraries=pg_stat_statements",
            "-c",
            "compute_query_id=on",
        )
        container_started = True

        _wait_for_postgres(port=postgres_port, password=admin_password)
        _create_extensions(port=postgres_port, password=admin_password)
        _provision_database(
            port=postgres_port,
            admin_password=admin_password,
            migrator_password=migrator_password,
            runtime_password=runtime_password,
            observer_password=observer_password,
        )
        _migrate_database(port=postgres_port, migrator_password=migrator_password)

        auth_settings = _auth_settings(hibp_base_url, smtp_capture.smtp_port)
        _seed_account(
            port=postgres_port,
            migrator_password=migrator_password,
            auth_settings=auth_settings,
        )

        api_server, api_thread = _start_api(
            _runtime_settings(
                port=postgres_port,
                runtime_password=runtime_password,
                auth_settings=auth_settings,
            ),
            api_port,
        )

        _build_web()
        with tempfile.TemporaryDirectory(prefix="dante-access-auth-e2e-") as directory:
            cert_path, key_path = _generate_tls_material(Path(directory))
            preview_process = _start_preview(
                api_port=api_port,
                cert_path=cert_path,
                key_path=key_path,
            )
            print(
                "DANTE Access/Auth full-stack ready: "
                f"{_WEB_ORIGIN} using disposable PostgreSQL 18.6 + {_EMAIL_RUNTIME_LABEL}."
            )

            while not stop_event.wait(0.25):
                if preview_process.poll() is not None:
                    raise RuntimeError(
                        "Vite HTTPS preview exited before the full-stack run completed."
                    )
    finally:
        _stop_process(preview_process)
        if api_server is not None:
            api_server.should_exit = True
        if api_thread is not None:
            api_thread.join(timeout=10)
        smtp_capture.close()
        hibp_server.shutdown()
        hibp_thread.join(timeout=2)
        hibp_server.server_close()
        if container_started:
            _docker("rm", "--force", container_name, check=False)


if __name__ == "__main__":
    main()
