"""B09-A direct/current Responsibility and expected Participation relations."""

from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, ForeignKeyConstraint, Index, Text
from sqlalchemy.orm import Mapped, mapped_column

from dante.platform.database.metadata import Base
from dante.platform.database.references import NativeRef


class EventExpectedParticipationRow(Base):
    """Current expected/intended Person involvement in one Event."""

    __tablename__ = "event_expected_participation"
    __table_args__ = (
        CheckConstraint(
            "requirement_code IN ('required','optional')",
            name="requirement",
        ),
        ForeignKeyConstraint(
            ["event_ref"],
            ["dante.event.event_ref"],
            name="fk_event_expected_participation_event",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        ForeignKeyConstraint(
            ["participant_person_ref"],
            ["dante.person.person_ref"],
            name="fk_event_expected_participation_participant_person",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        Index(
            "ix_event_expected_participation_person_event",
            "participant_person_ref",
            "event_ref",
        ),
    )

    event_ref: Mapped[NativeRef] = mapped_column(primary_key=True)
    participant_person_ref: Mapped[NativeRef] = mapped_column(primary_key=True)
    requirement_code: Mapped[str] = mapped_column(Text, nullable=False)
    established_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class ActivityResponsibilityRow(Base):
    """Current single-holder Responsibility relation for one Activity."""

    __tablename__ = "activity_responsibility"
    __table_args__ = (
        ForeignKeyConstraint(
            ["activity_ref"],
            ["dante.activity.activity_ref"],
            name="fk_activity_responsibility_activity",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        ForeignKeyConstraint(
            ["responsible_person_ref"],
            ["dante.person.person_ref"],
            name="fk_activity_responsibility_person",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        Index(
            "ix_activity_responsibility_person_activity",
            "responsible_person_ref",
            "activity_ref",
        ),
    )

    activity_ref: Mapped[NativeRef] = mapped_column(primary_key=True)
    responsible_person_ref: Mapped[NativeRef] = mapped_column(nullable=False)
    established_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class EventResponsibilityRow(Base):
    """Current single-holder Responsibility relation for one Event."""

    __tablename__ = "event_responsibility"
    __table_args__ = (
        ForeignKeyConstraint(
            ["event_ref"],
            ["dante.event.event_ref"],
            name="fk_event_responsibility_event",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        ForeignKeyConstraint(
            ["responsible_person_ref"],
            ["dante.person.person_ref"],
            name="fk_event_responsibility_person",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        Index(
            "ix_event_responsibility_person_event",
            "responsible_person_ref",
            "event_ref",
        ),
    )

    event_ref: Mapped[NativeRef] = mapped_column(primary_key=True)
    responsible_person_ref: Mapped[NativeRef] = mapped_column(nullable=False)
    established_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
