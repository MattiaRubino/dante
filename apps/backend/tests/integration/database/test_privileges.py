"""Real PostgreSQL acceptance tests for CP3 role and privilege separation."""

from typing import Any

import psycopg
import pytest
from psycopg import errors

pytestmark = pytest.mark.postgres


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
    with _role_connection(
        database,
        "dante_runtime",
        database.cluster.runtime_password,
    ) as connection:
        with pytest.raises(errors.InsufficientPrivilege):
            connection.execute(statement)


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

        membership = connection.execute(
            "SELECT m.admin_option, m.inherit_option, m.set_option "
            "FROM pg_auth_members AS m "
            "JOIN pg_roles AS role ON role.oid = m.roleid "
            "JOIN pg_roles AS member ON member.oid = m.member "
            "WHERE role.rolname = 'dante_owner' AND member.rolname = 'dante_migrator'"
        ).fetchone()

    assert roles["dante_owner"] == (False, True, False, False, False, False, False)
    assert roles["dante_migrator"] == (True, False, False, False, False, False, False)
    assert roles["dante_runtime"] == (True, False, False, False, False, False, False)
    assert membership == (False, False, True)


def test_migrator_requires_explicit_set_role_and_creates_owner_owned_objects(
    migrated_database: Any,
) -> None:
    with _role_connection(
        migrated_database,
        "dante_migrator",
        migrated_database.cluster.migrator_password,
    ) as connection:
        before = connection.execute("SELECT current_user").fetchone()
        assert before == ("dante_migrator",)

        with pytest.raises(errors.InsufficientPrivilege):
            connection.execute("CREATE TABLE dante.cp3_without_owner_role (id integer)")

        connection.execute("SET ROLE dante_owner")
        after = connection.execute("SELECT current_user").fetchone()
        assert after == ("dante_owner",)
        connection.execute("CREATE TABLE dante.cp3_owner_probe (id integer PRIMARY KEY)")

    with _admin_connection(migrated_database) as connection:
        owner = connection.execute(
            "SELECT tableowner FROM pg_tables "
            "WHERE schemaname = 'dante' AND tablename = 'cp3_owner_probe'"
        ).fetchone()

    assert owner == ("dante_owner",)


def test_runtime_receives_only_expected_default_object_privileges(
    migrated_database: Any,
) -> None:
    _create_privilege_probe(migrated_database)

    with _role_connection(
        migrated_database,
        "dante_runtime",
        migrated_database.cluster.runtime_password,
    ) as connection:
        inserted = connection.execute(
            "INSERT INTO dante.cp3_privilege_probe (kind, value) "
            "VALUES ('alpha', 'created') RETURNING id"
        ).fetchone()
        assert inserted is not None
        row_id = int(inserted[0])

        selected = connection.execute(
            "SELECT kind::text, value FROM dante.cp3_privilege_probe WHERE id = %s",
            (row_id,),
        ).fetchone()
        assert selected == ("alpha", "created")

        connection.execute(
            "UPDATE dante.cp3_privilege_probe SET value = 'updated' WHERE id = %s",
            (row_id,),
        )
        connection.execute(
            "DELETE FROM dante.cp3_privilege_probe WHERE id = %s",
            (row_id,),
        )

        with pytest.raises(errors.InsufficientPrivilege):
            connection.execute("SELECT dante.cp3_probe_function()")


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
        "SELECT * FROM dante.alembic_version",
    )

    for statement in denied_statements:
        _assert_runtime_denied(migrated_database, statement)


def test_database_and_schema_grants_are_explicitly_hardened(migrated_database: Any) -> None:
    with _admin_connection(migrated_database) as connection:
        runtime_database = connection.execute(
            "SELECT "
            "has_database_privilege('dante_runtime', %s, 'CONNECT'), "
            "has_database_privilege('dante_runtime', %s, 'TEMP'), "
            "has_schema_privilege('dante_runtime', 'dante', 'USAGE'), "
            "has_schema_privilege('dante_runtime', 'dante', 'CREATE')",
            (migrated_database.name, migrated_database.name),
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

    assert runtime_database == (True, False, True, False)
    assert "CONNECT" not in public_database_privileges
    assert "TEMPORARY" not in public_database_privileges
