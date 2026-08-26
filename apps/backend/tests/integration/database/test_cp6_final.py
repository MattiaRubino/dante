"""CP6-05 final advisory-lock and concurrent Role-13 acceptance."""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from datetime import UTC, date, datetime, timedelta
from threading import Barrier
from typing import Any, Literal
from uuid import UUID, uuid7

import psycopg
import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import text

from dante.platform.database.locking import (
    acquire_advisory_xact_locks,
    advisory_lock_key,
    occurrence_generation_lock_keys,
)
from dante.platform.database.runtime import create_database_runtime

pytestmark = pytest.mark.postgres

_FINAL_REVISION = "20260826_08"
_GOLDEN_REF = UUID("018f1f26-8b2e-7abc-8000-000000000001")
_GOLDEN_KEYS = {
    1: 114563613494871305,
    2: 186621207532799241,
    3: 258678801570727177,
    4: 330736395608655113,
    5: 402793989646583049,
    6: 474851583684510985,
    7: 546909177722438921,
}


def _connect(
    database: Any,
    user: str,
    password: str,
    *,
    owner: bool = False,
) -> psycopg.Connection[Any]:
    connection = psycopg.connect(
        **database.connection_kwargs(user, password),
        autocommit=True,
    )
    if owner:
        connection.execute("SET ROLE dante_owner")
    return connection


def _admin(database: Any) -> psycopg.Connection[Any]:
    return psycopg.connect(
        host=database.cluster.host,
        port=database.cluster.port,
        dbname=database.name,
        user=database.cluster.admin_user,
        password=database.cluster.admin_password,
        autocommit=True,
    )


def _postgres_lock_key(
    connection: psycopg.Connection[Any],
    namespace: int,
    ref: UUID,
) -> int:
    row = connection.execute(
        """
        SELECT ((%s::bigint << 56)
          | (get_byte(d,0)::bigint << 48) | (get_byte(d,1)::bigint << 40)
          | (get_byte(d,2)::bigint << 32) | (get_byte(d,3)::bigint << 24)
          | (get_byte(d,4)::bigint << 16) | (get_byte(d,5)::bigint << 8)
          | get_byte(d,6)::bigint)
        FROM (
            SELECT sha256(
                convert_to('dante-lock-v2','UTF8') || uuid_send(%s::uuid)
            ) AS d
        ) AS digest
        """,
        (namespace, ref),
    ).fetchone()
    assert row is not None
    return int(row[0])


def _create_source(
    connection: psycopg.Connection[Any],
    family: Literal["quota", "elapsed"],
) -> tuple[UUID, UUID, datetime]:
    routine_ref, state_ref = uuid7(), uuid7()
    anchor = datetime(2026, 1, 1, 12, 0, tzinfo=UTC)
    with connection.transaction():
        connection.execute(
            "INSERT INTO dante.routine(routine_ref) VALUES (%s)",
            (routine_ref,),
        )
        connection.execute(
            "INSERT INTO dante.native_address(native_ref,owner_family) "
            "VALUES (%s,'routine')",
            (routine_ref,),
        )
        connection.execute(
            "INSERT INTO dante.material_state_address"
            "(material_state_ref,native_owner_ref,facet_code) "
            "VALUES (%s,%s,'routine.recurrence')",
            (state_ref, routine_ref),
        )
        recurrence_family = "quota_per_period" if family == "quota" else "elapsed_interval"
        connection.execute(
            "INSERT INTO dante.routine_recurrence_state"
            "(material_state_ref,routine_ref,family_code,range_kind) "
            "VALUES (%s,%s,%s,'open')",
            (state_ref, routine_ref, recurrence_family),
        )
        if family == "quota":
            connection.execute(
                "INSERT INTO dante.routine_recurrence_quota_state"
                "(material_state_ref,quota_count,period_unit_code,period_span,frame_code) "
                "VALUES (%s,1,'day',1,'floating_local')",
                (state_ref,),
            )
        else:
            connection.execute(
                "INSERT INTO dante.routine_recurrence_elapsed_state"
                "(material_state_ref,elapsed_seconds,anchor_mode_code,anchor_at) "
                "VALUES (%s,60.000000,'fixed_anchor',%s)",
                (state_ref, anchor),
            )
        connection.execute(
            "INSERT INTO dante.routine_recurrence_current_history"
            "(routine_ref,material_state_ref,current_from_at) VALUES (%s,%s,%s)",
            (routine_ref, state_ref, anchor - timedelta(hours=1)),
        )
        connection.execute(
            "INSERT INTO dante.native_current_material_state"
            "(native_owner_ref,facet_code,material_state_ref) "
            "VALUES (%s,'routine.recurrence',%s)",
            (routine_ref, state_ref),
        )
    return routine_ref, state_ref, anchor


def _insert_generation(
    connection: psycopg.Connection[Any],
    family: Literal["quota", "elapsed"],
    routine_ref: UUID,
    state_ref: UUID,
    anchor: datetime,
) -> None:
    occurrence_ref = uuid7()
    connection.execute(
        "INSERT INTO dante.occurrence(occurrence_ref) VALUES (%s)",
        (occurrence_ref,),
    )
    connection.execute(
        "INSERT INTO dante.occurrence_generation"
        "(occurrence_ref,source_native_ref,governing_recurrence_state_ref,origin_code) "
        "VALUES (%s,%s,%s,'recurrence_generated')",
        (occurrence_ref, routine_ref, state_ref),
    )
    if family == "quota":
        connection.execute(
            "INSERT INTO dante.occurrence_generation_quota"
            "(occurrence_ref,period_start_date,period_end_date_exclusive,frame_code) "
            "VALUES (%s,%s,%s,'floating_local')",
            (occurrence_ref, date(2026, 1, 1), date(2026, 1, 2)),
        )
    else:
        connection.execute(
            "INSERT INTO dante.occurrence_generation_elapsed(occurrence_ref,expected_at) "
            "VALUES (%s,%s)",
            (occurrence_ref, anchor + timedelta(seconds=60)),
        )


def _race(database: Any, family: Literal["quota", "elapsed"]) -> list[str]:
    with _connect(
        database,
        "dante_migrator",
        database.cluster.migrator_password,
        owner=True,
    ) as owner:
        routine_ref, state_ref, anchor = _create_source(owner, family)
    barrier = Barrier(2)

    def worker() -> str:
        try:
            with (
                _connect(
                    database,
                    "dante_runtime",
                    database.cluster.runtime_password,
                ) as runtime,
                runtime.transaction(),
            ):
                _insert_generation(runtime, family, routine_ref, state_ref, anchor)
                barrier.wait(timeout=10)
            return "PASS"
        except psycopg.Error as error:
            return str(error.sqlstate)

    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = [executor.submit(worker) for _ in range(2)]
        return [future.result(timeout=20) for future in futures]


def test_cp6_final_python_and_postgresql_lock_contract(migrated_database: Any) -> None:
    with _admin(migrated_database) as connection:
        for namespace, expected in _GOLDEN_KEYS.items():
            assert advisory_lock_key(namespace, _GOLDEN_REF) == expected
            assert _postgres_lock_key(connection, namespace, _GOLDEN_REF) == expected
    assert occurrence_generation_lock_keys("routine", _GOLDEN_REF) == (
        _GOLDEN_KEYS[4],
        _GOLDEN_KEYS[6],
    )
    assert occurrence_generation_lock_keys("event", _GOLDEN_REF) == (
        _GOLDEN_KEYS[5],
        _GOLDEN_KEYS[7],
    )


@pytest.mark.asyncio
async def test_cp6_final_async_lock_helper_is_transaction_scoped(
    migrated_database: Any,
) -> None:
    runtime = create_database_runtime(migrated_database.runtime_settings())
    first, second = occurrence_generation_lock_keys("routine", _GOLDEN_REF)
    try:
        async with runtime.session_factory() as session:
            with pytest.raises(RuntimeError, match="active AsyncSession transaction"):
                await acquire_advisory_xact_locks(session, [first])
            async with session.begin():
                await acquire_advisory_xact_locks(session, [second, first, second])
                held = (
                    await session.execute(
                        text(
                            "SELECT count(*) FROM pg_locks "
                            "WHERE locktype='advisory' "
                            "AND pid=pg_backend_pid() AND granted"
                        )
                    )
                ).scalar_one()
                assert held == 2
                with _connect(
                    migrated_database,
                    "dante_runtime",
                    migrated_database.cluster.runtime_password,
                ) as probe:
                    result = probe.execute(
                        "SELECT pg_try_advisory_xact_lock(%s),"
                        "pg_try_advisory_xact_lock(%s)",
                        (first, second),
                    ).fetchone()
                    assert result == (False, False)
        with _connect(
            migrated_database,
            "dante_runtime",
            migrated_database.cluster.runtime_password,
        ) as probe:
            result = probe.execute(
                "SELECT pg_try_advisory_xact_lock(%s),pg_try_advisory_xact_lock(%s)",
                (first, second),
            ).fetchone()
            assert result == (True, True)
    finally:
        await runtime.dispose()


def test_cp6_final_role13_and_real_concurrency(migrated_database: Any) -> None:
    with _admin(migrated_database) as connection:
        row = connection.execute(
            "SELECT pg_get_functiondef(p.oid) "
            "FROM pg_proc p JOIN pg_namespace n ON n.oid=p.pronamespace "
            "WHERE n.nspname='dante' "
            "AND p.proname='enforce_occurrence_generation_integrity'"
        ).fetchone()
    assert row is not None
    definition = str(row[0])
    assert "pg_advisory_xact_lock" in definition
    assert "dante-lock-v2" in definition
    assert "FOR UPDATE" not in definition
    assert "CP6-M07: Part-14 advisory locks" not in definition
    assert sorted(_race(migrated_database, "quota")) == ["23514", "PASS"]
    assert sorted(_race(migrated_database, "elapsed")) == ["23514", "PASS"]


def test_cp6_final_revision_downgrades_exactly_to_m7(
    provisioned_database: Any,
    alembic_config: Config,
) -> None:
    command.upgrade(alembic_config, _FINAL_REVISION)
    command.downgrade(alembic_config, "20260826_07")
    with _admin(provisioned_database) as connection:
        row = connection.execute(
            "SELECT pg_get_functiondef(p.oid) "
            "FROM pg_proc p JOIN pg_namespace n ON n.oid=p.pronamespace "
            "WHERE n.nspname='dante' "
            "AND p.proname='enforce_occurrence_generation_integrity'"
        ).fetchone()
    assert row is not None
    definition = str(row[0])
    assert "CP6-M07: Part-14 advisory locks" in definition
    assert "dante-lock-v2" not in definition
    assert "pg_advisory_xact_lock" not in definition
    command.upgrade(alembic_config, _FINAL_REVISION)
