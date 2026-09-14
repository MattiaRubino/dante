"""B02-B/B02-C/B02-D Schedule mutation API proofs."""

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
    ReviseFloatingScheduleRequest,
    UndoScheduleUnscheduleRequest,
    UnscheduleScheduleRequest,
    establish_activity_schedule,
    revise_schedule_placement,
    undo_schedule_unschedule,
    unschedule_schedule,
)
from dante.modules.temporal.schedule import (
    EstablishedScheduleView,
    FloatingLocalIntervalPlacement,
    RestoredScheduleView,
    RevisedScheduleView,
    ScheduleInputError,
    ScheduleNotFoundError,
    ScheduleOperationIdReuseError,
    SchedulePersistenceError,
    ScheduleRevisionConflictError,
    ScheduleUndoConflictError,
    ScheduleUnscheduleConflictError,
    TemporalScheduleApplication,
    UnscheduledScheduleView,
)
from dante.platform.database.references import (
    MaterialStateRef,
    NativeRef,
    ScopedRecordRef,
)
from dante.platform.http.problem import ProblemError
from dante.platform.time import TimeZoneMode, TimeZonePolicy

_ACTIVITY_REF = NativeRef(UUID("0199a8c0-5e71-7bc0-8ad0-a2f403f5617d"))
_SCHEDULE_REF = ScopedRecordRef(UUID("0199a8c0-6e72-7cd1-9be1-b3f51406728e"))
_STATE_REF = MaterialStateRef(UUID("0199a8c0-7e73-7de2-8cf2-c4062517839f"))
_NEXT_STATE_REF = MaterialStateRef(UUID("0199a8c0-8e74-7ef3-9d03-d517362894a0"))
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


def _revision_result(*, replayed: bool = False) -> RevisedScheduleView:
    return RevisedScheduleView(
        schedule_ref=_SCHEDULE_REF,
        previous_material_state_ref=_STATE_REF,
        material_state_ref=_NEXT_STATE_REF,
        placement=FloatingLocalIntervalPlacement(
            starts_local_at=_START.replace(hour=16),
            ends_local_at=_END.replace(hour=17),
        ),
        created_at=_CREATED_AT,
        replayed=replayed,
    )


class _StaticScheduleApplication:
    def __init__(
        self,
        outcome: (RevisedScheduleView | UnscheduledScheduleView | RestoredScheduleView | Exception),
    ) -> None:
        self.outcome = outcome
        self.calls: list[dict[str, object]] = []

    def _result(self, expected: type[object]) -> object:
        if isinstance(self.outcome, Exception):
            raise self.outcome
        assert isinstance(self.outcome, expected)
        return self.outcome

    async def revise_floating_schedule(self, **kwargs: object) -> RevisedScheduleView:
        self.calls.append(kwargs)
        return cast(RevisedScheduleView, self._result(RevisedScheduleView))

    async def unschedule(self, **kwargs: object) -> UnscheduledScheduleView:
        self.calls.append(kwargs)
        return cast(UnscheduledScheduleView, self._result(UnscheduledScheduleView))

    async def undo_unschedule(self, **kwargs: object) -> RestoredScheduleView:
        self.calls.append(kwargs)
        return cast(RestoredScheduleView, self._result(RestoredScheduleView))


def _schedule_application(
    value: _StaticScheduleApplication,
) -> TemporalScheduleApplication:
    return cast(TemporalScheduleApplication, value)


def _revision_payload() -> ReviseFloatingScheduleRequest:
    return ReviseFloatingScheduleRequest(
        operation_id="operation:b02-c:revise",
        expected_placement_material_state_ref=UUID(str(_STATE_REF)),
        placement=FloatingLocalIntervalPlacementRequest(
            starts_local_at=_START.replace(hour=16),
            ends_local_at=_END.replace(hour=17),
        ),
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("replayed", [False, True])
async def test_schedule_revision_api_preserves_schedule_and_expected_state_basis(
    replayed: bool,
) -> None:
    application = _StaticScheduleApplication(_revision_result(replayed=replayed))
    response = Response()

    result = await revise_schedule_placement(
        schedule_ref=UUID(str(_SCHEDULE_REF)),
        payload=_revision_payload(),
        context=_context(),
        application=_schedule_application(application),
        response=response,
    )

    assert response.headers["Cache-Control"] == "no-store"
    assert result.model_dump(mode="json") == {
        "schedule_ref": str(_SCHEDULE_REF),
        "previous_placement_material_state_ref": str(_STATE_REF),
        "placement_material_state_ref": str(_NEXT_STATE_REF),
        "temporal_form": "floating_local",
        "starts_local_at": "2026-09-09T16:15:00",
        "ends_local_at": "2026-09-09T17:00:00",
        "replayed": replayed,
    }
    assert application.calls == [
        {
            "self_person_ref": _SELF_REF,
            "operation_id": "operation:b02-c:revise",
            "schedule_ref": _SCHEDULE_REF,
            "expected_material_state_ref": _STATE_REF,
            "placement": FloatingLocalIntervalPlacement(
                starts_local_at=_START.replace(hour=16),
                ends_local_at=_END.replace(hour=17),
            ),
        }
    ]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("failure", "status", "code"),
    [
        (ScheduleNotFoundError(), 404, "temporal.schedule.not_found"),
        (
            ScheduleOperationIdReuseError(),
            409,
            "temporal.schedule.operation_id_reused",
        ),
        (
            ScheduleRevisionConflictError(),
            409,
            "temporal.schedule.revision_conflict",
        ),
        (
            ScheduleInputError("invalid revision"),
            422,
            "temporal.schedule.invalid_revision",
        ),
        (
            SchedulePersistenceError(),
            503,
            "temporal.schedule.persistence_unavailable",
        ),
    ],
)
async def test_schedule_revision_api_maps_public_failures(
    failure: Exception,
    status: int,
    code: str,
) -> None:
    with pytest.raises(ProblemError) as error:
        await revise_schedule_placement(
            schedule_ref=UUID(str(_SCHEDULE_REF)),
            payload=_revision_payload(),
            context=_context(),
            application=_schedule_application(_StaticScheduleApplication(failure)),
            response=Response(),
        )

    assert error.value.status == status
    assert error.value.code == code


def _unscheduled_result(*, replayed: bool = False) -> UnscheduledScheduleView:
    return UnscheduledScheduleView(
        schedule_ref=_SCHEDULE_REF,
        previous_material_state_ref=_STATE_REF,
        unschedule_operation_id="operation:b02-d:unschedule",
        created_at=_CREATED_AT,
        replayed=replayed,
    )


def _restored_result(*, replayed: bool = False) -> RestoredScheduleView:
    return RestoredScheduleView(
        schedule_ref=_SCHEDULE_REF,
        restored_from_material_state_ref=_STATE_REF,
        material_state_ref=_NEXT_STATE_REF,
        placement=FloatingLocalIntervalPlacement(
            starts_local_at=_START,
            ends_local_at=_END,
        ),
        created_at=_CREATED_AT,
        replayed=replayed,
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("replayed", [False, True])
async def test_schedule_unschedule_api_preserves_exact_current_basis(
    replayed: bool,
) -> None:
    application = _StaticScheduleApplication(_unscheduled_result(replayed=replayed))
    response = Response()

    result = await unschedule_schedule(
        schedule_ref=UUID(str(_SCHEDULE_REF)),
        payload=UnscheduleScheduleRequest(
            operation_id="operation:b02-d:unschedule",
            expected_placement_material_state_ref=UUID(str(_STATE_REF)),
        ),
        context=_context(),
        application=_schedule_application(application),
        response=response,
    )

    assert response.headers["Cache-Control"] == "no-store"
    assert result.model_dump(mode="json") == {
        "schedule_ref": str(_SCHEDULE_REF),
        "previous_placement_material_state_ref": str(_STATE_REF),
        "unschedule_operation_id": "operation:b02-d:unschedule",
        "replayed": replayed,
    }
    assert application.calls == [
        {
            "self_person_ref": _SELF_REF,
            "operation_id": "operation:b02-d:unschedule",
            "schedule_ref": _SCHEDULE_REF,
            "expected_material_state_ref": _STATE_REF,
        }
    ]


@pytest.mark.asyncio
@pytest.mark.parametrize("replayed", [False, True])
async def test_schedule_unschedule_undo_api_returns_new_monotonic_state(
    replayed: bool,
) -> None:
    application = _StaticScheduleApplication(_restored_result(replayed=replayed))
    response = Response()

    result = await undo_schedule_unschedule(
        schedule_ref=UUID(str(_SCHEDULE_REF)),
        payload=UndoScheduleUnscheduleRequest(
            operation_id="operation:b02-d:undo",
            unschedule_operation_id="operation:b02-d:unschedule",
        ),
        context=_context(),
        application=_schedule_application(application),
        response=response,
    )

    assert response.headers["Cache-Control"] == "no-store"
    assert result.model_dump(mode="json") == {
        "schedule_ref": str(_SCHEDULE_REF),
        "restored_from_placement_material_state_ref": str(_STATE_REF),
        "placement_material_state_ref": str(_NEXT_STATE_REF),
        "temporal_form": "floating_local",
        "starts_local_at": _START.isoformat(),
        "ends_local_at": _END.isoformat(),
        "replayed": replayed,
    }


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("endpoint", "failure", "status", "code"),
    [
        ("unschedule", ScheduleNotFoundError(), 404, "temporal.schedule.not_found"),
        (
            "unschedule",
            ScheduleOperationIdReuseError(),
            409,
            "temporal.schedule.operation_id_reused",
        ),
        (
            "unschedule",
            ScheduleUnscheduleConflictError(),
            409,
            "temporal.schedule.unschedule_conflict",
        ),
        (
            "unschedule",
            ScheduleInputError("invalid unschedule"),
            422,
            "temporal.schedule.invalid_unschedule",
        ),
        (
            "unschedule",
            SchedulePersistenceError(),
            503,
            "temporal.schedule.persistence_unavailable",
        ),
        (
            "undo",
            ScheduleNotFoundError(),
            404,
            "temporal.schedule.undo_not_found",
        ),
        (
            "undo",
            ScheduleOperationIdReuseError(),
            409,
            "temporal.schedule.operation_id_reused",
        ),
        (
            "undo",
            ScheduleUndoConflictError(),
            409,
            "temporal.schedule.undo_conflict",
        ),
        (
            "undo",
            ScheduleInputError("invalid Undo"),
            422,
            "temporal.schedule.invalid_undo",
        ),
        (
            "undo",
            SchedulePersistenceError(),
            503,
            "temporal.schedule.persistence_unavailable",
        ),
    ],
)
async def test_schedule_unschedule_and_undo_map_public_failures(
    endpoint: str,
    failure: Exception,
    status: int,
    code: str,
) -> None:
    application = _schedule_application(_StaticScheduleApplication(failure))
    if endpoint == "unschedule":
        request = unschedule_schedule(
            schedule_ref=UUID(str(_SCHEDULE_REF)),
            payload=UnscheduleScheduleRequest(
                operation_id="operation:b02-d:unschedule",
                expected_placement_material_state_ref=UUID(str(_STATE_REF)),
            ),
            context=_context(),
            application=application,
            response=Response(),
        )
    else:
        request = undo_schedule_unschedule(
            schedule_ref=UUID(str(_SCHEDULE_REF)),
            payload=UndoScheduleUnscheduleRequest(
                operation_id="operation:b02-d:undo",
                unschedule_operation_id="operation:b02-d:unschedule",
            ),
            context=_context(),
            application=application,
            response=Response(),
        )

    with pytest.raises(ProblemError) as error:
        await request

    assert error.value.status == status
    assert error.value.code == code
