"""Privacy, bounds and correlation proofs for structured application logs."""

import json
import logging
import stat
from pathlib import Path
from typing import cast

from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter

from dante.platform.config.observability import ObservabilitySettings
from dante.platform.observability.context import bind_request_id
from dante.platform.observability.logging import (
    DanteJsonFormatter,
    configure_logging,
    redact_text,
)

_EMAIL = "person@example.com"
_REQUEST_ID = "019d0000-0000-7000-8000-000000000001"


def _record(message: str) -> logging.LogRecord:
    return logging.LogRecord(
        name="dante.test",
        level=logging.ERROR,
        pathname=__file__,
        lineno=1,
        msg=message,
        args=(),
        exc_info=None,
    )


def _payload(formatter: DanteJsonFormatter, record: logging.LogRecord) -> dict[str, object]:
    return cast(dict[str, object], json.loads(formatter.format(record)))


def test_redact_text_removes_credentials_pii_queries_and_control_characters() -> None:
    reference = "019d0000-0000-7000-8000-000000000001"
    value = (
        "Bearer top.secret-token for person@example.com "
        "at postgres://runtime:database-secret@db.example/dante "
        "and https://dante.example/path?token=private#fragment "
        f"csrf=unstructured-secret ref={reference} ip=203.0.113.42 ipv6=2001:db8::1 "
        "jwt=eyJhbGciOiJIUzI1NiJ9.cGF5bG9hZA.c2lnbmF0dXJl\x00"
    )

    redacted = redact_text(value, maximum_characters=2_048)

    assert "top.secret-token" not in redacted
    assert _EMAIL not in redacted
    assert "runtime:database-secret" not in redacted
    assert "token=private" not in redacted
    assert "fragment" not in redacted
    assert "unstructured-secret" not in redacted
    assert reference not in redacted
    assert "203.0.113.42" not in redacted
    assert "2001:db8::1" not in redacted
    assert "eyJhbGciOiJIUzI1NiJ9" not in redacted
    assert "\x00" not in redacted


def test_redact_text_does_not_mistake_a_timestamp_for_an_ipv6_address() -> None:
    redacted = redact_text("completed at 14:15:17", maximum_characters=2_048)

    assert redacted == "completed at 14:15:17"


def test_formatter_drops_arbitrary_fields_and_never_serializes_exception_messages() -> None:
    formatter = DanteJsonFormatter(maximum_message_characters=512)
    record = _record(f"signin failed for {_EMAIL}")
    record.__dict__["dante_fields"] = {
        "outcome": "invalid_credentials",
        "http_route": "/api/v1/auth/signin",
        "email": _EMAIL,
        "raw_payload": "never-export-this",
    }
    record.__dict__["dante_exception_type"] = "DatabaseUnavailable"

    payload = _payload(formatter, record)
    serialized = json.dumps(payload)

    assert payload["outcome"] == "invalid_credentials"
    assert payload["http_route"] == "/api/v1/auth/signin"
    assert payload["exception_type"] == "DatabaseUnavailable"
    assert _EMAIL not in serialized
    assert "raw_payload" not in payload
    assert "never-export-this" not in serialized


def test_formatter_correlates_request_and_trace_without_business_identity() -> None:
    formatter = DanteJsonFormatter(maximum_message_characters=512)
    exporter = InMemorySpanExporter()
    provider = TracerProvider()
    provider.add_span_processor(SimpleSpanProcessor(exporter))
    tracer = provider.get_tracer("dante.test")

    try:
        with tracer.start_as_current_span("test-span") as span, bind_request_id(_REQUEST_ID):
            payload = _payload(formatter, _record("safe.event"))
            context = span.get_span_context()

        assert payload["request_id"] == _REQUEST_ID
        assert payload["trace_id"] == format(context.trace_id, "032x")
        assert payload["span_id"] == format(context.span_id, "016x")
        assert set(payload).isdisjoint({"email", "account_ref", "session_id", "user"})
    finally:
        provider.shutdown()


def test_formatter_bounds_the_emitted_event() -> None:
    formatter = DanteJsonFormatter(maximum_message_characters=256)

    payload = _payload(formatter, _record("x" * 1_000))

    event = cast(str, payload["event"])
    assert event.endswith("…[TRUNCATED]")
    assert len(event) < 280


def test_rotating_log_file_is_created_with_private_mode(tmp_path: Path) -> None:
    log_path = tmp_path / "nested" / "backend.jsonl"
    runtime = configure_logging(ObservabilitySettings(log_file=log_path))

    try:
        assert stat.S_IMODE(log_path.stat().st_mode) == 0o640
    finally:
        runtime.close()
