"""Fast contract tests for the CP3 SQLAlchemy runtime boundary."""

from pydantic import SecretStr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.pool import AsyncAdaptedQueuePool

from dante.platform.config.database import DatabaseSettings
from dante.platform.database.runtime import create_database_runtime


def _settings() -> DatabaseSettings:
    return DatabaseSettings(
        host="db.internal",
        port=5432,
        name="dante",
        user="dante_runtime",
        password=SecretStr("p@ss:/word"),
        connect_timeout_seconds=7,
        pool_size=3,
        max_overflow=4,
        pool_timeout_seconds=11.5,
        readiness_timeout_seconds=1.25,
    )


def test_database_url_is_structured_and_redacts_password() -> None:
    settings = _settings()

    url = settings.sqlalchemy_url()

    assert url.drivername == "postgresql+psycopg"
    assert url.username == "dante_runtime"
    assert url.host == "db.internal"
    assert url.port == 5432
    assert url.database == "dante"
    assert "p@ss:/word" not in str(url)
    assert "***" in str(url)
    assert url.render_as_string(hide_password=False).count("%40") == 1


def test_runtime_uses_bounded_async_pool_and_explicit_session_semantics() -> None:
    runtime = create_database_runtime(_settings())
    try:
        assert isinstance(runtime.engine.sync_engine.pool, AsyncAdaptedQueuePool)
        assert runtime.engine.sync_engine.pool.size() == 3
        assert runtime.engine.sync_engine.pool.timeout() == 11.5
        assert runtime.readiness_timeout_seconds == 1.25

        session = runtime.session_factory()
        assert isinstance(session, AsyncSession)
        assert session.sync_session.autobegin is False
        assert session.sync_session.expire_on_commit is False
        assert session.autoflush is True
    finally:
        runtime.engine.sync_engine.dispose()


def test_runtime_engine_never_enables_sql_parameter_echo() -> None:
    runtime = create_database_runtime(_settings())
    try:
        assert runtime.engine.echo is False
        assert runtime.engine.hide_parameters is True
    finally:
        runtime.engine.sync_engine.dispose()
