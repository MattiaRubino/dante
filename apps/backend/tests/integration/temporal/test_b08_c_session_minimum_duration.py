"""B08-C proof: TC-009 evaluates one Activity Session's active duration."""

from __future__ import annotations

from typing import Any

import pytest

from dante.modules.temporal.activity import TemporalActivityApplication
from dante.modules.temporal.life_area import LifeAreaApplication
from dante.modules.temporal.session_runtime import SessionApplication
from dante.modules.temporal.temporal_constraint import (
    SessionMinimumDurationRule,
    TemporalConstraintApplication,
)
from dante.platform.database.runtime import create_database_runtime
from tests.integration.temporal.test_b05_primary_life_area_assignment import _seed_self

pytestmark = pytest.mark.postgres


@pytest.mark.asyncio
async def test_b08_c_minimum_uses_one_session_active_time_and_never_blocks_end(
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
                self_person_ref=actor,
                operation_id="b08-c:area",
                name="Focus",
            )
        ).area
        activity = (
            await activities.create_activity(
                self_person_ref=actor,
                operation_id="b08-c:activity",
                title="Minimum duration proof",
                life_area_ref=area.life_area_ref,
            )
        ).activity
        rule = SessionMinimumDurationRule(duration_microseconds=86_400_000_000)
        created = await constraints.create_constraint(
            self_person_ref=actor,
            operation_id="b08-c:constraint",
            subject_native_ref=activity.activity_ref,
            rule=rule,
        )
        assert created.rule == rule

        started = await sessions.start(
            self_person_ref=actor,
            operation_id="b08-c:start",
            subject_kind="activity",
            subject_native_ref=activity.activity_ref,
        )
        assert len(started.duration_evaluations) == 1
        evaluation = started.duration_evaluations[0]
        assert evaluation.constraint_ref == created.constraint_ref
        assert evaluation.material_state_ref == created.material_state_ref
        assert evaluation.evaluation == "pending"

        paused = await sessions.pause(
            self_person_ref=actor,
            operation_id="b08-c:pause",
            session_ref=started.session_ref,
            expected_material_state_ref=started.timing_material_state_ref,
        )
        assert paused.duration_evaluations[0].evaluation == "pending"
        resumed = await sessions.resume(
            self_person_ref=actor,
            operation_id="b08-c:resume",
            session_ref=paused.session_ref,
            expected_material_state_ref=paused.timing_material_state_ref,
        )
        ended = await sessions.end(
            self_person_ref=actor,
            operation_id="b08-c:end",
            session_ref=resumed.session_ref,
            expected_material_state_ref=resumed.timing_material_state_ref,
        )
        assert ended.open is False
        assert ended.duration_evaluations[0].evaluation == "violated"
        assert ended.session_ref == started.session_ref
        assert ended.active_seconds <= ended.elapsed_seconds + 0.001

        separate = await sessions.start(
            self_person_ref=actor,
            operation_id="b08-c:start-separate",
            subject_kind="activity",
            subject_native_ref=activity.activity_ref,
        )
        assert separate.session_ref != ended.session_ref
        assert separate.duration_evaluations[0].evaluation == "pending"
    finally:
        await runtime.dispose()
