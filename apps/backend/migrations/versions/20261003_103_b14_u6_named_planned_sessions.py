"""B14-U6: name future Activity execution rows without creating Sessions."""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20261003_103"
down_revision: str | None = "20261003_102"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "activity_schedule_role",
        sa.Column("display_name", sa.Text(), nullable=True),
        schema="dante",
    )
    op.create_check_constraint(
        op.f("ck_activity_schedule_role_name"),
        "activity_schedule_role",
        "display_name IS NULL OR (role_code='planned' AND display_name=btrim(display_name) "
        "AND display_name<>'' AND char_length(display_name)<=300)",
        schema="dante",
    )
    bind = op.get_bind()
    bind.exec_driver_sql(
        "DROP FUNCTION dante.set_self_activity_schedule_role(uuid,uuid,uuid,text,integer)"
    )
    bind.exec_driver_sql("DROP FUNCTION dante.get_self_activity_schedule_roles(uuid,uuid[])")
    bind.exec_driver_sql("""
CREATE FUNCTION dante.set_self_activity_schedule_role(
    requested_self_person_ref uuid, requested_activity_ref uuid,
    requested_schedule_ref uuid, requested_role_code text,
    requested_presentation_order integer, requested_display_name text
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
       OR (requested_display_name IS NOT NULL AND
          (requested_role_code<>'planned' OR requested_display_name<>btrim(requested_display_name)
           OR requested_display_name='' OR char_length(requested_display_name)>300))
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
           OR prior.presentation_order IS DISTINCT FROM requested_presentation_order
           OR prior.display_name IS DISTINCT FROM requested_display_name THEN
            RAISE EXCEPTION USING ERRCODE='23505',
              CONSTRAINT='activity_schedule_role_conflict',
              MESSAGE='Schedule role conflicts with accepted intent';
        END IF;
        RETURN QUERY SELECT prior.schedule_ref,prior.role_code,prior.presentation_order,true;
        RETURN;
    END IF;
    INSERT INTO dante.activity_schedule_role(
        schedule_ref,activity_ref,role_code,presentation_order,display_name
    ) VALUES(requested_schedule_ref,requested_activity_ref,
             requested_role_code,requested_presentation_order,requested_display_name);
    RETURN QUERY SELECT requested_schedule_ref,requested_role_code,
           requested_presentation_order,false;
END;
$function$;
""")
    bind.exec_driver_sql("""
CREATE FUNCTION dante.get_self_activity_schedule_roles(
    requested_self_person_ref uuid, requested_activity_refs uuid[]
) RETURNS TABLE(schedule_ref uuid, role_code text, presentation_order integer, display_name text)
LANGUAGE sql SECURITY DEFINER STABLE PARALLEL RESTRICTED
SET search_path=pg_catalog,dante,pg_temp AS $function$
    SELECT purpose.schedule_ref,purpose.role_code,purpose.presentation_order,purpose.display_name
      FROM dante.activity_schedule_role AS purpose
      JOIN dante.activity_intention AS activity
        ON activity.activity_ref=purpose.activity_ref
     WHERE activity.self_person_ref=requested_self_person_ref
       AND purpose.activity_ref=ANY(requested_activity_refs)
$function$;
""")
    for signature in (
        "dante.set_self_activity_schedule_role(uuid,uuid,uuid,text,integer,text)",
        "dante.get_self_activity_schedule_roles(uuid,uuid[])",
    ):
        bind.exec_driver_sql(f"ALTER FUNCTION {signature} OWNER TO dante_owner")
        bind.exec_driver_sql(
            f"REVOKE ALL ON FUNCTION {signature} FROM PUBLIC,dante_runtime,dante_migrator"
        )
        bind.exec_driver_sql(f"GRANT EXECUTE ON FUNCTION {signature} TO dante_runtime")


def downgrade() -> None:
    raise NotImplementedError("Canonical Activity Schedule names are forward-only")
