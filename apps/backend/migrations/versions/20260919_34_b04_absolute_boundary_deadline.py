"""Activate B04-B absolute latest-bound / deadline Temporal Constraints.

Revision ID: 20260919_34
Revises: 20260918_33
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260919_34"
down_revision: str | None = "20260918_33"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_SCHEMA = "dante"
_OWNER = "dante_owner"
_MIGRATOR = "dante_migrator"
_RUNTIME = "dante_runtime"
_MUTATE_SIGNATURE = (
    "dante.mutate_self_absolute_boundary_constraint("
    "uuid,text,text,text,uuid,uuid,uuid,uuid,text,text,text,timestamp with time zone)"
)


def _sql(statement: str) -> None:
    op.get_bind().exec_driver_sql(statement)


def upgrade() -> None:
    """Extend the B04-A core to the frozen B04-B absolute boundary matrix."""
    op.drop_constraint(
        op.f("ck_temporal_constraint_state_constrained_facet"),
        "temporal_constraint_state",
        schema=_SCHEMA,
        type_="check",
    )
    op.create_check_constraint(
        op.f("ck_temporal_constraint_state_constrained_facet"),
        "temporal_constraint_state",
        "constrained_facet_code IN ('schedule.start','schedule.completion')",
        schema=_SCHEMA,
    )

    op.drop_constraint(
        op.f("ck_temporal_constraint_boundary_state_kind"),
        "temporal_constraint_boundary_state",
        schema=_SCHEMA,
        type_="check",
    )
    op.create_check_constraint(
        op.f("ck_temporal_constraint_boundary_state_kind"),
        "temporal_constraint_boundary_state",
        "boundary_kind_code IN ('earliest_start','latest_start','latest_completion')",
        schema=_SCHEMA,
    )

    # Keep typed rule validity in the deferred DB integrity layer. The two
    # widened row-level enums alone must not admit semantically invalid pairs.
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
            absolute_n integer;
            boundary_kind text;
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
            SELECT count(*) INTO absolute_n
              FROM dante.temporal_constraint_boundary_absolute_state
             WHERE material_state_ref=state_ref;
            SELECT boundary_kind_code, temporal_form_code
              INTO boundary_kind, temporal_form
              FROM dante.temporal_constraint_boundary_state
             WHERE material_state_ref=state_ref;

            pair_ok :=
                (boundary_kind='earliest_start' AND constrained_facet='schedule.start')
                OR (boundary_kind='latest_start' AND constrained_facet='schedule.start')
                OR (boundary_kind='latest_completion' AND constrained_facet='schedule.completion');

            IF family IS DISTINCT FROM 'boundary'
               OR boundary_n<>1
               OR absolute_n<>1
               OR temporal_form IS DISTINCT FROM 'absolute'
               OR NOT pair_ok THEN
                RAISE EXCEPTION USING
                    ERRCODE='23514',
                    CONSTRAINT=TG_NAME,
                    TABLE=TG_TABLE_NAME,
                    SCHEMA=TG_TABLE_SCHEMA,
                    MESSAGE='Temporal Constraint typed payload rejected',
                    DETAIL='B04-B requires exactly one absolute boundary payload and one admitted boundary-kind / constrained-facet pair';
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
        r"""
        CREATE FUNCTION dante.mutate_self_absolute_boundary_constraint(
            requested_self_person_ref uuid,
            requested_operation_id text,
            requested_intent_fingerprint text,
            requested_mutation_kind text,
            requested_subject_native_ref uuid,
            requested_constraint_ref uuid,
            requested_expected_material_state_ref uuid,
            requested_resulting_material_state_ref uuid,
            requested_boundary_kind_code text,
            requested_constrained_facet_code text,
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
            pair_ok boolean := false;
            existing_fingerprint text;
            existing_kind text;
            existing_constraint_ref uuid;
            existing_subject_ref uuid;
            existing_expected_ref uuid;
            existing_result_ref uuid;
            existing_created_at timestamptz;
            existing_strength text;
            existing_facet text;
            existing_boundary_kind text;
            existing_temporal_form text;
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

            pair_ok :=
                (requested_boundary_kind_code='earliest_start' AND requested_constrained_facet_code='schedule.start')
                OR (requested_boundary_kind_code='latest_start' AND requested_constrained_facet_code='schedule.start')
                OR (requested_boundary_kind_code='latest_completion' AND requested_constrained_facet_code='schedule.completion');

            IF requested_mutation_kind='create' THEN
                IF requested_expected_material_state_ref IS NOT NULL
                   OR requested_resulting_material_state_ref IS NULL
                   OR NOT pair_ok
                   OR requested_strength_code NOT IN ('hard','soft')
                   OR requested_boundary_at IS NULL
                   OR NOT isfinite(requested_boundary_at) THEN
                    RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT='ck_temporal_constraint_mutation_operation_state_shape', MESSAGE='Temporal Constraint create shape rejected';
                END IF;
            ELSIF requested_mutation_kind='revise' THEN
                IF requested_expected_material_state_ref IS NULL
                   OR requested_resulting_material_state_ref IS NULL
                   OR requested_expected_material_state_ref=requested_resulting_material_state_ref
                   OR NOT pair_ok
                   OR requested_strength_code NOT IN ('hard','soft')
                   OR requested_boundary_at IS NULL
                   OR NOT isfinite(requested_boundary_at) THEN
                    RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT='ck_temporal_constraint_mutation_operation_state_shape', MESSAGE='Temporal Constraint revision shape rejected';
                END IF;
            ELSE
                IF requested_expected_material_state_ref IS NULL
                   OR requested_resulting_material_state_ref IS NOT NULL
                   OR requested_boundary_kind_code IS NOT NULL
                   OR requested_constrained_facet_code IS NOT NULL
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
                RAISE EXCEPTION USING ERRCODE='23503', MESSAGE='Temporal Constraint self scope rejected', DETAIL='B04-B admits only self-owned Activity or Event subjects';
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
                   OR existing_subject_ref<>requested_subject_native_ref
                   OR (
                        requested_mutation_kind<>'create'
                        AND existing_constraint_ref<>requested_constraint_ref
                   )
                   OR (
                        requested_mutation_kind<>'create'
                        AND existing_expected_ref IS DISTINCT FROM requested_expected_material_state_ref
                   ) THEN
                    RAISE EXCEPTION USING ERRCODE='23505', CONSTRAINT='pk_temporal_constraint_mutation_operation', MESSAGE='Temporal Constraint operation id reused with different intent';
                END IF;
                IF existing_result_ref IS NOT NULL THEN
                    SELECT state.strength_code,
                           state.constrained_facet_code,
                           boundary.boundary_kind_code,
                           boundary.temporal_form_code,
                           payload.boundary_at
                      INTO existing_strength,
                           existing_facet,
                           existing_boundary_kind,
                           existing_temporal_form,
                           existing_boundary
                      FROM dante.temporal_constraint_state AS state
                      JOIN dante.temporal_constraint_boundary_state AS boundary
                        ON boundary.material_state_ref=state.material_state_ref
                      JOIN dante.temporal_constraint_boundary_absolute_state AS payload
                        ON payload.material_state_ref=boundary.material_state_ref
                     WHERE state.material_state_ref=existing_result_ref
                       AND state.constraint_ref=existing_constraint_ref;
                    IF NOT FOUND
                       OR existing_strength IS DISTINCT FROM requested_strength_code
                       OR existing_facet IS DISTINCT FROM requested_constrained_facet_code
                       OR existing_boundary_kind IS DISTINCT FROM requested_boundary_kind_code
                       OR existing_temporal_form IS DISTINCT FROM 'absolute'
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
                VALUES (requested_resulting_material_state_ref,requested_constraint_ref,'boundary',requested_strength_code,requested_constrained_facet_code);
                INSERT INTO dante.temporal_constraint_boundary_state(material_state_ref,boundary_kind_code,temporal_form_code)
                VALUES (requested_resulting_material_state_ref,requested_boundary_kind_code,'absolute');
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

    _sql(f"ALTER FUNCTION {_MUTATE_SIGNATURE} OWNER TO {_OWNER}")
    _sql(
        f"REVOKE ALL PRIVILEGES ON FUNCTION {_MUTATE_SIGNATURE} "
        f"FROM PUBLIC, {_RUNTIME}, {_MIGRATOR}"
    )
    _sql(f"GRANT EXECUTE ON FUNCTION {_MUTATE_SIGNATURE} TO {_RUNTIME}")


def downgrade() -> None:
    """Fail closed rather than discard accepted B04-B boundary semantics."""
    raise RuntimeError(
        "B04-B absolute boundary downgrade is intentionally refused; use a separately "
        "reviewed forward migration"
    )
