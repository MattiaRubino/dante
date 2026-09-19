"""Activate B04-E planned Schedule duration Temporal Constraints.

Revision ID: 20260919_40
Revises: 20260919_39
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "20260919_40"
down_revision: str | None = "20260919_39"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_SCHEMA = "dante"
_OWNER = "dante_owner"
_MIGRATOR = "dante_migrator"
_RUNTIME = "dante_runtime"
_MUTATE_SIGNATURE = (
    "dante.mutate_self_schedule_duration_constraint("
    "uuid,text,text,text,uuid,uuid,uuid,uuid,text,text,text,bigint)"
)
_ASSERT_SIGNATURE = (
    "dante.assert_absolute_schedule_move_hard_admissible("
    "uuid,timestamp with time zone,timestamp with time zone)"
)


def _sql(statement: str) -> None:
    op.get_bind().exec_driver_sql(statement)


def upgrade() -> None:
    """Activate exact planned-placement duration rules and movement enforcement."""
    op.drop_constraint(
        op.f("ck_temporal_constraint_state_family"),
        "temporal_constraint_state",
        schema=_SCHEMA,
        type_="check",
    )
    op.create_check_constraint(
        op.f("ck_temporal_constraint_state_family"),
        "temporal_constraint_state",
        "family_code IN ('boundary','window','duration')",
        schema=_SCHEMA,
    )

    op.create_table(
        "temporal_constraint_duration_state",
        sa.Column("material_state_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("duration_kind_code", sa.Text(), nullable=False),
        sa.Column("duration_microseconds", sa.BigInteger(), nullable=False),
        sa.PrimaryKeyConstraint(
            "material_state_ref",
            name=op.f("pk_temporal_constraint_duration_state"),
        ),
        sa.ForeignKeyConstraint(
            ["material_state_ref"],
            [f"{_SCHEMA}.temporal_constraint_state.material_state_ref"],
            name="fk_temporal_constraint_duration_state_constraint_state",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        sa.CheckConstraint(
            "duration_kind_code IN ('minimum','maximum')",
            name=op.f("ck_temporal_constraint_duration_state_kind"),
        ),
        sa.CheckConstraint(
            "duration_microseconds > 0",
            name=op.f("ck_temporal_constraint_duration_state_positive"),
        ),
        schema=_SCHEMA,
    )

    _sql(
        r"""
        CREATE OR REPLACE FUNCTION dante.enforce_temporal_constraint_rule_totality()
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
            constrained_facet text;
            boundary_n integer;
            boundary_absolute_n integer;
            window_n integer;
            window_absolute_n integer;
            duration_n integer;
            boundary_kind text;
            window_relationship text;
            duration_kind text;
            temporal_form text;
            pair_ok boolean := false;
        BEGIN
            state_ref := CASE WHEN TG_OP='DELETE' THEN OLD.material_state_ref ELSE NEW.material_state_ref END;
            SELECT family_code, constrained_facet_code
              INTO family, constrained_facet
              FROM dante.temporal_constraint_state
             WHERE material_state_ref=state_ref;
            IF NOT FOUND THEN
                IF TG_OP='DELETE' THEN RETURN OLD; END IF;
                RETURN NEW;
            END IF;

            SELECT count(*) INTO boundary_n
              FROM dante.temporal_constraint_boundary_state
             WHERE material_state_ref=state_ref;
            SELECT count(*) INTO boundary_absolute_n
              FROM dante.temporal_constraint_boundary_absolute_state
             WHERE material_state_ref=state_ref;
            SELECT count(*) INTO window_n
              FROM dante.temporal_constraint_window_state
             WHERE material_state_ref=state_ref;
            SELECT count(*) INTO window_absolute_n
              FROM dante.temporal_constraint_window_absolute_state
             WHERE material_state_ref=state_ref;
            SELECT count(*) INTO duration_n
              FROM dante.temporal_constraint_duration_state
             WHERE material_state_ref=state_ref;

            IF family='boundary' THEN
                SELECT boundary_kind_code, temporal_form_code
                  INTO boundary_kind, temporal_form
                  FROM dante.temporal_constraint_boundary_state
                 WHERE material_state_ref=state_ref;
                pair_ok :=
                    (boundary_kind='earliest_start' AND constrained_facet='schedule.start')
                    OR (boundary_kind='latest_start' AND constrained_facet='schedule.start')
                    OR (boundary_kind='latest_completion' AND constrained_facet='schedule.completion');
                IF boundary_n<>1 OR boundary_absolute_n<>1
                   OR window_n<>0 OR window_absolute_n<>0 OR duration_n<>0
                   OR temporal_form IS DISTINCT FROM 'absolute' OR NOT pair_ok THEN
                    RAISE EXCEPTION USING
                        ERRCODE='23514', CONSTRAINT=TG_NAME, TABLE=TG_TABLE_NAME, SCHEMA=TG_TABLE_SCHEMA,
                        MESSAGE='Temporal Constraint typed payload rejected',
                        DETAIL='boundary family requires exactly one admitted absolute boundary payload';
                END IF;
            ELSIF family='window' THEN
                SELECT relationship_code, temporal_form_code
                  INTO window_relationship, temporal_form
                  FROM dante.temporal_constraint_window_state
                 WHERE material_state_ref=state_ref;
                pair_ok :=
                    (window_relationship='start_within' AND constrained_facet='schedule.start')
                    OR (window_relationship='completion_within' AND constrained_facet='schedule.completion')
                    OR (window_relationship IN ('full_placement_contained','placement_overlaps') AND constrained_facet='schedule.placement');
                IF window_n<>1 OR window_absolute_n<>1
                   OR boundary_n<>0 OR boundary_absolute_n<>0 OR duration_n<>0
                   OR temporal_form IS DISTINCT FROM 'absolute' OR NOT pair_ok THEN
                    RAISE EXCEPTION USING
                        ERRCODE='23514', CONSTRAINT=TG_NAME, TABLE=TG_TABLE_NAME, SCHEMA=TG_TABLE_SCHEMA,
                        MESSAGE='Temporal Constraint typed payload rejected',
                        DETAIL='window family requires exactly one admitted absolute window payload';
                END IF;
            ELSIF family='duration' THEN
                SELECT duration_kind_code
                  INTO duration_kind
                  FROM dante.temporal_constraint_duration_state
                 WHERE material_state_ref=state_ref;
                pair_ok := duration_kind IN ('minimum','maximum')
                           AND constrained_facet='schedule.placement';
                IF duration_n<>1
                   OR boundary_n<>0 OR boundary_absolute_n<>0
                   OR window_n<>0 OR window_absolute_n<>0
                   OR NOT pair_ok THEN
                    RAISE EXCEPTION USING
                        ERRCODE='23514', CONSTRAINT=TG_NAME, TABLE=TG_TABLE_NAME, SCHEMA=TG_TABLE_SCHEMA,
                        MESSAGE='Temporal Constraint typed payload rejected',
                        DETAIL='duration family requires exactly one admitted schedule.placement duration payload';
                END IF;
            ELSE
                RAISE EXCEPTION USING
                    ERRCODE='23514', CONSTRAINT=TG_NAME, TABLE=TG_TABLE_NAME, SCHEMA=TG_TABLE_SCHEMA,
                    MESSAGE='Temporal Constraint typed payload rejected',
                    DETAIL='Temporal Constraint family is outside the activated B04-E rule algebra';
            END IF;

            IF TG_OP='DELETE' THEN RETURN OLD; END IF;
            RETURN NEW;
        END;
        $function$
        """
    )
    _sql(
        "ALTER FUNCTION dante.enforce_temporal_constraint_rule_totality() "
        f"OWNER TO {_OWNER}"
    )
    _sql(
        "REVOKE ALL PRIVILEGES ON FUNCTION dante.enforce_temporal_constraint_rule_totality() "
        f"FROM PUBLIC, {_RUNTIME}, {_MIGRATOR}"
    )

    _sql(
        "CREATE CONSTRAINT TRIGGER ctrg_temporal_constraint_duration_state_rule_totality "
        "AFTER INSERT OR UPDATE OR DELETE ON dante.temporal_constraint_duration_state "
        "DEFERRABLE INITIALLY DEFERRED FOR EACH ROW "
        "EXECUTE FUNCTION dante.enforce_temporal_constraint_rule_totality()"
    )
    _sql(
        "REVOKE ALL PRIVILEGES ON TABLE dante.temporal_constraint_duration_state "
        f"FROM PUBLIC, {_RUNTIME}, {_MIGRATOR}"
    )

    _sql(
        r"""
        CREATE FUNCTION dante.mutate_self_schedule_duration_constraint(
            requested_self_person_ref uuid,
            requested_operation_id text,
            requested_intent_fingerprint text,
            requested_mutation_kind text,
            requested_subject_native_ref uuid,
            requested_constraint_ref uuid,
            requested_expected_material_state_ref uuid,
            requested_resulting_material_state_ref uuid,
            requested_duration_kind_code text,
            requested_constrained_facet_code text,
            requested_strength_code text,
            requested_duration_microseconds bigint
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
            existing_facet text;
            existing_duration_kind text;
            existing_duration_microseconds bigint;
        BEGIN
            IF normalized_operation_id='' OR char_length(normalized_operation_id)>200 THEN
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
                   OR requested_duration_kind_code NOT IN ('minimum','maximum')
                   OR requested_constrained_facet_code<>'schedule.placement'
                   OR requested_strength_code NOT IN ('hard','soft')
                   OR requested_duration_microseconds IS NULL
                   OR requested_duration_microseconds<=0 THEN
                    RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT='ck_temporal_constraint_mutation_operation_state_shape', MESSAGE='Temporal Constraint duration create shape rejected';
                END IF;
            ELSIF requested_mutation_kind='revise' THEN
                IF requested_expected_material_state_ref IS NULL
                   OR requested_resulting_material_state_ref IS NULL
                   OR requested_expected_material_state_ref=requested_resulting_material_state_ref
                   OR requested_duration_kind_code NOT IN ('minimum','maximum')
                   OR requested_constrained_facet_code<>'schedule.placement'
                   OR requested_strength_code NOT IN ('hard','soft')
                   OR requested_duration_microseconds IS NULL
                   OR requested_duration_microseconds<=0 THEN
                    RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT='ck_temporal_constraint_mutation_operation_state_shape', MESSAGE='Temporal Constraint duration revision shape rejected';
                END IF;
            ELSE
                IF requested_expected_material_state_ref IS NULL
                   OR requested_resulting_material_state_ref IS NOT NULL
                   OR requested_duration_kind_code IS NOT NULL
                   OR requested_constrained_facet_code IS NOT NULL
                   OR requested_strength_code IS NOT NULL
                   OR requested_duration_microseconds IS NOT NULL THEN
                    RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT='ck_temporal_constraint_mutation_operation_state_shape', MESSAGE='Temporal Constraint duration retirement shape rejected';
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
                RAISE EXCEPTION USING ERRCODE='23503', MESSAGE='Temporal Constraint self scope rejected', DETAIL='B04-E duration admits only self-owned Activity or Event subjects';
            END IF;

            PERFORM pg_advisory_xact_lock(hashtextextended(requested_self_person_ref::text || ':' || normalized_operation_id,0));
            PERFORM pg_advisory_xact_lock(hashtextextended('temporal-constraint:' || requested_constraint_ref::text,0));

            SELECT operation.intent_fingerprint,
                   operation.mutation_kind,
                   operation.constraint_ref,
                   operation.subject_native_ref,
                   operation.expected_material_state_ref,
                   operation.resulting_material_state_ref,
                   operation.created_at
              INTO existing_fingerprint,existing_kind,existing_constraint_ref,
                   existing_subject_ref,existing_expected_ref,existing_result_ref,
                   existing_created_at
              FROM dante.temporal_constraint_mutation_operation AS operation
             WHERE operation.self_person_ref=requested_self_person_ref
               AND operation.operation_id=normalized_operation_id;
            IF FOUND THEN
                IF existing_fingerprint<>requested_intent_fingerprint
                   OR existing_kind<>requested_mutation_kind
                   OR existing_subject_ref<>requested_subject_native_ref
                   OR (requested_mutation_kind<>'create' AND existing_constraint_ref<>requested_constraint_ref)
                   OR (requested_mutation_kind<>'create' AND existing_expected_ref IS DISTINCT FROM requested_expected_material_state_ref) THEN
                    RAISE EXCEPTION USING ERRCODE='23505', CONSTRAINT='pk_temporal_constraint_mutation_operation', MESSAGE='Temporal Constraint operation id reused with different intent';
                END IF;
                IF existing_result_ref IS NOT NULL THEN
                    SELECT state.strength_code,
                           state.constrained_facet_code,
                           duration_state.duration_kind_code,
                           duration_state.duration_microseconds
                      INTO existing_strength,existing_facet,
                           existing_duration_kind,existing_duration_microseconds
                      FROM dante.temporal_constraint_state AS state
                      JOIN dante.temporal_constraint_duration_state AS duration_state
                        ON duration_state.material_state_ref=state.material_state_ref
                     WHERE state.material_state_ref=existing_result_ref
                       AND state.constraint_ref=existing_constraint_ref;
                    IF existing_strength IS DISTINCT FROM requested_strength_code
                       OR existing_facet IS DISTINCT FROM requested_constrained_facet_code
                       OR existing_duration_kind IS DISTINCT FROM requested_duration_kind_code
                       OR existing_duration_microseconds IS DISTINCT FROM requested_duration_microseconds THEN
                        RAISE EXCEPTION USING ERRCODE='23505', CONSTRAINT='pk_temporal_constraint_mutation_operation', MESSAGE='Temporal Constraint operation id reused with different duration payload';
                    END IF;
                END IF;
                RETURN QUERY SELECT existing_constraint_ref,existing_subject_ref,
                    existing_result_ref,existing_result_ref IS NOT NULL,
                    existing_created_at,true;
                RETURN;
            END IF;

            IF requested_mutation_kind='create' THEN
                IF EXISTS (
                    SELECT 1 FROM dante.temporal_constraint
                     WHERE temporal_constraint.constraint_ref=requested_constraint_ref
                ) THEN
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
                VALUES (requested_resulting_material_state_ref,requested_constraint_ref,'duration',requested_strength_code,'schedule.placement');
                INSERT INTO dante.temporal_constraint_duration_state(material_state_ref,duration_kind_code,duration_microseconds)
                VALUES (requested_resulting_material_state_ref,requested_duration_kind_code,requested_duration_microseconds);

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

            RETURN QUERY SELECT requested_constraint_ref,requested_subject_native_ref,
                requested_resulting_material_state_ref,
                requested_resulting_material_state_ref IS NOT NULL,
                recorded_at,false;
        END;
        $function$
        """
    )
    _sql(f"ALTER FUNCTION {_MUTATE_SIGNATURE} OWNER TO {_OWNER}")
    _sql(
        f"REVOKE ALL PRIVILEGES ON FUNCTION {_MUTATE_SIGNATURE} "
        f"FROM PUBLIC, {_RUNTIME}, {_MIGRATOR}"
    )
    _sql(f"GRANT EXECUTE ON FUNCTION {_MUTATE_SIGNATURE} TO {_RUNTIME}")

    _sql(
        r"""
        CREATE OR REPLACE FUNCTION dante.assert_absolute_schedule_move_hard_admissible(
            requested_subject_native_ref uuid,
            requested_starts_at timestamptz,
            requested_ends_at timestamptz
        )
        RETURNS void
        LANGUAGE plpgsql
        SECURITY DEFINER
        STABLE
        PARALLEL SAFE
        SET search_path = pg_catalog, dante, pg_temp
        AS $function$
        DECLARE
            rule record;
            satisfied boolean;
            candidate_duration interval;
        BEGIN
            IF requested_starts_at IS NULL OR requested_ends_at IS NULL
               OR NOT isfinite(requested_starts_at) OR NOT isfinite(requested_ends_at)
               OR requested_ends_at <= requested_starts_at THEN
                RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT='schedule_move_not_evaluable',
                    MESSAGE='Automatic Schedule move candidate is not an evaluable absolute interval';
            END IF;
            candidate_duration := requested_ends_at - requested_starts_at;

            FOR rule IN
                SELECT state.family_code,
                       state.constrained_facet_code,
                       boundary.boundary_kind_code,
                       boundary.temporal_form_code AS boundary_form,
                       boundary_payload.boundary_at,
                       window_state.relationship_code,
                       window_state.temporal_form_code AS window_form,
                       window_payload.starts_at AS window_starts_at,
                       window_payload.ends_at AS window_ends_at,
                       duration_state.duration_kind_code,
                       duration_state.duration_microseconds
                  FROM dante.temporal_constraint AS constraint_row
                  JOIN dante.scoped_current_material_state AS current
                    ON current.scoped_owner_ref=constraint_row.constraint_ref
                   AND current.facet_code='temporal_constraint.rule'
                  JOIN dante.temporal_constraint_state AS state
                    ON state.constraint_ref=constraint_row.constraint_ref
                   AND state.material_state_ref=current.material_state_ref
                  LEFT JOIN dante.temporal_constraint_boundary_state AS boundary
                    ON boundary.material_state_ref=state.material_state_ref
                  LEFT JOIN dante.temporal_constraint_boundary_absolute_state AS boundary_payload
                    ON boundary_payload.material_state_ref=state.material_state_ref
                  LEFT JOIN dante.temporal_constraint_window_state AS window_state
                    ON window_state.material_state_ref=state.material_state_ref
                  LEFT JOIN dante.temporal_constraint_window_absolute_state AS window_payload
                    ON window_payload.material_state_ref=state.material_state_ref
                  LEFT JOIN dante.temporal_constraint_duration_state AS duration_state
                    ON duration_state.material_state_ref=state.material_state_ref
                 WHERE constraint_row.subject_native_ref=requested_subject_native_ref
                   AND state.strength_code='hard'
            LOOP
                satisfied := NULL;
                IF rule.family_code='boundary' THEN
                    IF rule.boundary_form IS DISTINCT FROM 'absolute' OR rule.boundary_at IS NULL THEN
                        RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT='schedule_move_not_evaluable',
                            MESSAGE='Current hard Temporal Constraint cannot be evaluated for automatic movement';
                    END IF;
                    IF rule.boundary_kind_code='earliest_start'
                       AND rule.constrained_facet_code='schedule.start' THEN
                        satisfied := requested_starts_at >= rule.boundary_at;
                    ELSIF rule.boundary_kind_code='latest_start'
                       AND rule.constrained_facet_code='schedule.start' THEN
                        satisfied := requested_starts_at <= rule.boundary_at;
                    ELSIF rule.boundary_kind_code='latest_completion'
                       AND rule.constrained_facet_code='schedule.completion' THEN
                        satisfied := requested_ends_at <= rule.boundary_at;
                    ELSE
                        RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT='schedule_move_not_evaluable',
                            MESSAGE='Current hard Temporal Constraint boundary is outside the B04-E evaluator';
                    END IF;
                ELSIF rule.family_code='window' THEN
                    IF rule.window_form IS DISTINCT FROM 'absolute'
                       OR rule.window_starts_at IS NULL OR rule.window_ends_at IS NULL THEN
                        RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT='schedule_move_not_evaluable',
                            MESSAGE='Current hard Temporal Constraint window cannot be evaluated for automatic movement';
                    END IF;
                    IF rule.relationship_code='start_within'
                       AND rule.constrained_facet_code='schedule.start' THEN
                        satisfied := requested_starts_at >= rule.window_starts_at
                                     AND requested_starts_at <= rule.window_ends_at;
                    ELSIF rule.relationship_code='completion_within'
                       AND rule.constrained_facet_code='schedule.completion' THEN
                        satisfied := requested_ends_at >= rule.window_starts_at
                                     AND requested_ends_at <= rule.window_ends_at;
                    ELSIF rule.relationship_code='full_placement_contained'
                       AND rule.constrained_facet_code='schedule.placement' THEN
                        satisfied := requested_starts_at >= rule.window_starts_at
                                     AND requested_ends_at <= rule.window_ends_at;
                    ELSIF rule.relationship_code='placement_overlaps'
                       AND rule.constrained_facet_code='schedule.placement' THEN
                        satisfied := requested_starts_at < rule.window_ends_at
                                     AND requested_ends_at > rule.window_starts_at;
                    ELSE
                        RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT='schedule_move_not_evaluable',
                            MESSAGE='Current hard Temporal Constraint window relation is outside the B04-E evaluator';
                    END IF;
                ELSIF rule.family_code='duration' THEN
                    IF rule.constrained_facet_code IS DISTINCT FROM 'schedule.placement'
                       OR rule.duration_microseconds IS NULL
                       OR rule.duration_microseconds<=0 THEN
                        RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT='schedule_move_not_evaluable',
                            MESSAGE='Current hard duration constraint cannot be evaluated for automatic movement';
                    END IF;
                    IF rule.duration_kind_code='minimum' THEN
                        satisfied := candidate_duration >= rule.duration_microseconds * interval '1 microsecond';
                    ELSIF rule.duration_kind_code='maximum' THEN
                        satisfied := candidate_duration <= rule.duration_microseconds * interval '1 microsecond';
                    ELSE
                        RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT='schedule_move_not_evaluable',
                            MESSAGE='Current hard duration kind is outside the B04-E evaluator';
                    END IF;
                ELSE
                    RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT='schedule_move_not_evaluable',
                        MESSAGE='Current hard Temporal Constraint family is outside the B04-E evaluator';
                END IF;

                IF satisfied IS DISTINCT FROM true THEN
                    RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT='schedule_move_hard_constraint_violation',
                        MESSAGE='Automatic Schedule move violates a current hard Temporal Constraint';
                END IF;
            END LOOP;
        END;
        $function$
        """
    )
    _sql(f"ALTER FUNCTION {_ASSERT_SIGNATURE} OWNER TO {_OWNER}")
    _sql(
        f"REVOKE ALL PRIVILEGES ON FUNCTION {_ASSERT_SIGNATURE} "
        f"FROM PUBLIC, {_RUNTIME}, {_MIGRATOR}"
    )


def downgrade() -> None:
    """Fail closed rather than discard accepted B04-E duration semantics."""
    raise RuntimeError(
        "B04-E Schedule duration downgrade is intentionally refused; use a separately reviewed forward migration"
    )
