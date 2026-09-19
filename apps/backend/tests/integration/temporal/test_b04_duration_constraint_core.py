"""Real PostgreSQL proof for B04-E planned Schedule duration constraints."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Any
from uuid import UUID, uuid7

import psycopg
import pytest

_DURATION_SQL = """
SELECT constraint_ref,subject_native_ref,material_state_ref,active,created_at,replayed
FROM dante.mutate_self_schedule_duration_constraint(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
"""

_POLICY_SQL = """
SELECT schedule_ref,material_state_ref,active,created_at,replayed
FROM dante.mutate_self_schedule_movement_policy(%s,%s,%s,%s,%s,%s,%s,%s,%s)
"""

_MOVE_SQL = """
SELECT schedule_ref,subject_native_ref,movement_policy_material_state_ref,result_kind,
       proposal_ref,placement_material_state_ref,created_at,replayed
FROM dante.request_self_absolute_schedule_move(%s,%s,%s,%s,%s,%s,%s,%s,%s)
"""


def _runtime(database: Any) -> psycopg.Connection[Any]:
    return psycopg.connect(
        **database.connection_kwargs("dante_runtime", database.cluster.runtime_password)
    )


def _owner(database: Any) -> psycopg.Connection[Any]:
    connection = psycopg.connect(
        **database.connection_kwargs("dante_migrator", database.cluster.migrator_password)
    )
    connection.execute("SET ROLE dante_owner")
    connection.execute("SET search_path TO pg_catalog,dante,pg_temp")
    return connection


def _seed_activity(database: Any, *, suffix: str) -> tuple[UUID, UUID]:
    self_ref = uuid7()
    activity_ref = uuid7()
    now = datetime.now(UTC)
    with _owner(database) as connection:
        connection.execute("INSERT INTO dante.person(person_ref) VALUES (%s)", (self_ref,))
        connection.execute(
            "INSERT INTO dante.native_address(native_ref,owner_family) VALUES (%s,'person')",
            (self_ref,),
        )
        connection.execute("INSERT INTO dante.activity(activity_ref) VALUES (%s)", (activity_ref,))
        connection.execute(
            "INSERT INTO dante.native_address(native_ref,owner_family) VALUES (%s,'activity')",
            (activity_ref,),
        )
        connection.execute(
            """
            INSERT INTO dante.activity_intention(activity_ref,self_person_ref,title,created_at)
            VALUES (%s,%s,%s,%s)
            """,
            (activity_ref, self_ref, f"B04-E duration {suffix}", now),
        )
        connection.commit()
    return self_ref, activity_ref


def _seed_scheduled_activity(
    database: Any, *, suffix: str
) -> tuple[UUID, UUID, UUID, UUID, datetime]:
    self_ref, activity_ref = _seed_activity(database, suffix=suffix)
    schedule_ref = uuid7()
    placement_ref = uuid7()
    starts_at = datetime.now(UTC) + timedelta(days=1)
    ends_at = starts_at + timedelta(hours=1)
    with _runtime(database) as connection:
        row = connection.execute(
            """
            SELECT schedule_ref,material_state_ref
              FROM dante.establish_self_schedule_placement(%s,%s,%s,%s,%s,%s,%s::jsonb)
            """,
            (
                self_ref,
                f"operation:b04-e-establish-{suffix}",
                "e" * 64,
                activity_ref,
                schedule_ref,
                placement_ref,
                '{"kind":"absolute_interval","starts_at":"'
                + starts_at.isoformat()
                + '","ends_at":"'
                + ends_at.isoformat()
                + '"}',
            ),
        ).fetchone()
        connection.commit()
    assert row == (schedule_ref, placement_ref)
    return self_ref, activity_ref, schedule_ref, placement_ref, starts_at


def _duration(
    database: Any,
    *,
    self_ref: UUID,
    activity_ref: UUID,
    operation_id: str,
    fingerprint: str,
    mutation: str,
    constraint_ref: UUID,
    expected_ref: UUID | None,
    resulting_ref: UUID | None,
    kind: str | None,
    strength: str | None,
    microseconds: int | None,
) -> tuple[object, ...]:
    with _runtime(database) as connection:
        row = connection.execute(
            _DURATION_SQL,
            (
                self_ref,
                operation_id,
                fingerprint,
                mutation,
                activity_ref,
                constraint_ref,
                expected_ref,
                resulting_ref,
                kind,
                None if kind is None else "schedule.placement",
                strength,
                microseconds,
            ),
        ).fetchone()
        connection.commit()
    assert row is not None
    return row


def _set_direct_policy(
    database: Any, *, self_ref: UUID, schedule_ref: UUID, suffix: str
) -> UUID:
    state_ref = uuid7()
    with _runtime(database) as connection:
        row = connection.execute(
            _POLICY_SQL,
            (
                self_ref,
                f"operation:b04-e-policy-{suffix}",
                "7" * 64,
                "create",
                schedule_ref,
                None,
                state_ref,
                "automatic",
                "direct",
            ),
        ).fetchone()
        connection.commit()
    assert row is not None
    return state_ref


def _current_placement(database: Any, schedule_ref: UUID) -> UUID:
    with _owner(database) as connection:
        row = connection.execute(
            """
            SELECT material_state_ref
              FROM dante.scoped_current_material_state
             WHERE scoped_owner_ref=%s AND facet_code='schedule.placement'
            """,
            (schedule_ref,),
        ).fetchone()
    assert row is not None
    return row[0]


@pytest.mark.postgres
def test_b04_e_duration_create_revise_retire_history_and_replay(
    migrated_database: Any,
) -> None:
    self_ref, activity_ref = _seed_activity(migrated_database, suffix="lifecycle")
    constraint_ref = uuid7()
    first_ref = uuid7()
    created = _duration(
        migrated_database,
        self_ref=self_ref,
        activity_ref=activity_ref,
        operation_id="operation:b04-e-duration-create",
        fingerprint="1" * 64,
        mutation="create",
        constraint_ref=constraint_ref,
        expected_ref=None,
        resulting_ref=first_ref,
        kind="minimum",
        strength="hard",
        microseconds=45 * 60 * 1_000_000,
    )
    assert created[0] == constraint_ref
    assert created[2] == first_ref
    assert created[3] is True
    assert created[5] is False

    replay = _duration(
        migrated_database,
        self_ref=self_ref,
        activity_ref=activity_ref,
        operation_id="operation:b04-e-duration-create",
        fingerprint="1" * 64,
        mutation="create",
        constraint_ref=uuid7(),
        expected_ref=None,
        resulting_ref=uuid7(),
        kind="minimum",
        strength="hard",
        microseconds=45 * 60 * 1_000_000,
    )
    assert replay[0] == constraint_ref
    assert replay[2] == first_ref
    assert replay[5] is True

    second_ref = uuid7()
    revised = _duration(
        migrated_database,
        self_ref=self_ref,
        activity_ref=activity_ref,
        operation_id="operation:b04-e-duration-revise",
        fingerprint="2" * 64,
        mutation="revise",
        constraint_ref=constraint_ref,
        expected_ref=first_ref,
        resulting_ref=second_ref,
        kind="maximum",
        strength="soft",
        microseconds=90 * 60 * 1_000_000,
    )
    assert revised[2] == second_ref
    assert revised[3] is True

    with _runtime(migrated_database) as connection:
        with pytest.raises(psycopg.errors.UniqueViolation):
            connection.execute(
                _DURATION_SQL,
                (
                    self_ref,
                    "operation:b04-e-duration-stale",
                    "3" * 64,
                    "revise",
                    activity_ref,
                    constraint_ref,
                    first_ref,
                    uuid7(),
                    "minimum",
                    "schedule.placement",
                    "hard",
                    30 * 60 * 1_000_000,
                ),
            ).fetchone()
        connection.rollback()

    retired = _duration(
        migrated_database,
        self_ref=self_ref,
        activity_ref=activity_ref,
        operation_id="operation:b04-e-duration-retire",
        fingerprint="4" * 64,
        mutation="retire",
        constraint_ref=constraint_ref,
        expected_ref=second_ref,
        resulting_ref=None,
        kind=None,
        strength=None,
        microseconds=None,
    )
    assert retired[2] is None
    assert retired[3] is False

    with _owner(migrated_database) as connection:
        history = connection.execute(
            """
            SELECT material_state_ref,current_until_at
              FROM dante.temporal_constraint_current_history
             WHERE constraint_ref=%s
             ORDER BY current_from_at
            """,
            (constraint_ref,),
        ).fetchall()
        current = connection.execute(
            """
            SELECT material_state_ref
              FROM dante.scoped_current_material_state
             WHERE scoped_owner_ref=%s AND facet_code='temporal_constraint.rule'
            """,
            (constraint_ref,),
        ).fetchone()
    assert len(history) == 2
    assert history[0][0] == first_ref and history[0][1] is not None
    assert history[1][0] == second_ref and history[1][1] is not None
    assert current is None


@pytest.mark.postgres
def test_b04_e_hard_minimum_duration_blocks_automatic_move(
    migrated_database: Any,
) -> None:
    self_ref, activity_ref, schedule_ref, placement_ref, starts_at = _seed_scheduled_activity(
        migrated_database, suffix="hard-min"
    )
    policy_ref = _set_direct_policy(
        migrated_database, self_ref=self_ref, schedule_ref=schedule_ref, suffix="hard-min"
    )
    _duration(
        migrated_database,
        self_ref=self_ref,
        activity_ref=activity_ref,
        operation_id="operation:b04-e-hard-min",
        fingerprint="5" * 64,
        mutation="create",
        constraint_ref=uuid7(),
        expected_ref=None,
        resulting_ref=uuid7(),
        kind="minimum",
        strength="hard",
        microseconds=2 * 60 * 60 * 1_000_000,
    )

    requested_start = starts_at + timedelta(days=1)
    with _runtime(migrated_database) as connection:
        with pytest.raises(psycopg.errors.CheckViolation):
            connection.execute(
                _MOVE_SQL,
                (
                    self_ref,
                    "operation:b04-e-move-too-short",
                    "6" * 64,
                    schedule_ref,
                    placement_ref,
                    requested_start,
                    requested_start + timedelta(hours=1),
                    uuid7(),
                    uuid7(),
                ),
            ).fetchone()
        connection.rollback()
    assert _current_placement(migrated_database, schedule_ref) == placement_ref

    resulting_ref = uuid7()
    with _runtime(migrated_database) as connection:
        row = connection.execute(
            _MOVE_SQL,
            (
                self_ref,
                "operation:b04-e-move-long-enough",
                "8" * 64,
                schedule_ref,
                placement_ref,
                requested_start,
                requested_start + timedelta(hours=2),
                uuid7(),
                resulting_ref,
            ),
        ).fetchone()
        connection.commit()
    assert row is not None
    assert row[2] == policy_ref
    assert row[3] == "committed"
    assert row[5] == resulting_ref
    assert _current_placement(migrated_database, schedule_ref) == resulting_ref


@pytest.mark.postgres
def test_b04_e_soft_maximum_duration_does_not_block_automatic_move(
    migrated_database: Any,
) -> None:
    self_ref, activity_ref, schedule_ref, placement_ref, starts_at = _seed_scheduled_activity(
        migrated_database, suffix="soft-max"
    )
    _set_direct_policy(
        migrated_database, self_ref=self_ref, schedule_ref=schedule_ref, suffix="soft-max"
    )
    _duration(
        migrated_database,
        self_ref=self_ref,
        activity_ref=activity_ref,
        operation_id="operation:b04-e-soft-max",
        fingerprint="9" * 64,
        mutation="create",
        constraint_ref=uuid7(),
        expected_ref=None,
        resulting_ref=uuid7(),
        kind="maximum",
        strength="soft",
        microseconds=30 * 60 * 1_000_000,
    )

    resulting_ref = uuid7()
    requested_start = starts_at + timedelta(days=1)
    with _runtime(migrated_database) as connection:
        row = connection.execute(
            _MOVE_SQL,
            (
                self_ref,
                "operation:b04-e-soft-max-move",
                "a" * 64,
                schedule_ref,
                placement_ref,
                requested_start,
                requested_start + timedelta(hours=2),
                uuid7(),
                resulting_ref,
            ),
        ).fetchone()
        connection.commit()
    assert row is not None
    assert row[3] == "committed"
    assert row[5] == resulting_ref
