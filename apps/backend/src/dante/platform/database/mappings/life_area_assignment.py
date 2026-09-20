"""B05-B typed actor-local primary Life Area relations and immutable receipts."""

from datetime import datetime
from uuid import UUID

from sqlalchemy import BigInteger, CheckConstraint, DateTime, ForeignKeyConstraint, Index, Text
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column

from dante.platform.database.metadata import Base
from dante.platform.database.references import NativeRef


class ActivityLifeAreaAssignmentRow(Base):
    """Current actor-local primary organizational location of one Activity."""

    __tablename__ = "activity_life_area_assignment"
    __table_args__ = (
        CheckConstraint("revision>=1", name="revision"),
        ForeignKeyConstraint(
            ["activity_ref"],
            ["dante.activity.activity_ref"],
            name="fk_activity_life_area_assignment_activity_ref_activity",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        ForeignKeyConstraint(
            ["self_person_ref"],
            ["dante.person.person_ref"],
            name="fk_activity_life_area_assignment_self_person_ref_person",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        ForeignKeyConstraint(
            ["life_area_ref"],
            ["dante.life_area.life_area_ref"],
            name="fk_activity_life_area_assignment_life_area_ref_life_area",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        Index(
            "ix_activity_life_area_assignment_self_person_life_area",
            "self_person_ref",
            "life_area_ref",
            "activity_ref",
        ),
    )

    self_person_ref: Mapped[NativeRef] = mapped_column(primary_key=True)
    activity_ref: Mapped[NativeRef] = mapped_column(primary_key=True)
    life_area_ref: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), nullable=False)
    revision: Mapped[int] = mapped_column(BigInteger, nullable=False)
    assigned_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class EventLifeAreaAssignmentRow(Base):
    """Current actor-local primary organizational location of one Event."""

    __tablename__ = "event_life_area_assignment"
    __table_args__ = (
        CheckConstraint("revision>=1", name="revision"),
        ForeignKeyConstraint(
            ["event_ref"],
            ["dante.event.event_ref"],
            name="fk_event_life_area_assignment_event_ref_event",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        ForeignKeyConstraint(
            ["self_person_ref"],
            ["dante.person.person_ref"],
            name="fk_event_life_area_assignment_self_person_ref_person",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        ForeignKeyConstraint(
            ["life_area_ref"],
            ["dante.life_area.life_area_ref"],
            name="fk_event_life_area_assignment_life_area_ref_life_area",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        Index(
            "ix_event_life_area_assignment_self_person_life_area",
            "self_person_ref",
            "life_area_ref",
            "event_ref",
        ),
    )

    self_person_ref: Mapped[NativeRef] = mapped_column(primary_key=True)
    event_ref: Mapped[NativeRef] = mapped_column(primary_key=True)
    life_area_ref: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), nullable=False)
    revision: Mapped[int] = mapped_column(BigInteger, nullable=False)
    assigned_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class ActivityLifeAreaAssignmentOperationRow(Base):
    """Immutable idempotency receipt and organizational history for an Activity move."""

    __tablename__ = "activity_life_area_assignment_operation"
    __table_args__ = (
        CheckConstraint(
            "operation_id=btrim(operation_id) AND operation_id<>'' AND char_length(operation_id)<=200",
            name="operation_id",
        ),
        CheckConstraint("intent_fingerprint ~ '^[0-9a-f]{64}$'", name="fingerprint"),
        CheckConstraint("expected_revision>=0", name="expected_revision"),
        CheckConstraint("accepted_revision=expected_revision+1", name="accepted_revision"),
        ForeignKeyConstraint(
            ["activity_ref"],
            ["dante.activity.activity_ref"],
            name="fk_activity_area_assignment_op_activity_ref_activity",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        ForeignKeyConstraint(
            ["self_person_ref"],
            ["dante.person.person_ref"],
            name="fk_activity_area_assignment_op_self_person_ref_person",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        ForeignKeyConstraint(
            ["life_area_ref"],
            ["dante.life_area.life_area_ref"],
            name="fk_activity_area_assignment_op_life_area_ref_life_area",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
    )

    self_person_ref: Mapped[NativeRef] = mapped_column(primary_key=True)
    operation_id: Mapped[str] = mapped_column(Text, primary_key=True)
    intent_fingerprint: Mapped[str] = mapped_column(Text, nullable=False)
    activity_ref: Mapped[NativeRef] = mapped_column(nullable=False)
    life_area_ref: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), nullable=False)
    expected_revision: Mapped[int] = mapped_column(BigInteger, nullable=False)
    accepted_revision: Mapped[int] = mapped_column(BigInteger, nullable=False)
    accepted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class EventLifeAreaAssignmentOperationRow(Base):
    """Immutable idempotency receipt and organizational history for an Event move."""

    __tablename__ = "event_life_area_assignment_operation"
    __table_args__ = (
        CheckConstraint(
            "operation_id=btrim(operation_id) AND operation_id<>'' AND char_length(operation_id)<=200",
            name="operation_id",
        ),
        CheckConstraint("intent_fingerprint ~ '^[0-9a-f]{64}$'", name="fingerprint"),
        CheckConstraint("expected_revision>=0", name="expected_revision"),
        CheckConstraint("accepted_revision=expected_revision+1", name="accepted_revision"),
        ForeignKeyConstraint(
            ["event_ref"],
            ["dante.event.event_ref"],
            name="fk_event_life_area_assignment_operation_event_ref_event",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        ForeignKeyConstraint(
            ["self_person_ref"],
            ["dante.person.person_ref"],
            name="fk_event_life_area_assignment_operation_self_person_ref_person",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        ForeignKeyConstraint(
            ["life_area_ref"],
            ["dante.life_area.life_area_ref"],
            name="fk_event_life_area_assignment_operation_life_area_ref_life_area",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
    )

    self_person_ref: Mapped[NativeRef] = mapped_column(primary_key=True)
    operation_id: Mapped[str] = mapped_column(Text, primary_key=True)
    intent_fingerprint: Mapped[str] = mapped_column(Text, nullable=False)
    event_ref: Mapped[NativeRef] = mapped_column(nullable=False)
    life_area_ref: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), nullable=False)
    expected_revision: Mapped[int] = mapped_column(BigInteger, nullable=False)
    accepted_revision: Mapped[int] = mapped_column(BigInteger, nullable=False)
    accepted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
