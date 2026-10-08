"""B14 M2: same-logical Objective revision and correction with immutable audit."""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20261008_125"
down_revision: str | None = "20261008_124"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

def upgrade() -> None:
    op.create_table(
        "temporal_objective_definition_revision",
        sa.Column("objective_ref",sa.Uuid(),nullable=False),
        sa.Column("revision",sa.BigInteger(),nullable=False),
        sa.Column("self_person_ref",sa.Uuid(),nullable=False),
        sa.Column("operation_id",sa.Text(),nullable=False),
        sa.Column("intent_fingerprint",sa.Text(),nullable=False),
        sa.Column("label",sa.Text(),nullable=False),
        sa.Column("result_kind",sa.Text(),nullable=False),
        sa.Column("comparator_code",sa.Text()),
        sa.Column("target_value",sa.Numeric()),
        sa.Column("target_min",sa.Numeric()),
        sa.Column("target_max",sa.Numeric()),
        sa.Column("unit_code",sa.Text()),
        sa.Column("presentation_order",sa.Integer(),nullable=False),
        sa.Column("accepted_at",sa.DateTime(timezone=True),nullable=False),
        sa.Column("applied_evaluation_state_ref",sa.Uuid()),
        sa.Column("applied_assessment_code",sa.Text()),
        sa.PrimaryKeyConstraint("objective_ref","revision",
            name="pk_temporal_objective_definition_revision"),
        sa.UniqueConstraint("self_person_ref","operation_id",
            name="uq_temporal_objective_definition_operation"),
        sa.ForeignKeyConstraint(["objective_ref"],
            ["dante.temporal_objective.objective_ref"],
            name="fk_temporal_objective_definition_objective"),
        sa.ForeignKeyConstraint(["self_person_ref"],
            ["dante.person.person_ref"],
            name="fk_temporal_objective_definition_person"),
        sa.CheckConstraint("revision>=1",
            name=op.f("ck_temporal_objective_definition_revision_positive")),
        sa.CheckConstraint("operation_id=btrim(operation_id) AND "
            "char_length(operation_id) BETWEEN 1 AND 200",
            name=op.f("ck_temporal_objective_definition_revision_operation")),
        sa.CheckConstraint("intent_fingerprint ~ '^[0-9a-f]{64}$'",
            name=op.f("ck_temporal_objective_definition_revision_fingerprint")),
        sa.CheckConstraint("result_kind IN ('boolean','quantity','qualitative','range')",
            name=op.f("ck_temporal_objective_definition_revision_kind")),
        sa.CheckConstraint("label=btrim(label) AND label<>'' AND "
            "char_length(label)<=300 AND presentation_order BETWEEN 0 AND 999",
            name=op.f("ck_temporal_objective_definition_revision_label")),
        sa.CheckConstraint("isfinite(accepted_at)",
            name=op.f("ck_temporal_objective_definition_revision_time")),
        schema="dante",
    )
    conn=op.get_bind()
    conn.exec_driver_sql(
        "ALTER TABLE dante.temporal_objective_definition_revision OWNER TO dante_owner"
    )
    conn.exec_driver_sql(
        "REVOKE ALL ON dante.temporal_objective_definition_revision "
        "FROM PUBLIC,dante_runtime,dante_migrator"
    )
    sqls = (_DEFINITION,_REVISE,_LIST,_RESULT,_CORRECT)
    for sql in sqls:
        conn.execute(sa.text(sql))
    signatures = (
      "get_self_temporal_objective_definition(uuid,uuid)",
      "revise_self_temporal_objective_definition(uuid,text,text,uuid,bigint,text,text,text,numeric,numeric,numeric,text,integer,uuid)",
      "list_self_temporal_objectives(uuid,text,uuid)",
      "record_self_temporal_objective_result(uuid,text,text,uuid,uuid,uuid,boolean,numeric,text,text)",
      "correct_self_temporal_objective_result(uuid,text,text,uuid,uuid,uuid,boolean,numeric,text,text,uuid)",
    )
    for signature in signatures:
        conn.exec_driver_sql(f"ALTER FUNCTION dante.{signature} OWNER TO dante_owner")
        conn.exec_driver_sql(
            f"REVOKE ALL ON FUNCTION dante.{signature} "
            "FROM PUBLIC,dante_runtime,dante_migrator"
        )
        conn.exec_driver_sql(
            f"GRANT EXECUTE ON FUNCTION dante.{signature} TO dante_runtime"
        )

def downgrade() -> None:
    raise RuntimeError("M2 Objective correction history is forward-only")

_DEFINITION = r"""CREATE FUNCTION dante.get_self_temporal_objective_definition(
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
SELECT o.objective_ref,
       COALESCE(edit.revision,0::bigint) AS definition_revision,
       COALESCE(edit.label,o.label) AS label,
       COALESCE(edit.result_kind,o.result_kind) AS result_kind,
       CASE WHEN edit.revision IS NOT NULL THEN edit.comparator_code
            ELSE o.comparator_code END AS comparator_code,
       CASE WHEN edit.revision IS NOT NULL THEN edit.target_value
            ELSE o.target_value END AS target_value,
       CASE WHEN edit.revision IS NOT NULL THEN edit.target_min
            ELSE o.target_min END AS target_min,
       CASE WHEN edit.revision IS NOT NULL THEN edit.target_max
            ELSE o.target_max END AS target_max,
       CASE WHEN edit.revision IS NOT NULL THEN edit.unit_code
            ELSE o.unit_code END AS unit_code,
       COALESCE(edit.presentation_order,o.presentation_order) AS presentation_order,
       history.state_ref AS evaluation_state_ref
  FROM dante.temporal_objective AS o
  LEFT JOIN LATERAL (
      SELECT r.* FROM dante.temporal_objective_definition_revision r
       WHERE r.objective_ref=o.objective_ref ORDER BY r.revision DESC LIMIT 1
  ) edit ON TRUE
  LEFT JOIN dante.temporal_objective_evaluation_current_history history
    ON history.objective_ref=o.objective_ref AND history.current_until_at IS NULL
 WHERE o.objective_ref=requested_objective AND o.self_person_ref=actor
   AND dante._actual_subject_owned_as(actor,o.subject_kind,o.subject_native_ref)
$function$;"""
_REVISE = r"""CREATE FUNCTION dante.revise_self_temporal_objective_definition(
    actor uuid, requested_operation text, requested_fingerprint text,
    requested_objective uuid, requested_revision bigint,
    requested_label text, requested_kind text, requested_comparator text,
    requested_value numeric, requested_min numeric, requested_max numeric,
    requested_unit text, requested_order integer, requested_new_evaluation uuid
) RETURNS TABLE(objective_ref uuid, definition_revision bigint,
                evaluation_state_ref uuid, assessment_code text,
                replayed boolean)
LANGUAGE plpgsql SECURITY DEFINER VOLATILE PARALLEL UNSAFE
SET search_path=pg_catalog,dante,pg_temp AS $function$
#variable_conflict error
DECLARE owned record; current record; prior record;
        current_eval record; observed record;
        accepted timestamptz; new_assessment text; new_state uuid;
BEGIN
    IF requested_operation IS NULL OR requested_operation<>btrim(requested_operation)
       OR char_length(requested_operation) NOT BETWEEN 1 AND 200
       OR requested_fingerprint IS NULL OR requested_fingerprint !~ '^[0-9a-f]{64}$'
       OR requested_revision IS NULL OR requested_revision<0
       OR uuid_extract_version(requested_new_evaluation) IS DISTINCT FROM 7
       OR requested_label IS NULL OR requested_label<>btrim(requested_label)
       OR requested_label='' OR char_length(requested_label)>300
       OR requested_order IS NULL OR requested_order<0 OR requested_order>999
       OR requested_kind NOT IN ('boolean','quantity','range','qualitative')
       OR NOT (
           (requested_kind IN ('boolean','qualitative')
            AND requested_comparator IS NULL
            AND requested_value IS NULL AND requested_min IS NULL
            AND requested_max IS NULL AND requested_unit IS NULL)
           OR (requested_kind='quantity'
            AND requested_comparator IN ('eq','gte','lte')
            AND requested_value IS NOT NULL
            AND requested_min IS NULL AND requested_max IS NULL
            AND (requested_unit IS NULL OR (
                requested_unit=btrim(requested_unit) AND requested_unit<>''
                AND char_length(requested_unit)<=40)))
           OR (requested_kind='range'
            AND requested_comparator='between'
            AND requested_value IS NULL
            AND requested_min IS NOT NULL AND requested_max IS NOT NULL
            AND requested_min<=requested_max
            AND (requested_unit IS NULL OR (
                requested_unit=btrim(requested_unit) AND requested_unit<>''
                AND char_length(requested_unit)<=40)))
       ) THEN
        RAISE EXCEPTION USING ERRCODE='23514',
          CONSTRAINT='temporal_objective_definition_invalid',
          MESSAGE='Objective definition revision invalid';
    END IF;
    SELECT * INTO owned FROM dante.temporal_objective o
     WHERE o.objective_ref=requested_objective AND o.self_person_ref=actor
       AND dante._actual_subject_owned_as(actor,o.subject_kind,o.subject_native_ref)
     FOR UPDATE;
    IF NOT FOUND THEN
        RAISE EXCEPTION USING ERRCODE='23503',
          CONSTRAINT='temporal_objective_unavailable',
          MESSAGE='Objective unavailable in self scope';
    END IF;
    SELECT * INTO prior FROM dante.temporal_objective_definition_revision r
     WHERE r.self_person_ref=actor AND r.operation_id=requested_operation;
    IF FOUND THEN
        IF prior.intent_fingerprint IS DISTINCT FROM requested_fingerprint
           OR prior.objective_ref<>requested_objective THEN
            RAISE EXCEPTION USING ERRCODE='23505',
              CONSTRAINT='temporal_objective_definition_operation_reused',
              MESSAGE='Objective definition operation reused';
        END IF;
        SELECT h.state_ref,s.assessment_code INTO new_state,new_assessment
          FROM dante.temporal_objective_evaluation_current_history h
          JOIN dante.temporal_objective_evaluation_state s ON s.state_ref=h.state_ref
         WHERE h.objective_ref=requested_objective AND h.current_until_at IS NULL;
        RETURN QUERY SELECT requested_objective,prior.revision,
                            prior.applied_evaluation_state_ref,
                            prior.applied_assessment_code,true;
        RETURN;
    END IF;
    SELECT * INTO current FROM dante.get_self_temporal_objective_definition(
        actor,requested_objective
    );
    IF current.definition_revision<>requested_revision THEN
        RAISE EXCEPTION USING ERRCODE='40001',
          CONSTRAINT='temporal_objective_definition_stale',
          MESSAGE='Objective definition changed';
    END IF;
    SELECT s.state_ref,s.assessment_code,s.observation_ref,h.current_from_at
      INTO current_eval
      FROM dante.temporal_objective_evaluation_current_history h
      JOIN dante.temporal_objective_evaluation_state s ON s.state_ref=h.state_ref
     WHERE h.objective_ref=requested_objective AND h.current_until_at IS NULL;
    IF current_eval.state_ref IS NOT NULL AND requested_kind<>current.result_kind THEN
        RAISE EXCEPTION USING ERRCODE='23505',
          CONSTRAINT='temporal_objective_definition_observation_incompatible',
          MESSAGE='Recorded observation requires a compatible Objective type';
    END IF;
    new_assessment:=current_eval.assessment_code;
    IF current_eval.observation_ref IS NOT NULL AND (
       current.result_kind IS DISTINCT FROM requested_kind
       OR current.comparator_code IS DISTINCT FROM requested_comparator
       OR current.target_value IS DISTINCT FROM requested_value
       OR current.target_min IS DISTINCT FROM requested_min
       OR current.target_max IS DISTINCT FROM requested_max
    ) THEN
        SELECT * INTO observed FROM dante.temporal_objective_observation o
         WHERE o.observation_ref=current_eval.observation_ref;
        IF requested_kind='boolean' THEN
            new_assessment:=CASE WHEN observed.observed_boolean THEN 'satisfied'
                                 ELSE 'not_satisfied' END;
        ELSIF requested_kind='quantity' THEN
            new_assessment:=CASE requested_comparator
              WHEN 'eq' THEN CASE WHEN observed.observed_numeric=requested_value
                THEN 'satisfied' ELSE 'not_satisfied' END
              WHEN 'gte' THEN CASE WHEN observed.observed_numeric>=requested_value
                THEN 'satisfied' ELSE 'not_satisfied' END
              ELSE CASE WHEN observed.observed_numeric<=requested_value
                THEN 'satisfied' ELSE 'not_satisfied' END END;
        ELSIF requested_kind='range' THEN
            new_assessment:=CASE WHEN observed.observed_numeric BETWEEN
                        requested_min AND requested_max THEN 'satisfied'
                        ELSE 'not_satisfied' END;
        END IF;
    END IF;
    accepted:=clock_timestamp();
    new_state:=current_eval.state_ref;
    IF current_eval.observation_ref IS NOT NULL
       AND new_assessment IS DISTINCT FROM current_eval.assessment_code THEN
        IF accepted<=current_eval.current_from_at THEN
            accepted:=current_eval.current_from_at+interval '1 microsecond';
        END IF;
        INSERT INTO dante.temporal_objective_evaluation_state(
            state_ref,objective_ref,observation_ref,assessment_code,recorded_at
        ) VALUES (
            requested_new_evaluation,requested_objective,
            current_eval.observation_ref,new_assessment,accepted
        );
        UPDATE dante.temporal_objective_evaluation_current_history h
           SET current_until_at=accepted
         WHERE h.objective_ref=requested_objective AND h.current_until_at IS NULL;
        INSERT INTO dante.temporal_objective_evaluation_current_history(
            objective_ref,state_ref,current_from_at,current_until_at
        ) VALUES (
            requested_objective,requested_new_evaluation,accepted,NULL
        );
        new_state:=requested_new_evaluation;
    END IF;
    INSERT INTO dante.temporal_objective_definition_revision(
        objective_ref,revision,self_person_ref,operation_id,intent_fingerprint,
        label,result_kind,comparator_code,target_value,target_min,target_max,
        unit_code,presentation_order,accepted_at,
        applied_evaluation_state_ref,applied_assessment_code
    ) VALUES (
        requested_objective,requested_revision+1,actor,requested_operation,
        requested_fingerprint,requested_label,requested_kind,
        requested_comparator,requested_value,requested_min,requested_max,
        requested_unit,requested_order,accepted,new_state,new_assessment
    );
    RETURN QUERY SELECT requested_objective,requested_revision+1,
                        new_state,new_assessment,false;
END;
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
  ORDER BY definition.presentation_order,definition.objective_ref
$function$;"""
_RESULT = r"""CREATE OR REPLACE FUNCTION dante.record_self_temporal_objective_result(
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

    PERFORM 1
      FROM dante.temporal_objective AS o
     WHERE o.objective_ref=requested_objective_ref
       AND o.self_person_ref=requested_self_person_ref
     FOR UPDATE;
    IF NOT FOUND THEN
        RAISE EXCEPTION USING ERRCODE='23503',
            CONSTRAINT='temporal_objective_unavailable',
            MESSAGE='Temporal Objective unavailable';
    END IF;
    SELECT * INTO objective
      FROM dante.get_self_temporal_objective_definition(
          requested_self_person_ref,requested_objective_ref
      );
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
$function$;"""
_CORRECT = r"""CREATE FUNCTION dante.correct_self_temporal_objective_result(
    actor uuid, requested_operation text, requested_fingerprint text,
    requested_objective uuid, requested_observation uuid, requested_state uuid,
    requested_boolean boolean, requested_numeric numeric,
    requested_qualitative text, requested_assessment text,
    requested_expected_evaluation uuid
) RETURNS TABLE(objective_ref uuid, observation_ref uuid,
                evaluation_state_ref uuid, assessment_code text, replayed boolean)
LANGUAGE plpgsql SECURITY DEFINER VOLATILE PARALLEL UNSAFE
SET search_path=pg_catalog,dante,pg_temp AS $function$
#variable_conflict error
DECLARE prior record; current_ref uuid;
BEGIN
    -- Serialise with definition revisions and existing result commands.
    PERFORM 1 FROM dante.temporal_objective obj
      WHERE obj.objective_ref=requested_objective
        AND obj.self_person_ref=actor
        AND dante._actual_subject_owned_as(
            actor,obj.subject_kind,obj.subject_native_ref
        ) FOR UPDATE;
    IF NOT FOUND THEN
       RAISE EXCEPTION USING ERRCODE='23503',
          CONSTRAINT='temporal_objective_unavailable',
          MESSAGE='Objective unavailable';
    END IF;
    SELECT * INTO prior FROM dante.temporal_objective_result_operation op
     WHERE op.self_person_ref=actor AND op.operation_id=requested_operation;
    IF FOUND THEN
        IF prior.intent_fingerprint IS DISTINCT FROM requested_fingerprint
           OR prior.objective_ref<>requested_objective THEN
            RAISE EXCEPTION USING ERRCODE='23505',
              CONSTRAINT='temporal_objective_result_operation_reused',
              MESSAGE='Objective correction operation reused';
        END IF;
        RETURN QUERY SELECT r.* FROM dante.record_self_temporal_objective_result(
           actor,requested_operation,requested_fingerprint,requested_objective,
           requested_observation,requested_state,requested_boolean,requested_numeric,
           requested_qualitative,requested_assessment
        ) r;
        RETURN;
    END IF;
    SELECT h.state_ref INTO current_ref
      FROM dante.temporal_objective_evaluation_current_history h
     WHERE h.objective_ref=requested_objective AND h.current_until_at IS NULL;
    IF current_ref IS DISTINCT FROM requested_expected_evaluation THEN
        RAISE EXCEPTION USING ERRCODE='40001',
           CONSTRAINT='temporal_objective_result_stale',
           MESSAGE='Objective result correction state changed';
    END IF;
    RETURN QUERY SELECT r.* FROM dante.record_self_temporal_objective_result(
       actor,requested_operation,requested_fingerprint,requested_objective,
       requested_observation,requested_state,requested_boolean,requested_numeric,
       requested_qualitative,requested_assessment
    ) r;
END;
$function$;"""
