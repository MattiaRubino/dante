"""B11-B: qualify conditional function receipt references.

Revision ID: 20260927_83
Revises: 20260927_82

Revision 82 is immutable. Its PL/pgSQL functions deliberately use
``#variable_conflict error``; qualify operation-table columns that overlap the
RETURNS TABLE output variables before the capability is exercised.
"""

from collections.abc import Sequence

from alembic import op

revision: str = "20260927_83"
down_revision: str | None = "20260927_82"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_OWNER = "dante_owner"
_RUNTIME = "dante_runtime"
_MIGRATOR = "dante_migrator"


def _sql(statement: str) -> None:
    op.get_bind().exec_driver_sql(statement)


def upgrade() -> None:
    _sql(
        r"""
CREATE OR REPLACE FUNCTION dante.create_self_actual_realization_condition(
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

  SELECT operation.operation_kind,
         operation.intent_fingerprint,
         operation.condition_ref,
         operation.evaluation_ref,
         operation.created_at
    INTO prior
    FROM dante.conditional_temporal_operation AS operation
   WHERE operation.self_person_ref=requested_self_person_ref
     AND operation.operation_id=key;

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
CREATE OR REPLACE FUNCTION dante.evaluate_self_actual_realization_condition(
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

  SELECT operation.operation_kind,
         operation.intent_fingerprint,
         operation.condition_ref,
         operation.evaluation_ref,
         operation.created_at
    INTO prior
    FROM dante.conditional_temporal_operation AS operation
   WHERE operation.self_person_ref=requested_self_person_ref
     AND operation.operation_id=key;

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

    for signature in (
        "dante.create_self_actual_realization_condition(uuid,text,text,text,uuid,uuid)",
        "dante.evaluate_self_actual_realization_condition(uuid,text,text,uuid,uuid)",
    ):
        _sql(f"ALTER FUNCTION {signature} OWNER TO {_OWNER}")
        _sql(f"REVOKE ALL ON FUNCTION {signature} FROM PUBLIC,{_MIGRATOR}")
        _sql(f"GRANT EXECUTE ON FUNCTION {signature} TO {_RUNTIME}")


def downgrade() -> None:
    raise RuntimeError("B11-B qualification repair is forward-only.")
