"""B04-A Temporal Constraint API contract proofs."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import cast
from uuid import UUID

import pytest
from fastapi import Response

from dante.auth.contracts import Principal
from dante.context.contracts import DanteContext
from dante.modules.temporal.temporal_constraint import (
    AbsoluteEarliestStartRule,
    CreatedTemporalConstraintView,
    RevisedTemporalConstraintView,
    RetiredTemporalConstraintView,
    TemporalConstraintApplication,
    TemporalConstraintCurrentBoundaryRuleView,
    TemporalConstraintNotFoundError,
    TemporalConstraintOperationIdReuseError,
    TemporalConstraintStateConflictError,
    TemporalConstraintView,
    SessionMinimumDurationRule,
)
from dante.modules.temporal.temporal_constraint_api import (
    AbsoluteEarliestStartRuleRequest,
    CreateTemporalConstraintRequest,
    RetireTemporalConstraintRequest,
    ReviseTemporalConstraintRequest,
    SessionMinimumDurationRuleRequest,
    _rule_from_request,
    _rule_request,
    create_temporal_constraint,
    get_temporal_constraint,
    list_temporal_constraints_by_subject,
    retire_temporal_constraint,
    revise_temporal_constraint_rule,
)
from dante.platform.database.references import MaterialStateRef, NativeRef, ScopedRecordRef
from dante.platform.http.problem import ProblemError
from dante.platform.time import TimeZoneMode, TimeZonePolicy

_SELF_REF = NativeRef(UUID("0199a8c0-4e70-7abf-89c0-91e3f2e4506c"))
_SUBJECT_REF = NativeRef(UUID("0199a8c0-5e71-7bc0-8ad0-a2f403f5617d"))
_CONSTRAINT_REF = ScopedRecordRef(UUID("0199a8c0-6e72-7cd1-9be1-b3f51406728e"))
_STATE_REF = MaterialStateRef(UUID("0199a8c0-7e73-7de2-8cf2-c4062517839f"))
_NEXT_STATE_REF = MaterialStateRef(UUID("0199a8c0-8e74-7ef3-9d03-d517362894a0"))
_RECORDED_AT = datetime(2026, 9, 18, 16, 0, tzinfo=UTC)
_BOUNDARY_AT = datetime(2026, 9, 24, 8, 0, tzinfo=UTC)


def test_session_duration_rule_api_round_trip_keeps_the_bounded_semantics() -> None:
    payload = SessionMinimumDurationRuleRequest(
        duration_microseconds=2_700_000_000,
    )
    rule = _rule_from_request(payload)
    assert rule == SessionMinimumDurationRule(duration_microseconds=2_700_000_000)
    serialized = _rule_request(rule)
    assert serialized.model_dump() == payload.model_dump()


def _context() -> DanteContext:
    return DanteContext(
        principal=Principal(
            account_ref=UUID("00000000-0000-4000-8000-000000000001"),
            auth_session_ref=UUID("00000000-0000-4000-8000-000000000002"),
            authenticated_at=_RECORDED_AT,
            recent_auth_at=_RECORDED_AT,
        ),
        self_person_ref=_SELF_REF,
        timezone_policy=TimeZonePolicy(mode=TimeZoneMode.FOLLOW_DEVICE),
        effective_zone_id="Europe/Rome",
    )


def _rule() -> AbsoluteEarliestStartRule:
    return AbsoluteEarliestStartRule(strength="hard", boundary_at=_BOUNDARY_AT)


def _rule_request() -> AbsoluteEarliestStartRuleRequest:
    return AbsoluteEarliestStartRuleRequest(
        strength="hard",
        boundary_at=_BOUNDARY_AT,
    )


class _StaticConstraintApplication:
    def __init__(self, outcome: object) -> None:
        self.outcome = outcome
        self.calls: list[tuple[str, dict[str, object]]] = []

    def _value(self) -> object:
        if isinstance(self.outcome, Exception):
            raise self.outcome
        return self.outcome

    async def create_constraint(self, **kwargs: object) -> CreatedTemporalConstraintView:
        self.calls.append(("create", kwargs))
        return cast(CreatedTemporalConstraintView, self._value())

    async def revise_constraint(self, **kwargs: object) -> RevisedTemporalConstraintView:
        self.calls.append(("revise", kwargs))
        return cast(RevisedTemporalConstraintView, self._value())

    async def retire_constraint(self, **kwargs: object) -> RetiredTemporalConstraintView:
        self.calls.append(("retire", kwargs))
        return cast(RetiredTemporalConstraintView, self._value())

    async def get_constraint(self, **kwargs: object) -> TemporalConstraintView:
        self.calls.append(("get", kwargs))
        return cast(TemporalConstraintView, self._value())

    async def list_constraints_by_subject(self, **kwargs: object) -> list[TemporalConstraintView]:
        self.calls.append(("list", kwargs))
        return cast(list[TemporalConstraintView], self._value())


def _application(value: _StaticConstraintApplication) -> TemporalConstraintApplication:
    return cast(TemporalConstraintApplication, value)


@pytest.mark.asyncio
@pytest.mark.parametrize(("replayed", "status"), [(False, 201), (True, 200)])
async def test_constraint_create_api_preserves_typed_rule_and_replay_status(
    replayed: bool,
    status: int,
) -> None:
    application = _StaticConstraintApplication(
        CreatedTemporalConstraintView(
            constraint_ref=_CONSTRAINT_REF,
            subject_native_ref=_SUBJECT_REF,
            subject_kind="activity",
            material_state_ref=_STATE_REF,
            rule=_rule(),
            recorded_at=_RECORDED_AT,
            replayed=replayed,
        )
    )
    response = Response(status_code=201)

    result = await create_temporal_constraint(
        payload=CreateTemporalConstraintRequest(
            operation_id="operation:b04-a5:create",
            subject_ref=UUID(str(_SUBJECT_REF)),
            rule=_rule_request(),
        ),
        context=_context(),
        application=_application(application),
        response=response,
    )

    assert response.status_code == status
    assert response.headers["Cache-Control"] == "no-store"
    assert result.model_dump(mode="json") == {
        "constraint_ref": str(_CONSTRAINT_REF),
        "subject_ref": str(_SUBJECT_REF),
        "subject_kind": "activity",
        "material_state_ref": str(_STATE_REF),
        "rule": {
            "family": "boundary",
            "boundary_kind": "earliest_start",
            "constrained_facet": "schedule.start",
            "strength": "hard",
            "temporal_form": "absolute",
            "boundary_at": "2026-09-24T08:00:00Z",
        },
        "recorded_at": "2026-09-18T16:00:00Z",
        "replayed": replayed,
    }
    assert application.calls[0][1]["subject_native_ref"] == _SUBJECT_REF


@pytest.mark.asyncio
async def test_constraint_revision_and_retirement_api_preserve_cas_basis() -> None:
    revised_application = _StaticConstraintApplication(
        RevisedTemporalConstraintView(
            constraint_ref=_CONSTRAINT_REF,
            subject_native_ref=_SUBJECT_REF,
            subject_kind="activity",
            previous_material_state_ref=_STATE_REF,
            material_state_ref=_NEXT_STATE_REF,
            rule=_rule(),
            recorded_at=_RECORDED_AT,
            replayed=False,
        )
    )
    revised = await revise_temporal_constraint_rule(
        constraint_ref=UUID(str(_CONSTRAINT_REF)),
        payload=ReviseTemporalConstraintRequest(
            operation_id="operation:b04-a5:revise",
            expected_material_state_ref=UUID(str(_STATE_REF)),
            rule=_rule_request(),
        ),
        context=_context(),
        application=_application(revised_application),
        response=Response(),
    )
    assert revised.previous_material_state_ref == UUID(str(_STATE_REF))
    assert revised.material_state_ref == UUID(str(_NEXT_STATE_REF))
    assert revised_application.calls[0][1]["expected_material_state_ref"] == _STATE_REF

    retired_application = _StaticConstraintApplication(
        RetiredTemporalConstraintView(
            constraint_ref=_CONSTRAINT_REF,
            subject_native_ref=_SUBJECT_REF,
            subject_kind="activity",
            previous_material_state_ref=_NEXT_STATE_REF,
            recorded_at=_RECORDED_AT,
            replayed=False,
        )
    )
    retired = await retire_temporal_constraint(
        constraint_ref=UUID(str(_CONSTRAINT_REF)),
        payload=RetireTemporalConstraintRequest(
            operation_id="operation:b04-a5:retire",
            expected_material_state_ref=UUID(str(_NEXT_STATE_REF)),
        ),
        context=_context(),
        application=_application(retired_application),
        response=Response(),
    )
    assert retired.previous_material_state_ref == UUID(str(_NEXT_STATE_REF))
    assert retired_application.calls[0][1]["expected_material_state_ref"] == _NEXT_STATE_REF


@pytest.mark.asyncio
async def test_constraint_get_and_list_make_active_vs_retired_explicit() -> None:
    active = TemporalConstraintView(
        constraint_ref=_CONSTRAINT_REF,
        subject_native_ref=_SUBJECT_REF,
        subject_kind="event",
        status="active",
        current_rule=TemporalConstraintCurrentBoundaryRuleView(
            material_state_ref=_STATE_REF,
            family="boundary",
            boundary_kind="earliest_start",
            constrained_facet="schedule.start",
            strength="soft",
            temporal_form="absolute",
            boundary_at=_BOUNDARY_AT,
        ),
    )
    active_response = await get_temporal_constraint(
        constraint_ref=UUID(str(_CONSTRAINT_REF)),
        context=_context(),
        application=_application(_StaticConstraintApplication(active)),
        response=Response(),
    )
    assert active_response.status == "active"
    assert active_response.current_rule is not None
    assert active_response.current_rule.strength == "soft"

    retired = TemporalConstraintView(
        constraint_ref=_CONSTRAINT_REF,
        subject_native_ref=_SUBJECT_REF,
        subject_kind="event",
        status="retired",
        current_rule=None,
    )
    listed = await list_temporal_constraints_by_subject(
        context=_context(),
        application=_application(_StaticConstraintApplication([active, retired])),
        response=Response(),
        subject_ref=UUID(str(_SUBJECT_REF)),
    )
    assert [item.status for item in listed.items] == ["active", "retired"]
    assert listed.items[1].current_rule is None


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("failure", "code"),
    [
        (TemporalConstraintNotFoundError(), "temporal.constraint.not_found"),
        (
            TemporalConstraintOperationIdReuseError(),
            "temporal.constraint.operation_id_reused",
        ),
        (TemporalConstraintStateConflictError(), "temporal.constraint.state_conflict"),
    ],
)
async def test_constraint_revision_api_maps_public_conflicts(
    failure: Exception,
    code: str,
) -> None:
    with pytest.raises(ProblemError) as error:
        await revise_temporal_constraint_rule(
            constraint_ref=UUID(str(_CONSTRAINT_REF)),
            payload=ReviseTemporalConstraintRequest(
                operation_id="operation:b04-a5:revise",
                expected_material_state_ref=UUID(str(_STATE_REF)),
                rule=_rule_request(),
            ),
            context=_context(),
            application=_application(_StaticConstraintApplication(failure)),
            response=Response(),
        )
    assert error.value.code == code
    assert error.value.status in {404, 409}
