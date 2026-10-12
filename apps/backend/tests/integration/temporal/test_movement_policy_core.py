"""Real PostgreSQL proof for the B04-D Movement Policy canonical core."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Any
from uuid import UUID, uuid7

import psycopg
import pytest

_MUTATE_SQL = """
SELECT schedule_ref, material_state_ref, active, created_at, replayed
FROM dante.mutate_self_schedule_movement_policy(%s,%s,%s,%s,%s,%s,%s,%s,%s)
"""


def _seed_scheduled_activity(database: Any) -> tuple[UUID, UUID, UUID]:
    self_person_ref = uuid7()
    activity_ref = uuid7()
    schedule_ref = uuid7()
    placement_state_ref = uuid7()
    now = datetime.now(UTC)
    starts_at = now + timedelta(days=1)
    ends_at = starts_at + timedelta(hours=1)

    with psycopg.connect(
        **database.connection_kwargs("dante_migrator", database.cluster.migrator_password)
    ) as connection:
        connection.execute("SET ROLE dante_owner")
        connection.execute("SET search_path TO pg_catalog,dante,pg_temp")
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
            VALUES (%s,%s,'B04-D Activity',%s)
            """,
            (activity_ref, self_person_ref, now),
        )
        connection.commit()

    with psycopg.connect(
        **database.connection_kwargs("dante_runtime", database.cluster.runtime_password)
    ) as connection:
        row = connection.execute(
            """
            SELECT schedule_ref, material_state_ref
              FROM dante.establish_self_schedule_placement(
                   %s,%s,%s,%s,%s,%s,%s::jsonb
              )
            """,
            (
                self_person_ref,
                "operation:b04-d-establish",
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
    assert row is not None
    assert row[0] == schedule_ref
    assert row[1] == placement_state_ref
    return self_person_ref, schedule_ref, placement_state_ref


def _mutate(
    database: Any,
    *,
    self_person_ref: UUID,
    operation_id: str,
    fingerprint: str,
    mutation_kind: str,
    schedule_ref: UUID,
    expected_material_state_ref: UUID | None,
    resulting_material_state_ref: UUID | None,
    automatic_movement_code: str | None,
    acceptance_path_code: str | None,
) -> tuple[object, ...]:
    with psycopg.connect(
        **database.connection_kwargs("dante_runtime", database.cluster.runtime_password)
    ) as connection:
        row = connection.execute(
            _MUTATE_SQL,
            (
                self_person_ref,
                operation_id,
                fingerprint,
                mutation_kind,
                schedule_ref,
                expected_material_state_ref,
                resulting_material_state_ref,
                automatic_movement_code,
                acceptance_path_code,
            ),
        ).fetchone()
        connection.commit()
    assert row is not None
    return row


@pytest.mark.postgres
def test_b04_d_policy_create_revise_retire_is_independent_from_schedule_placement(
    migrated_database: Any,
) -> None:
    self_ref, schedule_ref, placement_state_ref = _seed_scheduled_activity(migrated_database)
    locked_state_ref = uuid7()

    created = _mutate(
        migrated_database,
        self_person_ref=self_ref,
        operation_id="operation:b04-d-policy-create",
        fingerprint="a" * 64,
        mutation_kind="create",
        schedule_ref=schedule_ref,
        expected_material_state_ref=None,
        resulting_material_state_ref=locked_state_ref,
        automatic_movement_code="blocked",
        acceptance_path_code="direct",
    )
    assert created[1] == locked_state_ref
    assert created[2] is True
    assert created[4] is False

    replay = _mutate(
        migrated_database,
        self_person_ref=self_ref,
        operation_id="operation:b04-d-policy-create",
        fingerprint="a" * 64,
        mutation_kind="create",
        schedule_ref=schedule_ref,
        expected_material_state_ref=None,
        resulting_material_state_ref=uuid7(),
        automatic_movement_code="blocked",
        acceptance_path_code="direct",
    )
    assert replay[1] == locked_state_ref
    assert replay[4] is True

    confirmation_state_ref = uuid7()
    revised = _mutate(
        migrated_database,
        self_person_ref=self_ref,
        operation_id="operation:b04-d-policy-revise",
        fingerprint="b" * 64,
        mutation_kind="revise",
        schedule_ref=schedule_ref,
        expected_material_state_ref=locked_state_ref,
        resulting_material_state_ref=confirmation_state_ref,
        automatic_movement_code="automatic",
        acceptance_path_code="confirmation_required",
    )
    assert revised[1] == confirmation_state_ref

    retired = _mutate(
        migrated_database,
        self_person_ref=self_ref,
        operation_id="operation:b04-d-policy-retire",
        fingerprint="c" * 64,
        mutation_kind="retire",
        schedule_ref=schedule_ref,
        expected_material_state_ref=confirmation_state_ref,
        resulting_material_state_ref=None,
        automatic_movement_code=None,
        acceptance_path_code=None,
    )
    assert retired[1] is None
    assert retired[2] is False

    with psycopg.connect(
        **migrated_database.connection_kwargs("dante_migrator", migrated_database.cluster.migrator_password)
    ) as connection:
        connection.execute("SET ROLE dante_owner")
        placement_current = connection.execute(
            """
            SELECT material_state_ref
              FROM dante.scoped_current_material_state
             WHERE scoped_owner_ref=%s AND facet_code='schedule.placement'
            """,
            (schedule_ref,),
        ).fetchone()
        policy_history = connection.execute(
            """
            SELECT state.material_state_ref,
                   state.automatic_movement_code,
                   state.acceptance_path_code,
                   history.current_until_at
              FROM dante.schedule_movement_policy_current_history AS history
              JOIN dante.schedule_movement_policy_state AS state
                ON state.schedule_ref=history.schedule_ref
               AND state.material_state_ref=history.material_state_ref
             WHERE history.schedule_ref=%s
             ORDER BY history.current_from_at
            """,
            (schedule_ref,),
        ).fetchall()
    assert placement_current == (placement_state_ref,)
    assert len(policy_history) == 2
    assert policy_history[0][0:3] == (locked_state_ref, "blocked", "direct")
    assert policy_history[0][3] is not None
    assert policy_history[1][0:3] == (
        confirmation_state_ref,
        "automatic",
        "confirmation_required",
    )
    assert policy_history[1][3] is not None


@pytest.mark.postgres
def test_b04_d_policy_expected_state_conflict_and_blocked_shape_fail_closed(
    migrated_database: Any,
) -> None:
    self_ref, schedule_ref, _ = _seed_scheduled_activity(migrated_database)
    state_ref = uuid7()
    _mutate(
        migrated_database,
        self_person_ref=self_ref,
        operation_id="operation:b04-d-policy-create-conflict",
        fingerprint="d" * 64,
        mutation_kind="create",
        schedule_ref=schedule_ref,
        expected_material_state_ref=None,
        resulting_material_state_ref=state_ref,
        automatic_movement_code="automatic",
        acceptance_path_code="direct",
    )

    with pytest.raises(psycopg.errors.UniqueViolation) as stale:
        _mutate(
            migrated_database,
            self_person_ref=self_ref,
            operation_id="operation:b04-d-policy-stale",
            fingerprint="f" * 64,
            mutation_kind="revise",
            schedule_ref=schedule_ref,
            expected_material_state_ref=uuid7(),
            resulting_material_state_ref=uuid7(),
            automatic_movement_code="automatic",
            acceptance_path_code="direct",
        )
    assert stale.value.diag.constraint_name == "movement_policy_state_conflict"

    with pytest.raises(psycopg.errors.CheckViolation):
        _mutate(
            migrated_database,
            self_person_ref=self_ref,
            operation_id="operation:b04-d-policy-invalid-shape",
            fingerprint="1" * 64,
            mutation_kind="revise",
            schedule_ref=schedule_ref,
            expected_material_state_ref=state_ref,
            resulting_material_state_ref=uuid7(),
            automatic_movement_code="blocked",
            acceptance_path_code="confirmation_required",
        )
