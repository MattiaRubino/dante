"""Low-cardinality DANTE application instruments."""

from __future__ import annotations

from dataclasses import dataclass
from time import perf_counter
from typing import Literal

from opentelemetry.metrics import Counter, Histogram, Meter, UpDownCounter
from opentelemetry.trace import Span, SpanKind, Status, StatusCode, Tracer

HttpOutcome = Literal["success", "client_error", "server_error"]
DependencyOutcome = Literal["success", "error", "timeout", "rejected"]
SigninOutcome = Literal[
    "success",
    "invalid_credentials",
    "invalid_input",
    "account_unavailable",
    "password_compromised",
    "rate_limited",
    "service_unavailable",
    "unexpected",
]


def _http_outcome(status_code: int) -> HttpOutcome:
    if status_code >= 500:
        return "server_error"
    if status_code >= 400:
        return "client_error"
    return "success"


class HttpTelemetry:
    """RED metrics for the bounded HTTP route template surface."""

    def __init__(self, meter: Meter) -> None:
        self._requests: Counter = meter.create_counter(
            "http.server.request.count",
            unit="{request}",
            description="Completed DANTE HTTP requests.",
        )
        self._duration: Histogram = meter.create_histogram(
            "http.server.request.duration",
            unit="s",
            description="DANTE HTTP request duration.",
        )
        self._active: UpDownCounter = meter.create_up_down_counter(
            "http.server.active_requests",
            unit="{request}",
            description="Currently active DANTE HTTP requests.",
        )

    def change_active(self, amount: int, *, method: str) -> None:
        self._active.add(amount, {"http.request.method": method})

    def complete(self, *, method: str, route: str, status_code: int, duration: float) -> None:
        attributes: dict[str, str | int] = {
            "http.request.method": method,
            "http.route": route,
            "http.response.status_code": status_code,
            "dante.outcome": _http_outcome(status_code),
        }
        self._requests.add(1, attributes)
        self._duration.record(duration, attributes)


class AuthTelemetry:
    """Security-safe Auth pressure and dependency signals without identity labels."""

    def __init__(self, meter: Meter) -> None:
        self._signin_attempts: Counter = meter.create_counter(
            "dante.auth.signin.attempts",
            unit="{attempt}",
            description="Signin attempts by bounded public outcome.",
        )
        self._signin_duration: Histogram = meter.create_histogram(
            "dante.auth.signin.duration",
            unit="s",
            description="End-to-end signin application duration.",
        )
        self._kdf_duration: Histogram = meter.create_histogram(
            "dante.auth.kdf.duration",
            unit="s",
            description="Argon2 worker execution duration.",
        )
        self._kdf_inflight: UpDownCounter = meter.create_up_down_counter(
            "dante.auth.kdf.inflight",
            unit="{operation}",
            description="Admitted Argon2 operations including queued work.",
        )
        self._kdf_active: UpDownCounter = meter.create_up_down_counter(
            "dante.auth.kdf.active",
            unit="{operation}",
            description="Argon2 operations currently executing on workers.",
        )
        self._kdf_rejections: Counter = meter.create_counter(
            "dante.auth.kdf.rejections",
            unit="{operation}",
            description="Argon2 admission or queue-timeout rejections.",
        )
        self._dependencies: Counter = meter.create_counter(
            "dante.auth.dependency.requests",
            unit="{request}",
            description="Bounded Auth dependency calls by outcome.",
        )
        self._dependency_duration: Histogram = meter.create_histogram(
            "dante.auth.dependency.duration",
            unit="s",
            description="Bounded Auth dependency duration.",
        )

    def record_signin(self, outcome: SigninOutcome, *, duration: float) -> None:
        attributes = {"dante.auth.outcome": outcome}
        self._signin_attempts.add(1, attributes)
        self._signin_duration.record(duration, attributes)

    def change_kdf_inflight(self, amount: int) -> None:
        self._kdf_inflight.add(amount)

    def change_kdf_active(self, amount: int) -> None:
        self._kdf_active.add(amount)

    def record_kdf(self, *, duration: float, outcome: DependencyOutcome) -> None:
        self._kdf_duration.record(duration, {"dante.outcome": outcome})

    def record_kdf_rejection(self, *, queue_state: Literal["full", "timeout"]) -> None:
        self._kdf_rejections.add(1, {"dante.queue_state": queue_state})

    def record_dependency(
        self,
        dependency: Literal["hibp"],
        *,
        outcome: DependencyOutcome,
        duration: float,
    ) -> None:
        attributes = {"server.address": dependency, "dante.outcome": outcome}
        self._dependencies.add(1, attributes)
        self._dependency_duration.record(duration, attributes)


@dataclass(frozen=True, slots=True)
class DatabaseOperation:
    """One in-process database span token without SQL text."""

    operation: str
    started: float
    span: Span


class DatabaseTelemetry:
    """Database client, pool and readiness signals without SQL or bind values."""

    def __init__(self, meter: Meter, tracer: Tracer) -> None:
        self._tracer = tracer
        self._operations: Counter = meter.create_counter(
            "db.client.operation.count",
            unit="{operation}",
            description="Completed PostgreSQL operations without statement text.",
        )
        self._duration: Histogram = meter.create_histogram(
            "db.client.operation.duration",
            unit="s",
            description="PostgreSQL operation duration without statement text.",
        )
        self._pool_connections: UpDownCounter = meter.create_up_down_counter(
            "db.client.connections.usage",
            unit="{connection}",
            description="SQLAlchemy pool connections by state.",
        )
        self._readiness: Counter = meter.create_counter(
            "dante.database.readiness.checks",
            unit="{check}",
            description="Database readiness checks by bounded outcome.",
        )
        self._readiness_duration: Histogram = meter.create_histogram(
            "dante.database.readiness.duration",
            unit="s",
            description="Database readiness check duration.",
        )

    def complete_operation(
        self,
        *,
        operation: str,
        outcome: Literal["success", "error"],
        duration: float,
    ) -> None:
        attributes = {
            "db.system.name": "postgresql",
            "db.operation.name": operation,
            "dante.outcome": outcome,
        }
        self._operations.add(1, attributes)
        self._duration.record(duration, attributes)

    def start_operation(self, operation: str) -> DatabaseOperation:
        span = self._tracer.start_span(
            f"postgresql.{operation.lower()}",
            kind=SpanKind.CLIENT,
            attributes={
                "db.system.name": "postgresql",
                "db.operation.name": operation,
            },
            record_exception=False,
            set_status_on_exception=False,
        )
        return DatabaseOperation(operation=operation, started=perf_counter(), span=span)

    def finish_operation(self, token: DatabaseOperation, *, failed: bool) -> None:
        outcome: Literal["success", "error"] = "error" if failed else "success"
        if failed and token.span.is_recording():
            token.span.set_status(Status(StatusCode.ERROR))
        token.span.end()
        self.complete_operation(
            operation=token.operation,
            outcome=outcome,
            duration=perf_counter() - token.started,
        )

    def change_pool(self, amount: int, *, state: Literal["idle", "used"] = "used") -> None:
        self._pool_connections.add(amount, {"state": state})

    def record_readiness(self, *, ready: bool, duration: float) -> None:
        attributes = {"dante.outcome": "success" if ready else "error"}
        self._readiness.add(1, attributes)
        self._readiness_duration.record(duration, attributes)
