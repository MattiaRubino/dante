"""B11-B: bounded conditional temporal evaluation over canonical Actual truth.

Revision ID: 20260927_82
Revises: 20260926_81

B11-B adds one bounded condition family, ``actual_realization``. PostgreSQL
computes condition truth from the current accepted Actual MaterialState. An
evaluation is immutable evidence and never performs the proposed effect.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260927_82"
down_revision: str | None = "20260926_81"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_SCHEMA = "dante"
_OWNER = "dante_owner"
_RUNTIME = "dante_runtime"
_MIGRATOR = "dante_migrator"


def _sql(statement: str) -> None:
    op.get_bind().exec_driver_sql(statement)


def upgrade() -> None:
    op.create_table(
        "conditional_temporal_intent",
        sa.Column("condition_ref", sa.Uuid(), nullable=False),
        sa.Column("self_person_ref", sa.Uuid(), nullable=False),
        sa.Column("subject_family", sa.Text(), nullable=False),
        sa.Column("subject_native_ref", sa.Uuid(), nullable=False),
        sa.Column("family_code", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint(
            "uuid_extract_version(condition_ref) IS NOT DISTINCT FROM 7",
            name=op.f("ck_conditional_temporal_intent_uuidv7"),
        ),
        sa.CheckConstraint(
            "subject_family IN ('activity','event','occurrence')",
            name=op.f("ck_conditional_temporal_intent_subject_family"),
        ),
        sa.CheckConstraint(
            "family_code='actual_realization'",
            name=op.f("ck_conditional_temporal_intent_family"),
        ),
        sa.CheckConstraint(
            "isfinite(created_at)",
            name=op.f("ck_conditional_temporal_intent_created_at"),
        ),
        sa.ForeignKeyConstraint(
            ["self_person_ref"],
            [f"{_SCHEMA}.person.person_ref"],
            name=op.f("fk_conditional_temporal_intent_person"),
            onupdate="NO ACTION",
            ondelete="NO ACTION",
        ),
        sa.ForeignKeyConstraint(
            ["subject_native_ref"],
            [f"{_SCHEMA}.native_address.native_ref"],
            name=op.f("fk_conditional_temporal_intent_subject"),
            onupdate="NO ACTION",
            ondelete="NO ACTION",
        ),
        sa.PrimaryKeyConstraint(
            "condition_ref", name=op.f("pk_conditional_temporal_intent")
        ),
        sa.UniqueConstraint(
            "self_person_ref",
            "subject_native_ref",
            "family_code",
            name=op.f("uq_conditional_temporal_intent_subject_family"),
        ),
        schema=_SCHEMA,
    )
    op.create_index(
        "ix_conditional_temporal_intent_subject",
        "conditional_temporal_intent",
        ["self_person_ref", "subject_family", "subject_native_ref"],
        schema=_SCHEMA,
    )

    op.create_table(
        "conditional_temporal_evaluation",
        sa.Column("evaluation_ref", sa.Uuid(), nullable=False),
        sa.Column("condition_ref", sa.Uuid(), nullable=False),
        sa.Column("result_code", sa.Text(), nullable=False),
        sa.Column("disposition_code", sa.Text(), nullable=False),
        sa.Column("actual_ref", sa.Uuid(), nullable=True),
        sa.Column("actual_realization_material_state_ref", sa.Uuid(), nullable=True),
        sa.Column("evaluated_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint(
            "uuid_extract_version(evaluation_ref) IS NOT DISTINCT FROM 7",
            name=op.f("ck_conditional_temporal_evaluation_uuidv7"),
        ),
        sa.CheckConstraint(
            "result_code IN ('satisfied','not_satisfied','indeterminate')",
            name=op.f("ck_conditional_temporal_evaluation_result"),
        ),
        sa.CheckConstraint(
            "(result_code='satisfied' AND disposition_code='allow') OR "
            "(result_code IN ('not_satisfied','indeterminate') AND disposition_code='withhold')",
            name=op.f("ck_conditional_temporal_evaluation_disposition"),
        ),
        sa.CheckConstraint(
            "(result_code='indeterminate' AND actual_ref IS NULL AND "
            "actual_realization_material_state_ref IS NULL) OR "
            "(result_code<>'indeterminate' AND actual_ref IS NOT NULL AND "
            "actual_realization_material_state_ref IS NOT NULL)",
            name=op.f("ck_conditional_temporal_evaluation_evidence_shape"),
        ),
        sa.CheckConstraint(
            "isfinite(evaluated_at)",
            name=op.f("ck_conditional_temporal_evaluation_evaluated_at"),
        ),
        sa.ForeignKeyConstraint(
            ["condition_ref"],
            [f"{_SCHEMA}.conditional_temporal_intent.condition_ref"],
            name=op.f("fk_conditional_temporal_evaluation_condition"),
            onupdate="NO ACTION",
            ondelete="NO ACTION",
        ),
        sa.ForeignKeyConstraint(
            ["actual_ref"],
            [f"{_SCHEMA}.actual.actual_ref"],
            name=op.f("fk_conditional_temporal_evaluation_actual"),
            onupdate="NO ACTION",
            ondelete="NO ACTION",
        ),
        sa.ForeignKeyConstraint(
            ["actual_realization_material_state_ref"],
            [f"{_SCHEMA}.actual_realization_state.material_state_ref"],
            name=op.f("fk_conditional_temporal_evaluation_actual_state"),
            onupdate="NO ACTION",
            ondelete="NO ACTION",
        ),
        sa.PrimaryKeyConstraint(
            "evaluation_ref", name=op.f("pk_conditional_temporal_evaluation")
        ),
        schema=_SCHEMA,
    )
    op.create_index(
        "ix_conditional_temporal_evaluation_condition_time",
        "conditional_temporal_evaluation",
        ["condition_ref", "evaluated_at", "evaluation_ref"],
        schema=_SCHEMA,
    )
    op.create_index(
        "ix_conditional_temporal_evaluation_actual_state",
        "conditional_temporal_evaluation",
        ["actual_realization_material_state_ref"],
        schema=_SCHEMA,
    )

    op.create_table(
        "conditional_temporal_operation",
        sa.Column("self_person_ref", sa.Uuid(), nullable=False),
        sa.Column("operation_id", sa.Text(), nullable=False),
        sa.Column("intent_fingerprint", sa.Text(), nullable=False),
        sa.Column("operation_kind", sa.Text(), nullable=False),
        sa.Column("condition_ref", sa.Uuid(), nullable=False),
        sa.Column("evaluation_ref", sa.Uuid(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint(
            "operation_id=btrim(operation_id) AND operation_id<>'' AND char_length(operation_id)<=200",
            name=op.f("ck_conditional_temporal_operation_id"),
        ),
        sa.CheckConstraint(
            "intent_fingerprint ~ '^[0-9a-f]{64}$'",
            name=op.f("ck_conditional_temporal_operation_fingerprint"),
        ),
        sa.CheckConstraint(
            "operation_kind IN ('create','evaluate')",
            name=op.f("ck_conditional_temporal_operation_kind"),
        ),
        sa.CheckConstraint(
            "(operation_kind='create' AND evaluation_ref IS NULL) OR "
            "(operation_kind='evaluate' AND evaluation_ref IS NOT NULL)",
            name=op.f("ck_conditional_temporal_operation_result_shape"),
        ),
        sa.CheckConstraint(
            "isfinite(created_at)",
            name=op.f("ck_conditional_temporal_operation_created_at"),
        ),
        sa.ForeignKeyConstraint(
            ["self_person_ref"],
            [f"{_SCHEMA}.person.person_ref"],
            name=op.f("fk_conditional_temporal_operation_person"),
            onupdate="NO ACTION",
            ondelete="NO ACTION",
        ),
        sa.ForeignKeyConstraint(
            ["condition_ref"],
            [f"{_SCHEMA}.conditional_temporal_intent.condition_ref"],
            name=op.f("fk_conditional_temporal_operation_condition"),
            onupdate="NO ACTION",
            ondelete="NO ACTION",
        ),
        sa.ForeignKeyConstraint(
            ["evaluation_ref"],
            [f"{_SCHEMA}.conditional_temporal_evaluation.evaluation_ref"],
            name=op.f("fk_conditional_temporal_operation_evaluation"),
            onupdate="NO ACTION",
            ondelete="NO ACTION",
        ),
        sa.PrimaryKeyConstraint(
            "self_person_ref",
            "operation_id",
            name=op.f("pk_conditional_temporal_operation"),
        ),
        sa.UniqueConstraint(
            "evaluation_ref",
            name=op.f("uq_conditional_temporal_operation_evaluation"),
        ),
        schema=_SCHEMA,
    )

    _sql(
        r"""
CREATE FUNCTION dante.enforce_b11b_conditional_evaluation_evidence()
RETURNS trigger
LANGUAGE plpgsql
SECURITY INVOKER
VOLATILE
PARALLEL UNSAFE
SET search_path=pg_catalog,dante,pg_temp
AS $function$
DECLARE
  evidence_actual uuid;
  evidence_subject uuid;
  condition_subject uuid;
BEGIN
  IF NEW.actual_realization_material_state_ref IS NULL THEN
    RETURN NEW;
  END IF;

  SELECT state.actual_ref, owner.subject_native_ref
    INTO evidence_actual, evidence_subject
    FROM dante.actual_realization_state AS state
    JOIN dante.actual AS owner ON owner.actual_ref=state.actual_ref
   WHERE state.material_state_ref=NEW.actual_realization_material_state_ref;

  SELECT intent.subject_native_ref
    INTO condition_subject
    FROM dante.conditional_temporal_intent AS intent
   WHERE intent.condition_ref=NEW.condition_ref;

  IF evidence_actual IS DISTINCT FROM NEW.actual_ref
     OR evidence_subject IS DISTINCT FROM condition_subject THEN
    RAISE EXCEPTION USING ERRCODE='23514',
      CONSTRAINT='conditional_temporal_evaluation_exact_actual',
      MESSAGE='Conditional evaluation evidence is not exact Actual truth for its subject';
  END IF;

  RETURN NEW;
END;
$function$
"""
    )
    _sql(
        r"""
CREATE CONSTRAINT TRIGGER conditional_temporal_evaluation_exact_actual
AFTER INSERT OR UPDATE ON dante.conditional_temporal_evaluation
DEFERRABLE INITIALLY DEFERRED
FOR EACH ROW EXECUTE FUNCTION dante.enforce_b11b_conditional_evaluation_evidence()
"""
    )

    _sql(
        r"""
CREATE FUNCTION dante.create_self_actual_realization_condition(
  requested_self_person_ref uuid,
  requested_subject_family text,
  requested_operation_id text,
  requested_intent_fingerprint text,
  requested_condition_ref uuid,
  requested_subject_native_ref uuid
) RETURNS TABLE(
  condition_ref uuid,
  subject_family text,
  subject_native_ref uuid,
  family_code text,
  created_at timestamptz,
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
  resolved_condition_ref uuid;
  resolved_created_at timestamptz;
  accepted_at timestamptz := statement_timestamp();
BEGIN
  IF key='' OR char_length(key)>200
     OR requested_intent_fingerprint !~ '^[0-9a-f]{64}$'
     OR uuid_extract_version(requested_condition_ref) IS DISTINCT FROM 7
     OR requested_subject_family NOT IN ('activity','event','occurrence') THEN
    RAISE EXCEPTION USING ERRCODE='23514',
      CONSTRAINT='conditional_temporal_create_input',
      MESSAGE='Conditional temporal create input rejected';
  END IF;

  IF NOT dante._actual_subject_owned_as(
    requested_self_person_ref,
    requested_subject_family,
    requested_subject_native_ref
  ) THEN
    RAISE EXCEPTION USING ERRCODE='23503',
      CONSTRAINT='conditional_temporal_subject_unavailable',
      MESSAGE='Conditional temporal subject unavailable';
  END IF;

  PERFORM pg_advisory_xact_lock(
    hashtextextended(requested_self_person_ref::text || ':conditional-op:' || key, 0)
  );

  SELECT operation_kind,intent_fingerprint,condition_ref,evaluation_ref,created_at
    INTO prior
    FROM dante.conditional_temporal_operation
   WHERE self_person_ref=requested_self_person_ref
     AND operation_id=key;

  IF FOUND THEN
    IF prior.operation_kind<>'create'
       OR prior.intent_fingerprint<>requested_intent_fingerprint THEN
      RAISE EXCEPTION USING ERRCODE='23505',
        CONSTRAINT='conditional_temporal_operation_reused',
        MESSAGE='Conditional temporal operation id reused with different intent';
    END IF;

    RETURN QUERY
    SELECT intent.condition_ref,intent.subject_family,intent.subject_native_ref,
           intent.family_code,intent.created_at,true
      FROM dante.conditional_temporal_intent AS intent
     WHERE intent.condition_ref=prior.condition_ref;
    RETURN;
  END IF;

  PERFORM pg_advisory_xact_lock(
    hashtextextended(
      requested_self_person_ref::text || ':conditional-intent:' || requested_subject_native_ref::text,
      0
    )
  );

  SELECT intent.condition_ref,intent.created_at
    INTO resolved_condition_ref,resolved_created_at
    FROM dante.conditional_temporal_intent AS intent
   WHERE intent.self_person_ref=requested_self_person_ref
     AND intent.subject_native_ref=requested_subject_native_ref
     AND intent.family_code='actual_realization';

  IF resolved_condition_ref IS NULL THEN
    resolved_condition_ref:=requested_condition_ref;
    resolved_created_at:=accepted_at;
    INSERT INTO dante.conditional_temporal_intent(
      condition_ref,self_person_ref,subject_family,subject_native_ref,family_code,created_at
    ) VALUES (
      resolved_condition_ref,requested_self_person_ref,requested_subject_family,
      requested_subject_native_ref,'actual_realization',resolved_created_at
    );
  ELSE
    IF NOT EXISTS (
      SELECT 1 FROM dante.conditional_temporal_intent AS intent
       WHERE intent.condition_ref=resolved_condition_ref
         AND intent.subject_family=requested_subject_family
    ) THEN
      RAISE EXCEPTION USING ERRCODE='23514',
        CONSTRAINT='conditional_temporal_subject_family_conflict',
        MESSAGE='Conditional temporal subject family conflict';
    END IF;
  END IF;

  INSERT INTO dante.conditional_temporal_operation(
    self_person_ref,operation_id,intent_fingerprint,operation_kind,
    condition_ref,evaluation_ref,created_at
  ) VALUES (
    requested_self_person_ref,key,requested_intent_fingerprint,'create',
    resolved_condition_ref,NULL,accepted_at
  );

  RETURN QUERY
  SELECT intent.condition_ref,intent.subject_family,intent.subject_native_ref,
         intent.family_code,intent.created_at,false
    FROM dante.conditional_temporal_intent AS intent
   WHERE intent.condition_ref=resolved_condition_ref;
END;
$function$
"""
    )

    _sql(
        r"""
CREATE FUNCTION dante.get_self_actual_realization_condition(
  requested_self_person_ref uuid,
  requested_condition_ref uuid
) RETURNS TABLE(
  condition_ref uuid,
  subject_family text,
  subject_native_ref uuid,
  family_code text,
  created_at timestamptz
)
LANGUAGE sql
SECURITY DEFINER
STABLE
PARALLEL SAFE
SET search_path=pg_catalog,dante,pg_temp
AS $function$
  SELECT intent.condition_ref,intent.subject_family,intent.subject_native_ref,
         intent.family_code,intent.created_at
    FROM dante.conditional_temporal_intent AS intent
   WHERE intent.condition_ref=requested_condition_ref
     AND intent.self_person_ref=requested_self_person_ref
     AND intent.family_code='actual_realization';
$function$
"""
    )

    _sql(
        r"""
CREATE FUNCTION dante.evaluate_self_actual_realization_condition(
  requested_self_person_ref uuid,
  requested_operation_id text,
  requested_intent_fingerprint text,
  requested_evaluation_ref uuid,
  requested_condition_ref uuid
) RETURNS TABLE(
  evaluation_ref uuid,
  condition_ref uuid,
  result_code text,
  disposition_code text,
  actual_ref uuid,
  actual_realization_material_state_ref uuid,
  evaluated_at timestamptz,
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
  subject_ref uuid;
  condition_family text;
  resolved_actual_ref uuid;
  resolved_actual_state_ref uuid;
  resolved_occurred boolean;
  actual_count integer;
  resolved_result text;
  resolved_disposition text;
  accepted_at timestamptz := statement_timestamp();
BEGIN
  IF key='' OR char_length(key)>200
     OR requested_intent_fingerprint !~ '^[0-9a-f]{64}$'
     OR uuid_extract_version(requested_evaluation_ref) IS DISTINCT FROM 7 THEN
    RAISE EXCEPTION USING ERRCODE='23514',
      CONSTRAINT='conditional_temporal_evaluate_input',
      MESSAGE='Conditional temporal evaluation input rejected';
  END IF;

  SELECT intent.subject_native_ref,intent.family_code
    INTO subject_ref,condition_family
    FROM dante.conditional_temporal_intent AS intent
   WHERE intent.condition_ref=requested_condition_ref
     AND intent.self_person_ref=requested_self_person_ref;
  IF NOT FOUND OR condition_family<>'actual_realization' THEN
    RAISE EXCEPTION USING ERRCODE='23503',
      CONSTRAINT='conditional_temporal_condition_unavailable',
      MESSAGE='Conditional temporal condition unavailable';
  END IF;

  PERFORM pg_advisory_xact_lock(
    hashtextextended(requested_self_person_ref::text || ':conditional-op:' || key, 0)
  );

  SELECT operation_kind,intent_fingerprint,condition_ref,evaluation_ref,created_at
    INTO prior
    FROM dante.conditional_temporal_operation
   WHERE self_person_ref=requested_self_person_ref
     AND operation_id=key;

  IF FOUND THEN
    IF prior.operation_kind<>'evaluate'
       OR prior.intent_fingerprint<>requested_intent_fingerprint
       OR prior.condition_ref<>requested_condition_ref THEN
      RAISE EXCEPTION USING ERRCODE='23505',
        CONSTRAINT='conditional_temporal_operation_reused',
        MESSAGE='Conditional temporal operation id reused with different intent';
    END IF;

    RETURN QUERY
    SELECT evaluation.evaluation_ref,evaluation.condition_ref,evaluation.result_code,
           evaluation.disposition_code,evaluation.actual_ref,
           evaluation.actual_realization_material_state_ref,evaluation.evaluated_at,true
      FROM dante.conditional_temporal_evaluation AS evaluation
     WHERE evaluation.evaluation_ref=prior.evaluation_ref;
    RETURN;
  END IF;

  PERFORM pg_advisory_xact_lock(
    hashtextextended('conditional-evaluate:' || requested_condition_ref::text, 0)
  );

  SELECT count(*)
    INTO actual_count
    FROM dante.actual AS owner
   WHERE owner.subject_native_ref=subject_ref;
  IF actual_count>1 THEN
    RAISE EXCEPTION USING ERRCODE='23514',
      CONSTRAINT='conditional_temporal_actual_ambiguous',
      MESSAGE='Conditional temporal subject has ambiguous Actual ownership';
  END IF;

  SELECT owner.actual_ref,state.material_state_ref,state.realization_occurred
    INTO resolved_actual_ref,resolved_actual_state_ref,resolved_occurred
    FROM dante.actual AS owner
    JOIN dante.scoped_current_material_state AS current
      ON current.scoped_owner_ref=owner.actual_ref
     AND current.facet_code='actual.realization'
    JOIN dante.actual_realization_state AS state
      ON state.actual_ref=owner.actual_ref
     AND state.material_state_ref=current.material_state_ref
   WHERE owner.subject_native_ref=subject_ref;

  IF resolved_actual_state_ref IS NULL THEN
    resolved_result:='indeterminate';
    resolved_disposition:='withhold';
    resolved_actual_ref:=NULL;
  ELSIF resolved_occurred IS TRUE THEN
    resolved_result:='satisfied';
    resolved_disposition:='allow';
  ELSE
    resolved_result:='not_satisfied';
    resolved_disposition:='withhold';
  END IF;

  INSERT INTO dante.conditional_temporal_evaluation(
    evaluation_ref,condition_ref,result_code,disposition_code,
    actual_ref,actual_realization_material_state_ref,evaluated_at
  ) VALUES (
    requested_evaluation_ref,requested_condition_ref,resolved_result,resolved_disposition,
    resolved_actual_ref,resolved_actual_state_ref,accepted_at
  );

  INSERT INTO dante.conditional_temporal_operation(
    self_person_ref,operation_id,intent_fingerprint,operation_kind,
    condition_ref,evaluation_ref,created_at
  ) VALUES (
    requested_self_person_ref,key,requested_intent_fingerprint,'evaluate',
    requested_condition_ref,requested_evaluation_ref,accepted_at
  );

  RETURN QUERY
  SELECT evaluation.evaluation_ref,evaluation.condition_ref,evaluation.result_code,
         evaluation.disposition_code,evaluation.actual_ref,
         evaluation.actual_realization_material_state_ref,evaluation.evaluated_at,false
    FROM dante.conditional_temporal_evaluation AS evaluation
   WHERE evaluation.evaluation_ref=requested_evaluation_ref;
END;
$function$
"""
    )

    for table in (
        "conditional_temporal_intent",
        "conditional_temporal_evaluation",
        "conditional_temporal_operation",
    ):
        _sql(f"ALTER TABLE dante.{table} OWNER TO {_OWNER}")
        _sql(
            f"REVOKE ALL PRIVILEGES ON TABLE dante.{table} "
            f"FROM PUBLIC,{_RUNTIME},{_MIGRATOR}"
        )

    trigger_signature = "dante.enforce_b11b_conditional_evaluation_evidence()"
    create_signature = (
        "dante.create_self_actual_realization_condition(uuid,text,text,text,uuid,uuid)"
    )
    get_signature = "dante.get_self_actual_realization_condition(uuid,uuid)"
    evaluate_signature = (
        "dante.evaluate_self_actual_realization_condition(uuid,text,text,uuid,uuid)"
    )

    _sql(f"ALTER FUNCTION {trigger_signature} OWNER TO {_OWNER}")
    _sql(f"REVOKE ALL ON FUNCTION {trigger_signature} FROM PUBLIC,{_RUNTIME},{_MIGRATOR}")

    for signature in (create_signature, get_signature, evaluate_signature):
        _sql(f"ALTER FUNCTION {signature} OWNER TO {_OWNER}")
        _sql(f"REVOKE ALL ON FUNCTION {signature} FROM PUBLIC,{_MIGRATOR}")
        _sql(f"GRANT EXECUTE ON FUNCTION {signature} TO {_RUNTIME}")


def downgrade() -> None:
    raise RuntimeError("B11-B migration is forward-only.")
