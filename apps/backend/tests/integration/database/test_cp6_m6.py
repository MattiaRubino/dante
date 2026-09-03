"""Real PostgreSQL acceptance tests for CP6-M06 Occurrence generation."""

from __future__ import annotations

import json
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any, cast
from uuid import UUID, uuid7

import psycopg
import pytest
from alembic import command
from alembic.config import Config
from psycopg import errors
from sqlalchemy import Table

from dante.platform.database.mappings import MAPPED_TABLES
from dante.platform.database.mappings.views import VIEW_METADATA
from dante.platform.database.metadata import Base

pytestmark = pytest.mark.postgres

_M5_REVISION = "20260825_05"
_M6_REVISION = "20260826_06"
_M6_TABLES = {
    "occurrence_generation",
    "occurrence_generation_calendar",
    "occurrence_generation_elapsed",
    "occurrence_generation_quota",
    "occurrence_generation_cyclic",
}
_POST_CP6_TABLES = {
    "account",
    "email_identity",
    "password_credential",
    "auth_session",
    "password_signup_challenge",
    "password_recovery_challenge",
    "account_profile_bootstrap",
    "apple_auth_grant",
    "external_auth_transaction",
    "external_identity",
    "external_link_challenge",
    "external_signup_challenge",
    "passkey_credential",
    "webauthn_account",
    "webauthn_challenge",
    "email_delivery_intent",
    "email_delivery_attempt",
    "email_provider_event",
    "email_recipient_suppression",
}
_M6_ROUTINE = "enforce_occurrence_generation_integrity"
_VIEWS = {
    "schedule_current_placement",
    "actual_current_realization",
    "session_current_timing",
    "routine_current_recurrence",
    "event_current_recurrence",
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


def _upgrade_m6(database: Any, alembic_config: Config) -> Any:
    command.upgrade(alembic_config, _M6_REVISION)
    return database


def _create_elapsed_routine(
    connection: psycopg.Connection[Any], *, elapsed_seconds: str = "60.000000"
) -> tuple[UUID, UUID, datetime]:
    routine_ref = uuid7()
    state_ref = uuid7()
    anchor = datetime(2026, 1, 1, 12, 0, tzinfo=UTC)
    current_from = datetime(2026, 1, 1, 11, 0, tzinfo=UTC)
    connection.execute("INSERT INTO dante.routine(routine_ref) VALUES (%s)", (routine_ref,))
    connection.execute(
        "INSERT INTO dante.native_address(native_ref,owner_family) VALUES (%s,'routine')",
        (routine_ref,),
    )
    connection.execute(
        "INSERT INTO dante.material_state_address(material_state_ref,native_owner_ref,facet_code) VALUES (%s,%s,'routine.recurrence')",
        (state_ref, routine_ref),
    )
    connection.execute(
        "INSERT INTO dante.routine_recurrence_state(material_state_ref,routine_ref,family_code,range_kind) VALUES (%s,%s,'elapsed_interval','open')",
        (state_ref, routine_ref),
    )
    connection.execute(
        "INSERT INTO dante.routine_recurrence_elapsed_state(material_state_ref,elapsed_seconds,anchor_mode_code,anchor_at) VALUES (%s,%s,'fixed_anchor',%s)",
        (state_ref, elapsed_seconds, anchor),
    )
    connection.execute(
        "INSERT INTO dante.routine_recurrence_current_history(routine_ref,material_state_ref,current_from_at) VALUES (%s,%s,%s)",
        (routine_ref, state_ref, current_from),
    )
    connection.execute(
        "INSERT INTO dante.native_current_material_state(native_owner_ref,facet_code,material_state_ref) VALUES (%s,'routine.recurrence',%s)",
        (routine_ref, state_ref),
    )
    return routine_ref, state_ref, anchor


def _insert_elapsed_occurrence(
    connection: psycopg.Connection[Any],
    *,
    routine_ref: UUID,
    state_ref: UUID,
    expected_at: datetime,
) -> UUID:
    occurrence_ref = uuid7()
    connection.execute(
        "INSERT INTO dante.occurrence(occurrence_ref) VALUES (%s)", (occurrence_ref,)
    )
    connection.execute(
        "INSERT INTO dante.occurrence_generation(occurrence_ref,source_native_ref,governing_recurrence_state_ref,origin_code) VALUES (%s,%s,%s,'recurrence_generated')",
        (occurrence_ref, routine_ref, state_ref),
    )
    connection.execute(
        "INSERT INTO dante.occurrence_generation_elapsed(occurrence_ref,expected_at) VALUES (%s,%s)",
        (occurrence_ref, expected_at),
    )
    return occurrence_ref


def test_m6_materializes_exact_final_structural_topology(
    provisioned_database: Any, alembic_config: Config
) -> None:
    database = _upgrade_m6(provisioned_database, alembic_config)
    with _admin_connection(database) as connection:
        table_count = connection.execute(
            "SELECT count(*) FROM pg_tables WHERE schemaname='dante' AND tablename<>'alembic_version'"
        ).fetchone()
        views = {
            str(row[0])
            for row in connection.execute("SELECT viewname FROM pg_views WHERE schemaname='dante'")
        }
        routines = list(
            connection.execute("""
            SELECT p.proname,p.prosecdef,p.provolatile,p.proparallel,p.proleakproof,
                   pg_get_userbyid(p.proowner),p.proconfig,
                   has_function_privilege('dante_runtime',p.oid,'EXECUTE'),
                   has_function_privilege('dante_migrator',p.oid,'EXECUTE'),
                   EXISTS (SELECT 1 FROM aclexplode(coalesce(p.proacl,acldefault('f',p.proowner))) acl WHERE acl.grantee=0 AND acl.privilege_type='EXECUTE')
            FROM pg_proc p JOIN pg_namespace n ON n.oid=p.pronamespace
            WHERE n.nspname='dante' ORDER BY p.proname
        """)
        )
        triggers = list(
            connection.execute("""
            SELECT t.tgname,t.tgconstraint<>0,con.condeferrable,con.condeferred
            FROM pg_trigger t JOIN pg_class c ON c.oid=t.tgrelid JOIN pg_namespace n ON n.oid=c.relnamespace
            LEFT JOIN pg_constraint con ON con.oid=t.tgconstraint
            WHERE n.nspname='dante' AND NOT t.tgisinternal ORDER BY t.tgname
        """)
        )
        index_count = connection.execute(
            "SELECT count(*) FROM pg_indexes WHERE schemaname='dante' AND tablename<>'alembic_version'"
        ).fetchone()
        constraint_counts = dict(
            connection.execute("""
            SELECT con.contype,count(*) FROM pg_constraint con
            JOIN pg_class c ON c.oid=con.conrelid JOIN pg_namespace n ON n.oid=c.relnamespace
            WHERE n.nspname='dante' AND c.relname<>'alembic_version' AND con.contype IN ('c','f','u')
            GROUP BY con.contype
        """)
        )
    assert table_count == (68,)
    assert views == _VIEWS
    assert len(routines) == 14
    assert {str(row[0]) for row in routines} >= {_M6_ROUTINE}
    for row in routines:
        (
            _,
            prosecdef,
            volatility,
            parallel,
            leakproof,
            owner,
            config,
            runtime_x,
            migrator_x,
            public_x,
        ) = row
        assert prosecdef is False
        assert volatility == "v"
        assert parallel == "u"
        assert leakproof is False
        assert owner == "dante_owner"
        assert config == ["search_path=pg_catalog, dante, pg_temp"]
        assert (runtime_x, migrator_x, public_x) == (False, False, False)
    assert len(triggers) == 75
    assert sum(not bool(row[1]) for row in triggers) == 18
    assert sum(bool(row[1]) for row in triggers) == 57
    assert all((not row[1]) or (row[2] and row[3]) for row in triggers)
    assert index_count == (95,)
    assert constraint_counts == {"c": 120, "f": 68, "u": 2}


def test_m6_sqlalchemy_mapping_is_exact_and_relationship_free() -> None:
    cp6_tables = tuple(table for table in MAPPED_TABLES if table.name not in _POST_CP6_TABLES)
    cp6_mappers = tuple(
        mapper
        for mapper in Base.registry.mappers
        if cast(Table, mapper.local_table).name not in _POST_CP6_TABLES
    )
    assert len(cp6_tables) == 68
    assert len(cp6_mappers) == 68
    assert {table.name for table in cp6_tables} >= _M6_TABLES
    assert all(len(mapper.relationships) == 0 for mapper in cp6_mappers)
    assert set(VIEW_METADATA.tables) == {f"dante.{name}" for name in _VIEWS}


def test_m6_runtime_business_acl_remains_deny_by_default(
    provisioned_database: Any, alembic_config: Config
) -> None:
    database = _upgrade_m6(provisioned_database, alembic_config)
    with _admin_connection(database) as connection:
        rows = list(
            connection.execute(
                """
            SELECT c.relname,
                   has_table_privilege('dante_runtime',c.oid,'SELECT'),
                   has_table_privilege('dante_runtime',c.oid,'INSERT'),
                   has_table_privilege('dante_runtime',c.oid,'UPDATE'),
                   has_table_privilege('dante_runtime',c.oid,'DELETE')
            FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace
            WHERE n.nspname='dante' AND c.relname = ANY(%s)
            ORDER BY c.relname
        """,
                (sorted(_M6_TABLES),),
            )
        )
    assert len(rows) == 5
    assert all(tuple(row[1:]) == (False, False, False, False) for row in rows)


def test_m6_native_ref_rejects_non_routine_event_source(
    provisioned_database: Any,
    alembic_config: Config,
) -> None:
    database = _upgrade_m6(provisioned_database, alembic_config)
    person_ref = uuid7()
    occurrence_ref = uuid7()

    def insert_invalid_source(connection: psycopg.Connection[Any]) -> None:
        with connection.transaction():
            connection.execute(
                "INSERT INTO dante.person(person_ref) VALUES (%s)",
                (person_ref,),
            )
            connection.execute(
                "INSERT INTO dante.native_address(native_ref,owner_family) VALUES (%s,'person')",
                (person_ref,),
            )
            connection.execute(
                "INSERT INTO dante.occurrence(occurrence_ref) VALUES (%s)",
                (occurrence_ref,),
            )
            connection.execute(
                "INSERT INTO dante.occurrence_generation"
                "(occurrence_ref,source_native_ref,origin_code) "
                "VALUES (%s,%s,'explicit_extra')",
                (occurrence_ref, person_ref),
            )

    with (
        _owner_connection(database) as connection,
        pytest.raises(errors.ForeignKeyViolation) as exc_info,
    ):
        insert_invalid_source(connection)
    assert exc_info.value.sqlstate == "23503"


def test_m6_explicit_extra_requires_zero_generated_coordinates(
    provisioned_database: Any,
    alembic_config: Config,
) -> None:
    database = _upgrade_m6(provisioned_database, alembic_config)
    with _owner_connection(database) as connection:
        with connection.transaction():
            routine_ref, _, _ = _create_elapsed_routine(connection)
        occurrence_ref = uuid7()

        def insert_invalid_coordinate() -> None:
            with connection.transaction():
                connection.execute(
                    "INSERT INTO dante.occurrence(occurrence_ref) VALUES (%s)",
                    (occurrence_ref,),
                )
                connection.execute(
                    "INSERT INTO dante.occurrence_generation"
                    "(occurrence_ref,source_native_ref,origin_code) "
                    "VALUES (%s,%s,'explicit_extra')",
                    (occurrence_ref, routine_ref),
                )
                connection.execute(
                    "INSERT INTO dante.occurrence_generation_elapsed"
                    "(occurrence_ref,expected_at) "
                    "VALUES (%s,timestamptz '2026-01-01 12:01:00+00')",
                    (occurrence_ref,),
                )

        with pytest.raises(errors.CheckViolation) as exc_info:
            insert_invalid_coordinate()
    assert exc_info.value.sqlstate == "23514"


def test_m6_elapsed_generated_coordinate_requires_exact_governing_lattice(
    provisioned_database: Any, alembic_config: Config
) -> None:
    database = _upgrade_m6(provisioned_database, alembic_config)
    with _owner_connection(database) as connection:
        with connection.transaction():
            routine_ref, state_ref, anchor = _create_elapsed_routine(connection)
        with connection.transaction():
            _insert_elapsed_occurrence(
                connection,
                routine_ref=routine_ref,
                state_ref=state_ref,
                expected_at=anchor + timedelta(seconds=60),
            )
        with pytest.raises(errors.CheckViolation) as exc_info, connection.transaction():
            _insert_elapsed_occurrence(
                connection,
                routine_ref=routine_ref,
                state_ref=state_ref,
                expected_at=anchor + timedelta(seconds=61),
            )
    assert exc_info.value.sqlstate == "23514"


def test_m6_non_quota_duplicate_generation_identity_is_rejected(
    provisioned_database: Any, alembic_config: Config
) -> None:
    database = _upgrade_m6(provisioned_database, alembic_config)
    with _owner_connection(database) as connection:
        with connection.transaction():
            routine_ref, state_ref, anchor = _create_elapsed_routine(connection)
        expected_at = anchor + timedelta(seconds=60)
        with connection.transaction():
            _insert_elapsed_occurrence(
                connection, routine_ref=routine_ref, state_ref=state_ref, expected_at=expected_at
            )
        with pytest.raises(errors.CheckViolation) as exc_info, connection.transaction():
            _insert_elapsed_occurrence(
                connection,
                routine_ref=routine_ref,
                state_ref=state_ref,
                expected_at=expected_at,
            )
    assert exc_info.value.sqlstate == "23514"


def test_m6_occurrence_generation_routine_has_no_dynamic_execute(
    provisioned_database: Any, alembic_config: Config
) -> None:
    database = _upgrade_m6(provisioned_database, alembic_config)
    with _admin_connection(database) as connection:
        definition = connection.execute("""
            SELECT pg_get_functiondef(p.oid) FROM pg_proc p JOIN pg_namespace n ON n.oid=p.pronamespace
            WHERE n.nspname='dante' AND p.proname='enforce_occurrence_generation_integrity'
        """).fetchone()
    assert definition is not None
    assert "EXECUTE " not in str(definition[0]).upper()


def test_m6_downgrade_returns_exactly_to_m5_surface(
    provisioned_database: Any, alembic_config: Config
) -> None:
    command.upgrade(alembic_config, _M6_REVISION)
    command.downgrade(alembic_config, _M5_REVISION)
    with _admin_connection(provisioned_database) as connection:
        table_count = connection.execute(
            "SELECT count(*) FROM pg_tables WHERE schemaname='dante' AND tablename<>'alembic_version'"
        ).fetchone()
        routine_count = connection.execute(
            "SELECT count(*) FROM pg_proc p JOIN pg_namespace n ON n.oid=p.pronamespace WHERE n.nspname='dante'"
        ).fetchone()
        trigger_count = connection.execute(
            "SELECT count(*) FROM pg_trigger t JOIN pg_class c ON c.oid=t.tgrelid JOIN pg_namespace n ON n.oid=c.relnamespace WHERE n.nspname='dante' AND NOT t.tgisinternal"
        ).fetchone()
        index_count = connection.execute(
            "SELECT count(*) FROM pg_indexes WHERE schemaname='dante' AND tablename<>'alembic_version'"
        ).fetchone()
        constraints = dict(
            connection.execute("""
            SELECT con.contype,count(*) FROM pg_constraint con JOIN pg_class c ON c.oid=con.conrelid JOIN pg_namespace n ON n.oid=c.relnamespace
            WHERE n.nspname='dante' AND c.relname<>'alembic_version' AND con.contype IN ('c','f','u') GROUP BY con.contype
        """)
        )
    assert table_count == (63,)
    assert routine_count == (13,)
    assert trigger_count == (66,)
    assert index_count == (87,)
    assert constraints == {"c": 109, "f": 61, "u": 2}


def test_m6_dictionary_reconciles_final_structural_surface() -> None:
    table_entries = {
        path.stem: json.loads(path.read_text(encoding="utf-8"))
        for path in (_DICTIONARY_ROOT / "tables").glob("*.json")
    }
    view_entries = {
        path.stem: json.loads(path.read_text(encoding="utf-8"))
        for path in (_DICTIONARY_ROOT / "views").glob("*.json")
    }
    routine_entries = {
        path.stem: json.loads(path.read_text(encoding="utf-8"))
        for path in (_DICTIONARY_ROOT / "routines").glob("*.json")
    }
    scope = json.loads((_DICTIONARY_ROOT / "scope.json").read_text(encoding="utf-8"))

    cp6_table_entries = {
        name: entry
        for name, entry in table_entries.items()
        if str(entry["implementation"]["introducing_stage"]).startswith("CP6-")
    }
    cp6_routine_entries = {
        name: entry
        for name, entry in routine_entries.items()
        if str(entry["implementation"]["introducing_stage"]).startswith("CP6-")
    }

    assert len(cp6_table_entries) == 68
    assert set(cp6_table_entries) >= _M6_TABLES
    assert set(view_entries) == _VIEWS
    assert len(cp6_routine_entries) == 14
    assert _M6_ROUTINE in cp6_routine_entries

    current = scope["current_materialization"]
    assert current["completed_stages"][:6] == [
        "CP6-M01",
        "CP6-M02",
        "CP6-M03",
        "CP6-M04",
        "CP6-M05",
        "CP6-M06",
    ]
    assert scope["expected_baseline"] == {
        "standalone_entries": {"tables": 68, "views": 5, "routines": 14, "total": 87},
        "embedded_objects": {"triggers": 75, "physical_indexes": 95},
        "constraints": {"foreign_keys": 68, "check_constraints": 120},
    }

    triggers = [
        trigger
        for entry in cp6_table_entries.values()
        for trigger in entry["structure"]["triggers"]
    ]
    assert len(triggers) == 75
    assert len({trigger["name"] for trigger in triggers}) == 75
    assert sum(not trigger["constraint_trigger"] for trigger in triggers) == 18
    assert sum(trigger["constraint_trigger"] for trigger in triggers) == 57
    m6_routine = cp6_routine_entries[_M6_ROUTINE]["structure"]["routine"]
    assert m6_routine == {
        "routine_kind": "function",
        "language": "plpgsql",
        "argument_types": [],
        "return_type": "trigger",
        "security": "INVOKER",
        "volatility": "VOLATILE",
        "parallel_safety": "UNSAFE",
        "leakproof": False,
        "function_search_path": ["pg_catalog", "dante", "pg_temp"],
        "direct_runtime_execute": False,
    }
