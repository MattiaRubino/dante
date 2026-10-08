"""A coordinated replan writes existing Activity rows as one accepted unit."""

from datetime import datetime
from types import SimpleNamespace
from typing import Any

import pytest
from fastapi import Response
from tests.integration.temporal.test_b14_u2_authoring import _seed_self

from dante.modules.temporal.activity_edit_snapshot_api import _SNAPSHOT, ActivityEditSnapshot
from dante.modules.temporal.activity_replan_api import (
    ActivityReplanCommand,
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
