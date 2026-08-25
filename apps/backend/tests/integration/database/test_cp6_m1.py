"""Real PostgreSQL acceptance tests for CP6-M01 native identity + NativeAddress."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any
from uuid import uuid4, uuid7

import psycopg
import pytest
from alembic import command
from alembic.config import Config
from psycopg import errors

from dante.platform.database.metadata import Base
from dante.platform.database.mappings import MAPPED_TABLES

pytestmark = pytest.mark.postgres

_EXPECTED_REVISION = "20260825_01"
_EXPECTED_TABLES = {
    "person",
    "living_referent",
    "asset",
    "place",
    "content_artifact",
    "collective",
    "possibility",
    "goal",
    "plan",
    "activity",
    "event",
    "routine",
    "occurrence",
    "session",
    "observation",
    "native_address",
}
_EXPECTED_CHECKS = {
    "ck_person_uuidv7",
    "ck_living_referent_uuidv7",
    "ck_asset_uuidv7",
    "ck_place_uuidv7",
    "ck_content_artifact_uuidv7",
    "ck_collective_uuidv7",
    "ck_possibility_uuidv7",
    "ck_goal_uuidv7",
    "ck_plan_uuidv7",
    "ck_activity_uuidv7",
    "ck_event_uuidv7",
    "ck_routine_uuidv7",
    "ck_occurrence_uuidv7",
    "ck_session_uuidv7",
    "ck_observation_uuidv7",
    "ck_native_address_owner_family",
}
_REPO_ROOT = Path(__file__).resolve().parents[5]
_DICTIONARY_ROOT = _REPO_ROOT / "docs" / "database" / "dictionary"


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


def _upgrade_m1(database: Any, alembic_config: Config) -> Any:
    command.upgrade(alembic_config, _EXPECTED_REVISION)
    return database


def test_m1_materializes_exact_stage_topology(
    provisioned_database: Any,
    alembic_config: Config,
) -> None:
    database = _upgrade_m1(provisioned_database, alembic_config)
    with _admin_connection(database) as connection:
        business_tables = {
            str(row[0])
            for row in connection.execute(
                "SELECT tablename FROM pg_tables "
                "WHERE schemaname = 'dante' AND tablename <> 'alembic_version'"
            )
        }
        owners = {
            (str(row[0]), str(row[1]))
            for row in connection.execute(
                "SELECT tablename, tableowner FROM pg_tables "
                "WHERE schemaname = 'dante' AND tablename <> 'alembic_version'"
            )
        }
        constraints = {
            (str(row[0]), str(row[1]), str(row[2]))
            for row in connection.execute(
                """
                SELECT table_class.relname, constraint_catalog.contype,
                       constraint_catalog.conname
                FROM pg_constraint AS constraint_catalog
                JOIN pg_class AS table_class
                  ON table_class.oid = constraint_catalog.conrelid
                JOIN pg_namespace AS namespace
                  ON namespace.oid = table_class.relnamespace
                WHERE namespace.nspname = 'dante'
                  AND table_class.relname <> 'alembic_version'
                """
            )
        }
        indexes = {
            (str(row[0]), str(row[1]))
            for row in connection.execute(
                "SELECT tablename, indexname FROM pg_indexes "
                "WHERE schemaname = 'dante' AND tablename <> 'alembic_version'"
            )
        }
        views = {
            str(row[0])
            for row in connection.execute(
                "SELECT viewname FROM pg_views WHERE schemaname = 'dante'"
            )
        }
        routines = {
            str(row[0])
            for row in connection.execute(
                """
                SELECT procedure.proname
                FROM pg_proc AS procedure
                JOIN pg_namespace AS namespace
                  ON namespace.oid = procedure.pronamespace
                WHERE namespace.nspname = 'dante'
                """
            )
        }
        triggers = {
            str(row[0])
            for row in connection.execute(
                """
                SELECT trigger_catalog.tgname
                FROM pg_trigger AS trigger_catalog
                JOIN pg_class AS table_class
                  ON table_class.oid = trigger_catalog.tgrelid
                JOIN pg_namespace AS namespace
                  ON namespace.oid = table_class.relnamespace
                WHERE namespace.nspname = 'dante'
                  AND NOT trigger_catalog.tgisinternal
                """
            )
        }

    assert business_tables == _EXPECTED_TABLES
    assert owners == {(table_name, "dante_owner") for table_name in _EXPECTED_TABLES}

    primary_keys = {name for _, kind, name in constraints if kind == "p"}
    checks = {name for _, kind, name in constraints if kind == "c"}
    foreign_keys = {name for _, kind, name in constraints if kind == "f"}
    unique_constraints = {name for _, kind, name in constraints if kind == "u"}

    assert primary_keys == {f"pk_{table_name}" for table_name in _EXPECTED_TABLES}
    assert checks == _EXPECTED_CHECKS
    assert foreign_keys == set()
    assert unique_constraints == set()
    assert indexes == {
        (table_name, f"pk_{table_name}") for table_name in _EXPECTED_TABLES
    }
    assert views == set()
    assert routines == set()
    assert triggers == set()


def test_m1_constraints_enforce_uuidv7_and_owner_family(
    provisioned_database: Any,
    alembic_config: Config,
) -> None:
    database = _upgrade_m1(provisioned_database, alembic_config)
    with _role_connection(
        database,
        "dante_migrator",
        database.cluster.migrator_password,
    ) as connection:
        connection.execute("SET ROLE dante_owner")

        with pytest.raises(errors.CheckViolation):
            connection.execute(
                "INSERT INTO dante.person (person_ref) VALUES (%s)",
                (uuid4(),),
            )

        valid_ref = uuid7()
        connection.execute(
            "INSERT INTO dante.person (person_ref) VALUES (%s)",
            (valid_ref,),
        )
        connection.execute(
            "INSERT INTO dante.native_address (native_ref, owner_family) "
            "VALUES (%s, 'person')",
            (valid_ref,),
        )

        with pytest.raises(errors.CheckViolation):
            connection.execute(
                "INSERT INTO dante.native_address (native_ref, owner_family) "
                "VALUES (%s, 'entity')",
                (uuid7(),),
            )


def test_m1_runtime_business_dml_remains_denied(
    provisioned_database: Any,
    alembic_config: Config,
) -> None:
    database = _upgrade_m1(provisioned_database, alembic_config)
    statements = (
        "SELECT * FROM dante.person",
        "INSERT INTO dante.person (person_ref) VALUES (%s)",
        "UPDATE dante.person SET person_ref = %s",
        "DELETE FROM dante.person",
        "SELECT * FROM dante.native_address",
        "INSERT INTO dante.native_address (native_ref, owner_family) "
        "VALUES (%s, 'person')",
    )

    with _admin_connection(database) as connection:
        privilege_matrix = {
            table_name: tuple(
                connection.execute(
                    "SELECT "
                    "has_table_privilege('dante_runtime', %s, 'SELECT'), "
                    "has_table_privilege('dante_runtime', %s, 'INSERT'), "
                    "has_table_privilege('dante_runtime', %s, 'UPDATE'), "
                    "has_table_privilege('dante_runtime', %s, 'DELETE')",
                    (qualified_name, qualified_name, qualified_name, qualified_name),
                ).fetchone()
                or ()
            )
            for table_name in _EXPECTED_TABLES
            for qualified_name in (f"dante.{table_name}",)
        }

    assert privilege_matrix == {
        table_name: (False, False, False, False)
        for table_name in _EXPECTED_TABLES
    }

    with _role_connection(
        database,
        "dante_runtime",
        database.cluster.runtime_password,
    ) as connection:
        for statement in statements:
            parameters = (uuid7(),) if "%s" in statement else None
            with pytest.raises(errors.InsufficientPrivilege):
                connection.execute(statement, parameters)


def test_m1_fails_before_business_ddl_when_p0_defaults_are_broadened(
    provisioned_database: Any,
    alembic_config: Config,
) -> None:
    with _admin_connection(provisioned_database) as connection:
        connection.execute(
            "ALTER DEFAULT PRIVILEGES FOR ROLE dante_owner IN SCHEMA dante "
            "GRANT SELECT ON TABLES TO dante_runtime"
        )

    with pytest.raises(
        RuntimeError,
        match="CP6-M01 requires P0 provisioning/security hardening",
    ):
        command.upgrade(alembic_config, _EXPECTED_REVISION)

    with _admin_connection(provisioned_database) as connection:
        business_tables = {
            str(row[0])
            for row in connection.execute(
                "SELECT tablename FROM pg_tables "
                "WHERE schemaname = 'dante' AND tablename <> 'alembic_version'"
            )
        }
        version_table = connection.execute(
            "SELECT to_regclass('dante.alembic_version')"
        ).fetchone()
        if version_table == ("dante.alembic_version",):
            revision_row = connection.execute(
                "SELECT version_num FROM dante.alembic_version"
            ).fetchone()
        else:
            revision_row = None

    assert business_tables == set()
    assert revision_row != (_EXPECTED_REVISION,)


def test_m1_sqlalchemy_mapping_remains_registered_and_relationship_free() -> None:
    m1_tables = tuple(table for table in MAPPED_TABLES if table.name in _EXPECTED_TABLES)
    m1_mappers = tuple(
        mapper
        for mapper in Base.registry.mappers
        if mapper.local_table.name in _EXPECTED_TABLES
    )

    assert {table.name for table in m1_tables} == _EXPECTED_TABLES
    assert {mapper.local_table.name for mapper in m1_mappers} == _EXPECTED_TABLES
    assert len(m1_mappers) == 16
    assert all(len(mapper.relationships) == 0 for mapper in m1_mappers)


def test_m1_dictionary_entries_match_live_m1(
    provisioned_database: Any,
    alembic_config: Config,
) -> None:
    database = _upgrade_m1(provisioned_database, alembic_config)
    table_directory = _DICTIONARY_ROOT / "tables"
    entries = {
        table_name: json.loads(
            (table_directory / f"{table_name}.json").read_text(encoding="utf-8")
        )
        for table_name in _EXPECTED_TABLES
    }

    with _admin_connection(database) as connection:
        database_columns = {
            (str(row[0]), str(row[1]), str(row[2]), str(row[3]))
            for row in connection.execute(
                """
                SELECT table_name, column_name, data_type, is_nullable
                FROM information_schema.columns
                WHERE table_schema = 'dante'
                  AND table_name <> 'alembic_version'
                """
            )
        }

    dictionary_columns = {
        (
            table_name,
            str(column["name"]),
            str(column["postgres_type"]),
            "YES" if bool(column["nullable"]) else "NO",
        )
        for table_name, entry in entries.items()
        for column in entry["structure"]["columns"]
    }

    assert dictionary_columns == database_columns
    assert {
        str(entry["implementation"]["alembic_revision"])
        for entry in entries.values()
    } == {_EXPECTED_REVISION}
    assert {
        str(entry["implementation"]["introducing_stage"])
        for entry in entries.values()
    } == {"CP6-M01"}
    assert {
        str(check["name"])
        for entry in entries.values()
        for check in entry["structure"]["check_constraints"]
    } == _EXPECTED_CHECKS
    assert {
        (table_name, str(index["name"]))
        for table_name, entry in entries.items()
        for index in entry["structure"]["indexes"]
    } == {
        (table_name, f"pk_{table_name}") for table_name in _EXPECTED_TABLES
    }
