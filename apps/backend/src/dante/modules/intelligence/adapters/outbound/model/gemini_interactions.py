"""Native Google Gemini Interactions adapter for the DANTE development binding.

Provider mechanics remain private. This adapter is not DANTE routing, memory, policy, truth,
or publication authority.
"""

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

GEMINI_INTERACTIONS_BINDING_REF = "google-gemini-interactions-flash-v2"
GEMINI_INTERACTIONS_HARNESS_REF = "gemini-flash-low-v1"
GEMINI_INTERACTIONS_ROUTE_REVISION = "gemini-flash-dev-v2"
GEMINI_INTERACTIONS_MODEL = "gemini-3.8-flash"
GEMINI_INTERACTIONS_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/interactions"
GEMINI_INTERACTIONS_API_REVISION = "2026-05-20"
GEMINI_INTERACTIONS_SERVICE_TIER = "standard"
_REQUIRED_FEATURE_MODES = frozenset(
    {
        "streaming:off",
        "background:off",
        "provider_continuation:off",
        "provider_native_tools:off",
        "provider_storage:off",
        "structured_output:on",
    }
)
_ALLOWED_REASONING_LEVELS = frozenset({"low", "medium", "high"})


class GeminiInteractionStatus(StrEnum):
    COMPLETED = "completed"
    INCOMPLETE = "incomplete"
    BUDGET_EXCEEDED = "budget_exceeded"
    FAILED = "failed"
    CANCELLED = "cancelled"
    IN_PROGRESS = "in_progress"
    REQUIRES_ACTION = "requires_action"
    QUEUED = "queued"


class GeminiTransportErrorKind(StrEnum):
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
    UNKNOWN = "unknown"


@dataclass(frozen=True, slots=True)
class GeminiInteractionsWireRequest:
    model: str
    input_text: str
    system_instruction: str | None
    max_output_tokens: int
    thinking_level: str
    timeout_seconds: float
    endpoint: str = GEMINI_INTERACTIONS_ENDPOINT
    api_revision: str = GEMINI_INTERACTIONS_API_REVISION
    service_tier: str = GEMINI_INTERACTIONS_SERVICE_TIER
    store: bool = False
    stream: bool = False
    background: bool = False
    tool_choice: str = "none"
    thinking_summaries: str = "none"
    structured_output_schema: dict[str, object] | None = None

    def __post_init__(self) -> None:
        if self.model != GEMINI_INTERACTIONS_MODEL:
            raise ValueError("Gemini wire request model must match admitted binding")
        if self.endpoint != GEMINI_INTERACTIONS_ENDPOINT:
            raise ValueError("Gemini wire request endpoint must match admitted binding")
        if self.api_revision != GEMINI_INTERACTIONS_API_REVISION:
            raise ValueError("Gemini wire request API revision must match admitted binding")
        if self.service_tier != GEMINI_INTERACTIONS_SERVICE_TIER:
            raise ValueError("Gemini wire request service tier must match admitted binding")
        if not self.input_text or not self.input_text.strip():
            raise ValueError("Gemini wire request input_text must be non-empty")
        if self.system_instruction is not None and not self.system_instruction.strip():
            raise ValueError("system_instruction must be non-empty when present")
        if self.max_output_tokens <= 0:
            raise ValueError("max_output_tokens must be positive")
        if self.thinking_level not in _ALLOWED_REASONING_LEVELS:
            raise ValueError("unsupported Gemini thinking level")
        if self.timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be positive")
        if self.store or self.stream or self.background:
            raise ValueError("development Gemini binding must be stateless unary store=false")
        if self.tool_choice != "none":
            raise ValueError("development Gemini binding must disable provider-native tools")
        if self.thinking_summaries != "none":
            raise ValueError("development Gemini binding must disable thinking summaries")


@dataclass(frozen=True, slots=True)
class GeminiInteractionsWireResponse:
    status: GeminiInteractionStatus
    interaction_id: str
    request_id: str | None
    output_text: str | None
    input_tokens: int | None
    output_tokens: int | None
    thought_tokens: int | None
    cached_tokens: int | None
    tool_use_tokens: int | None
    total_tokens: int | None
    model: str | None = None
    service_tier: str | None = None
    error_code: str | None = None


class GeminiInteractionsTransport(Protocol):
    async def create(
        self, request: GeminiInteractionsWireRequest
    ) -> GeminiInteractionsWireResponse: ...


class GeminiTransportError(RuntimeError):
    def __init__(
        self,
        kind: GeminiTransportErrorKind,
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


def _usage_from_response(response: GeminiInteractionsWireResponse) -> ProviderUsageEvidence:
    core = (response.input_tokens, response.output_tokens, response.total_tokens)
    if any(value is None for value in core):
        return _unknown_usage()
    return ProviderUsageEvidence(
        state=ProviderUsageState.KNOWN,
        input_tokens=response.input_tokens,
        output_tokens=response.output_tokens,
        total_tokens=response.total_tokens,
        reasoning_tokens=response.thought_tokens,
        cached_input_tokens=response.cached_tokens,
        tool_use_tokens=response.tool_use_tokens,
    )


def _provider_error_class(kind: GeminiTransportErrorKind) -> ProviderErrorClass:
    mapping = {
        GeminiTransportErrorKind.RATE_LIMIT: ProviderErrorClass.RATE_LIMIT,
        GeminiTransportErrorKind.CONNECTION: ProviderErrorClass.CONNECTION,
        GeminiTransportErrorKind.TIMEOUT: ProviderErrorClass.TIMEOUT,
        GeminiTransportErrorKind.INVALID_REQUEST: ProviderErrorClass.INVALID_REQUEST,
        GeminiTransportErrorKind.AUTHENTICATION: ProviderErrorClass.AUTHENTICATION,
        GeminiTransportErrorKind.PERMISSION: ProviderErrorClass.PERMISSION,
        GeminiTransportErrorKind.NOT_FOUND: ProviderErrorClass.NOT_FOUND,
        GeminiTransportErrorKind.CONFLICT: ProviderErrorClass.CONFLICT,
        GeminiTransportErrorKind.SERVER: ProviderErrorClass.SERVER,
        GeminiTransportErrorKind.INVALID_RESPONSE: ProviderErrorClass.INVALID_RESPONSE,
        GeminiTransportErrorKind.UNKNOWN: ProviderErrorClass.UNKNOWN,
    }
    return mapping[kind]


def _provider_error_outcome(
    kind: GeminiTransportErrorKind,
) -> tuple[ProviderAttemptOutcome, ProviderAcceptanceCertainty]:
    if kind in {GeminiTransportErrorKind.TIMEOUT, GeminiTransportErrorKind.CONNECTION}:
        return ProviderAttemptOutcome.INDETERMINATE, ProviderAcceptanceCertainty.POSSIBLE
    if kind is GeminiTransportErrorKind.INVALID_RESPONSE:
        return ProviderAttemptOutcome.INVALID_RESPONSE, ProviderAcceptanceCertainty.ESTABLISHED
    if kind in {
        GeminiTransportErrorKind.RATE_LIMIT,
        GeminiTransportErrorKind.CONFLICT,
        GeminiTransportErrorKind.SERVER,
    }:
        return ProviderAttemptOutcome.TRANSIENT_FAILURE, ProviderAcceptanceCertainty.ESTABLISHED
    if kind in {
        GeminiTransportErrorKind.INVALID_REQUEST,
        GeminiTransportErrorKind.AUTHENTICATION,
        GeminiTransportErrorKind.PERMISSION,
        GeminiTransportErrorKind.NOT_FOUND,
    }:
        return ProviderAttemptOutcome.PERMANENT_FAILURE, ProviderAcceptanceCertainty.ESTABLISHED
    return ProviderAttemptOutcome.INDETERMINATE, ProviderAcceptanceCertainty.POSSIBLE


class GeminiInteractionsAdapter:
    """Binding-specific native Gemini adapter with DANTE-owned normalization."""

    def __init__(
        self,
        transport: GeminiInteractionsTransport,
        *,
        clock: Callable[[], datetime] = _utc_now,
    ) -> None:
        self._transport = transport
        self._clock = clock

    async def invoke(self, request: ProviderInvocationRequest) -> ProviderAttemptResult:
        started_at = self._clock()
        preflight = self._preflight_error(request, started_at)
        if preflight is not None:
            return preflight

        timeout_seconds = (request.deadline - started_at).total_seconds()
        structured_schema: dict[str, object] | None = None
        if request.structured_output is not None:
            loaded = json.loads(request.structured_output.schema_json)
            if not isinstance(loaded, dict):
                return self._preflight_invalid_request(
                    request,
                    started_at,
                    code="structured_schema_not_object",
                )
            structured_schema = loaded

        if (
            request.provider_endpoint is None
            or request.provider_api_revision is None
            or request.provider_service_tier is None
        ):
            return self._preflight_invalid_request(
                request,
                started_at,
                code="missing_provider_binding_transport_identity",
            )

        wire_request = GeminiInteractionsWireRequest(
            model=request.provider_model,
            endpoint=request.provider_endpoint,
            api_revision=request.provider_api_revision,
            service_tier=request.provider_service_tier,
            input_text=request.rendered_input,
            system_instruction=request.rendered_instructions,
            max_output_tokens=request.max_output_tokens,
            thinking_level=request.reasoning_level or "low",
            timeout_seconds=timeout_seconds,
            structured_output_schema=structured_schema,
        )
        try:
            response = await self._transport.create(wire_request)
        except GeminiTransportError as exc:
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
        admitted = (
            request.provider_binding_ref == GEMINI_INTERACTIONS_BINDING_REF
            and request.provider_model == GEMINI_INTERACTIONS_MODEL
            and request.harness_profile_ref == GEMINI_INTERACTIONS_HARNESS_REF
            and request.route_config_identity.revision == GEMINI_INTERACTIONS_ROUTE_REVISION
            and request.provider_endpoint == GEMINI_INTERACTIONS_ENDPOINT
            and request.provider_api_revision == GEMINI_INTERACTIONS_API_REVISION
            and request.provider_service_tier == GEMINI_INTERACTIONS_SERVICE_TIER
            and request.reasoning_level in _ALLOWED_REASONING_LEVELS
            and frozenset(request.feature_modes) == _REQUIRED_FEATURE_MODES
        )
        if admitted:
            return None
        return ProviderAttemptResult(
            provider_attempt_id=request.provider_attempt_id,
            model_invocation_id=request.model_invocation_id,
            outcome=ProviderAttemptOutcome.UNSUPPORTED_FEATURE,
            acceptance=ProviderAcceptanceCertainty.NOT_ACCEPTED,
            usage=_unknown_usage(),
            started_at=started_at,
            completed_at=started_at,
            error_class=ProviderErrorClass.UNSUPPORTED_FEATURE,
            error_code="binding_protocol_or_feature_mode_not_admitted",
        )

    @staticmethod
    def _preflight_invalid_request(
        request: ProviderInvocationRequest,
        started_at: datetime,
        *,
        code: str,
    ) -> ProviderAttemptResult:
        return ProviderAttemptResult(
            provider_attempt_id=request.provider_attempt_id,
            model_invocation_id=request.model_invocation_id,
            outcome=ProviderAttemptOutcome.PRE_ACCEPTANCE_FAILURE,
            acceptance=ProviderAcceptanceCertainty.NOT_ACCEPTED,
            usage=_unknown_usage(),
            started_at=started_at,
            completed_at=started_at,
            error_class=ProviderErrorClass.INVALID_REQUEST,
            error_code=code,
        )

    def _normalize_response(
        self,
        request: ProviderInvocationRequest,
        response: GeminiInteractionsWireResponse,
        started_at: datetime,
        completed_at: datetime,
    ) -> ProviderAttemptResult:
        usage = _usage_from_response(response)
        provider_status = response.status.value

        if response.model is not None and response.model != request.provider_model:
            return self._invalid_response(
                request,
                response,
                usage,
                started_at,
                completed_at,
                code="provider_model_identity_mismatch",
            )
        if (
            response.service_tier is not None
            and response.service_tier != request.provider_service_tier
        ):
            return self._invalid_response(
                request,
                response,
                usage,
                started_at,
                completed_at,
                code="provider_service_tier_mismatch",
            )

        if response.status is GeminiInteractionStatus.CANCELLED:
            return ProviderAttemptResult(
                provider_attempt_id=request.provider_attempt_id,
                model_invocation_id=request.model_invocation_id,
                outcome=ProviderAttemptOutcome.CANCELLED,
                acceptance=ProviderAcceptanceCertainty.ESTABLISHED,
                usage=usage,
                started_at=started_at,
                completed_at=completed_at,
                provider_request_id=response.request_id,
                provider_response_id=response.interaction_id,
                provider_status=provider_status,
                finish_reason="provider_cancelled",
                error_class=ProviderErrorClass.CANCELLATION,
                error_code=response.error_code or "provider_cancelled",
            )
        if response.status is GeminiInteractionStatus.FAILED:
            return ProviderAttemptResult(
                provider_attempt_id=request.provider_attempt_id,
                model_invocation_id=request.model_invocation_id,
                outcome=ProviderAttemptOutcome.PERMANENT_FAILURE,
                acceptance=ProviderAcceptanceCertainty.ESTABLISHED,
                usage=usage,
                started_at=started_at,
                completed_at=completed_at,
                provider_request_id=response.request_id,
                provider_response_id=response.interaction_id,
                provider_status=provider_status,
                finish_reason="provider_failed",
                error_class=ProviderErrorClass.SERVER,
                error_code=response.error_code or "interaction_failed",
            )
        if response.status in {
            GeminiInteractionStatus.IN_PROGRESS,
            GeminiInteractionStatus.REQUIRES_ACTION,
            GeminiInteractionStatus.QUEUED,
        }:
            return self._invalid_response(
                request,
                response,
                usage,
                started_at,
                completed_at,
                code="unexpected_nonterminal_or_action_status",
            )
        if response.status is GeminiInteractionStatus.BUDGET_EXCEEDED:
            return ProviderAttemptResult(
                provider_attempt_id=request.provider_attempt_id,
                model_invocation_id=request.model_invocation_id,
                outcome=ProviderAttemptOutcome.INCOMPLETE,
                acceptance=ProviderAcceptanceCertainty.ESTABLISHED,
                usage=usage,
                started_at=started_at,
                completed_at=completed_at,
                provider_request_id=response.request_id,
                provider_response_id=response.interaction_id,
                provider_status=provider_status,
                finish_reason="budget_exceeded",
            )
        if response.output_text is None:
            return self._invalid_response(
                request,
                response,
                usage,
                started_at,
                completed_at,
                code="missing_model_output",
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
            if response.status is GeminiInteractionStatus.COMPLETED
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
            provider_response_id=response.interaction_id,
            provider_status=provider_status,
            finish_reason=(
                None
                if response.status is GeminiInteractionStatus.COMPLETED
                else "provider_incomplete"
            ),
            output_text=output_text,
            structured_output_json=structured_output_json,
        )

    @staticmethod
    def _invalid_response(
        request: ProviderInvocationRequest,
        response: GeminiInteractionsWireResponse,
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
            provider_response_id=response.interaction_id,
            provider_status=response.status.value,
            finish_reason=code,
            error_class=ProviderErrorClass.INVALID_RESPONSE,
            error_code=code,
        )
