"""B09 Responsibility and expected Participation relations plus authoring receipts."""

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


def _operation_constraints(subject: str) -> tuple[object, ...]:
    return (
        CheckConstraint(
            "operation_id=btrim(operation_id) AND operation_id<>'' "
            "AND char_length(operation_id)<=200",
            name="operation_id",
        ),
        CheckConstraint("intent_fingerprint ~ '^[0-9a-f]{64}$'", name="fingerprint"),
        ForeignKeyConstraint(
            ["self_person_ref"],
            ["dante.person.person_ref"],
            name=f"fk_{subject}_responsibility_op_self_person",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        ForeignKeyConstraint(
            [f"{subject}_ref"],
            [f"dante.{subject}.{subject}_ref"],
            name=f"fk_{subject}_responsibility_op_subject",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        ForeignKeyConstraint(
            ["responsible_person_ref"],
            ["dante.person.person_ref"],
            name=f"fk_{subject}_responsibility_op_person",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
    )


class ActivityResponsibilityOperationRow(Base):
    """Immutable receipt for one guarded Activity Responsibility authoring command."""

    __tablename__ = "activity_responsibility_operation"
    __table_args__ = _operation_constraints("activity")

    self_person_ref: Mapped[NativeRef] = mapped_column(primary_key=True)
    operation_id: Mapped[str] = mapped_column(Text, primary_key=True)
    intent_fingerprint: Mapped[str] = mapped_column(Text, nullable=False)
    activity_ref: Mapped[NativeRef] = mapped_column(nullable=False)
    responsible_person_ref: Mapped[NativeRef | None] = mapped_column()
    accepted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class EventResponsibilityOperationRow(Base):
    """Immutable receipt for one guarded Event Responsibility authoring command."""

    __tablename__ = "event_responsibility_operation"
    __table_args__ = _operation_constraints("event")

    self_person_ref: Mapped[NativeRef] = mapped_column(primary_key=True)
    operation_id: Mapped[str] = mapped_column(Text, primary_key=True)
    intent_fingerprint: Mapped[str] = mapped_column(Text, nullable=False)
    event_ref: Mapped[NativeRef] = mapped_column(nullable=False)
    responsible_person_ref: Mapped[NativeRef | None] = mapped_column()
    accepted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class EventExpectedParticipationOperationRow(Base):
    """Immutable receipt for one guarded expected Event Participation command."""

    __tablename__ = "event_expected_participation_operation"
    __table_args__ = (
        CheckConstraint(
            "operation_id=btrim(operation_id) AND operation_id<>'' "
            "AND char_length(operation_id)<=200",
            name="operation_id",
        ),
        CheckConstraint("intent_fingerprint ~ '^[0-9a-f]{64}$'", name="fingerprint"),
        CheckConstraint(
            "requirement_code IS NULL OR requirement_code IN ('required','optional')",
            name="requirement",
        ),
        ForeignKeyConstraint(
            ["self_person_ref"],
            ["dante.person.person_ref"],
            name="fk_event_expected_participation_op_self_person",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        ForeignKeyConstraint(
            ["event_ref"],
            ["dante.event.event_ref"],
            name="fk_event_expected_participation_op_event",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        ForeignKeyConstraint(
            ["participant_person_ref"],
            ["dante.person.person_ref"],
            name="fk_event_expected_participation_op_person",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
    )

    self_person_ref: Mapped[NativeRef] = mapped_column(primary_key=True)
    operation_id: Mapped[str] = mapped_column(Text, primary_key=True)
    intent_fingerprint: Mapped[str] = mapped_column(Text, nullable=False)
    event_ref: Mapped[NativeRef] = mapped_column(nullable=False)
    participant_person_ref: Mapped[NativeRef] = mapped_column(nullable=False)
    requirement_code: Mapped[str | None] = mapped_column(Text)
    accepted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
