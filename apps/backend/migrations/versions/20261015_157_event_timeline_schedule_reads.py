"""Owner-scoped Event Timeline placement and Undo receipt reads.

Revision ID: 20261015_157
Revises: 20261015_156

Event and Event Occurrence placement removal uses the pre-existing
guarded, monotonic generic Schedule commands. These bounded read functions
expose exact event-owned Schedule identity without runtime table SELECT.
"""
from collections.abc import Sequence

from alembic import op

revision: str = "20261015_157"
down_revision: str | None = "20261015_156"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_SCHEDULES = r"""
CREATE FUNCTION dante.list_self_event_timeline_schedules(
    requested_actor uuid, requested_event uuid
) RETURNS TABLE(
    schedule_ref uuid,
    subject_native_ref uuid,
    material_state_ref uuid,
    display_label text
)
LANGUAGE sql SECURITY DEFINER STABLE PARALLEL SAFE
SET search_path=pg_catalog,dante,pg_temp
AS $schedules$
    SELECT schedule.schedule_ref,
           schedule.subject_native_ref,
           current.material_state_ref,
           COALESCE(
               zoned.starts_local_at::text,
               floating.starts_local_at::text,
               lower(dates.date_span)::text,
               schedule.schedule_ref::text
           ) AS display_label
      FROM dante.event_expectation AS owned
      JOIN dante.schedule AS schedule
        ON schedule.subject_native_ref=owned.event_ref
           OR EXISTS (
               SELECT 1 FROM dante.occurrence_generation AS generation
                WHERE generation.source_native_ref=owned.event_ref
                  AND generation.occurrence_ref=schedule.subject_native_ref
           )
      LEFT JOIN dante.schedule_current_placement AS current
        ON current.scoped_owner_ref=schedule.schedule_ref
      LEFT JOIN dante.schedule_placement_named_zone_state AS zoned
        ON zoned.material_state_ref=current.material_state_ref
      LEFT JOIN dante.schedule_placement_floating_local_state AS floating
        ON floating.material_state_ref=current.material_state_ref
      LEFT JOIN dante.schedule_placement_date_state AS dates
        ON dates.material_state_ref=current.material_state_ref
     WHERE owned.event_ref=requested_event
       AND owned.self_person_ref=requested_actor
     ORDER BY display_label DESC,schedule.schedule_ref DESC LIMIT 1000
$schedules$;
"""

_UNDO = r"""
CREATE FUNCTION dante.list_self_event_timeline_undo(
    requested_actor uuid, requested_event uuid
) RETURNS TABLE(schedule_ref uuid,unschedule_operation_id text)
LANGUAGE sql SECURITY DEFINER STABLE PARALLEL SAFE
SET search_path=pg_catalog,dante,pg_temp
AS $undo$
    SELECT placement.schedule_ref,receipt.operation_id
      FROM dante.list_self_event_timeline_schedules(
          requested_actor,requested_event
      ) AS placement
      JOIN LATERAL (
        SELECT removed.operation_id
          FROM dante.schedule_unschedule_operation AS removed
         WHERE removed.self_person_ref=requested_actor
           AND removed.schedule_ref=placement.schedule_ref
           AND NOT EXISTS (
              SELECT 1 FROM dante.schedule_unschedule_undo_operation AS restored
               WHERE restored.self_person_ref=requested_actor
                 AND restored.schedule_ref=removed.schedule_ref
                 AND restored.unschedule_operation_id=removed.operation_id
           )
         ORDER BY removed.created_at DESC,removed.operation_id DESC LIMIT 1
      ) AS receipt ON true
     WHERE placement.material_state_ref IS NULL
     ORDER BY placement.schedule_ref
$undo$;
"""


def upgrade() -> None:
    db = op.get_bind()
    for sql in (_SCHEDULES, _UNDO):
        db.exec_driver_sql(sql)
    for name in (
        "dante.list_self_event_timeline_schedules(uuid,uuid)",
        "dante.list_self_event_timeline_undo(uuid,uuid)",
    ):
        db.exec_driver_sql(f"ALTER FUNCTION {name} OWNER TO dante_owner")
        db.exec_driver_sql(
            f"REVOKE ALL ON FUNCTION {name} FROM PUBLIC,dante_runtime,dante_migrator"
        )
        db.exec_driver_sql(f"GRANT EXECUTE ON FUNCTION {name} TO dante_runtime")


def downgrade() -> None:
    raise RuntimeError("Owner-scoped Event Timeline placement reads are forward-only")
