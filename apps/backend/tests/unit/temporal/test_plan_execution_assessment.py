"""Explicit planning basis and merge assessment never mutate actual execution."""

from dataclasses import replace
from datetime import UTC, datetime, timedelta
from types import SimpleNamespace
from uuid import uuid7

import pytest
from fastapi import Request, Response

from dante.modules.temporal import plan_work_api
from dante.modules.temporal.plan_work import PlanStepView, PlanWorkView


@pytest.mark.asyncio
async def test_explicit_slices_count_and_merge_reuse_temporal_evaluation(monkeypatch) -> None:
    plan_ref, state_ref, step_ref, activity_ref = (uuid7() for _ in range(4))
    plan = PlanWorkView(
        plan_ref=plan_ref, state_ref=state_ref, title="Album",
        created_at=datetime.now(UTC), replayed=False,
        steps=(PlanStepView(
            step_ref=step_ref, position=0, title="Record", activity_ref=activity_ref,
            divisible=False, max_planned_slices=1, merge_compatible=False,
            execution_strength_code="hard",
        ),),
    )

    class FakePlans:
        async def get(self, **_kwargs):
            return plan

    class FakeTemporal:
        status = "admissible"

        def __init__(self, _factory):
            pass

        async def evaluate_constraints(self, **_kwargs):
            return SimpleNamespace(status=self.status, hard_set_status="feasible", items=())

    monkeypatch.setattr(plan_work_api, "TemporalConstraintApplication", FakeTemporal)
    now = datetime(2026, 9, 29, 12, tzinfo=UTC)
    first_ref, second_ref = uuid7(), uuid7()
    payload = plan_work_api.AssessExecutionBody(
        expected_state_ref=state_ref,
        slices=[
            plan_work_api.ProposedSlice(slice_ref=first_ref, starts_at=now,
                                         ends_at=now + timedelta(hours=1)),
            plan_work_api.ProposedSlice(slice_ref=second_ref,
                                         starts_at=now + timedelta(hours=1),
                                         ends_at=now + timedelta(hours=2)),
        ],
        merge_pair=(first_ref, second_ref),
    )
    request = Request({"type": "http", "app": SimpleNamespace(
        state=SimpleNamespace(database_runtime=SimpleNamespace(session_factory=None))
    )})
    result = await plan_work_api.assess_plan_step_execution(
        plan_ref=plan_ref, step_ref=step_ref, payload=payload,
        context=SimpleNamespace(self_person_ref=uuid7()),
        application=FakePlans(), request=request, response=Response(),
    )
    assert result.basis == "explicit_proposed_slices"
    assert result.proposed_count == 2
    assert result.count_status == "violated_hard"
    assert result.merge_status == "incompatible"
    assert result.merge_reason == "merge_disallowed"

    plan = replace(plan, steps=(replace(
        plan.steps[0], divisible=True, max_planned_slices=2,
        merge_compatible=True, execution_strength_code="soft",
    ),))
    result = await plan_work_api.assess_plan_step_execution(
        plan_ref=plan_ref, step_ref=step_ref, payload=payload,
        context=SimpleNamespace(self_person_ref=uuid7()),
        application=FakePlans(), request=request, response=Response(),
    )
    assert result.count_status == "satisfied"
    assert result.merge_status == "compatible"
    assert result.merged_temporal_status == "admissible"

    FakeTemporal.status = "not_evaluable"
    result = await plan_work_api.assess_plan_step_execution(
        plan_ref=plan_ref, step_ref=step_ref, payload=payload,
        context=SimpleNamespace(self_person_ref=uuid7()),
        application=FakePlans(), request=request, response=Response(),
    )
    assert result.merge_status == "unknown"
    assert result.merge_reason == "temporal_rule_not_evaluable"
