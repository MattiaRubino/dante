"""PostgreSQL acceptance: coordinated Activity Timeline unplace and monotonic Undo."""

from __future__ import annotations

from datetime import datetime
from types import SimpleNamespace
from typing import Any, cast

import pytest
from fastapi import Request, Response
from tests.integration.temporal.test_primary_life_area_assignment import _seed_self

from dante.context.contracts import DanteContext
from dante.modules.temporal.activity_edit_snapshot_api import get_activity_edit_snapshot
from dante.modules.temporal.activity_inspector_api import get_self_activity_session_impact
from dante.modules.temporal.activity_replan_api import (
    ActivityTimelineUndoCommand,
    ActivityTimelineUnplaceCommand,
    list_activity_timeline_undo,
    undo_activity_timeline,
    unplace_activity_timeline,
)
from dante.modules.temporal.authoring import TemporalAuthoringApplication
from dante.modules.temporal.schedule import FloatingLocalIntervalPlacement
from dante.platform.database.runtime import create_database_runtime
from dante.platform.http.problem import ProblemError

pytestmark = pytest.mark.postgres


def _request(runtime: Any) -> Request:
    return cast(
        Request,
        SimpleNamespace(app=SimpleNamespace(state=SimpleNamespace(database_runtime=runtime))),
    )


def _context(actor: Any) -> DanteContext:
    return cast(DanteContext, SimpleNamespace(self_person_ref=actor))


@pytest.mark.asyncio
async def test_activity_unplace_preserves_identity_and_undo_restores_new_state(
    migrated_database: Any,
) -> None:
    actor = _seed_self(migrated_database)
    other = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    try:
        created = await TemporalAuthoringApplication(runtime.session_factory).create_activity(
            self_person_ref=actor,
            operation_id="timeline-unplace:activity",
            title="Activity resta anche senza collocazione",
            placement=FloatingLocalIntervalPlacement(
                starts_local_at=datetime(2026, 10, 18, 10, 0),  # noqa: DTZ001 - floating local
                ends_local_at=datetime(2026, 10, 18, 11, 0),  # noqa: DTZ001 - floating local
            ),
        )
        activity = created.item.subject_native_ref
        assert created.schedule is not None
        schedule = created.schedule
        impact = await get_self_activity_session_impact(
            activity, _context(actor), _request(runtime), Response()
        )
        assert impact.attempts == []

        with pytest.raises(ProblemError) as unavailable:
            await unplace_activity_timeline(
                activity,
                ActivityTimelineUnplaceCommand(
                    operation_id="timeline-unplace:other",
                    schedule_ref=schedule.schedule_ref,
                    expected_material_state_ref=schedule.material_state_ref,
                ),
                _context(other),
                _request(runtime),
                Response(),
            )
        assert unavailable.value.status == 409

        removed = await unplace_activity_timeline(
            activity,
            ActivityTimelineUnplaceCommand(
                operation_id="timeline-unplace:remove",
                schedule_ref=schedule.schedule_ref,
                expected_material_state_ref=schedule.material_state_ref,
            ),
            _context(actor),
            _request(runtime),
            Response(),
        )
        assert removed.schedule_ref == schedule.schedule_ref
        assert removed.placement_material_state_ref is None
        assert removed.operation_id == "timeline-unplace:remove"

        receipts = await list_activity_timeline_undo(
            activity, _context(actor), _request(runtime), Response()
        )
        assert any(
            receipt.schedule_ref == schedule.schedule_ref
            and receipt.unschedule_operation_id == removed.operation_id
            for receipt in receipts
        )
        with pytest.raises(ProblemError) as conflicting:
            await unplace_activity_timeline(
                activity,
                ActivityTimelineUnplaceCommand(
                    operation_id="timeline-unplace:second",
                    schedule_ref=schedule.schedule_ref,
                    expected_material_state_ref=schedule.material_state_ref,
                ),
                _context(actor),
                _request(runtime),
                Response(),
            )
        assert conflicting.value.status == 409

        undone = await undo_activity_timeline(
            activity,
            ActivityTimelineUndoCommand(
                operation_id="timeline-unplace:restore",
                schedule_ref=schedule.schedule_ref,
                unschedule_operation_id=removed.operation_id,
                expected_session_fingerprint=impact.fingerprint,
            ),
            _context(actor),
            _request(runtime),
            Response(),
        )
        assert undone.placement_material_state_ref is not None
        assert undone.placement_material_state_ref != schedule.material_state_ref

        snapshot = await get_activity_edit_snapshot(
            activity, _context(actor), _request(runtime), Response()
        )
        envelope = next(row for row in snapshot.schedules if row.role_code == "envelope")
        assert envelope.schedule_ref == schedule.schedule_ref
        assert envelope.placement_material_state_ref == undone.placement_material_state_ref
        assert envelope.starts_local_at == datetime(2026, 10, 18, 10, 0)  # noqa: DTZ001
        assert envelope.ends_local_at == datetime(2026, 10, 18, 11, 0)  # noqa: DTZ001
        assert (
            await list_activity_timeline_undo(
                activity, _context(actor), _request(runtime), Response()
            )
            == []
        )
    finally:
        await runtime.dispose()
