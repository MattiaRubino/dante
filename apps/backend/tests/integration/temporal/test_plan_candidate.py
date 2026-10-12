"""B12-B candidate search is deterministic, guarded and has no canonical effect."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Any

import pytest
from tests.integration.temporal.b05_legacy_test_support import ensure_test_life_area
from tests.integration.temporal.test_b02_schedule_create import _seed_self_person

from dante.modules.temporal.activity import TemporalActivityApplication
from dante.modules.temporal.actual_runtime import ActualApplication
from dante.modules.temporal.plan_candidate import (
    PlanCandidateApplication,
    PlanCandidateNotFoundError,
)
from dante.modules.temporal.plan_conflict import PlanConflictStateError
from dante.modules.temporal.plan_dependency import PlanDependencyApplication
from dante.modules.temporal.plan_work import PlanStepInput, PlanWorkApplication
from dante.modules.temporal.schedule import AbsoluteIntervalPlacement
from dante.modules.temporal.temporal_constraint import (
    AbsoluteBoundaryRule,
    ScheduleDurationRule,
    TemporalConstraintApplication,
    evaluate_current_constraint_snapshot,
)
from dante.modules.temporal.temporal_constraint import (
    AbsoluteIntervalPlacement as ConstraintIntervalPlacement,
)
from dante.platform.database.references import new_native_ref
from dante.platform.database.runtime import create_database_runtime

pytestmark = pytest.mark.postgres


@pytest.mark.asyncio
async def test_b12_b_fixed_duration_hard_rule_dependency_and_no_effect(
    migrated_database: Any,
) -> None:
    alice = _seed_self_person(migrated_database)
    bob = _seed_self_person(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    activities = TemporalActivityApplication(runtime.session_factory)
    plans = PlanWorkApplication(runtime.session_factory)
    dependencies = PlanDependencyApplication(runtime.session_factory)
    constraints = TemporalConstraintApplication(runtime.session_factory)
    actuals = ActualApplication(runtime.session_factory)
    search = PlanCandidateApplication(runtime.session_factory)
    try:
        area = ensure_test_life_area(migrated_database, alice)
        start = datetime(2026, 10, 1, 10, tzinfo=UTC)
        before = await activities.create_activity(
            self_person_ref=alice, life_area_ref=area,
            operation_id="b12b:before", title="Record",
        )
        mix = await activities.create_activity_with_schedule(
            self_person_ref=alice, life_area_ref=area,
            operation_id="b12b:mix", title="Mix",
            placement=AbsoluteIntervalPlacement(start, start + timedelta(hours=1)),
        )
        first, second = new_native_ref(), new_native_ref()
        initial = await plans.create(
            self_person_ref=alice, operation_id="b12b:plan", title="Album",
        )
        plan = await plans.replace(
            self_person_ref=alice, plan_ref=initial.plan_ref,
            expected_state_ref=initial.state_ref, operation_id="b12b:steps", title="Album",
            steps=(
                PlanStepInput(first, "Record", before.activity.activity_ref),
                PlanStepInput(second, "Mix", mix.activity.activity_ref),
            ),
        )
        rule = await constraints.create_constraint(
            self_person_ref=alice, operation_id="b12b:earliest",
            subject_native_ref=mix.activity.activity_ref,
            rule=AbsoluteBoundaryRule(
                boundary_kind="earliest_start", constrained_facet="schedule.start",
                strength="hard", boundary_at=start + timedelta(hours=1),
            ),
        )
        args = {"self_person_ref": alice, "plan_ref": plan.plan_ref,
                "step_ref": second, "expected_state_ref": plan.state_ref}
        result = await search.search(**args)
        assert result.basis_status == "supported"
        assert result.solver_status == "OPTIMAL"
        assert result.capacity_evaluated is False
        assert result.duration_microseconds == 3_600_000_000
        assert result.grid_size == 97
        assert result.constraint_states == ((rule.constraint_ref, rule.material_state_ref),)
        assert result.placement is not None
        assert result.placement.material_state_ref == mix.schedule.material_state_ref
        assert [item.starts_at for item in result.candidates] == [
            start + timedelta(hours=1), start + timedelta(hours=1, minutes=15),
            start + timedelta(hours=1, minutes=30),
        ]
        for candidate in result.candidates:
            assert candidate.ends_at - candidate.starts_at == timedelta(hours=1)
            assessment = evaluate_current_constraint_snapshot(
                subject_native_ref=mix.activity.activity_ref,
                placement=ConstraintIntervalPlacement(candidate.starts_at, candidate.ends_at),
                constraints=await constraints.list_constraints_by_subject(
                    self_person_ref=alice, subject_native_ref=mix.activity.activity_ref,
                ),
            )
            assert assessment.hard_set_status == "feasible"
            assert assessment.status == "admissible"
        assert await search.search(**args) == result
        assert await plans.get(self_person_ref=alice, plan_ref=plan.plan_ref) == plan
        unsupported = await search.search(
            self_person_ref=alice, plan_ref=plan.plan_ref,
            step_ref=first, expected_state_ref=plan.state_ref,
        )
        assert (unsupported.basis_status, unsupported.candidates) == ("unsupported", ())

        await dependencies.write(
            self_person_ref=alice, plan_ref=plan.plan_ref,
            operation_id="b12b:dependency", prerequisite_step_ref=first,
            dependent_step_ref=second, qualifier_code="actual_occurred",
            disposition_code=None,
        )
        unknown = await search.search(**args)
        assert (unknown.basis_status, unknown.solver_status, unknown.candidates) == (
            "unknown", None, (),
        )
        previous = await actuals.record(
            self_person_ref=alice, operation_id="b12b:false",
            subject_kind="activity", subject_native_ref=before.activity.activity_ref,
            realization_occurred=False, expected_material_state_ref=None,
        )
        assert (await search.search(**args)).basis_status == "blocked"
        await actuals.record(
            self_person_ref=alice, operation_id="b12b:true",
            subject_kind="activity", subject_native_ref=before.activity.activity_ref,
            realization_occurred=True,
            expected_material_state_ref=previous.material_state_ref,
        )
        assert (await search.search(**args)).candidates == result.candidates
        await constraints.create_constraint(
            self_person_ref=alice, operation_id="b12b:minimum-duration",
            subject_native_ref=mix.activity.activity_ref,
            rule=ScheduleDurationRule(
                duration_kind="minimum", strength="hard",
                duration_microseconds=2 * 3_600_000_000,
            ),
        )
        infeasible = await search.search(**args)
        assert (infeasible.basis_status, infeasible.solver_status,
                infeasible.candidates) == ("supported", "INFEASIBLE", ())
        assert len(infeasible.constraint_states) == 2
        assert await plans.get(self_person_ref=alice, plan_ref=plan.plan_ref) == plan
        with pytest.raises(PlanCandidateNotFoundError):
            await search.search(self_person_ref=alice, plan_ref=plan.plan_ref,
                                step_ref=new_native_ref(), expected_state_ref=plan.state_ref)
        with pytest.raises(PlanConflictStateError):
            await search.search(self_person_ref=alice, plan_ref=plan.plan_ref,
                                step_ref=second, expected_state_ref=initial.state_ref)
        with pytest.raises(LookupError):
            await search.search(self_person_ref=bob, plan_ref=plan.plan_ref,
                                step_ref=second, expected_state_ref=plan.state_ref)
    finally:
        await runtime.engine.dispose()
