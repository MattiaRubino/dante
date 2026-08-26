"""SQLAlchemy row mappings for owner-bound Routine/Event Recurrence."""

from datetime import date, datetime, time
from decimal import Decimal

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Date,
    DateTime,
    ForeignKeyConstraint,
    Index,
    Integer,
    Numeric,
    SmallInteger,
    Text,
    Time,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column

from dante.platform.database.metadata import Base
from dante.platform.database.references import MaterialStateRef, NativeRef


class RoutineRecurrenceStateRow(Base):
    """SQLAlchemy row mapping for ``dante.routine_recurrence_state``."""

    __tablename__ = "routine_recurrence_state"
    __table_args__ = (
        CheckConstraint(
            "family_code IN ('calendar_wall_clock','elapsed_interval','quota_per_period','cyclic_positional')",
            name="family_code",
        ),
        CheckConstraint(
            "range_kind IN ('open','until_boundary','expected_count')",
            name="range_kind",
        ),
        CheckConstraint(
            "((range_kind='expected_count' AND expected_occurrence_count IS NOT NULL AND expected_occurrence_count > 0) OR (range_kind IN ('open','until_boundary') AND expected_occurrence_count IS NULL))",
            name="expected_count",
        ),
        ForeignKeyConstraint(
            ["material_state_ref"],
            ["dante.material_state_address.material_state_ref"],
            name="fk_routine_recurrence_state_state_address",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        ForeignKeyConstraint(
            ["routine_ref"],
            ["dante.routine.routine_ref"],
            name="fk_routine_recurrence_state_routine_ref_routine",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        Index(
            "ix_routine_recurrence_state_routine_ref",
            "routine_ref",
        ),
    )

    material_state_ref: Mapped[MaterialStateRef] = mapped_column(primary_key=True)
    routine_ref: Mapped[NativeRef] = mapped_column(nullable=False)
    family_code: Mapped[str] = mapped_column(Text, nullable=False)
    range_kind: Mapped[str] = mapped_column(Text, nullable=False)
    expected_occurrence_count: Mapped[int | None] = mapped_column(Integer)


class RoutineRecurrenceCurrentHistoryRow(Base):
    """SQLAlchemy row mapping for ``dante.routine_recurrence_current_history``."""

    __tablename__ = "routine_recurrence_current_history"
    __table_args__ = (
        CheckConstraint(
            "isfinite(current_from_at) AND (current_until_at IS NULL OR (isfinite(current_until_at) AND current_until_at > current_from_at))",
            name="current_interval",
        ),
        ForeignKeyConstraint(
            ["routine_ref"],
            ["dante.routine.routine_ref"],
            name="fk_routine_recurrence_current_history_routine_ref_routine",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        ForeignKeyConstraint(
            ["material_state_ref"],
            ["dante.routine_recurrence_state.material_state_ref"],
            name="fk_routine_recurrence_current_history_recurrence_state",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        Index(
            "ux_routine_recurrence_current_history_open",
            "routine_ref",
            unique=True,
            postgresql_where=text("current_until_at IS NULL"),
        ),
        Index(
            "ix_routine_recurrence_current_history_material_state_ref",
            "material_state_ref",
        ),
    )

    routine_ref: Mapped[NativeRef] = mapped_column(primary_key=True)
    material_state_ref: Mapped[MaterialStateRef] = mapped_column(nullable=False)
    current_from_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), primary_key=True)
    current_until_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class RoutineRecurrenceBoundaryStateRow(Base):
    """SQLAlchemy row mapping for ``dante.routine_recurrence_boundary_state``."""

    __tablename__ = "routine_recurrence_boundary_state"
    __table_args__ = (
        CheckConstraint(
            "boundary_role IN ('pattern_anchor','effective_from','effective_until')",
            name="boundary_role",
        ),
        CheckConstraint(
            "boundary_kind IN ('date','floating_local','named_zone_local','absolute_instant')",
            name="boundary_kind",
        ),
        CheckConstraint(
            "((boundary_kind='date' AND date_value IS NOT NULL AND isfinite(date_value) AND local_value IS NULL AND zone_id IS NULL AND instant_value IS NULL AND resolved_at IS NULL) OR (boundary_kind='floating_local' AND local_value IS NOT NULL AND isfinite(local_value) AND date_value IS NULL AND zone_id IS NULL AND instant_value IS NULL AND resolved_at IS NULL) OR (boundary_kind='named_zone_local' AND local_value IS NOT NULL AND isfinite(local_value) AND zone_id IS NOT NULL AND date_value IS NULL AND instant_value IS NULL AND (resolved_at IS NULL OR isfinite(resolved_at))) OR (boundary_kind='absolute_instant' AND instant_value IS NOT NULL AND isfinite(instant_value) AND date_value IS NULL AND local_value IS NULL AND zone_id IS NULL AND resolved_at IS NULL))",
            name="boundary_payload",
        ),
        CheckConstraint(
            "((boundary_role='pattern_anchor' AND inclusive IS NULL) OR (boundary_role IN ('effective_from','effective_until') AND inclusive IS NOT NULL))",
            name="inclusive_role",
        ),
        ForeignKeyConstraint(
            ["material_state_ref"],
            ["dante.routine_recurrence_state.material_state_ref"],
            name="fk_routine_recurrence_boundary_state_recurrence_state",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
    )

    material_state_ref: Mapped[MaterialStateRef] = mapped_column(primary_key=True)
    boundary_role: Mapped[str] = mapped_column(Text, primary_key=True)
    boundary_kind: Mapped[str] = mapped_column(Text, nullable=False)
    inclusive: Mapped[bool | None] = mapped_column(Boolean)
    date_value: Mapped[date | None] = mapped_column(Date)
    local_value: Mapped[datetime | None] = mapped_column(DateTime(timezone=False))
    zone_id: Mapped[str | None] = mapped_column(Text)
    instant_value: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class RoutineRecurrenceCalendarStateRow(Base):
    """SQLAlchemy row mapping for ``dante.routine_recurrence_calendar_state``."""

    __tablename__ = "routine_recurrence_calendar_state"
    __table_args__ = (
        CheckConstraint(
            "pattern_code IN ('daily','weekly_weekdays','monthly_month_days','monthly_ordinal_weekdays','yearly_month_days','anchor_step')",
            name="pattern_code",
        ),
        CheckConstraint(
            "interval_count > 0",
            name="interval_positive",
        ),
        CheckConstraint(
            "clock_basis_code IN ('floating_local','named_zone','absolute_utc')",
            name="clock_basis",
        ),
        CheckConstraint(
            "((clock_basis_code='named_zone' AND zone_id IS NOT NULL) OR (clock_basis_code IN ('floating_local','absolute_utc') AND zone_id IS NULL))",
            name="zone_basis",
        ),
        CheckConstraint(
            "((pattern_code='anchor_step' AND step_unit_code IS NOT NULL AND step_unit_code IN ('day','week','month','year')) OR (pattern_code<>'anchor_step' AND step_unit_code IS NULL))",
            name="step_unit",
        ),
        ForeignKeyConstraint(
            ["material_state_ref"],
            ["dante.routine_recurrence_state.material_state_ref"],
            name="fk_routine_recurrence_calendar_state_recurrence_state",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
    )

    material_state_ref: Mapped[MaterialStateRef] = mapped_column(primary_key=True)
    pattern_code: Mapped[str] = mapped_column(Text, nullable=False)
    interval_count: Mapped[int] = mapped_column(Integer, nullable=False)
    clock_basis_code: Mapped[str] = mapped_column(Text, nullable=False)
    zone_id: Mapped[str | None] = mapped_column(Text)
    step_unit_code: Mapped[str | None] = mapped_column(Text)


class RoutineRecurrenceCalendarWallTimeRow(Base):
    """SQLAlchemy row mapping for ``dante.routine_recurrence_calendar_wall_time``."""

    __tablename__ = "routine_recurrence_calendar_wall_time"
    __table_args__ = (
        ForeignKeyConstraint(
            ["material_state_ref"],
            ["dante.routine_recurrence_calendar_state.material_state_ref"],
            name="fk_routine_recurrence_calendar_wall_time_calendar_state",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
    )

    material_state_ref: Mapped[MaterialStateRef] = mapped_column(primary_key=True)
    wall_time: Mapped[time] = mapped_column(Time(timezone=False), primary_key=True)


class RoutineRecurrenceCalendarWeekdayRow(Base):
    """SQLAlchemy row mapping for ``dante.routine_recurrence_calendar_weekday``."""

    __tablename__ = "routine_recurrence_calendar_weekday"
    __table_args__ = (
        CheckConstraint(
            "weekday_number BETWEEN 1 AND 7",
            name="weekday_range",
        ),
        ForeignKeyConstraint(
            ["material_state_ref"],
            ["dante.routine_recurrence_calendar_state.material_state_ref"],
            name="fk_routine_recurrence_calendar_weekday_calendar_state",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
    )

    material_state_ref: Mapped[MaterialStateRef] = mapped_column(primary_key=True)
    weekday_number: Mapped[int] = mapped_column(SmallInteger, primary_key=True)


class RoutineRecurrenceCalendarMonthDayRow(Base):
    """SQLAlchemy row mapping for ``dante.routine_recurrence_calendar_month_day``."""

    __tablename__ = "routine_recurrence_calendar_month_day"
    __table_args__ = (
        CheckConstraint(
            "(month_day BETWEEN 1 AND 31 OR month_day BETWEEN -31 AND -1)",
            name="month_day_range",
        ),
        ForeignKeyConstraint(
            ["material_state_ref"],
            ["dante.routine_recurrence_calendar_state.material_state_ref"],
            name="fk_routine_recurrence_calendar_month_day_calendar_state",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
    )

    material_state_ref: Mapped[MaterialStateRef] = mapped_column(primary_key=True)
    month_day: Mapped[int] = mapped_column(SmallInteger, primary_key=True)


class RoutineRecurrenceCalendarOrdinalWeekdayRow(Base):
    """SQLAlchemy row mapping for ``dante.routine_recurrence_calendar_ordinal_weekday``."""

    __tablename__ = "routine_recurrence_calendar_ordinal_weekday"
    __table_args__ = (
        CheckConstraint(
            "weekday_number BETWEEN 1 AND 7",
            name="weekday_range",
        ),
        CheckConstraint(
            "ordinal BETWEEN -5 AND 5 AND ordinal <> 0",
            name="ordinal_range",
        ),
        ForeignKeyConstraint(
            ["material_state_ref"],
            ["dante.routine_recurrence_calendar_state.material_state_ref"],
            name="fk_routine_recurrence_calendar_ordinal_weekday_calendar_state",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
    )

    material_state_ref: Mapped[MaterialStateRef] = mapped_column(primary_key=True)
    weekday_number: Mapped[int] = mapped_column(SmallInteger, primary_key=True)
    ordinal: Mapped[int] = mapped_column(SmallInteger, primary_key=True)


class RoutineRecurrenceCalendarYearMonthDayRow(Base):
    """SQLAlchemy row mapping for ``dante.routine_recurrence_calendar_year_month_day``."""

    __tablename__ = "routine_recurrence_calendar_year_month_day"
    __table_args__ = (
        CheckConstraint(
            "month_number BETWEEN 1 AND 12",
            name="month_range",
        ),
        CheckConstraint(
            "(month_day BETWEEN 1 AND 31 OR month_day BETWEEN -31 AND -1)",
            name="month_day_range",
        ),
        ForeignKeyConstraint(
            ["material_state_ref"],
            ["dante.routine_recurrence_calendar_state.material_state_ref"],
            name="fk_routine_recurrence_calendar_year_month_day_calendar_state",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
    )

    material_state_ref: Mapped[MaterialStateRef] = mapped_column(primary_key=True)
    month_number: Mapped[int] = mapped_column(SmallInteger, primary_key=True)
    month_day: Mapped[int] = mapped_column(SmallInteger, primary_key=True)


class RoutineRecurrenceElapsedStateRow(Base):
    """SQLAlchemy row mapping for ``dante.routine_recurrence_elapsed_state``."""

    __tablename__ = "routine_recurrence_elapsed_state"
    __table_args__ = (
        CheckConstraint(
            "elapsed_seconds NOT IN ('NaN'::numeric,'Infinity'::numeric,'-Infinity'::numeric) AND elapsed_seconds > 0 AND elapsed_seconds = trunc(elapsed_seconds, 6)",
            name="elapsed_positive",
        ),
        CheckConstraint(
            "anchor_mode_code IN ('fixed_anchor','previous_expected')",
            name="anchor_mode",
        ),
        CheckConstraint(
            "isfinite(anchor_at)",
            name="anchor_at",
        ),
        ForeignKeyConstraint(
            ["material_state_ref"],
            ["dante.routine_recurrence_state.material_state_ref"],
            name="fk_routine_recurrence_elapsed_state_recurrence_state",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
    )

    material_state_ref: Mapped[MaterialStateRef] = mapped_column(primary_key=True)
    elapsed_seconds: Mapped[Decimal] = mapped_column(Numeric, nullable=False)
    anchor_mode_code: Mapped[str] = mapped_column(Text, nullable=False)
    anchor_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class RoutineRecurrenceQuotaStateRow(Base):
    """SQLAlchemy row mapping for ``dante.routine_recurrence_quota_state``."""

    __tablename__ = "routine_recurrence_quota_state"
    __table_args__ = (
        CheckConstraint(
            "quota_count > 0",
            name="quota_positive",
        ),
        CheckConstraint(
            "period_span > 0",
            name="period_span_positive",
        ),
        CheckConstraint(
            "period_unit_code IN ('day','week','month','year')",
            name="period_unit",
        ),
        CheckConstraint(
            "frame_code IN ('floating_local','named_zone','absolute_utc')",
            name="frame",
        ),
        CheckConstraint(
            "((frame_code='named_zone' AND zone_id IS NOT NULL) OR (frame_code IN ('floating_local','absolute_utc') AND zone_id IS NULL))",
            name="zone_basis",
        ),
        CheckConstraint(
            "((period_unit_code='week' AND week_start IS NOT NULL AND week_start BETWEEN 1 AND 7) OR (period_unit_code<>'week' AND week_start IS NULL))",
            name="week_start",
        ),
        ForeignKeyConstraint(
            ["material_state_ref"],
            ["dante.routine_recurrence_state.material_state_ref"],
            name="fk_routine_recurrence_quota_state_recurrence_state",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
    )

    material_state_ref: Mapped[MaterialStateRef] = mapped_column(primary_key=True)
    quota_count: Mapped[int] = mapped_column(Integer, nullable=False)
    period_unit_code: Mapped[str] = mapped_column(Text, nullable=False)
    period_span: Mapped[int] = mapped_column(Integer, nullable=False)
    frame_code: Mapped[str] = mapped_column(Text, nullable=False)
    zone_id: Mapped[str | None] = mapped_column(Text)
    week_start: Mapped[int | None] = mapped_column(SmallInteger)


class RoutineRecurrenceCyclicStateRow(Base):
    """SQLAlchemy row mapping for ``dante.routine_recurrence_cyclic_state``."""

    __tablename__ = "routine_recurrence_cyclic_state"
    __table_args__ = (
        CheckConstraint(
            "cycle_length > 0",
            name="cycle_length_positive",
        ),
        CheckConstraint(
            "position_unit_code IN ('day','week')",
            name="position_unit",
        ),
        ForeignKeyConstraint(
            ["material_state_ref"],
            ["dante.routine_recurrence_state.material_state_ref"],
            name="fk_routine_recurrence_cyclic_state_recurrence_state",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
    )

    material_state_ref: Mapped[MaterialStateRef] = mapped_column(primary_key=True)
    cycle_length: Mapped[int] = mapped_column(Integer, nullable=False)
    position_unit_code: Mapped[str] = mapped_column(Text, nullable=False)


class RoutineRecurrenceCyclePositionRow(Base):
    """SQLAlchemy row mapping for ``dante.routine_recurrence_cycle_position``."""

    __tablename__ = "routine_recurrence_cycle_position"
    __table_args__ = (
        CheckConstraint(
            "position_index >= 0",
            name="position_nonnegative",
        ),
        ForeignKeyConstraint(
            ["material_state_ref"],
            ["dante.routine_recurrence_cyclic_state.material_state_ref"],
            name="fk_routine_recurrence_cycle_position_cyclic_state",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
    )

    material_state_ref: Mapped[MaterialStateRef] = mapped_column(primary_key=True)
    position_index: Mapped[int] = mapped_column(Integer, primary_key=True)
    generates_expected: Mapped[bool] = mapped_column(Boolean, nullable=False)


class EventRecurrenceStateRow(Base):
    """SQLAlchemy row mapping for ``dante.event_recurrence_state``."""

    __tablename__ = "event_recurrence_state"
    __table_args__ = (
        CheckConstraint(
            "family_code IN ('calendar_wall_clock','elapsed_interval','quota_per_period','cyclic_positional')",
            name="family_code",
        ),
        CheckConstraint(
            "range_kind IN ('open','until_boundary','expected_count')",
            name="range_kind",
        ),
        CheckConstraint(
            "((range_kind='expected_count' AND expected_occurrence_count IS NOT NULL AND expected_occurrence_count > 0) OR (range_kind IN ('open','until_boundary') AND expected_occurrence_count IS NULL))",
            name="expected_count",
        ),
        ForeignKeyConstraint(
            ["material_state_ref"],
            ["dante.material_state_address.material_state_ref"],
            name="fk_event_recurrence_state_state_address",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        ForeignKeyConstraint(
            ["event_ref"],
            ["dante.event.event_ref"],
            name="fk_event_recurrence_state_event_ref_event",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        Index(
            "ix_event_recurrence_state_event_ref",
            "event_ref",
        ),
    )

    material_state_ref: Mapped[MaterialStateRef] = mapped_column(primary_key=True)
    event_ref: Mapped[NativeRef] = mapped_column(nullable=False)
    family_code: Mapped[str] = mapped_column(Text, nullable=False)
    range_kind: Mapped[str] = mapped_column(Text, nullable=False)
    expected_occurrence_count: Mapped[int | None] = mapped_column(Integer)


class EventRecurrenceCurrentHistoryRow(Base):
    """SQLAlchemy row mapping for ``dante.event_recurrence_current_history``."""

    __tablename__ = "event_recurrence_current_history"
    __table_args__ = (
        CheckConstraint(
            "isfinite(current_from_at) AND (current_until_at IS NULL OR (isfinite(current_until_at) AND current_until_at > current_from_at))",
            name="current_interval",
        ),
        ForeignKeyConstraint(
            ["event_ref"],
            ["dante.event.event_ref"],
            name="fk_event_recurrence_current_history_event_ref_event",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        ForeignKeyConstraint(
            ["material_state_ref"],
            ["dante.event_recurrence_state.material_state_ref"],
            name="fk_event_recurrence_current_history_recurrence_state",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        Index(
            "ux_event_recurrence_current_history_open",
            "event_ref",
            unique=True,
            postgresql_where=text("current_until_at IS NULL"),
        ),
        Index(
            "ix_event_recurrence_current_history_material_state_ref",
            "material_state_ref",
        ),
    )

    event_ref: Mapped[NativeRef] = mapped_column(primary_key=True)
    material_state_ref: Mapped[MaterialStateRef] = mapped_column(nullable=False)
    current_from_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), primary_key=True)
    current_until_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class EventRecurrenceBoundaryStateRow(Base):
    """SQLAlchemy row mapping for ``dante.event_recurrence_boundary_state``."""

    __tablename__ = "event_recurrence_boundary_state"
    __table_args__ = (
        CheckConstraint(
            "boundary_role IN ('pattern_anchor','effective_from','effective_until')",
            name="boundary_role",
        ),
        CheckConstraint(
            "boundary_kind IN ('date','floating_local','named_zone_local','absolute_instant')",
            name="boundary_kind",
        ),
        CheckConstraint(
            "((boundary_kind='date' AND date_value IS NOT NULL AND isfinite(date_value) AND local_value IS NULL AND zone_id IS NULL AND instant_value IS NULL AND resolved_at IS NULL) OR (boundary_kind='floating_local' AND local_value IS NOT NULL AND isfinite(local_value) AND date_value IS NULL AND zone_id IS NULL AND instant_value IS NULL AND resolved_at IS NULL) OR (boundary_kind='named_zone_local' AND local_value IS NOT NULL AND isfinite(local_value) AND zone_id IS NOT NULL AND date_value IS NULL AND instant_value IS NULL AND (resolved_at IS NULL OR isfinite(resolved_at))) OR (boundary_kind='absolute_instant' AND instant_value IS NOT NULL AND isfinite(instant_value) AND date_value IS NULL AND local_value IS NULL AND zone_id IS NULL AND resolved_at IS NULL))",
            name="boundary_payload",
        ),
        CheckConstraint(
            "((boundary_role='pattern_anchor' AND inclusive IS NULL) OR (boundary_role IN ('effective_from','effective_until') AND inclusive IS NOT NULL))",
            name="inclusive_role",
        ),
        ForeignKeyConstraint(
            ["material_state_ref"],
            ["dante.event_recurrence_state.material_state_ref"],
            name="fk_event_recurrence_boundary_state_recurrence_state",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
    )

    material_state_ref: Mapped[MaterialStateRef] = mapped_column(primary_key=True)
    boundary_role: Mapped[str] = mapped_column(Text, primary_key=True)
    boundary_kind: Mapped[str] = mapped_column(Text, nullable=False)
    inclusive: Mapped[bool | None] = mapped_column(Boolean)
    date_value: Mapped[date | None] = mapped_column(Date)
    local_value: Mapped[datetime | None] = mapped_column(DateTime(timezone=False))
    zone_id: Mapped[str | None] = mapped_column(Text)
    instant_value: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class EventRecurrenceCalendarStateRow(Base):
    """SQLAlchemy row mapping for ``dante.event_recurrence_calendar_state``."""

    __tablename__ = "event_recurrence_calendar_state"
    __table_args__ = (
        CheckConstraint(
            "pattern_code IN ('daily','weekly_weekdays','monthly_month_days','monthly_ordinal_weekdays','yearly_month_days','anchor_step')",
            name="pattern_code",
        ),
        CheckConstraint(
            "interval_count > 0",
            name="interval_positive",
        ),
        CheckConstraint(
            "clock_basis_code IN ('floating_local','named_zone','absolute_utc')",
            name="clock_basis",
        ),
        CheckConstraint(
            "((clock_basis_code='named_zone' AND zone_id IS NOT NULL) OR (clock_basis_code IN ('floating_local','absolute_utc') AND zone_id IS NULL))",
            name="zone_basis",
        ),
        CheckConstraint(
            "((pattern_code='anchor_step' AND step_unit_code IS NOT NULL AND step_unit_code IN ('day','week','month','year')) OR (pattern_code<>'anchor_step' AND step_unit_code IS NULL))",
            name="step_unit",
        ),
        ForeignKeyConstraint(
            ["material_state_ref"],
            ["dante.event_recurrence_state.material_state_ref"],
            name="fk_event_recurrence_calendar_state_recurrence_state",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
    )

    material_state_ref: Mapped[MaterialStateRef] = mapped_column(primary_key=True)
    pattern_code: Mapped[str] = mapped_column(Text, nullable=False)
    interval_count: Mapped[int] = mapped_column(Integer, nullable=False)
    clock_basis_code: Mapped[str] = mapped_column(Text, nullable=False)
    zone_id: Mapped[str | None] = mapped_column(Text)
    step_unit_code: Mapped[str | None] = mapped_column(Text)


class EventRecurrenceCalendarWallTimeRow(Base):
    """SQLAlchemy row mapping for ``dante.event_recurrence_calendar_wall_time``."""

    __tablename__ = "event_recurrence_calendar_wall_time"
    __table_args__ = (
        ForeignKeyConstraint(
            ["material_state_ref"],
            ["dante.event_recurrence_calendar_state.material_state_ref"],
            name="fk_event_recurrence_calendar_wall_time_calendar_state",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
    )

    material_state_ref: Mapped[MaterialStateRef] = mapped_column(primary_key=True)
    wall_time: Mapped[time] = mapped_column(Time(timezone=False), primary_key=True)


class EventRecurrenceCalendarWeekdayRow(Base):
    """SQLAlchemy row mapping for ``dante.event_recurrence_calendar_weekday``."""

    __tablename__ = "event_recurrence_calendar_weekday"
    __table_args__ = (
        CheckConstraint(
            "weekday_number BETWEEN 1 AND 7",
            name="weekday_range",
        ),
        ForeignKeyConstraint(
            ["material_state_ref"],
            ["dante.event_recurrence_calendar_state.material_state_ref"],
            name="fk_event_recurrence_calendar_weekday_calendar_state",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
    )

    material_state_ref: Mapped[MaterialStateRef] = mapped_column(primary_key=True)
    weekday_number: Mapped[int] = mapped_column(SmallInteger, primary_key=True)


class EventRecurrenceCalendarMonthDayRow(Base):
    """SQLAlchemy row mapping for ``dante.event_recurrence_calendar_month_day``."""

    __tablename__ = "event_recurrence_calendar_month_day"
    __table_args__ = (
        CheckConstraint(
            "(month_day BETWEEN 1 AND 31 OR month_day BETWEEN -31 AND -1)",
            name="month_day_range",
        ),
        ForeignKeyConstraint(
            ["material_state_ref"],
            ["dante.event_recurrence_calendar_state.material_state_ref"],
            name="fk_event_recurrence_calendar_month_day_calendar_state",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
    )

    material_state_ref: Mapped[MaterialStateRef] = mapped_column(primary_key=True)
    month_day: Mapped[int] = mapped_column(SmallInteger, primary_key=True)


class EventRecurrenceCalendarOrdinalWeekdayRow(Base):
    """SQLAlchemy row mapping for ``dante.event_recurrence_calendar_ordinal_weekday``."""

    __tablename__ = "event_recurrence_calendar_ordinal_weekday"
    __table_args__ = (
        CheckConstraint(
            "weekday_number BETWEEN 1 AND 7",
            name="weekday_range",
        ),
        CheckConstraint(
            "ordinal BETWEEN -5 AND 5 AND ordinal <> 0",
            name="ordinal_range",
        ),
        ForeignKeyConstraint(
            ["material_state_ref"],
            ["dante.event_recurrence_calendar_state.material_state_ref"],
            name="fk_event_recurrence_calendar_ordinal_weekday_calendar_state",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
    )

    material_state_ref: Mapped[MaterialStateRef] = mapped_column(primary_key=True)
    weekday_number: Mapped[int] = mapped_column(SmallInteger, primary_key=True)
    ordinal: Mapped[int] = mapped_column(SmallInteger, primary_key=True)


class EventRecurrenceCalendarYearMonthDayRow(Base):
    """SQLAlchemy row mapping for ``dante.event_recurrence_calendar_year_month_day``."""

    __tablename__ = "event_recurrence_calendar_year_month_day"
    __table_args__ = (
        CheckConstraint(
            "month_number BETWEEN 1 AND 12",
            name="month_range",
        ),
        CheckConstraint(
            "(month_day BETWEEN 1 AND 31 OR month_day BETWEEN -31 AND -1)",
            name="month_day_range",
        ),
        ForeignKeyConstraint(
            ["material_state_ref"],
            ["dante.event_recurrence_calendar_state.material_state_ref"],
            name="fk_event_recurrence_calendar_year_month_day_calendar_state",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
    )

    material_state_ref: Mapped[MaterialStateRef] = mapped_column(primary_key=True)
    month_number: Mapped[int] = mapped_column(SmallInteger, primary_key=True)
    month_day: Mapped[int] = mapped_column(SmallInteger, primary_key=True)


class EventRecurrenceElapsedStateRow(Base):
    """SQLAlchemy row mapping for ``dante.event_recurrence_elapsed_state``."""

    __tablename__ = "event_recurrence_elapsed_state"
    __table_args__ = (
        CheckConstraint(
            "elapsed_seconds NOT IN ('NaN'::numeric,'Infinity'::numeric,'-Infinity'::numeric) AND elapsed_seconds > 0 AND elapsed_seconds = trunc(elapsed_seconds, 6)",
            name="elapsed_positive",
        ),
        CheckConstraint(
            "anchor_mode_code IN ('fixed_anchor','previous_expected')",
            name="anchor_mode",
        ),
        CheckConstraint(
            "isfinite(anchor_at)",
            name="anchor_at",
        ),
        ForeignKeyConstraint(
            ["material_state_ref"],
            ["dante.event_recurrence_state.material_state_ref"],
            name="fk_event_recurrence_elapsed_state_recurrence_state",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
    )

    material_state_ref: Mapped[MaterialStateRef] = mapped_column(primary_key=True)
    elapsed_seconds: Mapped[Decimal] = mapped_column(Numeric, nullable=False)
    anchor_mode_code: Mapped[str] = mapped_column(Text, nullable=False)
    anchor_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class EventRecurrenceQuotaStateRow(Base):
    """SQLAlchemy row mapping for ``dante.event_recurrence_quota_state``."""

    __tablename__ = "event_recurrence_quota_state"
    __table_args__ = (
        CheckConstraint(
            "quota_count > 0",
            name="quota_positive",
        ),
        CheckConstraint(
            "period_span > 0",
            name="period_span_positive",
        ),
        CheckConstraint(
            "period_unit_code IN ('day','week','month','year')",
            name="period_unit",
        ),
        CheckConstraint(
            "frame_code IN ('floating_local','named_zone','absolute_utc')",
            name="frame",
        ),
        CheckConstraint(
            "((frame_code='named_zone' AND zone_id IS NOT NULL) OR (frame_code IN ('floating_local','absolute_utc') AND zone_id IS NULL))",
            name="zone_basis",
        ),
        CheckConstraint(
            "((period_unit_code='week' AND week_start IS NOT NULL AND week_start BETWEEN 1 AND 7) OR (period_unit_code<>'week' AND week_start IS NULL))",
            name="week_start",
        ),
        ForeignKeyConstraint(
            ["material_state_ref"],
            ["dante.event_recurrence_state.material_state_ref"],
            name="fk_event_recurrence_quota_state_recurrence_state",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
    )

    material_state_ref: Mapped[MaterialStateRef] = mapped_column(primary_key=True)
    quota_count: Mapped[int] = mapped_column(Integer, nullable=False)
    period_unit_code: Mapped[str] = mapped_column(Text, nullable=False)
    period_span: Mapped[int] = mapped_column(Integer, nullable=False)
    frame_code: Mapped[str] = mapped_column(Text, nullable=False)
    zone_id: Mapped[str | None] = mapped_column(Text)
    week_start: Mapped[int | None] = mapped_column(SmallInteger)


class EventRecurrenceCyclicStateRow(Base):
    """SQLAlchemy row mapping for ``dante.event_recurrence_cyclic_state``."""

    __tablename__ = "event_recurrence_cyclic_state"
    __table_args__ = (
        CheckConstraint(
            "cycle_length > 0",
            name="cycle_length_positive",
        ),
        CheckConstraint(
            "position_unit_code IN ('day','week')",
            name="position_unit",
        ),
        ForeignKeyConstraint(
            ["material_state_ref"],
            ["dante.event_recurrence_state.material_state_ref"],
            name="fk_event_recurrence_cyclic_state_recurrence_state",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
    )

    material_state_ref: Mapped[MaterialStateRef] = mapped_column(primary_key=True)
    cycle_length: Mapped[int] = mapped_column(Integer, nullable=False)
    position_unit_code: Mapped[str] = mapped_column(Text, nullable=False)


class EventRecurrenceCyclePositionRow(Base):
    """SQLAlchemy row mapping for ``dante.event_recurrence_cycle_position``."""

    __tablename__ = "event_recurrence_cycle_position"
    __table_args__ = (
        CheckConstraint(
            "position_index >= 0",
            name="position_nonnegative",
        ),
        ForeignKeyConstraint(
            ["material_state_ref"],
            ["dante.event_recurrence_cyclic_state.material_state_ref"],
            name="fk_event_recurrence_cycle_position_cyclic_state",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
    )

    material_state_ref: Mapped[MaterialStateRef] = mapped_column(primary_key=True)
    position_index: Mapped[int] = mapped_column(Integer, primary_key=True)
    generates_expected: Mapped[bool] = mapped_column(Boolean, nullable=False)
