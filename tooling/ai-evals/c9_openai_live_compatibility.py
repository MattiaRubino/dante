"""One-shot C9 OpenAI live compatibility check using synthetic/public data only."""

from __future__ import annotations

import asyncio
import json
import os
import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path
from uuid import uuid7

from dante.modules.intelligence.adapters.outbound.model.openai_responses import (
    OPENAI_RESPONSES_BINDING_REF,
    OPENAI_TERRA_HARNESS_PROFILE_REF,
    OPENAI_TERRA_MODEL,
    OPENAI_TERRA_MODEL_TARGET_REF,
    OPENAI_TERRA_ROUTE_CONFIG_REVISION,
    OpenAIResponsesAdapter,
)
from dante.modules.intelligence.adapters.outbound.model.openai_sdk import (
    OpenAISDKResponsesTransport,
)
from dante.modules.intelligence.contracts.model_access import (
    ProviderAcceptanceCertainty,
    ProviderAttemptOutcome,
    ProviderInvocationRequest,
    ProviderUsageState,
    StructuredOutputContract,
)
from dante.modules.intelligence.contracts.route_config import RouteConfigSnapshot
from dante.modules.intelligence.route_config import RouteConfigLoadError, load_route_config

_PHASE = "C9_P4_LIVE_COMPATIBILITY"
_API_KEY_ENV = "DANTE_OPENAI_QUALIFICATION_API_KEY"
_REPO_ROOT = Path(__file__).resolve().parents[2]
_REVISIONS_ROOT = _REPO_ROOT / "apps/backend/config/intelligence/revisions"

_EXPECTED_MODEL_TARGETS = (OPENAI_TERRA_MODEL_TARGET_REF,)
_EXPECTED_HARNESSES = (OPENAI_TERRA_HARNESS_PROFILE_REF,)
_EXPECTED_BINDINGS = (OPENAI_RESPONSES_BINDING_REF,)
_EXPECTED_ROUTE_POLICIES = frozenset({"qualification-only:no-production-routing"})
_EXPECTED_FEATURE_MODES = frozenset(
    {
        "ask_dante:disabled",
        "background:off",
        "provider_continuation:off",
        "provider_native_tools:off",
        "provider_storage:off",
        "streaming:off",
    }
)
_EXPECTED_QUALIFICATION_REQUIREMENTS = frozenset(
    {
        "candidate-admission:c8",
        "adapter-conformance:c9",
        "live-compatibility:c9",
        "direct-dante-eval:c10",
        "privacy-security:before-private-data",
        "production-qualification:before-promotion",
    }
)
_EXPECTED_CONTROL_PROFILES = frozenset(
    {
        "provider-attempt:dante-owned",
        "egress:synthetic-public-minimized-only",
        "reasoning-effort:medium",
        "reasoning-context:current_turn",
        "service-tier:default",
        "truncation:disabled",
    }
)
_EXPECTED_RETRY_PROFILES = frozenset(
    {
        "provider-sdk:auto-retry-off",
        "dante-retry:classified-pre-acceptance-only",
    }
)
_EXPECTED_FALLBACK_PROFILES = frozenset({"provider-fallback:off"})
_EXPECTED_RESOURCE_PROFILES = frozenset({"attempt-resource-admission:required"})
_EXPECTED_SECURITY_PROFILES = frozenset(
    {
        "private-data:ineligible",
        "store:false",
        "provider-cache:unqualified-for-private-data",
    }
)
_EXPECTED_ROLLOUT_PROFILES = frozenset({"binding:inactive", "production:off"})

_PROVIDER_FEATURE_MODES = (
    "streaming:off",
    "background:off",
    "provider_continuation:off",
    "provider_native_tools:off",
    "provider_storage:off",
)

_SYNTHETIC_INPUT = (
    "Synthetic compatibility fixture. Return marker DANTE_C9_LIVE_OK and integer value 7 "
    "exactly according to the supplied JSON schema."
)
_SYNTHETIC_INSTRUCTIONS = (
    "This is a synthetic/public protocol compatibility check. Use no tools or external data. "
    "Return only the schema-conforming object."
)
_SYNTHETIC_SCHEMA = (
    '{"type":"object","properties":{'
    '"marker":{"type":"string","enum":["DANTE_C9_LIVE_OK"]},'
    '"value":{"type":"integer","enum":[7]}},'
    '"required":["marker","value"],"additionalProperties":false}'
)
_EXPECTED_FIXTURE: dict[str, object] = {
    "marker": "DANTE_C9_LIVE_OK",
    "value": 7,
}


class QualificationPostureError(RuntimeError):
    """Raised before dispatch when the candidate revision is not exactly qualification-safe."""


def _emit(payload: dict[str, object]) -> None:
    sys.stdout.write(json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n")


def _require_exact_set(
    observed: tuple[str, ...],
    expected: frozenset[str],
    *,
    field: str,
) -> None:
    if frozenset(observed) != expected:
        raise QualificationPostureError(f"unexpected qualification posture in {field}")


def _validate_snapshot(snapshot: RouteConfigSnapshot) -> None:
    document = snapshot.document
    if document.revision != OPENAI_TERRA_ROUTE_CONFIG_REVISION:
        raise QualificationPostureError("unexpected route-config revision")
    if document.model_targets != _EXPECTED_MODEL_TARGETS:
        raise QualificationPostureError("unexpected model target posture")
    if document.harness_profiles != _EXPECTED_HARNESSES:
        raise QualificationPostureError("unexpected harness posture")
    if document.provider_bindings != _EXPECTED_BINDINGS:
        raise QualificationPostureError("unexpected provider binding posture")

    for field, observed, expected in (
        ("route_policies", document.route_policies, _EXPECTED_ROUTE_POLICIES),
        ("feature_modes", document.feature_modes, _EXPECTED_FEATURE_MODES),
        (
            "qualification_requirements",
            document.qualification_requirements,
            _EXPECTED_QUALIFICATION_REQUIREMENTS,
        ),
        ("control_profiles", document.control_profiles, _EXPECTED_CONTROL_PROFILES),
        ("retry_profiles", document.retry_profiles, _EXPECTED_RETRY_PROFILES),
        ("fallback_profiles", document.fallback_profiles, _EXPECTED_FALLBACK_PROFILES),
        ("resource_profiles", document.resource_profiles, _EXPECTED_RESOURCE_PROFILES),
        ("security_profiles", document.security_profiles, _EXPECTED_SECURITY_PROFILES),
        ("rollout_profiles", document.rollout_profiles, _EXPECTED_ROLLOUT_PROFILES),
    ):
        _require_exact_set(observed, expected, field=field)


def _failure_evidence(
    *,
    snapshot: RouteConfigSnapshot,
    reason: str,
    outcome: str | None = None,
    acceptance: str | None = None,
    usage_state: str | None = None,
    error_class: str | None = None,
    error_code: str | None = None,
) -> dict[str, object]:
    return {
        "status": "FAIL",
        "phase": _PHASE,
        "route_revision": snapshot.identity.revision,
        "route_sha256": snapshot.identity.content_sha256,
        "provider": "openai",
        "api": "responses",
        "model": OPENAI_TERRA_MODEL,
        "reason": reason,
        "outcome": outcome,
        "acceptance": acceptance,
        "usage_state": usage_state,
        "error_class": error_class,
        "error_code": error_code,
    }


async def _run() -> int:
    try:
        snapshot = load_route_config(_REVISIONS_ROOT, OPENAI_TERRA_ROUTE_CONFIG_REVISION)
        _validate_snapshot(snapshot)
    except RouteConfigLoadError, QualificationPostureError:
        _emit(
            {
                "status": "BLOCKED",
                "phase": _PHASE,
                "reason": "qualification_posture_invalid",
            }
        )
        return 3

    api_key = os.environ.get(_API_KEY_ENV)
    if api_key is None or not api_key.strip():
        _emit(
            {
                "status": "BLOCKED",
                "phase": _PHASE,
                "reason": "missing_qualification_api_key",
                "required_env": _API_KEY_ENV,
            }
        )
        return 2

    started_at = datetime.now(UTC)
    request = ProviderInvocationRequest(
        provider_attempt_id=uuid7(),
        model_invocation_id=uuid7(),
        work_id=uuid7(),
        work_revision=1,
        provider_binding_ref=OPENAI_RESPONSES_BINDING_REF,
        model_target_ref=OPENAI_TERRA_MODEL_TARGET_REF,
        provider_model=OPENAI_TERRA_MODEL,
        harness_profile_ref=OPENAI_TERRA_HARNESS_PROFILE_REF,
        purpose="c9_live_compatibility",
        rendered_input=_SYNTHETIC_INPUT,
        rendered_instructions=_SYNTHETIC_INSTRUCTIONS,
        deadline=started_at + timedelta(seconds=60),
        max_output_tokens=512,
        route_config_identity=snapshot.identity,
        structured_output=StructuredOutputContract(
            name="dante_c9_live_compatibility",
            schema_json=_SYNTHETIC_SCHEMA,
            strict=True,
        ),
        feature_modes=_PROVIDER_FEATURE_MODES,
        security_basis_refs=("c9:synthetic-public-only", "c9:live-compatibility"),
    )

    transport = OpenAISDKResponsesTransport.from_api_key(api_key=api_key)
    try:
        result = await OpenAIResponsesAdapter(transport).invoke(request)
    finally:
        await transport.close()

    error_class = result.error_class.value if result.error_class is not None else None
    if (
        result.outcome is not ProviderAttemptOutcome.COMPLETED
        or result.acceptance is not ProviderAcceptanceCertainty.ESTABLISHED
    ):
        _emit(
            _failure_evidence(
                snapshot=snapshot,
                reason="provider_attempt_not_completed",
                outcome=result.outcome.value,
                acceptance=result.acceptance.value,
                usage_state=result.usage.state.value,
                error_class=error_class,
                error_code=result.error_code,
            )
        )
        return 1

    if result.usage.state is not ProviderUsageState.KNOWN:
        _emit(
            _failure_evidence(
                snapshot=snapshot,
                reason="provider_usage_not_known",
                outcome=result.outcome.value,
                acceptance=result.acceptance.value,
                usage_state=result.usage.state.value,
            )
        )
        return 1

    if result.provider_request_id is None or result.provider_response_id is None:
        _emit(
            _failure_evidence(
                snapshot=snapshot,
                reason="provider_ids_missing",
                outcome=result.outcome.value,
                acceptance=result.acceptance.value,
                usage_state=result.usage.state.value,
            )
        )
        return 1

    if result.structured_output_json is None:
        _emit(
            _failure_evidence(
                snapshot=snapshot,
                reason="structured_output_missing",
                outcome=result.outcome.value,
                acceptance=result.acceptance.value,
                usage_state=result.usage.state.value,
            )
        )
        return 1

    parsed: object = json.loads(result.structured_output_json)
    if parsed != _EXPECTED_FIXTURE:
        _emit(
            _failure_evidence(
                snapshot=snapshot,
                reason="fixture_assertion_failed",
                outcome=result.outcome.value,
                acceptance=result.acceptance.value,
                usage_state=result.usage.state.value,
            )
        )
        return 1

    _emit(
        {
            "status": "PASS",
            "phase": _PHASE,
            "route_revision": snapshot.identity.revision,
            "route_sha256": snapshot.identity.content_sha256,
            "provider": "openai",
            "api": "responses",
            "model": OPENAI_TERRA_MODEL,
            "outcome": result.outcome.value,
            "acceptance": result.acceptance.value,
            "usage_state": result.usage.state.value,
            "input_tokens": result.usage.input_tokens,
            "output_tokens": result.usage.output_tokens,
            "total_tokens": result.usage.total_tokens,
            "provider_request_id": result.provider_request_id,
            "provider_response_id": result.provider_response_id,
            "fixture_assertion": "PASS",
        }
    )
    return 0


def main() -> int:
    return asyncio.run(_run())


if __name__ == "__main__":
    raise SystemExit(main())
