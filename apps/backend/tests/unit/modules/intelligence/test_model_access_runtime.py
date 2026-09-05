"""Unit acceptance for deterministic ModelAccess routing, validation and evidence."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from pathlib import Path
from uuid import uuid7

import pytest

from dante.modules.intelligence.application.model_access import ModelAccessRuntime
from dante.modules.intelligence.contracts.model_access import (
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
            structured_output_json=self.payload,
        )


def _request(target: ModelTarget = ModelTarget.STRUCTURED_INTERPRETATION) -> ModelInvocationRequest:
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
    )


@pytest.mark.asyncio
async def test_two_active_targets_resolve_to_same_configured_gemini_binding() -> None:
    snapshot = load_route_config(_REVISIONS_ROOT, "gemini-flash-dev-v1")
    adapter = _CompletedAdapter()
    evidence = RecordingRuntimeEvidencePort()
    runtime = ModelAccessRuntime(
        snapshot,
        {"google-gemini-interactions-flash-v1": adapter},
        evidence=evidence,
    )

    structured = await runtime.invoke(_request(ModelTarget.STRUCTURED_INTERPRETATION))
    general = await runtime.invoke(_request(ModelTarget.GENERAL_REASONING))

    assert structured.outcome is ModelInvocationOutcome.COMPLETED
    assert general.outcome is ModelInvocationOutcome.COMPLETED
    assert structured.provider_binding_ref == "google-gemini-interactions-flash-v1"
    assert general.provider_binding_ref == structured.provider_binding_ref
    assert all(request.provider_model == "gemini-3.8-flash" for request in adapter.requests)
    assert all(request.reasoning_level == "low" for request in adapter.requests)
    assert all(request.max_output_tokens == 4096 for request in adapter.requests)
    assert any(event.kind.value == "provider_attempt" for event in evidence.events)
    assert any(
        metric.name == "reasoning_tokens" and metric.value == 7
        for event in evidence.events
        for metric in event.metrics
    )


@pytest.mark.asyncio
async def test_deep_reasoning_is_dormant_and_dispatches_no_provider_attempt() -> None:
    snapshot = load_route_config(_REVISIONS_ROOT, "gemini-flash-dev-v1")
    adapter = _CompletedAdapter()
    runtime = ModelAccessRuntime(snapshot, {"google-gemini-interactions-flash-v1": adapter})

    result = await runtime.invoke(_request(ModelTarget.DEEP_REASONING))

    assert result.outcome is ModelInvocationOutcome.UNAVAILABLE
    assert result.error_code == "model_target_not_active"
    assert adapter.requests == []


@pytest.mark.asyncio
async def test_provider_json_is_revalidated_independently_against_schema() -> None:
    snapshot = load_route_config(_REVISIONS_ROOT, "gemini-flash-dev-v1")
    adapter = _CompletedAdapter(payload='{"decision":"wrong"}')
    runtime = ModelAccessRuntime(snapshot, {"google-gemini-interactions-flash-v1": adapter})

    result = await runtime.invoke(_request())

    assert result.outcome is ModelInvocationOutcome.INVALID_RESPONSE
    assert result.output_text is None
    assert result.structured_output_json is None
    assert result.attempts[0].error_code == "structured_output_schema_mismatch"


@pytest.mark.asyncio
async def test_unsupported_schema_keyword_is_rejected_before_provider_egress() -> None:
    snapshot = load_route_config(_REVISIONS_ROOT, "gemini-flash-dev-v1")
    adapter = _CompletedAdapter()
    runtime = ModelAccessRuntime(snapshot, {"google-gemini-interactions-flash-v1": adapter})
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
    assert result.error_code is not None
    assert "unsupported_schema_keyword" in result.error_code
    assert adapter.requests == []
