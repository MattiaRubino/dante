"""B13-D: one Plan retains distinct structure, dependency and execution truth."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from types import SimpleNamespace
from typing import Any

import pytest
from fastapi import Request, Response
from tests.integration.temporal.b05_legacy_test_support import ensure_test_life_area
from tests.integration.temporal.test_b02_schedule_create import _seed_self_person

from dante.modules.temporal.activity import TemporalActivityApplication
from dante.modules.temporal.actual_runtime import ActualApplication
from dante.modules.temporal.plan_dependency import PlanDependencyApplication
from dante.modules.temporal.plan_work import (
    PlanStepInput,
    PlanWorkApplication,
    PlanWorkConflictError,
    PlanWorkInputError,
)
from dante.modules.temporal.plan_work_api import (
    AssessExecutionBody,
    ProposedSlice,
    assess_plan_step_execution,
)
from dante.modules.temporal.temporal_constraint import (
    ScheduleDurationRule,
    TemporalConstraintApplication,
)
from dante.platform.database.references import new_native_ref
from dante.platform.database.runtime import create_database_runtime
from dante.platform.http.problem import ProblemError

pytestmark = pytest.mark.postgres


@pytest.mark.asyncio
async def test_b13_d_one_plan_integrates_structure_dependency_and_execution(
    migrated_database: Any,
) -> None:
    alice = _seed_self_person(migrated_database)
    bob = _seed_self_person(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    plans = PlanWorkApplication(runtime.session_factory)
    dependencies = PlanDependencyApplication(runtime.session_factory)
    activities = TemporalActivityApplication(runtime.session_factory)
    actuals = ActualApplication(runtime.session_factory)
    constraints = TemporalConstraintApplication(runtime.session_factory)
    try:
        area = ensure_test_life_area(migrated_database, alice)
        activity_refs = []
        for name in ("Record", "Mix"):
            view = await activities.create_activity(
                self_person_ref=alice,
                life_area_ref=area,
                operation_id=f"b13d:activity:{name}",
                title=name,
            )
            activity_refs.append(view.activity.activity_ref)
        record_ref, mix_ref = new_native_ref(), new_native_ref()
        record = PlanStepInput(
            step_ref=record_ref,
            title="Record",
            activity_ref=activity_refs[0],
        )
        mix = PlanStepInput(
            step_ref=mix_ref,
            title="Mix",
            activity_ref=activity_refs[1],
            divisible=True,
            max_planned_slices=2,
            merge_compatible=True,
            execution_strength_code="hard",
        )
        initial = await plans.create(
            self_person_ref=alice,
            operation_id="b13d:plan",
            title="Album",
        )
        plan = await plans.replace(
            self_person_ref=alice,
            plan_ref=initial.plan_ref,
            expected_state_ref=initial.state_ref,
            operation_id="b13d:steps",
            title="Album",
            steps=(record, mix),
        )
        assert plan.steps[1].step_ref == mix_ref
        assert plan.steps[1].max_planned_slices == 2
        relation = await dependencies.write(
            self_person_ref=alice,
            plan_ref=plan.plan_ref,
            operation_id="b13d:dependency",
            prerequisite_step_ref=record_ref,
            dependent_step_ref=mix_ref,
            qualifier_code="actual_occurred",
            disposition_code=None,
        )
        assert relation.evaluation_code == "unknown"
        assert await plans.get(self_person_ref=bob, plan_ref=plan.plan_ref) is None
        assert await dependencies.list(self_person_ref=bob, plan_ref=plan.plan_ref) == ()

        reordered = await plans.replace(
            self_person_ref=alice,
            plan_ref=plan.plan_ref,
            expected_state_ref=plan.state_ref,
            operation_id="b13d:reorder",
            title="Album",
            steps=(mix, record),
        )
        assert [step.step_ref for step in reordered.steps] == [mix_ref, record_ref]
        assert reordered.steps[0].max_planned_slices == 2
        with pytest.raises(PlanWorkConflictError):
            await plans.replace(
                self_person_ref=alice,
                plan_ref=plan.plan_ref,
                expected_state_ref=plan.state_ref,
                operation_id="b13d:stale",
                title="Album",
                steps=(record, mix),
            )
        with pytest.raises(PlanWorkInputError, match="Active Plan Dependency endpoint"):
            await plans.replace(
                self_person_ref=alice,
                plan_ref=plan.plan_ref,
                expected_state_ref=reordered.state_ref,
                operation_id="b13d:remove-active",
                title="Album",
                steps=(mix,),
            )
        linked = await dependencies.get(
            self_person_ref=alice,
            plan_ref=plan.plan_ref,
            dependency_ref=relation.dependency_ref,
        )
        assert linked is not None
        assert (linked.prerequisite_activity_ref, linked.dependent_activity_ref) == tuple(
            activity_refs
        )

        await constraints.create_constraint(
            self_person_ref=alice,
            operation_id="b13d:duration",
            subject_native_ref=activity_refs[1],
            rule=ScheduleDurationRule(
                duration_kind="maximum",
                strength="hard",
                duration_microseconds=90 * 60 * 1_000_000,
            ),
        )

        start = datetime(2026, 10, 1, 10, tzinfo=UTC)
        slices = tuple(
            ProposedSlice(
                slice_ref=new_native_ref(),
                starts_at=start + timedelta(hours=offset),
                ends_at=start + timedelta(hours=offset + 1),
            )
            for offset in range(3)
        )
        request = Request(
            {
                "type": "http",
                "app": SimpleNamespace(
                    state=SimpleNamespace(database_runtime=runtime),
                ),
            }
        )
        context = SimpleNamespace(self_person_ref=alice)
        assessment = await assess_plan_step_execution(
            plan_ref=plan.plan_ref,
            step_ref=mix_ref,
            payload=AssessExecutionBody(
                expected_state_ref=reordered.state_ref,
                slices=list(slices),
                merge_pair=(slices[0].slice_ref, slices[1].slice_ref),
            ),
            context=context,
            application=plans,
            request=request,
            response=Response(),
        )
        assert (assessment.basis, assessment.count_status, assessment.merge_status) == (
            "explicit_proposed_slices",
            "violated_hard",
            "incompatible",
        )
        assert assessment.merged_temporal_status == "inadmissible"
        assert assessment.merged_temporal_rules[0].evaluation == "violated"
        assert all(item.temporal_status == "admissible" for item in assessment.slice_assessments)
        assert (await plans.get(self_person_ref=alice, plan_ref=plan.plan_ref)) == reordered
        assert (
            await dependencies.get(
                self_person_ref=alice,
                plan_ref=plan.plan_ref,
                dependency_ref=relation.dependency_ref,
            )
        ).evaluation_code == "unknown"
        with pytest.raises(ProblemError) as stale:
            await assess_plan_step_execution(
                plan_ref=plan.plan_ref,
                step_ref=mix_ref,
                payload=AssessExecutionBody(expected_state_ref=plan.state_ref, slices=[]),
                context=context,
                application=plans,
                request=request,
                response=Response(),
            )
        assert stale.value.status == 409

        actual = await actuals.record(
            self_person_ref=alice,
            operation_id="b13d:actual",
            subject_kind="activity",
            subject_native_ref=activity_refs[0],
            realization_occurred=True,
            expected_material_state_ref=None,
        )
        assert (
            await dependencies.get(
                self_person_ref=alice,
                plan_ref=plan.plan_ref,
                dependency_ref=relation.dependency_ref,
            )
        ).evaluation_code == "satisfied"
        await actuals.record(
            self_person_ref=alice,
            operation_id="b13d:actual-correction",
            subject_kind="activity",
            subject_native_ref=activity_refs[0],
            realization_occurred=False,
            expected_material_state_ref=actual.material_state_ref,
        )
        assert (
            await dependencies.get(
                self_person_ref=alice,
                plan_ref=plan.plan_ref,
                dependency_ref=relation.dependency_ref,
            )
        ).evaluation_code == "unsatisfied"
        assert (
            await PlanWorkApplication(runtime.session_factory).get(
                self_person_ref=alice,
                plan_ref=plan.plan_ref,
            )
        ).steps[0].max_planned_slices == 2

        retired_policy = await plans.replace(
            self_person_ref=alice,
            plan_ref=plan.plan_ref,
            expected_state_ref=reordered.state_ref,
            operation_id="b13d:retire-policy",
            title="Album",
            steps=(
                PlanStepInput(
                    step_ref=mix_ref,
                    title="Mix",
                    activity_ref=activity_refs[1],
                ),
                record,
            ),
        )
        assert retired_policy.steps[0].divisible is None
        retired_relation = await dependencies.write(
            self_person_ref=alice,
            plan_ref=plan.plan_ref,
            dependency_ref=relation.dependency_ref,
            expected_state_ref=relation.state_ref,
            operation_id="b13d:retire-dependency",
            prerequisite_step_ref=record_ref,
            dependent_step_ref=mix_ref,
            qualifier_code="actual_occurred",
            disposition_code=None,
            active=False,
        )
        assert not retired_relation.active
        assert [
            item.state_ref
            for item in await dependencies.history(
                self_person_ref=alice,
                plan_ref=plan.plan_ref,
                dependency_ref=relation.dependency_ref,
            )
        ] == [relation.state_ref, retired_relation.state_ref]
    finally:
        await runtime.dispose()
