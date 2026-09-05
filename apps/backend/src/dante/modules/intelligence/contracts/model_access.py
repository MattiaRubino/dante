"""Provider-neutral ModelAccess, ModelInvocation and ProviderAttempt contracts."""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from uuid import UUID

from dante.modules.intelligence.contracts.route_config import RouteConfigIdentity


class ModelTarget(StrEnum):
    """Logical cognition targets owned by DANTE rather than any provider."""

    STRUCTURED_INTERPRETATION = "structured_interpretation"
    GENERAL_REASONING = "general_reasoning"
    DEEP_REASONING = "deep_reasoning"


class ModelInvocationOutcome(StrEnum):
    """Logical model-invocation outcome after DANTE routing and validation."""

    COMPLETED = "completed"
    INCOMPLETE = "incomplete"
    REFUSED = "refused"
    FAILED = "failed"
    CANCELLED = "cancelled"
    INVALID_REQUEST = "invalid_request"
    INVALID_RESPONSE = "invalid_response"
    UNAVAILABLE = "unavailable"


class ProviderAttemptOutcome(StrEnum):
    """Normalized provider-attempt outcome independent of publication maturity."""

    COMPLETED = "completed"
    INCOMPLETE = "incomplete"
    REFUSED = "refused"
    PRE_ACCEPTANCE_FAILURE = "pre_acceptance_failure"
    TRANSIENT_FAILURE = "transient_failure"
    PERMANENT_FAILURE = "permanent_failure"
    INDETERMINATE = "indeterminate"
    CANCELLED = "cancelled"
    INVALID_RESPONSE = "invalid_response"
    UNSUPPORTED_FEATURE = "unsupported_feature"


class ProviderAcceptanceCertainty(StrEnum):
    """What DANTE can establish about provider acceptance/processing."""

    NOT_ACCEPTED = "not_accepted"
    POSSIBLE = "possible"
    ESTABLISHED = "established"


class ProviderUsageState(StrEnum):
    """Evidence state for provider usage; UNKNOWN is never zero."""

    KNOWN = "known"
    ESTIMATED = "estimated"
    UNKNOWN = "unknown"
    LATE = "late"


class ProviderErrorClass(StrEnum):
    """Provider-neutral classified failure surface for routing/runtime policy."""

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
    CANCELLATION = "cancellation"
    DEADLINE = "deadline"
    UNSUPPORTED_FEATURE = "unsupported_feature"
    UNKNOWN = "unknown"


def _require_text(value: str, *, name: str) -> None:
    if not value or not value.strip():
        raise ValueError(f"{name} must be non-empty")


def _require_texts(values: tuple[str, ...], *, name: str) -> None:
    if any(not value or not value.strip() for value in values):
        raise ValueError(f"{name} entries must be non-empty")
    if len(values) != len(set(values)):
        raise ValueError(f"{name} entries must be unique")


def _require_uuid7(value: UUID, *, name: str) -> None:
    if value.version != 7:
        raise ValueError(f"{name} must be UUIDv7")


def _require_aware(value: datetime, *, name: str) -> None:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError(f"{name} must be timezone-aware")


@dataclass(frozen=True, slots=True)
class StructuredOutputContract:
    """Provider-neutral JSON-schema transport contract, not Domain meaning."""

    name: str
    schema_json: str
    strict: bool = True

    def __post_init__(self) -> None:
        _require_text(self.name, name="name")
        _require_text(self.schema_json, name="schema_json")
        try:
            document = json.loads(self.schema_json)
        except json.JSONDecodeError as exc:
            raise ValueError("schema_json must contain valid JSON") from exc
        if not isinstance(document, dict):
            raise ValueError("schema_json must contain a JSON object schema")


@dataclass(frozen=True, slots=True)
class ModelInvocationRequest:
    """Provider-neutral logical cognition request supplied to ModelAccess."""

    model_invocation_id: UUID
    work_id: UUID
    work_revision: int
    target: ModelTarget
    purpose: str
    input_text: str
    deadline: datetime
    max_output_tokens: int
    instructions: str | None = None
    structured_output: StructuredOutputContract | None = None
    security_basis_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        _require_uuid7(self.model_invocation_id, name="model_invocation_id")
        _require_uuid7(self.work_id, name="work_id")
        if self.work_revision <= 0:
            raise ValueError("work_revision must be positive")
        _require_text(self.purpose, name="purpose")
        _require_text(self.input_text, name="input_text")
        if self.instructions is not None:
            _require_text(self.instructions, name="instructions")
        _require_aware(self.deadline, name="deadline")
        if self.max_output_tokens <= 0:
            raise ValueError("max_output_tokens must be positive")
        _require_texts(self.security_basis_refs, name="security_basis_refs")


@dataclass(frozen=True, slots=True)
class ProviderInvocationRequest:
    """Exact DANTE-owned provider attempt request after routing/harness binding."""

    provider_attempt_id: UUID
    model_invocation_id: UUID
    work_id: UUID
    work_revision: int
    provider_binding_ref: str
    model_target_ref: str
    provider_model: str
    harness_profile_ref: str
    purpose: str
    rendered_input: str
    deadline: datetime
    max_output_tokens: int
    route_config_identity: RouteConfigIdentity
    rendered_instructions: str | None = None
    structured_output: StructuredOutputContract | None = None
    reasoning_level: str | None = None
    feature_modes: tuple[str, ...] = ()
    security_basis_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        for name, uuid_value in (
            ("provider_attempt_id", self.provider_attempt_id),
            ("model_invocation_id", self.model_invocation_id),
            ("work_id", self.work_id),
        ):
            _require_uuid7(uuid_value, name=name)
        if self.work_revision <= 0:
            raise ValueError("work_revision must be positive")
        for name, text_value in (
            ("provider_binding_ref", self.provider_binding_ref),
            ("model_target_ref", self.model_target_ref),
            ("provider_model", self.provider_model),
            ("harness_profile_ref", self.harness_profile_ref),
            ("purpose", self.purpose),
            ("rendered_input", self.rendered_input),
        ):
            _require_text(text_value, name=name)
        if self.rendered_instructions is not None:
            _require_text(self.rendered_instructions, name="rendered_instructions")
        if self.reasoning_level is not None:
            _require_text(self.reasoning_level, name="reasoning_level")
        _require_aware(self.deadline, name="deadline")
        if self.max_output_tokens <= 0:
            raise ValueError("max_output_tokens must be positive")
        _require_texts(self.feature_modes, name="feature_modes")
        _require_texts(self.security_basis_refs, name="security_basis_refs")


@dataclass(frozen=True, slots=True)
class ProviderUsageEvidence:
    """Provider usage evidence with explicit detailed-token and unknown semantics."""

    state: ProviderUsageState
    input_tokens: int | None = None
    output_tokens: int | None = None
    total_tokens: int | None = None
    reasoning_tokens: int | None = None
    cached_input_tokens: int | None = None
    tool_use_tokens: int | None = None

    def __post_init__(self) -> None:
        values = (
            self.input_tokens,
            self.output_tokens,
            self.total_tokens,
            self.reasoning_tokens,
            self.cached_input_tokens,
            self.tool_use_tokens,
        )
        if any(value is not None and value < 0 for value in values):
            raise ValueError("provider usage token counts must not be negative")
        if self.state in {ProviderUsageState.KNOWN, ProviderUsageState.ESTIMATED}:
            if any(
                value is None
                for value in (self.input_tokens, self.output_tokens, self.total_tokens)
            ):
                raise ValueError("known/estimated provider usage requires core token counts")
            return
        if any(value is not None for value in values):
            raise ValueError("unknown/late provider usage must not fabricate token counts")


@dataclass(frozen=True, slots=True)
class ProviderAttemptResult:
    """Normalized attempt evidence; provider completion is not DANTE verification/publication."""

    provider_attempt_id: UUID
    model_invocation_id: UUID
    outcome: ProviderAttemptOutcome
    acceptance: ProviderAcceptanceCertainty
    usage: ProviderUsageEvidence
    started_at: datetime
    completed_at: datetime
    provider_request_id: str | None = None
    provider_response_id: str | None = None
    output_text: str | None = None
    structured_output_json: str | None = None
    refusal_reason: str | None = None
    error_class: ProviderErrorClass | None = None
    error_code: str | None = None

    def __post_init__(self) -> None:
        _require_uuid7(self.provider_attempt_id, name="provider_attempt_id")
        _require_uuid7(self.model_invocation_id, name="model_invocation_id")
        _require_aware(self.started_at, name="started_at")
        _require_aware(self.completed_at, name="completed_at")
        if self.completed_at < self.started_at:
            raise ValueError("completed_at must not precede started_at")
        for name, value in (
            ("provider_request_id", self.provider_request_id),
            ("provider_response_id", self.provider_response_id),
            ("output_text", self.output_text),
            ("structured_output_json", self.structured_output_json),
            ("refusal_reason", self.refusal_reason),
            ("error_code", self.error_code),
        ):
            if value is not None:
                _require_text(value, name=name)

        has_output = self.output_text is not None or self.structured_output_json is not None
        if self.outcome is ProviderAttemptOutcome.COMPLETED:
            if self.acceptance is not ProviderAcceptanceCertainty.ESTABLISHED:
                raise ValueError("COMPLETED requires ESTABLISHED provider acceptance")
            if not has_output:
                raise ValueError("COMPLETED requires provider output")
            if self.error_class is not None or self.refusal_reason is not None:
                raise ValueError("COMPLETED cannot carry provider error/refusal state")
            return

        if self.outcome is ProviderAttemptOutcome.INCOMPLETE:
            if self.acceptance is not ProviderAcceptanceCertainty.ESTABLISHED:
                raise ValueError("INCOMPLETE requires ESTABLISHED provider acceptance")
            if self.refusal_reason is not None:
                raise ValueError("INCOMPLETE cannot carry refusal state")
            return

        if self.outcome is ProviderAttemptOutcome.REFUSED:
            if self.acceptance is not ProviderAcceptanceCertainty.ESTABLISHED:
                raise ValueError("REFUSED requires ESTABLISHED provider acceptance")
            if self.refusal_reason is None:
                raise ValueError("REFUSED requires refusal_reason")
            if self.error_class is not None or has_output:
                raise ValueError("REFUSED cannot carry provider error/output state")
            return

        if self.outcome in {
            ProviderAttemptOutcome.PRE_ACCEPTANCE_FAILURE,
            ProviderAttemptOutcome.UNSUPPORTED_FEATURE,
        }:
            if self.acceptance is not ProviderAcceptanceCertainty.NOT_ACCEPTED:
                raise ValueError("pre-acceptance outcomes require NOT_ACCEPTED certainty")
        elif self.outcome is ProviderAttemptOutcome.INDETERMINATE:
            if self.acceptance is not ProviderAcceptanceCertainty.POSSIBLE:
                raise ValueError("INDETERMINATE requires POSSIBLE provider acceptance")
        elif self.acceptance is ProviderAcceptanceCertainty.NOT_ACCEPTED:
            raise ValueError("post-dispatch outcome cannot claim NOT_ACCEPTED certainty")

        if self.error_class is None:
            raise ValueError("failure provider outcome requires error_class")
        if has_output or self.refusal_reason is not None:
            raise ValueError("failure provider outcome cannot carry output/refusal state")


@dataclass(frozen=True, slots=True)
class ModelInvocationResult:
    """Logical invocation result after deterministic routing and DANTE validation."""

    model_invocation_id: UUID
    target: ModelTarget
    outcome: ModelInvocationOutcome
    route_config_identity: RouteConfigIdentity
    usage: ProviderUsageEvidence
    provider_binding_ref: str | None = None
    harness_profile_ref: str | None = None
    attempts: tuple[ProviderAttemptResult, ...] = ()
    output_text: str | None = None
    structured_output_json: str | None = None
    error_code: str | None = None

    def __post_init__(self) -> None:
        _require_uuid7(self.model_invocation_id, name="model_invocation_id")
        for name, value in (
            ("provider_binding_ref", self.provider_binding_ref),
            ("harness_profile_ref", self.harness_profile_ref),
            ("output_text", self.output_text),
            ("structured_output_json", self.structured_output_json),
            ("error_code", self.error_code),
        ):
            if value is not None:
                _require_text(value, name=name)
        if any(attempt.model_invocation_id != self.model_invocation_id for attempt in self.attempts):
            raise ValueError("all provider attempts must belong to this model invocation")

        has_output = self.output_text is not None or self.structured_output_json is not None
        if self.outcome is ModelInvocationOutcome.COMPLETED:
            if not self.attempts or not has_output:
                raise ValueError("completed model invocation requires attempt and output")
            if self.provider_binding_ref is None or self.harness_profile_ref is None:
                raise ValueError("completed model invocation requires selected route identity")
            return

        if self.outcome in {
            ModelInvocationOutcome.INVALID_REQUEST,
            ModelInvocationOutcome.UNAVAILABLE,
        }:
            if self.attempts or has_output:
                raise ValueError("pre-dispatch model outcome cannot carry attempt/output")
            return

        if not self.attempts:
            raise ValueError("post-dispatch model outcome requires provider attempt evidence")
