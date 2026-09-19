"""Real PostgreSQL proof for B04-B absolute boundary / deadline constraints."""

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
FROM dante.mutate_self_absolute_boundary_constraint(
    %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s
)
"""


def _seed_activity(database: Any) -> tuple[UUID, UUID]:
    self_person_ref = uuid7()
    activity_ref = uuid7()
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
            "INSERT INTO dante.person(person_ref) VALUES (%s)",
            (self_person_ref,),
        )
        connection.execute(
            "INSERT INTO dante.native_address(native_ref,owner_family) VALUES (%s,'person')",
            (self_person_ref,),
        )
        connection.execute(
            "INSERT INTO dante.activity(activity_ref) VALUES (%s)",
            (activity_ref,),
        )
        connection.execute(
            "INSERT INTO dante.native_address(native_ref,owner_family) VALUES (%s,'activity')",
            (activity_ref,),
        )
        connection.execute(
            """
            INSERT INTO dante.activity_intention(
                activity_ref,self_person_ref,title,created_at
            ) VALUES (%s,%s,'B04-B Activity',%s)
            """,
            (activity_ref, self_person_ref, now),
        )
        connection.commit()
    return self_person_ref, activity_ref


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
    boundary_kind_code: str | None,
    constrained_facet_code: str | None,
    strength_code: str | None,
    boundary_at: datetime | None,
) -> tuple[object, ...]:
    with psycopg.connect(
        **database.connection_kwargs(
            "dante_runtime",
            database.cluster.runtime_password,
        )
    ) as connection:
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
                boundary_kind_code,
                constrained_facet_code,
                strength_code,
                boundary_at,
            ),
        ).fetchone()
        connection.commit()
        assert row is not None
        return row


def _history(database: Any, constraint_ref: UUID) -> list[tuple[object, ...]]:
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
                   state.strength_code,
                   state.constrained_facet_code,
                   boundary.boundary_kind_code,
                   boundary.temporal_form_code,
                   payload.boundary_at,
                   history.current_until_at
              FROM dante.temporal_constraint_current_history AS history
              JOIN dante.temporal_constraint_state AS state
                ON state.constraint_ref=history.constraint_ref
               AND state.material_state_ref=history.material_state_ref
              JOIN dante.temporal_constraint_boundary_state AS boundary
                ON boundary.material_state_ref=state.material_state_ref
              JOIN dante.temporal_constraint_boundary_absolute_state AS payload
                ON payload.material_state_ref=state.material_state_ref
             WHERE history.constraint_ref=%s
             ORDER BY history.current_from_at
            """,
            (constraint_ref,),
        ).fetchall()


@pytest.mark.postgres
def test_b04_b_latest_start_to_deadline_preserves_history_cas_and_replay(
    migrated_database: Any,
) -> None:
    self_ref, activity_ref = _seed_activity(migrated_database)
    requested_constraint_ref = uuid7()
    first_state_ref = uuid7()
    latest_start = datetime(2026, 9, 25, 9, 0, tzinfo=UTC)

    created = _mutate(
        migrated_database,
        self_person_ref=self_ref,
        operation_id="operation:b04-b-latest-start",
        fingerprint="a" * 64,
        mutation_kind="create",
        subject_native_ref=activity_ref,
        constraint_ref=requested_constraint_ref,
        expected_material_state_ref=None,
        resulting_material_state_ref=first_state_ref,
        boundary_kind_code="latest_start",
        constrained_facet_code="schedule.start",
        strength_code="hard",
        boundary_at=latest_start,
    )
    assert created[0] == requested_constraint_ref
    assert created[2] == first_state_ref
    assert created[3] is True
    assert created[5] is False

    # Server-generated identity values may differ on retry; the operation receipt
    # remains the canonical accepted result.
    replay = _mutate(
        migrated_database,
        self_person_ref=self_ref,
        operation_id="operation:b04-b-latest-start",
        fingerprint="a" * 64,
        mutation_kind="create",
        subject_native_ref=activity_ref,
        constraint_ref=uuid7(),
        expected_material_state_ref=None,
        resulting_material_state_ref=uuid7(),
        boundary_kind_code="latest_start",
        constrained_facet_code="schedule.start",
        strength_code="hard",
        boundary_at=latest_start,
    )
    assert replay[0] == created[0]
    assert replay[2] == created[2]
    assert replay[4] == created[4]
    assert replay[5] is True

    deadline_state_ref = uuid7()
    deadline = latest_start + timedelta(days=2, hours=8)
    revised = _mutate(
        migrated_database,
        self_person_ref=self_ref,
        operation_id="operation:b04-b-deadline",
        fingerprint="b" * 64,
        mutation_kind="revise",
        subject_native_ref=activity_ref,
        constraint_ref=requested_constraint_ref,
        expected_material_state_ref=first_state_ref,
        resulting_material_state_ref=deadline_state_ref,
        boundary_kind_code="latest_completion",
        constrained_facet_code="schedule.completion",
        strength_code="soft",
        boundary_at=deadline,
    )
    assert revised[2] == deadline_state_ref
    assert revised[3] is True
    assert revised[5] is False

    with pytest.raises(psycopg.errors.UniqueViolation) as stale:
        _mutate(
            migrated_database,
            self_person_ref=self_ref,
            operation_id="operation:b04-b-stale",
            fingerprint="c" * 64,
            mutation_kind="revise",
            subject_native_ref=activity_ref,
            constraint_ref=requested_constraint_ref,
            expected_material_state_ref=first_state_ref,
            resulting_material_state_ref=uuid7(),
            boundary_kind_code="latest_start",
            constrained_facet_code="schedule.start",
            strength_code="hard",
            boundary_at=latest_start,
        )
    assert stale.value.diag.constraint_name == "temporal_constraint_state_conflict"

    history = _history(migrated_database, requested_constraint_ref)
    assert len(history) == 2
    assert history[0][0:6] == (
        first_state_ref,
        "hard",
        "schedule.start",
        "latest_start",
        "absolute",
        latest_start,
    )
    assert history[0][6] is not None
    assert history[1][0:6] == (
        deadline_state_ref,
        "soft",
        "schedule.completion",
        "latest_completion",
        "absolute",
        deadline,
    )
    assert history[1][6] is None


@pytest.mark.postgres
def test_b04_b_deferred_totality_rejects_invalid_boundary_kind_facet_pair(
    migrated_database: Any,
) -> None:
    _, activity_ref = _seed_activity(migrated_database)
    constraint_ref = uuid7()
    state_ref = uuid7()
    now = datetime.now(UTC)

    with psycopg.connect(
        **migrated_database.connection_kwargs(
            "dante_migrator",
            migrated_database.cluster.migrator_password,
        )
    ) as connection:
        connection.execute("SET ROLE dante_owner")
        connection.execute("SET search_path TO pg_catalog,dante,pg_temp")
        connection.execute(
            "INSERT INTO dante.temporal_constraint(constraint_ref,subject_native_ref) VALUES (%s,%s)",
            (constraint_ref, activity_ref),
        )
        connection.execute(
            "INSERT INTO dante.scoped_address(scoped_ref,scoped_family) VALUES (%s,'temporal_constraint')",
            (constraint_ref,),
        )
        connection.execute(
            """
            INSERT INTO dante.material_state_address(
                material_state_ref,native_owner_ref,scoped_owner_ref,facet_code
            ) VALUES (%s,NULL,%s,'temporal_constraint.rule')
            """,
            (state_ref, constraint_ref),
        )
        connection.execute(
            """
            INSERT INTO dante.temporal_constraint_state(
                material_state_ref,constraint_ref,family_code,strength_code,constrained_facet_code
            ) VALUES (%s,%s,'boundary','hard','schedule.completion')
            """,
            (state_ref, constraint_ref),
        )
        # latest_start may only constrain schedule.start; row-level enums accept
        # both values, so the deferred semantic totality trigger must reject this.
        connection.execute(
            """
            INSERT INTO dante.temporal_constraint_boundary_state(
                material_state_ref,boundary_kind_code,temporal_form_code
            ) VALUES (%s,'latest_start','absolute')
            """,
            (state_ref,),
        )
        connection.execute(
            """
            INSERT INTO dante.temporal_constraint_boundary_absolute_state(
                material_state_ref,boundary_at
            ) VALUES (%s,%s)
            """,
            (state_ref, now + timedelta(days=1)),
        )
        connection.execute(
            """
            INSERT INTO dante.scoped_current_material_state(
                scoped_owner_ref,facet_code,material_state_ref
            ) VALUES (%s,'temporal_constraint.rule',%s)
            """,
            (constraint_ref, state_ref),
        )
        connection.execute(
            """
            INSERT INTO dante.temporal_constraint_current_history(
                constraint_ref,material_state_ref,current_from_at,current_until_at
            ) VALUES (%s,%s,%s,NULL)
            """,
            (constraint_ref, state_ref, now),
        )

        with pytest.raises(psycopg.errors.CheckViolation) as rejected:
            connection.execute(
                "SET CONSTRAINTS ctrg_temporal_constraint_state_rule_totality IMMEDIATE"
            )
        assert rejected.value.diag.constraint_name == (
            "ctrg_temporal_constraint_state_rule_totality"
        )
        assert rejected.value.diag.message_primary == (
            "Temporal Constraint typed payload rejected"
        )
        connection.rollback()
