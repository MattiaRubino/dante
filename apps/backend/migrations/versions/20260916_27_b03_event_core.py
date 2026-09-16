"""Materialize the minimum B03-A Event expectation and idempotent create boundary.

Revision ID: 20260916_27
Revises: 20260915_26
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "20260916_27"
down_revision: str | None = "20260915_26"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_SCHEMA = "dante"
_OWNER = "dante_owner"
_MIGRATOR = "dante_migrator"
_RUNTIME = "dante_runtime"


def upgrade() -> None:
    """Create one typed personal Event expectation and guarded create receipt."""
    op.create_table(
        "event_expectation",
        sa.Column("event_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("self_person_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("title", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("event_ref", name=op.f("pk_event_expectation")),
        sa.ForeignKeyConstraint(
            ["event_ref"],
            [f"{_SCHEMA}.event.event_ref"],
            name="fk_event_expectation_event_ref_event",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        sa.ForeignKeyConstraint(
            ["self_person_ref"],
            [f"{_SCHEMA}.person.person_ref"],
            name="fk_event_expectation_self_person_ref_person",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        sa.CheckConstraint(
            "title=btrim(title) AND title<>'' AND char_length(title)<=300",
            name=op.f("ck_event_expectation_title"),
        ),
        schema=_SCHEMA,
    )
    op.create_index(
        "ix_event_expectation_self_person_created",
        "event_expectation",
        ["self_person_ref", "created_at", "event_ref"],
        unique=False,
        schema=_SCHEMA,
    )

    op.create_table(
        "event_create_operation",
        sa.Column("self_person_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("operation_id", sa.Text(), nullable=False),
        sa.Column("intent_fingerprint", sa.Text(), nullable=False),
        sa.Column("event_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint(
            "self_person_ref",
            "operation_id",
            name=op.f("pk_event_create_operation"),
        ),
        sa.UniqueConstraint(
            "event_ref",
            name=op.f("uq_event_create_operation_event_ref"),
        ),
        sa.ForeignKeyConstraint(
            ["self_person_ref"],
            [f"{_SCHEMA}.person.person_ref"],
            name="fk_event_create_operation_self_person_ref_person",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        sa.ForeignKeyConstraint(
            ["event_ref"],
            [f"{_SCHEMA}.event.event_ref"],
            name="fk_event_create_operation_event_ref_event",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        sa.CheckConstraint(
            "operation_id=btrim(operation_id) AND operation_id<>'' "
            "AND char_length(operation_id)<=200",
            name=op.f("ck_event_create_operation_operation_id"),
        ),
        sa.CheckConstraint(
            "intent_fingerprint ~ '^[0-9a-f]{64}$'",
            name=op.f("ck_event_create_operation_fingerprint"),
        ),
        schema=_SCHEMA,
    )

    op.execute(
        sa.text(
            r"""
            CREATE FUNCTION dante.create_self_event(
                requested_self_person_ref uuid,
                requested_operation_id text,
                requested_intent_fingerprint text,
                requested_event_ref uuid,
                requested_title text
            )
            RETURNS TABLE(
                event_ref uuid,
                title text,
                created_at timestamptz,
                replayed boolean
            )
            LANGUAGE plpgsql
            SECURITY DEFINER
            VOLATILE
            PARALLEL UNSAFE
            SET search_path = pg_catalog, dante, pg_temp
            AS $function$
            DECLARE
                normalized_operation_id text := btrim(requested_operation_id);
                normalized_title text := btrim(requested_title);
                existing_fingerprint text;
                existing_event_ref uuid;
                recorded_at timestamptz := statement_timestamp();
            BEGIN
                IF NOT EXISTS (
                    SELECT 1
                      FROM dante.person
                     WHERE person_ref = requested_self_person_ref
                ) THEN
                    RAISE EXCEPTION USING
                        ERRCODE='23503',
                        MESSAGE='Event self context rejected',
                        DETAIL='the authenticated self Person does not exist';
                END IF;

                IF normalized_operation_id = '' OR char_length(normalized_operation_id) > 200 THEN
                    RAISE EXCEPTION USING
                        ERRCODE='23514',
                        CONSTRAINT='ck_event_create_operation_operation_id',
                        MESSAGE='Event operation id rejected';
                END IF;
                IF requested_intent_fingerprint !~ '^[0-9a-f]{64}$' THEN
                    RAISE EXCEPTION USING
                        ERRCODE='23514',
                        CONSTRAINT='ck_event_create_operation_fingerprint',
                        MESSAGE='Event operation fingerprint rejected';
                END IF;
                IF normalized_title = '' OR char_length(normalized_title) > 300 THEN
                    RAISE EXCEPTION USING
                        ERRCODE='23514',
                        CONSTRAINT='ck_event_expectation_title',
                        MESSAGE='Event title rejected';
                END IF;
                IF uuid_extract_version(requested_event_ref) IS DISTINCT FROM 7 THEN
                    RAISE EXCEPTION USING
                        ERRCODE='23514',
                        MESSAGE='Event reference rejected',
                        DETAIL='Event NativeRef must be an application-issued UUIDv7';
                END IF;

                PERFORM pg_advisory_xact_lock(
                    hashtextextended(
                        requested_self_person_ref::text || ':' || normalized_operation_id,
                        0
                    )
                );

                SELECT operation.intent_fingerprint, operation.event_ref
                  INTO existing_fingerprint, existing_event_ref
                  FROM dante.event_create_operation AS operation
                 WHERE operation.self_person_ref = requested_self_person_ref
                   AND operation.operation_id = normalized_operation_id;

                IF FOUND THEN
                    IF existing_fingerprint <> requested_intent_fingerprint THEN
                        RAISE EXCEPTION USING
                            ERRCODE='23505',
                            CONSTRAINT='pk_event_create_operation',
                            MESSAGE='Event operation id reused with different intent';
                    END IF;

                    RETURN QUERY
                    SELECT expectation.event_ref,
                           expectation.title,
                           expectation.created_at,
                           true
                      FROM dante.event_expectation AS expectation
                     WHERE expectation.event_ref = existing_event_ref
                       AND expectation.self_person_ref = requested_self_person_ref;
                    IF NOT FOUND THEN
                        RAISE EXCEPTION USING
                            ERRCODE='XX001',
                            MESSAGE='Event operation receipt lost canonical Event';
                    END IF;
                    RETURN;
                END IF;

                INSERT INTO dante.event(event_ref)
                VALUES (requested_event_ref);

                INSERT INTO dante.native_address(native_ref, owner_family)
                VALUES (requested_event_ref, 'event');

                INSERT INTO dante.event_expectation(
                    event_ref,
                    self_person_ref,
                    title,
                    created_at
                ) VALUES (
                    requested_event_ref,
                    requested_self_person_ref,
                    normalized_title,
                    recorded_at
                );

                INSERT INTO dante.event_create_operation(
                    self_person_ref,
                    operation_id,
                    intent_fingerprint,
                    event_ref,
                    created_at
                ) VALUES (
                    requested_self_person_ref,
                    normalized_operation_id,
                    requested_intent_fingerprint,
                    requested_event_ref,
                    recorded_at
                );

                RETURN QUERY
                SELECT requested_event_ref,
                       normalized_title,
                       recorded_at,
                       false;
            END;
            $function$
            """
        )
    )
    op.execute(
        sa.text(
            f"ALTER FUNCTION dante.create_self_event(uuid,text,text,uuid,text) OWNER TO {_OWNER}"
        )
    )

    for table in ("event_expectation", "event_create_operation"):
        op.execute(
            sa.text(
                f"REVOKE ALL PRIVILEGES ON TABLE dante.{table} "
                f"FROM PUBLIC, {_RUNTIME}, {_MIGRATOR}"
            )
        )
    op.execute(sa.text(f"GRANT SELECT ON TABLE dante.event_expectation TO {_RUNTIME}"))
    op.execute(
        sa.text(
            "REVOKE ALL PRIVILEGES ON FUNCTION "
            "dante.create_self_event(uuid,text,text,uuid,text) "
            f"FROM PUBLIC, {_RUNTIME}, {_MIGRATOR}"
        )
    )
    op.execute(
        sa.text(
            "GRANT EXECUTE ON FUNCTION dante.create_self_event(uuid,text,text,uuid,text) "
            f"TO {_RUNTIME}"
        )
    )


def downgrade() -> None:
    """Remove B03-A only when no canonical Event was created through this slice."""
    op.execute(
        sa.text(
            r"""
            DO $block$
            BEGIN
                IF EXISTS (SELECT 1 FROM dante.event_expectation) THEN
                    RAISE EXCEPTION USING
                        ERRCODE='55000',
                        MESSAGE='B03-A downgrade refused',
                        DETAIL='Event expectations are canonical product data; use a separately reviewed forward migration instead of discarding them';
                END IF;
            END;
            $block$
            """
        )
    )
    op.execute(
        sa.text(
            "REVOKE ALL PRIVILEGES ON FUNCTION "
            "dante.create_self_event(uuid,text,text,uuid,text) "
            f"FROM PUBLIC, {_RUNTIME}, {_MIGRATOR}"
        )
    )
    op.execute(sa.text("DROP FUNCTION dante.create_self_event(uuid,text,text,uuid,text)"))
    op.drop_table("event_create_operation", schema=_SCHEMA)
    op.drop_index(
        "ix_event_expectation_self_person_created",
        table_name="event_expectation",
        schema=_SCHEMA,
    )
    op.drop_table("event_expectation", schema=_SCHEMA)
