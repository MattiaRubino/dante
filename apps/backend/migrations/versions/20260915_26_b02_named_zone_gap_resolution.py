"""Permit explicit earlier/later resolution for named-zone DST gaps.

Revision ID: 20260915_26
Revises: 20260915_25
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260915_26"
down_revision: str | None = "20260915_25"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def _execute(sql: str) -> None:
    op.execute(sa.text(sql))


def upgrade() -> None:
    """Accept only the two explicit Temporal-compatible resolutions of a DST gap."""
    _execute(
        r"""
        CREATE OR REPLACE FUNCTION dante.validate_iana_timezone()
        RETURNS trigger
        LANGUAGE plpgsql
        SET search_path = pg_catalog, dante, pg_temp
        AS $function$
        DECLARE
            zone_value text;
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
                canonical_end:=local_end AT TIME ZONE zone_value;
                round_trip_end:=canonical_end AT TIME ZONE zone_value;
                alternate_gap_end:=canonical_end-(round_trip_end-local_end);
                IF (resolved_end AT TIME ZONE zone_value) IS DISTINCT FROM local_end
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
        $function$
        """
    )


def downgrade() -> None:
    """Restore strict round-trip-only validation."""
    _execute(
        r"""
        CREATE OR REPLACE FUNCTION dante.validate_iana_timezone()
        RETURNS trigger
        LANGUAGE plpgsql
        SET search_path = pg_catalog, dante, pg_temp
        AS $function$
        DECLARE
            zone_value text;
            local_start timestamp;
            local_end timestamp;
            resolved_start timestamptz;
            resolved_end timestamptz;
            ok boolean;
        BEGIN
            IF TG_TABLE_NAME='schedule_placement_named_zone_state' THEN
                zone_value:=NEW.zone_id;
                local_start:=NEW.starts_local_at;
                local_end:=NEW.ends_local_at;
                resolved_start:=NEW.resolved_start_at;
                resolved_end:=NEW.resolved_end_at;
            ELSIF TG_TABLE_NAME IN ('routine_recurrence_boundary_state','event_recurrence_boundary_state') THEN
                IF NEW.boundary_kind<>'named_zone_local' THEN RETURN NEW; END IF;
                zone_value:=NEW.zone_id;
                local_start:=NEW.local_value;
                resolved_start:=NEW.resolved_at;
            ELSIF TG_TABLE_NAME IN ('routine_recurrence_calendar_state','event_recurrence_calendar_state') THEN
                IF NEW.clock_basis_code<>'named_zone' THEN RETURN NEW; END IF;
                zone_value:=NEW.zone_id;
            ELSIF TG_TABLE_NAME IN ('routine_recurrence_quota_state','event_recurrence_quota_state') THEN
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
                SELECT 1 FROM pg_catalog.pg_timezone_names WHERE name=zone_value
            ) INTO ok;
            IF NOT ok THEN
                RAISE EXCEPTION USING ERRCODE='22023', CONSTRAINT=TG_NAME,
                    TABLE=TG_TABLE_NAME, SCHEMA=TG_TABLE_SCHEMA,
                    MESSAGE='IANA timezone rejected',
                    DETAIL='zone identifier is not in PostgreSQL tzdb vocabulary';
            END IF;
            IF local_start IS NOT NULL AND resolved_start IS NOT NULL
               AND (resolved_start AT TIME ZONE zone_value) IS DISTINCT FROM local_start THEN
                RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT=TG_NAME,
                    TABLE=TG_TABLE_NAME, SCHEMA=TG_TABLE_SCHEMA,
                    MESSAGE='named-zone resolution rejected',
                    DETAIL='resolved instant must round-trip to the stored local coordinate and zone';
            END IF;
            IF local_end IS NOT NULL AND resolved_end IS NOT NULL
               AND (resolved_end AT TIME ZONE zone_value) IS DISTINCT FROM local_end THEN
                RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT=TG_NAME,
                    TABLE=TG_TABLE_NAME, SCHEMA=TG_TABLE_SCHEMA,
                    MESSAGE='named-zone end resolution rejected',
                    DETAIL='resolved end must round-trip to the stored local coordinate and zone';
            END IF;
            RETURN NEW;
        END;
        $function$
        """
    )
