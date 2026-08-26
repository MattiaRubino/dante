"""Materialize CP6-M06 Occurrence generation.

Revision ID: 20260826_06
Revises: 20260825_05
"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "20260826_06"
down_revision: str | None = "20260825_05"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_DANTE_SCHEMA = "dante"
_RUNTIME_ROLE = "dante_runtime"
_MIGRATOR_ROLE = "dante_migrator"
_OWNER_ROLE = "dante_owner"

_M6_TABLES = (
    "occurrence_generation",
    "occurrence_generation_calendar",
    "occurrence_generation_elapsed",
    "occurrence_generation_quota",
    "occurrence_generation_cyclic",
)


def _sql(statement: str) -> None:
    op.execute(sa.text(statement))


def _fk(
    local_columns: list[str],
    remote_columns: list[str],
    *,
    name: str,
) -> sa.ForeignKeyConstraint:
    return sa.ForeignKeyConstraint(
        local_columns,
        remote_columns,
        name=op.f(name),
        match="SIMPLE",
        onupdate="NO ACTION",
        ondelete="NO ACTION",
        deferrable=False,
    )


def _deny_table(name: str) -> None:
    _sql(
        f"REVOKE ALL PRIVILEGES ON TABLE dante.{name} "
        f"FROM PUBLIC, {_RUNTIME_ROLE}, {_MIGRATOR_ROLE}"
    )


def _create_tables() -> None:
    op.create_table(
        "occurrence_generation",
        sa.Column("occurrence_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("source_native_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column(
            "governing_recurrence_state_ref",
            postgresql.UUID(as_uuid=True),
            nullable=True,
        ),
        sa.Column("origin_code", sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint(
            "occurrence_ref",
            name=op.f("pk_occurrence_generation"),
        ),
        sa.CheckConstraint(
            "origin_code IN ('recurrence_generated','explicit_extra')",
            name=op.f("ck_occurrence_generation_origin_code"),
        ),
        sa.CheckConstraint(
            "((origin_code='recurrence_generated' "
            "AND governing_recurrence_state_ref IS NOT NULL) OR "
            "(origin_code='explicit_extra' "
            "AND governing_recurrence_state_ref IS NULL))",
            name=op.f("ck_occurrence_generation_governing_state_pair"),
        ),
        _fk(
            ["occurrence_ref"],
            ["dante.occurrence.occurrence_ref"],
            name="fk_occurrence_generation_occurrence_ref_occurrence",
        ),
        _fk(
            ["source_native_ref"],
            ["dante.native_address.native_ref"],
            name="fk_occurrence_generation_source_native_ref_native_address",
        ),
        _fk(
            ["governing_recurrence_state_ref"],
            ["dante.material_state_address.material_state_ref"],
            name="fk_occurrence_generation_state_address",
        ),
        schema=_DANTE_SCHEMA,
    )
    op.create_index(
        "ix_occurrence_generation_source_governing_state",
        "occurrence_generation",
        ["source_native_ref", "governing_recurrence_state_ref", "occurrence_ref"],
        schema=_DANTE_SCHEMA,
    )
    op.create_index(
        "ix_occurrence_generation_governing_recurrence_state_ref",
        "occurrence_generation",
        ["governing_recurrence_state_ref"],
        schema=_DANTE_SCHEMA,
    )

    op.create_table(
        "occurrence_generation_calendar",
        sa.Column("occurrence_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("generated_date", sa.Date(), nullable=False),
        sa.Column("generated_wall_time", sa.Time(timezone=False), nullable=True),
        sa.Column("clock_basis_code", sa.Text(), nullable=False),
        sa.Column("zone_id", sa.Text(), nullable=True),
        sa.Column("resolved_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint(
            "occurrence_ref",
            name=op.f("pk_occurrence_generation_calendar"),
        ),
        sa.CheckConstraint(
            "clock_basis_code IN ('floating_local','named_zone','absolute_utc')",
            name=op.f("ck_occurrence_generation_calendar_clock_basis"),
        ),
        sa.CheckConstraint(
            "((clock_basis_code='named_zone' AND zone_id IS NOT NULL) OR "
            "(clock_basis_code IN ('floating_local','absolute_utc') "
            "AND zone_id IS NULL))",
            name=op.f("ck_occurrence_generation_calendar_zone_basis"),
        ),
        sa.CheckConstraint(
            "isfinite(generated_date) AND "
            "(resolved_at IS NULL OR "
            "(clock_basis_code='named_zone' AND isfinite(resolved_at)))",
            name=op.f("ck_occurrence_generation_calendar_resolved_pair"),
        ),
        _fk(
            ["occurrence_ref"],
            ["dante.occurrence_generation.occurrence_ref"],
            name="fk_occurrence_generation_calendar_generation",
        ),
        schema=_DANTE_SCHEMA,
    )

    op.create_table(
        "occurrence_generation_elapsed",
        sa.Column("occurrence_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("expected_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint(
            "occurrence_ref",
            name=op.f("pk_occurrence_generation_elapsed"),
        ),
        sa.CheckConstraint(
            "isfinite(expected_at)",
            name=op.f("ck_occurrence_generation_elapsed_expected_at"),
        ),
        _fk(
            ["occurrence_ref"],
            ["dante.occurrence_generation.occurrence_ref"],
            name="fk_occurrence_generation_elapsed_generation",
        ),
        schema=_DANTE_SCHEMA,
    )

    op.create_table(
        "occurrence_generation_quota",
        sa.Column("occurrence_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("period_start_date", sa.Date(), nullable=False),
        sa.Column("period_end_date_exclusive", sa.Date(), nullable=False),
        sa.Column("frame_code", sa.Text(), nullable=False),
        sa.Column("zone_id", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint(
            "occurrence_ref",
            name=op.f("pk_occurrence_generation_quota"),
        ),
        sa.CheckConstraint(
            "isfinite(period_start_date) AND "
            "isfinite(period_end_date_exclusive) AND "
            "period_end_date_exclusive > period_start_date",
            name=op.f("ck_occurrence_generation_quota_period_order"),
        ),
        sa.CheckConstraint(
            "frame_code IN ('floating_local','named_zone','absolute_utc')",
            name=op.f("ck_occurrence_generation_quota_frame"),
        ),
        sa.CheckConstraint(
            "((frame_code='named_zone' AND zone_id IS NOT NULL) OR "
            "(frame_code IN ('floating_local','absolute_utc') "
            "AND zone_id IS NULL))",
            name=op.f("ck_occurrence_generation_quota_zone_basis"),
        ),
        _fk(
            ["occurrence_ref"],
            ["dante.occurrence_generation.occurrence_ref"],
            name="fk_occurrence_generation_quota_generation",
        ),
        schema=_DANTE_SCHEMA,
    )
    op.create_index(
        "ix_occurrence_generation_quota_period",
        "occurrence_generation_quota",
        ["period_start_date", "period_end_date_exclusive", "occurrence_ref"],
        schema=_DANTE_SCHEMA,
    )

    op.create_table(
        "occurrence_generation_cyclic",
        sa.Column("occurrence_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("generated_date", sa.Date(), nullable=False),
        sa.Column("position_index", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint(
            "occurrence_ref",
            name=op.f("pk_occurrence_generation_cyclic"),
        ),
        sa.CheckConstraint(
            "isfinite(generated_date)",
            name=op.f("ck_occurrence_generation_cyclic_generated_date"),
        ),
        sa.CheckConstraint(
            "position_index >= 0",
            name=op.f("ck_occurrence_generation_cyclic_position_nonnegative"),
        ),
        _fk(
            ["occurrence_ref"],
            ["dante.occurrence_generation.occurrence_ref"],
            name="fk_occurrence_generation_cyclic_generation",
        ),
        schema=_DANTE_SCHEMA,
    )

    for table in _M6_TABLES:
        _deny_table(table)


def _create_integrity_routine() -> None:
    _sql(
        r"""
        CREATE FUNCTION dante.enforce_occurrence_generation_integrity()
        RETURNS trigger
        LANGUAGE plpgsql
        SECURITY INVOKER
        VOLATILE
        PARALLEL UNSAFE
        SET search_path = pg_catalog, dante, pg_temp
        AS $function$
DECLARE
    occurrence_value uuid;
    g record;
    source_family text;
    family_value text;
    range_value text;
    expected_count_value integer;
    current_state uuid;
    calendar_n integer;
    elapsed_n integer;
    quota_n integer;
    cyclic_n integer;
    coordinate_n integer;
    bad boolean := false;
    duplicate_exists boolean := false;

    cal record;
    cal_pattern text;
    cal_interval integer;
    cal_rule_clock text;
    cal_rule_zone text;
    cal_step_unit text;
    generated_local timestamp;
    wall_n integer;
    selector_n integer;
    anchor_date date;
    date_delta integer;
    month_delta integer;
    year_delta integer;
    days_in_month integer;
    ordinal_value integer;

    elapsed_state record;
    elapsed_seconds_value numeric;
    elapsed_anchor timestamptz;
    diff_seconds numeric;
    step_number numeric;
    lower_step numeric;
    first_step numeric;

    quota_state record;
    quota_count_value integer;
    quota_period_unit text;
    quota_period_span integer;
    quota_rule_frame text;
    quota_rule_zone text;
    quota_week_start integer;
    materialized_quota_count integer;
    period_anchor date;
    expected_period_end date;

    cyclic_state record;
    cyclic_cycle_length integer;
    cyclic_position_unit text;
    cyclic_anchor date;
    cyclic_step integer;
    expected_position integer;
    position_generates boolean;
    first_cyclic_step integer;
    cyclic_span integer;
    full_cycles integer;
    remainder_steps integer;
    true_per_cycle integer;
    true_in_remainder integer;
    start_position integer;
    generated_rank integer;

    from_kind text;
    from_inclusive boolean;
    from_date date;
    from_local timestamp;
    from_instant timestamptz;
    from_zone text;
    from_resolved timestamptz;
    until_kind text;
    until_inclusive boolean;
    until_date date;
    until_local timestamp;
    until_instant timestamptz;
    until_zone text;
    until_resolved timestamptz;
    comparison_instant timestamptz;
BEGIN
    occurrence_value := CASE
        WHEN TG_OP='DELETE' THEN OLD.occurrence_ref
        ELSE NEW.occurrence_ref
    END;

    SELECT *
    INTO g
    FROM dante.occurrence_generation
    WHERE occurrence_ref=occurrence_value;

    IF NOT FOUND THEN
        IF TG_OP='DELETE' THEN RETURN OLD; END IF;
        RETURN NEW;
    END IF;

    SELECT owner_family
    INTO source_family
    FROM dante.native_address
    WHERE native_ref=g.source_native_ref;

    IF source_family NOT IN ('routine','event') THEN
        bad := true;
    END IF;

    SELECT
        (SELECT count(*) FROM dante.occurrence_generation_calendar
         WHERE occurrence_ref=occurrence_value),
        (SELECT count(*) FROM dante.occurrence_generation_elapsed
         WHERE occurrence_ref=occurrence_value),
        (SELECT count(*) FROM dante.occurrence_generation_quota
         WHERE occurrence_ref=occurrence_value),
        (SELECT count(*) FROM dante.occurrence_generation_cyclic
         WHERE occurrence_ref=occurrence_value)
    INTO calendar_n, elapsed_n, quota_n, cyclic_n;

    coordinate_n := calendar_n + elapsed_n + quota_n + cyclic_n;

    IF g.origin_code='explicit_extra' THEN
        IF g.governing_recurrence_state_ref IS NOT NULL OR coordinate_n<>0 THEN
            bad := true;
        END IF;
    ELSE
        IF g.governing_recurrence_state_ref IS NULL THEN
            bad := true;
        ELSIF source_family='routine' THEN
            SELECT s.family_code, s.range_kind, s.expected_occurrence_count
            INTO family_value, range_value, expected_count_value
            FROM dante.routine_recurrence_state s
            WHERE s.material_state_ref=g.governing_recurrence_state_ref
              AND s.routine_ref=g.source_native_ref;

            IF NOT FOUND THEN
                bad := true;
            ELSE
                SELECT material_state_ref
                INTO current_state
                FROM dante.native_current_material_state
                WHERE native_owner_ref=g.source_native_ref
                  AND facet_code='routine.recurrence';
            END IF;
        ELSIF source_family='event' THEN
            SELECT s.family_code, s.range_kind, s.expected_occurrence_count
            INTO family_value, range_value, expected_count_value
            FROM dante.event_recurrence_state s
            WHERE s.material_state_ref=g.governing_recurrence_state_ref
              AND s.event_ref=g.source_native_ref;

            IF NOT FOUND THEN
                bad := true;
            ELSE
                SELECT material_state_ref
                INTO current_state
                FROM dante.native_current_material_state
                WHERE native_owner_ref=g.source_native_ref
                  AND facet_code='event.recurrence';
            END IF;
        END IF;

        IF current_state IS DISTINCT FROM g.governing_recurrence_state_ref THEN
            bad := true;
        END IF;

        IF family_value='calendar_wall_clock' THEN
            IF calendar_n<>1 OR elapsed_n+quota_n+cyclic_n<>0 THEN
                bad := true;
            END IF;
        ELSIF family_value='elapsed_interval' THEN
            IF elapsed_n<>1 OR calendar_n+quota_n+cyclic_n<>0 THEN
                bad := true;
            END IF;
        ELSIF family_value='quota_per_period' THEN
            IF quota_n<>1 OR calendar_n+elapsed_n+cyclic_n<>0 THEN
                bad := true;
            END IF;
        ELSIF family_value='cyclic_positional' THEN
            IF cyclic_n<>1 OR calendar_n+elapsed_n+quota_n<>0 THEN
                bad := true;
            END IF;
        ELSE
            bad := true;
        END IF;

        IF NOT bad AND source_family='routine' THEN
            SELECT boundary_kind,inclusive,date_value,local_value,instant_value,
                   zone_id,resolved_at
            INTO from_kind,from_inclusive,from_date,from_local,from_instant,
                 from_zone,from_resolved
            FROM dante.routine_recurrence_boundary_state
            WHERE material_state_ref=g.governing_recurrence_state_ref
              AND boundary_role='effective_from';

            SELECT boundary_kind,inclusive,date_value,local_value,instant_value,
                   zone_id,resolved_at
            INTO until_kind,until_inclusive,until_date,until_local,until_instant,
                 until_zone,until_resolved
            FROM dante.routine_recurrence_boundary_state
            WHERE material_state_ref=g.governing_recurrence_state_ref
              AND boundary_role='effective_until';
        ELSIF NOT bad AND source_family='event' THEN
            SELECT boundary_kind,inclusive,date_value,local_value,instant_value,
                   zone_id,resolved_at
            INTO from_kind,from_inclusive,from_date,from_local,from_instant,
                 from_zone,from_resolved
            FROM dante.event_recurrence_boundary_state
            WHERE material_state_ref=g.governing_recurrence_state_ref
              AND boundary_role='effective_from';

            SELECT boundary_kind,inclusive,date_value,local_value,instant_value,
                   zone_id,resolved_at
            INTO until_kind,until_inclusive,until_date,until_local,until_instant,
                 until_zone,until_resolved
            FROM dante.event_recurrence_boundary_state
            WHERE material_state_ref=g.governing_recurrence_state_ref
              AND boundary_role='effective_until';
        END IF;

        IF NOT bad AND family_value='calendar_wall_clock' THEN
            SELECT * INTO cal
            FROM dante.occurrence_generation_calendar
            WHERE occurrence_ref=occurrence_value;

            IF source_family='routine' THEN
                SELECT s.pattern_code,s.interval_count,s.clock_basis_code,
                       s.zone_id,s.step_unit_code
                INTO cal_pattern,cal_interval,cal_rule_clock,
                     cal_rule_zone,cal_step_unit
                FROM dante.routine_recurrence_calendar_state s
                WHERE s.material_state_ref=g.governing_recurrence_state_ref;
                SELECT count(*) INTO wall_n
                FROM dante.routine_recurrence_calendar_wall_time
                WHERE material_state_ref=g.governing_recurrence_state_ref;
                SELECT date_value INTO anchor_date
                FROM dante.routine_recurrence_boundary_state
                WHERE material_state_ref=g.governing_recurrence_state_ref
                  AND boundary_role='pattern_anchor';
            ELSE
                SELECT s.pattern_code,s.interval_count,s.clock_basis_code,
                       s.zone_id,s.step_unit_code
                INTO cal_pattern,cal_interval,cal_rule_clock,
                     cal_rule_zone,cal_step_unit
                FROM dante.event_recurrence_calendar_state s
                WHERE s.material_state_ref=g.governing_recurrence_state_ref;
                SELECT count(*) INTO wall_n
                FROM dante.event_recurrence_calendar_wall_time
                WHERE material_state_ref=g.governing_recurrence_state_ref;
                SELECT date_value INTO anchor_date
                FROM dante.event_recurrence_boundary_state
                WHERE material_state_ref=g.governing_recurrence_state_ref
                  AND boundary_role='pattern_anchor';
            END IF;

            IF cal.clock_basis_code IS DISTINCT FROM cal_rule_clock
               OR cal.zone_id IS DISTINCT FROM cal_rule_zone THEN
                bad := true;
            END IF;

            IF wall_n=0 THEN
                IF cal.generated_wall_time IS NOT NULL OR cal.resolved_at IS NOT NULL THEN bad:=true; END IF;
            ELSE
                IF cal.generated_wall_time IS NULL THEN bad:=true;
                ELSIF source_family='routine' THEN
                    SELECT count(*) INTO selector_n FROM dante.routine_recurrence_calendar_wall_time
                    WHERE material_state_ref=g.governing_recurrence_state_ref AND wall_time=cal.generated_wall_time;
                    IF selector_n<>1 THEN bad:=true; END IF;
                ELSE
                    SELECT count(*) INTO selector_n FROM dante.event_recurrence_calendar_wall_time
                    WHERE material_state_ref=g.governing_recurrence_state_ref AND wall_time=cal.generated_wall_time;
                    IF selector_n<>1 THEN bad:=true; END IF;
                END IF;
                IF cal.clock_basis_code='named_zone' AND cal.resolved_at IS NULL THEN bad:=true; END IF;
            END IF;

            IF cal_pattern='daily' THEN
                IF cal_interval>1 AND (anchor_date IS NULL OR mod(cal.generated_date-anchor_date,cal_interval)<>0) THEN bad:=true; END IF;
            ELSIF cal_pattern='weekly_weekdays' THEN
                IF source_family='routine' THEN
                    SELECT count(*) INTO selector_n FROM dante.routine_recurrence_calendar_weekday
                    WHERE material_state_ref=g.governing_recurrence_state_ref AND weekday_number=extract(isodow from cal.generated_date)::int;
                ELSE
                    SELECT count(*) INTO selector_n FROM dante.event_recurrence_calendar_weekday
                    WHERE material_state_ref=g.governing_recurrence_state_ref AND weekday_number=extract(isodow from cal.generated_date)::int;
                END IF;
                IF selector_n<>1 THEN bad:=true; END IF;
                IF cal_interval>1 THEN
                    IF anchor_date IS NULL THEN bad:=true;
                    ELSE
                        date_delta := (cal.generated_date-(extract(isodow from cal.generated_date)::int-1)) - (anchor_date-(extract(isodow from anchor_date)::int-1));
                        IF mod(date_delta/7,cal_interval)<>0 THEN bad:=true; END IF;
                    END IF;
                END IF;
            ELSIF cal_pattern='monthly_month_days' THEN
                days_in_month := extract(day from (date_trunc('month',cal.generated_date)+interval '1 month - 1 day'))::int;
                IF source_family='routine' THEN
                    SELECT count(*) INTO selector_n FROM dante.routine_recurrence_calendar_month_day
                    WHERE material_state_ref=g.governing_recurrence_state_ref AND (month_day=extract(day from cal.generated_date)::int OR month_day=-(days_in_month-extract(day from cal.generated_date)::int+1));
                ELSE
                    SELECT count(*) INTO selector_n FROM dante.event_recurrence_calendar_month_day
                    WHERE material_state_ref=g.governing_recurrence_state_ref AND (month_day=extract(day from cal.generated_date)::int OR month_day=-(days_in_month-extract(day from cal.generated_date)::int+1));
                END IF;
                IF selector_n<1 THEN bad:=true; END IF;
                IF cal_interval>1 THEN
                    IF anchor_date IS NULL THEN bad:=true;
                    ELSE
                        month_delta := (extract(year from cal.generated_date)::int-extract(year from anchor_date)::int)*12 + extract(month from cal.generated_date)::int-extract(month from anchor_date)::int;
                        IF mod(month_delta,cal_interval)<>0 THEN bad:=true; END IF;
                    END IF;
                END IF;
            ELSIF cal_pattern='monthly_ordinal_weekdays' THEN
                days_in_month := extract(day from (date_trunc('month',cal.generated_date)+interval '1 month - 1 day'))::int;
                ordinal_value := ((extract(day from cal.generated_date)::int-1)/7)+1;
                IF source_family='routine' THEN
                    SELECT count(*) INTO selector_n FROM dante.routine_recurrence_calendar_ordinal_weekday
                    WHERE material_state_ref=g.governing_recurrence_state_ref AND weekday_number=extract(isodow from cal.generated_date)::int AND ordinal IN (ordinal_value,-(((days_in_month-extract(day from cal.generated_date)::int)/7)+1));
                ELSE
                    SELECT count(*) INTO selector_n FROM dante.event_recurrence_calendar_ordinal_weekday
                    WHERE material_state_ref=g.governing_recurrence_state_ref AND weekday_number=extract(isodow from cal.generated_date)::int AND ordinal IN (ordinal_value,-(((days_in_month-extract(day from cal.generated_date)::int)/7)+1));
                END IF;
                IF selector_n<1 THEN bad:=true; END IF;
                IF cal_interval>1 THEN
                    IF anchor_date IS NULL THEN bad:=true;
                    ELSE
                        month_delta := (extract(year from cal.generated_date)::int-extract(year from anchor_date)::int)*12 + extract(month from cal.generated_date)::int-extract(month from anchor_date)::int;
                        IF mod(month_delta,cal_interval)<>0 THEN bad:=true; END IF;
                    END IF;
                END IF;
            ELSIF cal_pattern='yearly_month_days' THEN
                days_in_month := extract(day from (date_trunc('month',cal.generated_date)+interval '1 month - 1 day'))::int;
                IF source_family='routine' THEN
                    SELECT count(*) INTO selector_n FROM dante.routine_recurrence_calendar_year_month_day
                    WHERE material_state_ref=g.governing_recurrence_state_ref AND month_number=extract(month from cal.generated_date)::int AND (month_day=extract(day from cal.generated_date)::int OR month_day=-(days_in_month-extract(day from cal.generated_date)::int+1));
                ELSE
                    SELECT count(*) INTO selector_n FROM dante.event_recurrence_calendar_year_month_day
                    WHERE material_state_ref=g.governing_recurrence_state_ref AND month_number=extract(month from cal.generated_date)::int AND (month_day=extract(day from cal.generated_date)::int OR month_day=-(days_in_month-extract(day from cal.generated_date)::int+1));
                END IF;
                IF selector_n<1 THEN bad:=true; END IF;
                IF cal_interval>1 THEN
                    IF anchor_date IS NULL THEN bad:=true;
                    ELSE
                        year_delta := extract(year from cal.generated_date)::int-extract(year from anchor_date)::int;
                        IF mod(year_delta,cal_interval)<>0 THEN bad:=true; END IF;
                    END IF;
                END IF;
            ELSIF cal_pattern='anchor_step' THEN
                IF anchor_date IS NULL THEN bad:=true;
                ELSE
                    IF cal_step_unit='day' THEN IF mod(cal.generated_date-anchor_date,cal_interval)<>0 THEN bad:=true; END IF;
                    ELSIF cal_step_unit='week' THEN IF mod(cal.generated_date-anchor_date,7*cal_interval)<>0 THEN bad:=true; END IF;
                    ELSIF cal_step_unit='month' THEN
                        month_delta := (extract(year from cal.generated_date)::int-extract(year from anchor_date)::int)*12 + extract(month from cal.generated_date)::int-extract(month from anchor_date)::int;
                        IF mod(month_delta,cal_interval)<>0 OR extract(day from cal.generated_date)::int<>extract(day from anchor_date)::int THEN bad:=true; END IF;
                    ELSIF cal_step_unit='year' THEN
                        year_delta := extract(year from cal.generated_date)::int-extract(year from anchor_date)::int;
                        IF mod(year_delta,cal_interval)<>0 OR extract(month from cal.generated_date)::int<>extract(month from anchor_date)::int OR extract(day from cal.generated_date)::int<>extract(day from anchor_date)::int THEN bad:=true; END IF;
                    ELSE bad:=true; END IF;
                END IF;
            ELSE bad:=true; END IF;

            generated_local := CASE WHEN cal.generated_wall_time IS NULL THEN NULL ELSE cal.generated_date+cal.generated_wall_time END;
            comparison_instant := CASE WHEN cal.clock_basis_code='named_zone' THEN cal.resolved_at WHEN cal.clock_basis_code='absolute_utc' AND generated_local IS NOT NULL THEN generated_local AT TIME ZONE 'UTC' ELSE NULL END;
            IF from_kind IS NOT NULL THEN
                IF from_kind='date' THEN IF cal.generated_date<from_date OR (cal.generated_date=from_date AND from_inclusive=false) THEN bad:=true; END IF;
                ELSIF from_kind IN ('floating_local','named_zone_local') THEN IF generated_local IS NULL OR generated_local<from_local OR (generated_local=from_local AND from_inclusive=false) THEN bad:=true; END IF;
                ELSIF from_kind='absolute_instant' THEN IF comparison_instant IS NULL OR comparison_instant<from_instant OR (comparison_instant=from_instant AND from_inclusive=false) THEN bad:=true; END IF;
                END IF;
            END IF;
            IF until_kind IS NOT NULL THEN
                IF until_kind='date' THEN IF cal.generated_date>until_date OR (cal.generated_date=until_date AND until_inclusive=false) THEN bad:=true; END IF;
                ELSIF until_kind IN ('floating_local','named_zone_local') THEN IF generated_local IS NULL OR generated_local>until_local OR (generated_local=until_local AND until_inclusive=false) THEN bad:=true; END IF;
                ELSIF until_kind='absolute_instant' THEN IF comparison_instant IS NULL OR comparison_instant>until_instant OR (comparison_instant=until_instant AND until_inclusive=false) THEN bad:=true; END IF;
                END IF;
            END IF;
            SELECT EXISTS (
                SELECT 1 FROM dante.occurrence_generation og
                JOIN dante.occurrence_generation_calendar x ON x.occurrence_ref=og.occurrence_ref
                WHERE og.source_native_ref=g.source_native_ref
                  AND og.governing_recurrence_state_ref=g.governing_recurrence_state_ref
                  AND og.origin_code='recurrence_generated'
                  AND og.occurrence_ref<>occurrence_value
                  AND x.generated_date=cal.generated_date
                  AND x.generated_wall_time IS NOT DISTINCT FROM cal.generated_wall_time
                  AND x.clock_basis_code=cal.clock_basis_code
                  AND x.zone_id IS NOT DISTINCT FROM cal.zone_id
                  AND x.resolved_at IS NOT DISTINCT FROM cal.resolved_at
            ) INTO duplicate_exists;
            IF duplicate_exists THEN bad:=true; END IF;
        ELSIF NOT bad AND family_value='elapsed_interval' THEN
            SELECT * INTO elapsed_state FROM dante.occurrence_generation_elapsed WHERE occurrence_ref=occurrence_value;
            IF source_family='routine' THEN
                SELECT r.elapsed_seconds,r.anchor_at INTO elapsed_seconds_value,elapsed_anchor
                FROM dante.routine_recurrence_elapsed_state r WHERE r.material_state_ref=g.governing_recurrence_state_ref;
            ELSE
                SELECT r.elapsed_seconds,r.anchor_at INTO elapsed_seconds_value,elapsed_anchor
                FROM dante.event_recurrence_elapsed_state r WHERE r.material_state_ref=g.governing_recurrence_state_ref;
            END IF;
            diff_seconds := extract(epoch from (elapsed_state.expected_at-elapsed_anchor));
            step_number := diff_seconds/elapsed_seconds_value;
            IF step_number<1 OR step_number<>trunc(step_number) THEN bad:=true; END IF;
            IF from_kind IS NOT NULL AND (from_kind<>'absolute_instant' OR elapsed_state.expected_at<from_instant OR (elapsed_state.expected_at=from_instant AND from_inclusive=false)) THEN bad:=true; END IF;
            IF until_kind IS NOT NULL AND (until_kind<>'absolute_instant' OR elapsed_state.expected_at>until_instant OR (elapsed_state.expected_at=until_instant AND until_inclusive=false)) THEN bad:=true; END IF;
            IF range_value='expected_count' THEN
                IF from_kind<>'absolute_instant' OR from_instant IS NULL THEN bad:=true;
                ELSE
                    lower_step := extract(epoch from (from_instant-elapsed_anchor))/elapsed_seconds_value;
                    IF from_inclusive THEN first_step:=greatest(1::numeric,ceil(lower_step)); ELSE first_step:=greatest(1::numeric,floor(lower_step)+1); END IF;
                    IF step_number<first_step OR step_number-first_step+1>expected_count_value THEN bad:=true; END IF;
                END IF;
            END IF;
            SELECT EXISTS (
                SELECT 1 FROM dante.occurrence_generation og JOIN dante.occurrence_generation_elapsed x ON x.occurrence_ref=og.occurrence_ref
                WHERE og.source_native_ref=g.source_native_ref AND og.governing_recurrence_state_ref=g.governing_recurrence_state_ref
                  AND og.origin_code='recurrence_generated' AND og.occurrence_ref<>occurrence_value AND x.expected_at=elapsed_state.expected_at
            ) INTO duplicate_exists;
            IF duplicate_exists THEN bad:=true; END IF;
        ELSIF NOT bad AND family_value='quota_per_period' THEN
            SELECT * INTO quota_state FROM dante.occurrence_generation_quota WHERE occurrence_ref=occurrence_value;
            IF source_family='routine' THEN
                PERFORM 1 FROM dante.routine WHERE routine_ref=g.source_native_ref FOR UPDATE;
                SELECT q.quota_count,q.period_unit_code,q.period_span,q.frame_code,q.zone_id,q.week_start
                INTO quota_count_value,quota_period_unit,quota_period_span,quota_rule_frame,quota_rule_zone,quota_week_start
                FROM dante.routine_recurrence_quota_state q WHERE q.material_state_ref=g.governing_recurrence_state_ref;
                SELECT date_value INTO period_anchor FROM dante.routine_recurrence_boundary_state WHERE material_state_ref=g.governing_recurrence_state_ref AND boundary_role='pattern_anchor';
            ELSE
                PERFORM 1 FROM dante.event WHERE event_ref=g.source_native_ref FOR UPDATE;
                SELECT q.quota_count,q.period_unit_code,q.period_span,q.frame_code,q.zone_id,q.week_start
                INTO quota_count_value,quota_period_unit,quota_period_span,quota_rule_frame,quota_rule_zone,quota_week_start
                FROM dante.event_recurrence_quota_state q WHERE q.material_state_ref=g.governing_recurrence_state_ref;
                SELECT date_value INTO period_anchor FROM dante.event_recurrence_boundary_state WHERE material_state_ref=g.governing_recurrence_state_ref AND boundary_role='pattern_anchor';
            END IF;
            IF quota_state.frame_code IS DISTINCT FROM quota_rule_frame OR quota_state.zone_id IS DISTINCT FROM quota_rule_zone THEN bad:=true; END IF;
            IF quota_period_unit='day' THEN
                expected_period_end:=quota_state.period_start_date+quota_period_span;
                IF quota_period_span>1 AND (period_anchor IS NULL OR mod(quota_state.period_start_date-period_anchor,quota_period_span)<>0) THEN bad:=true; END IF;
            ELSIF quota_period_unit='week' THEN
                expected_period_end:=quota_state.period_start_date+7*quota_period_span;
                IF extract(isodow from quota_state.period_start_date)::int<>quota_week_start THEN bad:=true;
                ELSIF quota_period_span>1 AND (period_anchor IS NULL OR mod(quota_state.period_start_date-period_anchor,7*quota_period_span)<>0) THEN bad:=true; END IF;
            ELSIF quota_period_unit='month' THEN
                expected_period_end:=(quota_state.period_start_date+make_interval(months=>quota_period_span))::date;
                IF extract(day from quota_state.period_start_date)::int<>1 THEN bad:=true;
                ELSIF quota_period_span>1 THEN
                    IF period_anchor IS NULL THEN bad:=true;
                    ELSE month_delta:=(extract(year from quota_state.period_start_date)::int-extract(year from period_anchor)::int)*12+extract(month from quota_state.period_start_date)::int-extract(month from period_anchor)::int; IF mod(month_delta,quota_period_span)<>0 THEN bad:=true; END IF;
                    END IF;
                END IF;
            ELSIF quota_period_unit='year' THEN
                expected_period_end:=(quota_state.period_start_date+make_interval(years=>quota_period_span))::date;
                IF extract(month from quota_state.period_start_date)::int<>1 OR extract(day from quota_state.period_start_date)::int<>1 THEN bad:=true;
                ELSIF quota_period_span>1 THEN
                    IF period_anchor IS NULL THEN bad:=true;
                    ELSE year_delta:=extract(year from quota_state.period_start_date)::int-extract(year from period_anchor)::int; IF mod(year_delta,quota_period_span)<>0 THEN bad:=true; END IF;
                    END IF;
                END IF;
            ELSE bad:=true; END IF;
            IF quota_state.period_end_date_exclusive IS DISTINCT FROM expected_period_end THEN bad:=true; END IF;
            IF from_kind IS NOT NULL AND (from_kind<>'date' OR from_inclusive IS DISTINCT FROM true OR quota_state.period_start_date<from_date) THEN bad:=true; END IF;
            IF until_kind IS NOT NULL AND (until_kind<>'date' OR until_inclusive IS DISTINCT FROM false OR quota_state.period_end_date_exclusive>until_date) THEN bad:=true; END IF;
            IF range_value='expected_count' THEN bad:=true; END IF;
            SELECT count(*) INTO materialized_quota_count
            FROM dante.occurrence_generation og JOIN dante.occurrence_generation_quota q ON q.occurrence_ref=og.occurrence_ref
            WHERE og.source_native_ref=g.source_native_ref AND og.governing_recurrence_state_ref=g.governing_recurrence_state_ref
              AND og.origin_code='recurrence_generated' AND q.period_start_date=quota_state.period_start_date AND q.period_end_date_exclusive=quota_state.period_end_date_exclusive;
            IF materialized_quota_count>quota_count_value THEN bad:=true; END IF;
        ELSIF NOT bad AND family_value='cyclic_positional' THEN
            SELECT * INTO cyclic_state FROM dante.occurrence_generation_cyclic WHERE occurrence_ref=occurrence_value;
            IF source_family='routine' THEN
                SELECT c.cycle_length,c.position_unit_code INTO cyclic_cycle_length,cyclic_position_unit FROM dante.routine_recurrence_cyclic_state c WHERE c.material_state_ref=g.governing_recurrence_state_ref;
                SELECT date_value INTO cyclic_anchor FROM dante.routine_recurrence_boundary_state WHERE material_state_ref=g.governing_recurrence_state_ref AND boundary_role='pattern_anchor';
            ELSE
                SELECT c.cycle_length,c.position_unit_code INTO cyclic_cycle_length,cyclic_position_unit FROM dante.event_recurrence_cyclic_state c WHERE c.material_state_ref=g.governing_recurrence_state_ref;
                SELECT date_value INTO cyclic_anchor FROM dante.event_recurrence_boundary_state WHERE material_state_ref=g.governing_recurrence_state_ref AND boundary_role='pattern_anchor';
            END IF;
            IF cyclic_anchor IS NULL OR cyclic_state.generated_date<cyclic_anchor THEN bad:=true;
            ELSIF cyclic_position_unit='day' THEN cyclic_step:=cyclic_state.generated_date-cyclic_anchor;
            ELSIF cyclic_position_unit='week' THEN date_delta:=cyclic_state.generated_date-cyclic_anchor; IF mod(date_delta,7)<>0 THEN bad:=true; END IF; cyclic_step:=date_delta/7;
            ELSE bad:=true; END IF;
            IF NOT bad THEN
                expected_position:=mod(cyclic_step,cyclic_cycle_length);
                IF cyclic_state.position_index<>expected_position THEN bad:=true; END IF;
                IF source_family='routine' THEN
                    SELECT generates_expected INTO position_generates FROM dante.routine_recurrence_cycle_position WHERE material_state_ref=g.governing_recurrence_state_ref AND position_index=expected_position;
                ELSE
                    SELECT generates_expected INTO position_generates FROM dante.event_recurrence_cycle_position WHERE material_state_ref=g.governing_recurrence_state_ref AND position_index=expected_position;
                END IF;
                IF position_generates IS DISTINCT FROM true THEN bad:=true; END IF;
            END IF;
            IF from_kind IS NOT NULL AND (from_kind<>'date' OR cyclic_state.generated_date<from_date OR (cyclic_state.generated_date=from_date AND from_inclusive=false)) THEN bad:=true; END IF;
            IF until_kind IS NOT NULL AND (until_kind<>'date' OR cyclic_state.generated_date>until_date OR (cyclic_state.generated_date=until_date AND until_inclusive=false)) THEN bad:=true; END IF;
            IF range_value='expected_count' THEN
                IF from_kind<>'date' OR from_date IS NULL THEN bad:=true;
                ELSE
                    IF cyclic_position_unit='day' THEN first_cyclic_step:=greatest(0,from_date-cyclic_anchor+CASE WHEN from_inclusive THEN 0 ELSE 1 END);
                    ELSE date_delta:=from_date-cyclic_anchor; first_cyclic_step:=greatest(0,CASE WHEN date_delta<=0 THEN 0 WHEN mod(date_delta,7)=0 THEN date_delta/7+CASE WHEN from_inclusive THEN 0 ELSE 1 END ELSE (date_delta/7)+1 END); END IF;
                    IF cyclic_step<first_cyclic_step THEN bad:=true;
                    ELSE
                        cyclic_span:=cyclic_step-first_cyclic_step+1; full_cycles:=cyclic_span/cyclic_cycle_length; remainder_steps:=mod(cyclic_span,cyclic_cycle_length); start_position:=mod(first_cyclic_step,cyclic_cycle_length);
                        IF source_family='routine' THEN
                            SELECT count(*) INTO true_per_cycle FROM dante.routine_recurrence_cycle_position WHERE material_state_ref=g.governing_recurrence_state_ref AND generates_expected=true;
                            SELECT count(*) INTO true_in_remainder FROM dante.routine_recurrence_cycle_position WHERE material_state_ref=g.governing_recurrence_state_ref AND generates_expected=true AND ((start_position+remainder_steps<=cyclic_cycle_length AND position_index>=start_position AND position_index<start_position+remainder_steps) OR (start_position+remainder_steps>cyclic_cycle_length AND (position_index>=start_position OR position_index<start_position+remainder_steps-cyclic_cycle_length)));
                        ELSE
                            SELECT count(*) INTO true_per_cycle FROM dante.event_recurrence_cycle_position WHERE material_state_ref=g.governing_recurrence_state_ref AND generates_expected=true;
                            SELECT count(*) INTO true_in_remainder FROM dante.event_recurrence_cycle_position WHERE material_state_ref=g.governing_recurrence_state_ref AND generates_expected=true AND ((start_position+remainder_steps<=cyclic_cycle_length AND position_index>=start_position AND position_index<start_position+remainder_steps) OR (start_position+remainder_steps>cyclic_cycle_length AND (position_index>=start_position OR position_index<start_position+remainder_steps-cyclic_cycle_length)));
                        END IF;
                        generated_rank:=full_cycles*true_per_cycle+true_in_remainder;
                        IF generated_rank>expected_count_value THEN bad:=true; END IF;
                    END IF;
                END IF;
            END IF;
            SELECT EXISTS (
                SELECT 1 FROM dante.occurrence_generation og JOIN dante.occurrence_generation_cyclic x ON x.occurrence_ref=og.occurrence_ref
                WHERE og.source_native_ref=g.source_native_ref AND og.governing_recurrence_state_ref=g.governing_recurrence_state_ref
                  AND og.origin_code='recurrence_generated' AND og.occurrence_ref<>occurrence_value
                  AND x.generated_date=cyclic_state.generated_date AND x.position_index=cyclic_state.position_index
            ) INTO duplicate_exists;
            IF duplicate_exists THEN bad:=true; END IF;
        END IF;
    END IF;

    IF bad THEN
        RAISE EXCEPTION USING
            ERRCODE='23514',
            CONSTRAINT=TG_NAME,
            TABLE=TG_TABLE_NAME,
            SCHEMA=TG_TABLE_SCHEMA,
            MESSAGE='Occurrence generation aggregate rejected',
            DETAIL='origin, current governing recurrence state and exact generated coordinate must satisfy the frozen Role-13 contract';
    END IF;

    IF TG_OP='DELETE' THEN RETURN OLD; END IF;
    RETURN NEW;
END;
        $function$
        """
    )
    _sql(
        f"ALTER FUNCTION dante.enforce_occurrence_generation_integrity() "
        f"OWNER TO {_OWNER_ROLE}"
    )
    _sql(
        "REVOKE ALL PRIVILEGES ON FUNCTION "
        "dante.enforce_occurrence_generation_integrity() "
        f"FROM PUBLIC, {_RUNTIME_ROLE}, {_MIGRATOR_ROLE}"
    )


def _create_triggers() -> None:
    immediate = (
        (
            "trg_occurrence_generation_native_ref",
            "occurrence_generation",
            "INSERT OR UPDATE OF source_native_ref",
            "enforce_native_ref_eligibility",
        ),
        (
            "trg_occurrence_generation_calendar_iana_timezone",
            "occurrence_generation_calendar",
            "INSERT OR UPDATE OF generated_date, generated_wall_time, clock_basis_code, zone_id, resolved_at",
            "validate_iana_timezone",
        ),
        (
            "trg_occurrence_generation_quota_iana_timezone",
            "occurrence_generation_quota",
            "INSERT OR UPDATE OF frame_code, zone_id",
            "validate_iana_timezone",
        ),
    )
    deferred = (
        ("ctrg_occurrence_owner_complete", "occurrence", "INSERT", "enforce_owner_creation_completeness"),
        ("ctrg_occurrence_generation_generation", "occurrence_generation", "INSERT OR UPDATE OR DELETE", "enforce_occurrence_generation_integrity"),
        ("ctrg_occurrence_generation_calendar_generation", "occurrence_generation_calendar", "INSERT OR UPDATE OR DELETE", "enforce_occurrence_generation_integrity"),
        ("ctrg_occurrence_generation_elapsed_generation", "occurrence_generation_elapsed", "INSERT OR UPDATE OR DELETE", "enforce_occurrence_generation_integrity"),
        ("ctrg_occurrence_generation_quota_generation", "occurrence_generation_quota", "INSERT OR UPDATE OR DELETE", "enforce_occurrence_generation_integrity"),
        ("ctrg_occurrence_generation_cyclic_generation", "occurrence_generation_cyclic", "INSERT OR UPDATE OR DELETE", "enforce_occurrence_generation_integrity"),
    )
    for name, table, event_sql, routine in immediate:
        _sql(f"CREATE TRIGGER {name} BEFORE {event_sql} ON dante.{table} FOR EACH ROW EXECUTE FUNCTION dante.{routine}()")
    for name, table, event_sql, routine in deferred:
        _sql(f"CREATE CONSTRAINT TRIGGER {name} AFTER {event_sql} ON dante.{table} DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION dante.{routine}()")


def upgrade() -> None:
    """Install M6 Occurrence generation without activating M7 runtime ACLs."""
    _create_tables()
    _create_integrity_routine()
    _create_triggers()


def downgrade() -> None:
    """Return exactly to the closed CP6-M05 surface."""
    deferred = (
        ("ctrg_occurrence_generation_cyclic_generation", "occurrence_generation_cyclic"),
        ("ctrg_occurrence_generation_quota_generation", "occurrence_generation_quota"),
        ("ctrg_occurrence_generation_elapsed_generation", "occurrence_generation_elapsed"),
        ("ctrg_occurrence_generation_calendar_generation", "occurrence_generation_calendar"),
        ("ctrg_occurrence_generation_generation", "occurrence_generation"),
        ("ctrg_occurrence_owner_complete", "occurrence"),
    )
    immediate = (
        ("trg_occurrence_generation_quota_iana_timezone", "occurrence_generation_quota"),
        ("trg_occurrence_generation_calendar_iana_timezone", "occurrence_generation_calendar"),
        ("trg_occurrence_generation_native_ref", "occurrence_generation"),
    )
    for name, table in deferred:
        _sql(f"DROP TRIGGER {name} ON dante.{table}")
    for name, table in immediate:
        _sql(f"DROP TRIGGER {name} ON dante.{table}")
    _sql("DROP FUNCTION dante.enforce_occurrence_generation_integrity()")
    for table in reversed(_M6_TABLES):
        op.drop_table(table, schema=_DANTE_SCHEMA)
