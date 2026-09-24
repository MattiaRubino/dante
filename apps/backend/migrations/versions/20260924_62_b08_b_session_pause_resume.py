"""B08-B immutable Session pause/resume transitions.

Revision ID: 20260924_62
Revises: 20260924_61
"""
from collections.abc import Sequence
import sqlalchemy as sa
from alembic import op

revision: str = "20260924_62"
down_revision: str | None = "20260924_61"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None
_SCHEMA = "dante"
_OWNER = "dante_owner"
_RUNTIME = "dante_runtime"
_MIGRATOR = "dante_migrator"

def _sql(statement: str) -> None:
    op.execute(sa.text(statement))

def upgrade() -> None:
    for action in ("pause", "resume"):
        op.create_table(
            f"session_{action}_operation",
            sa.Column("self_person_ref", sa.Uuid(), nullable=False),
            sa.Column("operation_id", sa.Text(), nullable=False),
            sa.Column("intent_fingerprint", sa.Text(), nullable=False),
            sa.Column("session_ref", sa.Uuid(), nullable=False),
            sa.Column("expected_material_state_ref", sa.Uuid(), nullable=False),
            sa.Column("resulting_material_state_ref", sa.Uuid(), nullable=False),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
            sa.CheckConstraint("operation_id=btrim(operation_id) AND operation_id<>'' AND char_length(operation_id)<=200", name=op.f(f"ck_session_{action}_operation_operation_id")),
            sa.CheckConstraint("intent_fingerprint ~ '^[0-9a-f]{64}$'", name=op.f(f"ck_session_{action}_operation_fingerprint")),
            sa.ForeignKeyConstraint(["self_person_ref"], ["dante.person.person_ref"], name=op.f(f"fk_session_{action}_operation_self_person_ref_person")),
            sa.ForeignKeyConstraint(["session_ref"], ["dante.session.session_ref"], name=op.f(f"fk_session_{action}_operation_session_ref_session")),
            sa.ForeignKeyConstraint(["resulting_material_state_ref"], ["dante.material_state_address.material_state_ref"], name=op.f(f"fk_session_{action}_operation_resulting_state_address")),
            sa.PrimaryKeyConstraint("self_person_ref", "operation_id", name=op.f(f"pk_session_{action}_operation")),
            schema=_SCHEMA,
        )
    _sql(r"""
CREATE FUNCTION dante._transition_self_session(
  requested_transition text, requested_self_person_ref uuid, requested_operation_id text,
  requested_intent_fingerprint text, requested_session_ref uuid,
  requested_expected_material_state_ref uuid, requested_resulting_material_state_ref uuid
) RETURNS TABLE(session_ref uuid,subject_native_ref uuid,timing_material_state_ref uuid,started_at timestamptz,ended_at timestamptz,replayed boolean)
LANGUAGE plpgsql SECURITY DEFINER VOLATILE PARALLEL UNSAFE
SET search_path=pg_catalog,dante,pg_temp
AS $function$
#variable_conflict error
DECLARE
 action_table text; normalized_operation_id text:=btrim(requested_operation_id);
 existing_fingerprint text; existing_session_ref uuid; existing_resulting_state uuid;
 current_state uuid; current_started_at timestamptz; current_start_precision text; current_ended_at timestamptz;
 current_pause_at timestamptz; subject_ref uuid; recorded_at timestamptz:=statement_timestamp(); affected integer;
BEGIN
 IF requested_transition NOT IN ('pause','resume') THEN RAISE EXCEPTION USING ERRCODE='23514',CONSTRAINT='session_transition_invalid'; END IF;
 action_table:='session_'||requested_transition||'_operation';
 IF normalized_operation_id='' OR char_length(normalized_operation_id)>200 OR requested_intent_fingerprint !~ '^[0-9a-f]{64}$' THEN
   RAISE EXCEPTION USING ERRCODE='23514',CONSTRAINT='session_transition_input_invalid';
 END IF;
 IF uuid_extract_version(requested_resulting_material_state_ref) IS DISTINCT FROM 7 OR requested_resulting_material_state_ref=requested_expected_material_state_ref THEN
   RAISE EXCEPTION USING ERRCODE='23514',CONSTRAINT='session_transition_resulting_state_invalid';
 END IF;
 PERFORM pg_advisory_xact_lock(hashtextextended(requested_self_person_ref::text||':'||requested_transition||':'||normalized_operation_id,0));
 EXECUTE format('SELECT intent_fingerprint,session_ref,resulting_material_state_ref FROM dante.%I WHERE self_person_ref=$1 AND operation_id=$2',action_table)
   INTO existing_fingerprint,existing_session_ref,existing_resulting_state USING requested_self_person_ref,normalized_operation_id;
 IF FOUND THEN
   IF existing_fingerprint<>requested_intent_fingerprint OR existing_session_ref<>requested_session_ref THEN RAISE EXCEPTION USING ERRCODE='23505',CONSTRAINT='session_operation_reused'; END IF;
   RETURN QUERY SELECT subject.session_ref,subject.subject_native_ref,existing_resulting_state,absolute_timing.started_at,absolute_timing.ended_at,true
     FROM dante.session_execution_subject subject JOIN dante.session_timing_absolute absolute_timing ON absolute_timing.material_state_ref=existing_resulting_state WHERE subject.session_ref=existing_session_ref;
   RETURN;
 END IF;
 SELECT subject.subject_native_ref INTO subject_ref FROM dante.session_execution_subject subject WHERE subject.session_ref=requested_session_ref;
 IF NOT FOUND OR NOT dante._session_subject_owned(requested_self_person_ref,subject_ref) THEN RAISE EXCEPTION USING ERRCODE='23503',CONSTRAINT='session_subject_unavailable'; END IF;
 PERFORM pg_advisory_xact_lock(hashtextextended(requested_session_ref::text,0));
 SELECT timing.material_state_ref,absolute_timing.started_at,absolute_timing.start_precision_code,absolute_timing.ended_at
  INTO current_state,current_started_at,current_start_precision,current_ended_at FROM dante.session_timing_current_history timing JOIN dante.session_timing_absolute absolute_timing ON absolute_timing.material_state_ref=timing.material_state_ref
  WHERE timing.session_ref=requested_session_ref AND timing.current_until_at IS NULL FOR UPDATE OF timing,absolute_timing;
 SELECT pause.paused_at INTO current_pause_at FROM dante.session_timing_pause pause WHERE pause.material_state_ref=current_state AND pause.resumed_at IS NULL FOR UPDATE;
 IF current_state IS DISTINCT FROM requested_expected_material_state_ref OR current_ended_at IS NOT NULL OR recorded_at<=current_started_at
   OR (requested_transition='pause' AND current_pause_at IS NOT NULL) OR (requested_transition='resume' AND (current_pause_at IS NULL OR recorded_at<=current_pause_at)) THEN
   RAISE EXCEPTION USING ERRCODE='40001',CONSTRAINT='session_'||requested_transition||'_conflict';
 END IF;
 INSERT INTO dante.material_state_address(material_state_ref,native_owner_ref,facet_code) VALUES(requested_resulting_material_state_ref,requested_session_ref,'session.timing');
 INSERT INTO dante.session_timing_state(material_state_ref,session_ref,timing_form_code) VALUES(requested_resulting_material_state_ref,requested_session_ref,'absolute');
 INSERT INTO dante.session_timing_absolute(material_state_ref,started_at,start_precision_code,ended_at,end_precision_code) VALUES(requested_resulting_material_state_ref,current_started_at,current_start_precision,NULL,NULL);
 INSERT INTO dante.session_timing_pause(material_state_ref,paused_at,pause_precision_code,resumed_at,resume_precision_code)
  SELECT requested_resulting_material_state_ref,pause.paused_at,pause.pause_precision_code,
   CASE WHEN requested_transition='resume' AND pause.resumed_at IS NULL THEN recorded_at ELSE pause.resumed_at END,
   CASE WHEN requested_transition='resume' AND pause.resumed_at IS NULL THEN 'exact' ELSE pause.resume_precision_code END
  FROM dante.session_timing_pause pause WHERE pause.material_state_ref=current_state;
 IF requested_transition='pause' THEN INSERT INTO dante.session_timing_pause(material_state_ref,paused_at,pause_precision_code) VALUES(requested_resulting_material_state_ref,recorded_at,'exact'); END IF;
 UPDATE dante.native_current_material_state SET material_state_ref=requested_resulting_material_state_ref WHERE native_owner_ref=requested_session_ref AND facet_code='session.timing' AND material_state_ref=current_state;
 GET DIAGNOSTICS affected=ROW_COUNT; IF affected<>1 THEN RAISE EXCEPTION USING ERRCODE='40001',CONSTRAINT='session_transition_conflict'; END IF;
 UPDATE dante.session_timing_current_history history SET current_until_at=recorded_at WHERE history.session_ref=requested_session_ref AND history.material_state_ref=current_state AND history.current_until_at IS NULL;
 INSERT INTO dante.session_timing_current_history(session_ref,material_state_ref,current_from_at) VALUES(requested_session_ref,requested_resulting_material_state_ref,recorded_at);
 EXECUTE format('INSERT INTO dante.%I(self_person_ref,operation_id,intent_fingerprint,session_ref,expected_material_state_ref,resulting_material_state_ref,created_at) VALUES($1,$2,$3,$4,$5,$6,$7)',action_table)
  USING requested_self_person_ref,normalized_operation_id,requested_intent_fingerprint,requested_session_ref,requested_expected_material_state_ref,requested_resulting_material_state_ref,recorded_at;
 RETURN QUERY SELECT requested_session_ref,subject_ref,requested_resulting_material_state_ref,current_started_at,NULL::timestamptz,false;
END;
$function$;
CREATE FUNCTION dante.pause_self_session(uuid,text,text,uuid,uuid,uuid) RETURNS TABLE(session_ref uuid,subject_native_ref uuid,timing_material_state_ref uuid,started_at timestamptz,ended_at timestamptz,replayed boolean)
LANGUAGE sql SECURITY DEFINER VOLATILE PARALLEL UNSAFE SET search_path=pg_catalog,dante,pg_temp AS 'SELECT * FROM dante._transition_self_session(''pause'',$1,$2,$3,$4,$5,$6)';
CREATE FUNCTION dante.resume_self_session(uuid,text,text,uuid,uuid,uuid) RETURNS TABLE(session_ref uuid,subject_native_ref uuid,timing_material_state_ref uuid,started_at timestamptz,ended_at timestamptz,replayed boolean)
LANGUAGE sql SECURITY DEFINER VOLATILE PARALLEL UNSAFE SET search_path=pg_catalog,dante,pg_temp AS 'SELECT * FROM dante._transition_self_session(''resume'',$1,$2,$3,$4,$5,$6)';
CREATE FUNCTION dante.session_is_paused(requested_self_person_ref uuid,requested_session_ref uuid)
RETURNS boolean LANGUAGE sql SECURITY DEFINER STABLE PARALLEL SAFE
SET search_path=pg_catalog,dante,pg_temp AS
'SELECT EXISTS(SELECT 1 FROM dante.session_execution_subject subject
 JOIN dante.session_timing_current_history timing ON timing.session_ref=subject.session_ref AND timing.current_until_at IS NULL
 JOIN dante.session_timing_pause pause ON pause.material_state_ref=timing.material_state_ref AND pause.resumed_at IS NULL
 WHERE subject.session_ref=$2 AND dante._session_subject_owned($1,subject.subject_native_ref))';
""")
    for name in ("pause_self_session", "resume_self_session"):
        signature=f"dante.{name}(uuid,text,text,uuid,uuid,uuid)"
        _sql(f"ALTER FUNCTION {signature} OWNER TO {_OWNER}")
        _sql(f"REVOKE ALL ON FUNCTION {signature} FROM PUBLIC, {_RUNTIME}, {_MIGRATOR}")
        _sql(f"GRANT EXECUTE ON FUNCTION {signature} TO {_RUNTIME}")
    _sql("ALTER FUNCTION dante.session_is_paused(uuid,uuid) OWNER TO dante_owner")
    _sql("REVOKE ALL ON FUNCTION dante.session_is_paused(uuid,uuid) FROM PUBLIC,dante_runtime,dante_migrator")
    _sql("GRANT EXECUTE ON FUNCTION dante.session_is_paused(uuid,uuid) TO dante_runtime")

def downgrade() -> None:
    raise RuntimeError("B08-B is forward-only: Session timing states are immutable history")
