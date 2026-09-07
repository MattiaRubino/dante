"""Private first-party API cache-policy regression proofs."""

from __future__ import annotations

from typing import cast

import pytest
from starlette.types import ASGIApp, Message, Receive, Scope, Send

from dante.platform.http.problem import RequestContextMiddleware


class _OkApp:
    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        _ = scope, receive
        await send({"type": "http.response.start", "status": 200, "headers": []})
        await send({"type": "http.response.body", "body": b"{}"})


def _scope(path: str) -> Scope:
    return cast(
        Scope,
        {
            "type": "http",
            "asgi": {"version": "3.0", "spec_version": "2.3"},
            "http_version": "1.1",
            "server": ("dante.test", 443),
            "client": ("127.0.0.1", 54321),
            "scheme": "https",
            "method": "GET",
            "root_path": "",
            "path": path,
            "raw_path": path.encode("ascii"),
            "query_string": b"",
            "headers": [],
            "state": {"request_id": "test-request-id"},
        },
    )


async def _headers_for(path: str) -> dict[bytes, bytes]:
    messages: list[Message] = []

    async def receive() -> Message:
        return {"type": "http.request", "body": b"", "more_body": False}

    async def send(message: Message) -> None:
        messages.append(message)

    middleware = RequestContextMiddleware(cast(ASGIApp, _OkApp()))
    await middleware(_scope(path), receive, send)

    start = next(message for message in messages if message["type"] == "http.response.start")
    return dict(start["headers"])


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "path",
    [
        "/api/v1/auth/session",
        "/api/v1/temporal/timeline/window",
    ],
)
async def test_private_first_party_api_responses_are_no_store(path: str) -> None:
    headers = await _headers_for(path)

    assert headers[b"cache-control"] == b"no-store"
    assert headers[b"x-request-id"] == b"test-request-id"


@pytest.mark.asyncio
async def test_unrelated_public_path_is_not_forced_into_private_cache_policy() -> None:
    headers = await _headers_for("/health/live")

    assert b"cache-control" not in headers
    assert headers[b"x-request-id"] == b"test-request-id"
