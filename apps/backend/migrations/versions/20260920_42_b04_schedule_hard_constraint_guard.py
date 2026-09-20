"""Enforce current B04 hard Temporal Constraints on canonical Schedule establish/revise.

Revision ID: 20260920_42
Revises: 20260919_41
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260920_42"
down_revision: str | None = "20260919_41"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_OWNER = "dante_owner"
_RUNTIME = "dante_runtime"
_MIGRATOR = "dante_migrator"
_ASSERT_SIGNATURE = "dante.assert_schedule_placement_hard_admissible(uuid,jsonb)"


def _execute(sql: str) -> None:
    op.execute(sa.text(sql))


def upgrade() -> None:
    """Make manual Schedule establish/revise obey the same current hard B04 rules."""
    _execute(
        r"""
        CREATE FUNCTION dante.assert_schedule_placement_hard_admissible(
            requested_subject_native_ref uuid,
            requested_payload jsonb
        )
        RETURNS void
        LANGUAGE plpgsql
        SECURITY DEFINER
        STABLE
        PARALLEL SAFE
        SET search_path = pg_catalog, dante, pg_temp
        AS $function$
        DECLARE
            placement_kind text;
            hard_exists boolean;
            candidate_starts_at timestamptz;
            candidate_ends_at timestamptz;
            inner_constraint text;
        BEGIN
            SELECT EXISTS (
                SELECT 1
                  FROM dante.temporal_constraint AS constraint_row
                  JOIN dante.scoped_current_material_state AS current
                    ON current.scoped_owner_ref=constraint_row.constraint_ref
                   AND current.facet_code='temporal_constraint.rule'
                  JOIN dante.temporal_constraint_state AS state
                    ON state.constraint_ref=constraint_row.constraint_ref
                   AND state.material_state_ref=current.material_state_ref
                 WHERE constraint_row.subject_native_ref=requested_subject_native_ref
                   AND state.strength_code='hard'
            ) INTO hard_exists;

            IF NOT hard_exists THEN
                RETURN;
            END IF;
            IF jsonb_typeof(requested_payload) IS DISTINCT FROM 'object' THEN
                RAISE EXCEPTION USING ERRCODE='23514',
                    CONSTRAINT='schedule_hard_constraint_not_evaluable',
                    MESSAGE='Schedule placement cannot be evaluated against current hard Temporal Constraints';
            END IF;

            placement_kind := requested_payload ->> 'kind';
            IF placement_kind='absolute_interval' THEN
                BEGIN
                    candidate_starts_at := (requested_payload ->> 'starts_at')::timestamptz;
                    candidate_ends_at := (requested_payload ->> 'ends_at')::timestamptz;
                EXCEPTION WHEN OTHERS THEN
                    RAISE EXCEPTION USING ERRCODE='23514',
                        CONSTRAINT='schedule_hard_constraint_not_evaluable',
                        MESSAGE='Absolute Schedule placement cannot be evaluated against current hard Temporal Constraints';
                END;
            ELSIF placement_kind='named_zone_local_interval' THEN
                BEGIN
                    candidate_starts_at := (requested_payload ->> 'resolved_start_at')::timestamptz;
                    candidate_ends_at := (requested_payload ->> 'resolved_end_at')::timestamptz;
                EXCEPTION WHEN OTHERS THEN
                    RAISE EXCEPTION USING ERRCODE='23514',
                        CONSTRAINT='schedule_hard_constraint_not_evaluable',
                        MESSAGE='Named-zone Schedule placement lacks an evaluable resolved interval';
                END;
            ELSE
                RAISE EXCEPTION USING ERRCODE='23514',
                    CONSTRAINT='schedule_hard_constraint_not_evaluable',
                    MESSAGE='Current hard absolute Temporal Constraints require an absolute or resolved named-zone Schedule placement';
            END IF;

            BEGIN
                PERFORM dante.assert_absolute_schedule_move_hard_admissible(
                    requested_subject_native_ref,
                    candidate_starts_at,
                    candidate_ends_at
                );
            EXCEPTION WHEN check_violation THEN
                GET STACKED DIAGNOSTICS inner_constraint = CONSTRAINT_NAME;
                IF inner_constraint='schedule_move_hard_constraint_violation' THEN
                    RAISE EXCEPTION USING ERRCODE='23514',
                        CONSTRAINT='schedule_hard_constraint_violation',
                        MESSAGE='Schedule placement violates a current hard Temporal Constraint';
                ELSIF inner_constraint='schedule_move_not_evaluable' THEN
                    RAISE EXCEPTION USING ERRCODE='23514',
                        CONSTRAINT='schedule_hard_constraint_not_evaluable',
                        MESSAGE='Schedule placement cannot be evaluated against a current hard Temporal Constraint';
                END IF;
                RAISE;
            END;
        END;
        $function$
        """
    )
    _execute(f"ALTER FUNCTION {_ASSERT_SIGNATURE} OWNER TO {_OWNER}")
    _execute(
        f"REVOKE ALL PRIVILEGES ON FUNCTION {_ASSERT_SIGNATURE} "
        f"FROM PUBLIC, {_RUNTIME}, {_MIGRATOR}"
    )

    _execute(
        r"""
        CREATE OR REPLACE FUNCTION dante.establish_self_schedule_placement(
            requested_self_person_ref uuid,
            requested_operation_id text,
            requested_intent_fingerprint text,
            requested_subject_native_ref uuid,
            requested_schedule_ref uuid,
            requested_material_state_ref uuid,
            requested_payload jsonb
        )
        RETURNS TABLE(
            subject_native_ref uuid,
            schedule_ref uuid,
            material_state_ref uuid,
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
            existing_fingerprint text;
            existing_subject_native_ref uuid;
            existing_schedule_ref uuid;
            existing_material_state_ref uuid;
            existing_created_at timestamptz;
        BEGIN
            IF normalized_operation_id = '' OR char_length(normalized_operation_id) > 200 THEN
                RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT='ck_schedule_establish_operation_operation_id', MESSAGE='Schedule operation id rejected';
            END IF;
            IF requested_intent_fingerprint !~ '^[0-9a-f]{64}$' THEN
                RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT='ck_schedule_establish_operation_fingerprint', MESSAGE='Schedule operation fingerprint rejected';
            END IF;
            IF uuid_extract_version(requested_schedule_ref) IS DISTINCT FROM 7
               OR uuid_extract_version(requested_material_state_ref) IS DISTINCT FROM 7 THEN
                RAISE EXCEPTION USING ERRCODE='23514', MESSAGE='Schedule placement reference rejected';
            END IF;
            IF NOT EXISTS (
                SELECT 1
                  FROM dante.native_address AS address
                 WHERE address.native_ref = requested_subject_native_ref
                   AND (
                       (address.owner_family='activity' AND EXISTS (
                           SELECT 1 FROM dante.activity_intention AS intention
                            WHERE intention.activity_ref=requested_subject_native_ref
                              AND intention.self_person_ref=requested_self_person_ref
                       ))
                       OR
                       (address.owner_family='event' AND EXISTS (
                           SELECT 1 FROM dante.event_expectation AS expectation
                            WHERE expectation.event_ref=requested_subject_native_ref
                              AND expectation.self_person_ref=requested_self_person_ref
                       ))
                   )
            ) THEN
                RAISE EXCEPTION USING ERRCODE='23503', MESSAGE='Schedule self scope rejected';
            END IF;

            PERFORM pg_advisory_xact_lock(hashtextextended(requested_self_person_ref::text || ':' || normalized_operation_id, 0));
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
                    RAISE EXCEPTION USING ERRCODE='23505', CONSTRAINT='pk_schedule_establish_operation', MESSAGE='Schedule operation id reused with different intent';
                END IF;
                IF dante.schedule_placement_payload_json(existing_schedule_ref, existing_material_state_ref) IS NULL THEN
                    RAISE EXCEPTION USING ERRCODE='XX001', MESSAGE='Schedule operation receipt lost canonical Schedule state';
                END IF;
                RETURN QUERY SELECT existing_subject_native_ref, existing_schedule_ref, existing_material_state_ref, existing_created_at, true;
                RETURN;
            END IF;

            PERFORM dante.assert_schedule_placement_hard_admissible(
                requested_subject_native_ref,
                requested_payload
            );

            INSERT INTO dante.schedule(schedule_ref, subject_native_ref)
            VALUES (requested_schedule_ref, requested_subject_native_ref);
            INSERT INTO dante.scoped_address(scoped_ref, scoped_family)
            VALUES (requested_schedule_ref, 'schedule');
            PERFORM dante.insert_schedule_placement_payload(requested_material_state_ref, requested_schedule_ref, requested_payload);
            INSERT INTO dante.scoped_current_material_state(scoped_owner_ref, facet_code, material_state_ref)
            VALUES (requested_schedule_ref, 'schedule.placement', requested_material_state_ref);
            INSERT INTO dante.schedule_placement_current_history(schedule_ref, material_state_ref, current_from_at, current_until_at)
            VALUES (requested_schedule_ref, requested_material_state_ref, recorded_at, NULL);
            INSERT INTO dante.schedule_establish_operation(
                self_person_ref, operation_id, intent_fingerprint, subject_native_ref,
                schedule_ref, material_state_ref, created_at
            ) VALUES (
                requested_self_person_ref, normalized_operation_id, requested_intent_fingerprint,
                requested_subject_native_ref, requested_schedule_ref, requested_material_state_ref,
                recorded_at
            );
            RETURN QUERY SELECT requested_subject_native_ref, requested_schedule_ref, requested_material_state_ref, recorded_at, false;
        END;
        $function$
        """
    )

    _execute(
        r"""
        CREATE OR REPLACE FUNCTION dante.revise_self_schedule_placement(
            requested_self_person_ref uuid,
            requested_operation_id text,
            requested_intent_fingerprint text,
            requested_schedule_ref uuid,
            requested_expected_material_state_ref uuid,
            requested_material_state_ref uuid,
            requested_payload jsonb
        )
        RETURNS TABLE(
            schedule_ref uuid,
            previous_material_state_ref uuid,
            material_state_ref uuid,
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
            recorded_at timestamptz;
            current_material_state_ref uuid;
            current_from_at timestamptz;
            subject_ref uuid;
            existing_fingerprint text;
            existing_schedule_ref uuid;
            existing_expected_material_state_ref uuid;
            existing_material_state_ref uuid;
            existing_created_at timestamptz;
        BEGIN
            IF normalized_operation_id = '' OR char_length(normalized_operation_id) > 200 THEN
                RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT='ck_schedule_revision_operation_operation_id', MESSAGE='Schedule revision operation id rejected';
            END IF;
            IF requested_intent_fingerprint !~ '^[0-9a-f]{64}$' THEN
                RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT='ck_schedule_revision_operation_fingerprint', MESSAGE='Schedule revision fingerprint rejected';
            END IF;
            IF uuid_extract_version(requested_schedule_ref) IS DISTINCT FROM 7
               OR uuid_extract_version(requested_expected_material_state_ref) IS DISTINCT FROM 7
               OR uuid_extract_version(requested_material_state_ref) IS DISTINCT FROM 7 THEN
                RAISE EXCEPTION USING ERRCODE='23514', MESSAGE='Schedule revision reference rejected';
            END IF;

            PERFORM pg_advisory_xact_lock(hashtextextended(requested_schedule_ref::text, 0));
            SELECT operation.intent_fingerprint,
                   operation.schedule_ref,
                   operation.expected_material_state_ref,
                   operation.material_state_ref,
                   operation.created_at
              INTO existing_fingerprint,
                   existing_schedule_ref,
                   existing_expected_material_state_ref,
                   existing_material_state_ref,
                   existing_created_at
              FROM dante.schedule_revision_operation AS operation
             WHERE operation.self_person_ref = requested_self_person_ref
               AND operation.operation_id = normalized_operation_id;
            IF FOUND THEN
                IF existing_fingerprint <> requested_intent_fingerprint
                   OR existing_schedule_ref <> requested_schedule_ref
                   OR existing_expected_material_state_ref <> requested_expected_material_state_ref THEN
                    RAISE EXCEPTION USING ERRCODE='23505', CONSTRAINT='pk_schedule_revision_operation', MESSAGE='Schedule revision operation id reused with different intent';
                END IF;
                IF dante.schedule_placement_payload_json(existing_schedule_ref, existing_material_state_ref) IS NULL THEN
                    RAISE EXCEPTION USING ERRCODE='XX001', MESSAGE='Schedule revision receipt lost canonical placement state';
                END IF;
                RETURN QUERY SELECT existing_schedule_ref, existing_expected_material_state_ref, existing_material_state_ref, existing_created_at, true;
                RETURN;
            END IF;

            SELECT schedule_row.subject_native_ref
              INTO subject_ref
              FROM dante.schedule AS schedule_row
              JOIN dante.native_address AS address
                ON address.native_ref=schedule_row.subject_native_ref
             WHERE schedule_row.schedule_ref=requested_schedule_ref
               AND (
                   (address.owner_family='activity' AND EXISTS (
                       SELECT 1 FROM dante.activity_intention AS intention
                        WHERE intention.activity_ref=schedule_row.subject_native_ref
                          AND intention.self_person_ref=requested_self_person_ref
                   ))
                   OR
                   (address.owner_family='event' AND EXISTS (
                       SELECT 1 FROM dante.event_expectation AS expectation
                        WHERE expectation.event_ref=schedule_row.subject_native_ref
                          AND expectation.self_person_ref=requested_self_person_ref
                   ))
               );
            IF NOT FOUND THEN
                RAISE EXCEPTION USING ERRCODE='23503', CONSTRAINT='schedule_revision_schedule_not_found', MESSAGE='Schedule revision self scope rejected';
            END IF;

            SELECT current.material_state_ref
              INTO current_material_state_ref
              FROM dante.scoped_current_material_state AS current
              JOIN dante.schedule_placement_state AS placement
                ON placement.material_state_ref = current.material_state_ref
               AND placement.schedule_ref = requested_schedule_ref
             WHERE current.scoped_owner_ref = requested_schedule_ref
               AND current.facet_code = 'schedule.placement'
             FOR UPDATE OF current;
            IF NOT FOUND OR current_material_state_ref IS DISTINCT FROM requested_expected_material_state_ref THEN
                RAISE EXCEPTION USING ERRCODE='23505', CONSTRAINT='schedule_revision_expected_state', MESSAGE='Schedule revision basis is stale';
            END IF;
            SELECT history.current_from_at
              INTO current_from_at
              FROM dante.schedule_placement_current_history AS history
             WHERE history.schedule_ref = requested_schedule_ref
               AND history.material_state_ref = current_material_state_ref
               AND history.current_until_at IS NULL
             FOR UPDATE;
            IF NOT FOUND THEN
                RAISE EXCEPTION USING ERRCODE='XX001', MESSAGE='Schedule current binding lost its open history episode';
            END IF;

            PERFORM dante.assert_schedule_placement_hard_admissible(
                subject_ref,
                requested_payload
            );

            recorded_at := GREATEST(clock_timestamp(), current_from_at + interval '1 microsecond');
            PERFORM dante.insert_schedule_placement_payload(requested_material_state_ref, requested_schedule_ref, requested_payload);
            UPDATE dante.schedule_placement_current_history AS history
               SET current_until_at = recorded_at
             WHERE history.schedule_ref = requested_schedule_ref
               AND history.material_state_ref = current_material_state_ref
               AND history.current_until_at IS NULL;
            UPDATE dante.scoped_current_material_state AS current
               SET material_state_ref = requested_material_state_ref
             WHERE current.scoped_owner_ref = requested_schedule_ref
               AND current.facet_code = 'schedule.placement'
               AND current.material_state_ref = current_material_state_ref;
            INSERT INTO dante.schedule_placement_current_history(schedule_ref, material_state_ref, current_from_at, current_until_at)
            VALUES (requested_schedule_ref, requested_material_state_ref, recorded_at, NULL);
            INSERT INTO dante.schedule_revision_operation(
                self_person_ref, operation_id, intent_fingerprint, schedule_ref,
                expected_material_state_ref, material_state_ref, created_at
            ) VALUES (
                requested_self_person_ref, normalized_operation_id, requested_intent_fingerprint,
                requested_schedule_ref, requested_expected_material_state_ref,
                requested_material_state_ref, recorded_at
            );
            RETURN QUERY SELECT requested_schedule_ref, requested_expected_material_state_ref, requested_material_state_ref, recorded_at, false;
        END;
        $function$
        """
    )


def downgrade() -> None:
    """Fail closed rather than silently re-enable hard-constraint bypass."""
    raise RuntimeError(
        "B04-F Schedule hard-constraint guard downgrade is intentionally refused; use a reviewed forward migration"
    )
