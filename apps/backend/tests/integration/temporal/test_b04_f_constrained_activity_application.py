"""Real PostgreSQL proof for B04-F atomic Activity + Temporal Constraint authoring."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any
from uuid import uuid7

import psycopg
import pytest
from b05_legacy_test_support import ensure_test_life_area

from dante.modules.temporal.constrained_activity import (
    ConstrainedActivityApplication,
    ConstrainedActivityOperationIdReuseError,
    _child_operation_id,
)
from dante.modules.temporal.temporal_constraint import (
    AbsoluteBoundaryRule,
    AbsoluteWindowRule,
    TemporalConstraintApplication,
)
from dante.platform.database.references import NativeRef
from dante.platform.database.runtime import create_database_runtime


def _seed_person(database: Any) -> NativeRef:
    self_ref = NativeRef(uuid7())
    with psycopg.connect(
        **database.connection_kwargs("dante_migrator", database.cluster.migrator_password)
    ) as connection:
        connection.execute("SET ROLE dante_owner")
        connection.execute("SET search_path TO pg_catalog,dante,pg_temp")
        connection.execute("INSERT INTO dante.person(person_ref) VALUES (%s)", (self_ref,))
        connection.execute(
            "INSERT INTO dante.native_address(native_ref,owner_family) VALUES (%s,'person')",
            (self_ref,),
        )
        connection.commit()
    return self_ref


def _seed_activity(database: Any, *, self_ref: NativeRef, title: str) -> NativeRef:
    activity_ref = NativeRef(uuid7())
    with psycopg.connect(
        **database.connection_kwargs("dante_migrator", database.cluster.migrator_password)
    ) as connection:
        connection.execute("SET ROLE dante_owner")
        connection.execute("SET search_path TO pg_catalog,dante,pg_temp")
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
            (activity_ref, self_ref, title, datetime.now(UTC)),
        )
        connection.commit()
    return activity_ref


@pytest.mark.postgres
@pytest.mark.asyncio
async def test_b04_f_atomic_constrained_activity_create_replay_and_changed_intent(
    migrated_database: Any,
) -> None:
    self_ref = _seed_person(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    application = ConstrainedActivityApplication(runtime.session_factory)
    constraint_application = TemporalConstraintApplication(runtime.session_factory)
    rules = (
        AbsoluteBoundaryRule(
            boundary_kind="earliest_start",
            constrained_facet="schedule.start",
            strength="hard",
            boundary_at=datetime(2026, 10, 10, 8, 0, tzinfo=UTC),
        ),
        AbsoluteBoundaryRule(
            boundary_kind="latest_completion",
            constrained_facet="schedule.completion",
            strength="hard",
            boundary_at=datetime(2026, 10, 10, 18, 0, tzinfo=UTC),
        ),
    )
    try:
        created = await application.create_activity_with_constraints(
            self_person_ref=self_ref,
            life_area_ref=ensure_test_life_area(migrated_database, self_ref),
            operation_id="operation:b04-f:constrained-deadline",
            title="Consegna relazione",
            rules=rules,
        )
        assert created.replayed is False
        assert len(created.constraints) == 2
        assert all(value.replayed is False for value in created.constraints)
        assert {value.constraint_ref for value in created.constraints} == {
            value.constraint_ref
            for value in await constraint_application.list_constraints_by_subject(
                self_person_ref=self_ref,
                subject_native_ref=created.activity.activity_ref,
            )
        }

        replay = await application.create_activity_with_constraints(
            self_person_ref=self_ref,
            life_area_ref=ensure_test_life_area(migrated_database, self_ref),
            operation_id="operation:b04-f:constrained-deadline",
            title="Consegna relazione",
            rules=rules,
        )
        assert replay.replayed is True
        assert replay.activity.activity_ref == created.activity.activity_ref
        assert tuple(value.constraint_ref for value in replay.constraints) == tuple(
            value.constraint_ref for value in created.constraints
        )
        assert all(value.replayed is True for value in replay.constraints)

        with pytest.raises(ConstrainedActivityOperationIdReuseError):
            await application.create_activity_with_constraints(
                self_person_ref=self_ref,
                life_area_ref=ensure_test_life_area(migrated_database, self_ref),
                operation_id="operation:b04-f:constrained-deadline",
                title="Consegna relazione",
                rules=(
                    AbsoluteBoundaryRule(
                        boundary_kind="latest_completion",
                        constrained_facet="schedule.completion",
                        strength="hard",
                        boundary_at=datetime(2026, 10, 11, 18, 0, tzinfo=UTC),
                    ),
                ),
            )
    finally:
        await runtime.dispose()


@pytest.mark.postgres
@pytest.mark.asyncio
async def test_b04_f_constraint_collision_rolls_back_new_activity(
    migrated_database: Any,
) -> None:
    self_ref = _seed_person(migrated_database)
    existing_activity_ref = _seed_activity(
        migrated_database, self_ref=self_ref, title="Existing collision owner"
    )
    parent_operation_id = "operation:b04-f:must-roll-back"
    runtime = create_database_runtime(migrated_database.runtime_settings())
    constraint_application = TemporalConstraintApplication(runtime.session_factory)
    application = ConstrainedActivityApplication(runtime.session_factory)
    try:
        # Occupy the deterministic first child receipt with a different canonical intent.
        await constraint_application.create_constraint(
            self_person_ref=self_ref,
            operation_id=_child_operation_id(parent_operation_id, 0),
            subject_native_ref=existing_activity_ref,
            rule=AbsoluteWindowRule(
                relationship="full_placement_contained",
                constrained_facet="schedule.placement",
                strength="hard",
                starts_at=datetime(2026, 10, 12, 8, 0, tzinfo=UTC),
                ends_at=datetime(2026, 10, 12, 12, 0, tzinfo=UTC),
            ),
        )

        with pytest.raises(ConstrainedActivityOperationIdReuseError):
            await application.create_activity_with_constraints(
                self_person_ref=self_ref,
                life_area_ref=ensure_test_life_area(migrated_database, self_ref),
                operation_id=parent_operation_id,
                title="This Activity must roll back",
                rules=(
                    AbsoluteBoundaryRule(
                        boundary_kind="latest_completion",
                        constrained_facet="schedule.completion",
                        strength="hard",
                        boundary_at=datetime(2026, 10, 12, 17, 0, tzinfo=UTC),
                    ),
                ),
            )

        with psycopg.connect(
            **migrated_database.connection_kwargs(
                "dante_migrator", migrated_database.cluster.migrator_password
            )
        ) as connection:
            connection.execute("SET ROLE dante_owner")
            row = connection.execute(
                "SELECT count(*) FROM dante.activity_intention WHERE self_person_ref=%s AND title=%s",
                (self_ref, "This Activity must roll back"),
            ).fetchone()
        assert row == (0,)
    finally:
        await runtime.dispose()
