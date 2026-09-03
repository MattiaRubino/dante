"""Inactive OpenAI Responses adapter for the admitted GPT-5.6 Terra candidate."""

from __future__ import annotations

import json
from collections.abc import Callable
from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum
from typing import Protocol

from dante.modules.intelligence.contracts.model_access import (
    ProviderAcceptanceCertainty,
    ProviderAttemptOutcome,
    ProviderAttemptResult,
    ProviderErrorClass,
    ProviderInvocationRequest,
    ProviderUsageEvidence,
    ProviderUsageState,
)

OPENAI_RESPONSES_BINDING_REF = "openai-responses-terra-candidate-v1"
OPENAI_TERRA_MODEL_TARGET_REF = "ask-readonly-terra-v1"
OPENAI_TERRA_HARNESS_PROFILE_REF = "ask-readonly-openai-v1"
OPENAI_TERRA_MODEL = "gpt-5.6-terra"
OPENAI_TERRA_ROUTE_CONFIG_REVISION = "openai-terra-candidate-v1"

_REQUIRED_FEATURE_MODES = frozenset(
    {
        "streaming:off",
        "background:off",
        "provider_continuation:off",
        "provider_native_tools:off",
        "provider_storage:off",
    }
)


class OpenAIResponseStatus(StrEnum):
    """Final non-background status exposed by the C9 transport seam."""

    COMPLETED = "completed"
    INCOMPLETE = "incomplete"


class OpenAITransportErrorKind(StrEnum):
    """Provider-specific transport failure classes before DANTE normalization."""

    RATE_LIMIT = "rate_limit"
    CONNECTION = "connection"
    TIMEOUT = "timeout"
    INVALID_REQUEST = "invalid_request"
    AUTHENTICATION = "authentication"
    PERMISSION = "permission"
    NOT_FOUND = "not_found"
    CONFLICT = "conflict"
    SERVER = "server"
    INVALID_RESPONSE = "invalid_response"
    CANCELLED = "cancelled"
    UNKNOWN = "unknown"


@dataclass(frozen=True, slots=True)
class OpenAIResponsesWireRequest:
    """Exact request surface allowed to reach the OpenAI Responses transport."""

    model: str
    input_text: str
    instructions: str | None
    max_output_tokens: int
    store: bool
    structured_output_name: str | None = None
    structured_output_schema_json: str | None = None
    structured_output_strict: bool | None = None


@dataclass(frozen=True, slots=True)
class OpenAIResponsesWireResponse:
    """Minimal provider response surface consumed by the DANTE adapter."""

    status: OpenAIResponseStatus
    response_id: str
    request_id: str | None
    output_text: str | None
    refusal_reason: str | None
    input_tokens: int | None
    output_tokens: int | None
    total_tokens: int | None


class OpenAIResponsesTransport(Protocol):
    """Narrow provider transport seam implemented later by the private OpenAI SDK wrapper."""

    async def create(self, request: OpenAIResponsesWireRequest) -> OpenAIResponsesWireResponse: ...


class OpenAITransportError(RuntimeError):
    """Provider-specific transport error that never escapes the adapter boundary."""

    def __init__(
        self,
        kind: OpenAITransportErrorKind,
        *,
        code: str | None = None,
        request_id: str | None = None,
    ) -> None:
        super().__init__(kind.value)
        self.kind = kind
        self.code = code
        self.request_id = request_id


def _utc_now() -> datetime:
    return datetime.now(UTC)


def _unknown_usage() -> ProviderUsageEvidence:
    return ProviderUsageEvidence(state=ProviderUsageState.UNKNOWN)


def _usage_from_response(response: OpenAIResponsesWireResponse) -> ProviderUsageEvidence:
    counts = (response.input_tokens, response.output_tokens, response.total_tokens)
    if any(value is None for value in counts):
        return _unknown_usage()
    return ProviderUsageEvidence(
        state=ProviderUsageState.KNOWN,
        input_tokens=response.input_tokens,
        output_tokens=response.output_tokens,
        total_tokens=response.total_tokens,
    )


def _provider_error_class(kind: OpenAITransportErrorKind) -> ProviderErrorClass:
    mapping = {
        OpenAITransportErrorKind.RATE_LIMIT: ProviderErrorClass.RATE_LIMIT,
        OpenAITransportErrorKind.CONNECTION: ProviderErrorClass.CONNECTION,
        OpenAITransportErrorKind.TIMEOUT: ProviderErrorClass.TIMEOUT,
        OpenAITransportErrorKind.INVALID_REQUEST: ProviderErrorClass.INVALID_REQUEST,
        OpenAITransportErrorKind.AUTHENTICATION: ProviderErrorClass.AUTHENTICATION,
        OpenAITransportErrorKind.PERMISSION: ProviderErrorClass.PERMISSION,
        OpenAITransportErrorKind.NOT_FOUND: ProviderErrorClass.NOT_FOUND,
        OpenAITransportErrorKind.CONFLICT: ProviderErrorClass.CONFLICT,
        OpenAITransportErrorKind.SERVER: ProviderErrorClass.SERVER,
        OpenAITransportErrorKind.INVALID_RESPONSE: ProviderErrorClass.INVALID_RESPONSE,
        OpenAITransportErrorKind.CANCELLED: ProviderErrorClass.CANCELLATION,
        OpenAITransportErrorKind.UNKNOWN: ProviderErrorClass.UNKNOWN,
    }
    return mapping[kind]


def _provider_error_outcome(
    kind: OpenAITransportErrorKind,
) -> tuple[ProviderAttemptOutcome, ProviderAcceptanceCertainty]:
    if kind in {OpenAITransportErrorKind.TIMEOUT, OpenAITransportErrorKind.CONNECTION}:
        return ProviderAttemptOutcome.INDETERMINATE, ProviderAcceptanceCertainty.POSSIBLE
    if kind is OpenAITransportErrorKind.CANCELLED:
        return ProviderAttemptOutcome.CANCELLED, ProviderAcceptanceCertainty.POSSIBLE
    if kind is OpenAITransportErrorKind.INVALID_RESPONSE:
        return ProviderAttemptOutcome.INVALID_RESPONSE, ProviderAcceptanceCertainty.ESTABLISHED
    if kind in {
        OpenAITransportErrorKind.RATE_LIMIT,
        OpenAITransportErrorKind.CONFLICT,
        OpenAITransportErrorKind.SERVER,
    }:
        return ProviderAttemptOutcome.TRANSIENT_FAILURE, ProviderAcceptanceCertainty.ESTABLISHED
    if kind in {
        OpenAITransportErrorKind.INVALID_REQUEST,
        OpenAITransportErrorKind.AUTHENTICATION,
        OpenAITransportErrorKind.PERMISSION,
        OpenAITransportErrorKind.NOT_FOUND,
    }:
        return ProviderAttemptOutcome.PERMANENT_FAILURE, ProviderAcceptanceCertainty.ESTABLISHED
    return ProviderAttemptOutcome.INDETERMINATE, ProviderAcceptanceCertainty.POSSIBLE


class OpenAIResponsesAdapter:
    """Binding-specific inactive adapter; it owns protocol normalization only."""

    def __init__(
        self,
        transport: OpenAIResponsesTransport,
        *,
        clock: Callable[[], datetime] = _utc_now,
    ) -> None:
        self._transport = transport
        self._clock = clock

    async def invoke(self, request: ProviderInvocationRequest) -> ProviderAttemptResult:
        started_at = self._clock()
        preflight_error = self._preflight_error(request, started_at)
        if preflight_error is not None:
            return preflight_error

        wire_request = OpenAIResponsesWireRequest(
            model=OPENAI_TERRA_MODEL,
            input_text=request.rendered_input,
            instructions=request.rendered_instructions,
            max_output_tokens=request.max_output_tokens,
            store=False,
            structured_output_name=(
                request.structured_output.name if request.structured_output is not None else None
            ),
            structured_output_schema_json=(
                request.structured_output.schema_json
                if request.structured_output is not None
                else None
            ),
            structured_output_strict=(
                request.structured_output.strict if request.structured_output is not None else None
            ),
        )

        try:
            response = await self._transport.create(wire_request)
        except OpenAITransportError as exc:
            completed_at = self._clock()
            outcome, acceptance = _provider_error_outcome(exc.kind)
            return ProviderAttemptResult(
                provider_attempt_id=request.provider_attempt_id,
                model_invocation_id=request.model_invocation_id,
                outcome=outcome,
                acceptance=acceptance,
                usage=_unknown_usage(),
                started_at=started_at,
                completed_at=completed_at,
                provider_request_id=exc.request_id,
                error_class=_provider_error_class(exc.kind),
                error_code=exc.code,
            )

        completed_at = self._clock()
        return self._normalize_response(request, response, started_at, completed_at)

    def _preflight_error(
        self,
        request: ProviderInvocationRequest,
        started_at: datetime,
    ) -> ProviderAttemptResult | None:
        if request.deadline <= started_at:
            return ProviderAttemptResult(
                provider_attempt_id=request.provider_attempt_id,
                model_invocation_id=request.model_invocation_id,
                outcome=ProviderAttemptOutcome.PRE_ACCEPTANCE_FAILURE,
                acceptance=ProviderAcceptanceCertainty.NOT_ACCEPTED,
                usage=_unknown_usage(),
                started_at=started_at,
                completed_at=started_at,
                error_class=ProviderErrorClass.DEADLINE,
                error_code="deadline_before_dispatch",
            )

        expected_values = (
            (request.provider_binding_ref, OPENAI_RESPONSES_BINDING_REF),
            (request.model_target_ref, OPENAI_TERRA_MODEL_TARGET_REF),
            (request.provider_model, OPENAI_TERRA_MODEL),
            (request.harness_profile_ref, OPENAI_TERRA_HARNESS_PROFILE_REF),
            (request.route_config_identity.revision, OPENAI_TERRA_ROUTE_CONFIG_REVISION),
        )
        feature_modes = frozenset(request.feature_modes)
        if any(observed != expected for observed, expected in expected_values) or (
            feature_modes != _REQUIRED_FEATURE_MODES
        ):
            return ProviderAttemptResult(
                provider_attempt_id=request.provider_attempt_id,
                model_invocation_id=request.model_invocation_id,
                outcome=ProviderAttemptOutcome.UNSUPPORTED_FEATURE,
                acceptance=ProviderAcceptanceCertainty.NOT_ACCEPTED,
                usage=_unknown_usage(),
                started_at=started_at,
                completed_at=started_at,
                error_class=ProviderErrorClass.UNSUPPORTED_FEATURE,
                error_code="binding_or_feature_mode_not_admitted",
            )
        return None

    def _normalize_response(
        self,
        request: ProviderInvocationRequest,
        response: OpenAIResponsesWireResponse,
        started_at: datetime,
        completed_at: datetime,
    ) -> ProviderAttemptResult:
        usage = _usage_from_response(response)
        if response.refusal_reason is not None:
            if response.output_text is not None:
                return self._invalid_response(
                    request,
                    response,
                    usage,
                    started_at,
                    completed_at,
                    code="refusal_with_output",
                )
            return ProviderAttemptResult(
                provider_attempt_id=request.provider_attempt_id,
                model_invocation_id=request.model_invocation_id,
                outcome=ProviderAttemptOutcome.REFUSED,
                acceptance=ProviderAcceptanceCertainty.ESTABLISHED,
                usage=usage,
                started_at=started_at,
                completed_at=completed_at,
                provider_request_id=response.request_id,
                provider_response_id=response.response_id,
                refusal_reason=response.refusal_reason,
            )

        if response.output_text is None:
            return self._invalid_response(
                request,
                response,
                usage,
                started_at,
                completed_at,
                code="missing_output",
            )

        if request.structured_output is not None:
            try:
                parsed = json.loads(response.output_text)
            except json.JSONDecodeError:
                return self._invalid_response(
                    request,
                    response,
                    usage,
                    started_at,
                    completed_at,
                    code="invalid_structured_json",
                )
            if not isinstance(parsed, dict):
                return self._invalid_response(
                    request,
                    response,
                    usage,
                    started_at,
                    completed_at,
                    code="structured_output_not_object",
                )
            output_text = None
            structured_output_json = response.output_text
        else:
            output_text = response.output_text
            structured_output_json = None

        outcome = (
            ProviderAttemptOutcome.COMPLETED
            if response.status is OpenAIResponseStatus.COMPLETED
            else ProviderAttemptOutcome.INCOMPLETE
        )
        return ProviderAttemptResult(
            provider_attempt_id=request.provider_attempt_id,
            model_invocation_id=request.model_invocation_id,
            outcome=outcome,
            acceptance=ProviderAcceptanceCertainty.ESTABLISHED,
            usage=usage,
            started_at=started_at,
            completed_at=completed_at,
            provider_request_id=response.request_id,
            provider_response_id=response.response_id,
            output_text=output_text,
            structured_output_json=structured_output_json,
        )

    @staticmethod
    def _invalid_response(
        request: ProviderInvocationRequest,
        response: OpenAIResponsesWireResponse,
        usage: ProviderUsageEvidence,
        started_at: datetime,
        completed_at: datetime,
        *,
        code: str,
    ) -> ProviderAttemptResult:
        return ProviderAttemptResult(
            provider_attempt_id=request.provider_attempt_id,
            model_invocation_id=request.model_invocation_id,
            outcome=ProviderAttemptOutcome.INVALID_RESPONSE,
            acceptance=ProviderAcceptanceCertainty.ESTABLISHED,
            usage=usage,
            started_at=started_at,
            completed_at=completed_at,
            provider_request_id=response.request_id,
            provider_response_id=response.response_id,
            error_class=ProviderErrorClass.INVALID_RESPONSE,
            error_code=code,
        )
