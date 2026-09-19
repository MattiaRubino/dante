"""B04-B Temporal Constraint typed boundary API contract proofs."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import cast
from uuid import UUID

import pytest
from fastapi import Response
from pydantic import ValidationError

from dante.auth.contracts import Principal
from dante.context.contracts import DanteContext
from dante.modules.temporal.temporal_constraint import (
    AbsoluteBoundaryRule,
    CreatedTemporalConstraintView,
    TemporalConstraintApplication,
)
from dante.modules.temporal.temporal_constraint_api import (
    AbsoluteLatestCompletionRuleRequest,
    AbsoluteLatestStartRuleRequest,
    CreateTemporalConstraintRequest,
    create_temporal_constraint,
)
from dante.platform.database.references import MaterialStateRef, NativeRef, ScopedRecordRef
from dante.platform.time import TimeZoneMode, TimeZonePolicy

_SELF_REF = NativeRef(UUID("0199b000-1111-7111-8111-111111111111"))
_SUBJECT_REF = NativeRef(UUID("0199b000-2222-7222-8222-222222222222"))
_CONSTRAINT_REF = ScopedRecordRef(UUID("0199b000-3333-7333-8333-333333333333"))
_STATE_REF = MaterialStateRef(UUID("0199b000-4444-7444-8444-444444444444"))
_RECORDED_AT = datetime(2026, 9, 19, 8, 0, tzinfo=UTC)
_DEADLINE = datetime(2026, 9, 30, 17, 0, tzinfo=UTC)


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


class _StaticApplication:
    async def create_constraint(self, **_: object) -> CreatedTemporalConstraintView:
        return CreatedTemporalConstraintView(
            constraint_ref=_CONSTRAINT_REF,
            subject_native_ref=_SUBJECT_REF,
            subject_kind="activity",
            material_state_ref=_STATE_REF,
            rule=AbsoluteBoundaryRule(
                boundary_kind="latest_completion",
                constrained_facet="schedule.completion",
                strength="hard",
                boundary_at=_DEADLINE,
            ),
            recorded_at=_RECORDED_AT,
            replayed=False,
        )


def _application() -> TemporalConstraintApplication:
    return cast(TemporalConstraintApplication, _StaticApplication())


@pytest.mark.asyncio
async def test_b04_b_create_api_preserves_latest_completion_deadline_semantics() -> None:
    response = Response(status_code=201)
    result = await create_temporal_constraint(
        payload=CreateTemporalConstraintRequest(
            operation_id="operation:b04-b:deadline-api",
            subject_ref=UUID(str(_SUBJECT_REF)),
            rule=AbsoluteLatestCompletionRuleRequest(
                strength="hard",
                boundary_at=_DEADLINE,
            ),
        ),
        context=_context(),
        application=_application(),
        response=response,
    )

    assert response.status_code == 201
    assert result.rule.boundary_kind == "latest_completion"
    assert result.rule.constrained_facet == "schedule.completion"
    assert result.rule.temporal_form == "absolute"
    assert result.rule.boundary_at == _DEADLINE


def test_b04_b_request_union_rejects_invalid_latest_start_completion_pair() -> None:
    with pytest.raises(ValidationError):
        CreateTemporalConstraintRequest.model_validate(
            {
                "operation_id": "operation:b04-b:invalid-pair",
                "subject_ref": str(_SUBJECT_REF),
                "rule": {
                    "family": "boundary",
                    "boundary_kind": "latest_start",
                    "constrained_facet": "schedule.completion",
                    "strength": "hard",
                    "temporal_form": "absolute",
                    "boundary_at": _DEADLINE.isoformat(),
                },
            }
        )


def test_b04_b_latest_start_request_carries_schedule_start_facet() -> None:
    value = AbsoluteLatestStartRuleRequest(
        strength="soft",
        boundary_at=_DEADLINE,
    )
    assert value.boundary_kind == "latest_start"
    assert value.constrained_facet == "schedule.start"
