"""Unit acceptance for Intelligence policy-consumer contracts."""

from datetime import UTC, datetime, timedelta
from uuid import uuid7

import pytest

from dante.modules.intelligence.contracts.policy import (
    ModelEgressPolicyRequest,
    PolicyBoundary,
    PolicyDecision,
    PolicyDecisionOutcome,
    PolicyRequestContext,
)
from tests.unit.modules.intelligence.fakes import ScriptedPolicyPort


def _context() -> PolicyRequestContext:
    return PolicyRequestContext(
        work_id=uuid7(),
        work_revision=1,
        principal_binding="principal:self",
        recipient="self",
        surface="private_in_app",
        purpose="ask_dante",
        authz_basis_refs=("authz:current",),
        visibility_basis_refs=("visibility:current",),
    )


def _decision(context: PolicyRequestContext) -> PolicyDecision:
    return PolicyDecision(
        decision_id=uuid7(),
        boundary=PolicyBoundary.MODEL_EGRESS,
        outcome=PolicyDecisionOutcome.ALLOW,
        work_id=context.work_id,
        work_revision=context.work_revision,
        principal_binding=context.principal_binding,
        recipient=context.recipient,
        surface=context.surface,
        purpose=context.purpose,
        basis_refs=("policy:egress:v1", "authz:current"),
        revalidation_requirement="before_each_material_send",
        internal_reason_code="eligible_minimized_context",
        evaluated_at=datetime.now(UTC),
    )


def test_policy_decision_requires_material_basis_and_valid_time_window() -> None:
    context = _context()
    now = datetime.now(UTC)

    with pytest.raises(ValueError, match="basis_refs"):
        PolicyDecision(
            decision_id=uuid7(),
            boundary=PolicyBoundary.MODEL_EGRESS,
            outcome=PolicyDecisionOutcome.ALLOW,
            work_id=context.work_id,
            work_revision=1,
            principal_binding=context.principal_binding,
            recipient=context.recipient,
            surface=context.surface,
            purpose=context.purpose,
            basis_refs=(),
            revalidation_requirement="before_send",
            internal_reason_code="allow",
            evaluated_at=now,
        )

    with pytest.raises(ValueError, match="valid_until"):
        PolicyDecision(
            decision_id=uuid7(),
            boundary=PolicyBoundary.MODEL_EGRESS,
            outcome=PolicyDecisionOutcome.DENY,
            work_id=context.work_id,
            work_revision=1,
            principal_binding=context.principal_binding,
            recipient=context.recipient,
            surface=context.surface,
            purpose=context.purpose,
            basis_refs=("policy:egress:v1",),
            revalidation_requirement="before_send",
            internal_reason_code="revoked",
            evaluated_at=now,
            valid_until=now - timedelta(seconds=1),
        )


@pytest.mark.asyncio
async def test_policy_fake_is_boundary_specific_and_records_current_request() -> None:
    context = _context()
    decision = _decision(context)
    request = ModelEgressPolicyRequest(
        context=context,
        consumer_context_id=uuid7(),
        recipient_binding="provider-candidate:test",
        projection_ref="consumer-projection:v1",
        prior_egress_attempt_refs=("egress:prior",),
    )
    policy = ScriptedPolicyPort({PolicyBoundary.MODEL_EGRESS: decision})

    result = await policy.authorize_model_egress(request)

    assert result == decision
    assert policy.model_egress_requests == [request]
    assert result.boundary is PolicyBoundary.MODEL_EGRESS


@pytest.mark.asyncio
async def test_policy_fake_rejects_decision_for_different_request_context() -> None:
    current_context = _context()
    stale_context = _context()
    request = ModelEgressPolicyRequest(
        context=current_context,
        consumer_context_id=uuid7(),
        recipient_binding="provider-candidate:test",
        projection_ref="consumer-projection:v1",
    )
    policy = ScriptedPolicyPort({PolicyBoundary.MODEL_EGRESS: _decision(stale_context)})

    with pytest.raises(ValueError, match="current request context"):
        await policy.authorize_model_egress(request)
