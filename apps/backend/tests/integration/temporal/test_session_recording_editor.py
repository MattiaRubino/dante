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
    SessionEditorWrite,
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


@pytest.mark.asyncio
async def test_grouped_recording_rolls_back_main_when_child_overlaps_parent_pause(
    migrated_database: Any,
) -> None:
    actor = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    end = datetime.now(UTC) - timedelta(hours=2)
    start = end - timedelta(hours=2)
    try:
        created = await TemporalAuthoringApplication(runtime.session_factory).create_activity(
            self_person_ref=actor,
            operation_id="editor-batch:create",
            title="Grouped recording",
            placement=AbsoluteIntervalPlacement(starts_at=start, ends_at=end),
            planned_slices=(None,),
            planned_slice_names=("Reading",),
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
        main = SessionEditorWrite(
            operation_id="editor-batch:main",
            planned_schedule_ref=None,
            session_ref=None,
            expected_material_state_ref=None,
            started_at=start,
            ended_at=end,
            pause_ranges=((start + timedelta(minutes=45), start + timedelta(minutes=60)),),
        )
        invalid_child = SessionEditorWrite(
            operation_id="editor-batch:invalid-child",
            planned_schedule_ref=planned,
            session_ref=None,
            expected_material_state_ref=None,
            started_at=start + timedelta(minutes=30),
            ended_at=start + timedelta(minutes=65),
            pause_ranges=(),
        )
        with pytest.raises(SessionInputError):
            await application.write_editor_batch(
                self_person_ref=actor,
                activity_ref=activity,
                commands=(invalid_child, main),
            )
        assert not await application.list_for_subject(
            self_person_ref=actor, subject_native_ref=activity
        ), "A failed child must roll back the main, not leave a partial recording."
        valid_child = SessionEditorWrite(
            operation_id="editor-batch:valid-child",
            planned_schedule_ref=planned,
            session_ref=None,
            expected_material_state_ref=None,
            started_at=start + timedelta(minutes=10),
            ended_at=start + timedelta(minutes=35),
            pause_ranges=(),
        )
        records = await application.write_editor_batch(
            self_person_ref=actor,
            activity_ref=activity,
            commands=(valid_child, main),
        )
        assert len(records) == 2
        assert records[0].planned_schedule_ref is None
        assert records[1].planned_schedule_ref == planned
        assert all(not record.open for record in records)
        same = await application.write_editor_batch(
            self_person_ref=actor,
            activity_ref=activity,
            commands=(main, valid_child),
        )
        assert [record.session_ref for record in same] == [record.session_ref for record in records]
        assert all(record.replayed for record in same)
        assert (
            len(
                await application.list_for_subject(
                    self_person_ref=actor, subject_native_ref=activity
                )
            )
            == 2
        )
    finally:
        await runtime.dispose()


@pytest.mark.asyncio
async def test_grouped_editor_records_named_sessions_without_inventing_a_main(
    migrated_database: Any,
) -> None:
    actor = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    end = datetime.now(UTC) - timedelta(hours=1)
    start = end - timedelta(hours=1)
    try:
        created = await TemporalAuthoringApplication(runtime.session_factory).create_activity(
            self_person_ref=actor,
            operation_id="editor-independent:create",
            title="Independent sessions",
            placement=AbsoluteIntervalPlacement(starts_at=start, ends_at=end),
            planned_slices=(None,),
            planned_slice_names=("Independent",),
            session_capture_mode="disabled",
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
        result = await application.write_editor_batch(
            self_person_ref=actor,
            activity_ref=activity,
            commands=(
                SessionEditorWrite(
                    operation_id="editor-independent:record",
                    planned_schedule_ref=planned,
                    session_ref=None,
                    expected_material_state_ref=None,
                    started_at=start,
                    ended_at=end,
                    pause_ranges=(),
                ),
            ),
        )
        assert len(result) == 1
        assert result[0].planned_schedule_ref == planned
        assert not result[0].open
        assert [
            record.planned_schedule_ref
            for record in await application.list_for_subject(
                self_person_ref=actor, subject_native_ref=activity
            )
        ] == [planned]
    finally:
        await runtime.dispose()


@pytest.mark.asyncio
async def test_grouped_child_resumes_in_second_main_interval_as_one_attempt(
    migrated_database: Any,
) -> None:
    """A named child may pause across the main gap and resume without a second attempt."""
    actor = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    end = datetime.now(UTC) - timedelta(hours=2)
    start = end - timedelta(minutes=75)
    try:
        created = await TemporalAuthoringApplication(runtime.session_factory).create_activity(
            self_person_ref=actor,
            operation_id="editor-multi-parent:create",
            title="Child resumes after main pause",
            placement=AbsoluteIntervalPlacement(starts_at=start, ends_at=end),
            planned_slices=(None,),
            planned_slice_names=("Reading",),
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
        main = SessionEditorWrite(
            operation_id="editor-multi-parent:main",
            planned_schedule_ref=None,
            session_ref=None,
            expected_material_state_ref=None,
            started_at=start,
            ended_at=end,
            pause_ranges=((start + timedelta(minutes=25), start + timedelta(minutes=35)),),
        )
        child = SessionEditorWrite(
            operation_id="editor-multi-parent:child",
            planned_schedule_ref=planned,
            session_ref=None,
            expected_material_state_ref=None,
            started_at=start + timedelta(minutes=5),
            ended_at=start + timedelta(minutes=65),
            pause_ranges=((start + timedelta(minutes=20), start + timedelta(minutes=40)),),
        )
        application = SessionApplication(runtime.session_factory)
        records = await application.write_editor_batch(
            self_person_ref=actor,
            activity_ref=activity,
            commands=(child, main),
        )
        assert len(records) == 2
        main_record, child_record = records
        assert main_record.planned_schedule_ref is None
        assert child_record.planned_schedule_ref == planned
        assert child_record.paused_seconds == pytest.approx(20 * 60, abs=1)
        assert child_record.active_seconds == pytest.approx(40 * 60, abs=1)
        assert (
            len(
                await application.list_for_subject(
                    self_person_ref=actor, subject_native_ref=activity
                )
            )
            == 2
        )

        correction = await application.write_editor_batch(
            self_person_ref=actor,
            activity_ref=activity,
            commands=(
                SessionEditorWrite(
                    operation_id="editor-multi-parent:correct-child",
                    planned_schedule_ref=planned,
                    session_ref=child_record.session_ref,
                    expected_material_state_ref=child_record.timing_material_state_ref,
                    started_at=start + timedelta(minutes=6),
                    ended_at=start + timedelta(minutes=65),
                    pause_ranges=((start + timedelta(minutes=20), start + timedelta(minutes=40)),),
                ),
            ),
        )
        assert len(correction) == 1
        assert correction[0].session_ref == child_record.session_ref
        assert correction[0].timing_material_state_ref != child_record.timing_material_state_ref
        assert correction[0].paused_seconds == pytest.approx(20 * 60, abs=1)
        assert (
            len(
                await application.list_for_subject(
                    self_person_ref=actor, subject_native_ref=activity
                )
            )
            == 2
        )
    finally:
        await runtime.dispose()


@pytest.mark.asyncio
async def test_grouped_correction_moves_main_and_child_together_without_exposing_an_invalid_final_state(
    migrated_database: Any,
) -> None:
    actor = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    start = datetime.now(UTC) - timedelta(hours=6)
    end = start + timedelta(hours=1)
    try:
        created = await TemporalAuthoringApplication(runtime.session_factory).create_activity(
            self_person_ref=actor,
            operation_id="editor-move:create",
            title="Move both actual recordings",
            placement=AbsoluteIntervalPlacement(starts_at=start, ends_at=end),
            planned_slices=(None,),
            planned_slice_names=("Reading",),
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
        original = await application.write_editor_batch(
            self_person_ref=actor,
            activity_ref=activity,
            commands=(
                SessionEditorWrite(
                    operation_id="editor-move:main",
                    planned_schedule_ref=None,
                    session_ref=None,
                    expected_material_state_ref=None,
                    started_at=start,
                    ended_at=end,
                    pause_ranges=(),
                ),
                SessionEditorWrite(
                    operation_id="editor-move:child",
                    planned_schedule_ref=planned,
                    session_ref=None,
                    expected_material_state_ref=None,
                    started_at=start + timedelta(minutes=10),
                    ended_at=start + timedelta(minutes=30),
                    pause_ranges=(),
                ),
            ),
        )
        shifted = start + timedelta(hours=2)
        main, child = original
        with pytest.raises(SessionInputError):
            await application.write_editor_batch(
                self_person_ref=actor,
                activity_ref=activity,
                commands=(
                    SessionEditorWrite(
                        operation_id="editor-move:main-alone",
                        planned_schedule_ref=None,
                        session_ref=main.session_ref,
                        expected_material_state_ref=main.timing_material_state_ref,
                        started_at=shifted,
                        ended_at=shifted + timedelta(hours=1),
                        pause_ranges=(),
                    ),
                ),
            )
        corrected = await application.write_editor_batch(
            self_person_ref=actor,
            activity_ref=activity,
            commands=(
                SessionEditorWrite(
                    operation_id="editor-move:main-and-child",
                    planned_schedule_ref=None,
                    session_ref=main.session_ref,
                    expected_material_state_ref=main.timing_material_state_ref,
                    started_at=shifted,
                    ended_at=shifted + timedelta(hours=1),
                    pause_ranges=(),
                ),
                SessionEditorWrite(
                    operation_id="editor-move:child-with-main",
                    planned_schedule_ref=planned,
                    session_ref=child.session_ref,
                    expected_material_state_ref=child.timing_material_state_ref,
                    started_at=shifted + timedelta(minutes=10),
                    ended_at=shifted + timedelta(minutes=30),
                    pause_ranges=(),
                ),
            ),
        )
        assert [row.session_ref for row in corrected] == [
            main.session_ref,
            child.session_ref,
        ]
        assert [row.started_at for row in corrected] == [
            shifted,
            shifted + timedelta(minutes=10),
        ]
        assert (
            len(
                await application.list_for_subject(
                    self_person_ref=actor,
                    subject_native_ref=activity,
                )
            )
            == 2
        )
    finally:
        await runtime.dispose()
