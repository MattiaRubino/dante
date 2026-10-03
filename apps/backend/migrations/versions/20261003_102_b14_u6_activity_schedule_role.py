"""B14-U6: persist the Activity envelope versus planned Schedule role."""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20261003_102"
down_revision: str | None = "20261002_101"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "activity_schedule_role",
        sa.Column("schedule_ref", sa.Uuid(), nullable=False),
        sa.Column("activity_ref", sa.Uuid(), nullable=False),
        sa.Column("role_code", sa.Text(), nullable=False),
        sa.Column("presentation_order", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("schedule_ref", name="pk_activity_schedule_role"),
        sa.UniqueConstraint(
            "activity_ref", "role_code", "presentation_order",
            name="uq_activity_schedule_role_owner_role_order",
        ),
        sa.CheckConstraint(
            "role_code IN ('envelope','planned')", name="role",
        ),
        sa.CheckConstraint(
            "(role_code='envelope' AND presentation_order=0) OR "
            "(role_code='planned' AND presentation_order BETWEEN 1 AND 100)",
            name="order",
        ),
        sa.ForeignKeyConstraint(
            ["schedule_ref"], ["dante.schedule.schedule_ref"],
            name="fk_activity_schedule_role_schedule",
        ),
        sa.ForeignKeyConstraint(
            ["activity_ref"], ["dante.activity_intention.activity_ref"],
            name="fk_activity_schedule_role_activity",
        ),
        schema="dante",
    )
    bind = op.get_bind()
    bind.exec_driver_sql("""
CREATE FUNCTION dante.set_self_activity_schedule_role(
    requested_self_person_ref uuid, requested_activity_ref uuid,
    requested_schedule_ref uuid, requested_role_code text,
    requested_presentation_order integer
) RETURNS TABLE(schedule_ref uuid, role_code text, presentation_order integer, replayed boolean)
LANGUAGE plpgsql SECURITY DEFINER VOLATILE PARALLEL UNSAFE
SET search_path=pg_catalog,dante,pg_temp AS $function$
#variable_conflict error
DECLARE prior record;
BEGIN
    IF requested_role_code IS NULL OR requested_role_code NOT IN ('envelope','planned')
       OR requested_presentation_order IS NULL
       OR NOT ((requested_role_code='envelope' AND requested_presentation_order=0)
          OR (requested_role_code='planned' AND requested_presentation_order BETWEEN 1 AND 100))
    THEN
        RAISE EXCEPTION USING ERRCODE='23514',
          CONSTRAINT='activity_schedule_role_invalid', MESSAGE='Activity Schedule role rejected';
    END IF;
    PERFORM 1 FROM dante.activity_intention AS activity
     JOIN dante.schedule AS planned ON planned.subject_native_ref=activity.activity_ref
     WHERE activity.activity_ref=requested_activity_ref
       AND activity.self_person_ref=requested_self_person_ref
       AND planned.schedule_ref=requested_schedule_ref FOR SHARE OF activity,planned;
    IF NOT FOUND THEN
        RAISE EXCEPTION USING ERRCODE='23503',
          CONSTRAINT='activity_schedule_role_owner_unavailable',
          MESSAGE='Activity Schedule unavailable to this self';
    END IF;
    SELECT * INTO prior FROM dante.activity_schedule_role AS current
     WHERE current.schedule_ref=requested_schedule_ref;
    IF FOUND THEN
        IF prior.activity_ref IS DISTINCT FROM requested_activity_ref
           OR prior.role_code IS DISTINCT FROM requested_role_code
           OR prior.presentation_order IS DISTINCT FROM requested_presentation_order THEN
            RAISE EXCEPTION USING ERRCODE='23505',
              CONSTRAINT='activity_schedule_role_conflict',
              MESSAGE='Schedule role conflicts with accepted intent';
        END IF;
        RETURN QUERY SELECT prior.schedule_ref,prior.role_code,prior.presentation_order,true;
        RETURN;
    END IF;
    INSERT INTO dante.activity_schedule_role(
        schedule_ref,activity_ref,role_code,presentation_order
    ) VALUES(requested_schedule_ref,requested_activity_ref,
             requested_role_code,requested_presentation_order);
    RETURN QUERY SELECT requested_schedule_ref,requested_role_code,
           requested_presentation_order,false;
END;
$function$;
""")
    bind.exec_driver_sql("""
CREATE FUNCTION dante.get_self_activity_schedule_roles(
    requested_self_person_ref uuid, requested_activity_refs uuid[]
) RETURNS TABLE(schedule_ref uuid, role_code text, presentation_order integer)
LANGUAGE sql SECURITY DEFINER STABLE PARALLEL RESTRICTED
SET search_path=pg_catalog,dante,pg_temp AS $function$
    SELECT purpose.schedule_ref,purpose.role_code,purpose.presentation_order
      FROM dante.activity_schedule_role AS purpose
      JOIN dante.activity_intention AS activity
        ON activity.activity_ref=purpose.activity_ref
     WHERE activity.self_person_ref=requested_self_person_ref
       AND purpose.activity_ref=ANY(requested_activity_refs)
$function$;
""")
    for signature in (
        "dante.set_self_activity_schedule_role(uuid,uuid,uuid,text,integer)",
        "dante.get_self_activity_schedule_roles(uuid,uuid[])",
    ):
        bind.exec_driver_sql(f"ALTER FUNCTION {signature} OWNER TO dante_owner")
        bind.exec_driver_sql(
            f"REVOKE ALL ON FUNCTION {signature} FROM PUBLIC,dante_runtime,dante_migrator"
        )
        bind.exec_driver_sql(f"GRANT EXECUTE ON FUNCTION {signature} TO dante_runtime")
    bind.exec_driver_sql(
        "REVOKE ALL ON TABLE dante.activity_schedule_role "
        "FROM PUBLIC,dante_runtime,dante_migrator"
    )


def downgrade() -> None:
    raise RuntimeError("B14-U6 Schedule role requires a reviewed forward migration")
