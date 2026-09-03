"""Unit acceptance for provider-neutral ModelAccess and ProviderAttempt contracts."""

from datetime import UTC, datetime, timedelta
from uuid import uuid7

import pytest

from dante.modules.intelligence.contracts.model_access import (
    ProviderAcceptanceCertainty,
    ProviderAttemptOutcome,
    ProviderAttemptResult,
    ProviderErrorClass,
    ProviderInvocationRequest,
    ProviderUsageEvidence,
    ProviderUsageState,
    StructuredOutputContract,
)
from dante.modules.intelligence.contracts.route_config import RouteConfigIdentity

_NOW = datetime(2026, 9, 3, 20, 0, tzinfo=UTC)


def _request() -> ProviderInvocationRequest:
    return ProviderInvocationRequest(
        provider_attempt_id=uuid7(),
        model_invocation_id=uuid7(),
        work_id=uuid7(),
        work_revision=1,
        provider_binding_ref="openai-responses-terra-candidate-v1",
        model_target_ref="ask-readonly-terra-v1",
        provider_model="gpt-5.6-terra",
        harness_profile_ref="ask-readonly-openai-v1",
        purpose="qualification",
        rendered_input="Synthetic public qualification prompt",
        deadline=_NOW + timedelta(seconds=30),
        max_output_tokens=128,
        route_config_identity=RouteConfigIdentity(
            revision="openai-terra-candidate-v1",
            content_sha256="0" * 64,
        ),
        feature_modes=(
            "streaming:off",
            "background:off",
            "provider_continuation:off",
            "provider_native_tools:off",
            "provider_storage:off",
        ),
        security_basis_refs=("c9:synthetic-public-only",),
    )


def test_provider_invocation_requires_dante_allocated_uuid7_attempt_identity() -> None:
    request = _request()
    assert request.provider_attempt_id.version == 7
    assert request.model_invocation_id.version == 7


def test_structured_output_contract_rejects_non_object_json_schema() -> None:
    with pytest.raises(ValueError, match="JSON object schema"):
        StructuredOutputContract(name="answer", schema_json="[]")


def test_unknown_usage_cannot_fabricate_zero_token_counts() -> None:
    with pytest.raises(ValueError, match="must not fabricate"):
        ProviderUsageEvidence(
            state=ProviderUsageState.UNKNOWN,
            input_tokens=0,
            output_tokens=0,
            total_tokens=0,
        )


def test_completed_provider_attempt_requires_output_and_established_acceptance() -> None:
    request = _request()
    with pytest.raises(ValueError, match="requires provider output"):
        ProviderAttemptResult(
            provider_attempt_id=request.provider_attempt_id,
            model_invocation_id=request.model_invocation_id,
            outcome=ProviderAttemptOutcome.COMPLETED,
            acceptance=ProviderAcceptanceCertainty.ESTABLISHED,
            usage=ProviderUsageEvidence(
                state=ProviderUsageState.KNOWN,
                input_tokens=10,
                output_tokens=4,
                total_tokens=14,
            ),
            started_at=_NOW,
            completed_at=_NOW,
        )


def test_indeterminate_provider_attempt_requires_possible_acceptance() -> None:
    request = _request()
    with pytest.raises(ValueError, match="requires POSSIBLE"):
        ProviderAttemptResult(
            provider_attempt_id=request.provider_attempt_id,
            model_invocation_id=request.model_invocation_id,
            outcome=ProviderAttemptOutcome.INDETERMINATE,
            acceptance=ProviderAcceptanceCertainty.ESTABLISHED,
            usage=ProviderUsageEvidence(state=ProviderUsageState.UNKNOWN),
            started_at=_NOW,
            completed_at=_NOW,
            error_class=ProviderErrorClass.TIMEOUT,
        )


def test_incomplete_provider_attempt_may_preserve_partial_output_without_promotion() -> None:
    request = _request()
    result = ProviderAttemptResult(
        provider_attempt_id=request.provider_attempt_id,
        model_invocation_id=request.model_invocation_id,
        outcome=ProviderAttemptOutcome.INCOMPLETE,
        acceptance=ProviderAcceptanceCertainty.ESTABLISHED,
        usage=ProviderUsageEvidence(state=ProviderUsageState.UNKNOWN),
        started_at=_NOW,
        completed_at=_NOW,
        output_text="partial",
    )
    assert result.outcome is ProviderAttemptOutcome.INCOMPLETE
    assert result.output_text == "partial"
