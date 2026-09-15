"""Activate B02-E1 Schedule forms and lossless coarse local-period precision.

Revision ID: 20260915_25
Revises: 20260914_24
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "20260915_25"
down_revision: str | None = "20260914_24"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_SCHEMA = "dante"
_OWNER = "dante_owner"
_MIGRATOR = "dante_migrator"
_RUNTIME = "dante_runtime"
_ESTABLISH_SIGNATURE = (
    "dante.establish_self_schedule_placement(uuid,text,text,uuid,uuid,uuid,jsonb)"
)
_REVISE_SIGNATURE = "dante.revise_self_schedule_placement(uuid,text,text,uuid,uuid,uuid,jsonb)"
_UNDO_SIGNATURE = "dante.undo_self_schedule_unschedule_any(uuid,text,text,uuid,text,uuid)"


def _execute(sql: str) -> None:
    op.execute(sa.text(sql))


def upgrade() -> None:
    """Install the bounded B02-E1 form-generic Schedule capability."""
    op.create_table(
        "schedule_placement_coarse_local_period_state",
        sa.Column("material_state_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("local_date", sa.Date(), nullable=False),
        sa.Column("period_code", sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint(
            "material_state_ref",
            name=op.f("pk_schedule_placement_coarse_local_period_state"),
        ),
        sa.ForeignKeyConstraint(
            ["material_state_ref"],
            [f"{_SCHEMA}.schedule_placement_state.material_state_ref"],
            name="fk_schedule_placement_coarse_local_period_state_placement_state",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        sa.CheckConstraint(
            "period_code IN ('morning','afternoon','evening')",
            name=op.f("ck_schedule_placement_coarse_local_period_state_period"),
        ),
        schema=_SCHEMA,
    )

    _execute(
        "ALTER TABLE dante.schedule_placement_state "
        "DROP CONSTRAINT ck_schedule_placement_state_temporal_form"
    )
    _execute(
        "ALTER TABLE dante.schedule_placement_state "
        "ADD CONSTRAINT ck_schedule_placement_state_temporal_form CHECK ("
        "temporal_form_code IN "
        "('date_span','floating_local','named_zone_local','absolute',"
        "'coarse_local_period'))"
    )

    _execute(
        r"""
        CREATE OR REPLACE FUNCTION dante.enforce_schedule_placement_totality()
        RETURNS trigger
        LANGUAGE plpgsql
        SET search_path = pg_catalog, dante, pg_temp
        AS $function$
        DECLARE
            state_ref uuid;
            form text;
            date_n int;
            floating_n int;
            named_n int;
            absolute_n int;
            coarse_n int;
        BEGIN
            state_ref := CASE
                WHEN TG_OP = 'DELETE' THEN OLD.material_state_ref
                ELSE NEW.material_state_ref
            END;
            SELECT placement.temporal_form_code
              INTO form
              FROM dante.schedule_placement_state AS placement
             WHERE placement.material_state_ref = state_ref;
            IF NOT FOUND THEN
                IF TG_OP = 'DELETE' THEN RETURN OLD; END IF;
                RETURN NEW;
            END IF;
            SELECT
                (SELECT count(*) FROM dante.schedule_placement_date_state AS payload WHERE payload.material_state_ref = state_ref),
                (SELECT count(*) FROM dante.schedule_placement_floating_local_state AS payload WHERE payload.material_state_ref = state_ref),
                (SELECT count(*) FROM dante.schedule_placement_named_zone_state AS payload WHERE payload.material_state_ref = state_ref),
                (SELECT count(*) FROM dante.schedule_placement_absolute_state AS payload WHERE payload.material_state_ref = state_ref),
                (SELECT count(*) FROM dante.schedule_placement_coarse_local_period_state AS payload WHERE payload.material_state_ref = state_ref)
              INTO date_n, floating_n, named_n, absolute_n, coarse_n;
            IF date_n + floating_n + named_n + absolute_n + coarse_n <> 1
               OR (form = 'date_span' AND date_n <> 1)
               OR (form = 'floating_local' AND floating_n <> 1)
               OR (form = 'named_zone_local' AND named_n <> 1)
               OR (form = 'absolute' AND absolute_n <> 1)
               OR (form = 'coarse_local_period' AND coarse_n <> 1) THEN
                RAISE EXCEPTION USING
                    ERRCODE='23514',
                    CONSTRAINT=TG_NAME,
                    TABLE=TG_TABLE_NAME,
                    SCHEMA=TG_TABLE_SCHEMA,
                    MESSAGE='Schedule placement payload rejected',
                    DETAIL='exactly one typed payload must match temporal_form_code';
            END IF;
            IF TG_OP = 'DELETE' THEN RETURN OLD; END IF;
            RETURN NEW;
        END;
        $function$
        """
    )
    _execute(
        "CREATE CONSTRAINT TRIGGER "
        "ctrg_schedule_placement_coarse_local_period_state_placement_payload "
        "AFTER INSERT OR UPDATE OR DELETE ON "
        "dante.schedule_placement_coarse_local_period_state "
        "DEFERRABLE INITIALLY DEFERRED FOR EACH ROW "
        "EXECUTE FUNCTION dante.enforce_schedule_placement_totality()"
    )

    _execute(
        r"""
        CREATE FUNCTION dante.insert_schedule_placement_payload(
            requested_material_state_ref uuid,
            requested_schedule_ref uuid,
            requested_payload jsonb
        )
        RETURNS void
        LANGUAGE plpgsql
        SECURITY DEFINER
        VOLATILE
        PARALLEL UNSAFE
        SET search_path = pg_catalog, dante, pg_temp
        AS $function$
        DECLARE
            placement_kind text;
        BEGIN
            IF jsonb_typeof(requested_payload) IS DISTINCT FROM 'object' THEN
                RAISE EXCEPTION USING ERRCODE='23514', MESSAGE='Schedule placement payload must be an object';
            END IF;
            placement_kind := requested_payload ->> 'kind';
            IF placement_kind NOT IN (
                'date_span',
                'floating_local_interval',
                'named_zone_local_interval',
                'absolute_interval',
                'coarse_local_period'
            ) THEN
                RAISE EXCEPTION USING ERRCODE='23514', MESSAGE='Schedule placement kind rejected';
            END IF;

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

            IF placement_kind = 'date_span' THEN
                IF (requested_payload - 'kind' - 'start_date' - 'end_date_exclusive') <> '{}'::jsonb
                   OR requested_payload ->> 'start_date' IS NULL
                   OR requested_payload ->> 'end_date_exclusive' IS NULL THEN
                    RAISE EXCEPTION USING ERRCODE='23514', MESSAGE='Date-span Schedule payload rejected';
                END IF;
                INSERT INTO dante.schedule_placement_state(
                    material_state_ref, schedule_ref, temporal_form_code
                ) VALUES (
                    requested_material_state_ref, requested_schedule_ref, 'date_span'
                );
                INSERT INTO dante.schedule_placement_date_state(material_state_ref, date_span)
                VALUES (
                    requested_material_state_ref,
                    daterange(
                        (requested_payload ->> 'start_date')::date,
                        (requested_payload ->> 'end_date_exclusive')::date,
                        '[)'
                    )
                );
            ELSIF placement_kind = 'floating_local_interval' THEN
                IF (requested_payload - 'kind' - 'starts_local_at' - 'ends_local_at') <> '{}'::jsonb
                   OR requested_payload ->> 'starts_local_at' IS NULL
                   OR requested_payload ->> 'ends_local_at' IS NULL THEN
                    RAISE EXCEPTION USING ERRCODE='23514', MESSAGE='Floating-local Schedule payload rejected';
                END IF;
                INSERT INTO dante.schedule_placement_state(
                    material_state_ref, schedule_ref, temporal_form_code
                ) VALUES (
                    requested_material_state_ref, requested_schedule_ref, 'floating_local'
                );
                INSERT INTO dante.schedule_placement_floating_local_state(
                    material_state_ref, extent_code, starts_local_at, ends_local_at
                ) VALUES (
                    requested_material_state_ref,
                    'interval',
                    (requested_payload ->> 'starts_local_at')::timestamp,
                    (requested_payload ->> 'ends_local_at')::timestamp
                );
            ELSIF placement_kind = 'named_zone_local_interval' THEN
                IF (requested_payload - 'kind' - 'starts_local_at' - 'ends_local_at' - 'zone_id' - 'resolved_start_at' - 'resolved_end_at') <> '{}'::jsonb
                   OR requested_payload ->> 'starts_local_at' IS NULL
                   OR requested_payload ->> 'ends_local_at' IS NULL
                   OR requested_payload ->> 'zone_id' IS NULL
                   OR requested_payload ->> 'resolved_start_at' IS NULL
                   OR requested_payload ->> 'resolved_end_at' IS NULL THEN
                    RAISE EXCEPTION USING ERRCODE='23514', MESSAGE='Named-zone Schedule payload rejected';
                END IF;
                INSERT INTO dante.schedule_placement_state(
                    material_state_ref, schedule_ref, temporal_form_code
                ) VALUES (
                    requested_material_state_ref, requested_schedule_ref, 'named_zone_local'
                );
                INSERT INTO dante.schedule_placement_named_zone_state(
                    material_state_ref,
                    extent_code,
                    starts_local_at,
                    ends_local_at,
                    zone_id,
                    resolved_start_at,
                    resolved_end_at
                ) VALUES (
                    requested_material_state_ref,
                    'interval',
                    (requested_payload ->> 'starts_local_at')::timestamp,
                    (requested_payload ->> 'ends_local_at')::timestamp,
                    requested_payload ->> 'zone_id',
                    (requested_payload ->> 'resolved_start_at')::timestamptz,
                    (requested_payload ->> 'resolved_end_at')::timestamptz
                );
            ELSIF placement_kind = 'absolute_interval' THEN
                IF (requested_payload - 'kind' - 'starts_at' - 'ends_at') <> '{}'::jsonb
                   OR requested_payload ->> 'starts_at' IS NULL
                   OR requested_payload ->> 'ends_at' IS NULL THEN
                    RAISE EXCEPTION USING ERRCODE='23514', MESSAGE='Absolute Schedule payload rejected';
                END IF;
                INSERT INTO dante.schedule_placement_state(
                    material_state_ref, schedule_ref, temporal_form_code
                ) VALUES (
                    requested_material_state_ref, requested_schedule_ref, 'absolute'
                );
                INSERT INTO dante.schedule_placement_absolute_state(
                    material_state_ref, extent_code, starts_at, ends_at
                ) VALUES (
                    requested_material_state_ref,
                    'interval',
                    (requested_payload ->> 'starts_at')::timestamptz,
                    (requested_payload ->> 'ends_at')::timestamptz
                );
            ELSE
                IF (requested_payload - 'kind' - 'local_date' - 'period') <> '{}'::jsonb
                   OR requested_payload ->> 'local_date' IS NULL
                   OR requested_payload ->> 'period' IS NULL THEN
                    RAISE EXCEPTION USING ERRCODE='23514', MESSAGE='Coarse local-period Schedule payload rejected';
                END IF;
                INSERT INTO dante.schedule_placement_state(
                    material_state_ref, schedule_ref, temporal_form_code
                ) VALUES (
                    requested_material_state_ref, requested_schedule_ref, 'coarse_local_period'
                );
                INSERT INTO dante.schedule_placement_coarse_local_period_state(
                    material_state_ref, local_date, period_code
                ) VALUES (
                    requested_material_state_ref,
                    (requested_payload ->> 'local_date')::date,
                    requested_payload ->> 'period'
                );
            END IF;
        END;
        $function$
        """
    )

    _execute(
        r"""
        CREATE FUNCTION dante.schedule_placement_payload_json(
            requested_schedule_ref uuid,
            requested_material_state_ref uuid
        )
        RETURNS jsonb
        LANGUAGE plpgsql
        SECURITY DEFINER
        STABLE
        PARALLEL SAFE
        SET search_path = pg_catalog, dante, pg_temp
        AS $function$
        DECLARE
            placement_form text;
            result_payload jsonb;
        BEGIN
            SELECT placement.temporal_form_code
              INTO placement_form
              FROM dante.schedule_placement_state AS placement
             WHERE placement.schedule_ref = requested_schedule_ref
               AND placement.material_state_ref = requested_material_state_ref;
            IF NOT FOUND THEN RETURN NULL; END IF;

            IF placement_form = 'date_span' THEN
                SELECT jsonb_build_object(
                    'kind', 'date_span',
                    'start_date', lower(payload.date_span),
                    'end_date_exclusive', upper(payload.date_span)
                ) INTO result_payload
                FROM dante.schedule_placement_date_state AS payload
                WHERE payload.material_state_ref = requested_material_state_ref;
            ELSIF placement_form = 'floating_local' THEN
                SELECT jsonb_build_object(
                    'kind', 'floating_local_interval',
                    'starts_local_at', payload.starts_local_at,
                    'ends_local_at', payload.ends_local_at
                ) INTO result_payload
                FROM dante.schedule_placement_floating_local_state AS payload
                WHERE payload.material_state_ref = requested_material_state_ref
                  AND payload.extent_code = 'interval';
            ELSIF placement_form = 'named_zone_local' THEN
                SELECT jsonb_build_object(
                    'kind', 'named_zone_local_interval',
                    'starts_local_at', payload.starts_local_at,
                    'ends_local_at', payload.ends_local_at,
                    'zone_id', payload.zone_id,
                    'resolved_start_at', payload.resolved_start_at,
                    'resolved_end_at', payload.resolved_end_at
                ) INTO result_payload
                FROM dante.schedule_placement_named_zone_state AS payload
                WHERE payload.material_state_ref = requested_material_state_ref
                  AND payload.extent_code = 'interval';
            ELSIF placement_form = 'absolute' THEN
                SELECT jsonb_build_object(
                    'kind', 'absolute_interval',
                    'starts_at', payload.starts_at,
                    'ends_at', payload.ends_at
                ) INTO result_payload
                FROM dante.schedule_placement_absolute_state AS payload
                WHERE payload.material_state_ref = requested_material_state_ref
                  AND payload.extent_code = 'interval';
            ELSIF placement_form = 'coarse_local_period' THEN
                SELECT jsonb_build_object(
                    'kind', 'coarse_local_period',
                    'local_date', payload.local_date,
                    'period', payload.period_code
                ) INTO result_payload
                FROM dante.schedule_placement_coarse_local_period_state AS payload
                WHERE payload.material_state_ref = requested_material_state_ref;
            END IF;
            RETURN result_payload;
        END;
        $function$
        """
    )

    _execute(
        r"""
        CREATE FUNCTION dante.establish_self_schedule_placement(
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
            subject_family text;
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
            SELECT address.owner_family
              INTO subject_family
              FROM dante.native_address AS address
             WHERE address.native_ref = requested_subject_native_ref;
            IF subject_family IS DISTINCT FROM 'activity' THEN
                RAISE EXCEPTION USING ERRCODE='23503', MESSAGE='Schedule subject rejected for B02-E1';
            END IF;
            IF NOT EXISTS (
                SELECT 1 FROM dante.activity_intention AS intention
                WHERE intention.activity_ref = requested_subject_native_ref
                  AND intention.self_person_ref = requested_self_person_ref
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
        CREATE FUNCTION dante.revise_self_schedule_placement(
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

            IF NOT EXISTS (
                SELECT 1
                  FROM dante.schedule AS schedule_row
                  JOIN dante.activity_intention AS intention
                    ON intention.activity_ref = schedule_row.subject_native_ref
                 WHERE schedule_row.schedule_ref = requested_schedule_ref
                   AND intention.self_person_ref = requested_self_person_ref
            ) THEN
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
        r"""
        CREATE FUNCTION dante.undo_self_schedule_unschedule_any(
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
            IF requested_intent_fingerprint !~ '^[0-9a-f]{64}$' THEN
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

            IF NOT EXISTS (
                SELECT 1
                  FROM dante.schedule AS schedule_row
                  JOIN dante.activity_intention AS intention
                    ON intention.activity_ref = schedule_row.subject_native_ref
                 WHERE schedule_row.schedule_ref = requested_schedule_ref
                   AND intention.self_person_ref = requested_self_person_ref
            ) THEN
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

    for signature in (
        "dante.insert_schedule_placement_payload(uuid,uuid,jsonb)",
        "dante.schedule_placement_payload_json(uuid,uuid)",
        _ESTABLISH_SIGNATURE,
        _REVISE_SIGNATURE,
        _UNDO_SIGNATURE,
    ):
        _execute(f"ALTER FUNCTION {signature} OWNER TO {_OWNER}")
        _execute(
            f"REVOKE ALL PRIVILEGES ON FUNCTION {signature} FROM PUBLIC, {_RUNTIME}, {_MIGRATOR}"
        )
    for signature in (_ESTABLISH_SIGNATURE, _REVISE_SIGNATURE, _UNDO_SIGNATURE):
        _execute(f"GRANT EXECUTE ON FUNCTION {signature} TO {_RUNTIME}")

    _execute(f"ALTER TABLE dante.schedule_placement_coarse_local_period_state OWNER TO {_OWNER}")
    _execute(
        "REVOKE ALL PRIVILEGES ON TABLE "
        "dante.schedule_placement_coarse_local_period_state "
        f"FROM PUBLIC, {_RUNTIME}, {_MIGRATOR}"
    )
    _execute(
        f"GRANT SELECT ON TABLE dante.schedule_placement_coarse_local_period_state TO {_RUNTIME}"
    )


def downgrade() -> None:
    """Remove B02-E1 only when no new-form data or receipts depend on it."""
    _execute(
        r"""
        DO $block$
        BEGIN
            IF EXISTS (
                SELECT 1 FROM dante.schedule_placement_state AS placement
                WHERE placement.temporal_form_code = 'coarse_local_period'
            ) OR EXISTS (
                SELECT 1
                  FROM dante.schedule_establish_operation AS operation
                  JOIN dante.schedule_placement_state AS placement
                    ON placement.material_state_ref = operation.material_state_ref
                 WHERE placement.temporal_form_code <> 'floating_local'
            ) OR EXISTS (
                SELECT 1
                  FROM dante.schedule_revision_operation AS operation
                  JOIN dante.schedule_placement_state AS placement
                    ON placement.material_state_ref = operation.material_state_ref
                 WHERE placement.temporal_form_code <> 'floating_local'
            ) THEN
                RAISE EXCEPTION USING
                    ERRCODE='55000',
                    MESSAGE='B02-E1 downgrade refused',
                    DETAIL='new-form Schedule history must remain reconstructible';
            END IF;
        END;
        $block$
        """
    )
    for signature in (_UNDO_SIGNATURE, _REVISE_SIGNATURE, _ESTABLISH_SIGNATURE):
        _execute(f"DROP FUNCTION {signature}")
    _execute("DROP FUNCTION dante.schedule_placement_payload_json(uuid,uuid)")
    _execute("DROP FUNCTION dante.insert_schedule_placement_payload(uuid,uuid,jsonb)")
    _execute(
        "DROP TRIGGER "
        "ctrg_schedule_placement_coarse_local_period_state_placement_payload "
        "ON dante.schedule_placement_coarse_local_period_state"
    )
    op.drop_table("schedule_placement_coarse_local_period_state", schema=_SCHEMA)
    _execute(
        "ALTER TABLE dante.schedule_placement_state "
        "DROP CONSTRAINT ck_schedule_placement_state_temporal_form"
    )
    _execute(
        "ALTER TABLE dante.schedule_placement_state "
        "ADD CONSTRAINT ck_schedule_placement_state_temporal_form CHECK ("
        "temporal_form_code IN "
        "('date_span','floating_local','named_zone_local','absolute'))"
    )
    _execute(
        r"""
        CREATE OR REPLACE FUNCTION dante.enforce_schedule_placement_totality()
        RETURNS trigger
        LANGUAGE plpgsql
        SET search_path = pg_catalog, dante, pg_temp
        AS $function$
        DECLARE
            state_ref uuid;
            form text;
            date_n int;
            floating_n int;
            named_n int;
            absolute_n int;
        BEGIN
            state_ref := CASE WHEN TG_OP='DELETE' THEN OLD.material_state_ref ELSE NEW.material_state_ref END;
            SELECT placement.temporal_form_code INTO form
              FROM dante.schedule_placement_state AS placement
             WHERE placement.material_state_ref = state_ref;
            IF NOT FOUND THEN IF TG_OP='DELETE' THEN RETURN OLD; END IF; RETURN NEW; END IF;
            SELECT
                (SELECT count(*) FROM dante.schedule_placement_date_state AS payload WHERE payload.material_state_ref=state_ref),
                (SELECT count(*) FROM dante.schedule_placement_floating_local_state AS payload WHERE payload.material_state_ref=state_ref),
                (SELECT count(*) FROM dante.schedule_placement_named_zone_state AS payload WHERE payload.material_state_ref=state_ref),
                (SELECT count(*) FROM dante.schedule_placement_absolute_state AS payload WHERE payload.material_state_ref=state_ref)
              INTO date_n, floating_n, named_n, absolute_n;
            IF date_n+floating_n+named_n+absolute_n<>1
               OR (form='date_span' AND date_n<>1)
               OR (form='floating_local' AND floating_n<>1)
               OR (form='named_zone_local' AND named_n<>1)
               OR (form='absolute' AND absolute_n<>1) THEN
                RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT=TG_NAME, TABLE=TG_TABLE_NAME, SCHEMA=TG_TABLE_SCHEMA,
                    MESSAGE='Schedule placement payload rejected', DETAIL='exactly one typed payload must match temporal_form_code';
            END IF;
            IF TG_OP='DELETE' THEN RETURN OLD; END IF;
            RETURN NEW;
        END;
        $function$
        """
    )
