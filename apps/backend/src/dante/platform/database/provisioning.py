"""Explicit administrative provisioning for DANTE PostgreSQL security boundaries."""

import asyncio
from typing import Any

from psycopg import AsyncConnection, sql
from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

from dante.platform.config.database import (
    ConnectTimeoutSeconds,
    DatabasePort,
    DatabaseText,
)

OWNER_ROLE = "dante_owner"
MIGRATOR_ROLE = "dante_migrator"
RUNTIME_ROLE = "dante_runtime"
_DANTE_ROLES = frozenset((OWNER_ROLE, MIGRATOR_ROLE, RUNTIME_ROLE))


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


async def _ensure_roles_and_schema(connection: AsyncConnection[Any]) -> None:
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
        "ALTER ROLE dante_owner NOLOGIN INHERIT NOSUPERUSER NOCREATEDB NOCREATEROLE "
        "NOREPLICATION NOBYPASSRLS PASSWORD NULL",
        "ALTER ROLE dante_migrator LOGIN NOINHERIT NOSUPERUSER NOCREATEDB "
        "NOCREATEROLE NOREPLICATION NOBYPASSRLS",
        "ALTER ROLE dante_runtime LOGIN NOINHERIT NOSUPERUSER NOCREATEDB "
        "NOCREATEROLE NOREPLICATION NOBYPASSRLS",
        "REVOKE CREATE ON SCHEMA public FROM PUBLIC",
        "CREATE SCHEMA IF NOT EXISTS dante AUTHORIZATION dante_owner",
        "ALTER SCHEMA dante OWNER TO dante_owner",
        "REVOKE ALL ON SCHEMA dante FROM PUBLIC",
    )
    for statement in statements:
        await connection.execute(statement)


async def _reconcile_role_memberships(connection: AsyncConnection[Any]) -> None:
    result = await connection.execute(
        """
        SELECT granted.rolname, member.rolname
        FROM pg_auth_members AS membership
        JOIN pg_roles AS granted ON granted.oid = membership.roleid
        JOIN pg_roles AS member ON member.oid = membership.member
        WHERE granted.rolname IN ('dante_owner', 'dante_migrator', 'dante_runtime')
           OR member.rolname IN ('dante_owner', 'dante_migrator', 'dante_runtime')
        """
    )
    rows = [(str(row[0]), str(row[1])) for row in await result.fetchall()]

    external_edges = [
        (granted_role, member_role)
        for granted_role, member_role in rows
        if granted_role not in _DANTE_ROLES or member_role not in _DANTE_ROLES
    ]
    if external_edges:
        raise RuntimeError(
            "DANTE role membership graph contains external-role edges; "
            "manual security review is required"
        )

    for granted_role, member_role in rows:
        await connection.execute(
            sql.SQL("REVOKE {} FROM {}").format(
                sql.Identifier(granted_role),
                sql.Identifier(member_role),
            )
        )

    await connection.execute(
        "GRANT dante_owner TO dante_migrator "
        "WITH INHERIT FALSE, SET TRUE, ADMIN FALSE"
    )


async def _configure_database_privileges(
    connection: AsyncConnection[Any],
    database_name: str,
) -> None:
    database = sql.Identifier(database_name)
    statements = (
        sql.SQL(
            "REVOKE CONNECT, TEMPORARY, CREATE ON DATABASE {} FROM PUBLIC"
        ).format(database),
        sql.SQL(
            "REVOKE TEMPORARY, CREATE ON DATABASE {} FROM dante_migrator, dante_runtime"
        ).format(database),
        sql.SQL(
            "GRANT CONNECT ON DATABASE {} TO dante_migrator, dante_runtime"
        ).format(database),
        sql.SQL(
            "ALTER ROLE dante_runtime IN DATABASE {} "
            "SET search_path = pg_catalog, dante, pg_temp"
        ).format(database),
        sql.SQL(
            "ALTER ROLE dante_migrator IN DATABASE {} "
            "SET search_path = pg_catalog, dante, pg_temp"
        ).format(database),
    )
    for statement in statements:
        await connection.execute(statement)

    await connection.execute(
        "REVOKE ALL ON SCHEMA public FROM PUBLIC, dante_migrator, dante_runtime"
    )
    await connection.execute("GRANT USAGE ON SCHEMA public TO dante_owner")
    await connection.execute(
        "REVOKE ALL ON SCHEMA dante FROM PUBLIC, dante_migrator, dante_runtime"
    )
    await connection.execute("GRANT USAGE ON SCHEMA dante TO dante_runtime")


async def _configure_credentials(
    connection: AsyncConnection[Any],
    settings: ProvisioningSettings,
) -> None:
    await connection.execute("SET password_encryption = 'scram-sha-256'")
    setting_result = await connection.execute("SHOW password_encryption")
    setting_row = await setting_result.fetchone()
    if setting_row != ("scram-sha-256",):
        raise RuntimeError("DANTE provisioning requires SCRAM-SHA-256 password encryption")

    encoding = connection.info.encoding
    credentials = (
        (MIGRATOR_ROLE, settings.migrator_password),
        (RUNTIME_ROLE, settings.runtime_password),
    )
    for role_name, password in credentials:
        connection.pgconn.change_password(
            role_name.encode(encoding),
            password.get_secret_value().encode(encoding),
        )

    await connection.execute("ALTER ROLE dante_owner PASSWORD NULL")


async def _configure_owner_defaults(connection: AsyncConnection[Any]) -> None:
    await connection.execute("SET ROLE dante_owner")
    try:
        statements = (
            "ALTER DEFAULT PRIVILEGES IN SCHEMA dante "
            "REVOKE ALL ON TABLES FROM dante_runtime",
            "ALTER DEFAULT PRIVILEGES IN SCHEMA dante "
            "REVOKE ALL ON SEQUENCES FROM dante_runtime",
            "ALTER DEFAULT PRIVILEGES IN SCHEMA dante "
            "REVOKE ALL ON TYPES FROM dante_runtime",
            "ALTER DEFAULT PRIVILEGES IN SCHEMA dante "
            "REVOKE ALL ON ROUTINES FROM dante_runtime",
            "ALTER DEFAULT PRIVILEGES REVOKE EXECUTE ON ROUTINES FROM PUBLIC",
            "ALTER DEFAULT PRIVILEGES REVOKE USAGE ON TYPES FROM PUBLIC",
        )
        for statement in statements:
            await connection.execute(statement)
    finally:
        await connection.execute("RESET ROLE")


async def _reconcile_technical_runtime_privileges(
    connection: AsyncConnection[Any],
) -> None:
    await connection.execute(
        """
        DO $$
        BEGIN
            IF to_regclass('dante.alembic_version') IS NOT NULL THEN
                REVOKE ALL PRIVILEGES ON TABLE dante.alembic_version FROM dante_runtime;
            END IF;
        END
        $$
        """
    )


async def _verify_security_posture(
    connection: AsyncConnection[Any],
    database_name: str,
) -> None:
    role_result = await connection.execute(
        """
        SELECT rolname, rolcanlogin, rolinherit, rolsuper, rolcreatedb,
               rolcreaterole, rolreplication, rolbypassrls
        FROM pg_roles
        WHERE rolname IN ('dante_owner', 'dante_migrator', 'dante_runtime')
        """
    )
    role_rows = await role_result.fetchall()
    roles = {str(row[0]): tuple(row[1:]) for row in role_rows}
    expected_roles = {
        OWNER_ROLE: (False, True, False, False, False, False, False),
        MIGRATOR_ROLE: (True, False, False, False, False, False, False),
        RUNTIME_ROLE: (True, False, False, False, False, False, False),
    }
    if roles != expected_roles:
        raise RuntimeError("DANTE role attributes failed P0 reconciliation")

    membership_result = await connection.execute(
        """
        SELECT granted.rolname, member.rolname,
               membership.admin_option,
               membership.inherit_option,
               membership.set_option
        FROM pg_auth_members AS membership
        JOIN pg_roles AS granted ON granted.oid = membership.roleid
        JOIN pg_roles AS member ON member.oid = membership.member
        WHERE granted.rolname IN ('dante_owner', 'dante_migrator', 'dante_runtime')
           OR member.rolname IN ('dante_owner', 'dante_migrator', 'dante_runtime')
        """
    )
    membership_rows = await membership_result.fetchall()
    normalized_memberships = {
        (str(row[0]), str(row[1]), bool(row[2]), bool(row[3]), bool(row[4]))
        for row in membership_rows
    }
    expected_memberships = {
        (OWNER_ROLE, MIGRATOR_ROLE, False, False, True),
    }
    if normalized_memberships != expected_memberships:
        raise RuntimeError("DANTE role membership graph failed P0 reconciliation")

    database_result = await connection.execute(
        """
        SELECT
            has_database_privilege('dante_runtime', %s, 'CONNECT'),
            has_database_privilege('dante_runtime', %s, 'TEMP'),
            has_database_privilege('dante_runtime', %s, 'CREATE'),
            has_database_privilege('dante_migrator', %s, 'CONNECT'),
            has_database_privilege('dante_migrator', %s, 'TEMP'),
            has_database_privilege('dante_migrator', %s, 'CREATE')
        """,
        (
            database_name,
            database_name,
            database_name,
            database_name,
            database_name,
            database_name,
        ),
    )
    database_row = await database_result.fetchone()
    if database_row is None or tuple(database_row) != (True, False, False, True, False, False):
        raise RuntimeError("DANTE database privileges failed P0 reconciliation")

    schema_result = await connection.execute(
        """
        SELECT
            has_schema_privilege('dante_runtime', 'dante', 'USAGE'),
            has_schema_privilege('dante_runtime', 'dante', 'CREATE'),
            has_schema_privilege('dante_runtime', 'public', 'USAGE'),
            has_schema_privilege('dante_runtime', 'public', 'CREATE'),
            has_schema_privilege('dante_migrator', 'dante', 'USAGE'),
            has_schema_privilege('dante_migrator', 'public', 'USAGE')
        """
    )
    schema_row = await schema_result.fetchone()
    if schema_row is None or tuple(schema_row) != (True, False, False, False, False, False):
        raise RuntimeError("DANTE schema privileges failed P0 reconciliation")

    owner_password_result = await connection.execute(
        "SELECT rolpassword FROM pg_authid WHERE rolname = 'dante_owner'"
    )
    owner_password = await owner_password_result.fetchone()
    if owner_password != (None,):
        raise RuntimeError("dante_owner must remain passwordless")


async def provision_database(settings: ProvisioningSettings) -> None:
    """Idempotently provision the exact CP6 P0 security envelope."""
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
        await _ensure_roles_and_schema(connection)
        await _reconcile_role_memberships(connection)
        await _configure_database_privileges(connection, settings.name)
        await _configure_credentials(connection, settings)
        await _configure_owner_defaults(connection)
        await _reconcile_technical_runtime_privileges(connection)
        await _verify_security_posture(connection, settings.name)
    finally:
        await connection.close()


async def _provision_from_environment() -> None:
    await provision_database(ProvisioningSettings())


def main() -> None:
    """Run explicit database provisioning from dedicated environment variables."""
    asyncio.run(_provision_from_environment())


if __name__ == "__main__":
    main()
