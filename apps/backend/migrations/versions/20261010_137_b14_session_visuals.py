"""B14: bounded actor-owned real Session timing read for one-card projection."""

from collections.abc import Sequence

from alembic import op

revision: str = "20261010_137"
down_revision: str | None = "20261010_136"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    bind = op.get_bind()
    bind.exec_driver_sql(_VISUALS)
    signature = "dante.list_self_activity_session_visuals(uuid,timestamptz,timestamptz)"
    bind.exec_driver_sql(f"ALTER FUNCTION {signature} OWNER TO dante_owner")
    bind.exec_driver_sql(
        f"REVOKE ALL ON FUNCTION {signature} FROM PUBLIC,dante_runtime,dante_migrator"
    )
    bind.exec_driver_sql(f"GRANT EXECUTE ON FUNCTION {signature} TO dante_runtime")


def downgrade() -> None:
    raise RuntimeError("Historical real Session projection is forward-only")


_VISUALS = r"""
CREATE FUNCTION dante.list_self_activity_session_visuals(
    requested_actor uuid, visible_start_at timestamptz, visible_end_at timestamptz
) RETURNS TABLE(
    activity_ref uuid, session_ref uuid, planned_schedule_ref uuid,
    started_at timestamptz, ended_at timestamptz, pause_ranges jsonb
)
LANGUAGE plpgsql SECURITY DEFINER STABLE PARALLEL RESTRICTED
SET search_path=pg_catalog,dante,pg_temp AS $function$
BEGIN
    IF visible_start_at IS NULL OR visible_end_at IS NULL
       OR visible_start_at>=visible_end_at
       OR visible_end_at-visible_start_at>interval '31 days' THEN
        RAISE EXCEPTION 'Invalid visual read window'
          USING ERRCODE='22023',CONSTRAINT='session_visual_window_invalid';
    END IF;
    RETURN QUERY
    SELECT activity.activity_ref,subject.session_ref,link.schedule_ref,
           absolute_timing.started_at,absolute_timing.ended_at,
           COALESCE((
             SELECT jsonb_agg(jsonb_build_object(
                    'started_at',pause.paused_at,'ended_at',pause.resumed_at
                  ) ORDER BY pause.paused_at)
               FROM dante.session_timing_pause pause
              WHERE pause.material_state_ref=timing.material_state_ref
           ),'[]'::jsonb)
      FROM dante.activity_intention activity
      JOIN dante.session_execution_subject subject
        ON subject.subject_native_ref=activity.activity_ref
      JOIN dante.session_timing_current_history timing
        ON timing.session_ref=subject.session_ref AND timing.current_until_at IS NULL
      JOIN dante.session_timing_absolute absolute_timing
        ON absolute_timing.material_state_ref=timing.material_state_ref
      LEFT JOIN dante.session_planned_schedule_link link
        ON link.session_ref=subject.session_ref
     WHERE activity.self_person_ref=requested_actor
       AND absolute_timing.started_at<visible_end_at
       AND (absolute_timing.ended_at IS NULL OR absolute_timing.ended_at>visible_start_at)
     ORDER BY absolute_timing.started_at DESC,subject.session_ref
     LIMIT 2000;
END;
$function$;
"""