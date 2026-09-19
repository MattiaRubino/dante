"""B04-C Temporal Constraint window and evaluation API contract proofs."""

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
    AbsoluteIntervalPlacement,
    AbsoluteWindowRule,
    CreatedTemporalConstraintView,
    TemporalConstraintApplication,
    TemporalConstraintEvaluationItem,
    TemporalConstraintEvaluationView,
)
from dante.modules.temporal.temporal_constraint_api import (
    AbsoluteIntervalPlacementRequest,
    AbsoluteStartWithinWindowRuleRequest,
    CreateTemporalConstraintRequest,
    EvaluateTemporalConstraintsRequest,
    create_temporal_constraint,
    evaluate_temporal_constraints,
)
from dante.platform.database.references import MaterialStateRef, NativeRef, ScopedRecordRef
from dante.platform.time import TimeZoneMode, TimeZonePolicy

_SELF_REF = NativeRef(UUID("0199c000-1111-7111-8111-111111111111"))
_SUBJECT_REF = NativeRef(UUID("0199c000-2222-7222-8222-222222222222"))
_CONSTRAINT_REF = ScopedRecordRef(UUID("0199c000-3333-7333-8333-333333333333"))
_STATE_REF = MaterialStateRef(UUID("0199c000-4444-7444-8444-444444444444"))
_RECORDED_AT = datetime(2026, 9, 19, 9, 0, tzinfo=UTC)
_STARTS_AT = datetime(2026, 10, 5, 9, 0, tzinfo=UTC)
_ENDS_AT = datetime(2026, 10, 5, 12, 0, tzinfo=UTC)


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
            rule=AbsoluteWindowRule(
                relationship="start_within",
                constrained_facet="schedule.start",
                strength="soft",
                starts_at=_STARTS_AT,
                ends_at=_ENDS_AT,
            ),
            recorded_at=_RECORDED_AT,
            replayed=False,
        )

    async def evaluate_constraints(self, **_: object) -> TemporalConstraintEvaluationView:
        placement = AbsoluteIntervalPlacement(
            starts_at=datetime(2026, 10, 5, 10, 0, tzinfo=UTC),
            ends_at=datetime(2026, 10, 5, 11, 0, tzinfo=UTC),
        )
        return TemporalConstraintEvaluationView(
            subject_native_ref=_SUBJECT_REF,
            placement=placement,
            status="admissible",
            hard_set_status="feasible",
            items=(
                TemporalConstraintEvaluationItem(
                    constraint_ref=_CONSTRAINT_REF,
                    material_state_ref=_STATE_REF,
                    family="window",
                    rule_code="start_within",
                    constrained_facet="schedule.start",
                    strength="soft",
                    evaluation="satisfied",
                    reason_code="schedule_start_within_window",
                ),
            ),
        )


def _application() -> TemporalConstraintApplication:
    return cast(TemporalConstraintApplication, _StaticApplication())


@pytest.mark.asyncio
async def test_b04_c_create_api_preserves_typed_window_semantics() -> None:
    response = Response(status_code=201)
    result = await create_temporal_constraint(
        payload=CreateTemporalConstraintRequest(
            operation_id="operation:b04-c:window-api",
            subject_ref=UUID(str(_SUBJECT_REF)),
            rule=AbsoluteStartWithinWindowRuleRequest(
                strength="soft",
                starts_at=_STARTS_AT,
                ends_at=_ENDS_AT,
            ),
        ),
        context=_context(),
        application=_application(),
        response=response,
    )
    assert result.rule.family == "window"
    assert result.rule.relationship == "start_within"
    assert result.rule.constrained_facet == "schedule.start"
    assert result.rule.temporal_form == "absolute"


@pytest.mark.asyncio
async def test_b04_c_evaluate_api_exposes_canonical_backend_explanation() -> None:
    response = Response(status_code=200)
    result = await evaluate_temporal_constraints(
        payload=EvaluateTemporalConstraintsRequest(
            subject_ref=UUID(str(_SUBJECT_REF)),
            placement=AbsoluteIntervalPlacementRequest(
                starts_at=datetime(2026, 10, 5, 10, 0, tzinfo=UTC),
                ends_at=datetime(2026, 10, 5, 11, 0, tzinfo=UTC),
            ),
        ),
        context=_context(),
        application=_application(),
        response=response,
    )
    assert result.status == "admissible"
    assert result.hard_set_status == "feasible"
    assert result.items[0].reason_code == "schedule_start_within_window"
    assert result.items[0].evaluation == "satisfied"


def test_b04_c_request_union_rejects_window_relation_facet_mismatch() -> None:
    with pytest.raises(ValidationError):
        CreateTemporalConstraintRequest.model_validate(
            {
                "operation_id": "operation:b04-c:invalid-window-pair",
                "subject_ref": str(_SUBJECT_REF),
                "rule": {
                    "family": "window",
                    "relationship": "start_within",
                    "constrained_facet": "schedule.completion",
                    "strength": "hard",
                    "temporal_form": "absolute",
                    "starts_at": _STARTS_AT.isoformat(),
                    "ends_at": _ENDS_AT.isoformat(),
                },
            }
        )
