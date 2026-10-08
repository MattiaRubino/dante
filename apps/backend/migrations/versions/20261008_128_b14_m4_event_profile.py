"""B14 M4: append-only Event profile edit behind actor ownership and CAS."""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSONB

revision: str = "20261008_128"
down_revision: str | None = "20261008_127"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_PROFILE_EDIT = """
CREATE FUNCTION dante.revise_self_event_profile(
  actor uuid, requested_event uuid, requested_operation text,
  requested_expected_revision bigint, requested_title text,
  requested_description text, requested_location text, requested_color_code text
) RETURNS TABLE(
 event_ref uuid, title text, description text, location text,
 color_code text, revision bigint, replayed boolean
)
LANGUAGE plpgsql SECURITY DEFINER VOLATILE PARALLEL UNSAFE
SET search_path=pg_catalog,dante,pg_temp AS $function$
#variable_conflict error
DECLARE owned record; prior record;
        current_revision bigint;
        existing_profile jsonb; proposed_profile jsonb;
        accepted_at timestamptz := statement_timestamp();
BEGIN
 IF requested_operation IS NULL OR requested_operation<>btrim(requested_operation)
    OR requested_operation='' OR char_length(requested_operation)>200
    OR requested_expected_revision IS NULL OR requested_expected_revision<0
    OR requested_title IS NULL OR requested_title<>btrim(requested_title)
    OR requested_title='' OR char_length(requested_title)>300
    OR (requested_description IS NOT NULL AND
       (requested_description<>btrim(requested_description) OR requested_description=''))
    OR (requested_location IS NOT NULL AND
       (requested_location<>btrim(requested_location) OR requested_location=''))
    OR (requested_color_code IS NOT NULL AND
       requested_color_code !~ '^#[0-9A-F]{6}$')
 THEN
  RAISE EXCEPTION USING ERRCODE='23514',
   CONSTRAINT='event_profile_invalid',MESSAGE='Invalid Event metadata';
 END IF;
 PERFORM 1 FROM dante.person p WHERE p.person_ref=actor FOR UPDATE;
 IF NOT FOUND OR NOT EXISTS(
   SELECT 1 FROM dante.account_application_context c
   WHERE c.self_person_ref=actor
 ) THEN
  RAISE EXCEPTION USING ERRCODE='23503',
   CONSTRAINT='event_profile_unavailable', MESSAGE='Self context unavailable';
 END IF;
 SELECT * INTO owned FROM dante.event_expectation e
  WHERE e.event_ref=requested_event AND e.self_person_ref=actor FOR UPDATE;
 IF NOT FOUND THEN
  RAISE EXCEPTION USING ERRCODE='23503',
   CONSTRAINT='event_profile_unavailable',MESSAGE='Event outside actor scope';
 END IF;
 proposed_profile:=jsonb_build_object(
  'title',requested_title,'description',requested_description,
  'location',requested_location,'color_code',requested_color_code
 );
 SELECT * INTO prior FROM dante.event_profile_revision r
  WHERE r.self_person_ref=actor AND r.operation_id=requested_operation;
 IF FOUND THEN
  IF prior.event_ref<>requested_event
    OR prior.expected_revision<>requested_expected_revision
    OR prior.current_profile IS DISTINCT FROM proposed_profile
  THEN
   RAISE EXCEPTION USING ERRCODE='23505',
    CONSTRAINT='uq_event_profile_revision_operation',
    MESSAGE='Event profile operation ID reused';
  END IF;
  RETURN QUERY SELECT requested_event,
    prior.current_profile->>'title',prior.current_profile->>'description',
    prior.current_profile->>'location',prior.current_profile->>'color_code',
    prior.revision,true;
  RETURN;
 END IF;
 SELECT COALESCE(MAX(r.revision),0) INTO current_revision
  FROM dante.event_profile_revision r WHERE r.event_ref=requested_event;
 IF EXISTS(SELECT 1 FROM dante.event_recurrence_state er
           WHERE er.event_ref=requested_event) THEN
  RAISE EXCEPTION USING ERRCODE='23505',
   CONSTRAINT='event_profile_recurring_source',
   MESSAGE='Edit selected Occurrence through scoped profile, not recurring source';
 END IF;
 IF current_revision<>requested_expected_revision THEN
  RAISE EXCEPTION USING ERRCODE='23505',
   CONSTRAINT='event_profile_revision_conflict',MESSAGE='Event changed';
 END IF;
 existing_profile:=jsonb_build_object(
  'title',owned.title,'description',owned.description,
  'location',owned.location,'color_code',owned.color_code
 );
 IF existing_profile=proposed_profile THEN
  RAISE EXCEPTION USING ERRCODE='23514',
   CONSTRAINT='event_profile_no_change',MESSAGE='Event metadata unchanged';
 END IF;
 UPDATE dante.event_expectation AS e SET
  title=requested_title, description=requested_description,
  location=requested_location,color_code=requested_color_code
  WHERE e.event_ref=requested_event AND e.self_person_ref=actor;
 INSERT INTO dante.event_profile_revision(
   event_ref,revision,self_person_ref,operation_id,expected_revision,
   previous_profile,current_profile,revised_at
 ) VALUES(
   requested_event,current_revision+1,actor,requested_operation,
   requested_expected_revision,existing_profile,proposed_profile,accepted_at
 );
 RETURN QUERY SELECT requested_event,requested_title,requested_description,
  requested_location,requested_color_code,current_revision+1,false;
END
$function$;
"""


_PROFILE_REVISION_READ = """
CREATE FUNCTION dante.get_self_event_profile_revision(
  actor uuid, requested_event uuid
) RETURNS bigint
LANGUAGE sql SECURITY DEFINER STABLE PARALLEL SAFE
SET search_path=pg_catalog,dante,pg_temp AS $function$
  SELECT CASE WHEN EXISTS (
    SELECT 1 FROM dante.event_expectation e
    WHERE e.event_ref=requested_event AND e.self_person_ref=actor
  ) THEN (
    SELECT COALESCE(MAX(r.revision),0) FROM dante.event_profile_revision r
    WHERE r.event_ref=requested_event AND r.self_person_ref=actor
  ) ELSE NULL END
$function$;
"""


def upgrade() -> None:
    op.create_table(
        "event_profile_revision",
        sa.Column("event_ref", sa.Uuid(), nullable=False),
        sa.Column("revision", sa.BigInteger(), nullable=False),
        sa.Column("self_person_ref", sa.Uuid(), nullable=False),
        sa.Column("operation_id", sa.Text(), nullable=False),
        sa.Column("expected_revision", sa.BigInteger(), nullable=False),
        sa.Column("previous_profile", JSONB(), nullable=False),
        sa.Column("current_profile", JSONB(), nullable=False),
        sa.Column("revised_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("event_ref", "revision", name="pk_event_profile_revision"),
        sa.UniqueConstraint("self_person_ref", "operation_id",
                            name="uq_event_profile_revision_operation"),
        sa.ForeignKeyConstraint(["event_ref"], ["dante.event_expectation.event_ref"],
                                name="fk_event_profile_revision_event"),
        sa.ForeignKeyConstraint(["self_person_ref"], ["dante.person.person_ref"],
                                name="fk_event_profile_revision_person"),
        sa.CheckConstraint("revision>=1 AND expected_revision>=0",
                           name=op.f("ck_event_profile_revision_revision")),
        schema="dante",
    )
    db = op.get_bind()
    db.exec_driver_sql("ALTER TABLE dante.event_profile_revision OWNER TO dante_owner")
    db.exec_driver_sql("REVOKE ALL ON dante.event_profile_revision FROM PUBLIC,dante_runtime,dante_migrator")
    db.exec_driver_sql(_PROFILE_EDIT)
    db.exec_driver_sql(_PROFILE_REVISION_READ)
    for sig in (
        "dante.revise_self_event_profile(uuid,uuid,text,bigint,text,text,text,text)",
        "dante.get_self_event_profile_revision(uuid,uuid)",
    ):
        db.exec_driver_sql(f"ALTER FUNCTION {sig} OWNER TO dante_owner")
        db.exec_driver_sql(
            f"REVOKE ALL ON FUNCTION {sig} FROM PUBLIC,dante_migrator,dante_runtime"
        )
        db.exec_driver_sql(f"GRANT EXECUTE ON FUNCTION {sig} TO dante_runtime")


def downgrade() -> None:
    raise NotImplementedError("M4 immutable Event profile audit is forward-only")
