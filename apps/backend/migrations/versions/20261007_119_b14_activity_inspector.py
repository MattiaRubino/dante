"""Self-scoped Activity profile revision and reversible product visibility.

Revision ID: 20261007_119
Revises: 20261007_118
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSONB

revision: str = "20261007_119"
down_revision: str | None = "20261007_118"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("activity_intention", sa.Column("profile_revision", sa.BigInteger(), server_default="0", nullable=False), schema="dante")
    op.add_column("activity_intention", sa.Column("retired_at", sa.DateTime(timezone=True)), schema="dante")
    op.add_column("activity_intention", sa.Column("retired_operation_id", sa.Text()), schema="dante")
    op.create_check_constraint("ck_activity_intention_profile_revision", "activity_intention", "profile_revision >= 0", schema="dante")
    op.create_check_constraint("ck_activity_intention_retired_pair", "activity_intention", "(retired_at IS NULL) = (retired_operation_id IS NULL)", schema="dante")
    op.create_table(
        "activity_profile_revision",
        sa.Column("activity_ref", sa.Uuid(), nullable=False),
        sa.Column("revision", sa.BigInteger(), nullable=False),
        sa.Column("self_person_ref", sa.Uuid(), nullable=False),
        sa.Column("operation_id", sa.Text(), nullable=False),
        sa.Column("previous_profile", JSONB(), nullable=False),
        sa.Column("current_profile", JSONB(), nullable=False),
        sa.Column("revised_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("activity_ref", "revision", name="pk_activity_profile_revision"),
        sa.UniqueConstraint("self_person_ref", "operation_id", name="uq_activity_profile_revision_operation"),
        sa.ForeignKeyConstraint(["activity_ref"], ["dante.activity_intention.activity_ref"], name="fk_activity_profile_revision_activity"),
        sa.ForeignKeyConstraint(["self_person_ref"], ["dante.person.person_ref"], name="fk_activity_profile_revision_person"),
        sa.CheckConstraint("revision >= 1", name="ck_activity_profile_revision_positive"),
        schema="dante",
    )
    bind = op.get_bind()
    for statement in (_READ, _REVISE, _RETIRE):
        bind.exec_driver_sql(statement)
    bind.exec_driver_sql("ALTER TABLE dante.activity_profile_revision OWNER TO dante_owner")
    bind.exec_driver_sql("REVOKE ALL ON dante.activity_profile_revision FROM PUBLIC,dante_runtime,dante_migrator")
    for signature in (
        "get_self_activity_profile(uuid,uuid)",
        "revise_self_activity_profile(uuid,uuid,text,bigint,text,text,text,text)",
        "retire_self_activity(uuid,uuid,text)",
    ):
        bind.exec_driver_sql(f"ALTER FUNCTION dante.{signature} OWNER TO dante_owner")
        bind.exec_driver_sql(f"REVOKE ALL ON FUNCTION dante.{signature} FROM PUBLIC,dante_runtime,dante_migrator")
        bind.exec_driver_sql(f"GRANT EXECUTE ON FUNCTION dante.{signature} TO dante_runtime")


def downgrade() -> None:
    raise RuntimeError("20261007_119 is forward-only; Activity edits cannot be discarded")


_READ = """
CREATE FUNCTION dante.get_self_activity_profile(actor uuid, requested_activity uuid)
RETURNS TABLE(activity_ref uuid, title text, description text, location text,
              color_code text, revision bigint)
LANGUAGE sql SECURITY DEFINER STABLE PARALLEL SAFE
SET search_path=pg_catalog,dante,pg_temp AS $$
SELECT a.activity_ref,a.title,a.description,a.location,a.color_code,a.profile_revision
  FROM dante.activity_intention AS a
 WHERE a.activity_ref=requested_activity AND a.self_person_ref=actor
   AND a.retired_at IS NULL
$$;
"""

_REVISE = """
CREATE FUNCTION dante.revise_self_activity_profile(
    actor uuid, requested_activity uuid, operation text, expected_revision bigint,
    new_title text, new_description text, new_location text, new_color text
) RETURNS TABLE(activity_ref uuid, title text, description text, location text,
                color_code text, revision bigint, replayed boolean)
LANGUAGE plpgsql SECURITY DEFINER VOLATILE PARALLEL UNSAFE
SET search_path=pg_catalog,dante,pg_temp AS $$
#variable_conflict error
DECLARE owned dante.activity_intention%ROWTYPE;
        prior dante.activity_profile_revision%ROWTYPE;
BEGIN
    IF operation IS NULL OR operation<>btrim(operation) OR operation=''
       OR char_length(operation)>200 OR expected_revision IS NULL OR expected_revision<0
       OR new_title IS NULL OR new_title<>btrim(new_title)
       OR new_title='' OR char_length(new_title)>300
       OR (new_description IS NOT NULL AND (new_description<>btrim(new_description) OR new_description=''))
       OR (new_location IS NOT NULL AND (new_location<>btrim(new_location) OR new_location=''))
       OR (new_color IS NOT NULL AND new_color !~ '^#[0-9A-F]{6}$') THEN
        RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT='activity_profile_invalid',
            MESSAGE='Invalid Activity profile';
    END IF;
    SELECT * INTO owned FROM dante.activity_intention AS a
     WHERE a.activity_ref=requested_activity AND a.self_person_ref=actor FOR UPDATE;
    IF NOT FOUND OR owned.retired_at IS NOT NULL THEN
        RAISE EXCEPTION USING ERRCODE='23503', CONSTRAINT='activity_profile_unavailable',
            MESSAGE='Activity unavailable';
    END IF;
    SELECT * INTO prior FROM dante.activity_profile_revision AS history
     WHERE history.self_person_ref=actor AND history.operation_id=operation;
    IF FOUND THEN
        IF prior.activity_ref<>requested_activity
           OR prior.current_profile IS DISTINCT FROM jsonb_build_object(
               'title',new_title,'description',new_description,
               'location',new_location,'color_code',new_color
           ) THEN
            RAISE EXCEPTION USING ERRCODE='23505', CONSTRAINT='activity_profile_operation_reused',
                MESSAGE='Operation reused for different content';
        END IF;
        RETURN QUERY SELECT prior.activity_ref,prior.current_profile->>'title',
                            prior.current_profile->>'description',
                            prior.current_profile->>'location',
                            prior.current_profile->>'color_code',prior.revision,true;
        RETURN;
    END IF;
    IF owned.profile_revision<>expected_revision THEN
        RAISE EXCEPTION USING ERRCODE='23505', CONSTRAINT='activity_profile_stale',
            MESSAGE='Activity changed';
    END IF;
    INSERT INTO dante.activity_profile_revision(
        activity_ref,revision,self_person_ref,operation_id,
        previous_profile,current_profile,revised_at
    ) VALUES (
        requested_activity,owned.profile_revision+1,actor,operation,
        jsonb_build_object('title',owned.title,'description',owned.description,
                           'location',owned.location,'color_code',owned.color_code),
        jsonb_build_object('title',new_title,'description',new_description,
                           'location',new_location,'color_code',new_color),
        statement_timestamp()
    );
    UPDATE dante.activity_intention AS a
       SET title=new_title,description=new_description,location=new_location,
           color_code=new_color,profile_revision=owned.profile_revision+1
     WHERE a.activity_ref=requested_activity;
    RETURN QUERY SELECT requested_activity,new_title,new_description,new_location,
                        new_color,owned.profile_revision+1,false;
END;
$$;
"""

_RETIRE = """
CREATE FUNCTION dante.retire_self_activity(actor uuid, requested_activity uuid, operation text)
RETURNS boolean
LANGUAGE plpgsql SECURITY DEFINER VOLATILE PARALLEL UNSAFE
SET search_path=pg_catalog,dante,pg_temp AS $$
DECLARE owned dante.activity_intention%ROWTYPE;
BEGIN
    IF operation IS NULL OR operation<>btrim(operation) OR operation=''
       OR char_length(operation)>200 THEN
        RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT='activity_profile_invalid',
            MESSAGE='Invalid operation';
    END IF;
    SELECT * INTO owned FROM dante.activity_intention AS a
     WHERE a.activity_ref=requested_activity AND a.self_person_ref=actor FOR UPDATE;
    IF NOT FOUND THEN
        RAISE EXCEPTION USING ERRCODE='23503', CONSTRAINT='activity_profile_unavailable',
            MESSAGE='Activity unavailable';
    END IF;
    IF owned.retired_at IS NOT NULL THEN
        IF owned.retired_operation_id=operation THEN RETURN true; END IF;
        RAISE EXCEPTION USING ERRCODE='23505', CONSTRAINT='activity_profile_stale',
            MESSAGE='Activity already retired';
    END IF;
    IF EXISTS (
        SELECT 1 FROM dante.list_self_subject_sessions(actor,requested_activity) AS session
         WHERE session.ended_at IS NULL
    ) THEN
        RAISE EXCEPTION USING ERRCODE='23505', CONSTRAINT='activity_profile_active_session',
            MESSAGE='End active Session before retirement';
    END IF;
    UPDATE dante.activity_intention AS a
       SET retired_at=statement_timestamp(),retired_operation_id=operation
     WHERE a.activity_ref=requested_activity;
    RETURN false;
END;
$$;
"""
