"""Real PostgreSQL acceptance tests for runtime connectivity and recovery."""

from __future__ import annotations

import time
from typing import Any

import psycopg
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text

from dante.bootstrap.app import create_app
from dante.platform.config.settings import Environment, Settings
from dante.platform.database.runtime import create_database_runtime

pytestmark = pytest.mark.postgres

_TRUSTED_SEARCH_PATH = "pg_catalog,dante,pg_temp"


@pytest.mark.asyncio
async def test_runtime_connects_as_exact_identity_with_trusted_search_path(
    migrated_database: Any,
) -> None:
    runtime = create_database_runtime(migrated_database.runtime_settings())
    try:
        async with runtime.engine.connect() as connection:
            row = (
                await connection.execute(
                    text("SELECT session_user, current_user, current_setting('search_path')")
                )
            ).one()

        assert row[0:2] == ("dante_runtime", "dante_runtime")
        assert str(row[2]).replace(" ", "") == _TRUSTED_SEARCH_PATH
        assert await runtime.is_ready() is True
    finally:
        await runtime.dispose()


@pytest.mark.asyncio
async def test_pool_pre_ping_recovers_a_stale_returned_connection(
    migrated_database: Any,
) -> None:
    runtime = create_database_runtime(
        migrated_database.runtime_settings(pool_size=1, max_overflow=0)
    )
    try:
        async with runtime.engine.connect() as connection:
            backend_pid = int(await connection.scalar(text("SELECT pg_backend_pid()")))

        admin = await psycopg.AsyncConnection.connect(
            host=migrated_database.cluster.host,
            port=migrated_database.cluster.port,
            dbname=migrated_database.name,
            user=migrated_database.cluster.admin_user,
            password=migrated_database.cluster.admin_password,
            autocommit=True,
        )
        try:
            result = await admin.execute("SELECT pg_terminate_backend(%s)", (backend_pid,))
            assert (await result.fetchone()) == (True,)
        finally:
            await admin.close()

        assert await runtime.is_ready() is True
    finally:
        await runtime.dispose()


def test_liveness_survives_database_outage_and_readiness_recovers_without_app_restart(
    migrated_database: Any,
    postgres_cluster: Any,
) -> None:
    settings = Settings(
        env=Environment.LOCAL,
        release_sha="local",
        build_id="local",
        debug=False,
        database=migrated_database.runtime_settings(
            pool_size=1,
            max_overflow=0,
            pool_timeout_seconds=1.0,
            readiness_timeout_seconds=0.5,
        ),
    )

    with TestClient(create_app(settings)) as client:
        assert client.get("/health/live").status_code == 200
        ready = client.get("/health/ready")
        assert ready.status_code == 200
        assert ready.json() == {"status": "ready"}

        postgres_cluster.stop()
        try:
            assert client.get("/health/live").status_code == 200
            unavailable = client.get("/health/ready")
            assert unavailable.status_code == 503
            assert unavailable.json() == {"status": "not_ready"}
        finally:
            postgres_cluster.start()

        deadline = time.monotonic() + 10
        recovered = None
        while time.monotonic() < deadline:
            recovered = client.get("/health/ready")
            if recovered.status_code == 200:
                break
            time.sleep(0.1)

        assert recovered is not None
        assert recovered.status_code == 200
        assert recovered.json() == {"status": "ready"}


def test_readiness_response_never_exposes_database_details(migrated_database: Any) -> None:
    settings = Settings(
        env=Environment.LOCAL,
        release_sha="local",
        build_id="local",
        debug=False,
        database=migrated_database.runtime_settings(readiness_timeout_seconds=0.25),
    )

    with TestClient(create_app(settings)) as client:
        migrated_database.cluster.stop()
        try:
            response = client.get("/health/ready")
        finally:
            migrated_database.cluster.start()

    assert response.status_code == 503
    payload = response.text
    assert migrated_database.cluster.runtime_password not in payload
    assert migrated_database.name not in payload
    assert migrated_database.cluster.host not in payload


@pytest.mark.asyncio
async def test_engine_dispose_is_safe_after_real_use(migrated_database: Any) -> None:
    runtime = create_database_runtime(migrated_database.runtime_settings())
    async with runtime.engine.connect() as connection:
        assert await connection.scalar(text("SELECT 1")) == 1

    await runtime.dispose()
