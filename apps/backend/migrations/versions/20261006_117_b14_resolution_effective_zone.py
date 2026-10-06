"""Resolve completed Event reviews in the person's effective IANA zone.

Revision ID: 20261006_117
Revises: 20261006_116

Date spans close at their exclusive upper local midnight; floating intervals
use the same validated effective zone. The inbox remains a derived read model.
"""

from collections.abc import Sequence

from alembic import op

revision: str = "20261006_117"
down_revision: str | None = "20261006_116"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_OLD_SIGNATURE = "dante.list_self_resolution_queue(uuid)"
_SIGNATURE = "dante.list_self_resolution_queue(uuid,text)"


def upgrade() -> None:
    connection = op.get_bind()
    connection.exec_driver_sql(f"DROP FUNCTION {_OLD_SIGNATURE}")
    connection.exec_driver_sql(r"""
CREATE FUNCTION dante.list_self_resolution_queue(
    requested_self_person_ref uuid, requested_effective_zone_id text
)
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
                 AND absolute_timing.ended_at <= now())
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
           AND (
               EXISTS (
                   SELECT 1 FROM dante.reality_review_policy_current_history AS current_policy
                   JOIN dante.reality_review_policy_state AS policy
                     ON policy.state_ref=current_policy.state_ref
                   WHERE current_policy.subject_kind='activity'
                     AND current_policy.subject_native_ref=bounded.activity_ref
                     AND current_policy.current_until_at IS NULL
                     AND policy.mode_code='review_on_end'
               )
               OR (
                   NOT EXISTS (
                       SELECT 1 FROM dante.reality_review_policy_current_history AS current_policy
                        WHERE current_policy.subject_kind='activity'
                          AND current_policy.subject_native_ref=bounded.activity_ref
                          AND current_policy.current_until_at IS NULL
                   )
                   AND EXISTS (
                       SELECT 1 FROM dante.activity_outcome_review_policy_current_history AS current_policy
                       JOIN dante.activity_outcome_review_policy_state AS policy
                         ON policy.activity_ref=current_policy.activity_ref
                        AND policy.state_ref=current_policy.state_ref
                       WHERE current_policy.activity_ref=bounded.activity_ref
                         AND current_policy.current_until_at IS NULL
                         AND policy.mode_code='review_on_end'
                   )
               )
           )
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
    ),
    ended_events AS (
        SELECT event.event_ref AS source_event_ref,
               CASE WHEN direct.event_ref IS NOT NULL THEN 'event'::text
                    ELSE 'occurrence'::text END AS subject_kind,
               schedule.subject_native_ref AS subject_ref,
               event.title,
               COALESCE(
                   absolute_state.ends_at,
                   named_state.resolved_end_at,
                   floating_state.ends_local_at AT TIME ZONE requested_effective_zone_id,
                   upper(date_state.date_span)::timestamp AT TIME ZONE requested_effective_zone_id
               ) AS effective_at,
               row_number() OVER (
                   PARTITION BY schedule.subject_native_ref
                   ORDER BY COALESCE(
                   absolute_state.ends_at,
                   named_state.resolved_end_at,
                   floating_state.ends_local_at AT TIME ZONE requested_effective_zone_id,
                   upper(date_state.date_span)::timestamp AT TIME ZONE requested_effective_zone_id
               ) DESC,
                            schedule.schedule_ref DESC
               ) AS position
          FROM dante.schedule AS schedule
          JOIN dante.schedule_current_placement AS current_placement
            ON current_placement.scoped_owner_ref=schedule.schedule_ref
          JOIN dante.schedule_placement_state AS placement
            ON placement.schedule_ref=schedule.schedule_ref
           AND placement.material_state_ref=current_placement.material_state_ref
     LEFT JOIN dante.schedule_placement_absolute_state AS absolute_state
            ON absolute_state.material_state_ref=placement.material_state_ref
           AND absolute_state.extent_code='interval'
     LEFT JOIN dante.schedule_placement_named_zone_state AS named_state
            ON named_state.material_state_ref=placement.material_state_ref
           AND named_state.extent_code='interval'
     LEFT JOIN dante.schedule_placement_floating_local_state AS floating_state
            ON floating_state.material_state_ref=placement.material_state_ref
           AND floating_state.extent_code='interval'
     LEFT JOIN dante.schedule_placement_date_state AS date_state
            ON date_state.material_state_ref=placement.material_state_ref
     LEFT JOIN dante.event_expectation AS direct
            ON direct.event_ref=schedule.subject_native_ref
           AND direct.self_person_ref=requested_self_person_ref
     LEFT JOIN dante.occurrence_generation AS generation
            ON generation.occurrence_ref=schedule.subject_native_ref
           AND NOT EXISTS (
               SELECT 1 FROM dante.occurrence_skip AS skipped
                WHERE skipped.occurrence_ref=generation.occurrence_ref
           )
          JOIN dante.event_expectation AS event
            ON event.event_ref=COALESCE(direct.event_ref,generation.source_native_ref)
           AND event.self_person_ref=requested_self_person_ref
         WHERE COALESCE(
                   absolute_state.ends_at,
                   named_state.resolved_end_at,
                   floating_state.ends_local_at AT TIME ZONE requested_effective_zone_id,
                   upper(date_state.date_span)::timestamp AT TIME ZONE requested_effective_zone_id
               ) <= now()
    ),
    event_reality_items AS (
        SELECT 'realization_review'::text AS reason_code,
               ended.subject_kind,ended.subject_ref,ended.title,ended.effective_at,
               NULL::uuid AS reconciliation_ref,NULL::uuid AS outcome_ref,
               'event.policy.review_on_end'::text AS purpose_code,
               NULL::uuid AS session_ref,NULL::uuid AS session_timing_material_state_ref
          FROM ended_events AS ended
          JOIN dante.reality_review_policy_current_history AS policy_current
            ON policy_current.subject_kind=ended.subject_kind
           AND policy_current.subject_native_ref=ended.subject_ref
           AND policy_current.current_until_at IS NULL
          JOIN dante.reality_review_policy_state AS policy
            ON policy.state_ref=policy_current.state_ref
           AND policy.mode_code='review_on_end'
         WHERE ended.position=1
           AND NOT EXISTS (
               SELECT 1 FROM dante.actual AS actual
                JOIN dante.actual_realization_current_history AS current_actual
                  ON current_actual.actual_ref=actual.actual_ref
                 AND current_actual.current_until_at IS NULL
               WHERE actual.subject_native_ref=ended.subject_ref
           )
    ),
    objective_review_items AS (
        SELECT 'objective_review'::text AS reason_code,
               'activity'::text AS subject_kind,activity.activity_ref AS subject_ref,
               activity.title,bounded.effective_at,
               NULL::uuid AS reconciliation_ref,NULL::uuid AS outcome_ref,
               'objective.review'::text AS purpose_code,
               bounded.session_ref,bounded.session_timing_material_state_ref
          FROM latest_bounded_session AS bounded
          JOIN dante.activity_intention AS activity
            ON activity.activity_ref=bounded.activity_ref
         WHERE bounded.position=1
           AND EXISTS (
               SELECT 1 FROM dante.temporal_objective AS objective
                WHERE objective.self_person_ref=requested_self_person_ref
                  AND objective.subject_kind='activity'
                  AND objective.subject_native_ref=activity.activity_ref
                  AND NOT EXISTS (
                      SELECT 1 FROM dante.temporal_objective_evaluation_current_history AS evaluation
                       WHERE evaluation.objective_ref=objective.objective_ref
                         AND evaluation.current_until_at IS NULL
                  )
           )
        UNION ALL
        SELECT 'objective_review'::text,ended.subject_kind,ended.subject_ref,
               ended.title,ended.effective_at,
               NULL::uuid,NULL::uuid,'objective.review'::text,NULL::uuid,NULL::uuid
          FROM ended_events AS ended
         WHERE ended.position=1
           AND EXISTS (
               SELECT 1 FROM dante.temporal_objective AS objective
                WHERE objective.self_person_ref=requested_self_person_ref
                  AND objective.subject_kind=ended.subject_kind
                  AND objective.subject_native_ref=ended.subject_ref
                  AND NOT EXISTS (
                      SELECT 1 FROM dante.temporal_objective_evaluation_current_history AS evaluation
                       WHERE evaluation.objective_ref=objective.objective_ref
                         AND evaluation.current_until_at IS NULL
                  )
           )
    )
    SELECT * FROM reconciliation_items
    UNION ALL SELECT * FROM realization_review_items
    UNION ALL SELECT * FROM event_reality_items
    UNION ALL SELECT * FROM objective_review_items
    ORDER BY effective_at DESC, subject_ref, reason_code
$function$;
""")
    connection.exec_driver_sql(f"ALTER FUNCTION {_SIGNATURE} OWNER TO dante_owner")
    connection.exec_driver_sql(
        f"REVOKE ALL ON FUNCTION {_SIGNATURE} FROM PUBLIC,dante_runtime,dante_migrator"
    )
    connection.exec_driver_sql(f"GRANT EXECUTE ON FUNCTION {_SIGNATURE} TO dante_runtime")


def downgrade() -> None:
    raise RuntimeError("20261006_117 requires a reviewed forward migration")
