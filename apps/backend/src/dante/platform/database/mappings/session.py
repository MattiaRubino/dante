"""SQLAlchemy row mappings for the Session timing/history family."""

from datetime import datetime
from decimal import Decimal

from sqlalchemy import CheckConstraint, DateTime, ForeignKeyConstraint, Index, Numeric, Text, text
from sqlalchemy.orm import Mapped, mapped_column

from dante.platform.database.metadata import Base
from dante.platform.database.references import MaterialStateRef, NativeRef


class SessionTimingStateRow(Base):
    """Session timing MaterialState envelope."""

    __tablename__ = "session_timing_state"
    __table_args__ = (
        CheckConstraint(
            "timing_form_code IN ('absolute','elapsed_only')",
            name="timing_form",
        ),
        ForeignKeyConstraint(
            ["material_state_ref"],
            ["dante.material_state_address.material_state_ref"],
            name="fk_session_timing_state_state_address",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        ForeignKeyConstraint(
            ["session_ref"],
            ["dante.session.session_ref"],
            name="fk_session_timing_state_session_ref_session",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        Index("ix_session_timing_state_session_ref", "session_ref"),
    )

    material_state_ref: Mapped[MaterialStateRef] = mapped_column(primary_key=True)
    session_ref: Mapped[NativeRef] = mapped_column(nullable=False)
    timing_form_code: Mapped[str] = mapped_column(Text, nullable=False)


class SessionTimingAbsoluteRow(Base):
    """Absolute Session timing payload."""

    __tablename__ = "session_timing_absolute"
    __table_args__ = (
        CheckConstraint(
            "start_precision_code IN ('exact','approximate','rounded') AND isfinite(started_at)",
            name="start_precision",
        ),
        CheckConstraint(
            "(ended_at IS NULL AND end_precision_code IS NULL) OR "
            "(ended_at IS NOT NULL AND end_precision_code IS NOT NULL "
            "AND isfinite(ended_at) "
            "AND end_precision_code IN ('exact','approximate','rounded'))",
            name="end_precision",
        ),
        CheckConstraint(
            "ended_at IS NULL OR ended_at > started_at",
            name="interval_order",
        ),
        ForeignKeyConstraint(
            ["material_state_ref"],
            ["dante.session_timing_state.material_state_ref"],
            name="fk_session_timing_absolute_timing_state",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
    )

    material_state_ref: Mapped[MaterialStateRef] = mapped_column(primary_key=True)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    start_precision_code: Mapped[str] = mapped_column(Text, nullable=False)
    ended_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    end_precision_code: Mapped[str | None] = mapped_column(Text)


class SessionTimingElapsedRow(Base):
    """Elapsed-only Session timing payload."""

    __tablename__ = "session_timing_elapsed"
    __table_args__ = (
        CheckConstraint(
            "elapsed_seconds NOT IN "
            "('NaN'::numeric,'Infinity'::numeric,'-Infinity'::numeric) "
            "AND elapsed_seconds > 0",
            name="elapsed_positive",
        ),
        CheckConstraint(
            "elapsed_precision_code IN ('exact','approximate','rounded')",
            name="elapsed_precision",
        ),
        ForeignKeyConstraint(
            ["material_state_ref"],
            ["dante.session_timing_state.material_state_ref"],
            name="fk_session_timing_elapsed_timing_state",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
    )

    material_state_ref: Mapped[MaterialStateRef] = mapped_column(primary_key=True)
    elapsed_seconds: Mapped[Decimal] = mapped_column(Numeric, nullable=False)
    elapsed_precision_code: Mapped[str] = mapped_column(Text, nullable=False)


class SessionTimingPauseRow(Base):
    """Pause interval within an absolute Session timing state."""

    __tablename__ = "session_timing_pause"
    __table_args__ = (
        CheckConstraint(
            "pause_precision_code IN ('exact','approximate','rounded') AND isfinite(paused_at)",
            name="pause_precision",
        ),
        CheckConstraint(
            "resume_precision_code IS NULL OR "
            "resume_precision_code IN ('exact','approximate','rounded')",
            name="resume_precision",
        ),
        CheckConstraint(
            "(resumed_at IS NULL AND resume_precision_code IS NULL) OR "
            "(resumed_at IS NOT NULL AND isfinite(resumed_at) "
            "AND resume_precision_code IS NOT NULL AND resumed_at > paused_at)",
            name="resume_pair",
        ),
        ForeignKeyConstraint(
            ["material_state_ref"],
            ["dante.session_timing_absolute.material_state_ref"],
            name="fk_session_timing_pause_timing_absolute",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        Index(
            "ux_session_timing_pause_open",
            "material_state_ref",
            unique=True,
            postgresql_where=text("resumed_at IS NULL"),
        ),
    )

    material_state_ref: Mapped[MaterialStateRef] = mapped_column(primary_key=True)
    paused_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), primary_key=True)
    pause_precision_code: Mapped[str] = mapped_column(Text, nullable=False)
    resumed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    resume_precision_code: Mapped[str | None] = mapped_column(Text)


class SessionTimingCurrentHistoryRow(Base):
    """Session timing currentness history."""

    __tablename__ = "session_timing_current_history"
    __table_args__ = (
        CheckConstraint(
            "isfinite(current_from_at) AND (current_until_at IS NULL OR "
            "(isfinite(current_until_at) AND current_until_at > current_from_at))",
            name="current_interval",
        ),
        ForeignKeyConstraint(
            ["session_ref"],
            ["dante.session.session_ref"],
            name="fk_session_timing_current_history_session_ref_session",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        ForeignKeyConstraint(
            ["material_state_ref"],
            ["dante.session_timing_state.material_state_ref"],
            name="fk_session_timing_current_history_timing_state",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        Index(
            "ux_session_timing_current_history_open",
            "session_ref",
            unique=True,
            postgresql_where=text("current_until_at IS NULL"),
        ),
        Index(
            "ix_session_timing_current_history_material_state_ref",
            "material_state_ref",
        ),
    )

    session_ref: Mapped[NativeRef] = mapped_column(primary_key=True)
    material_state_ref: Mapped[MaterialStateRef] = mapped_column(nullable=False)
    current_from_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), primary_key=True)
    current_until_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
