"""Real PostgreSQL acceptance tests for CP3 transaction semantics."""

from typing import Any

import pytest
from sqlalchemy import text
from sqlalchemy.exc import InvalidRequestError

from dante.platform.database.runtime import create_database_runtime

pytestmark = pytest.mark.postgres


async def _create_probe_table(database: Any) -> None:
    runtime = create_database_runtime(database.runtime_settings())
    try:
        async with runtime.engine.begin() as connection:
            await connection.exec_driver_sql("SET ROLE dante_owner")
            await connection.exec_driver_sql(
                "CREATE TABLE dante.cp3_transaction_probe ("
                "id bigint PRIMARY KEY, value text NOT NULL)"
            )
            await connection.exec_driver_sql("RESET ROLE")
    finally:
        await runtime.dispose()


@pytest.mark.asyncio
async def test_autobegin_false_rejects_implicit_transaction(migrated_database: Any) -> None:
    runtime = create_database_runtime(migrated_database.runtime_settings())
    try:
        async with runtime.session_factory() as session:
            with pytest.raises(InvalidRequestError, match="Autobegin is disabled"):
                await session.execute(text("SELECT 1"))
    finally:
        await runtime.dispose()


@pytest.mark.asyncio
async def test_real_commit_persists_across_sessions(migrated_database: Any) -> None:
    await _create_probe_table(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    try:
        async with runtime.session_factory.begin() as session:
            await session.execute(
                text("INSERT INTO dante.cp3_transaction_probe (id, value) VALUES (1, 'committed')")
            )

        async with runtime.session_factory.begin() as session:
            value = await session.scalar(
                text("SELECT value FROM dante.cp3_transaction_probe WHERE id = 1")
            )
            assert value == "committed"
    finally:
        await runtime.dispose()


@pytest.mark.asyncio
async def test_exception_rolls_back_entire_application_transaction(migrated_database: Any) -> None:
    await _create_probe_table(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    try:
        with pytest.raises(RuntimeError, match="force rollback"):
            async with runtime.session_factory.begin() as session:
                await session.execute(
                    text("INSERT INTO dante.cp3_transaction_probe (id, value) VALUES (1, 'first')")
                )
                await session.execute(
                    text("INSERT INTO dante.cp3_transaction_probe (id, value) VALUES (2, 'second')")
                )
                raise RuntimeError("force rollback")

        async with runtime.session_factory.begin() as session:
            count = await session.scalar(text("SELECT count(*) FROM dante.cp3_transaction_probe"))
            assert count == 0
    finally:
        await runtime.dispose()


@pytest.mark.asyncio
async def test_flush_does_not_commit(migrated_database: Any) -> None:
    await _create_probe_table(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    try:
        with pytest.raises(RuntimeError, match="rollback after flush"):
            async with runtime.session_factory.begin() as session:
                await session.execute(
                    text("INSERT INTO dante.cp3_transaction_probe (id, value) VALUES (1, 'flushed')")
                )
                await session.flush()

                async with runtime.engine.connect() as observer:
                    observed = await observer.scalar(
                        text("SELECT count(*) FROM dante.cp3_transaction_probe WHERE id = 1")
                    )
                    assert observed == 0

                raise RuntimeError("rollback after flush")

        async with runtime.session_factory.begin() as session:
            count = await session.scalar(text("SELECT count(*) FROM dante.cp3_transaction_probe"))
            assert count == 0
    finally:
        await runtime.dispose()


@pytest.mark.asyncio
async def test_savepoint_failure_preserves_outer_transaction(migrated_database: Any) -> None:
    await _create_probe_table(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    try:
        async with runtime.session_factory.begin() as session:
            await session.execute(
                text("INSERT INTO dante.cp3_transaction_probe (id, value) VALUES (1, 'outer')")
            )
            with pytest.raises(RuntimeError, match="savepoint rollback"):
                async with session.begin_nested():
                    await session.execute(
                        text("INSERT INTO dante.cp3_transaction_probe (id, value) VALUES (2, 'nested')")
                    )
                    raise RuntimeError("savepoint rollback")

        async with runtime.session_factory.begin() as session:
            rows = (
                await session.execute(
                    text("SELECT id, value FROM dante.cp3_transaction_probe ORDER BY id")
                )
            ).all()
            assert rows == [(1, "outer")]
    finally:
        await runtime.dispose()
