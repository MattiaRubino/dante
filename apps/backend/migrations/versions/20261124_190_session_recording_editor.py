"""Owner-scoped retrospective Session recording and immutable timing correction."""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20261124_190"
down_revision: str | None = "20261123_189"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "session_editor_operation",
        sa.Column("self_person_ref", sa.Uuid(), nullable=False),
        sa.Column("operation_id", sa.Text(), nullable=False),
        sa.Column("intent_fingerprint", sa.Text(), nullable=False),
        sa.Column("session_ref", sa.Uuid(), nullable=False),
        sa.Column("resulting_material_state_ref", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint(
            "self_person_ref", "operation_id", name="pk_session_editor_operation"
        ),
        sa.ForeignKeyConstraint(
            ["self_person_ref"],
            ["dante.person.person_ref"],
            name="fk_session_editor_operation_person",
        ),
        sa.ForeignKeyConstraint(
            ["session_ref"],
            ["dante.session.session_ref"],
            name="fk_session_editor_operation_session",
        ),
        sa.ForeignKeyConstraint(
            ["resulting_material_state_ref"],
            ["dante.session_timing_state.material_state_ref"],
            name="fk_session_editor_operation_state",
        ),
        sa.CheckConstraint(
            "operation_id=btrim(operation_id) AND operation_id<>'' AND char_length(operation_id)<=200",
            name="operation_id",
        ),
        sa.CheckConstraint("intent_fingerprint ~ '^[0-9a-f]{64}$'", name="fingerprint"),
        schema="dante",
    )
    bind = op.get_bind()
    for definition, signature in (
        (_READ, "dante.list_self_activity_session_editor_attempts(uuid,uuid)"),
        (
            _WRITE,
            "dante.write_self_activity_session_editor(uuid,text,text,uuid,uuid,uuid,uuid,uuid,timestamptz,timestamptz,jsonb)",
        ),
    ):
        bind.exec_driver_sql(definition)
        bind.exec_driver_sql(f"ALTER FUNCTION {signature} OWNER TO dante_owner")
        bind.exec_driver_sql(
            f"REVOKE ALL ON FUNCTION {signature} FROM PUBLIC,dante_runtime,dante_migrator"
        )
        bind.exec_driver_sql(f"GRANT EXECUTE ON FUNCTION {signature} TO dante_runtime")
    bind.exec_driver_sql("ALTER TABLE dante.session_editor_operation OWNER TO dante_owner")
    bind.exec_driver_sql(
        "REVOKE ALL ON dante.session_editor_operation FROM PUBLIC,dante_runtime,dante_migrator"
    )


def downgrade() -> None:
    raise RuntimeError("Factual Session correction requires a reviewed forward migration")


_READ = r"""
CREATE FUNCTION dante.list_self_activity_session_editor_attempts(
    requested_actor uuid, requested_activity uuid
) RETURNS TABLE(
    session_ref uuid, planned_schedule_ref uuid, timing_material_state_ref uuid,
    started_at timestamptz, ended_at timestamptz, pause_ranges jsonb
)
LANGUAGE sql SECURITY DEFINER STABLE PARALLEL RESTRICTED
SET search_path=pg_catalog,dante,pg_temp AS $function$
    SELECT subject.session_ref, link.schedule_ref, current.material_state_ref,
           timing.started_at, timing.ended_at,
           COALESCE((
               SELECT jsonb_agg(jsonb_build_object(
                   'started_at', pause.paused_at, 'ended_at', pause.resumed_at
               ) ORDER BY pause.paused_at)
                 FROM dante.session_timing_pause pause
                WHERE pause.material_state_ref=current.material_state_ref
           ), '[]'::jsonb)
      FROM dante.activity_intention activity
      JOIN dante.session_execution_subject subject
        ON subject.subject_native_ref=activity.activity_ref
      JOIN dante.session_timing_current_history current
        ON current.session_ref=subject.session_ref AND current.current_until_at IS NULL
      JOIN dante.session_timing_absolute timing
        ON timing.material_state_ref=current.material_state_ref
      LEFT JOIN dante.session_planned_schedule_link link ON link.session_ref=subject.session_ref
     WHERE activity.activity_ref=requested_activity AND activity.self_person_ref=requested_actor
       AND activity.retired_at IS NULL
     ORDER BY timing.started_at, subject.session_ref;
$function$;
"""


_WRITE = r"""
CREATE FUNCTION dante.write_self_activity_session_editor(
    requested_actor uuid, requested_operation_id text, requested_fingerprint text,
    requested_activity uuid, requested_planned uuid, requested_session uuid,
    requested_expected_state uuid, requested_result_state uuid,
    requested_start timestamptz, requested_end timestamptz, requested_pauses jsonb
) RETURNS TABLE(
    session_ref uuid, subject_native_ref uuid, timing_material_state_ref uuid,
    started_at timestamptz, ended_at timestamptz, replayed boolean
)
LANGUAGE plpgsql SECURITY DEFINER VOLATILE PARALLEL UNSAFE
SET search_path=pg_catalog,dante,pg_temp AS $function$
#variable_conflict error
DECLARE
    prior record;
    previous record;
    row_pause record;
    other record;
    previous_pause_end timestamptz;
    recorded_at timestamptz := clock_timestamp();
    mode_code text;
    linked uuid;
    changed integer;
BEGIN
    IF requested_operation_id IS NULL OR requested_operation_id<>btrim(requested_operation_id)
       OR char_length(requested_operation_id) NOT BETWEEN 1 AND 200
       OR requested_fingerprint !~ '^[0-9a-f]{64}$'
       OR uuid_extract_version(requested_session) IS DISTINCT FROM 7
       OR uuid_extract_version(requested_result_state) IS DISTINCT FROM 7
       OR requested_start IS NULL OR requested_end IS NULL
       OR NOT isfinite(requested_start) OR NOT isfinite(requested_end)
       OR requested_start>=requested_end OR requested_end>recorded_at
       OR requested_pauses IS NULL OR jsonb_typeof(requested_pauses)<>'array' THEN
        RAISE EXCEPTION 'Invalid retrospective Session interval'
            USING ERRCODE='23514',CONSTRAINT='session_editor_invalid';
    END IF;
    -- Serialize all edits to one Activity, including changes to its main clock.
    SELECT activity.activity_ref INTO linked
      FROM dante.activity_intention activity
     WHERE activity.activity_ref=requested_activity AND activity.self_person_ref=requested_actor
       AND activity.retired_at IS NULL
     FOR UPDATE;
    IF linked IS NULL THEN
        RAISE EXCEPTION 'Activity unavailable'
            USING ERRCODE='23503',CONSTRAINT='session_editor_activity_unavailable';
    END IF;
    SELECT operation.* INTO prior
      FROM dante.session_editor_operation operation
     WHERE operation.self_person_ref=requested_actor
       AND operation.operation_id=requested_operation_id;
    IF FOUND THEN
        IF prior.intent_fingerprint<>requested_fingerprint THEN
            RAISE EXCEPTION 'Session editor operation id reused'
                USING ERRCODE='23505',CONSTRAINT='session_editor_operation_reused';
        END IF;
        RETURN QUERY SELECT prior.session_ref,requested_activity,
                            prior.resulting_material_state_ref,
                            timing.started_at,timing.ended_at,true
          FROM dante.session_timing_absolute timing
         WHERE timing.material_state_ref=prior.resulting_material_state_ref;
        RETURN;
    END IF;
    IF requested_planned IS NOT NULL AND NOT EXISTS (
        SELECT 1 FROM dante.activity_schedule_role role
         WHERE role.activity_ref=requested_activity
           AND role.schedule_ref=requested_planned AND role.role_code='planned'
    ) THEN
        RAISE EXCEPTION 'Planned Session unavailable'
            USING ERRCODE='23503',CONSTRAINT='session_editor_planned_unavailable';
    END IF;
    SELECT state.mode_code INTO mode_code
      FROM dante.activity_execution_policy_current_history policy
      JOIN dante.activity_execution_policy_state state
        ON state.activity_ref=policy.activity_ref AND state.state_ref=policy.state_ref
     WHERE policy.activity_ref=requested_activity AND policy.current_until_at IS NULL;
    IF requested_planned IS NULL AND COALESCE(mode_code,'disabled') NOT IN ('live','record_and_live') THEN
        RAISE EXCEPTION 'Main Session capture disabled'
            USING ERRCODE='23514',CONSTRAINT='session_editor_capture_disabled';
    END IF;
    previous_pause_end := requested_start;
    FOR row_pause IN SELECT * FROM jsonb_to_recordset(requested_pauses)
        AS p(started_at timestamptz, ended_at timestamptz)
        ORDER BY started_at
    LOOP
        IF row_pause.started_at IS NULL OR row_pause.ended_at IS NULL
           OR NOT isfinite(row_pause.started_at) OR NOT isfinite(row_pause.ended_at)
           OR row_pause.started_at<=previous_pause_end
           OR row_pause.ended_at<=row_pause.started_at
           OR row_pause.ended_at>requested_end THEN
            RAISE EXCEPTION 'Invalid Session pause interval'
                USING ERRCODE='23514',CONSTRAINT='session_editor_invalid';
        END IF;
        previous_pause_end := row_pause.ended_at;
    END LOOP;

    IF requested_expected_state IS NULL THEN
        IF EXISTS (
            SELECT 1 FROM dante.session_execution_subject subject
            LEFT JOIN dante.session_planned_schedule_link link
              ON link.session_ref=subject.session_ref
            WHERE subject.subject_native_ref=requested_activity
              AND link.schedule_ref IS NOT DISTINCT FROM requested_planned
        ) THEN
            RAISE EXCEPTION 'Session already recorded'
                USING ERRCODE='23505',CONSTRAINT='session_editor_already_recorded';
        END IF;
    ELSE
        SELECT subject.session_ref,current.material_state_ref,timing.ended_at,
               link.schedule_ref AS planned_ref
          INTO previous
          FROM dante.session_execution_subject subject
          JOIN dante.session_timing_current_history current
            ON current.session_ref=subject.session_ref AND current.current_until_at IS NULL
          JOIN dante.session_timing_absolute timing
            ON timing.material_state_ref=current.material_state_ref
          LEFT JOIN dante.session_planned_schedule_link link ON link.session_ref=subject.session_ref
         WHERE subject.session_ref=requested_session
           AND subject.subject_native_ref=requested_activity;
        IF previous.material_state_ref IS DISTINCT FROM requested_expected_state
           OR previous.ended_at IS NULL
           OR previous.planned_ref IS DISTINCT FROM requested_planned THEN
            RAISE EXCEPTION 'Session changed or remains open'
                USING ERRCODE='23505',CONSTRAINT='session_editor_stale';
        END IF;
        IF EXISTS (
            SELECT 1 FROM dante.actual_realization_session_basis basis
             WHERE basis.session_ref=requested_session
        ) THEN
            RAISE EXCEPTION 'Session is already used by a recorded outcome'
                USING ERRCODE='23505',CONSTRAINT='session_editor_dependent_actual';
        END IF;
    END IF;

    -- A named execution must fit in the active, non-paused part of a real main
    -- Session when main capture is configured. Main corrections cannot orphan
    -- any already recorded named execution.
    IF mode_code IN ('live','record_and_live') AND requested_planned IS NOT NULL THEN
        IF NOT EXISTS (
            SELECT 1 FROM dante.session_execution_subject subject
            JOIN dante.session_timing_current_history current
              ON current.session_ref=subject.session_ref AND current.current_until_at IS NULL
            JOIN dante.session_timing_absolute timing
              ON timing.material_state_ref=current.material_state_ref
            LEFT JOIN dante.session_planned_schedule_link link ON link.session_ref=subject.session_ref
            WHERE subject.subject_native_ref=requested_activity AND link.session_ref IS NULL
              AND timing.ended_at IS NOT NULL
              AND timing.started_at<=requested_start AND timing.ended_at>=requested_end
              AND NOT EXISTS (
                  SELECT 1 FROM dante.session_timing_pause pause
                   WHERE pause.material_state_ref=current.material_state_ref
                     AND pause.paused_at<requested_end AND pause.resumed_at>requested_start
                     AND NOT EXISTS (
                         SELECT 1 FROM jsonb_to_recordset(requested_pauses)
                            AS p(started_at timestamptz,ended_at timestamptz)
                          WHERE p.started_at<=greatest(pause.paused_at,requested_start)
                            AND p.ended_at>=least(pause.resumed_at,requested_end)
                     )
              )
        ) THEN
            RAISE EXCEPTION 'Named Session must fit inside active main Session'
                USING ERRCODE='23514',CONSTRAINT='session_editor_outside_main';
        END IF;
    ELSIF requested_planned IS NULL AND mode_code IN ('live','record_and_live') THEN
        FOR other IN
            SELECT timing.started_at,timing.ended_at,current.material_state_ref
              FROM dante.session_execution_subject subject
              JOIN dante.session_planned_schedule_link link ON link.session_ref=subject.session_ref
              JOIN dante.session_timing_current_history current
                ON current.session_ref=subject.session_ref AND current.current_until_at IS NULL
              JOIN dante.session_timing_absolute timing
                ON timing.material_state_ref=current.material_state_ref
             WHERE subject.subject_native_ref=requested_activity
               AND timing.ended_at IS NOT NULL
        LOOP
            IF other.started_at<requested_start OR other.ended_at>requested_end
               OR EXISTS (
                   SELECT 1 FROM jsonb_to_recordset(requested_pauses)
                       AS p(started_at timestamptz,ended_at timestamptz)
                    WHERE p.started_at<other.ended_at AND p.ended_at>other.started_at
                      AND NOT EXISTS (
                          SELECT 1 FROM dante.session_timing_pause child_pause
                           WHERE child_pause.material_state_ref=other.material_state_ref
                             AND child_pause.paused_at<=greatest(p.started_at,other.started_at)
                             AND child_pause.resumed_at>=least(p.ended_at,other.ended_at)
                      )
               ) THEN
                RAISE EXCEPTION 'Main Session cannot exclude a recorded child'
                    USING ERRCODE='23514',CONSTRAINT='session_editor_outside_main';
            END IF;
        END LOOP;
    END IF;

    IF requested_expected_state IS NULL THEN
        INSERT INTO dante.session(session_ref) VALUES(requested_session);
        INSERT INTO dante.native_address(native_ref,owner_family)
        VALUES(requested_session,'session');
    END IF;
    INSERT INTO dante.material_state_address(material_state_ref,native_owner_ref,facet_code)
    VALUES(requested_result_state,requested_session,'session.timing');
    INSERT INTO dante.session_timing_state(material_state_ref,session_ref,timing_form_code)
    VALUES(requested_result_state,requested_session,'absolute');
    INSERT INTO dante.session_timing_absolute(
        material_state_ref,started_at,start_precision_code,ended_at,end_precision_code
    ) VALUES(requested_result_state,requested_start,'exact',requested_end,'exact');
    INSERT INTO dante.session_timing_pause(
        material_state_ref,paused_at,pause_precision_code,resumed_at,resume_precision_code
    ) SELECT requested_result_state,p.started_at,'exact',p.ended_at,'exact'
        FROM jsonb_to_recordset(requested_pauses)
        AS p(started_at timestamptz,ended_at timestamptz);
    IF requested_expected_state IS NULL THEN
        INSERT INTO dante.native_current_material_state(native_owner_ref,facet_code,material_state_ref)
        VALUES(requested_session,'session.timing',requested_result_state);
        INSERT INTO dante.session_timing_current_history(session_ref,material_state_ref,current_from_at)
        VALUES(requested_session,requested_result_state,recorded_at);
        INSERT INTO dante.session_execution_subject(session_ref,subject_native_ref)
        VALUES(requested_session,requested_activity);
        IF requested_planned IS NOT NULL THEN
            INSERT INTO dante.session_planned_schedule_link(session_ref,schedule_ref,linked_at)
            VALUES(requested_session,requested_planned,recorded_at);
        END IF;
    ELSE
        UPDATE dante.native_current_material_state SET material_state_ref=requested_result_state
         WHERE native_owner_ref=requested_session AND facet_code='session.timing'
           AND material_state_ref=requested_expected_state;
        GET DIAGNOSTICS changed=ROW_COUNT;
        IF changed<>1 THEN
            RAISE EXCEPTION 'Session changed'
                USING ERRCODE='23505',CONSTRAINT='session_editor_stale';
        END IF;
        UPDATE dante.session_timing_current_history SET current_until_at=recorded_at
         WHERE session_ref=requested_session AND material_state_ref=requested_expected_state
           AND current_until_at IS NULL;
        INSERT INTO dante.session_timing_current_history(session_ref,material_state_ref,current_from_at)
        VALUES(requested_session,requested_result_state,recorded_at);
    END IF;
    INSERT INTO dante.session_editor_operation(
        self_person_ref,operation_id,intent_fingerprint,session_ref,
        resulting_material_state_ref,created_at
    ) VALUES(requested_actor,requested_operation_id,requested_fingerprint,
             requested_session,requested_result_state,recorded_at);
    RETURN QUERY SELECT requested_session,requested_activity,requested_result_state,
                        requested_start,requested_end,false;
END;
$function$;
"""
