"""Production-shaped native Gemini candidate for DANTE direct evals.

This remains evaluation tooling, but unlike the historical OpenAI-compatible Gemini candidate it
executes fixtures through the real DANTE bootstrap composition, ModelAccessRuntime, exact route
revision, native Gemini Interactions adapter and private HTTP transport.
"""

from __future__ import annotations

import json
import os
import time
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Final
from uuid import uuid7

from dante.bootstrap.intelligence import create_development_model_access_runtime
from dante.modules.intelligence.adapters.outbound.model.gemini_interactions import (
    GEMINI_INTERACTIONS_API_REVISION,
    GEMINI_INTERACTIONS_BINDING_REF,
    GEMINI_INTERACTIONS_MODEL,
    GEMINI_INTERACTIONS_ROUTE_REVISION,
    GEMINI_INTERACTIONS_SERVICE_TIER,
)
from dante.modules.intelligence.contracts.model_access import (
    ModelInvocationOutcome,
    ModelInvocationRequest,
    ModelTarget,
    StructuredOutputContract,
)

from dante_eval_core import CandidateResult, EvalFixture

_REPO_ROOT: Final = Path(__file__).resolve().parents[2]
_REVISIONS_ROOT: Final = _REPO_ROOT / "apps" / "backend" / "config" / "intelligence" / "revisions"
_KEY_ENV_NAMES: Final = ("DANTE_GEMINI_API_KEY", "DANTE_EVAL_GEMINI_API_KEY")
_STRUCTURED_FAMILIES: Final = frozenset({"DANTE-E02", "DANTE-E03", "DANTE-E11", "DANTE-E12"})


def _api_key_from_environment() -> str:
    for name in _KEY_ENV_NAMES:
        value = os.environ.get(name)
        if value is not None and value.strip():
            return value
    raise ValueError("DANTE_GEMINI_API_KEY or DANTE_EVAL_GEMINI_API_KEY is not set")


def _target_for_fixture(fixture: EvalFixture) -> ModelTarget:
    if fixture.family in _STRUCTURED_FAMILIES:
        return ModelTarget.STRUCTURED_INTERPRETATION
    return ModelTarget.GENERAL_REASONING


class GeminiNativeModelAccessCandidate:
    candidate_id = "google-gemini-native-modelaccess"

    def __init__(self) -> None:
        self._resources = create_development_model_access_runtime(
            api_key=_api_key_from_environment(),
            revisions_root=_REVISIONS_ROOT,
            route_revision=GEMINI_INTERACTIONS_ROUTE_REVISION,
        )
        self._runtime = self._resources.runtime
        self._snapshot = self._runtime.route_config

    @property
    def identity(self) -> dict[str, str]:
        return {
            "candidate_id": self.candidate_id,
            "serving_platform": "google-gemini-developer-api",
            "protocol_family": "gemini-interactions-v1beta-native",
            "model": GEMINI_INTERACTIONS_MODEL,
            "route_revision": self._snapshot.identity.revision,
            "route_sha256": self._snapshot.identity.content_sha256,
            "binding": GEMINI_INTERACTIONS_BINDING_REF,
            "api_revision_marker": GEMINI_INTERACTIONS_API_REVISION,
            "service_tier": GEMINI_INTERACTIONS_SERVICE_TIER,
            "reasoning_level": "low",
            "store": "false",
            "background": "false",
            "provider_native_tools": "off",
        }

    async def invoke(self, fixture: EvalFixture, *, timeout_seconds: float) -> CandidateResult:
        if not fixture.requires_model:
            raise ValueError("candidate must not be invoked for model-avoidance fixture")
        if fixture.response_schema is None:
            raise ValueError("native candidate requires a response schema")

        target = _target_for_fixture(fixture)
        deadline_seconds = min(timeout_seconds, 90.0)
        request = ModelInvocationRequest(
            model_invocation_id=uuid7(),
            work_id=uuid7(),
            work_revision=1,
            target=target,
            purpose=f"direct-eval:{fixture.family}:{fixture.fixture_id}",
            input_text=fixture.input_text,
            instructions=fixture.instructions,
            deadline=datetime.now(UTC) + timedelta(seconds=deadline_seconds),
            max_output_tokens=fixture.max_output_tokens,
            structured_output=StructuredOutputContract(
                name=f"dante_eval_{fixture.fixture_id.replace('-', '_')}",
                schema_json=json.dumps(fixture.response_schema, separators=(",", ":")),
            ),
            security_basis_refs=("synthetic-public-eval-only",),
            required_route_config_identity=self._snapshot.identity,
            required_capabilities=("text", "structured_output"),
            required_feature_modes=(
                "streaming:off",
                "background:off",
                "provider_continuation:off",
                "provider_native_tools:off",
                "provider_storage:off",
            ),
            max_provider_attempts=1,
        )

        started = time.perf_counter()
        result = await self._runtime.invoke(request)
        latency_ms = int((time.perf_counter() - started) * 1000)
        attempt = result.attempts[0] if result.attempts else None

        reasoning_tokens = result.usage.reasoning_tokens
        billable_output_tokens = None
        if result.usage.output_tokens is not None:
            billable_output_tokens = result.usage.output_tokens + (reasoning_tokens or 0)

        return CandidateResult(
            output_text=(
                result.structured_output_json
                if result.outcome is ModelInvocationOutcome.COMPLETED
                else None
            ),
            input_tokens=result.usage.input_tokens,
            output_tokens=result.usage.output_tokens,
            total_tokens=result.usage.total_tokens,
            reasoning_tokens=reasoning_tokens,
            cached_input_tokens=result.usage.cached_input_tokens,
            tool_use_tokens=result.usage.tool_use_tokens,
            billable_output_tokens=billable_output_tokens,
            provider_request_id=attempt.provider_request_id if attempt is not None else None,
            provider_response_id=attempt.provider_response_id if attempt is not None else None,
            latency_ms=latency_ms,
            provider_status=(
                attempt.provider_status
                if attempt is not None and attempt.provider_status is not None
                else result.outcome.value
            ),
            error_class=result.error_class.value if result.error_class is not None else None,
            error_code=result.error_code,
            finish_reason=result.finish_reason,
        )

    async def close(self) -> None:
        await self._resources.close()
