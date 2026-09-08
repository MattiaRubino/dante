"""B00 temporal Timeline application/API contract proof."""

from __future__ import annotations

from datetime import UTC, date, datetime, timedelta
from uuid import UUID

import pytest
from fastapi import Response

from dante.auth.contracts import Principal
from dante.context.contracts import DanteContext
from dante.modules.temporal.api import get_timeline_window
from dante.modules.temporal.application import TemporalTimelineApplication
from dante.modules.temporal.contracts import (
    MAX_TIMELINE_WINDOW_DAYS,
    TimelineWindowQuery,
    TimelineWindowValidationError,
)
from dante.platform.database.references import NativeRef
from dante.platform.http.problem import ProblemError
from dante.platform.time import TimeZoneMode, TimeZonePolicy

_ACCOUNT_REF = UUID("00000000-0000-4000-8000-000000000001")
_SESSION_REF = UUID("00000000-0000-4000-8000-000000000002")
_SELF_PERSON_REF = NativeRef(UUID("0194f7c2-7b6a-7abc-8def-0123456789ab"))


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


def test_application_binds_empty_window_to_authenticated_self_and_effective_zone() -> None:
    query = TimelineWindowQuery(
        start_date=date(2026, 10, 24),
        end_date_exclusive=date(2026, 10, 27),
    )
    context = _context(effective_zone_id="Europe/Rome")

    result = TemporalTimelineApplication().read_window(query=query, context=context)

    assert result.start_date == query.start_date
    assert result.end_date_exclusive == query.end_date_exclusive
    assert result.self_person_ref == _SELF_PERSON_REF
    assert result.effective_zone_id == "Europe/Rome"


@pytest.mark.asyncio
async def test_api_returns_truthful_empty_window_without_exposing_internal_owner_ref() -> None:
    response = Response()
    result = await get_timeline_window(
        _context(),
        response,
        date(2026, 9, 7),
        date(2026, 9, 14),
    )

    assert result.model_dump(mode="json") == {
        "kind": "empty",
        "start_date": "2026-09-07",
        "end_date_exclusive": "2026-09-14",
        "effective_zone_id": "Europe/Rome",
    }
    assert response.headers["Cache-Control"] == "no-store"


@pytest.mark.asyncio
async def test_api_maps_invalid_window_to_public_validation_problem() -> None:
    with pytest.raises(ProblemError) as error:
        await get_timeline_window(
            _context(),
            Response(),
            date(2026, 9, 7),
            date(2026, 9, 7),
        )

    assert error.value.status == 400
    assert error.value.code == "temporal.invalid_timeline_window"
    assert error.value.category == "validation"
    assert error.value.retryable is False
