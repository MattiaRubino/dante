"""A bounded, self-scoped read model for the post-create Activity editor."""

from __future__ import annotations

from typing import Annotated, Any
from uuid import UUID

from fastapi import APIRouter, Depends, Request, Response
from pydantic import BaseModel, ConfigDict
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from dante.context.contracts import DanteContext
from dante.context.dependencies import require_dante_context
from dante.modules.temporal.decomposition_api import ActivityScheduleResponse
from dante.modules.temporal.reality_objective_api import ObjectiveResponse, RealityPolicyResponse
from dante.platform.http.problem import ProblemError

router = APIRouter(prefix="/api/v1/temporal/activities", tags=["temporal"])
ReadContext = Annotated[DanteContext, Depends(require_dante_context)]


class EditExecutionPolicy(BaseModel):
    activity_ref: UUID
    mode_code: str
    state_ref: UUID | None


class EditPlacementLock(BaseModel):
    schedule_ref: UUID
    locked: bool
    revision: int


class EditReminder(BaseModel):
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
      JOIN dante.schedule_current_placement AS current
        ON current.scoped_owner_ref=s.schedule_ref
      JOIN dante.schedule_placement_state AS state
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
