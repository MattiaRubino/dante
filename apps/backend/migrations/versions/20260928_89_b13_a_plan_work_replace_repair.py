"""B13-A forward repair: qualify accepted-current Plan binding in replace."""

from collections.abc import Sequence

from alembic import op

revision: str = "20260928_89"
down_revision: str | None = "20260928_88"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.get_bind().exec_driver_sql(
        """
CREATE OR REPLACE FUNCTION dante.replace_self_plan_work(
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
  UPDATE dante.plan_current_work_state AS current
     SET state_ref=requested_state_ref WHERE current.plan_ref=requested_plan_ref;
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


def downgrade() -> None:
    raise RuntimeError("B13-A Plan replace repair is forward-only.")
