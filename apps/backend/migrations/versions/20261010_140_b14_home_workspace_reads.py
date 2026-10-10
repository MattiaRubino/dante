"""B14 Home Context Rail: bounded, truthful owner-only finished work and Objectives.

Only real ended Sessions and accepted occurred Actuals count as historical work.
Objective work is based on canonical Objective current evaluation, not time passage.
"""
from collections.abc import Sequence

from alembic import op

revision: str = "20261010_140"
down_revision: str | None = "20261010_139"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    bind = op.get_bind()
    for declaration in (_FINISHED, _OBJECTIVES):
        bind.exec_driver_sql(declaration)
    for signature in (
        "dante.list_self_home_finished_work(uuid,integer)",
        "dante.list_self_home_objective_work(uuid,integer)",
    ):
        bind.exec_driver_sql(f"ALTER FUNCTION {signature} OWNER TO dante_owner")
        bind.exec_driver_sql(
            f"REVOKE ALL ON FUNCTION {signature} FROM PUBLIC,dante_runtime,dante_migrator"
        )
        bind.exec_driver_sql(f"GRANT EXECUTE ON FUNCTION {signature} TO dante_runtime")


def downgrade() -> None:
    raise RuntimeError("Bounded owner-only work history needs reviewed forward evolution")


_FINISHED = r"""
CREATE FUNCTION dante.list_self_home_finished_work(actor uuid, max_rows integer)
RETURNS TABLE(
    subject_kind text, subject_ref uuid, title text,
    session_ref uuid, started_at timestamptz, ended_at timestamptz,
    record_kind text
)
LANGUAGE plpgsql SECURITY DEFINER STABLE PARALLEL RESTRICTED
SET search_path=pg_catalog,dante,pg_temp AS $function$
BEGIN
  IF actor IS NULL OR max_rows IS NULL OR max_rows NOT BETWEEN 1 AND 100 THEN
    RAISE EXCEPTION 'Invalid bounded history request' USING ERRCODE='22023';
  END IF;
  RETURN QUERY
  WITH completed AS (
    SELECT 'activity'::text AS kind, activity.activity_ref AS ref,
           activity.title::text AS name, subject.session_ref,
           timing.started_at, timing.ended_at, 'session_ended'::text AS reason
      FROM dante.activity_intention activity
      JOIN dante.session_execution_subject subject
        ON subject.subject_native_ref=activity.activity_ref
      JOIN dante.session_timing_current_history history
        ON history.session_ref=subject.session_ref AND history.current_until_at IS NULL
      JOIN dante.session_timing_absolute timing
        ON timing.material_state_ref=history.material_state_ref
     WHERE activity.self_person_ref=actor
       AND timing.ended_at IS NOT NULL
       AND timing.ended_at >= clock_timestamp()-interval '90 days'
    UNION ALL
    SELECT CASE WHEN event.event_ref IS NOT NULL THEN 'event' ELSE 'activity' END,
           actual.subject_native_ref,
           COALESCE(event.title, activity.title, 'Elementi registrati')::text,
           NULL::uuid,
           timing.started_at, timing.ended_at, 'realization_occurred'::text
      FROM dante.actual actual
      JOIN dante.actual_realization_current_history history
        ON history.actual_ref=actual.actual_ref AND history.current_until_at IS NULL
      JOIN dante.actual_realization_state state
        ON state.material_state_ref=history.material_state_ref
       AND state.realization_occurred=true
      JOIN dante.actual_realization_timing timing
        ON timing.material_state_ref=state.material_state_ref
      LEFT JOIN dante.event_expectation event
        ON event.event_ref=actual.subject_native_ref
       AND event.self_person_ref=actor
      LEFT JOIN dante.activity_intention activity
        ON activity.activity_ref=actual.subject_native_ref
       AND activity.self_person_ref=actor
     WHERE (event.event_ref IS NOT NULL OR activity.activity_ref IS NOT NULL)
       AND timing.ended_at IS NOT NULL
       AND timing.ended_at >= clock_timestamp()-interval '90 days'
  )
  SELECT completed.kind,completed.ref,completed.name,completed.session_ref,
         completed.started_at,completed.ended_at,completed.reason
    FROM completed ORDER BY completed.ended_at DESC,completed.ref
    LIMIT max_rows;
END;
$function$;
"""


_OBJECTIVES = r"""
CREATE FUNCTION dante.list_self_home_objective_work(actor uuid, max_rows integer)
RETURNS TABLE(
    objective_ref uuid, subject_kind text, subject_ref uuid,
    subject_title text, label text, result_kind text, presentation_order integer,
    draft_revision bigint, draft_updated_at timestamptz
)
LANGUAGE plpgsql SECURITY DEFINER STABLE PARALLEL RESTRICTED
SET search_path=pg_catalog,dante,pg_temp AS $function$
BEGIN
  IF actor IS NULL OR max_rows IS NULL OR max_rows NOT BETWEEN 1 AND 100 THEN
    RAISE EXCEPTION 'Invalid bounded Objective request' USING ERRCODE='22023';
  END IF;
  RETURN QUERY
  WITH owners AS MATERIALIZED (
    SELECT objective.objective_ref,objective.subject_kind,
           objective.subject_native_ref,objective.label,objective.result_kind,
           objective.presentation_order,objective.created_at
      FROM dante.temporal_objective objective
     WHERE objective.self_person_ref=actor AND objective.retired_at IS NULL
     ORDER BY objective.created_at DESC,objective.objective_ref
     LIMIT 500
  )
  SELECT o.objective_ref,o.subject_kind,o.subject_native_ref,
         COALESCE(activity.title,event.title,'Occorrenza')::text AS subject_title,
         o.label,o.result_kind,o.presentation_order,
         draft.revision,draft.updated_at
    FROM owners o
    JOIN LATERAL dante.list_self_temporal_objectives(
      actor,o.subject_kind,o.subject_native_ref
    ) current_objective ON current_objective.objective_ref=o.objective_ref
    LEFT JOIN dante.temporal_objective_input_draft draft
      ON draft.objective_ref=o.objective_ref AND draft.owner_person_ref=actor
    LEFT JOIN dante.activity_intention activity
      ON activity.activity_ref=o.subject_native_ref
      AND activity.self_person_ref=actor AND activity.retired_at IS NULL
    LEFT JOIN dante.event_expectation event
      ON event.event_ref=o.subject_native_ref AND event.self_person_ref=actor
   WHERE current_objective.observation_ref IS NULL
     AND (o.subject_kind='occurrence' OR
       activity.activity_ref IS NOT NULL OR event.event_ref IS NOT NULL)
   ORDER BY o.created_at DESC,o.objective_ref
   LIMIT max_rows;
END;
$function$;
"""