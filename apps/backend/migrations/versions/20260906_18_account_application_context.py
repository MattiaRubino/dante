"""Materialize the bounded authenticated DANTE application context.

Revision ID: 20260906_18
Revises: 20260904_17
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "20260906_18"
down_revision: str | None = "20260904_17"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_SCHEMA = "dante"
_OWNER = "dante_owner"
_MIGRATOR = "dante_migrator"
_RUNTIME = "dante_runtime"


def upgrade() -> None:
    """Create Account→DANTE self-context persistence and narrow bootstrap capability."""
    op.create_table(
        "account_application_context",
        sa.Column("account_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("self_person_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("timezone_mode", sa.Text(), nullable=False),
        sa.Column("fixed_zone_id", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("account_ref", name=op.f("pk_account_application_context")),
        sa.ForeignKeyConstraint(
            ["account_ref"],
            [f"{_SCHEMA}.account.account_ref"],
            name="fk_account_application_context_account_ref_account",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        sa.ForeignKeyConstraint(
            ["self_person_ref"],
            [f"{_SCHEMA}.person.person_ref"],
            name="fk_account_application_context_self_person_ref_person",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        sa.CheckConstraint(
            "timezone_mode IN ('follow_device','fixed')",
            name=op.f("ck_account_application_context_timezone_mode"),
        ),
        sa.CheckConstraint(
            "(timezone_mode='follow_device' AND fixed_zone_id IS NULL) OR "
            "(timezone_mode='fixed' AND fixed_zone_id IS NOT NULL "
            "AND fixed_zone_id=btrim(fixed_zone_id) AND fixed_zone_id<>'' "
            "AND char_length(fixed_zone_id)<=255 "
            "AND fixed_zone_id !~ '^[+-]([0-9]{2}|[0-9]{4}|[0-9]{2}:[0-9]{2})$')",
            name=op.f("ck_account_application_context_timezone_policy"),
        ),
        schema=_SCHEMA,
    )

    op.execute(
        sa.text(
            r"""
            CREATE FUNCTION dante.validate_account_application_timezone()
            RETURNS trigger
            LANGUAGE plpgsql
            SECURITY INVOKER
            VOLATILE
            PARALLEL UNSAFE
            SET search_path = pg_catalog, dante, pg_temp
            AS $function$
            BEGIN
                IF NEW.timezone_mode = 'fixed' AND NOT EXISTS (
                    SELECT 1 FROM pg_catalog.pg_timezone_names
                    WHERE name = NEW.fixed_zone_id
                ) THEN
                    RAISE EXCEPTION USING
                        ERRCODE='23514',
                        CONSTRAINT='ck_account_application_context_timezone_policy',
                        TABLE=TG_TABLE_NAME,
                        SCHEMA=TG_TABLE_SCHEMA,
                        MESSAGE='Account application timezone rejected',
                        DETAIL='fixed timezone policy requires a runtime-available named IANA timezone';
                END IF;
                RETURN NEW;
            END;
            $function$
            """
        )
    )
    op.execute(sa.text(f"ALTER FUNCTION dante.validate_account_application_timezone() OWNER TO {_OWNER}"))
    op.execute(
        sa.text(
            "REVOKE ALL PRIVILEGES ON FUNCTION dante.validate_account_application_timezone() "
            f"FROM PUBLIC, {_RUNTIME}, {_MIGRATOR}"
        )
    )
    op.execute(
        sa.text(
            "CREATE TRIGGER trg_account_application_context_timezone "
            "BEFORE INSERT OR UPDATE OF timezone_mode, fixed_zone_id "
            "ON dante.account_application_context "
            "FOR EACH ROW EXECUTE FUNCTION dante.validate_account_application_timezone()"
        )
    )

    op.execute(
        sa.text(
            r"""
            CREATE FUNCTION dante.ensure_account_application_context(
                requested_account_ref uuid,
                requested_self_person_ref uuid
            )
            RETURNS TABLE(
                account_ref uuid,
                self_person_ref uuid,
                timezone_mode text,
                fixed_zone_id text
            )
            LANGUAGE plpgsql
            SECURITY DEFINER
            VOLATILE
            PARALLEL UNSAFE
            SET search_path = pg_catalog, dante, pg_temp
            AS $function$
            DECLARE
                account_status text;
            BEGIN
                SELECT a.status_code
                  INTO account_status
                  FROM dante.account AS a
                 WHERE a.account_ref = requested_account_ref
                 FOR UPDATE;

                IF NOT FOUND THEN
                    RAISE EXCEPTION USING ERRCODE='23503',
                        MESSAGE='Account application context account rejected',
                        DETAIL='the requested Account does not exist';
                END IF;
                IF account_status <> 'active' THEN
                    RAISE EXCEPTION USING ERRCODE='23514',
                        MESSAGE='Account application context account rejected',
                        DETAIL='only an active Account may own an application context';
                END IF;

                RETURN QUERY
                SELECT c.account_ref, c.self_person_ref, c.timezone_mode, c.fixed_zone_id
                  FROM dante.account_application_context AS c
                 WHERE c.account_ref = requested_account_ref;
                IF FOUND THEN
                    RETURN;
                END IF;

                IF uuid_extract_version(requested_self_person_ref) IS DISTINCT FROM 7 THEN
                    RAISE EXCEPTION USING ERRCODE='23514',
                        MESSAGE='Account application context Person reference rejected',
                        DETAIL='self Person must use an application-issued UUIDv7 NativeRef';
                END IF;

                INSERT INTO dante.person(person_ref)
                VALUES (requested_self_person_ref);

                INSERT INTO dante.native_address(native_ref, owner_family)
                VALUES (requested_self_person_ref, 'person');

                INSERT INTO dante.account_application_context(
                    account_ref,
                    self_person_ref,
                    timezone_mode,
                    fixed_zone_id
                ) VALUES (
                    requested_account_ref,
                    requested_self_person_ref,
                    'follow_device',
                    NULL
                );

                RETURN QUERY
                SELECT c.account_ref, c.self_person_ref, c.timezone_mode, c.fixed_zone_id
                  FROM dante.account_application_context AS c
                 WHERE c.account_ref = requested_account_ref;
            END;
            $function$
            """
        )
    )
    op.execute(
        sa.text(
            f"ALTER FUNCTION dante.ensure_account_application_context(uuid,uuid) OWNER TO {_OWNER}"
        )
    )

    op.execute(
        sa.text(
            f"REVOKE ALL PRIVILEGES ON TABLE dante.account_application_context "
            f"FROM PUBLIC, {_RUNTIME}, {_MIGRATOR}"
        )
    )
    op.execute(
        sa.text(f"GRANT SELECT ON TABLE dante.account_application_context TO {_RUNTIME}")
    )
    op.execute(
        sa.text(
            "REVOKE ALL PRIVILEGES ON FUNCTION dante.ensure_account_application_context(uuid,uuid) "
            f"FROM PUBLIC, {_RUNTIME}, {_MIGRATOR}"
        )
    )
    op.execute(
        sa.text(
            f"GRANT EXECUTE ON FUNCTION dante.ensure_account_application_context(uuid,uuid) "
            f"TO {_RUNTIME}"
        )
    )


def downgrade() -> None:
    """Remove PV-02 only while no persisted Account↔Person context would be orphaned."""
    op.execute(
        sa.text(
            r"""
            DO $block$
            BEGIN
                IF EXISTS (SELECT 1 FROM dante.account_application_context) THEN
                    RAISE EXCEPTION USING
                        ERRCODE='55000',
                        MESSAGE='PV-02 downgrade refused',
                        DETAIL='account_application_context contains semantic Account-to-Person bindings; use a separately reviewed forward migration instead of discarding them';
                END IF;
            END;
            $block$
            """
        )
    )
    op.execute(
        sa.text(
            "REVOKE ALL PRIVILEGES ON FUNCTION dante.ensure_account_application_context(uuid,uuid) "
            f"FROM PUBLIC, {_RUNTIME}, {_MIGRATOR}"
        )
    )
    op.execute(sa.text("DROP FUNCTION dante.ensure_account_application_context(uuid,uuid)"))
    op.execute(sa.text("DROP TRIGGER trg_account_application_context_timezone ON dante.account_application_context"))
    op.execute(
        sa.text(
            "REVOKE ALL PRIVILEGES ON FUNCTION dante.validate_account_application_timezone() "
            f"FROM PUBLIC, {_RUNTIME}, {_MIGRATOR}"
        )
    )
    op.execute(sa.text("DROP FUNCTION dante.validate_account_application_timezone()"))
    op.drop_table("account_application_context", schema=_SCHEMA)
