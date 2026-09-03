"""Unit acceptance for AI-03A request-local Context contracts."""

from datetime import UTC, datetime
from uuid import uuid7

import pytest

from dante.modules.intelligence.contracts.context import (
    AggregateContextRepresentation,
    ContextFragment,
    ContextManifest,
    ContextPlan,
    ContextReadiness,
    ContextReadinessState,
    ContextResourceConstraints,
    ExposureState,
    InformationNeedStatus,
    InstructionProvenance,
    NeedReadiness,
    RealityScope,
    RealityScopeKind,
    ReferenceBindingState,
    SourceCurrentness,
    SourceRealityClass,
    TextContextRepresentation,
)
from dante.modules.intelligence.contracts.references import NativeRefBinding


def _current_scope() -> RealityScope:
    return RealityScope(kind=RealityScopeKind.CANONICAL_CURRENT)


def _source() -> NativeRefBinding:
    return NativeRefBinding(native_ref=uuid7())


def test_reality_scope_keeps_current_history_and_scenario_distinct() -> None:
    with pytest.raises(ValueError, match="requires only an as_of"):
        RealityScope(kind=RealityScopeKind.MATERIAL_HISTORICAL)

    historical = RealityScope(
        kind=RealityScopeKind.MATERIAL_HISTORICAL,
        as_of=datetime.now(UTC),
    )
    assert historical.as_of is not None

    with pytest.raises(ValueError, match="requires scenario_ref"):
        RealityScope(kind=RealityScopeKind.SCENARIO)


def test_context_plan_protected_and_unresolved_needs_must_belong_to_plan() -> None:
    need_id = uuid7()
    unknown_need = uuid7()
    constraints = ContextResourceConstraints(
        max_fragments=20,
        max_bytes=100_000,
        max_estimated_tokens=12_000,
        max_refinements=2,
    )

    with pytest.raises(ValueError, match="protected needs must belong"):
        ContextPlan(
            plan_id=uuid7(),
            revision=1,
            work_id=uuid7(),
            work_revision=1,
            objective="answer",
            purpose="ask_dante",
            principal_binding="principal:self",
            reality_scope=_current_scope(),
            privacy_compartment="self:private",
            resource_constraints=constraints,
            information_need_ids=(need_id,),
            protected_need_ids=(unknown_need,),
        )

    with pytest.raises(ValueError, match="unresolved reference needs must belong"):
        ContextPlan(
            plan_id=uuid7(),
            revision=1,
            work_id=uuid7(),
            work_revision=1,
            objective="answer",
            purpose="ask_dante",
            principal_binding="principal:self",
            reality_scope=_current_scope(),
            privacy_compartment="self:private",
            resource_constraints=constraints,
            information_need_ids=(need_id,),
            unresolved_reference_need_ids=(unknown_need,),
        )


def test_source_content_is_not_current_user_instruction() -> None:
    assert InstructionProvenance.SOURCE_CONTENT is not InstructionProvenance.CURRENT_USER_INSTRUCTION
    assert InstructionProvenance.DATA is not InstructionProvenance.TRUSTED_SYSTEM_INSTRUCTION


def test_context_fragment_is_source_linked_and_timezone_aware() -> None:
    need_id = uuid7()
    fragment = ContextFragment(
        fragment_id=uuid7(),
        need_ids=(need_id,),
        source_binding=_source(),
        source_class=SourceRealityClass.CANONICAL_CURRENT,
        reality_scope=_current_scope(),
        reference_binding=ReferenceBindingState.EXACT,
        source_standing="canonical_owner_projection",
        sensitivity="private",
        instruction_provenance=InstructionProvenance.DATA,
        retrieved_at=datetime.now(UTC),
        currentness=SourceCurrentness.CURRENT,
        representation=AggregateContextRepresentation(
            metric="distance",
            value=12.5,
            unit="km",
        ),
    )
    assert fragment.need_ids == (need_id,)

    with pytest.raises(ValueError, match="timezone-aware"):
        ContextFragment(
            fragment_id=uuid7(),
            need_ids=(need_id,),
            source_binding=_source(),
            source_class=SourceRealityClass.OPEN_WORLD,
            reality_scope=RealityScope(kind=RealityScopeKind.OPEN_WORLD_ASSERTION),
            reference_binding=ReferenceBindingState.UNRESOLVED,
            source_standing="open_world_source",
            sensitivity="public",
            instruction_provenance=InstructionProvenance.SOURCE_CONTENT,
            retrieved_at=datetime.fromisoformat("2026-09-03T12:00:00"),
            currentness=SourceCurrentness.UNKNOWN,
            representation=TextContextRepresentation(text="source material"),
        )


def test_partial_context_readiness_requires_declared_limitation() -> None:
    need_id = uuid7()
    with pytest.raises(ValueError, match="requires declared limitations"):
        ContextReadiness(
            readiness_id=uuid7(),
            plan_id=uuid7(),
            plan_revision=1,
            state=ContextReadinessState.PARTIAL_WITH_DECLARED_LIMITATION,
            need_states=(
                NeedReadiness(
                    need_id=need_id,
                    status=InformationNeedStatus.PARTIAL,
                ),
            ),
            evaluated_at=datetime.now(UTC),
        )


def test_context_manifest_does_not_confuse_not_sent_with_exposure() -> None:
    with pytest.raises(ValueError, match="NOT_SENT"):
        ContextManifest(
            manifest_id=uuid7(),
            consumer_context_id=uuid7(),
            work_id=uuid7(),
            work_revision=1,
            plan_id=uuid7(),
            plan_revision=1,
            information_need_ids=(uuid7(),),
            exposed_fragment_ids=(uuid7(),),
            source_bindings=(_source(),),
            reality_scope=_current_scope(),
            exposure_state=ExposureState.NOT_SENT,
            consumer_binding="deterministic:test",
            created_at=datetime.now(UTC),
        )
