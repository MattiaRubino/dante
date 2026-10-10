"""Owner isolation, real runtime transitions, untimed provenance and retirement."""

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
from dante.modules.temporal.session_runtime import (
    SessionApplication, SessionNotFoundError, SessionCaptureDisabledError,
)
from dante.platform.database.runtime import create_database_runtime

pytestmark = pytest.mark.postgres


@pytest.mark.asyncio
async def test_panel_untimed_start_pause_resume_stop_owner_isolation_and_no_actual(
    migrated_database: Any,
):
    actor, other = _seed_self(migrated_database), _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    request = SimpleNamespace(app=SimpleNamespace(state=SimpleNamespace(database_runtime=runtime)))
    context = SimpleNamespace(self_person_ref=actor, effective_zone_id="Europe/Rome")
    now = datetime.now(UTC)
    try:
        created = await TemporalAuthoringApplication(runtime.session_factory).create_activity(
            self_person_ref=actor,
            operation_id="panel:create",
            title="Studio",
            placement=AbsoluteIntervalPlacement(
                starts_at=now - timedelta(hours=1), ends_at=now + timedelta(hours=1)
            ),
            planned_slices=(None,),
            planned_slice_names=("Ripasso",),
            session_capture_mode="live",
        )
        response = Response()
        panel = await get_session_panel(context, request, response)
        assert response.headers["Cache-Control"] == "no-store"
        assert len(panel.groups) == 1
        assert panel.groups[0].activity_ref == created.item.subject_native_ref
        planned = next(r for r in panel.groups[0].rows if r.planned_schedule_ref)
        assert planned.name == "Ripasso"
        assert planned.execution is None
        other_panel = await get_session_panel(
            SimpleNamespace(self_person_ref=other, effective_zone_id="UTC"), request, Response()
        )
        assert other_panel.groups == []
        sessions = SessionApplication(runtime.session_factory)
        main = await sessions.start(
            self_person_ref=actor, subject_kind="activity",
            subject_native_ref=created.item.subject_native_ref,
            operation_id="panel:main:start",
        )
        assert main.open
        kwargs = {
            "self_person_ref": actor,
            "operation_id": "panel:start",
            "activity_ref": created.item.subject_native_ref,
            "schedule_ref": planned.planned_schedule_ref,
        }
        started = await sessions.start_planned(**kwargs)
        replay = await sessions.start_planned(**kwargs)
        assert replay.replayed
        assert replay.session_ref == started.session_ref
        with pytest.raises(SessionNotFoundError):
            await sessions.start_planned(
                **{**kwargs, "self_person_ref": other, "operation_id": "panel:other"}
            )
        panel = await get_session_panel(context, request, Response())
        live = next(r for r in panel.groups[0].rows if r.planned_schedule_ref)
        assert live.execution.session_ref == started.session_ref
        paused = await sessions.pause(
            self_person_ref=actor,
            session_ref=started.session_ref,
            expected_material_state_ref=started.timing_material_state_ref,
            operation_id="panel:pause",
        )
        panel = await get_session_panel(context, request, Response())
        assert next(r for r in panel.groups[0].rows if r.planned_schedule_ref).execution.paused
        resumed = await sessions.resume(
            self_person_ref=actor,
            session_ref=started.session_ref,
            expected_material_state_ref=paused.timing_material_state_ref,
            operation_id="panel:resume",
        )
        await sessions.end(
            self_person_ref=actor,
            session_ref=started.session_ref,
            expected_material_state_ref=resumed.timing_material_state_ref,
            operation_id="panel:end",
        )
        panel = await get_session_panel(context, request, Response())
        assert len(panel.groups) == 1  # main Session remains open
        assert not any(
            row.planned_schedule_ref is not None
            for group in panel.groups for row in group.rows
        )  # finished child no longer masquerades as an unstarted row
        with psycopg.connect(**migrated_database.connection_kwargs(
            "dante_migrator", migrated_database.cluster.migrator_password,
        )) as connection:
            connection.execute("SET ROLE dante_owner")
            assert connection.execute(
                "SELECT count(*) FROM dante.schedule_current_placement WHERE scoped_owner_ref=%s",
                (planned.planned_schedule_ref,),
            ).fetchone() == (0,)
            assert connection.execute(
                "SELECT count(*) FROM dante.actual WHERE subject_native_ref=%s",
                (created.item.subject_native_ref,),
            ).fetchone() == (0,)
    finally:
        await runtime.dispose()


@pytest.mark.asyncio
async def test_retired_untimed_row_cannot_start_and_is_not_projected(migrated_database: Any):
    actor = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    now = datetime.now(UTC)
    try:
        created = await TemporalAuthoringApplication(runtime.session_factory).create_activity(
            self_person_ref=actor,
            operation_id="panel:retire:create",
            title="Archivio",
            placement=AbsoluteIntervalPlacement(
                starts_at=now - timedelta(hours=1), ends_at=now + timedelta(hours=1)
            ),
            planned_slices=(None,),
            planned_slice_names=("Da eliminare",),
            session_capture_mode="live",
        )
        activity = created.item.subject_native_ref
        async with runtime.session_factory() as session, session.begin():
            schedule = await session.scalar(
                text(
                    "SELECT schedule_ref FROM dante.get_self_activity_schedule_roles(:actor,CAST(ARRAY[:activity] AS uuid[])) WHERE role_code='planned'"
                ),
                {"actor": actor, "activity": activity},
            )
            await session.execute(
                text("SELECT dante.retire_self_planned_schedule(:actor,:activity,:schedule)"),
                {"actor": actor, "activity": activity, "schedule": schedule},
            )
        with pytest.raises(SessionNotFoundError):
            await SessionApplication(runtime.session_factory).start_planned(
                self_person_ref=actor,
                operation_id="panel:retired:start",
                activity_ref=activity,
                schedule_ref=schedule,
            )
        panel = await get_session_panel(
            SimpleNamespace(self_person_ref=actor, effective_zone_id="UTC"),
            SimpleNamespace(app=SimpleNamespace(state=SimpleNamespace(database_runtime=runtime))),
            Response(),
        )
        assert [r.name for g in panel.groups for r in g.rows] == ["Sessione attività"]
    finally:
        await runtime.dispose()


@pytest.mark.asyncio
async def test_independent_untimed_planned_session_without_main_capture(
    migrated_database: Any,
) -> None:
    """The optional generic Activity clock stays disabled; named slice can run."""
    actor = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    request = SimpleNamespace(
        app=SimpleNamespace(state=SimpleNamespace(database_runtime=runtime))
    )
    ctx = SimpleNamespace(self_person_ref=actor, effective_zone_id="UTC")
    now = datetime.now(UTC)
    try:
        created = await TemporalAuthoringApplication(runtime.session_factory).create_activity(
            self_person_ref=actor, operation_id="panel:independent:create",
            title="Studio senza cronometro principale",
            placement=AbsoluteIntervalPlacement(
                starts_at=now-timedelta(minutes=15),
                ends_at=now+timedelta(minutes=45),
            ),
            planned_slices=(None,),
            planned_slice_names=("Ripasso indipendente",),
            session_capture_mode="disabled",
        )
        activity = created.item.subject_native_ref
        panel = await get_session_panel(ctx, request, Response())
        assert len(panel.groups) == 1
        assert [row.name for row in panel.groups[0].rows] == ["Ripasso indipendente"]
        row = panel.groups[0].rows[0]
        assert row.planned_schedule_ref is not None
        assert row.execution is None
        sessions = SessionApplication(runtime.session_factory)
        with pytest.raises(SessionCaptureDisabledError):
            await sessions.start(
                self_person_ref=actor, subject_kind="activity",
                subject_native_ref=activity, operation_id="panel:independent:generic",
            )
        started = await sessions.start_planned(
            self_person_ref=actor, activity_ref=activity,
            schedule_ref=row.planned_schedule_ref,
            operation_id="panel:independent:planned",
        )
        assert started.open
        live = await get_session_panel(ctx, request, Response())
        assert live.groups[0].rows[0].execution.session_ref == started.session_ref
        ended = await sessions.end(
            self_person_ref=actor, session_ref=started.session_ref,
            expected_material_state_ref=started.timing_material_state_ref,
            operation_id="panel:independent:end",
        )
        assert not ended.open
        after = await get_session_panel(ctx, request, Response())
        assert after.groups == []
        assert len(after.visuals) == 1
    finally:
        await runtime.dispose()
