"""Materialize the B04-D Schedule Movement Policy canonical core.

Revision ID: 20260919_37
Revises: 20260919_36
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "20260919_37"
down_revision: str | None = "20260919_36"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_SCHEMA = "dante"
_OWNER = "dante_owner"
_MIGRATOR = "dante_migrator"
_RUNTIME = "dante_runtime"
_MUTATE_SIGNATURE = (
    "dante.mutate_self_schedule_movement_policy("
    "uuid,text,text,text,uuid,uuid,uuid,text,text)"
)
_RESOLVE_SIGNATURE = "dante.resolve_self_schedule_movement_policy(uuid,uuid)"


def _execute(sql: str) -> None:
    op.execute(sa.text(sql))


def upgrade() -> None:
    """Install independently revisable movement governance for accepted Schedules."""
    # Movement Policy is a typed Schedule-owned rule facet. It is not a new
    # NativeRef/ScopedRecordRef root and it does not duplicate TemporalConstraint
    # geometry.
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
        "'schedule.placement','schedule.movement_policy','actual.realization',"
        "'session.timing','routine.recurrence','event.recurrence',"
        "'temporal_constraint.rule')",
        schema=_SCHEMA,
    )

    op.create_table(
        "schedule_movement_policy_state",
        sa.Column("material_state_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("schedule_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("automatic_movement_code", sa.Text(), nullable=False),
        sa.Column("acceptance_path_code", sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint(
            "material_state_ref",
            name=op.f("pk_schedule_movement_policy_state"),
        ),
        sa.UniqueConstraint(
            "schedule_ref",
            "material_state_ref",
            name=op.f("uq_schedule_movement_policy_state_schedule_material"),
        ),
        sa.ForeignKeyConstraint(
            ["material_state_ref"],
            [f"{_SCHEMA}.material_state_address.material_state_ref"],
            name="fk_schedule_movement_policy_state_material_state_address",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        sa.ForeignKeyConstraint(
            ["schedule_ref"],
            [f"{_SCHEMA}.schedule.schedule_ref"],
            name="fk_schedule_movement_policy_state_schedule",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        sa.CheckConstraint(
            "automatic_movement_code IN ('blocked','automatic')",
            name=op.f("ck_schedule_movement_policy_state_automatic_movement"),
        ),
        sa.CheckConstraint(
            "acceptance_path_code IN ('direct','confirmation_required')",
            name=op.f("ck_schedule_movement_policy_state_acceptance_path"),
        ),
        sa.CheckConstraint(
            "automatic_movement_code='automatic' OR acceptance_path_code='direct'",
            name=op.f("ck_schedule_movement_policy_state_blocked_shape"),
        ),
        schema=_SCHEMA,
    )
    op.create_index(
        "ix_schedule_movement_policy_state_schedule_ref",
        "schedule_movement_policy_state",
        ["schedule_ref"],
        unique=False,
        schema=_SCHEMA,
    )

    op.create_table(
        "schedule_movement_policy_current_history",
        sa.Column("schedule_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("material_state_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("current_from_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("current_until_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint(
            "schedule_ref",
            "current_from_at",
            name=op.f("pk_schedule_movement_policy_current_history"),
        ),
        sa.ForeignKeyConstraint(
            ["schedule_ref", "material_state_ref"],
            [
                f"{_SCHEMA}.schedule_movement_policy_state.schedule_ref",
                f"{_SCHEMA}.schedule_movement_policy_state.material_state_ref",
            ],
            name="fk_schedule_movement_policy_current_history_state",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        sa.CheckConstraint(
            "isfinite(current_from_at) AND (current_until_at IS NULL OR "
            "(isfinite(current_until_at) AND current_until_at > current_from_at))",
            name=op.f("ck_schedule_movement_policy_current_history_interval"),
        ),
        schema=_SCHEMA,
    )
    op.create_index(
        "ux_schedule_movement_policy_current_history_open",
        "schedule_movement_policy_current_history",
        ["schedule_ref"],
        unique=True,
        schema=_SCHEMA,
        postgresql_where=sa.text("current_until_at IS NULL"),
    )
    op.create_index(
        "ix_schedule_movement_policy_current_history_material_state_ref",
        "schedule_movement_policy_current_history",
        ["material_state_ref"],
        unique=False,
        schema=_SCHEMA,
    )

    op.create_table(
        "schedule_movement_policy_mutation_operation",
        sa.Column("self_person_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("operation_id", sa.Text(), nullable=False),
        sa.Column("intent_fingerprint", sa.Text(), nullable=False),
        sa.Column("mutation_kind", sa.Text(), nullable=False),
        sa.Column("schedule_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("expected_material_state_ref", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("resulting_material_state_ref", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("automatic_movement_code", sa.Text(), nullable=True),
        sa.Column("acceptance_path_code", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint(
            "self_person_ref",
            "operation_id",
            name=op.f("pk_schedule_movement_policy_mutation_operation"),
        ),
        sa.ForeignKeyConstraint(
            ["self_person_ref"],
            [f"{_SCHEMA}.person.person_ref"],
            name="fk_schedule_movement_policy_mutation_operation_self_person",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        sa.ForeignKeyConstraint(
            ["schedule_ref"],
            [f"{_SCHEMA}.schedule.schedule_ref"],
            name="fk_schedule_movement_policy_mutation_operation_schedule",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        sa.ForeignKeyConstraint(
            ["schedule_ref", "expected_material_state_ref"],
            [
                f"{_SCHEMA}.schedule_movement_policy_state.schedule_ref",
                f"{_SCHEMA}.schedule_movement_policy_state.material_state_ref",
            ],
            name="fk_schedule_movement_policy_mutation_operation_expected_state",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        sa.ForeignKeyConstraint(
            ["schedule_ref", "resulting_material_state_ref"],
            [
                f"{_SCHEMA}.schedule_movement_policy_state.schedule_ref",
                f"{_SCHEMA}.schedule_movement_policy_state.material_state_ref",
            ],
            name="fk_schedule_movement_policy_mutation_operation_resulting_state",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        sa.CheckConstraint(
            "operation_id=btrim(operation_id) AND operation_id<>'' "
            "AND char_length(operation_id)<=200",
            name=op.f("ck_schedule_movement_policy_mutation_operation_operation_id"),
        ),
        sa.CheckConstraint(
            "intent_fingerprint ~ '^[0-9a-f]{64}$'",
            name=op.f("ck_schedule_movement_policy_mutation_operation_fingerprint"),
        ),
        sa.CheckConstraint(
            "mutation_kind IN ('create','revise','retire')",
            name=op.f("ck_schedule_movement_policy_mutation_operation_kind"),
        ),
        sa.CheckConstraint(
            "(mutation_kind='create' AND expected_material_state_ref IS NULL "
            "AND resulting_material_state_ref IS NOT NULL "
            "AND automatic_movement_code IS NOT NULL AND acceptance_path_code IS NOT NULL) OR "
            "(mutation_kind='revise' AND expected_material_state_ref IS NOT NULL "
            "AND resulting_material_state_ref IS NOT NULL "
            "AND automatic_movement_code IS NOT NULL AND acceptance_path_code IS NOT NULL) OR "
            "(mutation_kind='retire' AND expected_material_state_ref IS NOT NULL "
            "AND resulting_material_state_ref IS NULL "
            "AND automatic_movement_code IS NULL AND acceptance_path_code IS NULL)",
            name=op.f("ck_schedule_movement_policy_mutation_operation_shape"),
        ),
        schema=_SCHEMA,
    )
    op.create_index(
        "ix_schedule_movement_policy_mutation_operation_schedule_ref",
        "schedule_movement_policy_mutation_operation",
        ["schedule_ref"],
        unique=False,
        schema=_SCHEMA,
    )
    op.create_index(
        "ux_schedule_movement_policy_mutation_operation_resulting_state",
        "schedule_movement_policy_mutation_operation",
        ["resulting_material_state_ref"],
        unique=True,
        schema=_SCHEMA,
        postgresql_where=sa.text("resulting_material_state_ref IS NOT NULL"),
    )

    # Extend the shared MaterialState totality dispatcher with exactly one new
    # typed owner/facet branch. No generic Rule/EAV payload is introduced.
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
            movement_n integer;
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
                   (SELECT count(*) FROM dante.schedule_movement_policy_state WHERE material_state_ref=state_ref),
                   (SELECT count(*) FROM dante.actual_realization_state WHERE material_state_ref=state_ref),
                   (SELECT count(*) FROM dante.session_timing_state WHERE material_state_ref=state_ref),
                   (SELECT count(*) FROM dante.routine_recurrence_state WHERE material_state_ref=state_ref),
                   (SELECT count(*) FROM dante.event_recurrence_state WHERE material_state_ref=state_ref)
              INTO schedule_n,movement_n,actual_n,session_n,routine_n,event_n;

            IF a.facet_code='temporal_constraint.rule' THEN
                SELECT count(*) INTO constraint_n FROM dante.temporal_constraint_state WHERE material_state_ref=state_ref;
                SELECT EXISTS (
                    SELECT 1 FROM dante.temporal_constraint_state AS s
                    JOIN dante.scoped_address AS x
                      ON x.scoped_ref=a.scoped_owner_ref AND x.scoped_family='temporal_constraint'
                    WHERE s.material_state_ref=state_ref
                      AND s.constraint_ref=a.scoped_owner_ref
                      AND a.native_owner_ref IS NULL
                ) INTO owner_ok;
                owner_ok := owner_ok AND constraint_n=1
                    AND schedule_n+movement_n+actual_n+session_n+routine_n+event_n=0;
            ELSIF a.facet_code='schedule.placement' THEN
                SELECT EXISTS (
                    SELECT 1 FROM dante.schedule_placement_state AS s
                    JOIN dante.scoped_address AS x
                      ON x.scoped_ref=a.scoped_owner_ref AND x.scoped_family='schedule'
                    WHERE s.material_state_ref=state_ref
                      AND s.schedule_ref=a.scoped_owner_ref
                      AND a.native_owner_ref IS NULL
                ) INTO owner_ok;
                owner_ok := owner_ok AND schedule_n=1
                    AND movement_n+actual_n+session_n+routine_n+event_n+constraint_n=0;
            ELSIF a.facet_code='schedule.movement_policy' THEN
                SELECT EXISTS (
                    SELECT 1 FROM dante.schedule_movement_policy_state AS s
                    JOIN dante.scoped_address AS x
                      ON x.scoped_ref=a.scoped_owner_ref AND x.scoped_family='schedule'
                    WHERE s.material_state_ref=state_ref
                      AND s.schedule_ref=a.scoped_owner_ref
                      AND a.native_owner_ref IS NULL
                ) INTO owner_ok;
                owner_ok := owner_ok AND movement_n=1
                    AND schedule_n+actual_n+session_n+routine_n+event_n+constraint_n=0;
            ELSIF a.facet_code='actual.realization' THEN
                SELECT EXISTS (SELECT 1 FROM dante.actual_realization_state s JOIN dante.scoped_address x ON x.scoped_ref=a.scoped_owner_ref AND x.scoped_family='actual' WHERE s.material_state_ref=state_ref AND s.actual_ref=a.scoped_owner_ref AND a.native_owner_ref IS NULL) INTO owner_ok;
                owner_ok := owner_ok AND actual_n=1 AND schedule_n+movement_n+session_n+routine_n+event_n+constraint_n=0;
            ELSIF a.facet_code='session.timing' THEN
                SELECT EXISTS (SELECT 1 FROM dante.session_timing_state s JOIN dante.native_address x ON x.native_ref=a.native_owner_ref AND x.owner_family='session' WHERE s.material_state_ref=state_ref AND s.session_ref=a.native_owner_ref AND a.scoped_owner_ref IS NULL) INTO owner_ok;
                owner_ok := owner_ok AND session_n=1 AND schedule_n+movement_n+actual_n+routine_n+event_n+constraint_n=0;
            ELSIF a.facet_code='routine.recurrence' THEN
                SELECT EXISTS (SELECT 1 FROM dante.routine_recurrence_state s JOIN dante.native_address x ON x.native_ref=a.native_owner_ref AND x.owner_family='routine' WHERE s.material_state_ref=state_ref AND s.routine_ref=a.native_owner_ref AND a.scoped_owner_ref IS NULL) INTO owner_ok;
                owner_ok := owner_ok AND routine_n=1 AND schedule_n+movement_n+actual_n+session_n+event_n+constraint_n=0;
            ELSIF a.facet_code='event.recurrence' THEN
                SELECT EXISTS (SELECT 1 FROM dante.event_recurrence_state s JOIN dante.native_address x ON x.native_ref=a.native_owner_ref AND x.owner_family='event' WHERE s.material_state_ref=state_ref AND s.event_ref=a.native_owner_ref AND a.scoped_owner_ref IS NULL) INTO owner_ok;
                owner_ok := owner_ok AND event_n=1 AND schedule_n+movement_n+actual_n+session_n+routine_n+constraint_n=0;
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
        CREATE FUNCTION dante.enforce_schedule_movement_policy_history()
        RETURNS trigger
        LANGUAGE plpgsql
        SECURITY INVOKER
        VOLATILE
        PARALLEL UNSAFE
        SET search_path = pg_catalog, dante, pg_temp
        AS $function$
        DECLARE
            target_schedule_ref uuid;
            overlap_exists boolean;
            open_count integer;
        BEGIN
            target_schedule_ref := CASE WHEN TG_OP='DELETE' THEN OLD.schedule_ref ELSE NEW.schedule_ref END;
            IF TG_OP='INSERT' AND NEW.current_until_at IS NOT NULL THEN
                RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT=TG_NAME,
                    MESSAGE='Movement Policy current-history insert rejected';
            END IF;
            IF TG_OP='UPDATE' THEN
                IF NEW.schedule_ref IS DISTINCT FROM OLD.schedule_ref
                   OR NEW.material_state_ref IS DISTINCT FROM OLD.material_state_ref
                   OR NEW.current_from_at IS DISTINCT FROM OLD.current_from_at THEN
                    RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT=TG_NAME,
                        MESSAGE='Movement Policy current-history identity mutation rejected';
                END IF;
                IF OLD.current_until_at IS NOT NULL
                   AND NEW.current_until_at IS DISTINCT FROM OLD.current_until_at THEN
                    RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT=TG_NAME,
                        MESSAGE='Movement Policy closed history cannot be reopened or moved';
                END IF;
            END IF;
            SELECT EXISTS (
                SELECT 1
                  FROM dante.schedule_movement_policy_current_history AS a
                  JOIN dante.schedule_movement_policy_current_history AS b
                    ON a.schedule_ref=b.schedule_ref
                   AND (a.schedule_ref,a.current_from_at)<>(b.schedule_ref,b.current_from_at)
                 WHERE a.schedule_ref=target_schedule_ref
                   AND (a.current_until_at IS NULL OR a.current_until_at>b.current_from_at)
                   AND (b.current_until_at IS NULL OR b.current_until_at>a.current_from_at)
            ) INTO overlap_exists;
            SELECT count(*) INTO open_count
              FROM dante.schedule_movement_policy_current_history
             WHERE schedule_ref=target_schedule_ref AND current_until_at IS NULL;
            IF overlap_exists OR open_count>1 THEN
                RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT=TG_NAME,
                    MESSAGE='Movement Policy current-history equivalence rejected';
            END IF;
            IF TG_OP='DELETE' THEN RETURN OLD; END IF;
            RETURN NEW;
        END;
        $function$
        """
    )
    _execute(
        "ALTER FUNCTION dante.enforce_schedule_movement_policy_history() "
        f"OWNER TO {_OWNER}"
    )
    _execute(
        "REVOKE ALL PRIVILEGES ON FUNCTION dante.enforce_schedule_movement_policy_history() "
        f"FROM PUBLIC, {_RUNTIME}, {_MIGRATOR}"
    )
    _execute(
        "CREATE CONSTRAINT TRIGGER ctrg_schedule_movement_policy_state_totality "
        "AFTER INSERT OR UPDATE OR DELETE ON dante.schedule_movement_policy_state "
        "DEFERRABLE INITIALLY DEFERRED FOR EACH ROW "
        "EXECUTE FUNCTION dante.enforce_material_state_totality()"
    )
    _execute(
        "CREATE CONSTRAINT TRIGGER ctrg_schedule_movement_policy_current_history_equivalence "
        "AFTER INSERT OR UPDATE OR DELETE ON dante.schedule_movement_policy_current_history "
        "DEFERRABLE INITIALLY DEFERRED FOR EACH ROW "
        "EXECUTE FUNCTION dante.enforce_schedule_movement_policy_history()"
    )

    _execute(
        r"""
        CREATE FUNCTION dante.mutate_self_schedule_movement_policy(
            requested_self_person_ref uuid,
            requested_operation_id text,
            requested_intent_fingerprint text,
            requested_mutation_kind text,
            requested_schedule_ref uuid,
            requested_expected_material_state_ref uuid,
            requested_resulting_material_state_ref uuid,
            requested_automatic_movement_code text,
            requested_acceptance_path_code text
        )
        RETURNS TABLE(
            schedule_ref uuid,
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
        DECLARE
            normalized_operation_id text := btrim(requested_operation_id);
            recorded_at timestamptz := statement_timestamp();
            current_state_ref uuid;
            current_from_at timestamptz;
            existing_fingerprint text;
            existing_kind text;
            existing_schedule_ref uuid;
            existing_expected_ref uuid;
            existing_result_ref uuid;
            existing_automatic text;
            existing_acceptance text;
            existing_created_at timestamptz;
        BEGIN
            IF normalized_operation_id='' OR char_length(normalized_operation_id)>200 THEN
                RAISE EXCEPTION USING ERRCODE='23514', MESSAGE='Movement Policy operation id rejected';
            END IF;
            IF requested_intent_fingerprint !~ '^[0-9a-f]{64}$' THEN
                RAISE EXCEPTION USING ERRCODE='23514', MESSAGE='Movement Policy fingerprint rejected';
            END IF;
            IF requested_mutation_kind NOT IN ('create','revise','retire') THEN
                RAISE EXCEPTION USING ERRCODE='23514', MESSAGE='Movement Policy mutation kind rejected';
            END IF;
            IF uuid_extract_version(requested_schedule_ref) IS DISTINCT FROM 7
               OR (requested_expected_material_state_ref IS NOT NULL AND uuid_extract_version(requested_expected_material_state_ref) IS DISTINCT FROM 7)
               OR (requested_resulting_material_state_ref IS NOT NULL AND uuid_extract_version(requested_resulting_material_state_ref) IS DISTINCT FROM 7) THEN
                RAISE EXCEPTION USING ERRCODE='23514', MESSAGE='Movement Policy reference rejected';
            END IF;
            IF requested_mutation_kind IN ('create','revise') THEN
                IF requested_resulting_material_state_ref IS NULL
                   OR requested_automatic_movement_code NOT IN ('blocked','automatic')
                   OR requested_acceptance_path_code NOT IN ('direct','confirmation_required')
                   OR (requested_automatic_movement_code='blocked' AND requested_acceptance_path_code<>'direct') THEN
                    RAISE EXCEPTION USING ERRCODE='23514', MESSAGE='Movement Policy state rejected';
                END IF;
            ELSIF requested_resulting_material_state_ref IS NOT NULL
               OR requested_automatic_movement_code IS NOT NULL
               OR requested_acceptance_path_code IS NOT NULL THEN
                RAISE EXCEPTION USING ERRCODE='23514', MESSAGE='Movement Policy retirement payload rejected';
            END IF;

            IF NOT EXISTS (
                SELECT 1
                  FROM dante.schedule AS schedule_row
                  JOIN dante.native_address AS address
                    ON address.native_ref=schedule_row.subject_native_ref
                 WHERE schedule_row.schedule_ref=requested_schedule_ref
                   AND (
                        (address.owner_family='activity' AND EXISTS (
                            SELECT 1 FROM dante.activity_intention AS activity
                             WHERE activity.activity_ref=schedule_row.subject_native_ref
                               AND activity.self_person_ref=requested_self_person_ref
                        ))
                        OR
                        (address.owner_family='event' AND EXISTS (
                            SELECT 1 FROM dante.event_expectation AS event_row
                             WHERE event_row.event_ref=schedule_row.subject_native_ref
                               AND event_row.self_person_ref=requested_self_person_ref
                        ))
                   )
            ) THEN
                RAISE EXCEPTION USING ERRCODE='23503', CONSTRAINT='movement_policy_schedule_not_found', MESSAGE='Movement Policy self scope rejected';
            END IF;

            PERFORM pg_advisory_xact_lock(hashtextextended(requested_schedule_ref::text, 0));
            SELECT operation.intent_fingerprint,
                   operation.mutation_kind,
                   operation.schedule_ref,
                   operation.expected_material_state_ref,
                   operation.resulting_material_state_ref,
                   operation.automatic_movement_code,
                   operation.acceptance_path_code,
                   operation.created_at
              INTO existing_fingerprint,existing_kind,existing_schedule_ref,
                   existing_expected_ref,existing_result_ref,existing_automatic,
                   existing_acceptance,existing_created_at
              FROM dante.schedule_movement_policy_mutation_operation AS operation
             WHERE operation.self_person_ref=requested_self_person_ref
               AND operation.operation_id=normalized_operation_id;
            IF FOUND THEN
                IF existing_fingerprint IS DISTINCT FROM requested_intent_fingerprint
                   OR existing_kind IS DISTINCT FROM requested_mutation_kind
                   OR existing_schedule_ref IS DISTINCT FROM requested_schedule_ref
                   OR existing_expected_ref IS DISTINCT FROM requested_expected_material_state_ref
                   OR existing_automatic IS DISTINCT FROM requested_automatic_movement_code
                   OR existing_acceptance IS DISTINCT FROM requested_acceptance_path_code THEN
                    RAISE EXCEPTION USING ERRCODE='23505', CONSTRAINT='pk_schedule_movement_policy_mutation_operation', MESSAGE='Movement Policy operation id reused with different intent';
                END IF;
                RETURN QUERY SELECT existing_schedule_ref,existing_result_ref,
                    existing_result_ref IS NOT NULL,existing_created_at,true;
                RETURN;
            END IF;

            SELECT history.material_state_ref, history.current_from_at
              INTO current_state_ref,current_from_at
              FROM dante.schedule_movement_policy_current_history AS history
             WHERE history.schedule_ref=requested_schedule_ref
               AND history.current_until_at IS NULL
             FOR UPDATE;

            IF requested_mutation_kind='create' THEN
                IF requested_expected_material_state_ref IS NOT NULL OR current_state_ref IS NOT NULL THEN
                    RAISE EXCEPTION USING ERRCODE='23505', CONSTRAINT='movement_policy_state_conflict', MESSAGE='Movement Policy create basis rejected';
                END IF;
            ELSE
                IF requested_expected_material_state_ref IS NULL
                   OR current_state_ref IS DISTINCT FROM requested_expected_material_state_ref THEN
                    RAISE EXCEPTION USING ERRCODE='23505', CONSTRAINT='movement_policy_state_conflict', MESSAGE='Movement Policy current state conflict';
                END IF;
                recorded_at := GREATEST(clock_timestamp(), current_from_at + interval '1 microsecond');
            END IF;

            IF requested_mutation_kind IN ('create','revise') THEN
                INSERT INTO dante.material_state_address(
                    material_state_ref,native_owner_ref,scoped_owner_ref,facet_code
                ) VALUES (
                    requested_resulting_material_state_ref,NULL,requested_schedule_ref,'schedule.movement_policy'
                );
                INSERT INTO dante.schedule_movement_policy_state(
                    material_state_ref,schedule_ref,automatic_movement_code,acceptance_path_code
                ) VALUES (
                    requested_resulting_material_state_ref,requested_schedule_ref,
                    requested_automatic_movement_code,requested_acceptance_path_code
                );
                IF requested_mutation_kind='revise' THEN
                    UPDATE dante.schedule_movement_policy_current_history AS history
                       SET current_until_at=recorded_at
                     WHERE history.schedule_ref=requested_schedule_ref
                       AND history.material_state_ref=requested_expected_material_state_ref
                       AND history.current_until_at IS NULL;
                    IF NOT FOUND THEN
                        RAISE EXCEPTION USING ERRCODE='XX001', MESSAGE='Movement Policy current history lost expected open state';
                    END IF;
                END IF;
                INSERT INTO dante.schedule_movement_policy_current_history(
                    schedule_ref,material_state_ref,current_from_at,current_until_at
                ) VALUES (
                    requested_schedule_ref,requested_resulting_material_state_ref,recorded_at,NULL
                );
            ELSE
                UPDATE dante.schedule_movement_policy_current_history AS history
                   SET current_until_at=recorded_at
                 WHERE history.schedule_ref=requested_schedule_ref
                   AND history.material_state_ref=requested_expected_material_state_ref
                   AND history.current_until_at IS NULL;
                IF NOT FOUND THEN
                    RAISE EXCEPTION USING ERRCODE='XX001', MESSAGE='Movement Policy current history lost expected open state';
                END IF;
            END IF;

            INSERT INTO dante.schedule_movement_policy_mutation_operation(
                self_person_ref,operation_id,intent_fingerprint,mutation_kind,
                schedule_ref,expected_material_state_ref,resulting_material_state_ref,
                automatic_movement_code,acceptance_path_code,created_at
            ) VALUES (
                requested_self_person_ref,normalized_operation_id,requested_intent_fingerprint,
                requested_mutation_kind,requested_schedule_ref,requested_expected_material_state_ref,
                requested_resulting_material_state_ref,requested_automatic_movement_code,
                requested_acceptance_path_code,recorded_at
            );
            RETURN QUERY SELECT requested_schedule_ref,requested_resulting_material_state_ref,
                requested_resulting_material_state_ref IS NOT NULL,recorded_at,false;
        END;
        $function$
        """
    )
    _execute(f"ALTER FUNCTION {_MUTATE_SIGNATURE} OWNER TO {_OWNER}")

    _execute(
        r"""
        CREATE FUNCTION dante.resolve_self_schedule_movement_policy(
            requested_self_person_ref uuid,
            requested_schedule_ref uuid
        )
        RETURNS TABLE(
            schedule_ref uuid,
            material_state_ref uuid,
            automatic_movement_code text,
            acceptance_path_code text
        )
        LANGUAGE sql
        SECURITY DEFINER
        STABLE
        PARALLEL SAFE
        SET search_path = pg_catalog, dante, pg_temp
        AS $function$
            SELECT state.schedule_ref,
                   state.material_state_ref,
                   state.automatic_movement_code,
                   state.acceptance_path_code
              FROM dante.schedule_movement_policy_current_history AS history
              JOIN dante.schedule_movement_policy_state AS state
                ON state.schedule_ref=history.schedule_ref
               AND state.material_state_ref=history.material_state_ref
              JOIN dante.schedule AS schedule_row
                ON schedule_row.schedule_ref=state.schedule_ref
              JOIN dante.native_address AS address
                ON address.native_ref=schedule_row.subject_native_ref
             WHERE state.schedule_ref=requested_schedule_ref
               AND history.current_until_at IS NULL
               AND (
                    (address.owner_family='activity' AND EXISTS (
                        SELECT 1 FROM dante.activity_intention AS activity
                         WHERE activity.activity_ref=schedule_row.subject_native_ref
                           AND activity.self_person_ref=requested_self_person_ref
                    ))
                    OR
                    (address.owner_family='event' AND EXISTS (
                        SELECT 1 FROM dante.event_expectation AS event_row
                         WHERE event_row.event_ref=schedule_row.subject_native_ref
                           AND event_row.self_person_ref=requested_self_person_ref
                    ))
               );
        $function$
        """
    )
    _execute(f"ALTER FUNCTION {_RESOLVE_SIGNATURE} OWNER TO {_OWNER}")

    for table in (
        "schedule_movement_policy_state",
        "schedule_movement_policy_current_history",
        "schedule_movement_policy_mutation_operation",
    ):
        _execute(
            f"REVOKE ALL PRIVILEGES ON TABLE dante.{table} "
            f"FROM PUBLIC, {_RUNTIME}, {_MIGRATOR}"
        )

    for signature in (_MUTATE_SIGNATURE, _RESOLVE_SIGNATURE):
        _execute(
            f"REVOKE ALL PRIVILEGES ON FUNCTION {signature} "
            f"FROM PUBLIC, {_RUNTIME}, {_MIGRATOR}"
        )
        _execute(f"GRANT EXECUTE ON FUNCTION {signature} TO {_RUNTIME}")


def downgrade() -> None:
    """Fail closed because policy history is canonical governance state."""
    raise RuntimeError(
        "B04-D Movement Policy downgrade is intentionally refused; use a separately "
        "reviewed forward migration to retire policy state without erasing history"
    )
