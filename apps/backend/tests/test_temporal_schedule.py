"""B02-B existing Activity Schedule application/API contract proof."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import cast
from uuid import UUID

import pytest
from fastapi import Response

from dante.auth.contracts import Principal
from dante.context.contracts import DanteContext
from dante.modules.temporal.activity import (
    ActivityInputError,
    ActivityNotFoundError,
    ActivityOperationIdReuseError,
    ActivityPersistenceError,
    ActivityView,
    CreateScheduledActivityResult,
    TemporalActivityApplication,
)
from dante.modules.temporal.api import (
    EstablishActivityScheduleRequest,
    FloatingLocalIntervalPlacementRequest,
    establish_activity_schedule,
)
from dante.modules.temporal.schedule import (
    EstablishedScheduleView,
    FloatingLocalIntervalPlacement,
)
from dante.platform.database.references import MaterialStateRef, NativeRef, ScopedRecordRef
from dante.platform.http.problem import ProblemError
from dante.platform.time import TimeZoneMode, TimeZonePolicy

_ACTIVITY_REF = NativeRef(UUID("0199a8c0-5e71-7bc0-8ad0-a2f403f5617d"))
_SCHEDULE_REF = ScopedRecordRef(UUID("0199a8c0-6e72-7cd1-9be1-b3f51406728e"))
_STATE_REF = MaterialStateRef(UUID("0199a8c0-7e73-7de2-8cf2-c4062517839f"))
_SELF_REF = NativeRef(UUID("0199a8c0-4e70-7abf-89c0-91e3f2e4506c"))
_CREATED_AT = datetime(2026, 9, 8, 8, 0, tzinfo=UTC)
_START = datetime(2026, 9, 9, 14, 15)  # noqa: DTZ001
_END = datetime(2026, 9, 9, 15, 0)  # noqa: DTZ001


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


def _result(*, replayed: bool = False) -> CreateScheduledActivityResult:
    placement = FloatingLocalIntervalPlacement(
        starts_local_at=_START,
        ends_local_at=_END,
    )
    return CreateScheduledActivityResult(
        activity=ActivityView(
            activity_ref=_ACTIVITY_REF,
            title="Activity esistente",
            created_at=_CREATED_AT,
        ),
        schedule=EstablishedScheduleView(
            subject_native_ref=_ACTIVITY_REF,
            schedule_ref=_SCHEDULE_REF,
            material_state_ref=_STATE_REF,
            placement=placement,
            created_at=_CREATED_AT,
            replayed=replayed,
        ),
        replayed=replayed,
    )


class _StaticActivityApplication:
    def __init__(
        self,
        outcome: CreateScheduledActivityResult | Exception,
    ) -> None:
        self.outcome = outcome
        self.calls: list[dict[str, object]] = []

    async def schedule_existing_activity(self, **kwargs: object) -> CreateScheduledActivityResult:
        self.calls.append(kwargs)
        if isinstance(self.outcome, Exception):
            raise self.outcome
        return self.outcome


def _application(value: _StaticActivityApplication) -> TemporalActivityApplication:
    return cast(TemporalActivityApplication, value)


def _payload() -> EstablishActivityScheduleRequest:
    return EstablishActivityScheduleRequest(
        operation_id="operation:b02-b:place",
        placement=FloatingLocalIntervalPlacementRequest(
            starts_local_at=_START,
            ends_local_at=_END,
        ),
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(("replayed", "expected_status"), [(False, 201), (True, 200)])
async def test_existing_activity_schedule_api_preserves_identity_and_replay_status(
    replayed: bool,
    expected_status: int,
) -> None:
    application = _StaticActivityApplication(_result(replayed=replayed))
    response = Response(status_code=201)

    result = await establish_activity_schedule(
        activity_ref=UUID(str(_ACTIVITY_REF)),
        payload=_payload(),
        context=_context(),
        application=_application(application),
        response=response,
    )

    assert response.status_code == expected_status
    assert response.headers["Cache-Control"] == "no-store"
    assert result.model_dump(mode="json") == {
        "activity_ref": str(_ACTIVITY_REF),
        "title": "Activity esistente",
        "created_at": "2026-09-08T08:00:00Z",
        "schedule_ref": str(_SCHEDULE_REF),
        "placement_material_state_ref": str(_STATE_REF),
        "temporal_form": "floating_local",
        "starts_local_at": "2026-09-09T14:15:00",
        "ends_local_at": "2026-09-09T15:00:00",
        "replayed": replayed,
    }
    assert application.calls[0]["activity_ref"] == _ACTIVITY_REF


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("failure", "status", "code"),
    [
        (ActivityNotFoundError(), 404, "temporal.activity.not_found"),
        (
            ActivityOperationIdReuseError(),
            409,
            "temporal.schedule.operation_id_reused",
        ),
        (
            ActivityInputError("invalid placement"),
            422,
            "temporal.schedule.invalid_establish",
        ),
        (
            ActivityPersistenceError(),
            503,
            "temporal.schedule.persistence_unavailable",
        ),
    ],
)
async def test_existing_activity_schedule_api_maps_public_failures(
    failure: Exception,
    status: int,
    code: str,
) -> None:
    with pytest.raises(ProblemError) as error:
        await establish_activity_schedule(
            activity_ref=UUID(str(_ACTIVITY_REF)),
            payload=_payload(),
            context=_context(),
            application=_application(_StaticActivityApplication(failure)),
            response=Response(status_code=201),
        )

    assert error.value.status == status
    assert error.value.code == code
