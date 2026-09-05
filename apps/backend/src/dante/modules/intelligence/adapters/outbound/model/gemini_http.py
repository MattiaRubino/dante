"""Private HTTP transport for Google Gemini Interactions API.

The API key is constructor-only and never enters DANTE contracts, route artifacts or logs.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Protocol, cast

import httpx2

from dante.modules.intelligence.adapters.outbound.model.gemini_interactions import (
    GeminiInteractionStatus,
    GeminiInteractionsWireRequest,
    GeminiInteractionsWireResponse,
    GeminiTransportError,
    GeminiTransportErrorKind,
)


class _HttpResponse(Protocol):
    status_code: int
    headers: Mapping[str, str]

    def json(self) -> object: ...


class _AsyncHttpClient(Protocol):
    async def post(
        self,
        url: str,
        *,
        headers: Mapping[str, str],
        json: object,
        timeout: float,
    ) -> _HttpResponse: ...

    async def aclose(self) -> None: ...


def _text(value: object, *, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise GeminiTransportError(GeminiTransportErrorKind.INVALID_RESPONSE, code=field)
    return value


def _optional_text(value: object, *, field: str) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str) or not value.strip():
        raise GeminiTransportError(GeminiTransportErrorKind.INVALID_RESPONSE, code=field)
    return value


def _optional_nonnegative_int(value: object) -> int | None:
    if value is None:
        return None
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise GeminiTransportError(
            GeminiTransportErrorKind.INVALID_RESPONSE,
            code="invalid_usage_count",
        )
    return value


def _error_kind(status_code: int) -> GeminiTransportErrorKind:
    if status_code == 400:
        return GeminiTransportErrorKind.INVALID_REQUEST
    if status_code == 401:
        return GeminiTransportErrorKind.AUTHENTICATION
    if status_code == 403:
        return GeminiTransportErrorKind.PERMISSION
    if status_code == 404:
        return GeminiTransportErrorKind.NOT_FOUND
    if status_code == 409:
        return GeminiTransportErrorKind.CONFLICT
    if status_code == 429:
        return GeminiTransportErrorKind.RATE_LIMIT
    if status_code >= 500:
        return GeminiTransportErrorKind.SERVER
    return GeminiTransportErrorKind.UNKNOWN


def _error_code_from_object(value: object) -> str | None:
    if not isinstance(value, dict):
        return None
    for key in ("status", "code", "reason"):
        candidate = value.get(key)
        if isinstance(candidate, str) and candidate.strip():
            return candidate
        if isinstance(candidate, int) and not isinstance(candidate, bool):
            return str(candidate)
    return None


def _provider_error_code(payload: object) -> str | None:
    if not isinstance(payload, dict):
        return None
    direct = _error_code_from_object(payload.get("error"))
    if direct is not None:
        return direct
    errors = payload.get("errors")
    if isinstance(errors, list):
        for error in errors:
            code = _error_code_from_object(error)
            if code is not None:
                return code
    return None


def _model_output_text(payload: dict[str, object]) -> str | None:
    steps = payload.get("steps")
    if not isinstance(steps, list):
        return None
    chunks: list[str] = []
    for step in steps:
        if not isinstance(step, dict) or step.get("type") != "model_output":
            continue
        content = step.get("content")
        if not isinstance(content, list):
            continue
        for block in content:
            if not isinstance(block, dict) or block.get("type") != "text":
                continue
            text = block.get("text")
            if isinstance(text, str):
                chunks.append(text)
    if not chunks:
        return None
    return "".join(chunks)


def _request_payload(request: GeminiInteractionsWireRequest) -> dict[str, object]:
    payload: dict[str, object] = {
        "model": request.model,
        "input": request.input_text,
        "stream": request.stream,
        "store": request.store,
        "background": request.background,
        "service_tier": request.service_tier,
        "generation_config": {
            "max_output_tokens": request.max_output_tokens,
            "thinking_level": request.thinking_level,
            "thinking_summaries": request.thinking_summaries,
            "tool_choice": request.tool_choice,
        },
    }
    if request.system_instruction is not None:
        payload["system_instruction"] = request.system_instruction
    if request.structured_output_schema is not None:
        payload["response_format"] = {
            "type": "text",
            "mime_type": "application/json",
            "schema": request.structured_output_schema,
        }
    return payload


class GeminiInteractionsHttpTransport:
    """Unary, stateless, no-retry Interactions API transport."""

    def __init__(self, api_key: str, *, client: _AsyncHttpClient | None = None) -> None:
        if not api_key or not api_key.strip():
            raise ValueError("Gemini API key must be non-empty")
        self._api_key = api_key
        if client is None:
            self._client = cast(_AsyncHttpClient, httpx2.AsyncClient())
            self._owns_client = True
        else:
            self._client = client
            self._owns_client = False

    async def create(
        self,
        request: GeminiInteractionsWireRequest,
    ) -> GeminiInteractionsWireResponse:
        headers = {
            "x-goog-api-key": self._api_key,
            "content-type": "application/json",
            # Retained as an explicit schema marker. Google's post-June-2026 service may ignore
            # this header because the May-20 schema is now the only supported Interactions shape.
            "Api-Revision": request.api_revision,
        }
        try:
            response = await self._client.post(
                request.endpoint,
                headers=headers,
                json=_request_payload(request),
                timeout=request.timeout_seconds,
            )
        except httpx2.TimeoutException as exc:
            raise GeminiTransportError(GeminiTransportErrorKind.TIMEOUT) from exc
        except httpx2.ConnectError as exc:
            raise GeminiTransportError(GeminiTransportErrorKind.CONNECTION) from exc
        except httpx2.RequestError as exc:
            raise GeminiTransportError(GeminiTransportErrorKind.CONNECTION) from exc

        request_id = response.headers.get("x-request-id") or response.headers.get(
            "x-goog-request-id"
        )
        try:
            payload = response.json()
        except ValueError as exc:
            raise GeminiTransportError(
                GeminiTransportErrorKind.INVALID_RESPONSE,
                code="response_not_json",
                request_id=request_id,
            ) from exc

        if not 200 <= response.status_code < 300:
            raise GeminiTransportError(
                _error_kind(response.status_code),
                code=_provider_error_code(payload),
                request_id=request_id,
            )
        if not isinstance(payload, dict):
            raise GeminiTransportError(
                GeminiTransportErrorKind.INVALID_RESPONSE,
                code="response_root_not_object",
                request_id=request_id,
            )
        document = cast(dict[str, object], payload)
        try:
            status = GeminiInteractionStatus(_text(document.get("status"), field="missing_status"))
        except ValueError as exc:
            raise GeminiTransportError(
                GeminiTransportErrorKind.INVALID_RESPONSE,
                code="unknown_interaction_status",
                request_id=request_id,
            ) from exc

        usage_raw = document.get("usage")
        usage = cast(dict[str, object], usage_raw) if isinstance(usage_raw, dict) else {}
        return GeminiInteractionsWireResponse(
            status=status,
            interaction_id=_text(document.get("id"), field="missing_interaction_id"),
            request_id=request_id,
            output_text=_model_output_text(document),
            input_tokens=_optional_nonnegative_int(usage.get("total_input_tokens")),
            output_tokens=_optional_nonnegative_int(usage.get("total_output_tokens")),
            thought_tokens=_optional_nonnegative_int(usage.get("total_thought_tokens")),
            cached_tokens=_optional_nonnegative_int(usage.get("total_cached_tokens")),
            tool_use_tokens=_optional_nonnegative_int(usage.get("total_tool_use_tokens")),
            total_tokens=_optional_nonnegative_int(usage.get("total_tokens")),
            model=_optional_text(document.get("model"), field="invalid_model"),
            service_tier=_optional_text(
                document.get("service_tier"), field="invalid_service_tier"
            ),
            error_code=_provider_error_code(document),
        )

    async def close(self) -> None:
        if self._owns_client:
            await self._client.aclose()
