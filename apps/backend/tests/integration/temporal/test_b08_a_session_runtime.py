"""B08-A behavioral proof for Activity/Occurrence Session start, read, and end."""

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
    SessionNotFoundError,
    SessionOperationReuseError,
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
async def test_b08_a_activity_session_is_scoped_idempotent_and_does_not_fabricate_reality(
    migrated_database: Any,
) -> None:
    alice = _seed_self(migrated_database)
    bob = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    areas = LifeAreaApplication(runtime.session_factory)
    activities = TemporalActivityApplication(runtime.session_factory)
    sessions = SessionApplication(runtime.session_factory)
    try:
        area = (
            await areas.create(
                self_person_ref=alice,
                operation_id="b08-a:activity-area",
                name="Focus",
            )
        ).area
        activity = (
            await activities.create_activity(
                self_person_ref=alice,
                operation_id="b08-a:activity",
                title="Write B08 proof",
                life_area_ref=area.life_area_ref,
            )
        ).activity
        other_activity = (
            await activities.create_activity(
                self_person_ref=alice,
                operation_id="b08-a:activity-other",
                title="Different B08 proof",
                life_area_ref=area.life_area_ref,
            )
        ).activity

        started = await sessions.start(
            self_person_ref=alice,
            operation_id="b08-a:activity-start",
            subject_kind="activity",
            subject_native_ref=activity.activity_ref,
        )
        assert started.open
        assert started.subject_native_ref == activity.activity_ref

        replay = await sessions.start(
            self_person_ref=alice,
            operation_id="b08-a:activity-start",
            subject_kind="activity",
            subject_native_ref=activity.activity_ref,
        )
        assert replay.replayed
        assert replay.session_ref == started.session_ref
        assert replay.timing_material_state_ref == started.timing_material_state_ref

        with pytest.raises(SessionOperationReuseError):
            await sessions.start(
                self_person_ref=alice,
                operation_id="b08-a:activity-start",
                subject_kind="activity",
                subject_native_ref=other_activity.activity_ref,
            )

        listed = await sessions.list_for_subject(
            self_person_ref=alice,
            subject_native_ref=activity.activity_ref,
        )
        assert [item.session_ref for item in listed] == [started.session_ref]
        fetched = await sessions.get(self_person_ref=alice, session_ref=started.session_ref)
        assert fetched.session_ref == started.session_ref
        assert fetched.open

        with pytest.raises(SessionNotFoundError):
            await sessions.start(
                self_person_ref=alice,
                operation_id="b08-a:activity-wrong-family",
                subject_kind="occurrence",
                subject_native_ref=activity.activity_ref,
            )
        with pytest.raises(SessionNotFoundError):
            await sessions.start(
                self_person_ref=bob,
                operation_id="b08-a:activity-foreign",
                subject_kind="activity",
                subject_native_ref=activity.activity_ref,
            )

        ended = await sessions.end(
            self_person_ref=alice,
            operation_id="b08-a:activity-end",
            session_ref=started.session_ref,
            expected_material_state_ref=started.timing_material_state_ref,
        )
        assert not ended.open
        assert ended.ended_at is not None
        assert ended.timing_material_state_ref == started.timing_material_state_ref

        end_replay = await sessions.end(
            self_person_ref=alice,
            operation_id="b08-a:activity-end",
            session_ref=started.session_ref,
            expected_material_state_ref=started.timing_material_state_ref,
        )
        assert end_replay.replayed
        assert end_replay.session_ref == started.session_ref
        assert end_replay.ended_at == ended.ended_at

        with pytest.raises(SessionEndConflictError):
            await sessions.end(
                self_person_ref=alice,
                operation_id="b08-a:activity-end-again",
                session_ref=started.session_ref,
                expected_material_state_ref=started.timing_material_state_ref,
            )

        restarted = await sessions.start(
            self_person_ref=alice,
            operation_id="b08-a:activity-restart",
            subject_kind="activity",
            subject_native_ref=activity.activity_ref,
        )
        assert restarted.session_ref != started.session_ref
        assert restarted.open

        with _admin(migrated_database) as connection:
            schedule_count, actual_count, subject_count = connection.execute(
                """
                SELECT
                  (SELECT count(*) FROM dante.schedule WHERE subject_native_ref=%s),
                  (SELECT count(*) FROM dante.actual WHERE subject_native_ref=%s),
                  (SELECT count(*) FROM dante.session_execution_subject
                     WHERE subject_native_ref=%s)
                """,
                (activity.activity_ref, activity.activity_ref, activity.activity_ref),
            ).fetchone()
        assert schedule_count == 0
        assert actual_count == 0
        assert subject_count == 2
    finally:
        await runtime.dispose()


@pytest.mark.asyncio
async def test_b08_a_occurrence_session_uses_the_occurrence_identity_without_schedule(
    migrated_database: Any,
) -> None:
    alice = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    areas = LifeAreaApplication(runtime.session_factory)
    routines = RoutineApplication(runtime.session_factory)
    occurrences = OccurrenceApplication(runtime.session_factory)
    sessions = SessionApplication(runtime.session_factory)
    try:
        area = (
            await areas.create(
                self_person_ref=alice,
                operation_id="b08-a:occurrence-area",
                name="Routine",
            )
        ).area
        routine = await routines.create(
            self_person_ref=alice,
            operation_id="b08-a:routine",
            title="Session proof routine",
            life_area_ref=area.life_area_ref,
            starts_on=date(2026, 10, 1),
            wall_time=time(8),
        )
        checkpoint = await occurrences.checkpoint(
            owner="routine",
            self_person_ref=alice,
            source_ref=routine.routine_ref,
            operation_id="b08-a:occurrence-checkpoint",
            start_date=date(2026, 10, 1),
            end_date_exclusive=date(2026, 10, 2),
            effective_zone_id="Europe/Rome",
        )
        assert checkpoint.occurrences
        occurrence_ref = NativeRef(checkpoint.occurrences[0].occurrence_ref)

        with pytest.raises(SessionNotFoundError):
            await sessions.start(
                self_person_ref=alice,
                operation_id="b08-a:occurrence-wrong-family",
                subject_kind="activity",
                subject_native_ref=occurrence_ref,
            )

        started = await sessions.start(
            self_person_ref=alice,
            operation_id="b08-a:occurrence-start",
            subject_kind="occurrence",
            subject_native_ref=occurrence_ref,
        )
        assert started.open
        assert started.subject_native_ref == occurrence_ref

        fetched = await sessions.get(self_person_ref=alice, session_ref=started.session_ref)
        assert fetched.session_ref == started.session_ref
        assert fetched.subject_native_ref == occurrence_ref

        ended = await sessions.end(
            self_person_ref=alice,
            operation_id="b08-a:occurrence-end",
            session_ref=started.session_ref,
            expected_material_state_ref=started.timing_material_state_ref,
        )
        assert not ended.open
        assert ended.ended_at is not None

        canonical_occurrence = await occurrences.get(
            self_person_ref=alice,
            occurrence_ref=occurrence_ref,
        )
        assert not canonical_occurrence.skipped

        with _admin(migrated_database) as connection:
            schedule_count, actual_count = connection.execute(
                """
                SELECT
                  (SELECT count(*) FROM dante.schedule WHERE subject_native_ref=%s),
                  (SELECT count(*) FROM dante.actual WHERE subject_native_ref=%s)
                """,
                (occurrence_ref, occurrence_ref),
            ).fetchone()
        assert schedule_count == 0
        assert actual_count == 0
    finally:
        await runtime.dispose()
