"""B12-C self-scoped reviewed single Schedule admission through B04-D.

The short admission transaction locks Plan mutation and the current evidence
tables before checking the reviewed basis. The B04-D effect runs within it.
No candidate or generic Proposal table is introduced.
"""

from collections.abc import Sequence

from alembic import op

revision: str = "20260929_93"
down_revision: str | None = "20260929_92"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def _sql(value: str) -> None:
    op.get_bind().exec_driver_sql(value)


_GUARD = "dante.assert_self_plan_candidate_basis(uuid,uuid,uuid,uuid,uuid,uuid,uuid,jsonb,jsonb)"
_REQUEST = (
    "dante.request_self_plan_candidate_move("
    "uuid,text,text,uuid,uuid,uuid,uuid,uuid,uuid,timestamptz,timestamptz,jsonb,jsonb,uuid,uuid,boolean)"
)
_ACCEPT = (
    "dante.accept_self_plan_candidate_move("
    "uuid,text,text,uuid,uuid,uuid,uuid,uuid,uuid,jsonb,jsonb,uuid,boolean)"
)


def upgrade() -> None:
    _sql(r"""
CREATE FUNCTION dante.assert_self_plan_candidate_basis(
  requested_self_ref uuid, requested_plan_ref uuid, requested_step_ref uuid,
  requested_plan_state_ref uuid, requested_schedule_ref uuid,
  requested_schedule_state_ref uuid, requested_policy_state_ref uuid,
  requested_dependencies jsonb, requested_constraints jsonb
) RETURNS uuid
LANGUAGE plpgsql SECURITY DEFINER VOLATILE PARALLEL UNSAFE
SET search_path=pg_catalog,dante,pg_temp
AS $function$
#variable_conflict error
DECLARE
  subject_ref uuid;
  current_state uuid;
  current_policy uuid;
  current_dependencies jsonb;
  current_constraints jsonb;
BEGIN
  IF jsonb_typeof(requested_dependencies) IS DISTINCT FROM 'array'
     OR jsonb_typeof(requested_constraints) IS DISTINCT FROM 'array' THEN
    RAISE EXCEPTION USING ERRCODE='22023',CONSTRAINT='candidate_basis_shape',
      MESSAGE='Candidate basis must contain typed evidence arrays';
  END IF;

  PERFORM 1 FROM dante.plan_intention AS owner
   WHERE owner.plan_ref=requested_plan_ref
     AND owner.self_person_ref=requested_self_ref FOR UPDATE;
  IF NOT FOUND THEN
    RAISE EXCEPTION USING ERRCODE='23503',CONSTRAINT='candidate_plan_unavailable',
      MESSAGE='Self Plan unavailable';
  END IF;

  -- A new or retired rule/Actual/Outcome cannot cross this evidence check while
  -- the B04-D effect is pending. Plan and Dependency writers lock plan_intention.
  LOCK TABLE dante.schedule,dante.actual,dante.actual_realization_current_history,
    dante.outcome,dante.outcome_disposition_current_history,
    dante.temporal_constraint,dante.temporal_constraint_current_history IN SHARE MODE;

  SELECT current.state_ref,step.activity_ref INTO current_state,subject_ref
    FROM dante.plan_current_work_state AS current
    JOIN dante.plan_step_in_state AS step
      ON step.plan_ref=current.plan_ref AND step.state_ref=current.state_ref
   WHERE current.plan_ref=requested_plan_ref AND step.step_ref=requested_step_ref;
  IF NOT FOUND OR current_state IS DISTINCT FROM requested_plan_state_ref
     OR subject_ref IS NULL THEN
    RAISE EXCEPTION USING ERRCODE='40001',CONSTRAINT='candidate_plan_stale',
      MESSAGE='Plan Step changed since candidate review';
  END IF;
  PERFORM 1 FROM dante.activity_intention AS activity
   WHERE activity.activity_ref=subject_ref
     AND activity.self_person_ref=requested_self_ref FOR UPDATE;
  IF NOT FOUND OR (SELECT count(*) FROM dante.schedule AS schedule_row
                    WHERE schedule_row.subject_native_ref=subject_ref)<>1
     OR NOT EXISTS (SELECT 1 FROM dante.schedule AS schedule_row
                     WHERE schedule_row.schedule_ref=requested_schedule_ref
                       AND schedule_row.subject_native_ref=subject_ref) THEN
    RAISE EXCEPTION USING ERRCODE='40001',CONSTRAINT='candidate_schedule_stale',
      MESSAGE='Linked Activity Schedule changed since candidate review';
  END IF;
  IF NOT EXISTS (
    SELECT 1 FROM dante.schedule_current_placement AS current
     WHERE current.scoped_owner_ref=requested_schedule_ref
       AND current.material_state_ref=requested_schedule_state_ref
  ) THEN
    RAISE EXCEPTION USING ERRCODE='40001',CONSTRAINT='candidate_schedule_stale',
      MESSAGE='Accepted Schedule placement changed since candidate review';
  END IF;
  SELECT policy.material_state_ref INTO current_policy
    FROM dante.schedule_movement_policy_current_history AS policy
   WHERE policy.schedule_ref=requested_schedule_ref
     AND policy.current_until_at IS NULL FOR UPDATE OF policy;
  IF current_policy IS DISTINCT FROM requested_policy_state_ref
     OR current_policy IS NULL THEN
    RAISE EXCEPTION USING ERRCODE='40001',CONSTRAINT='candidate_policy_stale',
      MESSAGE='Movement Policy changed since candidate review';
  END IF;

  SELECT COALESCE(jsonb_agg(jsonb_build_array(
      relation.dependency_ref::text,relation.state_ref::text,
      relation.prerequisite_step_ref::text,relation.dependent_step_ref::text,
      relation.evaluation_code,
      relation.actual_material_state_ref::text,
      relation.outcome_material_state_ref::text
    ) ORDER BY relation.dependency_ref),'[]'::jsonb)
    INTO current_dependencies
    FROM dante.list_self_plan_dependencies(requested_self_ref,requested_plan_ref)
      AS relation WHERE relation.active;
  IF current_dependencies IS DISTINCT FROM requested_dependencies THEN
    RAISE EXCEPTION USING ERRCODE='40001',CONSTRAINT='candidate_dependency_stale',
      MESSAGE='Qualified Dependency basis changed since review';
  END IF;

  SELECT COALESCE(jsonb_agg(jsonb_build_array(
      rule.constraint_ref::text,current.material_state_ref::text
    ) ORDER BY rule.constraint_ref),'[]'::jsonb)
    INTO current_constraints
    FROM dante.temporal_constraint AS rule
    LEFT JOIN dante.scoped_current_material_state AS current
      ON current.scoped_owner_ref=rule.constraint_ref
     AND current.facet_code='temporal_constraint.rule'
   WHERE rule.subject_native_ref=subject_ref;
  IF current_constraints IS DISTINCT FROM requested_constraints THEN
    RAISE EXCEPTION USING ERRCODE='40001',CONSTRAINT='candidate_constraint_stale',
      MESSAGE='Temporal Constraint basis changed since review';
  END IF;
  RETURN subject_ref;
END;
$function$
""")

    _sql(r"""
CREATE FUNCTION dante.request_self_plan_candidate_move(
  requested_self_ref uuid, requested_operation_id text, requested_intent_fingerprint text,
  requested_plan_ref uuid, requested_step_ref uuid, requested_plan_state_ref uuid,
  requested_schedule_ref uuid, requested_schedule_state_ref uuid,
  requested_policy_state_ref uuid, requested_starts_at timestamptz,
  requested_ends_at timestamptz, requested_dependencies jsonb,
  requested_constraints jsonb, requested_proposal_ref uuid,
  requested_resulting_ref uuid, replay_only boolean
) RETURNS TABLE(
  schedule_ref uuid, subject_native_ref uuid, movement_policy_material_state_ref uuid,
  result_kind text, proposal_ref uuid, placement_material_state_ref uuid,
  created_at timestamptz, replayed boolean
)
LANGUAGE plpgsql SECURITY DEFINER VOLATILE PARALLEL UNSAFE
SET search_path=pg_catalog,dante,pg_temp
AS $function$
#variable_conflict error
DECLARE
  prior record;
  moved record;
  subject_ref uuid;
  b04_op text := 'b12c:'||requested_operation_id;
BEGIN
  IF requested_operation_id !~ '^[0-9a-f-]{36}$'
     OR requested_intent_fingerprint !~ '^[0-9a-f]{64}$' THEN
    RAISE EXCEPTION USING ERRCODE='22023',CONSTRAINT='candidate_request_shape',
      MESSAGE='Reviewed move command rejected';
  END IF;
  -- Serialize duplicate submissions before looking up their B04-D receipt.
  PERFORM 1 FROM dante.plan_intention AS owner
   WHERE owner.plan_ref=requested_plan_ref
     AND owner.self_person_ref=requested_self_ref FOR UPDATE;
  IF NOT FOUND THEN
    RAISE EXCEPTION USING ERRCODE='23503',CONSTRAINT='candidate_plan_unavailable',
      MESSAGE='Self Plan unavailable';
  END IF;
  SELECT operation.* INTO prior FROM dante.schedule_move_request_operation AS operation
   WHERE operation.self_person_ref=requested_self_ref AND operation.operation_id=b04_op;
  IF FOUND THEN
    IF prior.intent_fingerprint IS DISTINCT FROM requested_intent_fingerprint
       OR prior.schedule_ref IS DISTINCT FROM requested_schedule_ref
       OR prior.expected_placement_material_state_ref IS DISTINCT FROM requested_schedule_state_ref
       OR prior.starts_at IS DISTINCT FROM requested_starts_at
       OR prior.ends_at IS DISTINCT FROM requested_ends_at THEN
      RAISE EXCEPTION USING ERRCODE='23505',CONSTRAINT='candidate_operation_reused',
        MESSAGE='Reviewed move operation id reused with different intent';
    END IF;
    SELECT schedule_row.subject_native_ref INTO subject_ref
      FROM dante.schedule AS schedule_row
      JOIN dante.activity_intention AS activity
        ON activity.activity_ref=schedule_row.subject_native_ref
     WHERE schedule_row.schedule_ref=prior.schedule_ref
       AND activity.self_person_ref=requested_self_ref;
    RETURN QUERY SELECT prior.schedule_ref,subject_ref,
      prior.movement_policy_material_state_ref,prior.result_kind,
      prior.proposal_ref,prior.resulting_placement_material_state_ref,
      prior.created_at,true;
    RETURN;
  END IF;
  IF replay_only THEN
    RAISE EXCEPTION USING ERRCODE='P0002',CONSTRAINT='candidate_receipt_absent',
      MESSAGE='No prior reviewed move receipt';
  END IF;
  subject_ref := dante.assert_self_plan_candidate_basis(
    requested_self_ref,requested_plan_ref,requested_step_ref,
    requested_plan_state_ref,requested_schedule_ref,requested_schedule_state_ref,
    requested_policy_state_ref,requested_dependencies,requested_constraints
  );
  SELECT * INTO moved FROM dante.request_self_absolute_schedule_move(
    requested_self_ref,b04_op,requested_intent_fingerprint,
    requested_schedule_ref,requested_schedule_state_ref,
    requested_starts_at,requested_ends_at,
    requested_proposal_ref,requested_resulting_ref
  );
  RETURN QUERY SELECT moved.schedule_ref,moved.subject_native_ref,
    moved.movement_policy_material_state_ref,moved.result_kind,moved.proposal_ref,
    moved.placement_material_state_ref,moved.created_at,moved.replayed;
END;
$function$
""")

    _sql(r"""
CREATE FUNCTION dante.accept_self_plan_candidate_move(
  requested_self_ref uuid, requested_operation_id text, requested_intent_fingerprint text,
  requested_plan_ref uuid, requested_step_ref uuid, requested_plan_state_ref uuid,
  requested_schedule_ref uuid, requested_schedule_state_ref uuid,
  requested_policy_state_ref uuid, requested_dependencies jsonb,
  requested_constraints jsonb, requested_proposal_ref uuid, replay_only boolean
) RETURNS TABLE(
  proposal_ref uuid, schedule_ref uuid, subject_native_ref uuid,
  previous_placement_material_state_ref uuid, placement_material_state_ref uuid,
  created_at timestamptz, replayed boolean
)
LANGUAGE plpgsql SECURITY DEFINER VOLATILE PARALLEL UNSAFE
SET search_path=pg_catalog,dante,pg_temp
AS $function$
#variable_conflict error
DECLARE
  request_receipt record;
  prior record;
  proposal record;
  accepted record;
  subject_ref uuid;
  b04_op text := 'b12c-confirm:'||requested_operation_id;
BEGIN
  PERFORM 1 FROM dante.plan_intention AS owner
   WHERE owner.plan_ref=requested_plan_ref
     AND owner.self_person_ref=requested_self_ref FOR UPDATE;
  IF NOT FOUND THEN
    RAISE EXCEPTION USING ERRCODE='23503',CONSTRAINT='candidate_plan_unavailable',
      MESSAGE='Self Plan unavailable';
  END IF;
  SELECT operation.* INTO request_receipt
    FROM dante.schedule_move_request_operation AS operation
   WHERE operation.self_person_ref=requested_self_ref
     AND operation.operation_id='b12c:'||requested_operation_id;
  IF NOT FOUND OR request_receipt.result_kind<>'pending_confirmation'
     OR request_receipt.proposal_ref IS DISTINCT FROM requested_proposal_ref
     OR request_receipt.schedule_ref IS DISTINCT FROM requested_schedule_ref
     OR request_receipt.expected_placement_material_state_ref IS DISTINCT FROM requested_schedule_state_ref
     OR request_receipt.movement_policy_material_state_ref IS DISTINCT FROM requested_policy_state_ref THEN
    RAISE EXCEPTION USING ERRCODE='23503',CONSTRAINT='candidate_proposal_unavailable',
      MESSAGE='Reviewed pending move unavailable';
  END IF;
  SELECT operation.* INTO prior FROM dante.schedule_move_accept_operation AS operation
   WHERE operation.self_person_ref=requested_self_ref AND operation.operation_id=b04_op;
  IF FOUND THEN
    IF prior.intent_fingerprint IS DISTINCT FROM requested_intent_fingerprint
       OR prior.proposal_ref IS DISTINCT FROM requested_proposal_ref THEN
      RAISE EXCEPTION USING ERRCODE='23505',CONSTRAINT='candidate_confirmation_reused',
        MESSAGE='Reviewed confirmation reused with different intent';
    END IF;
    SELECT schedule_row.subject_native_ref INTO subject_ref FROM dante.schedule AS schedule_row
     WHERE schedule_row.schedule_ref=prior.schedule_ref;
    RETURN QUERY SELECT prior.proposal_ref,prior.schedule_ref,subject_ref,
      request_receipt.expected_placement_material_state_ref,
      prior.resulting_placement_material_state_ref,prior.created_at,true;
    RETURN;
  END IF;
  IF replay_only THEN
    RAISE EXCEPTION USING ERRCODE='P0002',CONSTRAINT='candidate_receipt_absent',
      MESSAGE='No prior confirmation receipt';
  END IF;
  subject_ref := dante.assert_self_plan_candidate_basis(
    requested_self_ref,requested_plan_ref,requested_step_ref,
    requested_plan_state_ref,requested_schedule_ref,requested_schedule_state_ref,
    requested_policy_state_ref,requested_dependencies,requested_constraints
  );
  SELECT * INTO proposal FROM dante.schedule_move_proposal AS entry
   WHERE entry.proposal_ref=requested_proposal_ref
     AND entry.self_person_ref=requested_self_ref;
  IF NOT FOUND OR proposal.schedule_ref IS DISTINCT FROM requested_schedule_ref
     OR proposal.expected_placement_material_state_ref IS DISTINCT FROM requested_schedule_state_ref
     OR proposal.movement_policy_material_state_ref IS DISTINCT FROM requested_policy_state_ref THEN
    RAISE EXCEPTION USING ERRCODE='40001',CONSTRAINT='candidate_proposal_stale',
      MESSAGE='Reviewed pending proposal basis changed';
  END IF;
  SELECT * INTO accepted FROM dante.accept_self_absolute_schedule_move_proposal(
    requested_self_ref,b04_op,requested_intent_fingerprint,
    requested_proposal_ref,uuidv7()
  );
  RETURN QUERY SELECT accepted.proposal_ref,accepted.schedule_ref,
    accepted.subject_native_ref,accepted.previous_placement_material_state_ref,
    accepted.placement_material_state_ref,accepted.created_at,accepted.replayed;
END;
$function$
""")
    for signature in (_GUARD, _REQUEST, _ACCEPT):
        _sql(f"ALTER FUNCTION {signature} OWNER TO dante_owner")
        _sql(f"REVOKE ALL ON FUNCTION {signature} FROM PUBLIC,dante_runtime,dante_migrator")
    for signature in (_REQUEST, _ACCEPT):
        _sql(f"GRANT EXECUTE ON FUNCTION {signature} TO dante_runtime")


def downgrade() -> None:
    raise RuntimeError("B12-C reviewed admission is forward-only.")
