"""Real PostgreSQL acceptance tests for CP6-M07 runtime ACL activation."""

from __future__ import annotations

from datetime import UTC, date, datetime, timedelta
from typing import Any
from uuid import UUID, uuid7

import psycopg
import pytest
from alembic import command
from alembic.config import Config
from psycopg import errors

from dante.platform.database.locking import (
    advisory_lock_key,
    occurrence_generation_lock_keys,
)
from dante.platform.database.metadata import Base

pytestmark = pytest.mark.postgres

_M6_REVISION = "20260826_06"
_M7_REVISION = "20260826_07"

_NO_INSERT = {
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
    "observation",
    "native_current_material_state",
    "scoped_current_material_state",
}
_HISTORY_COLUMNS = {
    "schedule_placement_current_history": "schedule_ref",
    "actual_realization_current_history": "actual_ref",
    "session_timing_current_history": "session_ref",
    "routine_recurrence_current_history": "routine_ref",
    "event_recurrence_current_history": "event_ref",
}
_VIEW_ACL = {
    "schedule_current_placement": ("scoped_owner_ref", True),
    "actual_current_realization": ("scoped_owner_ref", True),
    "session_current_timing": ("native_owner_ref", False),
    "routine_current_recurrence": ("native_owner_ref", False),
    "event_current_recurrence": ("native_owner_ref", False),
}
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
    "enforce_occurrence_generation_integrity",
    "validate_iana_timezone",
}
_GOLDEN_REF = UUID("018f1f26-8b2e-7abc-8000-000000000001")


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


def _runtime_connection(database: Any) -> psycopg.Connection[Any]:
    return psycopg.connect(
        **database.connection_kwargs(
            "dante_runtime",
            database.cluster.runtime_password,
        ),
        autocommit=True,
    )


def _upgrade_m7(database: Any, alembic_config: Config) -> Any:
    command.upgrade(alembic_config, _M7_REVISION)
    return database


def _mapped_table_names() -> set[str]:
    post_cp6_tables = {
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
    return {
        table.name for table in Base.metadata.tables.values() if table.name not in post_cp6_tables
    }


def _create_two_elapsed_routine_states(
    connection: psycopg.Connection[Any],
) -> tuple[UUID, UUID, UUID, datetime]:
    routine_ref = uuid7()
    first_state = uuid7()
    second_state = uuid7()
    anchor = datetime(2026, 1, 1, 12, 0, tzinfo=UTC)
    current_from = datetime(2026, 1, 1, 11, 0, tzinfo=UTC)

    with connection.transaction():
        connection.execute("INSERT INTO dante.routine(routine_ref) VALUES (%s)", (routine_ref,))
        connection.execute(
            "INSERT INTO dante.native_address(native_ref,owner_family) VALUES (%s,'routine')",
            (routine_ref,),
        )
        for state_ref, seconds in ((first_state, "60.000000"), (second_state, "120.000000")):
            connection.execute(
                "INSERT INTO dante.material_state_address"
                "(material_state_ref,native_owner_ref,facet_code) "
                "VALUES (%s,%s,'routine.recurrence')",
                (state_ref, routine_ref),
            )
            connection.execute(
                "INSERT INTO dante.routine_recurrence_state"
                "(material_state_ref,routine_ref,family_code,range_kind) "
                "VALUES (%s,%s,'elapsed_interval','open')",
                (state_ref, routine_ref),
            )
            connection.execute(
                "INSERT INTO dante.routine_recurrence_elapsed_state"
                "(material_state_ref,elapsed_seconds,anchor_mode_code,anchor_at) "
                "VALUES (%s,%s,'fixed_anchor',%s)",
                (state_ref, seconds, anchor),
            )
        connection.execute(
            "INSERT INTO dante.routine_recurrence_current_history"
            "(routine_ref,material_state_ref,current_from_at) VALUES (%s,%s,%s)",
            (routine_ref, first_state, current_from),
        )
        connection.execute(
            "INSERT INTO dante.native_current_material_state"
            "(native_owner_ref,facet_code,material_state_ref) "
            "VALUES (%s,'routine.recurrence',%s)",
            (routine_ref, first_state),
        )
    return routine_ref, first_state, second_state, current_from


def _create_quota_routine(
    connection: psycopg.Connection[Any],
) -> tuple[UUID, UUID]:
    routine_ref = uuid7()
    state_ref = uuid7()
    current_from = datetime(2026, 1, 1, 0, 0, tzinfo=UTC)

    with connection.transaction():
        connection.execute("INSERT INTO dante.routine(routine_ref) VALUES (%s)", (routine_ref,))
        connection.execute(
            "INSERT INTO dante.native_address(native_ref,owner_family) VALUES (%s,'routine')",
            (routine_ref,),
        )
        connection.execute(
            "INSERT INTO dante.material_state_address"
            "(material_state_ref,native_owner_ref,facet_code) "
            "VALUES (%s,%s,'routine.recurrence')",
            (state_ref, routine_ref),
        )
        connection.execute(
            "INSERT INTO dante.routine_recurrence_state"
            "(material_state_ref,routine_ref,family_code,range_kind) "
            "VALUES (%s,%s,'quota_per_period','open')",
            (state_ref, routine_ref),
        )
        connection.execute(
            "INSERT INTO dante.routine_recurrence_quota_state"
            "(material_state_ref,quota_count,period_unit_code,period_span,frame_code,zone_id,week_start) "
            "VALUES (%s,1,'day',1,'floating_local',NULL,NULL)",
            (state_ref,),
        )
        connection.execute(
            "INSERT INTO dante.routine_recurrence_current_history"
            "(routine_ref,material_state_ref,current_from_at) VALUES (%s,%s,%s)",
            (routine_ref, state_ref, current_from),
        )
        connection.execute(
            "INSERT INTO dante.native_current_material_state"
            "(native_owner_ref,facet_code,material_state_ref) "
            "VALUES (%s,'routine.recurrence',%s)",
            (routine_ref, state_ref),
        )
    return routine_ref, state_ref


def _acquire_generation_locks(
    connection: psycopg.Connection[Any],
    routine_ref: UUID,
) -> None:
    for lock_key in occurrence_generation_lock_keys("routine", routine_ref):
        connection.execute(
            "SELECT pg_catalog.pg_advisory_xact_lock(%s)",
            (lock_key,),
        )


def _insert_quota_occurrence(
    connection: psycopg.Connection[Any],
    *,
    routine_ref: UUID,
    state_ref: UUID,
    occurrence_ref: UUID,
) -> None:
    connection.execute(
        "INSERT INTO dante.occurrence(occurrence_ref) VALUES (%s)", (occurrence_ref,)
    )
    connection.execute(
        "INSERT INTO dante.occurrence_generation"
        "(occurrence_ref,source_native_ref,governing_recurrence_state_ref,origin_code) "
        "VALUES (%s,%s,%s,'recurrence_generated')",
        (occurrence_ref, routine_ref, state_ref),
    )
    connection.execute(
        "INSERT INTO dante.occurrence_generation_quota"
        "(occurrence_ref,period_start_date,period_end_date_exclusive,frame_code,zone_id) "
        "VALUES (%s,%s,%s,'floating_local',NULL)",
        (occurrence_ref, date(2026, 1, 1), date(2026, 1, 2)),
    )


def test_m7_activates_exact_table_and_view_acl_matrix(
    provisioned_database: Any,
    alembic_config: Config,
) -> None:
    database = _upgrade_m7(provisioned_database, alembic_config)
    tables = _mapped_table_names()
    assert len(tables) == 68
    assert len(_NO_INSERT) == 14
    assert len(_HISTORY_COLUMNS) == 5
    table_insert = tables - _NO_INSERT - set(_HISTORY_COLUMNS)
    assert len(table_insert) == 49

    with _admin_connection(database) as connection:
        actual_table_grants = {
            (str(row[0]), str(row[1]))
            for row in connection.execute(
                "SELECT table_name, privilege_type "
                "FROM information_schema.role_table_grants "
                "WHERE grantee='dante_runtime' AND table_schema='dante'"
            )
        }
        actual_column_grants = {
            (str(row[0]), str(row[1]), str(row[2]), bool(row[3]))
            for row in connection.execute(
                """
                SELECT c.relname, a.attname, acl.privilege_type, acl.is_grantable
                FROM pg_attribute AS a
                JOIN pg_class AS c ON c.oid=a.attrelid
                JOIN pg_namespace AS n ON n.oid=c.relnamespace
                CROSS JOIN LATERAL aclexplode(a.attacl) AS acl
                JOIN pg_roles AS r ON r.oid=acl.grantee
                WHERE n.nspname='dante'
                  AND r.rolname='dante_runtime'
                  AND a.attnum>0
                  AND NOT a.attisdropped
                """
            )
        }
        public_acl_count = connection.execute(
            """
            SELECT count(*)
            FROM pg_class AS c
            JOIN pg_namespace AS n ON n.oid=c.relnamespace
            CROSS JOIN LATERAL aclexplode(coalesce(c.relacl, acldefault('r',c.relowner))) AS acl
            WHERE n.nspname='dante'
              AND c.relkind IN ('r','v')
              AND acl.grantee=0
              AND c.relname<>'alembic_version'
            """
        ).fetchone()

    expected_table_grants = {(table, "SELECT") for table in tables}
    expected_table_grants |= {(table, "INSERT") for table in table_insert}
    expected_table_grants |= {(view, "SELECT") for view in _VIEW_ACL}
    expected_table_grants |= {
        (view, "DELETE") for view, (_, delete_allowed) in _VIEW_ACL.items() if delete_allowed
    }
    assert actual_table_grants == expected_table_grants

    expected_column_grants: set[tuple[str, str, str, bool]] = set()
    for table, owner_column in _HISTORY_COLUMNS.items():
        for column in (owner_column, "material_state_ref", "current_from_at"):
            expected_column_grants.add((table, column, "INSERT", False))
        expected_column_grants.add((table, "current_until_at", "UPDATE", False))
    for view, (owner_column, _) in _VIEW_ACL.items():
        expected_column_grants.add((view, owner_column, "INSERT", False))
        expected_column_grants.add((view, "material_state_ref", "INSERT", False))
        expected_column_grants.add((view, "material_state_ref", "UPDATE", False))
    assert actual_column_grants == expected_column_grants
    assert public_acl_count == (0,)


def test_m7_keeps_routines_directly_uncallable_and_role13_runtime_compatible(
    provisioned_database: Any,
    alembic_config: Config,
) -> None:
    database = _upgrade_m7(provisioned_database, alembic_config)
    with _admin_connection(database) as connection:
        rows = list(
            connection.execute(
                """
                SELECT p.proname,
                       has_function_privilege('dante_runtime',p.oid,'EXECUTE'),
                       has_function_privilege('dante_migrator',p.oid,'EXECUTE'),
                       EXISTS (
                         SELECT 1 FROM aclexplode(coalesce(p.proacl,acldefault('f',p.proowner))) acl
                         WHERE acl.grantee=0 AND acl.privilege_type='EXECUTE'
                       ),
                       pg_get_functiondef(p.oid)
                FROM pg_proc AS p
                JOIN pg_namespace AS n ON n.oid=p.pronamespace
                WHERE n.nspname='dante'
                ORDER BY p.proname
                """
            )
        )
    assert {str(row[0]) for row in rows} == _ROUTINES
    assert all(tuple(row[1:4]) == (False, False, False) for row in rows)
    role13 = next(
        str(row[4]) for row in rows if row[0] == "enforce_occurrence_generation_integrity"
    )
    assert "FOR UPDATE" not in role13
    assert "CP6-M07: Part-14 advisory locks" in role13


def test_m7_runtime_can_replace_current_recurrence_only_through_bounded_surfaces(
    provisioned_database: Any,
    alembic_config: Config,
) -> None:
    database = _upgrade_m7(provisioned_database, alembic_config)
    with _owner_connection(database) as owner:
        routine_ref, first_state, second_state, current_from = _create_two_elapsed_routine_states(
            owner
        )

    closure = current_from + timedelta(hours=2)
    with _runtime_connection(database) as runtime:
        with runtime.transaction():
            runtime.execute(
                "UPDATE dante.routine_recurrence_current_history "
                "SET current_until_at=%s "
                "WHERE routine_ref=%s AND current_until_at IS NULL",
                (closure, routine_ref),
            )
            runtime.execute(
                "INSERT INTO dante.routine_recurrence_current_history"
                "(routine_ref,material_state_ref,current_from_at) VALUES (%s,%s,%s)",
                (routine_ref, second_state, closure),
            )
            runtime.execute(
                "UPDATE dante.routine_current_recurrence SET material_state_ref=%s "
                "WHERE native_owner_ref=%s",
                (second_state, routine_ref),
            )

        row = runtime.execute(
            "SELECT material_state_ref FROM dante.routine_current_recurrence "
            "WHERE native_owner_ref=%s",
            (routine_ref,),
        ).fetchone()
        assert row == (second_state,)

        with pytest.raises(errors.InsufficientPrivilege):
            runtime.execute(
                "UPDATE dante.native_current_material_state SET material_state_ref=%s "
                "WHERE native_owner_ref=%s AND facet_code='routine.recurrence'",
                (first_state, routine_ref),
            )


def test_m7_runtime_quota_generation_uses_advisory_locks_without_owner_update(
    provisioned_database: Any,
    alembic_config: Config,
) -> None:
    database = _upgrade_m7(provisioned_database, alembic_config)
    with _owner_connection(database) as owner:
        routine_ref, state_ref = _create_quota_routine(owner)

    with _runtime_connection(database) as runtime:

        def insert_locked_occurrence() -> None:
            _acquire_generation_locks(runtime, routine_ref)
            _insert_quota_occurrence(
                runtime,
                routine_ref=routine_ref,
                state_ref=state_ref,
                occurrence_ref=uuid7(),
            )

        with runtime.transaction():
            insert_locked_occurrence()

        with pytest.raises(errors.CheckViolation) as exc_info, runtime.transaction():
            insert_locked_occurrence()
        assert exc_info.value.sqlstate == "23514"

        with pytest.raises(errors.InsufficientPrivilege):
            runtime.execute(
                "UPDATE dante.routine SET routine_ref=routine_ref WHERE routine_ref=%s",
                (routine_ref,),
            )


def test_m7_lock_key_contract_is_stable_and_namespaced() -> None:
    assert advisory_lock_key(1, _GOLDEN_REF) == 114563613494871305
    assert advisory_lock_key(4, _GOLDEN_REF) == 330736395608655113
    assert advisory_lock_key(6, _GOLDEN_REF) == 474851583684510985
    assert occurrence_generation_lock_keys("routine", _GOLDEN_REF) == (
        330736395608655113,
        474851583684510985,
    )
    assert occurrence_generation_lock_keys("event", _GOLDEN_REF) == (
        402793989646583049,
        546909177722438921,
    )
    with pytest.raises(
        ValueError,
        match=r"namespace_code must be in the frozen 1\.\.127 range",
    ):
        advisory_lock_key(0, _GOLDEN_REF)


def test_m7_downgrade_restores_m6_deny_by_default_and_role13_owner_lock(
    provisioned_database: Any,
    alembic_config: Config,
) -> None:
    command.upgrade(alembic_config, _M7_REVISION)
    command.downgrade(alembic_config, _M6_REVISION)
    tables = _mapped_table_names()
    with _admin_connection(provisioned_database) as connection:
        granted = {
            str(row[0])
            for row in connection.execute(
                """
                SELECT c.relname
                FROM pg_class AS c
                JOIN pg_namespace AS n ON n.oid=c.relnamespace
                WHERE n.nspname='dante'
                  AND c.relname = ANY(%s)
                  AND (
                    has_table_privilege('dante_runtime',c.oid,'SELECT')
                    OR has_table_privilege('dante_runtime',c.oid,'INSERT')
                    OR has_table_privilege('dante_runtime',c.oid,'UPDATE')
                    OR has_table_privilege('dante_runtime',c.oid,'DELETE')
                  )
                """,
                (sorted(tables | set(_VIEW_ACL)),),
            )
        }
        definition = connection.execute(
            """
            SELECT pg_get_functiondef(p.oid)
            FROM pg_proc AS p
            JOIN pg_namespace AS n ON n.oid=p.pronamespace
            WHERE n.nspname='dante'
              AND p.proname='enforce_occurrence_generation_integrity'
            """
        ).fetchone()
    assert granted == set()
    assert definition is not None
    role13 = str(definition[0])
    assert role13.count("FOR UPDATE") == 2
    assert "CP6-M07: Part-14 advisory locks" not in role13
