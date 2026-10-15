"""Isolated coordinated Activity Schedule Undo, with read-only receipt discovery.

Revision ID: 20261015_154
Revises: 20261015_153

Clones the reviewed generic Undo implementation, removing only the B14-149
generic-guard stanza. The clone is owner-only (no dante_runtime EXECUTE);
a dedicated Activity coordinator validates identity, Session CAS, role set and
placement locks BEFORE invoking it in a serializable transaction. Generic
Schedule Undo remains guarded exactly as before.
"""
from collections.abc import Sequence

from alembic import op

revision: str = "20261015_154"
down_revision: str | None = "20261015_153"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_GENERIC_ACTIVITY_GUARD = """            -- Serialize against planned Session Start before the Undo check.
            PERFORM 1 FROM dante.activity_intention AS activity
              JOIN dante.schedule AS owned
                ON owned.subject_native_ref=activity.activity_ref
             WHERE owned.schedule_ref=requested_schedule_ref
               AND activity.self_person_ref=requested_self_person_ref
             FOR UPDATE OF activity;
            IF EXISTS (
                SELECT 1 FROM dante.schedule AS owned
                JOIN dante.activity_intention AS activity
                  ON activity.activity_ref=owned.subject_native_ref
                 AND activity.self_person_ref=requested_self_person_ref
                JOIN dante.get_self_activity_schedule_roles(
                  requested_self_person_ref, ARRAY[activity.activity_ref]
                ) AS purpose ON purpose.schedule_ref=owned.schedule_ref
                WHERE owned.schedule_ref=requested_schedule_ref
                  AND (purpose.role_code='interval'
                       OR (purpose.role_code='envelope' AND (
                           EXISTS (
                               SELECT 1 FROM dante.get_self_activity_schedule_roles(
                                 requested_self_person_ref, ARRAY[activity.activity_ref]
                               ) AS sibling WHERE sibling.role_code='interval'
                           ) OR EXISTS (
                               SELECT 1 FROM dante.list_self_subject_sessions(
                                 requested_self_person_ref, activity.activity_ref
                               )
                           )
                       )))
            ) THEN
                RAISE EXCEPTION USING ERRCODE='23514',
                    CONSTRAINT='schedule_activity_interval_requires_replan',
                    MESSAGE='Activity interval Undo requires a coordinated Activity replan';
            END IF;

"""

_UNDO_RECEIPTS = r"""
CREATE FUNCTION dante.list_self_activity_timeline_undo(
    requested_actor uuid, requested_activity uuid
) RETURNS TABLE(schedule_ref uuid,unschedule_operation_id text)
LANGUAGE sql SECURITY DEFINER STABLE PARALLEL SAFE
SET search_path=pg_catalog,dante,pg_temp
AS $receipts$
  SELECT role.schedule_ref,
         latest.operation_id
  FROM dante.activity_intention AS owner
  JOIN LATERAL dante.get_self_activity_schedule_roles(
      requested_actor,ARRAY[owner.activity_ref]
  ) AS role ON role.role_code IN ('envelope','interval')
  JOIN LATERAL (
     SELECT removed.operation_id
       FROM dante.schedule_unschedule_operation AS removed
      WHERE removed.self_person_ref=requested_actor
        AND removed.schedule_ref=role.schedule_ref
        AND NOT EXISTS(
           SELECT 1 FROM dante.schedule_unschedule_undo_operation AS restored
            WHERE restored.self_person_ref=requested_actor
              AND restored.schedule_ref=removed.schedule_ref
              AND restored.unschedule_operation_id=removed.operation_id
        )
      ORDER BY removed.created_at DESC,removed.operation_id DESC LIMIT 1
  ) AS latest ON true
  WHERE owner.activity_ref=requested_activity
    AND owner.self_person_ref=requested_actor
    AND owner.retired_at IS NULL
  ORDER BY role.schedule_ref
$receipts$;
"""

def upgrade() -> None:
    db = op.get_bind()
    old_name = "dante.undo_self_schedule_unschedule_any"
    new_name = "dante.undo_self_activity_schedule_coordinated"
    signature = f"{old_name}(uuid,text,text,uuid,text,uuid)"
    definition = db.exec_driver_sql(
        f"SELECT pg_get_functiondef('{signature}'::regprocedure)"
    ).scalar_one()
    if definition.count(_GENERIC_ACTIVITY_GUARD) != 1:
        raise RuntimeError("Unexpected generic Undo guard: review independently")
    if definition.count(old_name) < 1:
        raise RuntimeError("Cannot identify generic Undo capability")
    clone = definition.replace(_GENERIC_ACTIVITY_GUARD, "").replace(old_name,new_name,1)
    db.exec_driver_sql(clone.replace("%", "%%"))
    db.exec_driver_sql(_UNDO_RECEIPTS)
    for name, direct in (
        (f"{new_name}(uuid,text,text,uuid,text,uuid)",False),
        ("dante.list_self_activity_timeline_undo(uuid,uuid)",True),
    ):
        db.exec_driver_sql(f"ALTER FUNCTION {name} OWNER TO dante_owner")
        db.exec_driver_sql(
            f"REVOKE ALL ON FUNCTION {name} FROM PUBLIC,dante_migrator,dante_runtime"
        )
        if direct:
            db.exec_driver_sql(f"GRANT EXECUTE ON FUNCTION {name} TO dante_runtime")


def downgrade() -> None:
    raise RuntimeError("Coordinated Activity Undo is forward-only")
