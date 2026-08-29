"""Owned OpenTelemetry providers and failure-isolated DANTE instruments."""

from __future__ import annotations

import asyncio
import logging
from contextlib import suppress
from dataclasses import dataclass
from threading import Thread

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.metrics import Meter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.metrics.view import ExplicitBucketHistogramAggregation, View
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import SpanLimits, TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.trace.sampling import ALWAYS_OFF, ParentBased, Sampler, TraceIdRatioBased
from opentelemetry.trace import Status, StatusCode, Tracer

from dante.platform.config.observability import ObservabilitySettings
from dante.platform.observability.logging import (
    LoggingRuntime,
    configure_logging,
    log_event,
)
from dante.platform.observability.metrics import AuthTelemetry, DatabaseTelemetry, HttpTelemetry

_LOGGER = logging.getLogger(__name__)
_INSTRUMENTATION_NAME = "dante.platform.observability"
_HTTP_BUCKETS = (0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0)
_DEPENDENCY_BUCKETS = (0.001, 0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0)


@dataclass(slots=True)
class ObservabilityRuntime:
    """Process-scoped providers and application instruments."""

    settings: ObservabilitySettings
    tracer_provider: TracerProvider
    meter_provider: MeterProvider
    tracer: Tracer
    meter: Meter
    http: HttpTelemetry
    auth: AuthTelemetry
    database: DatabaseTelemetry
    logging: LoggingRuntime
    _closed: bool = False

    async def aclose(self) -> None:
        """Flush bounded queues without making telemetry a shutdown blocker."""
        if self._closed:
            return
        self._closed = True

        timeout_millis = int(self.settings.shutdown_timeout_seconds * 1_000)

        shutdown_failures: list[BaseException] = []
        shutdown_complete = asyncio.Event()
        loop = asyncio.get_running_loop()

        def shutdown_providers() -> None:
            try:
                self.tracer_provider.force_flush(timeout_millis=timeout_millis)
                self.meter_provider.force_flush(timeout_millis=timeout_millis)
                self.tracer_provider.shutdown()
                self.meter_provider.shutdown(timeout_millis=timeout_millis)
            except BaseException as exc:  # noqa: BLE001 - never leak daemon failures to stderr
                shutdown_failures.append(exc)
            finally:
                with suppress(RuntimeError):
                    loop.call_soon_threadsafe(shutdown_complete.set)

        shutdown_thread = Thread(
            target=shutdown_providers,
            name="dante-observability-shutdown",
            daemon=True,
        )
        try:
            shutdown_thread.start()
            await asyncio.wait_for(
                shutdown_complete.wait(),
                timeout=self.settings.shutdown_timeout_seconds,
            )
            if shutdown_failures:
                raise RuntimeError("observability provider shutdown failed") from shutdown_failures[
                    0
                ]
        except TimeoutError as exc:
            log_event(
                _LOGGER,
                logging.WARNING,
                "observability.shutdown_timeout",
                fields={"outcome": "timeout"},
                exception=exc,
            )
        except RuntimeError as exc:
            log_event(
                _LOGGER,
                logging.WARNING,
                "observability.shutdown_failed",
                fields={"outcome": "error"},
                exception=exc,
            )
        finally:
            self.logging.close()


def mark_current_span_error(*, error_code: str, exception: BaseException | None = None) -> None:
    """Mark the active span with bounded error identity, never exception text."""
    span = trace.get_current_span()
    if not span.is_recording():
        return
    span.set_status(Status(StatusCode.ERROR))
    attributes: dict[str, str] = {"error.type": error_code}
    if exception is not None:
        attributes["exception.type"] = type(exception).__name__
    span.add_event("dante.error", attributes)


def _metric_views() -> tuple[View, ...]:
    return (
        View(
            instrument_name="http.server.request.duration",
            aggregation=ExplicitBucketHistogramAggregation(_HTTP_BUCKETS),
        ),
        View(
            instrument_name="db.client.operation.duration",
            aggregation=ExplicitBucketHistogramAggregation(_DEPENDENCY_BUCKETS),
        ),
        View(
            instrument_name="dante.auth.*.duration",
            aggregation=ExplicitBucketHistogramAggregation(_DEPENDENCY_BUCKETS),
        ),
    )


def _signal_endpoint(base_endpoint: str, signal: str) -> str:
    return f"{base_endpoint.rstrip('/')}/v1/{signal}"


def create_observability_runtime(
    *,
    settings: ObservabilitySettings,
    environment: str,
    release_sha: str,
    build_id: str,
) -> ObservabilityRuntime:
    """Build telemetry providers; exporter failure never weakens application truth."""
    logging_runtime = configure_logging(settings)
    resource = Resource.create(
        {
            "service.name": "dante-backend",
            "service.namespace": "dante",
            "service.version": release_sha,
            "deployment.environment.name": environment,
            "dante.build.id": build_id,
        }
    )

    metric_readers: list[PeriodicExportingMetricReader] = []
    sampler: Sampler = ALWAYS_OFF
    trace_exporter: OTLPSpanExporter | None = None
    exporters_active = False

    if settings.enabled:
        sampler = ParentBased(TraceIdRatioBased(settings.trace_sample_ratio))
        try:
            trace_exporter = OTLPSpanExporter(
                endpoint=_signal_endpoint(settings.otlp_http_endpoint, "traces"),
                timeout=settings.export_timeout_seconds,
            )
            metric_exporter = OTLPMetricExporter(
                endpoint=_signal_endpoint(settings.otlp_http_endpoint, "metrics"),
                timeout=settings.export_timeout_seconds,
            )
            metric_readers.append(
                PeriodicExportingMetricReader(
                    metric_exporter,
                    export_interval_millis=settings.metric_export_interval_seconds * 1_000,
                    export_timeout_millis=int(settings.export_timeout_seconds * 1_000),
                )
            )
            exporters_active = True
        except Exception as exc:  # noqa: BLE001 - telemetry construction is fail-open
            sampler = ALWAYS_OFF
            if trace_exporter is not None:
                with suppress(Exception):
                    trace_exporter.shutdown()  # type: ignore[no-untyped-call]
            trace_exporter = None
            metric_readers.clear()
            log_event(
                _LOGGER,
                logging.ERROR,
                "observability.exporter_initialization_failed",
                fields={"outcome": "error"},
                exception=exc,
            )

    meter_provider = MeterProvider(
        metric_readers=metric_readers,
        resource=resource,
        shutdown_on_exit=False,
        views=_metric_views(),
    )
    tracer_provider = TracerProvider(
        sampler=sampler,
        resource=resource,
        shutdown_on_exit=False,
        span_limits=SpanLimits(
            max_attributes=32,
            max_events=16,
            max_links=8,
            max_event_attributes=8,
            max_link_attributes=8,
        ),
        meter_provider=meter_provider,
    )
    if trace_exporter is not None:
        tracer_provider.add_span_processor(
            BatchSpanProcessor(
                trace_exporter,
                max_queue_size=settings.span_max_queue_size,
                schedule_delay_millis=settings.span_schedule_delay_milliseconds,
                max_export_batch_size=settings.span_max_export_batch_size,
                export_timeout_millis=settings.export_timeout_seconds * 1_000,
                meter_provider=meter_provider,
            )
        )

    tracer = tracer_provider.get_tracer(_INSTRUMENTATION_NAME)
    meter = meter_provider.get_meter(_INSTRUMENTATION_NAME)
    runtime = ObservabilityRuntime(
        settings=settings,
        tracer_provider=tracer_provider,
        meter_provider=meter_provider,
        tracer=tracer,
        meter=meter,
        http=HttpTelemetry(meter),
        auth=AuthTelemetry(meter),
        database=DatabaseTelemetry(meter, tracer),
        logging=logging_runtime,
    )
    log_event(
        _LOGGER,
        logging.INFO,
        "observability.runtime_initialized",
        fields={
            "service_name": "dante-backend",
            "environment": environment,
            "release_sha": release_sha,
            "build_id": build_id,
            "outcome": (
                "enabled" if exporters_active else "degraded" if settings.enabled else "disabled"
            ),
        },
    )
    return runtime
