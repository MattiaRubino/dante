"""Allow a named future planned Activity row without inventing a placement."""

from collections.abc import Sequence

from alembic import op

revision: str = "20261009_129"
down_revision: str | None = "20261008_128"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    bind = op.get_bind()
    bind.exec_driver_sql("""
CREATE FUNCTION dante.establish_self_unplaced_planned_schedule(
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
       AND role.presentation_order=requested_position;
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
ALTER FUNCTION dante.establish_self_unplaced_planned_schedule(uuid,uuid,uuid,integer,text)
    OWNER TO dante_owner;
REVOKE ALL ON FUNCTION dante.establish_self_unplaced_planned_schedule(uuid,uuid,uuid,integer,text)
    FROM PUBLIC,dante_runtime,dante_migrator;
GRANT EXECUTE ON FUNCTION dante.establish_self_unplaced_planned_schedule(uuid,uuid,uuid,integer,text)
    TO dante_runtime;
""")


def downgrade() -> None:
    raise RuntimeError("Unplaced planned rows require a reviewed forward migration")
