"""B13-C real PostgreSQL proof for Plan-contextual execution intent."""

from __future__ import annotations

from typing import Any

import pytest
from tests.integration.temporal.b05_legacy_test_support import ensure_test_life_area
from tests.integration.temporal.test_b02_schedule_create import _seed_self_person

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

pytestmark = pytest.mark.postgres


@pytest.mark.asyncio
async def test_b13_c_plan_step_policy_revision_scope_and_replay(migrated_database: Any) -> None:
    alice = _seed_self_person(migrated_database)
    bob = _seed_self_person(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    plans = PlanWorkApplication(runtime.session_factory)
    activities = TemporalActivityApplication(runtime.session_factory)
    try:
        activity_ref = (
            await activities.create_activity(
                self_person_ref=alice,
                life_area_ref=ensure_test_life_area(migrated_database, alice),
                operation_id="b13c:activity",
                title="Recording",
            )
        ).activity.activity_ref
        step_ref = new_native_ref()
        created = await plans.create(self_person_ref=alice, operation_id="b13c:plan", title="Album")
        policy = PlanStepInput(
            step_ref=step_ref, title="Recording", activity_ref=activity_ref,
            divisible=True, max_planned_slices=3, merge_compatible=True,
            execution_strength_code="hard",
        )
        first = await plans.replace(
            self_person_ref=alice, plan_ref=created.plan_ref,
            expected_state_ref=created.state_ref, operation_id="b13c:configure",
            title="Album", steps=(policy,),
        )
        assert first.steps[0].max_planned_slices == 3
        assert first.steps[0].execution_strength_code == "hard"
        assert (await plans.get(self_person_ref=alice, plan_ref=created.plan_ref)) == first
        assert await plans.get(self_person_ref=bob, plan_ref=created.plan_ref) is None
        assert (await plans.replace(
            self_person_ref=alice, plan_ref=created.plan_ref,
            expected_state_ref=created.state_ref, operation_id="b13c:configure",
            title="Album", steps=(policy,),
        )).replayed
        with pytest.raises(PlanWorkConflictError):
            await plans.replace(
                self_person_ref=alice, plan_ref=created.plan_ref,
                expected_state_ref=created.state_ref, operation_id="b13c:stale",
                title="Album", steps=(policy,),
            )
        with pytest.raises(PlanWorkNotFoundError):
            await plans.replace(
                self_person_ref=bob, plan_ref=created.plan_ref,
                expected_state_ref=first.state_ref, operation_id="b13c:foreign",
                title="Album", steps=(policy,),
            )
        with pytest.raises(PlanWorkInputError):
            await plans.replace(
                self_person_ref=alice, plan_ref=created.plan_ref,
                expected_state_ref=first.state_ref, operation_id="b13c:contradictory",
                title="Album", steps=(PlanStepInput(
                    step_ref=step_ref, title="Recording", activity_ref=activity_ref,
                    divisible=False, max_planned_slices=2, merge_compatible=True,
                    execution_strength_code="hard",
                ),),
            )
        second = await plans.replace(
            self_person_ref=alice, plan_ref=created.plan_ref,
            expected_state_ref=first.state_ref, operation_id="b13c:indivisible",
            title="Album", steps=(PlanStepInput(
                step_ref=step_ref, title="Recording", activity_ref=activity_ref,
                divisible=False, max_planned_slices=1, merge_compatible=False,
                execution_strength_code="soft",
            ),),
        )
        assert second.steps[0].divisible is False
        assert second.steps[0].max_planned_slices == 1
        retired = await plans.replace(
            self_person_ref=alice, plan_ref=created.plan_ref,
            expected_state_ref=second.state_ref, operation_id="b13c:retire",
            title="Album", steps=(PlanStepInput(
                step_ref=step_ref, title="Recording", activity_ref=activity_ref,
            ),),
        )
        assert retired.steps[0].divisible is None
        assert retired.steps[0].max_planned_slices is None
        assert (await plans.get(self_person_ref=alice, plan_ref=created.plan_ref)) == retired
    finally:
        await runtime.dispose()
