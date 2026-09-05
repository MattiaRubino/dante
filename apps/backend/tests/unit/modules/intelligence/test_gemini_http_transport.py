"""Unit acceptance for the private Gemini Interactions HTTP transport."""

from __future__ import annotations

from collections.abc import Mapping

import pytest

from dante.modules.intelligence.adapters.outbound.model.gemini_http import (
    GeminiInteractionsHttpTransport,
)
from dante.modules.intelligence.adapters.outbound.model.gemini_interactions import (
    GEMINI_INTERACTIONS_ENDPOINT,
    GEMINI_INTERACTIONS_MODEL,
    GeminiInteractionStatus,
    GeminiInteractionsWireRequest,
    GeminiTransportError,
    GeminiTransportErrorKind,
)


class _Response:
    def __init__(
        self,
        status_code: int,
        payload: object,
        headers: Mapping[str, str] | None = None,
    ) -> None:
        self.status_code = status_code
        self._payload = payload
        self.headers = headers or {}

    def json(self) -> object:
        return self._payload


class _Client:
    def __init__(self, response: _Response) -> None:
        self.response = response
        self.calls: list[tuple[str, Mapping[str, str], object, float]] = []
        self.closed = False

    async def post(
        self,
        url: str,
        *,
        headers: Mapping[str, str],
        json: object,
        timeout: float,
    ) -> _Response:
        self.calls.append((url, headers, json, timeout))
        return self.response

    async def aclose(self) -> None:
        self.closed = True


def _request(*, structured: bool = True) -> GeminiInteractionsWireRequest:
    return GeminiInteractionsWireRequest(
        model=GEMINI_INTERACTIONS_MODEL,
        input_text="Return exactly the structured result.",
        system_instruction="Use only supplied data.",
        max_output_tokens=128,
        thinking_level="low",
        timeout_seconds=30,
        structured_output_schema=(
            {"type": "object", "properties": {"ok": {"type": "boolean"}}}
            if structured
            else None
        ),
    )


@pytest.mark.asyncio
async def test_http_transport_forces_stateless_unary_native_interaction_request() -> None:
    client = _Client(
        _Response(
            200,
            {
                "id": "interaction-1",
                "status": "completed",
                "steps": [
                    {
                        "type": "model_output",
                        "content": [{"type": "text", "text": '{"ok":true}'}],
                    }
                ],
                "usage": {
                    "total_input_tokens": 100,
                    "total_output_tokens": 20,
                    "total_thought_tokens": 35,
                    "total_cached_tokens": 5,
                    "total_tool_use_tokens": 0,
                    "total_tokens": 155,
                },
            },
            {"x-goog-request-id": "request-1"},
        )
    )
    transport = GeminiInteractionsHttpTransport("secret", client=client)

    result = await transport.create(_request())

    assert result.status is GeminiInteractionStatus.COMPLETED
    assert result.output_text == '{"ok":true}'
    assert result.thought_tokens == 35
    assert result.cached_tokens == 5
    assert result.total_tokens == 155
    url, headers, payload, timeout = client.calls[0]
    assert url == GEMINI_INTERACTIONS_ENDPOINT
    assert headers["x-goog-api-key"] == "secret"
    assert timeout == 30
    assert isinstance(payload, dict)
    assert payload["store"] is False
    assert payload["stream"] is False
    assert payload["background"] is False
    assert payload["generation_config"] == {
        "max_output_tokens": 128,
        "thinking_level": "low",
        "thinking_summaries": "none",
        "tool_choice": "none",
    }
    assert payload["response_format"] == {
        "type": "text",
        "mime_type": "application/json",
        "schema": {"type": "object", "properties": {"ok": {"type": "boolean"}}},
    }


@pytest.mark.asyncio
async def test_http_transport_maps_rate_limit_without_exposing_provider_payload() -> None:
    client = _Client(
        _Response(
            429,
            {"error": {"status": "RESOURCE_EXHAUSTED", "message": "redacted detail"}},
            {"x-goog-request-id": "request-429"},
        )
    )
    transport = GeminiInteractionsHttpTransport("secret", client=client)

    with pytest.raises(GeminiTransportError) as caught:
        await transport.create(_request(structured=False))

    assert caught.value.kind is GeminiTransportErrorKind.RATE_LIMIT
    assert caught.value.code == "RESOURCE_EXHAUSTED"
    assert caught.value.request_id == "request-429"
