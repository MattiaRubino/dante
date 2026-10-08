"""Shared Reality review policy and bounded Activity/Event Objectives."""

from __future__ import annotations

import hashlib
import json
from decimal import Decimal
from typing import Annotated, Literal
from uuid import UUID, uuid7

from fastapi import APIRouter, Depends, Request, Response
from pydantic import BaseModel, ConfigDict, Field, model_validator
from sqlalchemy import text
from sqlalchemy.exc import DBAPIError, SQLAlchemyError

from dante.context.contracts import DanteContext
from dante.context.dependencies import require_dante_context, require_mutating_dante_context
from dante.platform.http.problem import ProblemError

router = APIRouter(prefix="/api/v1/temporal", tags=["temporal"])
Context = Annotated[DanteContext, Depends(require_dante_context)]
MutatingContext = Annotated[DanteContext, Depends(require_mutating_dante_context)]

RealitySubjectKind = Literal["activity", "event", "occurrence"]
ObjectiveSubjectKind = Literal["activity", "event", "occurrence"]
RealityMode = Literal["manual", "review_on_end", "auto_confirm_outcome"]
ObjectiveKind = Literal["boolean", "quantity", "qualitative", "range"]
ComparatorCode = Literal["eq", "gte", "lte", "between"]
AssessmentCode = Literal[
    "satisfied", "partial", "not_satisfied", "unknown", "indeterminate"
]


def _fingerprint(value: dict[str, object]) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")
    ).hexdigest()


def _subject_collection(kind: RealitySubjectKind) -> str:
    return {
        "activity": "activities",
        "event": "events",
        "occurrence": "occurrences",
    }[kind]


def _problem(exc: DBAPIError, *, noun: str) -> ProblemError:
    diagnostic = getattr(exc.orig, "diag", None)
    constraint = getattr(diagnostic, "constraint_name", None)
    if constraint in {
        "reality_review_policy_owner_unavailable",
        "temporal_objective_unavailable",
    }:
        return ProblemError(
            status=404,
            code=f"temporal.{noun}.unavailable",
            category="not_found",
            title=f"{noun.replace('_', ' ').title()} unavailable",
            detail="The requested subject is unavailable in this self scope.",
            retryable=False,
        )
    if constraint in {
        "reality_review_policy_operation_reused",
        "reality_review_policy_current_conflict",
        "temporal_objective_operation_reused",
        "temporal_objective_result_operation_reused",
        "temporal_objective_definition_operation_reused",
        "temporal_objective_definition_stale",
        "temporal_objective_definition_observation_incompatible",
        "temporal_objective_result_stale",
    }:
        return ProblemError(
            status=409,
            code=f"temporal.{noun}.conflict",
            category="conflict",
            title=f"{noun.replace('_', ' ').title()} conflict",
            detail="The command conflicts with current canonical state.",
            retryable=False,
        )
    if constraint in {
        "reality_review_policy_invalid",
        "temporal_objective_invalid",
        "temporal_objective_shape_invalid",
        "temporal_objective_result_invalid",
        "temporal_objective_result_shape_invalid",
        "temporal_objective_definition_invalid",
    }:
        return ProblemError(
            status=422,
            code=f"temporal.{noun}.invalid",
            category="validation",
            title=f"Invalid {noun.replace('_', ' ')}",
            detail="The submitted command is outside the accepted product contract.",
            retryable=False,
        )
    return ProblemError(
        status=409,
        code=f"temporal.{noun}.persistence",
        category="conflict",
        title=f"{noun.replace('_', ' ').title()} rejected",
        detail="The command could not be persisted safely.",
        retryable=False,
    )


class RealityPolicyCommand(BaseModel):
    model_config = ConfigDict(extra="forbid")

    operation_id: str = Field(min_length=1, max_length=200)
    mode_code: RealityMode
    expected_state_ref: UUID | None = None


class RealityPolicyResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    subject_kind: RealitySubjectKind
    subject_native_ref: UUID
    state_ref: UUID | None
    mode_code: RealityMode
    replayed: bool = False


class ObjectiveCreateCommand(BaseModel):
    model_config = ConfigDict(extra="forbid")

    operation_id: str = Field(min_length=1, max_length=200)
    label: str = Field(min_length=1, max_length=300)
    result_kind: ObjectiveKind
    comparator_code: ComparatorCode | None = None
    target_value: Decimal | None = None
    target_min: Decimal | None = None
    target_max: Decimal | None = None
    unit_code: str | None = Field(default=None, max_length=40)
    presentation_order: int = Field(ge=0, le=999)

    @model_validator(mode="after")
    def validate_shape(self) -> ObjectiveCreateCommand:
        if self.label != self.label.strip():
            raise ValueError("label must be trimmed")
        if self.unit_code is not None and (
            self.unit_code != self.unit_code.strip() or not self.unit_code
        ):
            raise ValueError("unit_code must be trimmed non-empty text")
        if self.result_kind in {"boolean", "qualitative"}:
            if any(
                value is not None
                for value in (
                    self.comparator_code,
                    self.target_value,
                    self.target_min,
                    self.target_max,
                    self.unit_code,
                )
            ):
                raise ValueError("boolean/qualitative Objective cannot carry a numeric target")
            return self
        if self.result_kind == "quantity":
            if (
                self.comparator_code not in {"eq", "gte", "lte"}
                or self.target_value is None
                or self.target_min is not None
                or self.target_max is not None
            ):
                raise ValueError("quantity Objective requires comparator and target_value")
            return self
        if (
            self.comparator_code != "between"
            or self.target_value is not None
            or self.target_min is None
            or self.target_max is None
            or self.target_min > self.target_max
        ):
            raise ValueError("range Objective requires ordered target_min/target_max")
        return self


class ObjectiveResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    objective_ref: UUID
    label: str
    result_kind: ObjectiveKind
    comparator_code: ComparatorCode | None
    target_value: Decimal | None
    target_min: Decimal | None
    target_max: Decimal | None
    unit_code: str | None
    presentation_order: int
    observation_ref: UUID | None = None
    observed_boolean: bool | None = None
    observed_numeric: Decimal | None = None
    qualitative_code: str | None = None
    evaluation_state_ref: UUID | None = None
    assessment_code: AssessmentCode | None = None
    replayed: bool = False


class ObjectiveResultCommand(BaseModel):
    model_config = ConfigDict(extra="forbid")

    operation_id: str = Field(min_length=1, max_length=200)
    observed_boolean: bool | None = None
    observed_numeric: Decimal | None = None
    qualitative_code: str | None = Field(default=None, max_length=120)
    assessment_code: AssessmentCode | None = None


class ObjectiveDefinitionStateResponse(BaseModel):
    """Current user-visible definition of the SAME logical Objective."""

    model_config = ConfigDict(extra="forbid")
    objective_ref: UUID
    definition_revision: int
    label: str
    result_kind: ObjectiveKind
    comparator_code: ComparatorCode | None
    target_value: Decimal | None
    target_min: Decimal | None
    target_max: Decimal | None
    unit_code: str | None
    presentation_order: int
    evaluation_state_ref: UUID | None


class ObjectiveDefinitionReviseCommand(ObjectiveCreateCommand):
    expected_revision: int = Field(ge=0)


class ObjectiveDefinitionReviseResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")
    objective_ref: UUID
    definition_revision: int
    evaluation_state_ref: UUID | None
    assessment_code: AssessmentCode | None
    replayed: bool


class ObjectiveResultCorrectionCommand(ObjectiveResultCommand):
    expected_evaluation_state_ref: UUID | None


class ObjectiveResultResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    objective_ref: UUID
    observation_ref: UUID
    evaluation_state_ref: UUID
    assessment_code: AssessmentCode
    replayed: bool = False


async def _reality_get(
    kind: RealitySubjectKind,
    subject_ref: UUID,
    context: Context,
    request: Request,
) -> RealityPolicyResponse:
    try:
        async with (
            request.app.state.database_runtime.session_factory() as session,
            session.begin(),
        ):
            row = (
                await session.execute(
                    text(
                        "SELECT * FROM dante.get_self_reality_review_policy("
                        ":actor,:kind,:subject)"
                    ),
                    {
                        "actor": context.self_person_ref,
                        "kind": kind,
                        "subject": subject_ref,
                    },
                )
            ).mappings().one_or_none()
    except SQLAlchemyError as exc:
        raise ProblemError(
            status=503,
            code="temporal.reality_policy.unavailable",
            category="service",
            title="Reality policy unavailable",
            detail="The Reality policy could not be read safely.",
            retryable=True,
        ) from exc
    if row is None:
        raise ProblemError(
            status=404,
            code="temporal.reality_policy.unavailable",
            category="not_found",
            title="Reality policy unavailable",
            detail="The requested subject is unavailable in this self scope.",
            retryable=False,
        )
    return RealityPolicyResponse(
        subject_kind=kind,
        subject_native_ref=subject_ref,
        state_ref=row["state_ref"],
        mode_code=row["mode_code"],
    )


async def _reality_set(
    kind: RealitySubjectKind,
    subject_ref: UUID,
    payload: RealityPolicyCommand,
    context: MutatingContext,
    request: Request,
    response: Response,
) -> RealityPolicyResponse:
    intent = {
        "version": 1,
        "subject_kind": kind,
        "subject_native_ref": str(subject_ref),
        "mode_code": payload.mode_code,
        "expected_state_ref": (
            None if payload.expected_state_ref is None else str(payload.expected_state_ref)
        ),
    }
    try:
        async with (
            request.app.state.database_runtime.session_factory() as session,
            session.begin(),
        ):
            row = (
                await session.execute(
                    text("""
                        SELECT * FROM dante.set_self_reality_review_policy(
                            :actor,:operation,:fingerprint,:kind,:subject,
                            :state,:mode,:expected
                        )
                    """),
                    {
                        "actor": context.self_person_ref,
                        "operation": payload.operation_id,
                        "fingerprint": _fingerprint(intent),
                        "kind": kind,
                        "subject": subject_ref,
                        "state": uuid7(),
                        "mode": payload.mode_code,
                        "expected": payload.expected_state_ref,
                    },
                )
            ).mappings().one()
    except DBAPIError as exc:
        raise _problem(exc, noun="reality_policy") from exc
    except SQLAlchemyError as exc:
        raise ProblemError(
            status=503,
            code="temporal.reality_policy.unavailable",
            category="service",
            title="Reality policy unavailable",
            detail="The Reality policy could not be persisted safely.",
            retryable=True,
        ) from exc
    response.status_code = 200 if row["replayed"] else 201
    response.headers["Cache-Control"] = "no-store"
    return RealityPolicyResponse(
        subject_kind=kind,
        subject_native_ref=subject_ref,
        state_ref=row["state_ref"],
        mode_code=row["mode_code"],
        replayed=bool(row["replayed"]),
    )


@router.get(
    "/activities/{subject_ref}/reality-policy",
    response_model=RealityPolicyResponse,
    operation_id="temporal_get_activity_reality_policy",
)
async def get_activity_reality_policy(
    subject_ref: UUID, context: Context, request: Request
) -> RealityPolicyResponse:
    return await _reality_get("activity", subject_ref, context, request)


@router.post(
    "/activities/{subject_ref}/reality-policy",
    response_model=RealityPolicyResponse,
    operation_id="temporal_set_activity_reality_policy",
)
async def set_activity_reality_policy(
    subject_ref: UUID,
    payload: RealityPolicyCommand,
    context: MutatingContext,
    request: Request,
    response: Response,
) -> RealityPolicyResponse:
    return await _reality_set("activity", subject_ref, payload, context, request, response)


@router.get(
    "/events/{subject_ref}/reality-policy",
    response_model=RealityPolicyResponse,
    operation_id="temporal_get_event_reality_policy",
)
async def get_event_reality_policy(
    subject_ref: UUID, context: Context, request: Request
) -> RealityPolicyResponse:
    return await _reality_get("event", subject_ref, context, request)


@router.post(
    "/events/{subject_ref}/reality-policy",
    response_model=RealityPolicyResponse,
    operation_id="temporal_set_event_reality_policy",
)
async def set_event_reality_policy(
    subject_ref: UUID,
    payload: RealityPolicyCommand,
    context: MutatingContext,
    request: Request,
    response: Response,
) -> RealityPolicyResponse:
    return await _reality_set("event", subject_ref, payload, context, request, response)


@router.get(
    "/occurrences/{subject_ref}/reality-policy",
    response_model=RealityPolicyResponse,
    operation_id="temporal_get_occurrence_reality_policy",
)
async def get_occurrence_reality_policy(
    subject_ref: UUID, context: Context, request: Request
) -> RealityPolicyResponse:
    return await _reality_get("occurrence", subject_ref, context, request)


@router.post(
    "/occurrences/{subject_ref}/reality-policy",
    response_model=RealityPolicyResponse,
    operation_id="temporal_set_occurrence_reality_policy",
)
async def set_occurrence_reality_policy(
    subject_ref: UUID,
    payload: RealityPolicyCommand,
    context: MutatingContext,
    request: Request,
    response: Response,
) -> RealityPolicyResponse:
    return await _reality_set("occurrence", subject_ref, payload, context, request, response)


async def _create_objective(
    kind: ObjectiveSubjectKind,
    subject_ref: UUID,
    payload: ObjectiveCreateCommand,
    context: MutatingContext,
    request: Request,
    response: Response,
) -> ObjectiveResponse:
    objective_ref = uuid7()
    intent = {
        "version": 1,
        "subject_kind": kind,
        "subject_native_ref": str(subject_ref),
        **payload.model_dump(mode="json"),
    }
    try:
        async with (
            request.app.state.database_runtime.session_factory() as session,
            session.begin(),
        ):
            row = (
                await session.execute(
                    text("""
                        SELECT * FROM dante.create_self_temporal_objective(
                            :actor,:operation,:fingerprint,:objective,:kind,:subject,
                            :label,:result_kind,:comparator,:target_value,:target_min,
                            :target_max,:unit,:presentation_order
                        )
                    """),
                    {
                        "actor": context.self_person_ref,
                        "operation": payload.operation_id,
                        "fingerprint": _fingerprint(intent),
                        "objective": objective_ref,
                        "kind": kind,
                        "subject": subject_ref,
                        "label": payload.label,
                        "result_kind": payload.result_kind,
                        "comparator": payload.comparator_code,
                        "target_value": payload.target_value,
                        "target_min": payload.target_min,
                        "target_max": payload.target_max,
                        "unit": payload.unit_code,
                        "presentation_order": payload.presentation_order,
                    },
                )
            ).mappings().one()
    except DBAPIError as exc:
        raise _problem(exc, noun="objective") from exc
    except SQLAlchemyError as exc:
        raise ProblemError(
            status=503,
            code="temporal.objective.unavailable",
            category="service",
            title="Objective unavailable",
            detail="The Objective could not be persisted safely.",
            retryable=True,
        ) from exc
    response.status_code = 200 if row["replayed"] else 201
    response.headers["Cache-Control"] = "no-store"
    return ObjectiveResponse(**dict(row))


async def _list_objectives(
    kind: ObjectiveSubjectKind,
    subject_ref: UUID,
    context: Context,
    request: Request,
) -> list[ObjectiveResponse]:
    try:
        async with (
            request.app.state.database_runtime.session_factory() as session,
            session.begin(),
        ):
            rows = (
                await session.execute(
                    text(
                        "SELECT * FROM dante.list_self_temporal_objectives("
                        ":actor,:kind,:subject)"
                    ),
                    {
                        "actor": context.self_person_ref,
                        "kind": kind,
                        "subject": subject_ref,
                    },
                )
            ).mappings().all()
    except SQLAlchemyError as exc:
        raise ProblemError(
            status=503,
            code="temporal.objective.unavailable",
            category="service",
            title="Objectives unavailable",
            detail="Objectives could not be read safely.",
            retryable=True,
        ) from exc
    return [ObjectiveResponse(**dict(row)) for row in rows]


@router.post(
    "/activities/{subject_ref}/objectives",
    response_model=ObjectiveResponse,
    operation_id="temporal_create_activity_objective",
)
async def create_activity_objective(
    subject_ref: UUID,
    payload: ObjectiveCreateCommand,
    context: MutatingContext,
    request: Request,
    response: Response,
) -> ObjectiveResponse:
    return await _create_objective("activity", subject_ref, payload, context, request, response)


@router.get(
    "/activities/{subject_ref}/objectives",
    response_model=list[ObjectiveResponse],
    operation_id="temporal_list_activity_objectives",
)
async def list_activity_objectives(
    subject_ref: UUID, context: Context, request: Request
) -> list[ObjectiveResponse]:
    return await _list_objectives("activity", subject_ref, context, request)


@router.post(
    "/events/{subject_ref}/objectives",
    response_model=ObjectiveResponse,
    operation_id="temporal_create_event_objective",
)
async def create_event_objective(
    subject_ref: UUID,
    payload: ObjectiveCreateCommand,
    context: MutatingContext,
    request: Request,
    response: Response,
) -> ObjectiveResponse:
    return await _create_objective("event", subject_ref, payload, context, request, response)


@router.get(
    "/events/{subject_ref}/objectives",
    response_model=list[ObjectiveResponse],
    operation_id="temporal_list_event_objectives",
)
async def list_event_objectives(
    subject_ref: UUID, context: Context, request: Request
) -> list[ObjectiveResponse]:
    return await _list_objectives("event", subject_ref, context, request)


@router.get(
    "/occurrences/{subject_ref}/objectives",
    response_model=list[ObjectiveResponse],
    operation_id="temporal_list_occurrence_objectives",
)
async def list_occurrence_objectives(
    subject_ref: UUID, context: Context, request: Request
) -> list[ObjectiveResponse]:
    return await _list_objectives("occurrence", subject_ref, context, request)


@router.get(
    "/objectives/{objective_ref}/definition",
    response_model=ObjectiveDefinitionStateResponse,
    operation_id="temporal_get_objective_definition",
)
async def get_objective_definition(
    objective_ref: UUID, context: Context, request: Request, response: Response,
) -> ObjectiveDefinitionStateResponse:
    try:
        async with request.app.state.database_runtime.session_factory() as session, session.begin():
            row = (await session.execute(
                text(
                    "SELECT * FROM dante.get_self_temporal_objective_definition("
                    ":actor,:objective)"
                ),
                {"actor": context.self_person_ref, "objective": objective_ref},
            )).mappings().one_or_none()
    except SQLAlchemyError as exc:
        raise ProblemError(
            status=503, code="temporal.objective.definition_read_unavailable",
            category="service", title="Objective definition unavailable",
            detail="Could not read the current Objective definition.", retryable=True,
        ) from exc
    if row is None:
        raise ProblemError(
            status=404, code="temporal.objective.unavailable", category="not_found",
            title="Objective unavailable", detail="Objective not found in self scope.",
        )
    response.headers["Cache-Control"] = "no-store"
    return ObjectiveDefinitionStateResponse(**dict(row))


@router.put(
    "/objectives/{objective_ref}/definition",
    response_model=ObjectiveDefinitionReviseResponse,
    operation_id="temporal_revise_objective_definition",
)
async def revise_objective_definition(
    objective_ref: UUID,
    payload: ObjectiveDefinitionReviseCommand,
    context: MutatingContext,
    request: Request,
    response: Response,
) -> ObjectiveDefinitionReviseResponse:
    intent = {
        "version": 1, "objective_ref": str(objective_ref),
        **payload.model_dump(mode="json"),
    }
    try:
        async with request.app.state.database_runtime.session_factory() as session, session.begin():
            row = (await session.execute(
                text(
                    "SELECT * FROM dante.revise_self_temporal_objective_definition("
                    ":actor,:operation,:fingerprint,:objective,:expected,"
                    ":label,:kind,:comparator,:target,:minimum,:maximum,"
                    ":unit,:ordering,:evaluation)"
                ),
                {
                    "actor": context.self_person_ref,
                    "operation": payload.operation_id,
                    "fingerprint": _fingerprint(intent),
                    "objective": objective_ref,
                    "expected": payload.expected_revision,
                    "label": payload.label,
                    "kind": payload.result_kind,
                    "comparator": payload.comparator_code,
                    "target": payload.target_value,
                    "minimum": payload.target_min,
                    "maximum": payload.target_max,
                    "unit": payload.unit_code,
                    "ordering": payload.presentation_order,
                    "evaluation": uuid7(),
                },
            )).mappings().one()
    except DBAPIError as exc:
        raise _problem(exc, noun="objective_definition") from exc
    except SQLAlchemyError as exc:
        raise ProblemError(
            status=503, code="temporal.objective.definition_write_unavailable",
            category="service", title="Objective definition unavailable",
            detail="Definition could not be persisted.", retryable=True,
        ) from exc
    response.headers["Cache-Control"] = "no-store"
    return ObjectiveDefinitionReviseResponse(**dict(row))


@router.post(
    "/objectives/{objective_ref}/correction",
    response_model=ObjectiveResultResponse,
    operation_id="temporal_correct_objective_result",
)
async def correct_objective_result(
    objective_ref: UUID,
    payload: ObjectiveResultCorrectionCommand,
    context: MutatingContext,
    request: Request,
    response: Response,
) -> ObjectiveResultResponse:
    intent = {
        "version": 1, "objective_ref": str(objective_ref),
        "operation_id": payload.operation_id,
        "observed_boolean": payload.observed_boolean,
        "observed_numeric": payload.observed_numeric,
        "qualitative_code": payload.qualitative_code,
        "assessment_code": payload.assessment_code,
        "expected_evaluation_state_ref": str(payload.expected_evaluation_state_ref)
        if payload.expected_evaluation_state_ref is not None else None,
    }
    try:
        async with request.app.state.database_runtime.session_factory() as session, session.begin():
            row = (await session.execute(
                text(
                    "SELECT * FROM dante.correct_self_temporal_objective_result("
                    ":actor,:operation,:fingerprint,:objective,:observation,:state,"
                    ":boolean,:numeric,:qualitative,:assessment,:expected)"
                ),
                {
                    "actor": context.self_person_ref,
                    "operation": payload.operation_id,
                    "fingerprint": _fingerprint(intent),
                    "objective": objective_ref,
                    "observation": uuid7(),
                    "state": uuid7(),
                    "boolean": payload.observed_boolean,
                    "numeric": payload.observed_numeric,
                    "qualitative": payload.qualitative_code,
                    "assessment": payload.assessment_code,
                    "expected": payload.expected_evaluation_state_ref,
                },
            )).mappings().one()
    except DBAPIError as exc:
        raise _problem(exc, noun="objective_result") from exc
    except SQLAlchemyError as exc:
        raise ProblemError(
            status=503, code="temporal.objective.correction_unavailable",
            category="service", title="Objective correction unavailable",
            detail="Corrected result could not be persisted.", retryable=True,
        ) from exc
    response.headers["Cache-Control"] = "no-store"
    return ObjectiveResultResponse(**dict(row))


@router.post(
    "/objectives/{objective_ref}/result",
    response_model=ObjectiveResultResponse,
    operation_id="temporal_record_objective_result",
)
async def record_objective_result(
    objective_ref: UUID,
    payload: ObjectiveResultCommand,
    context: MutatingContext,
    request: Request,
    response: Response,
) -> ObjectiveResultResponse:
    intent = {
        "version": 1,
        "objective_ref": str(objective_ref),
        **payload.model_dump(mode="json"),
    }
    try:
        async with (
            request.app.state.database_runtime.session_factory() as session,
            session.begin(),
        ):
            row = (
                await session.execute(
                    text("""
                        SELECT * FROM dante.record_self_temporal_objective_result(
                            :actor,:operation,:fingerprint,:objective,:observation,:state,
                            :observed_boolean,:observed_numeric,:qualitative,:assessment
                        )
                    """),
                    {
                        "actor": context.self_person_ref,
                        "operation": payload.operation_id,
                        "fingerprint": _fingerprint(intent),
                        "objective": objective_ref,
                        "observation": uuid7(),
                        "state": uuid7(),
                        "observed_boolean": payload.observed_boolean,
                        "observed_numeric": payload.observed_numeric,
                        "qualitative": payload.qualitative_code,
                        "assessment": payload.assessment_code,
                    },
                )
            ).mappings().one()
    except DBAPIError as exc:
        raise _problem(exc, noun="objective_result") from exc
    except SQLAlchemyError as exc:
        raise ProblemError(
            status=503,
            code="temporal.objective_result.unavailable",
            category="service",
            title="Objective result unavailable",
            detail="The Objective result could not be persisted safely.",
            retryable=True,
        ) from exc
    response.status_code = 200 if row["replayed"] else 201
    response.headers["Cache-Control"] = "no-store"
    return ObjectiveResultResponse(**dict(row))
