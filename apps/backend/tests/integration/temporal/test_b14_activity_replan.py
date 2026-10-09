"""A coordinated replan writes existing Activity rows as one accepted unit."""

from datetime import datetime
from types import SimpleNamespace
from typing import Any
from uuid import uuid7

import pytest
import psycopg
from fastapi import Response
from sqlalchemy import text
from tests.integration.temporal.test_b14_u2_authoring import _seed_self

from dante.modules.temporal.activity_edit_snapshot_api import _SNAPSHOT, ActivityEditSnapshot
from dante.modules.temporal.activity_replan_api import (
    ActivityReplanCommand,
    DeletePlannedRow,
    NewIntervalRow,
    NewPlannedRow,
    PlacePlannedRow,
    ReplanRow,
    apply_activity_replan,
    preview_activity_replan,
)
from dante.modules.temporal.authoring import TemporalAuthoringApplication
from dante.modules.temporal.schedule import NamedZoneLocalIntervalPlacement
from dante.platform.database.runtime import create_database_runtime
from dante.platform.http.problem import ProblemError

pytestmark = pytest.mark.postgres


def _window(start: int, end: int) -> NamedZoneLocalIntervalPlacement:
    return NamedZoneLocalIntervalPlacement(
        starts_local_at=datetime(2026, 10, 9, start),  # noqa: DTZ001
        ends_local_at=datetime(2026, 10, 9, end),  # noqa: DTZ001
        zone_id="Europe/Rome",
    )


def _move(row, start: int, end: int) -> ReplanRow:
    return ReplanRow(
        schedule_ref=row.schedule_ref,
        expected_material_state_ref=row.placement_material_state_ref,
        starts_local_at=datetime(2026, 10, 9, start),  # noqa: DTZ001
        ends_local_at=datetime(2026, 10, 9, end),  # noqa: DTZ001
    )


@pytest.mark.asyncio
async def test_activity_replan_previews_and_commits_dependent_rows_atomically(
    migrated_database: Any,
) -> None:
    actor = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    try:
        created = await TemporalAuthoringApplication(runtime.session_factory).create_activity(
            self_person_ref=actor, operation_id="replan:create", title="Studio",
            placement=_window(9, 12),
            activity_intervals=(_window(9, 10), _window(11, 12)),
            planned_slices=(_window(11, 12),),
            planned_slice_names=("Ripasso",),
        )
        activity = created.item.subject_native_ref
        async with runtime.session_factory() as session, session.begin():
            before = ActivityEditSnapshot.model_validate(await session.scalar(
                _SNAPSHOT, {"actor": actor, "activity": activity},
            ))
        intervals = [row for row in before.schedules if row.role_code == "interval"]
        planned = next(row for row in before.schedules if row.role_code == "planned")
        command = ActivityReplanCommand(
            operation_id="replan:move",
            intervals=[_move(intervals[0], 10, 11), _move(intervals[1], 12, 13)],
            planned_sessions=[_move(planned, 12, 13)],
        )
        context = SimpleNamespace(self_person_ref=actor)
        request = SimpleNamespace(app=SimpleNamespace(
            state=SimpleNamespace(database_runtime=runtime)))
        proposal = await preview_activity_replan(
            activity, command, context, request, Response(),
        )
        assert len(proposal.changes) == 4
        async with runtime.session_factory() as session, session.begin():
            still_before = ActivityEditSnapshot.model_validate(await session.scalar(
                _SNAPSHOT, {"actor": actor, "activity": activity},
            ))
            assert still_before.schedules == before.schedules
        after = await apply_activity_replan(
            activity, command, context, request, Response(),
        )
        assert [row.starts_local_at.hour for row in after.schedules] == [10, 10, 12, 12]
        assert [row.ends_local_at.hour for row in after.schedules] == [13, 11, 13, 13]
        assert next(row for row in after.schedules if row.role_code == "planned").display_name == "Ripasso"
        with pytest.raises(ProblemError) as stale:
            await apply_activity_replan(
                activity, command.model_copy(update={"operation_id": "replan:stale"}),
                context, request, Response(),
            )
        assert stale.value.status == 409
    finally:
        await runtime.dispose()


@pytest.mark.asyncio
async def test_activity_replan_adds_and_removes_planned_sessions_without_reusing_history(
    migrated_database: Any,
) -> None:
    actor = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    try:
        created = await TemporalAuthoringApplication(runtime.session_factory).create_activity(
            self_person_ref=actor, operation_id="replan:replace:create", title="Studio",
            placement=_window(9, 12), activity_intervals=(_window(9, 12),),
            planned_slices=(_window(9, 10),), planned_slice_names=("Prima",),
        )
        activity = created.item.subject_native_ref
        async with runtime.session_factory() as session, session.begin():
            before = ActivityEditSnapshot.model_validate(await session.scalar(
                _SNAPSHOT, {"actor": actor, "activity": activity},
            ))
        interval = next(row for row in before.schedules if row.role_code == "interval")
        old = next(row for row in before.schedules if row.role_code == "planned")
        command = ActivityReplanCommand(
            operation_id="replan:replace:apply", intervals=[_move(interval, 9, 12)],
            remove_planned_sessions=[_move(old, 9, 10)],
            new_planned_sessions=[NewPlannedRow(
                client_ref=uuid7(), name="Seconda",
                starts_local_at=datetime(2026, 10, 9, 10),  # noqa: DTZ001
                ends_local_at=datetime(2026, 10, 9, 11),  # noqa: DTZ001
            )],
        )
        context = SimpleNamespace(self_person_ref=actor)
        request = SimpleNamespace(app=SimpleNamespace(
            state=SimpleNamespace(database_runtime=runtime)))
        preview = await preview_activity_replan(activity, command, context, request, Response())
        assert {change.role for change in preview.changes} == {"planned_added", "planned_removed"}
        after = await apply_activity_replan(activity, command, context, request, Response())
        accepted = [row for row in after.schedules if row.role_code == "planned"]
        assert len(accepted) == 2
        assert next(row for row in accepted if row.schedule_ref == old.schedule_ref).placement_material_state_ref is None
        added = next(row for row in accepted if row.schedule_ref != old.schedule_ref)
        assert added.display_name == "Seconda"
        assert added.presentation_order > old.presentation_order
        assert len([row for row in after.schedules if row.role_code == "interval"]) == 1
    finally:
        await runtime.dispose()


@pytest.mark.asyncio
async def test_activity_replan_retires_planned_rows_but_keeps_schedule_history(
    migrated_database: Any,
) -> None:
    actor = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    try:
        created = await TemporalAuthoringApplication(runtime.session_factory).create_activity(
            self_person_ref=actor, operation_id="replan:retire:create", title="Studio",
            placement=_window(9, 12), planned_slices=(_window(9, 10), None),
            planned_slice_names=("Mattina", "Libera"),
        )
        activity = created.item.subject_native_ref
        async with runtime.session_factory() as session, session.begin():
            before = ActivityEditSnapshot.model_validate(await session.scalar(
                _SNAPSHOT, {"actor": actor, "activity": activity},
            ))
        envelope = next(row for row in before.schedules if row.role_code == "envelope")
        planned = [row for row in before.schedules if row.role_code == "planned"]
        command = ActivityReplanCommand(
            operation_id="replan:retire:apply", envelope=_move(envelope, 9, 12),
            delete_planned_sessions=[DeletePlannedRow(
                schedule_ref=row.schedule_ref,
                expected_material_state_ref=row.placement_material_state_ref,
            ) for row in planned],
        )
        context = SimpleNamespace(self_person_ref=actor)
        request = SimpleNamespace(app=SimpleNamespace(
            state=SimpleNamespace(database_runtime=runtime)))
        preview = await preview_activity_replan(activity, command, context, request, Response())
        assert [change.role for change in preview.changes] == ["planned_deleted"] * 2
        after = await apply_activity_replan(activity, command, context, request, Response())
        assert not any(row.role_code == "planned" for row in after.schedules)
        with psycopg.connect(
            host=migrated_database.cluster.host, port=migrated_database.cluster.port,
            dbname=migrated_database.name, user=migrated_database.cluster.admin_user,
            password=migrated_database.cluster.admin_password,
        ) as connection:
            historical = connection.execute("""
                SELECT schedule_ref,retired_at FROM dante.activity_schedule_role
                 WHERE activity_ref=%s AND role_code='planned'
            """, (activity,)).fetchall()
        assert {row[0] for row in historical} == {row.schedule_ref for row in planned}
        assert all(row[1] is not None for row in historical)
        with pytest.raises(ProblemError) as stale:
            await apply_activity_replan(
                activity, command.model_copy(update={"operation_id": "replan:retire:stale"}),
                context, request, Response(),
            )
        assert stale.value.status == 422
    finally:
        await runtime.dispose()


@pytest.mark.asyncio
async def test_planned_time_can_be_added_removed_and_added_again_on_same_schedule(
    migrated_database: Any,
) -> None:
    actor = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    try:
        created = await TemporalAuthoringApplication(runtime.session_factory).create_activity(
            self_person_ref=actor, operation_id="replan:untimed:create", title="Studio",
            placement=_window(9, 12), planned_slices=(None,),
            planned_slice_names=("Ripasso",),
        )
        activity = created.item.subject_native_ref
        context = SimpleNamespace(self_person_ref=actor)
        request = SimpleNamespace(app=SimpleNamespace(
            state=SimpleNamespace(database_runtime=runtime)))

        async def snapshot() -> ActivityEditSnapshot:
            async with runtime.session_factory() as session, session.begin():
                return ActivityEditSnapshot.model_validate(await session.scalar(
                    _SNAPSHOT, {"actor": actor, "activity": activity},
                ))

        before = await snapshot()
        planned = next(row for row in before.schedules if row.role_code == "planned")
        envelope = next(row for row in before.schedules if row.role_code == "envelope")
        assert planned.placement_material_state_ref is None

        def place(op: str) -> ActivityReplanCommand:
            return ActivityReplanCommand(
                operation_id=op, envelope=_move(envelope, 9, 12),
                place_planned_sessions=[PlacePlannedRow(
                    schedule_ref=planned.schedule_ref,
                    starts_local_at=datetime(2026, 10, 9, 10),  # noqa: DTZ001
                    ends_local_at=datetime(2026, 10, 9, 11),  # noqa: DTZ001
                )],
            )

        proposed = await preview_activity_replan(activity, place("place:first"),
                                                  context, request, Response())
        assert [change.role for change in proposed.changes] == ["planned_placed"]
        timed = await apply_activity_replan(activity, place("place:first"),
                                            context, request, Response())
        placed = next(row for row in timed.schedules if row.role_code == "planned")
        assert placed.schedule_ref == planned.schedule_ref
        assert placed.starts_local_at.hour == 10
        removed = await apply_activity_replan(activity, ActivityReplanCommand(
            operation_id="place:remove", envelope=_move(envelope, 9, 12),
            remove_planned_sessions=[_move(placed, 10, 11)],
        ), context, request, Response())
        untimed = next(row for row in removed.schedules if row.role_code == "planned")
        assert untimed.schedule_ref == planned.schedule_ref
        assert untimed.placement_material_state_ref is None
        retimed = await apply_activity_replan(activity, place("place:again"),
                                              context, request, Response())
        again = next(row for row in retimed.schedules if row.role_code == "planned")
        assert again.schedule_ref == planned.schedule_ref
        assert again.placement_material_state_ref != placed.placement_material_state_ref
        assert (await snapshot()).schedules == retimed.schedules
    finally:
        await runtime.dispose()

@pytest.mark.asyncio
async def test_activity_replan_replaces_current_interval_without_erasing_role_history(
    migrated_database: Any,
) -> None:
    actor = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    try:
        created = await TemporalAuthoringApplication(runtime.session_factory).create_activity(
            self_person_ref=actor, operation_id="replan:intervals:create", title="Lavoro",
            placement=_window(9, 12),
            activity_intervals=(_window(9, 10), _window(11, 12)),
            planned_slices=(_window(11, 12),), planned_slice_names=("Pianificata",),
        )
        activity = created.item.subject_native_ref
        async with runtime.session_factory() as session, session.begin():
            before = ActivityEditSnapshot.model_validate(await session.scalar(
                _SNAPSHOT, {"actor": actor, "activity": activity},
            ))
        intervals = [row for row in before.schedules if row.role_code == "interval"]
        planned = next(row for row in before.schedules if row.role_code == "planned")
        new_ref = uuid7()
        command = ActivityReplanCommand(
            operation_id="replan:intervals:replace",
            intervals=[_move(intervals[1], 11, 12)],
            remove_intervals=[_move(intervals[0], 9, 10)],
            new_intervals=[NewIntervalRow(
                client_ref=new_ref,
                starts_local_at=datetime(2026, 10, 9, 10),  # noqa: DTZ001
                ends_local_at=datetime(2026, 10, 9, 11),  # noqa: DTZ001
            )],
            planned_sessions=[_move(planned, 11, 12)],
        )
        context = SimpleNamespace(self_person_ref=actor)
        request = SimpleNamespace(app=SimpleNamespace(
            state=SimpleNamespace(database_runtime=runtime)))
        preview = await preview_activity_replan(activity, command, context, request, Response())
        assert {change.role for change in preview.changes} == {
            "envelope", "interval_removed", "interval_added",
        }
        after = await apply_activity_replan(activity, command, context, request, Response())
        current_intervals = [row for row in after.schedules if row.role_code == "interval"]
        assert len(current_intervals) == 2
        assert intervals[0].schedule_ref not in {row.schedule_ref for row in current_intervals}
        assert intervals[1].schedule_ref in {row.schedule_ref for row in current_intervals}
        added = next(row for row in current_intervals
                     if row.schedule_ref != intervals[1].schedule_ref)
        assert added.presentation_order > max(row.presentation_order for row in intervals)
        assert (added.starts_local_at.hour, added.ends_local_at.hour) == (10, 11)
        envelope = next(row for row in after.schedules if row.role_code == "envelope")
        assert envelope.starts_local_at.hour == 10
        retained_planned = next(row for row in after.schedules if row.role_code == "planned")
        assert retained_planned.schedule_ref == planned.schedule_ref
        # The original role is historically accepted and never reassigned.
        async with runtime.session_factory() as session, session.begin():
            accepted = (await session.execute(text("""
                SELECT schedule_ref FROM dante.get_self_activity_schedule_roles(
                    :actor, CAST(ARRAY[:activity] AS uuid[]))
                WHERE role_code='interval'
            """), {"actor": actor, "activity": activity})).scalars().all()
        assert intervals[0].schedule_ref in accepted
        assert added.schedule_ref in accepted
    finally:
        await runtime.dispose()
