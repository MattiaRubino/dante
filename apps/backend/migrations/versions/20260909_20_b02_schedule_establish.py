"""Establish the first B02 accepted Schedule operation over CP6 material state.

Revision ID: 20260909_20
Revises: 20260908_19
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "20260909_20"
down_revision: str | None = "20260908_19"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_SCHEMA = "dante"
_OWNER = "dante_owner"
_MIGRATOR = "dante_migrator"
_RUNTIME = "dante_runtime"


def upgrade() -> None:
    """Add one narrow idempotent Schedule-establish capability for B02-A."""
    op.create_table(
        "schedule_establish_operation",
        sa.Column("self_person_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("operation_id", sa.Text(), nullable=False),
        sa.Column("intent_fingerprint", sa.Text(), nullable=False),
        sa.Column("subject_native_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("schedule_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("material_state_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint(
            "self_person_ref",
            "operation_id",
            name=op.f("pk_schedule_establish_operation"),
        ),
        sa.UniqueConstraint(
            "schedule_ref",
            name=op.f("uq_schedule_establish_operation_schedule_ref"),
        ),
        sa.UniqueConstraint(
            "material_state_ref",
            name=op.f("uq_schedule_establish_operation_material_state_ref"),
        ),
        sa.ForeignKeyConstraint(
            ["self_person_ref"],
            [f"{_SCHEMA}.person.person_ref"],
            name="fk_schedule_establish_operation_self_person_ref_person",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        sa.ForeignKeyConstraint(
            ["subject_native_ref"],
            [f"{_SCHEMA}.native_address.native_ref"],
            name="fk_schedule_establish_operation_subject_native_ref_native_address",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        sa.ForeignKeyConstraint(
            ["schedule_ref"],
            [f"{_SCHEMA}.schedule.schedule_ref"],
            name="fk_schedule_establish_operation_schedule_ref_schedule",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        sa.ForeignKeyConstraint(
            ["material_state_ref"],
            [f"{_SCHEMA}.schedule_placement_state.material_state_ref"],
            name="fk_schedule_establish_operation_material_state_ref_placement_state",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        sa.CheckConstraint(
            "operation_id=btrim(operation_id) AND operation_id<>'' "
            "AND char_length(operation_id)<=200",
            name=op.f("ck_schedule_establish_operation_operation_id"),
        ),
        sa.CheckConstraint(
            "intent_fingerprint ~ '^[0-9a-f]{64}$'",
            name=op.f("ck_schedule_establish_operation_fingerprint"),
        ),
        schema=_SCHEMA,
    )
    op.create_index(
        "ix_schedule_establish_operation_subject_native_ref",
        "schedule_establish_operation",
        ["subject_native_ref"],
        unique=False,
        schema=_SCHEMA,
    )

    op.execute(
        sa.text(
            r"""
            CREATE FUNCTION dante.establish_self_floating_schedule(
                requested_self_person_ref uuid,
                requested_operation_id text,
                requested_intent_fingerprint text,
                requested_subject_native_ref uuid,
                requested_schedule_ref uuid,
                requested_material_state_ref uuid,
                requested_starts_local_at timestamp without time zone,
                requested_ends_local_at timestamp without time zone
            )
            RETURNS TABLE(
                subject_native_ref uuid,
                schedule_ref uuid,
                material_state_ref uuid,
                starts_local_at timestamp without time zone,
                ends_local_at timestamp without time zone,
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
                recorded_at timestamptz := statement_timestamp();
                subject_family text;
                existing_fingerprint text;
                existing_subject_native_ref uuid;
                existing_schedule_ref uuid;
                existing_material_state_ref uuid;
                existing_created_at timestamptz;
                existing_starts_local_at timestamp without time zone;
                existing_ends_local_at timestamp without time zone;
            BEGIN
                IF normalized_operation_id = '' OR char_length(normalized_operation_id) > 200 THEN
                    RAISE EXCEPTION USING
                        ERRCODE='23514',
                        CONSTRAINT='ck_schedule_establish_operation_operation_id',
                        MESSAGE='Schedule operation id rejected';
                END IF;
                IF requested_intent_fingerprint !~ '^[0-9a-f]{64}$' THEN
                    RAISE EXCEPTION USING
                        ERRCODE='23514',
                        CONSTRAINT='ck_schedule_establish_operation_fingerprint',
                        MESSAGE='Schedule operation fingerprint rejected';
                END IF;
                IF uuid_extract_version(requested_schedule_ref) IS DISTINCT FROM 7 THEN
                    RAISE EXCEPTION USING
                        ERRCODE='23514',
                        MESSAGE='Schedule reference rejected',
                        DETAIL='Schedule ScopedRecordRef must be an application-issued UUIDv7';
                END IF;
                IF uuid_extract_version(requested_material_state_ref) IS DISTINCT FROM 7 THEN
                    RAISE EXCEPTION USING
                        ERRCODE='23514',
                        MESSAGE='Schedule placement state reference rejected',
                        DETAIL='Schedule placement MaterialStateRef must be an application-issued UUIDv7';
                END IF;
                IF requested_starts_local_at IS NULL
                   OR requested_ends_local_at IS NULL
                   OR NOT isfinite(requested_starts_local_at)
                   OR NOT isfinite(requested_ends_local_at)
                   OR requested_ends_local_at <= requested_starts_local_at THEN
                    RAISE EXCEPTION USING
                        ERRCODE='23514',
                        CONSTRAINT='ck_schedule_placement_floating_local_state_interval_order',
                        MESSAGE='Floating-local Schedule interval rejected';
                END IF;

                SELECT owner_family
                  INTO subject_family
                  FROM dante.native_address
                 WHERE native_ref = requested_subject_native_ref;
                IF subject_family IS DISTINCT FROM 'activity' THEN
                    RAISE EXCEPTION USING
                        ERRCODE='23503',
                        MESSAGE='Schedule subject rejected for B02-A',
                        DETAIL='the first activated Schedule path admits only Activity subjects';
                END IF;
                IF NOT EXISTS (
                    SELECT 1
                      FROM dante.activity_intention
                     WHERE activity_ref = requested_subject_native_ref
                       AND self_person_ref = requested_self_person_ref
                ) THEN
                    RAISE EXCEPTION USING
                        ERRCODE='23503',
                        MESSAGE='Schedule self scope rejected',
                        DETAIL='the Activity is not owned by the authenticated self Person';
                END IF;

                PERFORM pg_advisory_xact_lock(
                    hashtextextended(
                        requested_self_person_ref::text || ':' || normalized_operation_id,
                        0
                    )
                );

                SELECT operation.intent_fingerprint,
                       operation.subject_native_ref,
                       operation.schedule_ref,
                       operation.material_state_ref,
                       operation.created_at
                  INTO existing_fingerprint,
                       existing_subject_native_ref,
                       existing_schedule_ref,
                       existing_material_state_ref,
                       existing_created_at
                  FROM dante.schedule_establish_operation AS operation
                 WHERE operation.self_person_ref = requested_self_person_ref
                   AND operation.operation_id = normalized_operation_id;

                IF FOUND THEN
                    IF existing_fingerprint <> requested_intent_fingerprint
                       OR existing_subject_native_ref <> requested_subject_native_ref THEN
                        RAISE EXCEPTION USING
                            ERRCODE='23505',
                            CONSTRAINT='pk_schedule_establish_operation',
                            MESSAGE='Schedule operation id reused with different intent';
                    END IF;

                    SELECT payload.starts_local_at, payload.ends_local_at
                      INTO existing_starts_local_at, existing_ends_local_at
                      FROM dante.schedule AS schedule
                      JOIN dante.schedule_current_placement AS current
                        ON current.scoped_owner_ref = schedule.schedule_ref
                      JOIN dante.schedule_placement_state AS placement
                        ON placement.material_state_ref = current.material_state_ref
                       AND placement.schedule_ref = schedule.schedule_ref
                      JOIN dante.schedule_placement_floating_local_state AS payload
                        ON payload.material_state_ref = placement.material_state_ref
                     WHERE schedule.schedule_ref = existing_schedule_ref
                       AND schedule.subject_native_ref = existing_subject_native_ref
                       AND current.material_state_ref = existing_material_state_ref
                       AND placement.temporal_form_code = 'floating_local'
                       AND payload.extent_code = 'interval';
                    IF NOT FOUND THEN
                        RAISE EXCEPTION USING
                            ERRCODE='XX001',
                            MESSAGE='Schedule operation receipt lost canonical Schedule state';
                    END IF;
                    IF existing_starts_local_at IS DISTINCT FROM requested_starts_local_at
                       OR existing_ends_local_at IS DISTINCT FROM requested_ends_local_at THEN
                        RAISE EXCEPTION USING
                            ERRCODE='23505',
                            CONSTRAINT='pk_schedule_establish_operation',
                            MESSAGE='Schedule operation id reused with different placement';
                    END IF;

                    RETURN QUERY
                    SELECT existing_subject_native_ref,
                           existing_schedule_ref,
                           existing_material_state_ref,
                           existing_starts_local_at,
                           existing_ends_local_at,
                           existing_created_at,
                           true;
                    RETURN;
                END IF;

                INSERT INTO dante.schedule(schedule_ref, subject_native_ref)
                VALUES (requested_schedule_ref, requested_subject_native_ref);

                INSERT INTO dante.scoped_address(scoped_ref, scoped_family)
                VALUES (requested_schedule_ref, 'schedule');

                INSERT INTO dante.material_state_address(
                    material_state_ref,
                    native_owner_ref,
                    scoped_owner_ref,
                    facet_code
                ) VALUES (
                    requested_material_state_ref,
                    NULL,
                    requested_schedule_ref,
                    'schedule.placement'
                );

                INSERT INTO dante.schedule_placement_state(
                    material_state_ref,
                    schedule_ref,
                    temporal_form_code
                ) VALUES (
                    requested_material_state_ref,
                    requested_schedule_ref,
                    'floating_local'
                );

                INSERT INTO dante.schedule_placement_floating_local_state(
                    material_state_ref,
                    extent_code,
                    starts_local_at,
                    ends_local_at
                ) VALUES (
                    requested_material_state_ref,
                    'interval',
                    requested_starts_local_at,
                    requested_ends_local_at
                );

                INSERT INTO dante.scoped_current_material_state(
                    scoped_owner_ref,
                    facet_code,
                    material_state_ref
                ) VALUES (
                    requested_schedule_ref,
                    'schedule.placement',
                    requested_material_state_ref
                );

                INSERT INTO dante.schedule_placement_current_history(
                    schedule_ref,
                    material_state_ref,
                    current_from_at,
                    current_until_at
                ) VALUES (
                    requested_schedule_ref,
                    requested_material_state_ref,
                    recorded_at,
                    NULL
                );

                INSERT INTO dante.schedule_establish_operation(
                    self_person_ref,
                    operation_id,
                    intent_fingerprint,
                    subject_native_ref,
                    schedule_ref,
                    material_state_ref,
                    created_at
                ) VALUES (
                    requested_self_person_ref,
                    normalized_operation_id,
                    requested_intent_fingerprint,
                    requested_subject_native_ref,
                    requested_schedule_ref,
                    requested_material_state_ref,
                    recorded_at
                );

                RETURN QUERY
                SELECT requested_subject_native_ref,
                       requested_schedule_ref,
                       requested_material_state_ref,
                       requested_starts_local_at,
                       requested_ends_local_at,
                       recorded_at,
                       false;
            END;
            $function$
            """
        )
    )
    op.execute(
        sa.text(
            "ALTER FUNCTION dante.establish_self_floating_schedule(" 
            "uuid,text,text,uuid,uuid,uuid,timestamp without time zone,timestamp without time zone) "
            f"OWNER TO {_OWNER}"
        )
    )

    op.execute(
        sa.text(
            "REVOKE ALL PRIVILEGES ON TABLE dante.schedule_establish_operation "
            f"FROM PUBLIC, {_RUNTIME}, {_MIGRATOR}"
        )
    )
    op.execute(sa.text(f"GRANT SELECT ON TABLE dante.schedule_establish_operation TO {_RUNTIME}"))
    op.execute(
        sa.text(
            "REVOKE ALL PRIVILEGES ON FUNCTION dante.establish_self_floating_schedule(" 
            "uuid,text,text,uuid,uuid,uuid,timestamp without time zone,timestamp without time zone) "
            f"FROM PUBLIC, {_RUNTIME}, {_MIGRATOR}"
        )
    )
    op.execute(
        sa.text(
            "GRANT EXECUTE ON FUNCTION dante.establish_self_floating_schedule(" 
            "uuid,text,text,uuid,uuid,uuid,timestamp without time zone,timestamp without time zone) "
            f"TO {_RUNTIME}"
        )
    )


def downgrade() -> None:
    """Remove B02-A capability only when it has never produced canonical Schedule data."""
    op.execute(
        sa.text(
            r"""
            DO $block$
            BEGIN
                IF EXISTS (SELECT 1 FROM dante.schedule_establish_operation) THEN
                    RAISE EXCEPTION USING
                        ERRCODE='55000',
                        MESSAGE='B02-A downgrade refused',
                        DETAIL='Schedule establish receipts reference canonical Schedule history; use a separately reviewed forward migration instead of discarding them';
                END IF;
            END;
            $block$
            """
        )
    )
    op.execute(
        sa.text(
            "REVOKE ALL PRIVILEGES ON FUNCTION dante.establish_self_floating_schedule(" 
            "uuid,text,text,uuid,uuid,uuid,timestamp without time zone,timestamp without time zone) "
            f"FROM PUBLIC, {_RUNTIME}, {_MIGRATOR}"
        )
    )
    op.execute(
        sa.text(
            "DROP FUNCTION dante.establish_self_floating_schedule(" 
            "uuid,text,text,uuid,uuid,uuid,timestamp without time zone,timestamp without time zone)"
        )
    )
    op.drop_index(
        "ix_schedule_establish_operation_subject_native_ref",
        table_name="schedule_establish_operation",
        schema=_SCHEMA,
    )
    op.drop_table("schedule_establish_operation", schema=_SCHEMA)
