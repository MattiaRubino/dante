"""B05-A1: self-scoped LR-12 Life Area create/list, without a Domain owner.

Revision ID: 20260920_43
Revises: 20260920_42
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "20260920_43"
down_revision: str | None = "20260920_42"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_OWNER = "dante_owner"
_RUNTIME = "dante_runtime"
_MIGRATOR = "dante_migrator"
_CREATE = "dante.create_self_life_area(uuid,text,text,uuid,text)"
_LIST = "dante.list_self_life_areas(uuid)"


def upgrade() -> None:
    """Create an independent product-profile address, not a NativeRef."""
    op.create_table(
        "life_area",
        sa.Column("life_area_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("self_person_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("life_area_ref", name=op.f("pk_life_area")),
        sa.ForeignKeyConstraint(
            ["self_person_ref"],
            ["dante.person.person_ref"],
            name="fk_life_area_self_person_ref_person",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        sa.CheckConstraint(
            "uuid_extract_version(life_area_ref) IS NOT DISTINCT FROM 7",
            name=op.f("ck_life_area_uuidv7"),
        ),
        sa.CheckConstraint(
            "name=btrim(name) AND name<>'' AND char_length(name)<=100",
            name=op.f("ck_life_area_name"),
        ),
        schema="dante",
    )
    op.create_index(
        "ix_life_area_self_person_created",
        "life_area",
        ["self_person_ref", "created_at", "life_area_ref"],
        schema="dante",
    )
    op.create_table(
        "life_area_create_operation",
        sa.Column("self_person_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("operation_id", sa.Text(), nullable=False),
        sa.Column("intent_fingerprint", sa.Text(), nullable=False),
        sa.Column("life_area_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint(
            "self_person_ref", "operation_id", name=op.f("pk_life_area_create_operation")
        ),
        sa.UniqueConstraint(
            "life_area_ref", name=op.f("uq_life_area_create_operation_life_area_ref")
        ),
        sa.ForeignKeyConstraint(
            ["self_person_ref"],
            ["dante.person.person_ref"],
            name="fk_life_area_create_operation_self_person_ref_person",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        sa.ForeignKeyConstraint(
            ["life_area_ref"],
            ["dante.life_area.life_area_ref"],
            name="fk_life_area_create_operation_life_area_ref_life_area",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        sa.CheckConstraint(
            "operation_id=btrim(operation_id) AND operation_id<>'' "
            "AND char_length(operation_id)<=200",
            name=op.f("ck_life_area_create_operation_operation_id"),
        ),
        sa.CheckConstraint(
            "intent_fingerprint ~ '^[0-9a-f]{64}$'",
            name=op.f("ck_life_area_create_operation_fingerprint"),
        ),
        schema="dante",
    )

    op.execute(
        sa.text(r"""
        CREATE FUNCTION dante.create_self_life_area(
            requested_self_person_ref uuid,
            requested_operation_id text,
            requested_intent_fingerprint text,
            requested_life_area_ref uuid,
            requested_name text
        )
        RETURNS TABLE(life_area_ref uuid, name text, created_at timestamptz, replayed boolean)
        LANGUAGE plpgsql SECURITY DEFINER VOLATILE PARALLEL UNSAFE
        SET search_path = pg_catalog, dante, pg_temp
        AS $function$
        DECLARE
            normalized_operation_id text := btrim(requested_operation_id);
            normalized_name text := btrim(requested_name);
            existing_fingerprint text;
            existing_ref uuid;
            recorded_at timestamptz := statement_timestamp();
        BEGIN
            IF NOT EXISTS (SELECT 1 FROM dante.person WHERE person_ref=requested_self_person_ref)
               OR NOT EXISTS (
                   SELECT 1 FROM dante.account_application_context
                   WHERE self_person_ref=requested_self_person_ref
               ) THEN
                RAISE EXCEPTION USING ERRCODE='23503',
                    MESSAGE='Life Area self context rejected';
            END IF;
            IF normalized_operation_id IS NULL OR normalized_operation_id=''
               OR char_length(normalized_operation_id)>200 THEN
                RAISE EXCEPTION USING ERRCODE='23514',
                    CONSTRAINT='ck_life_area_create_operation_operation_id',
                    MESSAGE='Life Area operation id rejected';
            END IF;
            IF requested_intent_fingerprint IS NULL
               OR requested_intent_fingerprint !~ '^[0-9a-f]{64}$' THEN
                RAISE EXCEPTION USING ERRCODE='23514',
                    CONSTRAINT='ck_life_area_create_operation_fingerprint',
                    MESSAGE='Life Area fingerprint rejected';
            END IF;
            IF normalized_name IS NULL OR normalized_name=''
               OR char_length(normalized_name)>100 THEN
                RAISE EXCEPTION USING ERRCODE='23514',
                    CONSTRAINT='ck_life_area_name', MESSAGE='Life Area name rejected';
            END IF;
            IF uuid_extract_version(requested_life_area_ref) IS DISTINCT FROM 7 THEN
                RAISE EXCEPTION USING ERRCODE='23514',
                    CONSTRAINT='ck_life_area_uuidv7', MESSAGE='Life Area reference rejected';
            END IF;

            PERFORM pg_advisory_xact_lock(hashtextextended(
                'life_area:create:' || requested_self_person_ref::text || ':' || normalized_operation_id,
                0
            ));
            SELECT operation.intent_fingerprint, operation.life_area_ref
              INTO existing_fingerprint, existing_ref
              FROM dante.life_area_create_operation AS operation
             WHERE operation.self_person_ref=requested_self_person_ref
               AND operation.operation_id=normalized_operation_id;
            IF FOUND THEN
                IF existing_fingerprint<>requested_intent_fingerprint THEN
                    RAISE EXCEPTION USING ERRCODE='23505',
                        CONSTRAINT='pk_life_area_create_operation',
                        MESSAGE='Life Area operation id reused with different intent';
                END IF;
                RETURN QUERY
                SELECT area.life_area_ref, area.name, area.created_at, true
                  FROM dante.life_area AS area
                 WHERE area.life_area_ref=existing_ref
                   AND area.self_person_ref=requested_self_person_ref;
                IF NOT FOUND THEN
                    RAISE EXCEPTION USING ERRCODE='XX001',
                        MESSAGE='Life Area operation receipt lost its profile';
                END IF;
                RETURN;
            END IF;

            INSERT INTO dante.life_area(life_area_ref,self_person_ref,name,created_at)
            VALUES(requested_life_area_ref,requested_self_person_ref,normalized_name,recorded_at);
            INSERT INTO dante.life_area_create_operation(
                self_person_ref,operation_id,intent_fingerprint,life_area_ref,created_at
            ) VALUES (
                requested_self_person_ref,normalized_operation_id,requested_intent_fingerprint,
                requested_life_area_ref,recorded_at
            );
            RETURN QUERY SELECT requested_life_area_ref, normalized_name, recorded_at, false;
        END;
        $function$
    """)
    )
    op.execute(
        sa.text(r"""
        CREATE FUNCTION dante.list_self_life_areas(requested_self_person_ref uuid)
        RETURNS TABLE(life_area_ref uuid, name text, created_at timestamptz)
        LANGUAGE sql SECURITY DEFINER STABLE PARALLEL SAFE
        SET search_path = pg_catalog, dante, pg_temp
        AS $function$
            SELECT area.life_area_ref, area.name, area.created_at
              FROM dante.life_area AS area
             WHERE area.self_person_ref=requested_self_person_ref
               AND EXISTS (
                   SELECT 1 FROM dante.account_application_context
                   WHERE self_person_ref=requested_self_person_ref
               )
             ORDER BY area.created_at, area.life_area_ref;
        $function$
    """)
    )
    for signature in (_CREATE, _LIST):
        op.execute(sa.text(f"ALTER FUNCTION {signature} OWNER TO {_OWNER}"))
        op.execute(
            sa.text(
                f"REVOKE ALL PRIVILEGES ON FUNCTION {signature} FROM PUBLIC, {_RUNTIME}, {_MIGRATOR}"
            )
        )
        op.execute(sa.text(f"GRANT EXECUTE ON FUNCTION {signature} TO {_RUNTIME}"))
    for table in ("life_area", "life_area_create_operation"):
        op.execute(
            sa.text(
                f"REVOKE ALL PRIVILEGES ON TABLE dante.{table} FROM PUBLIC, {_RUNTIME}, {_MIGRATOR}"
            )
        )


def downgrade() -> None:
    """Refuse to destroy user-defined Life Areas or their creation receipts."""
    op.execute(
        sa.text(r"""
        DO $block$
        BEGIN
            IF EXISTS (SELECT 1 FROM dante.life_area)
               OR EXISTS (SELECT 1 FROM dante.life_area_create_operation) THEN
                RAISE EXCEPTION USING ERRCODE='55000',
                    MESSAGE='B05-A1 downgrade refused: Life Area product data exists';
            END IF;
        END;
        $block$
    """)
    )
    op.execute(sa.text(f"DROP FUNCTION {_LIST}"))
    op.execute(sa.text(f"DROP FUNCTION {_CREATE}"))
    op.drop_table("life_area_create_operation", schema="dante")
    op.drop_index("ix_life_area_self_person_created", table_name="life_area", schema="dante")
    op.drop_table("life_area", schema="dante")
