"""B14 Create closure: shared Reality policy and bounded Objectives.

Revision ID: 20261006_113
Revises: 20261006_112

Reality review remains separate from Actual. Objectives are product-scoped
Criterion specifications; recorded values become Observation identities and
their assessments remain Evaluation semantics, not Outcome.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20261006_113"
down_revision: str | None = "20261006_112"
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
        "reality_review_policy",
        sa.Column("subject_kind", sa.Text(), nullable=False),
        sa.Column("subject_native_ref", sa.Uuid(), nullable=False),
        sa.Column("self_person_ref", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint(
            "subject_kind IN ('activity','event','occurrence')",
            name="ck_reality_review_policy_subject_kind",
        ),
        sa.ForeignKeyConstraint(
            ["self_person_ref"], ["dante.person.person_ref"],
            name="fk_reality_review_policy_person",
        ),
        sa.PrimaryKeyConstraint(
            "subject_kind", "subject_native_ref",
            name="pk_reality_review_policy",
        ),
        schema=_SCHEMA,
    )
    op.create_index(
        "ix_reality_review_policy_self",
        "reality_review_policy",
        ["self_person_ref", "subject_kind"],
        schema=_SCHEMA,
    )
    op.create_table(
        "reality_review_policy_state",
        sa.Column("state_ref", sa.Uuid(), nullable=False),
        sa.Column("subject_kind", sa.Text(), nullable=False),
        sa.Column("subject_native_ref", sa.Uuid(), nullable=False),
        sa.Column("mode_code", sa.Text(), nullable=False),
        sa.Column("recorded_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint(
            "uuid_extract_version(state_ref) IS NOT DISTINCT FROM 7",
            name="ck_reality_review_policy_state_uuidv7",
        ),
        sa.CheckConstraint(
            "mode_code IN ('manual','review_on_end','auto_confirm_outcome')",
            name="ck_reality_review_policy_state_mode",
        ),
        sa.CheckConstraint(
            "isfinite(recorded_at)",
            name="ck_reality_review_policy_state_recorded_at",
        ),
        sa.ForeignKeyConstraint(
            ["subject_kind", "subject_native_ref"],
            [
                "dante.reality_review_policy.subject_kind",
                "dante.reality_review_policy.subject_native_ref",
            ],
            name="fk_reality_review_policy_state_owner",
        ),
        sa.PrimaryKeyConstraint(
            "state_ref", name="pk_reality_review_policy_state"
        ),
        sa.UniqueConstraint(
            "subject_kind", "subject_native_ref", "state_ref",
            name="uq_reality_review_policy_state_owner",
        ),
        schema=_SCHEMA,
    )
    op.create_table(
        "reality_review_policy_current_history",
        sa.Column("subject_kind", sa.Text(), nullable=False),
        sa.Column("subject_native_ref", sa.Uuid(), nullable=False),
        sa.Column("state_ref", sa.Uuid(), nullable=False),
        sa.Column("current_from_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("current_until_at", sa.DateTime(timezone=True), nullable=True),
        sa.CheckConstraint(
            "isfinite(current_from_at) AND (current_until_at IS NULL OR "
            "(isfinite(current_until_at) AND current_until_at>current_from_at))",
            name="ck_reality_review_policy_current_history_interval",
        ),
        sa.ForeignKeyConstraint(
            ["subject_kind", "subject_native_ref", "state_ref"],
            [
                "dante.reality_review_policy_state.subject_kind",
                "dante.reality_review_policy_state.subject_native_ref",
                "dante.reality_review_policy_state.state_ref",
            ],
            name="fk_reality_review_policy_current_history_state",
        ),
        sa.PrimaryKeyConstraint(
            "subject_kind", "subject_native_ref", "current_from_at",
            name="pk_reality_review_policy_current_history",
        ),
        schema=_SCHEMA,
    )
    op.create_index(
        "ux_reality_review_policy_current_history_open",
        "reality_review_policy_current_history",
        ["subject_kind", "subject_native_ref"],
        unique=True,
        schema=_SCHEMA,
        postgresql_where=sa.text("current_until_at IS NULL"),
    )
    op.create_table(
        "reality_review_policy_operation",
        sa.Column("self_person_ref", sa.Uuid(), nullable=False),
        sa.Column("operation_id", sa.Text(), nullable=False),
        sa.Column("intent_fingerprint", sa.Text(), nullable=False),
        sa.Column("subject_kind", sa.Text(), nullable=False),
        sa.Column("subject_native_ref", sa.Uuid(), nullable=False),
        sa.Column("state_ref", sa.Uuid(), nullable=False),
        sa.CheckConstraint(
            "operation_id=btrim(operation_id) AND char_length(operation_id) BETWEEN 1 AND 200",
            name="ck_reality_review_policy_operation_id",
        ),
        sa.CheckConstraint(
            "intent_fingerprint ~ '^[0-9a-f]{64}$'",
            name="ck_reality_review_policy_operation_fingerprint",
        ),
        sa.ForeignKeyConstraint(
            ["self_person_ref"], ["dante.person.person_ref"],
            name="fk_reality_review_policy_operation_person",
        ),
        sa.ForeignKeyConstraint(
            ["subject_kind", "subject_native_ref", "state_ref"],
            [
                "dante.reality_review_policy_state.subject_kind",
                "dante.reality_review_policy_state.subject_native_ref",
                "dante.reality_review_policy_state.state_ref",
            ],
            name="fk_reality_review_policy_operation_state",
        ),
        sa.PrimaryKeyConstraint(
            "self_person_ref", "operation_id",
            name="pk_reality_review_policy_operation",
        ),
        schema=_SCHEMA,
    )

    # Preserve current Activity Reality policy behavior while the old bounded
    # Activity endpoint remains available for backward compatibility.
    _sql("""
INSERT INTO dante.reality_review_policy(
    subject_kind,subject_native_ref,self_person_ref,created_at
)
SELECT 'activity',p.activity_ref,p.self_person_ref,p.created_at
  FROM dante.activity_outcome_review_policy AS p
ON CONFLICT DO NOTHING;

INSERT INTO dante.reality_review_policy_state(
    state_ref,subject_kind,subject_native_ref,mode_code,recorded_at
)
SELECT s.state_ref,'activity',s.activity_ref,s.mode_code,s.recorded_at
  FROM dante.activity_outcome_review_policy_state AS s
ON CONFLICT DO NOTHING;

INSERT INTO dante.reality_review_policy_current_history(
    subject_kind,subject_native_ref,state_ref,current_from_at,current_until_at
)
SELECT 'activity',h.activity_ref,h.state_ref,h.current_from_at,h.current_until_at
  FROM dante.activity_outcome_review_policy_current_history AS h
ON CONFLICT DO NOTHING;
""")

    _sql("""
CREATE FUNCTION dante.get_self_reality_review_policy(
    requested_self_person_ref uuid,
    requested_subject_kind text,
    requested_subject_native_ref uuid
) RETURNS TABLE(
    state_ref uuid,
    mode_code text,
    current_from_at timestamptz
)
LANGUAGE plpgsql SECURITY DEFINER STABLE PARALLEL RESTRICTED
SET search_path=pg_catalog,dante,pg_temp AS $function$
BEGIN
    IF requested_subject_kind NOT IN ('activity','event','occurrence')
       OR NOT dante._actual_subject_owned_as(
            requested_self_person_ref,
            requested_subject_kind,
            requested_subject_native_ref
       ) THEN
        RETURN;
    END IF;

    RETURN QUERY
    SELECT h.state_ref, COALESCE(s.mode_code,'manual'), h.current_from_at
      FROM (SELECT 1) AS owned
 LEFT JOIN dante.reality_review_policy_current_history AS h
        ON h.subject_kind=requested_subject_kind
       AND h.subject_native_ref=requested_subject_native_ref
       AND h.current_until_at IS NULL
 LEFT JOIN dante.reality_review_policy_state AS s
        ON s.state_ref=h.state_ref;
END;
$function$;
""")

    _sql("""
CREATE FUNCTION dante.set_self_reality_review_policy(
    requested_self_person_ref uuid,
    requested_operation_id text,
    requested_intent_fingerprint text,
    requested_subject_kind text,
    requested_subject_native_ref uuid,
    requested_state_ref uuid,
    requested_mode_code text,
    requested_expected_state_ref uuid
) RETURNS TABLE(state_ref uuid, mode_code text, replayed boolean)
LANGUAGE plpgsql SECURITY DEFINER VOLATILE PARALLEL UNSAFE
SET search_path=pg_catalog,dante,pg_temp AS $function$
DECLARE
    prior record;
    current_state uuid;
    previous_from timestamptz;
    accepted_at timestamptz;
BEGIN
    IF requested_operation_id IS NULL
       OR requested_operation_id<>btrim(requested_operation_id)
       OR char_length(requested_operation_id) NOT BETWEEN 1 AND 200
       OR requested_intent_fingerprint IS NULL
       OR requested_intent_fingerprint !~ '^[0-9a-f]{64}$'
       OR requested_subject_kind NOT IN ('activity','event','occurrence')
       OR requested_mode_code NOT IN ('manual','review_on_end','auto_confirm_outcome')
       OR uuid_extract_version(requested_state_ref) IS DISTINCT FROM 7 THEN
        RAISE EXCEPTION USING ERRCODE='23514',
            CONSTRAINT='reality_review_policy_invalid',
            MESSAGE='Reality review policy command rejected';
    END IF;

    IF NOT dante._actual_subject_owned_as(
        requested_self_person_ref,
        requested_subject_kind,
        requested_subject_native_ref
    ) THEN
        RAISE EXCEPTION USING ERRCODE='23503',
            CONSTRAINT='reality_review_policy_owner_unavailable',
            MESSAGE='Reality policy subject is unavailable';
    END IF;

    SELECT * INTO prior
      FROM dante.reality_review_policy_operation AS operation
     WHERE operation.self_person_ref=requested_self_person_ref
       AND operation.operation_id=requested_operation_id;
    IF FOUND THEN
        IF prior.intent_fingerprint IS DISTINCT FROM requested_intent_fingerprint
           OR prior.subject_kind IS DISTINCT FROM requested_subject_kind
           OR prior.subject_native_ref IS DISTINCT FROM requested_subject_native_ref THEN
            RAISE EXCEPTION USING ERRCODE='23505',
                CONSTRAINT='reality_review_policy_operation_reused',
                MESSAGE='Reality review policy operation was reused';
        END IF;
        RETURN QUERY
        SELECT prior.state_ref, state.mode_code, true
          FROM dante.reality_review_policy_state AS state
         WHERE state.state_ref=prior.state_ref;
        RETURN;
    END IF;

    SELECT history.state_ref,history.current_from_at
      INTO current_state,previous_from
      FROM dante.reality_review_policy_current_history AS history
     WHERE history.subject_kind=requested_subject_kind
       AND history.subject_native_ref=requested_subject_native_ref
       AND history.current_until_at IS NULL;
    IF current_state IS DISTINCT FROM requested_expected_state_ref THEN
        RAISE EXCEPTION USING ERRCODE='40001',
            CONSTRAINT='reality_review_policy_current_conflict',
            MESSAGE='Reality review policy state changed';
    END IF;

    accepted_at:=statement_timestamp();
    IF previous_from IS NOT NULL AND accepted_at<=previous_from THEN
        accepted_at:=previous_from + interval '1 microsecond';
    END IF;

    INSERT INTO dante.reality_review_policy(
        subject_kind,subject_native_ref,self_person_ref,created_at
    ) VALUES(
        requested_subject_kind,requested_subject_native_ref,
        requested_self_person_ref,accepted_at
    ) ON CONFLICT (subject_kind,subject_native_ref) DO NOTHING;

    INSERT INTO dante.reality_review_policy_state(
        state_ref,subject_kind,subject_native_ref,mode_code,recorded_at
    ) VALUES(
        requested_state_ref,requested_subject_kind,requested_subject_native_ref,
        requested_mode_code,accepted_at
    );

    UPDATE dante.reality_review_policy_current_history AS history
       SET current_until_at=accepted_at
     WHERE history.subject_kind=requested_subject_kind
       AND history.subject_native_ref=requested_subject_native_ref
       AND history.current_until_at IS NULL;

    INSERT INTO dante.reality_review_policy_current_history(
        subject_kind,subject_native_ref,state_ref,current_from_at,current_until_at
    ) VALUES(
        requested_subject_kind,requested_subject_native_ref,
        requested_state_ref,accepted_at,NULL
    );

    INSERT INTO dante.reality_review_policy_operation(
        self_person_ref,operation_id,intent_fingerprint,
        subject_kind,subject_native_ref,state_ref
    ) VALUES(
        requested_self_person_ref,requested_operation_id,
        requested_intent_fingerprint,requested_subject_kind,
        requested_subject_native_ref,requested_state_ref
    );

    RETURN QUERY SELECT requested_state_ref,requested_mode_code,false;
END;
$function$;
""")

    op.create_table(
        "temporal_objective",
        sa.Column("objective_ref", sa.Uuid(), nullable=False),
        sa.Column("self_person_ref", sa.Uuid(), nullable=False),
        sa.Column("subject_kind", sa.Text(), nullable=False),
        sa.Column("subject_native_ref", sa.Uuid(), nullable=False),
        sa.Column("label", sa.Text(), nullable=False),
        sa.Column("result_kind", sa.Text(), nullable=False),
        sa.Column("comparator_code", sa.Text(), nullable=True),
        sa.Column("target_value", sa.Numeric(), nullable=True),
        sa.Column("target_min", sa.Numeric(), nullable=True),
        sa.Column("target_max", sa.Numeric(), nullable=True),
        sa.Column("unit_code", sa.Text(), nullable=True),
        sa.Column("presentation_order", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint(
            "uuid_extract_version(objective_ref) IS NOT DISTINCT FROM 7",
            name="ck_temporal_objective_uuidv7",
        ),
        sa.CheckConstraint(
            "subject_kind IN ('activity','event')",
            name="ck_temporal_objective_subject_kind",
        ),
        sa.CheckConstraint(
            "label=btrim(label) AND label<>'' AND char_length(label)<=300",
            name="ck_temporal_objective_label",
        ),
        sa.CheckConstraint(
            "result_kind IN ('boolean','quantity','qualitative','range')",
            name="ck_temporal_objective_result_kind",
        ),
        sa.CheckConstraint(
            "presentation_order>=0",
            name="ck_temporal_objective_presentation_order",
        ),
        sa.CheckConstraint(
            "unit_code IS NULL OR (unit_code=btrim(unit_code) AND unit_code<>'' AND char_length(unit_code)<=40)",
            name="ck_temporal_objective_unit",
        ),
        sa.CheckConstraint(
            "(result_kind IN ('boolean','qualitative') AND comparator_code IS NULL "
            "AND target_value IS NULL AND target_min IS NULL AND target_max IS NULL "
            "AND unit_code IS NULL) OR "
            "(result_kind='quantity' AND comparator_code IN ('eq','gte','lte') "
            "AND target_value IS NOT NULL AND target_min IS NULL AND target_max IS NULL) OR "
            "(result_kind='range' AND comparator_code='between' "
            "AND target_value IS NULL AND target_min IS NOT NULL AND target_max IS NOT NULL "
            "AND target_min<=target_max)",
            name="ck_temporal_objective_shape",
        ),
        sa.ForeignKeyConstraint(
            ["self_person_ref"], ["dante.person.person_ref"],
            name="fk_temporal_objective_person",
        ),
        sa.PrimaryKeyConstraint("objective_ref", name="pk_temporal_objective"),
        schema=_SCHEMA,
    )
    op.create_index(
        "ix_temporal_objective_subject",
        "temporal_objective",
        ["self_person_ref", "subject_kind", "subject_native_ref", "presentation_order"],
        schema=_SCHEMA,
    )
    op.create_table(
        "temporal_objective_create_operation",
        sa.Column("self_person_ref", sa.Uuid(), nullable=False),
        sa.Column("operation_id", sa.Text(), nullable=False),
        sa.Column("intent_fingerprint", sa.Text(), nullable=False),
        sa.Column("objective_ref", sa.Uuid(), nullable=False),
        sa.CheckConstraint(
            "operation_id=btrim(operation_id) AND char_length(operation_id) BETWEEN 1 AND 200",
            name="ck_temporal_objective_create_operation_id",
        ),
        sa.CheckConstraint(
            "intent_fingerprint ~ '^[0-9a-f]{64}$'",
            name="ck_temporal_objective_create_operation_fingerprint",
        ),
        sa.ForeignKeyConstraint(
            ["self_person_ref"], ["dante.person.person_ref"],
            name="fk_temporal_objective_create_operation_person",
        ),
        sa.ForeignKeyConstraint(
            ["objective_ref"], ["dante.temporal_objective.objective_ref"],
            name="fk_temporal_objective_create_operation_objective",
        ),
        sa.PrimaryKeyConstraint(
            "self_person_ref", "operation_id",
            name="pk_temporal_objective_create_operation",
        ),
        schema=_SCHEMA,
    )
    op.create_table(
        "temporal_objective_observation",
        sa.Column("observation_ref", sa.Uuid(), nullable=False),
        sa.Column("objective_ref", sa.Uuid(), nullable=False),
        sa.Column("observed_boolean", sa.Boolean(), nullable=True),
        sa.Column("observed_numeric", sa.Numeric(), nullable=True),
        sa.Column("qualitative_code", sa.Text(), nullable=True),
        sa.Column("recorded_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint(
            "isfinite(recorded_at)",
            name="ck_temporal_objective_observation_recorded_at",
        ),
        sa.CheckConstraint(
            "qualitative_code IS NULL OR "
            "(qualitative_code=btrim(qualitative_code) AND qualitative_code<>'' "
            "AND char_length(qualitative_code)<=120)",
            name="ck_temporal_objective_observation_qualitative",
        ),
        sa.ForeignKeyConstraint(
            ["observation_ref"], ["dante.observation.observation_ref"],
            name="fk_temporal_objective_observation_identity",
        ),
        sa.ForeignKeyConstraint(
            ["objective_ref"], ["dante.temporal_objective.objective_ref"],
            name="fk_temporal_objective_observation_objective",
        ),
        sa.PrimaryKeyConstraint(
            "observation_ref", name="pk_temporal_objective_observation"
        ),
        schema=_SCHEMA,
    )
    op.create_table(
        "temporal_objective_evaluation_state",
        sa.Column("state_ref", sa.Uuid(), nullable=False),
        sa.Column("objective_ref", sa.Uuid(), nullable=False),
        sa.Column("observation_ref", sa.Uuid(), nullable=False),
        sa.Column("assessment_code", sa.Text(), nullable=False),
        sa.Column("recorded_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint(
            "uuid_extract_version(state_ref) IS NOT DISTINCT FROM 7",
            name="ck_temporal_objective_evaluation_state_uuidv7",
        ),
        sa.CheckConstraint(
            "assessment_code IN ('satisfied','partial','not_satisfied','unknown','indeterminate')",
            name="ck_temporal_objective_evaluation_state_assessment",
        ),
        sa.CheckConstraint(
            "isfinite(recorded_at)",
            name="ck_temporal_objective_evaluation_state_recorded_at",
        ),
        sa.ForeignKeyConstraint(
            ["objective_ref"], ["dante.temporal_objective.objective_ref"],
            name="fk_temporal_objective_evaluation_state_objective",
        ),
        sa.ForeignKeyConstraint(
            ["observation_ref"], ["dante.temporal_objective_observation.observation_ref"],
            name="fk_temporal_objective_evaluation_state_observation",
        ),
        sa.PrimaryKeyConstraint(
            "state_ref", name="pk_temporal_objective_evaluation_state"
        ),
        sa.UniqueConstraint(
            "objective_ref", "state_ref",
            name="uq_temporal_objective_evaluation_state_owner",
        ),
        schema=_SCHEMA,
    )
    op.create_table(
        "temporal_objective_evaluation_current_history",
        sa.Column("objective_ref", sa.Uuid(), nullable=False),
        sa.Column("state_ref", sa.Uuid(), nullable=False),
        sa.Column("current_from_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("current_until_at", sa.DateTime(timezone=True), nullable=True),
        sa.CheckConstraint(
            "isfinite(current_from_at) AND (current_until_at IS NULL OR "
            "(isfinite(current_until_at) AND current_until_at>current_from_at))",
            name="ck_temporal_objective_evaluation_history_interval",
        ),
        sa.ForeignKeyConstraint(
            ["objective_ref", "state_ref"],
            [
                "dante.temporal_objective_evaluation_state.objective_ref",
                "dante.temporal_objective_evaluation_state.state_ref",
            ],
            name="fk_temporal_objective_evaluation_history_state",
        ),
        sa.PrimaryKeyConstraint(
            "objective_ref", "current_from_at",
            name="pk_temporal_objective_evaluation_history",
        ),
        schema=_SCHEMA,
    )
    op.create_index(
        "ux_temporal_objective_evaluation_history_open",
        "temporal_objective_evaluation_current_history",
        ["objective_ref"],
        unique=True,
        schema=_SCHEMA,
        postgresql_where=sa.text("current_until_at IS NULL"),
    )
    op.create_table(
        "temporal_objective_result_operation",
        sa.Column("self_person_ref", sa.Uuid(), nullable=False),
        sa.Column("operation_id", sa.Text(), nullable=False),
        sa.Column("intent_fingerprint", sa.Text(), nullable=False),
        sa.Column("objective_ref", sa.Uuid(), nullable=False),
        sa.Column("observation_ref", sa.Uuid(), nullable=False),
        sa.Column("state_ref", sa.Uuid(), nullable=False),
        sa.CheckConstraint(
            "operation_id=btrim(operation_id) AND char_length(operation_id) BETWEEN 1 AND 200",
            name="ck_temporal_objective_result_operation_id",
        ),
        sa.CheckConstraint(
            "intent_fingerprint ~ '^[0-9a-f]{64}$'",
            name="ck_temporal_objective_result_operation_fingerprint",
        ),
        sa.ForeignKeyConstraint(
            ["self_person_ref"], ["dante.person.person_ref"],
            name="fk_temporal_objective_result_operation_person",
        ),
        sa.ForeignKeyConstraint(
            ["objective_ref"], ["dante.temporal_objective.objective_ref"],
            name="fk_temporal_objective_result_operation_objective",
        ),
        sa.ForeignKeyConstraint(
            ["observation_ref"], ["dante.temporal_objective_observation.observation_ref"],
            name="fk_temporal_objective_result_operation_observation",
        ),
        sa.ForeignKeyConstraint(
            ["state_ref"], ["dante.temporal_objective_evaluation_state.state_ref"],
            name="fk_temporal_objective_result_operation_state",
        ),
        sa.PrimaryKeyConstraint(
            "self_person_ref", "operation_id",
            name="pk_temporal_objective_result_operation",
        ),
        schema=_SCHEMA,
    )

    _sql("""
CREATE FUNCTION dante.create_self_temporal_objective(
    requested_self_person_ref uuid,
    requested_operation_id text,
    requested_intent_fingerprint text,
    requested_objective_ref uuid,
    requested_subject_kind text,
    requested_subject_native_ref uuid,
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
       OR requested_subject_kind NOT IN ('activity','event')
       OR requested_label IS NULL OR requested_label<>btrim(requested_label)
       OR requested_label='' OR char_length(requested_label)>300
       OR requested_result_kind NOT IN ('boolean','quantity','qualitative','range')
       OR requested_presentation_order<0
       OR NOT dante._actual_subject_owned_as(
            requested_self_person_ref,
            requested_subject_kind,
            requested_subject_native_ref
       ) THEN
        RAISE EXCEPTION USING ERRCODE='23514',
            CONSTRAINT='temporal_objective_invalid',
            MESSAGE='Temporal Objective command rejected';
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
            MESSAGE='Temporal Objective shape rejected';
    END IF;

    SELECT * INTO prior
      FROM dante.temporal_objective_create_operation AS operation
     WHERE operation.self_person_ref=requested_self_person_ref
       AND operation.operation_id=requested_operation_id;
    IF FOUND THEN
        IF prior.intent_fingerprint IS DISTINCT FROM requested_intent_fingerprint THEN
            RAISE EXCEPTION USING ERRCODE='23505',
                CONSTRAINT='temporal_objective_operation_reused',
                MESSAGE='Temporal Objective operation was reused';
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
        requested_objective_ref,requested_self_person_ref,
        requested_subject_kind,requested_subject_native_ref,requested_label,
        requested_result_kind,requested_comparator_code,requested_target_value,
        requested_target_min,requested_target_max,requested_unit_code,
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
           requested_comparator_code,requested_target_value,requested_target_min,
           requested_target_max,requested_unit_code,requested_presentation_order,false;
END;
$function$;
""")

    _sql("""
CREATE FUNCTION dante.list_self_temporal_objectives(
    requested_self_person_ref uuid,
    requested_subject_kind text,
    requested_subject_native_ref uuid
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
    observation_ref uuid,
    observed_boolean boolean,
    observed_numeric numeric,
    qualitative_code text,
    evaluation_state_ref uuid,
    assessment_code text
)
LANGUAGE sql SECURITY DEFINER STABLE PARALLEL RESTRICTED
SET search_path=pg_catalog,dante,pg_temp AS $function$
    SELECT o.objective_ref,o.label,o.result_kind,o.comparator_code,
           o.target_value,o.target_min,o.target_max,o.unit_code,
           o.presentation_order,obs.observation_ref,obs.observed_boolean,
           obs.observed_numeric,obs.qualitative_code,e.state_ref,e.assessment_code
      FROM dante.temporal_objective AS o
 LEFT JOIN dante.temporal_objective_evaluation_current_history AS h
        ON h.objective_ref=o.objective_ref AND h.current_until_at IS NULL
 LEFT JOIN dante.temporal_objective_evaluation_state AS e
        ON e.objective_ref=o.objective_ref AND e.state_ref=h.state_ref
 LEFT JOIN dante.temporal_objective_observation AS obs
        ON obs.observation_ref=e.observation_ref
     WHERE o.self_person_ref=requested_self_person_ref
       AND o.subject_kind=requested_subject_kind
       AND o.subject_native_ref=requested_subject_native_ref
       AND dante._actual_subject_owned_as(
            requested_self_person_ref,
            requested_subject_kind,
            requested_subject_native_ref
       )
  ORDER BY o.presentation_order,o.objective_ref
$function$;
""")

    _sql("""
CREATE FUNCTION dante.record_self_temporal_objective_result(
    requested_self_person_ref uuid,
    requested_operation_id text,
    requested_intent_fingerprint text,
    requested_objective_ref uuid,
    requested_observation_ref uuid,
    requested_state_ref uuid,
    requested_observed_boolean boolean,
    requested_observed_numeric numeric,
    requested_qualitative_code text,
    requested_assessment_code text
) RETURNS TABLE(
    objective_ref uuid,
    observation_ref uuid,
    evaluation_state_ref uuid,
    assessment_code text,
    replayed boolean
)
LANGUAGE plpgsql SECURITY DEFINER VOLATILE PARALLEL UNSAFE
SET search_path=pg_catalog,dante,pg_temp AS $function$
DECLARE
    objective record;
    prior record;
    current_state uuid;
    previous_from timestamptz;
    accepted_at timestamptz;
    derived_assessment text;
BEGIN
    IF requested_operation_id IS NULL
       OR requested_operation_id<>btrim(requested_operation_id)
       OR char_length(requested_operation_id) NOT BETWEEN 1 AND 200
       OR requested_intent_fingerprint IS NULL
       OR requested_intent_fingerprint !~ '^[0-9a-f]{64}$'
       OR uuid_extract_version(requested_observation_ref) IS DISTINCT FROM 7
       OR uuid_extract_version(requested_state_ref) IS DISTINCT FROM 7 THEN
        RAISE EXCEPTION USING ERRCODE='23514',
            CONSTRAINT='temporal_objective_result_invalid',
            MESSAGE='Temporal Objective result command rejected';
    END IF;

    SELECT * INTO objective
      FROM dante.temporal_objective AS o
     WHERE o.objective_ref=requested_objective_ref
       AND o.self_person_ref=requested_self_person_ref
     FOR UPDATE;
    IF NOT FOUND THEN
        RAISE EXCEPTION USING ERRCODE='23503',
            CONSTRAINT='temporal_objective_unavailable',
            MESSAGE='Temporal Objective unavailable';
    END IF;

    IF objective.result_kind='boolean' THEN
        IF requested_observed_boolean IS NULL
           OR requested_observed_numeric IS NOT NULL
           OR requested_qualitative_code IS NOT NULL
           OR requested_assessment_code IS NOT NULL THEN
            RAISE EXCEPTION USING ERRCODE='23514',
                CONSTRAINT='temporal_objective_result_shape_invalid',
                MESSAGE='Boolean Objective result rejected';
        END IF;
        derived_assessment:=CASE WHEN requested_observed_boolean
            THEN 'satisfied' ELSE 'not_satisfied' END;
    ELSIF objective.result_kind='quantity' THEN
        IF requested_observed_boolean IS NOT NULL
           OR requested_observed_numeric IS NULL
           OR requested_qualitative_code IS NOT NULL
           OR requested_assessment_code IS NOT NULL THEN
            RAISE EXCEPTION USING ERRCODE='23514',
                CONSTRAINT='temporal_objective_result_shape_invalid',
                MESSAGE='Quantity Objective result rejected';
        END IF;
        derived_assessment:=CASE objective.comparator_code
            WHEN 'eq' THEN CASE WHEN requested_observed_numeric=objective.target_value
                           THEN 'satisfied' ELSE 'not_satisfied' END
            WHEN 'gte' THEN CASE WHEN requested_observed_numeric>=objective.target_value
                            THEN 'satisfied' ELSE 'not_satisfied' END
            WHEN 'lte' THEN CASE WHEN requested_observed_numeric<=objective.target_value
                            THEN 'satisfied' ELSE 'not_satisfied' END
        END;
    ELSIF objective.result_kind='range' THEN
        IF requested_observed_boolean IS NOT NULL
           OR requested_observed_numeric IS NULL
           OR requested_qualitative_code IS NOT NULL
           OR requested_assessment_code IS NOT NULL THEN
            RAISE EXCEPTION USING ERRCODE='23514',
                CONSTRAINT='temporal_objective_result_shape_invalid',
                MESSAGE='Range Objective result rejected';
        END IF;
        derived_assessment:=CASE
            WHEN requested_observed_numeric BETWEEN objective.target_min AND objective.target_max
            THEN 'satisfied' ELSE 'not_satisfied' END;
    ELSE
        IF requested_observed_boolean IS NOT NULL
           OR requested_observed_numeric IS NOT NULL
           OR requested_qualitative_code IS NULL
           OR requested_qualitative_code<>btrim(requested_qualitative_code)
           OR requested_qualitative_code=''
           OR char_length(requested_qualitative_code)>120
           OR requested_assessment_code NOT IN (
                'satisfied','partial','not_satisfied','unknown','indeterminate'
           ) THEN
            RAISE EXCEPTION USING ERRCODE='23514',
                CONSTRAINT='temporal_objective_result_shape_invalid',
                MESSAGE='Qualitative Objective result rejected';
        END IF;
        derived_assessment:=requested_assessment_code;
    END IF;

    SELECT * INTO prior
      FROM dante.temporal_objective_result_operation AS operation
     WHERE operation.self_person_ref=requested_self_person_ref
       AND operation.operation_id=requested_operation_id;
    IF FOUND THEN
        IF prior.intent_fingerprint IS DISTINCT FROM requested_intent_fingerprint
           OR prior.objective_ref IS DISTINCT FROM requested_objective_ref THEN
            RAISE EXCEPTION USING ERRCODE='23505',
                CONSTRAINT='temporal_objective_result_operation_reused',
                MESSAGE='Temporal Objective result operation was reused';
        END IF;
        RETURN QUERY
        SELECT prior.objective_ref,prior.observation_ref,prior.state_ref,
               state.assessment_code,true
          FROM dante.temporal_objective_evaluation_state AS state
         WHERE state.state_ref=prior.state_ref;
        RETURN;
    END IF;

    SELECT history.state_ref,history.current_from_at
      INTO current_state,previous_from
      FROM dante.temporal_objective_evaluation_current_history AS history
     WHERE history.objective_ref=requested_objective_ref
       AND history.current_until_at IS NULL;

    accepted_at:=statement_timestamp();
    IF previous_from IS NOT NULL AND accepted_at<=previous_from THEN
        accepted_at:=previous_from + interval '1 microsecond';
    END IF;

    INSERT INTO dante.observation(observation_ref)
    VALUES(requested_observation_ref);
    INSERT INTO dante.temporal_objective_observation(
        observation_ref,objective_ref,observed_boolean,
        observed_numeric,qualitative_code,recorded_at
    ) VALUES(
        requested_observation_ref,requested_objective_ref,
        requested_observed_boolean,requested_observed_numeric,
        requested_qualitative_code,accepted_at
    );
    INSERT INTO dante.temporal_objective_evaluation_state(
        state_ref,objective_ref,observation_ref,assessment_code,recorded_at
    ) VALUES(
        requested_state_ref,requested_objective_ref,
        requested_observation_ref,derived_assessment,accepted_at
    );

    UPDATE dante.temporal_objective_evaluation_current_history AS history
       SET current_until_at=accepted_at
     WHERE history.objective_ref=requested_objective_ref
       AND history.current_until_at IS NULL;
    INSERT INTO dante.temporal_objective_evaluation_current_history(
        objective_ref,state_ref,current_from_at,current_until_at
    ) VALUES(requested_objective_ref,requested_state_ref,accepted_at,NULL);
    INSERT INTO dante.temporal_objective_result_operation(
        self_person_ref,operation_id,intent_fingerprint,
        objective_ref,observation_ref,state_ref
    ) VALUES(
        requested_self_person_ref,requested_operation_id,
        requested_intent_fingerprint,requested_objective_ref,
        requested_observation_ref,requested_state_ref
    );

    RETURN QUERY
    SELECT requested_objective_ref,requested_observation_ref,
           requested_state_ref,derived_assessment,false;
END;
$function$;
""")

    for signature in (
        "dante.get_self_reality_review_policy(uuid,text,uuid)",
        "dante.set_self_reality_review_policy(uuid,text,text,text,uuid,uuid,text,uuid)",
        "dante.create_self_temporal_objective(uuid,text,text,uuid,text,uuid,text,text,text,numeric,numeric,numeric,text,integer)",
        "dante.list_self_temporal_objectives(uuid,text,uuid)",
        "dante.record_self_temporal_objective_result(uuid,text,text,uuid,uuid,uuid,boolean,numeric,text,text)",
    ):
        _sql(f"ALTER FUNCTION {signature} OWNER TO {_OWNER}")
        _sql(
            f"REVOKE ALL ON FUNCTION {signature} "
            f"FROM PUBLIC,{_RUNTIME},{_MIGRATOR}"
        )
        _sql(f"GRANT EXECUTE ON FUNCTION {signature} TO {_RUNTIME}")

    for table in (
        "reality_review_policy",
        "reality_review_policy_state",
        "reality_review_policy_current_history",
        "reality_review_policy_operation",
        "temporal_objective",
        "temporal_objective_create_operation",
        "temporal_objective_observation",
        "temporal_objective_evaluation_state",
        "temporal_objective_evaluation_current_history",
        "temporal_objective_result_operation",
    ):
        _sql(
            f"REVOKE ALL ON TABLE dante.{table} "
            f"FROM PUBLIC,{_RUNTIME},{_MIGRATOR}"
        )


def downgrade() -> None:
    raise RuntimeError("B14 shared Reality/Objectives requires a forward migration")
