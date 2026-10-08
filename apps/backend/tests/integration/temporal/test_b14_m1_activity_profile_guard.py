"""Regression: B14 M1 scoped metadata must not break a one-off Activity."""

from __future__ import annotations

from datetime import date, timedelta
from typing import Any

import pytest
from sqlalchemy import text
from tests.integration.temporal.test_b02_schedule_place import _context
from tests.integration.temporal.test_b14_u2_authoring import _seed_self

from dante.modules.temporal.application import (
    TemporalTimelineApplication,
    TimelineDateSpanActivityItem,
)
from dante.modules.temporal.authoring import TemporalAuthoringApplication
from dante.modules.temporal.contracts import TimelineWindowQuery
from dante.modules.temporal.schedule import (
    DateSpanPlacement,
    TemporalScheduleApplication,
)
from dante.platform.database.runtime import create_database_runtime

pytestmark = pytest.mark.postgres


@pytest.mark.asyncio
async def test_one_off_profile_snapshot_and_timeline_skip_occurrence_patch(
    migrated_database: Any,
) -> None:
    actor = _seed_self(migrated_database)
    other = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    try:
        created = await TemporalAuthoringApplication(
            runtime.session_factory
        ).create_activity(
            self_person_ref=actor,
            operation_id="m1-guard:create-one-off",
            title="Leggere",
            description="Una nota",
            location="Studio",
            item_color_code="#123ABC",
        )
        activity = created.item.subject_native_ref
        async with runtime.session_factory() as session, session.begin():
            origin = await session.scalar(
                text(
                    "SELECT dante.get_self_materialized_activity_occurrence("
                    ":actor,:activity)"
                ),
                {"actor": actor, "activity": activity},
            )
            assert origin is None
            profile = (await session.execute(
                text(
                    "SELECT * FROM dante.get_self_activity_profile("
                    ":actor,:activity)"
                ),
                {"actor": actor, "activity": activity},
            )).mappings().one()
            assert dict(profile) == {
                "activity_ref": activity,
                "title": "Leggere",
                "description": "Una nota",
                "location": "Studio",
                "color_code": "#123ABC",
                "revision": 0,
            }
            assert (await session.execute(
                text(
                    "SELECT * FROM dante.get_self_activity_profile("
                    ":actor,:activity)"
                ),
                {"actor": other, "activity": activity},
            )).first() is None

        today = date.today()
        await TemporalScheduleApplication(
            runtime.session_factory
        ).establish_schedule(
            self_person_ref=actor,
            operation_id="m1-guard:schedule-one-off",
            subject_native_ref=activity,
            placement=DateSpanPlacement(
                start_date=today,
                end_date_exclusive=today + timedelta(days=1),
            ),
        )
        projection = await TemporalTimelineApplication(
            runtime.session_factory
        ).read_window(
            query=TimelineWindowQuery(
                start_date=today,
                end_date_exclusive=today + timedelta(days=1),
            ),
            context=_context(actor),
        )
        assert any(
            isinstance(item, TimelineDateSpanActivityItem)
            and item.activity_ref == activity
            and item.title == "Leggere"
            for item in projection.items
        )
    finally:
        await runtime.dispose()
