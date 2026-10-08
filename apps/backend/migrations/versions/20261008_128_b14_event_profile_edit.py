"""B14 M4 immutable Event profile revisions for one-off Event Inspector editing.

Revision ID: 20261008_128
Revises: 20261008_127
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSONB

revision: str = "20261008_128"
down_revision: str | None = "20261008_127"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "event_expectation",
        sa.Column("profile_revision", sa.BigInteger(), server_default="0", nullable=False),
        schema="dante",
    )
    op.create_check_constraint(
        "ck_event_expectation_profile_revision", "event_expectation",
        "profile_revision >= 0", schema="dante",
    )
    op.create_table(
        "event_profile_revision",
        sa.Column("event_ref", sa.Uuid(), nullable=False),
        sa.Column("revision", sa.BigInteger(), nullable=False),
        sa.Column("self_person_ref", sa.Uuid(), nullable=False),
        sa.Column("operation_id", sa.Text(), nullable=False),
        sa.Column("previous_profile", JSONB(), nullable=False),
        sa.Column("current_profile", JSONB(), nullable=False),
        sa.Column("revised_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("event_ref", "revision", name="pk_event_profile_revision"),
        sa.UniqueConstraint(
            "self_person_ref", "operation_id", name="uq_event_profile_revision_operation"
        ),
        sa.ForeignKeyConstraint(
            ["event_ref"], ["dante.event_expectation.event_ref"],
            name="fk_event_profile_revision_event",
        ),
        sa.ForeignKeyConstraint(
            ["self_person_ref"], ["dante.person.person_ref"],
            name="fk_event_profile_revision_person",
        ),
        sa.CheckConstraint("revision >= 1", name="ck_event_profile_revision_positive"),
        schema="dante",
    )
    bind = op.get_bind()
    for statement in (_READ, _REVISE):
        bind.exec_driver_sql(statement)
    bind.exec_driver_sql("ALTER TABLE dante.event_profile_revision OWNER TO dante_owner")
    bind.exec_driver_sql(
        "REVOKE ALL ON dante.event_profile_revision FROM PUBLIC,dante_runtime,dante_migrator"
    )
    for signature in (
        "get_self_event_profile(uuid,uuid)",
        "revise_self_event_profile(uuid,uuid,text,bigint,text,text,text,text)",
    ):
        bind.exec_driver_sql(f"ALTER FUNCTION dante.{signature} OWNER TO dante_owner")
        bind.exec_driver_sql(
            f"REVOKE ALL ON FUNCTION dante.{signature} FROM PUBLIC,dante_runtime,dante_migrator"
        )
        bind.exec_driver_sql(f"GRANT EXECUTE ON FUNCTION dante.{signature} TO dante_runtime")


def downgrade() -> None:
    raise RuntimeError("20261008_128 is forward-only; Event edit audit cannot be discarded")


_READ = """
CREATE FUNCTION dante.get_self_event_profile(actor uuid, requested_event uuid)
RETURNS TABLE(event_ref uuid, title text, description text, location text,
              color_code text, revision bigint)
LANGUAGE sql SECURITY DEFINER STABLE PARALLEL SAFE
SET search_path=pg_catalog,dante,pg_temp AS $$
SELECT a.event_ref,a.title,a.description,a.location,a.color_code,a.profile_revision
  FROM dante.event_expectation AS a
 WHERE a.event_ref=requested_event AND a.self_person_ref=actor

$$;
"""

_REVISE = """
CREATE FUNCTION dante.revise_self_event_profile(
    actor uuid, requested_event uuid, operation text, expected_revision bigint,
    new_title text, new_description text, new_location text, new_color text
) RETURNS TABLE(event_ref uuid, title text, description text, location text,
                color_code text, revision bigint, replayed boolean)
LANGUAGE plpgsql SECURITY DEFINER VOLATILE PARALLEL UNSAFE
SET search_path=pg_catalog,dante,pg_temp AS $$
#variable_conflict error
DECLARE owned dante.event_expectation%ROWTYPE;
        prior dante.event_profile_revision%ROWTYPE;
BEGIN
    IF operation IS NULL OR operation<>btrim(operation) OR operation=''
       OR char_length(operation)>200 OR expected_revision IS NULL OR expected_revision<0
       OR new_title IS NULL OR new_title<>btrim(new_title)
       OR new_title='' OR char_length(new_title)>300
       OR (new_description IS NOT NULL AND (new_description<>btrim(new_description) OR new_description=''))
       OR (new_location IS NOT NULL AND (new_location<>btrim(new_location) OR new_location=''))
       OR (new_color IS NOT NULL AND new_color !~ '^#[0-9A-F]{6}$') THEN
        RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT='event_profile_invalid',
            MESSAGE='Invalid Event profile';
    END IF;
    SELECT * INTO owned FROM dante.event_expectation AS a
     WHERE a.event_ref=requested_event AND a.self_person_ref=actor FOR UPDATE;
    IF NOT FOUND THEN
        RAISE EXCEPTION USING ERRCODE='23503', CONSTRAINT='event_profile_unavailable',
            MESSAGE='Event unavailable';
    END IF;
    SELECT * INTO prior FROM dante.event_profile_revision AS history
     WHERE history.self_person_ref=actor AND history.operation_id=operation;
    IF FOUND THEN
        IF prior.event_ref<>requested_event
           OR prior.current_profile IS DISTINCT FROM jsonb_build_object(
               'title',new_title,'description',new_description,
               'location',new_location,'color_code',new_color
           ) THEN
            RAISE EXCEPTION USING ERRCODE='23505', CONSTRAINT='event_profile_operation_reused',
                MESSAGE='Operation reused for different content';
        END IF;
        RETURN QUERY SELECT prior.event_ref,prior.current_profile->>'title',
                            prior.current_profile->>'description',
                            prior.current_profile->>'location',
                            prior.current_profile->>'color_code',prior.revision,true;
        RETURN;
    END IF;
    IF EXISTS(SELECT 1 FROM dante.event_recurrence_state AS er
              WHERE er.event_ref=requested_event) THEN
        RAISE EXCEPTION USING ERRCODE='23505', CONSTRAINT='event_profile_recurring_source',
            MESSAGE='Edit the selected Occurrence, not a recurring Event source';
    END IF;
    IF owned.profile_revision<>expected_revision THEN
        RAISE EXCEPTION USING ERRCODE='23505', CONSTRAINT='event_profile_stale',
            MESSAGE='Event changed';
    END IF;
    INSERT INTO dante.event_profile_revision(
        event_ref,revision,self_person_ref,operation_id,
        previous_profile,current_profile,revised_at
    ) VALUES (
        requested_event,owned.profile_revision+1,actor,operation,
        jsonb_build_object('title',owned.title,'description',owned.description,
                           'location',owned.location,'color_code',owned.color_code),
        jsonb_build_object('title',new_title,'description',new_description,
                           'location',new_location,'color_code',new_color),
        statement_timestamp()
    );
    UPDATE dante.event_expectation AS a
       SET title=new_title,description=new_description,location=new_location,
           color_code=new_color,profile_revision=owned.profile_revision+1
     WHERE a.event_ref=requested_event;
    RETURN QUERY SELECT requested_event,new_title,new_description,new_location,
                        new_color,owned.profile_revision+1,false;
END;
$$;
"""

