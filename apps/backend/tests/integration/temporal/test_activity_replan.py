"""Real PostgreSQL contract for Activity intervals and named Session configuration."""

import hashlib
from datetime import datetime
from types import SimpleNamespace
from typing import Any, cast
from uuid import uuid7

import psycopg
import pytest
from fastapi import Request, Response
from sqlalchemy import text
from tests.integration.temporal.test_activity_quick_authoring_metadata import _seed_self

from dante.context.contracts import DanteContext
from dante.modules.temporal.activity_edit_snapshot_api import _SNAPSHOT, ActivityEditSnapshot
from dante.modules.temporal.activity_inspector_api import get_self_activity_session_impact
from dante.modules.temporal.activity_replan_api import (
    ActivityReplanCommand,
    DeletePlannedRow,
    NewIntervalRow,
    NewPlannedRow,
    ReplanRow,
    RetainedPlannedRow,
    apply_activity_replan,
    preview_activity_replan,
)
from dante.modules.temporal.authoring import TemporalAuthoringApplication
from dante.modules.temporal.decomposition_api import ActivityScheduleResponse
from dante.modules.temporal.schedule import (
    NamedZoneLocalIntervalPlacement,
    ScheduleActivityIntervalConflictError,
    TemporalScheduleApplication,
    _unschedule_undo_fingerprint,
)
from dante.modules.temporal.session_runtime import SessionApplication
from dante.platform.database.references import MaterialStateRef, NativeRef, ScopedRecordRef
from dante.platform.database.runtime import create_database_runtime
from dante.platform.http.problem import ProblemError

pytestmark = pytest.mark.postgres


def _window(start: int, end: int) -> NamedZoneLocalIntervalPlacement:
    return NamedZoneLocalIntervalPlacement(
        starts_local_at=datetime(2026, 10, 9, start),  # noqa: DTZ001
        ends_local_at=datetime(2026, 10, 9, end),  # noqa: DTZ001
        zone_id="Europe/Rome",
    )


def _move(row: ActivityScheduleResponse, start: int, end: int) -> ReplanRow:
    assert row.placement_material_state_ref is not None
    return ReplanRow(
        schedule_ref=row.schedule_ref,
        expected_material_state_ref=row.placement_material_state_ref,
        starts_local_at=datetime(2026, 10, 9, start),  # noqa: DTZ001
        ends_local_at=datetime(2026, 10, 9, end),  # noqa: DTZ001
    )


def _retain(row: ActivityScheduleResponse) -> RetainedPlannedRow:
    return RetainedPlannedRow(
        schedule_ref=row.schedule_ref,
        expected_material_state_ref=row.placement_material_state_ref,
    )


def _context(actor: object) -> DanteContext:
    return cast(DanteContext, SimpleNamespace(self_person_ref=actor))


def _request(runtime: Any) -> Request:
    return cast(
        Request,
        SimpleNamespace(app=SimpleNamespace(state=SimpleNamespace(database_runtime=runtime))),
    )


async def _snapshot(runtime: Any, actor: object, activity: object) -> ActivityEditSnapshot:
    async with runtime.session_factory() as session, session.begin():
        return ActivityEditSnapshot.model_validate(
            await session.scalar(_SNAPSHOT, {"actor": actor, "activity": activity})
        )


@pytest.mark.asyncio
async def test_replanning_an_activity_keeps_named_session_configuration_without_retiming_it(
    migrated_database: Any,
) -> None:
    actor = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    try:
        created = await TemporalAuthoringApplication(runtime.session_factory).create_activity(
            self_person_ref=actor,
            operation_id="session-lifecycle:move",
            title="Studio",
            placement=_window(9, 12),
            activity_intervals=(_window(9, 12),),
            planned_slices=(None,),
            planned_slice_names=("Ripasso",),
        )
        activity = created.item.subject_native_ref
        before = await _snapshot(runtime, actor, activity)
        interval = next(row for row in before.schedules if row.role_code == "interval")
        named = next(row for row in before.schedules if row.role_code == "planned")
        command = ActivityReplanCommand(
            operation_id="session-lifecycle:move:apply",
            intervals=[_move(interval, 10, 13)],
            planned_sessions=[_retain(named)],
        )
        preview = await preview_activity_replan(
            activity, command, _context(actor), _request(runtime), Response()
        )
        assert {change.role for change in preview.changes} == {"envelope", "interval"}
        after = await apply_activity_replan(
            activity, command, _context(actor), _request(runtime), Response()
        )
        retained = next(row for row in after.schedules if row.role_code == "planned")
        assert retained.schedule_ref == named.schedule_ref
        assert retained.display_name == "Ripasso"
        assert retained.placement_material_state_ref is None
    finally:
        await runtime.dispose()


@pytest.mark.asyncio
async def test_replacing_one_activity_interval_preserves_other_intervals_and_named_identity(
    migrated_database: Any,
) -> None:
    actor = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    try:
        created = await TemporalAuthoringApplication(runtime.session_factory).create_activity(
            self_person_ref=actor,
            operation_id="lifecycle:replace-interval",
            title="Lavoro",
            placement=_window(9, 12),
            activity_intervals=(_window(9, 10), _window(11, 12)),
            planned_slices=(None,),
            planned_slice_names=("Studio",),
        )
        activity = created.item.subject_native_ref
        before = await _snapshot(runtime, actor, activity)
        first, second = (row for row in before.schedules if row.role_code == "interval")
        named = next(row for row in before.schedules if row.role_code == "planned")
        command = ActivityReplanCommand(
            operation_id="lifecycle:replace-interval:apply",
            intervals=[_move(second, 11, 12)],
            remove_intervals=[_move(first, 9, 10)],
            new_intervals=[
                NewIntervalRow(
                    client_ref=uuid7(),
                    starts_local_at=datetime(2026, 10, 9, 10),  # noqa: DTZ001
                    ends_local_at=datetime(2026, 10, 9, 11),  # noqa: DTZ001
                )
            ],
            planned_sessions=[_retain(named)],
        )
        preview = await preview_activity_replan(
            activity, command, _context(actor), _request(runtime), Response()
        )
        assert {change.role for change in preview.changes} == {
            "envelope",
            "interval_removed",
            "interval_added",
        }
        after = await apply_activity_replan(
            activity, command, _context(actor), _request(runtime), Response()
        )
        current = [row for row in after.schedules if row.role_code == "interval"]
        assert len(current) == 2
        assert first.schedule_ref not in {row.schedule_ref for row in current}
        assert second.schedule_ref in {row.schedule_ref for row in current}
        retained = next(row for row in after.schedules if row.role_code == "planned")
        assert retained.schedule_ref == named.schedule_ref
        assert retained.placement_material_state_ref is None
        async with runtime.session_factory() as session, session.begin():
            accepted = (
                await session.scalars(
                    text("""
                SELECT schedule_ref FROM dante.get_self_activity_schedule_roles(
                    :actor,CAST(ARRAY[:activity] AS uuid[])) WHERE role_code='interval'
            """),
                    {"actor": actor, "activity": activity},
                )
            ).all()
        assert first.schedule_ref in accepted
    finally:
        await runtime.dispose()


@pytest.mark.asyncio
async def test_adding_a_named_session_creates_no_schedule_placement(
    migrated_database: Any,
) -> None:
    actor = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    try:
        created = await TemporalAuthoringApplication(runtime.session_factory).create_activity(
            self_person_ref=actor,
            operation_id="session-lifecycle:add",
            title="Studio",
            placement=_window(9, 12),
            activity_intervals=(_window(9, 12),),
        )
        activity = created.item.subject_native_ref
        before = await _snapshot(runtime, actor, activity)
        interval = next(row for row in before.schedules if row.role_code == "interval")
        after = await apply_activity_replan(
            activity,
            ActivityReplanCommand(
                operation_id="session-lifecycle:add:apply",
                intervals=[_move(interval, 9, 12)],
                new_planned_sessions=[NewPlannedRow(client_ref=uuid7(), name="Esercizi")],
            ),
            _context(actor),
            _request(runtime),
            Response(),
        )
        named = next(row for row in after.schedules if row.role_code == "planned")
        assert named.display_name == "Esercizi"
        assert named.placement_material_state_ref is None
        async with runtime.session_factory() as session, session.begin():
            count = await session.scalar(
                text(
                    "SELECT count(*) FROM dante.schedule_current_placement WHERE scoped_owner_ref=:schedule"
                ),
                {"schedule": named.schedule_ref},
            )
        assert count == 0
    finally:
        await runtime.dispose()


@pytest.mark.asyncio
async def test_named_session_delete_requires_explicit_accounting_and_retires_the_configuration(
    migrated_database: Any,
) -> None:
    actor = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    try:
        created = await TemporalAuthoringApplication(runtime.session_factory).create_activity(
            self_person_ref=actor,
            operation_id="session-lifecycle:delete",
            title="Studio",
            placement=_window(9, 12),
            activity_intervals=(_window(9, 12),),
            planned_slices=(None,),
            planned_slice_names=("Da eliminare",),
        )
        activity = created.item.subject_native_ref
        before = await _snapshot(runtime, actor, activity)
        interval = next(row for row in before.schedules if row.role_code == "interval")
        named = next(row for row in before.schedules if row.role_code == "planned")
        with pytest.raises(ProblemError):
            await preview_activity_replan(
                activity,
                ActivityReplanCommand(
                    operation_id="session-lifecycle:omitted", intervals=[_move(interval, 9, 12)]
                ),
                _context(actor),
                _request(runtime),
                Response(),
            )
        after = await apply_activity_replan(
            activity,
            ActivityReplanCommand(
                operation_id="session-lifecycle:delete:apply",
                intervals=[_move(interval, 9, 12)],
                delete_planned_sessions=[
                    DeletePlannedRow(
                        schedule_ref=named.schedule_ref,
                        expected_material_state_ref=named.placement_material_state_ref,
                    )
                ],
            ),
            _context(actor),
            _request(runtime),
            Response(),
        )
        assert not any(row.role_code == "planned" for row in after.schedules)
    finally:
        await runtime.dispose()


@pytest.mark.asyncio
async def test_placement_lock_allows_new_unplaced_named_session_but_blocks_movement(
    migrated_database: Any,
) -> None:
    actor = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    try:
        created = await TemporalAuthoringApplication(runtime.session_factory).create_activity(
            self_person_ref=actor,
            operation_id="lifecycle:locked",
            title="Studio",
            placement=_window(9, 12),
        )
        activity = created.item.subject_native_ref
        before = await _snapshot(runtime, actor, activity)
        envelope = next(row for row in before.schedules if row.role_code == "envelope")
        async with runtime.session_factory() as session, session.begin():
            await session.execute(
                text(
                    "SELECT * FROM dante.set_self_schedule_placement_lock(:actor,:schedule,true,NULL)"
                ),
                {"actor": actor, "schedule": envelope.schedule_ref},
            )
        unchanged = await apply_activity_replan(
            activity,
            ActivityReplanCommand(
                operation_id="lifecycle:locked:add",
                envelope=_move(envelope, 9, 12),
                new_planned_sessions=[NewPlannedRow(client_ref=uuid7(), name="Ripasso")],
            ),
            _context(actor),
            _request(runtime),
            Response(),
        )
        named = next(row for row in unchanged.schedules if row.role_code == "planned")
        assert named.placement_material_state_ref is None
        assert (
            next(
                row for row in unchanged.schedules if row.role_code == "envelope"
            ).placement_material_state_ref
            == envelope.placement_material_state_ref
        )
        with pytest.raises(ProblemError) as locked:
            await apply_activity_replan(
                activity,
                ActivityReplanCommand(
                    operation_id="lifecycle:locked:move",
                    envelope=_move(envelope, 10, 13),
                    planned_sessions=[_retain(named)],
                ),
                _context(actor),
                _request(runtime),
                Response(),
            )
        assert locked.value.status == 409
    finally:
        await runtime.dispose()


@pytest.mark.asyncio
async def test_keep_preserves_running_attempts_when_moving_and_named_x_deletes_only_its_attempt(
    migrated_database: Any,
) -> None:
    actor = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    try:
        created = await TemporalAuthoringApplication(runtime.session_factory).create_activity(
            self_person_ref=actor,
            operation_id="lifecycle:keep:create",
            title="Studio",
            placement=_window(9, 12),
            activity_intervals=(_window(9, 12),),
            planned_slices=(None,),
            planned_slice_names=("Ripasso",),
            session_capture_mode="live",
        )
        activity = created.item.subject_native_ref
        before = await _snapshot(runtime, actor, activity)
        named = next(row for row in before.schedules if row.role_code == "planned")
        sessions = SessionApplication(runtime.session_factory)
        main = await sessions.start(
            self_person_ref=actor,
            subject_kind="activity",
            subject_native_ref=activity,
            operation_id="lifecycle:keep:main",
        )
        child = await sessions.start_planned(
            self_person_ref=actor,
            operation_id="lifecycle:keep:child",
            activity_ref=activity,
            schedule_ref=ScopedRecordRef(named.schedule_ref),
        )
        interval = next(row for row in before.schedules if row.role_code == "interval")
        impact = await get_self_activity_session_impact(
            activity, _context(actor), _request(runtime), Response()
        )
        with pytest.raises(ProblemError) as confirmation:
            await apply_activity_replan(
                activity,
                ActivityReplanCommand(
                    operation_id="lifecycle:keep:unconfirmed",
                    intervals=[_move(interval, 10, 13)],
                    planned_sessions=[_retain(named)],
                ),
                _context(actor),
                _request(runtime),
                Response(),
            )
        assert confirmation.value.status == 409
        moved = await apply_activity_replan(
            activity,
            ActivityReplanCommand(
                operation_id="lifecycle:keep:move",
                intervals=[_move(interval, 10, 13)],
                planned_sessions=[_retain(named)],
                session_disposition="keep",
                expected_session_fingerprint=impact.fingerprint,
            ),
            _context(actor),
            _request(runtime),
            Response(),
        )
        assert next(
            r for r in moved.schedules if r.role_code == "interval"
        ).starts_local_at == datetime(2026, 10, 9, 10)  # noqa: DTZ001
        after_keep = await get_self_activity_session_impact(
            activity, _context(actor), _request(runtime), Response()
        )
        assert after_keep.fingerprint == impact.fingerprint
        assert {row.session_ref for row in after_keep.attempts} == {
            main.session_ref,
            child.session_ref,
        }

        current_interval = next(r for r in moved.schedules if r.role_code == "interval")
        without_named = await apply_activity_replan(
            activity,
            ActivityReplanCommand(
                operation_id="lifecycle:keep:remove-named",
                intervals=[_move(current_interval, 10, 13)],
                delete_planned_sessions=[
                    DeletePlannedRow(
                        schedule_ref=named.schedule_ref,
                        expected_material_state_ref=named.placement_material_state_ref,
                    )
                ],
                session_disposition="keep",
                expected_session_fingerprint=after_keep.fingerprint,
            ),
            _context(actor),
            _request(runtime),
            Response(),
        )
        assert not any(row.role_code == "planned" for row in without_named.schedules)
        remaining = await get_self_activity_session_impact(
            activity, _context(actor), _request(runtime), Response()
        )
        assert [row.session_ref for row in remaining.attempts] == [main.session_ref]
    finally:
        await runtime.dispose()


@pytest.mark.asyncio
async def test_direct_activity_envelope_revision_with_attempt_requires_confirmed_replan(
    migrated_database: Any,
) -> None:
    actor = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    try:
        created = await TemporalAuthoringApplication(runtime.session_factory).create_activity(
            self_person_ref=actor,
            operation_id="lifecycle:direct:create",
            title="Studio",
            placement=_window(9, 12),
            session_capture_mode="live",
        )
        activity = created.item.subject_native_ref
        await SessionApplication(runtime.session_factory).start(
            self_person_ref=actor,
            operation_id="lifecycle:direct:start",
            subject_kind="activity",
            subject_native_ref=activity,
        )
        before = await _snapshot(runtime, actor, activity)
        envelope = next(row for row in before.schedules if row.role_code == "envelope")
        assert envelope.placement_material_state_ref is not None
        with pytest.raises(ScheduleActivityIntervalConflictError):
            await TemporalScheduleApplication(runtime.session_factory).revise_schedule(
                self_person_ref=NativeRef(actor),
                operation_id="lifecycle:direct:forbidden",
                schedule_ref=ScopedRecordRef(envelope.schedule_ref),
                expected_material_state_ref=MaterialStateRef(envelope.placement_material_state_ref),
                placement=_window(10, 13),
            )
        impact = await get_self_activity_session_impact(
            activity, _context(actor), _request(runtime), Response()
        )
        after = await apply_activity_replan(
            activity,
            ActivityReplanCommand(
                operation_id="lifecycle:direct:confirmed",
                envelope=_move(envelope, 10, 13),
                session_disposition="keep",
                expected_session_fingerprint=impact.fingerprint,
            ),
            _context(actor),
            _request(runtime),
            Response(),
        )
        assert next(
            row for row in after.schedules if row.role_code == "envelope"
        ).starts_local_at == datetime(2026, 10, 9, 10)  # noqa: DTZ001
        assert (
            await get_self_activity_session_impact(
                activity, _context(actor), _request(runtime), Response()
            )
        ).fingerprint == impact.fingerprint
    finally:
        await runtime.dispose()


@pytest.mark.asyncio
async def test_generic_undo_cannot_restore_removed_activity_interval_around_a_running_session(
    migrated_database: Any,
) -> None:
    actor = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    try:
        created = await TemporalAuthoringApplication(runtime.session_factory).create_activity(
            self_person_ref=actor,
            operation_id="lifecycle:undo:create",
            title="Studio",
            placement=_window(9, 12),
            activity_intervals=(_window(9, 10), _window(11, 12)),
            session_capture_mode="live",
        )
        activity = created.item.subject_native_ref
        before = await _snapshot(runtime, actor, activity)
        first, second = (row for row in before.schedules if row.role_code == "interval")
        started = await SessionApplication(runtime.session_factory).start(
            self_person_ref=actor,
            subject_kind="activity",
            subject_native_ref=activity,
            operation_id="lifecycle:undo:start",
        )
        impact = await get_self_activity_session_impact(
            activity, _context(actor), _request(runtime), Response()
        )
        operation = "lifecycle:undo:remove"
        await apply_activity_replan(
            activity,
            ActivityReplanCommand(
                operation_id=operation,
                intervals=[_move(second, 11, 12)],
                remove_intervals=[_move(first, 9, 10)],
                session_disposition="keep",
                expected_session_fingerprint=impact.fingerprint,
            ),
            _context(actor),
            _request(runtime),
            Response(),
        )
        receipt = (
            f"replan:remove:{hashlib.sha256(operation.encode('utf-8')).hexdigest()}"
            f":{first.schedule_ref}"
        )
        schedules = TemporalScheduleApplication(runtime.session_factory)
        with pytest.raises(ScheduleActivityIntervalConflictError):
            await schedules.undo_unschedule(
                self_person_ref=NativeRef(actor),
                operation_id="lifecycle:undo:refused",
                schedule_ref=ScopedRecordRef(first.schedule_ref),
                unschedule_operation_id=receipt,
            )

        # The runtime can invoke the exposed DEFINER routine directly. It must
        # enforce the same refusal even without the Python application guard.
        with (
            psycopg.connect(
                **migrated_database.connection_kwargs(
                    "dante_runtime", migrated_database.cluster.runtime_password
                )
            ) as connection,
            pytest.raises(psycopg.errors.CheckViolation) as refused,
        ):
            connection.execute(
                "SELECT * FROM dante.undo_self_schedule_unschedule_any(%s,%s,%s,%s,%s,%s)",
                (
                    actor,
                    "lifecycle:undo:direct",
                    _unschedule_undo_fingerprint(
                        schedule_ref=ScopedRecordRef(first.schedule_ref),
                        unschedule_operation_id=receipt,
                    ),
                    first.schedule_ref,
                    receipt,
                    uuid7(),
                ),
            )
        assert refused.value.diag.constraint_name == "schedule_activity_interval_requires_replan"
        async with runtime.session_factory() as session, session.begin():
            restored = await session.scalar(
                text(
                    "SELECT EXISTS(SELECT 1 FROM dante.get_self_activity_schedule_roles("
                    ":actor, CAST(ARRAY[:activity] AS uuid[])) AS role "
                    "JOIN dante.schedule_current_placement AS placement "
                    "ON placement.scoped_owner_ref=role.schedule_ref "
                    "WHERE role.schedule_ref=:schedule)"
                ),
                {"actor": actor, "activity": activity, "schedule": first.schedule_ref},
            )
        assert restored is False
        after = await get_self_activity_session_impact(
            activity, _context(actor), _request(runtime), Response()
        )
        assert after.fingerprint == impact.fingerprint
        assert [row.session_ref for row in after.attempts] == [started.session_ref]
    finally:
        await runtime.dispose()
