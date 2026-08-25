"""Real PostgreSQL acceptance tests for CP6-M02 scoped/material-state controls."""

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

_M1_REVISION = "20260825_01"
_M2_REVISION = "20260825_02"
_M1_TABLES = {
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
_M2_TABLES = {
    "scoped_address",
    "schedule",
    "actual",
    "material_state_address",
    "native_current_material_state",
    "scoped_current_material_state",
}
_CUMULATIVE_TABLES = _M1_TABLES | _M2_TABLES
_M2_CHECKS = {
    "ck_scoped_address_scoped_family",
    "ck_schedule_uuidv7",
    "ck_actual_uuidv7",
    "ck_material_state_address_uuidv7",
    "ck_material_state_address_one_owner",
    "ck_material_state_address_facet_code",
    "ck_native_current_material_state_facet_code",
    "ck_scoped_current_material_state_facet_code",
}
_M2_FOREIGN_KEYS = {
    "fk_schedule_subject_native_ref_native_address",
    "fk_actual_subject_native_ref_native_address",
    "fk_material_state_address_native_owner_ref_native_address",
    "fk_material_state_address_scoped_owner_ref_scoped_address",
    "fk_native_current_material_state_owner_address",
    "fk_native_current_material_state_state_address",
    "fk_scoped_current_material_state_owner_address",
    "fk_scoped_current_material_state_state_address",
}
_M2_UNIQUES = {
    "uq_native_current_material_state_material_state_ref",
    "uq_scoped_current_material_state_material_state_ref",
}
_M2_EXPLICIT_INDEXES = {
    ("schedule", "ix_schedule_subject_native_ref"),
    ("actual", "ix_actual_subject_native_ref"),
    (
        "material_state_address",
        "ix_material_state_address_native_owner_ref_facet_code",
    ),
    (
        "material_state_address",
        "ix_material_state_address_scoped_owner_ref_facet_code",
    ),
}
_M2_DECLARED_CONSTRAINT_KINDS = {"p", "c", "f", "u"}
_M2_DECLARED_CONSTRAINT_COUNT = 24
_M2_NOT_NULL_CONSTRAINT_COUNT = 14

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


def _owner_connection(database: Any) -> psycopg.Connection[Any]:
    connection = psycopg.connect(
        **database.connection_kwargs(
            "dante_migrator",
            database.cluster.migrator_password,
        ),
        autocommit=True,
    )
    connection.execute("SET ROLE dante_owner")
    return connection


def _upgrade_m2(database: Any, alembic_config: Config) -> Any:
    command.upgrade(alembic_config, _M2_REVISION)
    return database


def test_m2_materializes_exact_cumulative_topology(
    provisioned_database: Any,
    alembic_config: Config,
) -> None:
    database = _upgrade_m2(provisioned_database, alembic_config)
    with _admin_connection(database) as connection:
        tables = {
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
            (
                str(row[0]),
                str(row[1]),
                str(row[2]),
                bool(row[3]),
                bool(row[4]),
                bool(row[5]),
                bool(row[6]),
            )
            for row in connection.execute(
                """
                SELECT table_class.relname,
                       constraint_catalog.contype,
                       constraint_catalog.conname,
                       constraint_catalog.condeferrable,
                       constraint_catalog.condeferred,
                       constraint_catalog.convalidated,
                       constraint_catalog.conenforced
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

    assert tables == _CUMULATIVE_TABLES
    assert owners == {(table_name, "dante_owner") for table_name in _CUMULATIVE_TABLES}

    primary_keys = {name for _, kind, name, *_ in constraints if kind == "p"}
    checks = {name for _, kind, name, *_ in constraints if kind == "c"}
    foreign_keys = {name for _, kind, name, *_ in constraints if kind == "f"}
    uniques = {name for _, kind, name, *_ in constraints if kind == "u"}

    assert len(primary_keys) == 22
    assert len(checks) == 24
    assert foreign_keys == _M2_FOREIGN_KEYS
    assert uniques == _M2_UNIQUES
    assert len(indexes) == 28
    assert _M2_EXPLICIT_INDEXES <= indexes
    assert views == set()
    assert routines == set()
    assert triggers == set()

    m2_constraints = [row for row in constraints if row[0] in _M2_TABLES]
    m2_declared_constraints = [
        row for row in m2_constraints if row[1] in _M2_DECLARED_CONSTRAINT_KINDS
    ]
    m2_not_null_constraints = [row for row in m2_constraints if row[1] == "n"]

    assert len(m2_declared_constraints) == _M2_DECLARED_CONSTRAINT_COUNT
    assert len(m2_not_null_constraints) == _M2_NOT_NULL_CONSTRAINT_COUNT
    assert len(m2_constraints) == (
        _M2_DECLARED_CONSTRAINT_COUNT + _M2_NOT_NULL_CONSTRAINT_COUNT
    )
    assert {kind for _, kind, *_ in m2_constraints} == {
        *_M2_DECLARED_CONSTRAINT_KINDS,
        "n",
    }
    assert all(
        not deferrable and not deferred and validated and enforced
        for _, _, _, deferrable, deferred, validated, enforced in m2_constraints
    )


def test_m2_constraints_and_foreign_keys_are_live(
    provisioned_database: Any,
    alembic_config: Config,
) -> None:
    database = _upgrade_m2(provisioned_database, alembic_config)
    with _owner_connection(database) as connection:
        activity_ref = uuid7()
        connection.execute(
            "INSERT INTO dante.activity (activity_ref) VALUES (%s)",
            (activity_ref,),
        )
        connection.execute(
            "INSERT INTO dante.native_address (native_ref, owner_family) "
            "VALUES (%s, 'activity')",
            (activity_ref,),
        )

        with pytest.raises(errors.CheckViolation):
            connection.execute(
                "INSERT INTO dante.schedule (schedule_ref, subject_native_ref) "
                "VALUES (%s, %s)",
                (uuid4(), activity_ref),
            )

        schedule_ref = uuid7()
        actual_ref = uuid7()
        connection.execute(
            "INSERT INTO dante.schedule (schedule_ref, subject_native_ref) "
            "VALUES (%s, %s)",
            (schedule_ref, activity_ref),
        )
        connection.execute(
            "INSERT INTO dante.actual (actual_ref, subject_native_ref) "
            "VALUES (%s, %s)",
            (actual_ref, activity_ref),
        )

        with pytest.raises(errors.ForeignKeyViolation):
            connection.execute(
                "INSERT INTO dante.actual (actual_ref, subject_native_ref) "
                "VALUES (%s, %s)",
                (uuid7(), uuid7()),
            )

        with pytest.raises(errors.CheckViolation):
            connection.execute(
                "INSERT INTO dante.scoped_address (scoped_ref, scoped_family) "
                "VALUES (%s, 'recurrence')",
                (uuid7(),),
            )

        connection.execute(
            "INSERT INTO dante.scoped_address (scoped_ref, scoped_family) "
            "VALUES (%s, 'schedule')",
            (schedule_ref,),
        )

        with pytest.raises(errors.CheckViolation):
            connection.execute(
                "INSERT INTO dante.material_state_address "
                "(material_state_ref, native_owner_ref, scoped_owner_ref, facet_code) "
                "VALUES (%s, %s, %s, 'schedule.placement')",
                (uuid7(), activity_ref, schedule_ref),
            )

        with pytest.raises(errors.CheckViolation):
            connection.execute(
                "INSERT INTO dante.material_state_address "
                "(material_state_ref, scoped_owner_ref, facet_code) "
                "VALUES (%s, %s, 'unknown.facet')",
                (uuid7(), schedule_ref),
            )

        with pytest.raises(errors.CheckViolation):
            connection.execute(
                "INSERT INTO dante.material_state_address "
                "(material_state_ref, scoped_owner_ref, facet_code) "
                "VALUES (%s, %s, 'schedule.placement')",
                (uuid4(), schedule_ref),
            )

        material_state_ref = uuid7()
        connection.execute(
            "INSERT INTO dante.material_state_address "
            "(material_state_ref, scoped_owner_ref, facet_code) "
            "VALUES (%s, %s, 'schedule.placement')",
            (material_state_ref, schedule_ref),
        )
        connection.execute(
            "INSERT INTO dante.scoped_current_material_state "
            "(scoped_owner_ref, facet_code, material_state_ref) "
            "VALUES (%s, 'schedule.placement', %s)",
            (schedule_ref, material_state_ref),
        )

        second_material_state_ref = uuid7()
        connection.execute(
            "INSERT INTO dante.material_state_address "
            "(material_state_ref, scoped_owner_ref, facet_code) "
            "VALUES (%s, %s, 'schedule.placement')",
            (second_material_state_ref, schedule_ref),
        )

        with pytest.raises(errors.CheckViolation):
            connection.execute(
                "INSERT INTO dante.scoped_current_material_state "
                "(scoped_owner_ref, facet_code, material_state_ref) "
                "VALUES (%s, 'session.timing', %s)",
                (schedule_ref, second_material_state_ref),
            )


def test_m2_runtime_business_dml_remains_denied(
    provisioned_database: Any,
    alembic_config: Config,
) -> None:
    database = _upgrade_m2(provisioned_database, alembic_config)
    with _admin_connection(database) as connection:
        privileges = {
            table_name: tuple(
                connection.execute(
                    "SELECT "
                    "has_table_privilege('dante_runtime', %s, 'SELECT'), "
                    "has_table_privilege('dante_runtime', %s, 'INSERT'), "
                    "has_table_privilege('dante_runtime', %s, 'UPDATE'), "
                    "has_table_privilege('dante_runtime', %s, 'DELETE')",
                    (qualified, qualified, qualified, qualified),
                ).fetchone()
                or ()
            )
            for table_name in _M2_TABLES
            for qualified in (f"dante.{table_name}",)
        }

    assert privileges == {
        table_name: (False, False, False, False)
        for table_name in _M2_TABLES
    }


def test_m2_upgrade_and_downgrade_preserve_m1_boundary(
    provisioned_database: Any,
    alembic_config: Config,
) -> None:
    command.upgrade(alembic_config, _M1_REVISION)
    with _admin_connection(provisioned_database) as connection:
        at_m1 = {
            str(row[0])
            for row in connection.execute(
                "SELECT tablename FROM pg_tables "
                "WHERE schemaname = 'dante' AND tablename <> 'alembic_version'"
            )
        }
    assert at_m1 == _M1_TABLES

    command.upgrade(alembic_config, _M2_REVISION)
    with _admin_connection(provisioned_database) as connection:
        at_m2 = {
            str(row[0])
            for row in connection.execute(
                "SELECT tablename FROM pg_tables "
                "WHERE schemaname = 'dante' AND tablename <> 'alembic_version'"
            )
        }
    assert at_m2 == _CUMULATIVE_TABLES

    command.downgrade(alembic_config, _M1_REVISION)
    with _admin_connection(provisioned_database) as connection:
        after_downgrade = {
            str(row[0])
            for row in connection.execute(
                "SELECT tablename FROM pg_tables "
                "WHERE schemaname = 'dante' AND tablename <> 'alembic_version'"
            )
        }
    assert after_downgrade == _M1_TABLES


def test_m2_sqlalchemy_mapping_is_exact_and_relationship_free() -> None:
    mapped_names = {table.name for table in MAPPED_TABLES}

    assert mapped_names == _CUMULATIVE_TABLES
    assert set(Base.metadata.tables) == {
        f"dante.{table_name}" for table_name in _CUMULATIVE_TABLES
    }
    assert len(tuple(Base.registry.mappers)) == 22
    assert all(len(mapper.relationships) == 0 for mapper in Base.registry.mappers)


def test_m2_dictionary_matches_live_stage_and_current_scope(
    provisioned_database: Any,
    alembic_config: Config,
) -> None:
    database = _upgrade_m2(provisioned_database, alembic_config)
    table_directory = _DICTIONARY_ROOT / "tables"
    entries = {
        path.stem: json.loads(path.read_text(encoding="utf-8"))
        for path in table_directory.glob("*.json")
    }
    scope = json.loads(
        (_DICTIONARY_ROOT / "scope.json").read_text(encoding="utf-8")
    )

    assert set(entries) == _CUMULATIVE_TABLES
    assert scope["status"] == "materializing"
    assert scope["current_materialization"] == {
        "completed_stages": ["CP6-M01", "CP6-M02"],
        "standalone_entries": {
            "tables": 22,
            "views": 0,
            "routines": 0,
            "total": 22,
        },
        "embedded_objects": {
            "triggers": 0,
            "physical_indexes": 28,
        },
        "constraints": {
            "foreign_keys": 8,
            "check_constraints": 24,
        },
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
    m2_entries = {name: entries[name] for name in _M2_TABLES}
    assert {
        str(entry["implementation"]["alembic_revision"])
        for entry in m2_entries.values()
    } == {_M2_REVISION}
    assert {
        str(entry["implementation"]["introducing_stage"])
        for entry in m2_entries.values()
    } == {"CP6-M02"}
    assert {
        str(check["name"])
        for entry in m2_entries.values()
        for check in entry["structure"]["check_constraints"]
    } == _M2_CHECKS
    assert {
        str(foreign_key["name"])
        for entry in m2_entries.values()
        for foreign_key in entry["structure"]["foreign_keys"]
    } == _M2_FOREIGN_KEYS
