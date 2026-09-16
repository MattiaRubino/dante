"""SQLAlchemy rows for the minimum B03-A Event persistence surface."""

from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, ForeignKeyConstraint, Index, Text
from sqlalchemy.orm import Mapped, mapped_column

from dante.platform.database.metadata import Base
from dante.platform.database.references import NativeRef


class EventExpectationRow(Base):
    """Initial durable expectation descriptor for one personal Event."""

    __tablename__ = "event_expectation"
    __table_args__ = (
        CheckConstraint(
            "title=btrim(title) AND title<>'' AND char_length(title)<=300",
            name="title",
        ),
        ForeignKeyConstraint(
            ["event_ref"],
            ["dante.event.event_ref"],
            name="fk_event_expectation_event_ref_event",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        ForeignKeyConstraint(
            ["self_person_ref"],
            ["dante.person.person_ref"],
            name="fk_event_expectation_self_person_ref_person",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        Index(
            "ix_event_expectation_self_person_created",
            "self_person_ref",
            "created_at",
            "event_ref",
        ),
    )

    event_ref: Mapped[NativeRef] = mapped_column(primary_key=True)
    self_person_ref: Mapped[NativeRef] = mapped_column(nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class EventCreateOperationRow(Base):
    """Idempotency receipt for one self-scoped CreateEvent operation."""

    __tablename__ = "event_create_operation"
    __table_args__ = (
        CheckConstraint(
            "operation_id=btrim(operation_id) AND operation_id<>'' "
            "AND char_length(operation_id)<=200",
            name="operation_id",
        ),
        CheckConstraint(
            "intent_fingerprint ~ '^[0-9a-f]{64}$'",
            name="fingerprint",
        ),
        ForeignKeyConstraint(
            ["self_person_ref"],
            ["dante.person.person_ref"],
            name="fk_event_create_operation_self_person_ref_person",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        ForeignKeyConstraint(
            ["event_ref"],
            ["dante.event.event_ref"],
            name="fk_event_create_operation_event_ref_event",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
    )

    self_person_ref: Mapped[NativeRef] = mapped_column(primary_key=True)
    operation_id: Mapped[str] = mapped_column(Text, primary_key=True)
    intent_fingerprint: Mapped[str] = mapped_column(Text, nullable=False)
    event_ref: Mapped[NativeRef] = mapped_column(nullable=False, unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
