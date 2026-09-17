"""Materialize bounded ordered Event-internal Agenda parts for B03-D.

Revision ID: 20260917_29
Revises: 20260917_28
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "20260917_29"
down_revision: str | None = "20260917_28"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_SCHEMA = "dante"
_OWNER = "dante_owner"
_MIGRATOR = "dante_migrator"
_RUNTIME = "dante_runtime"


def upgrade() -> None:
    """Add ordered Event-internal Agenda values without inflating their identity."""
    op.create_table(
        "event_agenda_part",
        sa.Column("event_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("position", sa.Integer(), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint(
            "event_ref",
            "position",
            name=op.f("pk_event_agenda_part"),
        ),
        sa.ForeignKeyConstraint(
            ["event_ref"],
            [f"{_SCHEMA}.event_expectation.event_ref"],
            name="fk_event_agenda_part_event_ref_event_expectation",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        sa.CheckConstraint(
            "position >= 1 AND position <= 100",
            name=op.f("ck_event_agenda_part_position"),
        ),
        sa.CheckConstraint(
            "content=btrim(content) AND content<>'' AND char_length(content)<=1000",
            name=op.f("ck_event_agenda_part_content"),
        ),
        schema=_SCHEMA,
    )

    op.execute(
        sa.text(
            r"""
            CREATE FUNCTION dante.create_self_event_with_agenda(
                requested_self_person_ref uuid,
                requested_operation_id text,
                requested_intent_fingerprint text,
                requested_event_ref uuid,
                requested_title text,
                requested_agenda_parts text[]
            )
            RETURNS TABLE(
                event_ref uuid,
                title text,
                created_at timestamptz,
                agenda_parts text[],
                replayed boolean
            )
            LANGUAGE plpgsql
            SECURITY DEFINER
            VOLATILE
            PARALLEL UNSAFE
            SET search_path = pg_catalog, dante, pg_temp
            AS $function$
            #variable_conflict error
            DECLARE
                normalized_agenda text[] := ARRAY[]::text[];
                candidate_part text;
                created_event_ref uuid;
                created_title text;
                event_created_at timestamptz;
                event_replayed boolean;
                persisted_agenda text[];
            BEGIN
                IF cardinality(COALESCE(requested_agenda_parts, ARRAY[]::text[])) > 100 THEN
                    RAISE EXCEPTION USING
                        ERRCODE='23514',
                        CONSTRAINT='ck_event_agenda_part_position',
                        MESSAGE='Event Agenda rejected',
                        DETAIL='an Event may contain at most 100 Agenda parts';
                END IF;

                FOREACH candidate_part IN ARRAY COALESCE(
                    requested_agenda_parts,
                    ARRAY[]::text[]
                ) LOOP
                    IF candidate_part IS NULL
                       OR btrim(candidate_part) = ''
                       OR char_length(btrim(candidate_part)) > 1000 THEN
                        RAISE EXCEPTION USING
                            ERRCODE='23514',
                            CONSTRAINT='ck_event_agenda_part_content',
                            MESSAGE='Event Agenda part rejected',
                            DETAIL='Agenda parts must contain 1 to 1000 non-padding characters';
                    END IF;
                    normalized_agenda := array_append(
                        normalized_agenda,
                        btrim(candidate_part)
                    );
                END LOOP;

                SELECT created.event_ref,
                       created.title,
                       created.created_at,
                       created.replayed
                  INTO created_event_ref,
                       created_title,
                       event_created_at,
                       event_replayed
                  FROM dante.create_self_event(
                        requested_self_person_ref,
                        requested_operation_id,
                        requested_intent_fingerprint,
                        requested_event_ref,
                        requested_title
                  ) AS created;

                IF event_replayed THEN
                    SELECT COALESCE(
                               array_agg(part.content ORDER BY part.position),
                               ARRAY[]::text[]
                           )
                      INTO persisted_agenda
                      FROM dante.event_agenda_part AS part
                     WHERE part.event_ref = created_event_ref;

                    IF persisted_agenda IS DISTINCT FROM normalized_agenda THEN
                        RAISE EXCEPTION USING
                            ERRCODE='XX001',
                            MESSAGE='Event operation receipt lost canonical Agenda',
                            DETAIL='the persisted Agenda does not match the accepted Event create intent';
                    END IF;
                ELSE
                    INSERT INTO dante.event_agenda_part(event_ref, position, content)
                    SELECT created_event_ref,
                           agenda.ordinality::integer,
                           agenda.content
                      FROM unnest(normalized_agenda)
                           WITH ORDINALITY AS agenda(content, ordinality);
                END IF;

                RETURN QUERY
                SELECT created_event_ref,
                       created_title,
                       event_created_at,
                       normalized_agenda,
                       event_replayed;
            END;
            $function$
            """
        )
    )
    op.execute(
        sa.text(
            "ALTER FUNCTION dante.create_self_event_with_agenda(uuid,text,text,uuid,text,text[]) "
            f"OWNER TO {_OWNER}"
        )
    )

    op.execute(
        sa.text(
            "REVOKE ALL PRIVILEGES ON TABLE dante.event_agenda_part "
            f"FROM PUBLIC, {_RUNTIME}, {_MIGRATOR}"
        )
    )
    op.execute(sa.text("GRANT SELECT ON TABLE dante.event_agenda_part TO dante_runtime"))
    op.execute(
        sa.text(
            "REVOKE ALL PRIVILEGES ON FUNCTION "
            "dante.create_self_event_with_agenda(uuid,text,text,uuid,text,text[]) "
            f"FROM PUBLIC, {_RUNTIME}, {_MIGRATOR}"
        )
    )
    op.execute(
        sa.text(
            "GRANT EXECUTE ON FUNCTION "
            "dante.create_self_event_with_agenda(uuid,text,text,uuid,text,text[]) "
            f"TO {_RUNTIME}"
        )
    )


def downgrade() -> None:
    """Remove B03-D only when no durable Agenda data would be discarded."""
    op.execute(
        sa.text(
            r"""
            DO $block$
            BEGIN
                IF EXISTS (SELECT 1 FROM dante.event_agenda_part) THEN
                    RAISE EXCEPTION USING
                        ERRCODE='55000',
                        MESSAGE='B03-D downgrade refused',
                        DETAIL='Event Agenda parts are canonical product data; use a separately reviewed forward migration instead of discarding them';
                END IF;
            END;
            $block$
            """
        )
    )
    op.execute(
        sa.text(
            "REVOKE ALL PRIVILEGES ON FUNCTION "
            "dante.create_self_event_with_agenda(uuid,text,text,uuid,text,text[]) "
            f"FROM PUBLIC, {_RUNTIME}, {_MIGRATOR}"
        )
    )
    op.execute(
        sa.text(
            "DROP FUNCTION dante.create_self_event_with_agenda(uuid,text,text,uuid,text,text[])"
        )
    )
    op.drop_table("event_agenda_part", schema=_SCHEMA)
