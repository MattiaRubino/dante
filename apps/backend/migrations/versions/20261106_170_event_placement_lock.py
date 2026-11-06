"""Allow owner-scoped placement locks for Event and recurring Event Schedules.

Revision ID: 20261106_170
Revises: 20261105_169
"""

from collections.abc import Sequence

from alembic import op

revision: str = "20261106_170"
down_revision: str | None = "20261105_169"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    db = op.get_bind()
    db.exec_driver_sql(_SET)
    db.exec_driver_sql(_GET)
    for signature in (
        "set_self_schedule_placement_lock(uuid,uuid,boolean,bigint)",
        "get_self_schedule_placement_lock(uuid,uuid)",
    ):
        db.exec_driver_sql(f"ALTER FUNCTION dante.{signature} OWNER TO dante_owner")
        db.exec_driver_sql(
            f"REVOKE ALL ON FUNCTION dante.{signature} FROM PUBLIC,dante_runtime,dante_migrator"
        )
        db.exec_driver_sql(f"GRANT EXECUTE ON FUNCTION dante.{signature} TO dante_runtime")


def downgrade() -> None:
    raise RuntimeError("20261106_170 is forward-only")


_SET = r"""
CREATE OR REPLACE FUNCTION dante.set_self_schedule_placement_lock(
    requested_self_person_ref uuid,
    requested_schedule_ref uuid,
    requested_locked boolean,
    requested_expected_revision bigint
) RETURNS TABLE(schedule_ref uuid, locked boolean, revision bigint, updated_at timestamptz, replayed boolean)
LANGUAGE plpgsql SECURITY DEFINER VOLATILE PARALLEL UNSAFE
SET search_path=pg_catalog,dante,pg_temp AS $function$
#variable_conflict error
DECLARE
    prior dante.schedule_placement_lock%%ROWTYPE;
    recorded_at timestamptz := statement_timestamp();
BEGIN
    IF requested_locked IS NULL THEN
        RAISE EXCEPTION USING ERRCODE='23514',
            CONSTRAINT='schedule_placement_lock_invalid',
            MESSAGE='A placement lock must specify its target state';
    END IF;
    IF NOT EXISTS (
        SELECT 1 FROM dante.schedule AS schedule_row
        WHERE schedule_row.schedule_ref=requested_schedule_ref
          AND (
            EXISTS (
                SELECT 1 FROM dante.activity_intention AS activity
                 WHERE activity.activity_ref=schedule_row.subject_native_ref
                   AND activity.self_person_ref=requested_self_person_ref
            ) OR EXISTS (
                SELECT 1 FROM dante.event_expectation AS expectation
                 WHERE expectation.event_ref=schedule_row.subject_native_ref
                   AND expectation.self_person_ref=requested_self_person_ref
            ) OR EXISTS (
                SELECT 1 FROM dante.occurrence_generation AS generation
                JOIN dante.event_expectation AS expectation
                  ON expectation.event_ref=generation.source_native_ref
                 WHERE generation.occurrence_ref=schedule_row.subject_native_ref
                   AND expectation.self_person_ref=requested_self_person_ref
            )
        )
    ) THEN
        RAISE EXCEPTION USING ERRCODE='23503',
            CONSTRAINT='schedule_placement_lock_schedule_unavailable',
            MESSAGE='Schedule unavailable in self scope';
    END IF;
    -- Serialize both setters and Schedule revisions on the same Schedule owner.
    PERFORM 1 FROM dante.schedule AS schedule_row
     WHERE schedule_row.schedule_ref=requested_schedule_ref FOR UPDATE;
    SELECT * INTO prior FROM dante.schedule_placement_lock AS current_lock
     WHERE current_lock.schedule_ref=requested_schedule_ref FOR UPDATE;
    IF NOT FOUND THEN
        IF requested_expected_revision IS NOT NULL THEN
            RAISE EXCEPTION USING ERRCODE='23505',
                CONSTRAINT='schedule_placement_lock_stale',
                MESSAGE='Placement lock basis is stale';
        END IF;
        INSERT INTO dante.schedule_placement_lock(
            schedule_ref,self_person_ref,locked,revision,updated_at
        ) VALUES(requested_schedule_ref,requested_self_person_ref,requested_locked,1,recorded_at);
        RETURN QUERY SELECT requested_schedule_ref,requested_locked,1::bigint,recorded_at,false;
        RETURN;
    END IF;
    IF prior.self_person_ref<>requested_self_person_ref THEN
        RAISE EXCEPTION USING ERRCODE='23503',
            CONSTRAINT='schedule_placement_lock_schedule_unavailable',
            MESSAGE='Schedule unavailable in self scope';
    END IF;
    IF prior.locked=requested_locked AND
       (requested_expected_revision IS NULL OR requested_expected_revision=prior.revision) THEN
        RETURN QUERY SELECT prior.schedule_ref,prior.locked,prior.revision,prior.updated_at,true;
        RETURN;
    END IF;
    IF requested_expected_revision IS DISTINCT FROM prior.revision THEN
        RAISE EXCEPTION USING ERRCODE='23505',
            CONSTRAINT='schedule_placement_lock_stale',
            MESSAGE='Placement lock basis is stale';
    END IF;
    UPDATE dante.schedule_placement_lock AS current_lock
       SET locked=requested_locked,revision=prior.revision+1,updated_at=recorded_at
     WHERE current_lock.schedule_ref=requested_schedule_ref;
    RETURN QUERY SELECT requested_schedule_ref,requested_locked,prior.revision+1,recorded_at,false;
END;
$function$;
"""

_GET = r"""
CREATE OR REPLACE FUNCTION dante.get_self_schedule_placement_lock(
    requested_self_person_ref uuid, requested_schedule_ref uuid
) RETURNS TABLE(schedule_ref uuid, locked boolean, revision bigint, updated_at timestamptz)
LANGUAGE sql SECURITY DEFINER STABLE PARALLEL SAFE
SET search_path=pg_catalog,dante,pg_temp AS $function$
SELECT schedule_row.schedule_ref,COALESCE(current_lock.locked,false),
       COALESCE(current_lock.revision,0),current_lock.updated_at
  FROM dante.schedule AS schedule_row

  LEFT JOIN dante.schedule_placement_lock AS current_lock
    ON current_lock.schedule_ref=schedule_row.schedule_ref
   AND current_lock.self_person_ref=requested_self_person_ref
 WHERE schedule_row.schedule_ref=requested_schedule_ref
   AND (
            EXISTS (
                SELECT 1 FROM dante.activity_intention AS activity
                 WHERE activity.activity_ref=schedule_row.subject_native_ref
                   AND activity.self_person_ref=requested_self_person_ref
            ) OR EXISTS (
                SELECT 1 FROM dante.event_expectation AS expectation
                 WHERE expectation.event_ref=schedule_row.subject_native_ref
                   AND expectation.self_person_ref=requested_self_person_ref
            ) OR EXISTS (
                SELECT 1 FROM dante.occurrence_generation AS generation
                JOIN dante.event_expectation AS expectation
                  ON expectation.event_ref=generation.source_native_ref
                 WHERE generation.occurrence_ref=schedule_row.subject_native_ref
                   AND expectation.self_person_ref=requested_self_person_ref
            )
        )
$function$;
"""
