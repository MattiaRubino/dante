"""B12-A diagnoses current Plan truth without changing canonical state."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Any

import pytest
from tests.integration.temporal.b05_legacy_test_support import ensure_test_life_area
from tests.integration.temporal.test_b02_schedule_create import _seed_self_person

from dante.modules.temporal.activity import TemporalActivityApplication
from dante.modules.temporal.actual_runtime import ActualApplication
from dante.modules.temporal.plan_conflict import (
    PlanConflictApplication,
    PlanConflictNotFoundError,
    PlanConflictStateError,
)
from dante.modules.temporal.plan_dependency import PlanDependencyApplication
from dante.modules.temporal.plan_work import PlanStepInput, PlanWorkApplication
from dante.modules.temporal.schedule import AbsoluteIntervalPlacement
from dante.modules.temporal.temporal_constraint import (
    ScheduleDurationRule,
    TemporalConstraintApplication,
)
from dante.platform.database.references import new_native_ref
from dante.platform.database.runtime import create_database_runtime

pytestmark = pytest.mark.postgres


@pytest.mark.asyncio
async def test_b12_a_read_only_current_violation_and_prerequisite(
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
    diagnosis = PlanConflictApplication(runtime.session_factory)
    try:
        area = ensure_test_life_area(migrated_database, alice)
        record = await activities.create_activity(
            self_person_ref=alice, life_area_ref=area,
            operation_id="b12a:record", title="Record",
        )
        start = datetime(2026, 10, 1, 10, tzinfo=UTC)
        mix = await activities.create_activity_with_schedule(
            self_person_ref=alice, life_area_ref=area,
            operation_id="b12a:mix", title="Mix",
            placement=AbsoluteIntervalPlacement(start, start + timedelta(hours=2)),
        )
        first, second = new_native_ref(), new_native_ref()
        initial = await plans.create(
            self_person_ref=alice, operation_id="b12a:plan", title="Album",
        )
        plan = await plans.replace(
            self_person_ref=alice, plan_ref=initial.plan_ref,
            expected_state_ref=initial.state_ref, operation_id="b12a:steps", title="Album",
            steps=(
                PlanStepInput(first, "Record", record.activity.activity_ref),
                PlanStepInput(second, "Mix", mix.activity.activity_ref),
            ),
        )
        await dependencies.write(
            self_person_ref=alice, plan_ref=plan.plan_ref,
            operation_id="b12a:dependency", prerequisite_step_ref=first,
            dependent_step_ref=second, qualifier_code="actual_occurred",
            disposition_code=None,
        )
        await constraints.create_constraint(
            self_person_ref=alice, operation_id="b12a:maximum",
            subject_native_ref=mix.activity.activity_ref,
            rule=ScheduleDurationRule(
                duration_kind="maximum", strength="hard",
                duration_microseconds=90 * 60 * 1_000_000,
            ),
        )

        first_view = await diagnosis.inspect(
            self_person_ref=alice, plan_ref=plan.plan_ref,
            expected_state_ref=plan.state_ref,
        )
        assert first_view.capacity_evaluated is False
        assert first_view.steps[0].diagnostics == ("unknown_basis",)
        assert first_view.steps[1].diagnostics == (
            "known_hard_violation", "unknown_basis",
        )
        assert first_view.steps[1].dependencies[0].evaluation_code == "unknown"
        assert first_view.steps[1].constraints[0].evaluation == "violated"
        placement = first_view.steps[1].placements[0]
        assert (placement.starts_at, placement.ends_at) == (
            start, start + timedelta(hours=2),
        )

        current = await actuals.record(
            self_person_ref=alice, operation_id="b12a:actual-false",
            subject_kind="activity", subject_native_ref=record.activity.activity_ref,
            realization_occurred=False, expected_material_state_ref=None,
        )
        blocked = await diagnosis.inspect(
            self_person_ref=alice, plan_ref=plan.plan_ref,
            expected_state_ref=plan.state_ref,
        )
        assert blocked.steps[1].diagnostics == (
            "known_hard_violation", "blocked_prerequisite",
        )
        assert blocked.steps[1].dependencies[0].evaluation_code == "unsatisfied"

        await actuals.record(
            self_person_ref=alice, operation_id="b12a:actual-true",
            subject_kind="activity", subject_native_ref=record.activity.activity_ref,
            realization_occurred=True,
            expected_material_state_ref=current.material_state_ref,
        )
        satisfied = await diagnosis.inspect(
            self_person_ref=alice, plan_ref=plan.plan_ref,
            expected_state_ref=plan.state_ref,
        )
        assert satisfied.steps[1].diagnostics == ("known_hard_violation",)
        assert satisfied.steps[1].dependencies[0].evaluation_code == "satisfied"
        assert satisfied.steps[1].placements == first_view.steps[1].placements
        assert await plans.get(self_person_ref=alice, plan_ref=plan.plan_ref) == plan

        with pytest.raises(PlanConflictNotFoundError):
            await diagnosis.inspect(
                self_person_ref=bob, plan_ref=plan.plan_ref,
                expected_state_ref=plan.state_ref,
            )
        with pytest.raises(PlanConflictStateError):
            await diagnosis.inspect(
                self_person_ref=alice, plan_ref=plan.plan_ref,
                expected_state_ref=initial.state_ref,
            )
    finally:
        await runtime.engine.dispose()
