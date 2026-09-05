"""Unit acceptance for deterministic Semantic Query contracts and fake gateway."""

from uuid import uuid7

import pytest

from dante.modules.intelligence.contracts.context import (
    ContextStrategy,
    ContextStrategyKind,
    CoverageRequirement,
    InformationGuarantee,
    InformationNeed,
    InformationNeedOrigin,
    InformationNeedStatus,
    NeedCriticality,
    RealityScope,
    RealityScopeKind,
    SourceCurrentness,
)
from dante.modules.intelligence.contracts.references import (
    NativeRefBinding,
    ReferenceBindingRequirement,
)
from dante.modules.intelligence.contracts.semantic_query import (
    SemanticAggregate,
    SemanticQueryOutcome,
    SemanticQueryRequest,
    SemanticQueryStatus,
)
from tests.unit.modules.intelligence.fakes import ScriptedSemanticQueryGateway


def _need() -> InformationNeed:
    return InformationNeed(
        need_id=uuid7(),
        revision=1,
        requirement="total running distance in the bounded period",
        origin=InformationNeedOrigin.USER_EXPLICIT,
        purpose="ask_dante",
        reality_scope=RealityScope(kind=RealityScopeKind.CANONICAL_CURRENT),
        reference_requirement=ReferenceBindingRequirement.UNIQUE_IN_SCOPE,
        criticality=NeedCriticality.REQUIRED,
        coverage_requirement=CoverageRequirement.BOUNDED_COMPLETE,
        acceptable_source_semantics=("actual.realization",),
        freshness_requirement="current_at_query",
        coherence_requirement="single_statement",
        fidelity_requirement="exact_numeric",
        status=InformationNeedStatus.MISSING,
    )


def _strategy(need: InformationNeed) -> ContextStrategy:
    return ContextStrategy(
        strategy_id=uuid7(),
        need_id=need.need_id,
        kind=ContextStrategyKind.DETERMINISTIC_AGGREGATION,
        purpose=need.purpose,
        reality_scope=need.reality_scope,
        required_guarantee=InformationGuarantee.BOUNDED_COMPLETE,
        source_classes=("actual.realization",),
        permitted_transformations=(),
        exclusions=(),
        max_refinements=0,
    )


def test_semantic_query_request_binds_need_and_strategy() -> None:
    need = _need()
    wrong_strategy = _strategy(_need())
    with pytest.raises(ValueError, match="must target"):
        SemanticQueryRequest(
            query_id=uuid7(),
            work_id=uuid7(),
            work_revision=1,
            information_need=need,
            strategy=wrong_strategy,
            capability_contract_id="activity.query.distance:v1",
            purpose="ask_dante",
        )


@pytest.mark.asyncio
async def test_scripted_gateway_returns_typed_structured_outcome() -> None:
    need = _need()
    strategy = _strategy(need)
    query_id = uuid7()
    source = NativeRefBinding(native_ref=uuid7())
    outcome = SemanticQueryOutcome(
        query_id=query_id,
        status=SemanticQueryStatus.SUCCEEDED,
        payload=SemanticAggregate(metric="distance", value=42.0, unit="km"),
        achieved_guarantee=InformationGuarantee.BOUNDED_COMPLETE,
        source_bindings=(source,),
        currentness=SourceCurrentness.CURRENT,
        basis_refs=("query:actual-distance:v1",),
        coherence_evidence=("single_statement",),
        source_standing="canonical_owner_query",
    )
    gateway = ScriptedSemanticQueryGateway({query_id: outcome})
    request = SemanticQueryRequest(
        query_id=query_id,
        work_id=uuid7(),
        work_revision=1,
        information_need=need,
        strategy=strategy,
        capability_contract_id="activity.query.distance:v1",
        purpose="ask_dante",
    )

    result = await gateway.execute(request)

    assert result == outcome
    assert gateway.requests == [request]


@pytest.mark.asyncio
async def test_unscripted_gateway_is_not_integration_ready_not_db_bypass() -> None:
    need = _need()
    request = SemanticQueryRequest(
        query_id=uuid7(),
        work_id=uuid7(),
        work_revision=1,
        information_need=need,
        strategy=_strategy(need),
        capability_contract_id="missing.capability.query:v1",
        purpose="ask_dante",
    )
    gateway = ScriptedSemanticQueryGateway({})

    result = await gateway.execute(request)

    assert result.status is SemanticQueryStatus.NOT_INTEGRATION_READY
    assert result.payload is None


def test_non_success_semantic_outcome_cannot_carry_payload() -> None:
    with pytest.raises(ValueError, match="must not carry payload"):
        SemanticQueryOutcome(
            query_id=uuid7(),
            status=SemanticQueryStatus.UNSUPPORTED,
            payload=SemanticAggregate(metric="distance", value=42.0, unit="km"),
        )
