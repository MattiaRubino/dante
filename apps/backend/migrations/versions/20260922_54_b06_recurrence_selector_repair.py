# ruff: noqa: S608
"""B06-B: forward repair for Recurrence calendar selector validation.

Revision ID: 20260922_54
Revises: 20260922_53
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260922_54"
down_revision: str | None = "20260922_53"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_OWNER = "dante_owner"
_RUNTIME = "dante_runtime"
_MIGRATOR = "dante_migrator"


def _sql(statement: str) -> None:
    op.execute(sa.text(statement))


def _replace_function(prefix: str, owner: str, owner_scope: str) -> str:
    """Build one strongly-typed owner-specific mutation capability."""
    return rf'''
CREATE OR REPLACE FUNCTION dante.replace_self_{prefix}_recurrence(
  requested_self_person_ref uuid, requested_operation_id text, requested_intent_fingerprint text,
  requested_{owner} uuid, requested_expected_material_state_ref uuid,
  requested_family_code text, requested_range_kind text, requested_expected_occurrence_count integer,
  requested_effective_from_date date, requested_effective_until_date date,
  requested_effective_from_instant timestamptz, requested_effective_until_instant timestamptz,
  requested_calendar_pattern_code text, requested_calendar_interval_count integer,
  requested_calendar_clock_basis_code text, requested_calendar_zone_id text,
  requested_calendar_step_unit_code text, requested_calendar_pattern_anchor_date date,
  requested_calendar_wall_times time[], requested_calendar_weekdays smallint[],
  requested_calendar_month_days smallint[], requested_calendar_ordinal_weekdays smallint[],
  requested_calendar_ordinals smallint[], requested_calendar_year_months smallint[],
  requested_calendar_year_month_days smallint[],
  requested_dst_nonexistent_local_time_policy text, requested_dst_ambiguous_local_time_policy text,
  requested_elapsed_seconds numeric, requested_elapsed_anchor_mode_code text,
  requested_elapsed_anchor_at timestamptz,
  requested_quota_count integer, requested_quota_period_unit_code text,
  requested_quota_period_span integer, requested_quota_frame_code text,
  requested_quota_zone_id text, requested_quota_week_start smallint,
  requested_cyclic_cycle_length integer, requested_cyclic_position_unit_code text,
  requested_cyclic_pattern_anchor_date date, requested_cyclic_generates_expected boolean[]
) RETURNS TABLE(material_state_ref uuid, accepted_at timestamptz, replayed boolean)
LANGUAGE plpgsql SECURITY DEFINER VOLATILE PARALLEL UNSAFE
SET search_path = pg_catalog, dante, pg_temp AS $function$
#variable_conflict error
DECLARE
  key text := btrim(requested_operation_id); recorded_at timestamptz := statement_timestamp();
  prior record; current_state uuid; new_state uuid := uuidv7();
  selector_count integer; i integer;
BEGIN
  IF key IS NULL OR key='' OR char_length(key)>200
     OR requested_intent_fingerprint IS NULL OR requested_intent_fingerprint !~ '^[0-9a-f]{{64}}$'
     OR requested_family_code NOT IN ('calendar_wall_clock','elapsed_interval','quota_per_period','cyclic_positional')
     OR requested_range_kind NOT IN ('open','until_boundary','expected_count')
     OR (requested_range_kind='expected_count' AND (requested_expected_occurrence_count IS NULL OR requested_expected_occurrence_count<=0))
     OR (requested_range_kind<>'expected_count' AND requested_expected_occurrence_count IS NOT NULL)
  THEN RAISE EXCEPTION USING ERRCODE='23514', MESSAGE='Recurrence command rejected'; END IF;
  PERFORM 1 FROM dante.person p WHERE p.person_ref=requested_self_person_ref FOR UPDATE;
  IF NOT FOUND OR NOT EXISTS (SELECT 1 FROM dante.account_application_context c WHERE c.self_person_ref=requested_self_person_ref) THEN
    RAISE EXCEPTION USING ERRCODE='23503', MESSAGE='Recurrence self context unavailable';
  END IF;
  SELECT * INTO prior FROM dante.{prefix}_recurrence_operation o
   WHERE o.self_person_ref=requested_self_person_ref AND o.operation_id=key;
  IF FOUND THEN
    IF prior.intent_fingerprint<>requested_intent_fingerprint OR prior.{owner}<>requested_{owner}
       OR prior.expected_material_state_ref IS DISTINCT FROM requested_expected_material_state_ref THEN
      RAISE EXCEPTION USING ERRCODE='23505', CONSTRAINT='pk_{prefix}_recurrence_operation', MESSAGE='Recurrence operation id reused';
    END IF;
    RETURN QUERY SELECT prior.accepted_material_state_ref,prior.accepted_at,true; RETURN;
  END IF;
  IF NOT EXISTS (SELECT 1 FROM dante.{owner_scope} x WHERE x.{owner}=requested_{owner} AND x.self_person_ref=requested_self_person_ref) THEN
    RAISE EXCEPTION USING ERRCODE='23503', CONSTRAINT='{prefix}_recurrence_unavailable', MESSAGE='Recurrence owner unavailable';
  END IF;
  SELECT n.material_state_ref INTO current_state FROM dante.native_current_material_state n
   WHERE n.native_owner_ref=requested_{owner} AND n.facet_code='{prefix}.recurrence' FOR UPDATE;
  IF current_state IS DISTINCT FROM requested_expected_material_state_ref THEN
    RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT='{prefix}_recurrence_state_conflict', MESSAGE='Recurrence state changed';
  END IF;
  IF requested_family_code='calendar_wall_clock' THEN
    IF requested_calendar_pattern_code NOT IN ('daily','weekly_weekdays','monthly_month_days','monthly_ordinal_weekdays','yearly_month_days','anchor_step')
       OR requested_calendar_interval_count IS NULL OR requested_calendar_interval_count<=0
       OR requested_calendar_clock_basis_code NOT IN ('floating_local','named_zone','absolute_utc')
       OR (requested_calendar_clock_basis_code='named_zone' AND (requested_calendar_zone_id IS NULL OR btrim(requested_calendar_zone_id)=''))
       OR (requested_calendar_clock_basis_code<>'named_zone' AND requested_calendar_zone_id IS NOT NULL)
       OR (requested_calendar_pattern_code='anchor_step' AND requested_calendar_step_unit_code NOT IN ('day','week','month','year'))
       OR (requested_calendar_pattern_code<>'anchor_step' AND requested_calendar_step_unit_code IS NOT NULL)
       OR requested_effective_from_date IS NULL OR NOT isfinite(requested_effective_from_date)
       OR requested_effective_from_instant IS NOT NULL OR requested_effective_until_instant IS NOT NULL
       OR (requested_range_kind='until_boundary' AND (requested_effective_until_date IS NULL OR requested_effective_until_date<=requested_effective_from_date))
       OR (requested_range_kind<>'until_boundary' AND requested_effective_until_date IS NOT NULL)
    THEN RAISE EXCEPTION USING ERRCODE='23514', MESSAGE='Calendar Recurrence rejected'; END IF;
    IF requested_calendar_clock_basis_code='named_zone' THEN
      IF requested_dst_nonexistent_local_time_policy<>'skip_civil_candidate'
         OR requested_dst_ambiguous_local_time_policy NOT IN ('earlier','later') THEN
        RAISE EXCEPTION USING ERRCODE='23514', MESSAGE='Named-zone calendar DST policy rejected';
      END IF;
    ELSIF requested_dst_nonexistent_local_time_policy IS NOT NULL OR requested_dst_ambiguous_local_time_policy IS NOT NULL THEN
      RAISE EXCEPTION USING ERRCODE='23514', MESSAGE='DST policy is only valid for named-zone calendar Recurrence';
    END IF;
    IF (requested_calendar_interval_count>1 OR requested_calendar_pattern_code='anchor_step')
       AND (requested_calendar_pattern_anchor_date IS NULL OR NOT isfinite(requested_calendar_pattern_anchor_date)) THEN
      RAISE EXCEPTION USING ERRCODE='23514', MESSAGE='Calendar pattern anchor required';
    END IF;
    IF requested_calendar_interval_count=1 AND requested_calendar_pattern_code<>'anchor_step' AND requested_calendar_pattern_anchor_date IS NOT NULL THEN
      RAISE EXCEPTION USING ERRCODE='23514', MESSAGE='Calendar pattern anchor not admitted';
    END IF;
    IF cardinality(COALESCE(requested_calendar_ordinal_weekdays,ARRAY[]::smallint[])) IS DISTINCT FROM cardinality(COALESCE(requested_calendar_ordinals,ARRAY[]::smallint[]))
       OR cardinality(COALESCE(requested_calendar_year_months,ARRAY[]::smallint[])) IS DISTINCT FROM cardinality(COALESCE(requested_calendar_year_month_days,ARRAY[]::smallint[])) THEN
      RAISE EXCEPTION USING ERRCODE='23514', MESSAGE='Calendar paired selectors rejected';
    END IF;
    IF EXISTS (SELECT 1 FROM unnest(COALESCE(requested_calendar_weekdays,ARRAY[]::smallint[])) v WHERE v NOT BETWEEN 1 AND 7)
       OR EXISTS (SELECT 1 FROM unnest(COALESCE(requested_calendar_month_days,ARRAY[]::smallint[])) v WHERE v NOT BETWEEN -31 AND 31 OR v=0)
       OR EXISTS (SELECT 1 FROM unnest(COALESCE(requested_calendar_ordinal_weekdays,ARRAY[]::smallint[])) v WHERE v NOT BETWEEN 1 AND 7)
       OR EXISTS (SELECT 1 FROM unnest(COALESCE(requested_calendar_ordinals,ARRAY[]::smallint[])) v WHERE v NOT BETWEEN -5 AND 5 OR v=0)
       OR EXISTS (SELECT 1 FROM unnest(COALESCE(requested_calendar_year_months,ARRAY[]::smallint[])) v WHERE v NOT BETWEEN 1 AND 12)
       OR EXISTS (SELECT 1 FROM unnest(COALESCE(requested_calendar_year_month_days,ARRAY[]::smallint[])) v WHERE v NOT BETWEEN -31 AND 31 OR v=0)
    THEN RAISE EXCEPTION USING ERRCODE='23514', MESSAGE='Calendar selector rejected'; END IF;
    SELECT count(*) INTO selector_count FROM (
      SELECT v::text FROM unnest(COALESCE(requested_calendar_weekdays,ARRAY[]::smallint[])) v GROUP BY v HAVING count(*)>1
      UNION ALL SELECT v::text FROM unnest(COALESCE(requested_calendar_month_days,ARRAY[]::smallint[])) v GROUP BY v HAVING count(*)>1
      UNION ALL SELECT w::text||':'||o::text FROM unnest(COALESCE(requested_calendar_ordinal_weekdays,ARRAY[]::smallint[]),COALESCE(requested_calendar_ordinals,ARRAY[]::smallint[])) q(w,o) GROUP BY 1 HAVING count(*)>1
      UNION ALL SELECT m::text||':'||d::text FROM unnest(COALESCE(requested_calendar_year_months,ARRAY[]::smallint[]),COALESCE(requested_calendar_year_month_days,ARRAY[]::smallint[])) q(m,d) GROUP BY 1 HAVING count(*)>1
      UNION ALL SELECT v::text FROM unnest(COALESCE(requested_calendar_wall_times,ARRAY[]::time[])) v GROUP BY v HAVING count(*)>1
    ) duplicate_selector;
    IF selector_count<>0 THEN RAISE EXCEPTION USING ERRCODE='23514', MESSAGE='Calendar selectors must be unique'; END IF;
  ELSIF requested_family_code='elapsed_interval' THEN
    IF requested_elapsed_seconds IS NULL OR requested_elapsed_seconds<=0 OR requested_elapsed_seconds<>trunc(requested_elapsed_seconds,6)
       OR requested_elapsed_anchor_mode_code NOT IN ('fixed_anchor','previous_expected') OR requested_elapsed_anchor_at IS NULL OR NOT isfinite(requested_elapsed_anchor_at)
       OR requested_effective_from_instant IS NULL OR NOT isfinite(requested_effective_from_instant)
       OR requested_effective_from_date IS NOT NULL OR requested_effective_until_date IS NOT NULL
       OR (requested_range_kind='until_boundary' AND (requested_effective_until_instant IS NULL OR requested_effective_until_instant<=requested_effective_from_instant))
       OR (requested_range_kind<>'until_boundary' AND requested_effective_until_instant IS NOT NULL)
    THEN RAISE EXCEPTION USING ERRCODE='23514', MESSAGE='Elapsed Recurrence rejected'; END IF;
  ELSIF requested_family_code='quota_per_period' THEN
    IF requested_range_kind='expected_count' OR requested_quota_count IS NULL OR requested_quota_count<=0
       OR requested_quota_period_unit_code NOT IN ('day','week','month','year') OR requested_quota_period_span IS NULL OR requested_quota_period_span<=0
       OR requested_quota_frame_code NOT IN ('floating_local','named_zone','absolute_utc')
       OR (requested_quota_frame_code='named_zone' AND (requested_quota_zone_id IS NULL OR btrim(requested_quota_zone_id)=''))
       OR (requested_quota_frame_code<>'named_zone' AND requested_quota_zone_id IS NOT NULL)
       OR ((requested_quota_period_unit_code='week') IS DISTINCT FROM (requested_quota_week_start IS NOT NULL))
       OR (requested_quota_week_start IS NOT NULL AND requested_quota_week_start NOT BETWEEN 1 AND 7)
       OR requested_effective_from_date IS NULL OR NOT isfinite(requested_effective_from_date)
       OR requested_effective_from_instant IS NOT NULL OR requested_effective_until_instant IS NOT NULL
       OR (requested_range_kind='until_boundary' AND (requested_effective_until_date IS NULL OR requested_effective_until_date<=requested_effective_from_date))
       OR (requested_range_kind<>'until_boundary' AND requested_effective_until_date IS NOT NULL)
       OR (requested_quota_period_span>1 AND (requested_calendar_pattern_anchor_date IS NULL OR NOT isfinite(requested_calendar_pattern_anchor_date)))
       OR (requested_quota_period_span=1 AND requested_calendar_pattern_anchor_date IS NOT NULL)
    THEN RAISE EXCEPTION USING ERRCODE='23514', MESSAGE='Quota Recurrence rejected'; END IF;
  ELSE
    IF requested_cyclic_cycle_length IS NULL OR requested_cyclic_cycle_length<=0
       OR requested_cyclic_position_unit_code NOT IN ('day','week')
       OR requested_cyclic_pattern_anchor_date IS NULL OR NOT isfinite(requested_cyclic_pattern_anchor_date)
       OR cardinality(requested_cyclic_generates_expected) IS DISTINCT FROM requested_cyclic_cycle_length
       OR requested_effective_from_date IS NULL OR NOT isfinite(requested_effective_from_date)
       OR requested_effective_from_instant IS NOT NULL OR requested_effective_until_instant IS NOT NULL
       OR (requested_range_kind='until_boundary' AND (requested_effective_until_date IS NULL OR requested_effective_until_date<=requested_effective_from_date))
       OR (requested_range_kind<>'until_boundary' AND requested_effective_until_date IS NOT NULL)
    THEN RAISE EXCEPTION USING ERRCODE='23514', MESSAGE='Cyclic Recurrence rejected'; END IF;
  END IF;
  INSERT INTO dante.material_state_address(material_state_ref,native_owner_ref,scoped_owner_ref,facet_code)
  VALUES(new_state,requested_{owner},NULL,'{prefix}.recurrence');
  INSERT INTO dante.{prefix}_recurrence_state(material_state_ref,{owner},family_code,range_kind,expected_occurrence_count)
  VALUES(new_state,requested_{owner},requested_family_code,requested_range_kind,requested_expected_occurrence_count);
  IF requested_family_code='calendar_wall_clock' THEN
    INSERT INTO dante.{prefix}_recurrence_calendar_state(material_state_ref,pattern_code,interval_count,clock_basis_code,zone_id,step_unit_code)
    VALUES(new_state,requested_calendar_pattern_code,requested_calendar_interval_count,requested_calendar_clock_basis_code,requested_calendar_zone_id,requested_calendar_step_unit_code);
    INSERT INTO dante.{prefix}_recurrence_boundary_state(material_state_ref,boundary_role,boundary_kind,inclusive,date_value,local_value,zone_id,instant_value,resolved_at)
    VALUES(new_state,'effective_from','date',true,requested_effective_from_date,NULL,NULL,NULL,NULL);
    IF requested_range_kind='until_boundary' THEN INSERT INTO dante.{prefix}_recurrence_boundary_state VALUES(new_state,'effective_until','date',false,requested_effective_until_date,NULL,NULL,NULL,NULL); END IF;
    IF requested_calendar_pattern_anchor_date IS NOT NULL THEN INSERT INTO dante.{prefix}_recurrence_boundary_state VALUES(new_state,'pattern_anchor','date',NULL,requested_calendar_pattern_anchor_date,NULL,NULL,NULL,NULL); END IF;
    INSERT INTO dante.{prefix}_recurrence_calendar_wall_time(material_state_ref,wall_time) SELECT new_state,v FROM unnest(COALESCE(requested_calendar_wall_times,ARRAY[]::time[])) v;
    INSERT INTO dante.{prefix}_recurrence_calendar_weekday(material_state_ref,weekday_number) SELECT new_state,v FROM unnest(COALESCE(requested_calendar_weekdays,ARRAY[]::smallint[])) v;
    INSERT INTO dante.{prefix}_recurrence_calendar_month_day(material_state_ref,month_day) SELECT new_state,v FROM unnest(COALESCE(requested_calendar_month_days,ARRAY[]::smallint[])) v;
    INSERT INTO dante.{prefix}_recurrence_calendar_ordinal_weekday(material_state_ref,weekday_number,ordinal) SELECT new_state,w,o FROM unnest(COALESCE(requested_calendar_ordinal_weekdays,ARRAY[]::smallint[]),COALESCE(requested_calendar_ordinals,ARRAY[]::smallint[])) q(w,o);
    INSERT INTO dante.{prefix}_recurrence_calendar_year_month_day(material_state_ref,month_number,month_day) SELECT new_state,m,d FROM unnest(COALESCE(requested_calendar_year_months,ARRAY[]::smallint[]),COALESCE(requested_calendar_year_month_days,ARRAY[]::smallint[])) q(m,d);
    IF requested_calendar_clock_basis_code='named_zone' THEN INSERT INTO dante.{prefix}_recurrence_calendar_dst_policy VALUES(new_state,requested_dst_nonexistent_local_time_policy,requested_dst_ambiguous_local_time_policy); END IF;
  ELSIF requested_family_code='elapsed_interval' THEN
    INSERT INTO dante.{prefix}_recurrence_elapsed_state VALUES(new_state,requested_elapsed_seconds,requested_elapsed_anchor_mode_code,requested_elapsed_anchor_at);
    INSERT INTO dante.{prefix}_recurrence_boundary_state VALUES(new_state,'effective_from','absolute_instant',true,NULL,NULL,NULL,requested_effective_from_instant,NULL);
    IF requested_range_kind='until_boundary' THEN INSERT INTO dante.{prefix}_recurrence_boundary_state VALUES(new_state,'effective_until','absolute_instant',false,NULL,NULL,NULL,requested_effective_until_instant,NULL); END IF;
  ELSIF requested_family_code='quota_per_period' THEN
    INSERT INTO dante.{prefix}_recurrence_quota_state VALUES(new_state,requested_quota_count,requested_quota_period_unit_code,requested_quota_period_span,requested_quota_frame_code,requested_quota_zone_id,requested_quota_week_start);
    INSERT INTO dante.{prefix}_recurrence_boundary_state VALUES(new_state,'effective_from','date',true,requested_effective_from_date,NULL,NULL,NULL,NULL);
    IF requested_range_kind='until_boundary' THEN INSERT INTO dante.{prefix}_recurrence_boundary_state VALUES(new_state,'effective_until','date',false,requested_effective_until_date,NULL,NULL,NULL,NULL); END IF;
    IF requested_calendar_pattern_anchor_date IS NOT NULL THEN INSERT INTO dante.{prefix}_recurrence_boundary_state VALUES(new_state,'pattern_anchor','date',NULL,requested_calendar_pattern_anchor_date,NULL,NULL,NULL,NULL); END IF;
  ELSE
    INSERT INTO dante.{prefix}_recurrence_cyclic_state VALUES(new_state,requested_cyclic_cycle_length,requested_cyclic_position_unit_code);
    INSERT INTO dante.{prefix}_recurrence_boundary_state VALUES(new_state,'effective_from','date',true,requested_effective_from_date,NULL,NULL,NULL,NULL);
    IF requested_range_kind='until_boundary' THEN INSERT INTO dante.{prefix}_recurrence_boundary_state VALUES(new_state,'effective_until','date',false,requested_effective_until_date,NULL,NULL,NULL,NULL); END IF;
    INSERT INTO dante.{prefix}_recurrence_boundary_state VALUES(new_state,'pattern_anchor','date',NULL,requested_cyclic_pattern_anchor_date,NULL,NULL,NULL,NULL);
    FOR i IN 1..requested_cyclic_cycle_length LOOP INSERT INTO dante.{prefix}_recurrence_cycle_position VALUES(new_state,i-1,requested_cyclic_generates_expected[i]); END LOOP;
  END IF;
  IF current_state IS NULL THEN
    INSERT INTO dante.native_current_material_state(native_owner_ref,facet_code,material_state_ref) VALUES(requested_{owner},'{prefix}.recurrence',new_state);
  ELSE
    UPDATE dante.{prefix}_recurrence_current_history SET current_until_at=recorded_at WHERE {owner}=requested_{owner} AND current_until_at IS NULL;
    UPDATE dante.native_current_material_state SET material_state_ref=new_state WHERE native_owner_ref=requested_{owner} AND facet_code='{prefix}.recurrence';
  END IF;
  INSERT INTO dante.{prefix}_recurrence_current_history({owner},material_state_ref,current_from_at,current_until_at) VALUES(requested_{owner},new_state,recorded_at,NULL);
  INSERT INTO dante.{prefix}_recurrence_operation(self_person_ref,operation_id,intent_fingerprint,{owner},expected_material_state_ref,accepted_material_state_ref,accepted_at)
  VALUES(requested_self_person_ref,key,requested_intent_fingerprint,requested_{owner},requested_expected_material_state_ref,new_state,recorded_at);
  RETURN QUERY SELECT new_state,recorded_at,false;
END;
$function$;
'''



def upgrade() -> None:
    signature = (
        "uuid,text,text,uuid,uuid,text,text,integer,date,date,timestamptz,timestamptz,"
        "text,integer,text,text,text,date,time[],smallint[],smallint[],smallint[],smallint[],"
        "smallint[],smallint[],text,text,numeric,text,timestamptz,integer,text,integer,text,text,"
        "smallint,integer,text,date,boolean[]"
    )
    for prefix, owner, scope in (
        ("routine", "routine_ref", "routine_intention"),
        ("event", "event_ref", "event_expectation"),
    ):
        _sql(_replace_function(prefix, owner, scope))
        _sql(f"ALTER FUNCTION dante.replace_self_{prefix}_recurrence({signature}) OWNER TO {_OWNER}")
        _sql(f"REVOKE ALL PRIVILEGES ON FUNCTION dante.replace_self_{prefix}_recurrence({signature}) FROM PUBLIC,{_RUNTIME},{_MIGRATOR}")
        _sql(f"GRANT EXECUTE ON FUNCTION dante.replace_self_{prefix}_recurrence({signature}) TO {_RUNTIME}")


def downgrade() -> None:
    raise RuntimeError("B06-B Recurrence selector repair requires a reviewed forward migration")
