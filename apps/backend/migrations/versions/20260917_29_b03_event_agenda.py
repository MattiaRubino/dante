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
    """Add ordered Event-internal Agenda values and aggregate CAS mutation control."""
    op.add_column(
        "event_create_operation",
        sa.Column(
            "accepted_agenda_parts",
            postgresql.ARRAY(sa.Text()),
            nullable=False,
            server_default=sa.text("ARRAY[]::text[]"),
        ),
        schema=_SCHEMA,
    )
    op.create_check_constraint(
        op.f("ck_event_create_operation_accepted_agenda_parts"),
        "event_create_operation",
        "cardinality(accepted_agenda_parts) <= 100",
        schema=_SCHEMA,
    )
    op.alter_column(
        "event_create_operation",
        "accepted_agenda_parts",
        server_default=None,
        schema=_SCHEMA,
    )

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

    op.create_table(
        "event_agenda_current",
        sa.Column("event_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("revision", sa.BigInteger(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("event_ref", name=op.f("pk_event_agenda_current")),
        sa.ForeignKeyConstraint(
            ["event_ref"],
            [f"{_SCHEMA}.event_expectation.event_ref"],
            name="fk_event_agenda_current_event_ref_event_expectation",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        sa.CheckConstraint(
            "revision >= 1",
            name=op.f("ck_event_agenda_current_revision"),
        ),
        schema=_SCHEMA,
    )

    op.create_table(
        "event_agenda_mutation_operation",
        sa.Column("self_person_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("operation_id", sa.Text(), nullable=False),
        sa.Column("intent_fingerprint", sa.Text(), nullable=False),
        sa.Column("event_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("expected_revision", sa.BigInteger(), nullable=False),
        sa.Column("resulting_revision", sa.BigInteger(), nullable=False),
        sa.Column(
            "accepted_agenda_parts",
            postgresql.ARRAY(sa.Text()),
            nullable=False,
        ),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint(
            "self_person_ref",
            "operation_id",
            name=op.f("pk_event_agenda_mutation_operation"),
        ),
        sa.ForeignKeyConstraint(
            ["self_person_ref"],
            [f"{_SCHEMA}.person.person_ref"],
            name="fk_event_agenda_mutation_operation_self_person_ref_person",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        sa.ForeignKeyConstraint(
            ["event_ref"],
            [f"{_SCHEMA}.event_expectation.event_ref"],
            name="fk_event_agenda_mutation_operation_event_ref_event_expectation",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        sa.CheckConstraint(
            "operation_id=btrim(operation_id) AND operation_id<>'' "
            "AND char_length(operation_id)<=200",
            name=op.f("ck_event_agenda_mutation_operation_operation_id"),
        ),
        sa.CheckConstraint(
            "intent_fingerprint ~ '^[0-9a-f]{64}$'",
            name=op.f("ck_event_agenda_mutation_operation_fingerprint"),
        ),
        sa.CheckConstraint(
            "expected_revision >= 0",
            name=op.f("ck_event_agenda_mutation_operation_expected_revision"),
        ),
        sa.CheckConstraint(
            "resulting_revision = expected_revision + 1",
            name=op.f("ck_event_agenda_mutation_operation_resulting_revision"),
        ),
        sa.CheckConstraint(
            "cardinality(accepted_agenda_parts) <= 100",
            name=op.f("ck_event_agenda_mutation_operation_accepted_agenda_parts"),
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
                agenda_revision bigint,
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
                accepted_agenda text[];
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
                    normalized_agenda := array_append(normalized_agenda, btrim(candidate_part));
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
                    SELECT operation.accepted_agenda_parts
                      INTO accepted_agenda
                      FROM dante.event_create_operation AS operation
                     WHERE operation.self_person_ref = requested_self_person_ref
                       AND operation.operation_id = btrim(requested_operation_id)
                       AND operation.event_ref = created_event_ref;
                    IF NOT FOUND THEN
                        RAISE EXCEPTION USING
                            ERRCODE='XX001',
                            MESSAGE='Event operation receipt lost canonical Agenda snapshot';
                    END IF;
                ELSE
                    INSERT INTO dante.event_agenda_part(event_ref, position, content)
                    SELECT created_event_ref,
                           agenda.ordinality::integer,
                           agenda.content
                      FROM unnest(normalized_agenda)
                           WITH ORDINALITY AS agenda(content, ordinality);

                    UPDATE dante.event_create_operation AS operation
                       SET accepted_agenda_parts = normalized_agenda
                     WHERE operation.self_person_ref = requested_self_person_ref
                       AND operation.operation_id = btrim(requested_operation_id)
                       AND operation.event_ref = created_event_ref;
                    IF NOT FOUND THEN
                        RAISE EXCEPTION USING
                            ERRCODE='XX001',
                            MESSAGE='Event operation receipt unavailable for canonical Agenda snapshot';
                    END IF;
                    accepted_agenda := normalized_agenda;
                END IF;

                RETURN QUERY
                SELECT created_event_ref,
                       created_title,
                       event_created_at,
                       0::bigint,
                       accepted_agenda,
                       event_replayed;
            END;
            $function$
            """
        )
    )

    op.execute(
        sa.text(
            r"""
            CREATE FUNCTION dante.replace_self_event_agenda(
                requested_self_person_ref uuid,
                requested_operation_id text,
                requested_intent_fingerprint text,
                requested_event_ref uuid,
                requested_expected_revision bigint,
                requested_agenda_parts text[]
            )
            RETURNS TABLE(
                event_ref uuid,
                agenda_revision bigint,
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
                normalized_operation_id text := btrim(requested_operation_id);
                normalized_agenda text[] := ARRAY[]::text[];
                candidate_part text;
                existing_fingerprint text;
                existing_event_ref uuid;
                existing_expected_revision bigint;
                existing_resulting_revision bigint;
                existing_agenda text[];
                current_revision bigint;
                next_revision bigint;
                recorded_at timestamptz := statement_timestamp();
            BEGIN
                IF normalized_operation_id = '' OR char_length(normalized_operation_id) > 200 THEN
                    RAISE EXCEPTION USING
                        ERRCODE='23514',
                        CONSTRAINT='ck_event_agenda_mutation_operation_operation_id',
                        MESSAGE='Event Agenda operation id rejected';
                END IF;
                IF requested_intent_fingerprint !~ '^[0-9a-f]{64}$' THEN
                    RAISE EXCEPTION USING
                        ERRCODE='23514',
                        CONSTRAINT='ck_event_agenda_mutation_operation_fingerprint',
                        MESSAGE='Event Agenda operation fingerprint rejected';
                END IF;
                IF requested_expected_revision < 0 THEN
                    RAISE EXCEPTION USING
                        ERRCODE='23514',
                        CONSTRAINT='ck_event_agenda_mutation_operation_expected_revision',
                        MESSAGE='Event Agenda expected revision rejected';
                END IF;
                IF cardinality(COALESCE(requested_agenda_parts, ARRAY[]::text[])) > 100 THEN
                    RAISE EXCEPTION USING
                        ERRCODE='23514',
                        CONSTRAINT='ck_event_agenda_mutation_operation_accepted_agenda_parts',
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
                    normalized_agenda := array_append(normalized_agenda, btrim(candidate_part));
                END LOOP;

                IF NOT EXISTS (
                    SELECT 1
                      FROM dante.event_expectation AS expectation
                     WHERE expectation.event_ref = requested_event_ref
                       AND expectation.self_person_ref = requested_self_person_ref
                ) THEN
                    RAISE EXCEPTION USING
                        ERRCODE='23503',
                        CONSTRAINT='fk_event_agenda_mutation_operation_event_ref_event_expectation',
                        MESSAGE='Event Agenda self context rejected';
                END IF;

                PERFORM pg_advisory_xact_lock(
                    hashtextextended(
                        requested_self_person_ref::text || ':' || normalized_operation_id,
                        0
                    )
                );
                PERFORM pg_advisory_xact_lock(
                    hashtextextended('event-agenda:' || requested_event_ref::text, 0)
                );

                SELECT operation.intent_fingerprint,
                       operation.event_ref,
                       operation.expected_revision,
                       operation.resulting_revision,
                       operation.accepted_agenda_parts
                  INTO existing_fingerprint,
                       existing_event_ref,
                       existing_expected_revision,
                       existing_resulting_revision,
                       existing_agenda
                  FROM dante.event_agenda_mutation_operation AS operation
                 WHERE operation.self_person_ref = requested_self_person_ref
                   AND operation.operation_id = normalized_operation_id;

                IF FOUND THEN
                    IF existing_fingerprint <> requested_intent_fingerprint
                       OR existing_event_ref <> requested_event_ref
                       OR existing_expected_revision <> requested_expected_revision THEN
                        RAISE EXCEPTION USING
                            ERRCODE='23505',
                            CONSTRAINT='pk_event_agenda_mutation_operation',
                            MESSAGE='Event Agenda operation id reused with different intent';
                    END IF;
                    RETURN QUERY
                    SELECT existing_event_ref,
                           existing_resulting_revision,
                           existing_agenda,
                           true;
                    RETURN;
                END IF;

                SELECT current.revision
                  INTO current_revision
                  FROM dante.event_agenda_current AS current
                 WHERE current.event_ref = requested_event_ref;
                IF NOT FOUND THEN
                    current_revision := 0;
                END IF;

                IF current_revision <> requested_expected_revision THEN
                    RAISE EXCEPTION USING
                        ERRCODE='23505',
                        CONSTRAINT='event_agenda_revision_conflict',
                        MESSAGE='Event Agenda revision conflict',
                        DETAIL='expected revision does not match current Agenda revision';
                END IF;

                DELETE FROM dante.event_agenda_part AS part
                 WHERE part.event_ref = requested_event_ref;

                INSERT INTO dante.event_agenda_part(event_ref, position, content)
                SELECT requested_event_ref,
                       agenda.ordinality::integer,
                       agenda.content
                  FROM unnest(normalized_agenda)
                       WITH ORDINALITY AS agenda(content, ordinality);

                next_revision := current_revision + 1;
                INSERT INTO dante.event_agenda_current(event_ref, revision, updated_at)
                VALUES (requested_event_ref, next_revision, recorded_at)
                ON CONFLICT (event_ref) DO UPDATE
                    SET revision = EXCLUDED.revision,
                        updated_at = EXCLUDED.updated_at;

                INSERT INTO dante.event_agenda_mutation_operation(
                    self_person_ref,
                    operation_id,
                    intent_fingerprint,
                    event_ref,
                    expected_revision,
                    resulting_revision,
                    accepted_agenda_parts,
                    created_at
                ) VALUES (
                    requested_self_person_ref,
                    normalized_operation_id,
                    requested_intent_fingerprint,
                    requested_event_ref,
                    requested_expected_revision,
                    next_revision,
                    normalized_agenda,
                    recorded_at
                );

                RETURN QUERY
                SELECT requested_event_ref,
                       next_revision,
                       normalized_agenda,
                       false;
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
            "ALTER FUNCTION dante.replace_self_event_agenda(uuid,text,text,uuid,bigint,text[]) "
            f"OWNER TO {_OWNER}"
        )
    )

    for table in (
        "event_agenda_part",
        "event_agenda_current",
        "event_agenda_mutation_operation",
    ):
        op.execute(
            sa.text(
                f"REVOKE ALL PRIVILEGES ON TABLE dante.{table} "
                f"FROM PUBLIC, {_RUNTIME}, {_MIGRATOR}"
            )
        )
    op.execute(sa.text("GRANT SELECT ON TABLE dante.event_agenda_part TO dante_runtime"))
    op.execute(sa.text("GRANT SELECT ON TABLE dante.event_agenda_current TO dante_runtime"))

    for signature in (
        "dante.create_self_event_with_agenda(uuid,text,text,uuid,text,text[])",
        "dante.replace_self_event_agenda(uuid,text,text,uuid,bigint,text[])",
    ):
        op.execute(
            sa.text(
                f"REVOKE ALL PRIVILEGES ON FUNCTION {signature} "
                f"FROM PUBLIC, {_RUNTIME}, {_MIGRATOR}"
            )
        )
        op.execute(sa.text(f"GRANT EXECUTE ON FUNCTION {signature} TO {_RUNTIME}"))


def downgrade() -> None:
    """Remove B03-D only when no durable Agenda truth or mutation history would be lost."""
    op.execute(
        sa.text(
            r"""
            DO $block$
            BEGIN
                IF EXISTS (SELECT 1 FROM dante.event_agenda_part)
                   OR EXISTS (SELECT 1 FROM dante.event_agenda_current)
                   OR EXISTS (SELECT 1 FROM dante.event_agenda_mutation_operation) THEN
                    RAISE EXCEPTION USING
                        ERRCODE='55000',
                        MESSAGE='B03-D downgrade refused',
                        DETAIL='Event Agenda state is canonical product/control data; use a separately reviewed forward migration instead of discarding it';
                END IF;
            END;
            $block$
            """
        )
    )

    for signature in (
        "dante.replace_self_event_agenda(uuid,text,text,uuid,bigint,text[])",
        "dante.create_self_event_with_agenda(uuid,text,text,uuid,text,text[])",
    ):
        op.execute(
            sa.text(
                f"REVOKE ALL PRIVILEGES ON FUNCTION {signature} "
                f"FROM PUBLIC, {_RUNTIME}, {_MIGRATOR}"
            )
        )
        op.execute(sa.text(f"DROP FUNCTION {signature}"))

    op.drop_table("event_agenda_mutation_operation", schema=_SCHEMA)
    op.drop_table("event_agenda_current", schema=_SCHEMA)
    op.drop_table("event_agenda_part", schema=_SCHEMA)
    op.drop_constraint(
        op.f("ck_event_create_operation_accepted_agenda_parts"),
        "event_create_operation",
        schema=_SCHEMA,
        type_="check",
    )
    op.drop_column(
        "event_create_operation",
        "accepted_agenda_parts",
        schema=_SCHEMA,
    )
