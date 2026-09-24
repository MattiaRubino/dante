"""B08-B proof: Session pause/resume advances immutable timing state only."""

from __future__ import annotations

from typing import Any

import psycopg
import pytest

from dante.modules.temporal.activity import TemporalActivityApplication
from dante.modules.temporal.life_area import LifeAreaApplication
from dante.modules.temporal.session_runtime import (
    SessionApplication,
    SessionPauseConflictError,
    SessionResumeConflictError,
)
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
async def test_b08_b_pause_resume_is_idempotent_and_preserves_timing_history(
    migrated_database: Any,
) -> None:
    alice = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    areas = LifeAreaApplication(runtime.session_factory)
    activities = TemporalActivityApplication(runtime.session_factory)
    sessions = SessionApplication(runtime.session_factory)
    try:
        area = (
            await areas.create(
                self_person_ref=alice,
                operation_id="b08-b:area",
                name="Focus",
            )
        ).area
        activity = (
            await activities.create_activity(
                self_person_ref=alice,
                operation_id="b08-b:activity",
                title="Pause proof",
                life_area_ref=area.life_area_ref,
            )
        ).activity
        started = await sessions.start(
            self_person_ref=alice,
            operation_id="b08-b:start",
            subject_kind="activity",
            subject_native_ref=activity.activity_ref,
        )
        paused = await sessions.pause(
            self_person_ref=alice,
            operation_id="b08-b:pause",
            session_ref=started.session_ref,
            expected_material_state_ref=started.timing_material_state_ref,
        )
        assert paused.session_ref == started.session_ref
        assert paused.paused
        assert paused.timing_material_state_ref != started.timing_material_state_ref
        replay = await sessions.pause(
            self_person_ref=alice,
            operation_id="b08-b:pause",
            session_ref=started.session_ref,
            expected_material_state_ref=started.timing_material_state_ref,
        )
        assert replay.replayed
        assert replay.timing_material_state_ref == paused.timing_material_state_ref
        with pytest.raises(SessionPauseConflictError):
            await sessions.pause(
                self_person_ref=alice,
                operation_id="b08-b:pause-again",
                session_ref=started.session_ref,
                expected_material_state_ref=paused.timing_material_state_ref,
            )

        rehydrated_pause = await sessions.get(
            self_person_ref=alice, session_ref=started.session_ref
        )
        assert rehydrated_pause.paused
        resumed = await sessions.resume(
            self_person_ref=alice,
            operation_id="b08-b:resume",
            session_ref=started.session_ref,
            expected_material_state_ref=paused.timing_material_state_ref,
        )
        assert not resumed.paused
        assert resumed.timing_material_state_ref != paused.timing_material_state_ref
        with pytest.raises(SessionResumeConflictError):
            await sessions.resume(
                self_person_ref=alice,
                operation_id="b08-b:resume-again",
                session_ref=started.session_ref,
                expected_material_state_ref=resumed.timing_material_state_ref,
            )

        with _admin(migrated_database) as connection:
            old_pause, completed_pause, state_count = connection.execute(
                """
                SELECT
                  (SELECT resumed_at FROM dante.session_timing_pause
                    WHERE material_state_ref=%s),
                  (SELECT resumed_at FROM dante.session_timing_pause
                    WHERE material_state_ref=%s),
                  (SELECT count(*) FROM dante.session_timing_current_history
                    WHERE session_ref=%s)
                """,
                (
                    paused.timing_material_state_ref,
                    resumed.timing_material_state_ref,
                    started.session_ref,
                ),
            ).fetchone()
        assert old_pause is None
        assert completed_pause is not None
        assert state_count == 3
    finally:
        await runtime.dispose()
