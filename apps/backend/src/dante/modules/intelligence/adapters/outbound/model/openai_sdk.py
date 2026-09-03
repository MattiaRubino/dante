"""Private OpenAI SDK transport for the admitted Responses/Terra qualification candidate."""

from __future__ import annotations

import json
from typing import Final, Literal, cast

import openai
from openai import AsyncOpenAI
from openai.types.responses.response import Response
from openai.types.responses.response_text_config_param import ResponseTextConfigParam

from dante.modules.intelligence.adapters.outbound.model.openai_responses import (
    OPENAI_TERRA_MODEL,
    OpenAIResponsesTransport,
    OpenAIResponsesWireRequest,
    OpenAIResponsesWireResponse,
    OpenAIResponseStatus,
    OpenAITransportError,
    OpenAITransportErrorKind,
)

_OPENAI_SDK_MAX_RETRIES: Final = 0
_OPENAI_REASONING_EFFORT: Final[Literal["medium"]] = "medium"
_OPENAI_SERVICE_TIER: Final[Literal["default"]] = "default"
_OPENAI_TRUNCATION: Final[Literal["disabled"]] = "disabled"


def _require_secret(value: str, *, name: str) -> None:
    if not value or not value.strip():
        raise ValueError(f"{name} must be non-empty")


def _structured_text_config(request: OpenAIResponsesWireRequest) -> ResponseTextConfigParam | None:
    if request.structured_output_schema_json is None:
        return None

    schema_value = json.loads(request.structured_output_schema_json)
    if not isinstance(schema_value, dict):
        raise OpenAITransportError(
            OpenAITransportErrorKind.INVALID_REQUEST,
            code="structured_schema_not_object",
        )
    schema = cast(dict[str, object], schema_value)
    return {
        "format": {
            "type": "json_schema",
            "name": cast(str, request.structured_output_name),
            "schema": schema,
            "strict": cast(bool, request.structured_output_strict),
        }
    }


def _extract_refusal(response: Response) -> str | None:
    """Extract refusal text without leaking SDK output types past this module."""

    document = cast(dict[str, object], response.model_dump(mode="python", by_alias=True))
    output = document.get("output")
    if not isinstance(output, list):
        return None

    for item in output:
        if not isinstance(item, dict) or item.get("type") != "message":
            continue
        content = item.get("content")
        if not isinstance(content, list):
            continue
        for part in content:
            if not isinstance(part, dict) or part.get("type") != "refusal":
                continue
            refusal = part.get("refusal")
            if isinstance(refusal, str) and refusal.strip():
                return refusal
    return None


def _status_error_kind(status_code: int) -> OpenAITransportErrorKind:
    if status_code == 408:
        return OpenAITransportErrorKind.TIMEOUT
    if status_code == 409:
        return OpenAITransportErrorKind.CONFLICT
    if status_code == 429:
        return OpenAITransportErrorKind.RATE_LIMIT
    if status_code >= 500:
        return OpenAITransportErrorKind.SERVER
    if status_code in {400, 422}:
        return OpenAITransportErrorKind.INVALID_REQUEST
    if status_code == 401:
        return OpenAITransportErrorKind.AUTHENTICATION
    if status_code == 403:
        return OpenAITransportErrorKind.PERMISSION
    if status_code == 404:
        return OpenAITransportErrorKind.NOT_FOUND
    return OpenAITransportErrorKind.UNKNOWN


def _failed_response_kind(response: Response) -> tuple[OpenAITransportErrorKind, str]:
    if response.error is None:
        return OpenAITransportErrorKind.INVALID_RESPONSE, "failed_without_error"

    code = response.error.code
    if code == "server_error":
        return OpenAITransportErrorKind.SERVER, code
    if code == "rate_limit_exceeded":
        return OpenAITransportErrorKind.RATE_LIMIT, code
    return OpenAITransportErrorKind.INVALID_REQUEST, code


def _wire_status(response: Response) -> OpenAIResponseStatus:
    if response.status == "completed":
        return OpenAIResponseStatus.COMPLETED
    if response.status == "incomplete":
        return OpenAIResponseStatus.INCOMPLETE
    if response.status == "cancelled":
        raise OpenAITransportError(
            OpenAITransportErrorKind.CANCELLED,
            code="response_cancelled",
            request_id=response._request_id,
        )
    if response.status == "failed":
        kind, code = _failed_response_kind(response)
        raise OpenAITransportError(kind, code=code, request_id=response._request_id)
    raise OpenAITransportError(
        OpenAITransportErrorKind.INVALID_RESPONSE,
        code=f"unexpected_response_status:{response.status}",
        request_id=response._request_id,
    )


def _wire_response(response: Response) -> OpenAIResponsesWireResponse:
    usage = response.usage
    output_text = response.output_text or None
    return OpenAIResponsesWireResponse(
        status=_wire_status(response),
        response_id=response.id,
        request_id=response._request_id,
        output_text=output_text,
        refusal_reason=_extract_refusal(response),
        input_tokens=usage.input_tokens if usage is not None else None,
        output_tokens=usage.output_tokens if usage is not None else None,
        total_tokens=usage.total_tokens if usage is not None else None,
    )


def _transport_error(exc: openai.APIError) -> OpenAITransportError:
    if isinstance(exc, openai.APITimeoutError):
        return OpenAITransportError(OpenAITransportErrorKind.TIMEOUT, code="sdk_timeout")
    if isinstance(exc, openai.APIConnectionError):
        return OpenAITransportError(OpenAITransportErrorKind.CONNECTION, code="sdk_connection")
    if isinstance(exc, openai.APIStatusError):
        return OpenAITransportError(
            _status_error_kind(exc.status_code),
            code=f"http_{exc.status_code}",
            request_id=exc.request_id,
        )
    return OpenAITransportError(OpenAITransportErrorKind.UNKNOWN, code=type(exc).__name__)


class OpenAISDKResponsesTransport(OpenAIResponsesTransport):
    """SDK-backed transport with retries and provider-managed continuation disabled."""

    def __init__(self, client: AsyncOpenAI) -> None:
        if client.max_retries != _OPENAI_SDK_MAX_RETRIES:
            raise ValueError("OpenAI SDK client must be constructed with max_retries=0")
        self._client = client

    @classmethod
    def from_api_key(
        cls,
        *,
        api_key: str,
        base_url: str | None = None,
    ) -> OpenAISDKResponsesTransport:
        _require_secret(api_key, name="api_key")
        client = AsyncOpenAI(
            api_key=api_key,
            base_url=base_url,
            max_retries=_OPENAI_SDK_MAX_RETRIES,
        )
        return cls(client)

    async def create(self, request: OpenAIResponsesWireRequest) -> OpenAIResponsesWireResponse:
        if request.model != OPENAI_TERRA_MODEL:
            raise OpenAITransportError(
                OpenAITransportErrorKind.INVALID_REQUEST,
                code="unexpected_provider_model",
            )

        text_config = _structured_text_config(request)
        try:
            if text_config is None:
                response = await self._client.responses.create(
                    model=request.model,
                    input=request.input_text,
                    instructions=request.instructions,
                    max_output_tokens=request.max_output_tokens,
                    reasoning={"effort": _OPENAI_REASONING_EFFORT},
                    service_tier=_OPENAI_SERVICE_TIER,
                    store=False,
                    stream=False,
                    background=False,
                    tools=[],
                    truncation=_OPENAI_TRUNCATION,
                    timeout=request.timeout_seconds,
                )
            else:
                response = await self._client.responses.create(
                    model=request.model,
                    input=request.input_text,
                    instructions=request.instructions,
                    max_output_tokens=request.max_output_tokens,
                    reasoning={"effort": _OPENAI_REASONING_EFFORT},
                    service_tier=_OPENAI_SERVICE_TIER,
                    store=False,
                    stream=False,
                    background=False,
                    tools=[],
                    text=text_config,
                    truncation=_OPENAI_TRUNCATION,
                    timeout=request.timeout_seconds,
                )
        except openai.APIError as exc:
            raise _transport_error(exc) from exc

        return _wire_response(response)

    async def close(self) -> None:
        await self._client.close()
