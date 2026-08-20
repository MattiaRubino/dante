"""Real PostgreSQL 18.4 acceptance harness for the CP3 persistence boundary."""

from __future__ import annotations

import asyncio
import secrets
import socket
import subprocess
import time
import uuid
from collections.abc import Generator
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import psycopg
import pytest
from alembic import command
from alembic.config import Config
from psycopg import sql
from pydantic import SecretStr
from sqlalchemy import URL

from dante.platform.config.database import DatabaseSettings
from dante.platform.database.provisioning import ProvisioningSettings, provision_database

_POSTGRES_IMAGE = "dante-postgres-local:18.4"
_BACKEND_ROOT = Path(__file__).resolve().parents[3]


@dataclass(frozen=True, slots=True)
class PostgresCluster:
    """One isolated PostgreSQL cluster created from the CP2-certified DANTE image."""

    host: str
    port: int
    admin_user: str
    admin_password: str
    migrator_password: str
    runtime_password: str
    container_name: str

    def stop(self) -> None:
        """Stop PostgreSQL while preserving the disposable acceptance cluster."""
        _docker("stop", "--signal", "SIGINT", "--timeout", "5", self.container_name)

    def start(self) -> None:
        """Restart PostgreSQL and wait for the exact CP3 acceptance version."""
        _docker("start", self.container_name)
        _wait_for_postgres(self)


@dataclass(frozen=True, slots=True)
class ProvisionedDatabase:
    """One fresh database inside the isolated CP3 acceptance cluster."""

    cluster: PostgresCluster
    name: str

    def sqlalchemy_url(self, user: str, password: str) -> URL:
        """Build a SQLAlchemy URL for a role in this acceptance database."""
        return URL.create(
            "postgresql+psycopg",
            username=user,
            password=password,
            host=self.cluster.host,
            port=self.cluster.port,
            database=self.name,
        )

    def runtime_settings(
        self,
        *,
        pool_size: int = 5,
        max_overflow: int = 10,
        pool_timeout_seconds: float = 30.0,
        readiness_timeout_seconds: float = 2.0,
    ) -> DatabaseSettings:
        """Return the exact runtime identity/configuration for this database."""
        return DatabaseSettings(
            host=self.cluster.host,
            port=self.cluster.port,
            name=self.name,
            user="dante_runtime",
            password=SecretStr(self.cluster.runtime_password),
            connect_timeout_seconds=1,
            pool_size=pool_size,
            max_overflow=max_overflow,
            pool_timeout_seconds=pool_timeout_seconds,
            readiness_timeout_seconds=readiness_timeout_seconds,
        )

    def connection_kwargs(self, user: str, password: str) -> dict[str, Any]:
        """Build psycopg keyword arguments without assembling a DSN string."""
        return {
            "host": self.cluster.host,
            "port": self.cluster.port,
            "dbname": self.name,
            "user": user,
            "password": password,
            "connect_timeout": 2,
        }


def _docker(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(  # noqa: S603
        ["docker", *args],  # noqa: S607
        check=check,
        capture_output=True,
        text=True,
    )


def _free_loopback_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listener:
        listener.bind(("127.0.0.1", 0))
        return int(listener.getsockname()[1])


def _wait_for_postgres(cluster: PostgresCluster) -> None:
    deadline = time.monotonic() + 60
    last_error: Exception | None = None
    while time.monotonic() < deadline:
        try:
            with psycopg.connect(
                host=cluster.host,
                port=cluster.port,
                dbname="dante",
                user=cluster.admin_user,
                password=cluster.admin_password,
                connect_timeout=1,
            ) as connection:
                version = connection.execute("SHOW server_version_num").fetchone()
                if version is not None and version[0] == "180004":
                    return
        except psycopg.Error as error:
            last_error = error
            time.sleep(0.25)

    logs = _docker("logs", cluster.container_name, check=False).stdout
    pytest.fail(
        "CP3 PostgreSQL acceptance cluster did not become ready as PostgreSQL 18.4. "
        f"Last connection error: {last_error!r}\nContainer logs:\n{logs}"
    )


def _create_database(cluster: PostgresCluster, database_name: str) -> None:
    with psycopg.connect(
        host=cluster.host,
        port=cluster.port,
        dbname="postgres",
        user=cluster.admin_user,
        password=cluster.admin_password,
        autocommit=True,
    ) as connection:
        connection.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(database_name)))

    with psycopg.connect(
        host=cluster.host,
        port=cluster.port,
        dbname=database_name,
        user=cluster.admin_user,
        password=cluster.admin_password,
        autocommit=True,
    ) as connection:
        connection.execute("CREATE EXTENSION postgis VERSION '3.6.4'")
        connection.execute("CREATE EXTENSION vector VERSION '0.8.6'")
        connection.execute("CREATE EXTENSION pg_trgm")
        connection.execute("CREATE EXTENSION unaccent")
        connection.execute("CREATE EXTENSION pg_stat_statements")


def _drop_database(cluster: PostgresCluster, database_name: str) -> None:
    with psycopg.connect(
        host=cluster.host,
        port=cluster.port,
        dbname="postgres",
        user=cluster.admin_user,
        password=cluster.admin_password,
        autocommit=True,
    ) as connection:
        connection.execute(
            "SELECT pg_terminate_backend(pid) "
            "FROM pg_stat_activity "
            "WHERE datname = %s AND pid <> pg_backend_pid()",
            (database_name,),
        )
        connection.execute(sql.SQL("DROP DATABASE {}").format(sql.Identifier(database_name)))


def _provision(cluster: PostgresCluster, database_name: str) -> None:
    settings = ProvisioningSettings(
        host=cluster.host,
        port=cluster.port,
        name=database_name,
        admin_user=cluster.admin_user,
        admin_password=SecretStr(cluster.admin_password),
        migrator_password=SecretStr(cluster.migrator_password),
        runtime_password=SecretStr(cluster.runtime_password),
        connect_timeout_seconds=2,
    )
    asyncio.run(provision_database(settings))


def _alembic_config(database: ProvisionedDatabase) -> Config:
    config = Config(toml_file=str(_BACKEND_ROOT / "pyproject.toml"))
    config.attributes["database_url"] = database.sqlalchemy_url(
        "dante_migrator",
        database.cluster.migrator_password,
    )
    return config


@pytest.fixture(scope="session")
def postgres_cluster() -> Generator[PostgresCluster]:
    """Start one disposable cluster without touching the ordinary LOCAL DANTE cluster."""
    image_check = _docker("image", "inspect", _POSTGRES_IMAGE, check=False)
    if image_check.returncode != 0:
        pytest.fail(
            "Required CP2 image dante-postgres-local:18.4 is not available. "
            "Build it with `docker compose -f infra/compose/local.yaml build postgres`."
        )

    cluster = PostgresCluster(
        host="127.0.0.1",
        port=_free_loopback_port(),
        admin_user="postgres",
        admin_password=secrets.token_urlsafe(32),
        migrator_password=secrets.token_urlsafe(32),
        runtime_password=secrets.token_urlsafe(32),
        container_name=f"dante-cp3-pytest-{uuid.uuid4().hex[:12]}",
    )

    _docker(
        "run",
        "--detach",
        "--name",
        cluster.container_name,
        "--publish",
        f"127.0.0.1:{cluster.port}:5432",
        "--env",
        "POSTGRES_DB=dante",
        "--env",
        f"POSTGRES_USER={cluster.admin_user}",
        "--env",
        f"POSTGRES_PASSWORD={cluster.admin_password}",
        _POSTGRES_IMAGE,
        "postgres",
        "-c",
        "shared_preload_libraries=pg_stat_statements",
        "-c",
        "compute_query_id=on",
    )

    try:
        _wait_for_postgres(cluster)
        yield cluster
    finally:
        _docker("rm", "--force", cluster.container_name, check=False)


@pytest.fixture
def provisioned_database(postgres_cluster: PostgresCluster) -> Generator[ProvisionedDatabase]:
    """Create a fresh extension-complete database and apply CP3 security provisioning."""
    database = ProvisionedDatabase(
        cluster=postgres_cluster,
        name=f"dante_cp3_{uuid.uuid4().hex[:16]}",
    )
    _create_database(postgres_cluster, database.name)
    _provision(postgres_cluster, database.name)

    try:
        yield database
    finally:
        _drop_database(postgres_cluster, database.name)


@pytest.fixture
def alembic_config(provisioned_database: ProvisionedDatabase) -> Config:
    """Return Alembic configured with only the dedicated migrator credential."""
    return _alembic_config(provisioned_database)


@pytest.fixture
def migrated_database(
    provisioned_database: ProvisionedDatabase,
    alembic_config: Config,
) -> ProvisionedDatabase:
    """Return a fresh provisioned database migrated from base to repository head."""
    command.upgrade(alembic_config, "head")
    return provisioned_database
