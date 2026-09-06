"""Unit acceptance for deterministic ModelAccess routing, validation and evidence."""

from __future__ import annotations

import asyncio
from datetime import UTC, datetime, timedelta
from pathlib import Path
from uuid import uuid7

import pytest

from dante.modules.intelligence.adapters.outbound.model.gemini_interactions import (
    GEMINI_INTERACTIONS_API_REVISION,
    GEMINI_INTERACTIONS_BINDING_REF,
    GEMINI_INTERACTIONS_ENDPOINT,
    GEMINI_INTERACTIONS_MODEL,
    GEMINI_INTERACTIONS_ROUTE_REVISION,
    GEMINI_INTERACTIONS_SERVICE_TIER,
)
from dante.modules.intelligence.application.model_access import ModelAccessRuntime
from dante.modules.intelligence.contracts.model_access import (
    ModelAccessErrorClass,
    ModelInvocationOutcome,
    ModelInvocationRequest,
    ModelTarget,
    ProviderAcceptanceCertainty,
    ProviderAttemptOutcome,
    ProviderAttemptResult,
    ProviderInvocationRequest,
    ProviderUsageEvidence,
    ProviderUsageState,
    StructuredOutputContract,
)
from dante.modules.intelligence.contracts.route_config import (
    RouteConfigIdentity,
    RouteConfigSnapshot,
)
from dante.modules.intelligence.route_config import load_route_config
from tests.unit.modules.intelligence.fakes import RecordingRuntimeEvidencePort

_BACKEND_ROOT = Path(__file__).resolve().parents[4]
_REVISIONS_ROOT = _BACKEND_ROOT / "config" / "intelligence" / "revisions"


class _CompletedAdapter:
    def __init__(self, payload: str = '{"decision":"ok"}') -> None:
        self.payload = payload
        self.requests: list[ProviderInvocationRequest] = []

    async def invoke(self, request: ProviderInvocationRequest) -> ProviderAttemptResult:
        self.requests.append(request)
        now = datetime.now(UTC)
        return ProviderAttemptResult(
            provider_attempt_id=request.provider_attempt_id,
            model_invocation_id=request.model_invocation_id,
            outcome=ProviderAttemptOutcome.COMPLETED,
            acceptance=ProviderAcceptanceCertainty.ESTABLISHED,
            usage=ProviderUsageEvidence(
                state=ProviderUsageState.KNOWN,
                input_tokens=20,
                output_tokens=5,
                reasoning_tokens=7,
                cached_input_tokens=0,
                tool_use_tokens=0,
                total_tokens=32,
            ),
            started_at=now,
            completed_at=now,
            provider_response_id="interaction-1",
            provider_status="completed",
            structured_output_json=self.payload,
        )


class _BlockingAdapter:
    def __init__(self) -> None:
        self.started = asyncio.Event()
        self.requests: list[ProviderInvocationRequest] = []

    async def invoke(self, request: ProviderInvocationRequest) -> ProviderAttemptResult:
        self.requests.append(request)
        self.started.set()
        await asyncio.Event().wait()
        raise AssertionError("blocking adapter should be cancelled by ModelAccess")


class _Cancellation:
    def __init__(self, *, cancelled: bool = False) -> None:
        self._event = asyncio.Event()
        if cancelled:
            self._event.set()

    @property
    def cancelled(self) -> bool:
        return self._event.is_set()

    async def wait(self) -> None:
        await self._event.wait()

    def cancel(self) -> None:
        self._event.set()


def _snapshot() -> RouteConfigSnapshot:
    return load_route_config(_REVISIONS_ROOT, GEMINI_INTERACTIONS_ROUTE_REVISION)


def _request(
    target: ModelTarget = ModelTarget.STRUCTURED_INTERPRETATION,
    *,
    required_identity: RouteConfigIdentity | None = None,
    required_capabilities: tuple[str, ...] = (),
    required_feature_modes: tuple[str, ...] = (),
    max_provider_attempts: int = 1,
) -> ModelInvocationRequest:
    return ModelInvocationRequest(
        model_invocation_id=uuid7(),
        work_id=uuid7(),
        work_revision=1,
        target=target,
        purpose="foundation-test",
        input_text="Return the bounded structured answer.",
        instructions="Use only supplied input.",
        deadline=datetime.now(UTC) + timedelta(seconds=60),
        max_output_tokens=9999,
        structured_output=StructuredOutputContract(
            name="answer",
            schema_json=(
                '{"type":"object","properties":{"decision":{"type":"string",'
                '"enum":["ok"]}},"required":["decision"],"additionalProperties":false}'
            ),
        ),
        security_basis_refs=("synthetic-public-only",),
        required_route_config_identity=required_identity,
        required_capabilities=required_capabilities,
        required_feature_modes=required_feature_modes,
        max_provider_attempts=max_provider_attempts,
    )


@pytest.mark.asyncio
async def test_two_active_targets_resolve_to_same_exact_configured_gemini_binding() -> None:
    snapshot = _snapshot()
    adapter = _CompletedAdapter()
    evidence = RecordingRuntimeEvidencePort()
    runtime = ModelAccessRuntime(
        snapshot,
        {GEMINI_INTERACTIONS_BINDING_REF: adapter},
        evidence=evidence,
    )

    structured = await runtime.invoke(
        _request(
            ModelTarget.STRUCTURED_INTERPRETATION,
            required_identity=snapshot.identity,
            required_capabilities=("text", "structured_output"),
            required_feature_modes=("provider_storage:off",),
        )
    )
    general = await runtime.invoke(_request(ModelTarget.GENERAL_REASONING))

    assert structured.outcome is ModelInvocationOutcome.COMPLETED
    assert general.outcome is ModelInvocationOutcome.COMPLETED
    assert structured.provider_binding_ref == GEMINI_INTERACTIONS_BINDING_REF
    assert structured.provider_model == GEMINI_INTERACTIONS_MODEL
    assert general.provider_binding_ref == structured.provider_binding_ref
    assert structured.started_at is not None
    assert structured.completed_at is not None
    assert all(request.provider_model == GEMINI_INTERACTIONS_MODEL for request in adapter.requests)
    assert all(
        request.provider_endpoint == GEMINI_INTERACTIONS_ENDPOINT for request in adapter.requests
    )
    assert all(
        request.provider_api_revision == GEMINI_INTERACTIONS_API_REVISION
        for request in adapter.requests
    )
    assert all(
        request.provider_service_tier == GEMINI_INTERACTIONS_SERVICE_TIER
        for request in adapter.requests
    )
    assert all(request.reasoning_level == "low" for request in adapter.requests)
    assert all(request.max_output_tokens == 4096 for request in adapter.requests)
    assert any(event.kind.value == "provider_attempt" for event in evidence.events)
    assert any(
        metric.name == "reasoning_tokens" and metric.value == 7
        for event in evidence.events
        for metric in event.metrics
    )
    assert any(
        "service-tier:standard" in event.correlation_refs
        for event in evidence.events
        if event.kind.value == "route"
    )


@pytest.mark.asyncio
async def test_deep_reasoning_is_dormant_and_dispatches_no_provider_attempt() -> None:
    adapter = _CompletedAdapter()
    runtime = ModelAccessRuntime(_snapshot(), {GEMINI_INTERACTIONS_BINDING_REF: adapter})

    result = await runtime.invoke(_request(ModelTarget.DEEP_REASONING))

    assert result.outcome is ModelInvocationOutcome.UNAVAILABLE
    assert result.error_class is ModelAccessErrorClass.CAPABILITY_UNAVAILABLE
    assert result.error_code == "model_target_not_active"
    assert adapter.requests == []


@pytest.mark.asyncio
async def test_provider_json_is_revalidated_independently_against_schema() -> None:
    adapter = _CompletedAdapter(payload='{"decision":"wrong"}')
    runtime = ModelAccessRuntime(_snapshot(), {GEMINI_INTERACTIONS_BINDING_REF: adapter})

    result = await runtime.invoke(_request())

    assert result.outcome is ModelInvocationOutcome.INVALID_RESPONSE
    assert result.error_class is ModelAccessErrorClass.INVALID_RESPONSE
    assert result.output_text is None
    assert result.structured_output_json is None
    assert result.attempts[0].error_code == "structured_output_schema_mismatch"


@pytest.mark.asyncio
async def test_unsupported_schema_keyword_is_rejected_before_provider_egress() -> None:
    adapter = _CompletedAdapter()
    runtime = ModelAccessRuntime(_snapshot(), {GEMINI_INTERACTIONS_BINDING_REF: adapter})
    request = _request()
    invalid = ModelInvocationRequest(
        model_invocation_id=request.model_invocation_id,
        work_id=request.work_id,
        work_revision=request.work_revision,
        target=request.target,
        purpose=request.purpose,
        input_text=request.input_text,
        instructions=request.instructions,
        deadline=request.deadline,
        max_output_tokens=request.max_output_tokens,
        structured_output=StructuredOutputContract(
            name="unsupported",
            schema_json='{"type":"object","oneOf":[]}',
        ),
        security_basis_refs=request.security_basis_refs,
    )

    result = await runtime.invoke(invalid)

    assert result.outcome is ModelInvocationOutcome.INVALID_REQUEST
    assert result.error_class is ModelAccessErrorClass.INVALID_REQUEST
    assert result.error_code is not None
    assert "unsupported_schema_keyword" in result.error_code
    assert adapter.requests == []


@pytest.mark.asyncio
async def test_route_identity_mismatch_fails_before_provider_egress() -> None:
    snapshot = _snapshot()
    adapter = _CompletedAdapter()
    runtime = ModelAccessRuntime(snapshot, {GEMINI_INTERACTIONS_BINDING_REF: adapter})
    wrong_identity = RouteConfigIdentity(
        revision=GEMINI_INTERACTIONS_ROUTE_REVISION,
        content_sha256="1" * 64,
    )

    result = await runtime.invoke(_request(required_identity=wrong_identity))

    assert result.outcome is ModelInvocationOutcome.INVALID_REQUEST
    assert result.error_class is ModelAccessErrorClass.ROUTE_MISMATCH
    assert result.error_code == "required_route_config_identity_mismatch"
    assert adapter.requests == []


@pytest.mark.asyncio
async def test_unavailable_capability_or_feature_mode_never_dispatches() -> None:
    adapter = _CompletedAdapter()
    runtime = ModelAccessRuntime(_snapshot(), {GEMINI_INTERACTIONS_BINDING_REF: adapter})

    capability = await runtime.invoke(_request(required_capabilities=("vision",)))
    feature = await runtime.invoke(_request(required_feature_modes=("streaming:on",)))

    assert capability.outcome is ModelInvocationOutcome.UNAVAILABLE
    assert capability.error_code == "required_capability_not_available"
    assert feature.outcome is ModelInvocationOutcome.UNAVAILABLE
    assert feature.error_code == "required_feature_mode_not_available"
    assert adapter.requests == []


@pytest.mark.asyncio
async def test_retry_budget_above_one_is_rejected_while_route_retry_is_off() -> None:
    adapter = _CompletedAdapter()
    runtime = ModelAccessRuntime(_snapshot(), {GEMINI_INTERACTIONS_BINDING_REF: adapter})

    result = await runtime.invoke(_request(max_provider_attempts=2))

    assert result.outcome is ModelInvocationOutcome.INVALID_REQUEST
    assert result.error_code == "retry_budget_not_supported_by_route"
    assert adapter.requests == []


@pytest.mark.asyncio
async def test_preexisting_cancellation_never_reaches_provider() -> None:
    adapter = _CompletedAdapter()
    runtime = ModelAccessRuntime(_snapshot(), {GEMINI_INTERACTIONS_BINDING_REF: adapter})

    result = await runtime.invoke(_request(), _Cancellation(cancelled=True))

    assert result.outcome is ModelInvocationOutcome.CANCELLED
    assert result.error_class is ModelAccessErrorClass.CANCELLATION
    assert result.attempts[0].acceptance is ProviderAcceptanceCertainty.NOT_ACCEPTED
    assert result.error_code == "cancelled_before_model_routing"
    assert adapter.requests == []


@pytest.mark.asyncio
async def test_cancellation_after_dispatch_preserves_acceptance_uncertainty() -> None:
    adapter = _BlockingAdapter()
    runtime = ModelAccessRuntime(_snapshot(), {GEMINI_INTERACTIONS_BINDING_REF: adapter})
    cancellation = _Cancellation()

    invocation = asyncio.create_task(runtime.invoke(_request(), cancellation))
    await adapter.started.wait()
    cancellation.cancel()
    result = await invocation

    assert result.outcome is ModelInvocationOutcome.CANCELLED
    assert result.error_class is ModelAccessErrorClass.CANCELLATION
    assert result.attempts[0].outcome is ProviderAttemptOutcome.CANCELLED
    assert result.attempts[0].acceptance is ProviderAcceptanceCertainty.POSSIBLE
    assert result.error_code == "local_cancellation_after_dispatch_acceptance_unknown"
