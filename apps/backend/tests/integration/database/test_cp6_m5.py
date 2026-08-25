"""Real PostgreSQL acceptance tests for CP6-M05 integrity/current-view materialization."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
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

def _admin_connection(database: Any, *, autocommit: bool = True) -> psycopg.Connection[Any]:
    return psycopg.connect(
        host=database.cluster.host,
        port=database.cluster.port,
        dbname=database.name,
        user=database.cluster.admin_user,
        password=database.cluster.admin_password,
        autocommit=autocommit,
    )


def _owner_connection(database: Any, *, autocommit: bool = False) -> psycopg.Connection[Any]:
    connection = psycopg.connect(
        **database.connection_kwargs("dante_migrator", database.cluster.migrator_password),
        autocommit=autocommit,
    )
    connection.execute("SET ROLE dante_owner")
    return connection


def _upgrade_m5(database: Any, alembic_config: Config) -> Any:
    command.upgrade(alembic_config, _M5_REVISION)
    return database


def _sqlstate(exc: BaseException) -> str | None:
    return getattr(exc, "sqlstate", None)


def _make_valid_schedule(connection: psycopg.Connection[Any]) -> tuple[Any, Any, Any]:
    activity_ref, schedule_ref, state_ref = uuid7(), uuid7(), uuid7()
    now = datetime.now(UTC).replace(microsecond=0)
    connection.execute("INSERT INTO dante.activity(activity_ref) VALUES (%s)", (activity_ref,))
    connection.execute(
        "INSERT INTO dante.native_address(native_ref,owner_family) VALUES (%s,'activity')",
        (activity_ref,),
    )
    connection.execute(
        "INSERT INTO dante.schedule(schedule_ref,subject_native_ref) VALUES (%s,%s)",
        (schedule_ref, activity_ref),
    )
    connection.execute(
        "INSERT INTO dante.scoped_address(scoped_ref,scoped_family) VALUES (%s,'schedule')",
        (schedule_ref,),
    )
    connection.execute(
        "INSERT INTO dante.material_state_address(material_state_ref,scoped_owner_ref,facet_code) "
        "VALUES (%s,%s,'schedule.placement')",
        (state_ref, schedule_ref),
    )
    connection.execute(
        "INSERT INTO dante.schedule_placement_state(material_state_ref,schedule_ref,temporal_form_code) "
        "VALUES (%s,%s,'date_span')",
        (state_ref, schedule_ref),
    )
    connection.execute(
        "INSERT INTO dante.schedule_placement_date_state(material_state_ref,date_span) "
        "VALUES (%s,'[2026-01-01,2026-01-02)'::daterange)",
        (state_ref,),
    )
    connection.execute(
        "INSERT INTO dante.schedule_current_placement(scoped_owner_ref,material_state_ref) VALUES (%s,%s)",
        (schedule_ref, state_ref),
    )
    connection.execute(
        "INSERT INTO dante.schedule_placement_current_history(schedule_ref,material_state_ref,current_from_at) "
        "VALUES (%s,%s,%s)",
        (schedule_ref, state_ref, now),
    )
    connection.execute("SET CONSTRAINTS ALL IMMEDIATE")
    connection.execute("SET CONSTRAINTS ALL DEFERRED")
    return schedule_ref, state_ref, now


def _make_valid_routine_recurrence(connection: psycopg.Connection[Any]) -> tuple[Any, Any, Any]:
    routine_ref, state_ref = uuid7(), uuid7()
    now = datetime.now(UTC).replace(microsecond=0)
    connection.execute("INSERT INTO dante.routine(routine_ref) VALUES (%s)", (routine_ref,))
    connection.execute(
        "INSERT INTO dante.native_address(native_ref,owner_family) VALUES (%s,'routine')",
        (routine_ref,),
    )
    connection.execute(
        "INSERT INTO dante.material_state_address(material_state_ref,native_owner_ref,facet_code) "
        "VALUES (%s,%s,'routine.recurrence')",
        (state_ref, routine_ref),
    )
    connection.execute(
        "INSERT INTO dante.routine_recurrence_state(material_state_ref,routine_ref,family_code,range_kind) "
        "VALUES (%s,%s,'calendar_wall_clock','open')",
        (state_ref, routine_ref),
    )
    connection.execute(
        "INSERT INTO dante.routine_recurrence_calendar_state"
        "(material_state_ref,pattern_code,interval_count,clock_basis_code) "
        "VALUES (%s,'daily',1,'floating_local')",
        (state_ref,),
    )
    connection.execute(
        "INSERT INTO dante.routine_current_recurrence(native_owner_ref,material_state_ref) VALUES (%s,%s)",
        (routine_ref, state_ref),
    )
    connection.execute(
        "INSERT INTO dante.routine_recurrence_current_history(routine_ref,material_state_ref,current_from_at) "
        "VALUES (%s,%s,%s)",
        (routine_ref, state_ref, now),
    )
    connection.execute("SET CONSTRAINTS ALL IMMEDIATE")
    connection.execute("SET CONSTRAINTS ALL DEFERRED")
    return routine_ref, state_ref, now


def test_m5_materializes_exact_topology_and_security(
    provisioned_database: Any,
    alembic_config: Config,
) -> None:
    database = _upgrade_m5(provisioned_database, alembic_config)
    with _admin_connection(database) as connection:
        table_count = connection.execute(
            "SELECT count(*) FROM pg_tables WHERE schemaname='dante' AND tablename<>'alembic_version'"
        ).fetchone()
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
                FROM pg_proc p JOIN pg_namespace n ON n.oid=p.pronamespace
                WHERE n.nspname='dante'
                """
            )
        }
        triggers = list(connection.execute(
            """
            SELECT t.tgname,t.tgconstraint<>0,con.condeferrable,con.condeferred
            FROM pg_trigger t
            JOIN pg_class c ON c.oid=t.tgrelid
            JOIN pg_namespace n ON n.oid=c.relnamespace
            LEFT JOIN pg_constraint con ON con.oid=t.tgconstraint
²È="25•˜±™…•Ñ}½‘”¤Y1UL€ •Ì°•Ì°Í¡•‘Õ±”¹Á±…•µ•¹Ðœ¤ˆ°(€€€€€€€€€€€€¡ÍÑ…Ñ•}É•˜°Í¡•‘Õ±•}É•˜¤°(€€€€€€€€¤(€€€€€€€Ý¥Ñ ÁåÑ•ÍÐ¹É…¥Í•Ì¡•ÉÉ½ÉÌ¹¡•­Y¥½±…Ñ¥½¸¤…Ì•á}¥¹™¼è(€€€€€€€€€€€½¹¹•Ñ¥½¸¹•á•ÕÑ” ‰MP=9MQI%9QL10%55%Qˆ¤(€€€€€€€…ÍÍ•ÉÐ}ÍÅ±ÍÑ…Ñ”¡•á}¥¹™¼¹Ù…±Õ”¤€ôô€ˆÈÌÔÄÐˆ(€€€€€€€½¹¹•Ñ¥½¸¹É½±±‰…¬ ¤((€€€Ý¥Ñ }½Ý¹•É}½¹¹•Ñ¥½¸¡‘…Ñ…‰…Í”¤…Ì½¹¹•Ñ¥½¸è(€€€€€€€}µ…­•}Ù…±¥‘}Í¡•‘Õ±”¡½¹¹•Ñ¥½¸¤(€€€€€€€½¹¹•Ñ¥½¸¹½µµ¥Ð ¤(()‘•˜Ñ•ÍÑ}´Õ}Í¡•‘Õ±•}Ù¥•Ý}‘•™…Õ±ÑÍ}™…•Ñ}…¹‘}‰±½­Í}•Í…Á” (€€€ÁÉ½Ù¥Í¥½¹•‘}‘…Ñ…‰…Í”è¹ä°(€€€…±•µ‰¥}½¹™¥œè½¹™¥œ°(¤€´ø9½¹”è(€€€‘…Ñ…‰…Í”€ô}ÕÁÉ…‘•}´Ô¡ÁÉ½Ù¥Í¥½¹•‘}‘…Ñ…‰…Í”°…±•µ‰¥}½¹™¥œ¤(€€€Ý¥Ñ }½Ý¹•É}½¹¹•Ñ¥½¸¡‘…Ñ…‰…Í”¤…Ì½¹¹•Ñ¥½¸è(€€€€€€€Í¡•‘Õ±•}É•˜°ÍÑ…Ñ•}É•˜°|€ô}µ…­•}Ù…±¥‘}Í¡•‘Õ±”¡½¹¹•Ñ¥½¸¤(€€€€€€€É½Ü€ô½¹¹•Ñ¥½¸¹•á•ÕÑ” (€€€€€€€€€€€€‰M1PÍ½Á•‘}½Ý¹•É}É•˜±™…•Ñ}½‘”±µ…Ñ•É¥…±}ÍÑ…Ñ•}É•˜I=4‘…¹Ñ”¹Í¡•‘Õ±•}ÕÉÉ•¹Ñ}Á±…•µ•¹Ð]!IÍ½Á•‘}½Ý¹•É}É•˜ô•Ìˆ°(€€€€€€€€€€€€¡Í¡•‘Õ±•}É•˜°¤°(€€€€€€€€¤¹™•Ñ¡½¹” ¤(€€€€€€€…ÍÍ•ÉÐÉ½Ü€ôô€¡Í¡•‘Õ±•}É•˜°€‰Í¡•‘Õ±”¹Á±…•µ•¹Ðˆ°ÍÑ…Ñ•}É•˜¤(€€€€€€€Ý¥Ñ ÁåÑ•ÍÐ¹É…¥Í•Ì¡ÁÍå½Áœ¹ÉÉ½È¤…Ì•á}¥¹™¼è(€€€€€€€€€€€½¹¹•Ñ¥½¸¹•á•ÕÑ” (€€€€€€€€€€€€€€€€‰UAQ‘…¹Ñ”¹Í¡•‘Õ±•}ÕÉÉ•¹Ñ}Á±…•µ•¹ÐMP™…•Ñ}½‘”ô…ÑÕ…°¹É•…±¥é…Ñ¥½¸œ]!IÍ½Á•‘}½Ý¹•É}É•˜ô•Ìˆ°(€€€€€€€€€€€€€€€€¡Í¡•‘Õ±•}É•˜°¤°(€€€€€€€€€€€€¤(€€€€€€€…ÍÍ•ÉÐ}ÍÅ±ÍÑ…Ñ”¡•á}¥¹™¼¹Ù…±Õ”¤€ôô€ˆÐÐÀÀÀˆ(€€€€€€€½¹¹•Ñ¥½¸¹É½±±‰…¬ ¤(()‘•˜Ñ•ÍÑ}´Õ}ÕÉÉ•¹Ñ}¡¥ÍÑ½Éå}¥Í}½¹•}Ý…å}…¹‘}•ÅÕ¥Ù…±•¹Ñ}Ñ½}ÕÉÉ•¹Ñ}‰¥¹‘¥¹œ (€€€ÁÉ½Ù¥Í¥½¹•‘}‘…Ñ…‰…Í”è¹ä°(€€€…±•µ‰¥}½¹™¥œè½¹™¥œ°(¤€´ø9½¹”è(€€€‘…Ñ…‰…Í”€ô}ÕÁÉ…‘•}´Ô¡ÁÉ½Ù¥Í¥½¹•‘}‘…Ñ…‰…Í”°…±•µ‰¥}½¹™¥œ¤(€€€Ý¥Ñ }½Ý¹•É}½¹¹•Ñ¥½¸¡‘…Ñ…‰…Í”¤…Ì½¹¹•Ñ¥½¸è(€€€€€€€Í¡•‘Õ±•}É•˜°|°ÍÑ…ÉÑ•€ô}µ…­•}Ù…±¥‘}Í¡•‘Õ±”¡½¹¹•Ñ¥½¸¤(€€€€€€€½¹¹•Ñ¥½¸¹•á•ÕÑ” (€€€€€€€€€€€€‰1QI=4‘…¹Ñ”¹Í¡•‘Õ±•}ÕÉÉ•¹Ñ}Á±…•µ•¹Ð]!IÍ½Á•‘}½Ý¹•É}É•˜ô•Ìˆ°(€€€€€€€€€€€€¡Í¡•‘Õ±•}É•˜°¤°(€€€€€€€€¤(€€€€€€€±½Í•‘}…Ð€ôÍÑ…ÉÑ•€¬Ñ¥µ•‘•±Ñ„¡µ¥¹ÕÑ•ÌôÄ¤(€€€€€€€½¹¹•Ñ¥½¸¹•á•ÕÑ” (€€€€€€€€€€€€‰UAQ‘…¹Ñ”¹Í¡•‘Õ±•}Á±…•µ•¹Ñ}ÕÉÉ•¹Ñ}¡¥ÍÑ½ÉäMPÕÉÉ•¹Ñ}Õ¹Ñ¥±}…Ðô•Ì€ˆ(€€€€€€€€€€€€‰]!IÍ¡•‘Õ±•}É•˜ô•Ì9ÕÉÉ•¹Ñ}™É½µ}…Ðô•Ìˆ°(€€€€€€€€€€€€¡±½Í•‘}…Ð°Í¡•‘Õ±•}É•˜°ÍÑ…ÉÑ•¤°(€€€€€€€€¤(€€€€€€€½¹¹•Ñ¥½¸¹•á•ÕÑ” ‰MP=9MQI%9QL10%55%Qˆ¤(€€€€€€€½¹¹•Ñ¥½¸¹•á•ÕÑ” ‰MP=9MQI%9QL10IIˆ¤(€€€€€€€½¹¹•Ñ¥½¸¹•á•ÕÑ” (€€€€€€€€€€€€‰UAQ‘…¹Ñ”¹Í¡•‘Õ±•}Á±…•µ•¹Ñ}ÕÉÉ•¹Ñ}¡¥ÍÑ½ÉäMPÕÉÉ•¹Ñ}Õ¹Ñ¥±}…Ðõ9U10€ˆ(€€€€€€€€€€€€‰]!IÍ¡•‘Õ±•}É•˜ô•Ì9ÕÉÉ•¹Ñ}™É½µ}…Ðô•Ìˆ°(€€€€€€€€€€€€¡Í¡•‘Õ±•}É•˜°ÍÑ…ÉÑ•¤°(€€€€€€€€¤(€€€€€€€Ý¥Ñ ÁåÑ•ÍÐ¹É…¥Í•Ì¡•ÉÉ½ÉÌ¹¡•­Y¥½±…Ñ¥½¸¤…Ì•á}¥¹™¼è(€€€€€€€€€€€½¹¹•Ñ¥½¸¹•á•ÕÑ” ‰MP=9MQI%9QL10%55%Qˆ¤(€€€€€€€…ÍÍ•ÉÐ}ÍÅ±ÍÑ…Ñ”¡•á}¥¹™¼¹Ù…±Õ”¤€ôô€ˆÈÌÔÄÐˆ(€€€€€€€½¹¹•Ñ¥½¸¹É½±±‰…¬ ¤(()‘•˜Ñ•ÍÑ}´Õ}Í•ÍÍ¥½¹}Á…ÕÍ•}•½µ•ÑÉå}¥Í}½µµ¥Ñ}¡•­• (€€€ÁÉ½Ù¥Í¥½¹•‘}‘…Ñ…‰…Í”è¹ä°(€€€…±•µ‰¥}½¹™¥œè½¹™¥œ°(¤€´ø9½¹”è(€€€‘…Ñ…‰…Í”€ô}ÕÁÉ…‘•}´Ô¡ÁÉ½Ù¥Í¥½¹•‘}‘…Ñ…‰…Í”°…±•µ‰¥}½¹™¥œ¤(€€€¹½Ü€ô‘…Ñ•Ñ¥µ”¹¹½Ü¡UQ¤¹É•Á±…”¡µ¥É½Í•½¹ôÀ¤(€€€Í•ÍÍ¥½¹}É•˜°ÍÑ…Ñ•}É•˜€ôÕÕ¥Ü ¤°ÕÕ¥Ü ¤(€€€Ý¥Ñ }½Ý¹•É}½¹¹•Ñ¥½¸¡‘…Ñ…‰…Í”¤…Ì½¹¹•Ñ¥½¸è(€€€€€€€½¹¹•Ñ¥½¸¹•á•ÕÑ” ‰%9MIP%9Q<‘…¹Ñ”¹Í•ÍÍ¥½¸¡Í•ÍÍ¥½¹}É•˜¤Y1UL€ •Ì¤ˆ°€¡Í•ÍÍ¥½¹}É•˜°¤¤(€€€€€€€½¹¹•Ñ¥½¸¹•á•ÕÑ” ‰%9MIP%9Q<‘…¹Ñ”¹¹…Ñ¥Ù•}…‘‘É•ÍÌ¡¹…Ñ¥Ù•}É•˜±½Ý¹•É}™…µ¥±ä¤Y1UL€ •Ì°Í•ÍÍ¥½¸œ¤ˆ°€¡Í•ÍÍ¥½¹}É•˜°¤¤(€€€€€€€½¹¹•Ñ¥½¸¹•á•ÕÑ” (€€€€€€€€€€€€‰%9MIP%9Q<‘…¹Ñ”¹µ…Ñ•É¥…±}ÍÑ…Ñ•}…‘‘É•ÍÌ¡µ…Ñ•É¥…±}ÍÑ…Ñ•}É•˜±¹…Ñ¥Ù•}½Ý¹•É}É•˜±™…•Ñ}½‘”¤Y1UL€ •Ì°•Ì°Í•ÍÍ¥½¸¹Ñ¥µ¥¹œœ¤ˆ°(€€€€€€€€€€€€¡ÍÑ…Ñ•}É•˜°Í•ÍÍ¥½¹}É•˜¤°(€€€€€€€€¤(€€€€€€€½¹¹•Ñ¥½¸¹•á•ÕÑ” (€€€€€€€€€€€€‰%9MIP%9Q<‘…¹Ñ”¹Í•ÍÍ¥½¹}Ñ¥µ¥¹}ÍÑ…Ñ”¡µ…Ñ•É¥…±}ÍÑ…Ñ•}É•˜±Í•ÍÍ¥½¹}É•˜±Ñ¥µ¥¹}™½Éµ}½‘”¤Y1UL€ •Ì°•Ì°…‰Í½±ÕÑ”œ¤ˆ°(€€€€€€€€€€€€¡ÍÑ…Ñ•}É•˜°Í•ÍÍ¥½¹}É•˜¤°(€€€€€€€€¤(€€€€€€€½¹¹•Ñ¥½¸¹•á•ÕÑ” (€€€€€€€€€€€€‰%9MIP%9Q<‘…¹Ñ”¹Í•ÍÍ¥½¹}Ñ¥µ¥¹}…‰Í½±ÕÑ”¡µ…Ñ•É¥…±}ÍÑ…Ñ•}É•˜±ÍÑ…ÉÑ•‘}…Ð±ÍÑ…ÉÑ}ÁÉ•¥Í¥½¹}½‘”±•¹‘•‘}…Ð±•¹‘}ÁÉ•¥Í¥½¹}½‘”¤€ˆ(€€€€€€€€€€€€‰Y1UL€ •Ì°•Ì°•á…Ðœ°•Ì°•á…Ðœ¤ˆ°(€€€€€€€€€€€€¡ÍÑ…Ñ•}É•˜°¹½Ü°¹½Ü€¬Ñ¥µ•‘•±Ñ„¡¡½ÕÉÌôÄ¤¤°(€€€€€€€€¤(€€€€€€€½¹¹•Ñ¥½¸¹•á•ÕÑ” ‰%9MIP%9Q<‘…¹Ñ”¹Í•ÍÍ¥½¹}ÕÉÉ•¹Ñ}Ñ¥µ¥¹œ¡¹…Ñ¥Ù•}½Ý¹•É}É•˜±µ…Ñ•É¥…±}ÍÑ…Ñ•}É•˜¤Y1UL€ •Ì°•Ì¤ˆ°€¡Í•ÍÍ¥½¹}É•˜°ÍÑ…Ñ•}É•˜¤¤(€€€€€€€½¹¹•Ñ¥½¸¹•á•ÕÑ” (€€€€€€€€€€€€‰%9MIP%9Q<‘…¹Ñ”¹Í•ÍÍ¥½¹}Ñ¥µ¥¹}ÕÉÉ•¹Ñ}¡¥ÍÑ½Éä¡Í•ÍÍ¥½¹}É•˜±µ…Ñ•É¥…±}ÍÑ…Ñ•}É•˜±ÕÉÉ•¹Ñ}™É½µ}…Ð¤Y1UL€ •Ì°•Ì°•Ì¤ˆ°(€€€€€€€€€€€€¡Í•ÍÍ¥½¹}É•˜°ÍÑ…Ñ•}É•˜°¹½Ü¤°(€€€€€€€€¤(€€€€€€€½¹¹•Ñ¥½¸¹•á•ÕÑ” (€€€€€€€€€€€€‰%9MIP%9Q<‘…¹Ñ”¹Í•ÍÍ¥½¹}Ñ¥µ¥¹}Á…ÕÍ”¡µ…Ñ•É¥…±}ÍÑ…Ñ•}É•˜±Á…ÕÍ•‘}…Ð±Á…ÕÍ•}ÁÉ•¥Í¥½¹}½‘”±É•ÍÕµ•‘}…Ð±É•ÍÕµ•}ÁÉ•¥Í¥½¹}½‘”¤€ˆ(€€€€€€€€€€€€‰Y1UL€ •Ì°•Ì°•á…Ðœ°•Ì°•á…Ðœ¤ˆ°(€€€€€€€€€€€€¡ÍÑ…Ñ•}É•˜°¹½Ü€´Ñ¥µ•‘•±Ñ„¡µ¥¹ÕÑ•ÌôÄ¤°¹½Ü€¬Ñ¥µ•‘•±Ñ„¡µ¥¹ÕÑ•ÌôÄ¤¤°(€€€€€€€€¤(€€€€€€€Ý¥Ñ ÁåÑ•ÍÐ¹É…¥Í•Ì¡•ÉÉ½ÉÌ¹¡•­Y¥½±…Ñ¥½¸¤…Ì•á}¥¹™¼è(€€€€€€€€€€€½¹¹•Ñ¥½¸¹•á•ÕÑ” ‰MP=9MQI%9QL10%55%Qˆ¤(€€€€€€€…ÍÍ•ÉÐ}ÍÅ±ÍÑ…Ñ”¡•á}¥¹™¼¹Ù…±Õ”¤€ôô€ˆÈÌÔÄÐˆ(€€€€€€€½¹¹•Ñ¥½¸¹É½±±‰…¬ ¤(()‘•˜Ñ•ÍÑ}´Õ}É•ÕÉÉ•¹•}…É•…Ñ•}•¹™½É•Í}Á…ÉÐÄÝ}…¹¡½É}µ…ÑÉ¥à (€€€ÁÉ½Ù¥Í¥½¹•‘}‘…Ñ…‰…Í”è¹ä°(€€€…±•µ‰¥}½¹™¥œè½¹™¥œ°(¤€´ø9½¹”è(€€€‘…Ñ…‰…Í”€ô}ÕÁÉ…‘•}´Ô¡ÁÉ½Ù¥Í¥½¹•‘}‘…Ñ…‰…Í”°…±•µ‰¥}½¹™¥œ¤(€€€Ý¥Ñ }½Ý¹•É}½¹¹•Ñ¥½¸¡‘…Ñ…‰…Í”¤…Ì½¹¹•Ñ¥½¸è(€€€€€€€|°ÍÑ…Ñ•}É•˜°|€ô}µ…­•}Ù…±¥‘}É½ÕÑ¥¹•}É•ÕÉÉ•¹”¡½¹¹•Ñ¥½¸¤(€€€€€€€½¹¹•Ñ¥½¸¹•á•ÕÑ” (€€€€€€€€€€€€‰%9MIP%9Q<‘…¹Ñ”¹É½ÕÑ¥¹•}É•ÕÉÉ•¹•}‰½Õ¹‘…Éå}ÍÑ…Ñ”ˆ(€€€€€€€€€€€€ˆ¡µ…Ñ•É¥…±}ÍÑ…Ñ•}É•˜±‰½Õ¹‘…Éå}É½±”±‰½Õ¹‘…Éå}­¥¹±‘…Ñ•}Ù…±Õ”¤Y1UL€ •Ì°Á…ÑÑ•É¹}…¹¡½Èœ°‘…Ñ”œ±‘…Ñ”€œÈÀÈØ´ÀÄ´ÀÄœ¤ˆ°(€€€€€€€€€€€€¡ÍÑ…Ñ•}É•˜°¤°(€€€€€€€€¤(€€€€€€€Ý¥Ñ ÁåÑ•ÍÐ¹É…¥Í•Ì¡•ÉÉ½ÉÌ¹¡•­Y¥½±…Ñ¥½¸¤…Ì•á}¥¹™¼è(€€€€€€€€€€€½¹¹•Ñ¥½¸¹•á•ÕÑ” ‰MP=9MQI%9QL10%55%Qˆ¤(€€€€€€€…ÍÍ•ÉÐ}ÍÅ±ÍÑ…Ñ”¡•á}¥¹™¼¹Ù…±Õ”¤€ôô€ˆÈÌÔÄÐˆ(€€€€€€€½¹¹•Ñ¥½¸¹É½±±‰…¬ ¤(()‘•˜Ñ•ÍÑ}´Õ}¥…¹…}é½¹•}Ù…±¥‘…Ñ½É}É•©•ÑÍ}Õ¹­¹½Ý¹}é½¹” (€€€ÁÉ½Ù¥Í¥½¹•‘}‘…Ñ…‰…Í”è¹ä°(€€€…±•µ‰¥}½¹™¥œè½¹™¥œ°(¤€´ø9½¹”è(€€€‘…Ñ…‰…Í”€ô}ÕÁÉ…‘•}´Ô¡ÁÉ½Ù¥Í¥½¹•‘}‘…Ñ…‰…Í”°…±•µ‰¥}½¹™¥œ¤(€€€Ý¥Ñ }½Ý¹•É}½¹¹•Ñ¥½¸¡‘…Ñ…‰…Í”°…ÕÑ½½µµ¥ÐõQÉÕ”¤…Ì½¹¹•Ñ¥½¸è(€€€€€€€Ý¥Ñ ÁåÑ•ÍÐ¹É…¥Í•Ì¡•ÉÉ½ÉÌ¹%¹Ù…±¥‘A…É…µ•Ñ•ÉY…±Õ”¤…Ì•á}¥¹™¼è(€€€€€€€€€€€½¹¹•Ñ¥½¸¹•á•ÕÑ” (€€€€€€€€€€€€€€€€‰%9MIP%9Q<‘…¹Ñ”¹Í¡•‘Õ±•}Á±…•µ•¹Ñ}¹…µ•‘}é½¹•}ÍÑ…Ñ”ˆ(€€€€€€€€€€€€€€€€ˆ¡µ…Ñ•É¥…±}ÍÑ…Ñ•}É•˜±•áÑ•¹Ñ}½‘”±ÍÑ…ÉÑÍ}±½…±}…Ð±é½¹•}¥¤€ˆ(€€€€€€€€€€€€€€€€‰Y1UL€ •Ì°Á½¥¹Ðœ±Ñ¥µ•ÍÑ…µÀ€œÈÀÈØ´ÀÄ´ÀÄ€ÄÈèÀÀœ°ÑŒ½•™¥¹¥Ñ•±å}9½Ñ}}i½¹”œ¤ˆ°(€€€€€€€€€€€€€€€€¡ÕÕ¥Ü ¤°¤°(€€€€€€€€€€€€¤(€€€€€€€€Œ	=IÑÉ¥•ÈµÕÍÐÉ•©•ÐÑ¡”Õ¹­¹½Ý¸%9¥‘•¹Ñ¥™¥•È‰•™½É”,•Ù…±Õ…Ñ¥½¸¸(€€€€€€€…ÍÍ•ÉÐ}ÍÅ±ÍÑ…Ñ”¡•á}¥¹™¼¹Ù…±Õ”¤€ôô€ˆÈÈÀÈÌˆ(()‘•˜Ñ•ÍÑ}´Õ}‘½Ý¹É…‘•}É•ÑÕÉ¹Í}•á…Ñ±å}Ñ½}´Ñ}ÍÕÉ™…” (€€€ÁÉ½Ù¥Í¥½¹•‘}‘…Ñ…‰…Í”è¹ä°(€€€…±•µ‰¥}½¹™¥œè½¹™¥œ°(¤€´ø9½¹”è(€€€½µµ…¹¹ÕÁÉ…‘”¡…±•µ‰¥}½¹™¥œ°}4Õ}IY%M%=8¤(€€€½µµ…¹¹‘½Ý¹É…‘”¡…±•µ‰¥}½¹™¥œ°}4Ñ}IY%M%=8¤(€€€Ý¥Ñ }…‘µ¥¹}½¹¹•Ñ¥½¸¡ÁÉ½Ù¥Í¥½¹•‘}‘…Ñ…‰…Í”¤…Ì½¹¹•Ñ¥½¸è(€€€€€€€Ù¥•ÝÌ€ô±¥ÍÐ¡½¹¹•Ñ¥½¸¹•á•ÕÑ” ‰M1P€ÄI=4Á}Ù¥•ÝÌ]!IÍ¡•µ…¹…µ”ô‘…¹Ñ”œˆ¤¤(€€€€€€€É½ÕÑ¥¹•Ì€ô±¥ÍÐ¡½¹¹•Ñ¥½¸¹•á•ÕÑ” (€€€€€€€€€€€€‰M1P€ÄI=4Á}ÁÉ½ŒÀ)=%8Á}¹…µ•ÍÁ…”¸=8¸¹½¥õÀ¹ÁÉ½¹…µ•ÍÁ…”]!I¸¹¹ÍÁ¹…µ”ô‘…¹Ñ”œˆ(€€€€€€€€¤¤(€€€€€€€ÑÉ¥•ÉÌ€ô±¥ÍÐ¡½¹¹•Ñ¥½¸¹•á•ÕÑ” (€€€€€€€€€€€€‰M1P€ÄI=4Á}ÑÉ¥•ÈÐ)=%8Á}±…ÍÌŒ=8Œ¹½¥õÐ¹ÑÉ•±¥)=%8Á}¹…µ•ÍÁ…”¸=8¸¹½¥õŒ¹É•±¹…µ•ÍÁ…”]!I¸¹¹ÍÁ¹…µ”ô‘…¹Ñ”œ99=PÐ¹Ñ¥Í¥¹Ñ•É¹…°ˆ(€€€€€€€€¤¤(€€€€€€€•¹‘}‘•˜€ô½¹¹•Ñ¥½¸¹•á•ÕÑ” (€€€€€€€€€€€€‰M1PÁ}•Ñ}½¹ÍÑÉ…¥¹Ñ‘•˜¡½¥±ÑÉÕ”¤I=4Á}½¹ÍÑÉ…¥¹Ð]!I½¹¹…µ”ô­}Í•ÍÍ¥½¹}Ñ¥µ¥¹}…‰Í½±ÕÑ•}•¹‘}ÁÉ•¥Í¥½¸œˆ(€€€€€€€€¤¹™•Ñ¡½¹” ¤(€€€…ÍÍ•ÉÐÙ¥•ÝÌ€ôôÉ½ÕÑ¥¹•Ì€ôôÑÉ¥•ÉÌ€ôômt(€€€…ÍÍ•ÉÐ•¹‘}‘•˜¥Ì¹½Ð9½¹”…¹€‰•¹‘}ÁÉ•¥Í¥½¹}½‘”%L9=P9U10ˆ¹½Ð¥¸ÍÑÈ¡•¹‘}‘•™lÁt¤(