"""SQLAlchemy rows for canonical B03 Event persistence."""

from datetime import datetime

from sqlalchemy import BigInteger, CheckConstraint, DateTime, ForeignKeyConstraint, Index, Integer, Text, text
from sqlalchemy.dialects.postgresql import ARRAY
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


class EventAgendaPartRow(Base):
    """Ordered Event-internal Agenda value; it is not a standalone identity owner."""

    __tablename__ = "event_agenda_part"
    __table_args__ = (
        CheckConstraint(
            "position >= 1 AND position <= 100",
            name="position",
        ),
        CheckConstraint(
            "content=btrim(content) AND content<>'' AND char_length(content)<=1000",
            name="content",
        ),
        ForeignKeyConstraint(
            ["event_ref"],
            ["dante.event_expectation.event_ref"],
            name="fk_event_agenda_part_event_ref_event_expectation",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
    )

    event_ref: Mapped[NativeRef] = mapped_column(primary_key=True)
    position: Mapped[int] = mapped_column(Integer, primary_key=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)


class EventAgendaCurrentRow(Base):
    """Aggregate CAS revision for the current ordered Agenda of one Event."""

    __tablename__ = "event_agenda_current"
    __table_args__ = (
        CheckConstraint("revision >= 1", name="revision"),
        ForeignKeyConstraint(
            ["event_ref"],
            ["dante.event_expectation.event_ref"],
            name="fk_event_agenda_current_event_ref_event_expectation",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
    )

    event_ref: Mapped[NativeRef] = mapped_column(primary_key=True)
    revision: Mapped[int] = mapped_column(BigInteger, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class EventAgendaMutationOperationRow(Base):
    """Idempotency receipt for one self-scoped whole-Agenda replacement."""

    __tablename__ = "event_agenda_mutation_operation"
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
        CheckConstraint("expected_revision >= 0", name="expected_revision"),
        CheckConstraint(
            "resulting_revision = expected_revision + 1",
            name="resulting_revision",
        ),
        CheckConstraint(
            "cardinality(accepted_agenda_parts) <= 100",
            name="accepted_agenda_parts",
        ),
        ForeignKeyConstraint(
            ["self_person_ref"],
            ["dante.person.person_ref"],
            name="fk_event_agenda_mutation_operation_self_person_ref_person",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        ForeignKeyConstraint(
            ["event_ref"],
            ["dante.event_expectation.event_ref"],
            name="fk_event_agenda_mutation_operation_event_ref_event_expectation",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
    )

    self_person_ref: Mapped[NativeRef] = mapped_column(primary_key=True)
    operation_id: Mapped[str] = mapped_column(Text, primary_key=True)
    intent_fingerprint: Mapped[str] = mapped_column(Text, nullable=False)
    event_ref: Mapped[NativeRef] = mapped_column(nullable=False)
    expected_revision: Mapped[int] = mapped_column(BigInteger, nullable=False)
    resulting_revision: Mapped[int] = mapped_column(BigInteger, nullable=False)
    accepted_agenda_parts: Mapped[list[str]] = mapped_column(ARRAY(Text), nullable=False)
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
        CheckConstraint(
            "cardinality(accepted_agenda_parts) <= 100",
            name="accepted_agenda_parts",
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
    accepted_agenda_parts: Mapped[list[str]] = mapped_column(
        ARRAY(Text),
        nullable=False,
        server_default=text("ARRAY[]::text[]"),
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
