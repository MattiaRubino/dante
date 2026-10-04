"""B14-U6: activate Activity Reality review and auto-confirm behavior.

`review_on_end` derives an inbox item only from a bounded real B08 Session.
`auto_confirm_outcome` may attest an already accepted B10 Outcome, but never
creates Actual, Outcome, completion, or other reality by inference.
"""

from collections.abc import Sequence

from alembic import op

revision: str = "20261004_105"
down_revision: str | None = "20261003_104"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_QUEUE_SIGNATURE = "dante.list_self_resolution_queue(uuid)"
_AUTO_SIGNATURE = (
    "dante.apply_self_activity_outcome_review_confirmation("
    "uuid,text,text,uuid,uuid,uuid,uuid)"
)


def _sql(statement: str) -> None:
    op.get_bind().exec_driver_sql(statement)


def upgrade() -> None:
    # The old queue exposed only B10 Reconciliation. Recreate the same named
    # capability with a typed product projection so no queue persistence or
    # second truth is introduced.
    _sql(f"DROP FUNCTION {_QUEUE_SIGNATURE}")
    _sql("""
CREATE FUNCTION dante.list_self_resolution_queue(requested_self_person_ref uuid)
RETURNS TABLE(
    reason_code text,
    subject_kind text,
    subject_ref uuid,
    title text,
    effective_at timestamptz,
    reconciliation_ref uuid,
    outcome_ref uuid,
    purpose_code text,
    session_ref uuid,
    session_timing_material_state_ref uuid
)
LANGUAGE sql SECURITY DEFINER STABLE PARALLEL UNSAFE
SET search_path = pg_catalog, dante, pg_temp
AS $function$
    WITH reconciliation_items AS (
        SELECT 'reconciliation_open'::text AS reason_code,
               CASE WHEN activity.activity_ref IS NOT NULL
                    THEN 'activity' ELSE 'event' END AS subject_kind,
               actual.subject_native_ref AS subject_ref,
               COALESCE(activity.title, event.title) AS title,
               current_reconciliation.current_from_at AS effective_at,
               reconciliation.reconciliation_ref,
               reconciliation.outcome_ref,
               reconciliation.purpose_code,
               NULL::uuid AS session_ref,
               NULL::uuid AS session_timing_material_state_ref
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
    ), latest_bounded_session AS (
        SELECT activity.activity_ref,
               execution.session_ref,
               current_timing.material_state_ref AS session_timing_material_state_ref,
               CASE
                   WHEN timing_state.timing_form_code = 'absolute'
                       THEN absolute_timing.ended_at
                   ELSE current_timing.current_from_at
               END AS effective_at,
               row_number() OVER (
                   PARTITION BY activity.activity_ref
                   ORDER BY
                       CASE
                           WHEN timing_state.timing_form_code = 'absolute'
                               THEN absolute_timing.ended_at
                           ELSE current_timing.current_from_at
                       END DESC,
                       execution.session_ref DESC
               ) AS position
          FROM dante.activity_intention AS activity
          JOIN dante.activity_outcome_review_policy_current_history AS policy_current
            ON policy_current.activity_ref = activity.activity_ref
           AND policy_current.current_until_at IS NULL
          JOIN dante.activity_outcome_review_policy_state AS policy_state
            ON policy_state.activity_ref = policy_current.activity_ref
           AND policy_state.state_ref = policy_current.state_ref
           AND policy_state.mode_code = 'review_on_end'
          JOIN dante.session_execution_subject AS execution
            ON execution.subject_native_ref = activity.activity_ref
          JOIN dante.session_timing_current_history AS current_timing
            ON current_timing.session_ref = execution.session_ref
           AND current_timing.current_until_at IS NULL
          JOIN dante.session_timing_state AS timing_state
            ON timing_state.session_ref = execution.session_ref
           AND timing_state.material_state_ref = current_timing.material_state_ref
     LEFT JOIN dante.session_timing_absolute AS absolute_timing
            ON absolute_timing.material_state_ref = timing_state.material_state_ref
     LEFT JOIN dante.session_timing_elapsed AS elapsed_timing
            ON elapsed_timing.material_state_ref = timing_state.material_state_ref
         WHERE activity.self_person_ref = requested_self_person_ref
           AND (
                (timing_state.timing_form_code = 'absolute'
                 AND absolute_timing.ended_at IS NOT NULL)
                OR
                (timing_state.timing_form_code = 'elapsed_only'
                 AND elapsed_timing.material_state_ref IS NOT NULL)
           )
    ), realization_review_items AS (
        SELECT 'realization_review'::text AS reason_code,
               'activity'::text AS subject_kind,
               activity.activity_ref AS subject_ref,
               activity.title,
               bounded.effective_at,
               NULL::uuid AS reconciliation_ref,
               NULL::uuid AS outcome_ref,
               'activity.policy.review_on_end'::text AS purpose_code,
               bounded.session_ref,
               bounded.session_timing_material_state_ref
          FROM latest_bounded_session AS bounded
          JOIN dante.activity_intention AS activity
            ON activity.activity_ref = bounded.activity_ref
         WHERE bounded.position = 1
           AND NOT EXISTS (
                SELECT 1
                  FROM dante.actual AS actual
                  JOIN dante.actual_realization_current_history AS current_actual
                    ON current_actual.actual_ref = actual.actual_ref
                   AND current_actual.current_until_at IS NULL
                  JOIN dante.actual_realization_session_basis AS basis
                    ON basis.actual_material_state_ref = current_actual.material_state_ref
                 WHERE actual.subject_native_ref = bounded.activity_ref
                   AND basis.session_ref = bounded.session_ref
                   AND basis.session_timing_material_state_ref =
                       bounded.session_timing_material_state_ref
           )
    )
    SELECT * FROM reconciliation_items
    UNION ALL
    SELECT * FROM realization_review_items
    ORDER BY effective_at DESC, subject_ref, reason_code
$function$;
""")
    _sql(f"ALTER FUNCTION {_QUEUE_SIGNATURE} OWNER TO dante_owner")
    _sql(
        f"REVOKE ALL ON FUNCTION {_QUEUE_SIGNATURE} "
        "FROM PUBLIC,dante_runtime,dante_migrator"
    )
    _sql(f"GRANT EXECUTE ON FUNCTION {_QUEUE_SIGNATURE} TO dante_runtime")

    # B10 remains the sole owner of Confirmation creation. This bounded helper
    # only decides whether the existing Confirmation capability is admissible
    # for an Activity whose accepted policy is auto_confirm_outcome.
    _sql("""
CREATE FUNCTION dante.apply_self_activity_outcome_review_confirmation(
    requested_self_person_ref uuid,
    requested_operation_id text,
    requested_intent_fingerprint text,
    requested_outcome_ref uuid,
    requested_outcome_state_ref uuid,
    requested_confirmation_ref uuid,
    requested_state_ref uuid
) RETURNS TABLE(confirmation_ref uuid, applied boolean, replayed boolean)
LANGUAGE plpgsql SECURITY DEFINER VOLATILE PARALLEL UNSAFE
SET search_path = pg_catalog, dante, pg_temp
AS $function$
BEGIN
    IF NOT EXISTS (
        SELECT 1
          FROM dante.outcome AS outcome
          JOIN dante.outcome_disposition_current_history AS current_outcome
            ON current_outcome.outcome_ref = outcome.outcome_ref
           AND current_outcome.material_state_ref = requested_outcome_state_ref
           AND current_outcome.current_until_at IS NULL
          JOIN dante.actual AS actual
            ON actual.actual_ref = outcome.actual_ref
          JOIN dante.activity_intention AS activity
            ON activity.activity_ref = actual.subject_native_ref
           AND activity.self_person_ref = requested_self_person_ref
          JOIN dante.activity_outcome_review_policy_current_history AS policy_current
            ON policy_current.activity_ref = activity.activity_ref
           AND policy_current.current_until_at IS NULL
          JOIN dante.activity_outcome_review_policy_state AS policy_state
            ON policy_state.activity_ref = policy_current.activity_ref
           AND policy_state.state_ref = policy_current.state_ref
         WHERE outcome.outcome_ref = requested_outcome_ref
           AND policy_state.mode_code = 'auto_confirm_outcome'
    ) THEN
        RETURN QUERY SELECT NULL::uuid, false, false;
        RETURN;
    END IF;

    RETURN QUERY
    SELECT accepted.confirmation_ref, true, accepted.replayed
      FROM dante.record_self_outcome_confirmation(
        requested_self_person_ref,
        requested_operation_id,
        requested_intent_fingerprint,
        requested_outcome_ref,
        requested_outcome_state_ref,
        requested_confirmation_ref,
        requested_state_ref,
        NULL,
        'activity.policy.auto',
        'attested'
      ) AS accepted;
END;
$function$;
""")
    _sql(f"ALTER FUNCTION {_AUTO_SIGNATURE} OWNER TO dante_owner")
    _sql(
        f"REVOKE ALL ON FUNCTION {_AUTO_SIGNATURE} "
        "FROM PUBLIC,dante_runtime,dante_migrator"
    )
    _sql(f"GRANT EXECUTE ON FUNCTION {_AUTO_SIGNATURE} TO dante_runtime")


def downgrade() -> None:
    raise RuntimeError("B14-U6 Reality runtime policy requires a reviewed forward migration")
