"""Deterministic C9 conformance for the inactive OpenAI Responses adapter."""

from datetime import UTC, datetime, timedelta
from uuid import uuid7

import pytest

from dante.modules.intelligence.adapters.outbound.model.openai_responses import (
    OPENAI_RESPONSES_BINDING_REF,
    OPENAI_TERRA_HARNESS_PROFILE_REF,
    OPENAI_TERRA_MODEL,
    OPENAI_TERRA_MODEL_TARGET_REF,
    OPENAI_TERRA_ROUTE_CONFIG_REVISION,
    OpenAIResponsesAdapter,
    OpenAIResponseStatus,
    OpenAIResponsesWireRequest,
    OpenAIResponsesWireResponse,
    OpenAITransportError,
    OpenAITransportErrorKind,
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

_NOW = datetime(2026, 9, 3, 20, 0, tzinfo=UTC)
_FEATURE_MODES = (
    "streaming:off",
    "background:off",
    "provider_continuation:off",
    "provider_native_tools:off",
    "provider_storage:off",
)


class ScriptedOpenAITransport:
    """Deterministic provider transport used only for adapter conformance."""

    requests: list[OpenAIResponsesWireRequest]

    def __init__(
        self,
        *,
        response: OpenAIResponsesWireResponse | None = None,
        error: OpenAITransportError | None = None,
    ) -> None:
        self.response = response
        self.error = error
        self.requests = []

    async def create(self, request: OpenAIResponsesWireRequest) -> OpenAIResponsesWireResponse:
        self.requests.append(request)
        if self.error is not None:
            raise self.error
        if self.response is None:
            raise AssertionError("scripted transport requires response or error")
        return self.response


def _request(
    *,
    provider_binding_ref: str = OPENAI_RESPONSES_BINDING_REF,
    deadline: datetime | None = None,
    structured_output: StructuredOutputContract | None = None,
) -> ProviderInvocationRequest:
    return ProviderInvocationRequest(
        provider_attempt_id=uuid7(),
        model_invocation_id=uuid7(),
        work_id=uuid7(),
        work_revision=1,
        provider_binding_ref=provider_binding_ref,
        model_target_ref=OPENAI_TERRA_MODEL_TARGET_REF,
        provider_model=OPENAI_TERRA_MODEL,
        harness_profile_ref=OPENAI_TERRA_HARNESS_PROFILE_REF,
        purpose="qualification",
        rendered_input="Synthetic public qualification prompt",
        rendered_instructions="Answer only from the supplied synthetic prompt.",
        deadline=deadline or (_NOW + timedelta(seconds=30)),
        max_output_tokens=128,
        route_config_identity=RouteConfigIdentity(
            revision=OPENAI_TERRA_ROUTE_CONFIG_REVISION,
            content_sha256="0" * 64,
        ),
        structured_output=structured_output,
        feature_modes=_FEATURE_MODES,
        security_basis_refs=("c9:synthetic-public-only",),
    )


def _response(
    *,
    status: OpenAIResponseStatus = OpenAIResponseStatus.COMPLETED,
    output_text: str | None = "synthetic answer",
    refusal_reason: str | None = None,
    input_tokens: int | None = 10,
    output_tokens: int | None = 4,
    total_tokens: int | None = 14,
) -> OpenAIResponsesWireResponse:
    return OpenAIResponsesWireResponse(
        status=status,
        response_id="resp_test",
        request_id="req_test",
        output_text=output_text,
        refusal_reason=refusal_reason,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        total_tokens=total_tokens,
    )


@pytest.mark.asyncio
async def test_completed_response_preserves_attempt_identity_usage_and_forces_no_store() -> None:
    request = _request()
    transport = ScriptedOpenAITransport(response=_response())
    adapter = OpenAIResponsesAdapter(transport, clock=lambda: _NOW)

    result = await adapter.invoke(request)

    assert result.provider_attempt_id == request.provider_attempt_id
    assert result.model_invocation_id == request.model_invocation_id
    assert result.outcome is ProviderAttemptOutcome.COMPLETED
    assert result.acceptance is ProviderAcceptanceCertainty.ESTABLISHED
    assert result.output_text == "synthetic answer"
    assert result.usage.state is ProviderUsageState.KNOWN
    assert result.usage.total_tokens == 14
    assert len(transport.requests) == 1
    wire_request = transport.requests[0]
    assert wire_request.model == OPENAI_TERRA_MODEL
    assert wire_request.store is False
    assert wire_request.timeout_seconds == 30.0


@pytest.mark.asyncio
async def test_incomplete_response_is_not_promoted_to_completed() -> None:
    request = _request()
    transport = ScriptedOpenAITransport(
        response=_response(status=OpenAIResponseStatus.INCOMPLETE, output_text="partial")
    )
    result = await OpenAIResponsesAdapter(transport, clock=lambda: _NOW).invoke(request)

    assert result.outcome is ProviderAttemptOutcome.INCOMPLETE
    assert result.output_text == "partial"


@pytest.mark.asyncio
async def test_refusal_is_distinct_from_infrastructure_failure() -> None:
    request = _request()
    transport = ScriptedOpenAITransport(
        response=_response(output_text=None, refusal_reason="provider_refusal")
    )
    result = await OpenAIResponsesAdapter(transport, clock=lambda: _NOW).invoke(request)

    assert result.outcome is ProviderAttemptOutcome.REFUSED
    assert result.refusal_reason == "provider_refusal"
    assert result.error_class is None


@pytest.mark.parametrize(
    ("kind", "expected_error"),
    [
        (OpenAITransportErrorKind.TIMEOUT, ProviderErrorClass.TIMEOUT),
        (OpenAITransportErrorKind.CONNECTION, ProviderErrorClass.CONNECTION),
    ],
)
@pytest.mark.asyncio
async def test_timeout_or_connection_loss_is_indeterminate_not_safe_preacceptance(
    kind: OpenAITransportErrorKind,
    expected_error: ProviderErrorClass,
) -> None:
    request = _request()
    transport = ScriptedOpenAITransport(error=OpenAITransportError(kind, code="lost"))
    result = await OpenAIResponsesAdapter(transport, clock=lambda: _NOW).invoke(request)

    assert result.outcome is ProviderAttemptOutcome.INDETERMINATE
    assert result.acceptance is ProviderAcceptanceCertainty.POSSIBLE
    assert result.error_class is expected_error
    assert result.usage.state is ProviderUsageState.UNKNOWN


@pytest.mark.asyncio
async def test_rate_limit_is_transient_but_still_an_established_provider_send() -> None:
    request = _request()
    transport = ScriptedOpenAITransport(
        error=OpenAITransportError(
            OpenAITransportErrorKind.RATE_LIMIT,
            code="rate_limit_exceeded",
            request_id="req_rate",
        )
    )
    result = await OpenAIResponsesAdapter(transport, clock=lambda: _NOW).invoke(request)

    assert result.outcome is ProviderAttemptOutcome.TRANSIENT_FAILURE
    assert result.acceptance is ProviderAcceptanceCertainty.ESTABLISHED
    assert result.error_class is ProviderErrorClass.RATE_LIMIT
    assert result.provider_request_id == "req_rate"


@pytest.mark.asyncio
async def test_unadmitted_binding_fails_before_transport_dispatch() -> None:
    request = _request(provider_binding_ref="different-provider-binding")
    transport = ScriptedOpenAITransport(response=_response())
    result = await OpenAIResponsesAdapter(transport, clock=lambda: _NOW).invoke(request)

    assert result.outcome is ProviderAttemptOutcome.UNSUPPORTED_FEATURE
    assert result.acceptance is ProviderAcceptanceCertainty.NOT_ACCEPTED
    assert result.error_class is ProviderErrorClass.UNSUPPORTED_FEATURE
    assert transport.requests == []


@pytest.mark.asyncio
async def test_expired_deadline_fails_before_transport_dispatch() -> None:
    request = _request(deadline=_NOW - timedelta(microseconds=1))
    transport = ScriptedOpenAITransport(response=_response())
    result = await OpenAIResponsesAdapter(transport, clock=lambda: _NOW).invoke(request)

    assert result.outcome is ProviderAttemptOutcome.PRE_ACCEPTANCE_FAILURE
    assert result.acceptance is ProviderAcceptanceCertainty.NOT_ACCEPTED
    assert result.error_class is ProviderErrorClass.DEADLINE
    assert transport.requests == []


@pytest.mark.asyncio
async def test_structured_output_is_json_object_checked_before_normalization() -> None:
    structured = StructuredOutputContract(
        name="answer",
        schema_json='{"type":"object","properties":{"answer":{"type":"string"}}}',
    )
    request = _request(structured_output=structured)
    transport = ScriptedOpenAITransport(response=_response(output_text='{"answer":"ok"}'))
    result = await OpenAIResponsesAdapter(transport, clock=lambda: _NOW).invoke(request)

    assert result.outcome is ProviderAttemptOutcome.COMPLETED
    assert result.output_text is None
    assert result.structured_output_json == '{"answer":"ok"}'
    wire_request = transport.requests[0]
    assert wire_request.structured_output_name == "answer"
    assert wire_request.structured_output_strict is True


@pytest.mark.asyncio
async def test_invalid_structured_output_fails_closed_after_provider_acceptance() -> None:
    structured = StructuredOutputContract(name="answer", schema_json='{"type":"object"}')
    request = _request(structured_output=structured)
    transport = ScriptedOpenAITransport(response=_response(output_text="not-json"))
    result = await OpenAIResponsesAdapter(transport, clock=lambda: _NOW).invoke(request)

    assert result.outcome is ProviderAttemptOutcome.INVALID_RESPONSE
    assert result.acceptance is ProviderAcceptanceCertainty.ESTABLISHED
    assert result.error_class is ProviderErrorClass.INVALID_RESPONSE
    assert result.error_code == "invalid_structured_json"


@pytest.mark.asyncio
async def test_missing_usage_is_unknown_not_zero() -> None:
    request = _request()
    transport = ScriptedOpenAITransport(
        response=_response(input_tokens=None, output_tokens=None, total_tokens=None)
    )
    result = await OpenAIResponsesAdapter(transport, clock=lambda: _NOW).invoke(request)

    assert result.usage.state is ProviderUsageState.UNKNOWN
    assert result.usage.total_tokens is None
