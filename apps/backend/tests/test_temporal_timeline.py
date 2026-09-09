"""B00/B02 temporal Timeline application/API contract proof."""

from __future__ import annotations

from datetime import UTC, date, datetime, timedelta
from typing import cast
from uuid import UUID

import pytest
from fastapi import Response

from dante.auth.contracts import Principal
from dante.context.contracts import DanteContext
from dante.modules.temporal.api import get_timeline_window
from dante.modules.temporal.application import (
    TemporalTimelineApplication,
    TimelineWindowResult,
    empty_timeline_window_result,
)
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
