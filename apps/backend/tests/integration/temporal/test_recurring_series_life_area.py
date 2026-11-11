"""Recurring Event Life Area series edits: atomicity, CAS and canonical readback."""

from __future__ import annotations

from dataclasses import replace
from datetime import date, time
from types import SimpleNamespace
from typing import Any, cast
from zoneinfo import ZoneInfo

import pytest
from fastapi import Request, Response
from sqlalchemy import text
from tests.integration.temporal.test_primary_life_area_assignment import _seed_self
from tests.integration.temporal.test_recurring_event_create import _daily_named_zone
from tests.integration.temporal.test_schedule_place import _context

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
from dante.modules.temporal.occurrence_api import get_recurring_event_occurrence_detail
from dante.modules.temporal.recurring_authoring import RecurringAuthoringApplication
from dante.modules.temporal.recurring_series_edit import (
    RecurringSeriesEditApplication,
)
from dante.modules.temporal.routine_occurrence_materialization import (
    RoutineOccurrenceMaterializationApplication,
)
from dante.platform.database.runtime import create_database_runtime

pytestmark = pytest.mark.postgres


@pytest.mark.asyncio
async def test_event_following_series_life_area_is_atomic_and_survives_reload(
    migrated_database: Any,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    actor = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    series = RecurringSeriesEditApplication(runtime.session_factory)
    authoring = RecurringAuthoringApplication(runtime.session_factory)
    policy = EventOccurrencePolicyApplication(runtime.session_factory)
    materializer = RoutineOccurrenceMaterializationApplication(runtime.session_factory)
    timeline = TemporalTimelineApplication(runtime.session_factory)
    day = date(2027, 1, 2)

    async def catalog(name: str) -> list[dict[str, Any]]:
        async with runtime.session_factory() as session, session.begin():
            rows = (
                (
                    await session.execute(
                        text(
                            "SELECT life_area_ref,revision,color_code,icon_code "
                            "FROM dante.list_self_life_areas(:actor) WHERE name=:name"
                        ),
                        {"actor": actor, "name": name},
                    )
                )
                .mappings()
                .all()
            )
            return [dict(row) for row in rows]

    async def selected() -> Any:
        window = await timeline.read_window(
            query=TimelineWindowQuery(
                start_date=day,
                end_date_exclusive=date(2027, 1, 4),
            ),
            context=_context(actor),
        )
        items = [
            item
            for item in window.items
            if isinstance(item, TimelineScheduledOccurrenceItem)
            and item.source_native_ref == created.source_ref
        ]
        assert items
        return items[0].occurrence_ref

    try:
        created = await authoring.create_event(
            self_person_ref=actor,
            operation_id="series-area:create-event",
            title="Evento con Life Area da serie",
            life_area_intent=None,
            agenda_parts=(),
            description=None,
            location=None,
            item_color_code=None,
            recurrence=_daily_named_zone(),
        )
        await policy.set(
            self_person_ref=actor,
            event_ref=created.source_ref,
            placement_kind="timed",
            duration_minutes=60,
            duration_days=None,
            reminder_lead_minutes=None,
        )
        await materializer.checkpoint_window(
            self_person_ref=actor,
            operation_id="series-area:checkpoint-before",
            start_date=day,
            end_date_exclusive=date(2027, 1, 4),
            effective_zone_id="Europe/Rome",
        )
        initial_ref = await selected()
        loaded = await series.source(self_person_ref=actor, selected_occurrence_ref=initial_ref)
        assert loaded.structure_snapshot["life_area_ref"] is None
        assert loaded.remaining_including_selected is None
        assert loaded.remaining_after_selected is None
        proposed = replace(loaded.recurrence, effective_from=day)
        structure = {
            **loaded.structure_snapshot,
            "new_life_area": {"name": "Serie Blu", "color_code": "#4285F4"},
        }
        preview = await series.preview(
            self_person_ref=actor,
            selected_occurrence_ref=initial_ref,
            requested_scope="this_and_following",
            expected_revision=loaded.edit_revision,
            expected_state_ref=loaded.recurrence_state_ref,
            effective_zone_id="Europe/Rome",
            proposed_recurrence=proposed,
            proposed_structure=structure,
            profile_patch=None,
        )
        assert await catalog("Serie Blu") == []
        accepted = await series.accept(
            self_person_ref=actor,
            selected_occurrence_ref=initial_ref,
            requested_scope="this_and_following",
            expected_revision=loaded.edit_revision,
            expected_state_ref=loaded.recurrence_state_ref,
            effective_zone_id="Europe/Rome",
            proposed_recurrence=proposed,
            proposed_structure=structure,
            profile_patch=None,
            expected_fingerprint=preview.fingerprint,
            operation_id="series-area:accept",
        )
        replay = await series.accept(
            self_person_ref=actor,
            selected_occurrence_ref=initial_ref,
            requested_scope="this_and_following",
            expected_revision=loaded.edit_revision,
            expected_state_ref=loaded.recurrence_state_ref,
            effective_zone_id="Europe/Rome",
            proposed_recurrence=proposed,
            proposed_structure=structure,
            profile_patch=None,
            expected_fingerprint=preview.fingerprint,
            operation_id="series-area:accept",
        )
        assert replay.replayed
        assert replay.recurrence_state_ref == accepted.recurrence_state_ref
        assert accepted.preserved_occurrence_ref is None
        assert replay.preserved_occurrence_ref is None
        assert accepted.superseded_count == len(preview.scope.target_occurrence_refs)
        existing = await catalog("Serie Blu")
        assert len(existing) == 1
        assert existing[0]["color_code"] == "#4285F4"
        assigned_ref = existing[0]["life_area_ref"]

        await materializer.checkpoint_window(
            self_person_ref=actor,
            operation_id="series-area:checkpoint-after",
            start_date=day,
            end_date_exclusive=date(2027, 1, 4),
            effective_zone_id="Europe/Rome",
        )
        current_ref = await selected()
        current = await series.source(self_person_ref=actor, selected_occurrence_ref=current_ref)
        assert current.structure_snapshot["life_area_ref"] == str(assigned_ref)
        assert "new_life_area" not in current.structure_snapshot

        request = cast(
            Request,
            SimpleNamespace(app=SimpleNamespace(state=SimpleNamespace(database_runtime=runtime))),
        )
        detail = await get_recurring_event_occurrence_detail(
            current_ref, _context(actor), request, Response()
        )
        assert detail.life_area_ref == assigned_ref

        # A subsequent global color edit must use the same transaction/CAS,
        # preserve the area identity, and reject stale revisions.
        recolor = {
            **current.structure_snapshot,
            "area_color_change": {
                "life_area_ref": str(assigned_ref),
                "expected_revision": existing[0]["revision"],
                "color_code": "#33B679",
            },
        }
        revised = replace(current.recurrence, effective_from=day)
        second_preview = await series.preview(
            self_person_ref=actor,
            selected_occurrence_ref=current_ref,
            requested_scope="this_and_following",
            expected_revision=current.edit_revision,
            expected_state_ref=current.recurrence_state_ref,
            effective_zone_id="Europe/Rome",
            proposed_recurrence=revised,
            proposed_structure=recolor,
            profile_patch=None,
        )
        await series.accept(
            self_person_ref=actor,
            selected_occurrence_ref=current_ref,
            requested_scope="this_and_following",
            expected_revision=current.edit_revision,
            expected_state_ref=current.recurrence_state_ref,
            effective_zone_id="Europe/Rome",
            proposed_recurrence=revised,
            proposed_structure=recolor,
            profile_patch=None,
            expected_fingerprint=second_preview.fingerprint,
            operation_id="series-area:recolor",
        )
        recolored = await catalog("Serie Blu")
        assert len(recolored) == 1
        assert recolored[0]["life_area_ref"] == assigned_ref
        assert recolored[0]["color_code"] == "#33B679"

        # Deliberately abort after transactional area creation. The new area
        # and any recurrence write must both disappear on rollback.
        await materializer.checkpoint_window(
            self_person_ref=actor,
            operation_id="series-area:checkpoint-recolored",
            start_date=day,
            end_date_exclusive=date(2027, 1, 4),
            effective_zone_id="Europe/Rome",
        )
        third_ref = await selected()
        third = await series.source(self_person_ref=actor, selected_occurrence_ref=third_ref)
        orphan = {
            **third.structure_snapshot,
            "life_area_ref": None,
            "new_life_area": {"name": "Area non committata", "color_code": "#FFD600"},
        }
        orphan_preview = await series.preview(
            self_person_ref=actor,
            selected_occurrence_ref=third_ref,
            requested_scope="this_and_following",
            expected_revision=third.edit_revision,
            expected_state_ref=third.recurrence_state_ref,
            effective_zone_id="Europe/Rome",
            proposed_recurrence=replace(third.recurrence, effective_from=day),
            proposed_structure=orphan,
            profile_patch=None,
        )

        async def abort_policy(*_args: Any, **_kwargs: Any) -> None:
            raise RuntimeError("forced atomic rollback")

        monkeypatch.setattr(series._policies, "replace_in_session", abort_policy)
        with pytest.raises(RuntimeError, match="forced atomic rollback"):
            await series.accept(
                self_person_ref=actor,
                selected_occurrence_ref=third_ref,
                requested_scope="this_and_following",
                expected_revision=third.edit_revision,
                expected_state_ref=third.recurrence_state_ref,
                effective_zone_id="Europe/Rome",
                proposed_recurrence=replace(third.recurrence, effective_from=day),
                proposed_structure=orphan,
                profile_patch=None,
                expected_fingerprint=orphan_preview.fingerprint,
                operation_id="series-area:aborted",
            )
        assert await catalog("Area non committata") == []
    finally:
        await runtime.dispose()


@pytest.mark.asyncio
async def test_monthly_all_day_event_following_edit_resolves_midnight_and_preserves_local_first(
    migrated_database: Any,
) -> None:
    """Real PostgreSQL: a local first edit must not block later all-day series authoring."""
    actor = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    authoring = RecurringAuthoringApplication(runtime.session_factory)
    policy = EventOccurrencePolicyApplication(runtime.session_factory)
    materializer = RoutineOccurrenceMaterializationApplication(runtime.session_factory)
    timeline = TemporalTimelineApplication(runtime.session_factory)
    series = RecurringSeriesEditApplication(runtime.session_factory)
    first_day = date(2026, 11, 16)
    selected_day = date(2026, 12, 21)
    next_day = date(2027, 1, 18)
    end_exclusive = date(2027, 1, 20)
    zone = ZoneInfo("Europe/Rome")
    recurrence = replace(
        _daily_named_zone(),
        effective_from=first_day,
        pattern_code="monthly_ordinal_weekdays",
        wall_times=(),
        ordinal_weekdays=((1, 3),),
    )

    try:
        created = await authoring.create_event(
            self_person_ref=actor,
            operation_id="all-day-series:create",
            title="Mensile tutto il giorno",
            life_area_intent=None,
            agenda_parts=("Scaletta iniziale",),
            description=None,
            location=None,
            item_color_code=None,
            recurrence=recurrence,
        )
        await policy.set(
            self_person_ref=actor,
            event_ref=created.source_ref,
            placement_kind="all_day",
            duration_minutes=None,
            duration_days=1,
            reminder_lead_minutes=None,
        )
        await materializer.checkpoint_window(
            self_person_ref=actor,
            operation_id="all-day-series:checkpoint",
            start_date=first_day,
            end_date_exclusive=end_exclusive,
            effective_zone_id="Europe/Rome",
        )
        window = await timeline.read_window(
            query=TimelineWindowQuery(start_date=first_day, end_date_exclusive=end_exclusive),
            context=_context(actor),
        )
        instances = {
            item.coordinate.generated_date: item
            for item in window.items
            if isinstance(item, TimelineScheduledOccurrenceItem)
            and item.source_native_ref == created.source_ref
            and isinstance(item.coordinate, CalendarCoordinate)
        }
        assert set(instances) == {first_day, selected_day, next_day}
        first_ref = instances[first_day].occurrence_ref
        selected_ref = instances[selected_day].occurrence_ref
        next_ref = instances[next_day].occurrence_ref

        request = Request(
            {
                "type": "http",
                "app": SimpleNamespace(state=SimpleNamespace(database_runtime=runtime)),
            }
        )
        local = await accept_event_occurrence_local_edit(
            first_ref,
            EventOccurrenceLocalEditCommand.model_validate(
                {
                    "operation_id": "all-day-series:first-local",
                    "expected_revision": 0,
                    "expected_recurrence_state_ref": created.recurrence_material_state_ref,
                    "profile_patch": {"title": "Prima istanza locale"},
                    "structure": {
                        "agenda_parts": ["Scaletta locale"],
                        "life_area_ref": None,
                        "expected_participants": [],
                    },
                }
            ),
            _context(actor),
            request,
            Response(),
        )
        assert local.revision == 1

        # In the original SQL this SELECT raised
        # occurrence_edit_unresolved_zone even though an all-day date has no
        # timed instant. The civil-midnight ordering must stay in Rome.
        async with runtime.session_factory() as session, session.begin():
            instant = await session.scalar(
                text("SELECT dante.occurrence_edit_coordinate_instant(:actor,:occurrence,:zone)"),
                {
                    "actor": actor,
                    "occurrence": selected_ref,
                    "zone": "Europe/Rome",
                },
            )
        assert instant is not None
        local_instant = instant.astimezone(zone)
        assert local_instant.date() == selected_day
        assert local_instant.timetz().replace(tzinfo=None) == time.min

        loaded = await series.source(
            self_person_ref=actor, selected_occurrence_ref=selected_ref
        )
        assert loaded.edit_revision == 1
        proposal = replace(loaded.recurrence, effective_from=selected_day)
        structure = {
            **loaded.structure_snapshot,
            "new_life_area": {
                "name": "Area mensile tutto il giorno",
                "color_code": "#4285F4",
            },
        }
        preview = await series.preview(
            self_person_ref=actor,
            selected_occurrence_ref=selected_ref,
            requested_scope="this_and_following",
            expected_revision=loaded.edit_revision,
            expected_state_ref=loaded.recurrence_state_ref,
            effective_zone_id="Europe/Rome",
            proposed_recurrence=proposal,
            proposed_structure=structure,
            profile_patch=None,
        )
        assert set(preview.scope.target_occurrence_refs) == {selected_ref, next_ref}
        assert first_ref not in preview.scope.target_occurrence_refs

        accepted = await series.accept(
            self_person_ref=actor,
            selected_occurrence_ref=selected_ref,
            requested_scope="this_and_following",
            expected_revision=loaded.edit_revision,
            expected_state_ref=loaded.recurrence_state_ref,
            effective_zone_id="Europe/Rome",
            proposed_recurrence=proposal,
            proposed_structure=structure,
            profile_patch=None,
            expected_fingerprint=preview.fingerprint,
            operation_id="all-day-series:accept",
        )
        assert accepted.source_ref == created.source_ref
        assert accepted.recurrence_state_ref != loaded.recurrence_state_ref

        async with runtime.session_factory() as session, session.begin():
            patch = await session.scalar(
                text("SELECT dante.get_self_occurrence_profile_patch(:actor,:occurrence)"),
                {"actor": actor, "occurrence": first_ref},
            )
            areas = (
                (
                    await session.execute(
                        text(
                            "SELECT life_area_ref,color_code FROM "
                            "dante.list_self_life_areas(:actor) WHERE name=:name"
                        ),
                        {
                            "actor": actor,
                            "name": "Area mensile tutto il giorno",
                        },
                    )
                )
                .mappings()
                .all()
            )
        assert patch["title"] == "Prima istanza locale"
        assert len(areas) == 1
        assert areas[0]["color_code"] == "#4285F4"
    finally:
        await runtime.dispose()
