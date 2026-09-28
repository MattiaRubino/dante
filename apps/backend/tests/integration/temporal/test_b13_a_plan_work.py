"""B13-A real PostgreSQL proof: Plan-owned Steps, ordering and history."""

from __future__ import annotations

from typing import Any

import psycopg
import pytest

from dante.modules.temporal.activity import TemporalActivityApplication
from dante.modules.temporal.plan_work import (
    PlanStepInput,
    PlanWorkApplication,
    PlanWorkConflictError,
    PlanWorkInputError,
    PlanWorkNotFoundError,
)
from dante.platform.database.references import new_native_ref
from dante.platform.database.runtime import create_database_runtime
from tests.integration.temporal.b05_legacy_test_support import ensure_test_life_area
from tests.integration.temporal.test_b02_schedule_create import _seed_self_person

pytestmark = pytest.mark.postgres


@pytest.mark.asyncio
async def test_b13_a_plan_structure_is_self_owned_ordered_and_historical(
    migrated_database: Any,
) -> None:
    alice = _seed_self_person(migrated_database)
    bob = _seed_self_person(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    plans = PlanWorkApplication(runtime.session_factory)
    activities = TemporalActivityApplication(runtime.session_factory)
    try:
        created = await plans.create(
            self_person_ref=alice, operation_id="b13a:create", title="Album"
        )
        assert created.plan_ref.version == created.state_ref.version == 7
        assert created.steps == ()
        assert (
            await plans.create(
                self_person_ref=alice, operation_id="b13a:create", title="Album"
            )
        ).replayed
        with pytest.raises(PlanWorkConflictError):
            await plans.create(
                self_person_ref=alice, operation_id="b13a:create", title="Different"
            )
        assert await plans.get(self_person_ref=bob, plan_ref=created.plan_ref) is None
        assert [item.plan_ref for item in await plans.list(self_person_ref=alice)] == [
            created.plan_ref
        ]

        activity = await activities.create_activity(
            self_person_ref=alice,
            life_area_ref=ensure_test_life_area(migrated_database, alice),
            operation_id="b13a:activity",
            title="Record vocals",
        )
        voice = new_native_ref()
        mix = new_native_ref()
        steps = (
            PlanStepInput(
                step_ref=voice, title="Record", activity_ref=activity.activity.activity_ref
            ),
            PlanStepInput(step_ref=mix, title="Mix"),
        )
        first = await plans.replace(
            self_person_ref=alice, plan_ref=created.plan_ref,
            expected_state_ref=created.state_ref,
            operation_id="b13a:steps", title="Album", steps=steps,
        )
        assert [(item.title, item.position) for item in first.steps] == [
            ("Record", 0), ("Mix", 1)
        ]
        assert first.steps[0].activity_ref == activity.activity.activity_ref
        assert first.steps[0].step_ref != first.steps[0].activity_ref
        reordered = await plans.replace(
            self_person_ref=alice, plan_ref=created.plan_ref,
            expected_state_ref=first.state_ref,
            operation_id="b13a:reorder", title="Album", steps=(steps[1], steps[0]),
        )
        assert [item.step_ref for item in reordered.steps] == [mix, voice]
        assert reordered.state_ref != first.state_ref
        assert (await plans.get(
            self_person_ref=alice, plan_ref=created.plan_ref
        )).state_ref == reordered.state_ref
        replay = await plans.replace(
            self_person_ref=alice, plan_ref=created.plan_ref,
            expected_state_ref=first.state_ref,
            operation_id="b13a:reorder", title="Album", steps=(steps[1], steps[0]),
        )
        assert replay.replayed and replay.state_ref == reordered.state_ref
        with pytest.raises(PlanWorkConflictError):
            await plans.replace(
                self_person_ref=alice, plan_ref=created.plan_ref,
                expected_state_ref=first.state_ref,
                operation_id="b13a:stale", title="Album", steps=steps,
            )
        with pytest.raises(PlanWorkConflictError):
            await plans.replace(
                self_person_ref=alice, plan_ref=created.plan_ref,
                expected_state_ref=reordered.state_ref,
                operation_id="b13a:duplicate-step", title="Album",
                steps=(steps[0], steps[0]),
            )
        with pytest.raises(PlanWorkConflictError):
            await plans.replace(
                self_person_ref=alice, plan_ref=created.plan_ref,
                expected_state_ref=reordered.state_ref,
                operation_id="b13a:duplicate-link", title="Album",
                steps=(
                    steps[0],
                    PlanStepInput(
                        step_ref=mix, title="Mix",
                        activity_ref=activity.activity.activity_ref,
                    ),
                ),
            )
        with pytest.raises(PlanWorkNotFoundError):
            await plans.replace(
                self_person_ref=alice, plan_ref=created.plan_ref,
                expected_state_ref=reordered.state_ref,
                operation_id="b13a:foreign-activity", title="Album",
                steps=(PlanStepInput(
                    step_ref=mix, title="Foreign Activity",
                    activity_ref=new_native_ref(),
                ),),
            )
        with pytest.raises(PlanWorkInputError):
            await plans.replace(
                self_person_ref=alice, plan_ref=created.plan_ref,
                expected_state_ref=reordered.state_ref,
                operation_id="b13a:bad-title", title=" ", steps=steps,
            )
        with pytest.raises(PlanWorkNotFoundError):
            await plans.replace(
                self_person_ref=bob, plan_ref=created.plan_ref,
                expected_state_ref=reordered.state_ref,
                operation_id="b13a:foreign-owner", title="Album", steps=steps,
            )

        another = await plans.create(
            self_person_ref=alice, operation_id="b13a:second-plan", title="Other"
        )
        with pytest.raises(PlanWorkNotFoundError):
            await plans.replace(
                self_person_ref=alice, plan_ref=another.plan_ref,
                expected_state_ref=another.state_ref,
                operation_id="b13a:cross-plan", title="Other",
                steps=(PlanStepInput(step_ref=voice, title="Foreign Step"),),
            )
        with psycopg.connect(
            host=migrated_database.cluster.host,
            port=migrated_database.cluster.port,
            dbname=migrated_database.name,
            user=migrated_database.cluster.admin_user,
            password=migrated_database.cluster.admin_password,
        ) as connection:
            states = connection.execute(
                "SELECT state_ref FROM dante.plan_work_state "
                "WHERE plan_ref=%s ORDER BY recorded_at",
                (created.plan_ref,),
            ).fetchall()
            history = connection.execute(
                "SELECT state_ref,current_until_at FROM dante.plan_work_current_history "
                "WHERE plan_ref=%s ORDER BY current_from_at",
                (created.plan_ref,),
            ).fetchall()
            old_steps = connection.execute(
                "SELECT step_ref,position FROM dante.plan_step_in_state "
                "WHERE state_ref=%s ORDER BY position",
                (first.state_ref,),
            ).fetchall()
        assert len(states) == len(history) == 3
        assert history[-1] == (reordered.state_ref, None)
        assert all(row[1] is not None for row in history[:-1])
        assert old_steps == [(voice, 0), (mix, 1)]
    finally:
        await runtime.engine.dispose()
