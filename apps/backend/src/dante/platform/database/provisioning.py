"""Explicit administrative provisioning for DANTE PostgreSQL security boundaries."""

import asyncio
from typing import Any

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from psycopg import AsyncConnection, sql

from dante.platform.config.database import (
    ConnectTimeoutSeconds,
    DatabasePort,
    DatabaseText,
)

OWNER_ROLE = "dante_owner"
MIGRATOR_ROLE = "dante_migrator"
RUNTIME_ROLE = "dante_runtime"


class ProvisioningSettings(BaseSettings):
    """Administrative inputs used only by the explicit provisioning command."""

    model_config = SettingsConfigDict(frozen=True, extra="ignore", validate_by_name=True)

    host: DatabaseText = Field(validation_alias="DANTE_DATABASE__HOST")
    port: DatabasePort = Field(default=5432, validation_alias="DANTE_DATABASE__PORT")
    name: DatabaseText = Field(validation_alias="DANTE_DATABASE__NAME")
    admin_user: DatabaseText = Field(default="postgres", validation_alias="DANTE_ADMIN__USER")
    admin_password: SecretStr = Field(validation_alias="DANTE_ADMIN__PASSWORD")
    migrator_password: SecretStr = Field(validation_alias="DANTE_MIGRATOR__PASSWORD")
    runtime_password: SecretStr = Field(validation_alias="DANTE_RUNTIME__PASSWORD")
    connect_timeout_seconds: ConnectTimeoutSeconds = Field(
        default=5,
        validation_alias="DANTE_DATABASE__CONNECT_TIMEOUT_SECONDS",
    )


async def _execute_statements(connection: AsyncConnection[Any]) -> None:
    statements = (
        """
        DO $$
        BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'dante_owner') THEN
                CREATE ROLE dante_owner NOLOGIN;
            END IF;
            IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'dante_migrator') THEN
                CREATE ROLE dante_migrator LOGIN;
            END IF;
            IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'dante_runtime') THEN
                CREATE ROLE dante_runtime LOGIN;
            END IF;
        END
        $$
        """,
        "ALTER ROLE dante_owner NOLOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE NOREPLICATION NOBYPASSRLS",
        "ALTER ROLE dante_migrator LOGIN NOINHERIT NOSUPERUSER NOCREATEDB NOCREATEROLE NOREPLICATION NOBYPASSRLS",
        "ALTER ROLE dante_runtime LOGIN NOINHERIT NOSUPERUSER NOCREATEDB NOCREATEROLE NOREPLICATION NOBYPASSRLS",
        "GRANT dante_owner TO dante_migrator WITH INHERIT FALSE, SET TRUE, ADMIN FALSE",
        "REVOKE dante_owner FROM dante_runtime",
        "REVOKE CREATE ON SCHEMA public FROM PUBLIC",
        "GRANT USAGE ON SCHEMA public TO dante_migrator, dante_runtime",
        "CREATE SCHEMA IF NOT EXISTS dante AUTHORIZATION dante_owner",
        "ALTER SCHEMA dante OWNER TO dante_owner",
        "REVOKE ALL ON SCHEMA dante FROM PUBLIC",
        "GRANT USAGE ON SCHEMA dante TO dante_runtime",
    )
    for statement in statements:
        await connection.execute(statement)


async def _configure_database_privileges(
    connection: AsyncConnection[Any],
    database_name: str,
) -> None:
    database = sql.Identifier(database_name)
    await connection.execute(
        sql.SQL("REVOKE CONNECT, TEMPORARY ON DATABASE {} FROM PUBLIC").format(database)
    )
    await connection.execute(
        sql.SQL("GRANT CONNECT ON DATABASE {} TO dante_migrator, dante_runtime").format(database)
    )
    await connection.execute(
        sql.SQL(
            "ALTER ROLE dante_runtime IN DATABASE {} SET search_path = dante, public"
        ).format(database)
    )
    await connection.execute(
        sql.SQL(
            "ALTER ROLE dante_migrator IN DATABASE {} SET search_path = dante, public"
        ).format(database)
    )


async def _configure_credentials(
    connection: AsyncConnection[Any],
    settings: ProvisioningSettings,
) -> None:
    await connection.execute(
        sql.SQL("ALTER ROLE dante_migrator PASSWORD {}").format(
            sql.Literal(settings.migrator_password.get_secret_value())
        )
    )
    await connection.execute(
        sql.SQL("ALTER ROLE dante_runtime PASSWORD {}").format(
            sql.Literal(settings.runtime_password.get_secret_value())
        )
    )


async def _configure_owner_defaults(connection: AsyncConnection[Any]) -> None:
    await connection.execute("SET ROLE dante_owner")
    try:
        statements = (
            "ALTER DEFAULT PRIVILEGES IN SCHEMA dante "
            "GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO dante_runtime",
            "ALTER DEFAULT PRIVILEGES IN SCHEMA dante "
            "GRANT USAGE ON SEQUENCES TO dante_runtime",
            "ALTER DEFAULT PRIVILEGES IN SCHEMA dante "
            "GRANT USAGE ON TYPES TO dante_runtime",
            "ALTER DEFAULT PRIVILEGES REVOKE EXECUTE ON ROUTINES FROM PUBLIC",
        )
        for statement in statements:
            await connection.execute(statement)
    finally:
        await connection.execute("RESET ROLE")


async def _reconcile_existing_runtime_privileges(
    connection: AsyncConnection[Any],
) -> None:
    await connection.execute(
        "GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA dante TO dante_runtime"
    )
    await connection.execute("GRANT USAGE ON ALL SEQUENCES IN SCHEMA dante TO dante_runtime")
    await connection.execute(
        """
        DO $$
        BEGIN
            IF to_regclass('dante.alembic_version') IS NOT NULL THEN
                EXECUTE 'REVOKE ALL PRIVILEGES ON TABLE dante.alembic_version FROM dante_runtime';
            END IF;
        END
        $$
        """
    )


async def provision_database(settings: ProvisioningSettings) -> None:
    """Idempotently provision DANTE roles, schema ownership and least-privilege ACLs."""
    connection = await AsyncConnection.connect(
        host=settings.host,
        port=settings.port,
        dbname=settings.name,
        user=settings.admin_user,
        password=settings.admin_password.get_secret_value(),
        connect_timeout=settings.connect_timeout_seconds,
        application_name="dante-provisioning",
        autocommit=True,
    )
    try:
        await _execute_statements(connection)
        await _configure_database_privileges(connection, settings.name)
        await _configure_credentials(connection, settings)
        await _configure_owner_defaults(connection)
        await _reconcile_existing_runtime_privileges(connection)
    finally:
        await connection.close()


async def _provision_from_environment() -> None:
    await provision_database(ProvisioningSettings())


def main() -> None:
    """Run explicit database provisioning from dedicated environment variables."""
    asyncio.run(_provision_from_environment())


if __name__ == "__main__":
    main()
