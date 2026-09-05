"""Unit acceptance for native Gemini Interactions provider normalization."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from uuid import uuid7

import pytest

from dante.modules.intelligence.adapters.outbound.model.gemini_interactions import (
    GEMINI_INTERACTIONS_BINDING_REF,
    GEMINI_INTERACTIONS_HARNESS_REF,
    GEMINI_INTERACTIONS_MODEL,
    GEMINI_INTERACTIONS_ROUTE_REVISION,
    GeminiInteractionStatus,
    GeminiInteractionsAdapter,
    GeminiInteractionsWireRequest,
    GeminiInteractionsWireResponse,
    GeminiTransportError,
    GeminiTransportErrorKind,
)
from dante.modules.intelligence.contracts.model_access import (
    ProviderAcceptanceCertainty,
    ProviderAttemptOutcome,
    ProviderErrorClass,
    ProviderInvocationRequest,
    ProviderUsageState,
    StructuredOutputContract,
)
from dante.modules.intelligence.contracts.route_config import RouteConfigIdentity

_NOW = datetime(2026, 9, 5, 12, 0, tzinfo=UTC)
_FEATURES = (
    "streaming:off",
    "background:off",
    "provider_continuation:off",
    "provider_native_tools:off",
    "provider_storage:off",
    "structured_output:on",
)


class _ScriptedTransport:
    def __init__(
        self,
        *,
        response: GeminiInteractionsWireResponse | None = None,
        error: GeminiTransportError | None = None,
    ) -> None:
        self.response = response
        self.error = error
        self.requests: list[GeminiInteractionsWireRequest] = []

    async def create(
        self, request: GeminiInteractionsWireRequest
    ) -> GeminiInteractionsWireResponse:
        self.requests.append(request)
        if self.error is not None:
            raise self.error
        assert self.response is not None
        return self.response


def _clock() -> datetime:
    return _NOW


def _request(*, structured: bool = True) -> ProviderInvocationRequest:
    return ProviderInvocationRequest(
        provider_attempt_id=uuid7(),
        model_invocation_id=uuid7(),
        work_id=uuid7(),
        work_revision=1,
        provider_binding_ref=GEMINI_INTERACTIONS_BINDING_REF,
        model_target_ref="structured_interpretation",
        provider_model=GEMINI_INTERACTIONS_MODEL,
        harness_profile_ref=GEMINI_INTERACTIONS_HARNESS_REF,
        purpose="foundation-test",
        rendered_input="Synthetic public prompt",
        rendered_instructions="Return only grounded data.",
        deadline=_NOW + timedelta(seconds=30),
        max_output_tokens=128,
        route_config_identity=RouteConfigIdentity(
            revision=GEMINI_INTERACTIONS_ROUTE_REVISION,
            content_sha256="0" * 64,
        ),
        structured_output=(
            StructuredOutputContract(
                name="answer",
                schema_json='{"type":"object","properties":{"ok":{"type":"boolean"}}}',
            )
            if structured
            else None
        ),
        reasoning_level="low",
        feature_modes=_FEATURES,
        security_basis_refs=("synthetic-public-only",),
    )


def _response(output_text: str = '{"ok":true}') -> GeminiInteractionsWireResponse:
    return GeminiInteractionsWireResponse(
        status=GeminiInteractionStatus.COMPLETED,
        interaction_id="interaction-1",
        request_id="request-1",
        output_text=output_text,
        input_tokens=100,
        output_tokens=20,
        thought_tokens=35,
        cached_tokens=5,
        tool_use_tokens=0,
        total_tokens=155,
    )


@pytest.mark.asyncio
async def test_native_adapter_preserves_thought_and_cached_usage() -> None:
    transport = _ScriptedTransport(response=_response())
    result = await GeminiInteractionsAdapter(transport, clock=_clock).invoke(_request())

    assert result.outcome is ProviderAttemptOutcome.COMPLETED
    assert result.acceptance is ProviderAcceptanceCertainty.ESTABLISHED
    assert result.structured_output_json == '{"ok":true}'
    assert result.usage.state is ProviderUsageState.KNOWN
    assert result.usage.input_tokens == 100
    assert result.usage.output_tokens == 20
    assert result.usage.reasoning_tokens == 35
    assert result.usage.cached_input_tokens == 5
    assert result.usage.total_tokens == 155
    wire = transport.requests[0]
    assert wire.store is False
    assert wire.stream is False
    assert wire.background is False
    assert wire.tool_choice == "none"
    assert wire.thinking_level == "low"


@pytest.mark.asyncio
async def test_invalid_structured_json_is_normalized_not_promoted() -> None:
    transport = _ScriptedTransport(response=_response("Here is the JSON"))
    result = await GeminiInteractionsAdapter(transport, clock=_clock).invoke(_request())

    assert result.outcome is ProviderAttemptOutcome.INVALID_RESPONSE
    assert result.error_class is ProviderErrorClass.INVALID_RESPONSE
    assert result.error_code == "invalid_structured_json"
    assert result.structured_output_json is None


@pytest.mark.asyncio
async def test_timeout_after_dispatch_is_indeterminate_not_blindly_retryable() -> None:
    transport = _ScriptedTransport(
        error=GeminiTransportError(GeminiTransportErrorKind.TIMEOUT)
    )
    result = await GeminiInteractionsAdapter(transport, clock=_clock).invoke(_request())

    assert result.outcome is ProviderAttemptOutcome.INDETERMINATE
    assert result.acceptance is ProviderAcceptanceCertainty.POSSIBLE
    assert result.error_class is ProviderErrorClass.TIMEOUT


@pytest.mark.asyncio
async def test_wrong_binding_is_rejected_before_transport_dispatch() -> None:
    transport = _ScriptedTransport(response=_response())
    request = _request()
    wrong = ProviderInvocationRequest(
        provider_attempt_id=request.provider_attempt_id,
        model_invocation_id=request.model_invocation_id,
        work_id=request.work_id,
        work_revision=request.work_revision,
        provider_binding_ref="wrong-binding",
        model_target_ref=request.model_target_ref,
        provider_model=request.provider_model,
        harness_profile_ref=request.harness_profile_ref,
        purpose=request.purpose,
        rendered_input=request.rendered_input,
        rendered_instructions=request.rendered_instructions,
        deadline=request.deadline,
        max_output_tokens=request.max_output_tokens,
        route_config_identity=request.route_config_identity,
        structured_output=request.structured_output,
        reasoning_level=request.reasoning_level,
        feature_modes=request.feature_modes,
        security_basis_refs=request.security_basis_refs,
    )

    result = await GeminiInteractionsAdapter(transport, clock=_clock).invoke(wrong)

    assert result.outcome is ProviderAttemptOutcome.UNSUPPORTED_FEATURE
    assert transport.requests == []
