"""Owner isolation, real runtime transitions, untimed provenance and retirement."""

from datetime import UTC, datetime, timedelta
from types import SimpleNamespace
from typing import Any, cast

import psycopg
import pytest
from fastapi import Request, Response
from sqlalchemy import text
from tests.integration.temporal.test_activity_quick_authoring_metadata import _seed_self

from dante.context.contracts import DanteContext
from dante.modules.temporal.authoring import TemporalAuthoringApplication
from dante.modules.temporal.schedule import AbsoluteIntervalPlacement
from dante.modules.temporal.session_panel_api import get_session_panel
from dante.modules.temporal.session_runtime import (
    SessionApplication,
    SessionCaptureDisabledError,
    SessionNotFoundError,
)
from dante.platform.database.references import ScopedRecordRef
from dante.platform.database.runtime import create_database_runtime

pytestmark = pytest.mark.postgres


def _fake_context(actor: object, zone_id: str = "UTC") -> DanteContext:
    """The Session Panel route only reads the actor and effective time zone."""
    return cast(
        DanteContext,
        SimpleNamespace(self_person_ref=actor, effective_zone_id=zone_id),
    )


def _fake_request(runtime: Any) -> Request:
    """Test the same app-state seam without a live ASGI request."""
    return cast(
        Request,
        SimpleNamespace(app=SimpleNamespace(state=SimpleNamespace(database_runtime=runtime))),
    )


@pytest.mark.asyncio
async def test_panel_untimed_start_pause_resume_stop_owner_isolation_and_no_actual(
    migrated_database: Any,
) -> None:
    actor, other = _seed_self(migrated_database), _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    request = _fake_request(runtime)
    context = _fake_context(actor, "Europe/Rome")
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
        other_panel = await get_session_panel(_fake_context(other), request, Response())
        assert other_panel.groups == []
        sessions = SessionApplication(runtime.session_factory)
        main = await sessions.start(
            self_person_ref=actor,
            subject_kind="activity",
            subject_native_ref=created.item.subject_native_ref,
            operation_id="panel:main:start",
        )
        assert main.open
        assert planned.planned_schedule_ref is not None
        started = await sessions.start_planned(
            self_person_ref=actor,
            operation_id="panel:start",
            activity_ref=created.item.subject_native_ref,
            schedule_ref=ScopedRecordRef(planned.planned_schedule_ref),
        )
        replay = await sessions.start_planned(
            self_person_ref=actor,
            operation_id="panel:start",
            activity_ref=created.item.subject_native_ref,
            schedule_ref=ScopedRecordRef(planned.planned_schedule_ref),
        )
        assert replay.replayed
        assert replay.session_ref == started.session_ref
        with pytest.raises(SessionNotFoundError):
            await sessions.start_planned(
                self_person_ref=other,
                operation_id="panel:other",
                activity_ref=created.item.subject_native_ref,
                schedule_ref=ScopedRecordRef(planned.planned_schedule_ref),
            )
        panel = await get_session_panel(context, request, Response())
        live = next(r for r in panel.groups[0].rows if r.planned_schedule_ref)
        assert live.execution is not None
        assert live.execution.session_ref == started.session_ref
        paused = await sessions.pause(
            self_person_ref=actor,
            session_ref=started.session_ref,
            expected_material_state_ref=started.timing_material_state_ref,
            operation_id="panel:pause",
        )
        panel = await get_session_panel(context, request, Response())
        paused_row = next(r for r in panel.groups[0].rows if r.planned_schedule_ref)
        assert paused_row.execution is not None
        assert paused_row.execution.paused
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
            row.planned_schedule_ref is not None for group in panel.groups for row in group.rows
        )  # finished child no longer masquerades as an unstarted row
        with psycopg.connect(
            **migrated_database.connection_kwargs(
                "dante_migrator",
                migrated_database.cluster.migrator_password,
            )
        ) as connection:
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
async def test_main_started_before_preview_exposes_all_children_and_preserves_cascade(
    migrated_database: Any,
) -> None:
    """Real DB read: main Play grants early child visibility, not automatic execution."""
    actor, outsider = _seed_self(migrated_database), _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    request = _fake_request(runtime)
    context = _fake_context(actor)
    now = datetime.now(UTC)
    try:
        created = await TemporalAuthoringApplication(runtime.session_factory).create_activity(
            self_person_ref=actor,
            operation_id="panel:main-early:create",
            title="Studio futuro",
            placement=AbsoluteIntervalPlacement(
                starts_at=now + timedelta(hours=2),
                ends_at=now + timedelta(hours=3),
            ),
            planned_slices=(None, None),
            planned_slice_names=("Ripasso", "Esercizi"),
            session_capture_mode="live",
        )
        activity = created.item.subject_native_ref
        before = await get_session_panel(context, request, Response())
        assert all(group.activity_ref != activity for group in before.groups)

        sessions = SessionApplication(runtime.session_factory)
        started = await sessions.start(
            self_person_ref=actor,
            subject_kind="activity",
            subject_native_ref=activity,
            operation_id="panel:main-early:start",
        )
        assert started.open

        panel = await get_session_panel(context, request, Response())
        group = next(group for group in panel.groups if group.activity_ref == activity)
        assert len(group.rows) == 3
        assert [row.name for row in group.rows] == [
            "Sessione attività", "Ripasso", "Esercizi",
        ]
        assert group.rows[0].execution is not None
        assert group.rows[0].execution.session_ref == started.session_ref
        assert all(row.execution is None for row in group.rows[1:])
        assert all(row.starts_at is None for row in group.rows[1:])
        assert len({row.planned_schedule_ref for row in group.rows[1:]}) == 2
        outsider_panel = await get_session_panel(
            _fake_context(outsider), request, Response()
        )
        assert all(group.activity_ref != activity for group in outsider_panel.groups)

        paused = await sessions.pause(
            self_person_ref=actor,
            session_ref=started.session_ref,
            expected_material_state_ref=started.timing_material_state_ref,
            operation_id="panel:main-early:pause",
        )
        paused_panel = await get_session_panel(context, request, Response())
        paused_group = next(
            group for group in paused_panel.groups if group.activity_ref == activity
        )
        assert len(paused_group.rows) == 3
        assert paused_group.rows[0].execution is not None
        assert paused_group.rows[0].execution.paused
        assert all(row.execution is None for row in paused_group.rows[1:])

        ended = await sessions.end(
            self_person_ref=actor,
            session_ref=started.session_ref,
            expected_material_state_ref=paused.timing_material_state_ref,
            operation_id="panel:main-early:stop",
        )
        assert not ended.open
        after = await get_session_panel(context, request, Response())
        assert all(group.activity_ref != activity for group in after.groups)
        # The Activity and its two planned children were never deleted.
        async with runtime.session_factory() as session, session.begin():
            refs = (
                (
                    await session.execute(
                        text(
                            "SELECT schedule_ref FROM dante.get_self_activity_schedule_roles("
                            ":actor, CAST(ARRAY[:activity] AS uuid[])) "
                            "WHERE role_code='planned'"
                        ),
                        {"actor": actor, "activity": activity},
                    )
                )
                .scalars()
                .all()
            )
        assert len(refs) == 2
    finally:
        await runtime.dispose()


@pytest.mark.asyncio
async def test_retired_untimed_row_cannot_start_and_is_not_projected(
    migrated_database: Any,
) -> None:
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
        assert schedule is not None
        with pytest.raises(SessionNotFoundError):
            await SessionApplication(runtime.session_factory).start_planned(
                self_person_ref=actor,
                operation_id="panel:retired:start",
                activity_ref=activity,
                schedule_ref=ScopedRecordRef(schedule),
            )
        panel = await get_session_panel(
            _fake_context(actor),
            _fake_request(runtime),
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
    request = _fake_request(runtime)
    ctx = _fake_context(actor)
    now = datetime.now(UTC)
    try:
        created = await TemporalAuthoringApplication(runtime.session_factory).create_activity(
            self_person_ref=actor,
            operation_id="panel:independent:create",
            title="Studio senza cronometro principale",
            placement=AbsoluteIntervalPlacement(
                starts_at=now - timedelta(minutes=15),
                ends_at=now + timedelta(minutes=45),
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
                self_person_ref=actor,
                subject_kind="activity",
                subject_native_ref=activity,
                operation_id="panel:independent:generic",
            )
        started = await sessions.start_planned(
            self_person_ref=actor,
            activity_ref=activity,
            schedule_ref=ScopedRecordRef(row.planned_schedule_ref),
            operation_id="panel:independent:planned",
        )
        assert started.open
        live = await get_session_panel(ctx, request, Response())
        assert live.groups[0].rows[0].execution is not None
        assert live.groups[0].rows[0].execution.session_ref == started.session_ref
        ended = await sessions.end(
            self_person_ref=actor,
            session_ref=started.session_ref,
            expected_material_state_ref=started.timing_material_state_ref,
            operation_id="panel:independent:end",
        )
        assert not ended.open
        after = await get_session_panel(ctx, request, Response())
        assert after.groups == []
        assert len(after.visuals) == 1
    finally:
        await runtime.dispose()


@pytest.mark.asyncio
async def test_two_simultaneous_activities_keep_independent_named_session_rows(
    migrated_database: Any,
) -> None:
    """Starting/stopping one Activity must not erase another Activity's ready rows."""
    actor = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    now = datetime.now(UTC)
    try:
        created = []
        for index, name in enumerate(("Studio", "Allenamento")):
            item = await TemporalAuthoringApplication(runtime.session_factory).create_activity(
                self_person_ref=actor,
                operation_id=f"panel:multi:create:{index}",
                title=name,
                placement=AbsoluteIntervalPlacement(
                    starts_at=now - timedelta(minutes=10),
                    ends_at=now + timedelta(minutes=25),
                ),
                planned_slices=(None,),
                planned_slice_names=(f"Parte {index + 1}",),
                session_capture_mode="disabled",
            )
            created.append(item.item.subject_native_ref)

        panel = await get_session_panel(_fake_context(actor), _fake_request(runtime), Response())
        assert {group.activity_ref for group in panel.groups} == set(created)
        rows = {
            group.activity_ref: next(
                row for row in group.rows if row.planned_schedule_ref is not None
            )
            for group in panel.groups
        }
        assert all(row.execution is None for row in rows.values())

        sessions = SessionApplication(runtime.session_factory)
        first_row = rows[created[0]]
        assert first_row.planned_schedule_ref is not None
        started = await sessions.start_planned(
            self_person_ref=actor,
            activity_ref=created[0],
            schedule_ref=ScopedRecordRef(first_row.planned_schedule_ref),
            operation_id="panel:multi:start",
        )
        running = await get_session_panel(_fake_context(actor), _fake_request(runtime), Response())
        assert {group.activity_ref for group in running.groups} == set(created)
        first_group = next(group for group in running.groups if group.activity_ref == created[0])
        assert any(
            row.execution and row.execution.session_ref == started.session_ref
            for row in first_group.rows
        )

        await sessions.end(
            self_person_ref=actor,
            session_ref=started.session_ref,
            expected_material_state_ref=started.timing_material_state_ref,
            operation_id="panel:multi:stop",
        )
        remaining = await get_session_panel(
            _fake_context(actor), _fake_request(runtime), Response()
        )
        assert {group.activity_ref for group in remaining.groups} == {created[1]}
        assert all(row.execution is None for row in remaining.groups[0].rows)
    finally:
        await runtime.dispose()


@pytest.mark.asyncio
async def test_named_session_can_start_before_activity_interval_from_direct_command(
    migrated_database: Any,
) -> None:
    """Starting a named execution early never shifts the accepted Activity plan."""
    actor = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    now = datetime.now(UTC)
    planned_start = now + timedelta(hours=2)
    planned_end = planned_start + timedelta(hours=1)
    try:
        created = await TemporalAuthoringApplication(runtime.session_factory).create_activity(
            self_person_ref=actor,
            operation_id="panel:early-named:create",
            title="Studio futuro",
            placement=AbsoluteIntervalPlacement(
                starts_at=planned_start,
                ends_at=planned_end,
            ),
            planned_slices=(None,),
            planned_slice_names=("Inizio anticipato",),
            session_capture_mode="disabled",
        )
        activity = created.item.subject_native_ref
        panel = await get_session_panel(_fake_context(actor), _fake_request(runtime), Response())
        # No fabricated preview row two hours before the planned Activity.
        assert all(group.activity_ref != activity for group in panel.groups)
        async with runtime.session_factory() as session, session.begin():
            refs = (
                (
                    await session.execute(
                        text(
                            "SELECT schedule_ref FROM dante.get_self_activity_schedule_roles("
                            ":actor, CAST(ARRAY[:activity] AS uuid[])) "
                            "WHERE role_code='planned'"
                        ),
                        {"actor": actor, "activity": activity},
                    )
                )
                .scalars()
                .all()
            )
        assert len(refs) == 1
        started = await SessionApplication(runtime.session_factory).start_planned(
            self_person_ref=actor,
            activity_ref=activity,
            schedule_ref=ScopedRecordRef(refs[0]),
            operation_id="panel:early-named:start",
        )
        assert started.open
        assert started.started_at < planned_start
        active = await get_session_panel(_fake_context(actor), _fake_request(runtime), Response())
        rows = [
            row for group in active.groups if group.activity_ref == activity for row in group.rows
        ]
        assert any(
            row.execution and row.execution.session_ref == started.session_ref for row in rows
        )
    finally:
        await runtime.dispose()
