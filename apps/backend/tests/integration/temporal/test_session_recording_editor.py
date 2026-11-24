"""Retrospective Session edits preserve identity, history and main-child bounds."""

from datetime import UTC, datetime, timedelta
from types import SimpleNamespace
from typing import Any

import pytest
from fastapi import Request, Response
from sqlalchemy import text
from tests.integration.temporal.test_activity_quick_authoring_metadata import _seed_self
from tests.integration.temporal.test_schedule_create import _context

from dante.modules.temporal.activity_inspector_api import (
    ActivitySessionAttemptDeleteCommand,
    delete_self_activity_session_attempt,
    get_self_activity_session_impact,
)
from dante.modules.temporal.authoring import TemporalAuthoringApplication
from dante.modules.temporal.schedule import AbsoluteIntervalPlacement
from dante.modules.temporal.session_runtime import (
    SessionApplication,
    SessionEditorConflictError,
    SessionInputError,
)
from dante.platform.database.runtime import create_database_runtime

pytestmark = pytest.mark.postgres


@pytest.mark.asyncio
async def test_editor_records_then_corrects_concluded_sessions_without_reopening_them(
    migrated_database: Any,
) -> None:
    actor = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    end = datetime.now(UTC) - timedelta(hours=1)
    start = end - timedelta(hours=2)
    try:
        created = await TemporalAuthoringApplication(runtime.session_factory).create_activity(
            self_person_ref=actor,
            operation_id="editor:create",
            title="Work",
            placement=AbsoluteIntervalPlacement(starts_at=start, ends_at=end),
            planned_slices=(None,),
            planned_slice_names=("Focus",),
            session_capture_mode="record_and_live",
        )
        activity = created.item.subject_native_ref
        async with runtime.session_factory() as session, session.begin():
            planned = (
                await session.execute(
                    text("""SELECT schedule_ref FROM dante.get_self_activity_schedule_roles(
                        :actor,CAST(ARRAY[:activity] AS uuid[])) WHERE role_code='planned'"""),
                    {"actor": actor, "activity": activity},
                )
            ).scalar_one()
        application = SessionApplication(runtime.session_factory)
        main = await application.write_editor(
            self_person_ref=actor,
            operation_id="editor:main",
            activity_ref=activity,
            planned_schedule_ref=None,
            session_ref=None,
            expected_material_state_ref=None,
            started_at=start,
            ended_at=end,
            pause_ranges=[(start + timedelta(minutes=45), start + timedelta(minutes=55))],
        )
        assert not main.open
        replayed_main = await application.write_editor(
            self_person_ref=actor,
            operation_id="editor:main",
            activity_ref=activity,
            planned_schedule_ref=None,
            session_ref=None,
            expected_material_state_ref=None,
            started_at=start,
            ended_at=end,
            pause_ranges=[(start + timedelta(minutes=45), start + timedelta(minutes=55))],
        )
        assert replayed_main.replayed
        assert replayed_main.session_ref == main.session_ref
        child = await application.write_editor(
            self_person_ref=actor,
            operation_id="editor:child",
            activity_ref=activity,
            planned_schedule_ref=planned,
            session_ref=None,
            expected_material_state_ref=None,
            started_at=start + timedelta(minutes=10),
            ended_at=start + timedelta(minutes=40),
            pause_ranges=[],
        )
        assert child.planned_schedule_ref == planned
        with pytest.raises(SessionEditorConflictError):
            await application.write_editor(
                self_person_ref=actor,
                operation_id="editor:duplicate",
                activity_ref=activity,
                planned_schedule_ref=planned,
                session_ref=None,
                expected_material_state_ref=None,
                started_at=start + timedelta(minutes=10),
                ended_at=start + timedelta(minutes=40),
                pause_ranges=[],
            )
        corrected = await application.write_editor(
            self_person_ref=actor,
            operation_id="editor:correct",
            activity_ref=activity,
            planned_schedule_ref=planned,
            session_ref=child.session_ref,
            expected_material_state_ref=child.timing_material_state_ref,
            started_at=start + timedelta(minutes=12),
            ended_at=start + timedelta(minutes=42),
            pause_ranges=[(start + timedelta(minutes=20), start + timedelta(minutes=25))],
        )
        assert corrected.session_ref == child.session_ref
        assert corrected.timing_material_state_ref != child.timing_material_state_ref
        assert corrected.active_seconds == pytest.approx(25 * 60, abs=1)
        assert (
            await application.get(self_person_ref=actor, session_ref=child.session_ref)
        ).ended_at
        with pytest.raises(SessionEditorConflictError):
            await application.write_editor(
                self_person_ref=actor,
                operation_id="editor:stale",
                activity_ref=activity,
                planned_schedule_ref=planned,
                session_ref=child.session_ref,
                expected_material_state_ref=child.timing_material_state_ref,
                started_at=start + timedelta(minutes=10),
                ended_at=start + timedelta(minutes=40),
                pause_ranges=[],
            )
        with pytest.raises(SessionInputError):
            await application.write_editor(
                self_person_ref=actor,
                operation_id="editor:outside",
                activity_ref=activity,
                planned_schedule_ref=None,
                session_ref=main.session_ref,
                expected_material_state_ref=main.timing_material_state_ref,
                started_at=start + timedelta(minutes=30),
                ended_at=end,
                pause_ranges=[],
            )
        request = Request(
            {
                "type": "http",
                "app": SimpleNamespace(state=SimpleNamespace(database_runtime=runtime)),
            }
        )
        impact = await get_self_activity_session_impact(
            activity, _context(actor), request, Response()
        )
        await delete_self_activity_session_attempt(
            activity,
            child.session_ref,
            ActivitySessionAttemptDeleteCommand(expected_session_fingerprint=impact.fingerprint),
            _context(actor),
            request,
            Response(),
        )
        assert [
            item.session_ref
            for item in await application.list_for_subject(
                self_person_ref=actor, subject_native_ref=activity
            )
        ] == [main.session_ref]
    finally:
        await runtime.dispose()
