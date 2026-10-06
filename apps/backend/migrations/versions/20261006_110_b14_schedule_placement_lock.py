"""Persist an explicit user placement lock, separate from B04 automation policy.

Revision ID: 20261006_110
Revises: 20261006_109
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20261006_110"
down_revision: str | None = "20261006_109"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "schedule_placement_lock",
        sa.Column("schedule_ref", sa.Uuid(), nullable=False),
        sa.Column("self_person_ref", sa.Uuid(), nullable=False),
        sa.Column("locked", sa.Boolean(), nullable=False),
        sa.Column("revision", sa.BigInteger(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("schedule_ref", name="pk_schedule_placement_lock"),
        sa.ForeignKeyConstraint(
            ["schedule_ref"], ["dante.schedule.schedule_ref"],
            name="fk_schedule_placement_lock_schedule",
            ondelete="NO ACTION", onupdate="NO ACTION",
        ),
        sa.ForeignKeyConstraint(
            ["self_person_ref"], ["dante.person.person_ref"],
            name="fk_schedule_placement_lock_person",
            ondelete="NO ACTION", onupdate="NO ACTION",
        ),
        sa.CheckConstraint("revision >= 1", name="ck_schedule_placement_lock_revision"),
        schema="dante",
    )
    bind = op.get_bind()
    bind.exec_driver_sql(_SET)
    bind.exec_driver_sql(_GET)
    bind.exec_driver_sql(_GUARD)
    bind.exec_driver_sql(
        "CREATE TRIGGER trg_schedule_placement_manual_lock "
        "BEFORE UPDATE OF current_until_at ON dante.schedule_placement_current_history "
        "FOR EACH ROW EXECUTE FUNCTION dante.enforce_schedule_placement_manual_lock()"
    )
    bind.exec_driver_sql(
        "REVOKE ALL ON dante.schedule_placement_lock FROM PUBLIC,dante_runtime,dante_migrator"
    )
    for signature in ("set_self_schedule_placement_lock(uuid,uuid,boolean,bigint)",
                      "get_self_schedule_placement_lock(uuid,uuid)"):
        bind.exec_driver_sql(f"REVOKE ALL ON FUNCTION dante.{signature} FROM PUBLIC,dante_runtime,dante_migrator")
        bind.exec_driver_sql(f"GRANT EXECUTE ON FUNCTION dante.{signature} TO dante_runtime")


def downgrade() -> None:
    raise RuntimeError("20261006_110 is forward-only after placement locks become canonical truth")


_SET = r"""
CREATE FUNCTION dante.set_self_schedule_placement_lock(
    requested_self_person_ref uuid,
    requested_schedule_ref uuid,
    requested_locked boolean,
    requested_expected_revision bigint
) RETURNS TABLE(schedule_ref uuid, locked boolean, revision bigint, updated_at timestamptz, replayed boolean)
LANGUAGE plpgsql SECURITY DEFINER VOLATILE PARALLEL UNSAFE
SET search_path=pg_catalog,dante,pg_temp AS $function$
#variable_conflict error
DECLARE
    prior dante.schedule_placement_lock%ROWTYPE;
    recorded_at timestamptz := statement_timestamp();
BEGIN
    IF requested_locked IS NULL THEN
        RAISE EXCEPTION USING ERRCODE='23514',
            CONSTRAINT='schedule_placement_lock_invalid',
            MESSAGE='A placement lock must specify its target state';
    END IF;
    IF NOT EXISTS (
        SELECT 1 FROM dante.schedule AS schedule_row
        JOIN dante.activity_intention AS activity
          ON activity.activity_ref=schedule_row.subject_native_ref
        WHERE schedule_row.schedule_ref=requested_schedule_ref
          AND activity.self_person_ref=requested_self_person_ref
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
CREATE FUNCTION dante.get_self_schedule_placement_lock(
    requested_self_person_ref uuid, requested_schedule_ref uuid
) RETURNS TABLE(schedule_ref uuid, locked boolean, revision bigint, updated_at timestamptz)
LANGUAGE sql SECURITY DEFINER STABLE PARALLEL SAFE
SET search_path=pg_catalog,dante,pg_temp AS $function$
SELECT schedule_row.schedule_ref,COALESCE(current_lock.locked,false),
       COALESCE(current_lock.revision,0),current_lock.updated_at
  FROM dante.schedule AS schedule_row
  JOIN dante.activity_intention AS activity ON activity.activity_ref=schedule_row.subject_native_ref
  LEFT JOIN dante.schedule_placement_lock AS current_lock
    ON current_lock.schedule_ref=schedule_row.schedule_ref
   AND current_lock.self_person_ref=requested_self_person_ref
 WHERE schedule_row.schedule_ref=requested_schedule_ref
   AND activity.self_person_ref=requested_self_person_ref
$function$;
"""

_GUARD = r"""
CREATE FUNCTION dante.enforce_schedule_placement_manual_lock()
RETURNS trigger LANGUAGE plpgsql SECURITY DEFINER VOLATILE PARALLEL UNSAFE
SET search_path=pg_catalog,dante,pg_temp AS $function$
BEGIN
    -- Serialize against a concurrent lock/unlock even when no lock row exists yet.
    PERFORM 1 FROM dante.schedule AS schedule_row
     WHERE schedule_row.schedule_ref=OLD.schedule_ref FOR UPDATE;
    IF OLD.current_until_at IS NULL AND NEW.current_until_at IS NOT NULL
       AND EXISTS (
           SELECT 1 FROM dante.schedule_placement_lock AS current_lock
            WHERE current_lock.schedule_ref=OLD.schedule_ref AND current_lock.locked
       ) THEN
        RAISE EXCEPTION USING ERRCODE='23514',
            CONSTRAINT='schedule_placement_manually_locked',
            MESSAGE='Unlock this Schedule before changing its placement';
    END IF;
    RETURN NEW;
END;
$function$;
"""
