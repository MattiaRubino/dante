"""Deterministic application-owned ModelAccess runtime.

The runtime resolves one logical ModelTarget to one immutable route snapshot and executes one
provider attempt. Retry/fallback remain deliberately off until independently qualified.
"""

from __future__ import annotations

import asyncio
from collections.abc import Mapping
from contextlib import suppress
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
    ModelAccessErrorClass,
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
from dante.modules.intelligence.ports.model_access import CancellationSignal
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
    if attempt.error_class is ProviderErrorClass.CANCELLATION:
        return ModelInvocationOutcome.CANCELLED
    if attempt.outcome is ProviderAttemptOutcome.INVALID_RESPONSE:
        return ModelInvocationOutcome.INVALID_RESPONSE
    return ModelInvocationOutcome.FAILED


def _model_error_class(attempt: ProviderAttemptResult) -> ModelAccessErrorClass | None:
    if attempt.outcome is ProviderAttemptOutcome.COMPLETED:
        return None
    if attempt.outcome is ProviderAttemptOutcome.INCOMPLETE:
        return ModelAccessErrorClass.PROVIDER_INCOMPLETE
    if attempt.outcome is ProviderAttemptOutcome.REFUSED:
        return ModelAccessErrorClass.REFUSED
    if attempt.error_class is ProviderErrorClass.CANCELLATION:
        return ModelAccessErrorClass.CANCELLATION
    if attempt.outcome is ProviderAttemptOutcome.CANCELLED:
        return ModelAccessErrorClass.CANCELLATION
    if attempt.outcome is ProviderAttemptOutcome.INVALID_RESPONSE:
        return ModelAccessErrorClass.INVALID_RESPONSE
    if attempt.outcome is ProviderAttemptOutcome.INDETERMINATE:
        return ModelAccessErrorClass.INDETERMINATE_EXTERNAL_OUTCOME
    if attempt.outcome is ProviderAttemptOutcome.TRANSIENT_FAILURE:
        return ModelAccessErrorClass.PROVIDER_TRANSIENT
    if attempt.outcome is ProviderAttemptOutcome.PERMANENT_FAILURE:
        return ModelAccessErrorClass.PROVIDER_PERMANENT
    if attempt.error_class is ProviderErrorClass.DEADLINE:
        return ModelAccessErrorClass.DEADLINE_EXCEEDED
    if attempt.error_class is ProviderErrorClass.UNSUPPORTED_FEATURE:
        return ModelAccessErrorClass.CAPABILITY_UNAVAILABLE
    if attempt.error_class is ProviderErrorClass.INVALID_REQUEST:
        return ModelAccessErrorClass.INVALID_REQUEST
    return ModelAccessErrorClass.UNKNOWN


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
        RuntimeEvidenceMetric(name=name, value=value) for name, value in values if value is not None
    )


def _synthetic_attempt(
    request: ModelInvocationRequest,
    *,
    started_at: datetime,
    outcome: ProviderAttemptOutcome,
    acceptance: ProviderAcceptanceCertainty,
    error_class: ProviderErrorClass,
    error_code: str,
) -> ProviderAttemptResult:
    return ProviderAttemptResult(
        provider_attempt_id=uuid7(),
        model_invocation_id=request.model_invocation_id,
        outcome=outcome,
        acceptance=acceptance,
        usage=_unknown_usage(),
        started_at=started_at,
        completed_at=_utc_now(),
        error_class=error_class,
        error_code=error_code,
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

    def _pre_dispatch_result(
        self,
        request: ModelInvocationRequest,
        *,
        started_at: datetime,
        outcome: ModelInvocationOutcome,
        error_class: ModelAccessErrorClass,
        error_code: str,
        binding: ProviderBindingDefinition | None = None,
        harness: HarnessProfileDefinition | None = None,
        attempt: ProviderAttemptResult | None = None,
    ) -> ModelInvocationResult:
        return ModelInvocationResult(
            model_invocation_id=request.model_invocation_id,
            target=request.target,
            outcome=outcome,
            route_config_identity=self._route_config.identity,
            usage=attempt.usage if attempt is not None else _unknown_usage(),
            provider_binding_ref=binding.ref if binding is not None else None,
            harness_profile_ref=harness.ref if harness is not None else None,
            provider_model=binding.model if binding is not None else None,
            attempts=(attempt,) if attempt is not None else (),
            error_class=error_class,
            error_code=error_code,
            started_at=started_at,
            completed_at=attempt.completed_at if attempt is not None else _utc_now(),
        )

    async def _execute_attempt(
        self,
        *,
        request: ModelInvocationRequest,
        provider_request: ProviderInvocationRequest,
        adapter: ProviderAdapter,
        cancellation: CancellationSignal | None,
    ) -> ProviderAttemptResult:
        dispatched_at = _utc_now()
        remaining_seconds = (provider_request.deadline - dispatched_at).total_seconds()
        if remaining_seconds <= 0:
            return _synthetic_attempt(
                request,
                started_at=dispatched_at,
                outcome=ProviderAttemptOutcome.PRE_ACCEPTANCE_FAILURE,
                acceptance=ProviderAcceptanceCertainty.NOT_ACCEPTED,
                error_class=ProviderErrorClass.DEADLINE,
                error_code="deadline_before_provider_dispatch",
            )
        if cancellation is not None and cancellation.cancelled:
            return _synthetic_attempt(
                request,
                started_at=dispatched_at,
                outcome=ProviderAttemptOutcome.PRE_ACCEPTANCE_FAILURE,
                acceptance=ProviderAcceptanceCertainty.NOT_ACCEPTED,
                error_class=ProviderErrorClass.CANCELLATION,
                error_code="cancelled_before_provider_dispatch",
            )

        provider_task = asyncio.create_task(adapter.invoke(provider_request))
        cancellation_task: asyncio.Task[None] | None = None
        if cancellation is not None:
            cancellation_task = asyncio.create_task(cancellation.wait())

        wait_set: set[asyncio.Task[object]] = {provider_task}
        if cancellation_task is not None:
            wait_set.add(cancellation_task)
        done, pending = await asyncio.wait(
            wait_set,
            timeout=remaining_seconds,
            return_when=asyncio.FIRST_COMPLETED,
        )

        if provider_task in done:
            if cancellation_task is not None:
                cancellation_task.cancel()
                with suppress(asyncio.CancelledError):
                    await cancellation_task
            return provider_task.result()

        provider_task.cancel()
        with suppress(asyncio.CancelledError):
            await provider_task
        for task in pending:
            task.cancel()
        for task in pending:
            with suppress(asyncio.CancelledError):
                await task

        if cancellation_task is not None and cancellation_task in done:
            return _synthetic_attempt(
                request,
                started_at=dispatched_at,
                outcome=ProviderAttemptOutcome.CANCELLED,
                acceptance=ProviderAcceptanceCertainty.POSSIBLE,
                error_class=ProviderErrorClass.CANCELLATION,
                error_code="local_cancellation_after_dispatch_acceptance_unknown",
            )

        return _synthetic_attempt(
            request,
            started_at=dispatched_at,
            outcome=ProviderAttemptOutcome.INDETERMINATE,
            acceptance=ProviderAcceptanceCertainty.POSSIBLE,
            error_class=ProviderErrorClass.TIMEOUT,
            error_code="modelaccess_deadline_after_dispatch_acceptance_unknown",
        )

    async def invoke(
        self,
        request: ModelInvocationRequest,
        cancellation: CancellationSignal | None = None,
    ) -> ModelInvocationResult:
        """Execute one champion attempt; fallback/retry remain intentionally disabled."""
        invocation_started_at = _utc_now()

        if cancellation is not None and cancellation.cancelled:
            attempt = _synthetic_attempt(
                request,
                started_at=invocation_started_at,
                outcome=ProviderAttemptOutcome.PRE_ACCEPTANCE_FAILURE,
                acceptance=ProviderAcceptanceCertainty.NOT_ACCEPTED,
                error_class=ProviderErrorClass.CANCELLATION,
                error_code="cancelled_before_model_routing",
            )
            return self._pre_dispatch_result(
                request,
                started_at=invocation_started_at,
                outcome=ModelInvocationOutcome.CANCELLED,
                error_class=ModelAccessErrorClass.CANCELLATION,
                error_code="cancelled_before_model_routing",
                attempt=attempt,
            )

        if request.max_provider_attempts != 1:
            return self._pre_dispatch_result(
                request,
                started_at=invocation_started_at,
                outcome=ModelInvocationOutcome.INVALID_REQUEST,
                error_class=ModelAccessErrorClass.INVALID_REQUEST,
                error_code="retry_budget_not_supported_by_route",
            )

        route_requirement_error = self._preflight_route_requirement_error(request)
        if route_requirement_error is not None:
            return self._pre_dispatch_result(
                request,
                started_at=invocation_started_at,
                outcome=ModelInvocationOutcome.INVALID_REQUEST,
                error_class=ModelAccessErrorClass.ROUTE_MISMATCH,
                error_code=route_requirement_error,
            )

        if request.structured_output is not None:
            try:
                validate_contract_schema(request.structured_output)
            except StructuredOutputValidationError as exc:
                return self._pre_dispatch_result(
                    request,
                    started_at=invocation_started_at,
                    outcome=ModelInvocationOutcome.INVALID_REQUEST,
                    error_class=ModelAccessErrorClass.INVALID_REQUEST,
                    error_code=str(exc),
                )

        route = self._route(request.target.value)
        if route is None or route.state is not RouteTargetState.ACTIVE:
            return self._pre_dispatch_result(
                request,
                started_at=invocation_started_at,
                outcome=ModelInvocationOutcome.UNAVAILABLE,
                error_class=ModelAccessErrorClass.CAPABILITY_UNAVAILABLE,
                error_code="model_target_not_active",
            )

        if route.champion_binding_ref is None or route.harness_profile_ref is None:
            raise RuntimeError("validated active route is missing champion binding or harness")

        binding = self._binding(route.champion_binding_ref)
        harness = self._harness(route.harness_profile_ref)

        required_capabilities = set(request.required_capabilities)
        if request.structured_output is not None:
            required_capabilities.add("structured_output")
        if not required_capabilities.issubset(binding.capabilities):
            return self._pre_dispatch_result(
                request,
                started_at=invocation_started_at,
                outcome=ModelInvocationOutcome.UNAVAILABLE,
                error_class=ModelAccessErrorClass.CAPABILITY_UNAVAILABLE,
                error_code="required_capability_not_available",
                binding=binding,
                harness=harness,
            )
        if not set(request.required_feature_modes).issubset(harness.feature_modes):
            return self._pre_dispatch_result(
                request,
                started_at=invocation_started_at,
                outcome=ModelInvocationOutcome.UNAVAILABLE,
                error_class=ModelAccessErrorClass.CAPABILITY_UNAVAILABLE,
                error_code="required_feature_mode_not_available",
                binding=binding,
                harness=harness,
            )

        adapter = self._adapters.get(binding.ref)
        if binding.state is ProviderBindingState.INACTIVE or adapter is None:
            return self._pre_dispatch_result(
                request,
                started_at=invocation_started_at,
                outcome=ModelInvocationOutcome.UNAVAILABLE,
                error_class=ModelAccessErrorClass.CAPABILITY_UNAVAILABLE,
                error_code="champion_binding_not_available",
                binding=binding,
                harness=harness,
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

        attempt = await self._execute_attempt(
            request=request,
            provider_request=provider_request,
            adapter=adapter,
            cancellation=cancellation,
        )
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
        if attempt.acceptance is ProviderAcceptanceCertainty.POSSIBLE:
            limitation_codes.append("provider-acceptance:possible")

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
            output_text=attempt.output_text
            if outcome is ModelInvocationOutcome.COMPLETED
            else None,
            structured_output_json=(
                attempt.structured_output_json
                if outcome is ModelInvocationOutcome.COMPLETED
                else None
            ),
            error_class=_model_error_class(attempt),
            error_code=attempt.error_code,
            finish_reason=attempt.finish_reason,
            started_at=invocation_started_at,
            completed_at=attempt.completed_at,
        )
