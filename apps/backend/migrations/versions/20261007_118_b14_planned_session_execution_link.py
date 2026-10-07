"""Bind an explicitly started real Session to one planned Activity Schedule.

Revision ID: 20261007_118
Revises: 20261006_117

The optional link is evidence of which plan the user started from. It never
turns a planned Schedule into a Session or asserts Actual realization.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20261007_118"
down_revision: str | None = "20261006_117"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "session_planned_schedule_link",
        sa.Column("session_ref", sa.Uuid(), nullable=False),
        sa.Column("schedule_ref", sa.Uuid(), nullable=False),
        sa.Column("linked_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("session_ref", name="pk_session_planned_schedule_link"),
        sa.ForeignKeyConstraint(
            ["session_ref"], ["dante.session_execution_subject.session_ref"],
            name="fk_session_planned_schedule_link_session", ondelete="NO ACTION", onupdate="NO ACTION",
        ),
        sa.ForeignKeyConstraint(
            ["schedule_ref"], ["dante.activity_schedule_role.schedule_ref"],
            name="fk_session_planned_schedule_link_role", ondelete="NO ACTION", onupdate="NO ACTION",
        ),
        schema="dante",
    )
    op.create_index(
        "ix_session_planned_schedule_link_schedule_ref",
        "session_planned_schedule_link", ["schedule_ref"], schema="dante",
    )
    bind = op.get_bind()
    bind.exec_driver_sql(_START)
    bind.exec_driver_sql(_READ)
    bind.exec_driver_sql(
        "ALTER TABLE dante.session_planned_schedule_link OWNER TO dante_owner"
    )
    bind.exec_driver_sql(
        "REVOKE ALL ON dante.session_planned_schedule_link FROM PUBLIC,dante_runtime,dante_migrator"
    )
    for signature in (
        "start_self_planned_activity_session(uuid,text,text,uuid,uuid,uuid,uuid)",
        "get_self_session_planned_schedule(uuid,uuid)",
    ):
        bind.exec_driver_sql(f"ALTER FUNCTION dante.{signature} OWNER TO dante_owner")
        bind.exec_driver_sql(
            f"REVOKE ALL ON FUNCTION dante.{signature} FROM PUBLIC,dante_runtime,dante_migrator"
        )
        bind.exec_driver_sql(f"GRANT EXECUTE ON FUNCTION dante.{signature} TO dante_runtime")


def downgrade() -> None:
    raise RuntimeError("20261007_118 is forward-only: real Session provenance must not be lost")


_START = r"""
CREATE FUNCTION dante.start_self_planned_activity_session(
    requested_self_person_ref uuid,
    requested_operation_id text,
    requested_intent_fingerprint text,
    requested_session_ref uuid,
    requested_material_state_ref uuid,
    requested_activity_ref uuid,
    requested_schedule_ref uuid
) RETURNS TABLE(
    session_ref uuid, subject_native_ref uuid, timing_material_state_ref uuid,
    started_at timestamptz, ended_at timestamptz, replayed boolean
)
LANGUAGE plpgsql SECURITY DEFINER VOLATILE PARALLEL UNSAFE
SET search_path=pg_catalog,dante,pg_temp AS $function$
#variable_conflict error
DECLARE
    result record;
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM dante.activity_schedule_role AS role
        JOIN dante.activity_intention AS activity
          ON activity.activity_ref=role.activity_ref
        JOIN dante.schedule AS schedule_row
          ON schedule_row.schedule_ref=role.schedule_ref
         AND schedule_row.subject_native_ref=activity.activity_ref
        JOIN dante.schedule_current_placement AS placement
          ON placement.scoped_owner_ref=schedule_row.schedule_ref
        WHERE role.schedule_ref=requested_schedule_ref
          AND role.activity_ref=requested_activity_ref
          AND role.role_code='planned'
          AND activity.self_person_ref=requested_self_person_ref
    ) THEN
        RAISE EXCEPTION USING ERRCODE='23503',
          CONSTRAINT='session_planned_schedule_unavailable',
          MESSAGE='Planned Session unavailable in self scope';
    END IF;

    SELECT * INTO STRICT result FROM dante.start_self_session(
        requested_self_person_ref, requested_operation_id,
        requested_intent_fingerprint, requested_session_ref,
        requested_material_state_ref, 'activity', requested_activity_ref
    );
    IF result.replayed THEN
        IF NOT EXISTS (
            SELECT 1 FROM dante.session_planned_schedule_link AS link
             WHERE link.session_ref=result.session_ref
               AND link.schedule_ref=requested_schedule_ref
        ) THEN
            RAISE EXCEPTION USING ERRCODE='23505',
              CONSTRAINT='session_planned_schedule_operation_conflict',
              MESSAGE='Planned Session start replay conflicts with its planning link';
        END IF;
    ELSE
        INSERT INTO dante.session_planned_schedule_link(session_ref,schedule_ref,linked_at)
        VALUES(result.session_ref,requested_schedule_ref,statement_timestamp());
    END IF;
    RETURN QUERY SELECT result.session_ref, result.subject_native_ref,
        result.timing_material_state_ref, result.started_at, result.ended_at,
        result.replayed;
END;
$function$;
"""


_READ = r"""
CREATE FUNCTION dante.get_self_session_planned_schedule(
    requested_self_person_ref uuid, requested_session_ref uuid
) RETURNS uuid
LANGUAGE sql SECURITY DEFINER STABLE PARALLEL SAFE
SET search_path=pg_catalog,dante,pg_temp AS $function$
SELECT link.schedule_ref
  FROM dante.session_execution_subject AS subject
  JOIN dante.activity_intention AS activity
    ON activity.activity_ref=subject.subject_native_ref
   AND activity.self_person_ref=requested_self_person_ref
  JOIN dante.session_planned_schedule_link AS link
    ON link.session_ref=subject.session_ref
 WHERE subject.session_ref=requested_session_ref
$function$;
"""
