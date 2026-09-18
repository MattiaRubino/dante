"""Real PostgreSQL proof for the B04-A Temporal Constraint canonical core."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Any
from uuid import UUID, uuid7

import psycopg
import pytest

_MUTATE_SQL = """
SELECT constraint_ref,
       subject_native_ref,
       material_state_ref,
       active,
       created_at,
       replayed
FROM dante.mutate_self_absolute_earliest_start_constraint(
    %s,%s,%s,%s,%s,%s,%s,%s,%s,%s
)
"""


def _seed_self_subjects(database: Any) -> tuple[UUID, UUID, UUID, UUID]:
    self_person_ref = uuid7()
    other_person_ref = uuid7()
    activity_ref = uuid7()
    event_ref = uuid7()
    now = datetime.now(UTC)

    with psycopg.connect(
        **database.connection_kwargs(
            "dante_migrator",
            database.cluster.migrator_password,
        )
    ) as connection:
        connection.execute("SET ROLE dante_owner")
        connection.execute("SET search_path TO pg_catalog,dante,pg_temp")
        connection.execute(
            "INSERT INTO dante.person(person_ref) VALUES (%s),(%s)",
            (self_person_ref, other_person_ref),
        )
        connection.execute(
            """
            INSERT INTO dante.native_address(native_ref, owner_family)
            VALUES (%s,'person'),(%s,'person')
            """,
            (self_person_ref, other_person_ref),
        )

        connection.execute(
            "INSERT INTO dante.activity(activity_ref) VALUES (%s)",
            (activity_ref,),
        )
        connection.execute(
            "INSERT INTO dante.native_address(native_ref, owner_family) VALUES (%s,'activity')",
            (activity_ref,),
        )
        connection.execute(
            """
            INSERT INTO dante.activity_intention(
                activity_ref,self_person_ref,title,created_at
            ) VALUES (%s,%s,'B04 Activity',%s)
            """,
            (activity_ref, self_person_ref, now),
        )

        connection.execute(
            "INSERT INTO dante.event(event_ref) VALUES (%s)",
            (event_ref,),
        )
        connection.execute(
            "INSERT INTO dante.native_address(native_ref, owner_family) VALUES (%s,'event')",
            (event_ref,),
        )
        connection.execute(
            """
            INSERT INTO dante.event_expectation(
                event_ref,self_person_ref,title,created_at
            ) VALUES (%s,%s,'B04 Event',%s)
            """,
            (event_ref, self_person_ref, now),
        )
        connection.commit()

    return self_person_ref, other_person_ref, activity_ref, event_ref


def _mutate(
    database: Any,
    *,
    self_person_ref: UUID,
    operation_id: str,
    fingerprint: str,
    mutation_kind: str,
    subject_native_ref: UUID,
    constraint_ref: UUID,
    expected_material_state_ref: UUID | None,
    resulting_material_state_ref: UUID | None,
    strength_code: str | None,
    boundary_at: datetime | None,
) -> tuple[object, ...]:
    with psycopg.connect(
        **database.connection_kwargs(
            "dante_migrator",
            database.cluster.migrator_password,
        )
    ) as connection:
        connection.execute("SET ROLE dante_runtime")
        row = connection.execute(
            _MUTATE_SQL,
            (
                self_person_ref,
                operation_id,
                fingerprint,
                mutation_kind,
                subject_native_ref,
                constraint_ref,
                expected_material_state_ref,
                resulting_material_state_ref,
                strength_code,
                boundary_at,
            ),
        ).fetchone()
        connection.commit()
        assert row is not None
        return row


def _current_state(database: Any, constraint_ref: UUID) -> UUID | None:
    with psycopg.connect(
        **database.connection_kwargs(
            "dante_migrator",
            database.cluster.migrator_password,
        )
    ) as connection:
        connection.execute("SET ROLE dante_owner")
        row = connection.execute(
            """
            SELECT current.material_state_ref
            FROM dante.scoped_current_material_state AS current
            WHERE current.scoped_owner_ref=%s
              AND current.facet_code='temporal_constraint.rule'
            """,
            (constraint_ref,),
        ).fetchone()
        return None if row is None else row[0]


def _constraint_history(database: Any, constraint_ref: UUID) -> list[tuple[object, ...]]:
    with psycopg.connect(
        **database.connection_kwargs(
            "dante_migrator",
            database.cluster.migrator_password,
        )
    ) as connection:
        connection.execute("SET ROLE dante_owner")
        return connection.execute(
            """
            SELECT history.material_state_ref,
                   history.current_from_at,
                   history.current_until_at,
                   state.strength_code,
                   state.constrained_facet_code,
                   boundary.boundary_kind_code,
                   boundary.temporal_form_code,
                   payload.boundary_at
            FROM dante.temporal_constraint_current_history AS history
            JOIN dante.temporal_constraint_state AS state
              ON state.constraint_ref=history.constraint_ref
             AND state.material_state_ref=history.material_state_ref
            JOIN dante.temporal_constraint_boundary_state AS boundary
              ON boundary.material_state_ref=state.material_state_ref
            JOIN dante.temporal_constraint_boundary_absolute_state AS payload
              ON payload.material_state_ref=boundary.material_state_ref
            WHERE history.constraint_ref=%s
            ORDER BY history.current_from_at
            """,
            (constraint_ref,),
        ).fetchall()


@pytest.mark.postgres
def test_b04_constraint_create_revise_retire_is_monotonic_cas_and_idempotent(
    migrated_database: Any,
) -> None:
    self_ref, _, activity_ref, _ = _seed_self_subjects(migrated_database)
    constraint_ref = uuid7()
    first_state_ref = uuid7()
    second_state_ref = uuid7()
    first_boundary = datetime(2026, 9, 20, 16, 0, tzinfo=UTC)
    second_boundary = first_boundary + timedelta(hours=1)

    created = _mutate(
        migrated_database,
        self_person_ref=self_ref,
        operation_id="operation:b04-a-create",
        fingerprint="1" * 64,
        mutation_kind="create",
        subject_native_ref=activity_ref,
        constraint_ref=constraint_ref,
        expected_material_state_ref=None,
        resulting_material_state_ref=first_state_ref,
        strength_code="hard",
        boundary_at=first_boundary,
    )
    assert created[0] == constraint_ref
    assert created[1] == activity_ref
    assert created[2] == first_state_ref
    assert created[3] is True
    assert created[5] is False
    assert _current_state(migrated_database, constraint_ref) == first_state_ref

    replay = _mutate(
        migrated_database,
        self_person_ref=self_ref,
        operation_id="operation:b04-a-create",
        fingerprint="1" * 64,
        mutation_kind="create",
        subject_native_ref=activity_ref,
        constraint_ref=constraint_ref,
        expected_material_state_ref=None,
        resulting_material_state_ref=first_state_ref,
        strength_code="hard",
        boundary_at=first_boundary,
    )
    assert replay[0:4] == created[0:4]
    assert replay[4] == created[4]
    assert replay[5] is True

    with pytest.raises(psycopg.errors.UniqueViolation):
        _mutate(
            migrated_database,
            self_person_ref=self_ref,
            operation_id="operation:b04-a-create",
            fingerprint="1" * 64,
            mutation_kind="create",
            subject_native_ref=activity_ref,
            constraint_ref=constraint_ref,
            expected_material_state_ref=None,
            resulting_material_state_ref=first_state_ref,
            strength_code="soft",
            boundary_at=first_boundary,
        )

    revised = _mutate(
        migrated_database,
        self_person_ref=self_ref,
        operation_id="operation:b04-a-revise",
        fingerprint="2" * 64,
        mutation_kind="revise",
        subject_native_ref=activity_ref,
        constraint_ref=constraint_ref,
        expected_material_state_ref=first_state_ref,
        resulting_material_state_ref=second_state_ref,
        strength_code="soft",
        boundary_at=second_boundary,
    )
    assert revised[2] == second_state_ref
    assert revised[3] is True
    assert revised[5] is False
    assert _current_state(migrated_database, constraint_ref) == second_state_ref

    with pytest.raises(psycopg.errors.UniqueViolation):
        _mutate(
            migrated_database,
            self_person_ref=self_ref,
            operation_id="operation:b04-a-stale",
            fingerprint="3" * 64,
            mutation_kind="revise",
            subject_native_ref=activity_ref,
            constraint_ref=constraint_ref,
            expected_material_state_ref=first_state_ref,
            resulting_material_state_ref=uuid7(),
            strength_code="hard",
            boundary_at=first_boundary,
        )

    retired = _mutate(
        migrated_database,
        self_person_ref=self_ref,
        operation_id="operation:b04-a-retire",
        fingerprint="4" * 64,
        mutation_kind="retire",
        subject_native_ref=activity_ref,
        constraint_ref=constraint_ref,
        expected_material_state_ref=second_state_ref,
        resulting_material_state_ref=None,
        strength_code=None,
        boundary_at=None,
    )
    assert retired[2] is None
    assert retired[3] is False
    assert retired[5] is False
    assert _current_state(migrated_database, constraint_ref) is None

    history = _constraint_history(migrated_database, constraint_ref)
    assert len(history) == 2
    assert history[0][0] == first_state_ref
    assert history[0][2] is not None
    assert history[0][3:] == (
        "hard",
        "schedule.start",
        "earliest_start",
        "absolute",
        first_boundary,
    )
    assert history[1][0] == second_state_ref
    assert history[1][2] is not None
    assert history[1][3:] == (
        "soft",
        "schedule.start",
        "earliest_start",
        "absolute",
        second_boundary,
    )

    with psycopg.connect(
        **migrated_database.connection_kwargs(
            "dante_migrator",
            migrated_database.cluster.migrator_password,
        )
    ) as connection:
        connection.execute("SET ROLE dante_owner")
        state_count = connection.execute(
            "SELECT count(*) FROM dante.temporal_constraint_state WHERE constraint_ref=%s",
            (constraint_ref,),
        ).fetchone()
        receipt_count = connection.execute(
            "SELECT count(*) FROM dante.temporal_constraint_mutation_operation WHERE constraint_ref=%s",
            (constraint_ref,),
        ).fetchone()
        assert state_count == (2,)
        assert receipt_count == (3,)


@pytest.mark.postgres
def test_b04_constraint_accepts_self_event_and_rejects_cross_self_activity(
    migrated_database: Any,
) -> None:
    self_ref, other_ref, activity_ref, event_ref = _seed_self_subjects(migrated_database)
    event_constraint_ref = uuid7()
    event_state_ref = uuid7()
    boundary = datetime(2026, 9, 21, 8, 30, tzinfo=UTC)

    event_created = _mutate(
        migrated_database,
        self_person_ref=self_ref,
        operation_id="operation:b04-a-event-create",
        fingerprint="5" * 64,
        mutation_kind="create",
        subject_native_ref=event_ref,
        constraint_ref=event_constraint_ref,
        expected_material_state_ref=None,
        resulting_material_state_ref=event_state_ref,
        strength_code="hard",
        boundary_at=boundary,
    )
    assert event_created[1] == event_ref
    assert event_created[2] == event_state_ref
    assert _current_state(migrated_database, event_constraint_ref) == event_state_ref

    with pytest.raises(psycopg.errors.ForeignKeyViolation):
        _mutate(
            migrated_database,
            self_person_ref=other_ref,
            operation_id="operation:b04-a-cross-self",
            fingerprint="6" * 64,
            mutation_kind="create",
            subject_native_ref=activity_ref,
            constraint_ref=uuid7(),
            expected_material_state_ref=None,
            resulting_material_state_ref=uuid7(),
            strength_code="hard",
            boundary_at=boundary,
        )


@pytest.mark.postgres
def test_b04_constraint_runtime_cannot_bypass_governed_mutation_function(
    migrated_database: Any,
) -> None:
    self_ref, _, activity_ref, _ = _seed_self_subjects(migrated_database)
    constraint_ref = uuid7()

    with psycopg.connect(
        **migrated_database.connection_kwargs(
            "dante_migrator",
            migrated_database.cluster.migrator_password,
        )
    ) as connection:
        connection.execute("SET ROLE dante_runtime")
        with pytest.raises(psycopg.errors.InsufficientPrivilege):
            connection.execute(
                "INSERT INTO dante.temporal_constraint(constraint_ref,subject_native_ref) VALUES (%s,%s)",
                (constraint_ref, activity_ref),
            )

    created = _mutate(
        migrated_database,
        self_person_ref=self_ref,
        operation_id="operation:b04-a-governed",
        fingerprint="7" * 64,
        mutation_kind="create",
        subject_native_ref=activity_ref,
        constraint_ref=constraint_ref,
        expected_material_state_ref=None,
        resulting_material_state_ref=uuid7(),
        strength_code="hard",
        boundary_at=datetime(2026, 9, 22, 7, 0, tzinfo=UTC),
    )
    assert created[0] == constraint_ref
    assert created[5] is False
