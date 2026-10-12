"""Real PostgreSQL proof for the B04-D governed automatic Schedule move path."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Any
from uuid import UUID, uuid7

import psycopg
import pytest

_POLICY_SQL = """
SELECT schedule_ref, material_state_ref, active, created_at, replayed
FROM dante.mutate_self_schedule_movement_policy(%s,%s,%s,%s,%s,%s,%s,%s,%s)
"""

_REQUEST_SQL = """
SELECT schedule_ref,
       subject_native_ref,
       movement_policy_material_state_ref,
       result_kind,
       proposal_ref,
       placement_material_state_ref,
       created_at,
       replayed
FROM dante.request_self_absolute_schedule_move(%s,%s,%s,%s,%s,%s,%s,%s,%s)
"""

_ACCEPT_SQL = """
SELECT proposal_ref,
       schedule_ref,
       subject_native_ref,
       previous_placement_material_state_ref,
       placement_material_state_ref,
       created_at,
       replayed
FROM dante.accept_self_absolute_schedule_move_proposal(%s,%s,%s,%s,%s)
"""

_BOUNDARY_SQL = """
SELECT constraint_ref, subject_native_ref, material_state_ref, active, created_at, replayed
FROM dante.mutate_self_absolute_boundary_constraint(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
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


def _seed_scheduled_activity(database: Any, *, suffix: str) -> tuple[UUID, UUID, UUID, UUID, datetime, datetime]:
    self_person_ref = uuid7()
    activity_ref = uuid7()
    schedule_ref = uuid7()
    placement_state_ref = uuid7()
    now = datetime.now(UTC)
    starts_at = now + timedelta(days=1)
    ends_at = starts_at + timedelta(hours=1)

    with _owner(database) as connection:
        connection.execute("INSERT INTO dante.person(person_ref) VALUES (%s)", (self_person_ref,))
        connection.execute(
            "INSERT INTO dante.native_address(native_ref,owner_family) VALUES (%s,'person')",
            (self_person_ref,),
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
            (activity_ref, self_person_ref, f"B04-D governed {suffix}", now),
        )
        connection.commit()

    with _runtime(database) as connection:
        row = connection.execute(
            """
            SELECT schedule_ref, material_state_ref
              FROM dante.establish_self_schedule_placement(%s,%s,%s,%s,%s,%s,%s::jsonb)
            """,
            (
                self_person_ref,
                f"operation:b04-d-establish-{suffix}",
                "e" * 64,
                activity_ref,
                schedule_ref,
                placement_state_ref,
                '{"kind":"absolute_interval","starts_at":"'
                + starts_at.isoformat()
                + '","ends_at":"'
                + ends_at.isoformat()
                + '"}',
            ),
        ).fetchone()
        connection.commit()
    assert row == (schedule_ref, placement_state_ref)
    return self_person_ref, activity_ref, schedule_ref, placement_state_ref, starts_at, ends_at


def _set_policy(
    database: Any,
    *,
    self_ref: UUID,
    schedule_ref: UUID,
    operation_id: str,
    fingerprint: str,
    expected_ref: UUID | None,
    resulting_ref: UUID,
    automatic: str,
    acceptance: str,
) -> tuple[object, ...]:
    with _runtime(database) as connection:
        row = connection.execute(
            _POLICY_SQL,
            (
                self_ref,
                operation_id,
                fingerprint,
                "create" if expected_ref is None else "revise",
                schedule_ref,
                expected_ref,
                resulting_ref,
                automatic,
                acceptance,
            ),
        ).fetchone()
        connection.commit()
    assert row is not None
    return row


def _request_move(
    database: Any,
    *,
    self_ref: UUID,
    operation_id: str,
    fingerprint: str,
    schedule_ref: UUID,
    expected_placement_ref: UUID,
    starts_at: datetime,
    ends_at: datetime,
    proposal_ref: UUID,
    resulting_ref: UUID,
) -> tuple[object, ...]:
    with _runtime(database) as connection:
        row = connection.execute(
            _REQUEST_SQL,
            (
                self_ref,
                operation_id,
                fingerprint,
                schedule_ref,
                expected_placement_ref,
                starts_at,
                ends_at,
                proposal_ref,
                resulting_ref,
            ),
        ).fetchone()
        connection.commit()
    assert row is not None
    return row


def _accept_move(
    database: Any,
    *,
    self_ref: UUID,
    operation_id: str,
    fingerprint: str,
    proposal_ref: UUID,
    resulting_ref: UUID,
) -> tuple[object, ...]:
    with _runtime(database) as connection:
        row = connection.execute(
            _ACCEPT_SQL,
            (self_ref, operation_id, fingerprint, proposal_ref, resulting_ref),
        ).fetchone()
        connection.commit()
    assert row is not None
    return row


def _add_boundary(
    database: Any,
    *,
    self_ref: UUID,
    activity_ref: UUID,
    strength: str,
    boundary_at: datetime,
    suffix: str,
) -> None:
    with _runtime(database) as connection:
        row = connection.execute(
            _BOUNDARY_SQL,
            (
                self_ref,
                f"operation:b04-d-boundary-{suffix}",
                ("a" if strength == "hard" else "b") * 64,
                "create",
                activity_ref,
                uuid7(),
                None,
                uuid7(),
                "latest_start",
                "schedule.start",
                strength,
                boundary_at,
            ),
        ).fetchone()
        connection.commit()
    assert row is not None


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
def test_b04_d_direct_move_commits_monotonic_placement_and_replays(
    migrated_database: Any,
) -> None:
    self_ref, _, schedule_ref, placement_ref, starts_at, _ = _seed_scheduled_activity(
        migrated_database, suffix="direct"
    )
    policy_ref = uuid7()
    _set_policy(
        migrated_database,
        self_ref=self_ref,
        schedule_ref=schedule_ref,
        operation_id="operation:b04-d-policy-direct",
        fingerprint="1" * 64,
        expected_ref=None,
        resulting_ref=policy_ref,
        automatic="automatic",
        acceptance="direct",
    )

    requested_start = starts_at + timedelta(days=1)
    requested_end = requested_start + timedelta(hours=2)
    resulting_ref = uuid7()
    moved = _request_move(
        migrated_database,
        self_ref=self_ref,
        operation_id="operation:b04-d-move-direct",
        fingerprint="2" * 64,
        schedule_ref=schedule_ref,
        expected_placement_ref=placement_ref,
        starts_at=requested_start,
        ends_at=requested_end,
        proposal_ref=uuid7(),
        resulting_ref=resulting_ref,
    )
    assert moved[0] == schedule_ref
    assert moved[2] == policy_ref
    assert moved[3] == "committed"
    assert moved[4] is None
    assert moved[5] == resulting_ref
    assert moved[7] is False
    assert _current_placement(migrated_database, schedule_ref) == resulting_ref

    replay = _request_move(
        migrated_database,
        self_ref=self_ref,
        operation_id="operation:b04-d-move-direct",
        fingerprint="2" * 64,
        schedule_ref=schedule_ref,
        expected_placement_ref=placement_ref,
        starts_at=requested_start,
        ends_at=requested_end,
        proposal_ref=uuid7(),
        resulting_ref=uuid7(),
    )
    assert replay[3] == "committed"
    assert replay[5] == resulting_ref
    assert replay[7] is True

    with _owner(migrated_database) as connection:
        history = connection.execute(
            """
            SELECT material_state_ref,current_until_at
              FROM dante.schedule_placement_current_history
             WHERE schedule_ref=%s
             ORDER BY current_from_at
            """,
            (schedule_ref,),
        ).fetchall()
    assert len(history) == 2
    assert history[0][0] == placement_ref and history[0][1] is not None
    assert history[1] == (resulting_ref, None)


@pytest.mark.postgres
def test_b04_d_confirmation_requires_fresh_placement_and_policy_basis(
    migrated_database: Any,
) -> None:
    self_ref, _, schedule_ref, placement_ref, starts_at, _ = _seed_scheduled_activity(
        migrated_database, suffix="confirmation"
    )
    policy_ref = uuid7()
    _set_policy(
        migrated_database,
        self_ref=self_ref,
        schedule_ref=schedule_ref,
        operation_id="operation:b04-d-policy-confirm",
        fingerprint="3" * 64,
        expected_ref=None,
        resulting_ref=policy_ref,
        automatic="automatic",
        acceptance="confirmation_required",
    )

    requested_start = starts_at + timedelta(days=2)
    requested_end = requested_start + timedelta(hours=1)
    proposal_ref = uuid7()
    pending = _request_move(
        migrated_database,
        self_ref=self_ref,
        operation_id="operation:b04-d-move-proposal",
        fingerprint="4" * 64,
        schedule_ref=schedule_ref,
        expected_placement_ref=placement_ref,
        starts_at=requested_start,
        ends_at=requested_end,
        proposal_ref=proposal_ref,
        resulting_ref=uuid7(),
    )
    assert pending[3] == "pending_confirmation"
    assert pending[4] == proposal_ref
    assert pending[5] is None
    assert pending[7] is False
    assert _current_placement(migrated_database, schedule_ref) == placement_ref

    resulting_ref = uuid7()
    accepted = _accept_move(
        migrated_database,
        self_ref=self_ref,
        operation_id="operation:b04-d-accept-proposal",
        fingerprint="5" * 64,
        proposal_ref=proposal_ref,
        resulting_ref=resulting_ref,
    )
    assert accepted[0] == proposal_ref
    assert accepted[1] == schedule_ref
    assert accepted[3] == placement_ref
    assert accepted[4] == resulting_ref
    assert accepted[6] is False
    assert _current_placement(migrated_database, schedule_ref) == resulting_ref

    replay = _accept_move(
        migrated_database,
        self_ref=self_ref,
        operation_id="operation:b04-d-accept-proposal",
        fingerprint="5" * 64,
        proposal_ref=proposal_ref,
        resulting_ref=uuid7(),
    )
    assert replay[4] == resulting_ref
    assert replay[6] is True

    self_ref2, _, schedule_ref2, placement_ref2, starts_at2, _ = _seed_scheduled_activity(
        migrated_database, suffix="policy-stale"
    )
    initial_policy_ref = uuid7()
    _set_policy(
        migrated_database,
        self_ref=self_ref2,
        schedule_ref=schedule_ref2,
        operation_id="operation:b04-d-policy-stale-create",
        fingerprint="6" * 64,
        expected_ref=None,
        resulting_ref=initial_policy_ref,
        automatic="automatic",
        acceptance="confirmation_required",
    )
    stale_proposal_ref = uuid7()
    _request_move(
        migrated_database,
        self_ref=self_ref2,
        operation_id="operation:b04-d-policy-stale-request",
        fingerprint="7" * 64,
        schedule_ref=schedule_ref2,
        expected_placement_ref=placement_ref2,
        starts_at=starts_at2 + timedelta(days=1),
        ends_at=starts_at2 + timedelta(days=1, hours=1),
        proposal_ref=stale_proposal_ref,
        resulting_ref=uuid7(),
    )
    _set_policy(
        migrated_database,
        self_ref=self_ref2,
        schedule_ref=schedule_ref2,
        operation_id="operation:b04-d-policy-stale-revise",
        fingerprint="8" * 64,
        expected_ref=initial_policy_ref,
        resulting_ref=uuid7(),
        automatic="automatic",
        acceptance="direct",
    )
    with pytest.raises(psycopg.errors.UniqueViolation) as stale_policy:
        _accept_move(
            migrated_database,
            self_ref=self_ref2,
            operation_id="operation:b04-d-policy-stale-accept",
            fingerprint="9" * 64,
            proposal_ref=stale_proposal_ref,
            resulting_ref=uuid7(),
        )
    assert stale_policy.value.diag.constraint_name == "schedule_move_policy_state"
    assert _current_placement(migrated_database, schedule_ref2) == placement_ref2


@pytest.mark.postgres
def test_b04_d_hard_constraints_block_automatic_move_while_soft_preferences_do_not(
    migrated_database: Any,
) -> None:
    self_ref, activity_ref, schedule_ref, placement_ref, starts_at, _ = _seed_scheduled_activity(
        migrated_database, suffix="hard"
    )
    _set_policy(
        migrated_database,
        self_ref=self_ref,
        schedule_ref=schedule_ref,
        operation_id="operation:b04-d-policy-hard",
        fingerprint="c" * 64,
        expected_ref=None,
        resulting_ref=uuid7(),
        automatic="automatic",
        acceptance="direct",
    )
    candidate_start = starts_at + timedelta(days=3)
    candidate_end = candidate_start + timedelta(hours=1)
    _add_boundary(
        migrated_database,
        self_ref=self_ref,
        activity_ref=activity_ref,
        strength="hard",
        boundary_at=candidate_start - timedelta(hours=1),
        suffix="hard",
    )
    with pytest.raises(psycopg.errors.CheckViolation) as violation:
        _request_move(
            migrated_database,
            self_ref=self_ref,
            operation_id="operation:b04-d-hard-block",
            fingerprint="d" * 64,
            schedule_ref=schedule_ref,
            expected_placement_ref=placement_ref,
            starts_at=candidate_start,
            ends_at=candidate_end,
            proposal_ref=uuid7(),
            resulting_ref=uuid7(),
        )
    assert violation.value.diag.constraint_name == "schedule_move_hard_constraint_violation"
    assert _current_placement(migrated_database, schedule_ref) == placement_ref

    self_ref2, activity_ref2, schedule_ref2, placement_ref2, starts_at2, _ = _seed_scheduled_activity(
        migrated_database, suffix="soft"
    )
    _set_policy(
        migrated_database,
        self_ref=self_ref2,
        schedule_ref=schedule_ref2,
        operation_id="operation:b04-d-policy-soft",
        fingerprint="e" * 64,
        expected_ref=None,
        resulting_ref=uuid7(),
        automatic="automatic",
        acceptance="direct",
    )
    soft_candidate_start = starts_at2 + timedelta(days=3)
    soft_candidate_end = soft_candidate_start + timedelta(hours=1)
    _add_boundary(
        migrated_database,
        self_ref=self_ref2,
        activity_ref=activity_ref2,
        strength="soft",
        boundary_at=soft_candidate_start - timedelta(hours=1),
        suffix="soft",
    )
    soft_result_ref = uuid7()
    moved = _request_move(
        migrated_database,
        self_ref=self_ref2,
        operation_id="operation:b04-d-soft-allowed",
        fingerprint="f" * 64,
        schedule_ref=schedule_ref2,
        expected_placement_ref=placement_ref2,
        starts_at=soft_candidate_start,
        ends_at=soft_candidate_end,
        proposal_ref=uuid7(),
        resulting_ref=soft_result_ref,
    )
    assert moved[3] == "committed"
    assert moved[5] == soft_result_ref
    assert _current_placement(migrated_database, schedule_ref2) == soft_result_ref
