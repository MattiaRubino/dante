# ruff: noqa: S608
"""B06-A correction: create the mandatory CP6 Routine recurrence companion.

CP6 deliberately rejects a bare ``routine`` owner.  A Routine source and its
initial Recurrence remain distinct things, but creation must establish both in
one transaction so the source never exists in an invalid intermediate state.

Revision ID: 20260921_50
Revises: 20260921_49
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260921_50"
down_revision: str | None = "20260921_49"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def _sql(value: str) -> None:
    op.execute(sa.text(value))


def upgrade() -> None:
    _sql("DROP FUNCTION dante.create_self_routine(uuid,text,text,uuid,text,uuid,uuid[])")
    _sql(_CREATE)
    _sql(
        "ALTER FUNCTION dante.create_self_routine(uuid,text,text,uuid,text,uuid,uuid[],date,time) "
        "OWNER TO dante_owner"
    )
    _sql(
        "REVOKE ALL PRIVILEGES ON FUNCTION "
        "dante.create_self_routine(uuid,text,text,uuid,text,uuid,uuid[],date,time) "
        "FROM PUBLIC,dante_runtime,dante_migrator"
    )
    _sql(
        "GRANT EXECUTE ON FUNCTION "
        "dante.create_self_routine(uuid,text,text,uuid,text,uuid,uuid[],date,time) "
        "TO dante_runtime"
    )


def downgrade() -> None:
    raise RuntimeError("B06-A Routine companion correction requires a reviewed forward migration")


_CREATE = r'''
CREATE FUNCTION dante.create_self_routine(
    requested_self_person_ref uuid, requested_operation_id text,
    requested_intent_fingerprint text, requested_routine_ref uuid,
    requested_title text, requested_life_area_ref uuid, requested_tag_refs uuid[],
    requested_starts_on date, requested_wall_time time
) RETURNS TABLE(routine_ref uuid, source_revision bigint, life_area_assignment_revision bigint,
                accepted_at timestamptz, replayed boolean)
LANGUAGE plpgsql SECURITY DEFINER VOLATILE PARALLEL UNSAFE
SET search_path = pg_catalog, dante, pg_temp AS $function$
#variable_conflict error
DECLARE
    key text := btrim(requested_operation_id); label text := btrim(requested_title);
    previous record; recorded_at timestamptz := statement_timestamp(); recurrence_state_ref uuid;
BEGIN
    IF key IS NULL OR key='' OR char_length(key)>200 OR label IS NULL OR label='' OR char_length(label)>300
       OR requested_intent_fingerprint IS NULL OR requested_intent_fingerprint !~ '^[0-9a-f]{64}$'
       OR uuid_extract_version(requested_routine_ref) IS DISTINCT FROM 7
       OR requested_starts_on IS NULL OR NOT isfinite(requested_starts_on) THEN
        RAISE EXCEPTION USING ERRCODE='23514', MESSAGE='Routine create command rejected';
    END IF;
    IF requested_tag_refs IS NOT NULL AND cardinality(requested_tag_refs)<>cardinality(ARRAY(SELECT DISTINCT value FROM unnest(requested_tag_refs) AS value)) THEN
        RAISE EXCEPTION USING ERRCODE='23514', MESSAGE='Routine create tags must be unique';
    END IF;
    PERFORM 1 FROM dante.person WHERE person_ref=requested_self_person_ref FOR UPDATE;
    IF NOT FOUND OR NOT EXISTS (SELECT 1 FROM dante.account_application_context WHERE self_person_ref=requested_self_person_ref) THEN
        RAISE EXCEPTION USING ERRCODE='23503', MESSAGE='Routine self context unavailable';
    END IF;
    SELECT * INTO previous FROM dante.routine_operation WHERE self_person_ref=requested_self_person_ref AND operation_id=key;
    IF FOUND THEN
        IF previous.intent_fingerprint<>requested_intent_fingerprint OR previous.kind<>'create' THEN
            RAISE EXCEPTION USING ERRCODE='23505', CONSTRAINT='pk_routine_operation', MESSAGE='Routine operation id reused';
        END IF;
        RETURN QUERY SELECT previous.routine_ref,previous.accepted_source_revision,1::bigint,previous.accepted_at,true; RETURN;
    END IF;
    IF NOT EXISTS (SELECT 1 FROM dante.life_area WHERE life_area_ref=requested_life_area_ref AND self_person_ref=requested_self_person_ref AND archived=false) THEN
        RAISE EXCEPTION USING ERRCODE='23503', CONSTRAINT='routine_life_area_unavailable', MESSAGE='Routine Life Area unavailable';
    END IF;
    IF requested_tag_refs IS NOT NULL AND EXISTS (
        SELECT 1 FROM unnest(requested_tag_refs) AS wanted(tag_ref) LEFT JOIN dante.product_tag AS tag
          ON tag.tag_ref=wanted.tag_ref AND tag.self_person_ref=requested_self_person_ref AND tag.archived=false
         WHERE tag.tag_ref IS NULL
    ) THEN
        RAISE EXCEPTION USING ERRCODE='23503', CONSTRAINT='routine_tag_unavailable', MESSAGE='Routine Tag unavailable';
    END IF;
    recurrence_state_ref := uuidv7();
    INSERT INTO dante.routine(routine_ref) VALUES(requested_routine_ref);
    INSERT INTO dante.native_address(native_ref,owner_family) VALUES(requested_routine_ref,'routine');
    INSERT INTO dante.material_state_address(material_state_ref,native_owner_ref,scoped_owner_ref,facet_code)
    VALUES(recurrence_state_ref,requested_routine_ref,NULL,'routine.recurrence');
    INSERT INTO dante.routine_recurrence_state(material_state_ref,routine_ref,family_code,range_kind,expected_occurrence_count)
    VALUES(recurrence_state_ref,requested_routine_ref,'calendar_wall_clock','open',NULL);
    INSERT INTO dante.routine_recurrence_calendar_state(material_state_ref,pattern_code,interval_count,clock_basis_code,zone_id,step_unit_code)
    VALUES(recurrence_state_ref,'daily',1,'floating_local',NULL,NULL);
    INSERT INTO dante.routine_recurrence_boundary_state(material_state_ref,boundary_role,boundary_kind,inclusive,date_value,local_value,zone_id,instant_value,resolved_at)
    VALUES(recurrence_state_ref,'effective_from','date',true,requested_starts_on,NULL,NULL,NULL,NULL);
    IF requested_wall_time IS NOT NULL THEN
        INSERT INTO dante.routine_recurrence_calendar_wall_time(material_state_ref,wall_time)
        VALUES(recurrence_state_ref,requested_wall_time);
    END IF;
    INSERT INTO dante.native_current_material_state(native_owner_ref,facet_code,material_state_ref)
    VALUES(requested_routine_ref,'routine.recurrence',recurrence_state_ref);
    INSERT INTO dante.routine_recurrence_current_history(routine_ref,material_state_ref,current_from_at,current_until_at)
    VALUES(requested_routine_ref,recurrence_state_ref,recorded_at,NULL);
    INSERT INTO dante.routine_intention(routine_ref,self_person_ref,title,lifecycle_state,source_revision,created_at,updated_at,lifecycle_changed_at)
    VALUES(requested_routine_ref,requested_self_person_ref,label,'active',1,recorded_at,recorded_at,recorded_at);
    INSERT INTO dante.routine_life_area_assignment(self_person_ref,routine_ref,life_area_ref,revision,assigned_at)
    VALUES(requested_self_person_ref,requested_routine_ref,requested_life_area_ref,1,recorded_at);
    INSERT INTO dante.routine_tag(self_person_ref,routine_ref,tag_ref,attached_at)
    SELECT requested_self_person_ref,requested_routine_ref,tag_ref,recorded_at FROM unnest(COALESCE(requested_tag_refs,ARRAY[]::uuid[])) AS tags(tag_ref);
    INSERT INTO dante.routine_operation(self_person_ref,operation_id,intent_fingerprint,routine_ref,kind,expected_source_revision,accepted_source_revision,accepted_at)
    VALUES(requested_self_person_ref,key,requested_intent_fingerprint,requested_routine_ref,'create',0,1,recorded_at);
    RETURN QUERY SELECT requested_routine_ref,1::bigint,1::bigint,recorded_at,false;
END;
$function$;
'''
