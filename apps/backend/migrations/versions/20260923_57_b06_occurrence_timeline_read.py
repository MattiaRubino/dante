"""B06-D: expose bounded self-scoped expected Occurrence Timeline reads.

Revision ID: 20260923_57
Revises: 20260922_56

The runtime keeps zero direct privileges on B06-C Occurrence provenance tables.
Timeline discovery crosses that boundary only through this SECURITY DEFINER
capability; already-scheduled Occurrences continue to use get_self_occurrence.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260923_57"
down_revision: str | None = "20260922_56"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_OWNER = "dante_owner"
_RUNTIME = "dante_runtime"
_MIGRATOR = "dante_migrator"
_SIGNATURE = "uuid,date,date,text"


def _sql(statement: str) -> None:
    op.execute(sa.text(statement))


def upgrade() -> None:
    """Add one bounded execute-only read capability for unscheduled expectations."""
    _sql(
        r"""
CREATE FUNCTION dante.list_self_expected_occurrences_in_window(
  requested_self_person_ref uuid,
  requested_start_date date,
  requested_end_date_exclusive date,
  requested_effective_zone_id text
) RETURNS TABLE(
  occurrence_ref uuid,
  source_native_ref uuid,
  governing_recurrence_state_ref uuid,
  origin_code text,
  family_code text,
  generated_date date,
  generated_wall_time time,
  clock_basis_code text,
  zone_id text,
  resolved_at timestamptz,
  expected_at timestamptz,
  period_start_date date,
  period_end_date_exclusive date,
  frame_code text,
  quota_zone_id text,
  position_index integer,
  skipped boolean,
  skip_reason text,
  skipped_at timestamptz
)
LANGUAGE plpgsql SECURITY DEFINER STABLE PARALLEL RESTRICTED
SET search_path=pg_catalog,dante,pg_temp AS $function$
#variable_conflict error
BEGIN
  IF requested_self_person_ref IS NULL
     OR requested_start_date IS NULL
     OR requested_end_date_exclusive IS NULL
     OR NOT isfinite(requested_start_date)
     OR NOT isfinite(requested_end_date_exclusive)
     OR requested_end_date_exclusive <= requested_start_date
     OR requested_end_date_exclusive - requested_start_date > 62 THEN
    RAISE EXCEPTION USING ERRCODE='22023',
      CONSTRAINT='occurrence_timeline_window_invalid',
      MESSAGE='Occurrence Timeline window must be a finite positive half-open range of at most 62 days';
  END IF;

  IF requested_effective_zone_id IS NULL
     OR requested_effective_zone_id <> btrim(requested_effective_zone_id)
     OR requested_effective_zone_id = ''
     OR char_length(requested_effective_zone_id) > 200
     OR NOT EXISTS (
       SELECT 1
         FROM pg_catalog.pg_timezone_names AS zone
        WHERE zone.name=requested_effective_zone_id
     ) THEN
    RAISE EXCEPTION USING ERRCODE='22023',
      CONSTRAINT='occurrence_timeline_zone_invalid',
      MESSAGE='Occurrence Timeline effective timezone is invalid';
  END IF;

  RETURN QUERY
  SELECT g.occurrence_ref,
         g.source_native_ref,
         g.governing_recurrence_state_ref,
         g.origin_code,
         COALESCE(rs.family_code,es.family_code) AS family_code,
         COALESCE(c.generated_date,cy.generated_date) AS generated_date,
         c.generated_wall_time,
         c.clock_basis_code,
         c.zone_id,
         c.resolved_at,
         e.expected_at,
         q.period_start_date,
         q.period_end_date_exclusive,
         q.frame_code,
         q.zone_id AS quota_zone_id,
         cy.position_index,
         false AS skipped,
         NULL::text AS skip_reason,
         NULL::timestamptz AS skipped_at
    FROM dante.occurrence_generation AS g
    LEFT JOIN dante.routine_recurrence_state AS rs
      ON rs.material_state_ref=g.governing_recurrence_state_ref
    LEFT JOIN dante.event_recurrence_state AS es
      ON es.material_state_ref=g.governing_recurrence_state_ref
    LEFT JOIN dante.occurrence_generation_calendar AS c
      ON c.occurrence_ref=g.occurrence_ref
    LEFT JOIN dante.occurrence_generation_elapsed AS e
      ON e.occurrence_ref=g.occurrence_ref
    LEFT JOIN dante.occurrence_generation_quota AS q
      ON q.occurrence_ref=g.occurrence_ref
    LEFT JOIN dante.occurrence_generation_cyclic AS cy
      ON cy.occurrence_ref=g.occurrence_ref
   WHERE g.origin_code='recurrence_generated'
     AND (
       EXISTS (
         SELECT 1
           FROM dante.routine_intention AS routine
          WHERE routine.routine_ref=g.source_native_ref
            AND routine.self_person_ref=requested_self_person_ref
       )
       OR EXISTS (
         SELECT 1
           FROM dante.event_expectation AS expectation
          WHERE expectation.event_ref=g.source_native_ref
            AND expectation.self_person_ref=requested_self_person_ref
       )
     )
     AND NOT EXISTS (
       SELECT 1
         FROM dante.occurrence_skip AS skip
        WHERE skip.occurrence_ref=g.occurrence_ref
     )
     AND NOT EXISTS (
       SELECT 1
         FROM dante.schedule AS schedule
         JOIN dante.schedule_current_placement AS current
           ON current.scoped_owner_ref=schedule.schedule_ref
        WHERE schedule.subject_native_ref=g.occurrence_ref
     )
     AND (
       (
         c.occurrence_ref IS NOT NULL
         AND c.resolved_at IS NOT NULL
         AND timezone(requested_effective_zone_id,c.resolved_at)::date
               >= requested_start_date
         AND timezone(requested_effective_zone_id,c.resolved_at)::date
               < requested_end_date_exclusive
       )
       OR (
         c.occurrence_ref IS NOT NULL
         AND c.clock_basis_code='absolute_utc'
         AND c.generated_wall_time IS NOT NULL
         AND timezone(
               requested_effective_zone_id,
               (c.generated_date+c.generated_wall_time) AT TIME ZONE 'UTC'
             )::date >= requested_start_date
         AND timezone(
               requested_effective_zone_id,
               (c.generated_date+c.generated_wall_time) AT TIME ZONE 'UTC'
             )::date < requested_end_date_exclusive
       )
       OR (
         c.occurrence_ref IS NOT NULL
         AND c.resolved_at IS NULL
         AND (c.clock_basis_code <> 'absolute_utc' OR c.generated_wall_time IS NULL)
         AND c.generated_date >= requested_start_date
         AND c.generated_date < requested_end_date_exclusive
       )
       OR (
         e.occurrence_ref IS NOT NULL
         AND timezone(requested_effective_zone_id,e.expected_at)::date
               >= requested_start_date
         AND timezone(requested_effective_zone_id,e.expected_at)::date
               < requested_end_date_exclusive
       )
       OR (
         q.occurrence_ref IS NOT NULL
         AND q.period_start_date < requested_end_date_exclusive
         AND q.period_end_date_exclusive > requested_start_date
       )
       OR (
         cy.occurrence_ref IS NOT NULL
         AND cy.generated_date >= requested_start_date
         AND cy.generated_date < requested_end_date_exclusive
       )
     )
   ORDER BY COALESCE(
              c.generated_date,
              timezone(requested_effective_zone_id,e.expected_at)::date,
              q.period_start_date,
              cy.generated_date
            ),
            g.occurrence_ref;
END;
$function$;
"""
    )
    _sql(
        "ALTER FUNCTION dante.list_self_expected_occurrences_in_window"
        f"({_SIGNATURE}) OWNER TO {_OWNER}"
    )
    _sql(
        "REVOKE ALL PRIVILEGES ON FUNCTION "
        f"dante.list_self_expected_occurrences_in_window({_SIGNATURE}) "
        f"FROM PUBLIC,{_RUNTIME},{_MIGRATOR}"
    )
    _sql(
        "GRANT EXECUTE ON FUNCTION "
        f"dante.list_self_expected_occurrences_in_window({_SIGNATURE}) TO {_RUNTIME}"
    )


def downgrade() -> None:
    """Remove only the derived read capability; no canonical history is rewritten."""
    _sql(
        "DROP FUNCTION IF EXISTS "
        f"dante.list_self_expected_occurrences_in_window({_SIGNATURE})"
    )
