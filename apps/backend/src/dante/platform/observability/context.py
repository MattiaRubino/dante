"""Request and distributed-trace correlation without business identity."""

from collections.abc import Iterator
from contextlib import contextmanager
from contextvars import ContextVar

from opentelemetry.trace import get_current_span

_REQUEST_ID: ContextVar[str | None] = ContextVar("dante_request_id", default=None)


@contextmanager
def bind_request_id(request_id: str) -> Iterator[None]:
    """Bind one public support identifier to the current async context."""
    token = _REQUEST_ID.set(request_id)
    try:
        yield
    finally:
        _REQUEST_ID.reset(token)


def correlation_fields() -> dict[str, str]:
    """Return only safe request/trace correlation fields for structured logs."""
    fields: dict[str, str] = {}
    request_id = _REQUEST_ID.get()
    if request_id is not None:
        fields["request_id"] = request_id

    span_context = get_current_span().get_span_context()
    if span_context.is_valid:
        fields["trace_id"] = format(span_context.trace_id, "032x")
        fields["span_id"] = format(span_context.span_id, "016x")
    return fields
