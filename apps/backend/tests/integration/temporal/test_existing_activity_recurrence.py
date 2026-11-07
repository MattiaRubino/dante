"""An accepted Activity becomes the first Routine instance without replacement."""

from __future__ import annotations

from datetime import date, datetime, time
from typing import Any

import pytest
from sqlalchemy import text
from tests.integration.temporal.test_activity_quick_authoring_metadata import _seed_self
from tests.integration.temporal.test_schedule_place import _context

from dante.modules.temporal.activity_edit_snapshot_api import _SNAPSHOT, ActivityEditSnapshot
from dante.modules.temporal.application import (
    TemporalTimelineApplication,
    TimelineExpectedOccurrenceItem,
    TimelineNamedZoneLocalActivityItem,
    TimelineNamedZoneLocalEventItem,
    TimelineScheduledOccurrenceItem,
)
from dante.modules.temporal.authoring import TemporalAuthoringApplication
from dante.modules.temporal.contracts import TimelineWindowQuery
from dante.modules.temporal.recurrence import CalendarRecurrence
from dante.modules.temporal.recurring_conversion import (
    ExistingActivityBasis,
    ExistingEventBasis,
    RecurringConversionApplication,
    RecurringConversionConflictError,
)
from dante.modules.temporal.routine_occurrence_materialization import (
    RoutineOccurrenceMaterializationApplication,
)
from dante.modules.temporal.schedule import NamedZoneLocalIntervalPlacement
from dante.platform.database.runtime import create_database_runtime

pytestmark = pytest.mark.postgres


@pytest.mark.asyncio
async def test_existing_activity_starts_series_with_same_first_identity_and_one_card(
    migrated_database: Any,
) -> None:
    actor = _seed_self(migrated_database)
    other = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    try:
        authored = await TemporalAuthoringApplication(runtime.session_factory).create_activity(
            self_person_ref=actor,
            operation_id="existing-repeat:create",
            title="Studio",
            placement=NamedZoneLocalIntervalPlacement(
                starts_local_at=datetime(2027, 1, 2, 10),  # noqa: DTZ001
                ends_local_at=datetime(2027, 1, 2, 11),  # noqa: DTZ001
                zone_id="Europe/Rome",
                disambiguation="earlier",
            ),
            planned_slices=(None,),
            planned_slice_names=("Ripasso",),
        )
        ref = authored.item.subject_native_ref
        async with runtime.session_factory() as session, session.begin():
            snapshot = ActivityEditSnapshot.model_validate(
                await session.scalar(_SNAPSHOT, {"actor": actor, "activity": ref})
            )
            revision = await session.scalar(
                text("SELECT revision FROM dante.get_self_activity_profile(:actor,:activity)"),
                {"actor": actor, "activity": ref},
            )
        envelope = next(row for row in snapshot.schedules if row.role_code == "envelope")
        assert envelope.placement_material_state_ref is not None
        basis = ExistingActivityBasis(
            activity_ref=ref,
            expected_profile_revision=revision,
            envelope_schedule_ref=envelope.schedule_ref,
            expected_placement_state_ref=envelope.placement_material_state_ref,
        )
        recurrence = CalendarRecurrence(
            family_code="calendar_wall_clock",
            range_kind="open",
            expected_occurrence_count=None,
            effective_from=date(2027, 1, 2),
            effective_until=None,
            pattern_code="daily",
            interval_count=1,
            clock_basis_code="named_zone",
            zone_id="Europe/Rome",
            pattern_anchor_date=None,
            wall_times=(time(10),),
            weekdays=(),
            month_days=(),
            ordinal_weekdays=(),
            year_month_days=(),
            nonexistent_local_time_policy="skip_civil_candidate",
            ambiguous_local_time_policy="earlier",
            step_unit_code=None,
        )
        conversion = RecurringConversionApplication(runtime.session_factory)
        with pytest.raises(RecurringConversionConflictError):
            await conversion.activity(
                self_person_ref=other,
                operation_id="existing-repeat:foreign",
                basis=basis,
                recurrence=recurrence,
            )
        started = await conversion.activity(
            self_person_ref=actor,
            operation_id="existing-repeat:start",
            basis=basis,
            recurrence=recurrence,
        )
        replay = await conversion.activity(
            self_person_ref=actor,
            operation_id="existing-repeat:start",
            basis=basis,
            recurrence=recurrence,
        )
        assert replay.replayed
        assert replay.source_ref == started.source_ref
        with pytest.raises(RecurringConversionConflictError):
            await conversion.activity(
                self_person_ref=actor,
                operation_id="existing-repeat:another",
                basis=basis,
                recurrence=recurrence,
            )
        materializer = RoutineOccurrenceMaterializationApplication(runtime.session_factory)
        await materializer.checkpoint_window(
            self_person_ref=actor,
            operation_id="existing-repeat:window",
            start_date=date(2027, 1, 2),
            end_date_exclusive=date(2027, 1, 4),
            effective_zone_id="Europe/Rome",
        )
        window = await TemporalTimelineApplication(runtime.session_factory).read_window(
            query=TimelineWindowQuery(
                start_date=date(2027, 1, 2),
                end_date_exclusive=date(2027, 1, 4),
            ),
            context=_context(actor),
        )
        cards = [
            row
            for row in window.items
            if isinstance(row, TimelineNamedZoneLocalActivityItem) and row.title == "Studio"
        ]
        assert len(cards) == 2
        assert cards[0].activity_ref == ref
        assert cards[0].starts_local_at.time() == time(10)
        assert cards[1].activity_ref != ref
        assert cards[1].starts_local_at.time() == time(10)
    finally:
        await runtime.dispose()


@pytest.mark.asyncio
async def test_existing_event_keeps_first_event_and_excludes_duplicate_occurrence(
    migrated_database: Any,
) -> None:
    actor = _seed_self(migrated_database)
    other = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    try:
        authored = await TemporalAuthoringApplication(runtime.session_factory).create_event(
            self_person_ref=actor,
            operation_id="existing-event-repeat:create",
            title="Visita",
            agenda_parts=("Arrivo", "Colloquio"),
            placement=NamedZoneLocalIntervalPlacement(
                starts_local_at=datetime(2027, 1, 2, 10),  # noqa: DTZ001
                ends_local_at=datetime(2027, 1, 2, 11),  # noqa: DTZ001
                zone_id="Europe/Rome",
                disambiguation="earlier",
            ),
        )
        original = authored.item.subject_native_ref
        assert authored.schedule is not None
        schedule = authored.schedule
        async with runtime.session_factory() as session, session.begin():
            profile_revision = await session.scalar(
                text("SELECT dante.get_self_event_profile_revision(:actor,:event)"),
                {"actor": actor, "event": original},
            )
        recurrence = CalendarRecurrence(
            family_code="calendar_wall_clock",
            range_kind="open",
            expected_occurrence_count=None,
            effective_from=date(2027, 1, 2),
            effective_until=None,
            pattern_code="daily",
            interval_count=1,
            clock_basis_code="named_zone",
            zone_id="Europe/Rome",
            pattern_anchor_date=None,
            wall_times=(time(10),),
            weekdays=(),
            month_days=(),
            ordinal_weekdays=(),
            year_month_days=(),
            nonexistent_local_time_policy="skip_civil_candidate",
            ambiguous_local_time_policy="earlier",
            step_unit_code=None,
        )
        basis = ExistingEventBasis(
            event_ref=original,
            expected_profile_revision=profile_revision,
            schedule_ref=schedule.schedule_ref,
            expected_placement_state_ref=schedule.material_state_ref,
        )
        conversion = RecurringConversionApplication(runtime.session_factory)
        with pytest.raises(RecurringConversionConflictError):
            await conversion.event(
                self_person_ref=other,
                operation_id="existing-event-repeat:foreign",
                basis=basis,
                recurrence=recurrence,
            )
        started = await conversion.event(
            self_person_ref=actor,
            operation_id="existing-event-repeat:start",
            basis=basis,
            recurrence=recurrence,
        )
        assert started.source_ref != original
        assert (
            await conversion.event(
                self_person_ref=actor,
                operation_id="existing-event-repeat:start",
                basis=basis,
                recurrence=recurrence,
            )
        ).replayed
        with pytest.raises(RecurringConversionConflictError):
            await conversion.event(
                self_person_ref=actor,
                operation_id="existing-event-repeat:duplicate",
                basis=basis,
                recurrence=recurrence,
            )
        materializer = RoutineOccurrenceMaterializationApplication(runtime.session_factory)
        await materializer.checkpoint_window(
            self_person_ref=actor,
            operation_id="existing-event-repeat:window",
            start_date=date(2027, 1, 2),
            end_date_exclusive=date(2027, 1, 4),
            effective_zone_id="Europe/Rome",
        )
        window = await TemporalTimelineApplication(runtime.session_factory).read_window(
            query=TimelineWindowQuery(
                start_date=date(2027, 1, 2),
                end_date_exclusive=date(2027, 1, 4),
            ),
            context=_context(actor),
        )
        originals = [
            item
            for item in window.items
            if isinstance(item, TimelineNamedZoneLocalEventItem) and item.event_ref == original
        ]
        following = [
            item
            for item in window.items
            if isinstance(item, TimelineScheduledOccurrenceItem)
            and item.source_native_ref == started.source_ref
        ]
        assert len(originals) == 1
        assert originals[0].schedule_ref == schedule.schedule_ref
        assert len(following) == 1
        assert following[0].coordinate is not None
        assert not [
            item
            for item in window.items
            if isinstance(item, TimelineExpectedOccurrenceItem)
            and item.source_native_ref == started.source_ref
            and item.coordinate.generated_date == date(2027, 1, 2)
        ]
        async with runtime.session_factory() as session, session.begin():
            first_occurrence = await session.scalar(
                text(
                    "SELECT first_occurrence_ref "
                    "FROM dante.get_self_event_recurring_first_by_source(:actor,:source)"
                ),
                {"actor": actor, "source": started.source_ref},
            )
            assert first_occurrence is not None
            first_origin = (
                await session.execute(
                    text(
                        "SELECT source_native_ref,generated_date "
                        "FROM dante.get_self_occurrence(:actor,:first)"
                    ),
                    {"actor": actor, "first": first_occurrence},
                )
            ).one()
            assert first_origin.source_native_ref == started.source_ref
            assert first_origin.generated_date == date(2027, 1, 2)
            assert (
                await session.scalar(
                    text(
                        "SELECT first_event_ref FROM dante.get_self_event_recurring_first_by_occurrence("
                        ":actor,:first)"
                    ),
                    {"actor": actor, "first": first_occurrence},
                )
                == original
            )
            assert (
                await session.scalar(
                    text(
                        "SELECT first_event_ref FROM dante.get_self_event_recurring_first_by_occurrence("
                        ":actor,:first)"
                    ),
                    {"actor": other, "first": first_occurrence},
                )
                is None
            )
            assert (
                await session.scalar(
                    text(
                        "SELECT source_event_ref "
                        "FROM dante.get_self_event_recurring_seed(:actor,:event)"
                    ),
                    {"actor": actor, "event": original},
                )
                == started.source_ref
            )
            assert (
                await session.scalar(
                    text("SELECT 1 FROM dante.get_self_event_recurrence(:actor,:event)"),
                    {"actor": actor, "event": original},
                )
                is None
            )
            assert (
                await session.scalar(
                    text(
                        "SELECT source_event_ref "
                        "FROM dante.get_self_event_recurring_seed(:actor,:event)"
                    ),
                    {"actor": other, "event": original},
                )
                is None
            )
    finally:
        await runtime.dispose()
