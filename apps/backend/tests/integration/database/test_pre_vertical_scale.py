"""Real PostgreSQL proof for bounded PV-03 scale-harness first-use convergence."""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from datetime import UTC, datetime
from threading import Barrier
from typing import Any
from uuid import UUID

import psycopg
import pytest

from tooling.pre_vertical_foundation.scale import ScaleProfile, build_scale_plan

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


def _runtime(database: Any) -> psycopg.Connection[Any]:
    return psycopg.connect(
        **database.connection_kwargs(
            "dante_runtime",
            database.cluster.runtime_password,
        ),
        autocommit=True,
    )


def _ensure_candidate(
    database: Any,
    *,
    barrier: Barrier,
    account_ref: UUID,
    candidate_self_person_ref: UUID,
) -> tuple[UUID, UUID, str, str | None]:
    with _runtime(database) as connection:
        barrier.wait(timeout=5)
        row = connection.execute(
            """
            SELECT account_ref,self_person_ref,timezone_mode,fixed_zone_id
            FROM dante.ensure_account_application_context(%s,%s)
            """,
            (account_ref, candidate_self_person_ref),
        ).fetchone()
    assert row is not None
    return UUID(str(row[0])), UUID(str(row[1])), str(row[2]), None if row[3] is None else str(row[3])


def test_small_profile_concurrent_first_use_converges_to_one_self_person(
    migrated_database: Any,
) -> None:
    """Twelve bounded contenders prove semantics, not a workload or performance budget."""
    plan = build_scale_plan(ScaleProfile.SMALL)
    account_ref = plan[0].account_ref
    candidates = tuple(item.self_person_ref for item in plan)

    with _owner(migrated_database) as connection:
        connection.execute(
            """
            INSERT INTO dante.account(account_ref,status_code,created_at,disabled_at)
            VALUES (%s,'active',%s,NULL)
            """,
            (account_ref, datetime(2026, 9, 6, 12, 0, tzinfo=UTC)),
        )

    barrier = Barrier(len(candidates))
    with ThreadPoolExecutor(max_workers=len(candidates)) as executor:
        futures = [
            executor.submit(
                _ensure_candidate,
                migrated_database,
                barrier=barrier,
                account_ref=account_ref,
                candidate_self_person_ref=candidate,
            )
            for candidate in candidates
        ]
        results = [future.result(timeout=10) for future in futures]

    assert len(set(results)) == 1
    resolved = results[0]
    assert resolved[0] == account_ref
    assert resolved[1] in candidates
    assert resolved[2:] == ("follow_device", None)

    with _owner(migrated_database) as connection:
        counts = connection.execute(
            """
            SELECT
              (SELECT count(*) FROM dante.account_application_context WHERE account_ref=%s),
              (SELECT count(*) FROM dante.person WHERE person_ref = ANY(%s::uuid[])),
              (SELECT count(*) FROM dante.native_address
                 WHERE native_ref = ANY(%s::uuid[]) AND owner_family='person')
            """,
            (account_ref, list(candidates), list(candidates)),
        ).fetchone()

    assert counts == (1, 1, 1)
