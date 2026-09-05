"""Regression tests for native Gemini terminal-status and structured JSON normalization."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from uuid import uuid7

import pytest

from dante.modules.intelligence.adapters.outbound.model.gemini_interactions import (
    GEMINI_INTERACTIONS_API_REVISION,
    GEMINI_INTERACTIONS_BINDING_REF,
    GEMINI_INTERACTIONS_ENDPOINT,
    GEMINI_INTERACTIONS_HARNESS_REF,
    GEMINI_INTERACTIONS_MODEL,
    GEMINI_INTERACTIONS_ROUTE_REVISION,
    GEMINI_INTERACTIONS_SERVICE_TIER,
    GeminiInteractionsAdapter,
    GeminiInteractionStatus,
    GeminiInteractionsWireRequest,
    GeminiInteractionsWireResponse,
)
from dante.modules.intelligence.contracts.model_access import (
    ProviderAcceptanceCertainty,
    ProviderAttemptOutcome,
    ProviderErrorClass,
    ProviderInvocationRequest,
    StructuredOutputContract,
)
from dante.modules.intelligence.contracts.route_config import RouteConfigIdentity

_NOW = datetime(2026, 9, 5, 14, 30, tzinfo=UTC)
_FEATURES = (
    "streaming:off",
    "background:off",
    "provider_continuation:off",
    "provider_native_tools:off",
    "provider_storage:off",
    "structured_output:on",
)


class _Transport:
    def __init__(self, response: GeminiInteractionsWireResponse) -> None:
        self.response = response
        self.requests: list[GeminiInteractionsWireRequest] = []

    async def create(
        self, request: GeminiInteractionsWireRequest
    ) -> GeminiInteractionsWireResponse:
        self.requests.append(request)
        return self.response


def _clock() -> datetime:
    return _NOW


def _request(*, schema_json: str = '{"type":"object"}') -> ProviderInvocationRequest:
    return ProviderInvocationRequest(
        provider_attempt_id=uuid7(),
        model_invocation_id=uuid7(),
        work_id=uuid7(),
        work_revision=1,
        provider_binding_ref=GEMINI_INTERACTIONS_BINDING_REF,
        model_target_ref="structured_interpretation",
        provider_model=GEMINI_INTERACTIONS_MODEL,
        harness_profile_ref=GEMINI_INTERACTIONS_HARNESS_REF,
        purpose="terminal-status-regression",
        rendered_input="Synthetic public prompt",
        rendered_instructions="Return only schema-conforming JSON.",
        deadline=_NOW + timedelta(seconds=30),
        max_output_tokens=512,
        route_config_identity=RouteConfigIdentity(
            revision=GEMINI_INTERACTIONS_ROUTE_REVISION,
            content_sha256="0" * 64,
        ),
        structured_output=StructuredOutputContract(name="answer", schema_json=schema_json),
        reasoning_level="low",
        feature_modes=_FEATURES,
        security_basis_refs=("synthetic-public-only",),
        provider_endpoint=GEMINI_INTERACTIONS_ENDPOINT,
        provider_api_revision=GEMINI_INTERACTIONS_API_REVISION,
        provider_service_tier=GEMINI_INTERACTIONS_SERVICE_TIER,
    )


def _response(
    *,
    status: GeminiInteractionStatus,
    output_text: str | None,
) -> GeminiInteractionsWireResponse:
    return GeminiInteractionsWireResponse(
        status=status,
        interaction_id=None,
        request_id=None,
        output_text=output_text,
        input_tokens=100,
        output_tokens=2,
        thought_tokens=303,
        cached_tokens=0,
        tool_use_tokens=0,
        total_tokens=405,
        model=GEMINI_INTERACTIONS_MODEL,
        service_tier=GEMINI_INTERACTIONS_SERVICE_TIER,
    )


@pytest.mark.asyncio
async def test_incomplete_status_wins_over_partial_structured_json() -> None:
    transport = _Transport(
        _response(status=GeminiInteractionStatus.INCOMPLETE, output_text="{")
    )

    result = await GeminiInteractionsAdapter(transport, clock=_clock).invoke(_request())

    assert result.outcome is ProviderAttemptOutcome.INCOMPLETE
    assert result.acceptance is ProviderAcceptanceCertainty.ESTABLISHED
    assert result.provider_status == "incomplete"
    assert result.finish_reason == "provider_incomplete"
    assert result.error_class is None
    assert result.error_code is None


@pytest.mark.asyncio
async def test_generic_failed_status_is_transient_not_permanent() -> None:
    transport = _Transport(
        _response(status=GeminiInteractionStatus.FAILED, output_text=None)
    )

    result = await GeminiInteractionsAdapter(transport, clock=_clock).invoke(_request())

    assert result.outcome is ProviderAttemptOutcome.TRANSIENT_FAILURE
    assert result.acceptance is ProviderAcceptanceCertainty.ESTABLISHED
    assert result.error_class is ProviderErrorClass.SERVER
    assert result.error_code == "interaction_failed"


@pytest.mark.asyncio
async def test_adapter_accepts_non_object_structured_json_root() -> None:
    transport = _Transport(
        _response(status=GeminiInteractionStatus.COMPLETED, output_text='["A"]')
    )

    result = await GeminiInteractionsAdapter(transport, clock=_clock).invoke(
        _request(schema_json='{"type":"array","items":{"type":"string"}}')
    )

    assert result.outcome is ProviderAttemptOutcome.COMPLETED
    assert result.structured_output_json == '["A"]'
    assert result.error_class is None
