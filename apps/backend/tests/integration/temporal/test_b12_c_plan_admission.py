"""B12-C reviewed direct and pending single Schedule moves use canonical B04-D truth."""

from __future__ import annotations

import asyncio
from datetime import UTC, datetime, timedelta
from typing import Any
from uuid import uuid7

import pytest
from tests.integration.temporal.b05_legacy_test_support import ensure_test_life_area
from tests.integration.temporal.test_b02_schedule_create import _seed_self_person

from dante.modules.temporal.activity import TemporalActivityApplication
from dante.modules.temporal.movement_policy import (
    MovementPolicyApplication,
    MovementPolicyRule,
)
from dante.modules.temporal.plan_admission import (
    PlanAdmissionApplication,
    PlanAdmissionReuseError,
    PlanAdmissionStaleError,
    ReviewedMove,
)
from dante.modules.temporal.plan_candidate import PlanCandidateApplication, PlanCandidateView
from dante.modules.temporal.plan_conflict import PlanConflictStateError
from dante.modules.temporal.plan_work import PlanStepInput, PlanWorkApplication
from dante.modules.temporal.schedule import AbsoluteIntervalPlacement
from dante.modules.temporal.temporal_constraint import (
    AbsoluteBoundaryRule,
    TemporalConstraintApplication,
)
from dante.platform.database.references import new_native_ref
from dante.platform.database.runtime import create_database_runtime

pytestmark = pytest.mark.postgres


def _review(view: PlanCandidateView, operation_id: str) -> ReviewedMove:
    assert view.placement is not None
    assert view.movement_policy_material_state_ref is not None
    assert view.candidates
    candidate = view.candidates[0]
    return ReviewedMove(
        plan_ref=view.plan_ref, step_ref=view.step_ref,
        plan_state_ref=view.plan_state_ref, schedule_ref=view.placement.schedule_ref,
        schedule_state_ref=view.placement.material_state_ref,
        policy_state_ref=view.movement_policy_material_state_ref,
        basis_fingerprint=view.basis_fingerprint,
        starts_at=candidate.starts_at, ends_at=candidate.ends_at,
        operation_id=operation_id,
    )


@pytest.mark.asyncio
async def test_b12_c_direct_pending_confirmation_and_stale_review(
    migrated_database: Any,
) -> None:
    alice = _seed_self_person(migrated_database)
    bob = _seed_self_person(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    activities = TemporalActivityApplication(runtime.session_factory)
    plans = PlanWorkApplication(runtime.session_factory)
    policies = MovementPolicyApplication(runtime.session_factory)
    constraints = TemporalConstraintApplication(runtime.session_factory)
    search = PlanCandidateApplication(runtime.session_factory)
    admission = PlanAdmissionApplication(runtime.session_factory)
    try:
        start = datetime(2026, 10, 2, 10, tzinfo=UTC)
        created = await activities.create_activity_with_schedule(
            self_person_ref=alice,
            life_area_ref=ensure_test_life_area(migrated_database, alice),
            operation_id="b12c:activity", title="Mix",
            placement=AbsoluteIntervalPlacement(start, start + timedelta(hours=1)),
        )
        initial = await plans.create(
            self_person_ref=alice, operation_id="b12c:plan", title="Album",
        )
        step_ref = new_native_ref()
        plan = await plans.replace(
            self_person_ref=alice, plan_ref=initial.plan_ref,
            expected_state_ref=initial.state_ref, operation_id="b12c:steps",
            title="Album",
            steps=(PlanStepInput(step_ref, "Mix", created.activity.activity_ref),),
        )
        policy = await policies.create_policy(
            self_person_ref=alice, operation_id="b12c:direct-policy",
            schedule_ref=created.schedule.schedule_ref,
            rule=MovementPolicyRule("automatic", "direct"),
        )
        args = {"self_person_ref": alice, "plan_ref": plan.plan_ref,
                "step_ref": step_ref, "expected_state_ref": plan.state_ref}
        first = await search.search(**args)
        direct_review = _review(first, str(uuid7()))
        with pytest.raises(LookupError):
            await admission.request(self_ref=bob, review=direct_review)
        first_result, second_result = await asyncio.gather(
            admission.request(self_ref=alice, review=direct_review),
            admission.request(self_ref=alice, review=direct_review),
        )
        assert {first_result.replayed, second_result.replayed} == {False, True}
        result = first_result
        assert result.kind == "committed"
        assert result.placement_state_ref is not None
        assert result.proposal_ref is None
        assert (await admission.request(self_ref=alice, review=direct_review)).replayed is True
        with pytest.raises(PlanAdmissionReuseError):
            await admission.request(
                self_ref=alice,
                review=ReviewedMove(
                    plan_ref=direct_review.plan_ref, step_ref=direct_review.step_ref,
                    plan_state_ref=direct_review.plan_state_ref,
                    schedule_ref=direct_review.schedule_ref,
                    schedule_state_ref=direct_review.schedule_state_ref,
                    policy_state_ref=direct_review.policy_state_ref,
                    basis_fingerprint=direct_review.basis_fingerprint,
                    starts_at=direct_review.starts_at + timedelta(minutes=15),
                    ends_at=direct_review.ends_at + timedelta(minutes=15),
                    operation_id=direct_review.operation_id,
                ),
            )
        moved = await search.search(**args)
        assert moved.placement is not None
        assert moved.placement.material_state_ref == result.placement_state_ref
        assert moved.placement.starts_at == direct_review.starts_at
        with pytest.raises(PlanAdmissionStaleError):
            await admission.request(self_ref=alice, review=_review(first, str(uuid7())))

        stale_constraint_review = _review(await search.search(**args), str(uuid7()))
        await constraints.create_constraint(
            self_person_ref=alice, operation_id="b12c:soft-rule",
            subject_native_ref=created.activity.activity_ref,
            rule=AbsoluteBoundaryRule(
                boundary_kind="earliest_start", constrained_facet="schedule.start",
                strength="soft", boundary_at=start,
            ),
        )
        with pytest.raises(PlanAdmissionStaleError):
            await admission.request(self_ref=alice, review=stale_constraint_review)

        await policies.revise_policy(
            self_person_ref=alice, operation_id="b12c:confirm-policy",
            schedule_ref=created.schedule.schedule_ref,
            expected_material_state_ref=policy.material_state_ref,
            rule=MovementPolicyRule("automatic", "confirmation_required"),
        )
        pending_review = _review(await search.search(**args), str(uuid7()))
        pending = await admission.request(self_ref=alice, review=pending_review)
        assert pending.kind == "pending_confirmation"
        assert pending.proposal_ref is not None
        assert pending.placement_state_ref is None
        assert (await search.search(**args)).placement == moved.placement
        assert (await admission.request(self_ref=alice, review=pending_review)).replayed is True
        accepted = await admission.accept(
            self_ref=alice, review=pending_review, proposal_ref=pending.proposal_ref,
        )
        assert accepted.kind == "committed"
        assert accepted.placement_state_ref != moved.placement.material_state_ref
        assert (await admission.accept(
            self_ref=alice, review=pending_review, proposal_ref=pending.proposal_ref,
        )).replayed is True
        assert (await search.search(**args)).placement.material_state_ref == accepted.placement_state_ref

        stale_policy_review = _review(await search.search(**args), str(uuid7()))
        stale_policy_proposal = await admission.request(self_ref=alice, review=stale_policy_review)
        assert stale_policy_proposal.proposal_ref is not None
        await policies.revise_policy(
            self_person_ref=alice, operation_id="b12c:blocked-policy",
            schedule_ref=created.schedule.schedule_ref,
            expected_material_state_ref=(await policies.get_policy(
                self_person_ref=alice, schedule_ref=created.schedule.schedule_ref,
            )).material_state_ref,
            rule=MovementPolicyRule("blocked", "direct"),
        )
        with pytest.raises(PlanAdmissionStaleError):
            await admission.accept(
                self_ref=alice, review=stale_policy_review,
                proposal_ref=stale_policy_proposal.proposal_ref,
            )
        assert (await search.search(**args)).placement.material_state_ref == accepted.placement_state_ref

        await plans.replace(
            self_person_ref=alice, plan_ref=plan.plan_ref,
            expected_state_ref=plan.state_ref, operation_id="b12c:revised-plan",
            title="Album revisited",
            steps=(PlanStepInput(step_ref, "Mix", created.activity.activity_ref),),
        )
        with pytest.raises(PlanConflictStateError):
            await admission.request(self_ref=alice, review=_review(first, str(uuid7())))
    finally:
        await runtime.engine.dispose()
