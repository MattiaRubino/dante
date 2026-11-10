"""Native bounded Event series: local exceptions then following edit, all atomic.

Real-stack persona E04 exposed HTTP 409 after two local Event revisions.
The regression exercises the production PostgreSQL functions, including
the selected Event title profile patch and new Life Area transaction.
"""

from __future__ import annotations

from dataclasses import replace
from datetime import date, time
from types import SimpleNamespace
from typing import Any

import pytest
from fastapi import Request, Response
from sqlalchemy import text
from sqlalchemy.exc import OperationalError
from tests.integration.temporal.test_primary_life_area_assignment import _seed_self
from tests.integration.temporal.test_recurring_event_create import _daily_named_zone
from tests.integration.temporal.test_schedule_place import _context

from dante.modules.temporal import recurring_series_edit
from dante.modules.temporal.application import (
    TemporalTimelineApplication,
    TimelineScheduledOccurrenceItem,
)
from dante.modules.temporal.contracts import TimelineWindowQuery
from dante.modules.temporal.event_occurrence_policy import EventOccurrencePolicyApplication
from dante.modules.temporal.occurrence import CalendarCoordinate
from dante.modules.temporal.occurrence_api import (
    EventOccurrenceLocalEditCommand,
    accept_event_occurrence_local_edit,
)
from dante.modules.temporal.recurring_authoring import RecurringAuthoringApplication
from dante.modules.temporal.recurring_series_edit import RecurringSeriesEditApplication
from dante.modules.temporal.routine_occurrence_materialization import (
    RoutineOccurrenceMaterializationApplication,
)
from dante.platform.database.runtime import create_database_runtime

pytestmark = pytest.mark.postgres


@pytest.mark.asyncio
async def test_native_finite_event_preserves_local_first_last_and_accepts_following(
    migrated_database: Any,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    actor = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    authoring = RecurringAuthoringApplication(runtime.session_factory)
    policies = EventOccurrencePolicyApplication(runtime.session_factory)
    materializer = RoutineOccurrenceMaterializationApplication(runtime.session_factory)
    timeline = TemporalTimelineApplication(runtime.session_factory)
    series = RecurringSeriesEditApplication(runtime.session_factory)
    first_date = date(2027, 1, 3)
    final_date = date(2027, 2, 28)
    next_date = date(2027, 1, 17)
    recurrence = replace(
        _daily_named_zone(),
        range_kind="expected_count",
        expected_occurrence_count=5,
        effective_from=first_date,
        pattern_code="weekly_weekdays",
        interval_count=2,
        pattern_anchor_date=first_date,
        weekdays=(7,),
        wall_times=(time(11, 20),),
    )

    try:
        created = await authoring.create_event(
            self_person_ref=actor,
            operation_id="e04:finite:create",
            title="E04 Event source",
            life_area_intent=None,
            agenda_parts=("Prima scaletta",),
            description=None,
            location=None,
            item_color_code=None,
            recurrence=recurrence,
        )
        await policies.set(
            self_person_ref=actor,
            event_ref=created.source_ref,
            placement_kind="timed",
            duration_minutes=40,
            duration_days=None,
            reminder_lead_minutes=None,
            placement_protected=True,
        )
        await materializer.checkpoint_window(
            self_person_ref=actor,
            operation_id="e04:finite:checkpoint",
            start_date=first_date,
            end_date_exclusive=date(2027, 3, 1),
            effective_zone_id="Europe/Rome",
        )
        window = await timeline.read_window(
            query=TimelineWindowQuery(start_date=first_date, end_date_exclusive=date(2027, 3, 1)),
            context=_context(actor),
        )
        physical = [
            item
            for item in window.items
            if isinstance(item, TimelineScheduledOccurrenceItem)
            and item.source_native_ref == created.source_ref
        ]
        by_date = {
            item.coordinate.generated_date: item
            for item in physical
            if isinstance(item.coordinate, CalendarCoordinate)
        }
        assert len(by_date) == len(physical) == 5
        assert sorted(by_date) == [
            first_date,
            next_date,
            date(2027, 1, 31),
            date(2027, 2, 14),
            final_date,
        ]
        request = Request(
            {
                "type": "http",
                "app": SimpleNamespace(state=SimpleNamespace(database_runtime=runtime)),
            }
        )
        context = _context(actor)
        for revision, target in enumerate((by_date[first_date], by_date[final_date])):
            saved = await accept_event_occurrence_local_edit(
                target.occurrence_ref,
                EventOccurrenceLocalEditCommand.model_validate(
                    {
                        "operation_id": f"e04:local:{revision}",
                        "expected_revision": revision,
                        "expected_recurrence_state_ref": created.recurrence_material_state_ref,
                        "profile_patch": {"title": f"E04 eccezione {revision}"},
                        "structure": {
                            "agenda_parts": [f"Scaletta eccezione {revision}"],
                            "life_area_ref": None,
                            "expected_participants": [],
                        },
                    }
                ),
                context,
                request,
                Response(),
            )
            assert saved.revision == revision + 1

        selected_ref = by_date[next_date].occurrence_ref
        source = await series.source(self_person_ref=actor, selected_occurrence_ref=selected_ref)
        assert source.edit_revision == 2
        assert source.remaining_including_selected == 4
        assert source.remaining_after_selected == 3
        proposal = replace(source.recurrence, effective_from=next_date, expected_occurrence_count=4)
        structure = {
            **source.structure_snapshot,
            "agenda_parts": ["Scaletta serie aggiornata"],
            "new_life_area": {"name": "E04 Area futura", "color_code": "#EA5C12"},
        }
        patch = {"title": "E04 serie aggiornata"}
        preview = await series.preview(
            self_person_ref=actor,
            selected_occurrence_ref=selected_ref,
            requested_scope="this_and_following",
            expected_revision=source.edit_revision,
            expected_state_ref=source.recurrence_state_ref,
            effective_zone_id="Europe/Rome",
            proposed_recurrence=proposal,
            proposed_structure=structure,
            profile_patch=patch,
        )
        assert len(preview.scope.protected_future_occurrence_refs) == 1

        # First attempt simulates the SQLSTATE 40001 observed during a
        # concurrent Life Area CREATE in Chromium E04. Real DB transaction
        # rolls back, then the same intent must commit in the next transaction
        # with one area and one series revision, without preview bypass.
        original_create = recurring_series_edit.create_life_area_in_session
        create_attempts = 0

        class SerializationAbortError(Exception):
            sqlstate = "40001"

        async def transient_create(*args: Any, **kwargs: Any) -> Any:
            nonlocal create_attempts
            create_attempts += 1
            if create_attempts == 1:
                raise OperationalError(
                    "redacted diagnostic statement",
                    {},
                    SerializationAbortError("simulated serialization failure"),
                )
            return await original_create(*args, **kwargs)

        monkeypatch.setattr(
            recurring_series_edit,
            "create_life_area_in_session",
            transient_create,
        )
        accepted = await series.accept(
            self_person_ref=actor,
            selected_occurrence_ref=selected_ref,
            requested_scope="this_and_following",
            expected_revision=source.edit_revision,
            expected_state_ref=source.recurrence_state_ref,
            effective_zone_id="Europe/Rome",
            proposed_recurrence=proposal,
            proposed_structure=structure,
            profile_patch=patch,
            expected_fingerprint=preview.fingerprint,
            operation_id="e04:series:accept",
        )
        assert create_attempts == 2
        replay = await series.accept(
            self_person_ref=actor,
            selected_occurrence_ref=selected_ref,
            requested_scope="this_and_following",
            expected_revision=source.edit_revision,
            expected_state_ref=source.recurrence_state_ref,
            effective_zone_id="Europe/Rome",
            proposed_recurrence=proposal,
            proposed_structure=structure,
            profile_patch=patch,
            expected_fingerprint=preview.fingerprint,
            operation_id="e04:series:accept",
        )
        assert replay.replayed
        assert replay.recurrence_state_ref == accepted.recurrence_state_ref
        assert create_attempts == 2
        assert accepted.protected_count == 1
        assert accepted.superseded_count == len(preview.scope.target_occurrence_refs)

        async with runtime.session_factory() as session, session.begin():
            area_rows = (
                await session.execute(
                    text(
                        "SELECT life_area_ref FROM dante.list_self_life_areas(:actor) "
                        "WHERE name='E04 Area futura'"
                    ),
                    {"actor": actor},
                )
            ).all()
            assert len(area_rows) == 1

        # The first and final explicit local edits must survive a source edit.
        await materializer.checkpoint_window(
            self_person_ref=actor,
            operation_id="e04:after:checkpoint",
            start_date=first_date,
            end_date_exclusive=date(2027, 3, 1),
            effective_zone_id="Europe/Rome",
        )
        after = await timeline.read_window(
            query=TimelineWindowQuery(start_date=first_date, end_date_exclusive=date(2027, 3, 1)),
            context=context,
        )
        titles = {
            item.coordinate.generated_date: item.title
            for item in after.items
            if isinstance(item, TimelineScheduledOccurrenceItem)
            and item.source_native_ref == created.source_ref
            and isinstance(item.coordinate, CalendarCoordinate)
        }
        assert titles[first_date] == "E04 eccezione 0"
        assert titles[final_date] == "E04 eccezione 1"
        assert titles[next_date] == "E04 serie aggiornata"

        beyond_final = date(2027, 3, 14)
        await materializer.checkpoint_window(
            self_person_ref=actor,
            operation_id="e04:after:last-boundary",
            start_date=beyond_final,
            end_date_exclusive=date(2027, 3, 15),
            effective_zone_id="Europe/Rome",
        )
        expired = await timeline.read_window(
            query=TimelineWindowQuery(
                start_date=beyond_final, end_date_exclusive=date(2027, 3, 15)
            ),
            context=context,
        )
        assert not any(
            item.source_native_ref == created.source_ref
            for item in expired.items
            if isinstance(item, TimelineScheduledOccurrenceItem)
        )
    finally:
        await runtime.dispose()
