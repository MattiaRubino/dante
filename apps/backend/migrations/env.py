"""Alembic environment for DANTE-owned PostgreSQL schema evolution."""

import asyncio

from alembic import context
from sqlalchemy import URL, Connection
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.pool import NullPool

from dante.platform.config.database import MigrationDatabaseSettings
from dante.platform.database.mappings import MAPPED_TABLES
from dante.platform.database.metadata import DANTE_SCHEMA, Base

config = context.config

if {table.fullname for table in MAPPED_TABLES} != set(Base.metadata.tables):
    raise RuntimeError("DANTE SQLAlchemy mapping registration is incomplete")

target_metadata = Base.metadata

_MIGRATOR_ROLE = "dante_migrator"
_OWNER_ROLE = "dante_owner"
_TRUSTED_SEARCH_PATH = "pg_catalog,dante,pg_temp"


def _migration_connection_config() -> tuple[URL, int]:
    injected = config.attributes.get("database_url")
    if isinstance(injected, URL):
        if injected.username != _MIGRATOR_ROLE:
            raise RuntimeError(
                "DANTE Alembic connection must authenticate exactly as dante_migrator"
            )
        return injected, 5

    settings = MigrationDatabaseSettings()
    return settings.sqlalchemy_url(), settings.connect_timeout_seconds


def _include_name(
    name: str | None,
    type_: str,
    parent_names: dict[str, str | None],
) -> bool:
    if type_ == "schema":
        return name == DANTE_SCHEMA
    if type_ == "table":
        return parent_names.get("schema_name") == DANTE_SCHEMA
    return True


def _assert_identity(
    connection: Connection,
    *,
    expected_session_user: str,
    expected_current_user: str,
) -> None:
    row = connection.exec_driver_sql(
        "SELECT session_user, current_user, current_setting('search_path')"
    ).one()
    normalized_search_path = str(row[2]).replace(" ", "")
    if (
        row[0] != expected_session_user
        or row[1] != expected_current_user
        or normalized_search_path != _TRUSTED_SEARCH_PATH
    ):
        raise RuntimeError("DANTE Alembic database identity/search_path precondition failed")


def _configure(connection: Connection) -> None:
    _assert_identity(
        connection,
        expected_session_user=_MIGRATOR_ROLE,
        expected_current_user=_MIGRATOR_ROLE,
    )

    connection.exec_driver_sql("SET ROLE dante_owner")
    _assert_identity(
        connection,
        expected_session_user=_MIGRATOR_ROLE,
        expected_current_user=_OWNER_ROLE,
    )
    connection.commit()

    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        include_schemas=True,
        include_name=_include_name,
        compare_type=True,
        compare_server_default=True,
        version_table_schema=DANTE_SCHEMA,
    )

    with context.begin_transaction():
        context.run_migrations()
        connection.exec_driver_sql(
            "REVOKE ALL PRIVILEGES ON TABLE dante.alembic_version FROM dante_runtime"
        )

    connection.exec_driver_sql("RESET ROLE")
    connection.commit()


async def _run_online() -> None:
    database_url, connect_timeout_seconds = _migration_connection_config()
    engine = create_async_engine(
        database_url,
        connect_args={
            "connect_timeout": connect_timeout_seconds,
            "application_name": "dante-migrator",
            "options": "-c search_path=pg_catalog,dante,pg_temp",
        },
        poolclass=NullPool,
        hide_parameters=True,
    )
    try:
        async with engine.connect() as connection:
            await connection.run_sync(_configure)
    finally:
        await engine.dispose()


def run_migrations_offline() -> None:
    """Reject offline execution because DANTE migrations require live role enforcement."""
    raise RuntimeError("DANTE Alembic migrations require an online PostgreSQL connection")


def run_migrations_online() -> None:
    """Run Alembic with the dedicated migrator identity and owner role."""
    asyncio.run(_run_online())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
