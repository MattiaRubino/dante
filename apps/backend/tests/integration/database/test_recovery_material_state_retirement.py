"""Real PostgreSQL acceptance for recovery-safe MaterialState retirement."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any
from uuid import UUID, uuid7

import psycopg
import pytest
from psycopg import errors, sql

pytestmark = pytest.mark.postgres


def _owner(database: Any) -> psycopg.Connection[Any]:
    connection = psycopg.connect(
        **database.connection_kwargs("dante_migrator", database.cluster.migrator_password),
        autocommit=True,
    )
    connection.execute("SET ROLE dante_owner")
    return connection


def _retire(
    connection: psycopg.Connection[Any], *, state_ref: UUID, payload_delete_sql: str
) -> UUID:
    suppression_ref = uuid7()
    with connection.transaction():
        connection.execute(
            "INSERT INTO dante.material_state_retirement"
            "(material_state_ref,retirement_code,retired_at,recovery_suppression_ref) "
            "VALUES (%s,'redacted',%s,%s)",
            (state_ref, datetime.now(UTC), suppression_ref),
        )
        connection.execute(payload_delete_sql, (state_ref,))
    return suppression_ref


def _assert_retired_continuity(
    connection: psycopg.Connection[Any],
    *,
    state_ref: UUID,
    owner_table: str,
    owner_column: str,
    owner_ref: UUID,
    state_table: str,
    history_table: str,
    history_owner_column: str,
    payload_table: str,
) -> None:
    statement = sql.SQL(
        """
        SELECT
          (SELECT count(*) FROM dante.{owner_table} WHERE {owner_column}=%s),
          (SELECT count(*) FROM dante.material_state_address WHERE material_state_ref=%s),
          (SELECT count(*) FROM dante.{state_table} WHERE material_state_ref=%s),
          (SELECT count(*) FROM dante.material_state_retirement WHERE material_state_ref=%s),
          (SELECT count(*) FROM dante.{payload_table} WHERE material_state_ref=%s),
          (SELECT count(*) FROM dante.{history_table}
             WHERE {history_owner_column}=%s AND material_state_ref=%s)
        """
    ).format(
        owner_table=sql.Identifier(owner_table),
        owner_column=sql.Identifier(owner_column),
        state_table=sql.Identifier(state_table),
        payload_table=sql.Identifier(payload_table),
        history_table=sql.Identifier(history_table),
        history_owner_column=sql.Identifier(history_owner_column),
    )
    row = connection.execute(
        statement,
        (owner_ref, state_ref, state_ref, state_ref, state_ref, owner_ref, state_ref),
    ).fetchone()
    assert row == (1, 1, 1, 1, 0, 1)


def test_recovery_retirement_materializes_exact_security_surface(migrated_database: Any) -> None:
    with psycopg.connect(
        host=migrated_database.cluster.host,
        port=migrated_database.cluster.port,
        dbname=migrated_database.name,
        user=migrated_database.cluster.admin_user,
        password=migrated_database.cluster.admin_password,
        autocommit=True,
    ) as connection:
        table_acl = connection.execute(
            "SELECT has_table_privilege('dante_runtime','dante.material_state_retirement','SELECT'),"
            "has_table_privilege('dante_runtime','dante.material_state_retirement','INSERT'),"
            "has_table_privilege('dante_runtime','dante.material_state_retirement','UPDATE'),"
            "has_table_privilege('dante_runtime','dante.material_state_retirement','DELETE')"
        ).fetchone()
        routine_acl = connection.execute(
            "SELECT has_function_privilege("
            "'dante_runtime','dante.enforce_material_state_retirement()','EXECUTE')"
        ).fetchone()
        trigger = connection.execute(
            """
            SELECT t.tgname, c.condeferrable, c.condeferred
            FROM pg_trigger t
            JOIN pg_constraint c ON c.oid=t.tgconstraint
            JOIN pg_class r ON r.oid=t.tgrelid
            JOIN pg_namespace n ON n.oid=r.relnamespace
            WHERE n.nspname='dante'
              AND r.relname='material_state_retirement'
              AND NOT t.tgisinternal
            """
        ).fetchone()
    assert table_acl == (True, False, False, False)
    assert routine_acl == (False,)
    assert trigger == ("ctrg_material_state_retirement_integrity", True, True)


def test_recovery_retirement_is_append_only(migrated_database: Any) -> None:
    with _owner(migrated_database) as connection:
        session_ref, state_ref, suppression_ref = uuid7(), uuid7(), uuid7()
        with connection.transaction():
            connection.execute("INSERT INTO dante.session(session_ref) VALUES (%s)", (session_ref,))
            connection.execute(
                "INSERT INTO dante.native_address(native_ref,owner_family) VALUES (%s,'session')",
                (session_ref,),
            )
            connection.execute(
                "INSERT INTO dante.material_state_address"
                "(material_state_ref,native_owner_ref,facet_code) "
                "VALUES (%s,%s,'session.timing')",
                (state_ref, session_ref),
            )
            connection.execute(
                "INSERT INTO dante.session_timing_state"
                "(material_state_ref,session_ref,timing_form_code) "
                "VALUES (%s,%s,'absolute')",
                (state_ref, session_ref),
            )
            connection.execute(
                "INSERT INTO dante.session_timing_absolute"
                "(material_state_ref,started_at,start_precision_code) "
                "VALUES (%s,%s,'exact')",
                (state_ref, datetime.now(UTC)),
            )
            connection.execute(
                "INSERT INTO dante.native_current_material_state"
                "(native_owner_ref,facet_code,material_state_ref) "
                "VALUES (%s,'session.timing',%s)",
                (session_ref, state_ref),
            )
            connection.execute(
                "INSERT INTO dante.session_timing_current_history"
                "(session_ref,material_state_ref,current_from_at) VALUES (%s,%s,%s)",
                (session_ref, state_ref, datetime.now(UTC)),
            )
        with connection.transaction():
            connection.execute(
                "INSERT INTO dante.material_state_retirement"
                "(material_state_ref,retirement_code,retired_at,recovery_suppression_ref) "
                "VALUES (%s,'redacted',%s,%s)",
                (state_ref, datetime.now(UTC), suppression_ref),
            )
            connection.execute(
                "DELETE FROM dante.session_timing_absolute WHERE material_state_ref=%s",
                (state_ref,),
            )
        with pytest.raises(errors.CheckViolation), connection.transaction():
            connection.execute(
                "UPDATE dante.material_state_retirement "
                "SET retirement_code='unavailable' WHERE material_state_ref=%s",
                (state_ref,),
            )
        with pytest.raises(errors.CheckViolation), connection.transaction():
            connection.execute(
                "DELETE FROM dante.material_state_retirement WHERE material_state_ref=%s",
                (state_ref,),
            )


def test_recovery_retirement_covers_all_five_material_facets(migrated_database: Any) -> None:
    now = datetime.now(UTC)
    with _owner(migrated_database) as connection:
        activity_ref = uuid7()
        with connection.transaction():
            connection.execute(
                "INSERT INTO dante.activity(activity_ref) VALUES (%s)", (activity_ref,)
            )
            connection.execute(
                "INSERT INTO dante.native_address(native_ref,owner_family) VALUES (%s,'activity')",
                (activity_ref,),
            )

        schedule_ref, schedule_state = uuid7(), uuid7()
        with connection.transaction():
            connection.execute(
                "INSERT INTO dante.schedule(schedule_ref,subject_native_ref) VALUES (%s,%s)",
                (schedule_ref, activity_ref),
            )
            connection.execute(
                "INSERT INTO dante.scoped_address(scoped_ref,scoped_family) VALUES (%s,'schedule')",
                (schedule_ref,),
            )
            connection.execute(
                "INSERT INTO dante.material_state_address"
                "(material_state_ref,scoped_owner_ref,facet_code) "
                "VALUES (%s,%s,'schedule.placement')",
                (schedule_state, schedule_ref),
            )
            connection.execute(
                "INSERT INTO dante.schedule_placement_state"
                "(material_state_ref,schedule_ref,temporal_form_code) "
                "VALUES (%s,%s,'date_span')",
                (schedule_state, schedule_ref),
            )
            connection.execute(
                "INSERT INTO dante.schedule_placement_date_state(material_state_ref,date_span) "
                "VALUES (%s,'[2026-08-30,2026-08-31)'::daterange)",
                (schedule_state,),
            )
            connection.execute(
                "INSERT INTO dante.scoped_current_material_state"
                "(scoped_owner_ref,facet_code,material_state_ref) "
                "VALUES (%s,'schedule.placement',%s)",
                (schedule_ref, schedule_state),
            )
            connection.execute(
                "INSERT INTO dante.schedule_placement_current_history"
                "(schedule_ref,material_state_ref,current_from_at) VALUES (%s,%s,%s)",
                (schedule_ref, schedule_state, now),
            )
        _retire(
            connection,
            state_ref=schedule_state,
            payload_delete_sql=(
                "DELETE FROM dante.schedule_placement_date_state WHERE material_state_ref=%s"
            ),
        )
        _assert_retired_continuity(
            connection,
            state_ref=schedule_state,
            owner_table="schedule",
            owner_column="schedule_ref",
            owner_ref=schedule_ref,
            state_table="schedule_placement_state",
            history_table="schedule_placement_current_history",
            history_owner_column="schedule_ref",
            payload_table="schedule_placement_date_state",
        )
        with pytest.raises(errors.CheckViolation), connection.transaction():
            connection.execute(
                "INSERT INTO dante.schedule_placement_date_state(material_state_ref,date_span) "
                "VALUES (%s,'[2026-09-01,2026-09-02)'::daterange)",
                (schedule_state,),
            )

        actual_ref, actual_state = uuid7(), uuid7()
        with connection.transaction():
            connection.execute(
                "INSERT INTO dante.actual(actual_ref,subject_native_ref) VALUES (%s,%s)",
                (actual_ref, activity_ref),
            )
            connection.execute(
                "INSERT INTO dante.scoped_address(scoped_ref,scoped_family) VALUES (%s,'actual')",
                (actual_ref,),
            )
            connection.execute(
                "INSERT INTO dante.material_state_address"
                "(material_state_ref,scoped_owner_ref,facet_code) "
                "VALUES (%s,%s,'actual.realization')",
                (actual_state, actual_ref),
            )
            connection.execute(
                "INSERT INTO dante.actual_realization_state"
                "(material_state_ref,actual_ref,realization_occurred) VALUES (%s,%s,true)",
                (actual_state, actual_ref),
            )
            connection.execute(
                "INSERT INTO dante.actual_realization_timing"
                "(material_state_ref,extent_code,started_at) VALUES (%s,'instant',%s)",
                (actual_state, now),
            )
            connection.execute(
                "INSERT INTO dante.scoped_current_material_state"
                "(scoped_owner_ref,facet_code,material_state_ref) "
                "VALUES (%s,'actual.realization',%s)",
                (actual_ref, actual_state),
            )
            connection.execute(
                "INSERT INTO dante.actual_realization_current_history"
                "(actual_ref,material_state_ref,current_from_at) VALUES (%s,%s,%s)",
                (actual_ref, actual_state, now),
            )
        _retire(
            connection,
            state_ref=actual_state,
            payload_delete_sql=(
                "DELETE FROM dante.actual_realization_timing WHERE material_state_ref=%s"
            ),
        )
        _assert_retired_continuity(
            connection,
            state_ref=actual_state,
            owner_table="actual",
            owner_column="actual_ref",
            owner_ref=actual_ref,
            state_table="actual_realization_state",
            history_table="actual_realization_current_history",
            history_owner_column="actual_ref",
            payload_table="actual_realization_timing",
        )
        with pytest.raises(errors.CheckViolation), connection.transaction():
            connection.execute(
                "INSERT INTO dante.actual_realization_timing"
                "(material_state_ref,extent_code,started_at) VALUES (%s,'instant',%s)",
                (actual_state, now),
            )

        session_ref, session_state = uuid7(), uuid7()
        with connection.transaction():
            connection.execute("INSERT INTO dante.session(session_ref) VALUES (%s)", (session_ref,))
            connection.execute(
                "INSERT INTO dante.native_address(native_ref,owner_family) VALUES (%s,'session')",
                (session_ref,),
            )
            connection.execute(
                "INSERT INTO dante.material_state_address"
                "(material_state_ref,native_owner_ref,facet_code) "
                "VALUES (%s,%s,'session.timing')",
                (session_state, session_ref),
            )
            connection.execute(
                "INSERT INTO dante.session_timing_state"
                "(material_state_ref,session_ref,timing_form_code) "
                "VALUES (%s,%s,'absolute')",
                (session_state, session_ref),
            )
            connection.execute(
                "INSERT INTO dante.session_timing_absolute"
                "(material_state_ref,started_at,start_precision_code) "
                "VALUES (%s,%s,'exact')",
                (session_state, now),
            )
            connection.execute(
                "INSERT INTO dante.native_current_material_state"
                "(native_owner_ref,facet_code,material_state_ref) "
                "VALUES (%s,'session.timing',%s)",
                (session_ref, session_state),
            )
            connection.execute(
                "INSERT INTO dante.session_timing_current_history"
                "(session_ref,material_state_ref,current_from_at) VALUES (%s,%s,%s)",
                (session_ref, session_state, now),
            )
        _retire(
            connection,
            state_ref=session_state,
            payload_delete_sql=(
                "DELETE FROM dante.session_timing_absolute WHERE material_state_ref=%s"
            ),
        )
        _assert_retired_continuity(
            connection,
            state_ref=session_state,
            owner_table="session",
            owner_column="session_ref",
            owner_ref=session_ref,
            state_table="session_timing_state",
            history_table="session_timing_current_history",
            history_owner_column="session_ref",
            payload_table="session_timing_absolute",
        )
        with pytest.raises(errors.CheckViolation), connection.transaction():
            connection.execute(
                "INSERT INTO dante.session_timing_absolute"
                "(material_state_ref,started_at,start_precision_code) "
                "VALUES (%s,%s,'exact')",
                (session_state, now),
            )

        routine_ref, routine_state = uuid7(), uuid7()
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
                (routine_state, routine_ref),
            )
            connection.execute(
                "INSERT INTO dante.routine_recurrence_state"
                "(material_state_ref,routine_ref,family_code,range_kind) "
                "VALUES (%s,%s,'elapsed_interval','open')",
                (routine_state, routine_ref),
            )
            connection.execute(
                "INSERT INTO dante.routine_recurrence_elapsed_state"
                "(material_state_ref,elapsed_seconds,anchor_mode_code,anchor_at) "
                "VALUES (%s,60,'fixed_anchor',%s)",
                (routine_state, now),
            )
            connection.execute(
                "INSERT INTO dante.native_current_material_state"
                "(native_owner_ref,facet_code,material_state_ref) "
                "VALUES (%s,'routine.recurrence',%s)",
                (routine_ref, routine_state),
            )
            connection.execute(
                "INSERT INTO dante.routine_recurrence_current_history"
                "(routine_ref,material_state_ref,current_from_at) VALUES (%s,%s,%s)",
                (routine_ref, routine_state, now),
            )
        _retire(
            connection,
            state_ref=routine_state,
            payload_delete_sql=(
                "DELETE FROM dante.routine_recurrence_elapsed_state WHERE material_state_ref=%s"
            ),
        )
        _assert_retired_continuity(
            connection,
            state_ref=routine_state,
            owner_table="routine",
            owner_column="routine_ref",
            owner_ref=routine_ref,
            state_table="routine_recurrence_state",
            history_table="routine_recurrence_current_history",
            history_owner_column="routine_ref",
            payload_table="routine_recurrence_elapsed_state",
        )
        with pytest.raises(errors.CheckViolation), connection.transaction():
            connection.execute(
                "INSERT INTO dante.routine_recurrence_elapsed_state"
                "(material_state_ref,elapsed_seconds,anchor_mode_code,anchor_at) "
                "VALUES (%s,60,'fixed_anchor',%s)",
                (routine_state, now),
            )

        event_ref, event_state = uuid7(), uuid7()
        with connection.transaction():
            connection.execute("INSERT INTO dante.event(event_ref) VALUES (%s)", (event_ref,))
            connection.execute(
                "INSERT INTO dante.native_address(native_ref,owner_family) VALUES (%s,'event')",
                (event_ref,),
            )
            connection.execute(
                "INSERT INTO dante.material_state_address"
                "(material_state_ref,native_owner_ref,facet_code) "
                "VALUES (%s,%s,'event.recurrence')",
                (event_state, event_ref),
            )
            connection.execute(
                "INSERT INTO dante.event_recurrence_state"
                "(material_state_ref,event_ref,family_code,range_kind) "
                "VALUES (%s,%s,'elapsed_interval','open')",
                (event_state, event_ref),
            )
            connection.execute(
                "INSERT INTO dante.event_recurrence_elapsed_state"
                "(material_state_ref,elapsed_seconds,anchor_mode_code,anchor_at) "
                "VALUES (%s,60,'fixed_anchor',%s)",
                (event_state, now),
            )
            connection.execute(
                "INSERT INTO dante.native_current_material_state"
                "(native_owner_ref,facet_code,material_state_ref) "
                "VALUES (%s,'event.recurrence',%s)",
                (event_ref, event_state),
            )
            connection.execute(
                "INSERT INTO dante.event_recurrence_current_history"
                "(event_ref,material_state_ref,current_from_at) VALUES (%s,%s,%s)",
                (event_ref, event_state, now),
            )
        _retire(
            connection,
            state_ref=event_state,
            payload_delete_sql=(
                "DELETE FROM dante.event_recurrence_elapsed_state WHERE material_state_ref=%s"
            ),
        )
        _assert_retired_continuity(
            connection,
            state_ref=event_state,
            owner_table="event",
            owner_column="event_ref",
            owner_ref=event_ref,
            state_table="event_recurrence_state",
            history_table="event_recurrence_current_history",
            history_owner_column="event_ref",
            payload_table="event_recurrence_elapsed_state",
        )
        with pytest.raises(errors.CheckViolation), connection.transaction():
            connection.execute(
                "INSERT INTO dante.event_recurrence_elapsed_state"
                "(material_state_ref,elapsed_seconds,anchor_mode_code,anchor_at) "
                "VALUES (%s,60,'fixed_anchor',%s)",
                (event_state, now),
            )
