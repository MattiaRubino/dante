"""Real PostgreSQL acceptance tests for CP6-M04 owner-bound Recurrence."""

from __future__ import annotations

import json
from datetime import UTC, datetime, time, timedelta
from pathlib import Path
from typing import Any
from uuid import uuid7

import psycopg
import pytest
from alembic import command
from alembic.config import Config
from psycopg import errors

from dante.platform.database.metadata import Base
from dante.platform.database.mappings import MAPPED_TABLES

pytestmark = pytest.mark.postgres

_M3_REVISION = "20260825_03"
_M4_REVISION = "20260825_04"
_PRE_M4_TABLES = {
    'activity',
    'actual',
    'actual_realization_current_history',
    'actual_realization_session_basis',
    'actual_realization_state',
    'actual_realization_timing',
    'asset',
    'collective',
    'content_artifact',
    'event',
    'goal',
    'living_referent',
    'material_state_address',
    'native_address',
    'native_current_material_state',
    'observation',
    'occurrence',
    'person',
    'place',
    'plan',
    'possibility',
    'routine',
    'schedule',
    'schedule_placement_absolute_state',
    'schedule_placement_current_history',
    'schedule_placement_date_state',
    'schedule_placement_floating_local_state',
    'schedule_placement_named_zone_state',
    'schedule_placement_state',
    'scoped_address',
    'scoped_current_material_state',
    'session',
    'session_timing_absolute',
    'session_timing_current_history',
    'session_timing_elapsed',
    'session_timing_pause',
    'session_timing_state',
}
_M4_TABLES = {
    'event_recurrence_boundary_state',
    'event_recurrence_calendar_month_day',
    'event_recurrence_calendar_ordinal_weekday',
    'event_recurrence_calendar_state',
    'event_recurrence_calendar_wall_time',
    'event_recurrence_calendar_weekday',
    'event_recurrence_calendar_year_month_day',
    'event_recurrence_current_history',
    'event_recurrence_cycle_position',
    'event_recurrence_cyclic_state',
    'event_recurrence_elapsed_state',
    'event_recurrence_quota_state',
    'event_recurrence_state',
    'routine_recurrence_boundary_state',
    'routine_recurrence_calendar_month_day',
    'routine_recurrence_calendar_ordinal_weekday',
    'routine_recurrence_calendar_state',
    'routine_recurrence_calendar_wall_time',
    'routine_recurrence_calendar_weekday',
    'routine_recurrence_calendar_year_month_day',
    'routine_recurrence_current_history',
    'routine_recurrence_cycle_position',
    'routine_recurrence_cyclic_state',
    'routine_recurrence_elapsed_state',
    'routine_recurrence_quota_state',
    'routine_recurrence_state',
}
_CUMULATIVE_TABLES = _PRE_M4_TABLES | _M4_TABLES
_M4_CHECKS = {
    'ck_event_recurrence_boundary_state_boundary_kind',
    'ck_event_recurrence_boundary_state_boundary_payload',
    'ck_event_recurrence_boundary_state_boundary_role',
    'ck_event_recurrence_boundary_state_inclusive_role',
    'ck_event_recurrence_calendar_month_day_month_day_range',
    'ck_event_recurrence_calendar_ordinal_weekday_ordinal_range',
    'ck_event_recurrence_calendar_ordinal_weekday_weekday_range',
    'ck_event_recurrence_calendar_state_clock_basis',
    'ck_event_recurrence_calendar_state_interval_positive',
    'ck_event_recurrence_calendar_state_pattern_code',
    'ck_event_recurrence_calendar_state_step_unit',
    'ck_event_recurrence_calendar_state_zone_basis',
    'ck_event_recurrence_calendar_weekday_weekday_range',
    'ck_event_recurrence_calendar_year_month_day_month_day_range',
    'ck_event_recurrence_calendar_year_month_day_month_range',
    'ck_event_recurrence_current_history_current_interval',
    'ck_event_recurrence_cycle_position_position_nonnegative',
    'ck_event_recurrence_cyclic_state_cycle_length_positive',
    'ck_event_recurrence_cyclic_state_position_unit',
    'ck_event_recurrence_elapsed_state_anchor_at',
    'ck_event_recurrence_elapsed_state_anchor_mode',
    'ck_event_recurrence_elapsed_state_elapsed_positive',
    'ck_event_recurrence_quota_state_frame',
    'ck_event_recurrence_quota_state_period_span_positive',
    'ck_event_recurrence_quota_state_period_unit',
    'ck_event_recurrence_quota_state_quota_positive',
    'ck_event_recurrence_quota_state_week_start',
    'ck_event_recurrence_quota_state_zone_basis',
    'ck_event_recurrence_state_expected_count',
    'ck_event_recurrence_state_family_code',
    'ck_event_recurrence_state_range_kind',
    'ck_routine_recurrence_boundary_state_boundary_kind',
    'ck_routine_recurrence_boundary_state_boundary_payload',
    'ck_routine_recurrence_boundary_state_boundary_role',
    'ck_routine_recurrence_boundary_state_inclusive_role',
    'ck_routine_recurrence_calendar_month_day_month_day_range',
    'ck_routine_recurrence_calendar_ordinal_weekday_ordinal_range',
    'ck_routine_recurrence_calendar_ordinal_weekday_weekday_range',
    'ck_routine_recurrence_calendar_state_clock_basis',
    'ck_routine_recurrence_calendar_state_interval_positive',
    'ck_routine_recurrence_calendar_state_pattern_code',
    'ck_routine_recurrence_calendar_state_step_unit',
    'ck_routine_recurrence_calendar_state_zone_basis',
    'ck_routine_recurrence_calendar_weekday_weekday_range',
    'ck_routine_recurrence_calendar_year_month_day_month_day_range',
    'ck_routine_recurrence_calendar_year_month_day_month_range',
    'ck_routine_recurrence_current_history_current_interval',
    'ck_routine_recurrence_cycle_position_position_nonnegative',
    'ck_routine_recurrence_cyclic_state_cycle_length_positive',
    'ck_routine_recurrence_cyclic_state_position_unit',
    'ck_routine_recurrence_elapsed_state_anchor_at',
    'ck_routine_recurrence_elapsed_state_anchor_mode',
    'ck_routine_recurrence_elapsed_state_elapsed_positive',
    'ck_routine_recurrence_quota_state_frame',
    'ck_routine_recurrence_quota_state_period_span_positive',
    'ck_routine_recurrence_quota_state_period_unit',
    'ck_routine_recurrence_quota_state_quota_positive',
    'ck_routine_recurrence_quota_state_week_start',
    'ck_routine_recurrence_quota_state_zone_basis',
    'ck_routine_recurrence_state_expected_count',
    'ck_routine_recurrence_state_family_code',
    'ck_routine_recurrence_state_range_kind',
}
_M4_FOREIGN_KEYS = {
    'fk_event_recurrence_boundary_state_recurrence_state',
    'fk_event_recurrence_calendar_month_day_calendar_state',
    'fk_event_recurrence_calendar_ordinal_weekday_calendar_state',
    'fk_event_recurrence_calendar_state_recurrence_state',
    'fk_event_recurrence_calendar_wall_time_calendar_state',
    'fk_event_recurrence_calendar_weekday_calendar_state',
    'fk_event_recurrence_calendar_year_month_day_calendar_state',
    'fk_event_recurrence_current_history_event_ref_event',
    'fk_event_recurrence_current_history_recurrence_state',
    'fk_event_recurrence_cycle_position_cyclic_state',
    'fk_event_recurrence_cyclic_state_recurrence_state',
    'fk_event_recurrence_elapsed_state_recurrence_state',
    'fk_event_recurrence_quota_state_recurrence_state',
    'fk_event_recurrence_state_event_ref_event',
    'fk_event_recurrence_state_state_address',
    'fk_routine_recurrence_boundary_state_recurrence_state',
    'fk_routine_recurrence_calendar_month_day_calendar_state',
    'fk_routine_recurrence_calendar_ordinal_weekday_calendar_state',
    'fk_routine_recurrence_calendar_state_recurrence_state',
    'fk_routine_recurrence_calendar_wall_time_calendar_state',
    'fk_routine_recurrence_calendar_weekday_calendar_state',
    'fk_routine_recurrence_calendar_year_month_day_calendar_state',
    'fk_routine_recurrence_current_history_recurrence_state',
    'fk_routine_recurrence_current_history_routine_ref_routine',
    'fk_routine_recurrence_cycle_position_cyclic_state',
    'fk_routine_recurrence_cyclic_state_recurrence_state',
    'fk_routine_recurrence_elapsed_state_recurrence_state',
    'fk_routine_recurrence_quota_state_recurrence_state',
    'fk_routine_recurrence_state_routine_ref_routine',
    'fk_routine_recurrence_state_state_address',
}
_M4_EXPLICIT_INDEXES = {
    ('event_recurrence_current_history', 'ix_event_recurrence_current_history_material_state_ref'),
    ('event_recurrence_current_history', 'ux_event_recurrence_current_history_open'),
    ('event_recurrence_state', 'ix_event_recurrence_state_event_ref'),
    ('routine_recurrence_current_history', 'ix_routine_recurrence_current_history_material_state_ref'),
    ('routine_recurrence_current_history', 'ux_routine_recurrence_current_history_open'),
    ('routine_recurrence_state', 'ix_routine_recurrence_state_routine_ref'),
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


def _upgrade_m4(database: Any, alembic_config: Config) -> Any:
    command.upgrade(alembic_config, _M4_REVISION)
    return database


def test_m4_materializes_exact_cumulative_topology(
    provisioned_database: Any,
    alembic_config: Config,
) -> None:
    database = _upgrade_m4(provisioned_database, alembic_config)
    with _admin_connection(database) as connection:
        tables = {str(r[0]) for r in connection.execute(
            "SELECT tablename FROM pg_tables "
            "WHERE schemaname='dante' AND tablename<>'alembic_version'"
        )}
        owners = {(str(r[0]), str(r[1])) for r in connection.execute(
            "SELECT tablename,tableowner FROM pg_tables "
            "WHERE schemaname='dante' AND tablename<>'alembic_version'"
        )}
        constraints = {tuple(r) for r in connection.execute(
            """
            SELECT c.relname,con.contype,con.conname,con.condeferrable,
                   con.condeferred,con.convalidated,con.conenforced
            FROM pg_constraint con
            JOIN pg_class c ON c.oid=con.conrelid
            JOIN pg_namespace n ON n.oid=c.relnamespace
            WHERE n.nspname='dante' AND c.relname<>'alembic_version'
            """
        )}
        indexes = {(str(r[0]), str(r[1])) for r in connection.execute(
            "SELECT tablename,indexname FROM pg_indexes "
            "WHERE schemaname='dante' AND tablename<>'alembic_version'"
        )}
        views = {str(r[0]) for r in connection.execute(
            "SELECT viewname FROM pg_views WHERE schemaname='dante'"
        )}
        routines = {str(r[0]) for r in connection.execute(
            "SELECT p.proname FROM pg_proc p JOIN pg_namespace n ON n.oid=p.pronamespace "
            "WHERE n.nspname='dante'"
        )}
        triggers = {str(r[0]) for r in connection.execute(
            "SELECT t.tgname FROM pg_trigger t JOIN pg_class c ON c.oid=t.tgrelid "
            "JOIN pg_namespace n ON n.oid=c.relnamespace "
            "WHERE n.nspname='dante' AND NOT t.tgisinternal"
        )}

    assert tables == _CUMULATIVE_TABLES
    assert owners == {(name, "dante_owner") for name in _CUMULATIVE_TABLES}
    assert len({r[2] for r in constraints if r[1] == "p"}) == 63
    assert len({r[2] for r in constraints if r[1] == "c"}) == 109
    assert len({r[2] for r in constraints if r[1] == "f"}) == 61
    assert len({r[2] for r in constraints if r[1] == "u"}) == 2
    assert len(indexes) == 87
    assert _M4_EXPLICIT_INDEXES <= indexes
    assert views == routines == triggers == set()

    m4 = [r for r in constraints if r[0] in _M4_TABLES]
    declared = [r for r in m4 if r[1] in {"p", "c", "f", "u"}]
    not_null = [r for r in m4 if r[1] == "n"]
    assert len(declared) == 118
    assert len(not_null) == 82
    assert len(m4) == 200
    assert {r[1] for r in m4} == {"p", "c", "f", "n"}
    assert {r[2] for r in m4 if r[1] == "c"} == _M4_CHECKS
    assert {r[2] for r in m4 if r[1] == "f"} == _M4_FOREIGN_KEYS
    assert all(not r[3] and not r[4] and r[5] and r[6] for r in m4)


def test_m4_constraints_foreign_keys_and_partial_uniques_are_live(
    provisioned_database: Any,
    alembic_config: Config,
) -> None:
    database = _upgrade_m4(provisioned_database, alembic_config)
    now = datetime.now(UTC).replace(microsecond=0)
    with _owner_connection(database) as connection:
        routine_ref, event_ref = uuid7(), uuid7()
        connection.execute(
            "INSERT INTO dante.routine(routine_ref) VALUES (%s)", (routine_ref,)
        )
        connection.execute(
            "INSERT INTO dante.event(event_ref) VALUES (%s)", (event_ref,)
        )
        connection.execute(
            "INSERT INTO dante.native_address(native_ref,owner_family) "
            "VALUES (%s,'routine'),(%s,'event')",
            (routine_ref, event_ref),
        )

        routine_state, event_state = uuid7(), uuid7()
        connection.execute(
            "INSERT INTO dante.material_state_address"
            "(material_state_ref,native_owner_ref,facet_code) "
            "VALUES (%s,%s,'routine.recurrence'),(%s,%s,'event.recurrence')",
            (routine_state, routine_ref, event_state, event_ref),
        )

        with pytest.raises(errors.CheckViolation):
            connection.execute(
                "INSERT INTO dante.routine_recurrence_state"
                "(material_state_ref,routine_ref,family_code,range_kind) "
                "VALUES (%s,%s,'bad','open')",
                (routine_state, routine_ref),
            )
        connection.execute(
            "INSERT INTO dante.routine_recurrence_state"
            "(material_state_ref,routine_ref,family_code,range_kind) "
            "VALUES (%s,%s,'calendar_wall_clock','open')",
            (routine_state, routine_ref),
        )
        connection.execute(
            "INSERT INTO dante.event_recurrence_state"
            "(material_state_ref,event_ref,family_code,range_kind,expected_occurrence_count) "
            "VALUES (%s,%s,'elapsed_interval','expected_count',2)",
            (event_state, event_ref),
        )

        with pytest.raises(errors.CheckViolation):
            connection.execute(
                "INSERT INTO dante.routine_recurrence_boundary_state"
                "(material_state_ref,boundary_role,boundary_kind,local_value,inclusive) "
                "VALUES (%s,'effective_from','named_zone_local',timestamp '2026-01-01 09:00',true)",
                (routine_state,),
            )
        connection.execute(
            "INSERT INTO dante.routine_recurrence_boundary_state"
            "(material_state_ref,boundary_role,boundary_kind,date_value,inclusive) "
            "VALUES (%s,'effective_from','date',date '2026-01-01',true)",
            (routine_state,),
        )

        with pytest.raises(errors.CheckViolation):
            connection.execute(
                "INSERT INTO dante.routine_recurrence_calendar_state"
                "(material_state_ref,pattern_code,interval_count,clock_basis_code) "
                "VALUES (%s,'weekly_weekdays',0,'floating_local')",
                (routine_state,),
            )
        connection.execute(
            "INSERT INTO dante.routine_recurrence_calendar_state"
            "(material_state_ref,pattern_code,interval_count,clock_basis_code) "
            "VALUES (%s,'weekly_weekdays',1,'floating_local')",
            (routine_state,),
        )
        connection.execute(
            "INSERT INTO dante.routine_recurrence_calendar_wall_time"
            "(material_state_ref,wall_time) VALUES (%s,%s)",
            (routine_state, time(9, 0)),
        )
        with pytest.raises(errors.CheckViolation):
            connection.execute(
                "INSERT INTO dante.routine_recurrence_calendar_weekday"
                "(material_state_ref,weekday_number) VALUES (%s,8)",
                (routine_state,),
            )
        connection.execute(
            "INSERT INTO dante.routine_recurrence_calendar_weekday"
            "(material_state_ref,weekday_number) VALUES (%s,1)",
            (routine_state,),
        )
        with pytest.raises(errors.CheckViolation):
            connection.execute(
                "INSERT INTO dante.routine_recurrence_calendar_month_day"
                "(material_state_ref,month_day) VALUES (%s,0)",
                (routine_state,),
            )
        with pytest.raises(errors.CheckViolation):
            connection.execute(
                "INSERT INTO dante.routine_recurrence_calendar_ordinal_weekday"
                "(material_state_ref,weekday_number,ordinal) VALUES (%s,1,0)",
                (routine_state,),
            )
        with pytest.raises(errors.CheckViolation):
            connection.execute(
                "INSERT INTO dante.routine_recurrence_calendar_year_month_day"
                "(material_state_ref,month_number,month_day) VALUES (%s,13,1)",
                (routine_state,),
            )

        with pytest.raises(errors.CheckViolation):
            connection.execute(
                "INSERT INTO dante.event_recurrence_elapsed_state"
                "(material_state_ref,elapsed_seconds,anchor_mode_code,anchor_at) "
                "VALUES (%s,'NaN','fixed_anchor',%s)",
                (event_state, now),
            )
        connection.execute(
            "INSERT INTO dante.event_recurrence_elapsed_state"
            "(material_state_ref,elapsed_seconds,anchor_mode_code,anchor_at) "
            "VALUES (%s,60,'fixed_anchor',%s)",
            (event_state, now),
        )
        with pytest.raises(errors.CheckViolation):
            connection.execute(
                "INSERT INTO dante.event_recurrence_quota_state"
                "(material_state_ref,quota_count,period_unit_code,period_span,frame_code) "
                "VALUES (%s,0,'day',1,'absolute_utc')",
                (event_state,),
            )
        connection.execute(
            "INSERT INTO dante.event_recurrence_quota_state"
            "(material_state_ref,quota_count,period_unit_code,period_span,frame_code) "
            "VALUES (%s,1,'day',1,'absolute_utc')",
            (event_state,),
        )
        with pytest.raises(errors.CheckViolation):
            connection.execute(
                "INSERT INTO dante.event_recurrence_cyclic_state"
                "(material_state_ref,cycle_length,position_unit_code) VALUES (%s,0,'day')",
                (event_state,),
            )
        connection.execute(
            "INSERT INTO dante.event_recurrence_cyclic_state"
            "(material_state_ref,cycle_length,position_unit_code) VALUES (%s,2,'day')",
            (event_state,),
        )
        with pytest.raises(errors.CheckViolation):
            connection.execute(
                "INSERT INTO dante.event_recurrence_cycle_position"
                "(material_state_ref,position_index,generates_expected) VALUES (%s,-1,true)",
                (event_state,),
            )
        connection.execute(
            "INSERT INTO dante.event_recurrence_cycle_position"
            "(material_state_ref,position_index,generates_expected) VALUES (%s,0,true)",
            (event_state,),
        )

        with pytest.raises(errors.ForeignKeyViolation):
            connection.execute(
                "INSERT INTO dante.event_recurrence_boundary_state"
                "(material_state_ref,boundary_role,boundary_kind,date_value,inclusive) "
                "VALUES (%s,'effective_from','date',date '2026-01-01',true)",
                (uuid7(),),
            )

        connection.execute(
            "INSERT INTO dante.routine_recurrence_current_history"
            "(routine_ref,material_state_ref,current_from_at) VALUES (%s,%s,%s)",
            (routine_ref, routine_state, now),
        )
        with pytest.raises(errors.UniqueViolation):
            connection.execute(
                "INSERT INTO dante.routine_recurrence_current_history"
                "(routine_ref,material_state_ref,current_from_at) VALUES (%s,%s,%s)",
                (routine_ref, routine_state, now + timedelta(seconds=1)),
            )


def test_m4_runtime_business_dml_remains_denied(
    provisioned_database: Any,
    alembic_config: Config,
) -> None:
    database = _upgrade_m4(provisioned_database, alembic_config)
    with _admin_connection(database) as connection:
        privileges = {
            name: tuple(connection.execute(
                "SELECT has_table_privilege('dante_runtime',%s,'SELECT'),"
                "has_table_privilege('dante_runtime',%s,'INSERT'),"
                "has_table_privilege('dante_runtime',%s,'UPDATE'),"
                "has_table_privilege('dante_runtime',%s,'DELETE')",
                tuple([f"dante.{name}"] * 4),
            ).fetchone() or ())
            for name in _M4_TABLES
        }
    assert privileges == {name: (False, False, False, False) for name in _M4_TABLES}


def test_m4_upgrade_and_downgrade_preserve_m3_boundary(
    provisioned_database: Any,
    alembic_config: Config,
) -> None:
    command.upgrade(alembic_config, _M3_REVISION)
    command.upgrade(alembic_config, _M4_REVISION)
    with _admin_connection(provisioned_database) as connection:
        at_m4 = {str(r[0]) for r in connection.execute(
            "SELECT tablename FROM pg_tables "
            "WHERE schemaname='dante' AND tablename<>'alembic_version'"
        )}
    assert at_m4 == _CUMULATIVE_TABLES
    command.downgrade(alembic_config, _M3_REVISION)
    with _admin_connection(provisioned_database) as connection:
        after = {str(r[0]) for r in connection.execute(
            "SELECT tablename FROM pg_tables "
            "WHERE schemaname='dante' AND tablename<>'alembic_version'"
        )}
    assert after == _PRE_M4_TABLES


def test_m4_sqlalchemy_mapping_is_exact_and_relationship_free() -> None:
    assert {table.name for table in MAPPED_TABLES} == _CUMULATIVE_TABLES
    assert set(Base.metadata.tables) == {f"dante.{name}" for name in _CUMULATIVE_TABLES}
    assert len(tuple(Base.registry.mappers)) == 63
    assert all(len(mapper.relationships) == 0 for mapper in Base.registry.mappers)


def test_m4_dictionary_matches_live_stage_and_current_scope(
    provisioned_database: Any,
    alembic_config: Config,
) -> None:
    database = _upgrade_m4(provisioned_database, alembic_config)
    table_dir = _DICTIONARY_ROOT / "tables"
    entries = {
        path.stem: json.loads(path.read_text(encoding="utf-8"))
        for path in table_dir.glob("*.json")
    }
    scope = json.loads((_DICTIONARY_ROOT / "scope.json").read_text(encoding="utf-8"))
    assert set(entries) == _CUMULATIVE_TABLES
    assert scope["current_materialization"] == {
        "completed_stages": ["CP6-M01", "CP6-M02", "CP6-M03", "CP6-M04"],
        "standalone_entries": {"tables": 63, "views": 0, "routines": 0, "total": 63},
        "embedded_objects": {"triggers": 0, "physical_indexes": 87},
        "constraints": {"foreign_keys": 61, "check_constraints": 109},
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

    m4_entries = {name: entries[name] for name in _M4_TABLES}
    assert {e["implementation"]["alembic_revision"] for e in m4_entries.values()} == {_M4_REVISION}
    assert {e["implementation"]["introducing_stage"] for e in m4_entries.values()} == {"CP6-M04"}
    assert {
        check["name"]
        for e in m4_entries.values()
        for check in e["structure"]["check_constraints"]
    } == _M4_CHECKS
    assert {
        fk["name"]
        for e in m4_entries.values()
        for fk in e["structure"]["foreign_keys"]
    } == _M4_FOREIGN_KEYS
    assert {
        (name, index["name"])
        for name, e in m4_entries.items()
        for index in e["structure"]["indexes"]
        if index["source"] == "explicit_index"
    } == _M4_EXPLICIT_INDEXES
