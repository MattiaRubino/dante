"""Process-scoped SQLAlchemy runtime and bounded readiness probing."""

from asyncio import timeout
from collections.abc import Callable
from contextlib import suppress
from dataclasses import dataclass
from time import perf_counter

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from dante.platform.config.database import DatabaseSettings
from dante.platform.observability.database import instrument_database_engine
from dante.platform.observability.metrics import DatabaseTelemetry

_RUNTIME_IDENTITY = "dante_runtime"
_TRUSTED_SEARCH_PATH = "pg_catalog,dante,pg_temp"


@dataclass(frozen=True, slots=True)
class DatabaseRuntime:
    """Long-lived engine/session factory owned by one backend process."""

    engine: AsyncEngine
    session_factory: async_sessionmaker[AsyncSession]
    readiness_timeout_seconds: float
    telemetry: DatabaseTelemetry | None = None
    detach_telemetry: Callable[[], None] | None = None

    async def is_ready(self) -> bool:
        """Check reachability plus the fail-closed runtime DB identity contract."""
        started = perf_counter()
        ready = False
        try:
            async with timeout(self.readiness_timeout_seconds):
                async with self.engine.connect() as connection:
                    row = (
                        await connection.execute(
                            text(
                                "SELECT session_user, current_user, current_setting('search_path')"
                            )
                        )
                    ).one()
                    normalized_search_path = str(row[2]).replace(" ", "")
                    ready = bool(
                        row[0] == _RUNTIME_IDENTITY
                        and row[1] == _RUNTIME_IDENTITY
                        and normalized_search_path == _TRUSTED_SEARCH_PATH
                    )
                    return ready
        except OSError, SQLAlchemyError, TimeoutError:
            return False
        finally:
            if self.telemetry is not None:
                with suppress(Exception):
                    self.telemetry.record_readiness(
                        ready=ready,
                        duration=perf_counter() - started,
                    )

    async def dispose(self) -> None:
        """Release all pooled connections owned by this process."""
        if self.detach_telemetry is not None:
            with suppress(Exception):
                self.detach_telemetry()
        await self.engine.dispose()


def create_database_runtime(
    settings: DatabaseSettings,
    *,
    telemetry: DatabaseTelemetry | None = None,
) -> DatabaseRuntime:
    """Create the lazy process-scoped async PostgreSQL runtime."""
    engine = create_async_engine(
        settings.sqlalchemy_url(),
        connect_args={
            "connect_timeout": settings.connect_timeout_seconds,
            "application_name": "dante-backend",
            "options": "-c search_path=pg_catalog,dante,pg_temp",
        },
        pool_pre_ping=True,
        pool_size=settings.pool_size,
        max_overflow=settings.max_overflow,
        pool_timeout=settings.pool_timeout_seconds,
        hide_parameters=True,
        echo=False,
        echo_pool=False,
    )
    session_factory = async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=True,
        autobegin=False,
    )
    detach_telemetry = (
        instrument_database_engine(engine, telemetry) if telemetry is not None else None
    )
    return DatabaseRuntime(
        engine=engine,
        session_factory=session_factory,
        readiness_timeout_seconds=settings.readiness_timeout_seconds,
        telemetry=telemetry,
        detach_telemetry=detach_telemetry,
    )
