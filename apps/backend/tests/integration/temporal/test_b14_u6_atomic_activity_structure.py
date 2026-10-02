"""Atomic root, direct children and planned Schedule rows use canonical owners."""

from __future__ import annotations

from datetime import UTC, datetime
from types import SimpleNamespace
from typing import Any

import psycopg
import pytest
from tests.integration.temporal.test_b14_u2_authoring import _seed_self

from dante.modules.temporal.authoring import (
    ActivityChildIntent,
    TemporalAuthoringApplication,
    TemporalAuthoringOperationIdReuseError,
    TemporalAuthoringStructureConflictError,
)
from dante.modules.temporal.decomposition_api import get_activity_children
from dante.modules.temporal.schedule import AbsoluteIntervalPlacement
from dante.platform.database.runtime import create_database_runtime

pytestmark = pytest.mark.postgres


@pytest.mark.asyncio
async def test_root_children_and_planned_slices_are_atomic_and_replayable(
    migrated_database: Any,
) -> None:
    actor = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    authoring = TemporalAuthoringApplication(runtime.session_factory)
    root_window = AbsoluteIntervalPlacement(
        starts_at=datetime(2026, 10, 20, 8, tzinfo=UTC),
        ends_at=datetime(2026, 10, 20, 18, tzinfo=UTC),
    )
    first_slice = AbsoluteIntervalPlacement(
        starts_at=datetime(2026, 10, 20, 9, tzinfo=UTC),
        ends_at=datetime(2026, 10, 20, 10, tzinfo=UTC),
    )
    second_slice = AbsoluteIntervalPlacement(
        starts_at=datetime(2026, 10, 20, 12, tzinfo=UTC),
        ends_at=datetime(2026, 10, 20, 13, tzinfo=UTC),
    )
    children = (
        ActivityChildIntent(
            title="Prepare materials",
            presentation_order=1,
            placement=first_slice,
            session_capture_mode="live",
        ),
        ActivityChildIntent(
            title="Present",
            requirement_code="optional",
            presentation_order=2,
            planned_slices=(second_slice,),
        ),
    )
    try:
        created = await authoring.create_activity(
            self_person_ref=actor,
            operation_id="u6:atomic:tree",
            title="Workshop",
            placement=root_window,
            planned_slices=(first_slice, second_slice),
            children=children,
            session_capture_mode="record_and_live",
        )
        assert not created.replayed
        assert len(created.children) == 2
        assert len(created.planned_slices) == 2
        assert created.children[0].schedule is not None
        assert created.children[1].planned_slices[0].subject_native_ref == (
            created.children[1].item.subject_native_ref
        )
        replay = await authoring.create_activity(
            self_person_ref=actor,
            operation_id="u6:atomic:tree",
            title="Workshop",
            placement=root_window,
            planned_slices=(first_slice, second_slice),
            children=children,
            session_capture_mode="record_and_live",
        )
        assert replay.replayed
        assert replay.item.subject_native_ref == created.item.subject_native_ref
        assert [child.decomposition_ref for child in replay.children] == [
            child.decomposition_ref for child in created.children
        ]
        assert [schedule.schedule_ref for schedule in replay.planned_slices] == [
            schedule.schedule_ref for schedule in created.planned_slices
        ]
        current = await get_activity_children(
            created.item.subject_native_ref,
            SimpleNamespace(self_person_ref=actor),
            SimpleNamespace(app=SimpleNamespace(state=SimpleNamespace(database_runtime=runtime))),
        )
        assert [child.child_activity_ref for child in current.children] == [
            child.item.subject_native_ref for child in created.children
        ]
        assert len(current.schedules) == 3
        assert len(current.children[0].schedules) == 1
        assert current.children[0].session_capture_mode == "live"
        assert len(current.children[1].schedules) == 1
        with pytest.raises(TemporalAuthoringOperationIdReuseError):
            await authoring.create_activity(
                self_person_ref=actor,
                operation_id="u6:atomic:tree",
                title="Workshop",
                placement=root_window,
                planned_slices=(first_slice, second_slice),
                children=children[:1],
                session_capture_mode="record_and_live",
            )

        outside = AbsoluteIntervalPlacement(
            starts_at=datetime(2026, 10, 21, 9, tzinfo=UTC),
            ends_at=datetime(2026, 10, 21, 10, tzinfo=UTC),
        )
        with pytest.raises(TemporalAuthoringStructureConflictError):
            await authoring.create_activity(
                self_person_ref=actor,
                operation_id="u6:atomic:rollback",
                title="No tree",
                placement=root_window,
                children=(ActivityChildIntent(title="Outside", placement=outside),),
            )
        with psycopg.connect(
            **migrated_database.connection_kwargs(
                "dante_migrator", migrated_database.cluster.migrator_password
            )
        ) as connection:
            connection.execute("SET ROLE dante_owner")
            assert connection.execute(
                "SELECT count(*) FROM dante.activity_intention WHERE title='No tree'"
            ).fetchone() == (0,)
            assert connection.execute(
                "SELECT count(*) FROM dante.schedule WHERE subject_native_ref=%s",
                (created.item.subject_native_ref,),
            ).fetchone() == (3,)
            assert connection.execute(
                "SELECT count(*) FROM dante.session_execution_subject "
                "WHERE subject_native_ref=ANY(%s)",
                (
                    [
                        created.item.subject_native_ref,
                        *(child.item.subject_native_ref for child in created.children),
                    ],
                ),
            ).fetchone() == (0,)
    finally:
        await runtime.dispose()
