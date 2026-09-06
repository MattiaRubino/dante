"""Real PostgreSQL proof for the bounded authenticated DANTE application context."""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeoutError
from datetime import UTC, datetime
from typing import Any
from uuid import UUID, uuid4, uuid7

import psycopg
import pytest
from psycopg import errors

pytestmark = pytest.mark.postgres


def _owner(database: Any) -> psycopg.Connection[Any]:
    connection = psycopg.connect(
        **database.connection_kwargs(
            "dante_migrator",
            database.cluster.migrator_password,
        ),
        autocommit=True,
    )
    connection.execute("SET ROLE dante_owner")
    return connection


def _runtime(database: Any, *, autocommit: bool = True) -> psycopg.Connection[Any]:
    return psycopg.connect(
        **database.connection_kwargs(
            "dante_runtime",
            database.cluster.runtime_password,
        ),
        autocommit=autocommit,
    )


def _create_account(database: Any, *, status: str = "active") -> UUID:
    account_ref = uuid7()
    created_at = datetime(2026, 9, 6, 12, 0, tzinfo=UTC)
    disabled_at = created_at if status == "disabled" else None
    with _owner(database) as connection:
        connection.execute(
            """
            INSERT INTO dante.account(account_ref,status_code,created_at,disabled_at)
            VALUES (%s,%s,%s,%s)
            """,
            (account_ref, status, created_at, disabled_at),
        )
    return account_ref


def _ensure(
    connection: psycopg.Connection[Any],
    account_ref: UUID,
    self_person_ref: UUID,
) -> tuple[Any, ...]:
    row = connection.execute(
        """
        SELECT account_ref,self_person_ref,timezone_mode,fixed_zone_id
        FROM dante.ensure_account_application_context(%s,%s)
        """,
        (account_ref, self_person_ref),
    ).fetchone()
    assert row is not None
    return tuple(row)


def test_runtime_acl_is_narrow(migrated_database: Any) -> None:
    with _owner(migrated_database) as connection:
        acl = connection.execute(
            """
            SELECT
              has_table_privilege('dante_runtime','dante.account_application_context','SELECT'),
              has_table_privilege('dante_runtime','dante.account_application_context','INSERT'),
              has_table_privilege('dante_runtime','dante.account_application_context','UPDATE'),
              has_table_privilege('dante_runtime','dante.account_application_context','DELETE'),
              has_table_privilege('dante_runtime','dante.person','INSERT'),
              has_function_privilege(
                'dante_runtime',
                'dante.ensure_account_application_context(uuid,uuid)',
                'EXECUTE'
              ),
              has_function_privilege(
                'dante_migrator',
                'dante.ensure_account_application_context(uuid,uuid)',
                'EXECUTE'
              ),
              EXISTS (
                SELECT 1
                FROM pg_proc p
                JOIN pg_namespace n ON n.oid=p.pronamespace
                CROSS JOIN LATERAL aclexplode(COALESCE(p.proacl, acldefault('f', p.proowner))) acl
                WHERE n.nspname='dante'
                  AND p.oid=to_regprocedure('dante.ensure_account_application_context(uuid,uuid)')
                  AND acl.grantee=0
                  AND acl.privilege_type='EXECUTE'
              )
            """
        ).fetchone()
    assert acl == (True, False, False, False, False, True, False, False)


def test_ensure_is_idempotent_and_does_not_create_second_person(migrated_database: Any) -> None:
    account_ref = _create_account(migrated_database)
    first_person_ref = uuid7()
    discarded_person_ref = uuid7()

    with _runtime(migrated_database) as connection:
        first = _ensure(connection, account_ref, first_person_ref)
        second = _ensure(connection, account_ref, discarded_person_ref)

    assert first == (account_ref, first_person_ref, "follow_device", None)
    assert second == first

    with _owner(migrated_database) as connection:
        counts = connection.execute(
            """
            SELECT
              (SELECT count(*) FROM dante.account_application_context WHERE account_ref=%s),
              (SELECT count(*) FROM dante.person WHERE person_ref IN (%s,%s)),
              (SELECT count(*) FROM dante.native_address
                 WHERE native_ref IN (%s,%s) AND owner_family='person')
            """,
            (
                account_ref,
                first_person_ref,
                discarded_person_ref,
                first_person_ref,
                discarded_person_ref,
            ),
        ).fetchone()
    assert counts == (1, 1, 1)


def test_concurrent_first_use_serializes_on_account_and_returns_one_context(
    migrated_database: Any,
) -> None:
    account_ref = _create_account(migrated_database)
    first_person_ref = uuid7()
    second_person_ref = uuid7()

    executor = ThreadPoolExecutor(max_workers=1)
    try:
        with _runtime(migrated_database, autocommit=False) as first_connection:
            with first_connection.transaction():
                first = _ensure(first_connection, account_ref, first_person_ref)

                def contender() -> tuple[Any, ...]:
                    with _runtime(migrated_database) as second_connection:
                        return _ensure(second_connection, account_ref, second_person_ref)

                future = executor.submit(contender)
                with pytest.raises(FutureTimeoutError):
                    future.result(timeout=0.2)

            second = future.result(timeout=5)
    finally:
        executor.shutdown(wait=True, cancel_futures=True)

    assert first == (account_ref, first_person_ref, "follow_device", None)
    assert second == first

    with _owner(migrated_database) as connection:
        counts = connection.execute(
            """
            SELECT
              (SELECT count(*) FROM dante.account_application_context WHERE account_ref=%s),
              (SELECT count(*) FROM dante.person WHERE person_ref IN (%s,%s)),
              (SELECT count(*) FROM dante.native_address
                 WHERE native_ref IN (%s,%s) AND owner_family='person')
            """,
            (
                account_ref,
                first_person_ref,
                second_person_ref,
                first_person_ref,
                second_person_ref,
            ),
        ).fetchone()
    assert counts == (1, 1, 1)


def test_disabled_account_and_non_uuidv7_person_are_rejected(migrated_database: Any) -> None:
    disabled_account_ref = _create_account(migrated_database, status="disabled")
    active_account_ref = _create_account(migrated_database)
    rejected_person_ref = uuid7()
    uuid4_person_ref = uuid4()

    with _runtime(migrated_database) as connection:
        with pytest.raises(errors.CheckViolation):
            _ensure(connection, disabled_account_ref, rejected_person_ref)
        with pytest.raises(errors.CheckViolation):
            _ensure(connection, active_account_ref, uuid4_person_ref)

    with _owner(migrated_database) as connection:
        counts = connection.execute(
            """
            SELECT
              (SELECT count(*) FROM dante.account_application_context
                 WHERE account_ref IN (%s,%s)),
              (SELECT count(*) FROM dante.person WHERE person_ref IN (%s,%s))
            """,
            (
                disabled_account_ref,
                active_account_ref,
                rejected_person_ref,
                uuid4_person_ref,
            ),
        ).fetchone()
    assert counts == (0, 0)


def test_timezone_policy_rejects_invalid_fixed_zone_and_inconsistent_shape(
    migrated_database: Any,
) -> None:
    account_ref = _create_account(migrated_database)
    self_person_ref = uuid7()
    with _runtime(migrated_database) as connection:
        _ensure(connection, account_ref, self_person_ref)

    with _owner(migrated_database) as connection:
        connection.execute(
            """
            UPDATE dante.account_application_context
               SET timezone_mode='fixed', fixed_zone_id='Europe/Rome'
             WHERE account_ref=%s
            """,
            (account_ref,),
        )
        assert connection.execute(
            "SELECT timezone_mode,fixed_zone_id FROM dante.account_application_context WHERE account_ref=%s",
            (account_ref,),
        ).fetchone() == ("fixed", "Europe/Rome")

        with pytest.raises(errors.CheckViolation):
            connection.execute(
                """
                UPDATE dante.account_application_context
                   SET fixed_zone_id='Not/AZone'
                 WHERE account_ref=%s
                """,
                (account_ref,),
            )
        with pytest.raises(errors.CheckViolation):
            connection.execute(
                """
                UPDATE dante.account_application_context
                   SET fixed_zone_id='+02:00'
                 WHERE account_ref=%s
                """,
                (account_ref,),
            )
        with pytest.raises(errors.CheckViolation):
            connection.execute(
                """
                UPDATE dante.account_application_context
                   SET timezone_mode='follow_device', fixed_zone_id='Europe/Rome'
                 WHERE account_ref=%s
                """,
                (account_ref,),
            )

        connection.execute(
            """
            UPDATE dante.account_application_context
               SET timezone_mode='follow_device', fixed_zone_id=NULL
             WHERE account_ref=%s
            """,
            (account_ref,),
        )
