"""Guard generated Activity admission against deleted/invalid Routine Occurrences.

Revision ID: 20261015_150
Revises: 20261014_149

The authoring receipt is committed before the final generated Activity binding.
Acquire a source/Occurrence row lock at receipt creation so a coordinated
deletion may serialize with it. Binding must independently refuse skipped
Occurrences and sources outside the authenticated actor's scope.

This migration is *not* itself a recurring hard-deletion capability.
"""
from collections.abc import Sequence

from alembic import op

revision: str = "20261015_150"
down_revision: str | None = "20261014_149"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ADMISSION = r"""
CREATE FUNCTION dante.guard_generated_activity_creation()
RETURNS trigger
LANGUAGE plpgsql SECURITY DEFINER VOLATILE PARALLEL UNSAFE
SET search_path=pg_catalog,dante,pg_temp
AS $admission$
DECLARE
    candidate_text text;
    candidate uuid;
    source_ref uuid;
BEGIN
    IF left(NEW.operation_id, char_length('b14:occurrence-activity:'))
       <> 'b14:occurrence-activity:' THEN
        RETURN NEW;
    END IF;

    candidate_text := substring(
        NEW.operation_id FROM char_length('b14:occurrence-activity:') + 1
    );
    IF candidate_text IS NULL OR
       candidate_text !~* '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
    THEN
        RAISE EXCEPTION USING ERRCODE='23514',
            CONSTRAINT='generated_activity_occurrence_invalid',
            MESSAGE='Generated Activity requires a valid Occurrence identity';
    END IF;
    candidate := candidate_text::uuid;

    SELECT g.source_native_ref INTO source_ref
      FROM dante.occurrence_generation AS g
      JOIN dante.routine_intention AS r
        ON r.routine_ref=g.source_native_ref
       AND r.self_person_ref=NEW.self_person_ref
     WHERE g.occurrence_ref=candidate
       AND NOT EXISTS (
         SELECT 1 FROM dante.occurrence_skip AS skipped
          WHERE skipped.occurrence_ref=candidate
       )
     FOR SHARE OF g,r;
    -- Take a fresh READ COMMITTED statement snapshot after acquiring the
    -- generation lock: a concurrent skipper may have committed while we waited.
    IF source_ref IS NULL OR EXISTS (
        SELECT 1 FROM dante.occurrence_skip AS skipped
        WHERE skipped.occurrence_ref=candidate
    ) THEN
        RAISE EXCEPTION USING ERRCODE='23514',
            CONSTRAINT='generated_activity_occurrence_unavailable',
            MESSAGE='Generated Activity Occurrence is deleted, skipped or not owned';
    END IF;
    RETURN NEW;
END;
$admission$;
"""

_BIND = r"""
CREATE OR REPLACE FUNCTION dante.bind_self_routine_occurrence_activity(
    uuid, uuid, uuid
) RETURNS TABLE(occurrence_ref uuid,activity_ref uuid,created_at timestamptz,replayed boolean)
LANGUAGE plpgsql SECURITY DEFINER VOLATILE PARALLEL UNSAFE
SET search_path=pg_catalog,dante,pg_temp
AS $binding$
#variable_conflict error
DECLARE prior dante.routine_occurrence_activity_instance%ROWTYPE;
        accepted_at timestamptz:=statement_timestamp();
BEGIN
    -- The same source and Occurrence locks are used at generated creation.
    PERFORM 1 FROM dante.occurrence_generation AS g
      JOIN dante.routine_intention AS routine
        ON routine.routine_ref=g.source_native_ref
       AND routine.self_person_ref=$1
     WHERE g.occurrence_ref=$2
       AND NOT EXISTS (
         SELECT 1 FROM dante.occurrence_skip AS skipped
          WHERE skipped.occurrence_ref=$2
       )
     FOR SHARE OF g,routine;
    -- Re-read skip only *after* the lock, never rely solely on a snapshot
    -- obtained before a concurrent skip transaction committed.
    IF NOT FOUND OR EXISTS(
      SELECT 1 FROM dante.occurrence_skip AS skipped
       WHERE skipped.occurrence_ref=$2
    ) OR NOT EXISTS(
      SELECT 1 FROM dante.activity_intention AS activity
       WHERE activity.activity_ref=$3
         AND activity.self_person_ref=$1
         AND activity.retired_at IS NULL
    ) THEN
        RAISE EXCEPTION USING ERRCODE='23503',
            CONSTRAINT='routine_occurrence_activity_instance_unavailable',
            MESSAGE='Generated Activity cannot bind to deleted or foreign Occurrence';
    END IF;

    SELECT * INTO prior
      FROM dante.routine_occurrence_activity_instance AS linked
     WHERE linked.occurrence_ref=$2 FOR UPDATE;
    IF FOUND THEN
        IF prior.activity_ref IS DISTINCT FROM $3 OR
           prior.self_person_ref IS DISTINCT FROM $1 THEN
            RAISE EXCEPTION USING ERRCODE='23505',
                CONSTRAINT='routine_occurrence_activity_instance_conflict',
                MESSAGE='Existing generated instance has another Activity';
        END IF;
        RETURN QUERY SELECT prior.occurrence_ref,prior.activity_ref,
                            prior.created_at,true;
        RETURN;
    END IF;

    INSERT INTO dante.routine_occurrence_activity_instance(
        occurrence_ref,activity_ref,self_person_ref,created_at
    ) VALUES($2,$3,$1,accepted_at);
    RETURN QUERY SELECT $2,$3,accepted_at,false;
END;
$binding$;
"""

def upgrade() -> None:
    db = op.get_bind()
    db.exec_driver_sql(_ADMISSION)
    db.exec_driver_sql(
        "ALTER FUNCTION dante.guard_generated_activity_creation() OWNER TO dante_owner"
    )
    db.exec_driver_sql(
        "REVOKE ALL ON FUNCTION dante.guard_generated_activity_creation() "
        "FROM PUBLIC,dante_runtime,dante_migrator"
    )
    db.exec_driver_sql(
        "CREATE TRIGGER trg_activity_create_generated_occurrence_guard "
        "BEFORE INSERT ON dante.activity_create_operation FOR EACH ROW "
        "EXECUTE FUNCTION dante.guard_generated_activity_creation()"
    )
    db.exec_driver_sql(_BIND.replace("%", "%%"))
    db.exec_driver_sql(
        "ALTER FUNCTION dante.bind_self_routine_occurrence_activity(uuid,uuid,uuid) "
        "OWNER TO dante_owner"
    )
    db.exec_driver_sql(
        "REVOKE ALL ON FUNCTION "
        "dante.bind_self_routine_occurrence_activity(uuid,uuid,uuid) "
        "FROM PUBLIC,dante_runtime,dante_migrator"
    )
    db.exec_driver_sql(
        "GRANT EXECUTE ON FUNCTION "
        "dante.bind_self_routine_occurrence_activity(uuid,uuid,uuid) TO dante_runtime"
    )


def downgrade() -> None:
    raise RuntimeError("Generated Activity admission is forward-only")
