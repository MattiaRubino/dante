"""Check edited main/child Session containment after an atomic group settles."""

from collections.abc import Sequence

from alembic import op

revision: str = "20261125_192"
down_revision: str | None = "20261124_191"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_SIGNATURE = (
    "dante.write_self_activity_session_editor("
    "uuid,text,text,uuid,uuid,uuid,uuid,uuid,timestamptz,timestamptz,jsonb)"
)
_START = "    ELSIF requested_planned IS NULL AND mode_code IN ('live','record_and_live') THEN"
_END = "\n    END IF;\n\n    IF requested_expected_state IS NULL THEN"

_CHECK = """
CREATE FUNCTION dante.enforce_session_editor_main_children()
RETURNS trigger LANGUAGE plpgsql SECURITY DEFINER
SET search_path=pg_catalog,dante,pg_temp AS $function$
DECLARE
    main record;
    child record;
BEGIN
    SELECT subject.subject_native_ref AS activity_ref,
           timing.started_at, timing.ended_at, current.material_state_ref
      INTO main
      FROM dante.session_execution_subject subject
      JOIN dante.session_timing_current_history current
        ON current.session_ref=subject.session_ref AND current.current_until_at IS NULL
      JOIN dante.session_timing_absolute timing
        ON timing.material_state_ref=current.material_state_ref
     WHERE subject.session_ref=NEW.session_ref
       AND NOT EXISTS (
           SELECT 1 FROM dante.session_planned_schedule_link link
            WHERE link.session_ref=subject.session_ref
       );
    IF NOT FOUND OR main.ended_at IS NULL THEN
        RETURN NULL;
    END IF;

    FOR child IN
        SELECT timing.started_at, timing.ended_at, current.material_state_ref
          FROM dante.session_execution_subject subject
          JOIN dante.session_planned_schedule_link link
            ON link.session_ref=subject.session_ref
          JOIN dante.session_timing_current_history current
            ON current.session_ref=subject.session_ref AND current.current_until_at IS NULL
          JOIN dante.session_timing_absolute timing
            ON timing.material_state_ref=current.material_state_ref
         WHERE subject.subject_native_ref=main.activity_ref
           AND timing.ended_at IS NOT NULL
    LOOP
        IF child.started_at<main.started_at OR child.ended_at>main.ended_at
           OR EXISTS (
               SELECT 1 FROM dante.session_timing_pause main_pause
                WHERE main_pause.material_state_ref=main.material_state_ref
                  AND main_pause.paused_at<child.ended_at
                  AND main_pause.resumed_at>child.started_at
                  AND NOT EXISTS (
                      SELECT 1 FROM dante.session_timing_pause child_pause
                       WHERE child_pause.material_state_ref=child.material_state_ref
                         AND child_pause.paused_at<=greatest(main_pause.paused_at,child.started_at)
                         AND child_pause.resumed_at>=least(main_pause.resumed_at,child.ended_at)
                  )
           ) THEN
            RAISE EXCEPTION 'Main Session cannot exclude a recorded child'
                USING ERRCODE='23514',CONSTRAINT='session_editor_outside_main';
        END IF;
    END LOOP;
    RETURN NULL;
END;
$function$;
"""


def upgrade() -> None:
    database = op.get_bind()
    definition = database.exec_driver_sql(
        "SELECT pg_get_functiondef(%s::regprocedure)", (_SIGNATURE,)
    ).scalar_one()
    start = definition.find(_START)
    end = definition.find(_END, start) if start >= 0 else -1
    if start < 0 or end < 0 or definition.count(_START) != 1:
        raise RuntimeError("Unexpected Session editor hierarchy guard")
    # The immediate named-Session guard remains in the function. Only the
    # main-to-existing-children check moves to the deferred constraint.
    updated = definition[:start] + definition[end + 1 :]
    database.exec_driver_sql(updated.replace("%", "%%"))
    database.exec_driver_sql(_CHECK)
    database.exec_driver_sql(
        "ALTER FUNCTION dante.enforce_session_editor_main_children() OWNER TO dante_owner"
    )
    database.exec_driver_sql(
        "REVOKE ALL ON FUNCTION dante.enforce_session_editor_main_children() "
        "FROM PUBLIC,dante_runtime,dante_migrator"
    )
    database.exec_driver_sql(
        """CREATE CONSTRAINT TRIGGER ctrg_session_editor_main_children
            AFTER INSERT ON dante.session_editor_operation
            DEFERRABLE INITIALLY DEFERRED FOR EACH ROW
            EXECUTE FUNCTION dante.enforce_session_editor_main_children()"""
    )


def downgrade() -> None:
    raise RuntimeError("Forward-only Dante migration: factual Session hierarchy")
