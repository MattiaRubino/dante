"""Retrospective Session remains actual execution, never planned Schedule or Actual."""

from __future__ import annotations

import hashlib
from datetime import UTC, datetime, timedelta
from typing import Any
from uuid import uuid7

import psycopg
import pytest
from tests.integration.temporal.test_b04_f_constrained_activity_application import (
    _seed_activity,
    _seed_person,
)

from dante.modules.temporal.session_runtime import (
    SessionApplication,
    SessionCaptureDisabledError,
    SessionInputError,
    SessionOperationReuseError,
)
from dante.platform.database.runtime import create_database_runtime

pytestmark = pytest.mark.postgres


@pytest.mark.asyncio
async def test_manual_activity_session_requires_record_policy_and_is_idempotent(
    migrated_database: Any,
) -> None:
    actor = _seed_person(migrated_database)
    activity = _seed_activity(migrated_database, self_ref=actor, title="Past work")
    other = _seed_activity(migrated_database, self_ref=actor, title="Other work")
    runtime = create_database_runtime(migrated_database.runtime_settings())
    sessions = SessionApplication(runtime.session_factory)
    end = datetime.now(UTC) - timedelta(hours=1)
    start = end - timedelta(minutes=30)
    try:
        with pytest.raises(SessionCaptureDisabledError):
            await sessions.record_manual(
                self_person_ref=actor, operation_id="manual:disabled", activity_ref=activity,
                started_at=start, ended_at=end,
            )
        with psycopg.connect(**migrated_database.connection_kwargs(
            "dante_runtime", migrated_database.cluster.runtime_password,
        )) as connection:
            connection.execute(
                "SELECT * FROM dante.set_self_activity_execution_policy(%s,%s,%s,%s,%s,%s,%s)",
                (actor, "manual:policy", hashlib.sha256(b"manual:policy").hexdigest(),
                 activity, uuid7(), "record", None),
            )
        with pytest.raises(SessionCaptureDisabledError):
            await sessions.start(
                self_person_ref=actor, operation_id="manual:no-live", subject_kind="activity",
                subject_native_ref=activity,
            )
        created = await sessions.record_manual(
            self_person_ref=actor, operation_id="manual:accepted", activity_ref=activity,
            started_at=start, ended_at=end,
        )
        assert created.started_at == start
        assert created.ended_at == end
        assert not created.open
        assert not created.replayed
        replayed = await sessions.record_manual(
            self_person_ref=actor, operation_id="manual:accepted", activity_ref=activity,
            started_at=start, ended_at=end,
        )
        assert replayed.replayed
        assert replayed.session_ref == created.session_ref
        assert [item.session_ref for item in await sessions.list_for_subject(
            self_person_ref=actor, subject_native_ref=activity,
        )] == [created.session_ref]
        with pytest.raises(SessionOperationReuseError):
            await sessions.record_manual(
                self_person_ref=actor, operation_id="manual:accepted", activity_ref=other,
                started_at=start, ended_at=end,
            )
        with pytest.raises(SessionInputError):
            await sessions.record_manual(
                self_person_ref=actor, operation_id="manual:future", activity_ref=activity,
                started_at=end, ended_at=datetime.now(UTC) + timedelta(minutes=1),
            )
        with psycopg.connect(**migrated_database.connection_kwargs(
            "dante_migrator", migrated_database.cluster.migrator_password,
        )) as connection:
            connection.execute("SET ROLE dante_owner")
            assert connection.execute(
                "SELECT count(*) FROM dante.actual WHERE subject_native_ref=%s", (activity,)
            ).fetchone() == (0,)
    finally:
        await runtime.dispose()
