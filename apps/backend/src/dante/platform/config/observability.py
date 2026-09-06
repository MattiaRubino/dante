"""Validated production configuration for DANTE operational telemetry."""

from enum import StrEnum
from pathlib import Path
from typing import Annotated, Self
from urllib.parse import urlsplit, urlunsplit

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    StringConstraints,
    field_validator,
    model_validator,
)

PositiveFloat = Annotated[float, Field(gt=0)]
PositiveInt = Annotated[int, Field(gt=0)]
SamplingRatio = Annotated[float, Field(ge=0, le=1)]
NonBlankText = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]


class LogLevel(StrEnum):
    """Supported application logging thresholds."""

    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


class ObservabilitySettings(BaseModel):
    """Immutable, bounded observability policy embedded in process settings."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    enabled: bool = False
    otlp_http_endpoint: str = "http://127.0.0.1:4318"
    trace_sample_ratio: SamplingRatio = 0.10
    trace_health_checks: bool = False
    export_timeout_seconds: Annotated[float, Field(gt=0, le=30)] = 3.0
    shutdown_timeout_seconds: Annotated[float, Field(gt=0, le=30)] = 5.0
    metric_export_interval_seconds: Annotated[int, Field(ge=5, le=300)] = 30
    span_schedule_delay_milliseconds: Annotated[int, Field(ge=100, le=30_000)] = 5_000
    span_max_queue_size: Annotated[int, Field(ge=128, le=65_536)] = 2_048
    span_max_export_batch_size: Annotated[int, Field(ge=1, le=2_048)] = 256

    log_level: LogLevel = LogLevel.INFO
    log_file: Path | None = None
    log_file_max_bytes: Annotated[int, Field(ge=1_048_576, le=1_073_741_824)] = 10_485_760
    log_file_backup_count: Annotated[int, Field(ge=1, le=20)] = 5
    log_message_max_characters: Annotated[int, Field(ge=256, le=16_384)] = 2_048

    @field_validator("otlp_http_endpoint")
    @classmethod
    def validate_otlp_http_endpoint(cls, value: str) -> str:
        """Accept one credential-free OTLP/HTTP base endpoint."""
        candidate = value.strip()
        parts = urlsplit(candidate)
        if parts.scheme not in {"http", "https"}:
            raise ValueError("otlp_http_endpoint must use http or https")
        if parts.hostname is None or parts.username is not None or parts.password is not None:
            raise ValueError("otlp_http_endpoint must be a credential-free network endpoint")
        if parts.query or parts.fragment:
            raise ValueError("otlp_http_endpoint must not contain query or fragment")

        normalized_path = parts.path.rstrip("/")
        if normalized_path not in {"", "/otlp"}:
            raise ValueError("otlp_http_endpoint path must be empty or /otlp")

        try:
            port = parts.port
        except ValueError as exc:
            raise ValueError("otlp_http_endpoint contains an invalid port") from exc

        host = parts.hostname.lower()
        host_for_authority = f"[{host}]" if ":" in host else host
        default_port = 443 if parts.scheme == "https" else 80
        authority = (
            host_for_authority if port in {None, default_port} else f"{host_for_authority}:{port}"
        )
        return urlunsplit((parts.scheme, authority, normalized_path, "", ""))

    @field_validator("log_file")
    @classmethod
    def validate_log_file(cls, value: Path | None) -> Path | None:
        """Reject ambiguous directory-shaped log destinations."""
        if value is None:
            return None
        if not value.name or value.name in {".", ".."}:
            raise ValueError("log_file must identify a file")
        return value

    @model_validator(mode="after")
    def validate_batch_bounds(self) -> Self:
        """Keep the exporter queue bounded and internally coherent."""
        if self.span_max_export_batch_size > self.span_max_queue_size:
            raise ValueError("span_max_export_batch_size cannot exceed span_max_queue_size")
        return self
