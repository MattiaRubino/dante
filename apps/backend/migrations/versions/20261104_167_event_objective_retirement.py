"""Permit owner-scoped retirement of one-off Event Objectives.

Recurring Event sources still require an occurrence/source-scoped edit. This
revision retains the Activity local-exception behavior introduced at _166.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20261104_167"
down_revision: str | None = "20261103_166"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.get_bind().execute(sa.text(_RETIRE))


def downgrade() -> None:
    raise RuntimeError("20261104_167 is forward-only")


_RETIRE = r"""CREATE OR REPLACE FUNCTION dante.retire_self_temporal_objective(
    actor uuid, requested_objective uuid, requested_operation text,
    requested_fingerprint text, requested_revision bigint
) RETURNS TABLE(objective_ref uuid, replayed boolean)
LANGUAGE plpgsql SECURITY DEFINER VOLATILE PARALLEL UNSAFE
SET search_path=pg_catalog,dante,pg_temp AS $function$
#variable_conflict error
DECLARE owned record; current_definition record; bound_source uuid;
BEGIN
    IF requested_operation IS NULL OR requested_operation<>btrim(requested_operation)
       OR char_length(requested_operation) NOT BETWEEN 1 AND 200
       OR requested_fingerprint IS NULL
       OR requested_fingerprint !~ '^[0-9a-f]{64}$'
       OR requested_revision IS NULL OR requested_revision < 0 THEN
        RAISE EXCEPTION USING ERRCODE='23514',
          CONSTRAINT='temporal_objective_retirement_invalid',
          MESSAGE='Invalid retirement command';
    END IF;
    -- Serialize Activity local exceptions with source-wide reconciliation.
    SELECT generation.source_native_ref INTO bound_source
      FROM dante.temporal_objective AS item
      JOIN dante.temporal_objective_create_operation AS origin
        ON origin.objective_ref=item.objective_ref
       AND origin.self_person_ref=item.self_person_ref
      JOIN dante.routine_occurrence_activity_instance AS binding
        ON binding.activity_ref=item.subject_native_ref
       AND binding.self_person_ref=item.self_person_ref
      JOIN dante.occurrence_generation AS generation
        ON generation.occurrence_ref=binding.occurrence_ref
     WHERE item.objective_ref=requested_objective
       AND item.self_person_ref=actor
       AND left(origin.operation_id,char_length('b14:objective:'))='b14:objective:';
    IF bound_source IS NOT NULL THEN
        PERFORM pg_advisory_xact_lock(hashtextextended(
            'dante:recurrence-materialization:'||bound_source::text,0));
    END IF;
    SELECT * INTO owned FROM dante.temporal_objective AS item
     WHERE item.objective_ref=requested_objective AND item.self_person_ref=actor
       AND item.subject_kind IN ('activity','event')
       AND dante._actual_subject_owned_as(actor,item.subject_kind,item.subject_native_ref)
     FOR UPDATE;
    IF NOT FOUND THEN
        RAISE EXCEPTION USING ERRCODE='23503',
          CONSTRAINT='temporal_objective_unavailable',
          MESSAGE='Objective unavailable';
    END IF;
    IF owned.subject_kind='event' AND EXISTS (
        SELECT 1 FROM dante.event_recurrence_state AS recurrence
         WHERE recurrence.event_ref=owned.subject_native_ref
    ) THEN
        RAISE EXCEPTION USING ERRCODE='23514',
          CONSTRAINT='temporal_objective_retirement_source_unsupported',
          MESSAGE='Recurring Event source requires a scoped edit';
    END IF;
    IF owned.retired_at IS NOT NULL THEN
        IF owned.retirement_operation_id=requested_operation
           AND owned.retirement_fingerprint=requested_fingerprint THEN
            RETURN QUERY SELECT requested_objective,true;
            RETURN;
        END IF;
        RAISE EXCEPTION USING ERRCODE='23505',
          CONSTRAINT='temporal_objective_retirement_stale',
          MESSAGE='Objective was already retired';
    END IF;
    SELECT * INTO current_definition
      FROM dante.get_self_temporal_objective_definition(actor,requested_objective);
    IF NOT FOUND OR current_definition.definition_revision<>requested_revision THEN
        RAISE EXCEPTION USING ERRCODE='40001',
          CONSTRAINT='temporal_objective_retirement_stale',
          MESSAGE='Objective definition changed';
    END IF;
    IF EXISTS(
        SELECT 1 FROM dante.temporal_objective_observation AS observation
         WHERE observation.objective_ref=requested_objective
    ) OR EXISTS(
        SELECT 1 FROM dante.temporal_objective_evaluation_state AS evaluation
         WHERE evaluation.objective_ref=requested_objective
    ) THEN
        RAISE EXCEPTION USING ERRCODE='23505',
          CONSTRAINT='temporal_objective_retirement_recorded',
          MESSAGE='An Objective with recorded results cannot be retired';
    END IF;
    IF owned.subject_kind='activity' AND EXISTS (
        SELECT 1 FROM dante.temporal_objective_create_operation AS origin
         WHERE origin.objective_ref=requested_objective
           AND origin.self_person_ref=actor
           AND left(origin.operation_id,char_length('b14:objective:'))='b14:objective:'
    ) AND NOT EXISTS (
        SELECT 1 FROM dante.routine_occurrence_activity_instance AS binding
         WHERE binding.self_person_ref=actor
           AND binding.activity_ref=owned.subject_native_ref
    ) THEN
        RAISE EXCEPTION USING ERRCODE='23514',
          CONSTRAINT='temporal_objective_retirement_source_unsupported',
          MESSAGE='Unbound recurring Objective cannot be locally retired';
    END IF;
    UPDATE dante.temporal_objective AS item
       SET retired_at=clock_timestamp(),
           retirement_operation_id=requested_operation,
           retirement_fingerprint=requested_fingerprint
     WHERE item.objective_ref=requested_objective AND item.self_person_ref=actor;
    RETURN QUERY SELECT requested_objective,false;
END;
$function$;"""
