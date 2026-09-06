"""ASGI boundary proofs for low-cardinality HTTP telemetry."""

import asyncio
from types import SimpleNamespace
from typing import cast

import pytest
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter
from starlette.types import Message, Receive, Scope, Send

from dante.platform.config.observability import ObservabilitySettings
from dante.platform.observability.middleware import ObservabilityMiddleware
from dante.platform.observability.runtime import ObservabilityRuntime


class RecordingHttpTelemetry:
    def __init__(self) -> None:
        self.active: list[tuple[int, str]] = []
        self.completed: list[tuple[str, str, int, float]] = []

    def change_active(self, amount: int, *, method: str) -> None:
        self.active.append((amount, method))

    def complete(self, *, method: str, route: str, status_code: int, duration: float) -> None:
        self.completed.append((method, route, status_code, duration))


def _runtime(
    provider: TracerProvider,
    telemetry: RecordingHttpTelemetry,
    *,
    trace_health_checks: bool = False,
) -> ObservabilityRuntime:
    return cast(
        ObservabilityRuntime,
        SimpleNamespace(
            settings=ObservabilitySettings(trace_health_checks=trace_health_checks),
            tracer=provider.get_tracer("dante.test"),
            http=telemetry,
        ),
    )


async def _invoke(
    runtime: ObservabilityRuntime,
    *,
    path: str,
    route: str,
    method: str = "GET",
    status_code: int = 200,
    headers: list[tuple[bytes, bytes]] | None = None,
) -> list[Message]:
    scope = cast(
        Scope,
        {
            "type": "http",
            "asgi": {"version": "3.0", "spec_version": "2.3"},
            "http_version": "1.1",
            "method": method,
            "scheme": "https",
            "path": path,
            "raw_path": path.encode(),
            "query_string": b"email=person@example.com",
            "root_path": "",
            "headers": headers or [],
            "client": ("127.0.0.1", 1234),
            "server": ("dante.test", 443),
        },
    )
    sent: list[Message] = []

    async def receive() -> Message:
        return {"type": "http.request", "body": b"", "more_body": False}

    async def send(message: Message) -> None:
        sent.append(message)

    async def routed_app(inner_scope: Scope, inner_receive: Receive, inner_send: Send) -> None:
        del inner_receive
        inner_scope["route"] = SimpleNamespace(path=route)
        await inner_send({"type": "http.response.start", "status": status_code, "headers": []})
        await inner_send({"type": "http.response.body", "body": b"", "more_body": False})

    middleware = ObservabilityMiddleware(routed_app, runtime=runtime)
    await middleware(scope, receive, send)
    return sent


@pytest.mark.asyncio
async def test_http_span_uses_only_the_route_template_and_bounded_method() -> None:
    exporter = InMemorySpanExporter()
    provider = TracerProvider()
    provider.add_span_processor(SimpleSpanProcessor(exporter))
    telemetry = RecordingHttpTelemetry()
    runtime = _runtime(provider, telemetry)

    try:
        messages = await _invoke(
            runtime,
            path="/people/person@example.com",
            route="/people/{person_ref}",
            method="GET",
            status_code=201,
        )
        spans = exporter.get_finished_spans()

        assert messages[0]["status"] == 201
        assert telemetry.active == [(1, "GET"), (-1, "GET")]
        assert telemetry.completed[0][:3] == ("GET", "/people/{person_ref}", 201)
        assert len(spans) == 1
        assert spans[0].name == "GET /people/{person_ref}"
        assert spans[0].attributes is not None
        assert spans[0].attributes["http.route"] == "/people/{person_ref}"
        assert "person@example.com" not in str(spans[0].attributes)
    finally:
        provider.shutdown()


@pytest.mark.asyncio
async def test_health_request_keeps_metrics_but_skips_spans_by_default() -> None:
    exporter = InMemorySpanExporter()
    provider = TracerProvider()
    provider.add_span_processor(SimpleSpanProcessor(exporter))
    telemetry = RecordingHttpTelemetry()
    runtime = _runtime(provider, telemetry)

    try:
        await _invoke(runtime, path="/health/ready", route="/health/ready")

        assert exporter.get_finished_spans() == ()
        assert telemetry.completed[0][:3] == ("GET", "/health/ready", 200)
    finally:
        provider.shutdown()


@pytest.mark.asyncio
async def test_duplicate_trace_context_is_ignored_without_rejecting_the_request() -> None:
    exporter = InMemorySpanExporter()
    provider = TracerProvider()
    provider.add_span_processor(SimpleSpanProcessor(exporter))
    telemetry = RecordingHttpTelemetry()
    runtime = _runtime(provider, telemetry)
    duplicate = [
        (b"traceparent", b"00-11111111111111111111111111111111-2222222222222222-01"),
        (b"traceparent", b"00-33333333333333333333333333333333-4444444444444444-01"),
    ]

    try:
        await _invoke(runtime, path="/access", route="/access", headers=duplicate)
        spans = exporter.get_finished_spans()

        assert len(spans) == 1
        assert spans[0].parent is None
    finally:
        provider.shutdown()


@pytest.mark.asyncio
async def test_cancelled_request_is_not_classified_as_a_server_failure() -> None:
    exporter = InMemorySpanExporter()
    provider = TracerProvider()
    provider.add_span_processor(SimpleSpanProcessor(exporter))
    telemetry = RecordingHttpTelemetry()
    runtime = _runtime(provider, telemetry)
    scope = cast(
        Scope,
        {
            "type": "http",
            "method": "GET",
            "path": "/access",
            "headers": [],
        },
    )

    async def cancelled_app(_scope: Scope, _receive: Receive, _send: Send) -> None:
        _scope["route"] = SimpleNamespace(path="/access")
        raise asyncio.CancelledError

    async def receive() -> Message:
        return {"type": "http.request", "body": b"", "more_body": False}

    async def send(_message: Message) -> None:
        return None

    try:
        middleware = ObservabilityMiddleware(cancelled_app, runtime=runtime)
        with pytest.raises(asyncio.CancelledError):
            await middleware(scope, receive, send)

        spans = exporter.get_finished_spans()
        assert telemetry.active == [(1, "GET"), (-1, "GET")]
        assert telemetry.completed[0][:3] == ("GET", "/access", 499)
        assert len(spans) == 1
        assert spans[0].status.status_code.name == "UNSET"
        assert [event.name for event in spans[0].events] == ["dante.request_cancelled"]
    finally:
        provider.shutdown()
