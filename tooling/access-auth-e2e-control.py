from __future__ import annotations

import argparse
import json
import subprocess
import time
from dataclasses import dataclass
from uuid import UUID

import psycopg

_CONTAINER_PREFIX = "dante-fullstack-"
_DATABASE_PORT_KEY = "5432/tcp"


@dataclass(frozen=True, slots=True)
class _ContainerDatabase:
    name: str
    host_port: int
    database_name: str
    admin_password: str


def _docker(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["docker", *args],
        check=True,
        text=True,
        capture_output=True,
    )


def _find_container() -> _ContainerDatabase:
    listing = _docker(
        "ps",
        "--all",
        "--filter",
        f"name={_CONTAINER_PREFIX}",
        "--format",
        "{{.Names}}",
    )
    names = [line.strip() for line in listing.stdout.splitlines() if line.strip()]
    if len(names) != 1:
        raise RuntimeError(
            "Expected exactly one disposable DANTE Access/Auth container; "
            f"found {len(names)}: {names}"
        )

    name = names[0]
    inspection_payload = json.loads(_docker("inspect", name).stdout)
    if not isinstance(inspection_payload, list) or len(inspection_payload) != 1:
        raise RuntimeError(
            "Docker did not return one Access/Auth container inspection."
        )
    inspection = inspection_payload[0]

    environment = {}
    for item in inspection["Config"]["Env"]:
        key, separator, value = item.partition("=")
        if separator:
            environment[key] = value

    database_name = environment.get("POSTGRES_DB")
    admin_password = environment.get("POSTGRES_PASSWORD")
    bindings = inspection["HostConfig"]["PortBindings"].get(_DATABASE_PORT_KEY)
    if not database_name or not admin_password or not bindings:
        raise RuntimeError("Disposable Access/Auth PostgreSQL metadata is incomplete.")

    host_port_raw = bindings[0].get("HostPort")
    if not host_port_raw:
        raise RuntimeError(
            "Disposable Access/Auth PostgreSQL host port is unavailable."
        )

    return _ContainerDatabase(
        name=name,
        host_port=int(host_port_raw),
        database_name=database_name,
        admin_password=admin_password,
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


def _mutate_session(
    database: _ContainerDatabase, session_ref: UUID, *, expire: bool
) -> None:
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
            raise RuntimeError(
                f"Synthetic AuthSession mutation affected {cursor.rowcount} rows."
            )
        connection.commit()


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Private loopback/process E2E control for the DANTE Access/Auth harness."
    )
    parser.add_argument(
        "action",
        choices=("revoke-session", "expire-session", "database-stop", "database-start"),
    )
    parser.add_argument("auth_session_ref", nargs="?")
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

    if args.auth_session_ref is None:
        raise RuntimeError(f"{args.action} requires an AuthSession reference.")
    session_ref = UUID(args.auth_session_ref)
    _mutate_session(
        database,
        session_ref,
        expire=args.action == "expire-session",
    )


if __name__ == "__main__":
    main()
