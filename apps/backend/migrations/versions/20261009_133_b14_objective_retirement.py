"""B14 M5: owner-scoped Objective retirement without removing recorded history."""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20261009_133"
down_revision: str | None = "20261009_132"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    bind = op.get_bind()
    bind.exec_driver_sql(
        "ALTER TABLE dante.temporal_objective "
        "ADD COLUMN retired_at timestamptz, "
        "ADD COLUMN retirement_operation_id text, "
        "ADD COLUMN retirement_fingerprint text"
    )
    for statement in (_EFFECTIVE_DEFINITION, _LIST, _RETIRE):
        bind.execute(sa.text(statement))
    for signature in (
        "get_self_temporal_objective_definition(uuid,uuid)",
        "list_self_temporal_objectives(uuid,text,uuid)",
        "retire_self_temporal_objective(uuid,uuid,text,text,bigint)",
    ):
        bind.exec_driver_sql(f"ALTER FUNCTION dante.{signature} OWNER TO dante_owner")
        bind.exec_driver_sql(
            f"REVOKE ALL ON FUNCTION dante.{signature} "
            "FROM PUBLIC,dante_runtime,dante_migrator"
        )
        bind.exec_driver_sql(f"GRANT EXECUTE ON FUNCTION dante.{signature} TO dante_runtime")


def downgrade() -> None:
    raise RuntimeError("Objective retirement history requires a reviewed forward migration")


_EFFECTIVE_DEFINITION = r"""CREATE OR REPLACE FUNCTION dante.get_self_temporal_objective_definition(
    actor uuid, requested_objective uuid
) RETURNS TABLE(
    objective_ref uuid, definition_revision bigint,
    label text, result_kind text, comparator_code text,
    target_value numeric, target_min numeric, target_max numeric,
    unit_code text, presentation_order integer,
    evaluation_state_ref uuid
)
LANGUAGE sql SECURITY DEFINER STABLE PARALLEL RESTRICTED
SET search_path=pg_catalog,dante,pg_temp AS $function$
SELECT o.objective_ref,COALESCE(local_edit.revision,0::bigint),
    CASE WHEN policy.revision IS NOT NULL AND
             (local_edit.revision IS NULL OR
              policy.accepted_at>=local_edit.accepted_at)
         THEN policy.label ELSE COALESCE(local_edit.label,o.label) END,
    CASE WHEN policy.revision IS NOT NULL AND
             (local_edit.revision IS NULL OR
              policy.accepted_at>=local_edit.accepted_at)
         THEN policy.result_kind ELSE COALESCE(local_edit.result_kind,o.result_kind) END,
    CASE WHEN policy.revision IS NOT NULL AND
             (local_edit.revision IS NULL OR
              policy.accepted_at>=local_edit.accepted_at)
         THEN policy.comparator_code
         WHEN local_edit.revision IS NOT NULL THEN local_edit.comparator_code
         ELSE o.comparator_code END,
    CASE WHEN policy.revision IS NOT NULL AND
             (local_edit.revision IS NULL OR
              policy.accepted_at>=local_edit.accepted_at)
         THEN policy.target_value
         WHEN local_edit.revision IS NOT NULL THEN local_edit.target_value
         ELSE o.target_value END,
    CASE WHEN policy.revision IS NOT NULL AND
             (local_edit.revision IS NULL OR
              policy.accepted_at>=local_edit.accepted_at)
         THEN policy.target_min
         WHEN local_edit.revision IS NOT NULL THEN local_edit.target_min
         ELSE o.target_min END,
    CASE WHEN policy.revision IS NOT NULL AND
             (local_edit.revision IS NULL OR
              policy.accepted_at>=local_edit.accepted_at)
         THEN policy.target_max
         WHEN local_edit.revision IS NOT NULL THEN local_edit.target_max
         ELSE o.target_max END,
    CASE WHEN policy.revision IS NOT NULL AND
             (local_edit.revision IS NULL OR
              policy.accepted_at>=local_edit.accepted_at)
         THEN policy.unit_code
         WHEN local_edit.revision IS NOT NULL THEN local_edit.unit_code
         ELSE o.unit_code END,
    CASE WHEN policy.revision IS NOT NULL AND
             (local_edit.revision IS NULL OR
              policy.accepted_at>=local_edit.accepted_at)
         THEN policy.presentation_order
         ELSE COALESCE(local_edit.presentation_order,o.presentation_order) END,
    hist.state_ref
  FROM dante.temporal_objective o
  LEFT JOIN LATERAL (
       SELECT r.* FROM dante.temporal_objective_definition_revision r
        WHERE r.objective_ref=o.objective_ref
        ORDER BY r.revision DESC LIMIT 1
  ) local_edit ON TRUE
  LEFT JOIN LATERAL dante.get_self_objective_series_state(
      actor,o.objective_ref
  ) origin ON TRUE
  LEFT JOIN LATERAL (
      SELECT p.* FROM dante.temporal_objective_series_edit p
       WHERE p.source_native_ref=origin.source_native_ref
         AND p.template_slot=origin.template_slot
         AND CASE
             WHEN origin.occurrence_ref IS NULL THEN FALSE
             WHEN p.selected_objective_ref=o.objective_ref THEN TRUE
             ELSE dante.occurrence_edit_coordinate_instant(
                 actor,origin.occurrence_ref,p.effective_zone_id
             ) > GREATEST(p.anchor_at,p.accepted_at)
         END
       ORDER BY p.revision DESC LIMIT 1
  ) policy ON TRUE
  LEFT JOIN dante.temporal_objective_evaluation_current_history hist
    ON hist.objective_ref=o.objective_ref AND hist.current_until_at IS NULL
 WHERE o.objective_ref=requested_objective AND o.self_person_ref=actor
   AND o.retired_at IS NULL
   AND dante._actual_subject_owned_as(actor,o.subject_kind,o.subject_native_ref)
$function$;"""

_LIST = r"""CREATE OR REPLACE FUNCTION dante.list_self_temporal_objectives(
    requested_self_person_ref uuid,
    requested_subject_kind text,
    requested_subject_native_ref uuid
) RETURNS TABLE(
    objective_ref uuid, label text, result_kind text, comparator_code text,
    target_value numeric, target_min numeric, target_max numeric,
    unit_code text, presentation_order integer,
    observation_ref uuid, observed_boolean boolean, observed_numeric numeric,
    qualitative_code text, evaluation_state_ref uuid, assessment_code text
)
LANGUAGE sql SECURITY DEFINER STABLE PARALLEL RESTRICTED
SET search_path=pg_catalog,dante,pg_temp AS $function$
    SELECT definition.objective_ref,definition.label,definition.result_kind,
           definition.comparator_code,definition.target_value,
           definition.target_min,definition.target_max,definition.unit_code,
           definition.presentation_order,obs.observation_ref,
           obs.observed_boolean,obs.observed_numeric,obs.qualitative_code,
           e.state_ref,e.assessment_code
      FROM dante.temporal_objective AS objective
      CROSS JOIN LATERAL dante.get_self_temporal_objective_definition(
          requested_self_person_ref,objective.objective_ref
      ) definition
 LEFT JOIN dante.temporal_objective_evaluation_current_history AS h
        ON h.objective_ref=objective.objective_ref AND h.current_until_at IS NULL
 LEFT JOIN dante.temporal_objective_evaluation_state AS e
        ON e.objective_ref=objective.objective_ref AND e.state_ref=h.state_ref
 LEFT JOIN dante.temporal_objective_observation AS obs
        ON obs.observation_ref=e.observation_ref
     WHERE objective.self_person_ref=requested_self_person_ref
       AND objective.subject_kind=requested_subject_kind
       AND objective.subject_native_ref=requested_subject_native_ref
       AND objective.retired_at IS NULL
  ORDER BY definition.presentation_order,definition.objective_ref
$function$;"""

_RETIRE = r"""CREATE FUNCTION dante.retire_self_temporal_objective(
    actor uuid, requested_objective uuid, requested_operation text,
    requested_fingerprint text, requested_revision bigint
) RETURNS TABLE(objective_ref uuid, replayed boolean)
LANGUAGE plpgsql SECURITY DEFINER VOLATILE PARALLEL UNSAFE
SET search_path=pg_catalog,dante,pg_temp AS $function$
#variable_conflict error
DECLARE owned record; current_definition record;
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
    SELECT * INTO owned FROM dante.temporal_objective AS item
     WHERE item.objective_ref=requested_objective AND item.self_person_ref=actor
       AND item.subject_kind='activity'
       AND dante._actual_subject_owned_as(actor,item.subject_kind,item.subject_native_ref)
     FOR UPDATE;
    IF NOT FOUND THEN
        RAISE EXCEPTION USING ERRCODE='23503',
          CONSTRAINT='temporal_objective_unavailable',
          MESSAGE='Objective unavailable';
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
    IF EXISTS (
        SELECT 1 FROM dante.temporal_objective_create_operation AS origin
         WHERE origin.objective_ref=requested_objective
           AND origin.self_person_ref=actor
           AND origin.operation_id LIKE 'b14:objective:%'
    ) THEN
        RAISE EXCEPTION USING ERRCODE='23514',
          CONSTRAINT='temporal_objective_retirement_source_unsupported',
          MESSAGE='Recurrence-derived Objective needs a source-scoped retirement policy';
    END IF;
    UPDATE dante.temporal_objective AS item
       SET retired_at=clock_timestamp(),
           retirement_operation_id=requested_operation,
           retirement_fingerprint=requested_fingerprint
     WHERE item.objective_ref=requested_objective AND item.self_person_ref=actor;
    RETURN QUERY SELECT requested_objective,false;
END;
$function$;"""
