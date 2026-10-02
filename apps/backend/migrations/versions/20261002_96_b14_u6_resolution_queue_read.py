"""B14-U6 bounded read over current B10 reconciliation truth.

No queue storage is created. A SECURITY DEFINER projection preserves the B10
default-deny table grants and exposes only authenticated self-owned subjects.
"""

from collections.abc import Sequence

from alembic import op

revision: str = "20261002_96"
down_revision: str | None = "20261001_95"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_SIGNATURE = "dante.list_self_resolution_queue(uuid)"


def upgrade() -> None:
    op.get_bind().exec_driver_sql("""
CREATE FUNCTION dante.list_self_resolution_queue(requested_self_person_ref uuid)
RETURNS TABLE(
    subject_kind text,
    subject_ref uuid,
    title text,
    reconciliation_ref uuid,
    outcome_ref uuid,
    purpose_code text
)
LANGUAGE sql SECURITY DEFINER STABLE PARALLEL UNSAFE
SET search_path = pg_catalog, dante, pg_temp
AS $function$
    SELECT CASE WHEN activity.activity_ref IS NOT NULL
                THEN 'activity' ELSE 'event' END AS subject_kind,
           actual.subject_native_ref AS subject_ref,
           COALESCE(activity.title, event.title) AS title,
           reconciliation.reconciliation_ref,
           reconciliation.outcome_ref,
           reconciliation.purpose_code
      FROM dante.outcome_reconciliation AS reconciliation
      JOIN dante.outcome_reconciliation_current_history AS current_reconciliation
        ON current_reconciliation.reconciliation_ref = reconciliation.reconciliation_ref
       AND current_reconciliation.current_until_at IS NULL
      JOIN dante.outcome_reconciliation_state AS state
        ON state.material_state_ref = current_reconciliation.material_state_ref
       AND state.reconciliation_ref = reconciliation.reconciliation_ref
      JOIN dante.outcome_disposition_current_history AS current_outcome
        ON current_outcome.outcome_ref = reconciliation.outcome_ref
       AND current_outcome.material_state_ref = reconciliation.outcome_disposition_material_state_ref
       AND current_outcome.current_until_at IS NULL
      JOIN dante.outcome_disposition_state AS disposition
        ON disposition.material_state_ref = current_outcome.material_state_ref
      JOIN dante.outcome AS outcome
        ON outcome.outcome_ref = reconciliation.outcome_ref
      JOIN dante.actual AS actual
        ON actual.actual_ref = outcome.actual_ref
      JOIN dante.actual_realization_current_history AS current_actual
        ON current_actual.actual_ref = actual.actual_ref
       AND current_actual.material_state_ref = disposition.actual_realization_material_state_ref
       AND current_actual.current_until_at IS NULL
 LEFT JOIN dante.activity_intention AS activity
        ON activity.activity_ref = actual.subject_native_ref
       AND activity.self_person_ref = requested_self_person_ref
 LEFT JOIN dante.event_expectation AS event
        ON event.event_ref = actual.subject_native_ref
       AND event.self_person_ref = requested_self_person_ref
     WHERE state.action_code = 'unresolved'
       AND (activity.activity_ref IS NOT NULL OR event.event_ref IS NOT NULL)
  ORDER BY current_reconciliation.current_from_at DESC,
           reconciliation.reconciliation_ref
$function$;
""")
    op.get_bind().exec_driver_sql(f"ALTER FUNCTION {_SIGNATURE} OWNER TO dante_owner")
    op.get_bind().exec_driver_sql(
        f"REVOKE ALL ON FUNCTION {_SIGNATURE} FROM PUBLIC, dante_runtime, dante_migrator"
    )
    op.get_bind().exec_driver_sql(
        f"GRANT EXECUTE ON FUNCTION {_SIGNATURE} TO dante_runtime"
    )


def downgrade() -> None:
    raise RuntimeError("B14-U6 queue read requires a reviewed forward migration")
