"""M2 recurring Objective definition: stable template lineage and selected/future policy."""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20261008_126"
down_revision: str | None = "20261008_125"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

def upgrade() -> None:
    op.create_table(
        "temporal_objective_series_edit",
        sa.Column("self_person_ref",sa.Uuid(),nullable=False),
        sa.Column("operation_id",sa.Text(),nullable=False),
        sa.Column("intent_fingerprint",sa.Text(),nullable=False),
        sa.Column("source_native_ref",sa.Uuid(),nullable=False),
        sa.Column("selected_objective_ref",sa.Uuid(),nullable=False),
        sa.Column("selected_occurrence_ref",sa.Uuid(),nullable=False),
        sa.Column("template_slot",sa.Integer(),nullable=False),
        sa.Column("revision",sa.BigInteger(),nullable=False),
        sa.Column("expected_revision",sa.BigInteger(),nullable=False),
        sa.Column("expected_recurrence_state_ref",sa.Uuid()),
        sa.Column("selected_definition_revision",sa.BigInteger(),nullable=False),
        sa.Column("effective_zone_id",sa.Text(),nullable=False),
        sa.Column("anchor_at",sa.DateTime(timezone=True),nullable=False),
        sa.Column("accepted_at",sa.DateTime(timezone=True),nullable=False),
        sa.Column("label",sa.Text(),nullable=False),
        sa.Column("result_kind",sa.Text(),nullable=False),
        sa.Column("comparator_code",sa.Text()),
        sa.Column("target_value",sa.Numeric()),
        sa.Column("target_min",sa.Numeric()),
        sa.Column("target_max",sa.Numeric()),
        sa.Column("unit_code",sa.Text()),
        sa.Column("presentation_order",sa.Integer(),nullable=False),
        sa.Column("applied_evaluation_state_ref",sa.Uuid()),
        sa.Column("applied_assessment_code",sa.Text()),
        sa.PrimaryKeyConstraint("self_person_ref","operation_id",
            name="pk_temporal_objective_series_edit"),
        sa.UniqueConstraint("source_native_ref","template_slot","revision",
            name="uq_temporal_objective_series_edit_revision"),
        sa.ForeignKeyConstraint(["self_person_ref"],["dante.person.person_ref"],
            name="fk_temporal_objective_series_edit_person"),
        sa.ForeignKeyConstraint(["source_native_ref"],["dante.native_address.native_ref"],
            name="fk_temporal_objective_series_edit_source"),
        sa.ForeignKeyConstraint(["selected_objective_ref"],["dante.temporal_objective.objective_ref"],
            name="fk_temporal_objective_series_edit_objective"),
        sa.ForeignKeyConstraint(["selected_occurrence_ref"],["dante.occurrence.occurrence_ref"],
            name="fk_temporal_objective_series_edit_occurrence"),
        sa.CheckConstraint("template_slot BETWEEN 0 AND 99 AND revision>=1 "
            "AND expected_revision>=0 AND selected_definition_revision>=1",
            name=op.f("ck_temporal_objective_series_edit_revision")),
        sa.CheckConstraint("operation_id=btrim(operation_id) AND "
            "char_length(operation_id) BETWEEN 1 AND 200",
            name=op.f("ck_temporal_objective_series_edit_operation")),
        sa.CheckConstraint("intent_fingerprint ~ '^[0-9a-f]{64}$'",
            name=op.f("ck_temporal_objective_series_edit_fingerprint")),
        sa.CheckConstraint("label=btrim(label) AND label<>'' "
            "AND char_length(label)<=300 AND presentation_order BETWEEN 0 AND 999",
            name=op.f("ck_temporal_objective_series_edit_label")),
        schema="dante",
    )
    conn=op.get_bind()
    conn.exec_driver_sql("ALTER TABLE dante.temporal_objective_series_edit OWNER TO dante_owner")
    conn.exec_driver_sql("REVOKE ALL ON dante.temporal_objective_series_edit "
                         "FROM PUBLIC,dante_runtime,dante_migrator")
    for sql in (_SERIES_CONTEXT,_EFFECTIVE_DEFINITION,_SERIES_ACCEPT):
        conn.execute(sa.text(sql))
    for signature in (
        "get_self_objective_series_state(uuid,uuid)",
        "get_self_temporal_objective_definition(uuid,uuid)",
        "accept_self_objective_series_edit(uuid,uuid,text,text,bigint,bigint,uuid,text,text,text,text,numeric,numeric,numeric,text,integer,uuid)",
    ):
        conn.exec_driver_sql(f"ALTER FUNCTION dante.{signature} OWNER TO dante_owner")
        conn.exec_driver_sql(f"REVOKE ALL ON FUNCTION dante.{signature} "
                             "FROM PUBLIC,dante_runtime,dante_migrator")
        conn.exec_driver_sql(f"GRANT EXECUTE ON FUNCTION dante.{signature} TO dante_runtime")

def downgrade() -> None:
    raise RuntimeError("M2 recurring Objective source-policy history is forward-only")

_SERIES_CONTEXT = r"""CREATE FUNCTION dante.get_self_objective_series_state(
    actor uuid, requested_objective uuid
) RETURNS TABLE(
    source_native_ref uuid, occurrence_ref uuid, template_slot integer,
    source_revision bigint, recurrence_state_ref uuid
)
LANGUAGE plpgsql SECURITY DEFINER STABLE PARALLEL RESTRICTED
SET search_path=pg_catalog,dante,pg_temp AS $function$
#variable_conflict error
DECLARE obj record; operation_text text; slot_text text; slot integer;
        bound_occurrence uuid; bound_source uuid; policy_objectives jsonb;
        current_state uuid;
BEGIN
    SELECT o.* INTO obj FROM dante.temporal_objective o
     WHERE o.objective_ref=requested_objective AND o.self_person_ref=actor;
    IF NOT FOUND THEN RETURN; END IF;
    SELECT op.operation_id INTO operation_text
      FROM dante.temporal_objective_create_operation op
     WHERE op.self_person_ref=actor AND op.objective_ref=requested_objective;
    slot_text:=split_part(operation_text,':',5);
    IF slot_text IS NULL OR slot_text !~ '^(0|[1-9][0-9]?)$'
       OR obj.subject_kind NOT IN ('activity','occurrence') THEN
        RETURN;
    END IF;
    slot:=slot_text::integer;
    IF operation_text IS DISTINCT FROM format(
        'b14:objective:%s:%s:%s',obj.subject_kind,obj.subject_native_ref,slot
    ) THEN RETURN; END IF;
    IF obj.subject_kind='activity' THEN
        bound_occurrence:=dante.get_self_materialized_activity_occurrence(
            actor,obj.subject_native_ref
        );
    ELSE
        bound_occurrence:=obj.subject_native_ref;
    END IF;
    IF bound_occurrence IS NULL THEN RETURN; END IF;
    SELECT g.source_native_ref INTO bound_source
      FROM dante.get_self_occurrence(actor,bound_occurrence) g
     WHERE g.origin_code='recurrence_generated';
    IF NOT FOUND THEN RETURN; END IF;
    SELECT r.activity_template->'objectives' INTO policy_objectives
      FROM dante.routine_occurrence_policy r
     WHERE r.routine_ref=bound_source AND r.self_person_ref=actor;
    IF NOT FOUND THEN
        SELECT e.objectives INTO policy_objectives
          FROM dante.event_occurrence_policy e
         WHERE e.event_ref=bound_source AND e.self_person_ref=actor;
    END IF;
    IF jsonb_typeof(policy_objectives) IS DISTINCT FROM 'array'
       OR jsonb_array_length(policy_objectives)<=slot THEN RETURN; END IF;
    IF obj.subject_kind='activity' THEN
        SELECT r.material_state_ref INTO current_state
          FROM dante.get_self_routine_recurrence(actor,bound_source) r;
    ELSE
        SELECT r.material_state_ref INTO current_state
          FROM dante.get_self_event_recurrence(actor,bound_source) r;
    END IF;
    RETURN QUERY SELECT bound_source,bound_occurrence,slot,
        (SELECT COALESCE(MAX(p.revision),0)
           FROM dante.temporal_objective_series_edit p
          WHERE p.source_native_ref=bound_source AND p.template_slot=slot),
        current_state;
END;
$function$;"""
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
   AND dante._actual_subject_owned_as(actor,o.subject_kind,o.subject_native_ref)
$function$;"""
_SERIES_ACCEPT = r"""CREATE FUNCTION dante.accept_self_objective_series_edit(
    actor uuid, selected_objective uuid, operation text, fingerprint text,
    expected_definition bigint, expected_source bigint, expected_recurrence uuid,
    effective_zone text, requested_label text, requested_kind text,
    requested_comparator text, requested_value numeric, requested_min numeric,
    requested_max numeric, requested_unit text, requested_order integer,
    requested_evaluation uuid
) RETURNS TABLE(
    objective_ref uuid, definition_revision bigint,
    source_revision bigint, evaluation_state_ref uuid,
    assessment_code text, replayed boolean
)
LANGUAGE plpgsql SECURITY DEFINER VOLATILE PARALLEL UNSAFE
SET search_path=pg_catalog,dante,pg_temp AS $function$
#variable_conflict error
DECLARE origin record; updated_origin record; prior record; selected_revision record;
        candidate record; target_obj uuid; target_has_fact boolean;
        accepted timestamptz; anchor timestamptz;
        current_since timestamptz; target_instant timestamptz;
BEGIN
    SELECT * INTO origin FROM dante.get_self_objective_series_state(
        actor,selected_objective
    );
    IF NOT FOUND THEN
        RAISE EXCEPTION USING ERRCODE='23514',
          CONSTRAINT='temporal_objective_series_unsupported',
          MESSAGE='Objective is not a canonically generated recurring template item';
    END IF;
    -- Canonical Routine or Event owner row is the serialization point.
    PERFORM 1 FROM dante.routine_intention r
      WHERE r.routine_ref=origin.source_native_ref AND r.self_person_ref=actor FOR UPDATE;
    IF NOT FOUND THEN
        PERFORM 1 FROM dante.event_expectation e
          WHERE e.event_ref=origin.source_native_ref AND e.self_person_ref=actor FOR UPDATE;
        IF NOT FOUND THEN
            RAISE EXCEPTION USING ERRCODE='23503',
              CONSTRAINT='temporal_objective_unavailable',
              MESSAGE='Recurring source unavailable';
        END IF;
    END IF;
    SELECT * INTO prior FROM dante.temporal_objective_series_edit p
      WHERE p.self_person_ref=actor AND p.operation_id=operation;
    IF FOUND THEN
        IF prior.intent_fingerprint IS DISTINCT FROM fingerprint
           OR prior.selected_objective_ref<>selected_objective
           OR prior.expected_revision<>expected_source
           OR prior.expected_recurrence_state_ref IS DISTINCT FROM expected_recurrence
           THEN
            RAISE EXCEPTION USING ERRCODE='23505',
              CONSTRAINT='temporal_objective_series_operation_reused',
              MESSAGE='Recurring objective operation reused';
        END IF;
        RETURN QUERY SELECT selected_objective,prior.selected_definition_revision,
                prior.revision,prior.applied_evaluation_state_ref,
                prior.applied_assessment_code,true;
        RETURN;
    END IF;
    SELECT * INTO updated_origin FROM dante.get_self_objective_series_state(
        actor,selected_objective
    );
    IF updated_origin.source_revision<>expected_source OR
       updated_origin.recurrence_state_ref IS DISTINCT FROM expected_recurrence THEN
        RAISE EXCEPTION USING ERRCODE='40001',
          CONSTRAINT='temporal_objective_series_stale',
          MESSAGE='Recurring Objective source changed since preview';
    END IF;
    accepted:=clock_timestamp();
    anchor:=dante.occurrence_edit_coordinate_instant(
        actor,origin.occurrence_ref,effective_zone
    );
    -- Lock each existing future target Objective before checking facts.
    -- A concurrent Observation or individual Objective edit cannot slip
    -- between this check and the accepted source-wide policy.
    FOR candidate IN SELECT * FROM dante.list_self_recurrence_edit_occurrences(
        actor,origin.occurrence_ref
    ) LOOP
        IF candidate.occurrence_ref=origin.occurrence_ref
           OR candidate.origin_code<>'recurrence_generated' THEN CONTINUE; END IF;
        target_instant:=dante.occurrence_edit_coordinate_instant(
            actor,candidate.occurrence_ref,effective_zone
        );
        IF target_instant<=GREATEST(anchor,accepted) THEN CONTINUE; END IF;
        IF candidate.skipped OR EXISTS (
            SELECT 1 FROM dante.actual a
             WHERE a.subject_native_ref=candidate.occurrence_ref
        ) OR EXISTS (
            SELECT 1 FROM dante.routine_occurrence_activity_instance link
             JOIN dante.actual a ON a.subject_native_ref=link.activity_ref
            WHERE link.occurrence_ref=candidate.occurrence_ref
        ) THEN
            RAISE EXCEPTION USING ERRCODE='23505',
              CONSTRAINT='temporal_objective_series_future_conflict',
              MESSAGE='Future Occurrence contains a skip or recorded reality';
        END IF;
        target_obj:=NULL;
        SELECT o.objective_ref INTO target_obj
          FROM dante.temporal_objective o
          JOIN dante.temporal_objective_create_operation op
            ON op.objective_ref=o.objective_ref AND op.self_person_ref=actor
          LEFT JOIN dante.routine_occurrence_activity_instance link
            ON o.subject_kind='activity' AND link.activity_ref=o.subject_native_ref
         WHERE o.self_person_ref=actor
           AND (
                (o.subject_kind='occurrence'
                 AND o.subject_native_ref=candidate.occurrence_ref)
                OR (o.subject_kind='activity'
                    AND link.occurrence_ref=candidate.occurrence_ref)
           )
           AND op.operation_id=format(
               'b14:objective:%s:%s:%s',
               o.subject_kind,o.subject_native_ref,origin.template_slot
           )
         LIMIT 1;
        IF target_obj IS NOT NULL THEN
            PERFORM 1 FROM dante.temporal_objective o
             WHERE o.objective_ref=target_obj FOR UPDATE;
            IF EXISTS (
                SELECT 1 FROM dante.temporal_objective_definition_revision r
                 WHERE r.objective_ref=target_obj
            ) OR EXISTS (
                SELECT 1 FROM dante.temporal_objective_observation obs
                 WHERE obs.objective_ref=target_obj
            ) THEN
                RAISE EXCEPTION USING ERRCODE='23505',
                  CONSTRAINT='temporal_objective_series_future_conflict',
                  MESSAGE='Future Objective contains an individual edit or recorded fact';
            END IF;
        END IF;
    END LOOP;
    SELECT * INTO selected_revision FROM dante.revise_self_temporal_objective_definition(
        actor,operation,fingerprint,selected_objective,expected_definition,
        requested_label,requested_kind,requested_comparator,
        requested_value,requested_min,requested_max,requested_unit,
        requested_order,requested_evaluation
    );
    INSERT INTO dante.temporal_objective_series_edit(
        self_person_ref,operation_id,intent_fingerprint,source_native_ref,
        selected_objective_ref,selected_occurrence_ref,template_slot,
        revision,expected_revision,expected_recurrence_state_ref,
        selected_definition_revision,effective_zone_id,anchor_at,accepted_at,
        label,result_kind,comparator_code,target_value,target_min,target_max,
        unit_code,presentation_order,
        applied_evaluation_state_ref,applied_assessment_code
    ) VALUES(
        actor,operation,fingerprint,origin.source_native_ref,
        selected_objective,origin.occurrence_ref,origin.template_slot,
        expected_source+1,expected_source,expected_recurrence,
        selected_revision.definition_revision,effective_zone,anchor,accepted,
        requested_label,requested_kind,requested_comparator,
        requested_value,requested_min,requested_max,requested_unit,requested_order,
        selected_revision.evaluation_state_ref,selected_revision.assessment_code
    );
    RETURN QUERY SELECT selected_objective,selected_revision.definition_revision,
                expected_source+1,selected_revision.evaluation_state_ref,
                selected_revision.assessment_code,false;
END;
$function$;"""
