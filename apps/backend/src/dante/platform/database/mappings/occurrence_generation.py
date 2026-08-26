"""SQLAlchemy row mappings for CP6-M06 Occurrence generation."""

from datetime import date, datetime, time

from sqlalchemy import (
    CheckConstraint,
    Date,
    DateTime,
    ForeignKeyConstraint,
    Index,
    Integer,
    Text,
    Time,
)
from sqlalchemy.orm import Mapped, mapped_column

from dante.platform.database.metadata import Base
from dante.platform.database.references import MaterialStateRef, NativeRef


class OccurrenceGenerationRow(Base):
    """SQLAlchemy row mapping for ``dante.occurrence_generation``."""

    __tablename__ = "occurrence_generation"
    __table_args__ = (
        CheckConstraint(
            "origin_code IN ('recurrence_generated','explicit_extra')",
            name="origin_code",
        ),
        CheckConstraint(
            "((origin_code='recurrence_generated' AND governing_recurrence_state_ref IS NOT NULL) "
            "OR (origin_code='explicit_extra' AND governing_recurrence_state_ref IS NULL))",
            name="governing_state_pair",
        ),
        ForeignKeyConstraint(
            ["occurrence_ref"],
            ["dante.occurrence.occurrence_ref"],
            name="fk_occurrence_generation_occurrence_ref_occurrence",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        ForeignKeyConstraint(
            ["source_native_ref"],
            ["dante.native_address.native_ref"],
            name="fk_occurrence_generation_source_native_ref_native_address",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        ForeignKeyConstraint(
            ["governing_recurrence_state_ref"],
            ["dante.material_state_address.material_state_ref"],
            name="fk_occurrence_generation_state_address",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        Index(
            "ix_occurrence_generation_source_governing_state",
            "source_native_ref",
            "governing_recurrence_state_ref",
            "occurrence_ref",
        ),
        Index(
            "ix_occurrence_generation_governing_recurrence_state_ref",
            "governing_recurrence_state_ref",
        ),
    )

    occurrence_ref: Mapped[NativeRef] = mapped_column(primary_key=True)
    source_native_ref: Mapped[NativeRef] = mapped_column(nullable=False)
    governing_recurrence_state_ref: Mapped[MaterialStateRef | None] = mapped_column()
    origin_code: Mapped[str] = mapped_column(Text, nullable=False)


class OccurrenceGenerationCalendarRow(Base):
    """SQLAlchemy row mapping for ``dante.occurrence_generation_calendar``."""

    __tablename__ = "occurrence_generation_calendar"
    __table_args__ = (
        CheckConstraint(
            "clock_basis_code IN ('floating_local','named_zone','absolute_utc')",
            name="clock_basis",
        ),
        CheckConstraint(
            "((clock_basis_code='named_zone' AND zone_id IS NOT NULL) "
            "OR (clock_basis_code IN ('floating_local','absolute_utc') AND zone_id IS NULL))",
            name="zone_basis",
        ),
        CheckConstraint(
            "isfinite(generated_date) AND "
            "(resolved_at IS NULL OR (clock_basis_code='named_zone' AND isfinite(resolved_at)))",
            name="resolved_pair",
        ),
        ForeignKeyConstraint(
            ["occurrence_ref"],
            ["dante.occurrence_generation.occurrence_ref"],
            name="fk_occurrence_generation_calendar_generation",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
    )

    occurrence_ref: Mapped[NativeRef] = mapped_column(primary_key=True)
    generated_date: Mapped[date] = mapped_column(Date, nullable=False)
    generated_wall_time: Mapped[time | None] = mapped_column(Time(timezone=False))
    clock_basis_code: Mapped[str] = mapped_column(Text, nullable=False)
    zone_id: Mapped[str | None] = mapped_column(Text)
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class OccurrenceGenerationElapsedRow(Base):
    """SQLAlchemy row mapping for ``dante.occurrence_generation_elapsed``."""

    __tablename__ = "occurrence_generation_elapsed"
    __table_args__ = (
        CheckConstraint("isfinite(expected_at)", name="expected_at"),
        ForeignKeyConstraint(
            ["occurrence_ref"],
            ["dante.occurrence_generation.occurrence_ref"],
            name="fk_occurrence_generation_elapsed_generation",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
    )

    occurrence_ref: Mapped[NativeRef] = mapped_column(primary_key=True)
    expected_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class OccurrenceGenerationQuotaRow(Base):
    """SQLAlchemy row mapping for ``dante.occurrence_generation_quota``."""

    __tablename__ = "occurrence_generation_quota"
    __table_args__ = (
        CheckConstraint(
            "isfinite(period_start_date) AND isfinite(period_end_date_exclusive) "
            "AND period_end_date_exclusive > period_start_date",
            name="period_order",
        ),
        CheckConstraint(
            "frame_code IN ('floating_local','named_zone','absolute_utc')",
            name="frame",
        ),
        CheckConstraint(
            "((frame_code='named_zone' AND zone_id IS NOT NULL) "
            "OR (frame_code IN ('floating_local','absolute_utc') AND zone_id IS NULL))",
            name="zone_basis",
        ),
        ForeignKeyConstraint(
            ["occurrence_ref"],
            ["dante.occurrence_generation.occurrence_ref"],
            name="fk_occurrence_generation_quota_generation",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        Index(
            "ix_occurrence_generation_quota_period",
            "period_start_date",
            "period_end_date_exclusive",
            "occurrence_ref",
        ),
    )

    occurrence_ref: Mapped[NativeRef] = mapped_column(primary_key=True)
    period_start_date: Mapped[date] = mapped_column(Date, nullable=False)
    period_end_date_exclusive: Mapped[date] = mapped_column(Date, nullable=False)
    frame_code: Mapped[str] = mapped_column(Text, nullable=False)
    zone_id: Mapped[str | None] = mapped_column(Text)


class OccurrenceGenerationCyclicRow(Base):
    """SQLAlchemy row mapping for ``dante.occurrence_generation_cyclic``."""

    __tablename__ = "occurrence_generation_cyclic"
    __table_args__ = (
        CheckConstraint("isfinite(generated_date)", name="generated_date"),
        CheckConstraint("position_index >= 0", name="position_nonnegative"),
        ForeignKeyConstraint(
            ["occurrence_ref"],
            ["dante.occurrence_generation.occurrence_ref"],
            name="fk_occurrence_generation_cyclic_generation",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
    )

    occurrence_ref: Mapped[NativeRef] = mapped_column(primary_key=True)
    generated_date: Mapped[date] = mapped_column(Date, nullable=False)
    position_index: Mapped[int] = mapped_column(Integer, nullable=False)
