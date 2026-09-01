"""Focused pre-routing HTTP security and bounded-body proof for Access/Auth."""

from __future__ import annotations

from typing import cast

import pytest
from starlette.types import ASGIApp, Message, Receive, Scope, Send

from dante.auth.dependencies import AuthRequestBodyLimitMiddleware, BrowserAuthSecurityMiddleware
from dante.auth.sessions import WEB_CLIENT_HEADER_NAME, WEB_CLIENT_HEADER_VALUE

_CANONICAL_ORIGIN = "https://dante.test"


class _RecorderApp:
    def __init__(self) -> None:
        self.calls = 0
        self.bodies: list[bytes] = []

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        self.calls += 1
        chunks: list[bytes] = []
        while True:
            message = await receive()
            if message["type"] == "http.disconnect":
                break
            assert message["type"] == "http.request"
            chunks.append(message.get("body", b""))
            if not message.get("more_body", False):
                break
        self.bodies.append(b"".join(chunks))
        await send({"type": "http.response.start", "status": 204, "headers": []})
        await send({"type": "http.response.body", "body": b""})


def _scope(
    *,
    method: str = "POST",
    path: str = "/api/v1/auth/future",
    headers: tuple[tuple[bytes, bytes], ...] = (),
) -> Scope:
    return cast(
        Scope,
        {
            "type": "http",
            "asgi": {"version": "3.0", "spec_version": "2.3"},
            "http_version": "1.1",
            "server": ("dante.test", 443),
            "client": ("127.0.0.1", 54321),
            "scheme": "https",
            "method": method,
            "root_path": "",
            "path": path,
            "raw_path": path.encode("ascii"),
            "query_string": b"",
            "headers": list(headers),
            "state": {"request_id": "test-request-id"},
        },
    )


def _browser_headers(
    *, content_type: bytes = b"application/json"
) -> tuple[tuple[bytes, bytes], ...]:
    return (
        (b"origin", _CANONICAL_ORIGIN.encode("ascii")),
        (b"sec-fetch-site", b"same-origin"),
        (WEB_CLIENT_HEADER_NAME.lower().encode("ascii"), WEB_CLIENT_HEADER_VALUE.encode("ascii")),
        (b"content-type", content_type),
    )


async def _invoke(
    app: ASGIApp,
    scope: Scope,
    messages: list[Message] | None = None,
) -> tuple[list[Message], int]:
    queue = list(messages or [{"type": "http.request", "body": b"", "more_body": False}])
    sent: list[Message] = []
    receive_calls = 0

    async def receive() -> Message:
        nonlocal receive_calls
        receive_calls += 1
        if queue:
            return queue.pop(0)
        return {"type": "http.disconnect"}

    async def send(message: Message) -> None:
        sent.append(message)

    await app(scope, receive, send)
    return sent, receive_calls


def _status(messages: list[Message]) -> int:
    start = next(message for message in messages if message["type"] == "http.response.start")
    return int(start["status"])


@pytest.mark.asyncio
async def test_future_auth_mutation_is_protected_before_request_body_is_read() -> None:
    recorder = _RecorderApp()
    middleware = BrowserAuthSecurityMiddleware(
        cast(ASGIApp, recorder),
        canonical_web_origin=_CANONICAL_ORIGIN,
    )

    sent, receive_calls = await _invoke(
        middleware,
        _scope(headers=((b"content-type", b"application/json"),)),
        [{"type": "http.request", "body": b'{"secret":"must-not-be-read"}'}],
    )

    assert _status(sent) == 403
    assert receive_calls == 0
    assert recorder.calls == 0


@pytest.mark.asyncio
async def test_valid_first_party_json_mutation_reaches_application() -> None:
    recorder = _RecorderApp()
    middleware = BrowserAuthSecurityMiddleware(
        cast(ASGIApp, recorder),
        canonical_web_origin=_CANONICAL_ORIGIN,
    )

    sent, _receive_calls = await _invoke(
        middleware,
        _scope(headers=_browser_headers()),
        [{"type": "http.request", "body": b"{}", "more_body": False}],
    )

    assert _status(sent) == 204
    assert recorder.calls == 1
    assert recorder.bodies == [b"{}"]


@pytest.mark.asyncio
async def test_apple_callback_is_the_reviewed_external_browser_ingress_exception() -> None:
    recorder = _RecorderApp()
    middleware = BrowserAuthSecurityMiddleware(
        cast(ASGIApp, recorder),
        canonical_web_origin=_CANONICAL_ORIGIN,
    )

    sent, _receive_calls = await _invoke(
        middleware,
        _scope(
            path="/api/v1/auth/apple/callback",
            headers=((b"content-type", b"application/x-www-form-urlencoded"),),
        ),
        [{"type": "http.request", "body": b"state=opaque", "more_body": False}],
    )

    assert _status(sent) == 204
    assert recorder.calls == 1


@pytest.mark.asyncio
async def test_declared_oversized_auth_body_is_rejected_without_reading_transport() -> None:
    recorder = _RecorderApp()
    middleware = AuthRequestBodyLimitMiddleware(cast(ASGIApp, recorder), max_body_bytes=8)

    sent, receive_calls = await _invoke(
        middleware,
        _scope(headers=((b"content-length", b"9"),)),
        [{"type": "http.request", "body": b"123456789", "more_body": False}],
    )

    assert _status(sent) == 413
    assert receive_calls == 0
    assert recorder.calls == 0


@pytest.mark.asyncio
async def test_streamed_auth_body_cannot_bypass_size_bound() -> None:
    recorder = _RecorderApp()
    middleware = AuthRequestBodyLimitMiddleware(cast(ASGIApp, recorder), max_body_bytes=8)

    sent, receive_calls = await _invoke(
        middleware,
        _scope(),
        [
            {"type": "http.request", "body": b"12345", "more_body": True},
            {"type": "http.request", "body": b"67890", "more_body": False},
        ],
    )

    assert _status(sent) == 413
    assert receive_calls == 2
    assert recorder.calls == 0


@pytest.mark.asyncio
async def test_duplicate_or_noncanonical_content_length_fails_closed() -> None:
    for headers in (
        ((b"content-length", b"1"), (b"content-length", b"1")),
        ((b"content-length", b"+1"),),
        ((b"content-length", b" 1"),),
    ):
        recorder = _RecorderApp()
        middleware = AuthRequestBodyLimitMiddleware(cast(ASGIApp, recorder), max_body_bytes=8)

        sent, receive_calls = await _invoke(middleware, _scope(headers=headers))

        assert _status(sent) == 400
        assert receive_calls == 0
        assert recorder.calls == 0


@pytest.mark.asyncio
async def test_declared_content_length_must_match_buffered_request_body() -> None:
    recorder = _RecorderApp()
    middleware = AuthRequestBodyLimitMiddleware(cast(ASGIApp, recorder), max_body_bytes=8)

    sent, receive_calls = await _invoke(
        middleware,
        _scope(headers=((b"content-length", b"5"),)),
        [{"type": "http.request", "body": b"abc", "more_body": False}],
    )

    assert _status(sent) == 400
    assert receive_calls == 1
    assert recorder.calls == 0


@pytest.mark.asyncio
async def test_bounded_body_is_replayed_byte_exactly_to_application() -> None:
    recorder = _RecorderApp()
    middleware = AuthRequestBodyLimitMiddleware(cast(ASGIApp, recorder), max_body_bytes=8)

    sent, receive_calls = await _invoke(
        middleware,
        _scope(headers=((b"content-length", b"6"),)),
        [
            {"type": "http.request", "body": b"abc", "more_body": True},
            {"type": "http.request", "body": b"def", "more_body": False},
        ],
    )

    assert _status(sent) == 204
    assert receive_calls == 2
    assert recorder.calls == 1
    assert recorder.bodies == [b"abcdef"]
