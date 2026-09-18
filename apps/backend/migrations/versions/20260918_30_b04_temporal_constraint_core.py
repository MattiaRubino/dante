"""Materialize the B04-A Temporal Constraint canonical core.

Revision ID: 20260918_30
Revises: 20260917_29
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "20260918_30"
down_revision: str | None = "20260917_29"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_SCHEMA = "dante"
_OWNER = "dante_owner"
_MIGRATOR = "dante_migrator"
_RUNTIME = "dante_runtime"
_MUTATE_SIGNATURE = (
    "dante.mutate_self_absolute_earliest_start_constraint("
    "uuid,text,text,text,uuid,uuid,uuid,uuid,text,timestamptz)"
)


def _execute(sql: str) -> None:
    op.execute(sa.text(sql))


def upgrade() -> None:
    """Install one complete typed Temporal Constraint path over shared CP6 controls."""
    # Extend the bounded scoped/material dispatchers. Temporal Constraint remains
    # a ScopedRecordRef family; it does not become a NativeRef root.
    op.drop_constraint(
        op.f("ck_scoped_address_scoped_family"),
        "scoped_address",
        schema=_SCHEMA,
        type_="check",
    )
    op.create_check_constraint(
        op.f("ck_scoped_address_scoped_family"),
        "scoped_address",
        "scoped_family IN ('schedule','actual','temporal_constraint')",
        schema=_SCHEMA,
    )

    op.drop_constraint(
        op.f("ck_material_state_address_facet_code"),
        "material_state_address",
        schema=_SCHEMA,
        type_="check",
    )
    op.create_check_constraint(
        op.f("ck_material_state_address_facet_code"),
        "material_state_address",
        "facet_code IN ("
        "'schedule.placement','actual.realization','session.timing',"
        "'routine.recurrence','event.recurrence','temporal_constraint.rule')",
        schema=_SCHEMA,
    )

    op.drop_constraint(
        op.f("ck_scoped_current_material_state_facet_code"),
        "scoped_current_material_state",
        schema=_SCHEMA,
        type_="check",
    )
    op.create_check_constraint(
        op.f("ck_scoped_current_material_state_facet_code"),
        "scoped_current_material_state",
        "facet_code IN ("
        "'schedule.placement','actual.realization','temporal_constraint.rule')",
        schema=_SCHEMA,
    )

    op.create_table(
        "temporal_constraint",
        sa.Column("constraint_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("subject_native_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.PrimaryKeyConstraint("constraint_ref", name=op.f("pk_temporal_constraint")),
        sa.UniqueConstraint(
            "constraint_ref",
            "subject_native_ref",
            name=op.f("uq_temporal_constraint_ref_subject"),
        ),
        sa.CheckConstraint(
            "uuid_extract_version(constraint_ref) IS NOT DISTINCT FROM 7",
            name=op.f("ck_temporal_constraint_uuidv7"),
        ),
        sa.ForeignKeyConstraint(
            ["subject_native_ref"],
            [f"{_SCHEMA}.native_address.native_ref"],
            name="fk_temporal_constraint_subject_native_ref_native_address",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        schema=_SCHEMA,
    )
    op.create_index(
        "ix_temporal_constraint_subject_native_ref",
        "temporal_constraint",
        ["subject_native_ref"],
        unique=False,
        schema=_SCHEMA,
    )

    op.create_table(
        "temporal_constraint_state",
        sa.Column("material_state_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("constraint_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("family_code", sa.Text(), nullable=False),
        sa.Column("strength_code", sa.Text(), nullable=False),
        sa.Column("constrained_facet_code", sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint(
            "material_state_ref",
            name=op.f("pk_temporal_constraint_state"),
        ),
        sa.UniqueConstraint(
            "constraint_ref",
            "material_state_ref",
            name=op.f("uq_temporal_constraint_state_constraint_material"),
        ),
        sa.ForeignKeyConstraint(
            ["material_state_ref"],
            [f"{_SCHEMA}.material_state_address.material_state_ref"],
            name="fk_temporal_constraint_state_material_state_address",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        sa.ForeignKeyConstraint(
            ["constraint_ref"],
            [f"{_SCHEMA}.temporal_constraint.constraint_ref"],
            name="fk_temporal_constraint_state_constraint_ref_temporal_constraint",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        sa.CheckConstraint(
            "family_code='boundary'",
            name=op.f("ck_temporal_constraint_state_family"),
        ),
        sa.CheckConstraint(
            "strength_code IN ('hard','soft')",
            name=op.f("ck_temporal_constraint_state_strength"),
        ),
        sa.CheckConstraint(
            "constrained_facet_code='schedule.start'",
            name=op.f("ck_temporal_constraint_state_constrained_facet"),
        ),
        schema=_SCHEMA,
    )
    op.create_index(
        "ix_temporal_constraint_state_constraint_ref",
        "temporal_constraint_state",
        ["constraint_ref"],
        unique=False,
        schema=_SCHEMA,
    )

    op.create_table(
        "temporal_constraint_boundary_state",
        sa.Column("material_state_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("boundary_kind_code", sa.Text(), nullable=False),
        sa.Column("temporal_form_code", sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint(
            "material_state_ref",
            name=op.f("pk_temporal_constraint_boundary_state"),
        ),
        sa.ForeignKeyConstraint(
            ["material_state_ref"],
            [f"{_SCHEMA}.temporal_constraint_state.material_state_ref"],
            name="fk_temporal_constraint_boundary_state_constraint_state",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        sa.CheckConstraint(
            "boundary_kind_code='earliest_start'",
            name=op.f("ck_temporal_constraint_boundary_state_kind"),
        ),
        sa.CheckConstraint(
            "temporal_form_code='absolute'",
            name=op.f("ck_temporal_constraint_boundary_state_temporal_form"),
        ),
        schema=_SCHEMA,
    )

    op.create_table(
        "temporal_constraint_boundary_absolute_state",
        sa.Column("material_state_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("boundary_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint(
            "material_state_ref",
            name=op.f("pk_temporal_constraint_boundary_absolute_state"),
        ),
        sa.ForeignKeyConstraint(
            ["material_state_ref"],
            [f"{_SCHEMA}.temporal_constraint_boundary_state.material_state_ref"],
            name="fk_temporal_constraint_boundary_absolute_state_boundary_state",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        sa.CheckConstraint(
            "isfinite(boundary_at)",
            name=op.f("ck_temporal_constraint_boundary_absolute_state_finite"),
        ),
        schema=_SCHEMA,
    )

    op.create_table(
        "temporal_constraint_current_history",
        sa.Column("constraint_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("material_state_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("current_from_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("current_until_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint(
            "constraint_ref",
            "current_from_at",
            name=op.f("pk_temporal_constraint_current_history"),
        ),
        sa.ForeignKeyConstraint(
            ["constraint_ref", "material_state_ref"],
            [
                f"{_SCHEMA}.temporal_constraint_state.constraint_ref",
                f"{_SCHEMA}.temporal_constraint_state.material_state_ref",
            ],
            name="fk_temporal_constraint_current_history_constraint_state",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        sa.CheckConstraint(
            "isfinite(current_from_at) AND (current_until_at IS NULL OR "
            "(isfinite(current_until_at) AND current_until_at > current_from_at))",
            name=op.f("ck_temporal_constraint_current_history_interval"),
        ),
        schema=_SCHEMA,
    )
    op.create_index(
        "ux_temporal_constraint_current_history_open",
        "temporal_constraint_current_history",
        ["constraint_ref"],
        unique=True,
        schema=_SCHEMA,
        postgresql_where=sa.text("current_until_at IS NULL"),
    )
    op.create_index(
        "ix_temporal_constraint_current_history_material_state_ref",
        "temporal_constraint_current_history",
        ["material_state_ref"],
        unique=False,
        schema=_SCHEMA,
    )

    op.create_table(
        "temporal_constraint_mutation_operation",
        sa.Column("self_person_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("operation_id", sa.Text(), nullable=False),
        sa.Column("intent_fingerprint", sa.Text(), nullable=False),
        sa.Column("mutation_kind", sa.Text(), nullable=False),
        sa.Column("constraint_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("subject_native_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("expected_material_state_ref", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("resulting_material_state_ref", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint(
            "self_person_ref",
            "operation_id",
            name=op.f("pk_temporal_constraint_mutation_operation"),
        ),
        sa.ForeignKeyConstraint(
            ["self_person_ref"],
            [f"{_SCHEMA}.person.person_ref"],
            name="fk_temporal_constraint_mutation_operation_self_person_person",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        sa.ForeignKeyConstraint(
            ["constraint_ref", "subject_native_ref"],
            [
                f"{_SCHEMA}.temporal_constraint.constraint_ref",
                f"{_SCHEMA}.temporal_constraint.subject_native_ref",
            ],
            name="fk_temporal_constraint_mutation_operation_constraint_subject",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        sa.ForeignKeyConstraint(
            ["constraint_ref", "expected_material_state_ref"],
            [
                f"{_SCHEMA}.temporal_constraint_state.constraint_ref",
                f"{_SCHEMA}.temporal_constraint_state.material_state_ref",
            ],
            name="fk_temporal_constraint_mutation_operation_expected_state",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        sa.ForeignKeyConstraint(
            ["constraint_ref", "resulting_material_state_ref"],
            [
                f"{_SCHEMA}.temporal_constraint_state.constraint_ref",
                f"{_SCHEMA}.temporal_constraint_state.material_state_ref",
            ],
            name="fk_temporal_constraint_mutation_operation_resulting_state",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        sa.CheckConstraint(
            "operation_id=btrim(operation_id) AND operation_id<>'' "
            "AND char_length(operation_id)<=200",
            name=op.f("ck_temporal_constraint_mutation_operation_operation_id"),
        ),
        sa.CheckConstraint(
            "intent_fingerprint ~ '^[0-9a-f]{64}$'",
            name=op.f("ck_temporal_constraint_mutation_operation_fingerprint"),
        ),
        sa.CheckConstraint(
            "mutation_kind IN ('create','revise','retire')",
            name=op.f("ck_temporal_constraint_mutation_operation_kind"),
        ),
        sa.CheckConstraint(
            "(mutation_kind='create' AND expected_material_state_ref IS NULL "
            "AND resulting_material_state_ref IS NOT NULL) OR "
            "(mutation_kind='revise' AND expected_material_state_ref IS NOT NULL "
            "AND resulting_material_state_ref IS NOT NULL) OR "
            "(mutation_kind='retire' AND expected_material_state_ref IS NOT NULL "
            "AND resulting_material_state_ref IS NULL)",
            name=op.f("ck_temporal_constraint_mutation_operation_state_shape"),
        ),
        schema=_SCHEMA,
    )
    op.create_index(
        "ix_temporal_constraint_mutation_operation_constraint_ref",
        "temporal_constraint_mutation_operation",
        ["constraint_ref"],
        unique=False,
        schema=_SCHEMA,
    )
    op.create_index(
        "ux_temporal_constraint_mutation_operation_resulting_state",
        "temporal_constraint_mutation_operation",
        ["resulting_material_state_ref"],
        unique=True,
        schema=_SCHEMA,
        postgresql_where=sa.text("resulting_material_state_ref IS NOT NULL"),
    )

    # Extend the existing bounded dispatcher routines rather than introducing a
    # second address/material-state engine.
    _execute(
        r"""
        CREATE OR REPLACE FUNCTION dante.enforce_scoped_address_owner()
        RETURNS trigger
        LANGUAGE plpgsql
        SECURITY INVOKER
        VOLATILE
        PARALLEL UNSAFE
        SET search_path = pg_catalog, dante, pg_temp
        AS $function$
        DECLARE
            owner_exists boolean := false;
        BEGIN
            CASE NEW.scoped_family
                WHEN 'schedule' THEN
                    SELECT EXISTS (SELECT 1 FROM dante.schedule WHERE schedule_ref=NEW.scoped_ref) INTO owner_exists;
                WHEN 'actual' THEN
                    SELECT EXISTS (SELECT 1 FROM dante.actual WHERE actual_ref=NEW.scoped_ref) INTO owner_exists;
                WHEN 'temporal_constraint' THEN
                    SELECT EXISTS (SELECT 1 FROM dante.temporal_constraint WHERE constraint_ref=NEW.scoped_ref) INTO owner_exists;
                ELSE owner_exists := false;
            END CASE;
            IF NOT owner_exists THEN
                RAISE EXCEPTION USING ERRCODE='23503', CONSTRAINT=TG_NAME, TABLE=TG_TABLE_NAME, SCHEMA=TG_TABLE_SCHEMA,
                    MESSAGE='scoped address owner binding rejected', DETAIL='scoped address must resolve to the declared bounded owner family';
            END IF;
            RETURN NEW;
        END;
        $function$
        """
    )

    _execute(
        r"""
        CREATE OR REPLACE FUNCTION dante.enforce_native_ref_eligibility()
        RETURNS trigger
        LANGUAGE plpgsql
        SECURITY INVOKER
        VOLATILE
        PARALLEL UNSAFE
        SET search_path = pg_catalog, dante, pg_temp
        AS $function$
        DECLARE
            ref_value uuid;
            family text;
            admitted boolean := false;
        BEGIN
            IF TG_TABLE_NAME='schedule' THEN
                ref_value := NEW.subject_native_ref;
            ELSIF TG_TABLE_NAME='actual' THEN
                ref_value := NEW.subject_native_ref;
            ELSIF TG_TABLE_NAME='temporal_constraint' THEN
                ref_value := NEW.subject_native_ref;
            ELSIF TG_TABLE_NAME='occurrence_generation' THEN
                ref_value := NEW.source_native_ref;
            ELSE
                RAISE EXCEPTION USING ERRCODE='23503', CONSTRAINT=TG_NAME, TABLE=TG_TABLE_NAME, SCHEMA=TG_TABLE_SCHEMA,
                    MESSAGE='native reference consumer is not in the bounded dispatcher';
            END IF;
            SELECT owner_family INTO family FROM dante.native_address WHERE native_ref=ref_value;
            IF TG_TABLE_NAME IN ('schedule','actual') THEN
                admitted := family IN ('activity','event','occurrence');
            ELSIF TG_TABLE_NAME='temporal_constraint' THEN
                admitted := family IN ('activity','event');
            ELSE
                admitted := family IN ('routine','event');
            END IF;
            IF family IS NULL OR NOT admitted THEN
                RAISE EXCEPTION USING ERRCODE='23503', CONSTRAINT=TG_NAME, TABLE=TG_TABLE_NAME, SCHEMA=TG_TABLE_SCHEMA,
                    MESSAGE='native reference family rejected', DETAIL='consumer admits only its frozen NativeRef owner families';
            END IF;
            RETURN NEW;
        END;
        $function$
        """
    )

    _execute(
        r"""
        CREATE OR REPLACE FUNCTION dante.enforce_material_state_totality()
        RETURNS trigger
        LANGUAGE plpgsql
        SECURITY INVOKER
        VOLATILE
        PARALLEL UNSAFE
        SET search_path = pg_catalog, dante, pg_temp
        AS $function$
        DECLARE
            state_ref uuid;
            a record;
            schedule_n integer;
            actual_n integer;
            session_n integer;
            routine_n integer;
            event_n integer;
            constraint_n integer := 0;
            owner_ok boolean := false;
        BEGIN
            state_ref := CASE WHEN TG_OP='DELETE' THEN OLD.material_state_ref ELSE NEW.material_state_ref END;
            SELECT material_state_ref,native_owner_ref,scoped_owner_ref,facet_code INTO a
              FROM dante.material_state_address WHERE material_state_ref=state_ref;
            IF NOT FOUND THEN
                IF TG_OP='DELETE' THEN RETURN OLD; END IF;
                RETURN NEW;
            END IF;
            SELECT (SELECT count(*) FROM dante.schedule_placement_state WHERE material_state_ref=state_ref),
                   (SELECT count(*) FROM dante.actual_realization_state WHERE material_state_ref=state_ref),
                   (SELECT count(*) FROM dante.session_timing_state WHERE material_state_ref=state_ref),
                   (SELECT count(*) FROM dante.routine_recurrence_state WHERE material_state_ref=state_ref),
                   (SELECT count(*) FROM dante.event_recurrence_state WHERE material_state_ref=state_ref)
              INTO schedule_n,actual_n,session_n,routine_n,event_n;

            IF a.facet_code='temporal_constraint.rule' THEN
                SELECT count(*) INTO constraint_n
                  FROM dante.temporal_constraint_state
                 WHERE material_state_ref=state_ref;
                SELECT EXISTS (
                    SELECT 1
                      FROM dante.temporal_constraint_state AS s
                      JOIN dante.scoped_address AS x
                        ON x.scoped_ref=a.scoped_owner_ref
                       AND x.scoped_family='temporal_constraint'
                     WHERE s.material_state_ref=state_ref
                       AND s.constraint_ref=a.scoped_owner_ref
                       AND a.native_owner_ref IS NULL
                ) INTO owner_ok;
                owner_ok := owner_ok AND constraint_n=1
                    AND schedule_n+actual_n+session_n+routine_n+event_n=0;
            ELSIF a.facet_code='schedule.placement' THEN
                SELECT EXISTS (SELECT 1 FROM dante.schedule_placement_state s JOIN dante.scoped_address x ON x.scoped_ref=a.scoped_owner_ref AND x.scoped_family='schedule' WHERE s.material_state_ref=state_ref AND s.schedule_ref=a.scoped_owner_ref AND a.native_owner_ref IS NULL) INTO owner_ok;
                owner_ok := owner_ok AND schedule_n=1 AND actual_n+session_n+routine_n+event_n=0;
            ELSIF a.facet_code='actual.realization' THEN
                SELECT EXISTS (SELECT 1 FROM dante.actual_realization_state s JOIN dante.scoped_address x ON x.scoped_ref=a.scoped_owner_ref AND x.scoped_family='actual' WHERE s.material_state_ref=state_ref AND s.actual_ref=a.scoped_owner_ref AND a.native_owner_ref IS NULL) INTO owner_ok;
                owner_ok := owner_ok AND actual_n=1 AND schedule_n+session_n+routine_n+event_n=0;
            ELSIF a.facet_code='session.timing' THEN
                SELECT EXISTS (SELECT 1 FROM dante.session_timing_state s JOIN dante.native_address x ON x.native_ref=a.native_owner_ref AND x.owner_family='session' WHERE s.material_state_ref=state_ref AND s.session_ref=a.native_owner_ref AND a.scoped_owner_ref IS NULL) INTO owner_ok;
                owner_ok := owner_ok AND session_n=1 AND schedule_n+actual_n+routine_n+event_n=0;
            ELSIF a.facet_code='routine.recurrence' THEN
                SELECT EXISTS (SELECT 1 FROM dante.routine_recurrence_state s JOIN dante.native_address x ON x.native_ref=a.native_owner_ref AND x.owner_family='routine' WHERE s.material_state_ref=state_ref AND s.routine_ref=a.native_owner_ref AND a.scoped_owner_ref IS NULL) INTO owner_ok;
                owner_ok := owner_ok AND routine_n=1 AND schedule_n+actual_n+session_n+event_n=0;
            ELSIF a.facet_code='event.recurrence' THEN
                SELECT EXISTS (SELECT 1 FROM dante.event_recurrence_state s JOIN dante.native_address x ON x.native_ref=a.native_owner_ref AND x.owner_family='event' WHERE s.material_state_ref=state_ref AND s.event_ref=a.native_owner_ref AND a.scoped_owner_ref IS NULL) INTO owner_ok;
                owner_ok := owner_ok AND event_n=1 AND schedule_n+actual_n+session_n+routine_n=0;
            END IF;
            IF NOT owner_ok THEN
                RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT=TG_NAME, TABLE=TG_TABLE_NAME, SCHEMA=TG_TABLE_SCHEMA,
                    MESSAGE='material state totality rejected', DETAIL='MaterialState address, bounded owner family, facet and payload must form one exact live state';
            END IF;
            IF TG_OP='DELETE' THEN RETURN OLD; END IF;
            RETURN NEW;
        END;
        $function$
        """
    )

    _execute(
        r"""
        CREATE OR REPLACE FUNCTION dante.enforce_current_history_equivalence()
        RETURNS trigger
        LANGUAGE plpgsql
        SECURITY INVOKER
        VOLATILE
        PARALLEL UNSAFE
        SET search_path = pg_catalog, dante, pg_temp
        AS $function$
        DECLARE
            owner_ref uuid;
            facet text;
            history_table text;
            overlap_exists boolean := false;
            open_count integer := 0;
            current_state uuid;
            open_state uuid;
        BEGIN
            IF TG_TABLE_NAME LIKE '%_current_history' THEN
                IF TG_OP='INSERT' AND NEW.current_until_at IS NOT NULL THEN
                    RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT=TG_NAME, TABLE=TG_TABLE_NAME, SCHEMA=TG_TABLE_SCHEMA,
                        MESSAGE='current-history insert rejected', DETAIL='a currentness episode must begin open';
                END IF;
                IF TG_OP='UPDATE' THEN
                    IF TG_TABLE_NAME='schedule_placement_current_history' AND
                       (NEW.schedule_ref IS DISTINCT FROM OLD.schedule_ref OR NEW.material_state_ref IS DISTINCT FROM OLD.material_state_ref OR NEW.current_from_at IS DISTINCT FROM OLD.current_from_at) THEN
                        RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT=TG_NAME, TABLE=TG_TABLE_NAME, SCHEMA=TG_TABLE_SCHEMA, MESSAGE='current-history identity mutation rejected';
                    ELSIF TG_TABLE_NAME='actual_realization_current_history' AND
                       (NEW.actual_ref IS DISTINCT FROM OLD.actual_ref OR NEW.material_state_ref IS DISTINCT FROM OLD.material_state_ref OR NEW.current_from_at IS DISTINCT FROM OLD.current_from_at) THEN
                        RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT=TG_NAME, TABLE=TG_TABLE_NAME, SCHEMA=TG_TABLE_SCHEMA, MESSAGE='current-history identity mutation rejected';
                    ELSIF TG_TABLE_NAME='session_timing_current_history' AND
                       (NEW.session_ref IS DISTINCT FROM OLD.session_ref OR NEW.material_state_ref IS DISTINCT FROM OLD.material_state_ref OR NEW.current_from_at IS DISTINCT FROM OLD.current_from_at) THEN
                        RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT=TG_NAME, TABLE=TG_TABLE_NAME, SCHEMA=TG_TABLE_SCHEMA, MESSAGE='current-history identity mutation rejected';
                    ELSIF TG_TABLE_NAME='routine_recurrence_current_history' AND
                       (NEW.routine_ref IS DISTINCT FROM OLD.routine_ref OR NEW.material_state_ref IS DISTINCT FROM OLD.material_state_ref OR NEW.current_from_at IS DISTINCT FROM OLD.current_from_at) THEN
                        RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT=TG_NAME, TABLE=TG_TABLE_NAME, SCHEMA=TG_TABLE_SCHEMA, MESSAGE='current-history identity mutation rejected';
                    ELSIF TG_TABLE_NAME='event_recurrence_current_history' AND
                       (NEW.event_ref IS DISTINCT FROM OLD.event_ref OR NEW.material_state_ref IS DISTINCT FROM OLD.material_state_ref OR NEW.current_from_at IS DISTINCT FROM OLD.current_from_at) THEN
                        RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT=TG_NAME, TABLE=TG_TABLE_NAME, SCHEMA=TG_TABLE_SCHEMA, MESSAGE='current-history identity mutation rejected';
                    ELSIF TG_TABLE_NAME='temporal_constraint_current_history' AND
                       (NEW.constraint_ref IS DISTINCT FROM OLD.constraint_ref OR NEW.material_state_ref IS DISTINCT FROM OLD.material_state_ref OR NEW.current_from_at IS DISTINCT FROM OLD.current_from_at) THEN
                        RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT=TG_NAME, TABLE=TG_TABLE_NAME, SCHEMA=TG_TABLE_SCHEMA, MESSAGE='current-history identity mutation rejected';
                    END IF;
                    IF OLD.current_until_at IS NOT NULL AND NEW.current_until_at IS DISTINCT FROM OLD.current_until_at THEN
                        RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT=TG_NAME, TABLE=TG_TABLE_NAME, SCHEMA=TG_TABLE_SCHEMA,
                            MESSAGE='current-history closure mutation rejected', DETAIL='a closed currentness episode cannot be reopened or moved';
                    END IF;
                    IF OLD.current_until_at IS NULL AND NEW.current_until_at IS NOT NULL AND
                       (NOT isfinite(NEW.current_until_at) OR NEW.current_until_at<=NEW.current_from_at) THEN
                        RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT=TG_NAME, TABLE=TG_TABLE_NAME, SCHEMA=TG_TABLE_SCHEMA, MESSAGE='current-history closure rejected';
                    END IF;
                END IF;
            END IF;

            IF TG_TABLE_NAME='schedule_placement_current_history' THEN owner_ref:=CASE WHEN TG_OP='DELETE' THEN OLD.schedule_ref ELSE NEW.schedule_ref END; facet:='schedule.placement'; history_table:='schedule';
            ELSIF TG_TABLE_NAME='actual_realization_current_history' THEN owner_ref:=CASE WHEN TG_OP='DELETE' THEN OLD.actual_ref ELSE NEW.actual_ref END; facet:='actual.realization'; history_table:='actual';
            ELSIF TG_TABLE_NAME='session_timing_current_history' THEN owner_ref:=CASE WHEN TG_OP='DELETE' THEN OLD.session_ref ELSE NEW.session_ref END; facet:='session.timing'; history_table:='session';
            ELSIF TG_TABLE_NAME='routine_recurrence_current_history' THEN owner_ref:=CASE WHEN TG_OP='DELETE' THEN OLD.routine_ref ELSE NEW.routine_ref END; facet:='routine.recurrence'; history_table:='routine';
            ELSIF TG_TABLE_NAME='event_recurrence_current_history' THEN owner_ref:=CASE WHEN TG_OP='DELETE' THEN OLD.event_ref ELSE NEW.event_ref END; facet:='event.recurrence'; history_table:='event';
            ELSIF TG_TABLE_NAME='temporal_constraint_current_history' THEN owner_ref:=CASE WHEN TG_OP='DELETE' THEN OLD.constraint_ref ELSE NEW.constraint_ref END; facet:='temporal_constraint.rule'; history_table:='temporal_constraint';
            ELSIF TG_TABLE_NAME='native_current_material_state' THEN owner_ref:=CASE WHEN TG_OP='DELETE' THEN OLD.native_owner_ref ELSE NEW.native_owner_ref END; facet:=CASE WHEN TG_OP='DELETE' THEN OLD.facet_code ELSE NEW.facet_code END; history_table:=split_part(facet,'.',1);
            ELSE owner_ref:=CASE WHEN TG_OP='DELETE' THEN OLD.scoped_owner_ref ELSE NEW.scoped_owner_ref END; facet:=CASE WHEN TG_OP='DELETE' THEN OLD.facet_code ELSE NEW.facet_code END; history_table:=split_part(facet,'.',1);
            END IF;

            IF history_table='schedule' THEN
                SELECT EXISTS (SELECT 1 FROM dante.schedule_placement_current_history a JOIN dante.schedule_placement_current_history b ON a.schedule_ref=b.schedule_ref AND (a.schedule_ref,a.current_from_at)<>(b.schedule_ref,b.current_from_at) WHERE a.schedule_ref=owner_ref AND (a.current_until_at IS NULL OR a.current_until_at>b.current_from_at) AND (b.current_until_at IS NULL OR b.current_until_at>a.current_from_at)) INTO overlap_exists;
                SELECT count(*) INTO open_count FROM dante.schedule_placement_current_history WHERE schedule_ref=owner_ref AND current_until_at IS NULL; SELECT material_state_ref INTO open_state FROM dante.schedule_placement_current_history WHERE schedule_ref=owner_ref AND current_until_at IS NULL LIMIT 1;
                SELECT material_state_ref INTO current_state FROM dante.scoped_current_material_state WHERE scoped_owner_ref=owner_ref AND facet_code=facet;
            ELSIF history_table='actual' THEN
                SELECT EXISTS (SELECT 1 FROM dante.actual_realization_current_history a JOIN dante.actual_realization_current_history b ON a.actual_ref=b.actual_ref AND (a.actual_ref,a.current_from_at)<>(b.actual_ref,b.current_from_at) WHERE a.actual_ref=owner_ref AND (a.current_until_at IS NULL OR a.current_until_at>b.current_from_at) AND (b.current_until_at IS NULL OR b.current_until_at>a.current_from_at)) INTO overlap_exists;
                SELECT count(*) INTO open_count FROM dante.actual_realization_current_history WHERE actual_ref=owner_ref AND current_until_at IS NULL; SELECT material_state_ref INTO open_state FROM dante.actual_realization_current_history WHERE actual_ref=owner_ref AND current_until_at IS NULL LIMIT 1;
                SELECT material_state_ref INTO current_state FROM dante.scoped_current_material_state WHERE scoped_owner_ref=owner_ref AND facet_code=facet;
            ELSIF history_table='session' THEN
                SELECT EXISTS (SELECT 1 FROM dante.session_timing_current_history a JOIN dante.session_timing_current_history b ON a.session_ref=b.session_ref AND (a.session_ref,a.current_from_at)<>(b.session_ref,b.current_from_at) WHERE a.session_ref=owner_ref AND (a.current_until_at IS NULL OR a.current_until_at>b.current_from_at) AND (b.current_until_at IS NULL OR b.current_until_at>a.current_from_at)) INTO overlap_exists;
                SELECT count(*) INTO open_count FROM dante.session_timing_current_history WHERE session_ref=owner_ref AND current_until_at IS NULL; SELECT material_state_ref INTO open_state FROM dante.session_timing_current_history WHERE session_ref=owner_ref AND current_until_at IS NULL LIMIT 1;
                SELECT material_state_ref INTO current_state FROM dante.native_current_material_state WHERE native_owner_ref=owner_ref AND facet_code=facet;
            ELSIF history_table='routine' THEN
                SELECT EXISTS (SELECT 1 FROM dante.routine_recurrence_current_history a JOIN dante.routine_recurrence_current_history b ON a.routine_ref=b.routine_ref AND (a.routine_ref,a.current_from_at)<>(b.routine_ref,b.current_from_at) WHERE a.routine_ref=owner_ref AND (a.current_until_at IS NULL OR a.current_until_at>b.current_from_at) AND (b.current_until_at IS NULL OR b.current_until_at>a.current_from_at)) INTO overlap_exists;
                SELECT count(*) INTO open_count FROM dante.routine_recurrence_current_history WHERE routine_ref=owner_ref AND current_until_at IS NULL; SELECT material_state_ref INTO open_state FROM dante.routine_recurrence_current_history WHERE routine_ref=owner_ref AND current_until_at IS NULL LIMIT 1;
                SELECT material_state_ref INTO current_state FROM dante.native_current_material_state WHERE native_owner_ref=owner_ref AND facet_code=facet;
            ELSIF history_table='event' THEN
                SELECT EXISTS (SELECT 1 FROM dante.event_recurrence_current_history a JOIN dante.event_recurrence_current_history b ON a.event_ref=b.event_ref AND (a.event_ref,a.current_from_at)<>(b.event_ref,b.current_from_at) WHERE a.event_ref=owner_ref AND (a.current_until_at IS NULL OR a.current_until_at>b.current_from_at) AND (b.current_until_at IS NULL OR b.current_until_at>a.current_from_at)) INTO overlap_exists;
                SELECT count(*) INTO open_count FROM dante.event_recurrence_current_history WHERE event_ref=owner_ref AND current_until_at IS NULL; SELECT material_state_ref INTO open_state FROM dante.event_recurrence_current_history WHERE event_ref=owner_ref AND current_until_at IS NULL LIMIT 1;
                SELECT material_state_ref INTO current_state FROM dante.native_current_material_state WHERE native_owner_ref=owner_ref AND facet_code=facet;
            ELSIF history_table='temporal_constraint' THEN
                SELECT EXISTS (SELECT 1 FROM dante.temporal_constraint_current_history a JOIN dante.temporal_constraint_current_history b ON a.constraint_ref=b.constraint_ref AND (a.constraint_ref,a.current_from_at)<>(b.constraint_ref,b.current_from_at) WHERE a.constraint_ref=owner_ref AND (a.current_until_at IS NULL OR a.current_until_at>b.current_from_at) AND (b.current_until_at IS NULL OR b.current_until_at>a.current_from_at)) INTO overlap_exists;
                SELECT count(*) INTO open_count FROM dante.temporal_constraint_current_history WHERE constraint_ref=owner_ref AND current_until_at IS NULL; SELECT material_state_ref INTO open_state FROM dante.temporal_constraint_current_history WHERE constraint_ref=owner_ref AND current_until_at IS NULL LIMIT 1;
                SELECT material_state_ref INTO current_state FROM dante.scoped_current_material_state WHERE scoped_owner_ref=owner_ref AND facet_code=facet;
            ELSE
                IF TG_OP='DELETE' THEN RETURN OLD; END IF;
                RETURN NEW;
            END IF;

            IF overlap_exists OR open_count>1 OR current_state IS DISTINCT FROM open_state OR ((current_state IS NULL) <> (open_count=0)) THEN
                RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT=TG_NAME, TABLE=TG_TABLE_NAME, SCHEMA=TG_TABLE_SCHEMA,
                    MESSAGE='current-history equivalence rejected', DETAIL='history episodes must not overlap and the sole open episode must equal the current binding';
            END IF;
            IF TG_OP='DELETE' THEN RETURN OLD; END IF;
            RETURN NEW;
        END;
        $function$
        """
    )

    _execute(
        r"""
        CREATE OR REPLACE FUNCTION dante.enforce_owner_creation_completeness()
        RETURNS trigger
        LANGUAGE plpgsql
        SECURITY INVOKER
        VOLATILE
        PARALLEL UNSAFE
        SET search_path = pg_catalog, dante, pg_temp
        AS $function$
        DECLARE
            owner_ref uuid;
            ok boolean := false;
        BEGIN
            IF TG_TABLE_NAME='schedule' THEN owner_ref:=NEW.schedule_ref; SELECT EXISTS (SELECT 1 FROM dante.scoped_current_material_state WHERE scoped_owner_ref=owner_ref AND facet_code='schedule.placement') INTO ok;
            ELSIF TG_TABLE_NAME='actual' THEN owner_ref:=NEW.actual_ref; SELECT EXISTS (SELECT 1 FROM dante.scoped_current_material_state WHERE scoped_owner_ref=owner_ref AND facet_code='actual.realization') INTO ok;
            ELSIF TG_TABLE_NAME='temporal_constraint' THEN owner_ref:=NEW.constraint_ref; SELECT EXISTS (SELECT 1 FROM dante.scoped_current_material_state WHERE scoped_owner_ref=owner_ref AND facet_code='temporal_constraint.rule') INTO ok;
            ELSIF TG_TABLE_NAME='session' THEN owner_ref:=NEW.session_ref; SELECT EXISTS (SELECT 1 FROM dante.native_current_material_state WHERE native_owner_ref=owner_ref AND facet_code='session.timing') INTO ok;
            ELSIF TG_TABLE_NAME='routine' THEN owner_ref:=NEW.routine_ref; SELECT EXISTS (SELECT 1 FROM dante.native_current_material_state WHERE native_owner_ref=owner_ref AND facet_code='routine.recurrence') INTO ok;
            ELSIF TG_TABLE_NAME='occurrence' THEN owner_ref:=NEW.occurrence_ref; SELECT EXISTS (SELECT 1 FROM dante.occurrence_generation WHERE occurrence_ref=owner_ref) INTO ok;
            ELSE ok:=false;
            END IF;
            IF NOT ok THEN
                RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT=TG_NAME, TABLE=TG_TABLE_NAME, SCHEMA=TG_TABLE_SCHEMA,
                    MESSAGE='semantic owner creation incomplete', DETAIL='the owner requires its frozen companion/current contract by commit';
            END IF;
            RETURN NEW;
        END;
        $function$
        """
    )

    _execute(
        r"""
        CREATE FUNCTION dante.enforce_temporal_constraint_rule_totality()
        RETURNS trigger
        LANGUAGE plpgsql
        SECURITY INVOKER
        VOLATILE
        PARALLEL UNSAFE
        SET search_path = pg_catalog, dante, pg_temp
        AS $function$
        DECLARE
            state_ref uuid;
            family text;
            boundary_n integer;
            absolute_n integer;
            boundary_kind text;
            temporal_form text;
        BEGIN
            state_ref := CASE WHEN TG_OP='DELETE' THEN OLD.material_state_ref ELSE NEW.material_state_ref END;
            SELECT family_code INTO family
              FROM dante.temporal_constraint_state
             WHERE material_state_ref=state_ref;
            IF NOT FOUND THEN
                IF TG_OP='DELETE' THEN RETURN OLD; END IF;
                RETURN NEW;
            END IF;
            SELECT count(*) INTO boundary_n
              FROM dante.temporal_constraint_boundary_state
             WHERE material_state_ref=state_ref;
            SELECT count(*) INTO absolute_n
              FROM dante.temporal_constraint_boundary_absolute_state
             WHERE material_state_ref=state_ref;
            SELECT boundary_kind_code, temporal_form_code
              INTO boundary_kind, temporal_form
              FROM dante.temporal_constraint_boundary_state
             WHERE material_state_ref=state_ref;
            IF family IS DISTINCT FROM 'boundary'
               OR boundary_n<>1
               OR absolute_n<>1
               OR boundary_kind IS DISTINCT FROM 'earliest_start'
               OR temporal_form IS DISTINCT FROM 'absolute' THEN
                RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT=TG_NAME, TABLE=TG_TABLE_NAME, SCHEMA=TG_TABLE_SCHEMA,
                    MESSAGE='Temporal Constraint typed payload rejected',
                    DETAIL='the B04-A rule state requires exactly one absolute earliest-start boundary payload';
            END IF;
            IF TG_OP='DELETE' THEN RETURN OLD; END IF;
            RETURN NEW;
        END;
        $function$
        """
    )
    _execute(
        "ALTER FUNCTION dante.enforce_temporal_constraint_rule_totality() "
        f"OWNER TO {_OWNER}"
    )
    _execute(
        "REVOKE ALL PRIVILEGES ON FUNCTION dante.enforce_temporal_constraint_rule_totality() "
        f"FROM PUBLIC, {_RUNTIME}, {_MIGRATOR}"
    )

    _execute(
        "CREATE TRIGGER trg_temporal_constraint_native_ref "
        "BEFORE INSERT OR UPDATE OF subject_native_ref ON dante.temporal_constraint "
        "FOR EACH ROW EXECUTE FUNCTION dante.enforce_native_ref_eligibility()"
    )
    _execute(
        "CREATE CONSTRAINT TRIGGER ctrg_temporal_constraint_owner_complete "
        "AFTER INSERT ON dante.temporal_constraint "
        "DEFERRABLE INITIALLY DEFERRED FOR EACH ROW "
        "EXECUTE FUNCTION dante.enforce_owner_creation_completeness()"
    )
    _execute(
        "CREATE CONSTRAINT TRIGGER ctrg_temporal_constraint_state_state_totality "
        "AFTER INSERT OR UPDATE OR DELETE ON dante.temporal_constraint_state "
        "DEFERRABLE INITIALLY DEFERRED FOR EACH ROW "
        "EXECUTE FUNCTION dante.enforce_material_state_totality()"
    )
    for table in (
        "temporal_constraint_state",
        "temporal_constraint_boundary_state",
        "temporal_constraint_boundary_absolute_state",
    ):
        _execute(
            f"CREATE CONSTRAINT TRIGGER ctrg_{table}_rule_totality "
            f"AFTER INSERT OR UPDATE OR DELETE ON dante.{table} "
            "DEFERRABLE INITIALLY DEFERRED FOR EACH ROW "
            "EXECUTE FUNCTION dante.enforce_temporal_constraint_rule_totality()"
        )
    _execute(
        "CREATE CONSTRAINT TRIGGER ctrg_temporal_constraint_current_history_equivalence "
        "AFTER INSERT OR UPDATE OR DELETE ON dante.temporal_constraint_current_history "
        "DEFERRABLE INITIALLY DEFERRED FOR EACH ROW "
        "EXECUTE FUNCTION dante.enforce_current_history_equivalence()"
    )

    _execute(
        r"""
        CREATE FUNCTION dante.mutate_self_absolute_earliest_start_constraint(
            requested_self_person_ref uuid,
            requested_operation_id text,
            requested_intent_fingerprint text,
            requested_mutation_kind text,
            requested_subject_native_ref uuid,
            requested_constraint_ref uuid,
            requested_expected_material_state_ref uuid,
            requested_resulting_material_state_ref uuid,
            requested_strength_code text,
            requested_boundary_at timestamptz
        )
        RETURNS TABLE(
            constraint_ref uuid,
            subject_native_ref uuid,
            material_state_ref uuid,
            active boolean,
            created_at timestamptz,
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
            recorded_at timestamptz := statement_timestamp();
            subject_family text;
            owner_matches boolean := false;
            current_state_ref uuid;
            existing_fingerprint text;
            existing_kind text;
            existing_constraint_ref uuid;
            existing_subject_ref uuid;
            existing_expected_ref uuid;
            existing_result_ref uuid;
            existing_created_at timestamptz;
            existing_strength text;
            existing_boundary timestamptz;
        BEGIN
            IF normalized_operation_id = '' OR char_length(normalized_operation_id) > 200 THEN
                RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT='ck_temporal_constraint_mutation_operation_operation_id', MESSAGE='Temporal Constraint operation id rejected';
            END IF;
            IF requested_intent_fingerprint !~ '^[0-9a-f]{64}$' THEN
                RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT='ck_temporal_constraint_mutation_operation_fingerprint', MESSAGE='Temporal Constraint operation fingerprint rejected';
            END IF;
            IF requested_mutation_kind NOT IN ('create','revise','retire') THEN
                RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT='ck_temporal_constraint_mutation_operation_kind', MESSAGE='Temporal Constraint mutation kind rejected';
            END IF;
            IF uuid_extract_version(requested_constraint_ref) IS DISTINCT FROM 7 THEN
                RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT='ck_temporal_constraint_uuidv7', MESSAGE='Temporal Constraint reference rejected';
            END IF;
            IF requested_mutation_kind='create' THEN
                IF requested_expected_material_state_ref IS NOT NULL
                   OR requested_resulting_material_state_ref IS NULL
                   OR requested_strength_code NOT IN ('hard','soft')
                   OR requested_boundary_at IS NULL
                   OR NOT isfinite(requested_boundary_at) THEN
                    RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT='ck_temporal_constraint_mutation_operation_state_shape', MESSAGE='Temporal Constraint create shape rejected';
                END IF;
            ELSIF requested_mutation_kind='revise' THEN
                IF requested_expected_material_state_ref IS NULL
                   OR requested_resulting_material_state_ref IS NULL
                   OR requested_expected_material_state_ref=requested_resulting_material_state_ref
                   OR requested_strength_code NOT IN ('hard','soft')
                   OR requested_boundary_at IS NULL
                   OR NOT isfinite(requested_boundary_at) THEN
                    RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT='ck_temporal_constraint_mutation_operation_state_shape', MESSAGE='Temporal Constraint revision shape rejected';
                END IF;
            ELSE
                IF requested_expected_material_state_ref IS NULL
                   OR requested_resulting_material_state_ref IS NOT NULL
                   OR requested_strength_code IS NOT NULL
                   OR requested_boundary_at IS NOT NULL THEN
                    RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT='ck_temporal_constraint_mutation_operation_state_shape', MESSAGE='Temporal Constraint retirement shape rejected';
                END IF;
            END IF;
            IF requested_resulting_material_state_ref IS NOT NULL
               AND uuid_extract_version(requested_resulting_material_state_ref) IS DISTINCT FROM 7 THEN
                RAISE EXCEPTION USING ERRCODE='23514', MESSAGE='Temporal Constraint MaterialStateRef rejected';
            END IF;

            SELECT address.owner_family
              INTO subject_family
              FROM dante.native_address AS address
             WHERE address.native_ref=requested_subject_native_ref;
            IF subject_family='activity' THEN
                SELECT EXISTS (
                    SELECT 1 FROM dante.activity_intention
                    WHERE activity_ref=requested_subject_native_ref
                      AND self_person_ref=requested_self_person_ref
                ) INTO owner_matches;
            ELSIF subject_family='event' THEN
                SELECT EXISTS (
                    SELECT 1 FROM dante.event_expectation
                    WHERE event_ref=requested_subject_native_ref
                      AND self_person_ref=requested_self_person_ref
                ) INTO owner_matches;
            END IF;
            IF NOT owner_matches THEN
                RAISE EXCEPTION USING ERRCODE='23503', MESSAGE='Temporal Constraint self scope rejected', DETAIL='B04-A admits only self-owned Activity or Event subjects';
            END IF;

            PERFORM pg_advisory_xact_lock(hashtextextended(requested_self_person_ref::text || ':' || normalized_operation_id, 0));
            PERFORM pg_advisory_xact_lock(hashtextextended('temporal-constraint:' || requested_constraint_ref::text, 0));

            SELECT operation.intent_fingerprint,
                   operation.mutation_kind,
                   operation.constraint_ref,
                   operation.subject_native_ref,
                   operation.expected_material_state_ref,
                   operation.resulting_material_state_ref,
                   operation.created_at
              INTO existing_fingerprint,
                   existing_kind,
                   existing_constraint_ref,
                   existing_subject_ref,
                   existing_expected_ref,
                   existing_result_ref,
                   existing_created_at
              FROM dante.temporal_constraint_mutation_operation AS operation
             WHERE operation.self_person_ref=requested_self_person_ref
               AND operation.operation_id=normalized_operation_id;
            IF FOUND THEN
                IF existing_fingerprint<>requested_intent_fingerprint
                   OR existing_kind<>requested_mutation_kind
                   OR existing_constraint_ref<>requested_constraint_ref
                   OR existing_subject_ref<>requested_subject_native_ref
                   OR existing_expected_ref IS DISTINCT FROM requested_expected_material_state_ref
                   OR existing_result_ref IS DISTINCT FROM requested_resulting_material_state_ref THEN
                    RAISE EXCEPTION USING ERRCODE='23505', CONSTRAINT='pk_temporal_constraint_mutation_operation', MESSAGE='Temporal Constraint operation id reused with different intent';
                END IF;
                IF existing_result_ref IS NOT NULL THEN
                    SELECT state.strength_code, payload.boundary_at
                      INTO existing_strength, existing_boundary
                      FROM dante.temporal_constraint_state AS state
                      JOIN dante.temporal_constraint_boundary_state AS boundary
                        ON boundary.material_state_ref=state.material_state_ref
                      JOIN dante.temporal_constraint_boundary_absolute_state AS payload
                        ON payload.material_state_ref=boundary.material_state_ref
                     WHERE state.material_state_ref=existing_result_ref
                       AND state.constraint_ref=existing_constraint_ref;
                    IF NOT FOUND
                       OR existing_strength IS DISTINCT FROM requested_strength_code
                       OR existing_boundary IS DISTINCT FROM requested_boundary_at THEN
                        RAISE EXCEPTION USING ERRCODE='23505', CONSTRAINT='pk_temporal_constraint_mutation_operation', MESSAGE='Temporal Constraint operation id reused with different rule payload';
                    END IF;
                END IF;
                RETURN QUERY SELECT existing_constraint_ref, existing_subject_ref, existing_result_ref, existing_result_ref IS NOT NULL, existing_created_at, true;
                RETURN;
            END IF;

            IF requested_mutation_kind='create' THEN
                IF EXISTS (SELECT 1 FROM dante.temporal_constraint WHERE temporal_constraint.constraint_ref=requested_constraint_ref) THEN
                    RAISE EXCEPTION USING ERRCODE='23505', CONSTRAINT='pk_temporal_constraint', MESSAGE='Temporal Constraint reference already exists';
                END IF;
                INSERT INTO dante.temporal_constraint(constraint_ref,subject_native_ref)
                VALUES (requested_constraint_ref,requested_subject_native_ref);
                INSERT INTO dante.scoped_address(scoped_ref,scoped_family)
                VALUES (requested_constraint_ref,'temporal_constraint');
            ELSE
                IF NOT EXISTS (
                    SELECT 1 FROM dante.temporal_constraint AS constraint_row
                    WHERE constraint_row.constraint_ref=requested_constraint_ref
                      AND constraint_row.subject_native_ref=requested_subject_native_ref
                ) THEN
                    RAISE EXCEPTION USING ERRCODE='23503', MESSAGE='Temporal Constraint target rejected';
                END IF;
                SELECT current.material_state_ref
                  INTO current_state_ref
                  FROM dante.scoped_current_material_state AS current
                 WHERE current.scoped_owner_ref=requested_constraint_ref
                   AND current.facet_code='temporal_constraint.rule';
                IF current_state_ref IS DISTINCT FROM requested_expected_material_state_ref THEN
                    RAISE EXCEPTION USING ERRCODE='23505', CONSTRAINT='temporal_constraint_state_conflict', MESSAGE='Temporal Constraint current state conflict', DETAIL='expected MaterialStateRef does not match current rule state';
                END IF;
            END IF;

            IF requested_mutation_kind IN ('create','revise') THEN
                INSERT INTO dante.material_state_address(material_state_ref,native_owner_ref,scoped_owner_ref,facet_code)
                VALUES (requested_resulting_material_state_ref,NULL,requested_constraint_ref,'temporal_constraint.rule');
                INSERT INTO dante.temporal_constraint_state(material_state_ref,constraint_ref,family_code,strength_code,constrained_facet_code)
                VALUES (requested_resulting_material_state_ref,requested_constraint_ref,'boundary',requested_strength_code,'schedule.start');
                INSERT INTO dante.temporal_constraint_boundary_state(material_state_ref,boundary_kind_code,temporal_form_code)
                VALUES (requested_resulting_material_state_ref,'earliest_start','absolute');
                INSERT INTO dante.temporal_constraint_boundary_absolute_state(material_state_ref,boundary_at)
                VALUES (requested_resulting_material_state_ref,requested_boundary_at);

                IF requested_mutation_kind='create' THEN
                    INSERT INTO dante.scoped_current_material_state(scoped_owner_ref,facet_code,material_state_ref)
                    VALUES (requested_constraint_ref,'temporal_constraint.rule',requested_resulting_material_state_ref);
                ELSE
                    UPDATE dante.scoped_current_material_state AS current
                       SET material_state_ref=requested_resulting_material_state_ref
                     WHERE current.scoped_owner_ref=requested_constraint_ref
                       AND current.facet_code='temporal_constraint.rule'
                       AND current.material_state_ref=requested_expected_material_state_ref;
                    IF NOT FOUND THEN
                        RAISE EXCEPTION USING ERRCODE='23505', CONSTRAINT='temporal_constraint_state_conflict', MESSAGE='Temporal Constraint current state conflict';
                    END IF;
                    UPDATE dante.temporal_constraint_current_history AS history
                       SET current_until_at=recorded_at
                     WHERE history.constraint_ref=requested_constraint_ref
                       AND history.material_state_ref=requested_expected_material_state_ref
                       AND history.current_until_at IS NULL;
                    IF NOT FOUND THEN
                        RAISE EXCEPTION USING ERRCODE='XX001', MESSAGE='Temporal Constraint current history lost expected open state';
                    END IF;
                END IF;
                INSERT INTO dante.temporal_constraint_current_history(constraint_ref,material_state_ref,current_from_at,current_until_at)
                VALUES (requested_constraint_ref,requested_resulting_material_state_ref,recorded_at,NULL);
            ELSE
                DELETE FROM dante.scoped_current_material_state AS current
                 WHERE current.scoped_owner_ref=requested_constraint_ref
                   AND current.facet_code='temporal_constraint.rule'
                   AND current.material_state_ref=requested_expected_material_state_ref;
                IF NOT FOUND THEN
                    RAISE EXCEPTION USING ERRCODE='23505', CONSTRAINT='temporal_constraint_state_conflict', MESSAGE='Temporal Constraint current state conflict';
                END IF;
                UPDATE dante.temporal_constraint_current_history AS history
                   SET current_until_at=recorded_at
                 WHERE history.constraint_ref=requested_constraint_ref
                   AND history.material_state_ref=requested_expected_material_state_ref
                   AND history.current_until_at IS NULL;
                IF NOT FOUND THEN
                    RAISE EXCEPTION USING ERRCODE='XX001', MESSAGE='Temporal Constraint current history lost expected open state';
                END IF;
            END IF;

            INSERT INTO dante.temporal_constraint_mutation_operation(
                self_person_ref,operation_id,intent_fingerprint,mutation_kind,
                constraint_ref,subject_native_ref,expected_material_state_ref,
                resulting_material_state_ref,created_at
            ) VALUES (
                requested_self_person_ref,normalized_operation_id,requested_intent_fingerprint,
                requested_mutation_kind,requested_constraint_ref,requested_subject_native_ref,
                requested_expected_material_state_ref,requested_resulting_material_state_ref,recorded_at
            );

            RETURN QUERY SELECT requested_constraint_ref, requested_subject_native_ref,
                requested_resulting_material_state_ref,
                requested_resulting_material_state_ref IS NOT NULL,
                recorded_at, false;
        END;
        $function$
        """
    )
    _execute(f"ALTER FUNCTION {_MUTATE_SIGNATURE} OWNER TO {_OWNER}")

    for table in (
        "temporal_constraint",
        "temporal_constraint_state",
        "temporal_constraint_boundary_state",
        "temporal_constraint_boundary_absolute_state",
        "temporal_constraint_current_history",
        "temporal_constraint_mutation_operation",
    ):
        _execute(
            f"REVOKE ALL PRIVILEGES ON TABLE dante.{table} "
            f"FROM PUBLIC, {_RUNTIME}, {_MIGRATOR}"
        )

    _execute(
        f"REVOKE ALL PRIVILEGES ON FUNCTION {_MUTATE_SIGNATURE} "
        f"FROM PUBLIC, {_RUNTIME}, {_MIGRATOR}"
    )
    _execute(f"GRANT EXECUTE ON FUNCTION {_MUTATE_SIGNATURE} TO {_RUNTIME}")


def downgrade() -> None:
    """Fail closed: B04-A rewires shared material-state dispatch and must not be erased casually."""
    raise RuntimeError(
        "B04-A downgrade is intentionally refused; use a separately reviewed forward migration "
        "to retire Temporal Constraint state without corrupting shared scoped/material history"
    )
