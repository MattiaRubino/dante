"""Real PostgreSQL proof for B04-C absolute window Temporal Constraints."""

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
FROM dante.mutate_self_absolute_window_constraint(
    %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s
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
            VALUES (%s,%s,'B04-C Activity',%s)
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
    relationship_code: str | None,
    constrained_facet_code: str | None,
    strength_code: str | None,
    starts_at: datetime | None,
    ends_at: datetime | None,
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
                relationship_code,
                constrained_facet_code,
                strength_code,
                starts_at,
                ends_at,
            ),
        ).fetchone()
        connection.commit()
        assert row is not None
        return row


@pytest.mark.postgres
def test_b04_c_window_create_revise_and_replay_preserve_typed_history(
    migrated_database: Any,
) -> None:
    self_ref, activity_ref = _seed_activity(migrated_database)
    constraint_ref = uuid7()
    first_state_ref = uuid7()
    starts_at = datetime(2026, 10, 1, 8, 0, tzinfo=UTC)
    ends_at = starts_at + timedelta(hours=4)

    created = _mutate(
        migrated_database,
        self_person_ref=self_ref,
        operation_id="operation:b04-c-window-create",
        fingerprint="a" * 64,
        mutation_kind="create",
        subject_native_ref=activity_ref,
        constraint_ref=constraint_ref,
        expected_material_state_ref=None,
        resulting_material_state_ref=first_state_ref,
        relationship_code="start_within",
        constrained_facet_code="schedule.start",
        strength_code="soft",
        starts_at=starts_at,
        ends_at=ends_at,
    )
    assert created[0] == constraint_ref
    assert created[2] == first_state_ref
    assert created[3] is True
    assert created[5] is False

    replay = _mutate(
        migrated_database,
        self_person_ref=self_ref,
        operation_id="operation:b04-c-window-create",
        fingerprint="a" * 64,
        mutation_kind="create",
        subject_native_ref=activity_ref,
        constraint_ref=uuid7(),
        expected_material_state_ref=None,
        resulting_material_state_ref=uuid7(),
        relationship_code="start_within",
        constrained_facet_code="schedule.start",
        strength_code="soft",
        starts_at=starts_at,
        ends_at=ends_at,
    )
    assert replay[0] == constraint_ref
    assert replay[2] == first_state_ref
    assert replay[5] is True

    second_state_ref = uuid7()
    revised = _mutate(
        migrated_database,
        self_person_ref=self_ref,
        operation_id="operation:b04-c-window-revise",
        fingerprint="b" * 64,
        mutation_kind="revise",
        subject_native_ref=activity_ref,
        constraint_ref=constraint_ref,
        expected_material_state_ref=first_state_ref,
        resulting_material_state_ref=second_state_ref,
        relationship_code="full_placement_contained",
        constrained_facet_code="schedule.placement",
        strength_code="hard",
        starts_at=starts_at + timedelta(hours=1),
        ends_at=ends_at + timedelta(hours=2),
    )
    assert revised[2] == second_state_ref

    with psycopg.connect(
        **migrated_database.connection_kwargs(
            "dante_migrator",
            migrated_database.cluster.migrator_password,
        )
    ) as connection:
        connection.execute("SET ROLE dante_owner")
        rows = connection.execute(
            """
            SELECT history.material_state_ref,
                   state.family_code,
                   state.strength_code,
                   state.constrained_facet_code,
                   window_state.relationship_code,
                   window_state.temporal_form_code,
                   payload.starts_at,
                   payload.ends_at,
                   history.current_until_at
              FROM dante.temporal_constraint_current_history AS history
              JOIN dante.temporal_constraint_state AS state
                ON state.constraint_ref=history.constraint_ref
               AND state.material_state_ref=history.material_state_ref
              JOIN dante.temporal_constraint_window_state AS window_state
                ON window_state.material_state_ref=state.material_state_ref
              JOIN dante.temporal_constraint_window_absolute_state AS payload
                ON payload.material_state_ref=state.material_state_ref
             WHERE history.constraint_ref=%s
             ORDER BY history.current_from_at
            """,
            (constraint_ref,),
        ).fetchall()
    assert len(rows) == 2
    assert rows[0][0:8] == (
        first_state_ref,
        "window",
        "soft",
        "schedule.start",
        "start_within",
        "absolute",
        starts_at,
        ends_at,
    )
    assert rows[0][8] is not None
    assert rows[1][0:6] == (
        second_state_ref,
        "window",
        "hard",
        "schedule.placement",
        "full_placement_contained",
        "absolute",
    )
    assert rows[1][8] is None


@pytest.mark.postgres
def test_b04_c_window_totality_rejects_relation_facet_mismatch(
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
            INSERT INTO dante.material_state_address(material_state_ref,native_owner_ref,scoped_owner_ref,facet_code)
            VALUES (%s,NULL,%s,'temporal_constraint.rule')
            """,
            (state_ref, constraint_ref),
        )
        connection.execute(
            """
            INSERT INTO dante.temporal_constraint_state(
                material_state_ref,constraint_ref,family_code,strength_code,constrained_facet_code
            ) VALUES (%s,%s,'window','hard','schedule.completion')
            """,
            (state_ref, constraint_ref),
        )
        connection.execute(
            """
            INSERT INTO dante.temporal_constraint_window_state(
                material_state_ref,relationship_code,temporal_form_code
            ) VALUES (%s,'start_within','absolute')
            """,
            (state_ref,),
        )
        connection.execute(
            """
            INSERT INTO dante.temporal_constraint_window_absolute_state(material_state_ref,starts_at,ends_at)
            VALUES (%s,%s,%s)
            """,
            (state_ref, now, now + timedelta(hours=1)),
        )
        with pytest.raises(psycopg.errors.CheckViolation) as rejected:
            connection.execute(
                "SET CONSTRAINTS ctrg_temporal_constraint_window_state_rule_totality IMMEDIATE"
            )
        assert rejected.value.diag.constraint_name == (
            "ctrg_temporal_constraint_window_state_rule_totality"
        )
        assert rejected.value.diag.message_primary == "Temporal Constraint typed payload rejected"
        connection.rollback()


@pytest.mark.postgres
def test_b04_c_window_row_shape_requires_positive_finite_interval(
    migrated_database: Any,
) -> None:
    self_ref, activity_ref = _seed_activity(migrated_database)
    with pytest.raises(psycopg.errors.CheckViolation):
        _mutate(
            migrated_database,
            self_person_ref=self_ref,
            operation_id="operation:b04-c-window-invalid-interval",
            fingerprint="c" * 64,
            mutation_kind="create",
            subject_native_ref=activity_ref,
            constraint_ref=uuid7(),
            expected_material_state_ref=None,
            resulting_material_state_ref=uuid7(),
            relationship_code="placement_overlaps",
            constrained_facet_code="schedule.placement",
            strength_code="hard",
            starts_at=datetime(2026, 10, 1, 12, 0, tzinfo=UTC),
            ends_at=datetime(2026, 10, 1, 12, 0, tzinfo=UTC),
        )
