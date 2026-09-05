"""Deterministic application-owned ModelAccess runtime.

The runtime resolves one logical ModelTarget to one immutable route snapshot and executes one
provider attempt. Retry/fallback remain deliberately off until independently qualified.
"""

from __future__ import annotations

from collections.abc import Mapping
from datetime import UTC, datetime, timedelta
from uuid import uuid7

from dante.modules.intelligence.application.structured_output import (
    StructuredOutputValidationError,
    validate_contract_schema,
    validate_structured_output,
)
from dante.modules.intelligence.contracts.evidence import (
    RuntimeEvidenceEvent,
    RuntimeEvidenceKind,
    RuntimeEvidenceMetric,
)
from dante.modules.intelligence.contracts.model_access import (
    ModelInvocationOutcome,
    ModelInvocationRequest,
    ModelInvocationResult,
    ProviderAcceptanceCertainty,
    ProviderAttemptOutcome,
    ProviderAttemptResult,
    ProviderErrorClass,
    ProviderInvocationRequest,
    ProviderUsageEvidence,
    ProviderUsageState,
)
from dante.modules.intelligence.contracts.route_config import (
    HarnessProfileDefinition,
    ProviderBindingDefinition,
    ProviderBindingState,
    RouteConfigSnapshot,
    RouteTargetState,
    TargetRouteDefinition,
)
from dante.modules.intelligence.ports.provider_adapter import ProviderAdapter
from dante.modules.intelligence.ports.runtime_evidence import RuntimeEvidencePort


def _utc_now() -> datetime:
    return datetime.now(UTC)


def _unknown_usage() -> ProviderUsageEvidence:
    return ProviderUsageEvidence(state=ProviderUsageState.UNKNOWN)


def _model_outcome(attempt: ProviderAttemptResult) -> ModelInvocationOutcome:
    if attempt.outcome is ProviderAttemptOutcome.COMPLETED:
        return ModelInvocationOutcome.COMPLETED
    if attempt.outcome is ProviderAttemptOutcome.INCOMPLETE:
        return ModelInvocationOutcome.INCOMPLETE
    if attempt.outcome is ProviderAttemptOutcome.REFUSED:
        return ModelInvocationOutcome.REFUSED
    if attempt.outcome is ProviderAttemptOutcome.CANCELLED:
        return ModelInvocationOutcome.CANCELLED
    if attempt.outcome is ProviderAttemptOutcome.INVALID_RESPONSE:
        return ModelInvocationOutcome.INVALID_RESPONSE
    return ModelInvocationOutcome.FAILED


def _usage_metrics(usage: ProviderUsageEvidence) -> tuple[RuntimeEvidenceMetric, ...]:
    values = (
        ("input_tokens", usage.input_tokens),
        ("output_tokens", usage.output_tokens),
        ("reasoning_tokens", usage.reasoning_tokens),
        ("cached_input_tokens", usage.cached_input_tokens),
        ("tool_use_tokens", usage.tool_use_tokens),
        ("total_tokens", usage.total_tokens),
    )
    return tuple(
        RuntimeEvidenceMetric(name=name, value=value)
        for name, value in values
        if value is not None
    )


class ModelAccessRuntime:
    """Resolve configured model targets without exposing provider semantics to callers."""

    def __init__(
        self,
        route_config: RouteConfigSnapshot,
        adapters: Mapping[str, ProviderAdapter],
        *,
        evidence: RuntimeEvidencePort | None = None,
    ) -> None:
        if route_config.document.schema_version < 2:
            raise ValueError("ModelAccessRuntime requires a typed route config")
        self._route_config = route_config
        self._adapters = dict(adapters)
        self._evidence = evidence

    @property
    def route_config(self) -> RouteConfigSnapshot:
        """Expose the immutable route snapshot identity, never mutable provider policy."""
        return self._route_config

    def _route(self, target_ref: str) -> TargetRouteDefinition | None:
        return next(
            (
                route
                for route in self._route_config.document.target_routes
                if route.target_ref == target_ref
            ),
            None,
        )

    def _harness(self, ref: str) -> HarnessProfileDefinition:
        return next(
            profile
            for profile in self._route_config.document.harness_definitions
            if profile.ref == ref
        )

    def _binding(self, ref: str) -> ProviderBindingDefinition:
        return next(
            binding
            for binding in self._route_config.document.provider_binding_definitions
            if binding.ref == ref
        )

    async def _emit(self, event: RuntimeEvidenceEvent) -> None:
        if self._evidence is not None:
            await self._evidence.emit(event)

    def _preflight_route_requirement_error(self, request: ModelInvocationRequest) -> str | None:
        required_identity = request.required_route_config_identity
        if required_identity is not None and required_identity != self._route_config.identity:
            return "required_route_config_identity_mismatch"
        return None

    async def invoke(self, request: ModelInvocationRequest) -> ModelInvocationResult:
        """Execute one champion attempt; fallback/retry remain intentionally disabled."""
        route_requirement_error = self._preflight_route_requirement_error(request)
        if route_requirement_error is not None:
            return ModelInvocationResult(
                model_invocation_id=request.model_invocation_id,
                target=request.target,
                outcome=ModelInvocationOutcome.INVALID_REQUEST,
                route_config_identity=self._route_config.identity,
                usage=_unknown_usage(),
                error_code=route_requirement_error,
            )

        if request.structured_output is not None:
            try:
                validate_contract_schema(request.structured_output)
            except StructuredOutputValidationError as exc:
                return ModelInvocationResult(
                    model_invocation_id=request.model_invocation_id,
                    target=request.target,
                    outcome=ModelInvocationOutcome.INVALID_REQUEST,
                    route_config_identity=self._route_config.identity,
                    usage=_unknown_usage(),
                    error_code=str(exc),
                )

        route = self._route(request.target.value)
        if route is None or route.state is not RouteTargetState.ACTIVE:
            return ModelInvocationResult(
                model_invocation_id=request.model_invocation_id,
                target=request.target,
                outcome=ModelInvocationOutcome.UNAVAILABLE,
                route_config_identity=self._route_config.identity,
                usage=_unknown_usage(),
                error_code="model_target_not_active",
            )

        assert route.champion_binding_ref is not None
        assert route.harness_profile_ref is not None
        binding = self._binding(route.champion_binding_ref)
        harness = self._harness(route.harness_profile_ref)

        required_capabilities = set(request.required_capabilities)
        if request.structured_output is not None:
            required_capabilities.add("structured_output")
        if not required_capabilities.issubset(binding.capabilities):
            return ModelInvocationResult(
                model_invocation_id=request.model_invocation_id,
                target=request.target,
                outcome=ModelInvocationOutcome.UNAVAILABLE,
                route_config_identity=self._route_config.identity,
                usage=_unknown_usage(),
                provider_binding_ref=binding.ref,
                harness_profile_ref=harness.ref,
                provider_model=binding.model,
                error_code="required_capability_not_available",
            )
        if not set(request.required_feature_modes).issubset(harness.feature_modes):
            return ModelInvocationResult(
                model_invocation_id=request.model_invocation_id,
                target=request.target,
                outcome=ModelInvocationOutcome.UNAVAILABLE,
                route_config_identity=self._route_config.identity,
                usage=_unknown_usage(),
                provider_binding_ref=binding.ref,
                harness_profile_ref=harness.ref,
                provider_model=binding.model,
                error_code="required_feature_mode_not_available",
            )

        adapter = self._adapters.get(binding.ref)
        if binding.state is ProviderBindingState.INACTIVE or adapter is None:
            return ModelInvocationResult(
                model_invocation_id=request.model_invocation_id,
                target=request.target,
                outcome=ModelInvocationOutcome.UNAVAILABLE,
                route_config_identity=self._route_config.identity,
                usage=_unknown_usage(),
                provider_binding_ref=binding.ref,
                harness_profile_ref=harness.ref,
                provider_model=binding.model,
                error_code="champion_binding_not_available",
            )

        now = _utc_now()
        effective_deadline = min(
            request.deadline,
            now + timedelta(seconds=harness.timeout_seconds),
        )
        provider_request = ProviderInvocationRequest(
            provider_attempt_id=uuid7(),
            model_invocation_id=request.model_invocation_id,
            work_id=request.work_id,
            work_revision=request.work_revision,
            provider_binding_ref=binding.ref,
            model_target_ref=request.target.value,
            provider_model=binding.model,
            harness_profile_ref=harness.ref,
            purpose=request.purpose,
            rendered_input=request.input_text,
            rendered_instructions=request.instructions,
            deadline=effective_deadline,
            max_output_tokens=min(request.max_output_tokens, harness.max_output_tokens),
            route_config_identity=self._route_config.identity,
            structured_output=request.structured_output,
            reasoning_level=harness.reasoning_level.value,
            feature_modes=harness.feature_modes,
            security_basis_refs=request.security_basis_refs,
            provider_endpoint=binding.endpoint,
            provider_api_revision=binding.api_revision,
            provider_service_tier=binding.service_tier,
        )

        route_refs = [
            f"model-invocation:{request.model_invocation_id}",
            f"target:{request.target.value}",
            f"route:{self._route_config.identity.revision}",
            f"route-sha256:{self._route_config.identity.content_sha256}",
            f"binding:{binding.ref}",
            f"harness:{harness.ref}",
            f"provider-model:{binding.model}",
        ]
        for name, value in (
            ("api-revision", binding.api_revision),
            ("service-tier", binding.service_tier),
            ("versioning", binding.versioning_posture),
            ("data-zone", binding.data_zone),
            ("retention-mode", binding.retention_mode),
        ):
            if value is not None:
                route_refs.append(f"{name}:{value}")

        await self._emit(
            RuntimeEvidenceEvent(
                event_id=uuid7(),
                work_id=request.work_id,
                work_revision=request.work_revision,
                kind=RuntimeEvidenceKind.ROUTE,
                outcome_code="champion_selected",
                occurred_at=now,
                correlation_refs=tuple(route_refs),
            )
        )

        attempt = await adapter.invoke(provider_request)
        if (
            attempt.outcome is ProviderAttemptOutcome.COMPLETED
            and request.structured_output is not None
            and attempt.structured_output_json is not None
        ):
            try:
                validate_structured_output(
                    request.structured_output,
                    attempt.structured_output_json,
                )
            except StructuredOutputValidationError:
                attempt = ProviderAttemptResult(
                    provider_attempt_id=attempt.provider_attempt_id,
                    model_invocation_id=attempt.model_invocation_id,
                    outcome=ProviderAttemptOutcome.INVALID_RESPONSE,
                    acceptance=ProviderAcceptanceCertainty.ESTABLISHED,
                    usage=attempt.usage,
                    started_at=attempt.started_at,
                    completed_at=attempt.completed_at,
                    provider_request_id=attempt.provider_request_id,
                    provider_response_id=attempt.provider_response_id,
                    provider_status=attempt.provider_status,
                    finish_reason=attempt.finish_reason,
                    error_class=ProviderErrorClass.INVALID_RESPONSE,
                    error_code="structured_output_schema_mismatch",
                )

        latency_ms = max(
            0,
            int((attempt.completed_at - attempt.started_at).total_seconds() * 1000),
        )
        limitation_codes: list[str] = []
        if attempt.usage.state is ProviderUsageState.UNKNOWN:
            limitation_codes.append("usage:unknown")
        if attempt.finish_reason is not None:
            limitation_codes.append(f"finish:{attempt.finish_reason}")

        await self._emit(
            RuntimeEvidenceEvent(
                event_id=uuid7(),
                work_id=request.work_id,
                work_revision=request.work_revision,
                kind=RuntimeEvidenceKind.PROVIDER_ATTEMPT,
                outcome_code=attempt.outcome.value,
                occurred_at=attempt.completed_at,
                correlation_refs=tuple(
                    ref
                    for ref in (
                        f"model-invocation:{request.model_invocation_id}",
                        f"provider-attempt:{attempt.provider_attempt_id}",
                        f"binding:{binding.ref}",
                        f"harness:{harness.ref}",
                        f"provider-request:{attempt.provider_request_id}"
                        if attempt.provider_request_id is not None
                        else None,
                        f"provider-response:{attempt.provider_response_id}"
                        if attempt.provider_response_id is not None
                        else None,
                        f"provider-status:{attempt.provider_status}"
                        if attempt.provider_status is not None
                        else None,
                    )
                    if ref is not None
                ),
                limitation_codes=tuple(limitation_codes),
                metrics=(
                    RuntimeEvidenceMetric(name="latency_ms", value=latency_ms),
                    *_usage_metrics(attempt.usage),
                ),
            )
        )

        outcome = _model_outcome(attempt)
        return ModelInvocationResult(
            model_invocation_id=request.model_invocation_id,
            target=request.target,
            outcome=outcome,
            route_config_identity=self._route_config.identity,
            usage=attempt.usage,
            provider_binding_ref=binding.ref,
            harness_profile_ref=harness.ref,
            provider_model=binding.model,
            attempts=(attempt,),
            output_text=attempt.output_text if outcome is ModelInvocationOutcome.COMPLETED else None,
            structured_output_json=(
                attempt.structured_output_json
                if outcome is ModelInvocationOutcome.COMPLETED
                else None
            ),
            error_code=attempt.error_code,
        )
