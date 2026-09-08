"""Materialize the minimum B01 Activity persistence and idempotent create boundary.

Revision ID: 20260908_19
Revises: 20260906_18
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "20260908_19"
down_revision: str | None = "20260906_18"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_SCHEMA = "dante"
_OWNER = "dante_owner"
_MIGRATOR = "dante_migrator"
_RUNTIME = "dante_runtime"


def upgrade() -> None:
    """Create one typed personal Activity descriptor and a guarded create receipt."""
    op.create_table(
        "activity_intention",
        sa.Column("activity_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("self_person_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("title", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("activity_ref", name=op.f("pk_activity_intention")),
        sa.ForeignKeyConstraint(
            ["activity_ref"],
            [f"{_SCHEMA}.activity.activity_ref"],
            name="fk_activity_intention_activity_ref_activity",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        sa.ForeignKeyConstraint(
            ["self_person_ref"],
            [f"{_SCHEMA}.person.person_ref"],
            name="fk_activity_intention_self_person_ref_person",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        sa.CheckConstraint(
            "title=btrim(title) AND title<>'' AND char_length(title)<=300",
            name=op.f("ck_activity_intention_title"),
        ),
        schema=_SCHEMA,
    )
    op.create_index(
        "ix_activity_intention_self_person_created",
        "activity_intention",
        ["self_person_ref", "created_at", "activity_ref"],
        unique=False,
        schema=_SCHEMA,
    )

    op.create_table(
        "activity_create_operation",
        sa.Column("self_person_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("operation_id", sa.Text(), nullable=False),
        sa.Column("intent_fingerprint", sa.Text(), nullable=False),
        sa.Column("activity_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint(
            "self_person_ref",
            "operation_id",
            name=op.f("pk_activity_create_operation"),
        ),
        sa.UniqueConstraint(
            "activity_ref",
            name=op.f("uq_activity_create_operation_activity_ref"),
        ),
        sa.ForeignKeyConstraint(
            ["self_person_ref"],
            [f"{_SCHEMA}.person.person_ref"],
            name="fk_activity_create_operation_self_person_ref_person",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        sa.ForeignKeyConstraint(
            ["activity_ref"],
            [f"{_SCHEMA}.activity.activity_ref"],
            name="fk_activity_create_operation_activity_ref_activity",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        sa.CheckConstraint(
            "operation_id=btrim(operation_id) AND operation_id<>'' "
            "AND char_length(operation_id)<=200",
            name=op.f("ck_activity_create_operation_operation_id"),
        ),
        sa.CheckConstraint(
            "intent_fingerprint ~ '^[0-9a-f]{64}$'",
            name=op.f("ck_activity_create_operation_fingerprint"),
        ),
        schema=_SCHEMA,
    )

    op.execute(
        sa.text(
            r"""
            CREATE FUNCTION dante.create_self_activity(
                requested_self_person_ref uuid,
                requested_operation_id text,
                requested_intent_fingerprint text,
                requested_activity_ref uuid,
                requested_title text
            )
            RETURNS TABLE(
                activity_ref uuid,
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
                existing_activity_ref uuid;
                recorded_at timestamptz := statement_timestamp();
            BEGIN
                IF NOT EXISTS (
                    SELECT 1 FROM dante.person
                    WHERE person_ref = requested_self_person_ref
                ) THEN
                    RAISE EXCEPTION USING
                        ERRCODE='23503',
                        MESSAGE='Activity self context rejected',
                        DETAIL='the authenticated self Person does not exist';
                END IF;

                IF normalized_operation_id = '' OR char_length(normalized_operation_id) > 200 THEN
                    RAISE EXCEPTION USING
                        ERRCODE='23514',
                        CONSTRAINT='ck_activity_create_operation_operation_id',
                        MESSAGE='Activity operation id rejected';
                END IF;
                IF requested_intent_fingerprint !~ '^[0-9a-f]{64}$' THEN
                    RAISE EXCEPTION USING
                        ERRCODE='23514',
                        CONSTRAINT='ck_activity_create_operation_fingerprint',
                        MESSAGE='Activity operation fingerprint rejected';
                END IF;
                IF normalized_title = '' OR char_length(normalized_title) > 300 THEN
                    RAISE EXCEPTION USING
                        ERRCODE='23514',
                        CONSTRAINT='ck_activity_intention_title',
                        MESSAGE='Activity title rejected';
                END IF;
                IF uuid_extract_version(requested_activity_ref) IS DISTINCT FROM 7 THEN
                    RAISE EXCEPTION USING
                        ERRCODE='23514',
                        MESSAGE='Activity reference rejected',
                        DETAIL='Activity NativeRef must be an application-issued UUIDv7';
                END IF;

                PERFORM pg_advisory_xact_lock(
                    hashtextextended(
                        requested_self_person_ref::text || ':' || normalized_operation_id,
                        0
                    )
                );

                SELECT operation.intent_fingerprint, operation.activity_ref
                  INTO existing_fingerprint, existing_activity_ref
                  FROM dante.activity_create_operation AS operation
                 WHERE operation.self_person_ref = requested_self_person_ref
                   AND operation.operation_id = normalized_operation_id;

                IF FOUND THEN
                    IF existing_fingerprint <> requested_intent_fingerprint THEN
                        RAISE EXCEPTION USING
                            ERRCODE='23505',
                            CONSTRAINT='pk_activity_create_operation',
                            MESSAGE='Activity operation id reused with different intent';
                    END IF;

                    RETURN QUERY
                    SELECT intention.activity_ref,
                           intention.title,
                           intention.created_at,
                           true
                      FROM dante.activity_intention AS intention
                     WHERE intention.activity_ref = existing_activity_ref
                       AND intention.self_person_ref = requested_self_person_ref;
                    IF NOT FOUND THEN
                        RAISE EXCEPTION USING
                            ERRCODE='XX001',
                            MESSAGE='Activity operation receipt lost canonical Activity';
                    END IF;
                    RETURN;
                END IF;

                INSERT INTO dante.activity(activity_ref)
                VALUES (requested_activity_ref);

                INSERT INTO dante.native_address(native_ref, owner_family)
                VALUES (requested_activity_ref, 'activity');

                INSERT INTO dante.activity_intention(
                    activity_ref,
                    self_person_ref,
                    title,
                    created_at
                ) VALUES (
                    requested_activity_ref,
                    requested_self_person_ref,
                    normalized_title,
                    recorded_at
                );

                INSERT INTO dante.activity_create_operation(
                    self_person_ref,
                    operation_id,
                    intent_fingerprint,
                    activity_ref,
                    created_at
                ) VALUES (
                    requested_self_person_ref,
                    normalized_operation_id,
                    requested_intent_fingerprint,
                    requested_activity_ref,
                    recorded_at
                );

                RETURN QUERY
                SELECT requested_activity_ref,
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
            "ALTER FUNCTION dante.create_self_activity(uuid,text,text,uuid,text) "
            f"OWNER TO {_OWNER}"
        )
    )

    for table in ("activity_intention", "activity_create_operation"):
        op.execute(
            sa.text(
                f"REVOKE ALL PRIVILEGES ON TABLE dante.{table} "
                f"FROM PUBLIC, {_RUNTIME}, {_MIGRATOR}"
            )
        )
    op.execute(sa.text(f"GRANT SELECT ON TABLE dante.activity_intention TO {_RUNTIME}"))
    op.execute(
        sa.text(
            "REVOKE ALL PRIVILEGES ON FUNCTION "
            "dante.create_self_activity(uuid,text,text,uuid,text) "
            f"FROM PUBLIC, {_RUNTIME}, {_MIGRATOR}"
        )
    )
    op.execute(
        sa.text(
            "GRANT EXECUTE ON FUNCTION dante.create_self_activity(uuid,text,text,uuid,text) "
            f"TO {_RUNTIME}"
        )
    )


def downgrade() -> None:
    """Remove B01 only when no canonical Activity was created through this slice."""
    op.execute(
        sa.text(
            r"""
            DO $block$
            BEGIN
                IF EXISTS (SELECT 1 FROM dante.activity_intention) THEN
                    RAISE EXCEPTION USING
                        ERRCODE='55000',
                        MESSAGE='B01 downgrade refused',
                        DETAIL='Activity intentions are canonical product data; use a separately reviewed forward migration instead of discarding them';
                END IF;
            END;
            $block$
            """
        )
    )
    op.execute(
        sa.text(
            "REVOKE ALL PRIVILEGES ON FUNCTION "
            "dante.create_self_activity(uuid,text,text,uuid,text) "
            f"FROM PUBLIC, {_RUNTIME}, {_MIGRATOR}"
        )
    )
    op.execute(sa.text("DROP FUNCTION dante.create_self_activity(uuid,text,text,uuid,text)"))
    op.drop_table("activity_create_operation", schema=_SCHEMA)
    op.drop_index(
        "ix_activity_intention_self_person_created",
        table_name="activity_intention",
        schema=_SCHEMA,
    )
    op.drop_table("activity_intention", schema=_SCHEMA)
