"""B06-D PostgreSQL proof for Occurrence use of shared Schedule history."""

from __future__ import annotations

from datetime import date, time
from typing import Any

import psycopg
import pytest
from tests.integration.temporal.test_b05_primary_life_area_assignment import _seed_self

from dante.modules.temporal.life_area import LifeAreaApplication
from dante.modules.temporal.occurrence import OccurrenceApplication
from dante.modules.temporal.routine import RoutineApplication
from dante.modules.temporal.schedule import (
    CoarseLocalPeriodPlacement,
    DateSpanPlacement,
    ScheduleNotFoundError,
    ScheduleOperationIdReuseError,
    TemporalScheduleApplication,
)
from dante.platform.database.references import NativeRef
from dante.platform.database.runtime import create_database_runtime

pytestmark = pytest.mark.postgres


@pytest.mark.asyncio
async def test_occurrence_reuses_schedule_identity_history_and_self_scope(
    migrated_database: Any,
) -> None:
    alice = _seed_self(migrated_database)
    bob = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    areas = LifeAreaApplication(runtime.session_factory)
    routines = RoutineApplication(runtime.session_factory)
    occurrences = OccurrenceApplication(runtime.session_factory)
    schedules = TemporalScheduleApplication(runtime.session_factory)
    try:
        area = (
            await areas.create(
                self_person_ref=alice,
                operation_id="b06-d:area",
                name="Salute",
            )
        ).area
        routine = await routines.create(
            self_person_ref=alice,
            operation_id="b06-d:routine",
            title="Farmaco",
            life_area_ref=area.life_area_ref,
            starts_on=date(2026, 10, 1),
            wall_time=time(8),
        )
        checkpoint = await occurrences.checkpoint(
            owner="routine",
            self_person_ref=alice,
            source_ref=routine.routine_ref,
            operation_id="b06-d:checkpoint",
            start_date=date(2026, 10, 1),
            end_date_exclusive=date(2026, 10, 2),
            effective_zone_id="Europe/Rome",
        )
        occurrence_ref = NativeRef(checkpoint.occurrences[0].occurrence_ref)
        initial = await schedules.establish_schedule(
            self_person_ref=alice,
            operation_id="b06-d:schedule",
            subject_native_ref=occurrence_ref,
            placement=DateSpanPlacement(
                start_date=date(2026, 10, 1),
                end_date_exclusive=date(2026, 10, 2),
            ),
        )
        replay = await schedules.establish_schedule(
            self_person_ref=alice,
            operation_id="b06-d:schedule",
            subject_native_ref=occurrence_ref,
            placement=DateSpanPlacement(
                start_date=date(2026, 10, 1),
                end_date_exclusive=date(2026, 10, 2),
            ),
        )
        assert replay.replayed
        assert replay.schedule_ref == initial.schedule_ref
        assert replay.material_state_ref == initial.material_state_ref

        with pytest.raises(ScheduleOperationIdReuseError):
            await schedules.establish_schedule(
                self_person_ref=alice,
                operation_id="b06-d:schedule",
                subject_native_ref=occurrence_ref,
                placement=CoarseLocalPeriodPlacement(
                    local_date=date(2026, 10, 1),
                    period="morning",
                ),
            )
        with pytest.raises(ScheduleNotFoundError):
            await schedules.establish_schedule(
                self_person_ref=bob,
                operation_id="b06-d:foreign",
                subject_native_ref=occurrence_ref,
                placement=CoarseLocalPeriodPlacement(
                    local_date=date(2026, 10, 1),
                    period="morning",
                ),
            )

        revised = await schedules.revise_schedule(
            self_person_ref=alice,
            operation_id="b06-d:revise",
            schedule_ref=initial.schedule_ref,
            expected_material_state_ref=initial.material_state_ref,
            placement=CoarseLocalPeriodPlacement(
                local_date=date(2026, 10, 1),
                period="morning",
            ),
        )
        unscheduled = await schedules.unschedule(
            self_person_ref=alice,
            operation_id="b06-d:unschedule",
            schedule_ref=initial.schedule_ref,
            expected_material_state_ref=revised.material_state_ref,
        )
        restored = await schedules.undo_unschedule(
            self_person_ref=alice,
            operation_id="b06-d:undo",
            schedule_ref=initial.schedule_ref,
            unschedule_operation_id=unscheduled.unschedule_operation_id,
        )
        assert restored.restored_from_material_state_ref == revised.material_state_ref
        assert restored.material_state_ref != revised.material_state_ref
        assert restored.placement == revised.placement

        with psycopg.connect(
            **migrated_database.connection_kwargs(
                "dante_migrator", migrated_database.cluster.migrator_password
            )
        ) as connection:
            connection.execute("SET ROLE dante_owner")
            assert connection.execute(
                "SELECT count(*), count(*) FILTER (WHERE current_until_at IS NULL) "
                "FROM dante.schedule_placement_current_history WHERE schedule_ref=%s",
                (initial.schedule_ref,),
            ).fetchone() == (3, 1)
    finally:
        await runtime.dispose()
