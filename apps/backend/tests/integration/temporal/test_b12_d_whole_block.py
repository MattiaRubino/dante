"""B12-D: accepted Plan truth flows through diagnosis, candidate, review and Timeline."""

from __future__ import annotations

from datetime import UTC, date, datetime, timedelta
from typing import Any
from uuid import uuid7

import pytest
from tests.integration.temporal.b05_legacy_test_support import ensure_test_life_area
from tests.integration.temporal.test_b02_schedule_create import _context, _seed_self_person
from tests.integration.temporal.test_b12_c_plan_admission import _review

from dante.modules.temporal.activity import TemporalActivityApplication
from dante.modules.temporal.actual_runtime import ActualApplication
from dante.modules.temporal.application import (
    TemporalTimelineApplication,
    TimelineAbsoluteActivityItem,
)
from dante.modules.temporal.contracts import TimelineWindowQuery
from dante.modules.temporal.movement_policy import MovementPolicyApplication, MovementPolicyRule
from dante.modules.temporal.plan_admission import PlanAdmissionApplication, PlanAdmissionStaleError
from dante.modules.temporal.plan_candidate import PlanCandidateApplication
from dante.modules.temporal.plan_conflict import PlanConflictApplication
from dante.modules.temporal.plan_dependency import PlanDependencyApplication
from dante.modules.temporal.plan_work import PlanStepInput, PlanWorkApplication
from dante.modules.temporal.schedule import AbsoluteIntervalPlacement
from dante.modules.temporal.temporal_constraint import (
    AbsoluteBoundaryRule,
    TemporalConstraintApplication,
)
from dante.platform.database.references import new_native_ref
from dante.platform.database.runtime import create_database_runtime

pytestmark = pytest.mark.postgres


@pytest.mark.asyncio
async def test_b12_d_conflict_to_reviewed_proposal_to_accepted_timeline(
    migrated_database: Any,
) -> None:
    alice = _seed_self_person(migrated_database)
    bob = _seed_self_person(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    activities = TemporalActivityApplication(runtime.session_factory)
    plans = PlanWorkApplication(runtime.session_factory)
    dependencies = PlanDependencyApplication(runtime.session_factory)
    actuals = ActualApplication(runtime.session_factory)
    constraints = TemporalConstraintApplication(runtime.session_factory)
    policies = MovementPolicyApplication(runtime.session_factory)
    diagnosis = PlanConflictApplication(runtime.session_factory)
    candidates = PlanCandidateApplication(runtime.session_factory)
    admission = PlanAdmissionApplication(runtime.session_factory)
    timeline = TemporalTimelineApplication(runtime.session_factory)
    try:
        start = datetime(2026, 10, 2, 10, tzinfo=UTC)
        area = ensure_test_life_area(migrated_database, alice)
        record = await activities.create_activity(
            self_person_ref=alice,
            life_area_ref=area,
            operation_id="b12d:record",
            title="Record",
        )
        mix = await activities.create_activity_with_schedule(
            self_person_ref=alice,
            life_area_ref=area,
            operation_id="b12d:mix",
            title="Mix",
            placement=AbsoluteIntervalPlacement(start, start + timedelta(hours=1)),
        )
        record_step, mix_step = new_native_ref(), new_native_ref()
        initial = await plans.create(
            self_person_ref=alice,
            operation_id="b12d:plan",
            title="Album",
        )
        plan = await plans.replace(
            self_person_ref=alice,
            plan_ref=initial.plan_ref,
            expected_state_ref=initial.state_ref,
            operation_id="b12d:steps",
            title="Album",
            steps=(
                PlanStepInput(record_step, "Record", record.activity.activity_ref),
                PlanStepInput(mix_step, "Mix", mix.activity.activity_ref),
            ),
        )
        relation = await dependencies.write(
            self_person_ref=alice,
            plan_ref=plan.plan_ref,
            operation_id="b12d:dependency",
            prerequisite_step_ref=record_step,
            dependent_step_ref=mix_step,
            qualifier_code="actual_occurred",
            disposition_code=None,
        )
        assert relation.evaluation_code == "unknown"
        await constraints.create_constraint(
            self_person_ref=alice,
            operation_id="b12d:hard-earliest",
            subject_native_ref=mix.activity.activity_ref,
            rule=AbsoluteBoundaryRule(
                boundary_kind="earliest_start",
                constrained_facet="schedule.start",
                strength="hard",
                boundary_at=start + timedelta(hours=1),
            ),
        )
        await policies.create_policy(
            self_person_ref=alice,
            operation_id="b12d:policy",
            schedule_ref=mix.schedule.schedule_ref,
            rule=MovementPolicyRule("automatic", "confirmation_required"),
        )
        args = {
            "self_person_ref": alice,
            "plan_ref": plan.plan_ref,
            "step_ref": mix_step,
            "expected_state_ref": plan.state_ref,
        }
        before = await diagnosis.inspect(
            self_person_ref=alice,
            plan_ref=plan.plan_ref,
            expected_state_ref=plan.state_ref,
        )
        assert "known_hard_violation" in before.steps[1].diagnostics
        assert "unknown_basis" in before.steps[1].diagnostics
        assert (await candidates.search(**args)).basis_status == "unknown"
        with pytest.raises(LookupError):
            await candidates.search(**{**args, "self_person_ref": bob})

        occurred = await actuals.record(
            self_person_ref=alice,
            operation_id="b12d:occurred",
            subject_kind="activity",
            subject_native_ref=record.activity.activity_ref,
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
        eligible = await candidates.search(**args)
        assert (eligible.basis_status, eligible.solver_status) == ("supported", "OPTIMAL")
        assert eligible.candidates[0].starts_at >= start + timedelta(hours=1)
        reviewed = _review(eligible, str(uuid7()))
        pending = await admission.request(self_ref=alice, review=reviewed)
        assert pending.kind == "pending_confirmation"
        assert pending.proposal_ref is not None
        assert pending.placement_state_ref is None
        assert (await admission.request(self_ref=alice, review=reviewed)).replayed

        window = TimelineWindowQuery(date(2026, 10, 2), date(2026, 10, 3))
        current = await timeline.read_window(query=window, context=_context(alice))
        assert len(current.items) == 1
        item = current.items[0]
        assert isinstance(item, TimelineAbsoluteActivityItem)
        assert (item.activity_ref, item.placement_material_state_ref, item.starts_at) == (
            mix.activity.activity_ref,
            mix.schedule.material_state_ref,
            start,
        )

        not_occurred = await actuals.record(
            self_person_ref=alice,
            operation_id="b12d:correct-not-occurred",
            subject_kind="activity",
            subject_native_ref=record.activity.activity_ref,
            realization_occurred=False,
            expected_material_state_ref=occurred.material_state_ref,
        )
        with pytest.raises(PlanAdmissionStaleError):
            await admission.accept(
                self_ref=alice,
                review=reviewed,
                proposal_ref=pending.proposal_ref,
            )
        assert (await candidates.search(**args)).placement.material_state_ref == (
            mix.schedule.material_state_ref
        )
        await actuals.record(
            self_person_ref=alice,
            operation_id="b12d:correct-occurred",
            subject_kind="activity",
            subject_native_ref=record.activity.activity_ref,
            realization_occurred=True,
            expected_material_state_ref=not_occurred.material_state_ref,
        )
        fresh = _review(await candidates.search(**args), str(uuid7()))
        next_pending = await admission.request(self_ref=alice, review=fresh)
        assert next_pending.proposal_ref is not None
        accepted = await admission.accept(
            self_ref=alice,
            review=fresh,
            proposal_ref=next_pending.proposal_ref,
        )
        assert accepted.kind == "committed"
        assert accepted.placement_state_ref != mix.schedule.material_state_ref
        assert (
            await admission.accept(
                self_ref=alice,
                review=fresh,
                proposal_ref=next_pending.proposal_ref,
            )
        ).replayed

        reloaded = await PlanWorkApplication(runtime.session_factory).get(
            self_person_ref=alice,
            plan_ref=plan.plan_ref,
        )
        assert reloaded is not None
        assert [step.activity_ref for step in reloaded.steps] == [
            record.activity.activity_ref,
            mix.activity.activity_ref,
        ]
        reread = await PlanDependencyApplication(runtime.session_factory).get(
            self_person_ref=alice,
            plan_ref=plan.plan_ref,
            dependency_ref=relation.dependency_ref,
        )
        assert reread is not None
        assert (
            reread.prerequisite_step_ref,
            reread.dependent_step_ref,
            reread.evaluation_code,
        ) == (record_step, mix_step, "satisfied")
        after = await TemporalTimelineApplication(runtime.session_factory).read_window(
            query=window,
            context=_context(alice),
        )
        moved = [entry for entry in after.items if isinstance(entry, TimelineAbsoluteActivityItem)]
        assert len(moved) == 1
        assert (
            moved[0].schedule_ref,
            moved[0].placement_material_state_ref,
            moved[0].starts_at,
        ) == (
            mix.schedule.schedule_ref,
            accepted.placement_state_ref,
            fresh.starts_at,
        )
        assert (await candidates.search(**args)).placement.material_state_ref == (
            accepted.placement_state_ref
        )
    finally:
        await runtime.engine.dispose()
