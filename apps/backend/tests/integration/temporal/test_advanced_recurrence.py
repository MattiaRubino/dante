"""B11-A PostgreSQL proof for Actual-backed advanced Recurrence."""

from __future__ import annotations

from datetime import UTC, date, datetime, time, timedelta
from decimal import Decimal
from typing import Any

import psycopg
import pytest

from dante.modules.temporal.actual_runtime import ActualApplication
from dante.modules.temporal.advanced_recurrence import (
    AdvancedElapsedRecurrence,
    AdvancedRecurrenceApplication,
)
from dante.modules.temporal.life_area import LifeAreaApplication
from dante.modules.temporal.occurrence import OccurrenceApplication
from dante.modules.temporal.recurrence import RecurrenceApplication
from dante.modules.temporal.routine import RoutineApplication
from dante.modules.temporal.session_runtime import SessionApplication
from dante.platform.database.references import NativeRef
from dante.platform.database.runtime import create_database_runtime
from tests.integration.temporal.test_b05_primary_life_area_assignment import _seed_self

pytestmark = pytest.mark.postgres


def _admin(database: Any) -> psycopg.Connection[Any]:
    return psycopg.connect(
        host=database.cluster.host,
        port=database.cluster.port,
        dbname=database.name,
        user=database.cluster.admin_user,
        password=database.cluster.admin_password,
        autocommit=True,
    )


@pytest.mark.asyncio
async def test_b11_a_completion_relative_waits_for_actual_and_pins_exact_reality(
    migrated_database: Any,
) -> None:
    alice = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    areas = LifeAreaApplication(runtime.session_factory)
    routines = RoutineApplication(runtime.session_factory)
    occurrences = OccurrenceApplication(runtime.session_factory)
    recurrences = RecurrenceApplication(runtime.session_factory)
    advanced = AdvancedRecurrenceApplication(runtime.session_factory)
    sessions = SessionApplication(runtime.session_factory)
    actuals = ActualApplication(runtime.session_factory)
    try:
        area = (
            await areas.create(
                self_person_ref=alice,
                operation_id="b11-a:completion:area",
                name="Completion recurrence",
            )
        ).area
        routine = await routines.create(
            self_person_ref=alice,
            operation_id="b11-a:completion:routine",
            title="Dose completion-relative",
            life_area_ref=area.life_area_ref,
            starts_on=date(2026, 10, 1),
            wall_time=time(8),
        )
        seed = await occurrences.checkpoint(
            owner="routine",
            self_person_ref=alice,
            source_ref=routine.routine_ref,
            operation_id="b11-a:completion:seed",
            start_date=date(2026, 10, 1),
            end_date_exclusive=date(2026, 10, 2),
            effective_zone_id="Europe/Rome",
        )
        assert len(seed.occurrences) == 1
        anchor_occurrence_ref = NativeRef(seed.occurrences[0].occurrence_ref)

        current = await recurrences.get(
            owner="routine",
            self_person_ref=alice,
            owner_ref=routine.routine_ref,
        )
        assert current is not None
        accepted = await advanced.replace(
            owner="routine",
            self_person_ref=alice,
            operation_id="b11-a:completion:rule",
            source_ref=routine.routine_ref,
            expected_material_state_ref=current.material_state_ref,
            recurrence=AdvancedElapsedRecurrence(
                range_kind="open",
                expected_occurrence_count=None,
                effective_from=datetime(2026, 10, 1, tzinfo=UTC),
                effective_until=None,
                elapsed_seconds=Decimal("3600.000000"),
                anchor_mode_code="previous_completion",
            ),
        )
        assert accepted.recurrence.recurrence.anchor_mode_code == "previous_completion"
        assert accepted.recurrence.recurrence.anchor_source_native_ref is None

        # Session lifecycle is execution context, not happened truth. Ending it must
        # not fabricate the Actual completion required by this Recurrence.
        session = await sessions.start(
            self_person_ref=alice,
            operation_id="b11-a:completion:session-start",
            subject_kind="occurrence",
            subject_native_ref=anchor_occurrence_ref,
        )
        ended_session = await sessions.end(
            self_person_ref=alice,
            operation_id="b11-a:completion:session-end",
            session_ref=session.session_ref,
            expected_material_state_ref=session.timing_material_state_ref,
        )
        assert ended_session.ended_at is not None

        blocked = await advanced.checkpoint(
            owner="routine",
            self_person_ref=alice,
            operation_id="b11-a:completion:before-actual",
            source_ref=routine.routine_ref,
            governing_recurrence_state_ref=accepted.recurrence.material_state_ref,
            start_at=datetime(2026, 10, 1, tzinfo=UTC),
            end_at_exclusive=datetime(2026, 10, 4, tzinfo=UTC),
        )
        assert blocked.occurrences == ()
        assert not blocked.replayed

        started_at = datetime(2026, 10, 1, 9, 0, tzinfo=UTC)
        completed_at = datetime(2026, 10, 1, 9, 45, tzinfo=UTC)
        actual = await actuals.record(
            self_person_ref=alice,
            operation_id="b11-a:completion:actual",
            subject_kind="occurrence",
            subject_native_ref=anchor_occurrence_ref,
            realization_occurred=True,
            expected_material_state_ref=None,
            extent_code="interval",
            started_at=started_at,
            ended_at=completed_at,
        )

        generated = await advanced.checkpoint(
            owner="routine",
            self_person_ref=alice,
            operation_id="b11-a:completion:after-actual",
            source_ref=routine.routine_ref,
            governing_recurrence_state_ref=accepted.recurrence.material_state_ref,
            start_at=datetime(2026, 10, 1, tzinfo=UTC),
            end_at_exclusive=datetime(2026, 10, 4, tzinfo=UTC),
        )
        assert len(generated.occurrences) == 1
        dependent = generated.occurrences[0]
        assert dependent.expected_at == completed_at + timedelta(hours=1)
        assert dependent.anchor_occurrence_ref == anchor_occurrence_ref
        assert dependent.anchor_actual_ref == actual.actual_ref
        assert dependent.anchor_actual_material_state_ref == actual.material_state_ref
        assert dependent.anchor_completed_at == completed_at
        assert dependent.created

        replay = await advanced.checkpoint(
            owner="routine",
            self_person_ref=alice,
            operation_id="b11-a:completion:after-actual",
            source_ref=routine.routine_ref,
            governing_recurrence_state_ref=accepted.recurrence.material_state_ref,
            start_at=datetime(2026, 10, 1, tzinfo=UTC),
            end_at_exclusive=datetime(2026, 10, 4, tzinfo=UTC),
        )
        assert replay.replayed
        assert len(replay.occurrences) == 1
        assert replay.occurrences[0].occurrence_ref == dependent.occurrence_ref
        assert not replay.occurrences[0].created

        corrected_completion = completed_at + timedelta(minutes=20)
        corrected = await actuals.record(
            self_person_ref=alice,
            operation_id="b11-a:completion:actual-correction",
            subject_kind="occurrence",
            subject_native_ref=anchor_occurrence_ref,
            realization_occurred=True,
            expected_material_state_ref=actual.material_state_ref,
            extent_code="interval",
            started_at=started_at,
            ended_at=corrected_completion,
        )
        assert corrected.material_state_ref != actual.material_state_ref

        after_correction = await advanced.checkpoint(
            owner="routine",
            self_person_ref=alice,
            operation_id="b11-a:completion:after-correction",
            source_ref=routine.routine_ref,
            governing_recurrence_state_ref=accepted.recurrence.material_state_ref,
            start_at=datetime(2026, 10, 1, tzinfo=UTC),
            end_at_exclusive=datetime(2026, 10, 4, tzinfo=UTC),
        )
        assert after_correction.occurrences == ()

        with _admin(migrated_database) as connection:
            proof = connection.execute(
                """
                SELECT anchor_actual_material_state_ref,anchor_completed_at,expected_at
                  FROM dante.occurrence_generation_actual_anchor
                 WHERE occurrence_ref=%s
                """,
                (dependent.occurrence_ref,),
            ).fetchone()
            count = connection.execute(
                """
                SELECT count(*)
                  FROM dante.occurrence_generation_actual_anchor
                 WHERE governing_recurrence_state_ref=%s
                """,
                (accepted.recurrence.material_state_ref,),
            ).fetchone()
        assert proof == (
            actual.material_state_ref,
            completed_at,
            completed_at + timedelta(hours=1),
        )
        assert count == (1,)
    finally:
        await runtime.dispose()


@pytest.mark.asyncio
async def test_b11_a_anchor_stream_maps_each_qualifying_actual_once(
    migrated_database: Any,
) -> None:
    alice = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    areas = LifeAreaApplication(runtime.session_factory)
    routines = RoutineApplication(runtime.session_factory)
    occurrences = OccurrenceApplication(runtime.session_factory)
    recurrences = RecurrenceApplication(runtime.session_factory)
    advanced = AdvancedRecurrenceApplication(runtime.session_factory)
    actuals = ActualApplication(runtime.session_factory)
    try:
        area = (
            await areas.create(
                self_person_ref=alice,
                operation_id="b11-a:stream:area",
                name="Anchor stream",
            )
        ).area
        anchor_routine = await routines.create(
            self_person_ref=alice,
            operation_id="b11-a:stream:anchor-routine",
            title="Anchor routine",
            life_area_ref=area.life_area_ref,
            starts_on=date(2026, 10, 1),
            wall_time=time(8),
        )
        target_routine = await routines.create(
            self_person_ref=alice,
            operation_id="b11-a:stream:target-routine",
            title="Mapped routine",
            life_area_ref=area.life_area_ref,
            starts_on=date(2026, 10, 1),
            wall_time=time(12),
        )
        anchors = await occurrences.checkpoint(
            owner="routine",
            self_person_ref=alice,
            source_ref=anchor_routine.routine_ref,
            operation_id="b11-a:stream:seed",
            start_date=date(2026, 10, 1),
            end_date_exclusive=date(2026, 10, 3),
            effective_zone_id="Europe/Rome",
        )
        assert len(anchors.occurrences) == 2

        completion_times = (
            datetime(2026, 10, 1, 9, 15, tzinfo=UTC),
            datetime(2026, 10, 2, 10, 20, tzinfo=UTC),
        )
        actual_states: set[UUID] = set()
        for index, (item, completed_at) in enumerate(
            zip(anchors.occurrences, completion_times, strict=True), start=1
        ):
            actual = await actuals.record(
                self_person_ref=alice,
                operation_id=f"b11-a:stream:actual:{index}",
                subject_kind="occurrence",
                subject_native_ref=NativeRef(item.occurrence_ref),
                realization_occurred=True,
                expected_material_state_ref=None,
                extent_code="interval",
                started_at=completed_at - timedelta(minutes=30),
                ended_at=completed_at,
            )
            actual_states.add(actual.material_state_ref)

        target_current = await recurrences.get(
            owner="routine",
            self_person_ref=alice,
            owner_ref=target_routine.routine_ref,
        )
        assert target_current is not None
        accepted = await advanced.replace(
            owner="routine",
            self_person_ref=alice,
            operation_id="b11-a:stream:rule",
            source_ref=target_routine.routine_ref,
            expected_material_state_ref=target_current.material_state_ref,
            recurrence=AdvancedElapsedRecurrence(
                range_kind="open",
                expected_occurrence_count=None,
                effective_from=datetime(2026, 10, 1, tzinfo=UTC),
                effective_until=None,
                elapsed_seconds=Decimal("1800.000000"),
                anchor_mode_code="anchor_stream",
                anchor_source_family="routine",
                anchor_source_native_ref=anchor_routine.routine_ref,
            ),
        )
        assert accepted.recurrence.recurrence.anchor_source_native_ref == anchor_routine.routine_ref

        mapped = await advanced.checkpoint(
            owner="routine",
            self_person_ref=alice,
            operation_id="b11-a:stream:checkpoint",
            source_ref=target_routine.routine_ref,
            governing_recurrence_state_ref=accepted.recurrence.material_state_ref,
            start_at=datetime(2026, 10, 1, tzinfo=UTC),
            end_at_exclusive=datetime(2026, 10, 4, tzinfo=UTC),
        )
        assert len(mapped.occurrences) == 2
        assert {item.anchor_occurrence_ref for item in mapped.occurrences} == {
            item.occurrence_ref for item in anchors.occurrences
        }
        assert {item.anchor_actual_material_state_ref for item in mapped.occurrences} == actual_states
        assert {item.expected_at for item in mapped.occurrences} == {
            completion + timedelta(minutes=30) for completion in completion_times
        }

        replay = await advanced.checkpoint(
            owner="routine",
            self_person_ref=alice,
            operation_id="b11-a:stream:checkpoint",
            source_ref=target_routine.routine_ref,
            governing_recurrence_state_ref=accepted.recurrence.material_state_ref,
            start_at=datetime(2026, 10, 1, tzinfo=UTC),
            end_at_exclusive=datetime(2026, 10, 4, tzinfo=UTC),
        )
        assert replay.replayed
        assert {item.occurrence_ref for item in replay.occurrences} == {
            item.occurrence_ref for item in mapped.occurrences
        }

        with _admin(migrated_database) as connection:
            proof = connection.execute(
                """
                SELECT count(*),count(DISTINCT anchor_occurrence_ref)
                  FROM dante.occurrence_generation_actual_anchor
                 WHERE governing_recurrence_state_ref=%s
                """,
                (accepted.recurrence.material_state_ref,),
            ).fetchone()
        assert proof == (2, 2)
    finally:
        await runtime.dispose()
