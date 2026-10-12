"""PostgreSQL proof for the B04-A API activation boundary."""

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


def _seed_activity(database: Any) -> tuple[UUID, UUID]:
    self_person_ref = uuid7()
    activity_ref = uuid7()
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
            ) VALUES (%s,%s,'B04 A5 Activity',%s)
            """,
            (activity_ref, self_person_ref, datetime.now(UTC)),
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
                strength_code,
                boundary_at,
            ),
        ).fetchone()
        connection.commit()
        assert row is not None
        return row


@pytest.mark.postgres
def test_b04_a5_replay_returns_accepted_refs_when_retry_supplies_fresh_generated_refs(
    migrated_database: Any,
) -> None:
    self_ref, activity_ref = _seed_activity(migrated_database)
    constraint_ref = uuid7()
    first_state_ref = uuid7()
    second_state_ref = uuid7()
    boundary = datetime(2026, 9, 24, 7, 30, tzinfo=UTC)

    created = _mutate(
        migrated_database,
        self_person_ref=self_ref,
        operation_id="operation:b04-a5:create",
        fingerprint="a" * 64,
        mutation_kind="create",
        subject_native_ref=activity_ref,
        constraint_ref=constraint_ref,
        expected_material_state_ref=None,
        resulting_material_state_ref=first_state_ref,
        strength_code="hard",
        boundary_at=boundary,
    )
    assert created[0] == constraint_ref
    assert created[2] == first_state_ref
    assert created[5] is False

    create_replay = _mutate(
        migrated_database,
        self_person_ref=self_ref,
        operation_id="operation:b04-a5:create",
        fingerprint="a" * 64,
        mutation_kind="create",
        subject_native_ref=activity_ref,
        constraint_ref=uuid7(),
        expected_material_state_ref=None,
        resulting_material_state_ref=uuid7(),
        strength_code="hard",
        boundary_at=boundary,
    )
    assert create_replay[0] == constraint_ref
    assert create_replay[2] == first_state_ref
    assert create_replay[4] == created[4]
    assert create_replay[5] is True

    revised = _mutate(
        migrated_database,
        self_person_ref=self_ref,
        operation_id="operation:b04-a5:revise",
        fingerprint="b" * 64,
        mutation_kind="revise",
        subject_native_ref=activity_ref,
        constraint_ref=constraint_ref,
        expected_material_state_ref=first_state_ref,
        resulting_material_state_ref=second_state_ref,
        strength_code="soft",
        boundary_at=boundary + timedelta(hours=2),
    )
    assert revised[2] == second_state_ref
    assert revised[5] is False

    revise_replay = _mutate(
        migrated_database,
        self_person_ref=self_ref,
        operation_id="operation:b04-a5:revise",
        fingerprint="b" * 64,
        mutation_kind="revise",
        subject_native_ref=activity_ref,
        constraint_ref=constraint_ref,
        expected_material_state_ref=first_state_ref,
        resulting_material_state_ref=uuid7(),
        strength_code="soft",
        boundary_at=boundary + timedelta(hours=2),
    )
    assert revise_replay[0] == constraint_ref
    assert revise_replay[2] == second_state_ref
    assert revise_replay[4] == revised[4]
    assert revise_replay[5] is True


@pytest.mark.postgres
def test_b04_a5_runtime_can_read_current_rule_tables_but_not_history_or_receipts(
    migrated_database: Any,
) -> None:
    runtime_kwargs = migrated_database.connection_kwargs(
        "dante_runtime",
        migrated_database.cluster.runtime_password,
    )
    readable_tables = (
        "temporal_constraint",
        "temporal_constraint_state",
        "temporal_constraint_boundary_state",
        "temporal_constraint_boundary_absolute_state",
    )
    private_tables = (
        "temporal_constraint_current_history",
        "temporal_constraint_mutation_operation",
    )

    with psycopg.connect(**runtime_kwargs) as connection:
        for table in readable_tables:
            connection.execute(f"SELECT 1 FROM dante.{table} LIMIT 1").fetchone()

    for table in private_tables:
        with psycopg.connect(**runtime_kwargs) as connection:
            with pytest.raises(psycopg.errors.InsufficientPrivilege):
                connection.execute(f"SELECT 1 FROM dante.{table} LIMIT 1").fetchone()
