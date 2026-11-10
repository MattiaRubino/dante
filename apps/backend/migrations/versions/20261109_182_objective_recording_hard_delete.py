"""Irreversible recorded Objective-result removal, retaining the Objective.

Revision ID: 20261109_182
Revises: 20261108_181

The self-scoped SECURITY DEFINER capability deletes all observed values,
evaluation states, input-confirmation records and result-operation evidence
in one transaction. It does not retire or recreate the Objective definition.
"""

from collections.abc import Sequence

from alembic import op

revision: str = "20261109_182"
down_revision: str | None = "20261108_181"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_FUNCTION = r"""
CREATE FUNCTION dante.delete_self_temporal_objective_recording(
    actor uuid, requested_objective uuid, expected_evaluation_state uuid
) RETURNS TABLE(objective_ref uuid, removed_observations integer)
LANGUAGE plpgsql SECURITY DEFINER VOLATILE PARALLEL UNSAFE
SET search_path=pg_catalog,dante,pg_temp AS $function$
#variable_conflict error
DECLARE owned record; current_state uuid; observations uuid[];
BEGIN
    IF actor IS NULL OR requested_objective IS NULL
       OR expected_evaluation_state IS NULL THEN
        RAISE EXCEPTION 'Missing recorded Objective or expected state'
          USING ERRCODE='22023',
                CONSTRAINT='temporal_objective_recording_invalid';
    END IF;

    SELECT * INTO owned
      FROM dante.temporal_objective o
     WHERE o.objective_ref=requested_objective AND o.self_person_ref=actor
       AND dante._actual_subject_owned_as(
           actor,o.subject_kind,o.subject_native_ref
       )
     FOR UPDATE;
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Objective outside self scope'
          USING ERRCODE='23503',CONSTRAINT='temporal_objective_unavailable';
    END IF;

    SELECT h.state_ref INTO current_state
      FROM dante.temporal_objective_evaluation_current_history h
     WHERE h.objective_ref=requested_objective
       AND h.current_until_at IS NULL;
    IF current_state IS DISTINCT FROM expected_evaluation_state THEN
        RAISE EXCEPTION 'Objective result changed or was deleted'
          USING ERRCODE='40001',
                CONSTRAINT='temporal_objective_recording_stale';
    END IF;

    SELECT array_agg(o.observation_ref ORDER BY o.observation_ref)
      INTO observations
      FROM dante.temporal_objective_observation o
     WHERE o.objective_ref=requested_objective;
    IF COALESCE(array_length(observations,1),0)=0 THEN
        RAISE EXCEPTION 'No accepted Objective result exists'
          USING ERRCODE='40001',
                CONSTRAINT='temporal_objective_recording_stale';
    END IF;

    -- The input draft also holds confirmation metadata. Delete its entire
    -- record rather than leaving a "confirmed" or "cancelled" artefact.
    DELETE FROM dante.temporal_objective_input_draft d
     WHERE d.objective_ref=requested_objective;
    DELETE FROM dante.temporal_objective_result_operation op
     WHERE op.objective_ref=requested_objective;

    -- Definition history is retained as a definition, but must no longer
    -- identify or describe a deleted recorded Evaluation state.
    UPDATE dante.temporal_objective_definition_revision r
       SET applied_evaluation_state_ref=NULL,applied_assessment_code=NULL
     WHERE r.objective_ref=requested_objective
       AND r.applied_evaluation_state_ref IS NOT NULL;

    DELETE FROM dante.temporal_objective_evaluation_current_history h
     WHERE h.objective_ref=requested_objective;
    DELETE FROM dante.temporal_objective_evaluation_state s
     WHERE s.objective_ref=requested_objective;
    DELETE FROM dante.temporal_objective_observation o
     WHERE o.objective_ref=requested_objective;
    DELETE FROM dante.observation o
     WHERE o.observation_ref=ANY(observations);

    objective_ref:=requested_objective;
    removed_observations:=array_length(observations,1);
    RETURN NEXT;
END;
$function$;
"""


_UNRECORDED = r"""
CREATE FUNCTION dante.assert_self_temporal_objective_unrecorded(
    actor uuid, requested_objective uuid
) RETURNS void
LANGUAGE plpgsql SECURITY DEFINER VOLATILE PARALLEL UNSAFE
SET search_path=pg_catalog,dante,pg_temp AS $function$
BEGIN
    PERFORM 1 FROM dante.temporal_objective o
     WHERE o.objective_ref=requested_objective AND o.self_person_ref=actor
       AND dante._actual_subject_owned_as(
           actor,o.subject_kind,o.subject_native_ref
       )
     FOR UPDATE;
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Objective unavailable'
          USING ERRCODE='23503',CONSTRAINT='temporal_objective_unavailable';
    END IF;
    IF EXISTS (
        SELECT 1 FROM dante.temporal_objective_observation o
         WHERE o.objective_ref=requested_objective
    ) THEN
        RAISE EXCEPTION 'Recorded Objective definition is locked'
          USING ERRCODE='23505',
                CONSTRAINT='temporal_objective_recording_locked';
    END IF;
END;
$function$;
"""


def upgrade() -> None:
    bind = op.get_bind()
    for sql in (_FUNCTION, _UNRECORDED):
        bind.exec_driver_sql(sql)
    for signature in (
        "dante.delete_self_temporal_objective_recording(uuid,uuid,uuid)",
        "dante.assert_self_temporal_objective_unrecorded(uuid,uuid)",
    ):
        bind.exec_driver_sql(f"ALTER FUNCTION {signature} OWNER TO dante_owner")
        bind.exec_driver_sql(
            f"REVOKE ALL ON FUNCTION {signature} FROM PUBLIC,dante_runtime,dante_migrator"
        )
        bind.exec_driver_sql(f"GRANT EXECUTE ON FUNCTION {signature} TO dante_runtime")


def downgrade() -> None:
    raise RuntimeError("Objective recorded-result deletion is forward-only")
