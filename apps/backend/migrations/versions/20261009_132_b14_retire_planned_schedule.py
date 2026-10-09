"""Retire a planned Activity row while retaining its Schedule history."""

from collections.abc import Sequence

from alembic import op

revision: str = "20261009_132"
down_revision: str | None = "20261009_131"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    bind = op.get_bind()
    bind.exec_driver_sql("ALTER TABLE dante.activity_schedule_role ADD COLUMN retired_at timestamptz")
    bind.exec_driver_sql("ALTER TABLE dante.activity_schedule_role "
                         "DROP CONSTRAINT uq_activity_schedule_role_owner_role_order")
    bind.exec_driver_sql("""
CREATE UNIQUE INDEX uq_activity_schedule_role_owner_role_order
    ON dante.activity_schedule_role(activity_ref,role_code,presentation_order)
    WHERE retired_at IS NULL
""")
    bind.exec_driver_sql("""
CREATE OR REPLACE FUNCTION dante.get_self_activity_schedule_roles(
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
       AND purpose.retired_at IS NULL
$function$;
""")
    bind.exec_driver_sql("""
CREATE FUNCTION dante.retire_self_planned_schedule(
    requested_actor uuid, requested_activity uuid, requested_schedule uuid
) RETURNS uuid
LANGUAGE plpgsql SECURITY DEFINER VOLATILE PARALLEL UNSAFE
SET search_path=pg_catalog,dante,pg_temp AS $function$
BEGIN
    PERFORM 1 FROM dante.activity_intention AS activity
      JOIN dante.activity_schedule_role AS purpose
        ON purpose.activity_ref=activity.activity_ref
     WHERE activity.activity_ref=requested_activity
       AND activity.self_person_ref=requested_actor AND activity.retired_at IS NULL
       AND purpose.schedule_ref=requested_schedule AND purpose.role_code='planned'
       AND purpose.retired_at IS NULL
     FOR UPDATE OF activity,purpose;
    IF NOT FOUND THEN
        RAISE EXCEPTION USING ERRCODE='23505',
            CONSTRAINT='planned_schedule_retirement_conflict', MESSAGE='Planned row changed';
    END IF;
    IF EXISTS (SELECT 1 FROM dante.schedule_current_placement AS placement
                WHERE placement.scoped_owner_ref=requested_schedule)
       OR EXISTS (
           SELECT 1 FROM dante.list_self_subject_sessions(requested_actor,requested_activity)
                      AS execution
            WHERE dante.get_self_session_planned_schedule(
                requested_actor,execution.session_ref)=requested_schedule
       ) THEN
        RAISE EXCEPTION USING ERRCODE='23505',
            CONSTRAINT='planned_schedule_retirement_conflict',
            MESSAGE='Planned row has current placement or recorded execution';
    END IF;
    UPDATE dante.activity_schedule_role
       SET retired_at=clock_timestamp()
     WHERE schedule_ref=requested_schedule;
    RETURN requested_schedule;
END;
$function$;
""")
    bind.exec_driver_sql("""
CREATE OR REPLACE FUNCTION dante.establish_self_unplaced_planned_schedule(
    requested_actor uuid, requested_activity uuid, requested_schedule uuid,
    requested_position integer, requested_display_name text
) RETURNS TABLE(schedule_ref uuid, replayed boolean)
LANGUAGE plpgsql SECURITY DEFINER VOLATILE PARALLEL UNSAFE
SET search_path=pg_catalog,dante,pg_temp AS $function$
#variable_conflict error
DECLARE prior record;
BEGIN
    IF requested_position IS NULL OR requested_position < 1 OR
       requested_schedule IS NULL OR uuid_extract_version(requested_schedule) IS DISTINCT FROM 7 OR
       (requested_display_name IS NOT NULL AND
        (requested_display_name = '' OR requested_display_name <> btrim(requested_display_name)
         OR char_length(requested_display_name) > 300)) THEN
        RAISE EXCEPTION USING ERRCODE='23514',
          CONSTRAINT='unplaced_planned_schedule_invalid', MESSAGE='Invalid planned row';
    END IF;
    PERFORM 1 FROM dante.activity_intention AS a
      WHERE a.activity_ref=requested_activity AND a.self_person_ref=requested_actor
      FOR UPDATE;
    IF NOT FOUND THEN
        RAISE EXCEPTION USING ERRCODE='23503',
          CONSTRAINT='unplaced_planned_schedule_unavailable', MESSAGE='Activity unavailable';
    END IF;
    SELECT role.schedule_ref, role.display_name INTO prior
      FROM dante.activity_schedule_role AS role
     WHERE role.activity_ref=requested_activity AND role.role_code='planned'
       AND role.retired_at IS NULL AND role.presentation_order=requested_position;
    IF FOUND THEN
        IF prior.display_name IS DISTINCT FROM requested_display_name OR EXISTS (
            SELECT 1 FROM dante.schedule_current_placement AS placement
             WHERE placement.scoped_owner_ref=prior.schedule_ref
        ) THEN
            RAISE EXCEPTION USING ERRCODE='23505',
              CONSTRAINT='unplaced_planned_schedule_conflict', MESSAGE='Planned row changed';
        END IF;
        RETURN QUERY SELECT prior.schedule_ref, true;
        RETURN;
    END IF;
    INSERT INTO dante.schedule(schedule_ref,subject_native_ref)
        VALUES(requested_schedule,requested_activity);
    INSERT INTO dante.scoped_address(scoped_ref,scoped_family)
        VALUES(requested_schedule,'schedule');
    PERFORM 1 FROM dante.set_self_activity_schedule_role(
        requested_actor,requested_activity,requested_schedule,
        'planned',requested_position,requested_display_name);
    RETURN QUERY SELECT requested_schedule, false;
END;
$function$;
""")
    bind.exec_driver_sql("""
CREATE FUNCTION dante.list_self_retired_planned_schedules(
    requested_actor uuid, requested_activity uuid
) RETURNS TABLE(schedule_ref uuid)
LANGUAGE sql SECURITY DEFINER STABLE PARALLEL RESTRICTED
SET search_path=pg_catalog,dante,pg_temp AS $function$
    SELECT purpose.schedule_ref
      FROM dante.activity_schedule_role AS purpose
      JOIN dante.activity_intention AS activity
        ON activity.activity_ref=purpose.activity_ref
     WHERE activity.self_person_ref=requested_actor
       AND activity.activity_ref=requested_activity
       AND purpose.role_code='planned' AND purpose.retired_at IS NOT NULL
$function$;
""")
    # The preceding placement capability must reject rows after retirement.
    # Replace its exact owned-role predicate without editing the applied _131 revision.
    prior_placement = bind.exec_driver_sql("""
        SELECT pg_get_functiondef(
            'dante.place_self_unplaced_planned_schedule(uuid,text,text,uuid,uuid,uuid,jsonb)'
            ::regprocedure)
    """).scalar_one()
    current_guard = "AND role.role_code='planned' FOR UPDATE OF a;"
    if prior_placement.count(current_guard) != 1:
        raise RuntimeError("Unexpected planned placement contract at _132 migration")
    bind.exec_driver_sql(prior_placement.replace(
        current_guard,
        "AND role.role_code='planned' AND role.retired_at IS NULL FOR UPDATE OF a;",
    ))
    for signature in (
        "dante.get_self_activity_schedule_roles(uuid,uuid[])",
        "dante.retire_self_planned_schedule(uuid,uuid,uuid)",
        "dante.establish_self_unplaced_planned_schedule(uuid,uuid,uuid,integer,text)",
        "dante.list_self_retired_planned_schedules(uuid,uuid)",
    ):
        bind.exec_driver_sql(f"ALTER FUNCTION {signature} OWNER TO dante_owner")
        bind.exec_driver_sql(
            f"REVOKE ALL ON FUNCTION {signature} FROM PUBLIC,dante_runtime,dante_migrator"
        )
        bind.exec_driver_sql(f"GRANT EXECUTE ON FUNCTION {signature} TO dante_runtime")


def downgrade() -> None:
    raise RuntimeError("Planned Schedule retirement requires a reviewed forward migration")
