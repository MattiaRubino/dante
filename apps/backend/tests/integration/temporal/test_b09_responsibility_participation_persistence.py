"""B09-A PostgreSQL proof for direct Responsibility and expected Participation relations."""

from __future__ import annotations

from typing import Any
from uuid import uuid7

import psycopg
import pytest
from psycopg import errors

pytestmark = pytest.mark.postgres
pytest_plugins = ("tests.integration.temporal.test_b01_activity_core",)

_TABLES = (
    "event_expected_participation",
    "activity_responsibility",
    "event_responsibility",
)


def _owner(database: Any) -> psycopg.Connection[Any]:
    connection = psycopg.connect(
        **database.connection_kwargs(
            "dante_migrator",
            database.cluster.migrator_password,
        ),
        autocommit=True,
    )
    connection.execute("SET ROLE dante_owner")
    return connection


def _admin(database: Any) -> psycopg.Connection[Any]:
    return psycopg.connect(
        host=database.cluster.host,
        port=database.cluster.port,
        dbname=database.name,
        user=database.cluster.admin_user,
        password=database.cluster.admin_password,
        autocommit=True,
    )


def _native(connection: psycopg.Connection[Any], table: str, ref: object) -> None:
    ref_column = f"{table}_ref"
    connection.execute(f"INSERT INTO dante.{table} ({ref_column}) VALUES (%s)", (ref,))
    connection.execute(
        "INSERT INTO dante.native_address (native_ref, owner_family) VALUES (%s, %s)",
        (ref, table),
    )


def test_b09_a_relations_keep_person_roles_typed_and_distinct(migrated_database: Any) -> None:
    event_ref = uuid7()
    activity_ref = uuid7()
    required_person = uuid7()
    optional_person = uuid7()

    with _owner(migrated_database) as connection:
        _native(connection, "event", event_ref)
        _native(connection, "activity", activity_ref)
        _native(connection, "person", required_person)
        _native(connection, "person", optional_person)

        assert connection.execute(
            "SELECT count(*) FROM dante.account_application_context "
            "WHERE self_person_ref IN (%s,%s)",
            (required_person, optional_person),
        ).fetchone() == (0,)

        connection.execute(
            "INSERT INTO dante.event_expected_participation "
            "(event_ref,participant_person_ref,requirement_code,established_at) "
            "VALUES (%s,%s,'required',statement_timestamp()),"
            "(%s,%s,'optional',statement_timestamp())",
            (event_ref, required_person, event_ref, optional_person),
        )
        connection.execute(
            "INSERT INTO dante.activity_responsibility "
            "(activity_ref,responsible_person_ref,established_at) "
            "VALUES (%s,%s,statement_timestamp())",
            (activity_ref, required_person),
        )
        connection.execute(
            "INSERT INTO dante.event_responsibility "
            "(event_ref,responsible_person_ref,established_at) "
            "VALUES (%s,%s,statement_timestamp())",
            (event_ref, optional_person),
        )

        assert connection.execute(
            "SELECT participant_person_ref,requirement_code "
            "FROM dante.event_expected_participation WHERE event_ref=%s "
            "ORDER BY requirement_code",
            (event_ref,),
        ).fetchall() == [(optional_person, "optional"), (required_person, "required")]
        assert connection.execute(
            "SELECT responsible_person_ref FROM dante.activity_responsibility WHERE activity_ref=%s",
            (activity_ref,),
        ).fetchone() == (required_person,)
        assert connection.execute(
            "SELECT responsible_person_ref FROM dante.event_responsibility WHERE event_ref=%s",
            (event_ref,),
        ).fetchone() == (optional_person,)

        with pytest.raises(errors.CheckViolation):
            connection.execute(
                "INSERT INTO dante.event_expected_participation "
                "(event_ref,participant_person_ref,requirement_code,established_at) "
                "VALUES (%s,%s,'accepted',statement_timestamp())",
                (event_ref, uuid7()),
            )

        with pytest.raises(errors.UniqueViolation):
            connection.execute(
                "INSERT INTO dante.activity_responsibility "
                "(activity_ref,responsible_person_ref,established_at) "
                "VALUES (%s,%s,statement_timestamp())",
                (activity_ref, optional_person),
            )


def test_b09_a_relation_tables_are_not_raw_runtime_mutation_surfaces(
    migrated_database: Any,
) -> None:
    with _admin(migrated_database) as connection:
        for table in _TABLES:
            qualified = f"dante.{table}"
            assert connection.execute(
                "SELECT "
                "has_table_privilege('dante_runtime', %s, 'SELECT'),"
                "has_table_privilege('dante_runtime', %s, 'INSERT'),"
                "has_table_privilege('dante_runtime', %s, 'UPDATE'),"
                "has_table_privilege('dante_runtime', %s, 'DELETE')",
                (qualified, qualified, qualified, qualified),
            ).fetchone() == (False, False, False, False)
