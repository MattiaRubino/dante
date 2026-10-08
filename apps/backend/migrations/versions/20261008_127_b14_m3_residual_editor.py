"""B14 M3: amend organizational assignment and presentation, preserving recorded truth."""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20261008_127"
down_revision: str | None = "20261008_126"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def _assign_sql(kind: str, descriptor: str) -> str:
    assignment = f"{kind}_life_area_assignment"
    operation = f"{assignment}_operation"
    return f"""
CREATE OR REPLACE FUNCTION dante.assign_self_{kind}_life_area(
  requested_self_person_ref uuid, requested_operation_id text,
  requested_intent_fingerprint text, requested_{kind}_ref uuid,
  requested_life_area_ref uuid, requested_expected_revision bigint
) RETURNS TABLE(life_area_ref uuid, assignment_revision bigint,
                assigned_at timestamptz, replayed boolean)
LANGUAGE plpgsql SECURITY DEFINER VOLATILE PARALLEL UNSAFE
SET search_path=pg_catalog,dante,pg_temp AS $function$
#variable_conflict error
DECLARE old_receipt record; current_row record;
        accepted_at timestamptz := statement_timestamp();
BEGIN
  IF requested_operation_id IS NULL OR requested_operation_id<>btrim(requested_operation_id)
     OR char_length(requested_operation_id) NOT BETWEEN 1 AND 200
     OR requested_intent_fingerprint IS NULL
     OR requested_intent_fingerprint !~ '^[0-9a-f]{{64}}$'
     OR requested_expected_revision IS NULL OR requested_expected_revision<0 THEN
    RAISE EXCEPTION USING ERRCODE='23514',
      CONSTRAINT='life_area_assignment_invalid', MESSAGE='Invalid organization command';
  END IF;
  PERFORM 1 FROM dante.person WHERE person_ref=requested_self_person_ref FOR UPDATE;
  IF NOT FOUND OR NOT EXISTS (
      SELECT 1 FROM dante.account_application_context
      WHERE self_person_ref=requested_self_person_ref
  ) THEN
    RAISE EXCEPTION USING ERRCODE='23503',
      CONSTRAINT='life_area_assignment_target_unavailable',
      MESSAGE='Self context unavailable';
  END IF;
  SELECT * INTO old_receipt FROM dante.{operation}
   WHERE self_person_ref=requested_self_person_ref AND operation_id=requested_operation_id;
  IF FOUND THEN
    IF old_receipt.intent_fingerprint IS DISTINCT FROM requested_intent_fingerprint
       OR old_receipt.{kind}_ref IS DISTINCT FROM requested_{kind}_ref
       OR old_receipt.life_area_ref IS DISTINCT FROM requested_life_area_ref
       OR old_receipt.expected_revision IS DISTINCT FROM requested_expected_revision THEN
      RAISE EXCEPTION USING ERRCODE='23505', CONSTRAINT='pk_{operation}',
        MESSAGE='Life Area operation ID reused';
    END IF;
    RETURN QUERY SELECT old_receipt.life_area_ref,old_receipt.accepted_revision,
      old_receipt.accepted_at,true;
    RETURN;
  END IF;
  PERFORM 1 FROM dante.{descriptor}
   WHERE {kind}_ref=requested_{kind}_ref AND self_person_ref=requested_self_person_ref;
  IF NOT FOUND THEN
    RAISE EXCEPTION USING ERRCODE='23503',
      CONSTRAINT='life_area_assignment_target_unavailable',
      MESSAGE='Item unavailable to this actor';
  END IF;
  IF requested_life_area_ref IS NOT NULL AND NOT EXISTS (
    SELECT 1 FROM dante.life_area
     WHERE life_area_ref=requested_life_area_ref
       AND self_person_ref=requested_self_person_ref AND archived=false
  ) THEN
    RAISE EXCEPTION USING ERRCODE='23503',
      CONSTRAINT='life_area_assignment_target_unavailable',
      MESSAGE='Life Area is not an active owned target';
  END IF;
  SELECT * INTO current_row FROM dante.{assignment}
   WHERE self_person_ref=requested_self_person_ref
     AND {kind}_ref=requested_{kind}_ref FOR UPDATE;
  IF NOT FOUND THEN
    IF requested_expected_revision<>0 THEN
      RAISE EXCEPTION USING ERRCODE='23514',
        CONSTRAINT='life_area_assignment_revision_conflict',
        MESSAGE='Expected unassigned state is stale';
    END IF;
    IF requested_life_area_ref IS NULL THEN
      RAISE EXCEPTION USING ERRCODE='23514',
        CONSTRAINT='life_area_assignment_no_change',MESSAGE='Already unassigned';
    END IF;
    INSERT INTO dante.{assignment}(
      {kind}_ref,self_person_ref,life_area_ref,revision,assigned_at
    ) VALUES(requested_{kind}_ref,requested_self_person_ref,
      requested_life_area_ref,1,accepted_at);
  ELSE
    IF current_row.revision<>requested_expected_revision THEN
      RAISE EXCEPTION USING ERRCODE='23514',
        CONSTRAINT='life_area_assignment_revision_conflict',
        MESSAGE='Assignment changed';
    END IF;
    IF current_row.life_area_ref IS NOT DISTINCT FROM requested_life_area_ref THEN
      RAISE EXCEPTION USING ERRCODE='23514',
        CONSTRAINT='life_area_assignment_no_change',MESSAGE='Assignment unchanged';
    END IF;
    UPDATE dante.{assignment} SET life_area_ref=requested_life_area_ref,
       revision=requested_expected_revision+1,assigned_at=accepted_at
     WHERE self_person_ref=requested_self_person_ref
       AND {kind}_ref=requested_{kind}_ref;
  END IF;
  INSERT INTO dante.{operation}(
    self_person_ref,operation_id,intent_fingerprint,{kind}_ref,
    life_area_ref,expected_revision,accepted_revision,accepted_at
  ) VALUES(requested_self_person_ref,requested_operation_id,requested_intent_fingerprint,
    requested_{kind}_ref,requested_life_area_ref,
    requested_expected_revision,requested_expected_revision+1,accepted_at);
  RETURN QUERY SELECT requested_life_area_ref,requested_expected_revision+1,accepted_at,false;
END
$function$;
"""  # noqa: S608


_UNASSIGNED = """
CREATE OR REPLACE FUNCTION dante.list_self_unassigned_life_area_items(
  requested_self_person_ref uuid
) RETURNS TABLE(subject_kind text, subject_native_ref uuid,title text,created_at timestamptz)
LANGUAGE sql SECURITY DEFINER STABLE PARALLEL SAFE
SET search_path=pg_catalog,dante,pg_temp AS $function$
SELECT 'activity'::text,a.activity_ref,a.title,a.created_at
FROM dante.activity_intention a
WHERE a.self_person_ref=requested_self_person_ref
 AND EXISTS(SELECT 1 FROM dante.account_application_context c
            WHERE c.self_person_ref=requested_self_person_ref)
 AND NOT EXISTS(SELECT 1 FROM dante.activity_life_area_assignment l
  WHERE l.self_person_ref=requested_self_person_ref AND l.activity_ref=a.activity_ref
   AND l.life_area_ref IS NOT NULL)
UNION ALL
SELECT 'event'::text,e.event_ref,e.title,e.created_at
FROM dante.event_expectation e
WHERE e.self_person_ref=requested_self_person_ref
 AND EXISTS(SELECT 1 FROM dante.account_application_context c
            WHERE c.self_person_ref=requested_self_person_ref)
 AND NOT EXISTS(SELECT 1 FROM dante.event_life_area_assignment l
  WHERE l.self_person_ref=requested_self_person_ref AND l.event_ref=e.event_ref
   AND l.life_area_ref IS NOT NULL)
ORDER BY 1,4,2
$function$;
"""


_PLANNED_NAME = """
CREATE FUNCTION dante.revise_self_planned_session_name(
 actor uuid, requested_activity uuid, requested_schedule uuid,
 expected_name text, new_name text
) RETURNS TABLE(schedule_ref uuid,display_name text,replayed boolean)
LANGUAGE plpgsql SECURITY DEFINER VOLATILE PARALLEL UNSAFE
SET search_path=pg_catalog,dante,pg_temp AS $function$
#variable_conflict error
DECLARE existing record;
BEGIN
 IF new_name IS NOT NULL AND
    (new_name<>btrim(new_name) OR new_name='' OR char_length(new_name)>300) THEN
   RAISE EXCEPTION USING ERRCODE='23514',
     CONSTRAINT='activity_planned_name_invalid',MESSAGE='Invalid planned Session label';
 END IF;
 PERFORM 1 FROM dante.activity_intention a
  WHERE a.activity_ref=requested_activity AND a.self_person_ref=actor
    AND a.retired_at IS NULL FOR UPDATE;
 IF NOT FOUND THEN
   RAISE EXCEPTION USING ERRCODE='23503',
    CONSTRAINT='activity_planned_name_unavailable',MESSAGE='Activity not found';
 END IF;
 SELECT * INTO existing FROM dante.activity_schedule_role r
  WHERE r.activity_ref=requested_activity AND r.schedule_ref=requested_schedule
   AND r.role_code='planned' FOR UPDATE;
 IF NOT FOUND THEN
   RAISE EXCEPTION USING ERRCODE='23503',
    CONSTRAINT='activity_planned_name_unavailable',MESSAGE='Planned row not found';
 END IF;
 IF existing.display_name IS NOT DISTINCT FROM new_name THEN
   RETURN QUERY SELECT requested_schedule,new_name,true;
   RETURN;
 END IF;
 IF existing.display_name IS DISTINCT FROM expected_name THEN
   RAISE EXCEPTION USING ERRCODE='23505',
    CONSTRAINT='activity_planned_name_stale',MESSAGE='Planned Session label changed';
 END IF;
 UPDATE dante.activity_schedule_role AS r SET display_name=new_name
  WHERE r.schedule_ref=requested_schedule AND r.activity_ref=requested_activity;
 RETURN QUERY SELECT requested_schedule,new_name,false;
END
$function$;
"""


_RETIRE = """
CREATE OR REPLACE FUNCTION dante.retire_self_activity(
 actor uuid, requested_activity uuid, operation text
) RETURNS boolean LANGUAGE plpgsql SECURITY DEFINER VOLATILE PARALLEL UNSAFE
SET search_path=pg_catalog,dante,pg_temp AS $function$
DECLARE owned record;
BEGIN
 IF operation IS NULL OR operation<>btrim(operation)
    OR operation='' OR char_length(operation)>200 THEN
   RAISE EXCEPTION USING ERRCODE='23514',
     CONSTRAINT='activity_profile_invalid',MESSAGE='Invalid operation';
 END IF;
 SELECT * INTO owned FROM dante.activity_intention a
  WHERE a.activity_ref=requested_activity AND a.self_person_ref=actor FOR UPDATE;
 IF NOT FOUND THEN
   RAISE EXCEPTION USING ERRCODE='23503',
     CONSTRAINT='activity_profile_unavailable',MESSAGE='Activity not owned';
 END IF;
 IF owned.retired_at IS NOT NULL THEN
   IF owned.retired_operation_id=operation THEN RETURN true; END IF;
   RAISE EXCEPTION USING ERRCODE='23505',
     CONSTRAINT='activity_profile_stale',MESSAGE='Activity already retired';
 END IF;
 IF EXISTS(SELECT 1 FROM dante.list_self_subject_sessions(actor,requested_activity) s
    WHERE s.ended_at IS NULL) THEN
   RAISE EXCEPTION USING ERRCODE='23505',
     CONSTRAINT='activity_profile_active_session',MESSAGE='Active execution';
 END IF;
 IF EXISTS(SELECT 1 FROM dante.list_self_subject_sessions(actor,requested_activity))
    OR EXISTS(SELECT 1 FROM dante.get_self_subject_actual(
      actor,'activity',requested_activity))
    OR EXISTS(SELECT 1 FROM dante.list_self_temporal_objectives(
      actor,'activity',requested_activity) AS o
      WHERE o.observation_ref IS NOT NULL OR o.evaluation_state_ref IS NOT NULL) THEN
   RAISE EXCEPTION USING ERRCODE='23505',
     CONSTRAINT='activity_profile_recorded_truth',
     MESSAGE='Recorded facts cannot be retired';
 END IF;
 UPDATE dante.activity_intention a
    SET retired_at=statement_timestamp(),retired_operation_id=operation
  WHERE a.activity_ref=requested_activity;
 RETURN false;
END
$function$;
"""


def upgrade() -> None:
    for kind in ("activity", "event"):
        for suffix in ("", "_operation"):
            op.alter_column(
                f"{kind}_life_area_assignment{suffix}", "life_area_ref",
                existing_type=sa.Uuid(), nullable=True, schema="dante",
            )
    bind = op.get_bind()
    for kind, descriptor in (
        ("activity", "activity_intention"),
        ("event", "event_expectation"),
    ):
        bind.exec_driver_sql(_assign_sql(kind, descriptor))
    bind.exec_driver_sql(_UNASSIGNED)
    bind.exec_driver_sql(_PLANNED_NAME)
    bind.exec_driver_sql(_RETIRE)
    signature = "dante.revise_self_planned_session_name(uuid,uuid,uuid,text,text)"
    bind.exec_driver_sql(f"ALTER FUNCTION {signature} OWNER TO dante_owner")
    bind.exec_driver_sql(
        f"REVOKE ALL ON FUNCTION {signature} FROM PUBLIC,dante_runtime,dante_migrator"
    )
    bind.exec_driver_sql(f"GRANT EXECUTE ON FUNCTION {signature} TO dante_runtime")


def downgrade() -> None:
    raise NotImplementedError("M3 organization and history guard are forward-only")
