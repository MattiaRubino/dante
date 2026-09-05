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

from dante.modules.intelligence.adapters.outbound.model.gemini_http import (  # noqa: E402
    GeminiInteractionsHttpTransport,
)
from dante.modules.intelligence.adapters.outbound.model.gemini_interactions import (  # noqa: E402
    GEMINI_INTERACTIONS_BINDING_REF,
    GeminiInteractionsAdapter,
)
from dante.modules.intelligence.application.model_access import ModelAccessRuntime  # noqa: E402
from dante.modules.intelligence.contracts.model_access import (  # noqa: E402
    ModelInvocationRequest,
    ModelTarget,
    StructuredOutputContract,
)
from dante.modules.intelligence.route_config import load_route_config  # noqa: E402

_REVISIONS_ROOT = _BACKEND_ROOT / "config" / "intelligence" / "revisions"


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Synthetic native Gemini ModelAccess smoke")
    parser.add_argument("--execute", action="store_true")
    return parser


async def _run(execute: bool) -> int:
    snapshot = load_route_config(_REVISIONS_ROOT, "gemini-flash-dev-v1")
    if not execute:
        print(
            json.dumps(
                {
                    "status": "READY",
                    "mode": "DRY_RUN",
                    "route_revision": snapshot.identity.revision,
                    "target": ModelTarget.STRUCTURED_INTERPRETATION.value,
                    "binding": GEMINI_INTERACTIONS_BINDING_REF,
                    "planned_provider_calls": 1,
                },
                sort_keys=True,
            )
        )
        return 0

    api_key = os.environ.get("DANTE_GEMINI_API_KEY")
    if api_key is None or not api_key.strip():
        print(json.dumps({"status": "BLOCKED", "reason": "DANTE_GEMINI_API_KEY is not set"}))
        return 2

    transport = GeminiInteractionsHttpTransport(api_key)
    adapter = GeminiInteractionsAdapter(transport)
    runtime = ModelAccessRuntime(snapshot, {GEMINI_INTERACTIONS_BINDING_REF: adapter})
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
    )

    try:
        result = await runtime.invoke(request)
    finally:
        await transport.close()

    print(
        json.dumps(
            {
                "status": result.outcome.value,
                "route_revision": result.route_config_identity.revision,
                "target": result.target.value,
                "binding": result.provider_binding_ref,
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
                "output": (
                    json.loads(result.structured_output_json)
                    if result.structured_output_json is not None
                    else None
                ),
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
