"""Real PostgreSQL acceptance tests for CP6 P0 role and privilege separation."""

import asyncio
from typing import Any

import psycopg
import pytest
from psycopg import errors
from pydantic import SecretStr

from dante.platform.database.provisioning import ProvisioningSettings, provision_database

pytestmark = pytest.mark.postgres

_TRUSTED_SEARCH_PATH = "pg_catalog,dante,pg_temp"


def _admin_connection(database: Any) -> psycopg.Connection[Any]:
    return psycopg.connect(
        host=database.cluster.host,
        port=database.cluster.port,
        dbname=database.name,
        user=database.cluster.admin_user,
        password=database.cluster.admin_password,
        autocommit=True,
    )


def _role_connection(database: Any, user: str, password: str) -> psycopg.Connection[Any]:
    return psycopg.connect(
        **database.connection_kwargs(user, password),
        autocommit=True,
    )


def _provisioning_settings(database: Any) -> ProvisioningSettings:
    return ProvisioningSettings(
        host=database.cluster.host,
        port=database.cluster.port,
        name=database.name,
        admin_user=database.cluster.admin_user,
        admin_password=SecretStr(database.cluster.admin_password),
        migrator_password=SecretStr(database.cluster.migrator_password),
        runtime_password=SecretStr(database.cluster.runtime_password),
        connect_timeout_seconds=2,
    )


def _create_privilege_probe(database: Any) -> None:
    with _role_connection(
        database,
        "dante_migrator",
        database.cluster.migrator_password,
    ) as connection:
        connection.execute("SET ROLE dante_owner")
        connection.execute("CREATE TYPE dante.cp3_probe_kind AS ENUM ('alpha', 'beta')")
        connection.execute(
            "CREATE TABLE dante.cp3_privilege_probe ("
            "id BIGSERIAL PRIMARY KEY, "
            "kind dante.cp3_probe_kind NOT NULL, "
            "value TEXT NOT NULL"
            ")"
        )
        connection.execute(
            "CREATE FUNCTION dante.cp3_probe_function() RETURNS integer "
            "LANGUAGE sql IMMUTABLE AS 'SELECT 1'"
        )


def _assert_runtime_denied(database: Any, statement: str) -> None:
    with (
        _role_connection(
            database,
            "dante_runtime",
            database.cluster.runtime_password,
        ) as connection,
        pytest.raises(errors.InsufficientPrivilege),
    ):
        connection.execute(statement)


def _dante_memberships(connection: psycopg.Connection[Any]) -> set[tuple[Any, ...]]:
    return {
        tuple(row)
        for row in connection.execute(
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
    }


def test_owner_migrator_and_runtime_roles_have_exact_security_posture(
    migrated_database: Any,
) -> None:
    with _admin_connection(migrated_database) as connection:
        rows = connection.execute(
            "SELECT rolname, rolcanlogin, rolinherit, rolsuper, rolcreatedb, "
            "rolcreaterole, rolreplication, rolbypassrls "
            "FROM pg_roles "
            "WHERE rolname IN ('dante_owner', 'dante_migrator', 'dante_runtime')"
        ).fetchall()
        roles = {str(row[0]): row[1:] for row in rows}
        memberships = _dante_memberships(connection)
        password_rows = connection.execute(
            "SELECT rolname, rolpassword FROM pg_authid "
            "WHERE rolname IN ('dante_owner', 'dante_migrator', 'dante_runtime')"
        ).fetchall()
        passwords = {str(row[0]): row[1] for row in password_rows}

    assert roles["dante_owner"] == (False, True, False, False, False, False, False)
    assert roles["dante_migrator"] == (True, False, False, False, False, False, False)
    assert roles["dante_runtime"] == (True, False, False, False, False, False, False)
    assert memberships == {
        ("dante_owner", "dante_migrator", False, False, True),
    }
    assert passwords["dante_owner"] is None
    assert str(passwords["dante_migrator"]).startswith("SCRAM-SHA-256$")
    assert str(passwords["dante_runtime"]).startswith("SCRAM-SHA-256$")


def test_migrator_requires_exact_identity_and_explicit_set_role(
    migrated_database: Any,
) -> None:
    with _role_connection(
        migrated_database,
        "dante_migrator",
        migrated_database.cluster.migrator_password,
    ) as connection:
        before = connection.execute(
            "SELECT session_user, current_user, current_setting('search_path')"
        ).fetchone()
        assert before is not None
        assert before[0:2] == ("dante_migrator", "dante_migrator")
        assert str(before[2]).replace(" ", "") == _TRUSTED_SEARCH_PATH

        with pytest.raises(errors.InsufficientPrivilege):
            connection.execute("CREATE TABLE dante.cp3_without_owner_role (id integer)")

        connection.execute("SET ROLE dante_owner")
        after = connection.execute(
            "SELECT session_user, current_user, current_setting('search_path')"
        ).fetchone()
        assert after is not None
        assert after[0:2] == ("dante_migrator", "dante_owner")
        assert str(after[2]).replace(" ", "") == _TRUSTED_SEARCH_PATH
        connection.execute("CREATE TABLE dante.cp3_owner_probe (id integer PRIMARY KEY)")

    with _admin_connection(migrated_database) as connection:
        owner = connection.execute(
            "SELECT tableowner FROM pg_tables "
            "WHERE schemaname = 'dante' AND tablename = 'cp3_owner_probe'"
        ).fetchone()

    assert owner == ("dante_owner",)


def test_new_owner_objects_are_deny_by_default_for_runtime(migrated_database: Any) -> None:
    _create_privilege_probe(migrated_database)

    with _admin_connection(migrated_database) as connection:
        effective_public_defaults = connection.execute(
            "SELECT "
            "has_function_privilege("
            "'dante_runtime', 'dante.cp3_probe_function()', 'EXECUTE'"
            "), "
            "has_type_privilege("
            "'dante_runtime', 'dante.cp3_probe_kind', 'USAGE'"
            ")"
        ).fetchone()

    assert effective_public_defaults == (False, False)

    denied_statements = (
        "SELECT * FROM dante.cp3_privilege_probe",
        "INSERT INTO dante.cp3_privilege_probe (kind, value) VALUES ('alpha', 'created')",
        "UPDATE dante.cp3_privilege_probe SET value = 'updated'",
        "DELETE FROM dante.cp3_privilege_probe",
        "SELECT nextval('dante.cp3_privilege_probe_id_seq')",
        "SELECT dante.cp3_probe_function()",
    )
    for statement in denied_statements:
        _assert_runtime_denied(migrated_database, statement)


def test_runtime_cannot_escalate_or_modify_schema_or_migration_history(
    migrated_database: Any,
) -> None:
    _create_privilege_probe(migrated_database)

    denied_statements = (
        "CREATE TABLE dante.cp3_runtime_create_forbidden (id integer)",
        "CREATE TABLE public.cp3_runtime_public_forbidden (id integer)",
        "ALTER TABLE dante.cp3_privilege_probe ADD COLUMN forbidden integer",
        "DROP TABLE dante.cp3_privilege_probe",
        "TRUNCATE dante.cp3_privilege_probe",
        "CREATE TEMP TABLE cp3_runtime_temp_forbidden (id integer)",
        "SET ROLE dante_owner",
        "SET ROLE dante_migrator",
        "SELECT * FROM dante.alembic_version",
    )

    for statement in denied_statements:
        _assert_runtime_denied(migrated_database, statement)


def test_database_schema_and_search_path_are_explicitly_hardened(
    migrated_database: Any,
) -> None:
    with _admin_connection(migrated_database) as connection:
        database_privileges = connection.execute(
            "SELECT "
            "has_database_privilege('dante_runtime', %s, 'CONNECT'), "
            "has_database_privilege('dante_runtime', %s, 'TEMP'), "
            "has_database_privilege('dante_runtime', %s, 'CREATE'), "
            "has_database_privilege('dante_migrator', %s, 'CONNECT'), "
            "has_database_privilege('dante_migrator', %s, 'TEMP'), "
            "has_database_privilege('dante_migrator', %s, 'CREATE')",
            (
                migrated_database.name,
                migrated_database.name,
                migrated_database.name,
                migrated_database.name,
                migrated_database.name,
                migrated_database.name,
            ),
        ).fetchone()
        schema_privileges = connection.execute(
            "SELECT "
            "has_schema_privilege('dante_runtime', 'dante', 'USAGE'), "
            "has_schema_privilege('dante_runtime', 'dante', 'CREATE'), "
            "has_schema_privilege('dante_runtime', 'public', 'USAGE'), "
            "has_schema_privilege('dante_runtime', 'public', 'CREATE'), "
            "has_schema_privilege('dante_migrator', 'dante', 'USAGE'), "
            "has_schema_privilege('dante_migrator', 'public', 'USAGE')"
        ).fetchone()
        public_database_privileges = {
            str(row[0])
            for row in connection.execute(
                "SELECT privilege_type "
                "FROM aclexplode((SELECT datacl FROM pg_database WHERE datname = %s)) "
                "WHERE grantee = 0",
                (migrated_database.name,),
            )
        }

    assert database_privileges == (True, False, False, True, False, False)
    assert schema_privileges == (True, False, False, False, False, False)
    assert "CONNECT" not in public_database_privileges
    assert "TEMPORARY" not in public_database_privileges
    assert "CREATE" not in public_database_privileges


def test_provisioning_reconciles_unexpected_dante_membership_edges(
    migrated_database: Any,
) -> None:
    with _admin_connection(migrated_database) as connection:
        connection.execute(
            "GRANT dante_migrator TO dante_runtime WITH INHERIT FALSE, SET TRUE, ADMIN FALSE"
        )
        assert len(_dante_memberships(connection)) == 2

    asyncio.run(provision_database(_provisioning_settings(migrated_database)))

    with _admin_connection(migrated_database) as connection:
        assert _dante_memberships(connection) == {
            ("dante_owner", "dante_migrator", False, False, True),
        }


def test_provisioning_fails_closed_on_external_role_membership_edges(
    migrated_database: Any,
) -> None:
    with _admin_connection(migrated_database) as connection:
        connection.execute("CREATE ROLE cp6_p0_external_granted NOLOGIN")
        connection.execute("CREATE ROLE cp6_p0_external_member NOLOGIN")
        connection.execute(
            "GRANT cp6_p0_external_granted TO dante_runtime "
            "WITH INHERIT FALSE, SET TRUE, ADMIN FALSE"
        )
        connection.execute(
            "GRANT dante_runtime TO cp6_p0_external_member "
            "WITH INHERIT FALSE, SET TRUE, ADMIN FALSE"
        )

    try:
        with pytest.raises(RuntimeError, match="external-role edges"):
            asyncio.run(provision_database(_provisioning_settings(migrated_database)))

        with _admin_connection(migrated_database) as connection:
            membership_names = {
                (str(row[0]), str(row[1])) for row in _dante_memberships(connection)
            }

        assert ("cp6_p0_external_granted", "dante_runtime") in membership_names
        assert ("dante_runtime", "cp6_p0_external_member") in membership_names
    finally:
        with _admin_connection(migrated_database) as connection:
            connection.execute("REVOKE cp6_p0_external_granted FROM dante_runtime")
            connection.execute("REVOKE dante_runtime FROM cp6_p0_external_member")
            connection.execute("DROP ROLE cp6_p0_external_granted")
            connection.execute("DROP ROLE cp6_p0_external_member")


def test_provisioning_rerun_does_not_broaden_migration_owned_object_acl(
    migrated_database: Any,
) -> None:
    with _role_connection(
        migrated_database,
        "dante_migrator",
        migrated_database.cluster.migrator_password,
    ) as connection:
        connection.execute("SET ROLE dante_owner")
        connection.execute("CREATE TABLE dante.cp6_p0_acl_probe (id bigint PRIMARY KEY)")
        connection.execute("GRANT SELECT ON TABLE dante.cp6_p0_acl_probe TO dante_runtime")

    asyncio.run(provision_database(_provisioning_settings(migrated_database)))

    with _admin_connection(migrated_database) as connection:
        privileges = {
            str(row[0])
            for row in connection.execute(
                "SELECT privilege_type "
                "FROM information_schema.role_table_grants "
                "WHERE grantee = 'dante_runtime' "
                "AND table_schema = 'dante' "
                "AND table_name = 'cp6_p0_acl_probe'"
            )
        }

    assert privileges == {"SELECT"}
