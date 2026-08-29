"""Bounded JSON logging with correlation and deny-by-default field handling."""

from __future__ import annotations

import json
import logging
import math
import os
import re
import sys
from collections.abc import Mapping
from datetime import UTC, datetime
from io import TextIOWrapper
from logging.handlers import RotatingFileHandler
from pathlib import Path
from types import TracebackType
from typing import Any, Final, TextIO, cast, override

from dante.platform.config.observability import ObservabilitySettings
from dante.platform.observability.context import correlation_fields

_SAFE_EVENT_FIELDS: Final[frozenset[str]] = frozenset(
    {
        "build_id",
        "dependency",
        "duration_ms",
        "environment",
        "error_category",
        "error_code",
        "exception_type",
        "http_method",
        "http_route",
        "http_status_code",
        "outcome",
        "queue_state",
        "release_sha",
        "retryable",
        "service_name",
    }
)
_SENSITIVE_KEY = re.compile(
    r"(?:authorization|cookie|csrf|email|password|pepper|secret|session|token|verifier|"
    r"account_ref|identity_ref)",
    re.IGNORECASE,
)
_EMAIL = re.compile(r"(?<![\w.+-])[\w.+-]{1,64}@[A-Za-z0-9.-]{1,253}\.[A-Za-z]{2,63}")
_AUTHORIZATION = re.compile(r"\b(?:basic|bearer)\s+[A-Za-z0-9._~+/=-]+", re.IGNORECASE)
_SECRET_ASSIGNMENT = re.compile(
    r"\b(?:authorization|cookie|csrf|password|pepper|secret|token|verifier)"
    r"(?:\s*[:=]\s*|%3[dD])(?:[^\s,;]+)",
    re.IGNORECASE,
)
_JWT = re.compile(r"\beyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\b")
_UUID = re.compile(
    r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-8][0-9a-f]{3}-[89ab][0-9a-f]{3}-"
    r"[0-9a-f]{12}\b",
    re.IGNORECASE,
)
_IPV4 = re.compile(
    r"(?<![\d.])(?:25[0-5]|2[0-4]\d|1?\d?\d)"
    r"(?:\.(?:25[0-5]|2[0-4]\d|1?\d?\d)){3}(?![\d.])"
)
_IPV6 = re.compile(
    r"(?<![0-9A-Fa-f:])(?:"
    r"(?:[0-9A-Fa-f]{1,4}:){7}[0-9A-Fa-f]{1,4}|"
    r"[0-9A-Fa-f:]*::[0-9A-Fa-f:]*"
    r")"
    r"(?![0-9A-Fa-f:])"
)
_URL_QUERY = re.compile(r"(?P<base>https?://[^\s?#]+)(?:\?[^\s#]*)?(?:#[^\s]*)?", re.IGNORECASE)
_DSN_USERINFO = re.compile(r"(?P<scheme>postgres(?:ql)?(?:\+\w+)?://)[^\s/@]+@", re.IGNORECASE)
_CONTROL_CHARACTERS = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")


def redact_text(value: str, *, maximum_characters: int) -> str:
    """Remove common credential/PII forms and bound one emitted string."""
    redacted = _CONTROL_CHARACTERS.sub("�", value)
    redacted = _DSN_USERINFO.sub(r"\g<scheme>[REDACTED]@", redacted)
    redacted = _AUTHORIZATION.sub("[REDACTED_AUTHORIZATION]", redacted)
    redacted = _SECRET_ASSIGNMENT.sub("[REDACTED_SECRET]", redacted)
    redacted = _JWT.sub("[REDACTED_TOKEN]", redacted)
    redacted = _EMAIL.sub("[REDACTED_EMAIL]", redacted)
    redacted = _UUID.sub("[REDACTED_REFERENCE]", redacted)
    redacted = _IPV4.sub("[REDACTED_IP]", redacted)
    redacted = _IPV6.sub("[REDACTED_IP]", redacted)
    redacted = _URL_QUERY.sub(r"\g<base>", redacted)
    if len(redacted) > maximum_characters:
        return f"{redacted[:maximum_characters]}…[TRUNCATED]"
    return redacted


def _safe_primitive(value: object, *, maximum_characters: int) -> str | int | float | bool:
    if isinstance(value, float) and not math.isfinite(value):
        return "[NON_FINITE]"
    if isinstance(value, bool | int | float):
        return value
    return redact_text(str(value), maximum_characters=maximum_characters)


class DanteJsonFormatter(logging.Formatter):
    """Serialize a stable operational envelope without arbitrary LogRecord extras."""

    def __init__(self, *, maximum_message_characters: int) -> None:
        super().__init__()
        self._maximum_message_characters = maximum_message_characters

    @override
    def format(self, record: logging.LogRecord) -> str:
        timestamp = datetime.fromtimestamp(record.created, tz=UTC).isoformat(
            timespec="milliseconds"
        )
        try:
            message = record.getMessage()
        except Exception:  # noqa: BLE001 - hostile __str__ implementations cannot break logging
            message = "logging.unformattable_event"
        payload: dict[str, str | int | float | bool] = {
            "timestamp": timestamp,
            "severity": record.levelname.lower(),
            "logger": redact_text(record.name, maximum_characters=256),
            "event": redact_text(
                message,
                maximum_characters=self._maximum_message_characters,
            ),
        }
        payload.update(correlation_fields())

        raw_fields = getattr(record, "dante_fields", None)
        if isinstance(raw_fields, Mapping):
            for raw_key, raw_value in raw_fields.items():
                key = str(raw_key)
                if key not in _SAFE_EVENT_FIELDS or _SENSITIVE_KEY.search(key):
                    continue
                payload[key] = _safe_primitive(
                    raw_value,
                    maximum_characters=self._maximum_message_characters,
                )

        exception_type = getattr(record, "dante_exception_type", None)
        if (
            exception_type is None
            and record.exc_info is not None
            and record.exc_info[0] is not None
        ):
            exception_type = record.exc_info[0].__name__
        if exception_type is not None:
            payload["exception_type"] = redact_text(
                str(exception_type),
                maximum_characters=256,
            )

        return json.dumps(payload, ensure_ascii=False, separators=(",", ":"), sort_keys=True)


class _DanteStreamHandler(logging.StreamHandler[TextIO]):
    pass


class _DanteRotatingFileHandler(RotatingFileHandler):
    @override
    def _open(self) -> TextIOWrapper[Any]:
        descriptor = os.open(
            self.baseFilename,
            os.O_WRONLY | os.O_APPEND | os.O_CREAT | getattr(os, "O_NOFOLLOW", 0),
            0o640,
        )
        try:
            return cast(
                TextIOWrapper[Any],
                os.fdopen(
                    descriptor,
                    self.mode,
                    encoding=self.encoding,
                    errors=self.errors,
                ),
            )
        except BaseException:
            os.close(descriptor)
            raise


class LoggingRuntime:
    """Owned logging handlers that can be deterministically released."""

    def __init__(self, handlers: tuple[logging.Handler, ...]) -> None:
        self._handlers = handlers

    def close(self) -> None:
        root = logging.getLogger()
        for handler in self._handlers:
            root.removeHandler(handler)
            handler.flush()
            handler.close()

    def __enter__(self) -> LoggingRuntime:
        return self

    def __exit__(
        self,
        _exception_type: type[BaseException] | None,
        _exception: BaseException | None,
        _traceback: TracebackType | None,
    ) -> None:
        self.close()


def configure_logging(settings: ObservabilitySettings) -> LoggingRuntime:
    """Install one stdout-first JSON pipeline plus an optional bounded local file."""
    root = logging.getLogger()
    for existing in tuple(root.handlers):
        if isinstance(existing, _DanteStreamHandler | _DanteRotatingFileHandler):
            root.removeHandler(existing)
            existing.close()

    formatter = DanteJsonFormatter(maximum_message_characters=settings.log_message_max_characters)
    handlers: list[logging.Handler] = []

    stream_handler = _DanteStreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    handlers.append(stream_handler)

    if settings.log_file is not None:
        log_path = Path(settings.log_file)
        log_path.parent.mkdir(mode=0o750, parents=True, exist_ok=True)
        descriptor = os.open(
            log_path,
            os.O_WRONLY | os.O_APPEND | os.O_CREAT | getattr(os, "O_NOFOLLOW", 0),
            0o640,
        )
        os.close(descriptor)
        log_path.chmod(0o640, follow_symlinks=False)
        file_handler = _DanteRotatingFileHandler(
            log_path,
            maxBytes=settings.log_file_max_bytes,
            backupCount=settings.log_file_backup_count,
            encoding="utf-8",
            delay=True,
        )
        file_handler.setFormatter(formatter)
        handlers.append(file_handler)

    root.setLevel(settings.log_level.value.upper())
    for handler in handlers:
        handler.setLevel(settings.log_level.value.upper())
        root.addHandler(handler)

    logging.getLogger("opentelemetry").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.access").disabled = True
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    return LoggingRuntime(tuple(handlers))


def log_event(
    logger: logging.Logger,
    level: int,
    event: str,
    *,
    fields: Mapping[str, object] | None = None,
    exception: BaseException | None = None,
) -> None:
    """Emit one deny-by-default structured event without exception messages/stacks."""
    extra: dict[str, object] = {"dante_fields": dict(fields or {})}
    if exception is not None:
        extra["dante_exception_type"] = type(exception).__name__
    logger.log(level, event, extra=extra)
