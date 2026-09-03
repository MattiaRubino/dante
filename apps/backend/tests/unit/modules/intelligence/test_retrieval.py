"""Unit acceptance for Retrieval planning/candidate/validation contracts."""

from datetime import UTC, datetime
from uuid import uuid7

import pytest
from tests.unit.modules.intelligence.fakes import ScriptedRetrievalGateway

from dante.modules.intelligence.contracts.context import (
    ContextFragment,
    InformationGuarantee,
    InstructionProvenance,
    RealityScope,
    RealityScopeKind,
    ReferenceBindingState,
    SourceCurrentness,
    SourceRealityClass,
    TextContextRepresentation,
)
from dante.modules.intelligence.contracts.references import (
    NativeRefBinding,
    ReferenceBindingRequirement,
)
from dante.modules.intelligence.contracts.retrieval import (
    CandidateValidationResult,
    CandidateValidationStatus,
    RetrievalBatch,
    RetrievalCandidate,
    RetrievalMechanism,
    RetrievalPlan,
    SourceLifecycleHint,
)


def _scope() -> RealityScope:
    return RealityScope(kind=RealityScopeKind.CANONICAL_CURRENT)


def _plan() -> RetrievalPlan:
    return RetrievalPlan(
        plan_id=uuid7(),
        work_id=uuid7(),
        work_revision=1,
        context_plan_id=uuid7(),
        context_plan_revision=1,
        information_need_ids=(uuid7(),),
        strategy_ids=(uuid7(),),
        purpose="ask_dante",
        reality_scope=_scope(),
        reference_requirement=ReferenceBindingRequirement.UNIQUE_IN_SCOPE,
        eligible_source_classes=("notes",),
        excluded_source_classes=("retired",),
        required_guarantee=InformationGuarantee.APPROXIMATE,
        freshness_requirement="reread_before_basis",
        coherence_requirement="source_local",
        fidelity_requirement="source_text",
        permitted_transformations=("query_rewrite",),
        max_candidates=20,
        max_refinements=2,
        budget_units=100,
    )


def _candidate(plan: RetrievalPlan) -> RetrievalCandidate:
    return RetrievalCandidate(
        candidate_id=uuid7(),
        plan_id=plan.plan_id,
        information_need_id=plan.information_need_ids[0],
        source_binding=NativeRefBinding(native_ref=uuid7()),
        source_class="notes",
        mechanism=RetrievalMechanism.SEMANTIC,
        retrieved_at=datetime.now(UTC),
        reality_scope=plan.reality_scope,
        currentness_hint=SourceCurrentness.UNKNOWN,
        source_lifecycle_hint=SourceLifecycleHint.ACTIVE,
        purpose_scope=plan.purpose,
        lineage_refs=("embedding:generation:test",),
        cost_units=1,
        rank=1,
        score=0.9,
    )


def _fragment(candidate: RetrievalCandidate) -> ContextFragment:
    return ContextFragment(
        fragment_id=uuid7(),
        need_ids=(candidate.information_need_id,),
        source_binding=candidate.source_binding,
        source_class=SourceRealityClass.CANONICAL_CURRENT,
        reality_scope=candidate.reality_scope,
        reference_binding=ReferenceBindingState.EXACT,
        source_standing="validated_source",
        sensitivity="private",
        instruction_provenance=InstructionProvenance.DATA,
        retrieved_at=datetime.now(UTC),
        currentness=SourceCurrentness.CURRENT,
        representation=TextContextRepresentation(text="validated source text"),
        transformation_lineage=candidate.lineage_refs,
    )


def test_retrieval_plan_rejects_source_class_in_both_eligible_and_excluded_sets() -> None:
    plan = _plan()
    with pytest.raises(ValueError, match="both eligible and excluded"):
        RetrievalPlan(
            plan_id=plan.plan_id,
            work_id=plan.work_id,
            work_revision=plan.work_revision,
            context_plan_id=plan.context_plan_id,
            context_plan_revision=plan.context_plan_revision,
            information_need_ids=plan.information_need_ids,
            strategy_ids=plan.strategy_ids,
            purpose=plan.purpose,
            reality_scope=plan.reality_scope,
            reference_requirement=plan.reference_requirement,
            eligible_source_classes=("notes",),
            excluded_source_classes=("notes",),
            required_guarantee=plan.required_guarantee,
            freshness_requirement=plan.freshness_requirement,
            coherence_requirement=plan.coherence_requirement,
            fidelity_requirement=plan.fidelity_requirement,
            permitted_transformations=plan.permitted_transformations,
            max_candidates=plan.max_candidates,
            max_refinements=plan.max_refinements,
            budget_units=plan.budget_units,
        )


def test_candidate_count_does_not_upgrade_approximate_guarantee() -> None:
    plan = _plan()
    candidates = (_candidate(plan), _candidate(plan))
    batch = RetrievalBatch(
        plan_id=plan.plan_id,
        candidates=candidates,
        achieved_guarantee=InformationGuarantee.APPROXIMATE,
        exhausted=True,
    )

    assert len(batch.candidates) == 2
    assert batch.achieved_guarantee is InformationGuarantee.APPROXIMATE


def test_only_eligible_validation_status_can_promote_context_fragment() -> None:
    plan = _plan()
    candidate = _candidate(plan)
    fragment = _fragment(candidate)

    accepted = CandidateValidationResult(
        candidate_id=candidate.candidate_id,
        status=CandidateValidationStatus.ELIGIBLE_CURRENT,
        fragment=fragment,
    )
    assert accepted.fragment == fragment

    with pytest.raises(ValueError, match="must not carry ContextFragment"):
        CandidateValidationResult(
            candidate_id=candidate.candidate_id,
            status=CandidateValidationStatus.STALE,
            fragment=fragment,
        )


@pytest.mark.asyncio
async def test_scripted_retrieval_fake_has_no_hidden_io_or_guarantee_upgrade() -> None:
    plan = _plan()
    candidate = _candidate(plan)
    batch = RetrievalBatch(
        plan_id=plan.plan_id,
        candidates=(candidate,),
        achieved_guarantee=InformationGuarantee.APPROXIMATE,
        exhausted=False,
        limitations=("candidate discovery remains approximate",),
    )
    validation = CandidateValidationResult(
        candidate_id=candidate.candidate_id,
        status=CandidateValidationStatus.ELIGIBLE_CURRENT,
        fragment=_fragment(candidate),
    )
    gateway = ScriptedRetrievalGateway(
        batches={plan.plan_id: batch},
        validations={candidate.candidate_id: validation},
    )

    retrieved = await gateway.retrieve(plan)
    validated = await gateway.validate(candidate)

    assert retrieved == batch
    assert validated == validation
    assert gateway.retrieve_requests == [plan]
    assert gateway.validation_requests == [candidate]
