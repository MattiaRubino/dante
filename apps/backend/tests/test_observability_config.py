"""Executable bounds for the operational telemetry configuration."""

from pathlib import Path

import pytest
from pydantic import ValidationError

from dante.platform.config.observability import ObservabilitySettings


def test_observability_defaults_are_local_and_fail_closed() -> None:
    settings = ObservabilitySettings()

    assert settings.enabled is False
    assert settings.otlp_http_endpoint == "http://127.0.0.1:4318"
    assert settings.trace_sample_ratio == 0.10
    assert settings.trace_health_checks is False
    assert settings.log_file is None


@pytest.mark.parametrize(
    ("raw", "normalized"),
    [
        ("HTTPS://OTEL.EXAMPLE.TEST:443/otlp/", "https://otel.example.test/otlp"),
        ("http://[::1]:4318/", "http://[::1]:4318"),
    ],
)
def test_otlp_endpoint_is_normalized_without_credentials(raw: str, normalized: str) -> None:
    settings = ObservabilitySettings(otlp_http_endpoint=raw)

    assert settings.otlp_http_endpoint == normalized


@pytest.mark.parametrize(
    "endpoint",
    [
        "ftp://otel.example.test",
        "https://user:secret@otel.example.test",
        "https://otel.example.test/path",
        "https://otel.example.test?token=secret",
        "https://otel.example.test#secret",
        "http://otel.example.test:not-a-port",
    ],
)
def test_otlp_endpoint_rejects_unsafe_or_ambiguous_values(endpoint: str) -> None:
    with pytest.raises(ValidationError):
        ObservabilitySettings(otlp_http_endpoint=endpoint)


def test_export_batch_cannot_exceed_its_bounded_queue() -> None:
    with pytest.raises(ValidationError, match="span_max_export_batch_size"):
        ObservabilitySettings(
            span_max_queue_size=128,
            span_max_export_batch_size=129,
        )


def test_log_file_requires_a_file_shaped_path() -> None:
    with pytest.raises(ValidationError, match="log_file"):
        ObservabilitySettings(log_file=Path())
