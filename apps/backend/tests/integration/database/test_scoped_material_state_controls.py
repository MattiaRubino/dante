"""Real PostgreSQL acceptance tests for CP6-M02 scoped/material-state controls."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, cast
from uuid import uuid4, uuid7

import psycopg
import pytest
from alembic import command
from alembic.config import Config
from psycopg import errors
from sqlalchemy import Table

from dante.platform.database.mappings import MAPPED_TABLES
from dante.platform.database.metadata import Base

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
    ("material_state_address", "ix_material_state_address_native_owner_ref_facet_code"),
    ("material_state_address", "ix_material_state_address_scoped_owner_ref_facet_code"),
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
        **database.connection_kwargs("dante_migrator", database.cluster.migrator_password),
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
                "WHERE schemaname='dante' AND tablename<>'alembic_version'"
            )
        }
        owners = {
            (str(row[0]), str(row[1]))
            for row in connection.execute(
                "SELECT tablename, tableowner FROM pg_tables "
                "WHERE schemaname='dante' AND tablename<>'alembic_version'"
            )
        }
        constraints = {
            tuple(row)
            for row in connection.execute(
                """
                SELECT c.relname, con.contype, con.conname, con.condeferrable,
                       con.condeferred, con.convalidated, con.conenforced
                FROM pg_constraint con
                JOIN pg_class c ON c.oid=con.conrelid
                JOIN pg_namespace n ON n.oid=c.relnamespace
                WHERE n.nspname='dante' AND c.relname<>'alembic_version'
                """
            )
        }
        indexes = {
            (str(row[0]), str(row[1]))
            for row in connection.execute(
                "SELECT tablename,indexname FROM pg_indexes "
                "WHERE schemaname='dante' AND tablename<>'alembic_version'"
            )
        }
        views = {
            str(row[0])
            for row in connection.execute("SELECT viewname FROM pg_views WHERE schemaname='dante'")
        }
        routines = {
            str(row[0])
            for row in connection.execute(
                "SELECT p.proname FROM pg_proc p JOIN pg_namespace n "
                "ON n.oid=p.pronamespace WHERE n.nspname='dante'"
            )
        }
        triggers = {
            str(row[0])
            for row in connection.execute(
                "SELECT t.tgname FROM pg_trigger t JOIN pg_class c ON c.oid=t.tgrelid "
                "JOIN pg_namespace n ON n.oid=c.relnamespace "
                "WHERE n.nspname='dante' AND NOT t.tgisinternal"
            )
        }

    assert tables == _CUMULATIVE_TABLES
    assert owners == {(name, "dante_owner") for name in _CUMULATIVE_TABLES}
    assert len({r[2] for r in constraints if r[1] == "p"}) == 22
    assert len({r[2] for r in constraints if r[1] == "c"}) == 24
    assert {r[2] for r in constraints if r[1] == "f"} == _M2_FOREIGN_KEYS
    assert {r[2] for r in constraints if r[1] == "u"} == _M2_UNIQUES
    assert len(indexes) == 28
    assert indexes >= _M2_EXPLICIT_INDEXES
    assert views == routines == triggers == set()

    m2_constraints = [r for r in constraints if r[0] in _M2_TABLES]
    declared = [r for r in m2_constraints if r[1] in _M2_DECLARED_CONSTRAINT_KINDS]
    not_null = [r for r in m2_constraints if r[1] == "n"]
    assert len(declared) == _M2_DECLARED_CONSTRAINT_COUNT
    assert len(not_null) == _M2_NOT_NULL_CONSTRAINT_COUNT
    assert len(m2_constraints) == 38
    assert {r[1] for r in m2_constraints} == {*_M2_DECLARED_CONSTRAINT_KINDS, "n"}
    assert all(not r[3] and not r[4] and r[5] and r[6] for r in m2_constraints)


def test_m2_constraints_and_foreign_keys_are_live(
    provisioned_database: Any,
    alembic_config: Config,
) -> None:
    database = _upgrade_m2(provisioned_database, alembic_config)
    with _owner_connection(database) as connection:
        activity_ref = uuid7()
        connection.execute("INSERT INTO dante.activity (activity_ref) VALUES (%s)", (activity_ref,))
        connection.execute(
            "INSERT INTO dante.native_address (native_ref,owner_family) VALUES (%s,'activity')",
            (activity_ref,),
        )
        with pytest.raises(errors.CheckViolation):
            connection.execute(
                "INSERT INTO dante.schedule (schedule_ref,subject_native_ref) VALUES (%s,%s)",
                (uuid4(), activity_ref),
            )
        schedule_ref = uuid7()
        actual_ref = uuid7()
        connection.execute(
            "INSERT INTO dante.schedule (schedule_ref,subject_native_ref) VALUES (%s,%s)",
            (schedule_ref, activity_ref),
        )
        connection.execute(
            "INSERT INTO dante.actual (actual_ref,subject_native_ref) VALUES (%s,%s)",
            (actual_ref, activity_ref),
        )
        with pytest.raises(errors.ForeignKeyViolation):
            connection.execute(
                "INSERT INTO dante.actual (actual_ref,subject_native_ref) VALUES (%s,%s)",
                (uuid7(), uuid7()),
            )
        with pytest.raises(errors.CheckViolation):
            connection.execute(
                "INSERT INTO dante.scoped_address (scoped_ref,scoped_family) VALUES (%s,'recurrence')",
                (uuid7(),),
            )
        connection.execute(
            "INSERT INTO dante.scoped_address (scoped_ref,scoped_family) VALUES (%s,'schedule')",
            (schedule_ref,),
        )
        with pytest.raises(errors.CheckViolation):
            connection.execute(
                "INSERT INTO dante.material_state_address "
                "(material_state_ref,native_owner_ref,scoped_owner_ref,facet_code) "
                "VALUES (%s,%s,%s,'schedule.placement')",
                (uuid7(), activity_ref, schedule_ref),
            )
        material_state_ref = uuid7()
        connection.execute(
            "INSERT INTO dante.material_state_address "
            "(material_state_ref,scoped_owner_ref,facet_code) "
            "VALUES (%s,%s,'schedule.placement')",
            (material_state_ref, schedule_ref),
        )
        connection.execute(
            "INSERT INTO dante.scoped_current_material_state "
            "(scoped_owner_ref,facet_code,material_state_ref) "
            "VALUES (%s,'schedule.placement',%s)",
            (schedule_ref, material_state_ref),
        )


def test_m2_runtime_business_dml_remains_denied(
    provisioned_database: Any,
    alembic_config: Config,
) -> None:
    database = _upgrade_m2(provisioned_database, alembic_config)
    with _admin_connection(database) as connection:
        privileges = {
            name: tuple(
                connection.execute(
                    "SELECT has_table_privilege('dante_runtime',%s,'SELECT'),"
                    "has_table_privilege('dante_runtime',%s,'INSERT'),"
                    "has_table_privilege('dante_runtime',%s,'UPDATE'),"
                    "has_table_privilege('dante_runtime',%s,'DELETE')",
                    tuple([f"dante.{name}"] * 4),
                ).fetchone()
                or ()
            )
            for name in _M2_TABLES
        }
    assert privileges == dict.fromkeys(_M2_TABLES, (False, False, False, False))


def test_m2_upgrade_and_downgrade_preserve_m1_boundary(
    provisioned_database: Any,
    alembic_config: Config,
) -> None:
    command.upgrade(alembic_config, _M1_REVISION)
    command.upgrade(alembic_config, _M2_REVISION)
    with _admin_connection(provisioned_database) as connection:
        at_m2 = {
            str(r[0])
            for r in connection.execute(
                "SELECT tablename FROM pg_tables "
                "WHERE schemaname='dante' AND tablename<>'alembic_version'"
            )
        }
    assert at_m2 == _CUMULATIVE_TABLES
    command.downgrade(alembic_config, _M1_REVISION)
    with _admin_connection(provisioned_database) as connection:
        after = {
            str(r[0])
            for r in connection.execute(
                "SELECT tablename FROM pg_tables "
                "WHERE schemaname='dante' AND tablename<>'alembic_version'"
            )
        }
    assert after == _M1_TABLES


def test_m2_sqlalchemy_mapping_remains_registered_and_relationship_free() -> None:
    stage_tables = tuple(t for t in MAPPED_TABLES if t.name in _CUMULATIVE_TABLES)
    stage_mappers = tuple(
        mapper
        for mapper in Base.registry.mappers
        if cast(Table, mapper.local_table).name in _CUMULATIVE_TABLES
    )
    assert {t.name for t in stage_tables} == _CUMULATIVE_TABLES
    assert {cast(Table, m.local_table).name for m in stage_mappers} == _CUMULATIVE_TABLES
    assert len(stage_mappers) == 22
    assert all(len(m.relationships) == 0 for m in stage_mappers)


def test_m2_dictionary_entries_match_live_m2(
    provisioned_database: Any,
    alembic_config: Config,
) -> None:
    database = _upgrade_m2(provisioned_database, alembic_config)
    table_dir = _DICTIONARY_ROOT / "tables"
    entries = {
        name: json.loads((table_dir / f"{name}.json").read_text(encoding="utf-8"))
        for name in _CUMULATIVE_TABLES
    }
    with _admin_connection(database) as connection:
        database_columns = {
            (str(r[0]), str(r[1]), str(r[2]), str(r[3]))
            for r in connection.execute(
                """
                SELECT table_name,column_name,
                       CASE WHEN data_type='USER-DEFINED' THEN udt_name ELSE data_type END,
                       is_nullable
                FROM information_schema.columns
                WHERE table_schema='dante' AND table_name<>'alembic_version'
                """
            )
        }
    dictionary_columns = {
        (name, str(c["name"]), str(c["postgres_type"]), "YES" if c["nullable"] else "NO")
        for name, entry in entries.items()
        for c in entry["structure"]["columns"]
    }
    assert dictionary_columns == database_columns
    m2_entries = {name: entries[name] for name in _M2_TABLES}
    assert {e["implementation"]["alembic_revision"] for e in m2_entries.values()} == {_M2_REVISION}
    assert {e["implementation"]["introducing_stage"] for e in m2_entries.values()} == {"CP6-M02"}
    assert {
        check["name"] for e in m2_entries.values() for check in e["structure"]["check_constraints"]
    } == _M2_CHECKS
    assert {
        fk["name"] for e in m2_entries.values() for fk in e["structure"]["foreign_keys"]
    } == _M2_FOREIGN_KEYS
