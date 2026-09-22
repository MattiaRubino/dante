# ruff: noqa: S608
"""B06-B: governed immutable Recurrence authoring for Routine and Event.

Revision ID: 20260922_52
Revises: 20260921_51
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260922_52"
down_revision: str | None = "20260921_51"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_SCHEMA = "dante"
_OWNER = "dante_owner"
_RUNTIME = "dante_runtime"
_MIGRATOR = "dante_migrator"


def _sql(statement: str) -> None:
    op.execute(sa.text(statement))


def _create_tables() -> None:
    for prefix, owner, owner_table in (
        ("routine", "routine_ref", "routine"),
        ("event", "event_ref", "event"),
    ):
        policy = f"{prefix}_recurrence_calendar_dst_policy"
        state = f"{prefix}_recurrence_state"
        receipt = f"{prefix}_recurrence_operation"
        op.create_table(
            policy,
            sa.Column("material_state_ref", sa.Uuid(), nullable=False),
            sa.Column("nonexistent_local_time_policy", sa.Text(), nullable=False),
            sa.Column("ambiguous_local_time_policy", sa.Text(), nullable=False),
            sa.PrimaryKeyConstraint("material_state_ref", name=op.f(f"pk_{policy}")),
            sa.ForeignKeyConstraint(
                ["material_state_ref"], [f"{_SCHEMA}.{state}.material_state_ref"],
                name=f"fk_{policy}_state", onupdate="NO ACTION", ondelete="NO ACTION", deferrable=False,
            ),
            sa.CheckConstraint(
                "nonexistent_local_time_policy='skip_civil_candidate'",
                name=op.f(f"ck_{policy}_nonexistent"),
            ),
            sa.CheckConstraint(
                "ambiguous_local_time_policy IN ('earlier','later')",
                name=op.f(f"ck_{policy}_ambiguous"),
            ),
            schema=_SCHEMA,
        )
        op.create_table(
            receipt,
            sa.Column("self_person_ref", sa.Uuid(), nullable=False),
            sa.Column("operation_id", sa.Text(), nullable=False),
            sa.Column("intent_fingerprint", sa.Text(), nullable=False),
            sa.Column(owner, sa.Uuid(), nullable=False),
            sa.Column("expected_material_state_ref", sa.Uuid(), nullable=True),
            sa.Column("accepted_material_state_ref", sa.Uuid(), nullable=False),
            sa.Column("accepted_at", sa.DateTime(timezone=True), nullable=False),
            sa.PrimaryKeyConstraint("self_person_ref", "operation_id", name=op.f(f"pk_{receipt}")),
            sa.ForeignKeyConstraint(["self_person_ref"], [f"{_SCHEMA}.person.person_ref"], name=f"fk_{receipt}_person", onupdate="NO ACTION", ondelete="NO ACTION", deferrable=False),
            sa.ForeignKeyConstraint([owner], [f"{_SCHEMA}.{owner_table}.{owner}"], name=f"fk_{receipt}_{owner}", onupdate="NO ACTION", ondelete="NO ACTION", deferrable=False),
            sa.ForeignKeyConstraint(["accepted_material_state_ref"], [f"{_SCHEMA}.{state}.material_state_ref"], name=f"fk_{receipt}_accepted", onupdate="NO ACTION", ondelete="NO ACTION", deferrable=False),
            sa.CheckConstraint("operation_id=btrim(operation_id) AND operation_id<>'' AND char_length(operation_id)<=200", name=op.f(f"ck_{receipt}_operation_id")),
            sa.CheckConstraint("intent_fingerprint ~ '^[0-9a-f]{64}$'", name=op.f(f"ck_{receipt}_fingerprint")),
            schema=_SCHEMA,
        )
        op.create_index(f"ix_{receipt}_{owner}_accepted", receipt, [owner, "accepted_at"], schema=_SCHEMA)
        _sql(f"REVOKE ALL PRIVILEGES ON TABLE {_SCHEMA}.{policy} FROM PUBLIC,{_RUNTIME},{_MIGRATOR}")
        _sql(f"REVOKE ALL PRIVILEGES ON TABLE {_SCHEMA}.{receipt} FROM PUBLIC,{_RUNTIME},{_MIGRATOR}")


_DST_INTEGRITY = r'''
CREATE FUNCTION dante.enforce_recurrence_dst_policy_integrity() RETURNS trigger
LANGUAGE plpgsql SECURITY DEFINER VOLATILE PARALLEL UNSAFE
SET search_path = pg_catalog, dante, pg_temp AS $function$
#variable_conflict error
DECLARE
  state_ref uuid; prefix text; family text; basis text; policy_count bigint;
BEGIN
  state_ref := CASE WHEN TG_OP='DELETE' THEN OLD.material_state_ref ELSE NEW.material_state_ref END;
  IF TG_TABLE_NAME LIKE 'routine_recurrence_%' THEN prefix := 'routine'; ELSE prefix := 'event'; END IF;
  IF prefix='routine' THEN
    SELECT s.family_code,c.clock_basis_code INTO family,basis FROM dante.routine_recurrence_state s
      LEFT JOIN dante.routine_recurrence_calendar_state c ON c.material_state_ref=s.material_state_ref
      WHERE s.material_state_ref=state_ref;
    IF NOT FOUND THEN IF TG_OP='DELETE' THEN RETURN OLD; END IF; RETURN NEW; END IF;
    SELECT count(*) INTO policy_count FROM dante.routine_recurrence_calendar_dst_policy WHERE material_state_ref=state_ref;
  ELSE
    SELECT s.family_code,c.clock_basis_code INTO family,basis FROM dante.event_recurrence_state s
      LEFT JOIN dante.event_recurrence_calendar_state c ON c.material_state_ref=s.material_state_ref
      WHERE s.material_state_ref=state_ref;
    IF NOT FOUND THEN IF TG_OP='DELETE' THEN RETURN OLD; END IF; RETURN NEW; END IF;
    SELECT count(*) INTO policy_count FROM dante.event_recurrence_calendar_dst_policy WHERE material_state_ref=state_ref;
  END IF;
  IF (family='calendar_wall_clock' AND basis='named_zone' AND policy_count<>1)
     OR (NOT (family='calendar_wall_clock' AND basis='named_zone') AND policy_count<>0) THEN
    RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT=TG_NAME,
      MESSAGE='Recurrence DST policy rejected',
      DETAIL='named-zone calendar Recurrence requires exactly one explicit historical DST policy; every other family/basis requires none';
  END IF;
  IF TG_OP='DELETE' THEN RETURN OLD; END IF;
  RETURN NEW;
END;
$function$;
'''


def _create_dst_integrity() -> None:
    _sql(_DST_INTEGRITY)
    for prefix in ("routine", "event"):
        _sql(
            f"CREATE CONSTRAINT TRIGGER ctrg_{prefix}_recurrence_calendar_dst_policy_dst_policy "
            f"AFTER INSERT OR UPDATE OR DELETE ON dante.{prefix}_recurrence_calendar_dst_policy "
            "DEFERRABLE INITIALLY DEFERRED FOR EACH ROW "
            "EXECUTE FUNCTION dante.enforce_recurrence_dst_policy_integrity()"
        )


def _replace_function(prefix: str, owner: str, owner_scope: str) -> str:
    """Build one strongly-typed owner-specific mutation capability."""
    return rf'''
CREATE FUNCTION dante.replace_self_{prefix}_recurrence(
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
      SELECT v FROM unnest(COALESCE(requested_calendar_weekdays,ARRAY[]::smallint[])) v GROUP BY v HAVING count(*)>1
      UNION ALL SELECT v FROM unnest(COALESCE(requested_calendar_month_days,ARRAY[]::smallint[])) v GROUP BY v HAVING count(*)>1
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


def _read_function(prefix: str, owner: str, owner_scope: str) -> str:
    return rf'''
CREATE FUNCTION dante.get_self_{prefix}_recurrence(requested_self_person_ref uuid, requested_{owner} uuid)
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


def _functions() -> None:
    for prefix, owner, scope in (("routine", "routine_ref", "routine_intention"), ("event", "event_ref", "event_expectation")):
        _sql(_replace_function(prefix, owner, scope))
        _sql(_read_function(prefix, owner, scope))
        replace_signature = "uuid,text,text,uuid,uuid,text,text,integer,date,date,timestamptz,timestamptz,text,integer,text,text,text,date,time[],smallint[],smallint[],smallint[],smallint[],smallint[],smallint[],text,text,numeric,text,timestamptz,integer,text,integer,text,text,smallint,integer,text,date,boolean[]"
        _sql(f"ALTER FUNCTION dante.replace_self_{prefix}_recurrence({replace_signature}) OWNER TO {_OWNER}")
        _sql(f"REVOKE ALL PRIVILEGES ON FUNCTION dante.replace_self_{prefix}_recurrence({replace_signature}) FROM PUBLIC,{_RUNTIME},{_MIGRATOR}")
        _sql(f"GRANT EXECUTE ON FUNCTION dante.replace_self_{prefix}_recurrence({replace_signature}) TO {_RUNTIME}")
        _sql(f"ALTER FUNCTION dante.get_self_{prefix}_recurrence(uuid,uuid) OWNER TO {_OWNER}")
        _sql(f"REVOKE ALL PRIVILEGES ON FUNCTION dante.get_self_{prefix}_recurrence(uuid,uuid) FROM PUBLIC,{_RUNTIME},{_MIGRATOR}")
        _sql(f"GRANT EXECUTE ON FUNCTION dante.get_self_{prefix}_recurrence(uuid,uuid) TO {_RUNTIME}")


def upgrade() -> None:
    _create_tables()
    _create_dst_integrity()
    _functions()


def downgrade() -> None:
    raise RuntimeError("B06-B immutable Recurrence authoring requires a reviewed forward migration")
