"""B14: persistent noncanonical Objective input, explicit atomic confirmation.

An unconfirmed value is NOT an Observation, Evaluation, Actual or Outcome.
"""
from collections.abc import Sequence

from alembic import op

revision: str = "20261010_139"
down_revision: str | None = "20261010_138"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    bind = op.get_bind()
    for sql in (_TABLE, _SAVE, _LIST, _CONFIRM):
        bind.exec_driver_sql(sql)
    bind.exec_driver_sql(
        "ALTER TABLE dante.temporal_objective_input_draft OWNER TO dante_owner"
    )
    bind.exec_driver_sql(
        "REVOKE ALL ON dante.temporal_objective_input_draft "
        "FROM PUBLIC,dante_runtime,dante_migrator"
    )
    for signature in (
        "dante.save_self_objective_input_draft(uuid,uuid,text,bigint,jsonb)",
        "dante.list_self_objective_input_drafts(uuid)",
        "dante.confirm_self_objective_input_draft(uuid,uuid,bigint,text,text,uuid,uuid)",
    ):
        bind.exec_driver_sql(f"ALTER FUNCTION {signature} OWNER TO dante_owner")
        bind.exec_driver_sql(
            f"REVOKE ALL ON FUNCTION {signature} FROM PUBLIC,dante_runtime,dante_migrator"
        )
        bind.exec_driver_sql(f"GRANT EXECUTE ON FUNCTION {signature} TO dante_runtime")


def downgrade() -> None:
    raise RuntimeError("Objective input draft and accepted confirmation are forward-only")


_TABLE = r"""
CREATE TABLE dante.temporal_objective_input_draft (
  objective_ref uuid CONSTRAINT pk_temporal_objective_input_draft PRIMARY KEY
    CONSTRAINT fk_temporal_objective_input_draft_objective
    REFERENCES dante.temporal_objective(objective_ref),
  owner_person_ref uuid NOT NULL,
  payload jsonb NOT NULL CONSTRAINT ck_temporal_objective_input_draft_payload
    CHECK (jsonb_typeof(payload)='object' AND octet_length(payload::text)<=4096),
  revision bigint NOT NULL DEFAULT 1 CONSTRAINT ck_temporal_objective_input_draft_revision
    CHECK (revision>=1),
  last_operation_id text NOT NULL,
  confirmed_operation_id text,
  observation_ref uuid,
  evaluation_state_ref uuid,
  assessment_code text,
  confirmed_at timestamptz,
  updated_at timestamptz NOT NULL DEFAULT clock_timestamp(),
  CONSTRAINT ck_temporal_objective_input_draft_confirmed CHECK (
    (confirmed_at IS NULL AND confirmed_operation_id IS NULL AND
     observation_ref IS NULL AND evaluation_state_ref IS NULL AND assessment_code IS NULL)
    OR
    (confirmed_at IS NOT NULL AND confirmed_operation_id IS NOT NULL AND
     observation_ref IS NOT NULL AND evaluation_state_ref IS NOT NULL AND assessment_code IS NOT NULL)
  )
);
CREATE INDEX ix_temporal_objective_input_draft_owner
 ON dante.temporal_objective_input_draft(owner_person_ref,updated_at DESC,objective_ref);
"""

_SAVE = r"""
CREATE FUNCTION dante.save_self_objective_input_draft(
  actor uuid, requested_objective uuid, operation_id text,
  expected_revision bigint, requested_payload jsonb
) RETURNS TABLE(
  objective_ref uuid, payload jsonb, revision bigint,
  confirmed_at timestamptz, updated_at timestamptz
)
LANGUAGE plpgsql SECURITY DEFINER VOLATILE PARALLEL UNSAFE
SET search_path=pg_catalog,dante,pg_temp AS $function$
#variable_conflict error
DECLARE previous dante.temporal_objective_input_draft%ROWTYPE;
BEGIN
  IF actor IS NULL OR requested_objective IS NULL OR
     operation_id IS NULL OR length(operation_id) NOT BETWEEN 1 AND 200
     OR requested_payload IS NULL OR jsonb_typeof(requested_payload)<>'object'
     OR octet_length(requested_payload::text)>4096 OR
     NOT (
       (requested_payload ? 'observed_boolean') OR
       (requested_payload ? 'observed_numeric') OR
       (requested_payload ? 'qualitative_code')
     ) THEN
    RAISE EXCEPTION 'Invalid Objective input'
      USING ERRCODE='22023',CONSTRAINT='objective_input_invalid';
  END IF;
  IF NOT EXISTS (
    SELECT 1 FROM dante.temporal_objective o
    WHERE o.objective_ref=requested_objective AND o.self_person_ref=actor
      AND o.retired_at IS NULL
  ) THEN
    RAISE EXCEPTION 'Objective unavailable'
      USING ERRCODE='23503',CONSTRAINT='objective_input_unavailable';
  END IF;
  SELECT * INTO previous FROM dante.temporal_objective_input_draft d
    WHERE d.objective_ref=requested_objective FOR UPDATE;
  IF NOT FOUND THEN
    IF expected_revision IS NOT NULL THEN
      RAISE EXCEPTION 'Stale Objective input'
        USING ERRCODE='40001',CONSTRAINT='objective_input_stale';
    END IF;
    INSERT INTO dante.temporal_objective_input_draft(
      objective_ref,owner_person_ref,payload,last_operation_id)
    VALUES (requested_objective,actor,requested_payload,operation_id);
  ELSE
    IF previous.owner_person_ref<>actor THEN
      RAISE EXCEPTION 'Objective input unavailable'
        USING ERRCODE='23503',CONSTRAINT='objective_input_unavailable';
    END IF;
    IF previous.last_operation_id=operation_id
       AND previous.payload=requested_payload THEN
      RETURN QUERY SELECT d.objective_ref,d.payload,d.revision,
                          d.confirmed_at,d.updated_at
        FROM dante.temporal_objective_input_draft d
        WHERE d.objective_ref=requested_objective;
      RETURN;
    END IF;
    IF previous.last_operation_id=operation_id OR previous.confirmed_at IS NOT NULL
       OR previous.revision IS DISTINCT FROM expected_revision THEN
      RAISE EXCEPTION 'Objective input changed or confirmed'
        USING ERRCODE='40001',CONSTRAINT='objective_input_stale';
    END IF;
    UPDATE dante.temporal_objective_input_draft d
       SET payload=requested_payload,revision=d.revision+1,
           last_operation_id=operation_id,updated_at=clock_timestamp()
     WHERE d.objective_ref=requested_objective;
  END IF;
  RETURN QUERY SELECT d.objective_ref,d.payload,d.revision,
                      d.confirmed_at,d.updated_at
    FROM dante.temporal_objective_input_draft d
   WHERE d.objective_ref=requested_objective;
END;
$function$;
"""

_LIST = r"""
CREATE FUNCTION dante.list_self_objective_input_drafts(actor uuid)
RETURNS TABLE(objective_ref uuid,payload jsonb,revision bigint,
              confirmed_at timestamptz,updated_at timestamptz)
LANGUAGE sql SECURITY DEFINER STABLE PARALLEL RESTRICTED
SET search_path=pg_catalog,dante,pg_temp AS $function$
  SELECT d.objective_ref,d.payload,d.revision,d.confirmed_at,d.updated_at
  FROM dante.temporal_objective_input_draft d
  WHERE d.owner_person_ref=actor
  ORDER BY d.updated_at DESC,d.objective_ref
  LIMIT 1000
$function$;
"""

_CONFIRM = r"""
CREATE FUNCTION dante.confirm_self_objective_input_draft(
  actor uuid, requested_objective uuid, expected_revision bigint,
  operation_id text, intent_fingerprint text,
  new_observation uuid, new_evaluation uuid
) RETURNS TABLE(
  objective_ref uuid,observation_ref uuid,evaluation_state_ref uuid,
  assessment_code text,replayed boolean
)
LANGUAGE plpgsql SECURITY DEFINER VOLATILE PARALLEL UNSAFE
SET search_path=pg_catalog,dante,pg_temp AS $function$
#variable_conflict error
DECLARE draft dante.temporal_objective_input_draft%ROWTYPE;
        accepted record;
BEGIN
  SELECT * INTO draft FROM dante.temporal_objective_input_draft d
    WHERE d.objective_ref=requested_objective AND d.owner_person_ref=actor
    FOR UPDATE;
  IF NOT FOUND THEN
    RAISE EXCEPTION 'Objective input unavailable'
      USING ERRCODE='23503',CONSTRAINT='objective_input_unavailable';
  END IF;
  IF draft.confirmed_at IS NOT NULL THEN
    IF draft.confirmed_operation_id=operation_id THEN
      RETURN QUERY SELECT draft.objective_ref,draft.observation_ref,
        draft.evaluation_state_ref,draft.assessment_code,true;
      RETURN;
    END IF;
    RAISE EXCEPTION 'Objective input already confirmed'
      USING ERRCODE='40001',CONSTRAINT='objective_input_stale';
  END IF;
  IF draft.revision IS DISTINCT FROM expected_revision
     OR operation_id IS NULL OR length(operation_id) NOT BETWEEN 1 AND 200
     OR intent_fingerprint IS NULL OR length(intent_fingerprint)<>64 THEN
    RAISE EXCEPTION 'Objective input changed'
      USING ERRCODE='40001',CONSTRAINT='objective_input_stale';
  END IF;
  SELECT * INTO STRICT accepted
    FROM dante.record_self_temporal_objective_result(
      actor,operation_id,intent_fingerprint,requested_objective,
      new_observation,new_evaluation,
      (draft.payload->>'observed_boolean')::boolean,
      (draft.payload->>'observed_numeric')::numeric,
      draft.payload->>'qualitative_code',
      draft.payload->>'assessment_code'
    );
  UPDATE dante.temporal_objective_input_draft d
     SET confirmed_operation_id=operation_id,
         observation_ref=accepted.observation_ref,
         evaluation_state_ref=accepted.evaluation_state_ref,
         assessment_code=accepted.assessment_code,
         confirmed_at=clock_timestamp(),updated_at=clock_timestamp()
   WHERE d.objective_ref=requested_objective;
  RETURN QUERY SELECT accepted.objective_ref,accepted.observation_ref,
    accepted.evaluation_state_ref,accepted.assessment_code,accepted.replayed;
END;
$function$;
"""