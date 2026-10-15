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


_COORDINATED_UNDO = r"""
CREATE FUNCTION dante.undo_self_activity_timeline(
    requested_actor uuid, requested_operation text, requested_fingerprint text,
    requested_schedule uuid, requested_removed_operation text,
    requested_next_state uuid, requested_activity uuid,
    requested_session_fingerprint text
) RETURNS TABLE(
    schedule_ref uuid, restored_from_material_state_ref uuid,
    material_state_ref uuid, placement_payload jsonb, created_at timestamptz,
    replayed boolean
)
LANGUAGE plpgsql SECURITY DEFINER VOLATILE PARALLEL UNSAFE
SET search_path=pg_catalog,dante,pg_temp
AS $coordinated$
DECLARE checked_role text;
BEGIN
    -- Guard both identity and concurrent Session state in the SQL admission.
    PERFORM 1 FROM dante.activity_intention AS owned
     WHERE owned.activity_ref=requested_activity
       AND owned.self_person_ref=requested_actor
       AND owned.retired_at IS NULL
     FOR UPDATE;
    IF NOT FOUND THEN
        RAISE EXCEPTION USING ERRCODE='23503',
          CONSTRAINT='activity_timeline_undo_unavailable';
    END IF;
    SELECT role.role_code INTO checked_role
      FROM dante.schedule AS schedule
      JOIN dante.get_self_activity_schedule_roles(
          requested_actor,ARRAY[requested_activity]
      ) AS role ON role.schedule_ref=schedule.schedule_ref
     WHERE schedule.schedule_ref=requested_schedule
       AND schedule.subject_native_ref=requested_activity
       AND role.role_code IN ('envelope','interval');
    IF checked_role IS NULL
       OR requested_session_fingerprint IS DISTINCT FROM
          dante.get_self_activity_session_impact_hash(
              requested_actor,requested_activity
          )
    THEN
        RAISE EXCEPTION USING ERRCODE='23505',
           CONSTRAINT='activity_timeline_undo_stale';
    END IF;
    IF EXISTS (
      SELECT 1 FROM dante.get_self_schedule_placement_lock(
          requested_actor,requested_schedule
      ) AS placement WHERE placement.locked
    ) THEN
       RAISE EXCEPTION USING ERRCODE='23505',
         CONSTRAINT='activity_timeline_undo_locked';
    END IF;
    IF checked_role='envelope' AND EXISTS (
      SELECT 1
        FROM dante.get_self_activity_schedule_roles(
          requested_actor,ARRAY[requested_activity]
        ) AS role
        JOIN dante.schedule_current_placement AS placement
          ON placement.scoped_owner_ref=role.schedule_ref
       WHERE role.role_code='interval'
    ) THEN
       RAISE EXCEPTION USING ERRCODE='23505',
          CONSTRAINT='activity_timeline_undo_envelope_conflict';
    END IF;
    RETURN QUERY
      SELECT * FROM dante.undo_self_activity_schedule_coordinated(
          requested_actor,requested_operation,requested_fingerprint,
          requested_schedule,requested_removed_operation,requested_next_state
      );
END;
$coordinated$;
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
    db.exec_driver_sql(_COORDINATED_UNDO)
    for name, direct in (
        (f"{new_name}(uuid,text,text,uuid,text,uuid)",False),
        ("dante.list_self_activity_timeline_undo(uuid,uuid)",True),
        ("dante.undo_self_activity_timeline(uuid,text,text,uuid,text,uuid,uuid,text)",True),
    ):
        db.exec_driver_sql(f"ALTER FUNCTION {name} OWNER TO dante_owner")
        db.exec_driver_sql(
            f"REVOKE ALL ON FUNCTION {name} FROM PUBLIC,dante_migrator,dante_runtime"
        )
        if direct:
            db.exec_driver_sql(f"GRANT EXECUTE ON FUNCTION {name} TO dante_runtime")


def downgrade() -> None:
    raise RuntimeError("Coordinated Activity Undo is forward-only")
