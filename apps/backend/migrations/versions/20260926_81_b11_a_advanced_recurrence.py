"""B11-A: completion-relative and anchor-stream-relative elapsed recurrence.

Revision ID: 20260926_81
Revises: 20260926_80

B11-A extends the existing elapsed_interval Recurrence family. It does not add a
second Recurrence root or a generic Anchor entity. Dynamic anchors are canonical
Actual MaterialStates, and every generated Occurrence pins the exact Actual
MaterialState used as its anchor.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260926_81"
down_revision: str | None = "20260926_80"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_SCHEMA = "dante"
_RUNTIME = "dante_runtime"
_MIGRATOR = "dante_migrator"
_OWNER = "dante_owner"


def _sql(statement: str) -> None:
    op.get_bind().exec_driver_sql(statement)


def _owner_scope(prefix: str) -> str:
    return "routine_intention" if prefix == "routine" else "event_expectation"


def _owner_column(prefix: str) -> str:
    return "routine_ref" if prefix == "routine" else "event_ref"


def _replace_dynamic_function(prefix: str) -> str:
    owner = _owner_column(prefix)
    owner_scope = _owner_scope(prefix)
    return rf"""
CREATE FUNCTION dante.replace_self_{prefix}_dynamic_elapsed_recurrence(
  requested_self_person_ref uuid,
  requested_operation_id text,
  requested_intent_fingerprint text,
  requested_{owner} uuid,
  requested_expected_material_state_ref uuid,
  requested_range_kind text,
  requested_expected_occurrence_count integer,
  requested_effective_from_instant timestamptz,
  requested_effective_until_instant timestamptz,
  requested_elapsed_seconds numeric,
  requested_anchor_mode_code text,
  requested_anchor_source_family text,
  requested_anchor_source_native_ref uuid
) RETURNS TABLE(material_state_ref uuid, accepted_at timestamptz, replayed boolean)
LANGUAGE plpgsql
SECURITY DEFINER
VOLATILE
PARALLEL UNSAFE
SET search_path=pg_catalog,dante,pg_temp
AS $function$
#variable_conflict error
DECLARE
  key text := btrim(requested_operation_id);
  prior record;
  current_state uuid;
  current_from timestamptz;
  new_state uuid := uuidv7();
  recorded_at timestamptz := statement_timestamp();
BEGIN
  IF key='' OR char_length(key)>200
     OR requested_intent_fingerprint !~ '^[0-9a-f]{{64}}$'
     OR requested_range_kind NOT IN ('open','until_boundary','expected_count')
     OR requested_elapsed_seconds IS NULL OR requested_elapsed_seconds<=0
     OR requested_elapsed_seconds<>trunc(requested_elapsed_seconds,6)
     OR requested_anchor_mode_code NOT IN ('previous_completion','anchor_stream')
     OR requested_effective_from_instant IS NULL
     OR NOT isfinite(requested_effective_from_instant)
     OR (requested_range_kind='until_boundary' AND (
          requested_effective_until_instant IS NULL
          OR NOT isfinite(requested_effective_until_instant)
          OR requested_effective_until_instant<=requested_effective_from_instant
        ))
     OR (requested_range_kind<>'until_boundary' AND requested_effective_until_instant IS NOT NULL)
     OR (requested_range_kind='expected_count' AND (
          requested_expected_occurrence_count IS NULL
          OR requested_expected_occurrence_count<=0
        ))
     OR (requested_range_kind<>'expected_count' AND requested_expected_occurrence_count IS NOT NULL)
     OR (requested_anchor_mode_code='previous_completion' AND (
          requested_anchor_source_family IS NOT NULL
          OR requested_anchor_source_native_ref IS NOT NULL
        ))
     OR (requested_anchor_mode_code='anchor_stream' AND (
          requested_anchor_source_family NOT IN ('routine','event')
          OR requested_anchor_source_native_ref IS NULL
        ))
  THEN
    RAISE EXCEPTION USING ERRCODE='23514',
      CONSTRAINT='{prefix}_dynamic_elapsed_recurrence_input',
      MESSAGE='Dynamic elapsed Recurrence rejected';
  END IF;

  PERFORM 1 FROM dante.person p
   WHERE p.person_ref=requested_self_person_ref FOR UPDATE;
  IF NOT FOUND OR NOT EXISTS (
    SELECT 1 FROM dante.account_application_context c
     WHERE c.self_person_ref=requested_self_person_ref
  ) THEN
    RAISE EXCEPTION USING ERRCODE='23503',
      CONSTRAINT='{prefix}_recurrence_unavailable',
      MESSAGE='Recurrence self context unavailable';
  END IF;

  IF NOT EXISTS (
    SELECT 1 FROM dante.{owner_scope} o
     WHERE o.{owner}=requested_{owner}
       AND o.self_person_ref=requested_self_person_ref
  ) THEN
    RAISE EXCEPTION USING ERRCODE='23503',
      CONSTRAINT='{prefix}_recurrence_unavailable',
      MESSAGE='Recurrence owner unavailable';
  END IF;

  IF requested_anchor_mode_code='anchor_stream' THEN
    IF requested_anchor_source_native_ref=requested_{owner} OR NOT (
      (requested_anchor_source_family='routine' AND EXISTS (
        SELECT 1 FROM dante.routine_intention r
         WHERE r.routine_ref=requested_anchor_source_native_ref
           AND r.self_person_ref=requested_self_person_ref
      )) OR
      (requested_anchor_source_family='event' AND EXISTS (
        SELECT 1 FROM dante.event_expectation e
         WHERE e.event_ref=requested_anchor_source_native_ref
           AND e.self_person_ref=requested_self_person_ref
      ))
    ) THEN
      RAISE EXCEPTION USING ERRCODE='23503',
        CONSTRAINT='{prefix}_advanced_recurrence_anchor_unavailable',
        MESSAGE='Anchor stream unavailable';
    END IF;
  END IF;

  PERFORM pg_advisory_xact_lock(hashtextextended(
    requested_self_person_ref::text || ':recurrence-op:' || key,0));

  SELECT * INTO prior FROM dante.{prefix}_recurrence_operation o
   WHERE o.self_person_ref=requested_self_person_ref
     AND o.operation_id=key;
  IF FOUND THEN
    IF prior.intent_fingerprint<>requested_intent_fingerprint
       OR prior.{owner}<>requested_{owner}
       OR prior.expected_material_state_ref IS DISTINCT FROM requested_expected_material_state_ref THEN
      RAISE EXCEPTION USING ERRCODE='23505',
        CONSTRAINT='pk_{prefix}_recurrence_operation',
        MESSAGE='Recurrence operation id reused';
    END IF;
    RETURN QUERY
    SELECT prior.accepted_material_state_ref,prior.accepted_at,true;
    RETURN;
  END IF;

  SELECT n.material_state_ref,h.current_from_at
    INTO current_state,current_from
    FROM dante.native_current_material_state n
    JOIN dante.{prefix}_recurrence_current_history h
      ON h.{owner}=requested_{owner}
     AND h.material_state_ref=n.material_state_ref
     AND h.current_until_at IS NULL
   WHERE n.native_owner_ref=requested_{owner}
     AND n.facet_code='{prefix}.recurrence'
   FOR UPDATE OF h;

  IF current_state IS DISTINCT FROM requested_expected_material_state_ref THEN
    RAISE EXCEPTION USING ERRCODE='40001',
      CONSTRAINT='{prefix}_recurrence_state_conflict',
      MESSAGE='Recurrence expected current state is stale';
  END IF;

  IF current_from IS NOT NULL AND recorded_at<=current_from THEN
    recorded_at:=current_from + interval '1 microsecond';
  END IF;

  INSERT INTO dante.material_state_address(
    material_state_ref,native_owner_ref,scoped_owner_ref,facet_code
  ) VALUES(new_state,requested_{owner},NULL,'{prefix}.recurrence');

  INSERT INTO dante.{prefix}_recurrence_state(
    material_state_ref,{owner},family_code,range_kind,expected_occurrence_count
  ) VALUES(
    new_state,requested_{owner},'elapsed_interval',requested_range_kind,
    requested_expected_occurrence_count
  );

  INSERT INTO dante.{prefix}_recurrence_elapsed_state(
    material_state_ref,elapsed_seconds,anchor_mode_code,anchor_at
  ) VALUES(
    new_state,requested_elapsed_seconds,requested_anchor_mode_code,NULL
  );

  INSERT INTO dante.{prefix}_recurrence_boundary_state(
    material_state_ref,boundary_role,boundary_kind,inclusive,
    date_value,local_value,zone_id,instant_value,resolved_at
  ) VALUES(
    new_state,'effective_from','absolute_instant',true,
    NULL,NULL,NULL,requested_effective_from_instant,NULL
  );

  IF requested_range_kind='until_boundary' THEN
    INSERT INTO dante.{prefix}_recurrence_boundary_state(
      material_state_ref,boundary_role,boundary_kind,inclusive,
      date_value,local_value,zone_id,instant_value,resolved_at
    ) VALUES(
      new_state,'effective_until','absolute_instant',false,
      NULL,NULL,NULL,requested_effective_until_instant,NULL
    );
  END IF;

  IF requested_anchor_mode_code='anchor_stream' THEN
    INSERT INTO dante.{prefix}_recurrence_elapsed_anchor_source(
      material_state_ref,anchor_source_family,anchor_source_native_ref
    ) VALUES(
      new_state,requested_anchor_source_family,requested_anchor_source_native_ref
    );
  END IF;

  UPDATE dante.{prefix}_recurrence_current_history
     SET current_until_at=recorded_at
   WHERE {owner}=requested_{owner}
     AND current_until_at IS NULL;
  UPDATE dante.native_current_material_state
     SET material_state_ref=new_state
   WHERE native_owner_ref=requested_{owner}
     AND facet_code='{prefix}.recurrence';
  INSERT INTO dante.{prefix}_recurrence_current_history(
    {owner},material_state_ref,current_from_at,current_until_at
  ) VALUES(requested_{owner},new_state,recorded_at,NULL);

  INSERT INTO dante.{prefix}_recurrence_operation(
    self_person_ref,operation_id,intent_fingerprint,{owner},
    expected_material_state_ref,accepted_material_state_ref,accepted_at
  ) VALUES(
    requested_self_person_ref,key,requested_intent_fingerprint,requested_{owner},
    requested_expected_material_state_ref,new_state,recorded_at
  );

  RETURN QUERY SELECT new_state,recorded_at,false;
END;
$function$;
"""


def _anchor_getter(prefix: str) -> str:
    owner = _owner_column(prefix)
    owner_scope = _owner_scope(prefix)
    return rf"""
CREATE FUNCTION dante.get_self_{prefix}_dynamic_elapsed_anchor(
  requested_self_person_ref uuid,
  requested_{owner} uuid
) RETURNS TABLE(
  anchor_mode_code text,
  anchor_source_family text,
  anchor_source_native_ref uuid
)
LANGUAGE plpgsql
SECURITY DEFINER
STABLE
PARALLEL RESTRICTED
SET search_path=pg_catalog,dante,pg_temp
AS $function$
#variable_conflict error
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM dante.{owner_scope} o
     WHERE o.{owner}=requested_{owner}
       AND o.self_person_ref=requested_self_person_ref
  ) THEN
    RAISE EXCEPTION USING ERRCODE='23503',
      CONSTRAINT='{prefix}_recurrence_unavailable',
      MESSAGE='Recurrence owner unavailable';
  END IF;

  RETURN QUERY
  SELECT e.anchor_mode_code,a.anchor_source_family,a.anchor_source_native_ref
    FROM dante.native_current_material_state n
    JOIN dante.{prefix}_recurrence_elapsed_state e
      ON e.material_state_ref=n.material_state_ref
    LEFT JOIN dante.{prefix}_recurrence_elapsed_anchor_source a
      ON a.material_state_ref=e.material_state_ref
   WHERE n.native_owner_ref=requested_{owner}
     AND n.facet_code='{prefix}.recurrence'
     AND e.anchor_mode_code IN ('previous_completion','anchor_stream');
END;
$function$;
"""


def _checkpoint_function(prefix: str) -> str:
    owner = _owner_column(prefix)
    owner_scope = _owner_scope(prefix)
    return rf"""
CREATE FUNCTION dante.checkpoint_self_{prefix}_dynamic_elapsed_occurrences(
  requested_self_person_ref uuid,
  requested_operation_id text,
  requested_intent_fingerprint text,
  requested_source_ref uuid,
  requested_governing_recurrence_state_ref uuid,
  requested_start_at timestamptz,
  requested_end_at_exclusive timestamptz
) RETURNS TABLE(
  accepted_at timestamptz,
  occurrence_ref uuid,
  expected_at timestamptz,
  anchor_occurrence_ref uuid,
  anchor_actual_ref uuid,
  anchor_actual_material_state_ref uuid,
  anchor_completed_at timestamptz,
  created boolean,
  replayed boolean
)
LANGUAGE plpgsql
SECURITY DEFINER
VOLATILE
PARALLEL UNSAFE
SET search_path=pg_catalog,dante,pg_temp
AS $function$
#variable_conflict error
DECLARE
  key text := btrim(requested_operation_id);
  prior record;
  rule record;
  anchor_source_ref uuid;
  anchor_source_family text;
  recorded_at timestamptz := statement_timestamp();
  anchor record;
  expected_value timestamptz;
  generated_ref uuid;
  created_count integer := 0;
  current_count integer := 0;
  prior_result record;
BEGIN
  IF key='' OR char_length(key)>200
     OR requested_intent_fingerprint !~ '^[0-9a-f]{{64}}$'
     OR requested_start_at IS NULL OR requested_end_at_exclusive IS NULL
     OR NOT isfinite(requested_start_at) OR NOT isfinite(requested_end_at_exclusive)
     OR requested_end_at_exclusive<=requested_start_at
     OR requested_end_at_exclusive-requested_start_at>interval '62 days'
  THEN
    RAISE EXCEPTION USING ERRCODE='23514',
      CONSTRAINT='advanced_recurrence_checkpoint_window',
      MESSAGE='Advanced Recurrence checkpoint window rejected';
  END IF;

  IF NOT EXISTS (
    SELECT 1 FROM dante.{owner_scope} o
     WHERE o.{owner}=requested_source_ref
       AND o.self_person_ref=requested_self_person_ref
  ) THEN
    RAISE EXCEPTION USING ERRCODE='23503',
      CONSTRAINT='{prefix}_advanced_recurrence_source_unavailable',
      MESSAGE='Advanced Recurrence source unavailable';
  END IF;

  PERFORM pg_advisory_xact_lock(hashtextextended(
    requested_self_person_ref::text || ':b11a-checkpoint:' || key,0));

  SELECT * INTO prior
    FROM dante.advanced_recurrence_checkpoint_operation o
   WHERE o.self_person_ref=requested_self_person_ref
     AND o.operation_id=key;
  IF FOUND THEN
    IF prior.intent_fingerprint<>requested_intent_fingerprint
       OR prior.source_native_ref<>requested_source_ref
       OR prior.source_family<>'{prefix}'
       OR prior.governing_recurrence_state_ref<>requested_governing_recurrence_state_ref
       OR prior.start_at<>requested_start_at
       OR prior.end_at_exclusive<>requested_end_at_exclusive THEN
      RAISE EXCEPTION USING ERRCODE='23505',
        CONSTRAINT='pk_advanced_recurrence_checkpoint_operation',
        MESSAGE='Advanced Recurrence checkpoint operation id reused';
    END IF;

    FOR prior_result IN
      SELECT p.*
        FROM dante.advanced_recurrence_checkpoint_result p
       WHERE p.self_person_ref=requested_self_person_ref
         AND p.operation_id=key
       ORDER BY p.occurrence_ref
    LOOP
      RETURN QUERY
      SELECT prior.accepted_at,p.occurrence_ref,p.expected_at,p.anchor_occurrence_ref,
             p.anchor_actual_ref,p.anchor_actual_material_state_ref,
             p.anchor_completed_at,false,true
        FROM dante.occurrence_generation_actual_anchor p
       WHERE p.occurrence_ref=prior_result.occurrence_ref;
    END LOOP;
    IF NOT FOUND THEN
      RETURN QUERY SELECT prior.accepted_at,NULL::uuid,NULL::timestamptz,NULL::uuid,
        NULL::uuid,NULL::uuid,NULL::timestamptz,false,true;
    END IF;
    RETURN;
  END IF;

  SELECT s.range_kind,s.expected_occurrence_count,
         e.elapsed_seconds,e.anchor_mode_code,
         a.anchor_source_family,a.anchor_source_native_ref,
         bf.instant_value AS effective_from,
         bu.instant_value AS effective_until
    INTO rule
    FROM dante.{prefix}_recurrence_state s
    JOIN dante.{prefix}_recurrence_elapsed_state e
      ON e.material_state_ref=s.material_state_ref
    LEFT JOIN dante.{prefix}_recurrence_elapsed_anchor_source a
      ON a.material_state_ref=s.material_state_ref
    JOIN dante.{prefix}_recurrence_boundary_state bf
      ON bf.material_state_ref=s.material_state_ref
     AND bf.boundary_role='effective_from'
    LEFT JOIN dante.{prefix}_recurrence_boundary_state bu
      ON bu.material_state_ref=s.material_state_ref
     AND bu.boundary_role='effective_until'
   WHERE s.{owner}=requested_source_ref
     AND s.material_state_ref=requested_governing_recurrence_state_ref
     AND s.family_code='elapsed_interval'
     AND e.anchor_mode_code IN ('previous_completion','anchor_stream');

  IF NOT FOUND THEN
    RAISE EXCEPTION USING ERRCODE='23503',
      CONSTRAINT='{prefix}_advanced_recurrence_unavailable',
      MESSAGE='Advanced Recurrence state unavailable';
  END IF;

  IF NOT EXISTS (
    SELECT 1 FROM dante.native_current_material_state n
     WHERE n.native_owner_ref=requested_source_ref
       AND n.facet_code='{prefix}.recurrence'
       AND n.material_state_ref=requested_governing_recurrence_state_ref
  ) THEN
    RAISE EXCEPTION USING ERRCODE='40001',
      CONSTRAINT='{prefix}_advanced_recurrence_state_conflict',
      MESSAGE='Advanced Recurrence state is not current';
  END IF;

  IF rule.anchor_mode_code='previous_completion' THEN
    anchor_source_ref:=requested_source_ref;
    anchor_source_family:='{prefix}';
  ELSE
    anchor_source_ref:=rule.anchor_source_native_ref;
    anchor_source_family:=rule.anchor_source_family;
  END IF;

  IF rule.anchor_mode_code='anchor_stream' AND NOT (
    (anchor_source_family='routine' AND EXISTS (
      SELECT 1 FROM dante.routine_intention r
       WHERE r.routine_ref=anchor_source_ref
         AND r.self_person_ref=requested_self_person_ref
    )) OR
    (anchor_source_family='event' AND EXISTS (
      SELECT 1 FROM dante.event_expectation e
       WHERE e.event_ref=anchor_source_ref
         AND e.self_person_ref=requested_self_person_ref
    ))
  ) THEN
    RAISE EXCEPTION USING ERRCODE='23503',
      CONSTRAINT='{prefix}_advanced_recurrence_anchor_unavailable',
      MESSAGE='Anchor stream unavailable';
  END IF;

  INSERT INTO dante.advanced_recurrence_checkpoint_operation(
    self_person_ref,operation_id,intent_fingerprint,
    source_native_ref,source_family,governing_recurrence_state_ref,
    start_at,end_at_exclusive,accepted_at
  ) VALUES(
    requested_self_person_ref,key,requested_intent_fingerprint,
    requested_source_ref,'{prefix}',requested_governing_recurrence_state_ref,
    requested_start_at,requested_end_at_exclusive,recorded_at
  );

  SELECT count(*) INTO current_count
    FROM dante.occurrence_generation_actual_anchor p
   WHERE p.governing_recurrence_state_ref=requested_governing_recurrence_state_ref;

  FOR anchor IN
    SELECT og.occurrence_ref AS anchor_occurrence_ref,
           act.actual_ref,
           ars.material_state_ref AS actual_material_state_ref,
           timing.ended_at AS completed_at
      FROM dante.occurrence_generation og
      JOIN dante.actual act
        ON act.subject_native_ref=og.occurrence_ref
      JOIN dante.scoped_current_material_state cm
        ON cm.scoped_owner_ref=act.actual_ref
       AND cm.facet_code='actual.realization'
      JOIN dante.actual_realization_state ars
        ON ars.actual_ref=act.actual_ref
       AND ars.material_state_ref=cm.material_state_ref
       AND ars.realization_occurred IS TRUE
      JOIN dante.actual_realization_timing timing
        ON timing.material_state_ref=ars.material_state_ref
       AND timing.extent_code='interval'
       AND timing.ended_at IS NOT NULL
     WHERE og.source_native_ref=anchor_source_ref
       AND NOT EXISTS (
         SELECT 1
           FROM dante.occurrence_generation_actual_anchor prior_anchor
          WHERE prior_anchor.governing_recurrence_state_ref=requested_governing_recurrence_state_ref
            AND prior_anchor.anchor_occurrence_ref=og.occurrence_ref
       )
       AND timing.ended_at + make_interval(secs => rule.elapsed_seconds::double precision) >= requested_start_at
       AND timing.ended_at + make_interval(secs => rule.elapsed_seconds::double precision) < requested_end_at_exclusive
       AND timing.ended_at + make_interval(secs => rule.elapsed_seconds::double precision) >= rule.effective_from
       AND (rule.effective_until IS NULL
            OR timing.ended_at + make_interval(secs => rule.elapsed_seconds::double precision) < rule.effective_until)
       AND (
         rule.anchor_mode_code='anchor_stream'
         OR NOT EXISTS (
           SELECT 1
             FROM dante.occurrence_generation_actual_anchor other
            WHERE other.governing_recurrence_state_ref=requested_governing_recurrence_state_ref
         )
         OR og.occurrence_ref=(
           SELECT last_generated.occurrence_ref
             FROM dante.occurrence_generation_actual_anchor last_generated
            WHERE last_generated.governing_recurrence_state_ref=requested_governing_recurrence_state_ref
            ORDER BY last_generated.expected_at DESC,last_generated.occurrence_ref DESC
            LIMIT 1
         )
       )
     ORDER BY timing.ended_at,og.occurrence_ref
  LOOP
    EXIT WHEN created_count>=10000;
    EXIT WHEN rule.range_kind='expected_count'
              AND current_count+created_count>=rule.expected_occurrence_count;
    IF rule.anchor_mode_code='previous_completion' AND created_count>0 THEN
      EXIT;
    END IF;

    expected_value:=anchor.completed_at + make_interval(secs => rule.elapsed_seconds::double precision);
    generated_ref:=uuidv7();

    INSERT INTO dante.occurrence(occurrence_ref) VALUES(generated_ref);
    INSERT INTO dante.native_address(native_ref,owner_family)
    VALUES(generated_ref,'occurrence');
    INSERT INTO dante.occurrence_generation(
      occurrence_ref,source_native_ref,governing_recurrence_state_ref,origin_code
    ) VALUES(
      generated_ref,requested_source_ref,requested_governing_recurrence_state_ref,
      'recurrence_generated'
    );
    INSERT INTO dante.occurrence_generation_elapsed(occurrence_ref,expected_at)
    VALUES(generated_ref,expected_value);
    INSERT INTO dante.occurrence_generation_actual_anchor(
      occurrence_ref,governing_recurrence_state_ref,relation_code,
      anchor_source_native_ref,anchor_occurrence_ref,
      anchor_actual_ref,anchor_actual_material_state_ref,
      anchor_completed_at,expected_at
    ) VALUES(
      generated_ref,requested_governing_recurrence_state_ref,
      rule.anchor_mode_code,anchor_source_ref,anchor.anchor_occurrence_ref,
      anchor.actual_ref,anchor.actual_material_state_ref,
      anchor.completed_at,expected_value
    );
    INSERT INTO dante.advanced_recurrence_checkpoint_result(
      self_person_ref,operation_id,occurrence_ref
    ) VALUES(requested_self_person_ref,key,generated_ref);

    created_count:=created_count+1;
    RETURN QUERY SELECT recorded_at,generated_ref,expected_value,anchor.anchor_occurrence_ref,
      anchor.actual_ref,anchor.actual_material_state_ref,anchor.completed_at,true,false;
  END LOOP;

  IF created_count=0 THEN
    RETURN QUERY SELECT recorded_at,NULL::uuid,NULL::timestamptz,NULL::uuid,
      NULL::uuid,NULL::uuid,NULL::timestamptz,false,false;
  END IF;
END;
$function$;
"""


def upgrade() -> None:
    for prefix in ("routine", "event"):
        table = f"{prefix}_recurrence_elapsed_state"
        op.drop_constraint(
            f"ck_{table}_anchor_mode", table, schema=_SCHEMA, type_="check"
        )
        op.drop_constraint(
            f"ck_{table}_anchor_at", table, schema=_SCHEMA, type_="check"
        )
        op.alter_column(table, "anchor_at", schema=_SCHEMA, nullable=True)
        op.create_check_constraint(
            f"ck_{table}_anchor_mode",
            table,
            "anchor_mode_code IN ('fixed_anchor','previous_expected','previous_completion','anchor_stream')",
            schema=_SCHEMA,
        )
        op.create_check_constraint(
            f"ck_{table}_anchor_at",
            table,
            "((anchor_mode_code IN ('fixed_anchor','previous_expected') AND anchor_at IS NOT NULL AND isfinite(anchor_at)) OR "
            "(anchor_mode_code IN ('previous_completion','anchor_stream') AND anchor_at IS NULL))",
            schema=_SCHEMA,
        )

        source_table = f"{prefix}_recurrence_elapsed_anchor_source"
        op.create_table(
            source_table,
            sa.Column("material_state_ref", sa.Uuid(), nullable=False),
            sa.Column("anchor_source_family", sa.Text(), nullable=False),
            sa.Column("anchor_source_native_ref", sa.Uuid(), nullable=False),
            sa.CheckConstraint(
                "anchor_source_family IN ('routine','event')",
                name=op.f(f"ck_{source_table}_family"),
            ),
            sa.ForeignKeyConstraint(
                ["material_state_ref"],
                [f"{_SCHEMA}.{table}.material_state_ref"],
                name=op.f(f"fk_{source_table}_elapsed_state"),
                onupdate="NO ACTION",
                ondelete="NO ACTION",
            ),
            sa.ForeignKeyConstraint(
                ["anchor_source_native_ref"],
                [f"{_SCHEMA}.native_address.native_ref"],
                name=op.f(f"fk_{source_table}_native_address"),
                onupdate="NO ACTION",
                ondelete="NO ACTION",
            ),
            sa.PrimaryKeyConstraint(
                "material_state_ref", name=op.f(f"pk_{source_table}")
            ),
            schema=_SCHEMA,
        )

    op.create_table(
        "occurrence_generation_actual_anchor",
        sa.Column("occurrence_ref", sa.Uuid(), nullable=False),
        sa.Column("governing_recurrence_state_ref", sa.Uuid(), nullable=False),
        sa.Column("relation_code", sa.Text(), nullable=False),
        sa.Column("anchor_source_native_ref", sa.Uuid(), nullable=False),
        sa.Column("anchor_occurrence_ref", sa.Uuid(), nullable=False),
        sa.Column("anchor_actual_ref", sa.Uuid(), nullable=False),
        sa.Column("anchor_actual_material_state_ref", sa.Uuid(), nullable=False),
        sa.Column("anchor_completed_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("expected_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint(
            "relation_code IN ('previous_completion','anchor_stream')",
            name=op.f("ck_occurrence_generation_actual_anchor_relation"),
        ),
        sa.CheckConstraint(
            "isfinite(anchor_completed_at) AND isfinite(expected_at) AND expected_at>anchor_completed_at",
            name=op.f("ck_occurrence_generation_actual_anchor_time"),
        ),
        sa.ForeignKeyConstraint(
            ["occurrence_ref"],
            [f"{_SCHEMA}.occurrence_generation.occurrence_ref"],
            name=op.f("fk_occurrence_generation_actual_anchor_generation"),
            onupdate="NO ACTION",
            ondelete="NO ACTION",
        ),
        sa.ForeignKeyConstraint(
            ["governing_recurrence_state_ref"],
            [f"{_SCHEMA}.material_state_address.material_state_ref"],
            name=op.f("fk_occurrence_generation_actual_anchor_recurrence_state"),
            onupdate="NO ACTION",
            ondelete="NO ACTION",
        ),
        sa.ForeignKeyConstraint(
            ["anchor_source_native_ref"],
            [f"{_SCHEMA}.native_address.native_ref"],
            name=op.f("fk_occurrence_generation_actual_anchor_source"),
            onupdate="NO ACTION",
            ondelete="NO ACTION",
        ),
        sa.ForeignKeyConstraint(
            ["anchor_occurrence_ref"],
            [f"{_SCHEMA}.occurrence.occurrence_ref"],
            name=op.f("fk_occurrence_generation_actual_anchor_occurrence"),
            onupdate="NO ACTION",
            ondelete="NO ACTION",
        ),
        sa.ForeignKeyConstraint(
            ["anchor_actual_ref"],
            [f"{_SCHEMA}.actual.actual_ref"],
            name=op.f("fk_occurrence_generation_actual_anchor_actual"),
            onupdate="NO ACTION",
            ondelete="NO ACTION",
        ),
        sa.ForeignKeyConstraint(
            ["anchor_actual_material_state_ref"],
            [f"{_SCHEMA}.actual_realization_state.material_state_ref"],
            name=op.f("fk_occurrence_generation_actual_anchor_actual_state"),
            onupdate="NO ACTION",
            ondelete="NO ACTION",
        ),
        sa.PrimaryKeyConstraint(
            "occurrence_ref", name=op.f("pk_occurrence_generation_actual_anchor")
        ),
        sa.UniqueConstraint(
            "governing_recurrence_state_ref",
            "anchor_occurrence_ref",
            name=op.f("uq_occurrence_generation_actual_anchor_state_anchor"),
        ),
        schema=_SCHEMA,
    )
    op.create_index(
        "ix_occurrence_generation_actual_anchor_state_expected",
        "occurrence_generation_actual_anchor",
        ["governing_recurrence_state_ref", "expected_at", "occurrence_ref"],
        schema=_SCHEMA,
    )

    op.create_table(
        "advanced_recurrence_checkpoint_operation",
        sa.Column("self_person_ref", sa.Uuid(), nullable=False),
        sa.Column("operation_id", sa.Text(), nullable=False),
        sa.Column("intent_fingerprint", sa.Text(), nullable=False),
        sa.Column("source_native_ref", sa.Uuid(), nullable=False),
        sa.Column("source_family", sa.Text(), nullable=False),
        sa.Column("governing_recurrence_state_ref", sa.Uuid(), nullable=False),
        sa.Column("start_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("end_at_exclusive", sa.DateTime(timezone=True), nullable=False),
        sa.Column("accepted_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint(
            "operation_id=btrim(operation_id) AND operation_id<>'' AND char_length(operation_id)<=200",
            name=op.f("ck_advanced_recurrence_checkpoint_operation_id"),
        ),
        sa.CheckConstraint(
            "intent_fingerprint ~ '^[0-9a-f]{64}$'",
            name=op.f("ck_advanced_recurrence_checkpoint_fingerprint"),
        ),
        sa.CheckConstraint(
            "source_family IN ('routine','event')",
            name=op.f("ck_advanced_recurrence_checkpoint_source_family"),
        ),
        sa.CheckConstraint(
            "isfinite(start_at) AND isfinite(end_at_exclusive) AND end_at_exclusive>start_at AND end_at_exclusive-start_at<=interval '62 days'",
            name=op.f("ck_advanced_recurrence_checkpoint_window"),
        ),
        sa.ForeignKeyConstraint(
            ["self_person_ref"],
            [f"{_SCHEMA}.person.person_ref"],
            name=op.f("fk_advanced_recurrence_checkpoint_person"),
            onupdate="NO ACTION",
            ondelete="NO ACTION",
        ),
        sa.ForeignKeyConstraint(
            ["source_native_ref"],
            [f"{_SCHEMA}.native_address.native_ref"],
            name=op.f("fk_advanced_recurrence_checkpoint_source"),
            onupdate="NO ACTION",
            ondelete="NO ACTION",
        ),
        sa.ForeignKeyConstraint(
            ["governing_recurrence_state_ref"],
            [f"{_SCHEMA}.material_state_address.material_state_ref"],
            name=op.f("fk_advanced_recurrence_checkpoint_state"),
            onupdate="NO ACTION",
            ondelete="NO ACTION",
        ),
        sa.PrimaryKeyConstraint(
            "self_person_ref",
            "operation_id",
            name=op.f("pk_advanced_recurrence_checkpoint_operation"),
        ),
        schema=_SCHEMA,
    )

    op.create_table(
        "advanced_recurrence_checkpoint_result",
        sa.Column("self_person_ref", sa.Uuid(), nullable=False),
        sa.Column("operation_id", sa.Text(), nullable=False),
        sa.Column("occurrence_ref", sa.Uuid(), nullable=False),
        sa.ForeignKeyConstraint(
            ["self_person_ref", "operation_id"],
            [
                f"{_SCHEMA}.advanced_recurrence_checkpoint_operation.self_person_ref",
                f"{_SCHEMA}.advanced_recurrence_checkpoint_operation.operation_id",
            ],
            name=op.f("fk_advanced_recurrence_checkpoint_result_operation"),
            onupdate="NO ACTION",
            ondelete="NO ACTION",
        ),
        sa.ForeignKeyConstraint(
            ["occurrence_ref"],
            [f"{_SCHEMA}.occurrence.occurrence_ref"],
            name=op.f("fk_advanced_recurrence_checkpoint_result_occurrence"),
            onupdate="NO ACTION",
            ondelete="NO ACTION",
        ),
        sa.PrimaryKeyConstraint(
            "self_person_ref",
            "operation_id",
            "occurrence_ref",
            name=op.f("pk_advanced_recurrence_checkpoint_result"),
        ),
        schema=_SCHEMA,
    )

    _sql(r"""
CREATE FUNCTION dante.enforce_b11a_recurrence_anchor_shape()
RETURNS trigger
LANGUAGE plpgsql
SECURITY INVOKER
VOLATILE
PARALLEL UNSAFE
SET search_path=pg_catalog,dante,pg_temp
AS $function$
DECLARE
  state_ref uuid := NEW.material_state_ref;
  mode_value text;
  source_count integer;
  source_family text;
  source_ref uuid;
  target_self uuid;
  source_self uuid;
BEGIN
  SELECT e.anchor_mode_code INTO mode_value
    FROM dante.routine_recurrence_elapsed_state e
   WHERE e.material_state_ref=state_ref;
  IF NOT FOUND THEN
    SELECT e.anchor_mode_code INTO mode_value
      FROM dante.event_recurrence_elapsed_state e
     WHERE e.material_state_ref=state_ref;
  END IF;
  IF mode_value IS NULL THEN
    RETURN NEW;
  END IF;

  SELECT count(*)
    INTO source_count
    FROM (
      SELECT anchor_source_family,anchor_source_native_ref
        FROM dante.routine_recurrence_elapsed_anchor_source
       WHERE material_state_ref=state_ref
      UNION ALL
      SELECT anchor_source_family,anchor_source_native_ref
        FROM dante.event_recurrence_elapsed_anchor_source
       WHERE material_state_ref=state_ref
    ) a;

  IF source_count=1 THEN
    SELECT a.anchor_source_family,a.anchor_source_native_ref
      INTO source_family,source_ref
      FROM (
        SELECT anchor_source_family,anchor_source_native_ref
          FROM dante.routine_recurrence_elapsed_anchor_source
         WHERE material_state_ref=state_ref
        UNION ALL
        SELECT anchor_source_family,anchor_source_native_ref
          FROM dante.event_recurrence_elapsed_anchor_source
         WHERE material_state_ref=state_ref
      ) a
     LIMIT 1;
  END IF;

  IF mode_value='anchor_stream' THEN
    IF source_count<>1 THEN
      RAISE EXCEPTION USING ERRCODE='23514',
        CONSTRAINT='b11a_anchor_stream_source_totality',
        MESSAGE='Anchor-stream Recurrence requires exactly one typed anchor source';
    END IF;
  ELSIF source_count<>0 THEN
    RAISE EXCEPTION USING ERRCODE='23514',
      CONSTRAINT='b11a_non_stream_anchor_source_absent',
      MESSAGE='Only anchor-stream Recurrence may carry an external anchor source';
  END IF;

  IF source_count=1 THEN
    IF (SELECT owner_family FROM dante.native_address WHERE native_ref=source_ref)
       IS DISTINCT FROM source_family THEN
      RAISE EXCEPTION USING ERRCODE='23514',
        CONSTRAINT='b11a_anchor_stream_source_family',
        MESSAGE='Anchor stream family does not match canonical Native owner family';
    END IF;

    SELECT self_person_ref INTO target_self
      FROM (
        SELECT r.self_person_ref
          FROM dante.routine_recurrence_state s
          JOIN dante.routine_intention r ON r.routine_ref=s.routine_ref
         WHERE s.material_state_ref=state_ref
        UNION ALL
        SELECT e.self_person_ref
          FROM dante.event_recurrence_state s
          JOIN dante.event_expectation e ON e.event_ref=s.event_ref
         WHERE s.material_state_ref=state_ref
      ) target LIMIT 1;

    IF source_family='routine' THEN
      SELECT self_person_ref INTO source_self
        FROM dante.routine_intention WHERE routine_ref=source_ref;
    ELSE
      SELECT self_person_ref INTO source_self
        FROM dante.event_expectation WHERE event_ref=source_ref;
    END IF;

    IF source_self IS DISTINCT FROM target_self THEN
      RAISE EXCEPTION USING ERRCODE='23514',
        CONSTRAINT='b11a_anchor_stream_self_scope',
        MESSAGE='Anchor stream must belong to the same self context';
    END IF;
  END IF;

  RETURN NEW;
END;
$function$
""")
    for table in (
        "routine_recurrence_elapsed_state",
        "event_recurrence_elapsed_state",
        "routine_recurrence_elapsed_anchor_source",
        "event_recurrence_elapsed_anchor_source",
    ):
        _sql(
            f"""CREATE CONSTRAINT TRIGGER {table}_b11a_anchor_shape
AFTER INSERT OR UPDATE ON dante.{table}
DEFERRABLE INITIALLY DEFERRED
FOR EACH ROW EXECUTE FUNCTION dante.enforce_b11a_recurrence_anchor_shape()"""
        )

    _sql(r"""
CREATE FUNCTION dante.enforce_b11a_actual_anchor_provenance()
RETURNS trigger
LANGUAGE plpgsql
SECURITY INVOKER
VOLATILE
PARALLEL UNSAFE
SET search_path=pg_catalog,dante,pg_temp
AS $function$
DECLARE
  p record;
  actual_subject uuid;
  actual_occurred boolean;
  actual_end timestamptz;
  elapsed_seconds numeric;
  anchor_mode text;
  recurrence_source uuid;
BEGIN
  SELECT * INTO p
    FROM dante.occurrence_generation_actual_anchor
   WHERE occurrence_ref=COALESCE(NEW.occurrence_ref,OLD.occurrence_ref);
  IF NOT FOUND THEN
    RETURN COALESCE(NEW,OLD);
  END IF;

  SELECT a.subject_native_ref,s.realization_occurred,t.ended_at
    INTO actual_subject,actual_occurred,actual_end
    FROM dante.actual a
    JOIN dante.actual_realization_state s
      ON s.actual_ref=a.actual_ref
     AND s.material_state_ref=p.anchor_actual_material_state_ref
    JOIN dante.actual_realization_timing t
      ON t.material_state_ref=s.material_state_ref
   WHERE a.actual_ref=p.anchor_actual_ref;

  IF actual_subject IS DISTINCT FROM p.anchor_occurrence_ref
     OR actual_occurred IS DISTINCT FROM true
     OR actual_end IS DISTINCT FROM p.anchor_completed_at THEN
    RAISE EXCEPTION USING ERRCODE='23514',
      CONSTRAINT='occurrence_generation_actual_anchor_exact_actual',
      MESSAGE='Advanced Recurrence anchor provenance is not an exact qualifying Actual state';
  END IF;

  SELECT g.source_native_ref INTO recurrence_source
    FROM dante.occurrence_generation g
   WHERE g.occurrence_ref=p.occurrence_ref
     AND g.governing_recurrence_state_ref=p.governing_recurrence_state_ref;
  IF recurrence_source IS NULL THEN
    RAISE EXCEPTION USING ERRCODE='23514',
      CONSTRAINT='occurrence_generation_actual_anchor_generation',
      MESSAGE='Advanced Recurrence provenance does not match generation';
  END IF;

  SELECT e.elapsed_seconds,e.anchor_mode_code
    INTO elapsed_seconds,anchor_mode
    FROM dante.routine_recurrence_elapsed_state e
   WHERE e.material_state_ref=p.governing_recurrence_state_ref
  UNION ALL
  SELECT e.elapsed_seconds,e.anchor_mode_code
    FROM dante.event_recurrence_elapsed_state e
   WHERE e.material_state_ref=p.governing_recurrence_state_ref
  LIMIT 1;

  IF anchor_mode IS DISTINCT FROM p.relation_code
     OR p.expected_at IS DISTINCT FROM
        p.anchor_completed_at + make_interval(secs => elapsed_seconds::double precision) THEN
    RAISE EXCEPTION USING ERRCODE='23514',
      CONSTRAINT='occurrence_generation_actual_anchor_relation',
      MESSAGE='Advanced Recurrence anchor relation is inconsistent';
  END IF;

  IF anchor_mode='previous_completion' AND p.anchor_source_native_ref<>recurrence_source THEN
    RAISE EXCEPTION USING ERRCODE='23514',
      CONSTRAINT='occurrence_generation_actual_anchor_completion_source',
      MESSAGE='Completion-relative anchor must belong to the recurrence source';
  END IF;

  RETURN NEW;
END;
$function$
""")
    _sql(r"""
CREATE CONSTRAINT TRIGGER occurrence_generation_actual_anchor_integrity
AFTER INSERT OR UPDATE ON dante.occurrence_generation_actual_anchor
DEFERRABLE INITIALLY DEFERRED
FOR EACH ROW EXECUTE FUNCTION dante.enforce_b11a_actual_anchor_provenance()
""")

    for prefix in ("routine", "event"):
        _sql(_replace_dynamic_function(prefix))
        _sql(_anchor_getter(prefix))
        _sql(_checkpoint_function(prefix))

    for table in (
        "routine_recurrence_elapsed_anchor_source",
        "event_recurrence_elapsed_anchor_source",
        "occurrence_generation_actual_anchor",
        "advanced_recurrence_checkpoint_operation",
        "advanced_recurrence_checkpoint_result",
    ):
        _sql(f"ALTER TABLE dante.{table} OWNER TO {_OWNER}")

    _sql("ALTER FUNCTION dante.enforce_b11a_recurrence_anchor_shape() OWNER TO dante_owner")
    _sql("ALTER FUNCTION dante.enforce_b11a_actual_anchor_provenance() OWNER TO dante_owner")
    for prefix in ("routine", "event"):
        signatures = (
            f"dante.replace_self_{prefix}_dynamic_elapsed_recurrence(uuid,text,text,uuid,uuid,text,integer,timestamptz,timestamptz,numeric,text,text,uuid)",
            f"dante.get_self_{prefix}_dynamic_elapsed_anchor(uuid,uuid)",
            f"dante.checkpoint_self_{prefix}_dynamic_elapsed_occurrences(uuid,text,text,uuid,uuid,timestamptz,timestamptz)",
        )
        for signature in signatures:
            _sql(f"ALTER FUNCTION {signature} OWNER TO {_OWNER}")

    for table in (
        "routine_recurrence_elapsed_anchor_source",
        "event_recurrence_elapsed_anchor_source",
        "occurrence_generation_actual_anchor",
        "advanced_recurrence_checkpoint_operation",
        "advanced_recurrence_checkpoint_result",
    ):
        _sql(
            f"REVOKE ALL PRIVILEGES ON TABLE dante.{table} "
            f"FROM PUBLIC,{_RUNTIME},{_MIGRATOR}"
        )

    _sql(
        "REVOKE ALL ON FUNCTION dante.enforce_b11a_recurrence_anchor_shape() "
        f"FROM PUBLIC,{_RUNTIME},{_MIGRATOR}"
    )
    _sql(
        "REVOKE ALL ON FUNCTION dante.enforce_b11a_actual_anchor_provenance() "
        f"FROM PUBLIC,{_RUNTIME},{_MIGRATOR}"
    )
    for prefix in ("routine", "event"):
        for signature in (
            f"dante.replace_self_{prefix}_dynamic_elapsed_recurrence(uuid,text,text,uuid,uuid,text,integer,timestamptz,timestamptz,numeric,text,text,uuid)",
            f"dante.get_self_{prefix}_dynamic_elapsed_anchor(uuid,uuid)",
            f"dante.checkpoint_self_{prefix}_dynamic_elapsed_occurrences(uuid,text,text,uuid,uuid,timestamptz,timestamptz)",
        ):
            _sql(f"REVOKE ALL ON FUNCTION {signature} FROM PUBLIC,{_MIGRATOR}")
            _sql(f"GRANT EXECUTE ON FUNCTION {signature} TO {_RUNTIME}")


def downgrade() -> None:
    raise RuntimeError("B11-A migration is forward-only.")
