"""B13-A: self-owned Plan and flat internal Step structure.

Each accepted revision is an immutable normalized snapshot. The explicit
current binding and interval history decide what is current; row order does not.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "20260928_87"
down_revision: str | None = "20260927_86"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_SCHEMA = "dante"
_RUNTIME = "dante_runtime"
_MIGRATOR = "dante_migrator"


def _sql(statement: str) -> None:
    op.get_bind().exec_driver_sql(statement)


def upgrade() -> None:
    op.create_table(
        "plan_intention",
        sa.Column("plan_ref", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("self_person_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["plan_ref"], ["dante.plan.plan_ref"], name="fk_plan_intention_plan"
        ),
        sa.ForeignKeyConstraint(
            ["self_person_ref"], ["dante.person.person_ref"],
            name="fk_plan_intention_person",
        ),
        schema=_SCHEMA,
    )
    op.create_index(
        "ix_plan_intention_self", "plan_intention", ["self_person_ref"], schema=_SCHEMA
    )
    op.create_table(
        "plan_step",
        sa.Column("step_ref", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("plan_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.CheckConstraint(
            "uuid_extract_version(step_ref) IS NOT DISTINCT FROM 7",
            name="ck_plan_step_uuidv7",
        ),
        sa.UniqueConstraint("plan_ref", "step_ref", name="uq_plan_step_owner"),
        sa.ForeignKeyConstraint(
            ["plan_ref"], ["dante.plan_intention.plan_ref"], name="fk_plan_step_plan"
        ),
        schema=_SCHEMA,
    )
    op.create_index("ix_plan_step_plan", "plan_step", ["plan_ref"], schema=_SCHEMA)
    op.create_table(
        "plan_work_state",
        sa.Column("state_ref", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("plan_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("title", sa.Text(), nullable=False),
        sa.Column("recorded_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint(
            "uuid_extract_version(state_ref) IS NOT DISTINCT FROM 7",
            name="ck_plan_work_state_uuidv7",
        ),
        sa.CheckConstraint(
            "title=btrim(title) AND title<>'' AND char_length(title)<=300",
            name="ck_plan_work_state_title",
        ),
        sa.UniqueConstraint("plan_ref", "state_ref", name="uq_plan_work_state_owner"),
        sa.ForeignKeyConstraint(
            ["plan_ref"], ["dante.plan_intention.plan_ref"],
            name="fk_plan_work_state_plan",
        ),
        schema=_SCHEMA,
    )
    op.create_index(
        "ix_plan_work_state_plan", "plan_work_state", ["plan_ref"], schema=_SCHEMA
    )
    op.create_table(
        "plan_step_in_state",
        sa.Column("state_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("plan_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("step_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("position", sa.Integer(), nullable=False),
        sa.Column("title", sa.Text(), nullable=False),
        sa.Column("activity_ref", postgresql.UUID(as_uuid=True), nullable=True),
        sa.PrimaryKeyConstraint(
            "state_ref", "step_ref", name="pk_plan_step_in_state"
        ),
        sa.UniqueConstraint(
            "state_ref", "position", name="uq_plan_step_in_state_position"
        ),
        sa.CheckConstraint(
            "position>=0 AND position<1000", name="ck_plan_step_in_state_position"
        ),
        sa.CheckConstraint(
            "title=btrim(title) AND title<>'' AND char_length(title)<=300",
            name="ck_plan_step_in_state_title",
        ),
        sa.ForeignKeyConstraint(
            ["plan_ref", "state_ref"],
            ["dante.plan_work_state.plan_ref", "dante.plan_work_state.state_ref"],
            name="fk_plan_step_in_state_work",
        ),
        sa.ForeignKeyConstraint(
            ["plan_ref", "step_ref"],
            ["dante.plan_step.plan_ref", "dante.plan_step.step_ref"],
            name="fk_plan_step_in_state_step",
        ),
        sa.ForeignKeyConstraint(
            ["activity_ref"], ["dante.activity.activity_ref"],
            name="fk_plan_step_in_state_activity",
        ),
        schema=_SCHEMA,
    )
    op.create_index(
        "ux_plan_step_in_state_activity", "plan_step_in_state",
        ["state_ref", "activity_ref"], unique=True, schema=_SCHEMA,
        postgresql_where=sa.text("activity_ref IS NOT NULL"),
    )
    op.create_table(
        "plan_current_work_state",
        sa.Column("plan_ref", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("state_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["plan_ref", "state_ref"],
            ["dante.plan_work_state.plan_ref", "dante.plan_work_state.state_ref"],
            name="fk_plan_current_work_state_state",
        ),
        schema=_SCHEMA,
    )
    op.create_table(
        "plan_work_current_history",
        sa.Column("plan_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("state_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("current_from_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("current_until_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint(
            "plan_ref", "current_from_at", name="pk_plan_work_current_history"
        ),
        sa.CheckConstraint(
            "isfinite(current_from_at) AND (current_until_at IS NULL OR "
            "(isfinite(current_until_at) AND current_until_at>current_from_at))",
            name="ck_plan_work_current_history_interval",
        ),
        sa.ForeignKeyConstraint(
            ["plan_ref", "state_ref"],
            ["dante.plan_work_state.plan_ref", "dante.plan_work_state.state_ref"],
            name="fk_plan_work_current_history_state",
        ),
        schema=_SCHEMA,
    )
    op.create_index(
        "ux_plan_work_current_history_open", "plan_work_current_history",
        ["plan_ref"], unique=True, schema=_SCHEMA,
        postgresql_where=sa.text("current_until_at IS NULL"),
    )
    op.create_table(
        "plan_work_operation",
        sa.Column("self_person_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("operation_id", sa.Text(), nullable=False),
        sa.Column("intent_fingerprint", sa.Text(), nullable=False),
        sa.Column("plan_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("state_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint(
            "self_person_ref", "operation_id", name="pk_plan_work_operation"
        ),
        sa.UniqueConstraint("state_ref", name="uq_plan_work_operation_state"),
        sa.CheckConstraint(
            "operation_id=btrim(operation_id) AND operation_id<>'' "
            "AND char_length(operation_id)<=200",
            name="ck_plan_work_operation_id",
        ),
        sa.CheckConstraint(
            "intent_fingerprint ~ '^[0-9a-f]{64}$'",
            name="ck_plan_work_operation_fingerprint",
        ),
        sa.ForeignKeyConstraint(
            ["self_person_ref"], ["dante.person.person_ref"],
            name="fk_plan_work_operation_person",
        ),
        sa.ForeignKeyConstraint(
            ["plan_ref", "state_ref"],
            ["dante.plan_work_state.plan_ref", "dante.plan_work_state.state_ref"],
            name="fk_plan_work_operation_state",
        ),
        schema=_SCHEMA,
    )

    _sql(
        """
CREATE FUNCTION dante.get_self_plan_work(
  requested_self_person_ref uuid, requested_plan_ref uuid
) RETURNS TABLE(
  plan_ref uuid, state_ref uuid, title text, created_at timestamptz,
  steps jsonb
) LANGUAGE sql SECURITY DEFINER STABLE PARALLEL SAFE
SET search_path=pg_catalog,dante,pg_temp
AS $function$
  SELECT owner.plan_ref,state.state_ref,state.title,owner.created_at,
         COALESCE((
           SELECT jsonb_agg(jsonb_build_object(
             'step_ref',item.step_ref,'position',item.position,
             'title',item.title,'activity_ref',item.activity_ref
           ) ORDER BY item.position)
           FROM dante.plan_step_in_state AS item
           WHERE item.state_ref=state.state_ref
         ),'[]'::jsonb)
    FROM dante.plan_intention AS owner
    JOIN dante.plan_current_work_state AS current
      ON current.plan_ref=owner.plan_ref
    JOIN dante.plan_work_current_history AS history
      ON history.plan_ref=current.plan_ref AND history.state_ref=current.state_ref
     AND history.current_until_at IS NULL
    JOIN dante.plan_work_state AS state
      ON state.plan_ref=current.plan_ref AND state.state_ref=current.state_ref
   WHERE owner.self_person_ref=requested_self_person_ref
     AND owner.plan_ref=requested_plan_ref;
$function$
"""
    )
    _sql(
        """
CREATE FUNCTION dante.list_self_plan_work(requested_self_person_ref uuid)
RETURNS TABLE(
  plan_ref uuid, state_ref uuid, title text, created_at timestamptz,
  steps jsonb
) LANGUAGE sql SECURITY DEFINER STABLE PARALLEL SAFE
SET search_path=pg_catalog,dante,pg_temp
AS $function$
  SELECT work.plan_ref,work.state_ref,work.title,work.created_at,work.steps
    FROM dante.plan_intention AS owner
    CROSS JOIN LATERAL dante.get_self_plan_work(
      requested_self_person_ref,owner.plan_ref
    ) AS work
   WHERE owner.self_person_ref=requested_self_person_ref
   ORDER BY owner.created_at,owner.plan_ref;
$function$
"""
    )
    _sql(
        """
CREATE FUNCTION dante.create_self_plan_work(
  requested_self_person_ref uuid, requested_operation_id text,
  requested_fingerprint text, requested_plan_ref uuid,
  requested_state_ref uuid, requested_title text
) RETURNS TABLE(
  plan_ref uuid, state_ref uuid, title text, created_at timestamptz,
  steps jsonb, replayed boolean
) LANGUAGE plpgsql SECURITY DEFINER VOLATILE PARALLEL UNSAFE
SET search_path=pg_catalog,dante,pg_temp
AS $function$
#variable_conflict error
DECLARE
  op_id text := btrim(requested_operation_id);
  clean_title text := btrim(requested_title);
  prior_fingerprint text;
  prior_plan uuid;
  stamp timestamptz := statement_timestamp();
BEGIN
  IF op_id IS NULL OR op_id='' OR char_length(op_id)>200
     OR requested_fingerprint !~ '^[0-9a-f]{64}$'
     OR clean_title IS NULL OR clean_title='' OR char_length(clean_title)>300
     OR uuid_extract_version(requested_plan_ref) IS DISTINCT FROM 7
     OR uuid_extract_version(requested_state_ref) IS DISTINCT FROM 7 THEN
    RAISE EXCEPTION USING ERRCODE='23514',MESSAGE='Plan input rejected';
  END IF;
  PERFORM pg_advisory_xact_lock(hashtextextended(
    'plan_operation:'||requested_self_person_ref::text||':'||op_id,0
  ));
  SELECT operation.intent_fingerprint,operation.plan_ref
    INTO prior_fingerprint,prior_plan
    FROM dante.plan_work_operation AS operation
   WHERE operation.self_person_ref=requested_self_person_ref
     AND operation.operation_id=op_id;
  IF FOUND THEN
    IF prior_fingerprint<>requested_fingerprint THEN
      RAISE EXCEPTION USING ERRCODE='23505',
        MESSAGE='Plan operation id reused with different intent';
    END IF;
    RETURN QUERY SELECT work.plan_ref,work.state_ref,work.title,work.created_at,
      COALESCE((SELECT jsonb_agg(jsonb_build_object(
        'step_ref',item.step_ref,'position',item.position,
        'title',item.title,'activity_ref',item.activity_ref
      ) ORDER BY item.position) FROM dante.plan_step_in_state AS item
        WHERE item.state_ref=work.state_ref),'[]'::jsonb),true
      FROM dante.plan_work_state AS work
      JOIN dante.plan_intention AS owner ON owner.plan_ref=work.plan_ref
      JOIN dante.plan_work_operation AS operation ON operation.state_ref=work.state_ref
     WHERE work.plan_ref=prior_plan AND operation.self_person_ref=requested_self_person_ref
       AND operation.operation_id=op_id;
    RETURN;
  END IF;
  IF NOT EXISTS (SELECT 1 FROM dante.person WHERE person_ref=requested_self_person_ref) THEN
    RAISE EXCEPTION USING ERRCODE='23503',MESSAGE='Plan self Person unavailable';
  END IF;
  INSERT INTO dante.plan(plan_ref) VALUES(requested_plan_ref);
  INSERT INTO dante.native_address(native_ref,owner_family)
  VALUES(requested_plan_ref,'plan');
  INSERT INTO dante.plan_intention(plan_ref,self_person_ref,created_at)
  VALUES(requested_plan_ref,requested_self_person_ref,stamp);
  INSERT INTO dante.plan_work_state(state_ref,plan_ref,title,recorded_at)
  VALUES(requested_state_ref,requested_plan_ref,clean_title,stamp);
  INSERT INTO dante.plan_current_work_state(plan_ref,state_ref)
  VALUES(requested_plan_ref,requested_state_ref);
  INSERT INTO dante.plan_work_current_history(plan_ref,state_ref,current_from_at)
  VALUES(requested_plan_ref,requested_state_ref,stamp);
  INSERT INTO dante.plan_work_operation(
    self_person_ref,operation_id,intent_fingerprint,plan_ref,state_ref,created_at
  ) VALUES (
    requested_self_person_ref,op_id,requested_fingerprint,
    requested_plan_ref,requested_state_ref,stamp
  );
  RETURN QUERY SELECT work.plan_ref,work.state_ref,work.title,work.created_at,
    work.steps,false FROM dante.get_self_plan_work(
      requested_self_person_ref,requested_plan_ref
    ) AS work;
END;
$function$
"""
    )
    _sql(
        """
CREATE FUNCTION dante.replace_self_plan_work(
  requested_self_person_ref uuid, requested_operation_id text,
  requested_fingerprint text, requested_plan_ref uuid,
  requested_expected_state_ref uuid, requested_state_ref uuid,
  requested_title text, requested_steps jsonb
) RETURNS TABLE(
  plan_ref uuid, state_ref uuid, title text, created_at timestamptz,
  steps jsonb, replayed boolean
) LANGUAGE plpgsql SECURITY DEFINER VOLATILE PARALLEL UNSAFE
SET search_path=pg_catalog,dante,pg_temp
AS $function$
#variable_conflict error
DECLARE
  op_id text := btrim(requested_operation_id);
  clean_title text := btrim(requested_title);
  prior_fingerprint text;
  prior_plan uuid;
  prior_state uuid;
  active_state uuid;
  active_from timestamptz;
  stamp timestamptz := statement_timestamp();
  item jsonb;
  item_ref uuid;
  item_activity uuid;
  item_title text;
  item_position integer := 0;
  existing_plan uuid;
BEGIN
  IF op_id IS NULL OR op_id='' OR char_length(op_id)>200
     OR requested_fingerprint !~ '^[0-9a-f]{64}$'
     OR clean_title IS NULL OR clean_title='' OR char_length(clean_title)>300
     OR requested_steps IS NULL OR jsonb_typeof(requested_steps)<>'array'
     OR jsonb_array_length(requested_steps)>1000
     OR uuid_extract_version(requested_state_ref) IS DISTINCT FROM 7 THEN
    RAISE EXCEPTION USING ERRCODE='23514',MESSAGE='Plan structure input rejected';
  END IF;
  PERFORM pg_advisory_xact_lock(hashtextextended(
    'plan_operation:'||requested_self_person_ref::text||':'||op_id,0
  ));
  SELECT operation.intent_fingerprint,operation.plan_ref,operation.state_ref
    INTO prior_fingerprint,prior_plan,prior_state
    FROM dante.plan_work_operation AS operation
   WHERE operation.self_person_ref=requested_self_person_ref
     AND operation.operation_id=op_id;
  IF FOUND THEN
    IF prior_fingerprint<>requested_fingerprint OR prior_plan<>requested_plan_ref THEN
      RAISE EXCEPTION USING ERRCODE='23505',
        MESSAGE='Plan operation id reused with different intent';
    END IF;
    RETURN QUERY SELECT state.plan_ref,state.state_ref,state.title,owner.created_at,
      COALESCE((SELECT jsonb_agg(jsonb_build_object(
        'step_ref',snapshot.step_ref,'position',snapshot.position,
        'title',snapshot.title,'activity_ref',snapshot.activity_ref
      ) ORDER BY snapshot.position) FROM dante.plan_step_in_state AS snapshot
        WHERE snapshot.state_ref=prior_state),'[]'::jsonb),true
      FROM dante.plan_work_state AS state
      JOIN dante.plan_intention AS owner ON owner.plan_ref=state.plan_ref
     WHERE state.state_ref=prior_state;
    RETURN;
  END IF;
  PERFORM 1 FROM dante.plan_intention AS owner
   WHERE owner.plan_ref=requested_plan_ref
     AND owner.self_person_ref=requested_self_person_ref FOR UPDATE;
  IF NOT FOUND THEN
    RAISE EXCEPTION USING ERRCODE='23503',MESSAGE='Self Plan unavailable';
  END IF;
  SELECT current.state_ref,history.current_from_at INTO active_state,active_from
    FROM dante.plan_current_work_state AS current
    JOIN dante.plan_work_current_history AS history
      ON history.plan_ref=current.plan_ref AND history.state_ref=current.state_ref
     AND history.current_until_at IS NULL
   WHERE current.plan_ref=requested_plan_ref FOR UPDATE OF current,history;
  IF active_state IS DISTINCT FROM requested_expected_state_ref THEN
    RAISE EXCEPTION USING ERRCODE='40001',MESSAGE='Plan current state conflict';
  END IF;
  IF stamp<=active_from THEN stamp:=active_from+interval '1 microsecond'; END IF;
  INSERT INTO dante.plan_work_state(state_ref,plan_ref,title,recorded_at)
  VALUES(requested_state_ref,requested_plan_ref,clean_title,stamp);
  FOR item IN SELECT value FROM jsonb_array_elements(requested_steps) AS element(value)
  LOOP
    IF jsonb_typeof(item)<>'object'
       OR jsonb_typeof(item->'step_ref')<>'string'
       OR jsonb_typeof(item->'title')<>'string'
       OR (item ? 'activity_ref' AND jsonb_typeof(item->'activity_ref') NOT IN ('string','null'))
       OR (item - 'step_ref' - 'title' - 'activity_ref')<>'{}'::jsonb THEN
      RAISE EXCEPTION USING ERRCODE='23514',MESSAGE='Plan Step shape rejected';
    END IF;
    BEGIN
      item_ref:=(item->>'step_ref')::uuid;
      item_activity:=NULLIF(item->>'activity_ref','')::uuid;
    EXCEPTION WHEN invalid_text_representation THEN
      RAISE EXCEPTION USING ERRCODE='23514',MESSAGE='Plan Step reference rejected';
    END;
    item_title:=btrim(item->>'title');
    IF uuid_extract_version(item_ref) IS DISTINCT FROM 7
       OR item_title IS NULL OR item_title='' OR char_length(item_title)>300 THEN
      RAISE EXCEPTION USING ERRCODE='23514',MESSAGE='Plan Step input rejected';
    END IF;
    IF item_activity IS NOT NULL AND NOT EXISTS (
      SELECT 1 FROM dante.activity_intention AS activity
       WHERE activity.activity_ref=item_activity
         AND activity.self_person_ref=requested_self_person_ref
    ) THEN
      RAISE EXCEPTION USING ERRCODE='23503',MESSAGE='Step Activity is not self-owned';
    END IF;
    SELECT existing.plan_ref INTO existing_plan
      FROM dante.plan_step AS existing WHERE existing.step_ref=item_ref;
    IF existing_plan IS NOT NULL AND existing_plan<>requested_plan_ref THEN
      RAISE EXCEPTION USING ERRCODE='23503',MESSAGE='Cross-Plan Step rejected';
    END IF;
    IF existing_plan IS NULL THEN
      INSERT INTO dante.plan_step(step_ref,plan_ref)
      VALUES(item_ref,requested_plan_ref);
    END IF;
    INSERT INTO dante.plan_step_in_state(
      state_ref,plan_ref,step_ref,position,title,activity_ref
    ) VALUES (
      requested_state_ref,requested_plan_ref,item_ref,item_position,item_title,item_activity
    );
    item_position:=item_position+1;
  END LOOP;
  UPDATE dante.plan_work_current_history
     SET current_until_at=stamp
   WHERE plan_work_current_history.plan_ref=requested_plan_ref
     AND current_until_at IS NULL;
  UPDATE dante.plan_current_work_state
     SET state_ref=requested_state_ref WHERE plan_ref=requested_plan_ref;
  INSERT INTO dante.plan_work_current_history(plan_ref,state_ref,current_from_at)
  VALUES(requested_plan_ref,requested_state_ref,stamp);
  INSERT INTO dante.plan_work_operation(
    self_person_ref,operation_id,intent_fingerprint,plan_ref,state_ref,created_at
  ) VALUES (
    requested_self_person_ref,op_id,requested_fingerprint,
    requested_plan_ref,requested_state_ref,stamp
  );
  RETURN QUERY SELECT work.plan_ref,work.state_ref,work.title,work.created_at,
    work.steps,false FROM dante.get_self_plan_work(
      requested_self_person_ref,requested_plan_ref
    ) AS work;
END;
$function$
"""
    )
    for name, signature in (
        ("get_self_plan_work", "uuid,uuid"),
        ("list_self_plan_work", "uuid"),
        ("create_self_plan_work", "uuid,text,text,uuid,uuid,text"),
        ("replace_self_plan_work", "uuid,text,text,uuid,uuid,uuid,text,jsonb"),
    ):
        _sql(f"ALTER FUNCTION dante.{name}({signature}) OWNER TO dante_owner")
        _sql(
            f"REVOKE ALL ON FUNCTION dante.{name}({signature}) "
            f"FROM PUBLIC,{_RUNTIME},{_MIGRATOR}"
        )
        _sql(f"GRANT EXECUTE ON FUNCTION dante.{name}({signature}) TO {_RUNTIME}")
    for name in (
        "plan_intention", "plan_step", "plan_work_state", "plan_step_in_state",
        "plan_current_work_state", "plan_work_current_history", "plan_work_operation",
    ):
        _sql(f"ALTER TABLE dante.{name} OWNER TO dante_owner")
        _sql(f"REVOKE ALL ON TABLE dante.{name} FROM PUBLIC,{_RUNTIME},{_MIGRATOR}")


def downgrade() -> None:
    raise RuntimeError(
        "B13-A canonical Plan structure is forward-only; use a reviewed forward migration."
    )
