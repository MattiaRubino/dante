"""Offline B06-D transport proof for Occurrence Schedule establishment."""

from __future__ import annotations

from datetime import UTC, date, datetime
from typing import cast
from uuid import UUID

import pytest
from fastapi import Response

from dante.auth.contracts import Principal
from dante.context.contracts import DanteContext
from dante.modules.temporal.api import DateSpanPlacementRequest
from dante.modules.temporal.occurrence import (
    OccurrenceApplication,
    OccurrenceWindowCheckpoint,
)
from dante.modules.temporal.occurrence_api import (
    EstablishOccurrenceScheduleRequest,
    OccurrenceWindowCheckpointRequest,
    checkpoint_occurrence_window,
    establish_occurrence_schedule,
)
from dante.modules.temporal.schedule import (
    DateSpanPlacement,
    EstablishedScheduleView,
    ScheduleInputError,
    ScheduleNotFoundError,
    ScheduleOperationIdReuseError,
    SchedulePersistenceError,
    TemporalScheduleApplication,
)
from dante.platform.database.references import MaterialStateRef, NativeRef, ScopedRecordRef
from dante.platform.http.problem import ProblemError
from dante.platform.time import TimeZoneMode, TimeZonePolicy

_OCCURRENCE_REF = NativeRef(UUID("0199a8c0-9e75-7af4-8e14-e6284737a5b1"))
_SCHEDULE_REF = ScopedRecordRef(UUID("0199a8c0-ae76-7bf5-9f25-f7395848b6c2"))
_STATE_REF = MaterialStateRef(UUID("0199a8c0-be77-7cf6-8036-a84a6959c7d3"))
_SELF_REF = NativeRef(UUID("0199a8c0-4e70-7abf-89c0-91e3f2e4506c"))
_CREATED_AT = datetime(2026, 9, 22, 8, 0, tzinfo=UTC)


def _context() -> DanteContext:
    return DanteContext(
        principal=Principal(
            account_ref=UUID("00000000-0000-4000-8000-000000000001"),
            auth_session_ref=UUID("00000000-0000-4000-8000-000000000002"),
            authenticated_at=_CREATED_AT,
            recent_auth_at=_CREATED_AT,
        ),
        self_person_ref=_SELF_REF,
        timezone_policy=TimeZonePolicy(mode=TimeZoneMode.FOLLOW_DEVICE),
        effective_zone_id="Europe/Rome",
    )


def _payload() -> EstablishOccurrenceScheduleRequest:
    return EstablishOccurrenceScheduleRequest(
        operation_id="b06-d:occurrence:schedule",
        placement=DateSpanPlacementRequest(
            start_date=date(2026, 10, 1),
            end_date_exclusive=date(2026, 10, 2),
        ),
    )


class _StaticApplication:
    def __init__(self, outcome: EstablishedScheduleView | Exception) -> None:
        self.outcome = outcome
        self.calls: list[dict[str, object]] = []

    async def establish_schedule(self, **kwargs: object) -> EstablishedScheduleView:
        self.calls.append(kwargs)
        if isinstance(self.outcome, Exception):
            raise self.outcome
        return self.outcome


class _StaticOccurrenceApplication:
    def __init__(self, outcome: OccurrenceWindowCheckpoint) -> None:
        self.outcome = outcome
        self.calls: list[dict[str, object]] = []

    async def checkpoint_window(self, **kwargs: object) -> OccurrenceWindowCheckpoint:
        self.calls.append(kwargs)
        return self.outcome


def _application(value: _StaticApplication) -> TemporalScheduleApplication:
    return cast(TemporalScheduleApplication, value)


def _occurrence_application(value: _StaticOccurrenceApplication) -> OccurrenceApplication:
    return cast(OccurrenceApplication, value)


def _result(*, replayed: bool) -> EstablishedScheduleView:
    return EstablishedScheduleView(
        subject_native_ref=_OCCURRENCE_REF,
        schedule_ref=_SCHEDULE_REF,
        material_state_ref=_STATE_REF,
        placement=DateSpanPlacement(
            start_date=date(2026, 10, 1),
            end_date_exclusive=date(2026, 10, 2),
        ),
        created_at=_CREATED_AT,
        replayed=replayed,
    )


@pytest.mark.asyncio
async def test_occurrence_window_checkpoint_uses_context_zone_and_preserves_counts() -> None:
    application = _StaticOccurrenceApplication(
        OccurrenceWindowCheckpoint(
            start_date=date(2026, 10, 1),
            end_date_exclusive=date(2026, 10, 8),
            effective_zone_id="Europe/Rome",
            source_count=2,
            occurrence_count=7,
            replayed_source_count=1,
        )
    )
    response = Response()

    result = await checkpoint_occurrence_window(
        payload=OccurrenceWindowCheckpointRequest(
            operation_id="b06-d:timeline-window",
            start_date=date(2026, 10, 1),
            end_date_exclusive=date(2026, 10, 8),
        ),
        context=_context(),
        application=_occurrence_application(application),
        response=response,
    )

    assert response.headers["Cache-Control"] == "no-store"
    assert result.model_dump(mode="json") == {
        "start_date": "2026-10-01",
        "end_date_exclusive": "2026-10-08",
        "effective_zone_id": "Europe/Rome",
        "source_count": 2,
        "occurrence_count": 7,
        "replayed_source_count": 1,
    }
    assert application.calls == [
        {
            "self_person_ref": _SELF_REF,
            "operation_id": "b06-d:timeline-window",
            "start_date": date(2026, 10, 1),
            "end_date_exclusive": date(2026, 10, 8),
            "effective_zone_id": "Europe/Rome",
        }
    ]


@pytest.mark.asyncio
@pytest.mark.parametrize(("replayed", "status"), [(False, 201), (True, 200)])
async def test_occurrence_schedule_response_preserves_identity_and_replay(
    replayed: bool,
    status: int,
) -> None:
    application = _StaticApplication(_result(replayed=replayed))
    response = Response(status_code=201)

    result = await establish_occurrence_schedule(
        occurrence_ref=UUID(str(_OCCURRENCE_REF)),
        payload=_payload(),
        context=_context(),
        application=_application(application),
        response=response,
    )

    assert response.status_code == status
    assert response.headers["Cache-Control"] == "no-store"
    assert result.model_dump(mode="json") == {
        "occurrence_ref": str(_OCCURRENCE_REF),
        "schedule_ref": str(_SCHEDULE_REF),
        "placement_material_state_ref": str(_STATE_REF),
        "placement": {
            "kind": "date_span",
            "start_date": "2026-10-01",
            "end_date_exclusive": "2026-10-02",
        },
        "replayed": replayed,
    }
    assert application.calls == [
        {
            "self_person_ref": _SELF_REF,
            "operation_id": "b06-d:occurrence:schedule",
            "subject_native_ref": _OCCURRENCE_REF,
            "placement": DateSpanPlacement(
                start_date=date(2026, 10, 1),
                end_date_exclusive=date(2026, 10, 2),
            ),
        }
    ]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("failure", "status", "code"),
    [
        (ScheduleInputError("invalid"), 422, "temporal.occurrence.schedule_invalid"),
        (ScheduleNotFoundError(), 404, "temporal.occurrence.unavailable"),
        (
            ScheduleOperationIdReuseError(),
            409,
            "temporal.occurrence.schedule_operation_id_reused",
        ),
        (
            SchedulePersistenceError(),
            503,
            "temporal.occurrence.schedule_unavailable",
        ),
    ],
)
async def test_occurrence_schedule_maps_public_failures(
    failure: Exception,
    status: int,
    code: str,
) -> None:
    with pytest.raises(ProblemError) as error:
        await establish_occurrence_schedule(
            occurrence_ref=UUID(str(_OCCURRENCE_REF)),
            payload=_payload(),
            context=_context(),
            application=_application(_StaticApplication(failure)),
            response=Response(status_code=201),
        )

    assert error.value.status == status
    assert error.value.code == code
