"""Guarded synthetic smoke for the production-shaped native Gemini ModelAccess path.

No provider call occurs unless --execute is supplied. The API key is read only from the local
environment and is never printed or persisted.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path
from uuid import uuid7

_BACKEND_ROOT = Path(__file__).resolve().parents[2] / "apps" / "backend"
sys.path.insert(0, str(_BACKEND_ROOT / "src"))

from dante.bootstrap.intelligence import (  # noqa: E402
    create_development_model_access_runtime,
)
from dante.modules.intelligence.adapters.outbound.model.gemini_interactions import (  # noqa: E402
    GEMINI_INTERACTIONS_BINDING_REF,
    GEMINI_INTERACTIONS_ROUTE_REVISION,
)
from dante.modules.intelligence.contracts.model_access import (  # noqa: E402
    ModelInvocationRequest,
    ModelTarget,
    StructuredOutputContract,
)
from dante.modules.intelligence.route_config import load_route_config  # noqa: E402

_REVISIONS_ROOT = _BACKEND_ROOT / "config" / "intelligence" / "revisions"
_KEY_ENV_NAMES = ("DANTE_GEMINI_API_KEY", "DANTE_EVAL_GEMINI_API_KEY")


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Synthetic native Gemini ModelAccess smoke")
    parser.add_argument("--execute", action="store_true")
    return parser


def _api_key_from_environment() -> str | None:
    for name in _KEY_ENV_NAMES:
        value = os.environ.get(name)
        if value is not None and value.strip():
            return value
    return None


async def _run(execute: bool) -> int:
    snapshot = load_route_config(_REVISIONS_ROOT, GEMINI_INTERACTIONS_ROUTE_REVISION)
    if not execute:
        print(
            json.dumps(
                {
                    "status": "READY",
                    "mode": "DRY_RUN",
                    "route_revision": snapshot.identity.revision,
                    "route_sha256": snapshot.identity.content_sha256,
                    "target": ModelTarget.STRUCTURED_INTERPRETATION.value,
                    "binding": GEMINI_INTERACTIONS_BINDING_REF,
                    "planned_provider_calls": 1,
                },
                sort_keys=True,
            )
        )
        return 0

    api_key = _api_key_from_environment()
    if api_key is None:
        print(
            json.dumps(
                {
                    "status": "BLOCKED",
                    "reason": (
                        "DANTE_GEMINI_API_KEY or DANTE_EVAL_GEMINI_API_KEY is not set"
                    ),
                }
            )
        )
        return 2

    resources = create_development_model_access_runtime(
        api_key=api_key,
        revisions_root=_REVISIONS_ROOT,
    )
    runtime = resources.runtime
    request = ModelInvocationRequest(
        model_invocation_id=uuid7(),
        work_id=uuid7(),
        work_revision=1,
        target=ModelTarget.STRUCTURED_INTERPRETATION,
        purpose="native-runtime-smoke",
        input_text="Synthetic smoke. Return ok=true and label exactly DANTE_GEMINI_NATIVE_OK.",
        instructions="Return only the schema-conforming answer. No tools or external data.",
        deadline=datetime.now(UTC) + timedelta(seconds=30),
        max_output_tokens=128,
        structured_output=StructuredOutputContract(
            name="native_smoke",
            schema_json=(
                '{"type":"object","properties":{"ok":{"type":"boolean","const":true},'
                '"label":{"type":"string","const":"DANTE_GEMINI_NATIVE_OK"}},'
                '"required":["ok","label"],"additionalProperties":false}'
            ),
        ),
        security_basis_refs=("synthetic-public-only",),
        required_route_config_identity=snapshot.identity,
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

    try:
        result = await runtime.invoke(request)
    finally:
        await resources.close()

    attempt = result.attempts[0] if result.attempts else None
    print(
        json.dumps(
            {
                "status": result.outcome.value,
                "route_revision": result.route_config_identity.revision,
                "route_sha256": result.route_config_identity.content_sha256,
                "target": result.target.value,
                "binding": result.provider_binding_ref,
                "model": result.provider_model,
                "harness": result.harness_profile_ref,
                "usage": {
                    "state": result.usage.state.value,
                    "input_tokens": result.usage.input_tokens,
                    "output_tokens": result.usage.output_tokens,
                    "reasoning_tokens": result.usage.reasoning_tokens,
                    "cached_input_tokens": result.usage.cached_input_tokens,
                    "tool_use_tokens": result.usage.tool_use_tokens,
                    "total_tokens": result.usage.total_tokens,
                },
                "attempt_outcomes": [attempt.outcome.value for attempt in result.attempts],
                "provider_status": attempt.provider_status if attempt is not None else None,
                "finish_reason": result.finish_reason,
                "output": (
                    json.loads(result.structured_output_json)
                    if result.structured_output_json is not None
                    else None
                ),
                "error_class": result.error_class.value if result.error_class is not None else None,
                "error_code": result.error_code,
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0 if result.outcome.value == "completed" else 1


def main() -> int:
    args = _parser().parse_args()
    return asyncio.run(_run(args.execute))


if __name__ == "__main__":
    raise SystemExit(main())
