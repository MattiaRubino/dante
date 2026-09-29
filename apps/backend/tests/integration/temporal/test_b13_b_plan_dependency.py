"""B13-B PostgreSQL proof of scoped direction, current truth and history."""

from __future__ import annotations

from typing import Any

import psycopg
import pytest
from tests.integration.temporal.b05_legacy_test_support import ensure_test_life_area
from tests.integration.temporal.test_b02_schedule_create import _seed_self_person

from dante.modules.temporal.activity import TemporalActivityApplication
from dante.modules.temporal.actual_runtime import ActualApplication
from dante.modules.temporal.outcome_runtime import OutcomeApplication
from dante.modules.temporal.plan_dependency import (
    PlanDependencyApplication,
    PlanDependencyConflictError,
    PlanDependencyNotFoundError,
)
from dante.modules.temporal.plan_work import (
    PlanStepInput,
    PlanWorkApplication,
    PlanWorkInputError,
)
from dante.platform.database.references import new_native_ref
from dante.platform.database.runtime import create_database_runtime

pytestmark = pytest.mark.postgres


@pytest.mark.asyncio
async def test_b13_b_dependency_reacts_to_current_actual_and_outcome(
    migrated_database: Any,
) -> None:
    alice = _seed_self_person(migrated_database)
    bob = _seed_self_person(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    plans = PlanWorkApplication(runtime.session_factory)
    dependencies = PlanDependencyApplication(runtime.session_factory)
    activities = TemporalActivityApplication(runtime.session_factory)
    actuals = ActualApplication(runtime.session_factory)
    outcomes = OutcomeApplication(runtime.session_factory)
    try:
        area = ensure_test_life_area(migrated_database, alice)
        first_activity = (
            await activities.create_activity(
                self_person_ref=alice,
                life_area_ref=area,
                operation_id="b13b:first-activity",
                title="Record",
            )
        ).activity.activity_ref
        second_activity = (
            await activities.create_activity(
                self_person_ref=alice,
                life_area_ref=area,
                operation_id="b13b:second-activity",
                title="Mix",
            )
        ).activity.activity_ref
        third_activity = (
            await activities.create_activity(
                self_person_ref=alice,
                life_area_ref=area,
                operation_id="b13b:third-activity",
                title="Master",
            )
        ).activity.activity_ref
        first_step, second_step = new_native_ref(), new_native_ref()
        steps = (
            PlanStepInput(step_ref=first_step, title="Record", activity_ref=first_activity),
            PlanStepInput(step_ref=second_step, title="Mix", activity_ref=second_activity),
        )
        plan = await plans.create(
            self_person_ref=alice,
            operation_id="b13b:plan",
            title="Album",
        )
        plan = await plans.replace(
            self_person_ref=alice,
            plan_ref=plan.plan_ref,
            expected_state_ref=plan.state_ref,
            operation_id="b13b:steps",
            title="Album",
            steps=steps,
        )
        actual_rule = await dependencies.write(
            self_person_ref=alice,
            plan_ref=plan.plan_ref,
            operation_id="b13b:actual-rule",
            prerequisite_step_ref=first_step,
            dependent_step_ref=second_step,
            qualifier_code="actual_occurred",
            disposition_code=None,
        )
        assert actual_rule.evaluation_code == "unknown"
        assert not actual_rule.cycle
        assert (
            await dependencies.write(
                self_person_ref=alice,
                plan_ref=plan.plan_ref,
                operation_id="b13b:actual-rule",
                prerequisite_step_ref=first_step,
                dependent_step_ref=second_step,
                qualifier_code="actual_occurred",
                disposition_code=None,
            )
        ).replayed
        assert await dependencies.list(self_person_ref=bob, plan_ref=plan.plan_ref) == ()
        assert (
            await dependencies.get(
                self_person_ref=bob,
                plan_ref=plan.plan_ref,
                dependency_ref=actual_rule.dependency_ref,
            )
            is None
        )
        with pytest.raises(PlanDependencyConflictError):
            await dependencies.write(
                self_person_ref=alice,
                plan_ref=plan.plan_ref,
                operation_id="b13b:duplicate",
                prerequisite_step_ref=first_step,
                dependent_step_ref=second_step,
                qualifier_code="actual_occurred",
                disposition_code=None,
            )
        with pytest.raises(PlanDependencyNotFoundError):
            await dependencies.write(
                self_person_ref=bob,
                plan_ref=plan.plan_ref,
                operation_id="b13b:foreign",
                prerequisite_step_ref=first_step,
                dependent_step_ref=second_step,
                qualifier_code="outcome_code",
                disposition_code="work.completed",
            )
        with pytest.raises(PlanWorkInputError, match="Active Plan Dependency endpoint"):
            await plans.replace(
                self_person_ref=alice,
                plan_ref=plan.plan_ref,
                expected_state_ref=plan.state_ref,
                operation_id="b13b:remove-active",
                title="Album",
                steps=steps[1:],
            )
        with pytest.raises(PlanWorkInputError, match="Active Plan Dependency endpoint"):
            await plans.replace(
                self_person_ref=alice,
                plan_ref=plan.plan_ref,
                expected_state_ref=plan.state_ref,
                operation_id="b13b:relink-active",
                title="Album",
                steps=(
                    PlanStepInput(step_ref=first_step, title="Record", activity_ref=third_activity),
                    steps[1],
                ),
            )
        reordered = await plans.replace(
            self_person_ref=alice,
            plan_ref=plan.plan_ref,
            expected_state_ref=plan.state_ref,
            operation_id="b13b:reorder",
            title="Album",
            steps=(steps[1], steps[0]),
        )
        assert reordered.steps[1].step_ref == first_step
        assert (
            await dependencies.get(
                self_person_ref=alice,
                plan_ref=plan.plan_ref,
                dependency_ref=actual_rule.dependency_ref,
            )
        ).prerequisite_activity_ref == first_activity
        actual = await actuals.record(
            self_person_ref=alice,
            operation_id="b13b:actual-false",
            subject_kind="activity",
            subject_native_ref=first_activity,
            realization_occurred=False,
            expected_material_state_ref=None,
        )
        assert (
            await dependencies.get(
                self_person_ref=alice,
                plan_ref=plan.plan_ref,
                dependency_ref=actual_rule.dependency_ref,
            )
        ).evaluation_code == "unsatisfied"
        actual = await actuals.record(
            self_person_ref=alice,
            operation_id="b13b:actual-true",
            subject_kind="activity",
            subject_native_ref=first_activity,
            realization_occurred=True,
            expected_material_state_ref=actual.material_state_ref,
        )
        assert (
            await dependencies.get(
                self_person_ref=alice,
                plan_ref=plan.plan_ref,
                dependency_ref=actual_rule.dependency_ref,
            )
        ).evaluation_code == "satisfied"
        outcome_rule = await dependencies.write(
            self_person_ref=alice,
            plan_ref=plan.plan_ref,
            operation_id="b13b:outcome-rule",
            prerequisite_step_ref=first_step,
            dependent_step_ref=second_step,
            qualifier_code="outcome_code",
            disposition_code="work.completed",
        )
        assert outcome_rule.evaluation_code == "unknown"
        outcome = await outcomes.record(
            self_person_ref=alice,
            operation_id="b13b:outcome-partial",
            actual_ref=actual.actual_ref,
            actual_realization_material_state_ref=actual.material_state_ref,
            expected_material_state_ref=None,
            disposition_code="work.partial",
        )
        assert (
            await dependencies.get(
                self_person_ref=alice,
                plan_ref=plan.plan_ref,
                dependency_ref=outcome_rule.dependency_ref,
            )
        ).evaluation_code == "unsatisfied"
        outcome = await outcomes.record(
            self_person_ref=alice,
            operation_id="b13b:outcome-completed",
            actual_ref=actual.actual_ref,
            actual_realization_material_state_ref=actual.material_state_ref,
            expected_material_state_ref=outcome.material_state_ref,
            disposition_code="work.completed",
        )
        assert (
            await dependencies.get(
                self_person_ref=alice,
                plan_ref=plan.plan_ref,
                dependency_ref=outcome_rule.dependency_ref,
            )
        ).evaluation_code == "satisfied"
        corrected_actual = await actuals.record(
            self_person_ref=alice,
            operation_id="b13b:actual-correct",
            subject_kind="activity",
            subject_native_ref=first_activity,
            realization_occurred=False,
            expected_material_state_ref=actual.material_state_ref,
        )
        assert (
            await dependencies.get(
                self_person_ref=alice,
                plan_ref=plan.plan_ref,
                dependency_ref=outcome_rule.dependency_ref,
            )
        ).evaluation_code == "unknown"
        assert (
            await dependencies.get(
                self_person_ref=alice,
                plan_ref=plan.plan_ref,
                dependency_ref=actual_rule.dependency_ref,
            )
        ).evaluation_code == "unsatisfied"
        outcome = await outcomes.record(
            self_person_ref=alice,
            operation_id="b13b:outcome-rebased",
            actual_ref=actual.actual_ref,
            actual_realization_material_state_ref=corrected_actual.material_state_ref,
            expected_material_state_ref=outcome.material_state_ref,
            disposition_code="work.completed",
        )
        assert (
            await dependencies.get(
                self_person_ref=alice,
                plan_ref=plan.plan_ref,
                dependency_ref=outcome_rule.dependency_ref,
            )
        ).evaluation_code == "satisfied"
        revised = await dependencies.write(
            self_person_ref=alice,
            plan_ref=plan.plan_ref,
            dependency_ref=actual_rule.dependency_ref,
            expected_state_ref=actual_rule.state_ref,
            operation_id="b13b:revise-actual-qualifier",
            prerequisite_step_ref=first_step,
            dependent_step_ref=second_step,
            qualifier_code="outcome_code",
            disposition_code="work.partial",
        )
        assert revised.dependency_ref == actual_rule.dependency_ref
        assert revised.state_ref != actual_rule.state_ref
        assert revised.evaluation_code == "unsatisfied"
        assert [
            row.state_ref
            for row in await dependencies.history(
                self_person_ref=alice,
                plan_ref=plan.plan_ref,
                dependency_ref=actual_rule.dependency_ref,
            )
        ] == [actual_rule.state_ref, revised.state_ref]
        with pytest.raises(PlanDependencyConflictError):
            await dependencies.write(
                self_person_ref=alice,
                plan_ref=plan.plan_ref,
                dependency_ref=outcome_rule.dependency_ref,
                expected_state_ref=new_native_ref(),
                operation_id="b13b:stale-revision",
                prerequisite_step_ref=first_step,
                dependent_step_ref=second_step,
                qualifier_code="outcome_code",
                disposition_code="work.completed",
            )
        retired = await dependencies.write(
            self_person_ref=alice,
            plan_ref=plan.plan_ref,
            dependency_ref=outcome_rule.dependency_ref,
            expected_state_ref=outcome_rule.state_ref,
            operation_id="b13b:retire-outcome",
            prerequisite_step_ref=first_step,
            dependent_step_ref=second_step,
            qualifier_code="outcome_code",
            disposition_code="work.completed",
            active=False,
        )
        assert not retired.active
        assert retired.evaluation_code is None
        history = await dependencies.history(
            self_person_ref=alice,
            plan_ref=plan.plan_ref,
            dependency_ref=outcome_rule.dependency_ref,
        )
        assert [item.state_ref for item in history] == [
            outcome_rule.state_ref,
            retired.state_ref,
        ]
        assert history[0].current_until_at is not None
        assert history[1].current_until_at is None
        with psycopg.connect(
            host=migrated_database.cluster.host,
            port=migrated_database.cluster.port,
            dbname=migrated_database.name,
            user=migrated_database.cluster.admin_user,
            password=migrated_database.cluster.admin_password,
        ) as connection:
            assert connection.execute(
                "SELECT count(*) FROM dante.plan_dependency_operation WHERE dependency_ref=%s",
                (outcome_rule.dependency_ref,),
            ).fetchone() == (2,)
            assert connection.execute(
                "SELECT state_ref FROM dante.plan_current_work_state WHERE plan_ref=%s",
                (plan.plan_ref,),
            ).fetchone() == (reordered.state_ref,)
    finally:
        await runtime.engine.dispose()


@pytest.mark.asyncio
async def test_b13_b_reverse_claim_and_cycle_are_visible(migrated_database: Any) -> None:
    alice = _seed_self_person(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    plans = PlanWorkApplication(runtime.session_factory)
    dependencies = PlanDependencyApplication(runtime.session_factory)
    activities = TemporalActivityApplication(runtime.session_factory)
    try:
        area = ensure_test_life_area(migrated_database, alice)
        refs = []
        for number in range(2):
            activity = await activities.create_activity(
                self_person_ref=alice,
                life_area_ref=area,
                operation_id=f"b13b:cycle:activity:{number}",
                title=f"Activity {number}",
            )
            refs.append(activity.activity.activity_ref)
        steps = tuple(
            PlanStepInput(
                step_ref=new_native_ref(),
                title=f"Step {i}",
                activity_ref=ref,
            )
            for i, ref in enumerate(refs)
        )
        plan = await plans.create(
            self_person_ref=alice,
            operation_id="b13b:cycle:plan",
            title="Cycle",
        )
        plan = await plans.replace(
            self_person_ref=alice,
            plan_ref=plan.plan_ref,
            expected_state_ref=plan.state_ref,
            operation_id="b13b:cycle:steps",
            title="Cycle",
            steps=steps,
        )
        for number, (before, after) in enumerate(((steps[0], steps[1]), (steps[1], steps[0]))):
            await dependencies.write(
                self_person_ref=alice,
                plan_ref=plan.plan_ref,
                operation_id=f"b13b:cycle:{number}",
                prerequisite_step_ref=before.step_ref,
                dependent_step_ref=after.step_ref,
                qualifier_code="actual_occurred",
                disposition_code=None,
            )
        loaded = await dependencies.list(self_person_ref=alice, plan_ref=plan.plan_ref)
        assert len(loaded) == 2
        assert all(item.cycle for item in loaded)
        assert {item.evaluation_code for item in loaded} == {"unknown"}
    finally:
        await runtime.engine.dispose()
