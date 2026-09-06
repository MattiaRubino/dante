"""Privacy-safe HTTP tracing and RED metrics at the ASGI boundary."""

from __future__ import annotations

import asyncio
from time import perf_counter
from typing import cast

from opentelemetry.context import Context
from opentelemetry.propagators.textmap import DefaultGetter
from opentelemetry.trace import Span, SpanKind, Status, StatusCode
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator
from starlette.types import ASGIApp, Message, Receive, Scope, Send

from dante.platform.observability.runtime import ObservabilityRuntime

_PROPAGATOR = TraceContextTextMapPropagator()
_GETTER = DefaultGetter()
_METHODS = frozenset({"DELETE", "GET", "HEAD", "OPTIONS", "PATCH", "POST", "PUT"})


def _method(scope: Scope) -> str:
    candidate = str(scope.get("method", "OTHER")).upper()
    return candidate if candidate in _METHODS else "OTHER"


def _parent_context(scope: Scope) -> Context | None:
    raw_headers = cast(list[tuple[bytes, bytes]], scope.get("headers", []))
    carrier: dict[str, str] = {}
    for accepted_name in (b"traceparent", b"tracestate"):
        values = [value for name, value in raw_headers if name.lower() == accepted_name]
        if len(values) > 1:
            return None
        if values:
            try:
                carrier[accepted_name.decode("ascii")] = values[0].decode("ascii")
            except UnicodeDecodeError:
                return None
    return _PROPAGATOR.extract(carrier, getter=_GETTER) if carrier else None


def _route_template(scope: Scope) -> str:
    route = scope.get("route")
    candidate = getattr(route, "path", None)
    if isinstance(candidate, str) and candidate.startswith("/") and len(candidate) <= 160:
        return candidate
    return "unmatched"


class ObservabilityMiddleware:
    """Record HTTP telemetry without URLs, query strings, headers or bodies."""

    def __init__(self, app: ASGIApp, *, runtime: ObservabilityRuntime) -> None:
        self._app = app
        self._runtime = runtime

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self._app(scope, receive, send)
            return

        method = _method(scope)
        path = str(scope.get("path", ""))
        if path.startswith("/health/") and not self._runtime.settings.trace_health_checks:
            await self._record_request(scope, receive, send, method=method, span=None)
            return

        with self._runtime.tracer.start_as_current_span(
            f"HTTP {method}",
            context=_parent_context(scope),
            kind=SpanKind.SERVER,
            record_exception=False,
            set_status_on_exception=False,
        ) as span:
            span.set_attribute("http.request.method", method)
            await self._record_request(scope, receive, send, method=method, span=span)

    async def _record_request(
        self,
        scope: Scope,
        receive: Receive,
        send: Send,
        *,
        method: str,
        span: Span | None,
    ) -> None:
        started = perf_counter()
        status_code = 500
        self._runtime.http.change_active(1, method=method)

        async def send_with_status(message: Message) -> None:
            nonlocal status_code
            if message["type"] == "http.response.start":
                status_code = int(message["status"])
            await send(message)

        try:
            await self._app(scope, receive, send_with_status)
        except asyncio.CancelledError:
            status_code = 499
            if span is not None and span.is_recording():
                span.add_event("dante.request_cancelled")
            raise
        except Exception as exc:
            if span is not None and span.is_recording():
                span.set_status(Status(StatusCode.ERROR))
                span.add_event("dante.unhandled_exception", {"exception.type": type(exc).__name__})
            raise
        finally:
            duration = perf_counter() - started
            route = _route_template(scope)
            self._runtime.http.change_active(-1, method=method)
            self._runtime.http.complete(
                method=method,
                route=route,
                status_code=status_code,
                duration=duration,
            )
            if span is not None and span.is_recording():
                span.update_name(f"{method} {route}")
                span.set_attribute("http.route", route)
                span.set_attribute("http.response.status_code", status_code)
                if status_code >= 500:
                    span.set_status(Status(StatusCode.ERROR))
