"""B14 Create closure: recurring Reality/Objectives inheritance.

Revision ID: 20261006_114
Revises: 20261006_113

Recurring Activity templates carry Objectives to each materialized Activity.
Recurring Event policy carries Reality/Objectives to each concrete Occurrence.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20261006_114"
down_revision: str | None = "20261006_113"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_OWNER = "dante_owner"
_RUNTIME = "dante_runtime"
_MIGRATOR = "dante_migrator"


def _sql(statement: str) -> None:
    op.get_bind().exec_driver_sql(statement)


def upgrade() -> None:
    op.drop_constraint(
        "ck_temporal_objective_subject_kind",
        "temporal_objective",
        schema="dante",
        type_="check",
    )
    op.create_check_constraint(
        "ck_temporal_objective_subject_kind",
        "temporal_objective",
        "subject_kind IN ('activity','event','occurrence')",
        schema="dante",
    )

    op.add_column(
        "event_occurrence_policy",
        sa.Column(
            "reality_mode",
            sa.Text(),
            nullable=False,
            server_default=sa.text("'manual'"),
        ),
        schema="dante",
    )
    op.add_column(
        "event_occurrence_policy",
        sa.Column(
            "objectives",
            sa.dialects.postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
            server_default=sa.text("'[]'::jsonb"),
        ),
        schema="dante",
    )
    op.create_check_constraint(
        "ck_event_occurrence_policy_reality_mode",
        "event_occurrence_policy",
        "reality_mode IN ('manual','review_on_end','auto_confirm_outcome')",
        schema="dante",
    )
    op.create_check_constraint(
        "ck_event_occurrence_policy_objectives",
        "event_occurrence_policy",
        "jsonb_typeof(objectives)='array'",
        schema="dante",
    )

    _sql("""
CREATE FUNCTION dante.create_self_occurrence_objective(
    requested_self_person_ref uuid,
    requested_operation_id text,
    requested_intent_fingerprint text,
    requested_objective_ref uuid,
    requested_occurrence_ref uuid,
    requested_label text,
    requested_result_kind text,
    requested_comparator_code text,
    requested_target_value numeric,
    requested_target_min numeric,
    requested_target_max numeric,
    requested_unit_code text,
    requested_presentation_order integer
) RETURNS TABLE(
    objective_ref uuid,
    label text,
    result_kind text,
    comparator_code text,
    target_value numeric,
    target_min numeric,
    target_max numeric,
    unit_code text,
    presentation_order integer,
    replayed boolean
)
LANGUAGE plpgsql SECURITY DEFINER VOLATILE PARALLEL UNSAFE
SET search_path=pg_catalog,dante,pg_temp AS $function$
DECLARE
    prior record;
    accepted_at timestamptz;
BEGIN
    IF requested_operation_id IS NULL
       OR requested_operation_id<>btrim(requested_operation_id)
       OR char_length(requested_operation_id) NOT BETWEEN 1 AND 200
       OR requested_intent_fingerprint IS NULL
       OR requested_intent_fingerprint !~ '^[0-9a-f]{64}$'
       OR uuid_extract_version(requested_objective_ref) IS DISTINCT FROM 7
       OR requested_label IS NULL
       OR requested_label<>btrim(requested_label)
       OR requested_label=''
       OR char_length(requested_label)>300
       OR requested_result_kind NOT IN ('boolean','quantity','qualitative','range')
       OR requested_presentation_order<0
       OR NOT dante._actual_subject_owned_as(
            requested_self_person_ref,'occurrence',requested_occurrence_ref
       ) THEN
        RAISE EXCEPTION USING ERRCODE='23514',
            CONSTRAINT='temporal_objective_invalid',
            MESSAGE='Occurrence Objective command rejected';
    END IF;

    IF NOT (
        (requested_result_kind IN ('boolean','qualitative')
         AND requested_comparator_code IS NULL
         AND requested_target_value IS NULL
         AND requested_target_min IS NULL
         AND requested_target_max IS NULL
         AND requested_unit_code IS NULL)
        OR
        (requested_result_kind='quantity'
         AND requested_comparator_code IN ('eq','gte','lte')
         AND requested_target_value IS NOT NULL
         AND requested_target_min IS NULL
         AND requested_target_max IS NULL
         AND (requested_unit_code IS NULL OR (
              requested_unit_code=btrim(requested_unit_code)
              AND requested_unit_code<>''
              AND char_length(requested_unit_code)<=40
         )))
        OR
        (requested_result_kind='range'
         AND requested_comparator_code='between'
         AND requested_target_value IS NULL
         AND requested_target_min IS NOT NULL
         AND requested_target_max IS NOT NULL
         AND requested_target_min<=requested_target_max
         AND (requested_unit_code IS NULL OR (
              requested_unit_code=btrim(requested_unit_code)
              AND requested_unit_code<>''
              AND char_length(requested_unit_code)<=40
         )))
    ) THEN
        RAISE EXCEPTION USING ERRCODE='23514',
            CONSTRAINT='temporal_objective_shape_invalid',
            MESSAGE='Occurrence Objective shape rejected';
    END IF;

    SELECT * INTO prior
      FROM dante.temporal_objective_create_operation AS operation
     WHERE operation.self_person_ref=requested_self_person_ref
       AND operation.operation_id=requested_operation_id;
    IF FOUND THEN
        IF prior.intent_fingerprint IS DISTINCT FROM requested_intent_fingerprint THEN
            RAISE EXCEPTION USING ERRCODE='23505',
                CONSTRAINT='temporal_objective_operation_reused',
                MESSAGE='Occurrence Objective operation was reused';
        END IF;
        RETURN QUERY
        SELECT o.objective_ref,o.label,o.result_kind,o.comparator_code,
               o.target_value,o.target_min,o.target_max,o.unit_code,
               o.presentation_order,true
          FROM dante.temporal_objective AS o
         WHERE o.objective_ref=prior.objective_ref;
        RETURN;
    END IF;

    accepted_at:=statement_timestamp();
    INSERT INTO dante.temporal_objective(
        objective_ref,self_person_ref,subject_kind,subject_native_ref,label,
        result_kind,comparator_code,target_value,target_min,target_max,
        unit_code,presentation_order,created_at
    ) VALUES(
        requested_objective_ref,requested_self_person_ref,'occurrence',
        requested_occurrence_ref,requested_label,requested_result_kind,
        requested_comparator_code,requested_target_value,requested_target_min,
        requested_target_max,requested_unit_code,
        requested_presentation_order,accepted_at
    );
    INSERT INTO dante.temporal_objective_create_operation(
        self_person_ref,operation_id,intent_fingerprint,objective_ref
    ) VALUES(
        requested_self_person_ref,requested_operation_id,
        requested_intent_fingerprint,requested_objective_ref
    );

    RETURN QUERY
    SELECT requested_objective_ref,requested_label,requested_result_kind,
           requested_comparator_code,requested_target_value,
           requested_target_min,requested_target_max,requested_unit_code,
           requested_presentation_order,false;
END;
$function$;
""")

    _sql("""
CREATE FUNCTION dante.set_self_event_occurrence_policy_v2(
    requested_self_person_ref uuid,
    requested_event_ref uuid,
    requested_placement_kind text,
    requested_duration_minutes integer,
    requested_duration_days integer,
    requested_reminder_lead_minutes integer,
    requested_reality_mode text,
    requested_objectives jsonb
) RETURNS TABLE(
    placement_kind text,
    duration_minutes integer,
    duration_days integer,
    reminder_lead_minutes integer,
    reality_mode text,
    objectives jsonb,
    created_at timestamptz,
    replayed boolean
)
LANGUAGE plpgsql SECURITY DEFINER VOLATILE PARALLEL UNSAFE
SET search_path=pg_catalog,dante,pg_temp AS $function$
DECLARE
    prior record;
    ts timestamptz := statement_timestamp();
BEGIN
    IF requested_placement_kind NOT IN ('timed','all_day')
       OR requested_reality_mode NOT IN ('manual','review_on_end','auto_confirm_outcome')
       OR requested_objectives IS NULL
       OR jsonb_typeof(requested_objectives)<>'array'
       OR (
           requested_placement_kind='timed'
           AND (
               requested_duration_minutes IS NULL
               OR requested_duration_minutes NOT BETWEEN 1 AND 525600
               OR requested_duration_days IS NOT NULL
           )
       )
       OR (
           requested_placement_kind='all_day'
           AND (
               requested_duration_days IS NULL
               OR requested_duration_days NOT BETWEEN 1 AND 3660
               OR requested_duration_minutes IS NOT NULL
               OR requested_reminder_lead_minutes IS NOT NULL
           )
       )
       OR (
           requested_reminder_lead_minutes IS NOT NULL
           AND requested_reminder_lead_minutes NOT BETWEEN 0 AND 10080
       ) THEN
        RAISE EXCEPTION USING
            ERRCODE='23514',
            CONSTRAINT='event_occurrence_policy_invalid',
            MESSAGE='Event occurrence policy rejected';
    END IF;

    IF NOT EXISTS (
        SELECT 1
          FROM dante.event_expectation AS event
         WHERE event.event_ref=requested_event_ref
           AND event.self_person_ref=requested_self_person_ref
    ) THEN
        RAISE EXCEPTION USING
            ERRCODE='23503',
            CONSTRAINT='event_occurrence_policy_event_unavailable',
            MESSAGE='Event occurrence policy source unavailable';
    END IF;

    SELECT * INTO prior
      FROM dante.event_occurrence_policy AS policy
     WHERE policy.self_person_ref=requested_self_person_ref
       AND policy.event_ref=requested_event_ref
     FOR UPDATE;

    IF FOUND THEN
        IF prior.placement_kind IS DISTINCT FROM requested_placement_kind
           OR prior.duration_minutes IS DISTINCT FROM requested_duration_minutes
           OR prior.duration_days IS DISTINCT FROM requested_duration_days
           OR prior.reminder_lead_minutes IS DISTINCT FROM requested_reminder_lead_minutes
           OR prior.reality_mode IS DISTINCT FROM requested_reality_mode
           OR prior.objectives IS DISTINCT FROM requested_objectives THEN
            RAISE EXCEPTION USING
                ERRCODE='23505',
                CONSTRAINT='pk_event_occurrence_policy',
                MESSAGE='Event occurrence policy already exists with different intent';
        END IF;
        RETURN QUERY
        SELECT prior.placement_kind,prior.duration_minutes,prior.duration_days,
               prior.reminder_lead_minutes,prior.reality_mode,prior.objectives,
               prior.created_at,true;
        RETURN;
    END IF;

    INSERT INTO dante.event_occurrence_policy(
        self_person_ref,event_ref,placement_kind,duration_minutes,duration_days,
        reminder_lead_minutes,reality_mode,objectives,created_at
    ) VALUES(
        requested_self_person_ref,requested_event_ref,requested_placement_kind,
        requested_duration_minutes,requested_duration_days,
        requested_reminder_lead_minutes,requested_reality_mode,
        requested_objectives,ts
    );

    RETURN QUERY
    SELECT requested_placement_kind,requested_duration_minutes,
           requested_duration_days,requested_reminder_lead_minutes,
           requested_reality_mode,requested_objectives,ts,false;
END;
$function$;
""")

    _sql("""
CREATE FUNCTION dante.get_self_event_occurrence_policy_v2(uuid,uuid)
RETURNS TABLE(
    placement_kind text,
    duration_minutes integer,
    duration_days integer,
    reminder_lead_minutes integer,
    reality_mode text,
    objectives jsonb,
    created_at timestamptz
)
LANGUAGE sql SECURITY DEFINER STABLE PARALLEL SAFE
SET search_path=pg_catalog,dante,pg_temp AS $function$
SELECT policy.placement_kind,policy.duration_minutes,policy.duration_days,
       policy.reminder_lead_minutes,policy.reality_mode,policy.objectives,
       policy.created_at
  FROM dante.event_occurrence_policy AS policy
  JOIN dante.event_expectation AS event
    ON event.event_ref=policy.event_ref
 WHERE policy.self_person_ref=$1
   AND policy.event_ref=$2
   AND event.self_person_ref=$1
$function$;
""")

    for signature in (
        "dante.create_self_occurrence_objective(uuid,text,text,uuid,uuid,text,text,text,numeric,numeric,numeric,text,integer)",
        "dante.set_self_event_occurrence_policy_v2(uuid,uuid,text,integer,integer,integer,text,jsonb)",
        "dante.get_self_event_occurrence_policy_v2(uuid,uuid)",
    ):
        _sql(f"ALTER FUNCTION {signature} OWNER TO {_OWNER}")
        _sql(
            f"REVOKE ALL ON FUNCTION {signature} "
            f"FROM PUBLIC,{_RUNTIME},{_MIGRATOR}"
        )
        _sql(f"GRANT EXECUTE ON FUNCTION {signature} TO {_RUNTIME}")


def downgrade() -> None:
    raise RuntimeError("B14 recurring Reality/Objectives inheritance is forward-only")
