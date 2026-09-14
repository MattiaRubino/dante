"""Resolve B02 Schedule PL/pgSQL output-column ambiguity.

Revision ID: 20260914_24
Revises: 20260914_23
Create Date: 2026-09-14
"""

from __future__ import annotations

from alembic import op

revision = "20260914_24"
down_revision = "20260914_23"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Qualify history columns under strict PL/pgSQL ambiguity handling."""
    op.execute(
        """
        CREATE OR REPLACE FUNCTION dante.revise_self_floating_schedule(
                        requested_self_person_ref uuid,
                        requested_operation_id text,
                        requested_intent_fingerprint text,
                        requested_schedule_ref uuid,
                        requested_expected_material_state_ref uuid,
                        requested_material_state_ref uuid,
                        requested_starts_local_at timestamp without time zone,
                        requested_ends_local_at timestamp without time zone
                    )
                    RETURNS TABLE(
                        schedule_ref uuid,
                        previous_material_state_ref uuid,
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
                    #variable_conflict error
                    DECLARE
                        normalized_operation_id text := btrim(requested_operation_id);
                        recorded_at timestamptz;
                        current_material_state_ref uuid;
                        current_from_at timestamptz;
                        existing_fingerprint text;
                        existing_schedule_ref uuid;
                        existing_expected_material_state_ref uuid;
                        existing_material_state_ref uuid;
                        existing_created_at timestamptz;
                        existing_starts_local_at timestamp without time zone;
                        existing_ends_local_at timestamp without time zone;
                    BEGIN
                        IF normalized_operation_id = ''
                           OR char_length(normalized_operation_id) > 200 THEN
                            RAISE EXCEPTION USING
                                ERRCODE='23514',
                                CONSTRAINT='ck_schedule_revision_operation_operation_id',
                                MESSAGE='Schedule revision operation id rejected';
                        END IF;
                        IF requested_intent_fingerprint !~ '^[0-9a-f]{64}$' THEN
                            RAISE EXCEPTION USING
                                ERRCODE='23514',
                                CONSTRAINT='ck_schedule_revision_operation_fingerprint',
                                MESSAGE='Schedule revision fingerprint rejected';
                        END IF;
                        IF uuid_extract_version(requested_schedule_ref) IS DISTINCT FROM 7
                           OR uuid_extract_version(
                               requested_expected_material_state_ref
                           ) IS DISTINCT FROM 7
                           OR uuid_extract_version(
                               requested_material_state_ref
                           ) IS DISTINCT FROM 7 THEN
                            RAISE EXCEPTION USING
                                ERRCODE='23514',
                                MESSAGE='Schedule revision reference rejected',
                                DETAIL='Schedule and placement references must be application-issued UUIDv7 values';
                        END IF;
                        IF requested_starts_local_at IS NULL
                           OR requested_ends_local_at IS NULL
                           OR NOT isfinite(requested_starts_local_at)
                           OR NOT isfinite(requested_ends_local_at)
                           OR requested_ends_local_at <= requested_starts_local_at
                           OR requested_starts_local_at::date
                              <> requested_ends_local_at::date THEN
                            RAISE EXCEPTION USING
                                ERRCODE='23514',
                                CONSTRAINT='ck_schedule_placement_floating_local_state_interval_order',
                                MESSAGE='Floating-local Schedule revision interval rejected';
                        END IF;
        
                        PERFORM pg_advisory_xact_lock(
                            hashtextextended(requested_schedule_ref::text, 0)
                        );
        
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
                               OR existing_expected_material_state_ref
                                  <> requested_expected_material_state_ref THEN
                                RAISE EXCEPTION USING
                                    ERRCODE='23505',
                                    CONSTRAINT='pk_schedule_revision_operation',
                                    MESSAGE='Schedule revision operation id reused with different intent';
                            END IF;
        
                            SELECT payload.starts_local_at, payload.ends_local_at
                              INTO existing_starts_local_at, existing_ends_local_at
                              FROM dante.schedule_placement_state AS placement
                              JOIN dante.schedule_placement_floating_local_state AS payload
                                ON payload.material_state_ref = placement.material_state_ref
                             WHERE placement.schedule_ref = existing_schedule_ref
                               AND placement.material_state_ref = existing_material_state_ref
                               AND placement.temporal_form_code = 'floating_local'
                               AND payload.extent_code = 'interval';
                            IF NOT FOUND THEN
                                RAISE EXCEPTION USING
                                    ERRCODE='XX001',
                                    MESSAGE='Schedule revision receipt lost canonical placement state';
                            END IF;
                            IF existing_starts_local_at
                                  IS DISTINCT FROM requested_starts_local_at
                               OR existing_ends_local_at
                                  IS DISTINCT FROM requested_ends_local_at THEN
                                RAISE EXCEPTION USING
                                    ERRCODE='23505',
                                    CONSTRAINT='pk_schedule_revision_operation',
                                    MESSAGE='Schedule revision operation id reused with different placement';
                            END IF;
        
                            RETURN QUERY
                            SELECT existing_schedule_ref,
                                   existing_expected_material_state_ref,
                                   existing_material_state_ref,
                                   existing_starts_local_at,
                                   existing_ends_local_at,
                                   existing_created_at,
                                   true;
                            RETURN;
                        END IF;
        
                        IF NOT EXISTS (
                            SELECT 1
                              FROM dante.schedule AS schedule
                              JOIN dante.activity_intention AS intention
                                ON intention.activity_ref = schedule.subject_native_ref
                             WHERE schedule.schedule_ref = requested_schedule_ref
                               AND intention.self_person_ref = requested_self_person_ref
                        ) THEN
                            RAISE EXCEPTION USING
                                ERRCODE='23503',
                                CONSTRAINT='schedule_revision_schedule_not_found',
                                MESSAGE='Schedule revision self scope rejected';
                        END IF;
        
                        SELECT current.material_state_ref
                          INTO current_material_state_ref
                          FROM dante.scoped_current_material_state AS current
                          JOIN dante.schedule_placement_state AS placement
                            ON placement.material_state_ref = current.material_state_ref
                           AND placement.schedule_ref = requested_schedule_ref
                           AND placement.temporal_form_code = 'floating_local'
                          JOIN dante.schedule_placement_floating_local_state AS payload
                            ON payload.material_state_ref = placement.material_state_ref
                           AND payload.extent_code = 'interval'
                         WHERE current.scoped_owner_ref = requested_schedule_ref
                           AND current.facet_code = 'schedule.placement'
                         FOR UPDATE OF current;
                        IF NOT FOUND THEN
                            RAISE EXCEPTION USING
                                ERRCODE='23503',
                                CONSTRAINT='schedule_revision_schedule_not_found',
                                MESSAGE='Schedule has no current accepted placement';
                        END IF;
                        IF current_material_state_ref
                              IS DISTINCT FROM requested_expected_material_state_ref THEN
                            RAISE EXCEPTION USING
                                ERRCODE='23505',
                                CONSTRAINT='schedule_revision_expected_state',
                                MESSAGE='Schedule revision basis is stale';
                        END IF;
        
                        SELECT history.current_from_at
                          INTO current_from_at
                          FROM dante.schedule_placement_current_history AS history
                         WHERE history.schedule_ref = requested_schedule_ref
                           AND history.material_state_ref = current_material_state_ref
                           AND history.current_until_at IS NULL
                         FOR UPDATE;
                        IF NOT FOUND THEN
                            RAISE EXCEPTION USING
                                ERRCODE='XX001',
                                MESSAGE='Schedule current binding lost its open history episode';
                        END IF;
        
                        recorded_at := GREATEST(
                            clock_timestamp(),
                            current_from_at + interval '1 microsecond'
                        );
        
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
        
                        UPDATE dante.schedule_placement_current_history AS history
                           SET current_until_at = recorded_at
                         WHERE history.schedule_ref = requested_schedule_ref
                           AND history.material_state_ref = current_material_state_ref
                           AND history.current_until_at IS NULL;
        
                        UPDATE dante.scoped_current_material_state
                           SET material_state_ref = requested_material_state_ref
                         WHERE scoped_owner_ref = requested_schedule_ref
                           AND facet_code = 'schedule.placement';
        
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
        
                        INSERT INTO dante.schedule_revision_operation(
                            self_person_ref,
                            operation_id,
                            intent_fingerprint,
                            schedule_ref,
                            expected_material_state_ref,
                            material_state_ref,
                            created_at
                        ) VALUES (
                            requested_self_person_ref,
                            normalized_operation_id,
                            requested_intent_fingerprint,
                            requested_schedule_ref,
                            requested_expected_material_state_ref,
                            requested_material_state_ref,
                            recorded_at
                        );
        
                        RETURN QUERY
                        SELECT requested_schedule_ref,
                               requested_expected_material_state_ref,
                               requested_material_state_ref,
                               requested_starts_local_at,
                               requested_ends_local_at,
                               recorded_at,
                               false;
                    END;
                    $function$
        """
    )

    op.execute(
        """
        CREATE OR REPLACE FUNCTION dante.unschedule_self_schedule(
                        requested_self_person_ref uuid,
                        requested_operation_id text,
                        requested_intent_fingerprint text,
                        requested_schedule_ref uuid,
                        requested_expected_material_state_ref uuid
                    )
                    RETURNS TABLE(
                        schedule_ref uuid,
                        previous_material_state_ref uuid,
                        unschedule_operation_id text,
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
                        recorded_at timestamptz;
                        current_material_state_ref uuid;
                        current_from_at timestamptz;
                        existing_fingerprint text;
                        existing_schedule_ref uuid;
                        existing_expected_material_state_ref uuid;
                        existing_created_at timestamptz;
                    BEGIN
                        IF normalized_operation_id = ''
                           OR char_length(normalized_operation_id) > 200 THEN
                            RAISE EXCEPTION USING
                                ERRCODE='23514',
                                CONSTRAINT='ck_schedule_unschedule_operation_operation_id',
                                MESSAGE='Schedule unschedule operation id rejected';
                        END IF;
                        IF requested_intent_fingerprint !~ '^[0-9a-f]{64}$' THEN
                            RAISE EXCEPTION USING
                                ERRCODE='23514',
                                CONSTRAINT='ck_schedule_unschedule_operation_fingerprint',
                                MESSAGE='Schedule unschedule fingerprint rejected';
                        END IF;
                        IF uuid_extract_version(requested_schedule_ref) IS DISTINCT FROM 7
                           OR uuid_extract_version(
                               requested_expected_material_state_ref
                           ) IS DISTINCT FROM 7 THEN
                            RAISE EXCEPTION USING
                                ERRCODE='23514',
                                MESSAGE='Schedule unschedule reference rejected',
                                DETAIL='Schedule and expected placement references must be application-issued UUIDv7 values';
                        END IF;
        
                        PERFORM pg_advisory_xact_lock(
                            hashtextextended(requested_schedule_ref::text, 0)
                        );
        
                        SELECT operation.intent_fingerprint,
                               operation.schedule_ref,
                               operation.expected_material_state_ref,
                               operation.created_at
                          INTO existing_fingerprint,
                               existing_schedule_ref,
                               existing_expected_material_state_ref,
                               existing_created_at
                          FROM dante.schedule_unschedule_operation AS operation
                         WHERE operation.self_person_ref = requested_self_person_ref
                           AND operation.operation_id = normalized_operation_id;
        
                        IF FOUND THEN
                            IF existing_fingerprint <> requested_intent_fingerprint
                               OR existing_schedule_ref <> requested_schedule_ref
                               OR existing_expected_material_state_ref
                                  <> requested_expected_material_state_ref THEN
                                RAISE EXCEPTION USING
                                    ERRCODE='23505',
                                    CONSTRAINT='pk_schedule_unschedule_operation',
                                    MESSAGE='Schedule unschedule operation id reused with different intent';
                            END IF;
                            RETURN QUERY
                            SELECT existing_schedule_ref,
                                   existing_expected_material_state_ref,
                                   normalized_operation_id,
                                   existing_created_at,
                                   true;
                            RETURN;
                        END IF;
        
                        IF NOT EXISTS (
                            SELECT 1
                              FROM dante.schedule AS schedule
                              JOIN dante.activity_intention AS intention
                                ON intention.activity_ref = schedule.subject_native_ref
                             WHERE schedule.schedule_ref = requested_schedule_ref
                               AND intention.self_person_ref = requested_self_person_ref
                        ) THEN
                            RAISE EXCEPTION USING
                                ERRCODE='23503',
                                CONSTRAINT='schedule_unschedule_schedule_not_found',
                                MESSAGE='Schedule unschedule self scope rejected';
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
                        IF NOT FOUND THEN
                            RAISE EXCEPTION USING
                                ERRCODE='23505',
                                CONSTRAINT='schedule_unschedule_expected_state',
                                MESSAGE='Schedule has no current accepted placement';
                        END IF;
                        IF current_material_state_ref
                              IS DISTINCT FROM requested_expected_material_state_ref THEN
                            RAISE EXCEPTION USING
                                ERRCODE='23505',
                                CONSTRAINT='schedule_unschedule_expected_state',
                                MESSAGE='Schedule unschedule basis is stale';
                        END IF;
        
                        SELECT history.current_from_at
                          INTO current_from_at
                          FROM dante.schedule_placement_current_history AS history
                         WHERE history.schedule_ref = requested_schedule_ref
                           AND history.material_state_ref = current_material_state_ref
                           AND history.current_until_at IS NULL
                         FOR UPDATE;
                        IF NOT FOUND THEN
                            RAISE EXCEPTION USING
                                ERRCODE='XX001',
                                MESSAGE='Schedule current binding lost its open history episode';
                        END IF;
        
                        recorded_at := GREATEST(
                            clock_timestamp(),
                            current_from_at + interval '1 microsecond'
                        );
        
                        UPDATE dante.schedule_placement_current_history AS history
                           SET current_until_at = recorded_at
                         WHERE history.schedule_ref = requested_schedule_ref
                           AND history.material_state_ref = current_material_state_ref
                           AND history.current_until_at IS NULL;
        
                        DELETE FROM dante.scoped_current_material_state
                         WHERE scoped_owner_ref = requested_schedule_ref
                           AND facet_code = 'schedule.placement'
                           AND material_state_ref = current_material_state_ref;
        
                        INSERT INTO dante.schedule_unschedule_operation(
                            self_person_ref,
                            operation_id,
                            intent_fingerprint,
                            schedule_ref,
                            expected_material_state_ref,
                            created_at
                        ) VALUES (
                            requested_self_person_ref,
                            normalized_operation_id,
                            requested_intent_fingerprint,
                            requested_schedule_ref,
                            requested_expected_material_state_ref,
                            recorded_at
                        );
        
                        RETURN QUERY
                        SELECT requested_schedule_ref,
                               requested_expected_material_state_ref,
                               normalized_operation_id,
                               recorded_at,
                               false;
                    END;
                    $function$
        """
    )

    op.execute(
        """
        CREATE OR REPLACE FUNCTION dante.undo_self_schedule_unschedule(
                        requested_self_person_ref uuid,
                        requested_operation_id text,
                        requested_intent_fingerprint text,
                        requested_schedule_ref uuid,
                        requested_unschedule_operation_id text,
                        requested_material_state_ref uuid
                    )
                    RETURNS TABLE(
                        schedule_ref uuid,
                        restored_from_material_state_ref uuid,
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
                    #variable_conflict error
                    DECLARE
                        normalized_operation_id text := btrim(requested_operation_id);
                        normalized_unschedule_operation_id text :=
                            btrim(requested_unschedule_operation_id);
                        recorded_at timestamptz;
                        unscheduled_at timestamptz;
                        original_material_state_ref uuid;
                        original_starts_local_at timestamp without time zone;
                        original_ends_local_at timestamp without time zone;
                        existing_fingerprint text;
                        existing_schedule_ref uuid;
                        existing_unschedule_operation_id text;
                        existing_restored_from_material_state_ref uuid;
                        existing_material_state_ref uuid;
                        existing_created_at timestamptz;
                        existing_starts_local_at timestamp without time zone;
                        existing_ends_local_at timestamp without time zone;
                    BEGIN
                        IF normalized_operation_id = ''
                           OR char_length(normalized_operation_id) > 200 THEN
                            RAISE EXCEPTION USING
                                ERRCODE='23514',
                                CONSTRAINT='ck_schedule_unschedule_undo_operation_operation_id',
                                MESSAGE='Schedule undo operation id rejected';
                        END IF;
                        IF normalized_unschedule_operation_id = ''
                           OR char_length(normalized_unschedule_operation_id) > 200 THEN
                            RAISE EXCEPTION USING
                                ERRCODE='23514',
                                CONSTRAINT='ck_schedule_unschedule_undo_operation_unschedule_operation_id',
                                MESSAGE='Schedule undo basis rejected';
                        END IF;
                        IF requested_intent_fingerprint !~ '^[0-9a-f]{64}$' THEN
                            RAISE EXCEPTION USING
                                ERRCODE='23514',
                                CONSTRAINT='ck_schedule_unschedule_undo_operation_fingerprint',
                                MESSAGE='Schedule undo fingerprint rejected';
                        END IF;
                        IF uuid_extract_version(requested_schedule_ref) IS DISTINCT FROM 7
                           OR uuid_extract_version(
                               requested_material_state_ref
                           ) IS DISTINCT FROM 7 THEN
                            RAISE EXCEPTION USING
                                ERRCODE='23514',
                                MESSAGE='Schedule undo reference rejected',
                                DETAIL='Schedule and new placement references must be application-issued UUIDv7 values';
                        END IF;
        
                        PERFORM pg_advisory_xact_lock(
                            hashtextextended(requested_schedule_ref::text, 0)
                        );
        
                        SELECT operation.intent_fingerprint,
                               operation.schedule_ref,
                               operation.unschedule_operation_id,
                               operation.restored_from_material_state_ref,
                               operation.material_state_ref,
                               operation.created_at
                          INTO existing_fingerprint,
                               existing_schedule_ref,
                               existing_unschedule_operation_id,
                               existing_restored_from_material_state_ref,
                               existing_material_state_ref,
                               existing_created_at
                          FROM dante.schedule_unschedule_undo_operation AS operation
                         WHERE operation.self_person_ref = requested_self_person_ref
                           AND operation.operation_id = normalized_operation_id;
        
                        IF FOUND THEN
                            IF existing_fingerprint <> requested_intent_fingerprint
                               OR existing_schedule_ref <> requested_schedule_ref
                               OR existing_unschedule_operation_id
                                  <> normalized_unschedule_operation_id THEN
                                RAISE EXCEPTION USING
                                    ERRCODE='23505',
                                    CONSTRAINT='pk_schedule_unschedule_undo_operation',
                                    MESSAGE='Schedule undo operation id reused with different intent';
                            END IF;
        
                            SELECT payload.starts_local_at, payload.ends_local_at
                              INTO existing_starts_local_at, existing_ends_local_at
                              FROM dante.schedule_placement_state AS placement
                              JOIN dante.schedule_placement_floating_local_state AS payload
                                ON payload.material_state_ref = placement.material_state_ref
                             WHERE placement.schedule_ref = existing_schedule_ref
                               AND placement.material_state_ref = existing_material_state_ref
                               AND placement.temporal_form_code = 'floating_local'
                               AND payload.extent_code = 'interval';
                            IF NOT FOUND THEN
                                RAISE EXCEPTION USING
                                    ERRCODE='XX001',
                                    MESSAGE='Schedule undo receipt lost canonical placement state';
                            END IF;
        
                            RETURN QUERY
                            SELECT existing_schedule_ref,
                                   existing_restored_from_material_state_ref,
                                   existing_material_state_ref,
                                   existing_starts_local_at,
                                   existing_ends_local_at,
                                   existing_created_at,
                                   true;
                            RETURN;
                        END IF;
        
                        IF NOT EXISTS (
                            SELECT 1
                              FROM dante.schedule AS schedule
                              JOIN dante.activity_intention AS intention
                                ON intention.activity_ref = schedule.subject_native_ref
                             WHERE schedule.schedule_ref = requested_schedule_ref
                               AND intention.self_person_ref = requested_self_person_ref
                        ) THEN
                            RAISE EXCEPTION USING
                                ERRCODE='23503',
                                CONSTRAINT='schedule_unschedule_undo_not_found',
                                MESSAGE='Schedule undo self scope rejected';
                        END IF;
        
                        SELECT operation.expected_material_state_ref,
                               operation.created_at
                          INTO original_material_state_ref,
                               unscheduled_at
                          FROM dante.schedule_unschedule_operation AS operation
                         WHERE operation.self_person_ref = requested_self_person_ref
                           AND operation.operation_id =
                               normalized_unschedule_operation_id
                           AND operation.schedule_ref = requested_schedule_ref;
                        IF NOT FOUND THEN
                            RAISE EXCEPTION USING
                                ERRCODE='23503',
                                CONSTRAINT='schedule_unschedule_undo_not_found',
                                MESSAGE='Schedule undo basis was not found';
                        END IF;
        
                        IF EXISTS (
                            SELECT 1
                              FROM dante.scoped_current_material_state
                             WHERE scoped_owner_ref = requested_schedule_ref
                               AND facet_code = 'schedule.placement'
                        ) OR EXISTS (
                            SELECT 1
                              FROM dante.schedule_placement_current_history AS history
                             WHERE history.schedule_ref = requested_schedule_ref
                               AND history.current_until_at IS NULL
                        ) OR NOT EXISTS (
                            SELECT 1
                              FROM dante.schedule_placement_current_history AS history
                             WHERE history.schedule_ref = requested_schedule_ref
                               AND history.material_state_ref = original_material_state_ref
                               AND history.current_until_at = unscheduled_at
                        ) OR EXISTS (
                            SELECT 1
                              FROM dante.schedule_placement_current_history AS history
                             WHERE history.schedule_ref = requested_schedule_ref
                               AND history.current_from_at >= unscheduled_at
                        ) THEN
                            RAISE EXCEPTION USING
                                ERRCODE='23505',
                                CONSTRAINT='schedule_unschedule_undo_expected_state',
                                MESSAGE='Schedule undo basis is stale';
                        END IF;
        
                        SELECT payload.starts_local_at, payload.ends_local_at
                          INTO original_starts_local_at, original_ends_local_at
                          FROM dante.schedule_placement_state AS placement
                          JOIN dante.schedule_placement_floating_local_state AS payload
                            ON payload.material_state_ref = placement.material_state_ref
                         WHERE placement.schedule_ref = requested_schedule_ref
                           AND placement.material_state_ref =
                               original_material_state_ref
                           AND placement.temporal_form_code = 'floating_local'
                           AND payload.extent_code = 'interval';
                        IF NOT FOUND THEN
                            RAISE EXCEPTION USING
                                ERRCODE='23514',
                                CONSTRAINT='schedule_unschedule_undo_unsupported_form',
                                MESSAGE='Schedule undo placement form is not activated';
                        END IF;
        
                        recorded_at := GREATEST(
                            clock_timestamp(),
                            unscheduled_at + interval '1 microsecond'
                        );
        
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
                            original_starts_local_at,
                            original_ends_local_at
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
        
                        INSERT INTO dante.schedule_unschedule_undo_operation(
                            self_person_ref,
                            operation_id,
                            intent_fingerprint,
                            schedule_ref,
                            unschedule_operation_id,
                            restored_from_material_state_ref,
                            material_state_ref,
                            created_at
                        ) VALUES (
                            requested_self_person_ref,
                            normalized_operation_id,
                            requested_intent_fingerprint,
                            requested_schedule_ref,
                            normalized_unschedule_operation_id,
                            original_material_state_ref,
                            requested_material_state_ref,
                            recorded_at
                        );
        
                        RETURN QUERY
                        SELECT requested_schedule_ref,
                               original_material_state_ref,
                               requested_material_state_ref,
                               original_starts_local_at,
                               original_ends_local_at,
                               recorded_at,
                               false;
                    END;
                    $function$
        """
    )


def downgrade() -> None:
    """Restore the immediately preceding function definitions."""
    op.execute(
        """
        CREATE FUNCTION dante.revise_self_floating_schedule(
                        requested_self_person_ref uuid,
                        requested_operation_id text,
                        requested_intent_fingerprint text,
                        requested_schedule_ref uuid,
                        requested_expected_material_state_ref uuid,
                        requested_material_state_ref uuid,
                        requested_starts_local_at timestamp without time zone,
                        requested_ends_local_at timestamp without time zone
                    )
                    RETURNS TABLE(
                        schedule_ref uuid,
                        previous_material_state_ref uuid,
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
                        recorded_at timestamptz;
                        current_material_state_ref uuid;
                        current_from_at timestamptz;
                        existing_fingerprint text;
                        existing_schedule_ref uuid;
                        existing_expected_material_state_ref uuid;
                        existing_material_state_ref uuid;
                        existing_created_at timestamptz;
                        existing_starts_local_at timestamp without time zone;
                        existing_ends_local_at timestamp without time zone;
                    BEGIN
                        IF normalized_operation_id = ''
                           OR char_length(normalized_operation_id) > 200 THEN
                            RAISE EXCEPTION USING
                                ERRCODE='23514',
                                CONSTRAINT='ck_schedule_revision_operation_operation_id',
                                MESSAGE='Schedule revision operation id rejected';
                        END IF;
                        IF requested_intent_fingerprint !~ '^[0-9a-f]{64}$' THEN
                            RAISE EXCEPTION USING
                                ERRCODE='23514',
                                CONSTRAINT='ck_schedule_revision_operation_fingerprint',
                                MESSAGE='Schedule revision fingerprint rejected';
                        END IF;
                        IF uuid_extract_version(requested_schedule_ref) IS DISTINCT FROM 7
                           OR uuid_extract_version(
                               requested_expected_material_state_ref
                           ) IS DISTINCT FROM 7
                           OR uuid_extract_version(
                               requested_material_state_ref
                           ) IS DISTINCT FROM 7 THEN
                            RAISE EXCEPTION USING
                                ERRCODE='23514',
                                MESSAGE='Schedule revision reference rejected',
                                DETAIL='Schedule and placement references must be application-issued UUIDv7 values';
                        END IF;
                        IF requested_starts_local_at IS NULL
                           OR requested_ends_local_at IS NULL
                           OR NOT isfinite(requested_starts_local_at)
                           OR NOT isfinite(requested_ends_local_at)
                           OR requested_ends_local_at <= requested_starts_local_at
                           OR requested_starts_local_at::date
                              <> requested_ends_local_at::date THEN
                            RAISE EXCEPTION USING
                                ERRCODE='23514',
                                CONSTRAINT='ck_schedule_placement_floating_local_state_interval_order',
                                MESSAGE='Floating-local Schedule revision interval rejected';
                        END IF;
        
                        PERFORM pg_advisory_xact_lock(
                            hashtextextended(requested_schedule_ref::text, 0)
                        );
        
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
                               OR existing_expected_material_state_ref
                                  <> requested_expected_material_state_ref THEN
                                RAISE EXCEPTION USING
                                    ERRCODE='23505',
                                    CONSTRAINT='pk_schedule_revision_operation',
                                    MESSAGE='Schedule revision operation id reused with different intent';
                            END IF;
        
                            SELECT payload.starts_local_at, payload.ends_local_at
                              INTO existing_starts_local_at, existing_ends_local_at
                              FROM dante.schedule_placement_state AS placement
                              JOIN dante.schedule_placement_floating_local_state AS payload
                                ON payload.material_state_ref = placement.material_state_ref
                             WHERE placement.schedule_ref = existing_schedule_ref
                               AND placement.material_state_ref = existing_material_state_ref
                               AND placement.temporal_form_code = 'floating_local'
                               AND payload.extent_code = 'interval';
                            IF NOT FOUND THEN
                                RAISE EXCEPTION USING
                                    ERRCODE='XX001',
                                    MESSAGE='Schedule revision receipt lost canonical placement state';
                            END IF;
                            IF existing_starts_local_at
                                  IS DISTINCT FROM requested_starts_local_at
                               OR existing_ends_local_at
                                  IS DISTINCT FROM requested_ends_local_at THEN
                                RAISE EXCEPTION USING
                                    ERRCODE='23505',
                                    CONSTRAINT='pk_schedule_revision_operation',
                                    MESSAGE='Schedule revision operation id reused with different placement';
                            END IF;
        
                            RETURN QUERY
                            SELECT existing_schedule_ref,
                                   existing_expected_material_state_ref,
                                   existing_material_state_ref,
                                   existing_starts_local_at,
                                   existing_ends_local_at,
                                   existing_created_at,
                                   true;
                            RETURN;
                        END IF;
        
                        IF NOT EXISTS (
                            SELECT 1
                              FROM dante.schedule AS schedule
                              JOIN dante.activity_intention AS intention
                                ON intention.activity_ref = schedule.subject_native_ref
                             WHERE schedule.schedule_ref = requested_schedule_ref
                               AND intention.self_person_ref = requested_self_person_ref
                        ) THEN
                            RAISE EXCEPTION USING
                                ERRCODE='23503',
                                CONSTRAINT='schedule_revision_schedule_not_found',
                                MESSAGE='Schedule revision self scope rejected';
                        END IF;
        
                        SELECT current.material_state_ref
                          INTO current_material_state_ref
                          FROM dante.scoped_current_material_state AS current
                          JOIN dante.schedule_placement_state AS placement
                            ON placement.material_state_ref = current.material_state_ref
                           AND placement.schedule_ref = requested_schedule_ref
                           AND placement.temporal_form_code = 'floating_local'
                          JOIN dante.schedule_placement_floating_local_state AS payload
                            ON payload.material_state_ref = placement.material_state_ref
                           AND payload.extent_code = 'interval'
                         WHERE current.scoped_owner_ref = requested_schedule_ref
                           AND current.facet_code = 'schedule.placement'
                         FOR UPDATE OF current;
                        IF NOT FOUND THEN
                            RAISE EXCEPTION USING
                                ERRCODE='23503',
                                CONSTRAINT='schedule_revision_schedule_not_found',
                                MESSAGE='Schedule has no current accepted placement';
                        END IF;
                        IF current_material_state_ref
                              IS DISTINCT FROM requested_expected_material_state_ref THEN
                            RAISE EXCEPTION USING
                                ERRCODE='23505',
                                CONSTRAINT='schedule_revision_expected_state',
                                MESSAGE='Schedule revision basis is stale';
                        END IF;
        
                        SELECT history.current_from_at
                          INTO current_from_at
                          FROM dante.schedule_placement_current_history AS history
                         WHERE history.schedule_ref = requested_schedule_ref
                           AND history.material_state_ref = current_material_state_ref
                           AND history.current_until_at IS NULL
                         FOR UPDATE;
                        IF NOT FOUND THEN
                            RAISE EXCEPTION USING
                                ERRCODE='XX001',
                                MESSAGE='Schedule current binding lost its open history episode';
                        END IF;
        
                        recorded_at := GREATEST(
                            clock_timestamp(),
                            current_from_at + interval '1 microsecond'
                        );
        
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
        
                        UPDATE dante.schedule_placement_current_history
                           SET current_until_at = recorded_at
                         WHERE schedule_ref = requested_schedule_ref
                           AND material_state_ref = current_material_state_ref
                           AND current_until_at IS NULL;
        
                        UPDATE dante.scoped_current_material_state
                           SET material_state_ref = requested_material_state_ref
                         WHERE scoped_owner_ref = requested_schedule_ref
                           AND facet_code = 'schedule.placement';
        
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
        
                        INSERT INTO dante.schedule_revision_operation(
                            self_person_ref,
                            operation_id,
                            intent_fingerprint,
                            schedule_ref,
                            expected_material_state_ref,
                            material_state_ref,
                            created_at
                        ) VALUES (
                            requested_self_person_ref,
                            normalized_operation_id,
                            requested_intent_fingerprint,
                            requested_schedule_ref,
                            requested_expected_material_state_ref,
                            requested_material_state_ref,
                            recorded_at
                        );
        
                        RETURN QUERY
                        SELECT requested_schedule_ref,
                               requested_expected_material_state_ref,
                               requested_material_state_ref,
                               requested_starts_local_at,
                               requested_ends_local_at,
                               recorded_at,
                               false;
                    END;
                    $function$
        """
    )

    op.execute(
        """
        CREATE FUNCTION dante.unschedule_self_schedule(
                        requested_self_person_ref uuid,
                        requested_operation_id text,
                        requested_intent_fingerprint text,
                        requested_schedule_ref uuid,
                        requested_expected_material_state_ref uuid
                    )
                    RETURNS TABLE(
                        schedule_ref uuid,
                        previous_material_state_ref uuid,
                        unschedule_operation_id text,
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
                        existing_fingerprint text;
                        existing_schedule_ref uuid;
                        existing_expected_material_state_ref uuid;
                        existing_created_at timestamptz;
                    BEGIN
                        IF normalized_operation_id = ''
                           OR char_length(normalized_operation_id) > 200 THEN
                            RAISE EXCEPTION USING
                                ERRCODE='23514',
                                CONSTRAINT='ck_schedule_unschedule_operation_operation_id',
                                MESSAGE='Schedule unschedule operation id rejected';
                        END IF;
                        IF requested_intent_fingerprint !~ '^[0-9a-f]{64}$' THEN
                            RAISE EXCEPTION USING
                                ERRCODE='23514',
                                CONSTRAINT='ck_schedule_unschedule_operation_fingerprint',
                                MESSAGE='Schedule unschedule fingerprint rejected';
                        END IF;
                        IF uuid_extract_version(requested_schedule_ref) IS DISTINCT FROM 7
                           OR uuid_extract_version(
                               requested_expected_material_state_ref
                           ) IS DISTINCT FROM 7 THEN
                            RAISE EXCEPTION USING
                                ERRCODE='23514',
                                MESSAGE='Schedule unschedule reference rejected',
                                DETAIL='Schedule and expected placement references must be application-issued UUIDv7 values';
                        END IF;
        
                        PERFORM pg_advisory_xact_lock(
                            hashtextextended(requested_schedule_ref::text, 0)
                        );
        
                        SELECT operation.intent_fingerprint,
                               operation.schedule_ref,
                               operation.expected_material_state_ref,
                               operation.created_at
                          INTO existing_fingerprint,
                               existing_schedule_ref,
                               existing_expected_material_state_ref,
                               existing_created_at
                          FROM dante.schedule_unschedule_operation AS operation
                         WHERE operation.self_person_ref = requested_self_person_ref
                           AND operation.operation_id = normalized_operation_id;
        
                        IF FOUND THEN
                            IF existing_fingerprint <> requested_intent_fingerprint
                               OR existing_schedule_ref <> requested_schedule_ref
                               OR existing_expected_material_state_ref
                                  <> requested_expected_material_state_ref THEN
                                RAISE EXCEPTION USING
                                    ERRCODE='23505',
                                    CONSTRAINT='pk_schedule_unschedule_operation',
                                    MESSAGE='Schedule unschedule operation id reused with different intent';
                            END IF;
                            RETURN QUERY
                            SELECT existing_schedule_ref,
                                   existing_expected_material_state_ref,
                                   normalized_operation_id,
                                   existing_created_at,
                                   true;
                            RETURN;
                        END IF;
        
                        IF NOT EXISTS (
                            SELECT 1
                              FROM dante.schedule AS schedule
                              JOIN dante.activity_intention AS intention
                                ON intention.activity_ref = schedule.subject_native_ref
                             WHERE schedule.schedule_ref = requested_schedule_ref
                               AND intention.self_person_ref = requested_self_person_ref
                        ) THEN
                            RAISE EXCEPTION USING
                                ERRCODE='23503',
                                CONSTRAINT='schedule_unschedule_schedule_not_found',
                                MESSAGE='Schedule unschedule self scope rejected';
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
                        IF NOT FOUND THEN
                            RAISE EXCEPTION USING
                                ERRCODE='23505',
                                CONSTRAINT='schedule_unschedule_expected_state',
                                MESSAGE='Schedule has no current accepted placement';
                        END IF;
                        IF current_material_state_ref
                              IS DISTINCT FROM requested_expected_material_state_ref THEN
                            RAISE EXCEPTION USING
                                ERRCODE='23505',
                                CONSTRAINT='schedule_unschedule_expected_state',
                                MESSAGE='Schedule unschedule basis is stale';
                        END IF;
        
                        SELECT history.current_from_at
                          INTO current_from_at
                          FROM dante.schedule_placement_current_history AS history
                         WHERE history.schedule_ref = requested_schedule_ref
                           AND history.material_state_ref = current_material_state_ref
                           AND history.current_until_at IS NULL
                         FOR UPDATE;
                        IF NOT FOUND THEN
                            RAISE EXCEPTION USING
                                ERRCODE='XX001',
                                MESSAGE='Schedule current binding lost its open history episode';
                        END IF;
        
                        recorded_at := GREATEST(
                            clock_timestamp(),
                            current_from_at + interval '1 microsecond'
                        );
        
                        UPDATE dante.schedule_placement_current_history
                           SET current_until_at = recorded_at
                         WHERE schedule_ref = requested_schedule_ref
                           AND material_state_ref = current_material_state_ref
                           AND current_until_at IS NULL;
        
                        DELETE FROM dante.scoped_current_material_state
                         WHERE scoped_owner_ref = requested_schedule_ref
                           AND facet_code = 'schedule.placement'
                           AND material_state_ref = current_material_state_ref;
        
                        INSERT INTO dante.schedule_unschedule_operation(
                            self_person_ref,
                            operation_id,
                            intent_fingerprint,
                            schedule_ref,
                            expected_material_state_ref,
                            created_at
                        ) VALUES (
                            requested_self_person_ref,
                            normalized_operation_id,
                            requested_intent_fingerprint,
                            requested_schedule_ref,
                            requested_expected_material_state_ref,
                            recorded_at
                        );
        
                        RETURN QUERY
                        SELECT requested_schedule_ref,
                               requested_expected_material_state_ref,
                               normalized_operation_id,
                               recorded_at,
                               false;
                    END;
                    $function$
        """
    )

    op.execute(
        """
        CREATE FUNCTION dante.undo_self_schedule_unschedule(
                        requested_self_person_ref uuid,
                        requested_operation_id text,
                        requested_intent_fingerprint text,
                        requested_schedule_ref uuid,
                        requested_unschedule_operation_id text,
                        requested_material_state_ref uuid
                    )
                    RETURNS TABLE(
                        schedule_ref uuid,
                        restored_from_material_state_ref uuid,
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
                        normalized_unschedule_operation_id text :=
                            btrim(requested_unschedule_operation_id);
                        recorded_at timestamptz;
                        unscheduled_at timestamptz;
                        original_material_state_ref uuid;
                        original_starts_local_at timestamp without time zone;
                        original_ends_local_at timestamp without time zone;
                        existing_fingerprint text;
                        existing_schedule_ref uuid;
                        existing_unschedule_operation_id text;
                        existing_restored_from_material_state_ref uuid;
                        existing_material_state_ref uuid;
                        existing_created_at timestamptz;
                        existing_starts_local_at timestamp without time zone;
                        existing_ends_local_at timestamp without time zone;
                    BEGIN
                        IF normalized_operation_id = ''
                           OR char_length(normalized_operation_id) > 200 THEN
                            RAISE EXCEPTION USING
                                ERRCODE='23514',
                                CONSTRAINT='ck_schedule_unschedule_undo_operation_operation_id',
                                MESSAGE='Schedule undo operation id rejected';
                        END IF;
                        IF normalized_unschedule_operation_id = ''
                           OR char_length(normalized_unschedule_operation_id) > 200 THEN
                            RAISE EXCEPTION USING
                                ERRCODE='23514',
                                CONSTRAINT='ck_schedule_unschedule_undo_operation_unschedule_operation_id',
                                MESSAGE='Schedule undo basis rejected';
                        END IF;
                        IF requested_intent_fingerprint !~ '^[0-9a-f]{64}$' THEN
                            RAISE EXCEPTION USING
                                ERRCODE='23514',
                                CONSTRAINT='ck_schedule_unschedule_undo_operation_fingerprint',
                                MESSAGE='Schedule undo fingerprint rejected';
                        END IF;
                        IF uuid_extract_version(requested_schedule_ref) IS DISTINCT FROM 7
                           OR uuid_extract_version(
                               requested_material_state_ref
                           ) IS DISTINCT FROM 7 THEN
                            RAISE EXCEPTION USING
                                ERRCODE='23514',
                                MESSAGE='Schedule undo reference rejected',
                                DETAIL='Schedule and new placement references must be application-issued UUIDv7 values';
                        END IF;
        
                        PERFORM pg_advisory_xact_lock(
                            hashtextextended(requested_schedule_ref::text, 0)
                        );
        
                        SELECT operation.intent_fingerprint,
                               operation.schedule_ref,
                               operation.unschedule_operation_id,
                               operation.restored_from_material_state_ref,
                               operation.material_state_ref,
                               operation.created_at
                          INTO existing_fingerprint,
                               existing_schedule_ref,
                               existing_unschedule_operation_id,
                               existing_restored_from_material_state_ref,
                               existing_material_state_ref,
                               existing_created_at
                          FROM dante.schedule_unschedule_undo_operation AS operation
                         WHERE operation.self_person_ref = requested_self_person_ref
                           AND operation.operation_id = normalized_operation_id;
        
                        IF FOUND THEN
                            IF existing_fingerprint <> requested_intent_fingerprint
                               OR existing_schedule_ref <> requested_schedule_ref
                               OR existing_unschedule_operation_id
                                  <> normalized_unschedule_operation_id THEN
                                RAISE EXCEPTION USING
                                    ERRCODE='23505',
                                    CONSTRAINT='pk_schedule_unschedule_undo_operation',
                                    MESSAGE='Schedule undo operation id reused with different intent';
                            END IF;
        
                            SELECT payload.starts_local_at, payload.ends_local_at
                              INTO existing_starts_local_at, existing_ends_local_at
                              FROM dante.schedule_placement_state AS placement
                              JOIN dante.schedule_placement_floating_local_state AS payload
                                ON payload.material_state_ref = placement.material_state_ref
                             WHERE placement.schedule_ref = existing_schedule_ref
                               AND placement.material_state_ref = existing_material_state_ref
                               AND placement.temporal_form_code = 'floating_local'
                               AND payload.extent_code = 'interval';
                            IF NOT FOUND THEN
                                RAISE EXCEPTION USING
                                    ERRCODE='XX001',
                                    MESSAGE='Schedule undo receipt lost canonical placement state';
                            END IF;
        
                            RETURN QUERY
                            SELECT existing_schedule_ref,
                                   existing_restored_from_material_state_ref,
                                   existing_material_state_ref,
                                   existing_starts_local_at,
                                   existing_ends_local_at,
                                   existing_created_at,
                                   true;
                            RETURN;
                        END IF;
        
                        IF NOT EXISTS (
                            SELECT 1
                              FROM dante.schedule AS schedule
                              JOIN dante.activity_intention AS intention
                                ON intention.activity_ref = schedule.subject_native_ref
                             WHERE schedule.schedule_ref = requested_schedule_ref
                               AND intention.self_person_ref = requested_self_person_ref
                        ) THEN
                            RAISE EXCEPTION USING
                                ERRCODE='23503',
                                CONSTRAINT='schedule_unschedule_undo_not_found',
                                MESSAGE='Schedule undo self scope rejected';
                        END IF;
        
                        SELECT operation.expected_material_state_ref,
                               operation.created_at
                          INTO original_material_state_ref,
                               unscheduled_at
                          FROM dante.schedule_unschedule_operation AS operation
                         WHERE operation.self_person_ref = requested_self_person_ref
                           AND operation.operation_id =
                               normalized_unschedule_operation_id
                           AND operation.schedule_ref = requested_schedule_ref;
                        IF NOT FOUND THEN
                            RAISE EXCEPTION USING
                                ERRCODE='23503',
                                CONSTRAINT='schedule_unschedule_undo_not_found',
                                MESSAGE='Schedule undo basis was not found';
                        END IF;
        
                        IF EXISTS (
                            SELECT 1
                              FROM dante.scoped_current_material_state
                             WHERE scoped_owner_ref = requested_schedule_ref
                               AND facet_code = 'schedule.placement'
                        ) OR EXISTS (
                            SELECT 1
                              FROM dante.schedule_placement_current_history
                             WHERE schedule_ref = requested_schedule_ref
                               AND current_until_at IS NULL
                        ) OR NOT EXISTS (
                            SELECT 1
                              FROM dante.schedule_placement_current_history
                             WHERE schedule_ref = requested_schedule_ref
                               AND material_state_ref = original_material_state_ref
                               AND current_until_at = unscheduled_at
                        ) OR EXISTS (
                            SELECT 1
                              FROM dante.schedule_placement_current_history
                             WHERE schedule_ref = requested_schedule_ref
                               AND current_from_at >= unscheduled_at
                        ) THEN
                            RAISE EXCEPTION USING
                                ERRCODE='23505',
                                CONSTRAINT='schedule_unschedule_undo_expected_state',
                                MESSAGE='Schedule undo basis is stale';
                        END IF;
        
                        SELECT payload.starts_local_at, payload.ends_local_at
                          INTO original_starts_local_at, original_ends_local_at
                          FROM dante.schedule_placement_state AS placement
                          JOIN dante.schedule_placement_floating_local_state AS payload
                            ON payload.material_state_ref = placement.material_state_ref
                         WHERE placement.schedule_ref = requested_schedule_ref
                           AND placement.material_state_ref =
                               original_material_state_ref
                           AND placement.temporal_form_code = 'floating_local'
                           AND payload.extent_code = 'interval';
                        IF NOT FOUND THEN
                            RAISE EXCEPTION USING
                                ERRCODE='23514',
                                CONSTRAINT='schedule_unschedule_undo_unsupported_form',
                                MESSAGE='Schedule undo placement form is not activated';
                        END IF;
        
                        recorded_at := GREATEST(
                            clock_timestamp(),
                            unscheduled_at + interval '1 microsecond'
                        );
        
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
                            original_starts_local_at,
                            original_ends_local_at
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
        
                        INSERT INTO dante.schedule_unschedule_undo_operation(
                            self_person_ref,
                            operation_id,
                            intent_fingerprint,
                            schedule_ref,
                            unschedule_operation_id,
                            restored_from_material_state_ref,
                            material_state_ref,
                            created_at
                        ) VALUES (
                            requested_self_person_ref,
                            normalized_operation_id,
                            requested_intent_fingerprint,
                            requested_schedule_ref,
                            normalized_unschedule_operation_id,
                            original_material_state_ref,
                            requested_material_state_ref,
                            recorded_at
                        );
        
                        RETURN QUERY
                        SELECT requested_schedule_ref,
                               original_material_state_ref,
                               requested_material_state_ref,
                               original_starts_local_at,
                               original_ends_local_at,
                               recorded_at,
                               false;
                    END;
                    $function$
        """
    )
