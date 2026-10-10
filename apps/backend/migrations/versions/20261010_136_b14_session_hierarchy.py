"""B14: atomic main-to-internal Session transitions and guarded internal Start."""

from collections.abc import Sequence

from alembic import op

revision: str = "20261010_136"
down_revision: str | None = "20261009_135"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    bind = op.get_bind()
    bind.exec_driver_sql(_MAIN_TRANSITION)
    bind.exec_driver_sql(
        "ALTER FUNCTION dante.transition_self_activity_session_group("
        "uuid,text,text,uuid,uuid,uuid,text) OWNER TO dante_owner"
    )
    bind.exec_driver_sql(
        "REVOKE ALL ON FUNCTION dante.transition_self_activity_session_group("
        "uuid,text,text,uuid,uuid,uuid,text) FROM PUBLIC,dante_runtime,dante_migrator"
    )
    bind.exec_driver_sql(
        "GRANT EXECUTE ON FUNCTION dante.transition_self_activity_session_group("
        "uuid,text,text,uuid,uuid,uuid,text) TO dante_runtime"
    )
    # Preserve the accepted _135 untimed-start contract. The admission
    # additions belong AFTER replay recognition, so replay of an already
    # accepted internal execution still works after its main has ended.
    bind.exec_driver_sql(_GUARD_PLANNED_START)


def downgrade() -> None:
    raise RuntimeError("Session execution history and owner guards are forward-only")


_MAIN_TRANSITION = r"""
CREATE FUNCTION dante.transition_self_activity_session_group(
    requested_actor uuid, requested_operation_id text,
    requested_fingerprint text, requested_session uuid,
    requested_expected_state uuid, requested_result_state uuid,
    requested_transition text
) RETURNS TABLE(
    session_ref uuid, subject_native_ref uuid, timing_material_state_ref uuid,
    started_at timestamptz, ended_at timestamptz, replayed boolean
)
LANGUAGE plpgsql SECURITY DEFINER VOLATILE PARALLEL UNSAFE
SET search_path=pg_catalog,dante,pg_temp AS $function$
#variable_conflict error
DECLARE
    owned_activity uuid;
    internal_session boolean := false;
    parent_result record;
    child record;
    child_operation text;
    child_fingerprint text;
BEGIN
    IF requested_transition NOT IN ('pause','resume','end') THEN
        RAISE EXCEPTION 'Invalid Session transition'
            USING ERRCODE='22023', CONSTRAINT='session_group_transition_invalid';
    END IF;
    -- Serializes against new planned starts (whose _135 capability locks
    -- this Activity), including the final pre-cascade child enumeration.
    SELECT activity.activity_ref INTO owned_activity
      FROM dante.session_execution_subject subject
      JOIN dante.activity_intention activity
        ON activity.activity_ref=subject.subject_native_ref
     WHERE subject.session_ref=requested_session
       AND activity.self_person_ref=requested_actor
     FOR UPDATE OF activity;
    IF owned_activity IS NOT NULL THEN
        SELECT EXISTS (
            SELECT 1 FROM dante.session_planned_schedule_link link
            WHERE link.session_ref=requested_session
        ) INTO internal_session;
    END IF;

    IF requested_transition='resume' AND internal_session THEN
        IF NOT EXISTS (
            SELECT 1 FROM dante.list_self_open_activity_sessions(requested_actor) runtime
             WHERE runtime.activity_ref=owned_activity
               AND runtime.planned_schedule_ref IS NULL
               AND NOT runtime.paused
        ) THEN
            RAISE EXCEPTION 'Main Session must be running'
                USING ERRCODE='23514',
                      CONSTRAINT='session_internal_requires_running_main';
        END IF;
    END IF;

    IF requested_transition='pause' THEN
        SELECT * INTO STRICT parent_result FROM dante.pause_self_session(
            requested_actor,requested_operation_id,requested_fingerprint,
            requested_session,requested_expected_state,requested_result_state
        );
    ELSIF requested_transition='resume' THEN
        SELECT * INTO STRICT parent_result FROM dante.resume_self_session(
            requested_actor,requested_operation_id,requested_fingerprint,
            requested_session,requested_expected_state,requested_result_state
        );
    ELSE
        SELECT * INTO STRICT parent_result FROM dante.end_self_session(
            requested_actor,requested_operation_id,requested_fingerprint,
            requested_session,requested_expected_state,requested_result_state
        );
    END IF;

    IF NOT parent_result.replayed AND owned_activity IS NOT NULL
       AND NOT internal_session AND requested_transition IN ('pause','end') THEN
        FOR child IN
            SELECT runtime.session_ref,runtime.timing_material_state_ref,runtime.paused
              FROM dante.list_self_open_activity_sessions(requested_actor) runtime
             WHERE runtime.activity_ref=owned_activity
               AND runtime.planned_schedule_ref IS NOT NULL
             ORDER BY runtime.session_ref
        LOOP
            IF requested_transition='end' OR NOT child.paused THEN
                child_operation := 'group:' || md5(
                    requested_operation_id || ':' || child.session_ref::text ||
                    ':' || requested_transition
                );
                child_fingerprint := md5(
                    child_operation || ':' || child.timing_material_state_ref::text
                ) || md5('dante:b14:main-cascade:' || child_operation);
                IF requested_transition='pause' THEN
                    PERFORM dante.pause_self_session(
                        requested_actor,child_operation,child_fingerprint,
                        child.session_ref,child.timing_material_state_ref,gen_random_uuid()
                    );
                ELSE
                    PERFORM dante.end_self_session(
                        requested_actor,child_operation,child_fingerprint,
                        child.session_ref,child.timing_material_state_ref,gen_random_uuid()
                    );
                END IF;
            END IF;
        END LOOP;
    END IF;
    RETURN QUERY SELECT parent_result.session_ref,parent_result.subject_native_ref,
        parent_result.timing_material_state_ref,parent_result.started_at,
        parent_result.ended_at,parent_result.replayed;
END;
$function$;
"""


_GUARD_PLANNED_START = r"""
DO $migration$
DECLARE definition text;
        anchor text := '    IF result.replayed THEN';
BEGIN
    SELECT pg_get_functiondef(
      'dante.start_self_planned_activity_session(uuid,text,text,uuid,uuid,uuid,uuid)'::regprocedure
    ) INTO definition;
    IF strpos(definition,anchor)=0 THEN
        RAISE EXCEPTION 'Unexpected planned Session start function structure';
    END IF;
    definition := replace(definition,anchor,'
    IF NOT result.replayed AND NOT EXISTS (
        SELECT 1 FROM dante.list_self_open_activity_sessions(requested_self_person_ref) runtime
        WHERE runtime.activity_ref=requested_activity_ref
          AND runtime.planned_schedule_ref IS NULL
          AND NOT runtime.paused
    ) THEN
        RAISE EXCEPTION USING ERRCODE=''23514'',
          CONSTRAINT=''session_internal_requires_running_main'',
          MESSAGE=''Start the main Activity Session first'';
    END IF;
    IF NOT result.replayed AND EXISTS (
        SELECT 1 FROM dante.schedule_current_placement current
        JOIN dante.schedule_placement_state state
          ON state.material_state_ref=current.material_state_ref
        LEFT JOIN dante.schedule_placement_absolute_state absolute
          ON absolute.material_state_ref=state.material_state_ref
        LEFT JOIN dante.schedule_placement_named_zone_state zoned
          ON zoned.material_state_ref=state.material_state_ref
        WHERE current.scoped_owner_ref=requested_schedule_ref
          AND COALESCE(absolute.starts_at,zoned.resolved_start_at)
              > clock_timestamp()
    ) THEN
        RAISE EXCEPTION USING ERRCODE=''23514'',
          CONSTRAINT=''session_internal_before_planned_start'',
          MESSAGE=''Internal Session cannot start before planned start'';
    END IF;
' || anchor);
    EXECUTE definition;
END;
$migration$;
"""
