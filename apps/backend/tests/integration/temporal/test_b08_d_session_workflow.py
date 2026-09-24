"""B08-D regression across direct Activity Sessions, TC-009 and Occurrence Sessions."""

from __future__ import annotations

from datetime import date, time
from typing import Any

import psycopg
import pytest

from dante.modules.temporal.activity import TemporalActivityApplication
from dante.modules.temporal.life_area import LifeAreaApplication
from dante.modules.temporal.occurrence import OccurrenceApplication
from dante.modules.temporal.routine import RoutineApplication
from dante.modules.temporal.session_runtime import (
    SessionApplication,
    SessionEndConflictError,
)
from dante.modules.temporal.temporal_constraint import (
    SessionMinimumDurationRule,
    TemporalConstraintApplication,
)
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
async def test_unplaced_activity_session_pause_resume_and_tc009_remain_independent(
    migrated_database: Any,
) -> None:
    actor = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    areas = LifeAreaApplication(runtime.session_factory)
    activities = TemporalActivityApplication(runtime.session_factory)
    constraints = TemporalConstraintApplication(runtime.session_factory)
    sessions = SessionApplication(runtime.session_factory)
    try:
        area = (
            await areas.create(
                self_person_ref=actor, operation_id="b08-d:activity-area", name="Focus"
            )
        ).area
        activity = (
            await activities.create_activity(
                self_person_ref=actor,
                operation_id="b08-d:activity",
                title="Direct execution without a plan",
                life_area_ref=area.life_area_ref,
            )
        ).activity
        constraint = await constraints.create_constraint(
            self_person_ref=actor,
            operation_id="b08-d:minimum",
            subject_native_ref=activity.activity_ref,
            rule=SessionMinimumDurationRule(duration_microseconds=86_400_000_000),
        )

        started = await sessions.start(
            self_person_ref=actor,
            operation_id="b08-d:activity-start",
            subject_kind="activity",
            subject_native_ref=activity.activity_ref,
        )
        assert started.open and not started.paused
        assert started.duration_evaluations[0].constraint_ref == constraint.constraint_ref
        assert started.duration_evaluations[0].evaluation == "pending"

        paused = await sessions.pause(
            self_person_ref=actor,
            operation_id="b08-d:activity-pause",
            session_ref=started.session_ref,
            expected_material_state_ref=started.timing_material_state_ref,
        )
        assert paused.paused and paused.open
        assert paused.duration_evaluations[0].evaluation == "pending"
        with pytest.raises(SessionEndConflictError):
            await sessions.end(
                self_person_ref=actor,
                operation_id="b08-d:paused-end-rejected",
                session_ref=started.session_ref,
                expected_material_state_ref=paused.timing_material_state_ref,
            )

        reloaded_pause = await sessions.get(
            self_person_ref=actor, session_ref=started.session_ref
        )
        assert reloaded_pause.paused
        assert reloaded_pause.timing_material_state_ref == paused.timing_material_state_ref
        resumed = await sessions.resume(
            self_person_ref=actor,
            operation_id="b08-d:activity-resume",
            session_ref=started.session_ref,
            expected_material_state_ref=reloaded_pause.timing_material_state_ref,
        )
        assert resumed.open and not resumed.paused
        assert resumed.timing_material_state_ref != paused.timing_material_state_ref
        ended = await sessions.end(
            self_person_ref=actor,
            operation_id="b08-d:activity-end",
            session_ref=started.session_ref,
            expected_material_state_ref=resumed.timing_material_state_ref,
        )
        assert not ended.open and not ended.paused
        assert ended.session_ref == started.session_ref
        assert ended.duration_evaluations[0].evaluation == "violated"
        assert ended.active_seconds == pytest.approx(
            ended.elapsed_seconds - ended.paused_seconds, abs=0.001
        )
        replay = await sessions.end(
            self_person_ref=actor,
            operation_id="b08-d:activity-end",
            session_ref=started.session_ref,
            expected_material_state_ref=resumed.timing_material_state_ref,
        )
        assert replay.replayed
        assert replay.timing_material_state_ref == ended.timing_material_state_ref

        second = await sessions.start(
            self_person_ref=actor,
            operation_id="b08-d:activity-second-start",
            subject_kind="activity",
            subject_native_ref=activity.activity_ref,
        )
        assert second.session_ref != started.session_ref
        assert second.duration_evaluations[0].evaluation == "pending"
        listed = await sessions.list_for_subject(
            self_person_ref=actor,
            subject_native_ref=activity.activity_ref,
        )
        assert [item.session_ref for item in listed] == [started.session_ref, second.session_ref]
        assert listed[0].duration_evaluations[0].evaluation == "violated"
        assert listed[1].duration_evaluations[0].evaluation == "pending"

        with _admin(migrated_database) as connection:
            schedule_count, actual_count, old_end, history_count = connection.execute(
                """
                SELECT
                  (SELECT count(*) FROM dante.schedule WHERE subject_native_ref=%s),
                  (SELECT count(*) FROM dante.actual WHERE subject_native_ref=%s),
                  (SELECT ended_at FROM dante.session_timing_absolute
                    WHERE material_state_ref=%s),
                  (SELECT count(*) FROM dante.session_timing_current_history
                    WHERE session_ref=%s)
                """,
                (
                    activity.activity_ref,
                    activity.activity_ref,
                    started.timing_material_state_ref,
                    started.session_ref,
                ),
            ).fetchone()
        assert (schedule_count, actual_count, old_end, history_count) == (0, 0, None, 4)
    finally:
        await runtime.dispose()


@pytest.mark.asyncio
async def test_occurrence_session_does_not_inherit_activity_duration_or_place_itself(
    migrated_database: Any,
) -> None:
    actor = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    areas = LifeAreaApplication(runtime.session_factory)
    routines = RoutineApplication(runtime.session_factory)
    occurrences = OccurrenceApplication(runtime.session_factory)
    sessions = SessionApplication(runtime.session_factory)
    try:
        area = (
            await areas.create(
                self_person_ref=actor, operation_id="b08-d:occurrence-area", name="Routine"
            )
        ).area
        routine = await routines.create(
            self_person_ref=actor,
            operation_id="b08-d:routine",
            title="Occurrence episode",
            life_area_ref=area.life_area_ref,
            starts_on=date(2026, 10, 1),
            wall_time=time(8),
        )
        checkpoint = await occurrences.checkpoint(
            owner="routine",
            self_person_ref=actor,
            source_ref=routine.routine_ref,
            operation_id="b08-d:checkpoint",
            start_date=date(2026, 10, 1),
            end_date_exclusive=date(2026, 10, 2),
            effective_zone_id="Europe/Rome",
        )
        occurrence_ref = NativeRef(checkpoint.occurrences[0].occurrence_ref)
        started = await sessions.start(
            self_person_ref=actor,
            operation_id="b08-d:occurrence-start",
            subject_kind="occurrence",
            subject_native_ref=occurrence_ref,
        )
        assert started.open and started.duration_evaluations == ()
        paused = await sessions.pause(
            self_person_ref=actor,
            operation_id="b08-d:occurrence-pause",
            session_ref=started.session_ref,
            expected_material_state_ref=started.timing_material_state_ref,
        )
        resumed = await sessions.resume(
            self_person_ref=actor,
            operation_id="b08-d:occurrence-resume",
            session_ref=paused.session_ref,
            expected_material_state_ref=paused.timing_material_state_ref,
        )
        ended = await sessions.end(
            self_person_ref=actor,
            operation_id="b08-d:occurrence-end",
            session_ref=resumed.session_ref,
            expected_material_state_ref=resumed.timing_material_state_ref,
        )
        reloaded = await sessions.get(self_person_ref=actor, session_ref=started.session_ref)
        assert reloaded.session_ref == started.session_ref
        assert not reloaded.open and reloaded.duration_evaluations == ()
        assert ended.active_seconds <= ended.elapsed_seconds + 0.001
        assert not (
            await occurrences.get(self_person_ref=actor, occurrence_ref=occurrence_ref)
        ).skipped
        with _admin(migrated_database) as connection:
            counts = connection.execute(
                """
                SELECT
                  (SELECT count(*) FROM dante.schedule WHERE subject_native_ref=%s),
                  (SELECT count(*) FROM dante.actual WHERE subject_native_ref=%s)
                """,
                (occurrence_ref, occurrence_ref),
            ).fetchone()
        assert counts == (0, 0)
    finally:
        await runtime.dispose()
