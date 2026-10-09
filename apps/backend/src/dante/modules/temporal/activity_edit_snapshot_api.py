"""A bounded, self-scoped read model for the post-create Activity editor."""

from __future__ import annotations

import hashlib
import json
from typing import Annotated, Any
from uuid import UUID, uuid7

from fastapi import APIRouter, Depends, Request, Response
from pydantic import BaseModel, ConfigDict, Field, model_validator
from sqlalchemy import text
from sqlalchemy.exc import DBAPIError, SQLAlchemyError

from dante.context.contracts import DanteContext
from dante.context.dependencies import require_dante_context, require_mutating_dante_context
from dante.modules.temporal.activity_inspector_api import ActivityProfileResponse
from dante.modules.temporal.decomposition_api import ActivityScheduleResponse
from dante.modules.temporal.reality_objective_api import ObjectiveResponse, RealityPolicyResponse
from dante.platform.http.problem import ProblemError

router = APIRouter(prefix="/api/v1/temporal/activities", tags=["temporal"])
ReadContext = Annotated[DanteContext, Depends(require_dante_context)]
WriteContext = Annotated[DanteContext, Depends(require_mutating_dante_context)]


class EditExecutionPolicy(BaseModel):
    activity_ref: UUID
    mode_code: str
    state_ref: UUID | None


class EditPlacementLock(BaseModel):
    schedule_ref: UUID
    locked: bool
    revision: int


class EditReminder(BaseModel):
    schedule_ref: UUID
    material_state_ref: UUID
    enabled: bool
    lead_minutes: int


class ActivityEditSnapshot(BaseModel):
    model_config = ConfigDict(extra="forbid")

    activity_ref: UUID
    execution_policy: EditExecutionPolicy
    reality_policy: RealityPolicyResponse
    child_guard_mode: str
    life_area_ref: UUID | None
    schedules: list[ActivityScheduleResponse]
    objectives: list[ObjectiveResponse]
    placement_lock: EditPlacementLock | None
    reminder: EditReminder | None


class EditProfileChange(BaseModel):
    model_config = ConfigDict(extra="forbid")
    expected_revision: int = Field(ge=0)
    title: str = Field(min_length=1, max_length=300)
    description: str | None = None
    location: str | None = None
    color_code: str | None = Field(default=None, pattern=r"^#[0-9A-Fa-f]{6}$")

    @model_validator(mode="after")
    def validate_text(self) -> EditProfileChange:
        if self.title != self.title.strip() or not self.title:
            raise ValueError("The Activity title must be trimmed and nonempty.")
        if any(value is not None and (not value or value != value.strip())
               for value in (self.description, self.location)):
            raise ValueError("Optional Activity text must be trimmed and nonempty.")
        return self


class EditPolicyChange(BaseModel):
    model_config = ConfigDict(extra="forbid")
    mode_code: str
    expected_state_ref: UUID | None = None


class EditReminderChange(BaseModel):
    model_config = ConfigDict(extra="forbid")
    schedule_ref: UUID
    expected_state_ref: UUID | None = None
    enabled: bool
    lead_minutes: int = Field(ge=0, le=10_080)


class ActivityCoreEditCommand(BaseModel):
    model_config = ConfigDict(extra="forbid")
    operation_id: str = Field(min_length=1, max_length=200)
    profile: EditProfileChange | None = None
    capture: EditPolicyChange | None = None
    reality: EditPolicyChange | None = None
    reminder: EditReminderChange | None = None

    @model_validator(mode="after")
    def validate_changes(self) -> ActivityCoreEditCommand:
        if all(value is None for value in (
            self.profile, self.capture, self.reality, self.reminder,
        )):
            raise ValueError("At least one change is required.")
        if self.capture is not None and self.capture.mode_code not in {
            "disabled", "record", "live", "record_and_live"
        }:
            raise ValueError("Unsupported Session capture mode.")
        if self.reality is not None and self.reality.mode_code not in {
            "manual", "review_on_end", "auto_confirm_outcome"
        }:
            raise ValueError("Unsupported Reality mode.")
        return self


class ActivityCoreEditResponse(BaseModel):
    profile: ActivityProfileResponse
    capture: EditExecutionPolicy
    reality: RealityPolicyResponse
    reminder: EditReminder | None


# All collections are bounded by one Activity ID and fetched in one database statement.
# The owner CTE is the authorization gate. Existing self-scoped functions retain their
# own checks; no private row or second connection is exposed to the client.
_SNAPSHOT = text("""
WITH owner AS MATERIALIZED (
    SELECT activity_ref FROM dante.get_self_activity_profile(:actor,:activity)
), placements AS MATERIALIZED (
    SELECT s.schedule_ref,s.subject_native_ref,
           current.material_state_ref AS placement_material_state_ref,
           state.temporal_form_code AS temporal_form,
           lower(dates.date_span) AS start_date,
           upper(dates.date_span) AS end_date_exclusive,
           COALESCE(floating.starts_local_at,zoned.starts_local_at) AS starts_local_at,
           COALESCE(floating.ends_local_at,zoned.ends_local_at) AS ends_local_at,
           zoned.zone_id,zoned.resolved_start_at,zoned.resolved_end_at,
           absolute.starts_at,absolute.ends_at,coarse.local_date,coarse.period_code,
           role.role_code,role.presentation_order,role.display_name
      FROM owner
      JOIN dante.schedule AS s ON s.subject_native_ref=owner.activity_ref
 LEFT JOIN dante.schedule_current_placement AS current
        ON current.scoped_owner_ref=s.schedule_ref
 LEFT JOIN dante.schedule_placement_state AS state
        ON state.schedule_ref=s.schedule_ref
       AND state.material_state_ref=current.material_state_ref
 LEFT JOIN dante.schedule_placement_date_state AS dates
        ON dates.material_state_ref=state.material_state_ref
 LEFT JOIN dante.schedule_placement_floating_local_state AS floating
        ON floating.material_state_ref=state.material_state_ref
 LEFT JOIN dante.schedule_placement_named_zone_state AS zoned
        ON zoned.material_state_ref=state.material_state_ref
 LEFT JOIN dante.schedule_placement_absolute_state AS absolute
        ON absolute.material_state_ref=state.material_state_ref
 LEFT JOIN dante.schedule_placement_coarse_local_period_state AS coarse
        ON coarse.material_state_ref=state.material_state_ref
 LEFT JOIN dante.get_self_activity_schedule_roles(:actor,CAST(ARRAY[:activity] AS uuid[])) AS role
        ON role.schedule_ref=s.schedule_ref
     WHERE current.material_state_ref IS NOT NULL OR NOT EXISTS (
         SELECT 1 FROM dante.schedule_placement_state AS history
          WHERE history.schedule_ref=s.schedule_ref
     )
), primary_schedule AS (
    SELECT schedule_ref FROM placements
     WHERE role_code='envelope' OR role_code IS NULL
     ORDER BY CASE WHEN role_code='envelope' THEN 0 ELSE 1 END, schedule_ref
     LIMIT 1
)
SELECT jsonb_build_object(
    'activity_ref',owner.activity_ref,
    'execution_policy',(SELECT jsonb_build_object('activity_ref',owner.activity_ref,
                          'mode_code',p.mode_code,'state_ref',p.state_ref)
                          FROM dante.get_self_activity_execution_policy(:actor,:activity) AS p),
    'reality_policy',(SELECT jsonb_build_object(
                        'subject_kind','activity','subject_native_ref',owner.activity_ref,
                        'mode_code',p.mode_code,'state_ref',p.state_ref)
                        FROM dante.get_self_reality_review_policy(:actor,'activity',:activity) AS p),
    'child_guard_mode',(SELECT mode_code FROM dante.get_self_activity_decomposition_policy(:actor,:activity)),
    'life_area_ref',(SELECT life_area_ref FROM dante.list_self_life_area_assignments(:actor)
                       WHERE subject_kind='activity' AND subject_native_ref=owner.activity_ref LIMIT 1),
    'schedules',(SELECT COALESCE(jsonb_agg(to_jsonb(p) - 'subject_native_ref' ORDER BY
                    CASE p.role_code WHEN 'envelope' THEN 0 WHEN 'interval' THEN 1
                         WHEN 'planned' THEN 2 ELSE 3 END,
                    p.presentation_order,p.schedule_ref),'[]'::jsonb) FROM placements AS p),
    'objectives',(SELECT COALESCE(jsonb_agg(to_jsonb(o) ORDER BY o.presentation_order,o.objective_ref),
                         '[]'::jsonb)
                    FROM dante.list_self_temporal_objectives(:actor,'activity',:activity) AS o),
    'placement_lock',(SELECT to_jsonb(l) FROM primary_schedule AS p
                       CROSS JOIN LATERAL dante.get_self_schedule_placement_lock(:actor,p.schedule_ref) AS l),
    'reminder',(SELECT to_jsonb(r) FROM primary_schedule AS p
                 CROSS JOIN LATERAL dante.get_self_schedule_reminder(:actor,p.schedule_ref) AS r)
) AS payload FROM owner
""")


@router.get(
    "/{activity_ref}/edit-snapshot",
    response_model=ActivityEditSnapshot,
    operation_id="temporal_get_activity_edit_snapshot",
)
async def get_activity_edit_snapshot(
    activity_ref: UUID, context: ReadContext, request: Request, response: Response,
) -> ActivityEditSnapshot:
    response.headers["Cache-Control"] = "no-store"
    try:
        async with request.app.state.database_runtime.session_factory() as session, session.begin():
            payload: dict[str, Any] | None = await session.scalar(
                _SNAPSHOT, {"actor": context.self_person_ref, "activity": activity_ref},
            )
    except SQLAlchemyError as exc:
        raise ProblemError(
            status=503, code="temporal.activity_edit.unavailable", category="service",
            title="Activity edit unavailable", detail="The Activity could not be read safely.",
            retryable=True,
        ) from exc
    if payload is None:
        raise ProblemError(
            status=404, code="temporal.activity_edit.not_found", category="not_found",
            title="Activity unavailable", detail="Activity unavailable in self scope.",
        )
    return ActivityEditSnapshot.model_validate(payload)


def _fingerprint(intent: dict[str, object]) -> str:
    return hashlib.sha256(
        json.dumps(intent, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


@router.put(
    "/{activity_ref}/core-edit",
    response_model=ActivityCoreEditResponse,
    operation_id="temporal_revise_activity_core",
)
async def revise_activity_core(
    activity_ref: UUID, body: ActivityCoreEditCommand,
    context: WriteContext, request: Request, response: Response,
) -> ActivityCoreEditResponse:
    """Apply guarded changes in one all-or-nothing transaction."""
    response.headers["Cache-Control"] = "no-store"
    digest = hashlib.sha256(body.operation_id.encode("utf-8")).hexdigest()
    params = {"actor": context.self_person_ref, "activity": activity_ref}
    try:
        async with request.app.state.database_runtime.session_factory() as session, session.begin():
            if body.capture is not None:
                change = body.capture
                intent = {
                    "version": 1, "activity_ref": str(activity_ref),
                    "mode_code": change.mode_code,
                    "expected_state_ref": str(change.expected_state_ref)
                    if change.expected_state_ref is not None else None,
                }
                await session.execute(text("""
                    SELECT * FROM dante.set_self_activity_execution_policy(
                        :actor,:operation,:fingerprint,:activity,:state,:mode,:expected)
                """), {
                    **params, "operation": f"edit:capture:{digest}",
                    "fingerprint": _fingerprint(intent), "state": uuid7(),
                    "mode": change.mode_code, "expected": change.expected_state_ref,
                })
            if body.reality is not None:
                change = body.reality
                intent = {
                    "version": 1, "subject_kind": "activity",
                    "subject_native_ref": str(activity_ref), "mode_code": change.mode_code,
                    "expected_state_ref": str(change.expected_state_ref)
                    if change.expected_state_ref is not None else None,
                }
                await session.execute(text("""
                    SELECT * FROM dante.set_self_reality_review_policy(
                        :actor,:operation,:fingerprint,'activity',:activity,:state,:mode,:expected)
                """), {
                    **params, "operation": f"edit:reality:{digest}",
                    "fingerprint": _fingerprint(intent), "state": uuid7(),
                    "mode": change.mode_code, "expected": change.expected_state_ref,
                })
            if body.profile is not None:
                change = body.profile
                await session.execute(text("""
                    SELECT * FROM dante.revise_self_activity_profile(
                        :actor,:activity,:operation,:revision,:title,
                        :description,:location,:color)
                """), {
                    **params, "operation": f"edit:profile:{digest}",
                    "revision": change.expected_revision,
                    "title": change.title.strip(),
                    "description": change.description.strip() or None if change.description else None,
                    "location": change.location.strip() or None if change.location else None,
                    "color": change.color_code.upper() if change.color_code else None,
                })
            if body.reminder is not None:
                change = body.reminder
                primary = await session.scalar(text("""
                    SELECT r.schedule_ref
                      FROM dante.get_self_activity_schedule_roles(
                        :actor, CAST(ARRAY[:activity] AS uuid[])) AS r
                     WHERE r.schedule_ref=:schedule
                       AND r.role_code='envelope'
                """), {**params, "schedule": change.schedule_ref})
                if primary is None:
                    raise ProblemError(
                        status=422, code="temporal.activity_edit.invalid_reminder_target",
                        category="validation", title="Invalid reminder target",
                        detail="The reminder must belong to this Activity's envelope.",
                    )
                intent = {
                    "version": 1, "schedule_ref": str(change.schedule_ref),
                    "expected_material_state_ref": str(change.expected_state_ref)
                    if change.expected_state_ref is not None else None,
                    "enabled": change.enabled, "lead_minutes": change.lead_minutes,
                }
                await session.execute(text("""
                    SELECT * FROM dante.configure_self_schedule_reminder(
                        :actor,:operation,:fingerprint,:schedule,:expected,
                        :reminder_ref,:material_state_ref,:enabled,:lead)
                """), {
                    **params, "operation": f"edit:reminder:{digest}",
                    "fingerprint": _fingerprint(intent),
                    "schedule": change.schedule_ref, "expected": change.expected_state_ref,
                    "reminder_ref": uuid7(), "material_state_ref": uuid7(),
                    "enabled": change.enabled, "lead": change.lead_minutes,
                })
            profile = (await session.execute(
                text("SELECT * FROM dante.get_self_activity_profile(:actor,:activity)"), params,
            )).mappings().one()
            capture = (await session.execute(
                text("SELECT * FROM dante.get_self_activity_execution_policy(:actor,:activity)"),
                params,
            )).mappings().one()
            reality = (await session.execute(text("""
                SELECT * FROM dante.get_self_reality_review_policy(:actor,'activity',:activity)
            """), params)).mappings().one()
            reminder = None
            if body.reminder is not None:
                reminder = (await session.execute(text("""
                    SELECT * FROM dante.get_self_schedule_reminder(:actor,:schedule)
                """), {**params, "schedule": body.reminder.schedule_ref})).mappings().one()
    except DBAPIError as exc:
        constraint = getattr(getattr(exc.orig, "diag", None), "constraint_name", None)
        if constraint and constraint.endswith("_unavailable"):
            raise ProblemError(
                status=404, code="temporal.activity_edit.not_found", category="not_found",
                title="Activity unavailable", detail="Activity unavailable in self scope.",
            ) from exc
        if constraint and constraint.endswith((
            "_stale", "_current_conflict", "_operation_reused",
        )):
            raise ProblemError(
                status=409, code="temporal.activity_edit.conflict", category="conflict",
                title="Activity changed", detail="Reload the Activity and retry.",
            ) from exc
        if constraint and (constraint.endswith("_invalid") or constraint in {
            "schedule_reminder_input", "schedule_reminder_schedule_unavailable",
        }):
            raise ProblemError(
                status=422, code="temporal.activity_edit.invalid", category="validation",
                title="Invalid Activity change", detail="Check the submitted Activity fields.",
            ) from exc
        raise ProblemError(
            status=503, code="temporal.activity_edit.unavailable", category="service",
            title="Activity edit unavailable", detail="The change could not be saved safely.",
            retryable=True,
        ) from exc
    except SQLAlchemyError as exc:
        raise ProblemError(
            status=503, code="temporal.activity_edit.unavailable", category="service",
            title="Activity edit unavailable", detail="The change could not be saved safely.",
            retryable=True,
        ) from exc
    return ActivityCoreEditResponse(
        profile=ActivityProfileResponse(**dict(profile)),
        capture=EditExecutionPolicy(activity_ref=activity_ref, mode_code=capture["mode_code"],
                                    state_ref=capture["state_ref"]),
        reality=RealityPolicyResponse(subject_kind="activity", subject_native_ref=activity_ref,
                                      mode_code=reality["mode_code"], state_ref=reality["state_ref"]),
        reminder=EditReminder(**dict(reminder)) if reminder is not None else None,
    )
