"""Allow an owned unplaced planned Schedule to receive its first/current placement."""

from collections.abc import Sequence

from alembic import op

revision: str = "20261009_131"
down_revision: str | None = "20261009_130"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.get_bind().exec_driver_sql("""
CREATE TABLE dante.planned_schedule_place_operation (
    self_person_ref uuid NOT NULL CONSTRAINT fk_planned_schedule_place_operation_person
        REFERENCES dante.person(person_ref),
    operation_id text NOT NULL,
    intent_fingerprint text NOT NULL,
    activity_ref uuid NOT NULL CONSTRAINT fk_planned_schedule_place_operation_activity
        REFERENCES dante.activity_intention(activity_ref),
    schedule_ref uuid NOT NULL CONSTRAINT fk_planned_schedule_place_operation_schedule
        REFERENCES dante.schedule(schedule_ref),
    material_state_ref uuid NOT NULL CONSTRAINT fk_planned_schedule_place_operation_state
        REFERENCES dante.schedule_placement_state(material_state_ref),
    created_at timestamptz NOT NULL,
    CONSTRAINT pk_planned_schedule_place_operation PRIMARY KEY(self_person_ref,operation_id),
    CONSTRAINT uq_planned_schedule_place_operation_state UNIQUE(material_state_ref),
    CONSTRAINT ck_planned_schedule_place_operation_id CHECK (
        operation_id=btrim(operation_id) AND operation_id<>'' AND char_length(operation_id)<=200),
    CONSTRAINT ck_planned_schedule_place_operation_fingerprint CHECK (
        intent_fingerprint ~ '^[0-9a-f]{64}$')
);
""")
    op.get_bind().exec_driver_sql("CREATE INDEX ix_planned_schedule_place_operation_schedule_ref "
                                  "ON dante.planned_schedule_place_operation(schedule_ref)")
    op.get_bind().exec_driver_sql("ALTER TABLE dante.planned_schedule_place_operation OWNER TO dante_owner")
    op.get_bind().exec_driver_sql("REVOKE ALL ON TABLE dante.planned_schedule_place_operation "
                                  "FROM PUBLIC,dante_runtime,dante_migrator")
    op.get_bind().exec_driver_sql("""
CREATE FUNCTION dante.place_self_unplaced_planned_schedule(
    requested_actor uuid, requested_operation text, requested_fingerprint text,
    requested_activity uuid, requested_schedule uuid, requested_state uuid,
    requested_payload jsonb
) RETURNS TABLE(schedule_ref uuid, material_state_ref uuid, replayed boolean)
LANGUAGE plpgsql SECURITY DEFINER VOLATILE PARALLEL UNSAFE
SET search_path=pg_catalog,dante,pg_temp AS $function$
#variable_conflict error
DECLARE prior dante.planned_schedule_place_operation%ROWTYPE;
        recorded_at timestamptz;
        last_until timestamptz;
BEGIN
    IF requested_operation IS NULL OR requested_operation<>btrim(requested_operation)
       OR requested_operation='' OR char_length(requested_operation)>200
       OR requested_fingerprint !~ '^[0-9a-f]{64}$'
       OR uuid_extract_version(requested_schedule) IS DISTINCT FROM 7
       OR uuid_extract_version(requested_state) IS DISTINCT FROM 7 THEN
        RAISE EXCEPTION USING ERRCODE='23514',
            CONSTRAINT='planned_schedule_placement_invalid', MESSAGE='Invalid placement';
    END IF;
    PERFORM pg_advisory_xact_lock(hashtextextended(requested_schedule::text,0));
    PERFORM pg_advisory_xact_lock(hashtextextended(requested_actor::text || ':' || requested_operation,0));
    SELECT * INTO prior FROM dante.planned_schedule_place_operation AS receipt
     WHERE receipt.self_person_ref=requested_actor AND receipt.operation_id=requested_operation;
    IF FOUND THEN
        IF prior.intent_fingerprint<>requested_fingerprint
           OR prior.activity_ref<>requested_activity
           OR prior.schedule_ref<>requested_schedule
           OR dante.schedule_placement_payload_json(prior.schedule_ref,prior.material_state_ref)
                IS NULL THEN
            RAISE EXCEPTION USING ERRCODE='23505',
                CONSTRAINT='planned_schedule_placement_conflict', MESSAGE='Placement operation reused';
        END IF;
        RETURN QUERY SELECT prior.schedule_ref,prior.material_state_ref,true;
        RETURN;
    END IF;
    PERFORM 1 FROM dante.activity_intention AS a
      JOIN dante.schedule AS s ON s.subject_native_ref=a.activity_ref
      JOIN dante.activity_schedule_role AS role
        ON role.activity_ref=a.activity_ref AND role.schedule_ref=s.schedule_ref
     WHERE a.activity_ref=requested_activity AND a.self_person_ref=requested_actor
       AND a.retired_at IS NULL AND s.schedule_ref=requested_schedule
       AND role.role_code='planned' FOR UPDATE OF a;
    IF NOT FOUND THEN
        RAISE EXCEPTION USING ERRCODE='23503',
            CONSTRAINT='planned_schedule_placement_unavailable', MESSAGE='Planned row unavailable';
    END IF;
    IF EXISTS (SELECT 1 FROM dante.scoped_current_material_state AS current
                WHERE current.scoped_owner_ref=requested_schedule
                  AND current.facet_code='schedule.placement')
       OR EXISTS (SELECT 1 FROM dante.schedule_placement_current_history AS history
                   WHERE history.schedule_ref=requested_schedule AND history.current_until_at IS NULL) THEN
        RAISE EXCEPTION USING ERRCODE='23505',
            CONSTRAINT='planned_schedule_placement_conflict', MESSAGE='Planned row already placed';
    END IF;
    PERFORM dante.assert_schedule_placement_hard_admissible(requested_activity,requested_payload);
    SELECT max(history.current_until_at) INTO last_until
      FROM dante.schedule_placement_current_history AS history
     WHERE history.schedule_ref=requested_schedule;
    recorded_at := GREATEST(clock_timestamp(),COALESCE(last_until,'-infinity'::timestamptz)
                                               + interval '1 microsecond');
    PERFORM dante.insert_schedule_placement_payload(requested_state,requested_schedule,requested_payload);
    INSERT INTO dante.scoped_current_material_state(scoped_owner_ref,facet_code,material_state_ref)
        VALUES(requested_schedule,'schedule.placement',requested_state);
    INSERT INTO dante.schedule_placement_current_history(
        schedule_ref,material_state_ref,current_from_at,current_until_at)
        VALUES(requested_schedule,requested_state,recorded_at,NULL);
    INSERT INTO dante.planned_schedule_place_operation(
        self_person_ref,operation_id,intent_fingerprint,activity_ref,
        schedule_ref,material_state_ref,created_at)
        VALUES(requested_actor,requested_operation,requested_fingerprint,requested_activity,
               requested_schedule,requested_state,recorded_at);
    RETURN QUERY SELECT requested_schedule,requested_state,false;
END;
$function$;
""")
    signature = "dante.place_self_unplaced_planned_schedule(uuid,text,text,uuid,uuid,uuid,jsonb)"
    op.get_bind().exec_driver_sql(f"ALTER FUNCTION {signature} OWNER TO dante_owner")
    op.get_bind().exec_driver_sql(
        f"REVOKE ALL ON FUNCTION {signature} FROM PUBLIC,dante_runtime,dante_migrator"
    )
    op.get_bind().exec_driver_sql(f"GRANT EXECUTE ON FUNCTION {signature} TO dante_runtime")


def downgrade() -> None:
    raise RuntimeError("Planned Schedule placements require a reviewed forward migration")
