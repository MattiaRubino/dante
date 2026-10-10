"""B14: real PostgreSQL atomic main→internal Session semantics and historical visuals."""

from datetime import UTC, datetime, timedelta
from types import SimpleNamespace
from typing import Any

import psycopg
import pytest
from fastapi import Response
from sqlalchemy import text
from tests.integration.temporal.test_b14_u2_authoring import _seed_self

from dante.modules.temporal.authoring import TemporalAuthoringApplication
from dante.modules.temporal.schedule import AbsoluteIntervalPlacement
from dante.modules.temporal.session_panel_api import get_session_panel
from dante.modules.temporal.session_runtime import SessionApplication, SessionInputError
from dante.platform.database.runtime import create_database_runtime

pytestmark = pytest.mark.postgres


@pytest.mark.asyncio
async def test_main_pause_resume_end_are_atomic_and_internal_actions_not_inverse(
    migrated_database: Any,
) -> None:
    actor = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    now = datetime.now(UTC)
    try:
        created = await TemporalAuthoringApplication(runtime.session_factory).create_activity(
            self_person_ref=actor,
            operation_id="hierarchy:create",
            title="Allenamento",
            placement=AbsoluteIntervalPlacement(
                starts_at=now - timedelta(minutes=10),
                ends_at=now + timedelta(hours=2),
            ),
            planned_slices=(None, None),
            planned_slice_names=("Riscaldamento", "Pesi"),
            session_capture_mode="live",
        )
        activity = created.item.subject_native_ref
        async with runtime.session_factory() as session, session.begin():
            refs = (await session.execute(text("""
                SELECT schedule_ref FROM dante.get_self_activity_schedule_roles(
                    :actor,CAST(ARRAY[:activity] AS uuid[])
                ) WHERE role_code='planned' ORDER BY presentation_order
            """), {"actor": actor, "activity": activity})).scalars().all()
        assert len(refs) == 2
        sessions = SessionApplication(runtime.session_factory)
        # No child starts independently of its generic Activity execution.
        with pytest.raises(SessionInputError):
            await sessions.start_planned(
                self_person_ref=actor, activity_ref=activity,
                schedule_ref=refs[0], operation_id="hierarchy:early-child",
            )
        main = await sessions.start(
            self_person_ref=actor, subject_kind="activity",
            subject_native_ref=activity, operation_id="hierarchy:main",
        )
        first = await sessions.start_planned(
            self_person_ref=actor, activity_ref=activity,
            schedule_ref=refs[0], operation_id="hierarchy:first",
        )
        second = await sessions.start_planned(
            self_person_ref=actor, activity_ref=activity,
            schedule_ref=refs[1], operation_id="hierarchy:second",
        )
        # Pausing a child never pauses its main.
        child_pause = await sessions.pause(
            self_person_ref=actor, session_ref=first.session_ref,
            expected_material_state_ref=first.timing_material_state_ref,
            operation_id="hierarchy:child-pause",
        )
        assert not (await sessions.get(
            self_person_ref=actor, session_ref=main.session_ref,
        )).paused

        parent_pause = await sessions.pause(
            self_person_ref=actor, session_ref=main.session_ref,
            expected_material_state_ref=main.timing_material_state_ref,
            operation_id="hierarchy:main-pause",
        )
        assert parent_pause.paused
        assert (await sessions.get(
            self_person_ref=actor, session_ref=first.session_ref,
        )).paused
        assert (await sessions.get(
            self_person_ref=actor, session_ref=second.session_ref,
        )).paused
        # A parent resume never resumes any child automatically.
        parent_resume = await sessions.resume(
            self_person_ref=actor, session_ref=main.session_ref,
            expected_material_state_ref=parent_pause.timing_material_state_ref,
            operation_id="hierarchy:main-resume",
        )
        assert not parent_resume.paused
        assert (await sessions.get(
            self_person_ref=actor, session_ref=first.session_ref,
        )).paused
        assert (await sessions.get(
            self_person_ref=actor, session_ref=second.session_ref,
        )).paused
        child_resume = await sessions.resume(
            self_person_ref=actor, session_ref=first.session_ref,
            expected_material_state_ref=child_pause.timing_material_state_ref,
            operation_id="hierarchy:child-resume",
        )
        assert not child_resume.paused
        assert not (await sessions.get(
            self_person_ref=actor, session_ref=main.session_ref,
        )).paused
        # Main stop closes both running and paused child executions.
        ended = await sessions.end(
            self_person_ref=actor, session_ref=main.session_ref,
            expected_material_state_ref=parent_resume.timing_material_state_ref,
            operation_id="hierarchy:main-stop",
        )
        assert not ended.open
        for ref in (first.session_ref, second.session_ref):
            assert not (await sessions.get(self_person_ref=actor, session_ref=ref)).open
        # Accepted replay never invents additional attempts or recomputes cascade.
        replay = await sessions.end(
            self_person_ref=actor, session_ref=main.session_ref,
            expected_material_state_ref=parent_resume.timing_material_state_ref,
            operation_id="hierarchy:main-stop",
        )
        assert replay.replayed
        assert replay.session_ref == main.session_ref

        request = SimpleNamespace(
            app=SimpleNamespace(state=SimpleNamespace(database_runtime=runtime)))
        context = SimpleNamespace(self_person_ref=actor, effective_zone_id="UTC")
        result = await get_session_panel(
            context, request, Response(),
            now - timedelta(days=1), now + timedelta(days=1),
        )
        assert len(result.visuals) == 3
        assert all(r.ended_at is not None for r in result.visuals)
        assert any(r.pause_ranges for r in result.visuals)
        # Runtime role has no direct Actual-table grant; inspect under
        # dedicated test migrator/owner identity, not application credentials.
        with psycopg.connect(**migrated_database.connection_kwargs(
            "dante_migrator", migrated_database.cluster.migrator_password,
        )) as connection:
            connection.execute("SET ROLE dante_owner")
            assert connection.execute(
                "SELECT count(*) FROM dante.actual WHERE subject_native_ref=%s",
                (activity,),
            ).fetchone() == (0,)
    finally:
        await runtime.dispose()


@pytest.mark.asyncio
async def test_internal_resume_is_blocked_while_main_is_paused(
    migrated_database: Any,
) -> None:
    actor = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    now = datetime.now(UTC)
    try:
        created = await TemporalAuthoringApplication(runtime.session_factory).create_activity(
            self_person_ref=actor, operation_id="paused-main:create",
            title="Studio",
            placement=AbsoluteIntervalPlacement(
                starts_at=now - timedelta(minutes=5),
                ends_at=now + timedelta(hours=1)),
            planned_slices=(None,), planned_slice_names=("Ripasso",),
            session_capture_mode="live",
        )
        activity = created.item.subject_native_ref
        async with runtime.session_factory() as session, session.begin():
            planned = await session.scalar(text("""
                SELECT schedule_ref FROM dante.get_self_activity_schedule_roles(
                    :actor,CAST(ARRAY[:activity] AS uuid[])
                ) WHERE role_code='planned'
            """), {"actor": actor, "activity": activity})
        sessions = SessionApplication(runtime.session_factory)
        main = await sessions.start(
            self_person_ref=actor, subject_kind="activity",
            subject_native_ref=activity, operation_id="paused-main:main",
        )
        child = await sessions.start_planned(
            self_person_ref=actor, activity_ref=activity,
            schedule_ref=planned, operation_id="paused-main:child",
        )
        await sessions.pause(
            self_person_ref=actor, session_ref=main.session_ref,
            expected_material_state_ref=main.timing_material_state_ref,
            operation_id="paused-main:pause",
        )
        paused_child = await sessions.get(
            self_person_ref=actor, session_ref=child.session_ref,
        )
        assert paused_child.paused
        with pytest.raises(SessionInputError):
            await sessions.resume(
                self_person_ref=actor, session_ref=child.session_ref,
                expected_material_state_ref=paused_child.timing_material_state_ref,
                operation_id="paused-main:child-resume",
            )
    finally:
        await runtime.dispose()
