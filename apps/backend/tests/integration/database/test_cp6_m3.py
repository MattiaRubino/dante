"""Permanent real-PostgreSQL stage proof for CP6-M03."""

from __future__ import annotations

import json
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any, cast
from uuid import uuid7

import psycopg
import pytest
from alembic import command
from alembic.config import Config
from psycopg import errors
from sqlalchemy import Table

from dante.platform.database.mappings import MAPPED_TABLES
from dante.platform.database.metadata import Base

pytestmark = pytest.mark.postgres

_M2_REVISION = "20260825_02"
_M3_REVISION = "20260825_03"
_M1_M2_TABLES = {
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
    "scoped_address",
    "schedule",
    "actual",
    "material_state_address",
    "native_current_material_state",
    "scoped_current_material_state",
}
_M3_TABLES = {
    "schedule_placement_state",
    "schedule_placement_date_state",
    "schedule_placement_floating_local_state",
    "schedule_placement_named_zone_state",
    "schedule_placement_absolute_state",
    "schedule_placement_current_history",
    "actual_realization_state",
    "actual_realization_timing",
    "actual_realization_session_basis",
    "actual_realization_current_history",
    "session_timing_state",
    "session_timing_absolute",
    "session_timing_elapsed",
    "session_timing_pause",
    "session_timing_current_history",
}
_CUMULATIVE_TABLES = _M1_M2_TABLES | _M3_TABLES
_M3_CHECKS = {
    "ck_schedule_placement_state_temporal_form",
    "ck_schedule_placement_date_state_date_span",
    "ck_schedule_placement_floating_local_state_extent",
    "ck_schedule_placement_floating_local_state_interval_order",
    "ck_schedule_placement_named_zone_state_extent",
    "ck_schedule_placement_named_zone_state_interval_order",
    "ck_schedule_placement_named_zone_state_resolved_pair",
    "ck_schedule_placement_absolute_state_extent",
    "ck_schedule_placement_absolute_state_interval_order",
    "ck_schedule_placement_current_history_current_interval",
    "ck_actual_realization_timing_extent",
    "ck_actual_realization_timing_interval_order",
    "ck_actual_realization_current_history_current_interval",
    "ck_session_timing_state_timing_form",
    "ck_session_timing_absolute_start_precision",
    "ck_session_timing_absolute_end_precision",
    "ck_session_timing_absolute_interval_order",
    "ck_session_timing_elapsed_elapsed_positive",
    "ck_session_timing_elapsed_elapsed_precision",
    "ck_session_timing_pause_pause_precision",
    "ck_session_timing_pause_resume_precision",
    "ck_session_timing_pause_resume_pair",
    "ck_session_timing_current_history_current_interval",
}
_M3_FOREIGN_KEYS = {
    "fk_schedule_placement_state_state_address",
    "fk_schedule_placement_state_schedule_ref_schedule",
    "fk_schedule_placement_date_state_placement_state",
    "fk_schedule_placement_floating_local_state_placement_state",
    "fk_schedule_placement_named_zone_state_placement_state",
    "fk_schedule_placement_absolute_state_placement_state",
    "fk_schedule_placement_current_history_schedule_ref_schedule",
    "fk_schedule_placement_current_history_placement_state",
    "fk_actual_realization_state_state_address",
    "fk_actual_realization_state_actual_ref_actual",
    "fk_actual_realization_timing_actual_state",
    "fk_actual_realization_session_basis_actual_state",
    "fk_actual_realization_session_basis_session_ref_session",
    "fk_actual_realization_session_basis_timing_state",
    "fk_actual_realization_current_history_actual_ref_actual",
    "fk_actual_realization_current_history_actual_state",
    "fk_session_timing_state_state_address",
    "fk_session_timing_state_session_ref_session",
    "fk_session_timing_absolute_timing_state",
    "fk_session_timing_elapsed_timing_state",
    "fk_session_timing_pause_timing_absolute",
    "fk_session_timing_current_history_session_ref_session",
    "fk_session_timing_current_history_timing_state",
}
_M3_EXPLICIT_INDEXES = {
    ("schedule_placement_state", "ix_schedule_placement_state_schedule_ref"),
    ("schedule_placement_current_history", "ux_schedule_placement_current_history_open"),
    (
        "schedule_placement_current_history",
        "ix_schedule_placement_current_history_material_state_ref",
    ),
    ("actual_realization_state", "ix_actual_realization_state_actual_ref"),
    ("actual_realization_session_basis", "ix_actual_realization_session_basis_session_ref"),
    ("actual_realization_session_basis", "ix_actual_realization_session_basis_timing_state"),
    ("actual_realization_current_history", "ux_actual_realization_current_history_open"),
    (
        "actual_realization_current_history",
        "ix_actual_realization_current_history_material_state_ref",
    ),
    ("session_timing_state", "ix_session_timing_state_session_ref"),
    ("session_timing_pause", "ux_session_timing_pause_open"),
    ("session_timing_current_history", "ux_session_timing_current_history_open"),
    ("session_timing_current_history", "ix_session_timing_current_history_material_state_ref"),
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


def _owner_connection(database: Any) -> psycopg.Connection[Any]:
    connection = psycopg.connect(
        **database.connection_kwargs("dante_migrator", database.cluster.migrator_password),
        autocommit=True,
    )
    connection.execute("SET ROLE dante_owner")
    return connection


def _upgrade_m3(database: Any, alembic_config: Config) -> Any:
    command.upgrade(alembic_config, _M3_REVISION)
    return database


def test_m3_materializes_exact_cumulative_topology(
    provisioned_database: Any,
    alembic_config: Config,
) -> None:
    database = _upgrade_m3(provisioned_database, alembic_config)
    with _admin_connection(database) as connection:
        tables = {
            str(r[0])
            for r in connection.execute(
                "SELECT tablename FROM pg_tables "
                "WHERE schemaname='dante' AND tablename<>'alembic_version'"
            )
        }
        owners = {
            (str(r[0]), str(r[1]))
            for r in connection.execute(
                "SELECT tablename,tableowner FROM pg_tables "
                "WHERE schemaname='dante' AND tablename<>'alembic_version'"
            )
        }
        constraints = {
            tuple(r)
            for r in connection.execute(
                """
            SELECT c.relname,con.contype,con.conname,con.condeferrable,
                   con.condeferred,con.convalidated,con.conenforced
            FROM pg_constraint con
            JOIN pg_class c ON c.oid=con.conrelid
            JOIN pg_namespace n ON n.oid=c.relnamespace
            WHERE n.nspname='dante' AND c.relname<>'alembic_version'
            """
            )
        }
        indexes = {
            (str(r[0]), str(r[1]))
            for r in connection.execute(
                "SELECT tablename,indexname FROM pg_indexes "
                "WHERE schemaname='dante' AND tablename<>'alembic_version'"
            )
        }
        views = {
            str(r[0])
            for r in connection.execute("SELECT viewname FROM pg_views WHERE schemaname='dante'")
        }
        routines = {
            str(r[0])
            for r in connection.execute(
                "SELECT p.proname FROM pg_proc p JOIN pg_namespace n ON n.oid=p.pronamespace "
                "WHERE n.nspname='dante'"
            )
        }
        triggers = {
            str(r[0])
            for r in connection.execute(
                "SELECT t.tgname FROM pg_trigger t JOIN pg_class c ON c.oid=t.tgrelid "
                "JOIN pg_namespace n ON n.oid=c.relnamespace "
                "WHERE n.nspname='dante' AND NOT t.tgisinternal"
            )
        }

    assert tables == _CUMULATIVE_TABLES
    assert owners == {(name, "dante_owner") for name in _CUMULATIVE_TABLES}
    assert len({r[2] for r in constraints if r[1] == "p"}) == 37
    assert len({r[2] for r in constraints if r[1] == "c"}) == 47
    assert len({r[2] for r in constraints if r[1] == "f"}) == 31
    assert len({r[2] for r in constraints if r[1] == "u"}) == 2
    assert len(indexes) == 55
    assert indexes >= _M3_EXPLICIT_INDEXES
    assert views == routines == triggers == set()

    m3 = [r for r in constraints if r[0] in _M3_TABLES]
    declared = [r for r in m3 if r[1] in {"p", "c", "f", "u"}]
    not_null = [r for r in m3 if r[1] == "n"]
    assert len(declared) == 61
    assert len(not_null) == 45
    assert len(m3) == 106
    assert {r[1] for r in m3} == {"p", "c", "f", "n"}
    assert {r[2] for r in m3 if r[1] == "c"} == _M3_CHECKS
    assert {r[2] for r in m3 if r[1] == "f"} == _M3_FOREIGN_KEYS
    assert all(not r[3] and not r[4] and r[5] and r[6] for r in m3)


def test_m3_constraints_foreign_keys_and_partial_uniques_are_live(
    provisioned_database: Any,
    alembic_config: Config,
) -> None:
    database = _upgrade_m3(provisioned_database, alembic_config)
    now = datetime.now(UTC).replace(microsecond=0)
    with _owner_connection(database) as connection:
        activity_ref = uuid7()
        schedule_ref = uuid7()
        actual_ref = uuid7()
        session_ref = uuid7()
        connection.execute("INSERT INTO dante.activity(activity_ref) VALUES (%s)", (activity_ref,))
        connection.execute("INSERT INTO dante.session(session_ref) VALUES (%s)", (session_ref,))
        connection.execute(
            "INSERT INTO dante.native_address(native_ref,owner_family) "
            "VALUES (%s,'activity'),(%s,'session')",
            (activity_ref, session_ref),
        )
        connection.execute(
            "INSERT INTO dante.schedule(schedule_ref,subject_native_ref) VALUES (%s,%s)",
            (schedule_ref, activity_ref),
        )
        connection.execute(
            "INSERT INTO dante.actual(actual_ref,subject_native_ref) VALUES (%s,%s)",
            (actual_ref, activity_ref),
        )
        connection.execute(
            "INSERT INTO dante.scoped_address(scoped_ref,scoped_family) "
            "VALUES (%s,'schedule'),(%s,'actual')",
            (schedule_ref, actual_ref),
        )

        schedule_state, actual_state, session_state = uuid7(), uuid7(), uuid7()
        connection.execute(
            "INSERT INTO dante.material_state_address"
            "(material_state_ref,scoped_owner_ref,facet_code) "
            "VALUES (%s,%s,'schedule.placement'),(%s,%s,'actual.realization')",
            (schedule_state, schedule_ref, actual_state, actual_ref),
        )
        connection.execute(
            "INSERT INTO dante.material_state_address"
            "(material_state_ref,native_owner_ref,facet_code) "
            "VALUES (%s,%s,'session.timing')",
            (session_state, session_ref),
        )

        with pytest.raises(errors.CheckViolation):
            connection.execute(
                "INSERT INTO dante.schedule_placement_state"
                "(material_state_ref,schedule_ref,temporal_form_code) VALUES (%s,%s,'bad')",
                (schedule_state, schedule_ref),
            )
        connection.execute(
            "INSERT INTO dante.schedule_placement_state"
            "(material_state_ref,schedule_ref,temporal_form_code) "
            "VALUES (%s,%s,'date_span')",
            (schedule_state, schedule_ref),
        )
        with pytest.raises(errors.CheckViolation):
            connection.execute(
                "INSERT INTO dante.schedule_placement_date_state"
                "(material_state_ref,date_span) "
                "VALUES (%s,'[2026-01-01,2026-01-01)'::daterange)",
                (schedule_state,),
            )
        connection.execute(
            "INSERT INTO dante.schedule_placement_date_state"
            "(material_state_ref,date_span) "
            "VALUES (%s,'[2026-01-01,2026-01-02)'::daterange)",
            (schedule_state,),
        )

        connection.execute(
            "INSERT INTO dante.session_timing_state"
            "(material_state_ref,session_ref,timing_form_code) VALUES (%s,%s,'absolute')",
            (session_state, session_ref),
        )
        connection.execute(
            "INSERT INTO dante.session_timing_absolute"
            "(material_state_ref,started_at,start_precision_code) VALUES (%s,%s,'exact')",
            (session_state, now),
        )
        with pytest.raises(errors.CheckViolation):
            connection.execute(
                "INSERT INTO dante.session_timing_elapsed"
                "(material_state_ref,elapsed_seconds,elapsed_precision_code) "
                "VALUES (%s,0,'exact')",
                (session_state,),
            )
        connection.execute(
            "INSERT INTO dante.session_timing_pause"
            "(material_state_ref,paused_at,pause_precision_code) VALUES (%s,%s,'exact')",
            (session_state, now + timedelta(minutes=1)),
        )
        with pytest.raises(errors.UniqueViolation):
            connection.execute(
                "INSERT INTO dante.session_timing_pause"
                "(material_state_ref,paused_at,pause_precision_code) VALUES (%s,%s,'rounded')",
                (session_state, now + timedelta(minutes=2)),
            )

        connection.execute(
            "INSERT INTO dante.actual_realization_state"
            "(material_state_ref,actual_ref,realization_occurred) VALUES (%s,%s,true)",
            (actual_state, actual_ref),
        )
        with pytest.raises(errors.CheckViolation):
            connection.execute(
                "INSERT INTO dante.actual_realization_timing"
                "(material_state_ref,extent_code,started_at) VALUES (%s,'bad',%s)",
                (actual_state, now),
            )
        connection.execute(
            "INSERT INTO dante.actual_realization_session_basis"
            "(actual_material_state_ref,session_ref,session_timing_material_state_ref) "
            "VALUES (%s,%s,%s)",
            (actual_state, session_ref, session_state),
        )

        connection.execute(
            "INSERT INTO dante.schedule_placement_current_history"
            "(schedule_ref,material_state_ref,current_from_at) VALUES (%s,%s,%s)",
            (schedule_ref, schedule_state, now),
        )
        with pytest.raises(errors.UniqueViolation):
            connection.execute(
                "INSERT INTO dante.schedule_placement_current_history"
                "(schedule_ref,material_state_ref,current_from_at) VALUES (%s,%s,%s)",
                (schedule_ref, schedule_state, now + timedelta(seconds=1)),
            )


def test_m3_runtime_business_dml_remains_denied(
    provisioned_database: Any,
    alembic_config: Config,
) -> None:
    database = _upgrade_m3(provisioned_database, alembic_config)
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
            for name in _M3_TABLES
        }
    assert privileges == dict.fromkeys(_M3_TABLES, (False, False, False, False))


def test_m3_upgrade_and_downgrade_preserve_m2_boundary(
    provisioned_database: Any,
    alembic_config: Config,
) -> None:
    command.upgrade(alembic_config, _M2_REVISION)
    command.upgrade(alembic_config, _M3_REVISION)
    with _admin_connection(provisioned_database) as connection:
        at_m3 = {
            str(r[0])
            for r in connection.execute(
                "SELECT tablename FROM pg_tables "
                "WHERE schemaname='dante' AND tablename<>'alembic_version'"
            )
        }
    assert at_m3 == _CUMULATIVE_TABLES
    command.downgrade(alembic_config, _M2_REVISION)
    with _admin_connection(provisioned_database) as connection:
        after = {
            str(r[0])
            for r in connection.execute(
                "SELECT tablename FROM pg_tables "
                "WHERE schemaname='dante' AND tablename<>'alembic_version'"
            )
        }
    assert after == _M1_M2_TABLES


def test_m3_sqlalchemy_mapping_is_exact_and_relationship_free() -> None:
    stage_tables = tuple(t for t in MAPPED_TABLES if t.name in _CUMULATIVE_TABLES)
    stage_mappers = tuple(
        mapper
        for mapper in Base.registry.mappers
        if cast(Table, mapper.local_table).name in _CUMULATIVE_TABLES
    )
    assert {t.name for t in stage_tables} == _CUMULATIVE_TABLES
    assert {cast(Table, m.local_table).name for m in stage_mappers} == _CUMULATIVE_TABLES
    assert len(stage_mappers) == 37
    assert all(len(m.relationships) == 0 for m in stage_mappers)


def test_m3_dictionary_matches_live_stage(
    provisioned_database: Any,
    alembic_config: Config,
) -> None:
    database = _upgrade_m3(provisioned_database, alembic_config)
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
    m3_entries = {name: entries[name] for name in _M3_TABLES}
    assert {e["implementation"]["alembic_revision"] for e in m3_entries.values()} == {_M3_REVISION}
    assert {e["implementation"]["introducing_stage"] for e in m3_entries.values()} == {"CP6-M03"}
    assert {
        check["name"] for e in m3_entries.values() for check in e["structure"]["check_constraints"]
    } == _M3_CHECKS
    assert {
        fk["name"] for e in m3_entries.values() for fk in e["structure"]["foreign_keys"]
    } == _M3_FOREIGN_KEYS
    assert {
        (name, index["name"])
        for name, e in m3_entries.items()
        for index in e["structure"]["indexes"]
        if index["source"] == "explicit_index"
    } == _M3_EXPLICIT_INDEXES
