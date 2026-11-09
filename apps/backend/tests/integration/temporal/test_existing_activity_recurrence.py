"""An accepted Activity becomes the first Routine instance without replacement."""

from __future__ import annotations

from dataclasses import replace
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
from dante.modules.temporal.occurrence import CalendarCoordinate, OccurrenceApplication
from dante.modules.temporal.placement_lock import PlacementLockApplication
from dante.modules.temporal.recurrence import CalendarRecurrence
from dante.modules.temporal.recurring_authoring import (
    EventAuthoringPolicy,
    RecurringAuthoringApplication,
)
from dante.modules.temporal.recurring_conversion import (
    ExistingActivityBasis,
    ExistingEventBasis,
    RecurringConversionApplication,
    RecurringConversionConflictError,
)
from dante.modules.temporal.recurring_series_edit import RecurringSeriesEditApplication
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
async def test_converted_activity_with_two_intervals_materializes_next_day(
    migrated_database: Any,
) -> None:
    """Regression: converted rich Activity must checkpoint its future materialization.

    One original Activity with two physical intervals and two planned Sessions
    must not produce a successful conversion POST followed by an HTTP 503 from
    the first routine occurrence checkpoint.
    """
    actor = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    day = date(2027, 1, 2)

    def placement(hour: int, minute: int, end_hour: int, end_minute: int):
        return NamedZoneLocalIntervalPlacement(
            starts_local_at=datetime(2027, 1, 2, hour, minute),  # noqa: DTZ001
            ends_local_at=datetime(2027, 1, 2, end_hour, end_minute),  # noqa: DTZ001
            zone_id="Europe/Rome",
            disambiguation="earlier",
        )

    try:
        authored = await TemporalAuthoringApplication(
            runtime.session_factory
        ).create_activity(
            self_person_ref=actor,
            operation_id="conversion:rich-two-intervals:create",
            title="Studio multiintervallo",
            placement=placement(9, 10, 11, 20),
            activity_intervals=(
                placement(9, 10, 9, 50),
                placement(10, 20, 11, 20),
            ),
            planned_slices=(placement(9, 20, 9, 30), None),
            planned_slice_names=("Studio iniziale", "Studio libero"),
        )
        activity_ref = authored.item.subject_native_ref
        async with runtime.session_factory() as session, session.begin():
            snapshot = ActivityEditSnapshot.model_validate(
                await session.scalar(
                    _SNAPSHOT, {"actor": actor, "activity": activity_ref},
                )
            )
            revision = await session.scalar(
                text("SELECT revision FROM dante.get_self_activity_profile(:actor,:activity)"),
                {"actor": actor, "activity": activity_ref},
            )
        envelope = next(
            row for row in snapshot.schedules if row.role_code == "envelope"
        )
        assert envelope.placement_material_state_ref is not None
        assert len([
            row for row in snapshot.schedules if row.role_code == "interval"
        ]) == 2
        assert len([
            row for row in snapshot.schedules if row.role_code == "planned"
        ]) == 2

        recurrence = CalendarRecurrence(
            family_code="calendar_wall_clock",
            range_kind="open",
            expected_occurrence_count=None,
            effective_from=day,
            effective_until=None,
            pattern_code="daily",
            interval_count=1,
            clock_basis_code="named_zone",
            zone_id="Europe/Rome",
            pattern_anchor_date=None,
            wall_times=(time(9, 10),),
            weekdays=(),
            month_days=(),
            ordinal_weekdays=(),
            year_month_days=(),
            nonexistent_local_time_policy="skip_civil_candidate",
            ambiguous_local_time_policy="earlier",
            step_unit_code=None,
        )
        converted = await RecurringConversionApplication(
            runtime.session_factory
        ).activity(
            self_person_ref=actor,
            operation_id="conversion:rich-two-intervals:start",
            basis=ExistingActivityBasis(
                activity_ref=activity_ref,
                expected_profile_revision=revision,
                envelope_schedule_ref=envelope.schedule_ref,
                expected_placement_state_ref=envelope.placement_material_state_ref,
            ),
            recurrence=recurrence,
        )
        assert converted.source_ref != activity_ref

        await RoutineOccurrenceMaterializationApplication(
            runtime.session_factory
        ).checkpoint_window(
            self_person_ref=actor,
            operation_id="conversion:rich-two-intervals:checkpoint",
            start_date=day,
            end_date_exclusive=date(2027, 1, 4),
            effective_zone_id="Europe/Rome",
        )
        timeline = await TemporalTimelineApplication(
            runtime.session_factory
        ).read_window(
            query=TimelineWindowQuery(
                start_date=day,
                end_date_exclusive=date(2027, 1, 4),
            ),
            context=_context(actor),
        )
        future = [
            row for row in timeline.items
            if isinstance(row, TimelineNamedZoneLocalActivityItem)
            and row.title == "Studio multiintervallo"
            and row.starts_local_at.date() == date(2027, 1, 3)
        ]
        assert len(future) == 2
        assert len({row.schedule_ref for row in future}) == 2
        activity_refs = {row.activity_ref for row in future}
        assert len(activity_refs) == 1
        generated_ref = next(iter(activity_refs))
        assert generated_ref != activity_ref

        async with runtime.session_factory() as session, session.begin():
            generated_snapshot = ActivityEditSnapshot.model_validate(
                await session.scalar(
                    _SNAPSHOT, {"actor": actor, "activity": generated_ref},
                )
            )
        assert len([
            row for row in generated_snapshot.schedules
            if row.role_code == "interval"
        ]) == 2
        assert [
            row.display_name for row in generated_snapshot.schedules
            if row.role_code == "planned"
        ] == ["Studio iniziale", "Studio libero"]
    finally:
        await runtime.dispose()


@pytest.mark.asyncio
@pytest.mark.parametrize("locked", [False, True], ids=["unlocked", "protected"])
async def test_existing_event_keeps_first_event_and_excludes_duplicate_occurrence(
    migrated_database: Any,
    locked: bool,
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
        locks = PlacementLockApplication(runtime.session_factory)
        if locked:
            original_lock = await locks.set(
                self_person_ref=actor,
                schedule_ref=schedule.schedule_ref,
                locked=True,
                expected_revision=None,
            )
            assert original_lock.locked is True
        else:
            assert (
                await locks.get(self_person_ref=actor, schedule_ref=schedule.schedule_ref)
            ).locked is False
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
        # Conversion preserves the original lock and extends that policy to
        # future Event Schedules; re-materialization must not drop it.
        assert (
            await locks.get(self_person_ref=actor, schedule_ref=schedule.schedule_ref)
        ).locked is locked
        assert (
            await locks.get(self_person_ref=actor, schedule_ref=following[0].schedule_ref)
        ).locked is locked
        assert not [
            item
            for item in window.items
            if isinstance(item, TimelineExpectedOccurrenceItem)
            and item.source_native_ref == started.source_ref
            and isinstance(item.coordinate, CalendarCoordinate)
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
                    text("SELECT dante.get_self_occurrence_edit_protection(:actor,:first)"),
                    {"actor": actor, "first": first_occurrence},
                )
                is None
            )
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
        # Re-edit the already converted Event from its *physical first*
        # Occurrence. Its Event Schedule is retained, but it must read the
        # selected+following title correction just like later Occurrences.
        series = RecurringSeriesEditApplication(runtime.session_factory)
        source = await series.source(
            self_person_ref=actor,
            selected_occurrence_ref=first_occurrence,
        )
        assert source.owner == "event"
        review = await series.preview(
            self_person_ref=actor,
            selected_occurrence_ref=first_occurrence,
            requested_scope="this_and_following",
            expected_revision=source.edit_revision,
            expected_state_ref=source.recurrence_state_ref,
            effective_zone_id="Europe/Rome",
            proposed_recurrence=source.recurrence,
            proposed_structure=source.structure_snapshot,
            profile_patch={"title": "Visita aggiornata"},
        )
        assert first_occurrence in review.scope.target_occurrence_refs
        await series.accept(
            self_person_ref=actor,
            selected_occurrence_ref=first_occurrence,
            requested_scope="this_and_following",
            expected_revision=source.edit_revision,
            expected_state_ref=source.recurrence_state_ref,
            effective_zone_id="Europe/Rome",
            proposed_recurrence=source.recurrence,
            proposed_structure=source.structure_snapshot,
            profile_patch={"title": "Visita aggiornata"},
            expected_fingerprint=review.fingerprint,
            operation_id="existing-event-repeat:edit-first",
        )
        revised_window = await TemporalTimelineApplication(runtime.session_factory).read_window(
            query=TimelineWindowQuery(
                start_date=date(2027, 1, 2),
                end_date_exclusive=date(2027, 1, 4),
            ),
            context=_context(actor),
        )
        revised_original = [
            item
            for item in revised_window.items
            if isinstance(item, TimelineNamedZoneLocalEventItem) and item.event_ref == original
        ]
        assert len(revised_original) == 1
        assert revised_original[0].schedule_ref == schedule.schedule_ref
        assert revised_original[0].title == "Visita aggiornata"

        async with runtime.session_factory() as session, session.begin():
            await session.execute(
                text(
                    "SELECT * FROM dante.revise_self_event_profile("
                    ":actor,:event,:operation,:expected,:title,:description,:location,:color)"
                ),
                {
                    "actor": actor,
                    "event": original,
                    "operation": "existing-event-repeat:local-first-edit",
                    "expected": profile_revision,
                    "title": "Visita locale aggiornata",
                    "description": None,
                    "location": None,
                    "color": None,
                },
            )
            assert (
                await session.scalar(
                    text("SELECT dante.get_self_occurrence_edit_protection(:actor,:first)"),
                    {"actor": actor, "first": first_occurrence},
                )
                == "local_change"
            )
    finally:
        await runtime.dispose()


@pytest.mark.asyncio
async def test_legacy_event_first_exclusion_recovers_once_without_copying_event(
    migrated_database: Any,
) -> None:
    """A 171-style seed is repaired on the next ordinary Timeline checkpoint."""
    actor = _seed_self(migrated_database)
    stranger = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    first_date = date(2099, 1, 5)
    recurrence = CalendarRecurrence(
        family_code="calendar_wall_clock",
        range_kind="open",
        expected_occurrence_count=None,
        effective_from=first_date,
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
    try:
        existing = await TemporalAuthoringApplication(runtime.session_factory).create_event(
            self_person_ref=actor,
            operation_id="legacy-first-event:original",
            title="Appuntamento originale",
            agenda_parts=("Agenda originale",),
            placement=NamedZoneLocalIntervalPlacement(
                starts_local_at=datetime(2099, 1, 5, 10),  # noqa: DTZ001
                ends_local_at=datetime(2099, 1, 5, 11),  # noqa: DTZ001
                zone_id="Europe/Rome",
                disambiguation="earlier",
            ),
        )
        event_ref = existing.item.subject_native_ref
        assert existing.schedule is not None
        schedule = existing.schedule
        series = await RecurringAuthoringApplication(runtime.session_factory).create_event(
            self_person_ref=actor,
            operation_id="legacy-first-event:series",
            title="Appuntamento originale",
            life_area_intent=None,
            recurrence=recurrence,
            agenda_parts=("Agenda originale",),
            policy=EventAuthoringPolicy(
                placement_kind="timed",
                duration_minutes=60,
                duration_days=None,
                reminder_lead_minutes=None,
                reality_mode="manual",
                objectives=(),
            ),
        )
        assert isinstance(schedule.placement, NamedZoneLocalIntervalPlacement)
        first = CalendarCoordinate(
            family_code="calendar_wall_clock",
            generated_date=first_date,
            generated_wall_time=time(10),
            clock_basis_code="named_zone",
            zone_id="Europe/Rome",
            resolved_at=schedule.placement.resolved_start_at,
        )
        async with runtime.session_factory() as session, session.begin():
            excluded = await OccurrenceApplication(runtime.session_factory).exclude_in_session(
                session,
                owner="event",
                self_person_ref=actor,
                source_ref=series.source_ref,
                governing_recurrence_state_ref=series.recurrence_material_state_ref,
                operation_id="b06d:existing-event-first:" + "a" * 64,
                coordinate=first,
            )
            profile_revision = await session.scalar(
                text("SELECT dante.get_self_event_profile_revision(:actor,:event)"),
                {"actor": actor, "event": event_ref},
            )
            await session.execute(
                text(
                    "SELECT * FROM dante.bind_self_event_recurring_seed("
                    ":actor,:event,:source,:schedule,:placement,:revision,:day)"
                ),
                {
                    "actor": actor,
                    "event": event_ref,
                    "source": series.source_ref,
                    "schedule": schedule.schedule_ref,
                    "placement": schedule.material_state_ref,
                    "revision": profile_revision,
                    "day": first_date,
                },
            )
        assert first.resolved_at is not None
        assert excluded.coordinate == replace(first, resolved_at=None)
        async with runtime.session_factory() as session, session.begin():
            assert (
                await session.scalars(
                    text(
                        "SELECT source_event_ref "
                        "FROM dante.list_self_event_pending_first_sources(:actor)"
                    ),
                    {"actor": actor},
                )
            ).all() == [series.source_ref]
            assert (
                await session.scalars(
                    text(
                        "SELECT source_event_ref "
                        "FROM dante.list_self_event_pending_first_sources(:actor)"
                    ),
                    {"actor": stranger},
                )
            ).all() == []
        async with runtime.session_factory() as session, session.begin():
            assert (
                await session.scalar(
                    text("SELECT dante.repair_self_event_legacy_first(:actor,:source)"),
                    {"actor": stranger, "source": series.source_ref},
                )
                is None
            )

        checkpoint = RoutineOccurrenceMaterializationApplication(runtime.session_factory)
        await checkpoint.checkpoint_window(
            self_person_ref=actor,
            operation_id="legacy-first-event:checkpoint",
            start_date=first_date,
            end_date_exclusive=date(2099, 1, 7),
            effective_zone_id="Europe/Rome",
        )
        async with runtime.session_factory() as session, session.begin():
            linked_ref = await session.scalar(
                text(
                    "SELECT first_occurrence_ref "
                    "FROM dante.get_self_event_recurring_first_by_source(:actor,:source)"
                ),
                {"actor": actor, "source": series.source_ref},
            )
            assert linked_ref is not None
            assert (
                await session.scalar(
                    text("SELECT dante.get_self_occurrence_edit_protection(:actor,:first)"),
                    {"actor": actor, "first": linked_ref},
                )
                is None
            )
        timeline = await TemporalTimelineApplication(runtime.session_factory).read_window(
            query=TimelineWindowQuery(
                start_date=first_date,
                end_date_exclusive=date(2099, 1, 7),
            ),
            context=_context(actor),
        )
        async with runtime.session_factory() as session, session.begin():
            assert (
                await session.scalars(
                    text(
                        "SELECT source_event_ref "
                        "FROM dante.list_self_event_pending_first_sources(:actor)"
                    ),
                    {"actor": actor},
                )
            ).all() == []
        assert (
            len(
                [
                    item
                    for item in timeline.items
                    if isinstance(item, TimelineNamedZoneLocalEventItem)
                    and item.event_ref == event_ref
                ]
            )
            == 1
        )
        assert (
            len(
                [
                    item
                    for item in timeline.items
                    if isinstance(item, TimelineScheduledOccurrenceItem)
                    and item.source_native_ref == series.source_ref
                ]
            )
            == 1
        )

        await checkpoint.checkpoint_window(
            self_person_ref=actor,
            operation_id="legacy-first-event:checkpoint-again",
            start_date=first_date,
            end_date_exclusive=date(2099, 1, 7),
            effective_zone_id="Europe/Rome",
        )
        async with runtime.session_factory() as session, session.begin():
            assert (
                await session.scalar(
                    text(
                        "SELECT first_occurrence_ref "
                        "FROM dante.get_self_event_recurring_first_by_source(:actor,:source)"
                    ),
                    {"actor": actor, "source": series.source_ref},
                )
                == linked_ref
            )
    finally:
        await runtime.dispose()
