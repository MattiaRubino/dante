"""Resolve named-zone DST gaps and preserve B02 Schedule retirement integrity.

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


def _install_schedule_totality(*, retirement_aware: bool) -> None:
    if retirement_aware:
        predicate = r"""
            IF EXISTS (
                SELECT 1
                  FROM dante.material_state_retirement
                 WHERE material_state_ref = state_ref
            ) THEN
                IF date_n + floating_n + named_n + absolute_n + coarse_n <> 0 THEN
                    RAISE EXCEPTION USING
                        ERRCODE='23514',
                        CONSTRAINT=TG_NAME,
                        TABLE=TG_TABLE_NAME,
                        SCHEMA=TG_TABLE_SCHEMA,
                        MESSAGE='retired Schedule placement payload rejected',
                        DETAIL='retired MaterialState keeps its envelope/reference continuity but no placement payload';
                END IF;
            ELSIF date_n + floating_n + named_n + absolute_n + coarse_n <> 1
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
        """
    else:
        predicate = r"""
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
        """

    _execute(
        f"""
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
{predicate}
            IF TG_OP = 'DELETE' THEN RETURN OLD; END IF;
            RETURN NEW;
        END;
        $function$
        """
    )


def _install_retirement_validator(*, include_coarse: bool) -> None:
    coarse_union = (
        "\n                  UNION ALL SELECT 1 FROM "
        "dante.schedule_placement_coarse_local_period_state "
        "WHERE material_state_ref=state_ref"
        if include_coarse
        else ""
    )
    _execute(
        f"""
        CREATE OR REPLACE FUNCTION dante.enforce_material_state_retirement()
        RETURNS trigger
        LANGUAGE plpgsql
        SECURITY INVOKER
        VOLATILE
        PARALLEL UNSAFE
        SET search_path = pg_catalog, dante, pg_temp
        AS $function$
        DECLARE
            state_ref uuid;
            facet text;
            payload_exists boolean := false;
        BEGIN
            IF TG_OP='UPDATE' OR TG_OP='DELETE' THEN
                RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT=TG_NAME,
                    TABLE=TG_TABLE_NAME, SCHEMA=TG_TABLE_SCHEMA,
                    MESSAGE='MaterialState retirement is immutable',
                    DETAIL='retirement/tombstone rows are append-only and may not be rewritten or removed';
            END IF;

            state_ref:=NEW.material_state_ref;
            SELECT facet_code INTO facet
              FROM dante.material_state_address
             WHERE material_state_ref=state_ref;
            IF NOT FOUND THEN
                RAISE EXCEPTION USING ERRCODE='23503', CONSTRAINT=TG_NAME,
                    TABLE=TG_TABLE_NAME, SCHEMA=TG_TABLE_SCHEMA,
                    MESSAGE='MaterialState retirement has no address',
                    DETAIL='retirement requires an existing MaterialStateRef address/envelope';
            END IF;

            IF facet='schedule.placement' THEN
                SELECT EXISTS (
                  SELECT 1 FROM dante.schedule_placement_date_state WHERE material_state_ref=state_ref
                  UNION ALL SELECT 1 FROM dante.schedule_placement_floating_local_state WHERE material_state_ref=state_ref
                  UNION ALL SELECT 1 FROM dante.schedule_placement_named_zone_state WHERE material_state_ref=state_ref
                  UNION ALL SELECT 1 FROM dante.schedule_placement_absolute_state WHERE material_state_ref=state_ref{coarse_union}
                ) INTO payload_exists;
            ELSIF facet='actual.realization' THEN
                SELECT EXISTS (
                  SELECT 1 FROM dante.actual_realization_timing WHERE material_state_ref=state_ref
                  UNION ALL SELECT 1 FROM dante.actual_realization_session_basis WHERE actual_material_state_ref=state_ref
                ) INTO payload_exists;
            ELSIF facet='session.timing' THEN
                SELECT EXISTS (
                  SELECT 1 FROM dante.session_timing_absolute WHERE material_state_ref=state_ref
                  UNION ALL SELECT 1 FROM dante.session_timing_elapsed WHERE material_state_ref=state_ref
                  UNION ALL SELECT 1 FROM dante.session_timing_pause WHERE material_state_ref=state_ref
                ) INTO payload_exists;
            ELSIF facet='routine.recurrence' THEN
                SELECT EXISTS (
                  SELECT 1 FROM dante.routine_recurrence_boundary_state WHERE material_state_ref=state_ref
                  UNION ALL SELECT 1 FROM dante.routine_recurrence_calendar_state WHERE material_state_ref=state_ref
                  UNION ALL SELECT 1 FROM dante.routine_recurrence_calendar_wall_time WHERE material_state_ref=state_ref
                  UNION ALL SELECT 1 FROM dante.routine_recurrence_calendar_weekday WHERE material_state_ref=state_ref
                  UNION ALL SELECT 1 FROM dante.routine_recurrence_calendar_month_day WHERE material_state_ref=state_ref
                  UNION ALL SELECT 1 FROM dante.routine_recurrence_calendar_ordinal_weekday WHERE material_state_ref=state_ref
                  UNION ALL SELECT 1 FROM dante.routine_recurrence_calendar_year_month_day WHERE material_state_ref=state_ref
                  UNION ALL SELECT 1 FROM dante.routine_recurrence_elapsed_state WHERE material_state_ref=state_ref
                  UNION ALL SELECT 1 FROM dante.routine_recurrence_quota_state WHERE material_state_ref=state_ref
                  UNION ALL SELECT 1 FROM dante.routine_recurrence_cyclic_state WHERE material_state_ref=state_ref
                  UNION ALL SELECT 1 FROM dante.routine_recurrence_cycle_position WHERE material_state_ref=state_ref
                ) INTO payload_exists;
            ELSIF facet='event.recurrence' THEN
                SELECT EXISTS (
                  SELECT 1 FROM dante.event_recurrence_boundary_state WHERE material_state_ref=state_ref
                  UNION ALL SELECT 1 FROM dante.event_recurrence_calendar_state WHERE material_state_ref=state_ref
                  UNION ALL SELECT 1 FROM dante.event_recurrence_calendar_wall_time WHERE material_state_ref=state_ref
                  UNION ALL SELECT 1 FROM dante.event_recurrence_calendar_weekday WHERE material_state_ref=state_ref
                  UNION ALL SELECT 1 FROM dante.event_recurrence_calendar_month_day WHERE material_state_ref=state_ref
                  UNION ALL SELECT 1 FROM dante.event_recurrence_calendar_ordinal_weekday WHERE material_state_ref=state_ref
                  UNION ALL SELECT 1 FROM dante.event_recurrence_calendar_year_month_day WHERE material_state_ref=state_ref
                  UNION ALL SELECT 1 FROM dante.event_recurrence_elapsed_state WHERE material_state_ref=state_ref
                  UNION ALL SELECT 1 FROM dante.event_recurrence_quota_state WHERE material_state_ref=state_ref
                  UNION ALL SELECT 1 FROM dante.event_recurrence_cyclic_state WHERE material_state_ref=state_ref
                  UNION ALL SELECT 1 FROM dante.event_recurrence_cycle_position WHERE material_state_ref=state_ref
                ) INTO payload_exists;
            ELSE
                RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT=TG_NAME,
                    TABLE=TG_TABLE_NAME, SCHEMA=TG_TABLE_SCHEMA,
                    MESSAGE='MaterialState retirement facet rejected',
                    DETAIL='retirement may target only a materialized DANTE MaterialState facet';
            END IF;

            IF payload_exists THEN
                RAISE EXCEPTION USING ERRCODE='23514', CONSTRAINT=TG_NAME,
                    TABLE=TG_TABLE_NAME, SCHEMA=TG_TABLE_SCHEMA,
                    MESSAGE='MaterialState retirement payload rejected',
                    DETAIL='a committed retirement must retain reference/history continuity while protected payload is absent';
            END IF;
            RETURN NEW;
        END;
        $function$
        """
    )


def upgrade() -> None:
    """Resolve DST gaps and restore anti-resurrection guards for every B02 form."""
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
    _install_schedule_totality(retirement_aware=True)
    _install_retirement_validator(include_coarse=True)


def downgrade() -> None:
    """Restore the exact pre-26 B02 validator behavior."""
    _install_retirement_validator(include_coarse=False)
    _install_schedule_totality(retirement_aware=False)
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
