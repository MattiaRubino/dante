# ruff: noqa: S608
"""B06-B: forward repair for governed Recurrence current-state readers.

Revision ID: 20260922_53
Revises: 20260922_52
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260922_53"
down_revision: str | None = "20260922_52"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_OWNER = "dante_owner"
_RUNTIME = "dante_runtime"
_MIGRATOR = "dante_migrator"


def _sql(statement: str) -> None:
    op.execute(sa.text(statement))


def _read_function(prefix: str, owner: str, owner_scope: str) -> str:
    return rf'''
CREATE OR REPLACE FUNCTION dante.get_self_{prefix}_recurrence(requested_self_person_ref uuid, requested_{owner} uuid)
RETURNS TABLE(
  material_state_ref uuid, family_code text, range_kind text, expected_occurrence_count integer,
  effective_from_date date, effective_until_date date, effective_from_instant timestamptz, effective_until_instant timestamptz,
  calendar_pattern_code text, calendar_interval_count integer, calendar_clock_basis_code text, calendar_zone_id text, calendar_step_unit_code text, calendar_pattern_anchor_date date,
  calendar_wall_times time[], calendar_weekdays smallint[], calendar_month_days smallint[], calendar_ordinal_weekdays smallint[], calendar_ordinals smallint[], calendar_year_months smallint[], calendar_year_month_days smallint[],
  dst_nonexistent_local_time_policy text, dst_ambiguous_local_time_policy text,
  elapsed_seconds numeric, elapsed_anchor_mode_code text, elapsed_anchor_at timestamptz,
  quota_count integer, quota_period_unit_code text, quota_period_span integer, quota_frame_code text, quota_zone_id text, quota_week_start smallint,
  cyclic_cycle_length integer, cyclic_position_unit_code text, cyclic_pattern_anchor_date date, cyclic_generates_expected boolean[]
)
LANGUAGE plpgsql SECURITY DEFINER STABLE PARALLEL RESTRICTED
SET search_path = pg_catalog, dante, pg_temp AS $function$
#variable_conflict error
BEGIN
  IF NOT EXISTS (SELECT 1 FROM dante.{owner_scope} x WHERE x.{owner}=requested_{owner} AND x.self_person_ref=requested_self_person_ref) THEN
    RAISE EXCEPTION USING ERRCODE='23503', CONSTRAINT='{prefix}_recurrence_unavailable', MESSAGE='Recurrence owner unavailable';
  END IF;
  RETURN QUERY
  SELECT s.material_state_ref,s.family_code,s.range_kind,s.expected_occurrence_count,
    bf.date_value,bu.date_value,bf.instant_value,bu.instant_value,
    c.pattern_code,c.interval_count,c.clock_basis_code,c.zone_id,c.step_unit_code,ba.date_value,
    ARRAY(SELECT w.wall_time FROM dante.{prefix}_recurrence_calendar_wall_time w WHERE w.material_state_ref=s.material_state_ref ORDER BY w.wall_time),
    ARRAY(SELECT w.weekday_number FROM dante.{prefix}_recurrence_calendar_weekday w WHERE w.material_state_ref=s.material_state_ref ORDER BY w.weekday_number),
    ARRAY(SELECT m.month_day FROM dante.{prefix}_recurrence_calendar_month_day m WHERE m.material_state_ref=s.material_state_ref ORDER BY m.month_day),
    ARRAY(SELECT o.weekday_number FROM dante.{prefix}_recurrence_calendar_ordinal_weekday o WHERE o.material_state_ref=s.material_state_ref ORDER BY o.weekday_number,o.ordinal),
    ARRAY(SELECT o.ordinal FROM dante.{prefix}_recurrence_calendar_ordinal_weekday o WHERE o.material_state_ref=s.material_state_ref ORDER BY o.weekday_number,o.ordinal),
    ARRAY(SELECT y.month_number FROM dante.{prefix}_recurrence_calendar_year_month_day y WHERE y.material_state_ref=s.material_state_ref ORDER BY y.month_number,y.month_day),
    ARRAY(SELECT y.month_day FROM dante.{prefix}_recurrence_calendar_year_month_day y WHERE y.material_state_ref=s.material_state_ref ORDER BY y.month_number,y.month_day),
    d.nonexistent_local_time_policy,d.ambiguous_local_time_policy,
    e.elapsed_seconds,e.anchor_mode_code,e.anchor_at,
    q.quota_count,q.period_unit_code,q.period_span,q.frame_code,q.zone_id,q.week_start,
    cy.cycle_length,cy.position_unit_code,ba.date_value,
    ARRAY(SELECT p.generates_expected FROM dante.{prefix}_recurrence_cycle_position p WHERE p.material_state_ref=s.material_state_ref ORDER BY p.position_index)
  FROM dante.{prefix}_recurrence_state s
  JOIN dante.native_current_material_state n ON n.native_owner_ref=s.{owner} AND n.facet_code='{prefix}.recurrence' AND n.material_state_ref=s.material_state_ref
  LEFT JOIN dante.{prefix}_recurrence_boundary_state bf ON bf.material_state_ref=s.material_state_ref AND bf.boundary_role='effective_from'
  LEFT JOIN dante.{prefix}_recurrence_boundary_state bu ON bu.material_state_ref=s.material_state_ref AND bu.boundary_role='effective_until'
  LEFT JOIN dante.{prefix}_recurrence_boundary_state ba ON ba.material_state_ref=s.material_state_ref AND ba.boundary_role='pattern_anchor'
  LEFT JOIN dante.{prefix}_recurrence_calendar_state c ON c.material_state_ref=s.material_state_ref
  LEFT JOIN dante.{prefix}_recurrence_calendar_dst_policy d ON d.material_state_ref=s.material_state_ref
  LEFT JOIN dante.{prefix}_recurrence_elapsed_state e ON e.material_state_ref=s.material_state_ref
  LEFT JOIN dante.{prefix}_recurrence_quota_state q ON q.material_state_ref=s.material_state_ref
  LEFT JOIN dante.{prefix}_recurrence_cyclic_state cy ON cy.material_state_ref=s.material_state_ref
  WHERE s.{owner}=requested_{owner};
END;
$function$;
'''


def upgrade() -> None:
    for prefix, owner, scope in (
        ("routine", "routine_ref", "routine_intention"),
        ("event", "event_ref", "event_expectation"),
    ):
        _sql(_read_function(prefix, owner, scope))
        _sql(f"ALTER FUNCTION dante.get_self_{prefix}_recurrence(uuid,uuid) OWNER TO {_OWNER}")
        _sql(f"REVOKE ALL PRIVILEGES ON FUNCTION dante.get_self_{prefix}_recurrence(uuid,uuid) FROM PUBLIC,{_RUNTIME},{_MIGRATOR}")
        _sql(f"GRANT EXECUTE ON FUNCTION dante.get_self_{prefix}_recurrence(uuid,uuid) TO {_RUNTIME}")


def downgrade() -> None:
    raise RuntimeError("B06-B Recurrence reader repair requires a reviewed forward migration")
