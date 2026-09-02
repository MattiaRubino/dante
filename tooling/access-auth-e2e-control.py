from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from uuid import UUID

import psycopg

_CONTAINER_PREFIX = "dante-fullstack-"
_DATABASE_PORT_KEY = "5432/tcp"
_SMTP_CONTROL_LABEL = "dante.e2e.smtp_control_port"
_E2E_CONTROL_ID_ENV = "DANTE_E2E_CONTROL_ID"
_E2E_CONTROL_LABEL = "dante.e2e.control_id"


@dataclass(frozen=True, slots=True)
class _ContainerDatabase:
    name: str
    host_port: int
    database_name: str
    admin_password: str
    smtp_control_port: int


def _docker_executable() -> str:
    executable = shutil.which("docker")
    if executable is None:
        raise RuntimeError("Required executable is unavailable: docker")
    return executable


def _docker(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(  # noqa: S603 - fixed Docker CLI argv; no shell interpretation
        [_docker_executable(), *args],
        check=True,
        text=True,
        capture_output=True,
    )


def _control_id() -> str:
    value = os.environ.get(_E2E_CONTROL_ID_ENV)
    if value is None or not value or value.strip() != value:
        raise RuntimeError(f"{_E2E_CONTROL_ID_ENV} must be a non-blank trimmed value.")
    return value


def _find_container() -> _ContainerDatabase:
    control_id = _control_id()
    listing = _docker(
        "ps",
        "--all",
        "--filter",
        f"name={_CONTAINER_PREFIX}",
        "--filter",
        f"label={_E2E_CONTROL_LABEL}={control_id}",
        "--format",
        "{{.Names}}",
    )
    names = [line.strip() for line in listing.stdout.splitlines() if line.strip()]
    if len(names) != 1:
        raise RuntimeError(
            "Expected exactly one disposable DANTE Access/Auth container for "
            f"control id {control_id!r}; found {len(names)}: {names}"
        )

    name = names[0]
    inspection_payload = json.loads(_docker("inspect", name).stdout)
    if not isinstance(inspection_payload, list) or len(inspection_payload) != 1:
        raise RuntimeError("Docker did not return one Access/Auth container inspection.")
    inspection = inspection_payload[0]

    environment = {}
    for item in inspection["Config"]["Env"]:
        key, separator, value = item.partition("=")
        if separator:
            environment[key] = value

    database_name = environment.get("POSTGRES_DB")
    admin_password = environment.get("POSTGRES_PASSWORD")
    bindings = inspection["HostConfig"]["PortBindings"].get(_DATABASE_PORT_KEY)
    labels = inspection["Config"].get("Labels") or {}
    smtp_control_port_raw = labels.get(_SMTP_CONTROL_LABEL)
    if not database_name or not admin_password or not bindings or not smtp_control_port_raw:
        raise RuntimeError("Disposable Access/Auth control metadata is incomplete.")

    host_port_raw = bindings[0].get("HostPort")
    if not host_port_raw:
        raise RuntimeError("Disposable Access/Auth PostgreSQL host port is unavailable.")

    try:
        smtp_control_port = int(smtp_control_port_raw)
    except ValueError as exc:
        raise RuntimeError("Disposable SMTP control port is malformed.") from exc
    if not 1 <= smtp_control_port <= 65_535:
        raise RuntimeError("Disposable SMTP control port is out of range.")

    return _ContainerDatabase(
        name=name,
        host_port=int(host_port_raw),
        database_name=database_name,
        admin_password=admin_password,
        smtp_control_port=smtp_control_port,
    )


def _connect(database: _ContainerDatabase) -> psycopg.Connection[tuple[object, ...]]:
    return psycopg.connect(
        host="127.0.0.1",
        port=database.host_port,
        dbname=database.database_name,
        user="postgres",
        password=database.admin_password,
        connect_timeout=2,
    )


def _wait_for_database(database: _ContainerDatabase) -> None:
    deadline = time.monotonic() + 30
    last_error: Exception | None = None
    while time.monotonic() < deadline:
        try:
            with _connect(database) as connection:
                row = connection.execute("SELECT 1").fetchone()
                if row == (1,):
                    return
        except psycopg.Error as exc:
            last_error = exc
            time.sleep(0.1)
    raise RuntimeError(
        "Disposable Access/Auth PostgreSQL did not recover after restart. "
        f"Last error: {last_error!r}"
    )


def _mutate_session(database: _ContainerDatabase, session_ref: UUID, *, expire: bool) -> None:
    with _connect(database) as connection:
        connection.execute("SET ROLE dante_owner")
        connection.execute("SET search_path TO pg_catalog,dante,pg_temp")
        if expire:
            cursor = connection.execute(
                """
                UPDATE dante.auth_session
                SET expires_at = authenticated_at + INTERVAL '1 microsecond'
                WHERE auth_session_ref = %s
                """,
                (session_ref,),
            )
        else:
            cursor = connection.execute(
                """
                UPDATE dante.auth_session
                SET revoked_at = GREATEST(clock_timestamp(), created_at),
                    revocation_reason_code = 'e2e_control'
                WHERE auth_session_ref = %s
                  AND revoked_at IS NULL
                """,
                (session_ref,),
            )
        if cursor.rowcount != 1:
            raise RuntimeError(f"Synthetic AuthSession mutation affected {cursor.rowcount} rows.")
        connection.commit()


def _email_control_url(database: _ContainerDatabase, path: str) -> str:
    return f"http://127.0.0.1:{database.smtp_control_port}{path}"


def _latest_email(
    database: _ContainerDatabase,
    *,
    recipient: str,
    subject: str | None,
    wait_seconds: float,
) -> str:
    query: dict[str, str] = {"recipient": recipient}
    if subject is not None:
        query["subject"] = subject
    url = _email_control_url(database, f"/latest?{urlencode(query)}")
    deadline = time.monotonic() + wait_seconds
    last_error: Exception | None = None

    while True:
        try:
            with urlopen(url, timeout=1) as response:  # noqa: S310 - loopback test control only
                if response.status != 200:
                    raise RuntimeError(
                        f"SMTP control returned unexpected status {response.status}."
                    )
                return response.read().decode("utf-8")
        except HTTPError as exc:
            if exc.code != 404:
                raise RuntimeError("SMTP capture control request failed.") from exc
            last_error = exc
        except URLError as exc:
            last_error = exc

        if time.monotonic() >= deadline:
            raise RuntimeError(
                "Expected captured email did not arrive before the bounded deadline. "
                f"Last control error: {last_error!r}"
            )
        time.sleep(0.05)


def _clear_emails(database: _ContainerDatabase) -> None:
    request = Request(  # noqa: S310 - internally constructed loopback test control URL
        _email_control_url(database, "/messages"),
        method="DELETE",
    )
    try:
        with urlopen(request, timeout=1) as response:  # noqa: S310 - loopback test control only
            if response.status != 204:
                raise RuntimeError(
                    f"SMTP clear control returned unexpected status {response.status}."
                )
    except (HTTPError, URLError) as exc:
        raise RuntimeError("SMTP capture clear request failed.") from exc


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Private loopback/process E2E control for the DANTE Access/Auth harness."
    )
    parser.add_argument(
        "action",
        choices=(
            "revoke-session",
            "expire-session",
            "database-stop",
            "database-start",
            "email-latest",
            "email-clear",
        ),
    )
    parser.add_argument("value", nargs="?")
    parser.add_argument("--subject")
    parser.add_argument("--wait-seconds", type=float, default=10.0)
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    database = _find_container()

    if args.action == "database-stop":
        _docker("stop", "--time", "0", database.name)
        return
    if args.action == "database-start":
        _docker("start", database.name)
        _wait_for_database(database)
        return
    if args.action == "email-clear":
        _clear_emails(database)
        return
    if args.action == "email-latest":
        if args.value is None:
            raise RuntimeError("email-latest requires a recipient address.")
        if args.wait_seconds <= 0 or args.wait_seconds > 60:
            raise RuntimeError("--wait-seconds must be within (0, 60].")
        message = _latest_email(
            database,
            recipient=args.value,
            subject=args.subject,
            wait_seconds=args.wait_seconds,
        )
        sys.stdout.write(f"{message}\n")
        return

    if args.value is None:
        raise RuntimeError(f"{args.action} requires an AuthSession reference.")
    session_ref = UUID(args.value)
    _mutate_session(
        database,
        session_ref,
        expire=args.action == "expire-session",
    )


if __name__ == "__main__":
    main()
