"""Runtime ownership and exporter failure-isolation proofs."""

import asyncio
from collections.abc import Callable
from threading import Event
from time import monotonic
from typing import NoReturn

import pytest
from sqlalchemy import event as sqlalchemy_event

import dante.platform.observability.runtime as runtime_module
from dante.platform.config.observability import ObservabilitySettings
from dante.platform.observability.database import _operation_name, instrument_database_engine
from dante.platform.observability.runtime import create_observability_runtime


@pytest.mark.parametrize(
    ("statement", "operation"),
    [
        ("SELECT email FROM dante.account", "SELECT"),
        ("\n\tinsert into dante.account values (...) ", "INSERT"),
        ("WITH secret AS (SELECT 1) SELECT * FROM secret", "OTHER"),
        ("-- user query\nDELETE FROM dante.account", "OTHER"),
        ("VACUUM dante.account", "OTHER"),
        ("", "OTHER"),
    ],
)
def test_database_operation_classifier_is_closed_and_statement_free(
    statement: str,
    operation: str,
) -> None:
    assert _operation_name(statement) == operation


@pytest.mark.asyncio
async def test_disabled_runtime_owns_and_closes_local_providers() -> None:
    runtime = create_observability_runtime(
        settings=ObservabilitySettings(enabled=False),
        environment="test",
        release_sha="test-release",
        build_id="test-build",
    )

    assert runtime.settings.enabled is False
    assert runtime.tracer_provider.resource.attributes["service.name"] == "dante-backend"
    assert runtime.tracer_provider.resource.attributes["service.version"] == "test-release"

    await runtime.aclose()
    await runtime.aclose()

    assert runtime._closed is True


@pytest.mark.asyncio
async def test_exporter_construction_failure_never_blocks_application_runtime(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def unavailable_exporter(*_args: object, **_kwargs: object) -> NoReturn:
        raise RuntimeError("collector detail that must not escape")

    monkeypatch.setattr(runtime_module, "OTLPSpanExporter", unavailable_exporter)
    runtime = create_observability_runtime(
        settings=ObservabilitySettings(enabled=True),
        environment="test",
        release_sha="test-release",
        build_id="test-build",
    )

    try:
        assert runtime.settings.enabled is True
        assert runtime.tracer_provider.resource.attributes["service.name"] == "dante-backend"
    finally:
        await runtime.aclose()


def test_export_signal_urls_are_derived_from_one_credential_free_base() -> None:
    signal_endpoint = runtime_module._signal_endpoint
    as_callable: Callable[[str, str], str] = signal_endpoint

    assert as_callable("https://otel.example.test/otlp", "traces") == (
        "https://otel.example.test/otlp/v1/traces"
    )
    assert as_callable("http://127.0.0.1:4318", "metrics") == ("http://127.0.0.1:4318/v1/metrics")


@pytest.mark.asyncio
async def test_shutdown_deadline_bounds_a_stuck_provider(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    runtime = create_observability_runtime(
        settings=ObservabilitySettings(enabled=False, shutdown_timeout_seconds=0.01),
        environment="test",
        release_sha="test-release",
        build_id="test-build",
    )
    release = Event()

    def blocked_flush(*, timeout_millis: int) -> bool:
        del timeout_millis
        return release.wait(timeout=1.0)

    monkeypatch.setattr(runtime.tracer_provider, "force_flush", blocked_flush)
    started = monotonic()
    await runtime.aclose()
    elapsed = monotonic() - started
    release.set()
    await asyncio.sleep(0.05)

    assert elapsed < 0.25
    assert runtime._closed is True


class RecordingDatabaseTelemetry:
    def __init__(self) -> None:
        self.pool_changes: list[tuple[int, str]] = []

    def change_pool(self, amount: int, *, state: str) -> None:
        self.pool_changes.append((amount, state))


def test_pool_metrics_do_not_recreate_a_connection_after_close(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    listeners: dict[str, Callable[..., None]] = {}

    def listen(_target: object, identifier: str, listener: Callable[..., None]) -> None:
        listeners[identifier] = listener

    def remove(_target: object, identifier: str, listener: Callable[..., None]) -> None:
        assert listeners.pop(identifier) is listener

    monkeypatch.setattr(sqlalchemy_event, "listen", listen)
    monkeypatch.setattr(sqlalchemy_event, "remove", remove)
    pool = object()
    sync_engine = type("SyncEngine", (), {"pool": pool})()
    engine = type("Engine", (), {"sync_engine": sync_engine})()
    telemetry = RecordingDatabaseTelemetry()

    detach = instrument_database_engine(engine, telemetry)  # type: ignore[arg-type]
    connection_record = object()
    listeners["connect"](None, connection_record)
    listeners["checkout"](None, connection_record, None)
    listeners["close"](None, connection_record)
    listeners["checkin"](None, connection_record)
    detach()

    assert telemetry.pool_changes == [
        (1, "idle"),
        (-1, "idle"),
        (1, "used"),
        (-1, "used"),
    ]
    assert listeners == {}


def test_pool_metrics_are_zeroed_when_instrumentation_detaches(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    listeners: dict[str, Callable[..., None]] = {}

    monkeypatch.setattr(
        sqlalchemy_event,
        "listen",
        lambda _target, identifier, listener: listeners.__setitem__(identifier, listener),
    )
    monkeypatch.setattr(sqlalchemy_event, "remove", lambda *_args: None)
    pool = object()
    sync_engine = type("SyncEngine", (), {"pool": pool})()
    engine = type("Engine", (), {"sync_engine": sync_engine})()
    telemetry = RecordingDatabaseTelemetry()

    detach = instrument_database_engine(engine, telemetry)  # type: ignore[arg-type]
    listeners["connect"](None, object())
    detach()

    assert telemetry.pool_changes == [(1, "idle"), (-1, "idle")]
