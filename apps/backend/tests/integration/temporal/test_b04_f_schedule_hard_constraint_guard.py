"""B04-F proof that canonical Schedule establish/revise cannot bypass hard constraints."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any
from uuid import uuid7

import psycopg
import pytest
from b05_legacy_test_support import ensure_test_life_area

from dante.modules.temporal.activity import (
    ActivityPersistenceError,
    TemporalActivityApplication,
)
from dante.modules.temporal.constrained_activity import ConstrainedActivityApplication
from dante.modules.temporal.schedule import (
    AbsoluteIntervalPlacement,
    FloatingLocalIntervalPlacement,
    SchedulePersistenceError,
    TemporalScheduleApplication,
)
from dante.modules.temporal.temporal_constraint import AbsoluteWindowRule
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


async def _create_windowed_activity(
    application: ConstrainedActivityApplication,
    *,
    database: Any,
    self_ref: NativeRef,
    operation_id: str,
) -> NativeRef:
    result = await application.create_activity_with_constraints(
        self_person_ref=self_ref,
        life_area_ref=ensure_test_life_area(database, self_ref),
        operation_id=operation_id,
        title=f"Windowed {operation_id}",
        rules=(
            AbsoluteWindowRule(
                relationship="full_placement_contained",
                constrained_facet="schedule.placement",
                strength="hard",
                starts_at=datetime(2026, 10, 20, 8, 0, tzinfo=UTC),
                ends_at=datetime(2026, 10, 20, 12, 0, tzinfo=UTC),
            ),
        ),
    )
    return result.activity.activity_ref


@pytest.mark.postgres
@pytest.mark.asyncio
async def test_b04_f_schedule_establish_enforces_hard_window_and_fails_closed_for_floating(
    migrated_database: Any,
) -> None:
    self_ref = _seed_person(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    constrained = ConstrainedActivityApplication(runtime.session_factory)
    activities = TemporalActivityApplication(runtime.session_factory)
    try:
        admissible_ref = await _create_windowed_activity(
            constrained,
            database=migrated_database,
            self_ref=self_ref,
            operation_id="operation:b04-f:guard:admissible",
        )
        admitted = await activities.schedule_existing_activity_with_placement(
            self_person_ref=self_ref,
            activity_ref=admissible_ref,
            operation_id="operation:b04-f:guard:place:inside",
            placement=AbsoluteIntervalPlacement(
                starts_at=datetime(2026, 10, 20, 9, 0, tzinfo=UTC),
                ends_at=datetime(2026, 10, 20, 10, 0, tzinfo=UTC),
            ),
        )
        assert admitted.schedule.placement == AbsoluteIntervalPlacement(
            starts_at=datetime(2026, 10, 20, 9, 0, tzinfo=UTC),
            ends_at=datetime(2026, 10, 20, 10, 0, tzinfo=UTC),
        )

        rejected_ref = await _create_windowed_activity(
            constrained,
            database=migrated_database,
            self_ref=self_ref,
            operation_id="operation:b04-f:guard:rejected",
        )
        with pytest.raises(ActivityPersistenceError):
            await activities.schedule_existing_activity_with_placement(
                self_person_ref=self_ref,
                activity_ref=rejected_ref,
                operation_id="operation:b04-f:guard:place:outside",
                placement=AbsoluteIntervalPlacement(
                    starts_at=datetime(2026, 10, 20, 13, 0, tzinfo=UTC),
                    ends_at=datetime(2026, 10, 20, 14, 0, tzinfo=UTC),
                ),
            )

        floating_ref = await _create_windowed_activity(
            constrained,
            database=migrated_database,
            self_ref=self_ref,
            operation_id="operation:b04-f:guard:floating",
        )
        with pytest.raises(ActivityPersistenceError):
            await activities.schedule_existing_activity_with_placement(
                self_person_ref=self_ref,
                activity_ref=floating_ref,
                operation_id="operation:b04-f:guard:place:floating",
                placement=FloatingLocalIntervalPlacement(
                    starts_local_at=datetime(2026, 10, 20, 9, 0),  # noqa: DTZ001
                    ends_local_at=datetime(2026, 10, 20, 10, 0),  # noqa: DTZ001
                ),
            )

        with psycopg.connect(
            **migrated_database.connection_kwargs(
                "dante_migrator", migrated_database.cluster.migrator_password
            )
        ) as connection:
            connection.execute("SET ROLE dante_owner")
            for subject_ref in (rejected_ref, floating_ref):
                row = connection.execute(
                    "SELECT count(*) FROM dante.schedule WHERE subject_native_ref=%s",
                    (subject_ref,),
                ).fetchone()
                assert row == (0,)
    finally:
        await runtime.dispose()


@pytest.mark.postgres
@pytest.mark.asyncio
async def test_b04_f_schedule_revision_rejects_hard_constraint_bypass_without_changing_current_state(
    migrated_database: Any,
) -> None:
    self_ref = _seed_person(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    constrained = ConstrainedActivityApplication(runtime.session_factory)
    activities = TemporalActivityApplication(runtime.session_factory)
    schedules = TemporalScheduleApplication(runtime.session_factory)
    try:
        activity_ref = await _create_windowed_activity(
            constrained,
            database=migrated_database,
            self_ref=self_ref,
            operation_id="operation:b04-f:guard:revise",
        )
        established = await activities.schedule_existing_activity_with_placement(
            self_person_ref=self_ref,
            activity_ref=activity_ref,
            operation_id="operation:b04-f:guard:revise:establish",
            placement=AbsoluteIntervalPlacement(
                starts_at=datetime(2026, 10, 20, 9, 0, tzinfo=UTC),
                ends_at=datetime(2026, 10, 20, 10, 0, tzinfo=UTC),
            ),
        )
        expected_ref = established.schedule.material_state_ref

        with pytest.raises(SchedulePersistenceError):
            await schedules.revise_schedule(
                self_person_ref=self_ref,
                operation_id="operation:b04-f:guard:revise:outside",
                schedule_ref=established.schedule.schedule_ref,
                expected_material_state_ref=expected_ref,
                placement=AbsoluteIntervalPlacement(
                    starts_at=datetime(2026, 10, 20, 13, 0, tzinfo=UTC),
                    ends_at=datetime(2026, 10, 20, 14, 0, tzinfo=UTC),
                ),
            )

        with psycopg.connect(
            **migrated_database.connection_kwargs(
                "dante_migrator", migrated_database.cluster.migrator_password
            )
        ) as connection:
            connection.execute("SET ROLE dante_owner")
            row = connection.execute(
                """
                SELECT material_state_ref
                  FROM dante.scoped_current_material_state
                 WHERE scoped_owner_ref=%s AND facet_code='schedule.placement'
                """,
                (established.schedule.schedule_ref,),
            ).fetchone()
            assert row == (expected_ref,)
    finally:
        await runtime.dispose()
