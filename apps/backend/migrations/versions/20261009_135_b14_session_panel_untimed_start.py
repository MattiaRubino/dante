"""Allow explicitly starting an active untimed planned row; preserve provenance.

Revision ID: 20261009_135
Revises: 20261009_134
"""

from collections.abc import Sequence

from alembic import op

revision: str = "20261009_135"
down_revision: str | None = "20261009_134"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # Replace only this owned capability. The original declaration, replay,
    # capture-policy enforcement and Session-link transaction remain unchanged.
    op.get_bind().exec_driver_sql("""
DO $migration$
DECLARE definition text;
        old_join text := '        JOIN dante.schedule_current_placement AS placement
          ON placement.scoped_owner_ref=schedule_row.schedule_ref';
        old_owner text := '          AND activity.self_person_ref=requested_self_person_ref';
BEGIN
    SELECT pg_get_functiondef(
      'dante.start_self_planned_activity_session(uuid,text,text,uuid,uuid,uuid,uuid)'::regprocedure
    ) INTO definition;
    IF strpos(definition,old_join)=0 OR strpos(definition,old_owner)=0 THEN
        RAISE EXCEPTION 'Unexpected planned Session start definition';
    END IF;
    definition := replace(definition,old_join,'');
    definition := replace(definition,old_owner,old_owner || '
          AND activity.retired_at IS NULL
          AND role.retired_at IS NULL
        FOR UPDATE OF activity,role');
    EXECUTE definition;
END;
$migration$;
""")
    bind = op.get_bind()
    bind.exec_driver_sql("""
CREATE FUNCTION dante.list_self_open_activity_sessions(requested_actor uuid)
RETURNS TABLE(activity_ref uuid,session_ref uuid,timing_material_state_ref uuid,
              planned_schedule_ref uuid,paused boolean)
LANGUAGE sql SECURITY DEFINER STABLE PARALLEL RESTRICTED
SET search_path=pg_catalog,dante,pg_temp AS $function$
WITH open_owned AS MATERIALIZED (
    SELECT activity.activity_ref,subject.session_ref,timing.material_state_ref,
           link.schedule_ref
      FROM dante.activity_intention activity
      JOIN dante.session_execution_subject subject ON subject.subject_native_ref=activity.activity_ref
      JOIN dante.session_timing_current_history timing ON timing.session_ref=subject.session_ref
                                                     AND timing.current_until_at IS NULL
      JOIN dante.session_timing_absolute absolute ON absolute.material_state_ref=timing.material_state_ref
      LEFT JOIN dante.session_planned_schedule_link link ON link.session_ref=subject.session_ref
     WHERE activity.self_person_ref=requested_actor AND absolute.ended_at IS NULL
)
SELECT owned.activity_ref,owned.session_ref,owned.material_state_ref,owned.schedule_ref,metrics.paused
  FROM open_owned owned
 CROSS JOIN LATERAL dante.get_self_session_runtime_metrics(
    requested_actor,owned.session_ref,owned.material_state_ref) metrics
$function$;
""")
    bind.exec_driver_sql("""
CREATE FUNCTION dante.list_self_session_panel_inputs(requested_actor uuid)
RETURNS TABLE(activity_ref uuid,title text,mode_code text,schedules jsonb,executions jsonb)
LANGUAGE sql SECURITY DEFINER STABLE PARALLEL RESTRICTED
SET search_path=pg_catalog,dante,pg_temp AS $function$
WITH open_executions AS MATERIALIZED (
  SELECT * FROM dante.list_self_open_activity_sessions(requested_actor)
), owned_activities AS MATERIALIZED (
  SELECT a.activity_ref FROM dante.activity_intention a
   WHERE a.self_person_ref=requested_actor AND a.retired_at IS NULL
), owners AS MATERIALIZED (
  SELECT a.activity_ref,policy.mode_code FROM owned_activities a
  CROSS JOIN LATERAL dante.get_self_activity_execution_policy(requested_actor,a.activity_ref) policy
   WHERE policy.mode_code IN ('live','record_and_live')
      OR a.activity_ref IN (SELECT e.activity_ref FROM open_executions e)
), roles AS MATERIALIZED (
  SELECT role.* FROM dante.get_self_activity_schedule_roles(
    requested_actor, ARRAY(SELECT a.activity_ref FROM owners a)) role
), placements AS MATERIALIZED (
  SELECT s.subject_native_ref AS activity_ref,s.schedule_ref,
         role.role_code,role.presentation_order,role.display_name,
         current.material_state_ref AS placement_material_state_ref,
         state.temporal_form_code AS temporal_form,
         lower(dates.date_span) AS start_date,upper(dates.date_span) AS end_date_exclusive,
         COALESCE(floating.starts_local_at,zoned.starts_local_at) AS starts_local_at,
         COALESCE(floating.ends_local_at,zoned.ends_local_at) AS ends_local_at,
         zoned.zone_id,zoned.resolved_start_at,zoned.resolved_end_at,
         absolute.starts_at,absolute.ends_at,coarse.local_date,coarse.period_code
    FROM owners JOIN dante.schedule s ON s.subject_native_ref=owners.activity_ref
    LEFT JOIN roles role ON role.schedule_ref=s.schedule_ref
    LEFT JOIN dante.schedule_current_placement current ON current.scoped_owner_ref=s.schedule_ref
    LEFT JOIN dante.schedule_placement_state state
      ON state.material_state_ref=current.material_state_ref AND state.schedule_ref=s.schedule_ref
    LEFT JOIN dante.schedule_placement_date_state dates ON dates.material_state_ref=state.material_state_ref
    LEFT JOIN dante.schedule_placement_floating_local_state floating ON floating.material_state_ref=state.material_state_ref
    LEFT JOIN dante.schedule_placement_named_zone_state zoned ON zoned.material_state_ref=state.material_state_ref
    LEFT JOIN dante.schedule_placement_absolute_state absolute ON absolute.material_state_ref=state.material_state_ref
    LEFT JOIN dante.schedule_placement_coarse_local_period_state coarse ON coarse.material_state_ref=state.material_state_ref
   WHERE (current.material_state_ref IS NOT NULL OR role.role_code='planned')
     AND NOT EXISTS (
       SELECT 1 FROM dante.activity_schedule_role retired
        WHERE retired.schedule_ref=s.schedule_ref AND retired.role_code='planned'
          AND retired.retired_at IS NOT NULL
     )
)
SELECT owner.activity_ref,profile.title,owner.mode_code,
       COALESCE((SELECT jsonb_agg(to_jsonb(p)-'activity_ref' ORDER BY p.presentation_order,p.schedule_ref)
                   FROM placements p WHERE p.activity_ref=owner.activity_ref),'[]'::jsonb) AS schedules,
       COALESCE((SELECT jsonb_agg(to_jsonb(e)-'activity_ref' ORDER BY e.session_ref)
                   FROM open_executions e WHERE e.activity_ref=owner.activity_ref),'[]'::jsonb) AS executions
  FROM owners owner
 CROSS JOIN LATERAL dante.get_self_activity_profile(requested_actor,owner.activity_ref) profile
 ORDER BY profile.title,owner.activity_ref
$function$;
""")
    for signature in (
        "dante.list_self_open_activity_sessions(uuid)",
        "dante.list_self_session_panel_inputs(uuid)",
    ):
        bind.exec_driver_sql(f"ALTER FUNCTION {signature} OWNER TO dante_owner")
        bind.exec_driver_sql(f"REVOKE ALL ON FUNCTION {signature} FROM PUBLIC,dante_runtime,dante_migrator")
        bind.exec_driver_sql(f"GRANT EXECUTE ON FUNCTION {signature} TO dante_runtime")


def downgrade() -> None:
    raise RuntimeError("20261009_135 is forward-only: preserve untimed Session provenance")
