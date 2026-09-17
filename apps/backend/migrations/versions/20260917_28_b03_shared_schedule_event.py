"""Share the proven Schedule capability between Activity and Event.

Revision ID: 20260917_28
Revises: 20260916_27
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260917_28"
down_revision: str | None = "20260916_27"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def _execute(sql: str) -> None:
    op.execute(sa.text(sql))


def _subject_scope_predicate(*, include_event: bool) -> str:
    event_branch = """
                    OR (
                        address.owner_family = 'event'
                        AND EXISTS (
                            SELECT 1
                              FROM dante.event_expectation AS expectation
                             WHERE expectation.event_ref = requested_subject_native_ref
                               AND expectation.self_person_ref = requested_self_person_ref
                        )
                    )""" if include_event else ""
    return f"""
            EXISTS (
                SELECT 1
                  FROM dante.native_address AS address
                 WHERE address.native_ref = requested_subject_native_ref
                   AND (
                       (
                           address.owner_family = 'activity'
                           AND EXISTS (
                               SELECT 1
                                 FROM dante.activity_intention AS intention
                                WHERE intention.activity_ref = requested_subject_native_ref
                                  AND intention.self_person_ref = requested_self_person_ref
                           )
                       ){event_branch}
                   )
            )
    """


def _schedule_scope_predicate(*, include_event: bool) -> str:
    event_branch = """
                            OR (
                                address.owner_family = 'event'
                                AND EXISTS (
                                    SELECT 1
                                      FROM dante.event_expectation AS expectation
                                     WHERE expectation.event_ref = schedule_row.subject_native_ref
                                       AND expectation.self_person_ref = requested_self_person_ref
                                )
                            )""" if include_event else ""
    return f"""
            EXISTS (
                SELECT 1
                  FROM dante.schedule AS schedule_row
                  JOIN dante.native_address AS address
                    ON address.native_ref = schedule_row.subject_native_ref
                 WHERE schedule_row.schedule_ref = requested_schedule_ref
                   AND (
                       (
                           address.owner_family = 'activity'
                           AND EXISTS (
                               SELECT 1
                                 FROM dante.activity_intention AS intention
                                WHERE intention.activity_ref = schedule_row.subject_native_ref
                                  AND intention.self_person_ref = requested_self_person_ref
                           )
                       ){event_branch}
                   )
            )
    """


def _install_schedule_capabilities(*, include_event: bool) -> None:
    subject_scope = _subject_scope_predicate(include_event=include_event)
    schedule_scope = _schedule_scope_predicate(include_event=include_event)

    _execute(
        f"""
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
            IF requested_intent_fingerprint !~ '^[0-9a-f]{{64}}$' THEN
                RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT='ck_schedule_establish_operation_fingerprint', MESSAGE='Schedule operation fingerprint rejected';
            END IF;
            IF uuid_extract_version(requested_schedule_ref) IS DISTINCT FROM 7
               OR uuid_extract_version(requested_material_state_ref) IS DISTINCT FROM 7 THEN
                RAISE EXCEPTION USING ERRCODE='23514', MESSAGE='Schedule placement reference rejected';
            END IF;
            IF NOT ({subject_scope}) THEN
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
        f"""
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
            existing_fingerprint text;
            existing_schedule_ref uuid;
            existing_expected_material_state_ref uuid;
            existing_material_state_ref uuid;
            existing_created_at timestamptz;
        BEGIN
            IF normalized_operation_id = '' OR char_length(normalized_operation_id) > 200 THEN
                RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT='ck_schedule_revision_operation_operation_id', MESSAGE='Schedule revision operation id rejected';
            END IF;
            IF requested_intent_fingerprint !~ '^[0-9a-f]{{64}}$' THEN
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

            IF NOT ({schedule_scope}) THEN
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

    _execute(
        f"""
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
            IF normalized_operation_id = '' OR char_length(normalized_operation_id) > 200 THEN
                RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT='ck_schedule_unschedule_operation_operation_id', MESSAGE='Schedule unschedule operation id rejected';
            END IF;
            IF requested_intent_fingerprint !~ '^[0-9a-f]{{64}}$' THEN
                RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT='ck_schedule_unschedule_operation_fingerprint', MESSAGE='Schedule unschedule fingerprint rejected';
            END IF;
            IF uuid_extract_version(requested_schedule_ref) IS DISTINCT FROM 7
               OR uuid_extract_version(requested_expected_material_state_ref) IS DISTINCT FROM 7 THEN
                RAISE EXCEPTION USING ERRCODE='23514', MESSAGE='Schedule unschedule reference rejected';
            END IF;

            PERFORM pg_advisory_xact_lock(hashtextextended(requested_schedule_ref::text, 0));
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
                   OR existing_expected_material_state_ref <> requested_expected_material_state_ref THEN
                    RAISE EXCEPTION USING ERRCODE='23505', CONSTRAINT='pk_schedule_unschedule_operation', MESSAGE='Schedule unschedule operation id reused with different intent';
                END IF;
                RETURN QUERY SELECT existing_schedule_ref, existing_expected_material_state_ref, normalized_operation_id, existing_created_at, true;
                RETURN;
            END IF;

            IF NOT ({schedule_scope}) THEN
                RAISE EXCEPTION USING ERRCODE='23503', CONSTRAINT='schedule_unschedule_schedule_not_found', MESSAGE='Schedule unschedule self scope rejected';
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
                RAISE EXCEPTION USING ERRCODE='23505', CONSTRAINT='schedule_unschedule_expected_state', MESSAGE='Schedule has no current accepted placement';
            END IF;
            IF current_material_state_ref IS DISTINCT FROM requested_expected_material_state_ref THEN
                RAISE EXCEPTION USING ERRCODE='23505', CONSTRAINT='schedule_unschedule_expected_state', MESSAGE='Schedule unschedule basis is stale';
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

            recorded_at := GREATEST(clock_timestamp(), current_from_at + interval '1 microsecond');
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
                self_person_ref, operation_id, intent_fingerprint, schedule_ref,
                expected_material_state_ref, created_at
            ) VALUES (
                requested_self_person_ref, normalized_operation_id, requested_intent_fingerprint,
                requested_schedule_ref, requested_expected_material_state_ref, recorded_at
            );
            RETURN QUERY SELECT requested_schedule_ref, requested_expected_material_state_ref, normalized_operation_id, recorded_at, false;
        END;
        $function$
        """
    )

    _execute(
        f"""
        CREATE OR REPLACE FUNCTION dante.undo_self_schedule_unschedule_any(
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
            placement_payload jsonb,
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
            normalized_unschedule_operation_id text := btrim(requested_unschedule_operation_id);
            recorded_at timestamptz;
            unscheduled_at timestamptz;
            original_material_state_ref uuid;
            original_payload jsonb;
            existing_fingerprint text;
            existing_schedule_ref uuid;
            existing_unschedule_operation_id text;
            existing_restored_from_material_state_ref uuid;
            existing_material_state_ref uuid;
            existing_created_at timestamptz;
            existing_payload jsonb;
        BEGIN
            IF normalized_operation_id = '' OR char_length(normalized_operation_id) > 200
               OR normalized_unschedule_operation_id = '' OR char_length(normalized_unschedule_operation_id) > 200 THEN
                RAISE EXCEPTION USING ERRCODE='23514', MESSAGE='Schedule undo operation identity rejected';
            END IF;
            IF requested_intent_fingerprint !~ '^[0-9a-f]{{64}}$' THEN
                RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT='ck_schedule_unschedule_undo_operation_fingerprint', MESSAGE='Schedule undo fingerprint rejected';
            END IF;
            IF uuid_extract_version(requested_schedule_ref) IS DISTINCT FROM 7
               OR uuid_extract_version(requested_material_state_ref) IS DISTINCT FROM 7 THEN
                RAISE EXCEPTION USING ERRCODE='23514', MESSAGE='Schedule undo reference rejected';
            END IF;

            PERFORM pg_advisory_xact_lock(hashtextextended(requested_schedule_ref::text, 0));
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
                   OR existing_unschedule_operation_id <> normalized_unschedule_operation_id THEN
                    RAISE EXCEPTION USING ERRCODE='23505', CONSTRAINT='pk_schedule_unschedule_undo_operation', MESSAGE='Schedule undo operation id reused with different intent';
                END IF;
                existing_payload := dante.schedule_placement_payload_json(existing_schedule_ref, existing_material_state_ref);
                IF existing_payload IS NULL THEN
                    RAISE EXCEPTION USING ERRCODE='XX001', MESSAGE='Schedule undo receipt lost canonical placement state';
                END IF;
                RETURN QUERY SELECT existing_schedule_ref, existing_restored_from_material_state_ref, existing_material_state_ref, existing_payload, existing_created_at, true;
                RETURN;
            END IF;

            IF NOT ({schedule_scope}) THEN
                RAISE EXCEPTION USING ERRCODE='23503', CONSTRAINT='schedule_unschedule_undo_not_found', MESSAGE='Schedule undo self scope rejected';
            END IF;
            SELECT operation.expected_material_state_ref, operation.created_at
              INTO original_material_state_ref, unscheduled_at
              FROM dante.schedule_unschedule_operation AS operation
             WHERE operation.self_person_ref = requested_self_person_ref
               AND operation.operation_id = normalized_unschedule_operation_id
               AND operation.schedule_ref = requested_schedule_ref;
            IF NOT FOUND THEN
                RAISE EXCEPTION USING ERRCODE='23503', CONSTRAINT='schedule_unschedule_undo_not_found', MESSAGE='Schedule undo basis was not found';
            END IF;
            IF EXISTS (
                SELECT 1 FROM dante.scoped_current_material_state AS current
                 WHERE current.scoped_owner_ref = requested_schedule_ref
                   AND current.facet_code = 'schedule.placement'
            ) OR EXISTS (
                SELECT 1 FROM dante.schedule_placement_current_history AS history
                 WHERE history.schedule_ref = requested_schedule_ref
                   AND history.current_until_at IS NULL
            ) OR NOT EXISTS (
                SELECT 1 FROM dante.schedule_placement_current_history AS history
                 WHERE history.schedule_ref = requested_schedule_ref
                   AND history.material_state_ref = original_material_state_ref
                   AND history.current_until_at = unscheduled_at
            ) OR EXISTS (
                SELECT 1 FROM dante.schedule_placement_current_history AS history
                 WHERE history.schedule_ref = requested_schedule_ref
                   AND history.current_from_at >= unscheduled_at
            ) THEN
                RAISE EXCEPTION USING ERRCODE='23505', CONSTRAINT='schedule_unschedule_undo_expected_state', MESSAGE='Schedule undo basis is stale';
            END IF;

            original_payload := dante.schedule_placement_payload_json(requested_schedule_ref, original_material_state_ref);
            IF original_payload IS NULL THEN
                RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT='schedule_unschedule_undo_unsupported_form', MESSAGE='Schedule undo placement form is not activated';
            END IF;
            recorded_at := GREATEST(clock_timestamp(), unscheduled_at + interval '1 microsecond');
            PERFORM dante.insert_schedule_placement_payload(requested_material_state_ref, requested_schedule_ref, original_payload);
            INSERT INTO dante.scoped_current_material_state(scoped_owner_ref, facet_code, material_state_ref)
            VALUES (requested_schedule_ref, 'schedule.placement', requested_material_state_ref);
            INSERT INTO dante.schedule_placement_current_history(schedule_ref, material_state_ref, current_from_at, current_until_at)
            VALUES (requested_schedule_ref, requested_material_state_ref, recorded_at, NULL);
            INSERT INTO dante.schedule_unschedule_undo_operation(
                self_person_ref, operation_id, intent_fingerprint, schedule_ref,
                unschedule_operation_id, restored_from_material_state_ref,
                material_state_ref, created_at
            ) VALUES (
                requested_self_person_ref, normalized_operation_id, requested_intent_fingerprint,
                requested_schedule_ref, normalized_unschedule_operation_id,
                original_material_state_ref, requested_material_state_ref, recorded_at
            );
            RETURN QUERY SELECT requested_schedule_ref, original_material_state_ref, requested_material_state_ref, original_payload, recorded_at, false;
        END;
        $function$
        """
    )


def upgrade() -> None:
    """Authorize Event as the second explicit owner of the shared Schedule engine."""
    _install_schedule_capabilities(include_event=True)


def downgrade() -> None:
    """Return to Activity-only Schedule authorization when no Event Schedule exists."""
    _execute(
        r"""
        DO $block$
        BEGIN
            IF EXISTS (
                SELECT 1
                  FROM dante.schedule AS schedule_row
                  JOIN dante.native_address AS address
                    ON address.native_ref = schedule_row.subject_native_ref
                 WHERE address.owner_family = 'event'
            ) THEN
                RAISE EXCEPTION USING
                    ERRCODE='55000',
                    MESSAGE='B03-B downgrade refused',
                    DETAIL='Event-owned Schedule identity/history is canonical product data';
            END IF;
        END;
        $block$
        """
    )
    _install_schedule_capabilities(include_event=False)
