"""Persist a second named IANA timezone for eligible one-off Schedule boundaries.

Extension is additive. Single-zone rows retain a NULL end_zone_id and all
existing resolved instants. A distinct end zone is represented in the same
immutable material-state payload, not in a mutable sidecar or a UTC-only value.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20261118_187"
down_revision: str | None = "20261111_186"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_INSERT_PLACEMENT = r"""CREATE OR REPLACE FUNCTION dante.insert_schedule_placement_payload(
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
                IF (requested_payload - 'kind' - 'starts_local_at' - 'ends_local_at' - 'zone_id' - 'end_zone_id' - 'resolved_start_at' - 'resolved_end_at') <> '{}'::jsonb
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
                    end_zone_id,
                    resolved_start_at,
                    resolved_end_at
                ) VALUES (
                    requested_material_state_ref,
                    'interval',
                    (requested_payload ->> 'starts_local_at')::timestamp,
                    (requested_payload ->> 'ends_local_at')::timestamp,
                    requested_payload ->> 'zone_id',
                    requested_payload ->> 'end_zone_id',
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
        $function$"""
_READ_PLACEMENT = r"""CREATE OR REPLACE FUNCTION dante.schedule_placement_payload_json(
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
                    'end_zone_id', payload.end_zone_id,
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
        $function$"""
_VALIDATE_ZONE = r"""CREATE OR REPLACE FUNCTION dante.validate_iana_timezone()
        RETURNS trigger
        LANGUAGE plpgsql
        SET search_path = pg_catalog, dante, pg_temp
        AS $function$
        DECLARE
            zone_value text;
            end_zone_value text;
            local_start timestamp;
            local_end timestamp;
            resolved_start timestamptz;
            resolved_end timestamptz;
            canonical_start timestamptz;
            canonical_end timestamptz;
            round_trip_start timestamp;
            round_trip_end timestamp;
            alternate_gap_start timestamptz;
            alternate_gap_end timestamptz;
            ok boolean;
        BEGIN
            IF TG_TABLE_NAME='schedule_placement_named_zone_state' THEN
                zone_value:=NEW.zone_id;
                end_zone_value:=COALESCE(NEW.end_zone_id,NEW.zone_id);
                local_start:=NEW.starts_local_at;
                local_end:=NEW.ends_local_at;
                resolved_start:=NEW.resolved_start_at;
                resolved_end:=NEW.resolved_end_at;
            ELSIF TG_TABLE_NAME IN (
                'routine_recurrence_boundary_state',
                'event_recurrence_boundary_state'
            ) THEN
                IF NEW.boundary_kind<>'named_zone_local' THEN RETURN NEW; END IF;
                zone_value:=NEW.zone_id;
                local_start:=NEW.local_value;
                resolved_start:=NEW.resolved_at;
            ELSIF TG_TABLE_NAME IN (
                'routine_recurrence_calendar_state',
                'event_recurrence_calendar_state'
            ) THEN
                IF NEW.clock_basis_code<>'named_zone' THEN RETURN NEW; END IF;
                zone_value:=NEW.zone_id;
            ELSIF TG_TABLE_NAME IN (
                'routine_recurrence_quota_state',
                'event_recurrence_quota_state'
            ) THEN
                IF NEW.frame_code<>'named_zone' THEN RETURN NEW; END IF;
                zone_value:=NEW.zone_id;
            ELSIF TG_TABLE_NAME='occurrence_generation_calendar' THEN
                IF NEW.clock_basis_code<>'named_zone' THEN RETURN NEW; END IF;
                zone_value:=NEW.zone_id;
                IF NEW.generated_wall_time IS NOT NULL THEN
                    local_start:=NEW.generated_date+NEW.generated_wall_time;
                    resolved_start:=NEW.resolved_at;
                END IF;
            ELSIF TG_TABLE_NAME='occurrence_generation_quota' THEN
                IF NEW.frame_code<>'named_zone' THEN RETURN NEW; END IF;
                zone_value:=NEW.zone_id;
            ELSE
                RETURN NEW;
            END IF;

            SELECT EXISTS (
                SELECT 1
                FROM pg_catalog.pg_timezone_names
                WHERE name=zone_value
            ) INTO ok;
            IF NOT ok THEN
                RAISE EXCEPTION USING
                    ERRCODE='22023',
                    CONSTRAINT=TG_NAME,
                    TABLE=TG_TABLE_NAME,
                    SCHEMA=TG_TABLE_SCHEMA,
                    MESSAGE='IANA timezone rejected',
                    DETAIL='zone identifier is not in PostgreSQL tzdb vocabulary';
            END IF;

            IF TG_TABLE_NAME='schedule_placement_named_zone_state'
               AND end_zone_value IS DISTINCT FROM zone_value THEN
                SELECT EXISTS(
                    SELECT 1 FROM pg_catalog.pg_timezone_names
                     WHERE name=end_zone_value
                ) INTO ok;
                IF NOT ok THEN
                    RAISE EXCEPTION USING
                        ERRCODE='22023',
                        CONSTRAINT=TG_NAME,
                        TABLE=TG_TABLE_NAME,
                        SCHEMA=TG_TABLE_SCHEMA,
                        MESSAGE='End IANA timezone rejected';
                END IF;
            END IF;

            IF local_start IS NOT NULL AND resolved_start IS NOT NULL THEN
                canonical_start:=local_start AT TIME ZONE zone_value;
                round_trip_start:=canonical_start AT TIME ZONE zone_value;
                alternate_gap_start:=canonical_start-(round_trip_start-local_start);
                IF (resolved_start AT TIME ZONE zone_value) IS DISTINCT FROM local_start
                   AND (
                       round_trip_start IS NOT DISTINCT FROM local_start
                       OR (
                           resolved_start IS DISTINCT FROM canonical_start
                           AND resolved_start IS DISTINCT FROM alternate_gap_start
                       )
                   ) THEN
                    RAISE EXCEPTION USING
                        ERRCODE='23514',
                        CONSTRAINT=TG_NAME,
                        TABLE=TG_TABLE_NAME,
                        SCHEMA=TG_TABLE_SCHEMA,
                        MESSAGE='named-zone resolution rejected',
                        DETAIL='resolved instant must match the local coordinate or one of its two explicit DST-gap resolutions';
                END IF;
            END IF;

            IF local_end IS NOT NULL AND resolved_end IS NOT NULL THEN
                canonical_end:=local_end AT TIME ZONE end_zone_value;
                round_trip_end:=canonical_end AT TIME ZONE end_zone_value;
                alternate_gap_end:=canonical_end-(round_trip_end-local_end);
                IF (resolved_end AT TIME ZONE end_zone_value) IS DISTINCT FROM local_end
                   AND (
                       round_trip_end IS NOT DISTINCT FROM local_end
                       OR (
                           resolved_end IS DISTINCT FROM canonical_end
                           AND resolved_end IS DISTINCT FROM alternate_gap_end
                       )
                   ) THEN
                    RAISE EXCEPTION USING
                        ERRCODE='23514',
                        CONSTRAINT=TG_NAME,
                        TABLE=TG_TABLE_NAME,
                        SCHEMA=TG_TABLE_SCHEMA,
                        MESSAGE='named-zone end resolution rejected',
                        DETAIL='resolved end must match the local coordinate or one of its two explicit DST-gap resolutions';
                END IF;
            END IF;
            RETURN NEW;
        END;
        $function$"""


def upgrade() -> None:
    op.add_column(
        "schedule_placement_named_zone_state",
        sa.Column("end_zone_id", sa.Text(), nullable=True),
        schema="dante",
    )
    op.execute("ALTER TABLE dante.schedule_placement_named_zone_state "
               "DROP CONSTRAINT ck_schedule_placement_named_zone_state_interval_order")
    op.execute(
        """ALTER TABLE dante.schedule_placement_named_zone_state
        ADD CONSTRAINT ck_schedule_placement_named_zone_state_interval_order
        CHECK (
          isfinite(starts_local_at)
          AND (
            (extent_code IN ('point','start_only') AND ends_local_at IS NULL)
            OR (
              extent_code='interval' AND ends_local_at IS NOT NULL
              AND isfinite(ends_local_at)
              AND (end_zone_id IS NOT NULL OR ends_local_at > starts_local_at)
            )
          )
        )"""
    )
    # Retain the existing zone validator for all recurrence, occurrence and
    # scheduling tables. Only the named Schedule end boundary uses end_zone_id.
    for statement in (_INSERT_PLACEMENT, _READ_PLACEMENT, _VALIDATE_ZONE):
        op.execute(sa.text(statement))


def downgrade() -> None:
    # Explicit refusal rather than destroying a user's original end timezone.
    connection = op.get_bind()
    exists = connection.scalar(sa.text(
        "SELECT EXISTS(SELECT 1 FROM dante.schedule_placement_named_zone_state "
        "WHERE end_zone_id IS NOT NULL)"
    ))
    if exists:
        raise RuntimeError("Cannot downgrade while dual-zone Schedules exist.")
    raise RuntimeError(
        "Dual-zone downgrade needs reviewed restoration of original SQL "
        "functions and constraints; automatic destructive downgrade denied."
    )
