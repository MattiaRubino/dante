"""HEAD-level PostgreSQL regression proof for the shared current-history dispatcher."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import Any, Literal
from uuid import UUID, uuid7

import psycopg
import pytest

HistoryFamily = Literal[
    "actual",
    "session",
    "routine_recurrence",
    "event_recurrence",
]


@dataclass(frozen=True)
class _HistoryCase:
    history_table: str
    owner_column: str
    owner_ref: UUID
    current_table: str
    current_owner_column: str
    facet_code: str
    constraint_name: str
    current_from_at: datetime


def _owner_connection(database: Any) -> psycopg.Connection[Any]:
    connection = psycopg.connect(
        **database.connection_kwargs(
            "dante_migrator",
            database.cluster.migrator_password,
        )
    )
    connection.execute("SET ROLE dante_owner")
    connection.execute("SET search_path TO pg_catalog,dante,pg_temp")
    return connection


def _seed_self_person(connection: psycopg.Connection[Any]) -> UUID:
    person_ref = uuid7()
    connection.execute("INSERT INTO dante.person(person_ref) VALUES (%s)", (person_ref,))
    connection.execute(
        "INSERT INTO dante.native_address(native_ref,owner_family) VALUES (%s,'person')",
        (person_ref,),
    )
    return person_ref


def _seed_actual(database: Any, now: datetime) -> _HistoryCase:
    with _owner_connection(database) as connection:
        self_person_ref = _seed_self_person(connection)
        activity_ref = uuid7()
        actual_ref = uuid7()
        state_ref = uuid7()

        connection.execute("INSERT INTO dante.activity(activity_ref) VALUES (%s)", (activity_ref,))
        connection.execute(
            "INSERT INTO dante.native_address(native_ref,owner_family) VALUES (%s,'activity')",
            (activity_ref,),
        )
        connection.execute(
            """
            INSERT INTO dante.activity_intention(
                activity_ref,self_person_ref,title,created_at
            ) VALUES (%s,%s,'B04 dispatcher actual subject',%s)
            """,
            (activity_ref, self_person_ref, now),
        )
        connection.execute(
            "INSERT INTO dante.actual(actual_ref,subject_native_ref) VALUES (%s,%s)",
            (actual_ref, activity_ref),
        )
        connection.execute(
            "INSERT INTO dante.scoped_address(scoped_ref,scoped_family) VALUES (%s,'actual')",
            (actual_ref,),
        )
        connection.execute(
            """
            INSERT INTO dante.material_state_address(
                material_state_ref,scoped_owner_ref,facet_code
            ) VALUES (%s,%s,'actual.realization')
            """,
            (state_ref, actual_ref),
        )
        connection.execute(
            """
            INSERT INTO dante.actual_realization_state(
                material_state_ref,actual_ref,realization_occurred
            ) VALUES (%s,%s,false)
            """,
            (state_ref, actual_ref),
        )
        connection.execute(
            """
            INSERT INTO dante.scoped_current_material_state(
                scoped_owner_ref,facet_code,material_state_ref
            ) VALUES (%s,'actual.realization',%s)
            """,
            (actual_ref, state_ref),
        )
        connection.execute(
            """
            INSERT INTO dante.actual_realization_current_history(
                actual_ref,material_state_ref,current_from_at
            ) VALUES (%s,%s,%s)
            """,
            (actual_ref, state_ref, now),
        )
        connection.commit()

    return _HistoryCase(
        history_table="actual_realization_current_history",
        owner_column="actual_ref",
        owner_ref=actual_ref,
        current_table="scoped_current_material_state",
        current_owner_column="scoped_owner_ref",
        facet_code="actual.realization",
        constraint_name="ctrg_actual_realization_current_history_current_history",
        current_from_at=now,
    )


def _seed_session(database: Any, now: datetime) -> _HistoryCase:
    with _owner_connection(database) as connection:
        session_ref = uuid7()
        state_ref = uuid7()

        connection.execute("INSERT INTO dante.session(session_ref) VALUES (%s)", (session_ref,))
        connection.execute(
            "INSERT INTO dante.native_address(native_ref,owner_family) VALUES (%s,'session')",
            (session_ref,),
        )
        connection.execute(
            """
            INSERT INTO dante.material_state_address(
                material_state_ref,native_owner_ref,facet_code
            ) VALUES (%s,%s,'session.timing')
            """,
            (state_ref, session_ref),
        )
        connection.execute(
            """
            INSERT INTO dante.session_timing_state(
                material_state_ref,session_ref,timing_form_code
            ) VALUES (%s,%s,'elapsed_only')
            """,
            (state_ref, session_ref),
        )
        connection.execute(
            """
            INSERT INTO dante.session_timing_elapsed(
                material_state_ref,elapsed_seconds,elapsed_precision_code
            ) VALUES (%s,60.000000,'exact')
            """,
            (state_ref,),
        )
        connection.execute(
            """
            INSERT INTO dante.native_current_material_state(
                native_owner_ref,facet_code,material_state_ref
            ) VALUES (%s,'session.timing',%s)
            """,
            (session_ref, state_ref),
        )
        connection.execute(
            """
            INSERT INTO dante.session_timing_current_history(
                session_ref,material_state_ref,current_from_at
            ) VALUES (%s,%s,%s)
            """,
            (session_ref, state_ref, now),
        )
        connection.commit()

    return _HistoryCase(
        history_table="session_timing_current_history",
        owner_column="session_ref",
        owner_ref=session_ref,
        current_table="native_current_material_state",
        current_owner_column="native_owner_ref",
        facet_code="session.timing",
        constraint_name="ctrg_session_timing_current_history_current_history",
        current_from_at=now,
    )


def _seed_routine_recurrence(database: Any, now: datetime) -> _HistoryCase:
    with _owner_connection(database) as connection:
        routine_ref = uuid7()
        state_ref = uuid7()

        connection.execute("INSERT INTO dante.routine(routine_ref) VALUES (%s)", (routine_ref,))
        connection.execute(
            "INSERT INTO dante.native_address(native_ref,owner_family) VALUES (%s,'routine')",
            (routine_ref,),
        )
        connection.execute(
            """
            INSERT INTO dante.material_state_address(
                material_state_ref,native_owner_ref,facet_code
            ) VALUES (%s,%s,'routine.recurrence')
            """,
            (state_ref, routine_ref),
        )
        connection.execute(
            """
            INSERT INTO dante.routine_recurrence_state(
                material_state_ref,routine_ref,family_code,range_kind
            ) VALUES (%s,%s,'elapsed_interval','open')
            """,
            (state_ref, routine_ref),
        )
        connection.execute(
            """
            INSERT INTO dante.routine_recurrence_elapsed_state(
                material_state_ref,elapsed_seconds,anchor_mode_code,anchor_at
            ) VALUES (%s,60.000000,'fixed_anchor',%s)
            """,
            (state_ref, now),
        )
        connection.execute(
            """
            INSERT INTO dante.native_current_material_state(
                native_owner_ref,facet_code,material_state_ref
            ) VALUES (%s,'routine.recurrence',%s)
            """,
            (routine_ref, state_ref),
        )
        connection.execute(
            """
            INSERT INTO dante.routine_recurrence_current_history(
                routine_ref,material_state_ref,current_from_at
            ) VALUES (%s,%s,%s)
            """,
            (routine_ref, state_ref, now),
        )
        connection.commit()

    return _HistoryCase(
        history_table="routine_recurrence_current_history",
        owner_column="routine_ref",
        owner_ref=routine_ref,
        current_table="native_current_material_state",
        current_owner_column="native_owner_ref",
        facet_code="routine.recurrence",
        constraint_name="ctrg_routine_recurrence_current_history_current_history",
        current_from_at=now,
    )


def _seed_event_recurrence(database: Any, now: datetime) -> _HistoryCase:
    with _owner_connection(database) as connection:
        self_person_ref = _seed_self_person(connection)
        event_ref = uuid7()
        state_ref = uuid7()

        connection.execute("INSERT INTO dante.event(event_ref) VALUES (%s)", (event_ref,))
        connection.execute(
            "INSERT INTO dante.native_address(native_ref,owner_family) VALUES (%s,'event')",
            (event_ref,),
        )
        connection.execute(
            """
            INSERT INTO dante.event_expectation(
                event_ref,self_person_ref,title,created_at
            ) VALUES (%s,%s,'B04 dispatcher event recurrence',%s)
            """,
            (event_ref, self_person_ref, now),
        )
        connection.execute(
            """
            INSERT INTO dante.material_state_address(
                material_state_ref,native_owner_ref,facet_code
            ) VALUES (%s,%s,'event.recurrence')
            """,
            (state_ref, event_ref),
        )
        connection.execute(
            """
            INSERT INTO dante.event_recurrence_state(
                material_state_ref,event_ref,family_code,range_kind
            ) VALUES (%s,%s,'elapsed_interval','open')
            """,
            (state_ref, event_ref),
        )
        connection.execute(
            """
            INSERT INTO dante.event_recurrence_elapsed_state(
                material_state_ref,elapsed_seconds,anchor_mode_code,anchor_at
            ) VALUES (%s,60.000000,'fixed_anchor',%s)
            """,
            (state_ref, now),
        )
        connection.execute(
            """
            INSERT INTO dante.native_current_material_state(
                native_owner_ref,facet_code,material_state_ref
            ) VALUES (%s,'event.recurrence',%s)
            """,
            (event_ref, state_ref),
        )
        connection.execute(
            """
            INSERT INTO dante.event_recurrence_current_history(
                event_ref,material_state_ref,current_from_at
            ) VALUES (%s,%s,%s)
            """,
            (event_ref, state_ref, now),
        )
        connection.commit()

    return _HistoryCase(
        history_table="event_recurrence_current_history",
        owner_column="event_ref",
        owner_ref=event_ref,
        current_table="native_current_material_state",
        current_owner_column="native_owner_ref",
        facet_code="event.recurrence",
        constraint_name="ctrg_event_recurrence_current_history_current_history",
        current_from_at=now,
    )


def _seed_case(database: Any, family: HistoryFamily, now: datetime) -> _HistoryCase:
    if family == "actual":
        return _seed_actual(database, now)
    if family == "session":
        return _seed_session(database, now)
    if family == "routine_recurrence":
        return _seed_routine_recurrence(database, now)
    return _seed_event_recurrence(database, now)


def _close_current_episode(database: Any, case: _HistoryCase, closed_at: datetime) -> None:
    with _owner_connection(database) as connection:
        connection.execute(
            f"DELETE FROM dante.{case.current_table} "  # noqa: S608 - identifiers are fixed test constants.
            f"WHERE {case.current_owner_column}=%s AND facet_code=%s",
            (case.owner_ref, case.facet_code),
        )
        connection.execute(
            f"UPDATE dante.{case.history_table} "  # noqa: S608 - identifiers are fixed test constants.
            "SET current_until_at=%s "
            f"WHERE {case.owner_column}=%s AND current_from_at=%s",
            (closed_at, case.owner_ref, case.current_from_at),
        )
        connection.execute(
            f"SET CONSTRAINTS {case.constraint_name} IMMEDIATE"  # noqa: S608 - fixed constant.
        )
        connection.commit()

    with _owner_connection(database) as connection:
        history_row = connection.execute(
            f"SELECT current_until_at FROM dante.{case.history_table} "  # noqa: S608
            f"WHERE {case.owner_column}=%s AND current_from_at=%s",
            (case.owner_ref, case.current_from_at),
        ).fetchone()
        current_row = connection.execute(
            f"SELECT count(*) FROM dante.{case.current_table} "  # noqa: S608
            f"WHERE {case.current_owner_column}=%s AND facet_code=%s",
            (case.owner_ref, case.facet_code),
        ).fetchone()

    assert history_row == (closed_at,)
    assert current_row == (0,)


@pytest.mark.postgres
@pytest.mark.parametrize(
    "family",
    ["actual", "session", "routine_recurrence", "event_recurrence"],
)
def test_b04_shared_current_history_dispatch_closes_legacy_family_at_head(
    migrated_database: Any,
    family: HistoryFamily,
) -> None:
    now = datetime.now(UTC).replace(microsecond=0)
    case = _seed_case(migrated_database, family, now)
    _close_current_episode(migrated_database, case, now + timedelta(minutes=5))
