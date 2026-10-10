"""A planned Schedule remains planning; explicitly starting it creates a linked Session."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Any

import psycopg
import pytest
from sqlalchemy import text
from tests.integration.temporal.test_b14_u2_authoring import _seed_self

from dante.modules.temporal.authoring import TemporalAuthoringApplication
from dante.modules.temporal.schedule import AbsoluteIntervalPlacement
from dante.modules.temporal.session_runtime import (
    SessionApplication,
    SessionNotFoundError,
    SessionOperationReuseError,
)
from dante.platform.database.runtime import create_database_runtime

pytestmark = pytest.mark.postgres


@pytest.mark.asyncio
async def test_planned_start_is_linked_replayable_and_never_actual(
    migrated_database: Any,
) -> None:
    actor = _seed_self(migrated_database)
    other_actor = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    try:
        created = await TemporalAuthoringApplication(runtime.session_factory).create_activity(
            self_person_ref=actor,
            operation_id="planned:activity",
            title="Preparazione",
            placement=AbsoluteIntervalPlacement(
                starts_at=datetime(2026, 10, 20, 8, tzinfo=UTC),
                ends_at=datetime(2026, 10, 20, 12, tzinfo=UTC),
            ),
            planned_slices=(
                AbsoluteIntervalPlacement(
                    starts_at=datetime(2026, 10, 20, 9, tzinfo=UTC),
                    ends_at=datetime(2026, 10, 20, 10, tzinfo=UTC),
                ),
            ),
            session_capture_mode="live",
        )
        activity_ref = created.item.subject_native_ref
        schedule_ref = created.planned_slices[0].schedule_ref
        sessions = SessionApplication(runtime.session_factory)
        with pytest.raises(SessionNotFoundError):
            await sessions.start_planned(
                self_person_ref=other_actor,
                operation_id="other:planned",
                activity_ref=activity_ref,
                schedule_ref=schedule_ref,
            )
        assert created.schedule is not None
        with pytest.raises(SessionNotFoundError):
            await sessions.start_planned(
                self_person_ref=actor,
                operation_id="planned:wrong-role",
                activity_ref=activity_ref,
                schedule_ref=created.schedule.schedule_ref,
            )
        started = await sessions.start_planned(
            self_person_ref=actor,
            operation_id="planned:start",
            activity_ref=activity_ref,
            schedule_ref=schedule_ref,
        )
        assert started.planned_schedule_ref == schedule_ref
        assert started.subject_native_ref == activity_ref
        assert started.open
        # The Activity editor must detect linked execution through existing
        # self-scoped functions; dante_runtime has no direct table SELECT grant.
        async with runtime.session_factory() as session, session.begin():
            linked = await session.scalar(text("""
                SELECT EXISTS(
                    SELECT 1
                      FROM dante.list_self_subject_sessions(:actor,:activity) AS execution
                     WHERE dante.get_self_session_planned_schedule(
                         :actor,execution.session_ref)=:schedule
                )
            """), {"actor": actor, "activity": activity_ref, "schedule": schedule_ref})
        assert linked is True
        replayed = await sessions.start_planned(
            self_person_ref=actor,
            operation_id="planned:start",
            activity_ref=activity_ref,
            schedule_ref=schedule_ref,
        )
        assert replayed.replayed
        assert replayed.session_ref == started.session_ref
        with pytest.raises(SessionOperationReuseError):
            await sessions.start(
                self_person_ref=actor,
                operation_id="planned:start",
                subject_kind="activity",
                subject_native_ref=activity_ref,
            )
        listed = await sessions.list_for_subject(
            self_person_ref=actor,
            subject_native_ref=activity_ref,
        )
        assert listed[0].planned_schedule_ref == schedule_ref
        with psycopg.connect(
            **migrated_database.connection_kwargs(
                "dante_migrator", migrated_database.cluster.migrator_password,
            )
        ) as connection:
            connection.execute("SET ROLE dante_owner")
            assert connection.execute(
                "SELECT count(*) FROM dante.actual WHERE subject_native_ref=%s", (activity_ref,)
            ).fetchone() == (0,)
    finally:
        await runtime.dispose()
