"""B00/B02 temporal Timeline application/API contract proof."""

from __future__ import annotations

from datetime import UTC, date, datetime, timedelta
from typing import Any, cast
from uuid import UUID

import pytest
from fastapi import Response

from dante.auth.contracts import Principal
from dante.context.contracts import DanteContext
from dante.modules.temporal.api import (
    TimelineNamedZoneLocalActivityResponse,
    TimelineScheduledActivityResponse,
    get_timeline_window,
)
from dante.modules.temporal.application import (
    TemporalTimelineApplication,
    TimelineAbsoluteActivityItem,
    TimelineCoarseLocalPeriodActivityItem,
    TimelineDateSpanActivityItem,
    TimelineExpectedOccurrenceItem,
    TimelineFloatingLocalActivityItem,
    TimelineNamedZoneLocalActivityItem,
    TimelineScheduledOccurrenceItem,
    TimelineWindowResult,
    empty_timeline_window_result,
)
from dante.modules.temporal.contracts import (
    MAX_TIMELINE_WINDOW_DAYS,
    TimelineWindowQuery,
    TimelineWindowValidationError,
)
from dante.modules.temporal.occurrence import CalendarCoordinate, QuotaCoordinate
from dante.modules.temporal.schedule import DateSpanPlacement
from dante.platform.database.references import MaterialStateRef, NativeRef, ScopedRecordRef
from dante.platform.http.problem import ProblemError
from dante.platform.time import TimeZoneMode, TimeZonePolicy

_ACCOUNT_REF = UUID("00000000-0000-4000-8000-000000000001")
_SESSION_REF = UUID("00000000-0000-4000-8000-000000000002")
_SELF_PERSON_REF = NativeRef(UUID("0194f7c2-7b6a-7abc-8def-0123456789ab"))
_ACTIVITY_REF = NativeRef(UUID("0199a8c0-5e71-7bc0-8ad0-a2f403f5617d"))
_SCHEDULE_REF = ScopedRecordRef(UUID("0199a8c0-6e72-7cd1-9be1-b3f51406728e"))
_STATE_REF = MaterialStateRef(UUID("0199a8c0-7e73-7de2-8cf2-c4062517839f"))
_OCCURRENCE_REF = NativeRef(UUID("0199a8c0-8e74-7ef3-9df3-d517362894a0"))
_SOURCE_REF = NativeRef(UUID("0199a8c0-9e75-7f04-8ae4-e6284739a5b1"))


def _context(*, effective_zone_id: str = "Europe/Rome") -> DanteContext:
    now = datetime(2026, 9, 7, 10, 0, tzinfo=UTC)
    principal = Principal(
        account_ref=_ACCOUNT_REF,
        auth_session_ref=_SESSION_REF,
        authenticated_at=now,
        recent_auth_at=now,
    )
    return DanteContext(
        principal=principal,
        self_person_ref=_SELF_PERSON_REF,
        timezone_policy=TimeZonePolicy(mode=TimeZoneMode.FOLLOW_DEVICE),
        effective_zone_id=effective_zone_id,
    )


class _StaticTimelineApplication:
    def __init__(self, result: TimelineWindowResult) -> None:
        self._result = result

    async def read_window(
        self,
        *,
        query: TimelineWindowQuery,
        context: DanteContext,
    ) -> TimelineWindowResult:
        assert query.start_date == self._result.start_date
        assert query.end_date_exclusive == self._result.end_date_exclusive
        assert context.self_person_ref == self._result.self_person_ref
        return self._result


def _application(result: TimelineWindowResult) -> TemporalTimelineApplication:
    return cast(TemporalTimelineApplication, _StaticTimelineApplication(result))


def test_timeline_query_is_half_open_and_bounded() -> None:
    query = TimelineWindowQuery(
        start_date=date(2026, 9, 1),
        end_date_exclusive=date(2026, 9, 8),
    )

    assert (query.end_date_exclusive - query.start_date).days == 7

    with pytest.raises(TimelineWindowValidationError):
        TimelineWindowQuery(
            start_date=date(2026, 9, 1),
            end_date_exclusive=date(2026, 9, 1),
        )

    with pytest.raises(TimelineWindowValidationError):
        TimelineWindowQuery(
            start_date=date(2026, 9, 1),
            end_date_exclusive=date(2026, 9, 1) + timedelta(days=MAX_TIMELINE_WINDOW_DAYS + 1),
        )


def test_empty_projection_binds_authenticated_self_and_effective_zone() -> None:
    query = TimelineWindowQuery(
        start_date=date(2026, 10, 24),
        end_date_exclusive=date(2026, 10, 27),
    )
    context = _context(effective_zone_id="Europe/Rome")

    result = empty_timeline_window_result(query=query, context=context)

    assert result.start_date == query.start_date
    assert result.end_date_exclusive == query.end_date_exclusive
    assert result.self_person_ref == _SELF_PERSON_REF
    assert result.effective_zone_id == "Europe/Rome"
    assert result.items == ()


def test_local_wall_clock_transport_forbids_fabricated_offsets() -> None:
    floating_schema = TimelineScheduledActivityResponse.model_json_schema()
    named_schema = TimelineNamedZoneLocalActivityResponse.model_json_schema()

    for schema, field_names in (
        (floating_schema, ("starts_local_at", "ends_local_at")),
        (
            named_schema,
            (
                "starts_local_at",
                "ends_local_at",
                "display_starts_local_at",
                "display_ends_local_at",
            ),
        ),
    ):
        properties = schema["properties"]
        for field_name in field_names:
            field_schema = properties[field_name]
            assert field_schema["type"] == "string"
            assert "pattern" in field_schema
            assert "format" not in field_schema


@pytest.mark.asyncio
async def test_api_returns_truthful_empty_window_without_exposing_internal_owner_ref() -> None:
    context = _context()
    query = TimelineWindowQuery(
        start_date=date(2026, 9, 7),
        end_date_exclusive=date(2026, 9, 14),
    )
    result = empty_timeline_window_result(query=query, context=context)
    response = Response()

    api_result = await get_timeline_window(
        context=context,
        application=_application(result),
        response=response,
        start_date=query.start_date,
        end_date_exclusive=query.end_date_exclusive,
    )

    assert api_result.model_dump(mode="json") == {
        "kind": "empty",
        "start_date": "2026-09-07",
        "end_date_exclusive": "2026-09-14",
        "effective_zone_id": "Europe/Rome",
    }
    assert response.headers["Cache-Control"] == "no-store"


@pytest.mark.asyncio
async def test_api_emits_each_timeline_form_without_flattening_coarse_or_dates() -> None:
    context = _context()
    query = TimelineWindowQuery(
        start_date=date(2026, 10, 25),
        end_date_exclusive=date(2026, 10, 26),
    )
    common: dict[str, Any] = {
        "activity_ref": _ACTIVITY_REF,
        "schedule_ref": _SCHEDULE_REF,
        "placement_material_state_ref": _STATE_REF,
        "title": "Forma temporale",
    }
    result = TimelineWindowResult(
        start_date=query.start_date,
        end_date_exclusive=query.end_date_exclusive,
        effective_zone_id="Europe/Rome",
        self_person_ref=context.self_person_ref,
        items=(
            TimelineDateSpanActivityItem(
                **common,
                start_date=date(2026, 10, 25),
                end_date_exclusive=date(2026, 10, 27),
            ),
            TimelineFloatingLocalActivityItem(
                **common,
                starts_local_at=datetime(2026, 10, 25, 9, 0),  # noqa: DTZ001
                ends_local_at=datetime(2026, 10, 25, 10, 0),  # noqa: DTZ001
            ),
            TimelineNamedZoneLocalActivityItem(
                **common,
                starts_local_at=datetime(2026, 10, 25, 2, 10),  # noqa: DTZ001
                ends_local_at=datetime(2026, 10, 25, 2, 40),  # noqa: DTZ001
                zone_id="Europe/Rome",
                resolved_start_at=datetime(2026, 10, 25, 1, 10, tzinfo=UTC),
                resolved_end_at=datetime(2026, 10, 25, 1, 40, tzinfo=UTC),
                display_starts_local_at=datetime(2026, 10, 25, 2, 10),  # noqa: DTZ001
                display_ends_local_at=datetime(2026, 10, 25, 2, 40),  # noqa: DTZ001
            ),
            TimelineAbsoluteActivityItem(
                **common,
                starts_at=datetime(2026, 10, 24, 22, 30, tzinfo=UTC),
                ends_at=datetime(2026, 10, 24, 23, 30, tzinfo=UTC),
                display_starts_local_at=datetime(2026, 10, 25, 0, 30),  # noqa: DTZ001
                display_ends_local_at=datetime(2026, 10, 25, 1, 30),  # noqa: DTZ001
            ),
            TimelineCoarseLocalPeriodActivityItem(
                **common,
                local_date=date(2026, 10, 25),
                period="afternoon",
            ),
        ),
    )

    api_result = await get_timeline_window(
        context=context,
        application=_application(result),
        response=Response(),
        start_date=query.start_date,
        end_date_exclusive=query.end_date_exclusive,
    )
    payload = api_result.model_dump(mode="json")

    assert payload["kind"] == "window"
    items = payload["items"]
    assert [item["temporal_form"] for item in items] == [
        "date_span",
        "floating_local",
        "named_zone_local",
        "absolute",
        "coarse_local_period",
    ]
    assert items[0]["start_date"] == "2026-10-25"
    assert "starts_local_at" not in items[0]
    assert items[1]["starts_local_at"] == "2026-10-25T09:00:00"
    assert items[2]["resolved_start_at"] == "2026-10-25T01:10:00Z"
    assert items[2]["display_starts_local_at"] == "2026-10-25T02:10:00"
    assert items[3]["starts_at"] == "2026-10-24T22:30:00Z"
    assert items[3]["display_starts_local_at"] == "2026-10-25T00:30:00"
    assert items[4]["period"] == "afternoon"
    assert "starts_local_at" not in items[4]


@pytest.mark.asyncio
async def test_api_keeps_scheduled_and_flexible_occurrence_semantics_distinct() -> None:
    context = _context()
    query = TimelineWindowQuery(
        start_date=date(2026, 10, 25),
        end_date_exclusive=date(2026, 11, 1),
    )
    result = TimelineWindowResult(
        start_date=query.start_date,
        end_date_exclusive=query.end_date_exclusive,
        effective_zone_id=context.effective_zone_id,
        self_person_ref=context.self_person_ref,
        items=(
            TimelineScheduledOccurrenceItem(
                occurrence_ref=_OCCURRENCE_REF,
                source_kind="routine",
                source_native_ref=_SOURCE_REF,
                title="Farmaco",
                coordinate=CalendarCoordinate(
                    family_code="calendar_wall_clock",
                    generated_date=date(2026, 10, 26),
                    generated_wall_time=None,
                    clock_basis_code="floating_local",
                    zone_id=None,
                    resolved_at=None,
                ),
                schedule_ref=_SCHEDULE_REF,
                placement_material_state_ref=_STATE_REF,
                placement=DateSpanPlacement(
                    start_date=date(2026, 10, 27),
                    end_date_exclusive=date(2026, 10, 28),
                ),
            ),
            TimelineExpectedOccurrenceItem(
                occurrence_ref=NativeRef(
                    UUID("0199a8c0-ae76-7015-9bf5-f739584ab6c2")
                ),
                source_kind="event",
                source_native_ref=NativeRef(
                    UUID("0199a8c0-be77-7126-8c06-084a695bc7d3")
                ),
                title="Allenamenti",
                coordinate=QuotaCoordinate(
                    family_code="quota_per_period",
                    period_start_date=date(2026, 10, 26),
                    period_end_date_exclusive=date(2026, 11, 2),
                    frame_code="floating_local",
                    zone_id=None,
                ),
            ),
        ),
    )

    api_result = await get_timeline_window(
        context=context,
        application=_application(result),
        response=Response(),
        start_date=query.start_date,
        end_date_exclusive=query.end_date_exclusive,
    )
    items = api_result.model_dump(mode="json")["items"]

    assert items[0]["kind"] == "scheduled_occurrence"
    assert items[0]["coordinate"]["generated_date"] == "2026-10-26"
    assert items[0]["placement"] == {
        "temporal_form": "date_span",
        "start_date": "2026-10-27",
        "end_date_exclusive": "2026-10-28",
    }
    assert items[1]["kind"] == "expected_occurrence"
    assert items[1]["coordinate"]["family_code"] == "quota_per_period"
    assert "placement" not in items[1]
    assert "starts_local_at" not in items[1]


@pytest.mark.asyncio
async def test_api_maps_invalid_window_to_public_validation_problem() -> None:
    context = _context()
    placeholder = TimelineWindowResult(
        start_date=date(2026, 9, 7),
        end_date_exclusive=date(2026, 9, 8),
        effective_zone_id="Europe/Rome",
        self_person_ref=context.self_person_ref,
        items=(),
    )

    with pytest.raises(ProblemError) as error:
        await get_timeline_window(
            context=context,
            application=_application(placeholder),
            response=Response(),
            start_date=date(2026, 9, 7),
            end_date_exclusive=date(2026, 9, 7),
        )

    assert error.value.status == 400
    assert error.value.code == "temporal.invalid_timeline_window"
    assert error.value.category == "validation"
    assert error.value.retryable is False
