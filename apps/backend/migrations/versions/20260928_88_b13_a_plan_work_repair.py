"""B13-A forward repair for Plan replay and catalog check identifiers."""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260928_88"
down_revision: str | None = "20260928_87"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_CHECK_RENAMES = (
    ("plan_step", "uuidv7"),
    ("plan_work_state", "uuidv7"),
    ("plan_work_state", "title"),
    ("plan_step_in_state", "position"),
    ("plan_step_in_state", "title"),
    ("plan_work_current_history", "interval"),
    ("plan_work_operation", "id"),
    ("plan_work_operation", "fingerprint"),
)


def upgrade() -> None:
    connection = op.get_bind()
    for table, suffix in _CHECK_RENAMES:
        expected = f"ck_{table}_{suffix}"
        old_prefix = f"ck_{table}_{expected}"[:50]
        matches = (
            connection.execute(
                sa.text(
                    "SELECT constraint.conname FROM pg_constraint AS constraint "
                    "JOIN pg_class AS relation ON relation.oid=constraint.conrelid "
                    "JOIN pg_namespace AS namespace ON namespace.oid=relation.relnamespace "
                    "WHERE namespace.nspname='dante' AND relation.relname=:table "
                    "AND constraint.contype='c' AND constraint.conname LIKE :old_name"
                ),
                {"table": table, "old_name": f"{old_prefix}%"},
            )
            .scalars()
            .all()
        )
        if len(matches) != 1:
            raise RuntimeError(f"Expected one _87 check for {table}.{suffix}: {matches}")
        old = matches[0]
        if not old.replace("_", "").isalnum():
            raise RuntimeError(f"Unexpected _87 check name: {old}")
        connection.exec_driver_sql(
            f'ALTER TABLE dante."{table}" RENAME CONSTRAINT "{old}" TO "{expected}"'
        )

    connection.exec_driver_sql(
        """
CREATE OR REPLACE FUNCTION dante.create_self_plan_work(
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
    RETURN QUERY SELECT work.plan_ref,work.state_ref,work.title,owner.created_at,
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


def downgrade() -> None:
    raise RuntimeError("B13-A Plan repair is forward-only.")
