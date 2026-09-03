"""C9 material-SDK conformance for the private OpenAI Responses transport."""

from __future__ import annotations

import json
from collections.abc import Callable
from typing import cast

import httpx2
import pytest
from openai import AsyncOpenAI

from dante.modules.intelligence.adapters.outbound.model.openai_responses import (
    OPENAI_TERRA_MODEL,
    OpenAIResponsesWireRequest,
    OpenAITransportError,
    OpenAITransportErrorKind,
)
from dante.modules.intelligence.adapters.outbound.model.openai_sdk import (
    OpenAISDKResponsesTransport,
)

_BASE_URL = "https://synthetic-openai.invalid/v1"


def _wire_request(*, structured: bool = False) -> OpenAIResponsesWireRequest:
    if structured:
        return OpenAIResponsesWireRequest(
            model=OPENAI_TERRA_MODEL,
            input_text="Synthetic public qualification prompt",
            instructions="Answer only from supplied synthetic data.",
            max_output_tokens=64,
            store=False,
            timeout_seconds=7.5,
            structured_output_name="synthetic_answer",
            structured_output_schema_json=(
                '{"type":"object","properties":{"answer":{"type":"string"}},'
                '"required":["answer"],"additionalProperties":false}'
            ),
            structured_output_strict=True,
        )
    return OpenAIResponsesWireRequest(
        model=OPENAI_TERRA_MODEL,
        input_text="Synthetic public qualification prompt",
        instructions="Answer only from supplied synthetic data.",
        max_output_tokens=64,
        store=False,
        timeout_seconds=7.5,
    )


def _server_error_handler(
    seen: list[httpx2.Request],
) -> Callable[[httpx2.Request], httpx2.Response]:
    def handler(request: httpx2.Request) -> httpx2.Response:
        seen.append(request)
        return httpx2.Response(
            500,
            request=request,
            headers={"x-request-id": "req_synthetic_500"},
            json={
                "error": {
                    "message": "synthetic server failure",
                    "type": "server_error",
                    "param": None,
                    "code": "server_error",
                }
            },
        )

    return handler


def _body(request: httpx2.Request) -> dict[str, object]:
    document = json.loads(request.content)
    assert isinstance(document, dict)
    return cast(dict[str, object], document)


@pytest.mark.asyncio
async def test_sdk_transport_rejects_client_with_hidden_retries() -> None:
    seen: list[httpx2.Request] = []
    http_client = httpx2.AsyncClient(transport=httpx2.MockTransport(_server_error_handler(seen)))
    client = AsyncOpenAI(
        api_key="synthetic-test-key",
        base_url=_BASE_URL,
        max_retries=1,
        http_client=http_client,
    )
    try:
        with pytest.raises(ValueError, match="max_retries=0"):
            OpenAISDKResponsesTransport(client)
    finally:
        await client.close()
    assert seen == []


@pytest.mark.asyncio
async def test_sdk_serializes_one_attempt_with_all_disabled_provider_modes() -> None:
    seen: list[httpx2.Request] = []
    http_client = httpx2.AsyncClient(transport=httpx2.MockTransport(_server_error_handler(seen)))
    client = AsyncOpenAI(
        api_key="synthetic-test-key",
        base_url=_BASE_URL,
        max_retries=0,
        http_client=http_client,
    )
    transport = OpenAISDKResponsesTransport(client)

    try:
        with pytest.raises(OpenAITransportError) as captured:
            await transport.create(_wire_request())
    finally:
        await transport.close()

    assert captured.value.kind is OpenAITransportErrorKind.SERVER
    assert captured.value.code == "http_500"
    assert captured.value.request_id == "req_synthetic_500"
    assert len(seen) == 1

    body = _body(seen[0])
    assert body["model"] == OPENAI_TERRA_MODEL
    assert body["input"] == "Synthetic public qualification prompt"
    assert body["instructions"] == "Answer only from supplied synthetic data."
    assert body["max_output_tokens"] == 64
    assert body["store"] is False
    assert body["stream"] is False
    assert body["background"] is False
    assert body["tools"] == []
    assert body["reasoning"] == {
        "effort": "medium",
        "context": "current_turn",
    }
    assert body["service_tier"] == "default"
    assert body["truncation"] == "disabled"
    assert "conversation" not in body
    assert "previous_response_id" not in body
    assert "prompt_cache_key" not in body
    assert "prompt_cache_retention" not in body


@pytest.mark.asyncio
async def test_sdk_serializes_strict_structured_output_without_enabling_tools() -> None:
    seen: list[httpx2.Request] = []
    http_client = httpx2.AsyncClient(transport=httpx2.MockTransport(_server_error_handler(seen)))
    client = AsyncOpenAI(
        api_key="synthetic-test-key",
        base_url=_BASE_URL,
        max_retries=0,
        http_client=http_client,
    )
    transport = OpenAISDKResponsesTransport(client)

    try:
        with pytest.raises(OpenAITransportError):
            await transport.create(_wire_request(structured=True))
    finally:
        await transport.close()

    assert len(seen) == 1
    body = _body(seen[0])
    text = body.get("text")
    assert isinstance(text, dict)
    text_mapping = cast(dict[str, object], text)
    response_format = text_mapping.get("format")
    assert isinstance(response_format, dict)
    format_mapping = cast(dict[str, object], response_format)
    assert format_mapping["type"] == "json_schema"
    assert format_mapping["name"] == "synthetic_answer"
    assert format_mapping["strict"] is True
    assert isinstance(format_mapping["schema"], dict)
    assert body["tools"] == []
    assert body["store"] is False
    assert body["background"] is False
