"""Real PostgreSQL acceptance tests for CP6-M05 integrity/current-view materialization."""

from __future__ import annotations

from typing import Any
from uuid import uuid7

import psycopg
import pytest
from alembic import command
from alembic.config import Config
from psycopg import errors

from dante.platform.database.metadata import Base
from dante.platform.database.mappings import MAPPED_TABLES
from dante.platform.database.mappings.views import VIEW_METADATA

pytestmark = pytest.mark.postgres

_M4_REVISION = "20260825_04"
_M5_REVISION = "20260825_05"
_ROUTINES = {
    "enforce_native_address_owner",
    "enforce_scoped_address_owner",
    "enforce_native_ref_eligibility",
    "enforce_material_state_totality",
    "enforce_current_material_state_binding",
    "enforce_current_history_equivalence",
    "enforce_owner_creation_completeness",
    "enforce_schedule_placement_totality",
    "enforce_actual_realization_basis",
    "enforce_session_timing_totality",
    "enforce_session_pause_consistency",
    "enforce_recurrence_aggregate_integrity",
    "validate_iana_timezone",
}
_VIEWS = {
    "schedule_current_placement",
    "actual_current_realization",
    "session_current_timing",
    "routine_current_recurrence",
    "event_current_recurrence",
}


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


def _upgrade_m5(database: Any, alembic_config: Config) -> Any:
    command.upgrade(alembic_config, _M5_REVISION)
    return database


def _sqlstate(exc: BaseException) -> str | None:
    return getattr(exc, "sqlstate", None)


def test_m5_materializes_exact_topology_and_routine_security(
    provisioned_database: Any,
    alembic_config: Config,
) -> None:
    database = _upgrade_m5(provisioned_database, alembic_config)
    with _admin_connection(database) as connection:
        tables = {str(r[0]) for r in connection.execute(
            "SELECT tablename FROM pg_tables WHERE schemaname='dante' AND tablename<>'alembic_version'"
        )}
        views = {str(r[0]) for r in connection.execute(
            "SELECT viewname FROM pg_views WHERE schemaname='dante'"
        )}
        routines = {
            str(r[0]): tuple(r[1:])
            for r in connection.execute(
                """
                SELECT p.proname,p.prosecdef,p.provolatile,p.proparallel,p.proleakproof,
                       pg_get_userbyid(p.proowner),p.proconfig,
                       has_function_privilege('dante_runtime',p.oid,'EXECUTE'),
                       has_function_privilege('dante_migrator',p.oid,'EXECUTE'),
                       EXISTS (
                         SELECT 1 FROM aclexplode(coalesce(p.proacl,acldefault('f',p.proowner))) acl
                         WHERE acl.grantee=0 AND acl.privilege_type='EXECUTE'
                       )
                FROM pg_proc p
                JOIN pg_namespace n ON n.oid=p.pronamespace
                WHERE n.nspname='dante'
                """
            )
        }
        triggers = list(connection.execute(
            """
            SELECT t.tgconstraint<>0,con.condeferrable,con.condeferred
            FROM pg_trigger t
            JOIN pg_class c ON c.oid=t.tgrelid
            JOIN pg_namespace n ON n.oid=c.relnamespace
            LEFT JOIN pg_constraint con ON con.oid=t.tgconstraint
            WHERE n.nspname='dante' AND NOT t.tgisinternal
            """
        ))
        index_count = connection.execute(
            "SELECT count(*) FROM pg_indexes WHERE schemaname='dante' AND tablename<>'alembic_version'"
        ).fetchone()
        constraint_counts = dict(connection.execute(
            """
            SELECT con.contype,count(*)
            FROM pg_constraint con
            JOIN pg_class c ON c.oid=con.conrelid
            JOIN pg_namespace n ON n.oid=c.relnamespace
            WHERE n.nspname='dante' AND c.relname<>'alembic_version' AND con.contype IN ('c','f','u')
            GROUP BY con.contype
            """
        ))

    assert len(tables) == 63
    assert views == _VIEWS
    assert set(routines) == _ROUTINES
    for attrs in routines.values():
        prosecdef, volatility, parallel, leakproof, owner, config, runtime_x, migrator_x, public_x = attrs
        assert prosecdef is False
        assert volatility == "v"
        assert parallel == "u"
        assert leakproof is False
        assert owner == "dante_owner"
        assert config == ["search_path=pg_catalog, dante, pg_temp"]
        assert (runtime_x, migrator_x, public_x) == (False, False, False)
    assert len(triggers) == 66
    assert sum(not bool(row[0]) for row in triggers) == 15
    assert sum(bool(row[0]) for row in triggers) == 51
    assert all((not row[0]) or (row[1] and row[2]) for row in triggers)
    assert index_count == (87,)
    assert constraint_counts == {"c": 109, "f": 61, "u": 2}


def test_m5_views_are_ordinary_updatable_local_check_option(
    provisioned_database: Any,
    alembic_config: Config,
) -> None:
    database = _upgrade_m5(provisioned_database, alembic_config)
    with _admin_connection(database) as connection:
        rows = list(connection.execute(
            """
            SELECT table_name,is_updatable,check_option
            FROM information_schema.views
            WHERE table_schema='dante'
            ORDER BY table_name
            """
        ))
        view_triggers = list(connection.execute(
            """
            SELECT t.tgname
            FROM pg_trigger t
            JOIN pg_class c ON c.oid=t.tgrelid
            JOIN pg_namespace n ON n.oid=c.relnamespace
            WHERE n.nspname='dante' AND c.relkind='v' AND NOT t.tgisinternal
            """
        ))
    assert {str(row[0]) for row in rows} == _VIEWS
    assert all(str(row[1]) == "YES" and str(row[2]) == "LOCAL" for row in rows)
    assert view_triggers == []


def test_m5_sqlalchemy_view_metadata_is_core_only() -> None:
    assert set(VIEW_METADATA.tables) == {f"dante.{name}" for name in _VIEWS}
    assert all(name not in Base.metadata.tables for name in VIEW_METADATA.tables)
    assert len(tuple(MAPPED_TABLES)) == 63
    assert len(tuple(Base.registry.mappers)) == 63
    assert all(len(mapper.relationships) == 0 for mapper in Base.registry.mappers)


def test_m5_native_address_owner_binding_rejects_wrong_family(
    provisioned_database: Any,
    alembic_config: Config,
) -> None:
    database = _upgrade_m5(provisioned_database, alembic_config)
    person_ref = uuid7()
    with _owner_connection(database) as connection:
        connection.execute("INSERT INTO dante.person(person_ref) VALUES (%s)", (person_ref,))
        with pytest.raises(errors.ForeignKeyViolation) as exc_info:
            connection.execute(
                "INSERT INTO dante.native_address(native_ref,owner_family) VALUES (%s,'asset')",
                (person_ref,),
            )
    assert _sqlstate(exc_info.value) == "23503"


def test_m5_iana_timezone_rejects_unknown_identifier_before_fk(
    provisioned_database: Any,
    alembic_config: Config,
) -> None:
    database = _upgrade_m5(provisioned_database, alembic_config)
    with _owner_connection(database) as connection:
        with pytest.raises(errors.InvalidParameterValue) as exc_info:
            connection.execute(
                """
                INSERT INTO dante.schedule_placement_named_zone_state
                    (material_state_ref,extent_code,starts_local_at,zone_id)
                VALUES (%s,'point',timestamp '2026-01-01 12:00','Etc/Definitely_Not_A_Zone')
                """,
                (uuid7(),),
            )
    assert _sqlstate(exc_info.value) == "22023"


def test_m5_part17_check_repairs_are_live(
    provisioned_database: Any,
    alembic_config: Config,
) -> None:
    database = _upgrade_m5(provisioned_database, alembic_config)
    names = (
        "ck_session_timing_absolute_end_precision",
        "ck_routine_recurrence_calendar_state_step_unit",
        "ck_event_recurrence_calendar_state_step_unit",
        "ck_routine_recurrence_quota_state_week_start",
        "ck_event_recurrence_quota_state_week_start",
        "ck_routine_recurrence_elapsed_state_elapsed_positive",
        "ck_event_recurrence_elapsed_state_elapsed_positive",
    )
    with _admin_connection(database) as connection:
        defs = {
            str(row[0]): str(row[1])
            for row in connection.execute(
                """
                SELECT conname,pg_get_constraintdef(oid,true)
                FROM pg_constraint
                WHERE conname = ANY(%s)
                """,
                (list(names),),
            )
        }
    assert set(defs) == set(names)
    assert "end_precision_code IS NOT NULL" in defs["ck_session_timing_absolute_end_precision"]
    assert "step_unit_code IS NOT NULL" in defs["ck_routine_recurrence_calendar_state_step_unit"]
    assert "step_unit_code IS NOT NULL" in defs["ck_event_recurrence_calendar_state_step_unit"]
    assert "week_start IS NOT NULL" in defs["ck_routine_recurrence_quota_state_week_start"]
    assert "week_start IS NOT NULL" in defs["ck_event_recurrence_quota_state_week_start"]
    assert "trunc(elapsed_seconds, 6)" in defs["ck_routine_recurrence_elapsed_state_elapsed_positive"]
    assert "trunc(elapsed_seconds, 6)" in defs["ck_event_recurrence_elapsed_state_elapsed_positive"]


def test_m5_routines_have_no_dynamic_execute(
    provisioned_database: Any,
    alembic_config: Config,
) -> None:
    database = _upgrade_m5(provisioned_database, alembic_config)
    with _admin_connection(database) as connection:
        definitions = [str(row[0]) for row in connection.execute(
            """
            SELECT pg_get_functiondef(p.oid)
            FROM pg_proc p
            JOIN pg_namespace n ON n.oid=p.pronamespace
            WHERE n.nspname='dante'
            """
        )]
    assert definitions
    assert all("EXECUTE " not in definition.upper() for definition in definitions)


def test_m5_downgrade_returns_to_m4_surface(
    provisioned_database: Any,
    alembic_config: Config,
) -> None:
    command.upgrade(alembic_config, _M5_REVISION)
    command.downgrade(alembic_config, _M4_REVISION)
    with _admin_connection(provisioned_database) as connection:
        views = list(connection.execute("SELECT 1 FROM pg_views WHERE schemaname='dante'"))
        routines = list(connection.execute(
            "SELECT 1 FROM pg_proc p JOIN pg_namespace n ON n.oid=p.pronamespace WHERE n.nspname='dante'"
        ))
        triggers = list(connection.execute(
            """
            SELECT 1
            FROM pg_trigger t
            JOIN pg_class c ON c.oid=t.tgrelid
            JOIN pg_namespace n ON n.oid=c.relnamespace
            WHERE n.nspname='dante' AND NOT t.tgisinternal
            """
        ))
        end_def = connection.execute(
            """
            SELECT pg_get_constraintdef(oid,true)
            FROM pg_constraint
            WHERE conname='ck_session_timing_absolute_end_precision'
            """
        ).fetchone()
    assert views == routines == triggers == []
    assert end_def is not None
    assert "end_precision_code IS NOT NULL" not in str(end_def[0])
