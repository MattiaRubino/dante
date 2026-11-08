"""Accept zero-revision CAS for a previously unprotected Schedule.

A missing placement_lock row is read as revision 0, so the owner-scoped
setter must accept expected_revision=0 on its first write. It must reject
revision=0 when a row already exists. No historical lock rows are rewritten.

Revision ID: 20261108_179
Revises: 20261107_178
"""

from collections.abc import Sequence

from alembic import op

revision: str = "20261108_179"
down_revision: str | None = "20261107_178"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    bind = op.get_bind()
    bind.exec_driver_sql(_SET)
    signature = "set_self_schedule_placement_lock(uuid,uuid,boolean,bigint)"
    bind.exec_driver_sql(f"ALTER FUNCTION dante.{signature} OWNER TO dante_owner")
    bind.exec_driver_sql(
        f"REVOKE ALL ON FUNCTION dante.{signature} FROM PUBLIC,dante_runtime,dante_migrator"
    )
    bind.exec_driver_sql(f"GRANT EXECUTE ON FUNCTION dante.{signature} TO dante_runtime")


def downgrade() -> None:
    raise RuntimeError("20261108_179 is forward-only")


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
        -- A fresh Schedule reports revision 0 via get_self_schedule_placement_lock.
        -- Accept that exact empty basis, but keep every established revision CAS-guarded.
        IF requested_expected_revision IS NOT NULL
           AND requested_expected_revision <> 0 THEN
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
