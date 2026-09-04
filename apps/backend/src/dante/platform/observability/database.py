"""SQLAlchemy event instrumentation that never records SQL or bind parameters."""

from __future__ import annotations

import re
from collections.abc import Callable
from contextlib import suppress
from threading import RLock
from typing import Any, Literal

from sqlalchemy import event
from sqlalchemy.ext.asyncio import AsyncEngine

from dante.platform.observability.metrics import DatabaseOperation, DatabaseTelemetry

_SQL_OPERATION = re.compile(r"^\s*([A-Za-z]+)")
_ALLOWED_OPERATIONS = frozenset({"CALL", "DELETE", "INSERT", "MERGE", "SELECT", "UPDATE"})


def _operation_name(statement: str) -> str:
    match = _SQL_OPERATION.match(statement)
    if match is None:
        return "OTHER"
    candidate = match.group(1).upper()
    return candidate if candidate in _ALLOWED_OPERATIONS else "OTHER"


def instrument_database_engine(
    engine: AsyncEngine,
    telemetry: DatabaseTelemetry,
) -> Callable[[], None]:
    """Attach bounded client/pool signals and return an exact detach callback."""
    active: dict[int, DatabaseOperation] = {}
    pool_states: dict[int, Literal["idle", "used"]] = {}
    lock = RLock()

    def transition_pool(
        connection_record: Any,
        state: Literal["idle", "used"] | None,
        *,
        allow_create: bool,
    ) -> None:
        key = id(connection_record)
        with lock:
            previous = pool_states.get(key)
            if previous is None and not allow_create:
                return
            if previous == state:
                return
            if state is None:
                pool_states.pop(key, None)
            else:
                pool_states[key] = state

        if previous is not None:
            with suppress(Exception):
                telemetry.change_pool(-1, state=previous)
        if state is not None:
            with suppress(Exception):
                telemetry.change_pool(1, state=state)

    def before_cursor_execute(
        _connection: Any,
        _cursor: Any,
        statement: str,
        _parameters: Any,
        context: Any,
        _executemany: bool,
    ) -> None:
        with suppress(Exception):
            token = telemetry.start_operation(_operation_name(statement))
            with lock:
                active[id(context)] = token

    def after_cursor_execute(
        _connection: Any,
        _cursor: Any,
        _statement: str,
        _parameters: Any,
        context: Any,
        _executemany: bool,
    ) -> None:
        with lock:
            token = active.pop(id(context), None)
        if token is not None:
            with suppress(Exception):
                telemetry.finish_operation(token, failed=False)

    def handle_error(exception_context: Any) -> None:
        context = getattr(exception_context, "execution_context", None)
        if context is None:
            return
        with lock:
            token = active.pop(id(context), None)
        if token is not None:
            with suppress(Exception):
                telemetry.finish_operation(token, failed=True)

    def connect(_dbapi_connection: Any, connection_record: Any) -> None:
        transition_pool(connection_record, "idle", allow_create=True)

    def close(_dbapi_connection: Any, connection_record: Any) -> None:
        transition_pool(connection_record, None, allow_create=False)

    def checkout(
        _dbapi_connection: Any,
        connection_record: Any,
        _connection_proxy: Any,
    ) -> None:
        transition_pool(connection_record, "used", allow_create=True)

    def checkin(_dbapi_connection: Any, connection_record: Any) -> None:
        transition_pool(connection_record, "idle", allow_create=False)

    sync_engine = engine.sync_engine
    pool = sync_engine.pool
    listeners: tuple[tuple[Any, str, Callable[..., None]], ...] = (
        (sync_engine, "before_cursor_execute", before_cursor_execute),
        (sync_engine, "after_cursor_execute", after_cursor_execute),
        (sync_engine, "handle_error", handle_error),
        (pool, "connect", connect),
        (pool, "close", close),
        (pool, "checkout", checkout),
        (pool, "checkin", checkin),
    )
    for target, identifier, listener in listeners:
        event.listen(target, identifier, listener)

    def detach() -> None:
        for target, identifier, listener in reversed(listeners):
            event.remove(target, identifier, listener)
        with lock:
            abandoned = tuple(active.values())
            active.clear()
            remaining_pool_states = tuple(pool_states.values())
            pool_states.clear()
        for token in abandoned:
            with suppress(Exception):
                telemetry.finish_operation(token, failed=True)
        for state in ("idle", "used"):
            count = remaining_pool_states.count(state)
            if count:
                with suppress(Exception):
                    telemetry.change_pool(-count, state=state)

    return detach
